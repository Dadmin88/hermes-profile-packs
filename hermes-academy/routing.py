"""Deterministic Academy Dean routing policy for profile learners.

This module is the repository-level reference implementation used by tests and
maintainers. The installed Dean follows the same policy from its preloaded
``faculty-routing`` skill; runtime profile-to-profile teaching does not depend
on this pack-root Python file being present.

Public API:
    route_learner(
        learner_profile,
        objective,
        manifest_path=None,
        installed_profiles=None,
    )
    minimize_learner_context(learner_profile, role, objective, skills=None)
"""
from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

MANIFEST = Path(__file__).resolve().parent / "academy.json"


@dataclass(frozen=True)
class RoutingResult:
    """Outcome of a routing decision."""

    faculty: Optional[str]
    approximate: bool
    reason: str


@dataclass(frozen=True)
class LearnerContext:
    """Minimized context passed to a faculty member about the learner."""

    learner_profile: str
    role: str
    objective: str
    relevant_skills: tuple[str, ...]


# Common natural-language terms that indicate each specialist-preference key.
TOPIC_KEYWORDS: dict[str, list[str]] = {
    "physics": [
        "physics", "mechanics", "thermodynamics", "kinematics", "dynamics",
        "newton", "momentum", "energy", "waves", "optics", "electromagnetism",
        "quantum", "relativity", "gravitation", "force", "velocity",
        "acceleration", "inertia",
    ],
    "chemistry": [
        "chemistry", "chemical", "bonding", "molecular", "stoichiometry",
        "reaction", "compound", "element", "atom", "organic chemistry",
        "inorganic", "periodic table", "solution", "acid", "base",
    ],
    "biology": [
        "biology", "biological", "cell", "genetics", "evolution", "ecology",
        "physiology", "organism", "dna", "rna", "protein", "metabolism",
        "photosynthesis", "respiration",
    ],
    "statistics": [
        "statistics", "statistical", "probability", "hypothesis testing",
        "regression", "distribution", "sampling", "confidence interval",
        "p-value", "bayesian", "inference",
    ],
    "data-science": [
        "data science", "data analysis", "machine learning", "modeling",
        "feature engineering", "data pipeline", "predictive",
        "database", "query optimization", "indexing",
    ],
    "philosophy": [
        "philosophy", "philosophical", "ethics", "moral", "logic",
        "epistemology", "metaphysics", "ontology", "aesthetics",
        "existentialism", "phenomenology",
    ],
    "law-and-legal-studies": [
        "law", "legal", "constitutional", "contract", "tort",
        "jurisprudence", "litigation", "statute", "regulation",
    ],
    "theology-and-religious-studies": [
        "theology", "religious", "doctrine", "scripture", "faith",
        "spirituality", "church", "mosque", "temple", "sacred",
    ],
    "education-and-pedagogy": [
        "pedagogy", "teaching", "instruction", "curriculum", "assessment",
        "learning science", "educational", "classroom",
    ],
    "cybersecurity": [
        "cybersecurity", "security", "threat model", "threat modeling",
        "vulnerability", "penetration", "firewall", "encryption",
        "authentication", "authorization", "incident response",
    ],
    "cloud-and-systems": [
        "cloud", "infrastructure", "distributed systems", "kubernetes",
        "docker", "aws", "azure", "gcp", "devops", "site reliability",
        "microservices", "container",
    ],
    "project-management": [
        "project management", "agile", "scrum", "kanban", "sprint",
        "backlog", "stakeholder", "milestone", "gantt", "waterfall",
    ],
    "automotive": [
        "automotive", "engine", "transmission", "brake", "suspension",
        "diagnostic", "obd", "vehicle", "mechanic", "torque",
    ],
    "culinary-arts": [
        "culinary", "cooking", "baking", "recipe", "kitchen",
        "gastronomy", "food safety", "cuisine", "chef",
    ],
    "music": [
        "music", "musical", "rhythm", "melody", "harmony", "chord",
        "scale", "composition", "ear training", "instrument",
    ],
}

# A single hit on one of these words is context, not enough evidence for a
# confident specialist route. Two related ambiguous hits, or one distinctive
# term/phrase, can still be sufficient.
AMBIGUOUS_SINGLE_KEYWORDS = {
    "dynamics", "momentum", "energy", "waves", "force",
    "bonding", "reaction", "compound", "element", "solution", "acid", "base",
    "cell", "regression", "distribution", "inference", "modeling",
    "ethics", "moral", "logic", "aesthetics", "contract", "regulation",
    "faith", "church", "temple", "sacred", "teaching", "instruction",
    "assessment", "classroom", "security", "infrastructure", "container",
    "engine", "transmission", "diagnostic", "torque", "scale", "composition",
    "instrument",
}

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "me",
    "i", "my", "your", "our", "their", "its", "it", "this", "that",
    "these", "those", "some", "any", "no", "not", "so", "very", "too",
    "just", "about", "how", "what", "which", "who", "when", "where",
    "why", "if", "then", "than", "also", "more", "most", "other",
    "into", "over", "after", "before", "between", "under", "again",
}


def _load_manifest(path: Optional[Path] = None) -> dict:
    target = path or MANIFEST
    return json.loads(target.read_text(encoding="utf-8"))


def _profile_names(manifest: dict) -> set[str]:
    return {p["name"] for p in manifest["profiles"]}


def _profile_by_name(manifest: dict) -> dict[str, dict]:
    return {p["name"]: p for p in manifest["profiles"]}


