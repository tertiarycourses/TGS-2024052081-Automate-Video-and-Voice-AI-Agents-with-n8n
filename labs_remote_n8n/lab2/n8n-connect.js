/* n8n-connect.js — the webhook URL box and the "Test connection" button.
 *
 * Shared verbatim by every lab website in both trees. One job: let a learner
 * prove the webhook works BEFORE the lab fails on them with a blank screen.
 *
 * ── Why the test is shaped the way it is ───────────────────────────────────
 * n8n registers a webhook PER METHOD, and it sends NO CORS headers on error
 * responses. Two consequences that dictate everything below:
 *
 *   1. A GET probe to a live POST-only webhook 404s with no CORS header, so the
 *      browser throws — exactly like an inactive workflow does. A "safe" probe
 *      therefore CANNOT tell "not Active" from "working fine". Only a request
 *      with the registered method (POST) can prove the workflow is Active.
 *
 *   2. When the POST probe throws a network/CORS error, that is itself the
 *      signal: n8n only emits CORS headers for a REGISTERED webhook, so a
 *      thrown request almost always means the workflow is not Active.
 *
 * So: mode="post" fires a real POST and proves activation. It is safe for the
 * labs that only run an LLM or a DB step. It is NOT safe for the labs that
 * spend money per run (HeyGen, Veo), so those declare mode="safe" and check
 * reachability only — a Test button must never quietly burn a learner's
 * credits. What each mode did and did not prove is stated in the result.
 *
 * ── Markup contract ────────────────────────────────────────────────────────
 *   <input type="url" id="webhookUrl"
 *          data-n8n-test="post"          post | safe
 *          data-n8n-key="lab8"           localStorage key (defaults to the id)
 *          data-n8n-path="veo-generate"> optional: input holds a BASE url and
 *                                        this path is appended to probe it
 * The button, the status line and the styles are injected — no per-site markup.
 */
