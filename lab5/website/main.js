// ---------------------------------------------------------------------------
// Lab 5 — AI Avatar News. No backend of its own:
//   1. POST topic to the n8n "heygen-generate" webhook → Ollama writes the
//      script, HeyGen starts rendering, returns { video_id, script }.
//   2. Poll the n8n "heygen-status" webhook until the video is ready, then
//      play it in the 16:9 (YouTube) player.
// ---------------------------------------------------------------------------
const GENERATE_URL = "http://localhost:5678/webhook/heygen-generate";
const STATUS_URL = "http://localhost:5678/webhook/heygen-status";
const POLL_MS = 15000; // HeyGen renders take a minute or more

const $ = (id) => document.getElementById(id);
let polling = null;

function setStatus(text, kind = "") {
  const pill = $("statusPill");
  pill.textContent = text;
  pill.className = "status-pill" + (kind ? " " + kind : "");
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
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    if (!res.ok) throw new Error(`n8n webhook ${res.status} — is the "HeyGen News Avatar" flow active?`);
    data = await res.json();
  } catch (e) {
    $("genBtn").disabled = false;
    setStatus("Error", "error");
    $("scriptText").textContent = `Could not reach the n8n flow. ${e.message}`;
    return;
  }

  if (data.script) $("scriptText").textContent = data.script;

  if (!data.video_id) {
    $("genBtn").disabled = false;
    setStatus("Error", "error");
    $("scriptText").textContent =
      "HeyGen did not return a video id. " + (data.error ? JSON.stringify(data.error) : "");
    return;
  }

  setStatus("Rendering video…", "working");
  $("hint").textContent = `Video ID ${data.video_id} — rendering at HeyGen. This can take 1–3 minutes.`;
  pollStatus(data.video_id);
}

function pollStatus(videoId) {
  const check = async () => {
    let s;
    try {
      const res = await fetch(STATUS_URL, {
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
        setStatus("No API credits", "error");
        $("hint").innerHTML =
          "HeyGen rendered nothing: <strong>the account has no API credits</strong>. " +
          "Add API credits in the HeyGen dashboard (Settings → Subscriptions / API), then generate again. " +
          "The script above was still written by Ollama.";
      } else {
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
