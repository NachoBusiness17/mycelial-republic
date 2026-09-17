// THE TOY CI — 3 lanes on the fifty-lane shim pattern (scripts/test_mud_fifty.js is the parent pattern).
// Lane A: P4 determinism — same seed + same tape twice => identical event log + identical sha256.
// Lane B: divergence falsifier — flip ONE input => named fork at the exact frame (INPUT_FORK @ t).
// Lane C: P-LEGAL sweep — two tapes from one seed, each individually never hit without a rollable telegraph.
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const GAME = path.join(__dirname, '..', 'dashboard', 'static', 'games', 'toy.html');
const html = fs.readFileSync(GAME, 'utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) { console.error('no script block found'); process.exit(1); }
const code = m[1];

// ---- DOM shim (fifty-lane pattern) ----
function makeCtx() {
  return new Proxy({}, {
    get(t, k) { if (k === 'canvas') return fakeCanvas; return (...a) => makeCtx(); },
    set() { return true; },
  });
}
const fakeCanvas = {
  width: 0, height: 0, style: {},
  getContext: () => makeCtx(),
  addEventListener: () => {},
  getBoundingClientRect: () => ({ left: 0, top: 0, width: 960, height: 600 }),
};
const shimWindow = { innerWidth: 960, innerHeight: 600, addEventListener: () => {} };
const shimDocument = { getElementById: () => fakeCanvas, createElement: () => ({ width: 0, height: 0, getContext: () => makeCtx() }) };
const shimRaf = () => 0;

let TOY = null;
// one fresh game instance per load — a page load, not a session carry-over (fleet lanes load
// fresh instances to prove same-day loads share the seed)
function loadToy() {
  const w = { innerWidth: 960, innerHeight: 600, addEventListener: () => {} };
  const fn = new Function('window', 'document', 'requestAnimationFrame', code);
  fn(w, shimDocument, shimRaf);
  return w.TOY;
}
try {
  TOY = loadToy();
} catch (e) {
  console.error('COMPILE/RUN ERROR:', e.stack);
  process.exit(1);
}
if (!TOY) { console.error('window.TOY missing'); process.exit(1); }

// ---- lane framework ----
const results = [];
let laneN = 0;
function lane(name, fn) {
  laneN++;
  try { fn(); results.push([laneN, name, true, '']); }
  catch (e) { results.push([laneN, name, false, e.message]); }
}
function assert(c, msg) { if (!c) throw new Error(msg || 'assert failed'); }
function eq(a, b, msg) { if (a !== b) throw new Error(`${msg || 'eq'}: got ${JSON.stringify(a)} want ${JSON.stringify(b)}`); }

// ---- replay driver: seed + static tape -> deep-copied receipt (snapshot before any reuse) ----
function replay(seed, tape, mode) {
  TOY.start(seed);
  for (const row of tape) TOY.tape.push(row);
  if (mode === 'batch') { for (let i = 0; i < 60; i++) TOY.pump(60); }
  else { TOY.pump(3600); }   // 60s at 60fps; pump returns early once the run ends
  return JSON.parse(JSON.stringify(TOY.receipt()));
}
function firstDiff(a, b) {
  const n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i++) {
    const x = JSON.stringify(a[i]), y = JSON.stringify(b[i]);
    if (x !== y) return { i, x: a[i], y: b[i] };
  }
  return null;
}
// P-LEGAL sweep, computed HERE, not trusted from the toy's own counter
function sweepPLegal(events) {
  let bad = 0;
  for (const hit of events.filter(e => e.e === 'hit')) {
    const tel = events.find(p => p.e === 'telegraph' && p.enemy === hit.enemy && Math.abs(p.t + 0.35 - hit.t) <= 0.001);
    if (!tel) bad++;
  }
  return bad;
}

