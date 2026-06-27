import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("KIMI_API_KEY"),
    base_url=os.getenv("KIMI_BASE_URL", "https://api.moonshot.ai/v1"),
)


def ask_llm(user_message: str, client_context: dict) -> str:
    system_prompt = """
You are Alfred, Carlyle's executive health intelligence assistant.

You help Carlyle understand client health data, goals, coaching notes,
biomarkers, wearable trends and relevant risks.

You do not diagnose disease.
You do not replace a doctor.
You provide structured observations, patterns, and suggested coaching focus areas.

Always base your answer on the provided client context.
If data is missing, say what is missing.
"""

    response = client.chat.completions.create(
        model="kimi-k2.6",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""
Client context:
{client_context}

Carlyle asks:
{user_message}
""",
            },
        ],
    )

    return response.choices[0].message.content
