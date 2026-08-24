"""Deterministic Academy Dean routing for profile learners.

Routes a profile learner (name, role, objective) to the most specific
installed Academy faculty member using the academy.json manifest as
authority. Never invents a profile that does not exist in the catalog.

Public API:
    route_learner(learner_profile, objective, manifest_path=None)
    minimize_learner_context(learner_profile, role, objective, skills=None)
"""
from __future__ import annotations

import json
import re
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


# ---------------------------------------------------------------------------
# Category mapping: manifest category -> broad fallback profile
# ---------------------------------------------------------------------------
CATEGORY_BROAD_FALLBACK: dict[str, str] = {
    "quantitative": "academy-mathematics-professor",
    "communication": "academy-writing-rhetoric-professor",
    "science": "academy-natural-sciences-professor",
    "technology": "academy-computer-science-professor",
    "humanities": "academy-history-professor",
    "social-sciences": "academy-social-sciences-professor",
    "professional": "academy-business-professor",
    "languages": "academy-language-instructor",
    "research": "academy-research-methods-professor",
    "vocational": "academy-skilled-trades-instructor",
    "health-sciences": "academy-health-sciences-professor",
    "creative": "academy-arts-design-instructor",
}

# ---------------------------------------------------------------------------
# Keyword expansion: maps common related terms to specialist_preferences keys.
# Each entry lists words/phrases that, when found in the objective, indicate
# the corresponding topic. The topic key itself is always implied.
# ---------------------------------------------------------------------------
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

# Single words in this set are useful evidence only in context. They are too
# ambiguous to justify a confident specialist route by themselves. Two or
# more hits in the same topic, or one distinctive/multi-word keyword, may
# still produce a specialist match.
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
    """Score manifest-declared specialist topics against an objective.

    The supplied manifest is authoritative. This matters for validators and
    callers that intentionally route against an alternate manifest rather
    than the repository default.
    """
    objective_lower = objective.lower()
    prefs = manifest.get("routing", {}).get("specialist_preferences", {})
    scores: dict[str, int] = {}

    for topic_key in prefs:
        keywords = TOPIC_KEYWORDS.get(topic_key, [topic_key.replace("-", " ")])
        score = 0
        for kw in keywords:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if not re.search(pattern, objective_lower):
                continue
            word_count = len(kw.split())
            if word_count > 1:
                # Phrases are strong evidence and outrank single words.
                score += word_count + 1
            elif kw in AMBIGUOUS_SINGLE_KEYWORDS:
                # One ambiguous word is context, not a confident route.
                score += 1
            else:
                # Distinctive domain terms may route confidently alone.
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
) -> RoutingResult:
    """Route a profile learner to the best Academy faculty member.

    Parameters
    ----------
    learner_profile : str
        Name of the requesting profile (e.g. "agency-backend-engineer").
    objective : str
        One-line learning objective.
    manifest_path : Path, optional
        Override manifest location (defaults to academy.json).

    Returns
    -------
    RoutingResult
        faculty: profile name or None if no safe match exists.
        approximate: True when the match is a broad fallback, not a specialist.
        reason: human-readable explanation of the routing decision.
    """
    manifest = _load_manifest(manifest_path)
    installed = _profile_names(manifest)
    profiles = _profile_by_name(manifest)
    prefs = manifest.get("routing", {}).get("specialist_preferences", {})

    # 1. Score specialist topics using only the selected manifest.
    scores = _topic_scores(objective, manifest)
    strong_topics = [topic for topic in prefs if scores.get(topic, 0) >= 2]

    if len(strong_topics) > 1:
        # A single CE event has one bounded objective and one instructor. If
        # several strong topics live in the same Academy category, route to
        # that category's broad faculty. If they cross category boundaries,
        # fail closed and ask the learner/user to narrow the competency rather
        # than arbitrarily choosing an unrelated "broad chair".
        categories = {
            profiles[prefs[topic]].get("category", "")
            for topic in strong_topics
            if prefs[topic] in profiles
        }
        if len(categories) == 1:
            category = next(iter(categories))
            fallback = CATEGORY_BROAD_FALLBACK.get(category)
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
                "broad faculty match; narrow the competency or choose an instructor."
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

        profile = profiles.get(specialist)
        if profile:
            category = profile.get("category", "")
            fallback = CATEGORY_BROAD_FALLBACK.get(category)
            if fallback and fallback in installed:
                return RoutingResult(
                    faculty=fallback,
                    approximate=True,
                    reason=(
                        f"Specialist '{specialist}' not installed; "
                        f"falling back to category broad faculty '{fallback}'."
                    ),
                )

    # 2. Role-description scan for requests without a clear specialist match.
    objective_words = _word_tokens(objective) - STOP_WORDS
    best_score = 0
    best_profiles: list[str] = []
    for profile in manifest["profiles"]:
        role_words = _word_tokens(profile.get("role", ""))
        score = len(objective_words & role_words)
        if score > best_score:
            best_score = score
            best_profiles = [profile["name"]]
        elif score == best_score and score > 0:
            best_profiles.append(profile["name"])

    # A single shared word is too weak for a safe approximate route. Requiring
    # at least two exact token hits prevents cases such as "base jumping" or
    # "fashion modeling" from being sent to an unrelated faculty member.
    if best_score >= 2 and len(best_profiles) == 1:
        best = best_profiles[0]
        return RoutingResult(
            faculty=best,
            approximate=True,
            reason=(
                f"No specialist matched; closest role-description match is '{best}'."
            ),
        )

    if best_score >= 2 and len(best_profiles) > 1:
        return RoutingResult(
            faculty=None,
            approximate=False,
            reason=(
                "No specialist matched and multiple faculty are equally close; "
                "narrow the competency or choose an instructor."
            ),
        )

    # 3. No safe match at all.
    return RoutingResult(
        faculty=None,
        approximate=False,
        reason="No Academy faculty member matches this objective.",
    )


def minimize_learner_context(
    learner_profile: str,
    role: str,
    objective: str,
    skills: Optional[list[str]] = None,
) -> LearnerContext:
    """Build a minimized learner context for the receiving faculty.

    Only includes what affects instruction: profile name, role, objective,
    and optionally relevant skill names. Never includes full profile state,
    memory, secrets, or conversations.
    """
    return LearnerContext(
        learner_profile=learner_profile,
        role=role,
        objective=objective,
        relevant_skills=tuple(skills) if skills else (),
    )
