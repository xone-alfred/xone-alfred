function renderMarkdown(text) {
  return text
    .replace(/^### (.*$)/gim, "<h3>$1</h3>")
    .replace(/^## (.*$)/gim, "<h2>$1</h2>")
    .replace(/^# (.*$)/gim, "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>")
    .replace(/\n- (.*)/gim, "<li>$1</li>")
    .replace(/\n/g, "<br>");
}

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
    div.textContent = `${client.first_name} ${client.last_name} - ${client.display_code}`;

    div.onclick = async () => {
      document.getElementById("display_code").value = client.display_code;
      document.getElementById("selected_client").textContent =
        `${client.first_name} ${client.last_name} (${client.display_code})`;

      box.innerHTML = "";
      document.getElementById("client_search").value =
        `${client.first_name} ${client.last_name}`;

      await loadClientProfile(client.display_code);
    };

    box.appendChild(div);
  });
}

async function loadClientProfile(displayCode) {
  const profileBox = document.getElementById("client_profile");
  profileBox.innerHTML = `<div class="loading">Loading client profile...</div>`;

  try {
    const res = await fetch(`/client/${encodeURIComponent(displayCode)}`);
    const client = await res.json();

    profileBox.innerHTML = `
      <div class="profile">
        <div class="profile-header">
          <div>
            <h2>${client.name}</h2>
            <div class="muted">${client.display_code}</div>
          </div>
          <div class="status-pill">${client.status}</div>
        </div>

        <div class="profile-grid">
          <div><span>Programme</span><strong>${client.programme || "Not set"}</strong></div>
          <div><span>Enrolled</span><strong>${client.enrolled_at || "Not set"}</strong></div>
          <div><span>Occupation</span><strong>${client.occupation || "Not set"}</strong></div>
          <div><span>Email</span><strong>${client.email || "Not set"}</strong></div>
        </div>
      </div>
    `;
  } catch (err) {
    profileBox.innerHTML = "Could not load client profile: " + err.message;
  }
}

async function askAlfred() {
  const responseBox = document.getElementById("response");

  responseBox.innerHTML = `
    <div class="thinking">
      <strong>Alfred is reviewing this client...</strong>
      <div>✓ Bloodwork</div>
      <div>✓ Weekly check-ins</div>
      <div>✓ Coaching notes</div>
      <div>✓ Wearables</div>
      <div class="muted">Generating recommendation...</div>
    </div>
  `;

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
      responseBox.textContent = "Error: " + JSON.stringify(data, null, 2);
      return;
    }

    responseBox.innerHTML = renderMarkdown(data.answer || JSON.stringify(data, null, 2));
  } catch (err) {
    responseBox.textContent = "Error: " + err.message;
  }
}

async function loadDashboard() {
  const res = await fetch("/dashboard");
  const data = await res.json();

  document.getElementById("dashboard").innerHTML = `
    <h3>Today's Overview</h3>

    <div class="metric red">
      ${data.attention.length} need attention
    </div>

    <div class="metric amber">
      ${data.review.length} need review
    </div>

    <div class="metric green">
      ${data.good.length} progressing well
    </div>

    <hr style="margin:20px 0">

    <strong>Morning Brief</strong>

    <p class="muted">
      Alfred reviewed every client overnight.
    </p>
  `;
}

loadDashboard();