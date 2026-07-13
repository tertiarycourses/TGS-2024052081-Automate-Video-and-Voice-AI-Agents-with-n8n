// ---------------------------------------------------------------------------
// Lab 10 — AI Video Generation (Gemini Veo 3.1)
//
//   you type a TOPIC
//     -> n8n webhook  /veo-generate
//        -> OpenAI (gpt-4.1-mini) turns the topic into a CINEMATIC SHOT description
//        -> Veo 3.1 starts a long-running generation, returns an operation name
//   -> the page polls /veo-status until Google says done
//   -> the MP4 is streamed back through /veo-file, so the API key NEVER
//      reaches the browser — same rule as the ElevenLabs lab (Lab 4).
//
// Nothing is hardcoded: the learner points this page at their own n8n in ⚙ Settings.
// ---------------------------------------------------------------------------
const STORE = "veo_n8n_base";
const DEFAULT_BASE = "https://n8n.tertiarytraining.com/webhook";
const POLL_MS = 5000;
const ESTIMATE_S = 75; // measured: a Veo 3.1 Fast 8-second clip lands in about a minute

const $ = (id) => document.getElementById(id);
const base = () => (localStorage.getItem(STORE) || DEFAULT_BASE).replace(/\/$/, "");

let polling = null;
let progressTimer = null;
let startedAt = 0;

/* ── settings ─────────────────────────────────────────────────────────── */
function openSettings() {
  $("baseUrl").value = localStorage.getItem(STORE) || DEFAULT_BASE;
  $("settingsModal").classList.add("active");
}
function closeSettings() {
  $("settingsModal").classList.remove("active");
}
function saveSettings() {
  localStorage.setItem(STORE, $("baseUrl").value.trim() || DEFAULT_BASE);
  closeSettings();
  setStatus(`Using ${base()}`);
}

/* ── progress ─────────────────────────────────────────────────────────── */
// Veo's operation API reports only done / not done — there is NO percentage to read.
// So this is an elapsed-time estimate that eases toward 95% and stops there, hitting
// 100% only when the video actually arrives. A bar that sits at 100% while still
// working is a lie.
function showProgress() {
  $("progress").hidden = false;
  setProgress(0, "OpenAI is writing the shot…");
  setStep(1);
}
function setProgress(pct, label, kind = "") {
  const p = Math.max(0, Math.min(100, Math.round(pct)));
  $("pFill").style.width = `${p}%`;
  $("pFill").className = `p-fill ${kind}`;
  $("pPct").textContent = `${p}%`;
  if (label) $("pLabel").textContent = label;
}
function setStep(n) {
  [1, 2, 3].forEach((i) => {
    $("step" + i).className = "step" + (i < n ? " is-done" : i === n ? " is-active" : "");
  });
}
function startVeoEstimate() {
  startedAt = Date.now();
  clearInterval(progressTimer);
  progressTimer = setInterval(() => {
    const s = (Date.now() - startedAt) / 1000;
    const frac = 1 - Math.exp(-s / (ESTIMATE_S / 2));
    setProgress(15 + frac * 80, `Veo 3.1 is filming… ${Math.round(s)}s elapsed (usually 1–2 min)`);
  }, 500);
}
function finishProgress(ok, msg) {
  clearInterval(progressTimer);
  progressTimer = null;
  setProgress(100, msg, ok ? "done" : "error");
  setStep(ok ? 3 : 2);
}

function setStatus(text, kind = "") {
  const el = $("status");
  el.textContent = text;
  el.className = "statusline" + (kind ? " " + kind : "");
}

/* ── generate ─────────────────────────────────────────────────────────── */
async function generate() {
  const topic = $("topic").value.trim();
  if (!topic) return setStatus("Enter a topic first.", "err");

  clearInterval(polling);
  $("genBtn").disabled = true;
  $("dlBtn").hidden = true;
  $("player").hidden = true;
  $("stageEmpty").hidden = false;
  $("promptBox").hidden = true;
  showProgress();
  setStatus("Asking n8n…");

  let data;
  try {
    const res = await fetch(`${base()}/veo-generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, model: $("model").value }),
    });
    if (!res.ok) throw new Error(`n8n returned ${res.status} — is the "Lab 10" flow published?`);
    data = await res.json();
  } catch (e) {
    $("genBtn").disabled = false;
    finishProgress(false, "Could not reach the n8n flow");
    setStatus(`Could not reach the n8n flow. ${e.message}`, "err");
    return;
  }

  // Show what OpenAI actually wrote — the topic you typed is NOT the prompt Veo saw.
  if (data.prompt) {
    $("promptText").textContent = data.prompt;
    $("promptBox").hidden = false;
  }

  if (!data.operation) {
    $("genBtn").disabled = false;
    finishProgress(false, "Veo did not start");
    setStatus(data.error || "Veo did not return an operation.", "err");
    return;
  }

  setStep(2);
  setProgress(15, "Veo 3.1 is filming…");
  startVeoEstimate();
  setStatus("Generating — this usually takes 1–2 minutes.");
  poll(data.operation);
}

function poll(operation) {
  const check = async () => {
    let s;
    try {
      const res = await fetch(`${base()}/veo-status`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ operation }),
      });
      s = await res.json();
    } catch {
      return; // transient — try again on the next tick
    }

    if (!s.done) return;

    clearInterval(polling);
    $("genBtn").disabled = false;

    if (s.failed) {
      finishProgress(false, "Veo failed");
      setStatus(s.error || "Veo failed.", "err");
      return;
    }

    const took = Math.round((Date.now() - startedAt) / 1000);
    finishProgress(true, `Filmed in ${took}s`);

    // n8n proxies the download, so the API key stays server-side.
    const url = `${base()}/veo-file?file_id=${encodeURIComponent(s.file_id)}`;
    const v = $("player");
    const dl = $("dlBtn");

    // Pull the MP4 down ONCE into a blob rather than streaming it from the webhook.
    // n8n's binary response does not honour HTTP Range requests, so a <video> pointed
    // straight at the webhook cannot seek or replay — it plays once and then refuses.
    // A blob URL is local, seekable, and replayable, and the download reuses it.
    setStatus("Fetching the video…");
    try {
      const blob = await (await fetch(url)).blob();
      const objectUrl = URL.createObjectURL(blob);
      v.src = objectUrl;
      dl.href = objectUrl;
    } catch {
      v.src = url; // fall back to streaming; replay may not work
      dl.href = url;
    }

    v.hidden = false;
    v.loop = false;
    $("stageEmpty").hidden = true;
    v.play().catch(() => {});
    dl.hidden = false;

    setStatus(`Done in ${took}s — the video is playing. Replay it, or use “Download MP4”.`, "ok");
  };

  check();
  polling = setInterval(check, POLL_MS);
}

window.generate = generate;
window.openSettings = openSettings;
window.closeSettings = closeSettings;
window.saveSettings = saveSettings;
