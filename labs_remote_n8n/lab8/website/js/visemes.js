/* Text → phonemes → visemes → a time-aligned mouth-shape track.
 *
 * The grapheme-to-phoneme pass is a rule-based English approximation, not a
 * dictionary lookup. That is on purpose: it is small, offline, and wrong in
 * ways the ear does not notice, because the real audio's loudness envelope
 * (see renderer.js) gates the jaw on top of this track. */

(function (global) {
  'use strict';

  /* ── phoneme inventory ───────────────────────────────────────────── */
  // Ordered longest-first; the first pattern that matches at the cursor wins.
  const G2P_RULES = [
    ['tch', ['CH']],  ['dge', ['JH']],  ['igh', ['AY']],  ['ough', ['AO']],
    ['ch', ['CH']],   ['sh', ['SH']],   ['th', ['TH']],   ['ph', ['F']],
    ['wh', ['W']],    ['ck', ['K']],    ['ng', ['NG']],   ['qu', ['K', 'W']],
    ['gh', ['G']],    ['kn', ['N']],    ['wr', ['R']],
    ['ee', ['IY']],   ['ea', ['IY']],   ['ie', ['IY']],   ['ei', ['EY']],
    ['oo', ['UW']],   ['ou', ['AW']],   ['ow', ['AW']],   ['oa', ['OW']],
    ['oi', ['OY']],   ['oy', ['OY']],   ['ai', ['EY']],   ['ay', ['EY']],
    ['au', ['AO']],   ['aw', ['AO']],   ['ue', ['UW']],   ['ui', ['UW']],
    ['ar', ['AA', 'R']], ['er', ['ER']], ['ir', ['ER']],  ['ur', ['ER']],
    ['or', ['AO', 'R']],
    ['a', ['AE']], ['e', ['EH']], ['i', ['IH']], ['o', ['AA']], ['u', ['AH']],
    ['y', ['IY']],
    ['b', ['B']], ['c', ['K']], ['d', ['D']], ['f', ['F']], ['g', ['G']],
    ['h', ['HH']], ['j', ['JH']], ['k', ['K']], ['l', ['L']], ['m', ['M']],
    ['n', ['N']], ['p', ['P']], ['r', ['R']], ['s', ['S']], ['t', ['T']],
    ['v', ['V']], ['w', ['W']], ['x', ['K', 'S']], ['z', ['Z']],
  ];

  /* Phoneme → viseme. 15-shape set, the same family HeyGen/Oculus/Rhubarb use. */
  const PHONEME_TO_VISEME = {
    P: 'PP', B: 'PP', M: 'PP',
    F: 'FF', V: 'FF',
    TH: 'TH',
    T: 'DD', D: 'DD', L: 'DD',
    K: 'kk', G: 'kk', NG: 'kk', HH: 'kk',
    CH: 'CH', JH: 'CH', SH: 'CH', ZH: 'CH',
    S: 'SS', Z: 'SS',
    N: 'nn',
    R: 'RR', ER: 'RR',
    AA: 'aa', AE: 'aa', AY: 'aa', AH: 'aa',
    EH: 'E', EY: 'E',
    IH: 'ih', IY: 'ih',
    AO: 'oh', OW: 'oh', OY: 'oh',
    UW: 'ou', AW: 'ou', W: 'ou',
    SIL: 'sil',
  };

  /* Relative duration of each phoneme class. Vowels carry the syllable; stops
   * are a blink. Units are arbitrary — the whole track gets scaled to the audio. */
  const PHONEME_WEIGHT = {
    P: 0.5, B: 0.5, T: 0.5, D: 0.5, K: 0.55, G: 0.55,
    M: 0.8, N: 0.8, NG: 0.8, L: 0.7, R: 0.8, ER: 1.2,
    F: 0.9, V: 0.9, S: 1.0, Z: 1.0, SH: 1.0, CH: 0.9, JH: 0.9, TH: 0.9,
    HH: 0.5, W: 0.7,
    AA: 1.6, AE: 1.5, AH: 1.1, AO: 1.6, AW: 1.7, AY: 1.7,
    EH: 1.3, EY: 1.6, IH: 1.1, IY: 1.4, OW: 1.6, OY: 1.8, UW: 1.5,
    SIL: 1.0,
  };

  /* Mouth geometry per viseme, all normalised 0..1 (or -1..1 for width).
   *   jaw    — how far the jaw drops
   *   width  — corner spread: 1 = wide smile-ish, -1 = pursed
   *   round  — lip rounding / protrusion
   *   press  — lips pressed together (kills the inner mouth)
   *   teeth  — how much upper teeth show */
  const VISEME_SHAPES = {
    sil: { jaw: 0.02, width: 0.00, round: 0.00, press: 0.85, teeth: 0.00 },
    PP:  { jaw: 0.00, width: 0.05, round: 0.05, press: 1.00, teeth: 0.00 },
    FF:  { jaw: 0.12, width: 0.25, round: 0.00, press: 0.35, teeth: 0.75 },
    TH:  { jaw: 0.22, width: 0.15, round: 0.00, press: 0.00, teeth: 0.55 },
    DD:  { jaw: 0.28, width: 0.20, round: 0.00, press: 0.00, teeth: 0.50 },
    kk:  { jaw: 0.35, width: 0.10, round: 0.05, press: 0.00, teeth: 0.30 },
    CH:  { jaw: 0.22, width: -0.30, round: 0.55, press: 0.00, teeth: 0.60 },
    SS:  { jaw: 0.10, width: 0.45, round: 0.00, press: 0.10, teeth: 0.85 },
    nn:  { jaw: 0.16, width: 0.15, round: 0.00, press: 0.20, teeth: 0.35 },
    RR:  { jaw: 0.30, width: -0.15, round: 0.40, press: 0.00, teeth: 0.20 },
    aa:  { jaw: 0.95, width: 0.15, round: 0.00, press: 0.00, teeth: 0.25 },
    E:   { jaw: 0.55, width: 0.55, round: 0.00, press: 0.00, teeth: 0.45 },
    ih:  { jaw: 0.30, width: 0.60, round: 0.00, press: 0.00, teeth: 0.55 },
    oh:  { jaw: 0.65, width: -0.55, round: 0.85, press: 0.00, teeth: 0.05 },
    ou:  { jaw: 0.35, width: -0.80, round: 1.00, press: 0.00, teeth: 0.00 },
  };

  /* ── grapheme → phoneme ──────────────────────────────────────────── */
  function wordToPhonemes(raw) {
    let w = raw.toLowerCase().replace(/[^a-z']/g, '');
    if (!w) return [];

    // Silent trailing 'e' ("make", "time") — but keep it in "be", "the".
    if (w.length > 3 && w.endsWith('e') && !/[aeiou]e$/.test(w)) w = w.slice(0, -1);

    const out = [];
    let i = 0;
    while (i < w.length) {
      let matched = false;
      for (const [pattern, phonemes] of G2P_RULES) {
        if (w.startsWith(pattern, i)) {
          // Doubled consonants ("letter", "happy") are one sound.
          const prev = out[out.length - 1];
          if (!(phonemes.length === 1 && prev === phonemes[0] && !isVowel(phonemes[0]))) {
            out.push(...phonemes);
          }
          i += pattern.length;
          matched = true;
          break;
        }
      }
      if (!matched) i++; // apostrophes and anything exotic
    }
    return out;
  }

  const VOWELS = new Set(['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UW']);
  const isVowel = (p) => VOWELS.has(p);

  /* ── script → weighted phoneme sequence ──────────────────────────── */
  // Splits on whitespace, keeps punctuation as silences so pauses land where
  // a human would take one.
  function scriptToSequence(text) {
    const seq = [];
    const tokens = String(text).trim().split(/\s+/).filter(Boolean);

    for (const token of tokens) {
      const phonemes = wordToPhonemes(token);
      for (const p of phonemes) {
        seq.push({ phoneme: p, viseme: PHONEME_TO_VISEME[p] || 'nn', weight: PHONEME_WEIGHT[p] || 1 });
      }
      // Punctuation → a silence proportional to how hard the stop is.
      const tail = token.match(/[,;:.!?…—-]+$/);
      if (tail) {
        const hard = /[.!?…]/.test(tail[0]);
        seq.push({ phoneme: 'SIL', viseme: 'sil', weight: hard ? 3.0 : 1.4 });
      } else if (phonemes.length) {
        seq.push({ phoneme: 'SIL', viseme: 'sil', weight: 0.25 }); // inter-word gap
      }
    }
    if (!seq.length) seq.push({ phoneme: 'SIL', viseme: 'sil', weight: 1 });
    return seq;
  }

  /* ── sequence → timeline stretched onto a real audio duration ────── */
  function buildTimeline(text, durationSec, opts = {}) {
    const leadIn = opts.leadIn ?? 0.08;   // audio almost never starts on frame 0
    const seq = scriptToSequence(text);
    const total = seq.reduce((s, p) => s + p.weight, 0) || 1;
    const speakable = Math.max(0.2, durationSec - leadIn);
    const scale = speakable / total;

    const track = [];
    let t = leadIn;
    for (const p of seq) {
      const dur = p.weight * scale;
      track.push({ start: t, end: t + dur, viseme: p.viseme, phoneme: p.phoneme });
      t += dur;
    }
    return track;
  }

  /* Sample the track at time t, cross-fading between neighbouring visemes so
   * the mouth glides instead of snapping. */
  function sampleTimeline(track, t, blendSec = 0.045) {
    if (!track || !track.length) return { ...VISEME_SHAPES.sil, viseme: 'sil' };

    let i = 0;
    while (i < track.length - 1 && track[i].end < t) i++;
    const cur = track[i];
    const shape = { ...VISEME_SHAPES[cur.viseme] };

    // Blend into the next viseme over the final `blendSec` of this one.
    const next = track[i + 1];
    if (next) {
      const remain = cur.end - t;
      if (remain < blendSec) {
        const k = clamp(1 - remain / blendSec, 0, 1) * 0.5; // 0 → 0.5 at the boundary
        const nShape = VISEME_SHAPES[next.viseme];
        for (const key of ['jaw', 'width', 'round', 'press', 'teeth']) {
          shape[key] = shape[key] * (1 - k) + nShape[key] * k;
        }
      }
    }
    shape.viseme = cur.viseme;
    return shape;
  }

  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  global.Visemes = { buildTimeline, sampleTimeline };
})(window);
