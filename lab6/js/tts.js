/* Speech synthesis.
 *
 * Two shapes of engine, and the difference matters:
 *   · Browser TTS speaks straight out of the OS. The page never sees the
 *     samples, so it can drive a live preview but can NOT be recorded.
 *   · Everything else returns an audio Blob, which we can decode, analyse and
 *     mux into an exported video.
 * Cloud calls go through the local proxy (server.js) because neither
 * ElevenLabs nor OpenAI sends CORS headers a browser will accept. */

(function (global) {
  'use strict';

  const PROXY = '/api';

  /* ── browser (offline, preview only) ─────────────────────────────── */

  function listVoices() {
    return new Promise((resolve) => {
      const voices = speechSynthesis.getVoices();
      if (voices.length) return resolve(voices);
      // Chrome populates the list asynchronously on first call.
      speechSynthesis.addEventListener('voiceschanged', () => resolve(speechSynthesis.getVoices()), { once: true });
      setTimeout(() => resolve(speechSynthesis.getVoices()), 1000);
    });
  }

  function speakBrowser(text, { voiceURI, rate = 1, pitch = 1, onBoundary, onEnd, onStart } = {}) {
    speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);
    const voice = speechSynthesis.getVoices().find((v) => v.voiceURI === voiceURI);
    if (voice) utter.voice = voice;
    utter.rate = rate;
    utter.pitch = pitch;

    utter.onstart = () => onStart && onStart();
    utter.onboundary = (e) => onBoundary && onBoundary(e.charIndex, e.elapsedTime);
    utter.onend = () => onEnd && onEnd();
    utter.onerror = (e) => {
      // 'interrupted'/'canceled' are what Stop looks like — not failures.
      if (e.error !== 'interrupted' && e.error !== 'canceled') console.warn('TTS error:', e.error);
      onEnd && onEnd();
    };

    speechSynthesis.speak(utter);
    return { cancel: () => speechSynthesis.cancel() };
  }

  /* Browser TTS gives no duration up front, so estimate one to drive the
   * viseme clock. ~2.9 syllables/sec at rate 1 is close for most voices. */
  function estimateDuration(text, rate = 1) {
    const syllables = String(text)
      .toLowerCase()
      .split(/\s+/)
      .filter(Boolean)
      .reduce((n, w) => n + Math.max(1, (w.match(/[aeiouy]+/g) || []).length), 0);
    return Math.max(0.6, (syllables / 2.9) / rate);
  }

  /* ── blob-returning engines ──────────────────────────────────────── */

  async function synthesize(engine, text, opts = {}) {
    const routes = {
      elevenlabs: () => post(`${PROXY}/tts/elevenlabs`, { text, apiKey: opts.apiKey, voiceId: opts.voiceId }),
      openai:     () => post(`${PROXY}/tts/openai`,     { text, apiKey: opts.apiKey, voice: opts.voice }),
      gemini:     () => post(`${PROXY}/tts/gemini`,     { text, apiKey: opts.apiKey, voice: opts.voice }),
      piper:      () => post(`${PROXY}/tts/piper`,      { text, baseUrl: opts.baseUrl, voice: opts.voice }),
    };
    const call = routes[engine];
    if (!call) throw new Error(`Unknown TTS engine: ${engine}`);
    return call();
  }

  /* Instant voice cloning. The clip can be a video — the proxy strips the audio
   * track with ffmpeg before anything is sent onward. Returns a voice ID usable
   * as the ElevenLabs voice immediately. */
  async function cloneVoice({ file, name, apiKey }) {
    let res;
    try {
      res = await fetch(`${PROXY}/voice/clone`, {
        method: 'POST',
        headers: {
          'Content-Type': file.type || 'application/octet-stream',
          'X-Api-Key': apiKey,
          'X-Voice-Name': name,
        },
        body: file,
      });
    } catch {
      throw new Error('Cannot reach the local proxy. Voice cloning needs `npm start`.');
    }

    const text = await res.text();
    let json = {};
    try { json = JSON.parse(text); } catch { /* fall through to the status check */ }

    if (!res.ok) {
      const msg = json.detail?.message || json.detail || json.message || text.slice(0, 200) || res.statusText;
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }
    if (!json.voice_id) throw new Error('ElevenLabs accepted the clip but returned no voice_id.');
    return json.voice_id;
  }

  async function post(url, body) {
    let res;
    try {
      res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
    } catch {
      throw new Error('Cannot reach the local proxy. Start it with `npm start` and open the app from http://localhost:8080.');
    }

    if (!res.ok) {
      const detail = await res.text().catch(() => '');
      throw new Error(`${res.status} ${res.statusText}${detail ? ` — ${detail.slice(0, 200)}` : ''}`);
    }
    return res.blob();
  }

  global.TTS = { listVoices, speakBrowser, estimateDuration, synthesize, cloneVoice };
})(window);