// ---- the frozen input tapes (static, byte-stable; frames at 60fps) ----
// TAPE_A: walk in, eat the windup, roll LATE so you roll THROUGH the bite (stays in arc),
//         turn while the walker stumbles, riposte x2 -> kill inside its recovery.
const TAPE_A = [
  [0, 'ArrowRight', 1], [40, 'ArrowRight', 0],
  [56, 'ShiftLeft', 1], [58, 'ShiftLeft', 0],
  [74, 'ArrowLeft', 1],
  [80, 'Space', 1], [82, 'Space', 0],
  [84, 'ArrowLeft', 0],
  [102, 'Space', 1], [104, 'Space', 0],
];
// TAPE_B: TAPE_A with ONE entry flipped — the roll press becomes a swing press (no roll).
const TAPE_B = TAPE_A.map(r => (r[0] === 56 && r[1] === 'ShiftLeft' && r[2] === 1) ? [56, 'Space', 1] : r);
// TAPE_C: same seed, different play — facetank and trade, no roll ever.
const TAPE_C = [
  [0, 'ArrowRight', 1], [40, 'ArrowRight', 0],
  [70, 'Space', 1], [72, 'Space', 0], [92, 'Space', 1], [94, 'Space', 0],
  [114, 'Space', 1], [116, 'Space', 0], [136, 'Space', 1], [138, 'Space', 0],
  [158, 'Space', 1], [160, 'Space', 0], [180, 'Space', 1], [182, 'Space', 0],
  [202, 'Space', 1], [204, 'Space', 0], [224, 'Space', 1], [226, 'Space', 0],
  [246, 'Space', 1], [248, 'Space', 0], [268, 'Space', 1], [270, 'Space', 0],
  [290, 'Space', 1], [292, 'Space', 0], [312, 'Space', 1], [314, 'Space', 0],
];
const SEED = 20260916;

// ================= LANE A: determinism (P4) =================
lane('A: toy compiles + window.TOY live + sha256 matches node:crypto', () => {
  eq(typeof TOY.start, 'function');
  eq(TOY.sha256('mag-toy-v1'), crypto.createHash('sha256').update('mag-toy-v1').digest('hex'), 'sha256(impl) vs node:crypto');
});

const ra1 = replay(SEED, TAPE_A, 'single');
const ra2 = replay(SEED, TAPE_A, 'single');
lane('A: same seed + same tape twice -> identical event log (byte-identical JSON)', () => {
  eq(JSON.stringify(ra1.events), JSON.stringify(ra2.events), 'event logs differ');
});
lane('A: same seed + same tape twice -> identical receipt sha256', () => {
  eq(ra1.sha256, ra2.sha256, 'sha differs across replays');
});
lane('A: receipt sha256 is the hash of its own canonical body', () => {
  const canon = JSON.stringify(Object.fromEntries(Object.entries(ra1).filter(([k]) => k !== 'sha256')));
  eq(ra1.sha256, crypto.createHash('sha256').update(canon).digest('hex'), 'receipt sha is not sha256(canonical)');
});
lane('A: batching-invariant — pump(3600) x1 == pump(60) x60 -> same sha', () => {
  const rb = replay(SEED, TAPE_A, 'batch');
  eq(rb.sha256, ra1.sha256, 'step batching changed the run');
});
lane('A: the verb actually fired (telegraph -> roll -> hit_dodged -> kill) and first telegraph < 3s', () => {
  const kinds = ra1.events.map(e => e.e);
  assert(kinds.includes('telegraph'), 'no telegraph');
  assert(kinds.includes('roll'), 'no roll');
  assert(kinds.includes('hit_dodged'), 'no dodge through the bite');
  assert(kinds.includes('kill'), 'no kill');
  const tel = ra1.events.find(e => e.e === 'telegraph');
  assert(tel.t < 3.0, `first telegraph at ${tel.t}s (gate: < 3s)`);
  eq(ra1.verdict, 'win', 'verdict');
  eq(ra1.hits_no_telegraph, 0, 'hits_no_telegraph');
  eq(ra1.hits_taken, 0, 'the perfect tape took damage');
});

