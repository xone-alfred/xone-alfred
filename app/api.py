from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from tools.client_summary import get_client_summary
from tools.search_clients import search_clients
from services.llm_service import ask_llm
from tools.get_client_profile import get_client_profile
from tools.dashboard import get_dashboard

app = FastAPI(title="Alfred Dev")

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str
    display_code: str = "XP-0001"


@app.get("/health")
def health():
    return {"status": "ok", "service": "alfred-dev"}


@app.get("/clients/search")
def client_search(q: str):
    return search_clients(q)


@app.get("/client/{display_code}")
def client_profile(display_code: str):
    return get_client_profile(display_code)


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/chat")
def chat(request: ChatRequest):
    client_summary = get_client_summary(request.display_code)

    response = ask_llm(
        user_message=request.message,
        client_context=client_summary,
    )

    return {
        "answer": response,
        "client": request.display_code,
    }
    
@app.get("/dashboard")
def dashboard():
    return get_dashboard()