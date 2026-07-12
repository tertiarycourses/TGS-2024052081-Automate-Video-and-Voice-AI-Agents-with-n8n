// ---------------------------------------------------------------------------
// Lab 8 — Interactive avatar, rendered IN THE BROWSER.
//
//   🎙️ you speak
//     -> Web Speech API  (speech-to-text, in the browser, free)
//        -> n8n webhook  -> gemma4 writes a short spoken reply
//     -> speechSynthesis (text-to-speech, in the browser, free)
//     -> the mouth is drawn on the photo, live, at 60fps
//
// Nothing is uploaded, nothing is rendered in a cloud, nothing costs a credit.
// The trade-off is honest: the mouth is DRAWN GEOMETRY, not real pixels. Lab 9
// does the same conversation with HeyGen's photoreal streaming avatar — compare.
//
// The browser never captures TTS audio samples (the OS speaks it), so we cannot
// drive the mouth from a waveform. Instead the viseme timeline runs on a synthetic
// clock and is re-synced on every word `boundary` event.
// ---------------------------------------------------------------------------
const STORE_URL = "lab8_n8n_webhook";
const DEFAULT_URL = "http://localhost:5678/webhook/avatar-chat";

const $ = (id) => document.getElementById(id);
const webhook = () => (localStorage.getItem(STORE_URL) || DEFAULT_URL).trim();

const state = {
  image: null,
  rig: null,
  renderer: null,
  timeline: null,
  speaking: false,
  listening: false,
  t0: 0,
  duration: 0,
  sessionId: "web-" + Math.random().toString(36).slice(2),
  history: [],          // the browser owns the transcript; n8n stays stateless
  queue: [],            // sentences waiting to be spoken
  lastLatency: null,
};

/* ── settings ─────────────────────────────────────────────────────────── */
function openSettings() {
  $("webhookUrl").value = localStorage.getItem(STORE_URL) || DEFAULT_URL;
  $("settingsModal").classList.add("active");
}
function closeSettings() { $("settingsModal").classList.remove("active"); }
function saveSettings() {
  localStorage.setItem(STORE_URL, $("webhookUrl").value.trim() || DEFAULT_URL);
  closeSettings();
  setStatus(`Talking to ${webhook()}`);
}

function setStatus(text, kind = "") {
  $("status").textContent = text;
  $("status").className = "statusline" + (kind ? " " + kind : "");
}
function setPill(text, kind = "") {
  $("statePill").textContent = text;
  $("statePill").className = "pill" + (kind ? " " + kind : "");
}
function addMsg(who, text) {
  const el = document.createElement("div");
  el.className = "msg " + who;
  el.textContent = text;
  $("chat").appendChild(el);
  $("chat").scrollTop = $("chat").scrollHeight;
}

/* ── the face ─────────────────────────────────────────────────────────── */
async function loadFace(src, name) {
  setStatus("Loading the face…");
  const img = new Image();
  img.crossOrigin = "anonymous";
  await new Promise((res, rej) => {
    img.onload = res;
    img.onerror = () => rej(new Error("Could not load that image."));
    img.src = src;
  });

  state.image = img;

  // Face.autoDetect resolves to { rig, detected } — NOT a rig. Hand the renderer the
  // wrapper and every frame dies on `undefined.x`.
  let detected = false;
  try {
    const found = await Face.autoDetect(img);
    state.rig = found?.rig || Face.defaultRig(img);
    detected = !!found?.detected;
  } catch {
    state.rig = Face.defaultRig(img);
  }

  state.renderer.setImage(img, state.rig);
  $("stageEmpty").hidden = true;
  setStatus(
    detected
      ? `Face detected${name ? ` — ${name}` : ""}. Hold the mic and talk.`
      : "Face loaded, but the eyes/mouth were not detected — the jaw may look off.",
    detected ? "ok" : "",
  );
}

