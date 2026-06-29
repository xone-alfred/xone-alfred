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

    div.onclick = async () => {
      document.getElementById("display_code").value = client.display_code;
      document.getElementById("selected_client").textContent =
        `Selected client: ${client.first_name} ${client.last_name} (${client.display_code})`;

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
  profileBox.innerHTML = "Loading client profile...";

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
          <div>
            <div class="label-small">Programme</div>
            <div>${client.programme || "Not set"}</div>
          </div>
          <div>
            <div class="label-small">Enrolled</div>
            <div>${client.enrolled_at || "Not set"}</div>
          </div>
          <div>
            <div class="label-small">Occupation</div>
            <div>${client.occupation || "Not set"}</div>
          </div>
          <div>
            <div class="label-small">Email</div>
            <div>${client.email || "Not set"}</div>
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    profileBox.innerHTML = "Could not load client profile: " + err.message;
  }
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