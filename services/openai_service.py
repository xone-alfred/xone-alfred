import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_openai(user_message: str, client_context: dict) -> str:
    system_prompt = """
You are Alfred, Carlyle's executive health intelligence assistant.
You help Carlyle understand client health data.
Do not diagnose disease. Base answers only on the provided context.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Client context:\n{client_context}\n\nCarlyle asks:\n{user_message}",
            },
        ],
    )

    return response.output_text
