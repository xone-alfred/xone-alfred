from fastapi import FastAPI
from pydantic import BaseModel

from tools.client_summary import get_client_summary
from services.openai_service import ask_openai

app = FastAPI(title="Alfred Dev")


class ChatRequest(BaseModel):
    message: str
    display_code: str = "XM-0001"


@app.get("/health")
def health():
    return {"status": "ok", "service": "alfred-dev"}


@app.post("/chat")
def chat(request: ChatRequest):
    client_summary = get_client_summary(request.display_code)

    response = ask_openai(
        user_message=request.message,
        client_context=client_summary,
    )

    return {
        "answer": response,
        "client": request.display_code,
    }
