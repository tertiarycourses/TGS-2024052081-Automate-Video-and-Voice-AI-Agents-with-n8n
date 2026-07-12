/* HeyGen v3, proxied through the Python backend.
 *
 * v1/v2 are on the sunset path (31 Oct 2026) and reject the current `sk_` keys,
 * so this talks to v3 only: the account's avatars and voices are listed, a render
 * is submitted, and the server polls it as a background job — the same job API
 * MuseTalk uses, so the UI watches both the same way.
 *
 * This is the cloud path: the script and the chosen avatar are rendered on
 * HeyGen's servers and it costs credits. MuseTalk does it locally for free. */

(function (global) {
  'use strict';

  const PROXY = '/api/heygen';

  // A key typed into the page overrides the server's .env key; if the field is
  // empty the server falls back to .env, which is the normal case.
  let apiKey = '';
  const setKey = (k) => { apiKey = (k || '').trim(); };

  async function req(path, opts = {}) {
    if (apiKey) opts.headers = { ...opts.headers, 'X-Api-Key': apiKey };

    let res;
    try {
      res = await fetch(`${PROXY}${path}`, opts);
    } catch {
      throw new Error('Cannot reach the local server — start it with `python python/app.py`.');
    }

    const text = await res.text();
    if (!res.ok) {
      // HeyGen's errors are the useful kind ("exceeded your limit of 3 photo
      // avatars") — surface them verbatim instead of a generic failure.
      let msg = text.slice(0, 220);
      try {
        const j = JSON.parse(text);
        msg = j.detail || j.error?.message || j.message || msg;
      } catch { /* keep the raw text */ }
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }
    return text ? JSON.parse(text) : null;
  }

  const listAvatars = () => req('/avatars');
  const listVoices = () => req('/voices');

  /* Upload a portrait as a new photo avatar. HeyGen caps how many an account may
   * hold, so this can legitimately fail — the caller shows the message. */
  async function uploadPhoto(file) {
    const data = await req('/upload', {
      method: 'POST',
      headers: { 'Content-Type': file.type || 'image/jpeg' },
      body: file,
    });
    const id = data?.data?.talking_photo_id || data?.talking_photo_id;
    if (!id) throw new Error('HeyGen accepted the upload but returned no avatar id.');
    return id;
  }

  /* Submit and watch. Renders take under a minute for a short script. */
  async function render({ avatarId, voiceId, text, onProgress }) {
    const { job_id } = await req('/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ avatar_id: avatarId, voice_id: voiceId, text }),
    });

    for (;;) {
      await new Promise((r) => setTimeout(r, 2000));
      const job = await (await fetch(`/api/render/status/${job_id}`)).json();

      if (job.status === 'error') throw new Error(job.message);
      onProgress && onProgress(job.message, job.pct);
      if (job.status === 'done') return job.url;
    }
  }

  global.HeyGen = { setKey, listAvatars, listVoices, uploadPhoto, render };
})(window);
