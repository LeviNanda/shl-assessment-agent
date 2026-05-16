from app.services.llm import generate_reply

reply = generate_reply(
    prompt="Write one short professional sentence for a recruiter recommending SHL assessments for a Java developer.",
    fallback="Fallback response: LLM is not connected."
)

print(reply)
