import re


ROLE_KEYWORDS = [
    "developer", "engineer", "manager", "sales", "analyst",
    "support", "consultant", "graduate", "administrator",
]

TECH_SKILLS = [
    "java", "python", "sql", "javascript", "react", "frontend",
    "backend", "cloud", "data", "coding", "software", "programming",
    "excel", "database", "qa", "testing",
]

SOFT_SKILLS = [
    "leadership", "communication", "stakeholder", "teamwork",
    "problem solving", "problem-solving", "collaboration",
    "customer", "presentation",
]

PERSONALITY_KEYWORDS = [
    "personality", "behavioral", "behavioural", "culture", "opq",
]

COGNITIVE_KEYWORDS = [
    "cognitive", "aptitude", "reasoning", "ability", "gsa",
]


def extract_context(text: str) -> dict:
    text_lower = text.lower()

    context = {
        "roles": [],
        "technical_skills": [],
        "soft_skills": [],
        "personality_required": False,
        "cognitive_required": False,
        "seniority": None,
    }

    for role in ROLE_KEYWORDS:
        if role in text_lower:
            context["roles"].append(role)

    for skill in TECH_SKILLS:
        if skill in text_lower:
            context["technical_skills"].append(skill)

    for skill in SOFT_SKILLS:
        if skill in text_lower:
            context["soft_skills"].append(skill)

    if any(word in text_lower for word in PERSONALITY_KEYWORDS):
        context["personality_required"] = True

    if any(word in text_lower for word in COGNITIVE_KEYWORDS):
        context["cognitive_required"] = True

    seniority_patterns = {
        "entry": r"\b(entry|junior|fresher|graduate)\b",
        "mid": r"\b(mid|middle|3 years|4 years|5 years)\b",
        "senior": r"\b(senior|lead|principal|architect)\b",
    }

    for level, pattern in seniority_patterns.items():
        if re.search(pattern, text_lower):
            context["seniority"] = level

    return context