(function (global) {
  'use strict';

  const STORE = (key) => `n8n_webhook_${key}`;

  /* ── storage ───────────────────────────────────────────────────────────── */
  function load(key) {
    try { return localStorage.getItem(STORE(key)) || ''; } catch { return ''; }
  }
  /* Only ever persist something that could actually be a webhook. Saving junk
   * means the next reload silently restores the junk, and the learner debugs a
   * typo they already fixed. */
  function save(key, url) {
    if (url && !/^https?:\/\//i.test(url)) return;
    try { localStorage.setItem(STORE(key), url); } catch { /* private mode */ }
  }

  /* Trailing whitespace pasted from n8n is invisible and breaks the URL. */
  const clean = (u) => (u || '').trim().replace(/\s+/g, '').replace(/\/+$/, '');

  /* The probe target. Most labs store the full webhook URL; the labs that store
   * a BASE (lab9, lab10) declare data-n8n-path and we append it. */
  function target(url, path) {
    const base = clean(url);
    if (!path) return base;
    return `${base}/${String(path).replace(/^\/+/, '')}`;
  }

  /* ── the probe ─────────────────────────────────────────────────────────── */
  async function probe(rawUrl, mode, path) {
    const url = target(rawUrl, path);

    if (!url) return { kind: 'err', msg: 'Paste the webhook URL first.' };
    if (!/^https?:\/\//i.test(url)) {
      return { kind: 'err', msg: 'The URL must start with http:// or https://' };
    }

    let origin;
    try { origin = new URL(url).origin; }
    catch { return { kind: 'err', msg: 'That is not a valid URL.' }; }

    /* The classic own-goal: the TEST url only fires once, and only while you are
     * watching the canvas with "Execute workflow" pressed. It is not the one the
     * lab should use. Catch it before anything else. */
    if (/\/webhook-test\//.test(url)) {
      return {
        kind: 'err',
        msg: 'That is the Test URL. It fires only once, and only while you press ' +
             '"Execute workflow" in n8n. Use the Production URL — /webhook/ , not /webhook-test/ .',
      };
    }

    /* Step 1 — is anything listening? mode:"no-cors" resolves for ANY http
     * response (even a 404) and rejects only on a real network failure, so it
     * cleanly separates "n8n is down / wrong host" from "n8n is up".
     *
     * Probe /healthz, NOT the bare origin: n8n redirects "/" to the sign-in page
     * and that redirect makes a no-cors fetch throw, which would report a
     * perfectly healthy n8n as unreachable. /healthz answers 200 on every n8n.
     * Fall back to the webhook URL itself for anything fronted by a proxy that
     * does not expose /healthz. */
    const reachable = await (async () => {
      for (const probeUrl of [`${origin}/healthz`, url]) {
        try {
          await fetch(probeUrl, { mode: 'no-cors', cache: 'no-store' });
          return true;
        } catch { /* try the next one */ }
      }
      return false;
    })();

    if (!reachable) {
      return {
        kind: 'err',
        msg: `Cannot reach n8n at ${origin} — nothing is listening there. ` +
             'Is n8n running? Check the host and port, and http:// vs https://.',
      };
    }

    /* Step 2 — reachability was all we were allowed to check. */
    if (mode === 'safe') {
      return {
        kind: 'warn',
        msg: `n8n is reachable at ${origin}. This lab spends vendor credits per run, ` +
             'so Test does not fire the workflow — activation is not proven. If the lab ' +
             'returns 404 when you use it, switch the workflow to Active in n8n.',
      };
    }

    /* Step 3 — POST for real. Only this proves the workflow is Active. */
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ __n8n_probe: true }),
        cache: 'no-store',
      });

      if (res.ok) {
        return { kind: 'ok', msg: `Connected. The workflow is Active and answered ${res.status}.` };
      }
      if (res.status === 404) {
        return {
          kind: 'err',
          msg: '404 — no webhook is registered at this path. The workflow is not Active, ' +
               'or the path does not match the Webhook node.',
        };
      }
      /* Any other readable status still proves the webhook is REGISTERED: n8n
       * only sends CORS headers for a webhook it knows about. The flow simply
       * choked on the probe payload, which carries no real fields. */
      return {
        kind: 'ok',
        msg: `Connected — the workflow is Active (n8n answered ${res.status}). It errored on the ` +
             'probe payload, which is expected: the probe sends no real input.',
      };
    } catch {
      /* No CORS headers came back. n8n emits them only for a registered webhook,
       * so this is overwhelmingly "the workflow is not Active". */
      return {
        kind: 'err',
        msg: 'No response the browser is allowed to read. n8n sends CORS headers only for a ' +
             'registered webhook, so the workflow is almost certainly NOT Active — switch it ' +
             'Active in n8n and test again. (If it is Active, check the path and that the ' +
             "Webhook node's Allowed Origins is *.)",
      };
    }
  }

  /* ── UI ────────────────────────────────────────────────────────────────── */
  const CSS = `
.n8n-conn{display:flex;gap:.5rem;align-items:center;margin:.45rem 0 0;flex-wrap:wrap}
.n8n-conn__btn{font:inherit;font-size:.82rem;font-weight:600;line-height:1;padding:.5rem .8rem;
  border-radius:.4rem;border:1px solid currentColor;background:transparent;color:inherit;
  cursor:pointer;opacity:.85}
.n8n-conn__btn:hover:not(:disabled){opacity:1}
.n8n-conn__btn:disabled{cursor:progress;opacity:.5}
.n8n-conn__msg{font-size:.8rem;line-height:1.45;margin:.4rem 0 0;flex:1 1 100%}
.n8n-conn__msg[data-kind="ok"]{color:#15803d}
.n8n-conn__msg[data-kind="err"]{color:#b91c1c}
.n8n-conn__msg[data-kind="warn"]{color:#b45309}
.n8n-conn__msg[data-kind="busy"]{opacity:.7}
@media (prefers-color-scheme:dark){
  .n8n-conn__msg[data-kind="ok"]{color:#4ade80}
  .n8n-conn__msg[data-kind="err"]{color:#f87171}
  .n8n-conn__msg[data-kind="warn"]{color:#fbbf24}
}`;

  function injectCSS() {
    if (document.getElementById('n8n-conn-css')) return;
    const s = document.createElement('style');
    s.id = 'n8n-conn-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function mount(input) {
    if (input.dataset.n8nMounted) return;
    input.dataset.n8nMounted = '1';

    const key = input.dataset.n8nKey || input.id || 'webhook';
    const mode = input.dataset.n8nTest === 'safe' ? 'safe' : 'post';
    const path = input.dataset.n8nPath || '';

    // Restore whatever the learner saved last time.
    const saved = load(key);
    if (saved && !input.value) input.value = saved;

    const row = document.createElement('div');
    row.className = 'n8n-conn';

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'n8n-conn__btn';
    btn.textContent = 'Test connection';

    const msg = document.createElement('p');
    msg.className = 'n8n-conn__msg';
    msg.setAttribute('role', 'status');

    row.append(btn, msg);
    input.insertAdjacentElement('afterend', row);

    // Persist on every edit, so the value survives a reload even without Test.
    input.addEventListener('change', () => save(key, clean(input.value)));

    btn.addEventListener('click', async () => {
      const url = clean(input.value);
      input.value = url;
      save(key, url);

      btn.disabled = true;
      msg.dataset.kind = 'busy';
      msg.textContent = mode === 'safe' ? 'Checking n8n…' : 'Sending a test request to n8n…';

      const res = await probe(url, mode, path);

      msg.dataset.kind = res.kind;
      msg.textContent = res.msg;
      btn.disabled = false;
    });
  }

  function init() {
    injectCSS();
    document.querySelectorAll('input[data-n8n-test]').forEach(mount);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.N8nConnect = { probe, load, save, url: load, clean };
})(window);
