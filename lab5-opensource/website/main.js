// Lab 5 (open-source) — free, local AI avatar news.
// Website → n8n "os-generate" webhook → Ollama script → local render service
// (macOS `say` + ffmpeg, or Wav2Lip if installed) → 1080p video URL. Synchronous.
const GENERATE_URL = "http://localhost:5678/webhook/os-generate";

const $ = (id) => document.getElementById(id);

function setStatus(text, kind = "") {
  const p = $("statusPill");
  p.textContent = text;
  p.className = "status-pill" + (kind ? " " + kind : "");
}

async function generate() {
  const topic = $("topic").value.trim();
  if (!topic) return;

  $("genBtn").disabled = true;
  $("player").style.display = "none";
  $("poster").style.display = "block";
  $("scriptText").textContent = "Writing the anchor script with Ollama, then rendering locally…";
  setStatus("Generating…", "working");
  $("hint").textContent = "Working: Ollama writes the script, then the local service renders the 1080p video (~10–30s).";

  try {
    const res = await fetch(GENERATE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    if (!res.ok) throw new Error(`n8n webhook ${res.status} — is the "Open-Source News Avatar" flow active?`);
    const data = await res.json();

    if (data.script) $("scriptText").textContent = data.script;

    if (data.video_url) {
      setStatus("● LIVE", "done");
      const v = $("player");
      v.src = data.video_url;
      v.style.display = "block";
      $("poster").style.display = "none";
      v.play().catch(() => {});
      $("hint").textContent =
        `Done — rendered locally with "${data.engine}" in ~${Math.round(data.duration || 0)}s of audio. No cloud, no credits.`;
    } else {
      setStatus("Error", "error");
      $("hint").textContent =
        "No video returned. Is the render service running (python3 render_service.py on port 8099)? " +
        (data.error ? JSON.stringify(data.error) : "");
    }
  } catch (e) {
    setStatus("Error", "error");
    $("scriptText").textContent = "Could not reach the n8n flow. " + e.message;
  } finally {
    $("genBtn").disabled = false;
  }
}

window.generate = generate;
