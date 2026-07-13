/* The 2D talking-head renderer.
 *
 * A photo has no jaw, so we fake one: the lower face is redrawn as a stack of
 * horizontal slices displaced downward, which reads as the jaw dropping. On top
 * of that we composite an inner mouth (dark cavity + teeth + tongue) and lips
 * painted in colours sampled from the photo itself, so the overlay inherits the
 * subject's skin and lighting instead of looking pasted on.
 *
 * Shape comes from the viseme track (visemes.js); *timing* comes from the real
 * audio's loudness, so silences close the mouth no matter what the text said. */

(function (global) {
  'use strict';

  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const smoothstep = (t) => { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); };

  class Renderer {
    constructor(canvas) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.image = null;
      this.rig = null;
      this.metrics = null;

      // The smoothed pose the mouth is actually drawn at, chased toward the target.
      this.pose = { jaw: 0, width: 0, round: 0, press: 1, teeth: 0 };
      this.crop = null;
      this.opts = { gain: 1, smoothing: 0.55, sway: true, breath: true, debug: false, frame: true };

      this.palette = null;
      this.viseme = 'sil';

      this._warpLayer = document.createElement('canvas');
    }

    setImage(image, rig) {
      this.image = image;
      this.setRig(rig);
      this.fit();
      this.palette = this._samplePalette();
    }

    setRig(rig) {
      this.rig = rig;
      this.metrics = global.Face.metrics(rig);
      if (this.image) { this.fit(); this.palette = this._samplePalette(); }
    }

    setOptions(patch) {
      const reframe = 'frame' in patch && patch.frame !== this.opts.frame;
      Object.assign(this.opts, patch);
      if (reframe && this.image) this.fit();
    }

    /* Decide which part of the photo the stage actually shows.
     *
     * "Frame to head" crops to a portrait box built from the rig, which is what
     * makes a full-body or group photo usable at all: the head fills the stage
     * instead of being forty pixels tall in the corner. Off, we show the whole
     * image. Either way this sets `crop` + `scale`, and every other coordinate in
     * the renderer goes through P()/S(), so nothing else has to care. */
    fit() {
      const img = this.image;
      const iw = img.naturalWidth, ih = img.naturalHeight;
      const m = this.metrics;

      let crop;
      if (this.opts.frame && m) {
        const fs = m.faceScale;                       // eyes → mouth distance
        let h = fs * 5.0;                             // forehead down to upper chest
        let w = h * 0.8;                              // 4:5 portrait
        // Never crop bigger than the photo we have.
        const k = Math.min(1, iw / w, ih / h);
        w *= k; h *= k;

        let x = m.eyeCenter.x - w / 2;
        let y = m.eyeCenter.y - h * 0.34;             // eyes sit on the upper third
        x = clamp(x, 0, iw - w);
        y = clamp(y, 0, ih - h);
        crop = { x, y, w, h };
      } else {
        crop = { x: 0, y: 0, w: iw, h: ih };
      }
      this.crop = crop;

      const maxW = 720, maxH = 900;
      const s = Math.min(maxW / crop.w, maxH / crop.h);
      this.canvas.width = Math.round(crop.w * s);
      this.canvas.height = Math.round(crop.h * s);
      this.scale = s;

      this._warpLayer.width = this.canvas.width;
      this._warpLayer.height = this.canvas.height;
    }

    // image pixel space → canvas space
    P(p) { return { x: (p.x - this.crop.x) * this.scale, y: (p.y - this.crop.y) * this.scale }; }
    S(v) { return v * this.scale; }
    // canvas y → image y, the inverse used by the jaw slices
    Y(yCanvas) { return this.crop.y + yCanvas / this.scale; }

    /* Pull skin, lip and shadow colours straight out of the photo so the drawn
     * mouth matches the subject under whatever lighting they were shot in. */
    _samplePalette() {
      const off = document.createElement('canvas');
      off.width = this.image.naturalWidth;
      off.height = this.image.naturalHeight;
      const c = off.getContext('2d', { willReadFrequently: true });
      c.drawImage(this.image, 0, 0);

      const m = this.metrics;
      const at = (x, y) => {
        x = clamp(Math.round(x), 0, off.width - 1);
        y = clamp(Math.round(y), 0, off.height - 1);
        const d = c.getImageData(x, y, 1, 1).data;
        return [d[0], d[1], d[2]];
      };
      const avg = (pts) => {
        const s = pts.reduce((a, p) => [a[0] + p[0], a[1] + p[1], a[2] + p[2]], [0, 0, 0]);
        return s.map((v) => Math.round(v / pts.length));
      };
      const lum = (p) => p[0] + p[1] + p[2];

      /* Read a patch and keep only its brighter half.
       *
       * Skin sampled from a single point is a trap: on a bearded man the chin is
       * beard, on a shadowed face the cheek edge is shadow. Either one returns a
       * near-black "skin" colour, which then poisons the teeth and the eyelids.
       * Sampling a patch and discarding the dark half rejects beard, stubble and
       * shadow, because skin is reliably the brighter population. */
      const patch = (cx, cy, radius) => {
        const pts = [];
        for (let dy = -2; dy <= 2; dy++) {
          for (let dx = -2; dx <= 2; dx++) {
            pts.push(at(cx + (dx * radius) / 2, cy + (dy * radius) / 2));
          }
        }
        pts.sort((a, b) => lum(b) - lum(a));
        return avg(pts.slice(0, Math.ceil(pts.length / 2)));
      };

      const fs = m.faceScale;
      // Cheeks — high, beside the nose, well clear of any beard line.
      const cheekY = m.eyeCenter.y + (m.mouthCenter.y - m.eyeCenter.y) * 0.45;
      const skin = avg([
        patch(m.eyeCenter.x - m.eyeWidth * 0.62, cheekY, fs * 0.08),
        patch(m.eyeCenter.x + m.eyeWidth * 0.62, cheekY, fs * 0.08),
      ]);
      // Lips: just above and below the mouth line, near the centre.
      const lip = avg([
        at(m.mouthCenter.x, m.mouthCenter.y - fs * 0.045),
        at(m.mouthCenter.x, m.mouthCenter.y + fs * 0.045),
        at(m.mouthCenter.x - m.mouthWidth * 0.2, m.mouthCenter.y),
      ]);

      const rgb = (v) => `rgb(${v[0]},${v[1]},${v[2]})`;
      const shade = (v, k) => rgb(v.map((x) => clamp(Math.round(x * k), 0, 255)));

      return {
        // Cavity shades come off the lip colour, so the inside of the mouth stays
        // in the same colour family (and the same light) as the face it's cut into.
        cavityDark: shade(lip, 0.16),
        cavity: shade(lip, 0.30),
        // Teeth are near-white but carry the scene's tint, so we pull them most
        // of the way to white rather than scaling the skin (which on a dark or
        // bearded face produced brown teeth).
        teeth: rgb(skin.map((v) => clamp(Math.round(v * 0.25 + 232 * 0.75), 0, 255))),
        tongue: `rgb(${(lip[0] * 0.62) | 0},${(lip[1] * 0.34) | 0},${(lip[2] * 0.36) | 0})`,
      };
    }

    /* ── the frame ───────────────────────────────────────────────────
     * shape : sampled viseme from the timeline (or null for idle)
     * level : 0..1 loudness of the audio right now
     * t     : seconds since playback started (drives idle motion) */
    draw(shape, level, t) {
      const ctx = this.ctx;
      const W = this.canvas.width, H = this.canvas.height;

      ctx.clearRect(0, 0, W, H);
      if (!this.image) return;

      const target = shape || { jaw: 0.02, width: 0, round: 0, press: 0.85, teeth: 0, viseme: 'sil' };
      this.viseme = target.viseme || 'sil';

      // Loudness gates the jaw: the viseme says *what* shape, the audio says how
      // far into it we actually are. Below the floor, everything closes.
      const energy = clamp(level, 0, 1);
      const drive = energy < 0.04 ? 0 : clamp(0.3 + 0.85 * energy, 0, 1.1);

      const want = {
        jaw:   clamp(target.jaw * drive * this.opts.gain, 0, 1),
        width: target.width,
        round: target.round,
        press: lerp(target.press, 1, 1 - clamp(drive * 1.6, 0, 1)),
        teeth: target.teeth * clamp(drive * 1.4, 0, 1),
      };

      // One-pole smoothing, so the mouth glides between shapes.
      const k = 1 - this.opts.smoothing;
      for (const key of Object.keys(this.pose)) {
        this.pose[key] = lerp(this.pose[key], want[key], k);
      }

      ctx.save();
      this._applyHeadMotion(ctx, t, energy);
      this._drawWarpedFace(ctx);
      this._drawMouth(ctx);
      ctx.restore();

      if (this.opts.debug) this._drawRig(ctx);
    }

    /* Idle life: a slow figure-of-eight sway plus a breathing scale, pivoting
     * around the base of the neck rather than the image centre. */
    _applyHeadMotion(ctx, t, energy) {
      const m = this.metrics;
      const pivot = this.P({ x: m.mouthCenter.x, y: m.mouthCenter.y + m.faceScale * 1.6 });

      // A hair of overscan: the sway rotates the whole frame, and without this
      // the corners would swing off the canvas and show through as blank.
      let rot = 0, dx = 0, dy = 0, sc = this.opts.sway ? 1.05 : 1;
      if (this.opts.sway) {
        rot = Math.sin(t * 0.55) * 0.010 + Math.sin(t * 0.23 + 1.1) * 0.006;
        dx = Math.sin(t * 0.41) * this.S(m.faceScale * 0.014);
        dy = Math.sin(t * 0.77 + 0.6) * this.S(m.faceScale * 0.009);
        // Speech nudges the head a little — energy leaks into motion.
        rot += Math.sin(t * 6.1) * 0.004 * energy;
        dy -= this.S(m.faceScale * 0.012) * energy;
      }
      if (this.opts.breath) sc *= 1 + Math.sin(t * 0.9) * 0.0035;

      ctx.translate(pivot.x + dx, pivot.y + dy);
      ctx.rotate(rot);
      ctx.scale(sc, sc);
      ctx.translate(-pivot.x, -pivot.y);
    }

    /* Jaw drop = a vertical stretch of the lower face, done as a stack of thin
     * slices pulled from progressively higher source rows.
     *
     * Two things keep it from tearing the photo apart:
     *   · the displaced slices are masked to a soft-edged ellipse over the jaw,
     *     so the background and the rest of the head are never touched;
     *   · displacement fades back to zero before that ellipse ends, so the mask
     *     boundary always sits on top of pixels identical to the ones beneath —
     *     no seam, at any jaw angle. */
    _drawWarpedFace(ctx) {
      const img = this.image;
      const W = this.canvas.width, H = this.canvas.height;
      const m = this.metrics;
      const fs = m.faceScale;
      const cr = this.crop;

      ctx.drawImage(img, cr.x, cr.y, cr.w, cr.h, 0, 0, W, H); // untouched base

      const jaw = clamp(this.pose.jaw, 0, 1.1);
      if (jaw < 0.005) return;

      const drop = fs * 0.085 * jaw;              // full-open jaw travel, in image px
      const topImg = m.mouthCenter.y - fs * 0.10; // just above the upper lip
      const botImg = m.mouthCenter.y + fs * 0.85; // below the chin, into the neck
      const span = botImg - topImg;

      // 0 at the top of the region → 1 at the chin → back to 0 at the bottom.
      const profile = (u) => {
        if (u < 0.55) return smoothstep(u / 0.55);
        if (u < 0.70) return 1;
        return 1 - smoothstep((u - 0.70) / 0.30);
      };

      const wl = this._warpLayer.getContext('2d');
      wl.setTransform(1, 0, 0, 1, 0, 0);
      wl.globalCompositeOperation = 'source-over';
      wl.filter = 'none';
      wl.clearRect(0, 0, W, H);

      const yTop = Math.max(0, Math.floor((topImg - cr.y) * this.scale));
      const yBot = Math.min(H, Math.ceil((botImg - cr.y) * this.scale));
      const SLICE = 2;

      for (let y = yTop; y < yBot; y += SLICE) {
        const yImg = this.Y(y);
        const d = drop * profile((yImg - topImg) / span);
        const srcY = clamp(yImg - d, 0, img.naturalHeight - 1);
        const srcH = Math.max(0.5, SLICE / this.scale);
        wl.drawImage(img, cr.x, srcY, cr.w, srcH, 0, y, W, SLICE + 1);
      }

      // Mask to the jaw. The blur is what makes the edge disappear.
      const cx = this.P(m.mouthCenter).x;
      const cy = (((topImg + botImg) / 2) - cr.y) * this.scale;
      wl.globalCompositeOperation = 'destination-in';
      wl.filter = `blur(${Math.max(2, this.S(fs * 0.10)).toFixed(1)}px)`;
      wl.fillStyle = '#000';
      wl.beginPath();
      wl.ellipse(cx, cy, this.S(fs * 0.78), (yBot - yTop) / 2, 0, 0, Math.PI * 2);
      wl.fill();

      ctx.drawImage(this._warpLayer, 0, 0);
    }

    /* The open mouth, composited straight onto the frame.
     *
     * Drawn onto the frame rather than an offscreen layer on purpose: the cavity
     * uses `multiply`, which only means anything when it has the photo's own
     * pixels underneath to darken. Multiplied into a transparent layer it is just
     * an opaque fill — which is exactly what made the mouth look like a sticker. */
    _drawMouth(ctx) {
      const m = this.metrics;
      const p = this.pose;
      const pal = this.palette;

      // A jaw hinges at the ears, so the mouth opens almost entirely *downward*:
      // the upper lip barely moves.
      const jawShift = this.S(m.faceScale * 0.085 * p.jaw * 0.25);
      const c = this.P(m.mouthCenter);
      const cx = c.x, cy = c.y + jawShift;

      const baseW = this.S(m.mouthWidth);
      // Width: spread on /i/ and /s/, purse hard on /u/ and /o/.
      const halfW = baseW * 0.5 * (1 + 0.16 * p.width - 0.34 * p.round);
      const open = clamp(1 - p.press, 0, 1);

      // A real speaking mouth is rarely more than ~0.4 × its width tall.
      const gape = baseW * 0.42 * clamp(p.jaw, 0, 1) * open;
      const topY = -gape * 0.22;
      const botY = gape * 0.78;

      // A shut mouth gets nothing drawn on it at all. The photo already has lips;
      // painting our own over them was making every silent frame look fake.
      if (gape <= this.S(m.faceScale * 0.010)) return;

      const feather = Math.max(1.2, baseW * 0.025);

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(m.mouthAngle);

      // 1 — cavity: darkens the photo instead of covering it, so skin texture and
      // lighting survive. Inset inside the lip line (0.84) so the lips still read.
      const cavW = halfW * 0.84;
      const grad = ctx.createLinearGradient(0, topY, 0, botY);
      grad.addColorStop(0, pal.cavityDark);
      grad.addColorStop(0.45, pal.cavity);
      grad.addColorStop(1, pal.tongue);

      ctx.filter = `blur(${feather.toFixed(2)}px)`;
      ctx.globalCompositeOperation = 'multiply';
      ctx.globalAlpha = open;
      ctx.fillStyle = grad;
      ctx.beginPath();
      mouthPath(ctx, cavW, topY, botY);
      ctx.fill();
      ctx.globalCompositeOperation = 'source-over';

      // 2 — teeth and tongue live strictly inside the cavity.
      ctx.beginPath();
      mouthPath(ctx, cavW, topY, botY);
      ctx.clip();

      const teeth = clamp(p.teeth, 0, 1);
      if (teeth > 0.05) {
        const th = gape * (0.16 + 0.18 * teeth);
        ctx.globalAlpha = teeth * 0.75;
        ctx.fillStyle = pal.teeth;
        ctx.beginPath();
        ctx.moveTo(-cavW, topY - gape * 0.15);
        ctx.lineTo(cavW, topY - gape * 0.15);
        ctx.quadraticCurveTo(cavW * 0.5, topY + th * 1.3, 0, topY + th);
        ctx.quadraticCurveTo(-cavW * 0.5, topY + th * 1.3, -cavW, topY - gape * 0.15);
        ctx.closePath();
        ctx.fill();
      }

      if (p.jaw > 0.3) {
        ctx.globalAlpha = clamp((p.jaw - 0.3) * 1.1, 0, 0.4);
        ctx.fillStyle = pal.tongue;
        ctx.beginPath();
        ctx.ellipse(0, botY * 1.1, cavW * 0.8, gape * 0.4, 0, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }

    /* Blinking used to live here. It painted a skin-coloured ellipse over each eye
     * and swept it down — which on a drawing reads as an eyelid, and on a real
     * photograph reads as a flash. There is no amount of tuning that fixes it: the
     * eye it has to cover is a photograph of an open eye, and a flat fill can't
     * become a lid. Doing nothing looks better than doing it badly, so the avatar
     * simply doesn't blink. A model that generates eyelid pixels (SadTalker, Hallo)
     * is the only honest way to get this. */

    _drawRig(ctx) {
      const m = this.metrics;
      ctx.save();
      ctx.strokeStyle = 'rgba(87,224,176,.9)';
      ctx.lineWidth = 1;
      for (const key of ['eyeL', 'eyeR', 'mouthL', 'mouthR']) {
        const p = this.P(this.rig[key]);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
        ctx.stroke();
      }
      const c = this.P(m.mouthCenter);
      ctx.strokeStyle = 'rgba(110,168,255,.8)';
      ctx.setLineDash([3, 3]);
      ctx.strokeRect(
        c.x - this.S(m.mouthWidth) * 0.75, c.y - this.S(m.faceScale * 0.12),
        this.S(m.mouthWidth) * 1.5, this.S(m.faceScale * 0.30)
      );
      ctx.restore();
    }

    /* Idle frame — avatar sitting there breathing, mouth shut. */
    idle(t) { this.draw(null, 0, t); }
  }

  /* An asymmetric almond: pinched at the corners, shallow on top, deep below.
   * `top` is negative, `bot` positive, both relative to the mouth line. */
  function mouthPath(c, halfW, top, bot) {
    c.moveTo(-halfW, 0);
    c.quadraticCurveTo(-halfW * 0.5, top * 1.25, 0, top);
    c.quadraticCurveTo(halfW * 0.5, top * 1.25, halfW, 0);
    c.quadraticCurveTo(halfW * 0.5, bot * 1.15, 0, bot);
    c.quadraticCurveTo(-halfW * 0.5, bot * 1.15, -halfW, 0);
    c.closePath();
  }

  global.Renderer = Renderer;
})(window);
