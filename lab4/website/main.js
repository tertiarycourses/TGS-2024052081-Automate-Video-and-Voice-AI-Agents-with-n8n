// ---------------------------------------------------------------------------
// Single-page app — no backend of its own. "Book by Voice" calls the n8n
// "Retell Web Call Trigger" flow, which creates a Retell web call (keeping the
// API key in n8n) and returns an access_token to start the WebRTC voice session.
// ---------------------------------------------------------------------------
const N8N_WEB_CALL_URL = "http://localhost:5678/webhook/retell-web-call";

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

async function startVoiceCall() {
  if (callActive) return;
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

    const res = await fetch(N8N_WEB_CALL_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });

    if (!res.ok) {
      throw new Error(`n8n webhook error ${res.status} — is the "Retell Web Call Trigger" workflow active?`);
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
