const form = document.getElementById("assessment-form");
const statusBox = document.getElementById("status");
const resultsSection = document.getElementById("results");
const submitButton = document.getElementById("submit-button");

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function statusClass(status) {
  const normalized = String(status || "").toLowerCase();
  if (normalized === "pass") return "status-pass";
  if (normalized === "partial") return "status-partial";
  return "status-missing";
}

function renderPresence(findings) {
  const tbody = document.querySelector("#presence-table tbody");
  tbody.innerHTML = findings.map(item => `
    <tr>
      <td>${escapeHtml(item.label)}</td>
      <td><span class="status-pill ${statusClass(item.status)}">${escapeHtml(item.status)}</span></td>
      <td>${escapeHtml(item.earned)}/${escapeHtml(item.possible)}</td>
      <td>${escapeHtml((item.found_paths || []).join(", ") || "None")}</td>
      <td>${escapeHtml(item.recommendation || "")}</td>
    </tr>
  `).join("");
}

function renderQuality(findings) {
  const tbody = document.querySelector("#quality-table tbody");
  const bars = document.getElementById("quality-bars");

  tbody.innerHTML = findings.map(item => `
    <tr>
      <td>${escapeHtml(item.label)}</td>
      <td><span class="status-pill ${statusClass(item.status)}">${escapeHtml(item.status)}</span></td>
      <td>${item.applicable === false ? "N/A" : `${escapeHtml(item.earned)}/${escapeHtml(item.possible)}`}</td>
      <td>${escapeHtml((item.evidence || []).join(", ") || "None")}</td>
      <td>${escapeHtml(item.recommendation || "")}</td>
    </tr>
  `).join("");

  bars.innerHTML = findings
    .filter(item => item.applicable !== false)
    .map(item => {
      const percent = Number(item.percent || 0);
      return `
        <div class="bar-row">
          <strong>${escapeHtml(item.label)}</strong>
          <div class="bar-track"><div class="bar-fill" style="width:${percent}%"></div></div>
          <span>${percent.toFixed(1)}%</span>
        </div>
      `;
    }).join("");
}

function renderPriorities(containerId, priorities) {
  const container = document.getElementById(containerId);
  if (!priorities || priorities.length === 0) {
    container.innerHTML = `<p class="muted">No priorities were returned.</p>`;
    return;
  }

  container.innerHTML = priorities.map((item, index) => {
    const label = typeof item === "string" ? item : item.label;
    const recommendation = typeof item === "string" ? "" : item.recommendation || "";
    return `
      <div class="priority">
        <strong>${index + 1}. ${escapeHtml(label)}</strong>
        ${recommendation ? `<div>${escapeHtml(recommendation)}</div>` : ""}
      </div>
    `;
  }).join("");
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  statusBox.className = "status";
  statusBox.textContent = "Cloning and assessing repository. This may take a minute...";
  submitButton.disabled = true;
  resultsSection.classList.add("hidden");

  const payload = {
    repository_url: document.getElementById("repository-url").value,
    hpc_applicable: document.getElementById("hpc-applicable").checked,
    use_ai: document.getElementById("use-ai").checked
  };

  try {
    const response = await fetch("/api/assess", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Assessment failed.");
    }

    document.getElementById("repository-name").textContent = data.repository_name;
    const repositoryLink = document.getElementById("repository-link");
    repositoryLink.textContent = data.repository_url;
    repositoryLink.href = data.repository_url;

    const presence = Number(data.presence.percent || 0);
    const quality = Number(data.quality.quality_percent || 0);

    document.getElementById("presence-score").textContent = `${presence.toFixed(1)}%`;
    document.getElementById("quality-score").textContent = `${quality.toFixed(1)}%`;
    document.getElementById("quality-band").textContent = data.quality.quality_band || "Unknown";
    document.getElementById("presence-meter").style.width = `${presence}%`;
    document.getElementById("quality-meter").style.width = `${quality}%`;

    renderPresence(data.presence.findings || []);
    renderQuality(data.quality.quality_findings || []);
    renderPriorities("deterministic-priorities", data.quality.priority_actions || []);

    if (data.ai && data.ai.ok) {
      renderPriorities("ai-priorities", data.ai.priorities || []);
    } else if (data.ai) {
      document.getElementById("ai-priorities").innerHTML =
        `<p class="muted">${escapeHtml(data.ai.message || "AI output was unavailable.")}</p>`;
    } else {
      document.getElementById("ai-priorities").innerHTML =
        `<p class="muted">AI was not requested for this assessment.</p>`;
    }

    document.getElementById("html-report").href = data.html_report_path;
    document.getElementById("json-report").href = data.json_report_path;

    resultsSection.classList.remove("hidden");
    statusBox.className = "status success";
    statusBox.textContent = "Assessment completed successfully.";
  } catch (error) {
    statusBox.className = "status error";
    statusBox.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
});