/* ── voices ───────────────────────────────────────────────────────────── */
function loadVoices() {
  const sel = $("voice");
  const voices = speechSynthesis.getVoices().filter((v) => v.lang.startsWith("en"));
  if (!voices.length) return;
  sel.innerHTML = "";
  voices.forEach((v, i) => {
    const o = document.createElement("option");
    o.value = i;
    o.textContent = `${v.name} — ${v.lang}`;
    sel.appendChild(o);
  });
}

/* ── speaking: TTS + the drawn mouth ──────────────────────────────────── */
// Speak a reply one SENTENCE at a time. The mouth starts on the first sentence
// instead of waiting for the whole paragraph to be ready — and an interrupted
// avatar can be cut off cleanly between sentences.
async function speakReply(text) {
  const sentences = text.match(/[^.!?]+[.!?]*/g) || [text];
  for (const s of sentences) {
    if (!state.speaking && state.interrupted) break;   // barge-in
    const line = s.trim();
    if (line) await speak(line);
  }
  state.interrupted = false;
}

function speak(text) {
  return new Promise((resolve) => {
    const voices = speechSynthesis.getVoices().filter((v) => v.lang.startsWith("en"));
    const u = new SpeechSynthesisUtterance(text);
    u.voice = voices[$("voice").value] || voices[0];
    u.rate = 1;

    // ~13 characters a second is a decent estimate of spoken English.
    state.duration = Math.max(1.2, text.length / 13);
    state.timeline = Visemes.buildTimeline(text, state.duration);
    state.t0 = performance.now() / 1000;
    state.speaking = true;
    setPill("Speaking", "speaking");
    $("stopBtn").disabled = false;

    // The browser never gives us the audio samples, so the clock is synthetic —
    // but it tells us when each WORD starts, and we snap the timeline to that.
    u.onboundary = (e) => {
      if (e.name !== "word" || !text.length) return;
      const fracThroughText = e.charIndex / text.length;
      const shouldBeAt = fracThroughText * state.duration;
      const isAt = performance.now() / 1000 - state.t0;
      state.t0 -= (shouldBeAt - isAt) * 0.5; // ease toward the truth, don't snap
    };

    u.onend = () => {
      state.speaking = false;
      state.timeline = null;
      setPill("Idle");
      $("stopBtn").disabled = true;
      resolve();
    };
    u.onerror = () => { u.onend(); };

    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  });
}

/* ── the render loop ──────────────────────────────────────────────────── */
function loop(now) {
  requestAnimationFrame(loop);
  if (!state.renderer || !state.image) return;

  const t = now / 1000;
  if (state.speaking && state.timeline) {
    const elapsed = t - state.t0;
    const shape = Visemes.sampleTimeline(state.timeline, elapsed);
    // A synthetic envelope: mouths do not open to full on every syllable.
    const level = 0.55 + 0.45 * Math.abs(Math.sin(elapsed * 9));
    state.renderer.draw(shape, level, t);
  } else {
    state.renderer.idle(t);
  }
}

/* ── the conversation ─────────────────────────────────────────────────── */
async function ask(message) {
  if (!message) return;
  const t0 = performance.now();
  addMsg("you", message);
  state.history.push({ role: "you", text: message });
  setPill("Thinking", "thinking");
  setStatus("gemma4 is thinking…");

  let reply;
  let timing = {};
  try {
    const res = await fetch(webhook(), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        sessionId: state.sessionId,
        history: state.history.slice(-6),   // n8n is stateless; the page owns the context
      }),
    });
    if (!res.ok) throw new Error(`n8n returned ${res.status} — is the Lab 8 flow published?`);
    const data = await res.json();
    reply = data.reply || data.output || "Sorry, I did not get a reply.";
    timing = data.timing || {};
  } catch (e) {
    setPill("Idle");
    setStatus(`Could not reach the n8n flow. ${e.message}`, "err");
    addMsg("bot", "I could not reach my brain — check the ⚙ webhook URL.");
    return;
  }

  addMsg("bot", reply);
  state.history.push({ role: "bot", text: reply });

  // Show where the time actually went — the lab measures latency, it does not claim it.
  const t = timing;
  const round = Math.round(performance.now() - t0);
  state.lastLatency = round;
  setStatus(
    `Replied in ${(round / 1000).toFixed(1)}s` +
      (t.generate_ms ? ` (model ${(t.total_ms / 1000).toFixed(1)}s, ${t.tokens} tokens)` : "") +
      " — speak any time to interrupt.",
    "ok",
  );

  await speakReply(reply);
}

