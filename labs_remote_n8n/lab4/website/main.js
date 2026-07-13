// ---------------------------------------------------------------------------
// Single-page app — no backend of its own. "Book by Voice" calls the n8n
// "ElevenLabs Web Call Trigger" flow, which asks ElevenLabs for a SIGNED URL
// (keeping the xi-api-key inside n8n) and returns it. The browser then opens a
// WebSocket straight to that signed URL to run the voice session.
//
// The page defaults to the remote n8n, so it works as soon as the
// "ElevenLabs Web Call Trigger" workflow is ACTIVE. Point it somewhere else via
// ⚙ Settings; that override is saved in this browser only (localStorage), as is
// the optional agent ID.
// ---------------------------------------------------------------------------
const STORE = {
  url: "gg_n8n_web_call_url",   // n8n "ElevenLabs Web Call Trigger" production webhook URL
  agent: "gg_elevenlabs_agent_id",  // optional: your own ElevenLabs agent ID
};

// Matches the `path` of the Webhook node in elevenlabs-web-call-flow.json. The browser
// calls this itself, so this URL only has to be reachable from the page — it is the calls
// that ElevenLabs' SERVERS make (the booking tools) that need a public ngrok URL.
const DEFAULT_WEBHOOK_URL = "https://n8n.tertiarytraining.com/webhook/elevenlabs-web-call";

const getWebhookUrl = () =>
  (localStorage.getItem(STORE.url) || "").trim() || DEFAULT_WEBHOOK_URL;
const getAgentId = () => (localStorage.getItem(STORE.agent) || "").trim();

// The ElevenLabs SDK is loaded lazily (only when a call starts) so that a slow or
// blocked CDN never stops the rest of the page (buttons) from working.
async function loadElevenLabs() {
  const mod = await import("https://cdn.jsdelivr.net/npm/@elevenlabs/client@0.1.4/+esm");
  return mod.Conversation;
}

// ===========================================================================
// Voice — ElevenLabs Conversational AI via n8n
// ===========================================================================
let conversation = null; // the active ElevenLabs session
let callActive = false;
let timerInterval = null;
let callSeconds = 0;

const $ = (id) => document.getElementById(id);

function showModal() {
  $("voiceModal").classList.add("active");
  document.body.style.overflow = "hidden";
}
function hideModal() {
  $("voiceModal").classList.remove("active");
  document.body.style.overflow = "";
}
function setStatus(text) {
  $("voiceStatus").textContent = text;
}
function setTalking(on) {
  $("pulse").classList.toggle("talking", on);
}
function updateTimer() {
  callSeconds++;
  const m = String(Math.floor(callSeconds / 60)).padStart(2, "0");
  const s = String(callSeconds % 60).padStart(2, "0");
  $("voiceTimer").textContent = `${m}:${s}`;
}

function onCallStarted() {
  callActive = true;
  setStatus("Speaking with Nina…");
  callSeconds = 0;
  timerInterval = setInterval(updateTimer, 1000);
}

function onCallEnded() {
  callActive = false;
  conversation = null;
  setStatus("Call ended");
  setTalking(false);
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = null;
  setTimeout(hideModal, 1500);
}

// ===========================================================================
// Settings — the learner's own n8n webhook URL + ElevenLabs agent ID
// ===========================================================================
function openSettings() {
  $("settingsUrl").value = getWebhookUrl();
  $("settingsUrl").placeholder = DEFAULT_WEBHOOK_URL;
  $("settingsAgent").value = getAgentId();
  $("settingsModal").classList.add("active");
  setTimeout(() => $("settingsUrl").focus(), 50);
}

function closeSettings() {
  $("settingsModal").classList.remove("active");
}

function saveSettings() {
  localStorage.setItem(STORE.url, $("settingsUrl").value.trim());
  localStorage.setItem(STORE.agent, $("settingsAgent").value.trim());
  closeSettings();
  renderSetupBanner();
}

// A URL always exists (the default), so "have you pasted one?" is not the useful
// question — "is n8n actually answering?" is. Probe it before the learner clicks
// anything, so a dead stack shows up here and not as a failed call.
//
// no-cors gives us an opaque response we cannot read, which is fine: we only care
// whether the request reached a server at all. It throws on connection refused, and
// resolves on any HTTP reply — including the 404 n8n returns for a GET on a POST
// webhook. Reachability is the signal; the status code is not.
async function renderSetupBanner() {
  const banner = $("setupBanner");
  if (!banner) return;
  const url = getWebhookUrl();

  let reachable = true;
  try {
    await fetch(url, { method: "GET", mode: "no-cors" });
  } catch {
    reachable = false;
  }

  banner.innerHTML = reachable
    ? ""
    : `⚙️ Cannot reach n8n at <strong>${url}</strong> — check you are online and make sure the ` +
      `<strong>ElevenLabs Web Call Trigger</strong> workflow is <strong>Active</strong>, ` +
      `or click <strong>⚙ Settings</strong> to point elsewhere.`;
  banner.style.display = reachable ? "none" : "block";
}

async function startVoiceCall() {
  if (callActive) return;

  // Always set: the ⚙ Settings override if the learner saved one, else the default.
  const webhookUrl = getWebhookUrl();

  showModal();
  setStatus("Connecting…");
  setTalking(false);
  callSeconds = 0;
  $("voiceTimer").textContent = "00:00";

  try {
    // The browser must be allowed to use the mic BEFORE the session opens, otherwise
    // ElevenLabs connects to a silent stream and Nina waits for a caller who never speaks.
    await navigator.mediaDevices.getUserMedia({ audio: true });

    const Conversation = await loadElevenLabs();

    // agent_id is optional: the n8n flow falls back to its own configured agent.
    const agentId = getAgentId();
    const res = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(agentId ? { agent_id: agentId } : {}),
    });

    if (!res.ok) {
      throw new Error(`n8n webhook error ${res.status} — is the "ElevenLabs Web Call Trigger" workflow active, and is the ⚙ URL correct?`);
    }

    const data = await res.json();

    // n8n passes ElevenLabs' own error through (e.g. bad agent id, quota exceeded).
    const signedUrl = data.signed_url;
    if (!signedUrl) {
      throw new Error(data.detail?.message || data.message || "No signed URL received from ElevenLabs");
    }

    conversation = await Conversation.startSession({
      signedUrl,
      onConnect: onCallStarted,
      onDisconnect: onCallEnded,
      onError: (e) => {
        console.error("ElevenLabs error:", e);
        setStatus("An error occurred. Please try again.");
        setTalking(false);
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = null;
        setTimeout(hideModal, 2500);
      },
      // "speaking" = the agent is talking; "listening" = waiting on the caller.
      onModeChange: ({ mode }) => setTalking(mode === "speaking"),
    });
  } catch (e) {
    console.error("Voice call error:", e);
    const msg = e.name === "NotAllowedError"
      ? "Microphone blocked — allow mic access and try again."
      : `Connection failed: ${e.message}`;
    setStatus(msg);
    setTimeout(hideModal, 3500);
  }
}

async function endVoiceCall() {
  if (conversation) await conversation.endSession();
  onCallEnded();
}
