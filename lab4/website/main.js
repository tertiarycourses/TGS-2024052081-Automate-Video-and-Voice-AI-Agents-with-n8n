// ---------------------------------------------------------------------------
// Single-page app — no backend of its own. "Book by Voice" calls the n8n
// "Retell Web Call Trigger" flow, which creates a Retell web call (keeping the
// API key in n8n) and returns an access_token to start the WebRTC voice session.
//
// NOTHING IS HARDCODED. Each learner points this page at their own n8n and
// their own Retell agent via the ⚙ Settings panel; both values are saved in
// this browser only (localStorage).
// ---------------------------------------------------------------------------
const STORE = {
  url: "gg_n8n_web_call_url",   // n8n "Retell Web Call Trigger" production webhook URL
  agent: "gg_retell_agent_id",  // optional: your own Retell agent_… ID
};
const URL_EXAMPLE = "http://localhost:5678/webhook/retell-web-call";

const getWebhookUrl = () => (localStorage.getItem(STORE.url) || "").trim();
const getAgentId = () => (localStorage.getItem(STORE.agent) || "").trim();

// The Retell SDK is loaded lazily (only when a call starts) so that a slow or
// blocked CDN never stops the rest of the page (buttons) from working.
async function loadRetellClient() {
  const mod = await import("https://cdn.jsdelivr.net/npm/retell-client-js-sdk@2.0.7/+esm");
  return new mod.RetellWebClient();
}

// ===========================================================================
// Voice — Retell via n8n
// ===========================================================================
let retellClient = null; // created on first call via loadRetellClient()
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

function attachRetellEvents(client) {
  client.on("call_started", () => {
    callActive = true;
    setStatus("Speaking with Nina…");
    callSeconds = 0;
    timerInterval = setInterval(updateTimer, 1000);
  });
  client.on("call_ended", () => {
    callActive = false;
    setStatus("Call ended");
    setTalking(false);
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = null;
    setTimeout(hideModal, 1500);
  });
  client.on("agent_start_talking", () => setTalking(true));
  client.on("agent_stop_talking", () => setTalking(false));
  client.on("error", (e) => {
    console.error("Retell error:", e);
    callActive = false;
    setStatus("An error occurred. Please try again.");
    setTalking(false);
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = null;
    setTimeout(hideModal, 2500);
  });
}

// ===========================================================================
// Settings — the learner's own n8n webhook URL + Retell agent ID
// ===========================================================================
function openSettings() {
  $("settingsUrl").value = getWebhookUrl();
  $("settingsUrl").placeholder = URL_EXAMPLE;
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

// Tells the learner, before they click anything, that the page is not wired up yet.
function renderSetupBanner() {
  const banner = $("setupBanner");
  if (!banner) return;
  banner.style.display = getWebhookUrl() ? "none" : "block";
}

async function startVoiceCall() {
  if (callActive) return;

  // No webhook yet → send the learner to Settings instead of failing cryptically.
  const webhookUrl = getWebhookUrl();
  if (!webhookUrl) {
    openSettings();
    return;
  }

  showModal();
  setStatus("Connecting…");
  setTalking(false);
  callSeconds = 0;
  $("voiceTimer").textContent = "00:00";

  try {
    // load the Retell SDK on first use; if the CDN is blocked this fails gracefully
    if (!retellClient) {
      retellClient = await loadRetellClient();
      attachRetellEvents(retellClient);
    }

    // agent_id is optional: the n8n flow falls back to its own configured agent.
    const agentId = getAgentId();
    const res = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(agentId ? { agent_id: agentId } : {}),
    });

    if (!res.ok) {
      throw new Error(`n8n webhook error ${res.status} — is the "Retell Web Call Trigger" workflow active, and is the ⚙ URL correct?`);
    }

    const data = await res.json();

    if (!data.access_token) {
      // n8n passes Retell's own error message through (e.g. quota exceeded)
      throw new Error(data.message || data.error?.message || "No access token received");
    }

    await retellClient.startCall({ accessToken: data.access_token });
  } catch (e) {
    console.error("Voice call error:", e);
    setStatus(`Connection failed: ${e.message}`);
    setTimeout(hideModal, 3500);
  }
}

function endVoiceCall() {
  try {
    if (retellClient) retellClient.stopCall();
  } catch (e) {
    console.error("Error stopping call:", e);
  }
  callActive = false;
  setTalking(false);
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = null;
  hideModal();
}

// Expose handlers to inline onclick attributes
window.startVoiceCall = startVoiceCall;
window.endVoiceCall = endVoiceCall;
window.openSettings = openSettings;
window.closeSettings = closeSettings;
window.saveSettings = saveSettings;

renderSetupBanner();
