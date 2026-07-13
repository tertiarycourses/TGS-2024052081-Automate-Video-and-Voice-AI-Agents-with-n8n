// Lab 5 (open-source) — free, local AI avatar news.
// Website → n8n "os-generate" webhook → Ollama script → local render service
// (macOS `say` + ffmpeg, or Wav2Lip if installed) → 1080p video URL. Synchronous.
const GENERATE_URL = "https://n8n.tertiarytraining.com/webhook/os-generate";
const RENDER_ESTIMATE_S = 25; // measured: ~17s for a 7s clip (TTS + Wav2Lip on Apple Silicon)

const $ = (id) => document.getElementById(id);

function setStatus(text, kind = "") {
  const p = $("statusPill");
  p.textContent = text;
  p.className = "status-pill" + (kind ? " " + kind : "");
}

// ---------------------------------------------------------------------------
// Progress bar.
//
// Unlike the HeyGen lab, this flow is SYNCHRONOUS: one request that returns only
// when the video is finished. There is no status endpoint to ask, so the bar is
// an elapsed-time ESTIMATE. It eases toward 95% and stops there — it only shows
// 100% when the video actually arrives. A bar that sits at 100% while still
// working is a lie, and learners notice.
// ---------------------------------------------------------------------------
let progressTimer = null;
let startedAt = 0;

function showProgress() {
  $("progress").hidden = false;
  setProgress(0, "Writing the anchor script…", "working");
  setStep(1);
}

function setProgress(pct, label, kind = "working") {
  const p = Math.max(0, Math.min(100, Math.round(pct)));
  const fill = $("progressFill");
  fill.style.width = p + "%";
  fill.className = "progress-fill " + kind;
  $("progressPct").textContent = p + "%";
  if (label) $("progressLabel").textContent = label;
}

function setStep(n) {
  [1, 2, 3].forEach((i) => {
    const el = $("step" + i);
    el.className = "step" + (i < n ? " is-done" : i === n ? " is-active" : "");
  });
}

function startProgress() {
  startedAt = Date.now();
  clearInterval(progressTimer);
  progressTimer = setInterval(() => {
    const elapsed = (Date.now() - startedAt) / 1000;
    // Ollama first (~the first few seconds), then the local render.
    if (elapsed > 4) setStep(2);
    const frac = 1 - Math.exp(-elapsed / (RENDER_ESTIMATE_S / 2));
    const pct = frac * 95; // 0 → 95%, never beyond
    const label =
      elapsed <= 4
        ? "Ollama is writing the anchor script…"
        : `Rendering locally with TTS + Wav2Lip… ${Math.round(elapsed)}s elapsed`;
    setProgress(pct, label, "working");
  }, 500);
}

function finishProgress(ok, message) {
  clearInterval(progressTimer);
  progressTimer = null;
  setProgress(100, message, ok ? "done" : "error");
  setStep(ok ? 3 : 2);
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
  showProgress();
  startProgress();

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
      const took = Math.round((Date.now() - startedAt) / 1000);
      // `engine` tells the truth: "wav2lip" = real lip sync; "kenburns" = the
      // fallback slideshow, which means Wav2Lip did not run.
      finishProgress(true, `Rendered locally in ${took}s with ${data.engine || "the local engine"}`);
      setStatus("● LIVE", "done");
      const v = $("player");
      v.src = data.video_url;
      v.style.display = "block";
      $("poster").style.display = "none";
      v.play().catch(() => {});
      $("hint").textContent =
        `Done — rendered locally with "${data.engine}" in ~${Math.round(data.duration || 0)}s of audio. No cloud, no credits.`;
    } else {
      finishProgress(false, "No video returned — is the render service running?");
      setStatus("Error", "error");
      $("hint").textContent =
        "No video returned. Is the render service running (python3 render_service.py on port 8099)? " +
        (data.error ? JSON.stringify(data.error) : "");
    }
  } catch (e) {
    finishProgress(false, "Could not reach the n8n flow");
    setStatus("Error", "error");
    $("scriptText").textContent = "Could not reach the n8n flow. " + e.message;
  } finally {
    $("genBtn").disabled = false;
  }
}

window.generate = generate;
