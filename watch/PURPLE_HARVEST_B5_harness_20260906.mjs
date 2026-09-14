// PURPLE HARVEST B5 — BAD APPLE FIELD falsifier harness (2026-09-06)
// Honest-verification rig: does NOT retype the pipeline. It loads the SHIPPED page
// (dashboard/static/bad_apple_field.html), stubs the DOM, evaluates the full page
// script (so the tested code IS the shipped code), and drives the real loop.
// Falsifiers from watch/PURPLE_HARVEST_TRIAGE_02_20260906.md (TRIAGE 06 / B5 card):
//   (1) DETERMINISM: rendering frame N twice gives byte-identical ImageData
//   (2) SUBSTRATE != PASSTHROUGH: mean|raw-field| > 8, and == 0 in identity mode
//   (3) PERF: render hot path <= 8ms/frame median on the 1200-frame segment
//   (4) LEDGER: append-only under pause/seek (driven through real keydown handlers)
// Plus a provenance check: the embedded frames must reproduce the ffmpeg-extracted
// source bytes (watch/inbox/bad_apple/seg.raw) bit-for-bit on sample frames.
import fs from 'fs';
import { performance } from 'perf_hooks';

const ROOT = 'C:/Users/foste/Documents/projects/local_sovereign_agent';
const html = fs.readFileSync(ROOT + '/dashboard/static/bad_apple_field.html', 'utf8');

// ---- extract the main script (the one with "use strict") ----------------------
const s0 = html.indexOf('<script>\n"use strict";');
const s1 = html.lastIndexOf('</script>');
if (s0 < 0 || s1 <= s0) throw new Error('main script not found');
const SCRIPT = html.slice(s0 + '<script>'.length, s1);

// ---- DOM stubs ----------------------------------------------------------------
function makeEl(tag) {
  return { tagName: tag, innerHTML: '', textContent: '', className: '', style: {},
    children: [],
    get firstChild() { return this.children[0] || null; },
    get lastChild() { return this.children[this.children.length - 1] || null; },
    appendChild(ch) { this.children.push(ch); return ch; },
    removeChild(ch) { const i = this.children.indexOf(ch); if (i >= 0) this.children.splice(i, 1); return ch; },
    querySelector(sel) { return sel === '.tot' ? (this.children.find(c => c.className === 'tot') || null) : null; } };
}
const falsEl = makeEl('div'), hudEl = makeEl('div'), ledgerEl = makeEl('div'), errEl = makeEl('div');
let putCount = 0;
const ctx = {
  imageSmoothingEnabled: false,
  createImageData(w, h) { return { data: new Uint8ClampedArray(w * h * 4), width: w, height: h }; },
  putImageData() { putCount++; }
};
const canvasEl = { width: 0, height: 0, getContext() { return ctx; } };
const elements = { c: canvasEl, hud: hudEl, fals: falsEl, ledger: ledgerEl, errbanner: errEl };
const handlers = {};
const windowStub = { addEventListener(type, fn) { (handlers[type] = handlers[type] || []).push(fn); } };
const rAFQ = [];
const raf = cb => { rAFQ.push(cb); return rAFQ.length; };

const run = new Function('window', 'document', 'performance', 'requestAnimationFrame', 'setInterval', SCRIPT);
run(windowStub, { getElementById: id => elements[id], createElement: makeEl }, performance, raf, () => 0);

const APP = windowStub.__BADAPPLE;
if (!APP) throw new Error('page did not expose window.__BADAPPLE');
const F = APP.FIELD, LEDGER = APP.LEDGER;

let fails = 0;
function check(name, ok, detail) {
  console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (detail ? '  — ' + detail : ''));
  if (!ok) fails++;
}

console.log('== B5 BAD APPLE FIELD — falsifiers (shipped code, Node 22 harness) ==');

// (0) decode integrity: the RLE stream must consume exactly
check('DECODE  RLE stream consumed exactly', F.decodeCheck.consumed === F.decodeCheck.total,
  `consumed=${F.decodeCheck.consumed} pxBytes=${F.decodeCheck.total} frames=${F.N} uniq=${F.N ? '' : ''}`);
check('DECODE  frame count', F.N === 1200, `N=${F.N}`);

// provenance: embedded frames reproduce the ffmpeg gray source bit-for-bit
{
  const raw = fs.readFileSync(ROOT + '/watch/inbox/bad_apple/seg.raw');
  const W = 96, H = 72, STRIDE = 12;
  let bad = 0, checked = 0;
  for (const f of [0, 1, 299, 300, 600, 900, 1199]) {
    const pk = F.frameUniq[f] * (STRIDE * H);
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const src = raw[f * W * H + y * W + x] >= 128 ? 1 : 0;
        const got = (F.packed[pk + y * STRIDE + (x >> 3)] >> (7 - (x & 7))) & 1;
        if (src !== got) bad++;
        checked++;
      }
    }
  }
  check('PROVENANCE embedded bits == ffmpeg gray source (7 frames, all pixels)', bad === 0,
    `${checked} pixels checked, ${bad} mismatches`);
}

