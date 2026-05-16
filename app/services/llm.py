import os
from dotenv import load_dotenv

from groq import Groq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def has_groq():
    return bool(GROQ_API_KEY)


def generate_reply(prompt: str, fallback: str) -> str:

    if not has_groq():
        return fallback

    try:
        client = Groq(api_key=GROQ_API_KEY)

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an SHL assessment recommendation assistant. "
                        "Never invent assessment names or URLs."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=300,
        )

        text = completion.choices[0].message.content.strip()

        if not text:
            return fallback

        return text

    except Exception as e:
        print("Groq Error:", e)
        return fallback