def _topic_scores(objective: str, manifest: dict) -> dict[str, int]:
    """Score manifest-declared specialist topics against an objective."""
    objective_lower = objective.lower()
    prefs = manifest.get("routing", {}).get("specialist_preferences", {})
    scores: dict[str, int] = {}

    for topic_key in prefs:
        keywords = TOPIC_KEYWORDS.get(topic_key, [topic_key.replace("-", " ")])
        score = 0
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if not re.search(pattern, objective_lower):
                continue
            word_count = len(keyword.split())
            if word_count > 1:
                score += word_count + 1
            elif keyword in AMBIGUOUS_SINGLE_KEYWORDS:
                score += 1
            else:
                score += 2
        if score:
            scores[topic_key] = score

    return scores


def _word_tokens(text: str) -> set[str]:
    """Return normalized word tokens for safe role-description matching."""
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text.lower()))


def route_learner(
    learner_profile: str,
    objective: str,
    manifest_path: Optional[Path] = None,
    installed_profiles: Optional[Iterable[str]] = None,
) -> RoutingResult:
    """Route a profile learner to the safest, most specific Academy faculty.

    ``installed_profiles`` may be supplied by callers that know the current Bot
    roster. When omitted, the manifest roster is treated as available, which is
    useful for repository validation and policy tests.
    """
    del learner_profile  # Identity is part of the contract, not a routing weight.

    manifest = _load_manifest(manifest_path)
    catalog = _profile_names(manifest)
    profiles = _profile_by_name(manifest)
    routing = manifest.get("routing", {})
    prefs = routing.get("specialist_preferences", {})
    category_fallbacks = routing.get("category_fallbacks", {})

    if installed_profiles is None:
        installed = set(catalog)
    else:
        installed = {str(name) for name in installed_profiles if str(name) in catalog}

    # 1. Prefer a clear specialist match.
    scores = _topic_scores(objective, manifest)
    strong_topics = [topic for topic in prefs if scores.get(topic, 0) >= 2]

    # 2. If several specialties are clearly present, only use a broad fallback
    # when all of them belong to one Academy category. Cross-category requests
    # are too broad for the one-objective/one-instructor CE contract.
    if len(strong_topics) > 1:
        categories = {
            profiles[prefs[topic]].get("category", "")
            for topic in strong_topics
            if prefs[topic] in profiles
        }
        if len(categories) == 1:
            category = next(iter(categories))
            fallback = category_fallbacks.get(category)
            if fallback and fallback in installed:
                return RoutingResult(
                    faculty=fallback,
                    approximate=True,
                    reason=(
                        f"Objective spans multiple '{category}' specialties; "
                        f"routing to broad faculty '{fallback}'."
                    ),
                )
        return RoutingResult(
            faculty=None,
            approximate=False,
            reason=(
                "Objective spans multiple Academy domains without one safe "
                "installed broad faculty match; narrow the competency or choose "
                "an instructor."
            ),
        )

    if len(strong_topics) == 1:
        topic = strong_topics[0]
        specialist = prefs[topic]
        if specialist in installed:
            return RoutingResult(
                faculty=specialist,
                approximate=False,
                reason=f"Direct specialist match for '{topic}'.",
            )

        # The topic is clear but its specialist is unavailable. Fall back only
        # to the installed broad representative for that specialist's category.
        profile = profiles.get(specialist)
        if profile:
            category = profile.get("category", "")
            fallback = category_fallbacks.get(category)
            if fallback and fallback in installed:
                return RoutingResult(
                    faculty=fallback,
                    approximate=True,
                    reason=(
                        f"Specialist '{specialist}' is not installed; falling back "
                        f"to category broad faculty '{fallback}'."
                    ),
                )

    # 3. Role-description scan for objectives without a clear specialist match.
    # Only installed profiles participate, and exact normalized word overlap is
    # used instead of substring matching.
    objective_words = _word_tokens(objective) - STOP_WORDS
    best_score = 0
    best_profiles: list[str] = []
    for profile in manifest["profiles"]:
        if profile["name"] not in installed:
            continue
        role_words = _word_tokens(profile.get("role", ""))
        score = len(objective_words & role_words)
        if score > best_score:
            best_score = score
            best_profiles = [profile["name"]]
        elif score == best_score and score > 0:
            best_profiles.append(profile["name"])

    # One shared word is too weak for a safe approximate route. A tie at the
    # accepted threshold also fails closed rather than depending on manifest
    # order or Python iteration details.
    if best_score >= 2 and len(best_profiles) == 1:
        best = best_profiles[0]
        return RoutingResult(
            faculty=best,
            approximate=True,
            reason=(
                f"No specialist matched; closest installed role-description "
                f"match is '{best}'."
            ),
        )

    if best_score >= 2 and len(best_profiles) > 1:
        return RoutingResult(
            faculty=None,
            approximate=False,
            reason=(
                "No specialist matched and multiple installed faculty are equally "
                "close; narrow the competency or choose an instructor."
            ),
        )

    return RoutingResult(
        faculty=None,
        approximate=False,
        reason="No installed Academy faculty member safely matches this objective.",
    )


def minimize_learner_context(
    learner_profile: str,
    role: str,
    objective: str,
    skills: Optional[list[str]] = None,
) -> LearnerContext:
    """Build the bounded learner context needed for a faculty handoff."""
    return LearnerContext(
        learner_profile=learner_profile,
        role=role,
        objective=objective,
        relevant_skills=tuple(skills) if skills else (),
    )