// (1) DETERMINISM
{
  const a = new Uint8ClampedArray(F.CW * F.CH * 4), b = new Uint8ClampedArray(F.CW * F.CH * 4);
  let byteMism = 0, hashMism = 0, n = 0;
  for (let f = 0; f < F.N; f += 53) {
    F.renderFrame(f, 0, false, a); const h1 = F.fnv1a32Bytes(a, a.length);
    F.renderFrame(f, 0, false, b); const h2 = F.fnv1a32Bytes(b, b.length);
    if (h1 !== h2) hashMism++;
    for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) { byteMism++; break; }
    n++;
  }
  check('(1) DETERMINISM  render twice -> byte-identical + hash-equal', byteMism === 0 && hashMism === 0,
    `${n} frames sampled, byteMism=${byteMism} hashMism=${hashMism}`);
}

// (2) SUBSTRATE != PASSTHROUGH (all 1200 frames, not a sample)
{
  const a = new Uint8ClampedArray(F.CW * F.CH * 4), b = new Uint8ClampedArray(F.CW * F.CH * 4);
  let sum = 0, min = 1e9, idMax = 0;
  for (let f = 0; f < F.N; f++) {
    F.renderFrame(f, 1, false, a);            // raw passthrough
    F.renderFrame(f, 0, false, b);            // field render
    const d = F.meanAbsDiff(a, b); sum += d; if (d < min) min = d;
    F.renderFrame(f, 0, true, b);             // identity-mode field
    const id = F.meanAbsDiff(a, b); if (id > idMax) idMax = id;
  }
  const mean = sum / F.N;
  check('(2a) SUBSTRATE  mean|raw-field| > 8 (transform is real, all frames)', mean > 8,
    `mean=${mean.toFixed(2)} min=${min.toFixed(2)} over ${F.N} frames`);
  check('(2b) IDENTITY   field-with-identity == raw exactly', idMax === 0, `max diff=${idMax}`);
}

// (3) PERF
{
  const a = new Uint8ClampedArray(F.CW * F.CH * 4);
  const times = [];
  for (let f = 0; f < F.N; f++) {
    const t0 = performance.now();
    F.renderFrame(f, 0, false, a);
    times.push(performance.now() - t0);
  }
  times.sort((x, y) => x - y);
  const med = times[times.length >> 1], p95 = times[(times.length * 0.95) | 0];
  check('(3) PERF  median <= 8ms/frame on the 1200-frame segment', med <= 8,
    `median=${med.toFixed(2)}ms p95=${p95.toFixed(2)}ms max=${times[times.length - 1].toFixed(2)}ms (Node JIT; browser pending)`);
}

// (4) LEDGER append-only under pause/seek — driven through the REAL key handlers
{
  const key = code => handlers.keydown.forEach(fn => fn({ code, preventDefault() {} }));
  const pump = (steps, msEach = 1000 / 60) => {
    let t = APP.time();                      // sync the virtual clock with the page's lastT
    for (let i = 0; i < steps; i++) {
      const cbs = rAFQ.splice(0);
      t += msEach;
      for (const cb of cbs) cb(t);
    }
  };
  const L0 = LEDGER.length;
  pump(600);                                   // ~10s virtual time playing at 30fps -> ~300 draws
  const played = LEDGER.length - L0;
  check('(4a) PLAY  rAF playback appends one row per drawn frame', played >= 280 && played <= 320,
    `rows appended=${played} over 600 rAF ticks (30fps pacing)`);
  const idsOk = LEDGER.every((r, i) => r.n === i);
  check('(4b) APPEND-ONLY  row ids contiguous 1..N (never spliced/reset)', idsOk, `total=${LEDGER.length}`);

  key('Space');                                // pause
  const Lp = LEDGER.length;
  pump(40);
  check('(4c) PAUSE  no appends while paused', LEDGER.length === Lp,
    `before=${Lp} after=${LEDGER.length} (delta=${LEDGER.length - Lp})`);

  key('ArrowRight');                           // seek +1s
  const Ls1 = LEDGER.length;
  const why1 = LEDGER[LEDGER.length - 1].why;
  key('ArrowLeft');                            // seek -1s
  const why2 = LEDGER[LEDGER.length - 1].why;
  check('(4d) SEEK  each seek appends exactly one new row', LEDGER.length === Ls1 + 1,
    `+1s row="${why1}" -1s row="${why2}"`);

  key('KeyR');
  key('KeyF');
  check('(4e) RESEED/VIEW  R and F each append', LEDGER.length === Ls1 + 3,
    `rows now=${LEDGER.length}`);

  key('Space');                                // resume
  const Lr = LEDGER.length;
  pump(240);                                   // ~4s playing -> ~120 draws
  const resumed = LEDGER.length - Lr;
  check('(4f) RESUME  playback appends again after pause/seek', resumed >= 110 && resumed <= 130,
    `rows appended=${resumed}`);
  check('(4g) APPEND-ONLY (final)  ids still contiguous', LEDGER.every((r, i) => r.n === i),
    `total rows=${LEDGER.length} head=0x${APP.head().toString(16)}`);
}

// (5) on-page falsifier strip agrees
{
  const t = falsEl.innerHTML;
  const passes = (t.match(/class="ok"/g) || []).length;
  const failsOnPage = (t.match(/class="no"/g) || []).length;
  check('(5) ON-PAGE STRIP  selftest PASS markers, zero FAIL', passes >= 3 && failsOnPage === 0,
    `ok=${passes} no=${failsOnPage}`);
}

console.log(fails === 0 ? '\nALL FALSIFIERS PASS' : `\n${fails} FALSIFIER(S) FAILED`);
process.exit(fails === 0 ? 0 : 1);
