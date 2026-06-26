import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def ask_openai(user_message: str, client_context: dict) -> str:
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

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
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

    return response.output_text
