"""Deterministic Academy Dean routing for profile learners.

Routes a profile learner (name, role, objective) to the most specific
installed Academy faculty member using the academy.json manifest as
authority.  Never invents a profile that does not exist in the catalog.

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
# Category mapping: manifest category → broad fallback profile
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
# the corresponding topic.  The topic key itself is always implied.
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


def _load_manifest(path: Optional[Path] = None) -> dict:
    target = path or MANIFEST
    return json.loads(target.read_text(encoding="utf-8"))


def _profile_names(manifest: dict) -> set[str]:
    return {p["name"] for p in manifest["profiles"]}


def _profile_by_name(manifest: dict) -> dict[str, dict]:
    return {p["name"]: p for p in manifest["profiles"]}


def _topic_from_objective(objective: str) -> Optional[str]:
    """Extract a specialist_preferences key from the objective text.

    Uses keyword expansion (TOPIC_KEYWORDS) to map natural-language terms
    in the objective to the corresponding specialist_preferences key.
    Returns the most specific match (topic with the most keyword hits).
    """
    objective_lower = objective.lower()
    manifest = _load_manifest()
    prefs = manifest.get("routing", {}).get("specialist_preferences", {})

    best: Optional[str] = None
    best_score = 0

    for topic_key in prefs:
        keywords = TOPIC_KEYWORDS.get(topic_key, [topic_key.replace("-", " ")])
        score = 0
        for kw in keywords:
            # Use word-boundary matching to avoid substring false positives
            # (e.g. "base" matching inside "database")
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, objective_lower):
                # Multi-word keywords get higher weight (more specific)
                word_count = len(kw.split())
                score += word_count
        if score > best_score:
            best_score = score
            best = topic_key

    return best if best_score > 0 else None


def _is_interdisciplinary(objective: str) -> bool:
    """Check if an objective spans multiple academic domains.

    Returns True if keywords from 2+ different specialist_preferences
    topics appear in the objective, indicating a genuinely cross-domain request.

    Uses a stricter threshold: requires at least 2 distinct domains with
    keyword hits, and excludes generic single-word keywords that appear
    across many domains (like "modeling", "analysis", "design").
    """
    objective_lower = objective.lower()
    manifest = _load_manifest()
    prefs = manifest.get("routing", {}).get("specialist_preferences", {})

    # Generic words that appear across many domains and shouldn't trigger
    # interdisciplinary detection on their own
    GENERIC_WORDS = {
        "modeling", "analysis", "design", "system", "systems", "theory",
        "practice", "method", "methods", "research", "evaluation",
        "management", "engineering", "science", "learning", "education",
        "security", "data", "model", "models",
    }

    domains_hit: set[str] = set()
    for topic_key in prefs:
        keywords = TOPIC_KEYWORDS.get(topic_key, [topic_key.replace("-", " ")])
        for kw in keywords:
            # Skip generic single-word keywords for interdisciplinary detection
            if len(kw.split()) == 1 and kw in GENERIC_WORDS:
                continue
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, objective_lower):
                domains_hit.add(topic_key)
                break  # One hit per domain is enough

    return len(domains_hit) >= 2


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
    prefs = manifest.get("routing", {}).get("specialist_preferences", {})
    broad_chairs = set(manifest.get("routing", {}).get("broad_chairs", []))

    # 1. Try specialist_preferences (most specific)
    topic = _topic_from_objective(objective)
    if topic and topic in prefs:
        # Check if the request is genuinely interdisciplinary (spans multiple domains)
        if _is_interdisciplinary(objective):
            for chair in broad_chairs:
                if chair in installed:
                    return RoutingResult(
                        faculty=chair,
                        approximate=True,
                        reason=(
                            f"Request spans multiple disciplines; "
                            f"routing to broad chair '{chair}'."
                        ),
                    )

        specialist = prefs[topic]
        if specialist in installed:
            return RoutingResult(
                faculty=specialist,
                approximate=False,
                reason=f"Direct specialist match for '{topic}'.",
            )
        # Specialist preference exists but profile not installed —
        # fall back to the category's broad representative.
        for profile in manifest["profiles"]:
            if profile["name"] == specialist:
                cat = profile.get("category", "")
                fallback = CATEGORY_BROAD_FALLBACK.get(cat)
                if fallback and fallback in installed:
                    return RoutingResult(
                        faculty=fallback,
                        approximate=True,
                        reason=(
                            f"Specialist '{specialist}' not installed; "
                            f"falling back to category broad faculty "
                            f"'{fallback}'."
                        ),
                    )

    # 2. Role-description scan for requests without a clear topic match
    objective_lower = objective.lower()
    # Filter out common stop words so weak matches don't dominate
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
    objective_words = [
        w for w in objective_lower.split()
        if w.isalpha() and w not in STOP_WORDS
    ]
    best: Optional[str] = None
    best_score = 0
    for profile in manifest["profiles"]:
        role_desc = profile.get("role", "").lower()
        score = sum(1 for word in objective_words if word in role_desc)
        if score > best_score:
            best_score = score
            best = profile["name"]

    if best and best_score > 0:
        return RoutingResult(
            faculty=best,
            approximate=True,
            reason=(
                f"No specialist matched; "
                f"closest role-description match is '{best}'."
            ),
        )

    # 3. No match at all
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
    and optionally relevant skill names.  Never includes full profile state,
    memory, secrets, or conversations.
    """
    return LearnerContext(
        learner_profile=learner_profile,
        role=role,
        objective=objective,
        relevant_skills=tuple(skills) if skills else (),
    )