/* ── listening (speech to text) ───────────────────────────────────────── */
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;

function toggleMic() {
  if (!SR) {
    setStatus("This browser has no speech recognition. Use Chrome or Edge — or type below.", "err");
    return;
  }
  if (!state.image) {
    setStatus("Pick a face first.", "err");
    return;
  }
  if (state.listening) { recognition?.stop(); return; }

  recognition = new SR();
  recognition.lang = "en-SG";
  // Interim results give us BARGE-IN: the moment the user starts talking we cut Aria
  // off, exactly as you would interrupt a person. Waiting politely for her to finish
  // is what makes a voice agent feel dead.
  recognition.interimResults = true;
  recognition.continuous = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    state.listening = true;
    $("micBtn").classList.add("live");
    $("micLabel").textContent = "Listening… (click to stop)";
    setPill("Listening", "listening");
    setStatus("Listening…");
  };
  recognition.onresult = (e) => {
    const last = e.results[e.results.length - 1];

    // Barge-in: any speech at all silences the avatar immediately.
    if (state.speaking) {
      state.interrupted = true;
      speechSynthesis.cancel();
      state.speaking = false;
      state.timeline = null;
      setPill("Listening", "listening");
    }

    if (!last.isFinal) return;          // interim — keep listening
    ask(last[0].transcript);
  };
  recognition.onerror = (e) => {
    setStatus(
      e.error === "not-allowed"
        ? "Microphone blocked. Allow it in the address bar, and use http://localhost."
        : `Speech recognition error: ${e.error}`,
      "err",
    );
  };
  recognition.onend = () => {
    state.listening = false;
    $("micBtn").classList.remove("live");
    $("micLabel").textContent = "Hold to talk";
    if (!state.speaking) setPill("Idle");
  };

  speechSynthesis.cancel();   // do not listen to ourselves
  recognition.start();
}

function stopAll() {
  speechSynthesis.cancel();
  recognition?.stop();
  state.speaking = false;
  state.timeline = null;
  setPill("Idle");
  $("stopBtn").disabled = true;
}

/* ── wiring ───────────────────────────────────────────────────────────── */
window.addEventListener("DOMContentLoaded", () => {
  state.renderer = new Renderer($("stage"));
  requestAnimationFrame(loop);

  document.querySelectorAll(".face[data-sample]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".face").forEach((b) => b.classList.remove("is-on"));
      btn.classList.add("is-on");
      loadFace(`samples/${btn.dataset.sample}.jpg`, btn.dataset.sample);
    });
  });

  $("fileInput").addEventListener("change", (e) => {
    const f = e.target.files?.[0];
    if (f) loadFace(URL.createObjectURL(f), f.name);
  });

  $("typedForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const v = $("typed").value.trim();
    $("typed").value = "";
    ask(v);
  });

  loadVoices();
  speechSynthesis.onvoiceschanged = loadVoices;

  // Warm the model. gemma4 is 9.6 GB; if it is not resident, the FIRST reply pays a
  // multi-second load tax and the demo looks broken. This costs one throwaway call.
  fetch(webhook(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: "hello", warm: true, sessionId: "warmup" }),
  }).then(() => setStatus("Aria is warm. Hold the mic and talk.", "ok")).catch(() => {});

  // Start on the first sample so the page is never a blank stage.
  document.querySelector(".face[data-sample]")?.click();
});

window.toggleMic = toggleMic;
window.stopAll = stopAll;
window.openSettings = openSettings;
window.closeSettings = closeSettings;
window.saveSettings = saveSettings;
