#!/usr/bin/env python3
"""Discover, recommend, and install Hermes Profile Packs.

Run with no arguments in a terminal for the interactive wizard. Existing
pack-first commands remain supported, for example::

    python install.py council --list
    python install.py agency agency-backend-engineer

For agents and scripts, use the non-interactive catalog/recommend/selection
flags together with --json where machine-readable output is useful.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
PACK_FILE = ROOT / "packs.json"
PACK_ALIASES = {
    "agency": "agency",
    "hermes-agency": "agency",
    "council": "council",
    "hermes-council": "council",
    "academy": "academy",
    "hermes-academy": "academy",
}
PACK_DISPLAY = {
    "agency": "Hermes Agency",
    "council": "Hermes Council",
    "academy": "Hermes Academy",
}
PACK_HINTS = {
    "agency": {
        "build", "work", "professional", "project", "software", "code", "coding",
        "develop", "development", "design", "product", "marketing", "business",
        "deploy", "devops", "engineering", "test", "qa", "content", "support",
    },
    "council": {
        "life", "personal", "health", "fitness", "parent", "parenting", "family",
        "relationship", "finance", "budget", "faith", "sleep", "home", "career",
        "travel", "nutrition", "stress", "time", "focus", "community", "recreation",
    },
    "academy": {
        "learn", "study", "teach", "teacher", "professor", "course", "class",
        "education", "practice", "understand", "school", "training", "lesson",
    },
}
QUERY_EXPANSIONS = {
    "api": {"backend", "integration", "web"},
    "web": {"frontend", "backend", "fullstack", "full-stack"},
    "website": {"frontend", "backend", "fullstack", "full-stack"},
    "app": {"application", "frontend", "backend"},
    "apps": {"application", "frontend", "backend"},
    "software": {"engineering", "architect", "developer"},
    "code": {"engineering", "developer", "programming"},
    "coding": {"engineering", "developer", "programming"},
    "developer": {"engineering", "programming"},
    "security": {"cybersecurity", "threat", "privacy", "secure"},
    "cyber": {"cybersecurity", "security", "threat"},
    "ai": {"mlops", "machine", "learning", "data"},
    "ml": {"mlops", "machine", "learning", "data"},
    "ui": {"ux", "frontend", "design", "interface"},
    "ux": {"ui", "design", "product"},
    "cloud": {"systems", "infrastructure", "devops", "reliability"},
    "ops": {"operations", "devops", "infrastructure", "reliability"},
    "sre": {"reliability", "site", "infrastructure"},
    "game": {"godot", "worldbuilder", "level", "game"},
    "games": {"godot", "worldbuilder", "level", "game"},
    "money": {"finance", "budget", "financial"},
    "finances": {"finance", "budget", "financial"},
    "parent": {"parenting", "family"},
    "kids": {"parenting", "family", "children"},
    "children": {"parenting", "family"},
    "workout": {"fitness", "movement", "training"},
    "exercise": {"fitness", "movement", "training"},
    "food": {"nutrition", "culinary", "meal"},
    "cooking": {"culinary", "food", "recipe"},
    "stress": {"resilience", "recovery", "coping"},
    "focus": {"attention", "time", "planning"},
    "religion": {"faith", "theology", "religious"},
    "christian": {"faith", "theology"},
    "math": {"mathematics", "quantitative"},
    "stats": {"statistics", "quantitative"},
    "car": {"automotive"},
    "cars": {"automotive"},
    "writing": {"writer", "rhetoric", "content"},
    "write": {"writer", "rhetoric", "content"},
    "research": {"research", "evidence", "methods"},
    "legal": {"law"},
    "law": {"legal"},
    "music": {"music"},
    "art": {"arts", "design", "creative"},
}
COORDINATION_TERMS = {
    "coordinate", "coordination", "orchestrate", "orchestrator", "steward", "dean",
    "team", "overview", "general", "everything", "whole", "manage", "management",
}
TOKEN_RE = re.compile(r"[a-z0-9]+")


class CLIError(ValueError):
    """User-facing CLI error."""


@dataclass(frozen=True)
class PackInfo:
    key: str
    name: str
    path: Path
    namespace: str
    manifest_path: Path
    purpose: str
    version: str
    orchestrator: str | None
    backbone: frozenset[str]
    categories: tuple[str, ...]
    profile_names: tuple[str, ...]


@dataclass(frozen=True)
class Profile:
    pack: str
    pack_name: str
    name: str
    display_name: str
    category: str
    description: str
    role: str
    jobs: tuple[str, ...]
    orchestrator: bool
    backbone: bool
    source_bytes: int

    def searchable_text(self) -> str:
        return " ".join(
            [
                self.name.replace("-", " "),
                self.display_name,
                self.category,
                self.description,
                self.role,
                *self.jobs,
            ]
        ).lower()

    def as_dict(self) -> dict:
        return {
            "pack": self.pack,
            "pack_name": self.pack_name,
            "name": self.name,
            "display_name": self.display_name,
            "category": self.category,
            "description": self.description,
            "role": self.role,
            "jobs": list(self.jobs),
            "orchestrator": self.orchestrator,
            "backbone": self.backbone,
            "estimated_source_bytes": self.source_bytes,
        }


def normalize_pack(value: str) -> str:
    try:
        return PACK_ALIASES[value.strip().lower()]
    except KeyError as exc:
        raise CLIError(f"unknown pack: {value}") from exc


def short_pack_name(name: str) -> str:
    if name.startswith("hermes-"):
        name = name[len("hermes-") :]
    return normalize_pack(name)


def _yaml_scalar(path: Path, key: str) -> str:
    if not path.is_file():
        return ""
    prefix = f"{key}:"
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith(prefix):
            continue
        value = line.split(":", 1)[1].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        return value.replace(r'\"', '"')
    return ""


def directory_size(path: Path) -> int:
    total = 0
    if not path.is_dir():
        return 0
    for child in path.rglob("*"):
        try:
            if child.is_file():
                total += child.stat().st_size
        except OSError:
            continue
    return total


def load_catalog(root: Path = ROOT) -> tuple[dict[str, PackInfo], list[Profile]]:
    pack_file = root / "packs.json"
    if not pack_file.is_file():
        raise CLIError(f"missing pack registry: {pack_file}")
    registry = json.loads(pack_file.read_text(encoding="utf-8"))

    packs: dict[str, PackInfo] = {}
    profiles: list[Profile] = []
    for record in registry.get("packs", []):
        key = short_pack_name(record["name"])
        pack_dir = root / record["path"]
        manifest_path = root / record["manifest"]
        if not manifest_path.is_file():
            raise CLIError(f"missing pack manifest: {record['manifest']}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_profiles = manifest.get("profiles", [])
        backbone = frozenset(manifest.get("backbone_profiles", []))
        orchestrator = manifest.get("orchestrator")
        categories = tuple(sorted({str(item.get("category", "other")) for item in manifest_profiles}))
        profile_names = tuple(str(item["name"]) for item in manifest_profiles)
        packs[key] = PackInfo(
            key=key,
            name=record["name"],
            path=pack_dir,
            namespace=record["namespace"],
            manifest_path=manifest_path,
            purpose=record.get("purpose", manifest.get("description", "")),
            version=str(manifest.get("version", "")),
            orchestrator=orchestrator,
            backbone=backbone,
            categories=categories,
            profile_names=profile_names,
        )
        for item in manifest_profiles:
            name = str(item["name"])
            source = pack_dir / "profiles" / name
            distribution = source / "distribution.yaml"
            description = str(item.get("description") or _yaml_scalar(distribution, "description"))
            role = str(item.get("role") or "")
            jobs = tuple(str(job) for job in item.get("jobs", []))
            profiles.append(
                Profile(
                    pack=key,
                    pack_name=record["name"],
                    name=name,
                    display_name=str(item.get("display_name") or name),
                    category=str(item.get("category") or "other"),
                    description=description,
                    role=role,
                    jobs=jobs,
                    orchestrator=name == orchestrator,
                    backbone=name in backbone,
                    source_bytes=directory_size(source),
                )
            )
    return packs, profiles


def tokenize(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def expanded_query(text: str) -> set[str]:
    tokens = tokenize(text)
    expanded = set(tokens)
    for token in tokens:
        expanded.update(QUERY_EXPANSIONS.get(token, set()))
    return expanded


def _profile_score(profile: Profile, query: str, query_tokens: set[str]) -> tuple[int, list[str]]:
    name_tokens = tokenize(profile.name.replace("-", " ") + " " + profile.display_name)
    category_tokens = tokenize(profile.category)
    job_tokens = tokenize(" ".join(profile.jobs))
    detail_tokens = tokenize(profile.description + " " + profile.role)

    score = 0
    reasons: list[str] = []

    name_hits = sorted(query_tokens & name_tokens)
    category_hits = sorted(query_tokens & category_tokens)
    job_hits = sorted(query_tokens & job_tokens)
    detail_hits = sorted(query_tokens & detail_tokens)

    score += len(name_hits) * 8
    score += len(category_hits) * 5
    score += len(job_hits) * 5
    score += len(detail_hits) * 3

    if name_hits:
        reasons.append("profile: " + ", ".join(name_hits[:3]))
    if category_hits:
        reasons.append("category: " + ", ".join(category_hits[:2]))
    if job_hits:
        reasons.append("capability: " + ", ".join(job_hits[:3]))
    if detail_hits:
        reasons.append("description: " + ", ".join(detail_hits[:3]))

    raw_query = " ".join(query.lower().split())
    searchable = profile.searchable_text()
    if raw_query and len(raw_query) >= 4 and raw_query in searchable:
        score += 14
        reasons.insert(0, "exact phrase match")

    pack_hits = sorted(tokenize(query) & PACK_HINTS.get(profile.pack, set()))
    if pack_hits:
        score += min(8, 2 * len(pack_hits))
        reasons.append(f"{PACK_DISPLAY[profile.pack]} intent")

    asks_for_coordination = bool(tokenize(query) & COORDINATION_TERMS)
    if profile.orchestrator:
        score += 9 if asks_for_coordination else -4
    if profile.backbone and not profile.orchestrator:
        score += 1

    return score, reasons


def recommend_profiles(
    profiles: Iterable[Profile],
    query: str,
    *,
    limit: int = 6,
    pack_filter: set[str] | None = None,
) -> list[tuple[Profile, int, list[str]]]:
    if not query.strip():
        raise CLIError("recommendation query cannot be empty")
    if limit < 1:
        raise CLIError("--limit must be at least 1")
    query_tokens = expanded_query(query)
    ranked: list[tuple[Profile, int, list[str]]] = []
    for profile in profiles:
        if pack_filter and profile.pack not in pack_filter:
            continue
        score, reasons = _profile_score(profile, query, query_tokens)
        if score > 0:
            ranked.append((profile, score, reasons))
    ranked.sort(
        key=lambda item: (
            -item[1],
            item[0].orchestrator,
            item[0].pack,
            item[0].category,
            item[0].name,
        )
    )
    return ranked[:limit]


def format_bytes(value: int) -> str:
    amount = float(value)
    units = ["B", "KiB", "MiB", "GiB"]
    unit = units[0]
    for unit in units:
        if amount < 1024.0 or unit == units[-1]:
            break
        amount /= 1024.0
    if unit == "B":
        return f"{int(amount)} {unit}"
    return f"{amount:.1f} {unit}"


def selected_stats(selected: Iterable[Profile], all_profiles: Iterable[Profile]) -> dict:
    selected_list = list(selected)
    all_list = list(all_profiles)
    selected_bytes = sum(profile.source_bytes for profile in selected_list)
    total_bytes = sum(profile.source_bytes for profile in all_list)
    by_pack: dict[str, int] = {}
    for profile in selected_list:
        by_pack[profile.pack] = by_pack.get(profile.pack, 0) + 1
    return {
        "selected_profiles": len(selected_list),
        "available_profiles": len(all_list),
        "skipped_profiles": max(0, len(all_list) - len(selected_list)),
        "estimated_source_bytes": selected_bytes,
        "estimated_source_bytes_skipped": max(0, total_bytes - selected_bytes),
        "by_pack": by_pack,
    }


def filter_packs(values: list[str] | None) -> set[str] | None:
    if not values:
        return None
    return {normalize_pack(value) for value in values}


def resolve_selection(
    profiles: list[Profile],
    *,
    explicit_names: list[str] | None,
    category_specs: list[str] | None,
    select_all: bool,
    pack_filter: set[str] | None,
) -> list[Profile]:
    by_name = {profile.name: profile for profile in profiles}
    chosen: dict[str, Profile] = {}

    if select_all:
        for profile in profiles:
            if not pack_filter or profile.pack in pack_filter:
                chosen[profile.name] = profile

    for name in explicit_names or []:
        for part in name.split(","):
            item = part.strip()
            if not item:
                continue
            profile = by_name.get(item)
            if not profile:
                raise CLIError(f"unknown profile: {item}")
            if pack_filter and profile.pack not in pack_filter:
                raise CLIError(f"profile {item} is outside the requested --pack filter")
            chosen[item] = profile

    for spec in category_specs or []:
        if ":" not in spec:
            raise CLIError("categories must use PACK:CATEGORY, for example agency:engineering")
        pack_value, category = spec.split(":", 1)
        pack = normalize_pack(pack_value)
        if pack_filter and pack not in pack_filter:
            raise CLIError(f"category {spec} is outside the requested --pack filter")
        matches = [profile for profile in profiles if profile.pack == pack and profile.category == category]
        if not matches:
            available = sorted({profile.category for profile in profiles if profile.pack == pack})
            raise CLIError(
                f"unknown category '{category}' for {pack}. Available: {', '.join(available)}"
            )
        for profile in matches:
            chosen[profile.name] = profile

    return sorted(chosen.values(), key=lambda profile: (profile.pack, profile.name))


def pack_installer(pack: PackInfo) -> Path:
    installer = pack.path / "install.py"
    if not installer.is_file():
        raise CLIError(f"missing installer for {pack.name}: {installer}")
    return installer


def install_selected(
    selected: list[Profile],
    packs: dict[str, PackInfo],
    *,
    force: bool,
    json_mode: bool,
) -> tuple[int, list[dict]]:
    grouped: dict[str, list[Profile]] = {}
    for profile in selected:
        grouped.setdefault(profile.pack, []).append(profile)

    results: list[dict] = []
    for pack_key in ("agency", "council", "academy"):
        members = grouped.get(pack_key)
        if not members:
            continue
        pack = packs[pack_key]
        command = [sys.executable, str(pack_installer(pack)), *[p.name for p in members]]
        if force:
            command.append("--force")
        if not json_mode:
            print(f"\n==> {PACK_DISPLAY[pack_key]}: {len(members)} profile(s)")
        completed = subprocess.run(
            command,
            text=True,
            capture_output=json_mode,
            check=False,
        )
        result = {
            "pack": pack_key,
            "profiles": [p.name for p in members],
            "returncode": completed.returncode,
        }
        if json_mode:
            result["stdout"] = completed.stdout
            result["stderr"] = completed.stderr
        results.append(result)
        if completed.returncode:
            return completed.returncode, results
    return 0, results


def print_pack_list(packs: dict[str, PackInfo], profiles: list[Profile]) -> None:
    counts = {key: 0 for key in packs}
    for profile in profiles:
        counts[profile.pack] = counts.get(profile.pack, 0) + 1
    for key in ("agency", "council", "academy"):
        if key not in packs:
            continue
        pack = packs[key]
        print(f"{key:<8} {pack.namespace:<11} {counts[key]:>3} profiles  {pack.purpose}")


def print_catalog(profiles: Iterable[Profile]) -> None:
    current: tuple[str, str] | None = None
    for profile in sorted(profiles, key=lambda p: (p.pack, p.category, p.name)):
        marker = (profile.pack, profile.category)
        if marker != current:
            print(f"\n{PACK_DISPLAY[profile.pack]} / {profile.category}")
            current = marker
        print(f"  {profile.name:<42} {profile.display_name}")


def _prompt(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt) as exc:
        print()
        raise CLIError("selection cancelled") from exc


def _parse_indices(value: str, count: int, *, blank_means_all: bool = False) -> list[int]:
    value = value.strip().lower()
    if not value:
        return list(range(count)) if blank_means_all else []
    if value in {"all", "a"}:
        return list(range(count))
    if value in {"none", "n"}:
        return []
    picked: set[int] = set()
    for chunk in value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            left, right = chunk.split("-", 1)
            try:
                start, end = int(left), int(right)
            except ValueError as exc:
                raise CLIError(f"invalid selection: {chunk}") from exc
            if start > end:
                start, end = end, start
            numbers = range(start, end + 1)
        else:
            try:
                numbers = [int(chunk)]
            except ValueError as exc:
                raise CLIError(f"invalid selection: {chunk}") from exc
        for number in numbers:
            if number < 1 or number > count:
                raise CLIError(f"selection {number} is outside 1-{count}")
            picked.add(number - 1)
    return sorted(picked)


def _choose_profiles(items: list[Profile], *, blank_means_all: bool = False) -> list[Profile]:
    for index, profile in enumerate(items, 1):
        description = profile.description or profile.role
        if len(description) > 96:
            description = description[:93].rstrip() + "..."
        print(f"  {index:>2}. {profile.display_name}  [{profile.name}]")
        if description:
            print(f"      {description}")
    suffix = " [Enter = all]" if blank_means_all else ""
    while True:
        value = _prompt(f"Select numbers (for example 1,3-5 or all){suffix}: ")
        try:
            indexes = _parse_indices(value, len(items), blank_means_all=blank_means_all)
            return [items[index] for index in indexes]
        except CLIError as exc:
            print(f"  {exc}")


def wizard_recommend(profiles: list[Profile]) -> list[Profile]:
    print("\nTell me what you want Hermes to help with.")
    print("Examples: 'build web apps', 'get my finances organized', 'learn cybersecurity'.")
    while True:
        query = _prompt("What do you need? ")
        try:
            ranked = recommend_profiles(profiles, query, limit=6)
        except CLIError as exc:
            print(f"  {exc}")
            continue
        if not ranked:
            print("I couldn't find a confident match. Try a few more concrete words, or browse instead.")
            continue
        print("\nSmallest useful matches I found:")
        for index, (profile, score, reasons) in enumerate(ranked, 1):
            why = "; ".join(reasons[:2]) or "catalog match"
            print(f"  {index}. {profile.display_name} ({PACK_DISPLAY[profile.pack]})")
            print(f"     {profile.name} · {why} · score {score}")
        chosen = _choose_profiles([item[0] for item in ranked], blank_means_all=True)
        if chosen:
            return chosen
        print("Nothing selected. Try another description or return to the main menu.")
        return []


def wizard_browse(packs: dict[str, PackInfo], profiles: list[Profile]) -> list[Profile]:
    pack_keys = [key for key in ("agency", "council", "academy") if key in packs]
    print("\nChoose a pack:")
    for index, key in enumerate(pack_keys, 1):
        count = sum(1 for profile in profiles if profile.pack == key)
        print(f"  {index}. {PACK_DISPLAY[key]} ({count} profiles) - {packs[key].purpose}")
    while True:
        value = _prompt("Pack number: ")
        try:
            indices = _parse_indices(value, len(pack_keys))
        except CLIError as exc:
            print(f"  {exc}")
            continue
        if len(indices) != 1:
            print("  Choose exactly one pack.")
            continue
        pack = pack_keys[indices[0]]
        break

    categories = list(packs[pack].categories)
    print(f"\n{PACK_DISPLAY[pack]} categories:")
    for index, category in enumerate(categories, 1):
        count = sum(1 for profile in profiles if profile.pack == pack and profile.category == category)
        print(f"  {index}. {category} ({count})")
    print("  all. Show the whole pack")
    while True:
        value = _prompt("Category number or all: ").lower()
        if value in {"all", "a"}:
            candidates = [profile for profile in profiles if profile.pack == pack]
            break
        try:
            indices = _parse_indices(value, len(categories))
        except CLIError as exc:
            print(f"  {exc}")
            continue
        if len(indices) != 1:
            print("  Choose exactly one category.")
            continue
        category = categories[indices[0]]
        candidates = [
            profile for profile in profiles if profile.pack == pack and profile.category == category
        ]
        break
    return _choose_profiles(sorted(candidates, key=lambda p: p.name))


def wizard_direct(profiles: list[Profile]) -> list[Profile]:
    query = _prompt("\nSearch profile names/descriptions: ")
    ranked = recommend_profiles(profiles, query, limit=20)
    if not ranked:
        print("No matching profiles found.")
        return []
    return _choose_profiles([item[0] for item in ranked])


def run_wizard(packs: dict[str, PackInfo], profiles: list[Profile], *, force: bool) -> int:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise CLIError("the interactive wizard requires a terminal; agents should use --agent-help")

    print("\nHermes Profile Packs 🪽")
    print("Pick only what helps. You can always add more later.")
    print(f"Catalog: {len(profiles)} profiles across {len(packs)} packs.\n")
    print("  1. Recommend a small set for me")
    print("  2. Browse packs and categories")
    print("  3. Search profiles directly")
    print("  4. Install everything")
    print("  5. Exit")

    selected: list[Profile]
    while True:
        choice = _prompt("Choose 1-5 [1]: ") or "1"
        if choice == "1":
            selected = wizard_recommend(profiles)
            if not selected:
                continue
            break
        if choice == "2":
            selected = wizard_browse(packs, profiles)
            if not selected:
                continue
            break
        if choice == "3":
            selected = wizard_direct(profiles)
            if not selected:
                continue
            break
        if choice == "4":
            selected = list(profiles)
            break
        if choice == "5":
            print("Nothing installed.")
            return 0
        print("Choose 1, 2, 3, 4, or 5.")

    stats = selected_stats(selected, profiles)
    print("\nInstall plan")
    for pack in ("agency", "council", "academy"):
        names = [p for p in selected if p.pack == pack]
        if names:
            print(f"  {PACK_DISPLAY[pack]}: {len(names)}")
            for profile in names:
                print(f"    - {profile.display_name} ({profile.name})")
    print(
        f"\nSelected {stats['selected_profiles']} of {stats['available_profiles']} profiles "
        f"(~{format_bytes(stats['estimated_source_bytes'])} source payload)."
    )
    if stats["skipped_profiles"]:
        print(
            f"Skipping {stats['skipped_profiles']} profiles "
            f"(~{format_bytes(stats['estimated_source_bytes_skipped'])} of catalog payload)."
        )
    answer = _prompt("Install this selection? [y/N]: ").lower()
    if answer not in {"y", "yes"}:
        print("Nothing installed.")
        return 0
    code, _ = install_selected(selected, packs, force=force, json_mode=False)
    return code


def legacy_delegate(argv: list[str]) -> int | None:
    if not argv or argv[0].startswith("-"):
        return None
    try:
        key = normalize_pack(argv[0])
    except CLIError:
        return None
    registry = json.loads(PACK_FILE.read_text(encoding="utf-8"))
    record = next(
        (item for item in registry.get("packs", []) if short_pack_name(item["name"]) == key),
        None,
    )
    if not record:
        raise CLIError(f"pack is registered but unavailable: {key}")
    installer = ROOT / record["path"] / "install.py"
    return subprocess.run([sys.executable, str(installer), *argv[1:]], check=False).returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Choose only the Hermes profiles you need, or install every pack.",
        epilog=(
            "Legacy pack commands still work: python install.py council --list. "
            "Run with no arguments in a terminal to launch the wizard."
        ),
    )
    parser.add_argument("--wizard", action="store_true", help="Launch the interactive selector.")
    parser.add_argument("--list-packs", action="store_true", help="List registered packs and exit.")
    parser.add_argument("--catalog", action="store_true", help="List the profile catalog and exit.")
    parser.add_argument("--recommend", metavar="TEXT", help="Recommend a small profile set for a goal and exit.")
    parser.add_argument("--agent-help", action="store_true", help="Print the non-interactive agent contract and exit.")
    parser.add_argument("--pack", action="append", help="Filter by pack; repeatable (agency, council, academy).")
    parser.add_argument("--profiles", nargs="+", help="Install explicit profile names. Comma-separated names also work.")
    parser.add_argument(
        "--category",
        action="append",
        metavar="PACK:CATEGORY",
        help="Install a category, for example agency:engineering. Repeatable.",
    )
    parser.add_argument("--all", action="store_true", help="Install all profiles, optionally limited by --pack.")
    parser.add_argument("--limit", type=int, default=6, help="Maximum recommendations (default: 6).")
    parser.add_argument("--dry-run", action="store_true", help="Print the install plan without changing Hermes.")
    parser.add_argument("--force", action="store_true", help="Re-apply selected distributions over existing profiles.")
    parser.add_argument("--yes", action="store_true", help="Approve a non-interactive install plan.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON. Never prompts.")
    return parser


def agent_help_payload() -> dict:
    return {
        "interactive": "python install.py",
        "catalog": "python install.py --catalog --json",
        "recommend": "python install.py --recommend 'build a web app' --json",
        "dry_run": "python install.py --profiles agency-backend-engineer agency-frontend-engineer --dry-run --json",
        "install_profiles": "python install.py --profiles agency-backend-engineer agency-frontend-engineer --yes --json",
        "install_category": "python install.py --category council:growth --yes --json",
        "install_everything": "python install.py --all --yes --json",
        "rules": [
            "--catalog and --recommend are read-only",
            "--json never prompts",
            "writes require --yes unless using the interactive wizard",
            "use --dry-run to inspect an exact install plan",
            "legacy pack-first commands remain supported",
        ],
    }


def emit_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    legacy = legacy_delegate(argv)
    if legacy is not None:
        return legacy

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        packs, profiles = load_catalog()
        pack_filter = filter_packs(args.pack)

        if not argv:
            return run_wizard(packs, profiles, force=False)
        if args.wizard:
            if args.json:
                raise CLIError("--wizard cannot be combined with --json")
            return run_wizard(packs, profiles, force=args.force)

        read_modes = sum(bool(value) for value in [args.list_packs, args.catalog, args.recommend, args.agent_help])
        if read_modes > 1:
            raise CLIError("choose only one of --list-packs, --catalog, --recommend, or --agent-help")
        if read_modes and (args.profiles or args.category or args.all or args.dry_run or args.yes):
            raise CLIError("read-only catalog/recommend modes cannot be combined with install-selection flags")

        filtered_profiles = [
            profile for profile in profiles if not pack_filter or profile.pack in pack_filter
        ]

        if args.agent_help:
            payload = agent_help_payload()
            if args.json:
                emit_json(payload)
            else:
                print("Agent/script usage (non-interactive):")
                for key, value in payload.items():
                    if key == "rules":
                        print("\nRules:")
                        for rule in value:
                            print(f"  - {rule}")
                    else:
                        print(f"  {key:<18} {value}")
            return 0

        if args.list_packs:
            if args.json:
                emit_json(
                    {
                        "packs": [
                            {
                                "key": key,
                                "name": packs[key].name,
                                "namespace": packs[key].namespace,
                                "purpose": packs[key].purpose,
                                "profile_count": sum(1 for p in profiles if p.pack == key),
                                "version": packs[key].version,
                            }
                            for key in ("agency", "council", "academy")
                            if key in packs and (not pack_filter or key in pack_filter)
                        ]
                    }
                )
            else:
                print_pack_list(
                    {key: value for key, value in packs.items() if not pack_filter or key in pack_filter},
                    filtered_profiles,
                )
            return 0

        if args.catalog:
            if args.json:
                emit_json(
                    {
                        "profile_count": len(filtered_profiles),
                        "profiles": [profile.as_dict() for profile in filtered_profiles],
                    }
                )
            else:
                print_catalog(filtered_profiles)
            return 0

        if args.recommend is not None:
            ranked = recommend_profiles(
                profiles,
                args.recommend,
                limit=args.limit,
                pack_filter=pack_filter,
            )
            if args.json:
                emit_json(
                    {
                        "query": args.recommend,
                        "limit": args.limit,
                        "recommendation_count": len(ranked),
                        "recommendations": [
                            {**profile.as_dict(), "score": score, "reasons": reasons}
                            for profile, score, reasons in ranked
                        ],
                    }
                )
            else:
                if not ranked:
                    print("No confident recommendations found.")
                    return 0
                print(f"Recommended for: {args.recommend}")
                for profile, score, reasons in ranked:
                    why = "; ".join(reasons[:3]) or "catalog match"
                    print(f"  {profile.name:<42} {profile.display_name}  score={score}")
                    print(f"    {why}")
            return 0

        selected = resolve_selection(
            profiles,
            explicit_names=args.profiles,
            category_specs=args.category,
            select_all=args.all,
            pack_filter=pack_filter,
        )
        if not selected:
            raise CLIError(
                "no profiles selected. Use the wizard, --profiles, --category, --all, --catalog, or --recommend."
            )

        stats = selected_stats(selected, profiles)
        plan = {
            "status": "plan",
            "profiles": [profile.name for profile in selected],
            "stats": stats,
        }
        if args.dry_run:
            if args.json:
                emit_json(plan)
            else:
                print(f"Would install {stats['selected_profiles']} profile(s):")
                for profile in selected:
                    print(f"  - {profile.name}")
                print(
                    f"Estimated source payload: {format_bytes(stats['estimated_source_bytes'])}; "
                    f"skipping {stats['skipped_profiles']} profile(s)."
                )
            return 0

        if not args.yes:
            if args.json or not (sys.stdin.isatty() and sys.stdout.isatty()):
                raise CLIError("installation requires --yes in non-interactive mode; use --dry-run first if desired")
            print(f"Install {len(selected)} selected profile(s)?")
            answer = _prompt("Continue? [y/N]: ").lower()
            if answer not in {"y", "yes"}:
                print("Nothing installed.")
                return 0

        code, results = install_selected(selected, packs, force=args.force, json_mode=args.json)
        if args.json:
            emit_json(
                {
                    "status": "ok" if code == 0 else "error",
                    "returncode": code,
                    "profiles": [profile.name for profile in selected],
                    "stats": stats,
                    "packs": results,
                }
            )
        elif code == 0:
            print(f"\nInstalled {len(selected)} selected Hermes profile(s).")
        return code

    except CLIError as exc:
        if "args" in locals() and getattr(args, "json", False):
            print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2
    except (json.JSONDecodeError, OSError) as exc:
        if "args" in locals() and getattr(args, "json", False):
            print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
