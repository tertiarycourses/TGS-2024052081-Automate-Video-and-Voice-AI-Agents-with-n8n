/* The rig: four points in image pixel space that everything else derives from.
 *   eyeL / eyeR  — pupil centres (set the head's roll axis and the face's scale)
 *   mouthL/mouthR— mouth corners (drive width, angle and the warp region)
 * Auto-placed on load, then hand-corrected in the rig dialog. */

(function (global) {
  'use strict';

  function defaultRig(w, h) {
    // Portrait framing that holds for most head-and-shoulders photos.
    return {
      eyeL:   { x: w * 0.385, y: h * 0.400 },
      eyeR:   { x: w * 0.615, y: h * 0.400 },
      mouthL: { x: w * 0.425, y: h * 0.640 },
      mouthR: { x: w * 0.575, y: h * 0.640 },
    };
  }

  /* Real landmark detection, via MediaPipe's face_landmarker running on WASM.
   *
   * This is what makes an arbitrary photo work without hand-placing the rig.
   * Everything is vendored under /vendor, so it runs offline after the first
   * load — nothing is fetched from a CDN at runtime.
   *
   * Indices into the 478-point mesh (the mesh is mirrored: index 33 is on the
   * LEFT of the image, which is the subject's right eye):
   *   33 / 133  — image-left eye, outer + inner corner
   *   362 / 263 — image-right eye, inner + outer corner
   *   61 / 291  — mouth corners */
  const LM = { eyeL: [33, 133], eyeR: [362, 263], mouthL: 61, mouthR: 291 };

  let landmarkerPromise = null;

  function loadLandmarker() {
    if (landmarkerPromise) return landmarkerPromise;

    landmarkerPromise = (async () => {
      const vision = await import('/vendor/vision_bundle.mjs');
      const fileset = await vision.FilesetResolver.forVisionTasks('/vendor/wasm');
      return vision.FaceLandmarker.createFromOptions(fileset, {
        baseOptions: { modelAssetPath: '/vendor/face_landmarker.task' },
        runningMode: 'IMAGE',
        numFaces: 1,
      });
    })().catch((err) => {
      landmarkerPromise = null; // let a later attempt retry
      throw err;
    });

    return landmarkerPromise;
  }

  /* Run the model over one rectangle of the photo, scaled into a square-ish input.
   * Returns landmarks already mapped back into image pixel coordinates. */
  const _scratch = document.createElement('canvas');

  function detectIn(landmarker, image, rect) {
    const MAX = 640; // the detector wants a face that's a decent share of its input
    const s = Math.min(MAX / rect.w, MAX / rect.h, 4);
    _scratch.width = Math.max(2, Math.round(rect.w * s));
    _scratch.height = Math.max(2, Math.round(rect.h * s));

    const c = _scratch.getContext('2d');
    c.clearRect(0, 0, _scratch.width, _scratch.height);
    c.drawImage(image, rect.x, rect.y, rect.w, rect.h, 0, 0, _scratch.width, _scratch.height);

    const pts = landmarker.detect(_scratch).faceLandmarks?.[0];
    if (!pts) return null;

    // normalised-in-crop → pixels-in-crop → pixels-in-image
    return pts.map((p) => ({ x: rect.x + p.x * rect.w, y: rect.y + p.y * rect.h }));
  }

  /* A face 60px tall inside a 1792×2400 photo is invisible to the detector when
   * the whole frame is fed in at once. So: try the whole frame, then sweep
   * progressively smaller overlapping tiles and stop at the first face. This is
   * what makes full-body and group shots work instead of silently falling back
   * to default framing. */
  function searchRects(w, h) {
    const rects = [{ x: 0, y: 0, w, h }];

    for (const div of [2, 3, 4]) {
      const tw = w / div, th = h / div;
      const stepX = tw / 2, stepY = th / 2; // 50% overlap: no face falls down a seam
      for (let y = 0; y + th <= h + 1; y += stepY) {
        for (let x = 0; x + tw <= w + 1; x += stepX) {
          rects.push({
            x: Math.max(0, Math.min(w - tw, x)),
            y: Math.max(0, Math.min(h - th, y)),
            w: tw, h: th,
          });
        }
      }
    }
    return rects;
  }

  async function autoDetect(image) {
    const w = image.naturalWidth, h = image.naturalHeight;
    const fallback = defaultRig(w, h);

    let landmarker;
    try {
      landmarker = await loadLandmarker();
    } catch (err) {
      // Model missing or WASM blocked — the rig is still hand-placeable.
      return { rig: fallback, detected: false, reason: err.message };
    }

    for (const rect of searchRects(w, h)) {
      let pts;
      try {
        pts = detectIn(landmarker, image, rect);
      } catch {
        continue;
      }
      if (!pts) continue;

      const mid = ([a, b]) => ({ x: (pts[a].x + pts[b].x) / 2, y: (pts[a].y + pts[b].y) / 2 });
      return {
        rig: {
          eyeL: mid(LM.eyeL),
          eyeR: mid(LM.eyeR),
          mouthL: pts[LM.mouthL],
          mouthR: pts[LM.mouthR],
        },
        detected: true,
      };
    }

    return { rig: fallback, detected: false, reason: 'no face found' };
  }

  /* Everything the renderer needs, in one derived object. */
  function metrics(rig) {
    const { mouthL, mouthR, eyeL, eyeR } = rig;
    const mouthW = Math.hypot(mouthR.x - mouthL.x, mouthR.y - mouthL.y);
    const eyeW = Math.hypot(eyeR.x - eyeL.x, eyeR.y - eyeL.y);
    return {
      mouthCenter: { x: (mouthL.x + mouthR.x) / 2, y: (mouthL.y + mouthR.y) / 2 },
      mouthWidth: mouthW,
      mouthAngle: Math.atan2(mouthR.y - mouthL.y, mouthR.x - mouthL.x),
      eyeCenter: { x: (eyeL.x + eyeR.x) / 2, y: (eyeL.y + eyeR.y) / 2 },
      eyeWidth: eyeW,
      // Distance eyes→mouth is the most reliable scale reference on a face.
      faceScale: Math.hypot(
        (mouthL.x + mouthR.x) / 2 - (eyeL.x + eyeR.x) / 2,
        (mouthL.y + mouthR.y) / 2 - (eyeL.y + eyeR.y) / 2
      ),
    };
  }

  /* ── the drag-the-handles editor ─────────────────────────────────── */
  const HANDLES = [
    { key: 'eyeL',   label: 'L eye',   color: '#57e0b0' },
    { key: 'eyeR',   label: 'R eye',   color: '#57e0b0' },
    { key: 'mouthL', label: 'L corner', color: '#6ea8ff' },
    { key: 'mouthR', label: 'R corner', color: '#6ea8ff' },
  ];

  function createEditor(canvas, image, rig) {
    const ctx = canvas.getContext('2d');
    const working = JSON.parse(JSON.stringify(rig));

    const maxW = 560, maxH = 480;
    const fit = Math.min(maxW / image.naturalWidth, maxH / image.naturalHeight, 1);
    canvas.width = Math.round(image.naturalWidth * fit);
    canvas.height = Math.round(image.naturalHeight * fit);

    /* Wheel-zoom and pan. Without this, placing handles on a face that is 60px
     * tall inside a full-body photo is guesswork. */
    const view = { zoom: 1, ox: 0, oy: 0 }; // ox/oy = top-left of the view, in image px

    const px = () => fit * view.zoom;       // image px → canvas px
    const toCanvas = (p) => ({ x: (p.x - view.ox) * px(), y: (p.y - view.oy) * px() });
    const toImage = (x, y) => ({ x: x / px() + view.ox, y: y / px() + view.oy });

    function clampView() {
      const viewW = canvas.width / px(), viewH = canvas.height / px();
      view.ox = Math.max(0, Math.min(image.naturalWidth - viewW, view.ox));
      view.oy = Math.max(0, Math.min(image.naturalHeight - viewH, view.oy));
    }

    let dragging = null;   // a handle key, or 'pan'
    let panFrom = null;

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const viewW = canvas.width / px(), viewH = canvas.height / px();
      ctx.drawImage(image, view.ox, view.oy, viewW, viewH, 0, 0, canvas.width, canvas.height);

      // Mouth axis, so the user can see the angle they're setting.
      const ml = toCanvas(working.mouthL), mr = toCanvas(working.mouthR);
      ctx.strokeStyle = 'rgba(110,168,255,.55)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(ml.x, ml.y); ctx.lineTo(mr.x, mr.y); ctx.stroke();
      ctx.setLineDash([]);

      for (const h of HANDLES) {
        const p = toCanvas(working[h.key]);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 7, 0, Math.PI * 2);
        ctx.fillStyle = h.color;
        ctx.fill();
        ctx.strokeStyle = 'rgba(0,0,0,.7)';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.font = '11px -apple-system, sans-serif';
        ctx.fillStyle = 'rgba(255,255,255,.9)';
        ctx.strokeStyle = 'rgba(0,0,0,.8)';
        ctx.lineWidth = 3;
        ctx.strokeText(h.label, p.x + 11, p.y - 8);
        ctx.fillText(h.label, p.x + 11, p.y - 8);
      }
    }

    function hit(x, y) {
      for (const h of HANDLES) {
        const p = toCanvas(working[h.key]);
        if (Math.hypot(p.x - x, p.y - y) < 14) return h.key;
      }
      return null;
    }

    const pos = (e) => {
      const r = canvas.getBoundingClientRect();
      return {
        x: (e.clientX - r.left) * (canvas.width / r.width),
        y: (e.clientY - r.top) * (canvas.height / r.height),
      };
    };

    canvas.onpointerdown = (e) => {
      const { x, y } = pos(e);
      const handle = hit(x, y);
      dragging = handle || 'pan';
      if (dragging === 'pan') panFrom = { x, y, ox: view.ox, oy: view.oy };
      canvas.setPointerCapture(e.pointerId);
    };

    canvas.onpointermove = (e) => {
      if (!dragging) return;
      const { x, y } = pos(e);

      if (dragging === 'pan') {
        view.ox = panFrom.ox - (x - panFrom.x) / px();
        view.oy = panFrom.oy - (y - panFrom.y) / px();
        clampView();
      } else {
        working[dragging] = toImage(
          Math.max(0, Math.min(canvas.width, x)),
          Math.max(0, Math.min(canvas.height, y))
        );
      }
      draw();
    };

    canvas.onpointerup = () => { dragging = null; panFrom = null; };

    canvas.onwheel = (e) => {
      e.preventDefault();
      const { x, y } = pos(e);
      const under = toImage(x, y);                      // keep this point pinned
      view.zoom = Math.max(1, Math.min(12, view.zoom * (e.deltaY < 0 ? 1.15 : 1 / 1.15)));
      view.ox = under.x - x / px();
      view.oy = under.y - y / px();
      clampView();
      draw();
    };

    draw();
    return { commit: () => JSON.parse(JSON.stringify(working)) };
  }

  global.Face = { defaultRig, autoDetect, metrics, createEditor };
})(window);
