from app.services.llm import generate_reply

prompt = """
User wants assessments for a Java developer with communication skills.
"""

reply = generate_reply(
    prompt,
    fallback="Fallback response."
)

print(reply)