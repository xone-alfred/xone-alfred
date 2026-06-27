from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from tools.client_summary import get_client_summary
from services.llm_service import ask_llm

app = FastAPI(title="Alfred Dev")


class ChatRequest(BaseModel):
    message: str
    display_code: str = "XP-0001"


@app.get("/health")
def health():
    return {"status": "ok", "service": "alfred-dev"}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>Alfred</title>
  <style>
    body { font-family: Arial; max-width: 900px; margin: 40px auto; }
    textarea, input { width: 100%; padding: 10px; margin: 8px 0; }
    button { padding: 10px 20px; }
    pre { white-space: pre-wrap; background: #f4f4f4; padding: 20px; }
  </style>
</head>
<body>
  <h1>Alfred</h1>
  <p>Carlyle's executive health intelligence assistant.</p>

  <label>Client Display Code</label>
  <input id="display_code" value="XP-0001" />

  <label>Question</label>
  <textarea id="message" rows="5">Summarise this client for Carlyle</textarea>

  <button onclick="askAlfred()">Ask Alfred</button>

  <h3>Response</h3>
  <pre id="response"></pre>

  <script>
    async function askAlfred() {
      document.getElementById("response").textContent = "Thinking...";
      const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          display_code: document.getElementById("display_code").value,
          message: document.getElementById("message").value
        })
      });
      const data = await res.json();
      document.getElementById("response").textContent = data.answer || JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>
"""


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
