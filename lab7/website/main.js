// Lab 7 — Cloud AI avatar via Replicate.
// Website → n8n "replicate-generate" → Ollama script → Replicate (Kokoro TTS →
// SadTalker) → prediction_id. Then poll "replicate-status" until the video is ready.
const GENERATE_URL = "http://localhost:5678/webhook/replicate-generate";
const STATUS_URL = "http://localhost:5678/webhook/replicate-status";
const POLL_MS = 8000;

const $ = (id) => document.getElementById(id);
let polling = null;

function setStatus(text, kind = "") {
  const p = $("statusPill");
  p.textContent = text;
  p.className = "status-pill" + (kind ? " " + kind : "");
}

async function generate() {
  const topic = $("topic").value.trim();
  if (!topic) return;
  clearInterval(polling);
  $("genBtn").disabled = true;
  $("player").style.display = "none";
  $("poster").style.display = "block";
  $("scriptText").textContent = "Writing the anchor script with Ollama…";
  setStatus("Writing script…", "working");

  let data;
  try {
    const res = await fetch(GENERATE_URL, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    if (!res.ok) throw new Error(`n8n webhook ${res.status}`);
    data = await res.json();
  } catch (e) {
    $("genBtn").disabled = false;
    setStatus("Error", "error");
    $("scriptText").textContent = "Could not reach the n8n flow. " + e.message;
    return;
  }

  if (data.script) $("scriptText").textContent = data.script;

  if (!data.prediction_id) {
    $("genBtn").disabled = false;
    setStatus("No Replicate credit", "error");
    $("hint").innerHTML =
      "Replicate returned no prediction — usually <strong>the account has no credit</strong>. " +
      "Add credit at <em>replicate.com/account/billing</em>, then generate again. " +
      "The script above was still written by Ollama.";
    return;
  }

  setStatus("Rendering (Replicate)…", "working");
  $("hint").textContent = `Prediction ${data.prediction_id} — Kokoro TTS then SadTalker. ~1–3 min.`;
  pollStatus(data.prediction_id);
}

function pollStatus(id) {
  const check = async () => {
    let s;
    try {
      const res = await fetch(STATUS_URL, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prediction_id: id }),
      });
      s = await res.json();
    } catch (e) { return; }

    if (s.status === "succeeded" && s.video_url) {
      clearInterval(polling);
      setStatus("● LIVE", "done");
      const v = $("player");
      v.src = s.video_url; v.style.display = "block";
      $("poster").style.display = "none";
      v.play().catch(() => {});
      $("genBtn").disabled = false;
      $("hint").textContent = "Done — rendered on Replicate (SadTalker).";
    } else if (s.status === "failed" || s.status === "canceled") {
      clearInterval(polling);
      $("genBtn").disabled = false;
      setStatus("Render failed", "error");
      $("hint").textContent = "Replicate render failed: " + (s.error || "unknown");
    } else {
      setStatus("Rendering… (" + (s.status || "processing") + ")", "working");
    }
  };
  check();
  polling = setInterval(check, POLL_MS);
}

window.generate = generate;
