// ---------------------------------------------------------------------------
// Lab 5 — AI Avatar News. No backend of its own:
//   1. POST topic to the n8n "heygen-generate" webhook → OpenAI writes the
//      script, HeyGen starts rendering, returns { video_id, script }.
//   2. Poll the n8n "heygen-status" webhook until the video is ready, then
//      play it in the 16:9 (YouTube) player.
// ---------------------------------------------------------------------------
const WEBHOOK_KEY = "lab7_base";
// The base the learner saved in the settings box (see n8n-connect.js). The old
// hardcoded localhost URL was wrong for anyone not running n8n on this machine.
const webhookBase = () =>
  (window.N8nConnect ? window.N8nConnect.load(WEBHOOK_KEY) : "") || "https://n8n.tertiarytraining.com/webhook";
const GENERATE_URL = () => `${webhookBase()}/heygen-generate`;
const STATUS_URL = () => `${webhookBase()}/heygen-status`;
const POLL_MS = 5000;        // ask HeyGen every 5s so the bar tracks reality closely
const RENDER_ESTIMATE_S = 120; // measured: a ~20s script renders in about two minutes

const $ = (id) => document.getElementById(id);
let polling = null;

function setStatus(text, kind = "") {
  const pill = $("statusPill");
  pill.textContent = text;
  pill.className = "status-pill" + (kind ? " " + kind : "");
}

// ---------------------------------------------------------------------------
// Progress bar.
//
// HeyGen's status API reports only "processing" or "completed" — there is NO
// percentage to read. So the bar is an honest ESTIMATE based on elapsed time:
// it eases toward 95% and STOPS there. It only shows 100% when HeyGen actually
// says completed. A bar that hits 100% and then keeps spinning is a lie, and
// learners notice.
// ---------------------------------------------------------------------------
let progressTimer = null;
let renderStartedAt = 0;

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

// The script step is quick; give it the first 15% of the bar.
function startRenderProgress() {
  renderStartedAt = Date.now();
  clearInterval(progressTimer);
  progressTimer = setInterval(() => {
    const elapsed = (Date.now() - renderStartedAt) / 1000;
    // Ease out: fast at first, then creeping — so a slow render never stalls at a
    // number that looks frozen, and never pretends to be finished.
    const frac = 1 - Math.exp(-elapsed / (RENDER_ESTIMATE_S / 2));
    const pct = 15 + frac * 80;                       // 15% → 95%, never beyond
    const secs = Math.round(elapsed);
    setProgress(pct, `HeyGen is rendering… ${secs}s elapsed (usually 1–3 min)`, "working");
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

  clearInterval(polling);
  $("genBtn").disabled = true;
  $("player").style.display = "none";
  $("poster").style.display = "block";
  $("scriptText").textContent = "Writing the anchor script with OpenAI…";
  setStatus("Writing script…", "working");
  showProgress();

  let data;
  try {
    const res = await fetch(GENERATE_URL(), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    if (!res.ok) throw new Error(`n8n webhook ${res.status} — is the "HeyGen News Avatar" flow active?`);
    data = await res.json();
  } catch (e) {
    $("genBtn").disabled = false;
    setStatus("Error", "error");
    finishProgress(false, "Could not reach the n8n flow");
    $("scriptText").textContent = `Could not reach the n8n flow. ${e.message}`;
    return;
  }

  if (data.script) $("scriptText").textContent = data.script;

  if (!data.video_id) {
    $("genBtn").disabled = false;
    setStatus("Error", "error");
    finishProgress(false, "HeyGen did not return a video id");
    $("scriptText").textContent =
      "HeyGen did not return a video id. " + (data.error ? JSON.stringify(data.error) : "");
    return;
  }

  // Script is written; the long phase starts now.
  setStep(2);
  setProgress(15, "HeyGen is rendering…", "working");
  startRenderProgress();

  setStatus("Rendering video…", "working");
  $("hint").textContent = `Video ID ${data.video_id} — rendering at HeyGen. This can take 1–3 minutes.`;
  pollStatus(data.video_id);
}

function pollStatus(videoId) {
  const check = async () => {
    let s;
    try {
      const res = await fetch(STATUS_URL(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ video_id: videoId }),
      });
      s = await res.json();
    } catch (e) {
      return; // transient; try again next tick
    }

    if (s.status === "completed" && s.video_url) {
      clearInterval(polling);
      const took = Math.round((Date.now() - renderStartedAt) / 1000);
      finishProgress(true, `Rendered in ${took}s — playing now`);
      setStatus("● LIVE", "done");
      const v = $("player");
      v.src = s.video_url;
      v.style.display = "block";
      $("poster").style.display = "none";
      v.play().catch(() => {});
      $("genBtn").disabled = false;
      $("hint").textContent = "Done! The AI news anchor video is playing above.";
    } else if (s.status === "failed") {
      clearInterval(polling);
      $("genBtn").disabled = false;
      const msg = s.error?.message || "";
      if (/insufficient credit/i.test(msg)) {
        finishProgress(false, "HeyGen has no API credits");
        setStatus("No API credits", "error");
        $("hint").innerHTML =
          "HeyGen rendered nothing: <strong>the account has no API credits</strong>. " +
          "Add API credits in the HeyGen dashboard (Settings → Subscriptions / API), then generate again. " +
          "The script above was still written by OpenAI.";
      } else {
        finishProgress(false, "HeyGen render failed");
        setStatus("Render failed", "error");
        $("hint").textContent = "HeyGen render failed: " + msg;
      }
    } else {
      setStatus("Rendering… (" + (s.status || "processing") + ")", "working");
    }
  };

  check();
  polling = setInterval(check, POLL_MS);
}

window.generate = generate;
