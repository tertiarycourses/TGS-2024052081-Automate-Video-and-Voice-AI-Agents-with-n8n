/* Glue: files in, audio + viseme track out, frames on the canvas.
 *
 * Two playback paths, because the two families of TTS engine are genuinely
 * different animals:
 *
 *   blob path  — real audio in an <audio> element. An AnalyserNode gives us the
 *                loudness envelope, so the mouth follows the actual waveform and
 *                the clock is the audio's own currentTime. Recordable.
 *   speech path — browser TTS. No samples, no analyser. We run a synthetic clock
 *                and a synthetic envelope, and re-sync on every word `boundary`
 *                event so drift never accumulates. Not recordable. */

(function () {
  'use strict';

  /* This app has to be SERVED, not opened off the disk. Double-clicked as a
   * file:// URL the page still paints — <img> tags load, so the sample
   * thumbnails appear — but every fetch() is blocked by CORS, so the samples,
   * the TTS proxy and the renderers all die at the first click. Detect it once
   * and say so, instead of letting each feature fail with its own vague error. */
  const SERVED_OVER_HTTP = location.protocol === 'http:' || location.protocol === 'https:';
  const FILE_URL_HINT =
    'Open the app at http://localhost:8137 — it cannot run from a file:// URL. ' +
    'Start it with start.command (macOS) or start.bat (Windows).';

  const $ = (id) => document.getElementById(id);

  const el = {
    avatarDrop: $('avatarDrop'), avatarFile: $('avatarFile'),
    btnEditFace: $('btnEditFace'), btnAutoFace: $('btnAutoFace'), faceHint: $('faceHint'),
    script: $('script'), scriptFile: $('scriptFile'), scriptStats: $('scriptStats'),
    ttsEngine: $('ttsEngine'), voice: $('voice'), rate: $('rate'), pitch: $('pitch'),
    rateVal: $('rateVal'), pitchVal: $('pitchVal'),
    piperUrl: $('piperUrl'), piperVoice: $('piperVoice'),
    elKey: $('elKey'), elVoice: $('elVoice'), oaKey: $('oaKey'), oaVoice: $('oaVoice'),
    gmKey: $('gmKey'), gmVoice: $('gmVoice'),
    elPreset: $('elPreset'), elCustomField: $('elCustomField'),
    btnPreviewGm: $('btnPreviewGm'), btnPreviewEl: $('btnPreviewEl'),
    btnDraft: $('btnDraft'), ollamaModel: $('ollamaModel'),
    audioDrop: $('audioDrop'), audioFile: $('audioFile'),
    lipEngine: $('lipEngine'), gain: $('gain'), smooth: $('smooth'),
    gainVal: $('gainVal'), smoothVal: $('smoothVal'),
    optFrame: $('optFrame'), optSway: $('optSway'),
    optBreath: $('optBreath'), optDebug: $('optDebug'),
    cloneDrop: $('cloneDrop'), cloneFile: $('cloneFile'), cloneName: $('cloneName'),
    btnClone: $('btnClone'), cloneStatus: $('cloneStatus'),
    hgKey: $('hgKey'), hgVoice: $('hgVoice'), hgStatus: $('hgStatus'),
    hgAvatar: $('hgAvatar'), btnHgUpload: $('btnHgUpload'),
    stage: $('stage'), stageEmpty: $('stageEmpty'), hgVideo: $('hgVideo'),
    visemeReadout: $('visemeReadout'),
    btnSpeak: $('btnSpeak'), btnStop: $('btnStop'), btnRender: $('btnRender'),
    btnPhotoreal: $('btnPhotoreal'),
    engineNote: $('engineNote'),
    btnGetWeights: $('btnGetWeights'),
    loopVideo: $('loopVideo'),
    meterFill: $('meterFill'), scrubber: $('scrubber'), timeLabel: $('timeLabel'),
    statusLine: $('statusLine'), engineBadge: $('engineBadge'),
    faceDialog: $('faceDialog'), faceCanvas: $('faceCanvas'), helpDialog: $('helpDialog'),
    btnHelp: $('btnHelp'),
  };

  const state = {
    image: null,
    imageFile: null,
    rig: null,
    audioBlob: null,
    audioUrl: null,
    uploadedAudio: null,   // File, when the user brings their own
    timeline: null,
    playing: false,
    mode: null,            // 'blob' | 'speech'
    clock: 0,              // seconds, speech path only
    lastFrame: 0,
    peak: 0.15,            // running loudness peak, for auto-normalising the meter
    recording: false,
  };

  const renderer = new Renderer(el.stage);

  /* ── audio graph. Built once, lazily: browsers require a user gesture. ── */
  const audio = {
    ctx: null, elem: null, source: null, analyser: null, dest: null, data: null,
  };

  function ensureAudioGraph() {
    if (audio.ctx) return;

    audio.ctx = new (window.AudioContext || window.webkitAudioContext)();
    audio.elem = new Audio();
    audio.elem.crossOrigin = 'anonymous';

    audio.source = audio.ctx.createMediaElementSource(audio.elem);
    audio.analyser = audio.ctx.createAnalyser();
    audio.analyser.fftSize = 1024;
    audio.analyser.smoothingTimeConstant = 0.5;
    audio.data = new Uint8Array(audio.analyser.fftSize);

    // Split: to the speakers, and to a stream we can hand to MediaRecorder.
    audio.dest = audio.ctx.createMediaStreamDestination();
    audio.source.connect(audio.analyser);
    audio.analyser.connect(audio.ctx.destination);
    audio.analyser.connect(audio.dest);

    audio.elem.addEventListener('ended', () => stop());
    audio.elem.addEventListener('timeupdate', updateScrub);
  }

  /* RMS of the current window, normalised against a decaying peak so a quiet
   * recording still opens the mouth as far as a loud one. */
  function currentLevel() {
    if (!audio.analyser) return 0;
    audio.analyser.getByteTimeDomainData(audio.data);

    let sum = 0;
    for (let i = 0; i < audio.data.length; i++) {
      const v = (audio.data[i] - 128) / 128;
      sum += v * v;
    }
    const rms = Math.sqrt(sum / audio.data.length);

    state.peak = Math.max(rms, state.peak * 0.999);
    return Math.min(1, rms / Math.max(0.08, state.peak * 0.75));
  }

  /* ── the render loop ─────────────────────────────────────────────── */
  function loop(now) {
    requestAnimationFrame(loop);
    const dt = Math.min(0.1, (now - state.lastFrame) / 1000 || 0);
    state.lastFrame = now;

    if (!state.image) return;

    if (!state.playing) {
      renderer.idle(now / 1000);
      setMeter(0);
      return;
    }

    let t, level;
    if (state.mode === 'blob') {
      t = audio.elem.currentTime;
      level = currentLevel();
    } else {
      state.clock += dt;
      t = state.clock;
      const shape = Visemes.sampleTimeline(state.timeline, t);
      // No waveform to analyse — fake a plausible envelope from the track itself.
      level = shape.viseme === 'sil' ? 0.02 : 0.62 + 0.25 * Math.sin(t * 19);
    }

    const shape = Visemes.sampleTimeline(state.timeline, t);
    renderer.draw(shape, level, now / 1000);
    setMeter(level);

    el.visemeReadout.hidden = false;
    el.visemeReadout.firstElementChild.textContent = `${shape.viseme}  ${t.toFixed(2)}s`;
  }
  requestAnimationFrame(loop);


  /* ── render progress ──────────────────────────────────────────────
     Wav2Lip and MuseTalk report a real percentage. HeyGen does NOT — it only says
     processing/completed — so for HeyGen we estimate from elapsed time and cap at
     95%, reaching 100% only when the video actually arrives. A bar that sits at
     100% while still spinning is a lie. */
  const rp = {
    box: document.getElementById('renderProg'),
    fill: document.getElementById('rpFill'),
    label: document.getElementById('rpLabel'),
    pct: document.getElementById('rpPct'),
    timer: null,
    startedAt: 0,
  };

  function showRenderProgress(engine) {
    rp.box.hidden = false;
    rp.startedAt = Date.now();
    setRenderProgress(0, `${engine}: starting…`);
  }

  function setRenderProgress(pct, label, kind = '') {
    const p = Math.max(0, Math.min(100, Math.round(pct)));
    rp.fill.style.width = `${p}%`;
    rp.fill.className = `rp-fill ${kind}`;
    rp.pct.textContent = `${p}%`;
    if (label) rp.label.textContent = label;
  }

  // HeyGen gives no percentage, so estimate: ease toward 95% over ~90s.
  function startHeyGenEstimate() {
    clearInterval(rp.timer);
    rp.timer = setInterval(() => {
      const s = (Date.now() - rp.startedAt) / 1000;
      const frac = 1 - Math.exp(-s / 45);
      setRenderProgress(frac * 95, `HeyGen is rendering… ${Math.round(s)}s elapsed (usually 1–3 min)`);
    }, 500);
  }

  function finishRenderProgress(ok, msg) {
    clearInterval(rp.timer);
    rp.timer = null;
    setRenderProgress(100, msg, ok ? 'done' : 'error');
    if (!ok) return;
    setTimeout(() => { rp.box.hidden = true; }, 4000);
  }

  const setMeter = (v) => { el.meterFill.style.width = `${Math.round(v * 100)}%`; };

  /* ── avatar ──────────────────────────────────────────────────────── */
  async function loadAvatar(file) {
    if (!file || !file.type.startsWith('image/')) return status('That file is not an image.', 'err');

    const url = URL.createObjectURL(file);
    const img = new Image();
    await new Promise((res, rej) => {
      img.onload = res;
      img.onerror = () => rej(new Error('Could not decode that image.'));
      img.src = url;
    }).catch((e) => status(e.message, 'err'));
    if (!img.naturalWidth) return;

    state.image = img;
    state.imageFile = file;

    el.stageEmpty.hidden = true;
    el.avatarDrop.classList.add('has-file');
    el.avatarDrop.querySelector('strong').textContent = file.name;
    el.btnEditFace.disabled = false;
    el.btnAutoFace.disabled = false;

    // Draw immediately on the default rig, then refine once the model answers —
    // loading ~13 MB of WASM the first time shouldn't leave a blank stage.
    state.rig = Face.defaultRig(img.naturalWidth, img.naturalHeight);
    renderer.setImage(img, state.rig);
    refreshButtons();
    status('Finding the face…');

    await applyDetection(img);
  }

  async function applyDetection(img) {
    const { rig, detected, reason } = await Face.autoDetect(img);
    state.rig = rig;
    renderer.setRig(rig);

    el.faceHint.textContent = detected
      ? 'Face detected — eyes and mouth corners placed. Fine-tune with “Adjust mouth & eyes” if the lips look off.'
      : 'No face detected — open “Adjust mouth & eyes” and drag the handles onto the eyes and mouth corners.';

    status(
      detected
        ? `Avatar ready (${img.naturalWidth}×${img.naturalHeight}) — face detected.`
        : `Avatar loaded, but no face was detected${reason ? ` (${reason})` : ''}. Place the rig by hand.`,
      detected ? 'ok' : 'err'
    );
  }

  /* ── script ──────────────────────────────────────────────────────── */
  function updateScriptStats() {
    const text = el.script.value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    const secs = TTS.estimateDuration(text || '', parseFloat(el.rate.value));
    el.scriptStats.textContent = `${words} words · ~${fmt(secs)}`;
    // Any script edit invalidates the synthesised audio.
    state.audioBlob = null;
    state.timeline = null;
    refreshButtons();
  }

  /* ── speak ───────────────────────────────────────────────────────── */
  async function speak({ record = false } = {}) {
    const text = el.script.value.trim();
    if (!text) return status('Write a script first.', 'err');
    if (!state.image && el.lipEngine.value === 'local') return status('Upload an avatar first.', 'err');

    stop();

    if (el.lipEngine.value === 'heygen') return renderWithHeyGen(text);

    const engine = el.ttsEngine.value;

    if (engine === 'browser') {
      if (record) return status('Browser TTS audio cannot be captured by the page — switch to Piper, ElevenLabs, OpenAI, or an uploaded audio file to export.', 'err');
      return speakWithBrowserTTS(text);
    }
    return speakWithAudio(text, engine, record);
  }

  /* Speech path — synthetic clock, corrected by word boundary events. */
  function speakWithBrowserTTS(text) {
    const rate = parseFloat(el.rate.value);
    const duration = TTS.estimateDuration(text, rate);

    state.timeline = Visemes.buildTimeline(text, duration);
    state.mode = 'speech';
    state.clock = 0;
    state.playing = true;
    setTransport(true);
    el.scrubber.disabled = true;
    status('Speaking (preview — not recordable).');

    TTS.speakBrowser(text, {
      voiceURI: el.voice.value,
      rate,
      pitch: parseFloat(el.pitch.value),
      onBoundary: (charIndex) => {
        // Nudge our clock toward where the real voice actually is.
        const expected = (charIndex / Math.max(1, text.length)) * duration;
        state.clock += (expected - state.clock) * 0.35;
        el.timeLabel.textContent = `${fmt(state.clock)} / ${fmt(duration)}`;
      },
      onEnd: () => stop(),
    });
  }

  /* Blob path — real audio, real analyser, real clock. */
  async function speakWithAudio(text, engine, record) {
    ensureAudioGraph();
    if (audio.ctx.state === 'suspended') await audio.ctx.resume();

    try {
      if (!state.audioBlob) {
        if (engine === 'upload') {
          if (!state.uploadedAudio) return status('Drop an audio file first.', 'err');
          state.audioBlob = state.uploadedAudio;
        } else {
          status(`Synthesising with ${engine}…`);
          el.btnSpeak.disabled = true;
          state.audioBlob = await TTS.synthesize(engine, text, engineOptions(engine));
        }
        if (state.audioUrl) URL.revokeObjectURL(state.audioUrl);
        state.audioUrl = URL.createObjectURL(state.audioBlob);
      }
    } catch (e) {
      el.btnSpeak.disabled = false;
      return status(e.message, 'err');
    }

    audio.elem.src = state.audioUrl;
    await new Promise((res) => {
      if (audio.elem.readyState >= 1) return res();
      audio.elem.addEventListener('loadedmetadata', res, { once: true });
    });

    const duration = audio.elem.duration;
    state.timeline = Visemes.buildTimeline(text, duration);
    state.mode = 'blob';
    state.peak = 0.15;
    el.scrubber.disabled = false;

    if (record) await startRecording();

    audio.elem.currentTime = 0;
    await audio.elem.play();

    state.playing = true;
    setTransport(true);
    status(record ? 'Recording…' : `Speaking · ${fmt(duration)} of audio.`);
  }

  /* Each blob-returning engine wants a different shape of credentials. */
  function engineOptions(engine) {
    switch (engine) {
      case 'elevenlabs': return {
        apiKey: el.elKey.value.trim(),
        // A preset picks the ID for you; "custom" hands control to the text field,
        // which is also where a freshly cloned voice lands.
        voiceId: el.elPreset.value === 'custom' ? el.elVoice.value.trim() : el.elPreset.value,
      };
      case 'openai':     return { apiKey: el.oaKey.value.trim(), voice: el.oaVoice.value };
      case 'gemini':     return { apiKey: el.gmKey.value.trim(), voice: el.gmVoice.value };
      case 'piper':      return { baseUrl: el.piperUrl.value.trim(), voice: el.piperVoice.value.trim() };
      default:           return {};
    }
  }

  function stop() {
    if (state.recording) finishRecording();
    speechSynthesis.cancel();
    if (audio.elem) audio.elem.pause();
    // The rendered MP4 (Wav2Lip / MuseTalk / HeyGen) plays in its own <video>.
    // Stop must stop THAT too — otherwise the button is dead while a video speaks.
    if (el.hgVideo && !el.hgVideo.hidden && !el.hgVideo.paused) el.hgVideo.pause();

    state.playing = false;
    setTransport(false);
    setMeter(0);
    el.visemeReadout.hidden = true;
    if (!state.recording) refreshButtons();
  }

  /* ── export (canvas frames + audio graph → webm) ─────────────────── */
  let recorder = null, chunks = [];

  async function startRecording() {
    const stream = el.stage.captureStream(30);
    audio.dest.stream.getAudioTracks().forEach((t) => stream.addTrack(t));

    const mime = ['video/webm;codecs=vp9,opus', 'video/webm;codecs=vp8,opus', 'video/webm']
      .find((m) => MediaRecorder.isTypeSupported(m));
    if (!mime) throw new Error('This browser cannot record WebM.');

    chunks = [];
    recorder = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 6_000_000 });
    recorder.ondataavailable = (e) => e.data.size && chunks.push(e.data);
    recorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'video/webm' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `digital-human-${Date.now()}.webm`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 5000);
      status(`Exported ${(blob.size / 1e6).toFixed(1)} MB of WebM.`, 'ok');
      state.recording = false;
      refreshButtons();
    };

    recorder.start(200);
    state.recording = true;
  }

  function finishRecording() {
    if (recorder && recorder.state !== 'inactive') recorder.stop();
    recorder = null;
  }

  /* ── HeyGen (v3) ─────────────────────────────────────────────────── */

  /* Populate the avatar/voice pickers from the account itself, rather than making
   * anyone paste opaque IDs. Runs the first time the HeyGen pane is opened. */
  let hgLoaded = false;
  let hgLoading = false;
  let serverHasWav2Lip = false;
  let serverHasMuseTalk = true;   // until /api/config says otherwise

  async function loadHeyGenLists() {
    HeyGen.setKey(el.hgKey.value);
    if (hgLoaded || hgLoading) return;
    hgLoading = true;
    refreshButtons();
    status('HeyGen: loading your avatars…');
    try {
      const [avatars, voices] = await Promise.all([HeyGen.listAvatars(), HeyGen.listVoices()]);

      el.hgAvatar.innerHTML = '';
      avatars.forEach((a) => {
        const o = document.createElement('option');
        o.value = a.id;
        o.textContent = a.kind === 'photo' ? `${a.name} (photo avatar)` : a.name;
        el.hgAvatar.appendChild(o);
      });

      el.hgVoice.innerHTML = '';
      const groups = { female: [], male: [], other: [] };
      voices.forEach((v) => (groups[v.gender] || groups.other).push(v));
      for (const [label, list] of Object.entries(groups)) {
        if (!list.length) continue;
        const g = document.createElement('optgroup');
        g.label = label[0].toUpperCase() + label.slice(1);
        list.slice(0, 40).forEach((v) => {
          const o = document.createElement('option');
          o.value = v.id;
          o.textContent = `${v.name} — ${v.language || ''}`.trim();
          g.appendChild(o);
        });
        el.hgVoice.appendChild(g);
      }

      hgLoaded = true;
      el.btnHgUpload.disabled = !state.imageFile;
      status(`HeyGen: ${avatars.length} avatars, ${voices.length} voices loaded.`, 'ok');
    } catch (e) {
      el.hgAvatar.innerHTML = '<option value="">— failed to load —</option>';
      el.hgVoice.innerHTML = '<option value="">— failed to load —</option>';
      status(`HeyGen: ${e.message}`, 'err');
    } finally {
      hgLoading = false;
      refreshButtons();
    }
  }

  async function renderWithHeyGen(text) {
    const avatarId = el.hgAvatar.value;
    const voiceId = el.hgVoice.value;
    if (!avatarId || !voiceId) return status('Pick a HeyGen avatar and voice.', 'err');

    el.hgStatus.hidden = false;
    el.btnSpeak.disabled = true;
    const t0 = performance.now();
    showRenderProgress('HeyGen');
    startHeyGenEstimate();

    try {
      const url = await HeyGen.render({
        avatarId, voiceId, text,
        onProgress: (msg, pct) => {
          el.hgStatus.textContent = msg;
          setMeter((pct || 0) / 100);
          status(`HeyGen: ${msg}`);
        },
      });

      el.stage.hidden = true;
      el.hgVideo.hidden = false;
      el.hgVideo.src = url;
      el.hgVideo.controls = true;
      el.hgVideo.loop = el.loopVideo.checked;
      await el.hgVideo.play().catch(() => {});

      const secs = Math.round((performance.now() - t0) / 1000);
      finishRenderProgress(true, `HeyGen rendered in ${secs}s`);
      el.hgStatus.textContent = `Done in ${secs}s.`;
      status('HeyGen video ready — right-click the player to save it.', 'ok');
    } catch (e) {
      finishRenderProgress(false, `HeyGen: ${e.message}`);
      el.hgStatus.textContent = e.message;
      status(`HeyGen: ${e.message}`, 'err');
    } finally {
      el.btnSpeak.disabled = false;
      setMeter(0);
    }
  }

  el.hgKey.addEventListener('change', () => { hgLoaded = false; loadHeyGenLists(); });

  el.btnHgUpload.addEventListener('click', async () => {
    if (!state.imageFile) return status('Upload a portrait first.', 'err');
    el.btnHgUpload.disabled = true;
    el.hgStatus.hidden = false;
    el.hgStatus.textContent = 'Uploading portrait to HeyGen…';
    try {
      const id = await HeyGen.uploadPhoto(state.imageFile);
      const o = document.createElement('option');
      o.value = id;
      o.textContent = `${state.imageFile.name} (just uploaded)`;
      el.hgAvatar.prepend(o);
      el.hgAvatar.value = id;
      el.hgStatus.textContent = 'Uploaded — it is now selected as the avatar.';
      status('Portrait uploaded to HeyGen.', 'ok');
    } catch (e) {
      // e.g. "You have exceeded your limit of 3 photo avatars."
      el.hgStatus.textContent = e.message;
      status(`HeyGen: ${e.message}`, 'err');
    } finally {
      el.btnHgUpload.disabled = false;
    }
  });

  /* ── ui plumbing ─────────────────────────────────────────────────── */
  function refreshButtons() {
    const hasScript = el.script.value.trim().length > 0;
    const heygen = el.lipEngine.value === 'heygen';
    // HeyGen v3 renders one of the account's own avatars, so it needs no local
    // image at all — only a script. (v2 used to require uploading the photo.)
    const ready = heygen ? (hasScript && hgLoaded && !hgLoading) : (hasScript && !!state.image);

    el.btnSpeak.disabled = !ready || state.recording;
    el.btnRender.disabled = !ready || heygen || el.ttsEngine.value === 'browser' || state.recording;
    // MuseTalk needs real audio samples, which browser TTS never exposes.
    const eng = el.lipEngine.value;
    const engineReady =
      (eng === 'musetalk' && serverHasMuseTalk) || (eng === 'wav2lip' && serverHasWav2Lip);
    el.btnPhotoreal.disabled =
      !engineReady || !hasScript || !state.imageFile ||
      el.ttsEngine.value === 'browser' || state.recording;
  }

  function setTransport(playing) {
    el.btnSpeak.disabled = playing;
    el.btnStop.disabled = !playing;
    el.btnRender.disabled = playing || el.ttsEngine.value === 'browser' || el.lipEngine.value === 'heygen';
  }

  function updateScrub() {
    if (state.mode !== 'blob' || !audio.elem.duration) return;
    const p = audio.elem.currentTime / audio.elem.duration;
    el.scrubber.value = Math.round(p * 1000);
    el.timeLabel.textContent = `${fmt(audio.elem.currentTime)} / ${fmt(audio.elem.duration)}`;
  }

  function status(msg, kind = '') {
    el.statusLine.textContent = msg;
    el.statusLine.className = `statusline ${kind}`;
  }

  const fmt = (s) => {
    if (!isFinite(s)) return '0:00';
    const m = Math.floor(s / 60);
    return `${m}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  };

  function showPane(attr, value) {
    document.querySelectorAll(`[${attr}]`).forEach((p) => { p.hidden = p.getAttribute(attr) !== value; });
  }

  /* Click / keyboard / drag-and-drop, all three routes into the same handler.
   *
   * The zone is a <label> wrapping a hidden input, so a click would normally be
   * forwarded natively — but we open the picker ourselves and preventDefault the
   * label, because relying on native forwarding to a `display:none` input is the
   * kind of thing that silently stops working. preventDefault is what stops the
   * chooser opening twice. */
  function wireDrop(zone, input, onFile) {
    zone.addEventListener('click', (e) => {
      if (e.target === input) return; // the real click we dispatched below
      e.preventDefault();
      input.click();
    });
    zone.setAttribute('tabindex', '0');
    zone.setAttribute('role', 'button');
    zone.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); }
    });

    input.addEventListener('change', () => input.files[0] && onFile(input.files[0]));
    ['dragenter', 'dragover'].forEach((ev) =>
      zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.add('over'); }));
    ['dragleave', 'drop'].forEach((ev) =>
      zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.remove('over'); }));
    zone.addEventListener('drop', (e) => e.dataTransfer.files[0] && onFile(e.dataTransfer.files[0]));
  }

  /* ── events ──────────────────────────────────────────────────────── */
  function acceptAudio(file) {
    state.uploadedAudio = file;
    state.audioBlob = null;
    el.audioDrop.classList.add('has-file');
    el.audioDrop.querySelector('strong').textContent = file.name;
    el.ttsEngine.value = 'upload';
    showPane('data-engine', 'upload');
    status(`Audio ready: ${file.name}`, 'ok');
    refreshButtons();
  }

  wireDrop(el.avatarDrop, el.avatarFile, loadAvatar);
  wireDrop(el.audioDrop, el.audioFile, acceptAudio);

  /* Drop a portrait anywhere — on the stage, on the panel, wherever it lands.
   * Without swallowing the page-level dragover, the browser just navigates away
   * to the dropped file, which is the least helpful thing it could do. */
  ['dragenter', 'dragover'].forEach((ev) =>
    window.addEventListener(ev, (e) => {
      if (e.dataTransfer?.types.includes('Files')) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        document.body.classList.add('dragging');
      }
    })
  );
  ['dragleave', 'dragend'].forEach((ev) =>
    window.addEventListener(ev, (e) => {
      if (!e.relatedTarget) document.body.classList.remove('dragging');
    })
  );
  window.addEventListener('drop', (e) => {
    document.body.classList.remove('dragging');
    const file = e.dataTransfer?.files[0];
    if (!file) return;
    e.preventDefault();

    if (file.type.startsWith('image/')) loadAvatar(file);
    else if (file.type.startsWith('audio/')) acceptAudio(file);
    else if (file.type.startsWith('video/')) acceptCloneClip(file);
    else if (file.type.startsWith('text/')) file.text().then((t) => { el.script.value = t; updateScriptStats(); });
    else status(`Don't know what to do with a ${file.type || 'file'} — drop an image, audio, video, or .txt.`, 'err');
  });

  el.scriptFile.parentElement.addEventListener('click', (e) => {
    if (e.target === el.scriptFile) return;
    e.preventDefault();
    el.scriptFile.click();
  });
  el.scriptFile.addEventListener('change', async () => {
    const f = el.scriptFile.files[0];
    if (f) { el.script.value = await f.text(); updateScriptStats(); }
  });

  el.script.addEventListener('input', updateScriptStats);

  el.ttsEngine.addEventListener('change', () => {
    showPane('data-engine', el.ttsEngine.value);
    state.audioBlob = null;
    refreshButtons();
  });

  el.lipEngine.addEventListener('change', () => {
    const eng = el.lipEngine.value;
    const heygen = eng === 'heygen';

    // The render driver is shared; the dropdown decides which endpoint it hits.
    if (eng === 'wav2lip') {
      window.__ENGINE_URL = '/api/render/wav2lip';
      window.__ENGINE_NAME = 'Wav2Lip';
      el.btnPhotoreal.textContent = '⚡ Render video (Wav2Lip)';
    } else if (eng === 'musetalk') {
      window.__ENGINE_URL = '/api/render/musetalk';
      window.__ENGINE_NAME = 'MuseTalk';
      el.btnPhotoreal.textContent = '✨ Render video (MuseTalk)';
    } else {
      window.__ENGINE_URL = null;
      window.__ENGINE_NAME = null;
      el.btnPhotoreal.textContent = '✨ Render video';
    }

    // The trap this avoids: "Speak" and "Export video" ALWAYS use the in-browser
    // drawn-mouth preview, whatever engine is selected. Only "Render video" calls the
    // engine. Learners kept switching engines, pressing Speak, and concluding that all
    // three looked identical — because they were all looking at the same preview.
    const isPreview = eng === 'local';
    // The button says what it DOES. The note below explains what it is for.
    el.btnSpeak.textContent = '▶ Start Speaking';
    el.btnSpeak.title = 'Play the script in the browser preview (instant, drawn mouth)';
    el.btnRender.textContent = '⬇ Export preview';
    el.btnRender.title = 'Saves the browser preview as a video — NOT the selected engine.';
    if (el.engineNote) {
      const engineLabel = eng === 'heygen' ? 'HeyGen (cloud)' : (window.__ENGINE_NAME || '');
      const missing =
        (eng === 'musetalk' && !serverHasMuseTalk) ? 'MuseTalk weights are not installed — run  ./setup.sh --musetalk  (3.5 GB, once), then restart the app.'
        : (eng === 'wav2lip' && !serverHasWav2Lip) ? 'Wav2Lip is not installed — see lab6/README.md.'
        : '';
      // Offer to fetch what is missing, right where the learner hits the wall.
      if (el.btnGetWeights) {
        const size = eng === 'musetalk' ? '3.5 GB' : '440 MB';
        el.btnGetWeights.hidden = !missing;
        el.btnGetWeights.textContent = `⬇ Download ${eng === 'musetalk' ? 'MuseTalk' : 'Wav2Lip'} weights (${size})`;
        el.btnGetWeights.dataset.engine = eng;
      }
      el.engineNote.textContent = missing
        ? missing
        : isPreview
          ? 'Start Speaking plays the instant browser preview — the mouth is drawn geometry, not a real render.'
          : `Start Speaking = quick browser preview.  To get the real ${engineLabel} video, press “Render video”.`;
    }

    // Only HeyGen has its own settings pane; the local engines share the preview one.
    showPane('data-lip', heygen ? 'heygen' : 'local');
    el.engineBadge.textContent = heygen ? 'Cloud engine' : 'Local engine';
    el.engineBadge.className = `badge ${heygen ? 'badge-cloud' : 'badge-local'}`;
    if (heygen) loadHeyGenLists();
    el.stage.hidden = false;
    el.hgVideo.hidden = true;
    refreshButtons();
  });

  const bindSlider = (input, label, key, fmtFn = (v) => v.toFixed(2)) => {
    const apply = () => {
      const v = parseFloat(input.value);
      label.textContent = fmtFn(v);
      if (key) renderer.setOptions({ [key]: v });
    };
    input.addEventListener('input', apply);
    apply();
  };
  bindSlider(el.gain, el.gainVal, 'gain');
  bindSlider(el.smooth, el.smoothVal, 'smoothing');
  bindSlider(el.rate, el.rateVal, null);
  bindSlider(el.pitch, el.pitchVal, null);
  el.rate.addEventListener('input', updateScriptStats);

  [['optFrame', 'frame'], ['optSway', 'sway'], ['optBreath', 'breath'], ['optDebug', 'debug']]
    .forEach(([id, key]) => {
      el[id].addEventListener('change', () => renderer.setOptions({ [key]: el[id].checked }));
    });

  el.btnSpeak.addEventListener('click', () => speak());
  el.btnStop.addEventListener('click', stop);

  // Loop is a user setting, not a hardcoded choice. Off by default: a clip that
  // repeats forever gets in the way when you are judging lip sync — but for a
  // side-by-side engine comparison you often WANT it running on a loop.
  el.loopVideo.addEventListener('change', () => {
    el.hgVideo.loop = el.loopVideo.checked;                 // applies mid-playback
    localStorage.setItem('dh_loop', el.loopVideo.checked ? '1' : '0');
  });
  el.loopVideo.checked = localStorage.getItem('dh_loop') === '1';
  el.hgVideo.loop = el.loopVideo.checked;


  // Keep Stop usable while the rendered video is playing.
  el.hgVideo.addEventListener('play', () => { el.btnStop.disabled = false; });
  el.hgVideo.addEventListener('pause', () => { el.btnStop.disabled = true; });
  el.hgVideo.addEventListener('ended', () => { el.btnStop.disabled = true; });
  el.btnRender.addEventListener('click', () => speak({ record: true }));

  el.scrubber.addEventListener('input', () => {
    if (state.mode !== 'blob' || !audio.elem.duration) return;
    audio.elem.currentTime = (el.scrubber.value / 1000) * audio.elem.duration;
  });

  el.btnAutoFace.addEventListener('click', async () => {
    status('Finding the face…');
    await applyDetection(state.image);
  });

  el.btnEditFace.addEventListener('click', () => {
    const editor = Face.createEditor(el.faceCanvas, state.image, state.rig);
    el.faceDialog.showModal();
    el.faceDialog.addEventListener('close', () => {
      if (el.faceDialog.returnValue === 'ok') {
        state.rig = editor.commit();
        renderer.setRig(state.rig);
        status('Rig saved.', 'ok');
      }
    }, { once: true });
  });

  el.btnHelp.addEventListener('click', () => el.helpDialog.showModal());

  /* ── photoreal render (MuseTalk, locally) ────────────────────────── */

  /* The neural model needs the actual audio samples, which browser TTS never
   * hands over. So we synthesise first (or reuse what Speak already made) and
   * post the portrait + that audio to the Python service. */
  el.btnPhotoreal.addEventListener('click', async () => {
    const text = el.script.value.trim();
    if (!state.imageFile) return status('Upload an avatar first.', 'err');
    if (!text) return status('Write a script first.', 'err');

    const engine = el.ttsEngine.value;
    if (engine === 'browser') {
      return status('Browser TTS audio can\'t be captured, so MuseTalk has nothing to sync to. Pick Gemini, ElevenLabs, OpenAI, Piper, or upload audio.', 'err');
    }

    stop();
    el.btnPhotoreal.disabled = true;

    try {
      if (!state.audioBlob) {
        if (engine === 'upload') {
          if (!state.uploadedAudio) throw new Error('Drop an audio file first.');
          state.audioBlob = state.uploadedAudio;
        } else {
          status(`Synthesising with ${engine}…`);
          state.audioBlob = await TTS.synthesize(engine, text, engineOptions(engine));
        }
      }

      const form = new FormData();
      form.append('image', state.imageFile, state.imageFile.name || 'portrait.png');
      form.append('audio', state.audioBlob, 'audio.wav');

      showRenderProgress(window.__ENGINE_NAME || 'MuseTalk');
      status(`Sending to ${window.__ENGINE_NAME || 'MuseTalk'}…`);
      const res = await fetch(window.__ENGINE_URL || '/api/render/musetalk', { method: 'POST', body: form });
      if (!res.ok) throw new Error((await res.text()).slice(0, 200));
      const { job_id } = await res.json();

      // Poll. First run is slow — it loads ~3.5 GB of weights before frame one.
      for (;;) {
        await new Promise((r) => setTimeout(r, 1000));
        const job = await (await fetch(`/api/render/status/${job_id}`)).json();

        if (job.status === 'error') throw new Error(job.message);
        setMeter((job.pct || 0) / 100);
        setRenderProgress(job.pct || 0, `${window.__ENGINE_NAME || 'MuseTalk'}: ${job.message}`);
        status(`${window.__ENGINE_NAME || 'MuseTalk'}: ${job.message} (${job.pct}%)`);

        if (job.status === 'done') {
          el.stage.hidden = true;
          el.hgVideo.hidden = false;
          el.hgVideo.src = job.url;
          el.hgVideo.controls = true;
          el.hgVideo.loop = el.loopVideo.checked;
          await el.hgVideo.play().catch(() => {});
          finishRenderProgress(true, `${window.__ENGINE_NAME || 'MuseTalk'} render complete`);
          status('Render ready — right-click the player to save the MP4.', 'ok');
          break;
        }
      }
    } catch (e) {
      finishRenderProgress(false, `${window.__ENGINE_NAME || 'MuseTalk'}: ${e.message}`);
      status(`${window.__ENGINE_NAME || 'MuseTalk'}: ${e.message}`, 'err');
    } finally {
      el.btnPhotoreal.disabled = false;
      setMeter(0);
    }
  });

  /* ── voice preview ───────────────────────────────────────────────── */
  el.elPreset.addEventListener('change', () => {
    el.elCustomField.hidden = el.elPreset.value !== 'custom';
    state.audioBlob = null;
  });
  el.gmVoice.addEventListener('change', () => { state.audioBlob = null; });

  // Speak one line in the selected voice, without touching the real script or
  // the avatar — so you can shop for a voice before committing to a render.
  async function previewVoice(engine) {
    const line = 'Hi, this is how I sound. I can narrate your script in this voice.';
    ensureAudioGraph();
    if (audio.ctx.state === 'suspended') await audio.ctx.resume();

    status(`Previewing the ${engine} voice…`);
    try {
      const blob = await TTS.synthesize(engine, line, engineOptions(engine));
      stop();
      audio.elem.src = URL.createObjectURL(blob);
      state.timeline = null;      // preview drives the meter, not the avatar
      await audio.elem.play();
      status('Voice preview playing.', 'ok');
    } catch (e) {
      status(e.message, 'err');
    }
  }
  el.btnPreviewGm.addEventListener('click', () => previewVoice('gemini'));
  el.btnPreviewEl.addEventListener('click', () => previewVoice('elevenlabs'));

  /* ── script drafting with a local Ollama model ───────────────────── */
  el.btnDraft.addEventListener('click', async () => {
    const brief = el.script.value.trim();
    if (!brief) return status('Put a topic or rough notes in the script box first.', 'err');

    el.btnDraft.disabled = true;
    status(`Drafting with ${el.ollamaModel.value}…`);
    try {
      const res = await fetch('/api/script/ollama', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brief, model: el.ollamaModel.value.trim() }),
      });
      const text = await res.text();
      if (!res.ok) throw new Error(text.slice(0, 200));

      const { script } = JSON.parse(text);
      if (!script) throw new Error('Ollama returned an empty script.');
      el.script.value = script;
      updateScriptStats();
      status('Script drafted locally.', 'ok');
    } catch (e) {
      status(`Ollama: ${e.message}`, 'err');
    } finally {
      el.btnDraft.disabled = false;
    }
  });

  /* ── sample portraits ────────────────────────────────────────────── */
  document.querySelectorAll('.sample').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const name = btn.dataset.sample;
      status('Loading sample…');
      try {
        const blob = await (await fetch(`samples/${name}.jpg`)).blob();
        await loadAvatar(new File([blob], `${name}.jpg`, { type: 'image/jpeg' }));
      } catch (e) {
        status(SERVED_OVER_HTTP
          ? `Could not load that sample: ${e.message}`
          : FILE_URL_HINT, 'err');
      }
    });
  });

  /* ── voice cloning ───────────────────────────────────────────────── */
  let cloneClip = null;

  function acceptCloneClip(file) {
    cloneClip = file;
    el.cloneDrop.classList.add('has-file');
    el.cloneDrop.querySelector('strong').textContent = file.name;
    el.cloneDrop.querySelector('span').textContent =
      `${(file.size / 1e6).toFixed(1)} MB · ${file.type.startsWith('video/') ? 'audio will be extracted' : 'audio'}`;
    if (!el.cloneName.value) el.cloneName.value = file.name.replace(/\.[^.]+$/, '');
    el.btnClone.disabled = false;
    el.cloneStatus.hidden = true;

    // A dropped video only makes sense for cloning — take the user there.
    el.ttsEngine.value = 'elevenlabs';
    showPane('data-engine', 'elevenlabs');
    document.getElementById('clonePanel').open = true;
    status(`Clip ready for cloning: ${file.name}`, 'ok');
    refreshButtons();
  }

  wireDrop(el.cloneDrop, el.cloneFile, acceptCloneClip);

  el.btnClone.addEventListener('click', async () => {
    const apiKey = el.elKey.value.trim();
    if (!apiKey) return cloneMsg('Paste your ElevenLabs API key above first.', true);
    if (!cloneClip) return cloneMsg('Drop a clip first.', true);

    el.btnClone.disabled = true;
    cloneMsg(cloneClip.type.startsWith('video/')
      ? 'Extracting audio, then uploading… (a big video takes a moment)'
      : 'Uploading the clip…');

    try {
      const voiceId = await TTS.cloneVoice({
        file: cloneClip,
        name: el.cloneName.value.trim() || 'Cloned voice',
        apiKey,
      });
      el.elVoice.value = voiceId;
      state.audioBlob = null; // the voice changed, so any synthesised audio is stale
      cloneMsg(`Cloned. Voice ID ${voiceId} is now selected — hit Speak.`);
      status('Voice cloned and selected.', 'ok');
    } catch (e) {
      cloneMsg(e.message, true);
      status(`Voice cloning failed: ${e.message}`, 'err');
    } finally {
      el.btnClone.disabled = false;
    }
  });

  function cloneMsg(msg, isErr = false) {
    el.cloneStatus.hidden = false;
    el.cloneStatus.textContent = msg;
    el.cloneStatus.style.color = isErr ? 'var(--danger)' : 'var(--muted)';
  }

  /* ── boot ────────────────────────────────────────────────────────── */

  /* Ask the proxy which services it already has keys for (booleans only — the
   * keys themselves stay on the server). Anything covered by .env gets its key
   * field marked as pre-configured, so nobody has to paste a secret into a page. */
  async function loadServerConfig() {
    let cfg;
    try {
      cfg = await (await fetch('/api/config')).json();
    } catch {
      // No backend: opened from file://, or served as a static site. The browser
      // preview still works entirely client-side, but nothing that needs the
      // server does — so don't offer buttons that can only fail.
      serverHasMuseTalk = false;
      el.btnPhotoreal.title = 'Needs the Python backend — run python/app.py.';
      refreshButtons();
      // On file:// the browser preview doesn't work either (fetch is blocked, so
      // even the sample portraits fail) — keep the URL hint on screen instead.
      status(SERVED_OVER_HTTP
        ? 'No backend detected — browser TTS and the live preview still work.'
        : FILE_URL_HINT, 'err');
      return;
    }

    const wire = (ok, input, service) => {
      if (!ok) return;
      input.placeholder = `Using ${service} key from .env`;
      input.classList.add('from-env');
      input.title = 'A key is configured server-side. Type here only to override it.';
    };

    wire(cfg.gemini, el.gmKey, 'Gemini');
    wire(cfg.elevenlabs, el.elKey, 'ElevenLabs');
    wire(cfg.openai, el.oaKey, 'OpenAI');
    wire(cfg.heygen, el.hgKey, 'HeyGen');

    // On a server without the model weights (or a GPU), photoreal rendering isn't
    // on offer — say so rather than leaving a button that fails a minute later.
    serverHasMuseTalk = !!cfg.musetalk;
    serverHasWav2Lip = !!cfg.wav2lip;
    if (!serverHasMuseTalk) {
      el.btnPhotoreal.title = 'MuseTalk is not installed on this server — use HeyGen, or run locally.';
    }

    // Default to the engine that's actually ready to go.
    if (cfg.gemini) {
      el.ttsEngine.value = 'gemini';
      showPane('data-engine', 'gemini');
      status('Gemini key loaded from .env — pick an avatar and hit Speak.', 'ok');
    }
    refreshButtons();
  }

  (async function init() {
    loadServerConfig();
    const voices = await TTS.listVoices();
    const preferred = voices.filter((v) => v.lang.startsWith('en'));
    (preferred.length ? preferred : voices).forEach((v) => {
      const opt = document.createElement('option');
      opt.value = v.voiceURI;
      opt.textContent = `${v.name} — ${v.lang}${v.localService ? '' : ' (network)'}`;
      el.voice.appendChild(opt);
    });
    if (!voices.length) status('No system voices found — pick another TTS engine.', 'err');

    updateScriptStats();
    refreshButtons();
  })();
})();


  /* ── one-click weight download ─────────────────────────────────────
     The weights are far too big to commit, so a fresh clone has a greyed-out
     engine. Rather than send the learner to a shell, fetch them here and show
     the same progress bar the renders use. */
  async function downloadWeights(engine) {
    const btn = el.btnGetWeights;
    btn.disabled = true;
    showRenderProgress(engine === 'musetalk' ? 'MuseTalk' : 'Wav2Lip');

    try {
      const res = await fetch(`/api/models/download/${engine}`, { method: 'POST' });
      if (!res.ok) throw new Error((await res.text()).slice(0, 200));
      const { job_id } = await res.json();

      for (;;) {
        await new Promise((r) => setTimeout(r, 1500));
        const job = await (await fetch(`/api/render/status/${job_id}`)).json();
        if (job.status === 'error') throw new Error(job.message);
        setRenderProgress(job.pct || 0, job.message);
        if (job.status === 'done') break;
      }

      finishRenderProgress(true, `${engine} weights installed`);
      // Re-read the config so the engine becomes selectable without a restart.
      const cfg = await (await fetch('/api/config')).json();
      serverHasMuseTalk = !!cfg.musetalk;
      serverHasWav2Lip = !!cfg.wav2lip;
      btn.hidden = true;
      el.lipEngine.dispatchEvent(new Event('change', { bubbles: true }));
      status(`${engine} is ready.`, 'ok');
    } catch (e) {
      finishRenderProgress(false, `Download failed: ${e.message}`);
      status(`Download failed: ${e.message}`, 'err');
    } finally {
      btn.disabled = false;
      refreshButtons();
    }
  }

  el.btnGetWeights.addEventListener('click', () => downloadWeights(el.btnGetWeights.dataset.engine));

  if (!SERVED_OVER_HTTP) status(FILE_URL_HINT, 'err');