// ================= LANE B: divergence falsifier (flip ONE input) =================
const rb1 = replay(SEED, TAPE_B, 'single');
lane('B: flipped input -> receipts diverge (sha differs, tape is load-bearing)', () => {
  assert(rb1.sha256 !== ra1.sha256, 'one flipped input changed nothing — tape is decoration');
});
lane('B: fork is named at the exact frame — first differing event is the flipped input', () => {
  const d = firstDiff(ra1.events, rb1.events);
  assert(d, 'event logs identical despite sha diff (impossible)');
  const forkFrame = TAPE_A[2][0], forkT = +(forkFrame / 60).toFixed(3);   // the flipped entry lives at TAPE_A[2]
  assert(d.x.e === 'input' && d.x.t === forkT, `fork at unexpected event ${JSON.stringify(d.x)}`);
  assert(d.x.code === 'ShiftLeft' && d.y.code === 'Space' && d.x.t === d.y.t,
    `flip mismatch ${JSON.stringify(d.x)} vs ${JSON.stringify(d.y)}`);
  console.log(`    INPUT_FORK @ t=${d.x.t} (frame ${forkFrame}): ShiftLeft press -> Space press`);
});
lane('B: the verb fork — at the telegraph end, TAPE_A dodged the bite and TAPE_B ate it', () => {
  const tel = ra1.events.find(e => e.e === 'telegraph');
  const biteT = +(tel.t + 0.35).toFixed(3);
  const xa = ra1.events.find(e => e.t === biteT && (e.e === 'hit' || e.e === 'hit_dodged'));
  const xb = rb1.events.find(e => e.t === biteT && (e.e === 'hit' || e.e === 'hit_dodged'));
  assert(xa && xb, 'no bite event pair at the telegraph end');
  eq(xa.e, 'hit_dodged', 'TAPE_A bite outcome');
  eq(xb.e, 'hit', 'TAPE_B bite outcome');
  eq(xa.t, xb.t, 'fork pair at different times');
  console.log(`    VERB_FORK @ t=${xa.t}: rolled through the bite (hit_dodged) vs ate it (hit, -${xb.dmg} hp)`);
  assert(rb1.hits_taken >= 1, 'unrolled tape took no damage');
  assert(rb1.hits_no_telegraph === 0, 'divergent run broke P-LEGAL');
});

// ================= LANE C: P-LEGAL sweep (two tapes, one seed) =================
const rc = replay(SEED, TAPE_C, 'single');
lane('C: P-LEGAL sweep on TAPE_A — harness recomputes: no hit without a rollable telegraph', () => {
  eq(sweepPLegal(ra1.events), 0, 'TAPE_A sweep found an illegal hit');
});
lane('C: P-LEGAL sweep on TAPE_C (facetank tape, same seed) — still no hit without a telegraph', () => {
  assert(rc.events.some(e => e.e === 'hit'), 'facetank tape never got hit — sweep is vacuous');
  eq(sweepPLegal(rc.events), 0, 'TAPE_C sweep found an illegal hit');
  eq(rc.hits_no_telegraph, 0, 'toy counter disagrees with the harness sweep');
});
lane('C: divergence is legal play — same seed, different tape, different log, both P-LEGAL', () => {
  assert(JSON.stringify(ra1.events) !== JSON.stringify(rc.events), 'same seed alone decided the run — tape not load-bearing');
  assert(ra1.sha256 !== rc.sha256, 'receipts identical across tapes');
});

// ================= FLEET SEED LAW (W1A): same UTC day -> same starting toy =================
// THE WEAVE build order #58 (the fleet ritual): a fresh load with NO seed derives the run seed
// from the UTC day ("fleet-YYYY-MM-DD" -> FNV-1a 32 -> LCG seed) — same day, same toy, everywhere.
// Explicit seeds always win. The harness re-derives the hash itself — bytes, not reports.
function fleetSeedOfHarness(ds) {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < ds.length; i++) { h ^= ds.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return (h >>> 0) || 1;
}
lane('FLT: default load (no seed) = the fleet seed of the reported UTC day', () => {
  const T2 = loadToy();
  eq(T2.seed0, fleetSeedOfHarness('fleet-' + T2.fleetDate), 'load seed is not fleet-derived');
  eq(T2.fleetSeed, T2.seed0, 'exposed fleetSeed disagrees with the load seed');
});
lane('FLT: two fresh same-day loads share the seed — the fleet ritual', () => {
  const A = loadToy(), B = loadToy();
  eq(A.fleetDate, B.fleetDate, 'UTC day differs across loads');
  eq(A.seed0, B.seed0, 'same-day loads do not share the seed');
});
lane('FLT: explicit seeds always win — start(4242) overrides the fleet seed', () => {
  const T2 = loadToy();
  T2.start(4242);
  eq(T2.seed0, 4242, 'explicit seed lost');
  assert(4242 !== fleetSeedOfHarness('fleet-' + T2.fleetDate), 'control broken: 4242 equals today fleet seed');
});

// ================= report =================
const fails = results.filter(r => !r[2]);
for (const [n, name, ok, err] of results) {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${String(n).padStart(2)} ${name}${ok ? '' : '  — ' + err}`);
}
console.log(`\n${results.length - fails.length}/${results.length} lanes green${fails.length ? `, ${fails.length} RED` : ''}`);
console.log(`toy: ${html.split('\n').length} lines, seed ${SEED}, tape A sha ${ra1.sha256.slice(0, 16)}…, verdict ${ra1.verdict}, duration ${ra1.duration_s}s`);
process.exit(fails.length ? 1 : 0);
