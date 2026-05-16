OFF_TOPIC_KEYWORDS = [
    "legal advice", "employment law", "salary negotiation",
    "resume", "cv", "cover letter", "interview tips",
    "hiring strategy", "ignore previous instructions",
    "system prompt", "jailbreak", "forget your rules",
]


def is_off_topic(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in OFF_TOPIC_KEYWORDS)


def is_comparison_query(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in ["compare", "difference", "vs", "versus"])