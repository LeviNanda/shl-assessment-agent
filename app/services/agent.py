from app.models.schemas import ChatRequest, ChatResponse, Recommendation
from app.services.guardrails import is_off_topic, is_comparison_query
from app.services.retriever import search_catalog
from app.services.context_extractor import extract_context
from app.services.comparison import compare_assessments


def extract_user_context(messages):
    return " ".join([m.content for m in messages if m.role == "user"])


def latest_user_message(messages):
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return ""


def has_enough_context(text: str) -> bool:
    context = extract_context(text)

    if len(text.split()) < 5:
        return False

    return (
        len(context["roles"]) > 0
        or len(context["technical_skills"]) > 0
        or len(context["soft_skills"]) > 0
        or context["personality_required"]
        or context["cognitive_required"]
    )


def clarification_question(text: str) -> str:
    context = extract_context(text)

    if not context["roles"] and not context["technical_skills"]:
        return "What role are you hiring for, and what technical skills should the assessment cover?"

    if not context["seniority"]:
        return "What seniority level is this role: entry-level, mid-level, or senior?"

    return "Which traits matter most: technical skills, cognitive ability, personality, communication, or leadership?"


def build_recommendations(results):
    recommendations = []
    seen_urls = set()

    for item in results:
        name = item.get("name", "").strip()
        url = item.get("url", "").strip()

        if not name or not url or url in seen_urls:
            continue

        if "shl.com" not in url:
            continue

        seen_urls.add(url)

        recommendations.append(
            Recommendation(
                name=name,
                url=url,
                test_type=item.get("test_type") or "SHL Assessment",
            )
        )

    return recommendations[:10]


def run_agent(request: ChatRequest):
    user_context = extract_user_context(request.messages)
    latest_message = latest_user_message(request.messages)

    if is_off_topic(latest_message):
        return ChatResponse(
            reply="I can only help with SHL assessment recommendations and comparisons based on the SHL catalog.",
            recommendations=[],
            end_of_conversation=False,
        )

    if is_comparison_query(latest_message):
        return ChatResponse(
            reply=compare_assessments(latest_message),
            recommendations=[],
            end_of_conversation=False,
        )

    if not has_enough_context(user_context):
        return ChatResponse(
            reply=clarification_question(user_context),
            recommendations=[],
            end_of_conversation=False,
        )

    results = search_catalog(user_context, top_k=10)
    recommendations = build_recommendations(results)

    if not recommendations:
        return ChatResponse(
            reply="I could not find a strong match in the SHL catalog. Please provide the role, skills, and assessment type.",
            recommendations=[],
            end_of_conversation=False,
        )

    return ChatResponse(
        reply=f"Based on the SHL catalog and your conversation history, here are {len(recommendations)} suitable assessments.",
        recommendations=recommendations,
        end_of_conversation=False,
    )