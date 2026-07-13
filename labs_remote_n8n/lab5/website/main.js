// ---------------------------------------------------------------------------
// MediRefill — "Ask Ava" prescription refill voice agent (Lab 5), built on the Vapi Web SDK.
//
// Vapi differs from the ElevenLabs lab on purpose, and the difference IS the lesson:
//   ElevenLabs (Lab 4)  browser -> n8n -> signed URL -> WebSocket (ElevenLabs runs the model)
//                   (a PRIVATE key must be kept server-side, so n8n mints the call)
//   Vapi   (Lab 4b) browser -> Vapi directly, using a PUBLIC key
//                   (a public key can ONLY start calls, so it is safe in the page)
//
// Nothing is hardcoded: the learner adds their own public key + assistant ID via
// the ⚙ Settings panel, saved in this browser only (localStorage).
// ---------------------------------------------------------------------------
const STORE = {
  key: "medirefill_vapi_public_key",
  assistant: "medirefill_vapi_assistant_id",
};

const getKey = () => (localStorage.getItem(STORE.key) || "").trim();
const getAssistant = () => (localStorage.getItem(STORE.assistant) || "").trim();

const $ = (id) => document.getElementById(id);

// The SDK is loaded lazily so a slow/blocked CDN never stops the rest of the page.
// The CDN's ESM build wraps the CommonJS default export twice, so the constructor
// can sit at mod.default.default. Unwrap until we actually find the function.
async function loadVapi() {
  const mod = await import("https://cdn.jsdelivr.net/npm/@vapi-ai/web@2.3.8/+esm");
  const Vapi = [mod.default?.default, mod.default, mod.Vapi, mod].find(
    (candidate) => typeof candidate === "function",
  );
  if (!Vapi) throw new Error("Could not find the Vapi constructor in the SDK module");
  return new Vapi(getKey());
}

// ===========================================================================
// Settings
// ===========================================================================
function openSettings() {
  $("settingsKey").value = getKey();
  $("settingsAssistant").value = getAssistant();
  $("settingsModal").classList.add("active");
  setTimeout(() => $("settingsKey").focus(), 50);
}
function closeSettings() {
  $("settingsModal").classList.remove("active");
}
function saveSettings() {
  localStorage.setItem(STORE.key, $("settingsKey").value.trim());
  localStorage.setItem(STORE.assistant, $("settingsAssistant").value.trim());
  vapi = null; // rebuild the client with the new key on the next call
  closeSettings();
  renderSetupBanner();
}
function renderSetupBanner() {
  $("setupBanner").style.display = getKey() && getAssistant() ? "none" : "block";
}

// ===========================================================================
// Voice call
// ===========================================================================
let vapi = null;
let callActive = false;
let timerInterval = null;
let callSeconds = 0;

function setStatus(text) { $("voiceStatus").textContent = text; }
function setTalking(on) { $("pulse").classList.toggle("talking", on); }
function showModal() { $("voiceModal").classList.add("active"); }
function hideModal() { $("voiceModal").classList.remove("active"); }

function updateTimer() {
  callSeconds++;
  const m = String(Math.floor(callSeconds / 60)).padStart(2, "0");
  const s = String(callSeconds % 60).padStart(2, "0");
  $("voiceTimer").textContent = `${m}:${s}`;
}

function addTranscript(role, text) {
  const el = document.createElement("div");
  el.className = role === "user" ? "you" : "";
  el.textContent = `${role === "user" ? "You" : "Ava"}: ${text}`;
  $("transcript").appendChild(el);
  $("transcript").scrollTop = $("transcript").scrollHeight;
}

function attachEvents(client) {
  client.on("call-start", () => {
    callActive = true;
    setStatus("Listening — go ahead and ask.");
    callSeconds = 0;
    timerInterval = setInterval(updateTimer, 1000);
  });
  client.on("call-end", () => {
    callActive = false;
    setStatus("Call ended");
    setTalking(false);
    clearInterval(timerInterval);
    timerInterval = null;
    setTimeout(hideModal, 1500);
  });
  client.on("speech-start", () => setTalking(true));
  client.on("speech-end", () => setTalking(false));

  // Live transcript: proof to the learner that grounding worked (or did not).
  client.on("message", (msg) => {
    if (msg?.type === "transcript" && msg.transcriptType === "final") {
      addTranscript(msg.role, msg.transcript);
    }
  });
  client.on("error", (e) => {
    console.error("Vapi error:", e);
    callActive = false;
    setStatus(`Call failed: ${e?.errorMsg || e?.message || "check your public key and assistant ID"}`);
    setTalking(false);
    clearInterval(timerInterval);
    setTimeout(hideModal, 3500);
  });
}

async function startVoiceCall() {
  if (callActive) return;

  // Not configured yet -> send the learner to Settings instead of failing cryptically.
  if (!getKey() || !getAssistant()) {
    openSettings();
    return;
  }

  $("transcript").innerHTML = "";
  $("voiceTimer").textContent = "00:00";
  showModal();
  setStatus("Connecting…");

  try {
    if (!vapi) {
      vapi = await loadVapi();
      attachEvents(vapi);
    }
    await vapi.start(getAssistant());
  } catch (e) {
    console.error("Could not start the call:", e);
    setStatus(`Connection failed: ${e.message}`);
    setTimeout(hideModal, 3500);
  }
}

function endVoiceCall() {
  try {
    if (vapi) vapi.stop();
  } catch (e) {
    console.error("Error stopping the call:", e);
  }
  callActive = false;
  setTalking(false);
  clearInterval(timerInterval);
  timerInterval = null;
  hideModal();
}

window.startVoiceCall = startVoiceCall;
window.endVoiceCall = endVoiceCall;
window.openSettings = openSettings;
window.closeSettings = closeSettings;
window.saveSettings = saveSettings;

renderSetupBanner();
