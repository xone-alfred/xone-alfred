from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from tools.client_summary import get_client_summary
from tools.search_clients import search_clients
from services.llm_service import ask_llm

app = FastAPI(title="Alfred Dev")


class ChatRequest(BaseModel):
    message: str
    display_code: str = "XP-0001"


@app.get("/health")
def health():
    return {"status": "ok", "service": "alfred-dev"}


@app.get("/clients/search")
def client_search(q: str):
    return search_clients(q)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>Alfred</title>
  <style>
    body { font-family: Arial; max-width: 900px; margin: 40px auto; }
    textarea, input { width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }
    button { padding: 10px 20px; cursor: pointer; }
    pre { white-space: pre-wrap; background: #f4f4f4; padding: 20px; }
    .result { padding: 10px; border: 1px solid #ddd; margin: 5px 0; cursor: pointer; }
    .result:hover { background: #f2f2f2; }
    .muted { color: #666; font-size: 14px; }
  </style>
</head>
<body>
  <h1>Alfred</h1>
  <p>Carlyle's executive health intelligence assistant.</p>

  <label>Search Client</label>
  <input id="client_search" placeholder="Type a client name or XP code..." oninput="searchClients()" />
  <input id="display_code" type="hidden" value="XP-0001" />

  <div id="selected_client" class="muted">Selected client: XP-0001</div>
  <div id="search_results"></div>

  <label>Ask Alfred</label>
  <textarea id="message" rows="5">Summarise this client for Carlyle</textarea>

  <button onclick="askAlfred()">Ask Alfred</button>

  <h3>Response</h3>
  <pre id="response"></pre>

  <script>
    async function searchClients() {
      const q = document.getElementById("client_search").value;
      const box = document.getElementById("search_results");

      if (q.length < 2) {
        box.innerHTML = "";
        return;
      }

      const res = await fetch(`/clients/search?q=${encodeURIComponent(q)}`);
      const clients = await res.json();

      box.innerHTML = "";

      clients.forEach(client => {
        const div = document.createElement("div");
        div.className = "result";
        div.textContent = `${client.first_name} ${client.last_name} — ${client.display_code}`;

        div.onclick = () => {
          document.getElementById("display_code").value = client.display_code;
          document.getElementById("selected_client").textContent =
            `Selected client: ${client.first_name} ${client.last_name} (${client.display_code})`;
          box.innerHTML = "";
          document.getElementById("client_search").value =
            `${client.first_name} ${client.last_name}`;
        };

        box.appendChild(div);
      });
    }

    async function askAlfred() {
      document.getElementById("response").textContent = "Thinking...";

      try {
        const res = await fetch("/chat", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            display_code: document.getElementById("display_code").value,
            message: document.getElementById("message").value
          })
        });

        const data = await res.json();

        if (!res.ok) {
          document.getElementById("response").textContent =
            "Error: " + JSON.stringify(data, null, 2);
          return;
        }

        document.getElementById("response").textContent =
          data.answer || JSON.stringify(data, null, 2);

      } catch (err) {
        document.getElementById("response").textContent = "Error: " + err.message;
      }
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
