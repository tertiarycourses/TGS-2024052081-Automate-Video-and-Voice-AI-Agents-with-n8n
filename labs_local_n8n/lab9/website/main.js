// ---------------------------------------------------------------------------
// Lab 9 — Interactive avatar, streamed from the cloud (HeyGen LiveAvatar).
//
//   press Start
//     -> n8n webhook /liveavatar-session
//        -> POST https://api.liveavatar.com/v2/embeddings   (X-API-KEY lives in n8n)
//        -> returns a SHORT-LIVED embed URL
//   -> the page drops that URL into an <iframe> and you talk to the avatar
//
// The API key never reaches this page. The browser only gets a ticket — the same
// rule as the ElevenLabs (Lab 4) and Veo (Lab 10) labs.
//
// Note: HeyGen's old /v1/streaming.* API is SUNSET (off entirely by end of March
// 2026). LiveAvatar replaces it, and it needs its OWN key: a HeyGen API key is
// rejected with "Invalid API key".
// ---------------------------------------------------------------------------
const STORE_BASE = "lab9_n8n_base";
const DEFAULT_BASE = "http://localhost:5678/webhook";

const $ = (id) => document.getElementById(id);
const base = () => ($("baseUrl").value.trim() || DEFAULT_BASE).replace(/\/$/, "");

function setStatus(text, kind = "") {
  $("status").textContent = text;
  $("status").className = "statusline" + (kind ? " " + kind : "");
}

function showFrame(url) {
  $("avatarFrame").innerHTML =
    '<iframe allow="microphone; autoplay; clipboard-write; encrypted-media" allowfullscreen ' +
    'src="' + url.replace(/"/g, "&quot;") + '"></iframe>';
  $("startBtn").disabled = true;
  $("endBtn").disabled = false;
}

/* ── the API route: n8n mints the session ─────────────────────────────── */
async function startSession() {
  const avatar_id = $("avatarId").value.trim();
  if (!avatar_id) return setStatus("Enter an avatar id first.", "err");

  $("startBtn").disabled = true;
  setStatus("Asking n8n for a session…");

  try {
    const res = await fetch(`${base()}/liveavatar-session`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        avatar_id,
        context_id: $("context").value || undefined,
        orientation: "horizontal",
      }),
    });
    if (!res.ok) throw new Error(`n8n returned ${res.status} — is the Lab 9 flow published?`);
    const data = await res.json();
    if (!data.ok || !data.url) throw new Error(data.error || "LiveAvatar did not return an embed URL.");

    showFrame(data.url);
    setStatus("Live. Allow the microphone, then talk to Nova — this is burning credits.", "ok");
    localStorage.setItem(STORE_BASE, base());
  } catch (e) {
    $("startBtn").disabled = false;
    setStatus(`Could not start the session. ${e.message}`, "err");
  }
}

function endSession() {
  $("avatarFrame").innerHTML =
    '<div class="placeholder"><div class="dot"></div>' +
    "<p>Session ended. Press <strong>Start session</strong> to talk again.</p></div>";
  $("startBtn").disabled = false;
  $("endBtn").disabled = true;
  setStatus("Session ended — that embed URL is short-lived and is now spent.");
}

/* ── the fallback: paste a share/embed URL directly ───────────────────── */
function loadShareUrl() {
  const url = $("shareUrl").value.trim();
  if (!url) return setStatus("Paste a share or embed URL first.", "err");
  showFrame(url);
  setStatus("Loaded that URL directly — no n8n, no API key involved.", "ok");
  try { localStorage.setItem("heygen_ia_url", url); } catch {}
}

/* ── personas come from the account, through n8n ──────────────────────── */
async function loadContexts() {
  const sel = $("context");
  try {
    const res = await fetch(`${base()}/liveavatar-contexts`);
    const data = await res.json();
    const list = data.contexts || [];
    sel.innerHTML = '<option value="">Default persona</option>';
    list.forEach((c) => {
      const o = document.createElement("option");
      o.value = c.id;
      o.textContent = c.name;
      sel.appendChild(o);
    });
    if (!list.length) sel.innerHTML = '<option value="">No personas found — using the default</option>';
  } catch {
    sel.innerHTML = '<option value="">Could not reach n8n — check the webhook base</option>';
  }
}

window.addEventListener("DOMContentLoaded", () => {
  $("baseUrl").value = localStorage.getItem(STORE_BASE) || DEFAULT_BASE;
  const saved = localStorage.getItem("heygen_ia_url");
  if (saved) $("shareUrl").value = saved;
  loadContexts();
});

window.startSession = startSession;
window.endSession = endSession;
window.loadShareUrl = loadShareUrl;
