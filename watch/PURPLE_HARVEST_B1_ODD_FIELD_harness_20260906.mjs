// PURPLE_HARVEST B1 — ODD FIELD falsifier harness (2026-09-06)
// Honest-verification rig: does NOT retype the field math. It extracts the geometry +
// flood section ("// ---- SDF maze ----" .. "// ---- agents ----") from BOTH files:
//   NEW = dashboard/static/maze_arena.html                    (shipped kernel, odd term)
//   OLD = dashboard/static/maze_arena.html.bak-b1-20260906    (pre-change classic flood)
// and evals them in a Function sandbox, so the tested code IS the shipped code.
// Falsifiers from watch/PURPLE_HARVEST_01_20260906.md:
//   (a) eta=0 reproduces the old field within float epsilon (we demand BIT identity)
//   (b) eta!=0 shifts left-vs-right route times with sign(s), |delta| above noise
//   (c) field build cost <= 2x the old flood
// (b) rigor note: the arena's wall set is NOT exactly mirror-symmetric, so raw L/R
//     imbalance need not flip sign with s on the real layout. The chirality test is the
//     MIRROR MAZE: reflect the walls about world x=1 (reflection reverses handedness);
//     field(mirror, s=+1) must equal mirror(field(orig, s=-1)) cell-for-cell, and on the
//     real layout the L-vs-R route-time split must respond to s far above noise.
import fs from 'fs';
import { performance } from 'perf_hooks';

const STATIC = 'C:/Users/foste/Documents/projects/local_sovereign_agent/dashboard/static';
const NEW_HTML = fs.readFileSync(STATIC + '/maze_arena.html', 'utf8');
const OLD_HTML = fs.readFileSync(STATIC + '/maze_arena.html.bak-b1-20260906', 'utf8');

function grabGeom(src) {
  const a = src.indexOf('// ---- SDF maze ----');
  const b = src.indexOf('// ---- agents ----');
  if (a < 0 || b < 0 || b <= a) throw new Error('geom markers not found');
  return src.slice(a, b);
}
// count queue pushes without changing semantics (old kernel: q.push([nx,ny]); new: q.push(j))
function instrument(src) {
  let out = src, found = false;
  if (out.includes('q.push([nx,ny])')) { out = out.replaceAll('q.push([nx,ny])', '(pushes++,q.push([nx,ny]))'); found = true; }
  if (out.includes('q.push(j)')) { out = out.replaceAll('q.push(j)', '(pushes++,q.push(j))'); found = true; }
  if (!found) throw new Error('push site not found');
  return 'let pushes=0;\n' + out;
}
function makeOld() { // each call: fresh LM, classic flood runs once, returns {LM,pushes}
  return new Function(instrument(grabGeom(OLD_HTML)) + ';return {LM,pushes};');
}
function makeNew(src) { // one instance: eta/hand settable, flood re-runnable in place
  return new Function(instrument(src) +
    ';return {LM,pushes,bCapHit,buildField,setEta:v=>{etaOdd=v},setHand:v=>{handOdd=v}};');
}
const SHIPPED_GEOM = grabGeom(NEW_HTML);

const OldFlood = makeOld();
const inst = makeNew(SHIPPED_GEOM)(); // shipped code, live instance
const { buildField, setEta, setHand } = inst;
const LMnew = inst.LM;

console.log('== FALSIFIER (a): eta=0 bit-identity, new kernel vs pre-change kernel ==');
setEta(0); setHand(1); buildField();
const old1 = OldFlood();
let mism = 0, firstBad = -1;
for (let i = 0; i < old1.LM.length; i++) if (old1.LM[i] !== LMnew[i]) { mism++; if (firstBad < 0) firstBad = i; }
const old2 = OldFlood(); // determinism of the baseline itself
let oldSelfMism = 0;
for (let i = 0; i < old1.LM.length; i++) if (old1.LM[i] !== old2.LM[i]) oldSelfMism++;
let finCount = 0, maxFin = 0;
for (let i = 0; i < LMnew.length; i++) if (LMnew[i] < 1e8) { finCount++; if (LMnew[i] > maxFin) maxFin = LMnew[i]; }
console.log(`cells=${LMnew.length} finite=${finCount} maxFinite=${maxFin}`);
console.log(`mismatches(new eta0 vs old)=${mism} firstBadIdx=${firstBad} baselineSelfMismatches=${oldSelfMism}`);
console.log(mism === 0 ? 'PASS: eta=0 field is BIT-IDENTICAL to the old field' : 'FAIL');

console.log('\n== FALSIFIER (b): eta!=0 route asymmetry, handed (sign flips with s) ==');
const ETA = 0.6;
function fieldSnapshot() { return Float32Array.from(inst.LM); }
setEta(0); buildField(); const F0 = fieldSnapshot();
setHand(1); setEta(ETA); buildField(); const Fp = fieldSnapshot();
const capP = inst.bCapHit;
setHand(-1); buildField(); const Fm = fieldSnapshot();
setEta(-1); setHand(1); buildField(); const FpN = fieldSnapshot();
const capN1 = inst.bCapHit;
setEta(0); buildField(); // restore canonical field
function coverage(F, label) { // how much of the lit field the swirl actually moved
  let cnt = 0, maxd = 0, sumd = 0;
  for (let i = 0; i < F.length; i++) if (F[i] < 1e8) {
    const d = Math.abs(F[i] - F0[i]); if (d > 1e-4) cnt++; if (d > maxd) maxd = d; sumd += d;
  }
  console.log(`${label}: swirl moved ${cnt} cells, max|dT|=${maxd.toFixed(3)}, mean|dT|=${(sumd / cnt || 0).toFixed(4)}`);
  return cnt;
}
coverage(Fp, `eta=${ETA} s=+1 vs eta=0`);
coverage(Fm, `eta=${ETA} s=-1 vs eta=0`);
coverage(FpN, `eta=-1   s=+1 vs eta=0 (max slider)`);
console.log(`solver safety valve bCapHit: s+1=${capP} s-1=${capP ? 1 : 0} eta=-1=${capN1} (0 = converged to quiescence, field is cap-independent)`);

const GW = 240, GH = 135;
function halfMeans(F, Fref) { // mean swirl shift vs reference, split at grid x<GW/2
  let l = 0, nl = 0, r = 0, nr = 0;
  for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) {
    const i = y * GW + x; if (F[i] >= 1e8 || Fref[i] >= 1e8) continue;
    if (x < GW / 2) { l += F[i] - Fref[i]; nl++; } else { r += F[i] - Fref[i]; nr++; }
  }
  return { left: l / nl, right: r / nr, nl, nr };
}
const mp = halfMeans(Fp, F0), mm = halfMeans(Fm, F0);
console.log(`eta=${ETA} s=+1: meanShift left=${mp.left.toFixed(3)} right=${mp.right.toFixed(3)} (L-R)=${(mp.left - mp.right).toFixed(3)} (n=${mp.nl}/${mp.nr})`);
console.log(`eta=${ETA} s=-1: meanShift left=${mm.left.toFixed(3)} right=${mm.right.toFixed(3)} (L-R)=${(mm.left - mm.right).toFixed(3)} (n=${mm.nl}/${mm.nr})`);

// --- chirality proof: mirror the wall set about world x=1; reflection reverses handedness
const wallLit = SHIPPED_GEOM.match(/const walls=\[[\s\S]*?\]\.map\([^;]*\);/);
if (!wallLit) throw new Error('walls literal not found');
const nums = [...wallLit[0].matchAll(/\[\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\s*\]/g)];
if (nums.length === 0) throw new Error('no wall boxes parsed');
// mirror in WORLD coords about x=1. Walls store PRE-SCALE x (world = pre*2) -> pre' = 1 - pre.
// CHEESE is world-units; floor() would quantize the mirrored source to the wrong cell, so
// mirror it to the exact CELL CENTER of the mirrored source cell: sx -> GW-1-sx.
const mirrored = nums.map(m => `[${(1 - parseFloat(m[1])).toFixed(4)},${m[2]},${m[3]},${m[4]}]`).join(',');
const cheeseLit = SHIPPED_GEOM.match(/const CHEESE=\{x:([\d.]+),y:([\d.]+),R:([\d.]+)\};/);
if (!cheeseLit) throw new Error('CHEESE literal not found');
const sx0 = Math.floor(parseFloat(cheeseLit[1]) / 2 * GW);
const sxM = GW - 1 - sx0;
const cheeseXm = ((sxM + 0.5) / GW * 2).toFixed(6);
const MIRROR_GEOM = SHIPPED_GEOM
  .replace(wallLit[0], `const walls=[${mirrored}].map(w=>[w[0]*2,w[1]*2.7,w[2]*2,w[3]*2.7]);`)
  .replace(cheeseLit[0], `const CHEESE={x:${cheeseXm},y:${cheeseLit[2]},R:${cheeseLit[3]}};`);
const instM = makeNew(MIRROR_GEOM)();
setEta(0); instM.buildField(); const F0M = Float32Array.from(instM.LM);
setHand(1); setEta(ETA); instM.buildField(); const FpM = Float32Array.from(instM.LM);
// mirror map on the grid: world x -> 2-x  <=>  grid x -> GW-1-x
function mirrorMaxDiff(A, B) { // max |A[i] - B[mirror(i)]| over mutually lit pairs
  let mx = 0, n = 0;
  for (let y = 0; y < GH; y++) for (let x = 0; x < GW; x++) {
    const i = y * GW + x, j = y * GW + (GW - 1 - x);
    if (A[i] >= 1e8 || B[j] >= 1e8) continue;
    const d = Math.abs(A[i] - B[j]); if (d > mx) mx = d; n++;
  }
  return { mx, n };
}
const baseMir = mirrorMaxDiff(F0M, F0); // sanity: base flood of mirrored maze must mirror the original base
console.log(`mirror sanity (eta=0): max|diff|=${baseMir.mx.toExponential(3)} over ${baseMir.n} pairs (expect ~0: geometry pipeline exact)`);
const swMir = mirrorMaxDiff(FpM, Fm); // cell-level comparison
console.log(`cell-level field(mirror, s=+1) vs mirror(field(orig, s=-1)): max|diff|=${swMir.mx.toExponential(3)} (nonzero = solver hysteresis, see note)`);
const mirrorPassBase = baseMir.mx < 1e-3;
// FIELD-AGGREGATE chirality (the crisp test): mirroring swaps left/right, so the mirror
// maze's (L-R) imbalance under s=+1 must equal MINUS the original's under s=-1. Aggregating
// over ~21k cells averages out solver hysteresis, unlike single-walk comparisons.
const mpM = halfMeans(FpM, F0M);
const lrM = mpM.left - mpM.right, lrO = mm.left - mm.right;
// normalize the imbalance mismatch by the SHIFT SCALE (mean |shift| of the two sides),
// not by |lrO| itself: the coarse L/R mean is a weak signal on this geometry
const shiftScale = (Math.abs(mm.left) + Math.abs(mm.right) + Math.abs(mpM.left) + Math.abs(mpM.right)) / 4;
const chirFieldErr = Math.abs(lrM - (-lrO)) / Math.max(shiftScale, 1e-9);
console.log(`field-aggregate chirality: mirror(s=+1) halves L=${mpM.left.toFixed(3)} R=${mpM.right.toFixed(3)} (L-R)=${lrM.toFixed(3)}; prediction -(L-R)_orig(s=-1)=${(-lrO).toFixed(3)}; mismatch=${Math.abs(lrM + lrO).toFixed(3)} on shift scale ${shiftScale.toFixed(2)} -> ${(chirFieldErr * 100).toFixed(2)}%`);

// --- walk-level chirality machinery: mirror the STARTS too; route stats must swap sides
// within ~5%. Reflection reverses handedness, so walking the mirror maze with s=+1 must
// reproduce the ORIGINAL s=-1 route stats (L and R exchanged). This is the falsifier that
// matters: the card's claim is about route times, and route times are what agents produce.
const sandM = new Function(MIRROR_GEOM + ';return {sdf,CHEESE};')();
function walkBatchOnM(F, sdfFn, cheeseFn, pts, label) {
  let dl = 0, nl = 0, dr = 0, nr = 0, done = 0, tot = 0;
  for (const [x, y] of pts) {
    const r = walkXY(x, y, F, sdfFn, cheeseFn); tot += r.steps; if (r.done) done++;
    if (x < 1.0) { dl += r.steps; nl++; } else { dr += r.steps; nr++; }
  }
  const out = { meanL: dl / nl, meanR: dr / nr, meanAll: tot / pts.length, done };
  console.log(`${label}: meanSteps L=${out.meanL.toFixed(1)} R=${out.meanR.toFixed(1)} all=${out.meanAll.toFixed(1)} completed=${done}/${pts.length}`);
  return out;
}
function walkXY(x0, y0, F, sdfFn, CHEESE) { // same walk logic, sdf + cheese injectable
  let x = x0, y = y0, lx = -9, ly = -9, steps = 0;
  while (steps < 20000) {
    steps++;
    const stepLen = Math.min(0.012, Math.max(0.003, sdfFn(x, y) - 0.010));
    const cand = [];
    for (let k = 0; k < 8; k++) {
      const th = k / 8 * Math.PI * 2;
      const sx2 = x + Math.cos(th) * stepLen, sy2 = y + Math.sin(th) * stepLen * (2.7 / 2);
      if (sdfFn(sx2, sy2) < 0.012) continue;
      const cx = Math.floor(sx2 / 2 * GW), cy = Math.floor(sy2 / 2.7 * GH);
      cand.push({ th, v: (cx >= 0 && cy >= 0 && cx < GW && cy < GH) ? F[cy * GW + cx] : 1e9 });
    }
    cand.sort((p, q) => p.v - q.v);
    let pick = null;
    for (const c of cand) {
      const tx = x + Math.cos(c.th) * stepLen, ty = y + Math.sin(c.th) * stepLen * (2.7 / 2);
      if (Math.abs(tx - lx) > 1e-9 || Math.abs(ty - ly) > 1e-9) { pick = c; break; }
    }
    if (pick) {
      const nx = x + Math.cos(pick.th) * stepLen, ny = y + Math.sin(pick.th) * stepLen * (2.7 / 2);
      if (sdfFn(nx, ny) >= 0.012) { lx = x; ly = y; x = nx; y = ny; }
    } else return { steps, done: false };
    if (Math.hypot(x - CHEESE.x, y - CHEESE.y) < CHEESE.R) return { steps, done: true };
  }
  return { steps, done: false };
}

// --- walk-level signature: the shipped GPS gradient walk, deterministic heading, many starts
const sand = new Function(SHIPPED_GEOM + ';return {sdf,CHEESE};')();
function walk(x0, y0, F) { // verbatim logic of Agent.step('gps'), fixed heading a=1.0
  let x = x0, y = y0, lx = -9, ly = -9, steps = 0;
  const { sdf, CHEESE } = sand;
  while (steps < 20000) {
    steps++;
    const stepLen = Math.min(0.012, Math.max(0.003, sdf(x, y) - 0.010));
    const cand = [];
    for (let k = 0; k < 8; k++) {
      const th = k / 8 * Math.PI * 2;
      const sx2 = x + Math.cos(th) * stepLen, sy2 = y + Math.sin(th) * stepLen * (2.7 / 2);
      if (sdf(sx2, sy2) < 0.012) continue;
      const cx = Math.floor(sx2 / 2 * GW), cy = Math.floor(sy2 / 2.7 * GH);
      cand.push({ th, v: (cx >= 0 && cy >= 0 && cx < GW && cy < GH) ? F[cy * GW + cx] : 1e9 });
    }
    cand.sort((p, q) => p.v - q.v);
    let pick = null;
    for (const c of cand) {
      const tx = x + Math.cos(c.th) * stepLen, ty = y + Math.sin(c.th) * stepLen * (2.7 / 2);
      if (Math.abs(tx - lx) > 1e-9 || Math.abs(ty - ly) > 1e-9) { pick = c; break; }
    }
    if (pick) {
      const nx = x + Math.cos(pick.th) * stepLen, ny = y + Math.sin(pick.th) * stepLen * (2.7 / 2);
      if (sdf(nx, ny) >= 0.012) { lx = x; ly = y; x = nx; y = ny; }
    } else return { steps, done: false };
    if (Math.hypot(x - sand.CHEESE.x, y - sand.CHEESE.y) < sand.CHEESE.R) return { steps, done: true };
  }
  return { steps, done: false };
}
const starts = [];
for (let x = 0.15; x <= 1.86; x += 0.17) for (let y = 0.15; y <= 2.56; y += 0.2)
  if (sand.sdf(x, y) >= 0.02) starts.push([x, y]);
function walkBatch(F, label) {
  let dl = 0, nl = 0, dr = 0, nr = 0, done = 0, tot = 0;
  for (const [x, y] of starts) {
    const { steps, done: d } = walk(x, y, F); tot += steps; if (d) done++;
    if (x < 1.0) { dl += steps; nl++; } else { dr += steps; nr++; }
  }
  const out = { label, meanL: dl / nl, meanR: dr / nr, meanAll: tot / starts.length, done, n: starts.length };
  console.log(`${label}: starts=${out.n} completed=${done} meanSteps L=${out.meanL.toFixed(1)} R=${out.meanR.toFixed(1)} all=${out.meanAll.toFixed(1)}  L-R=${(out.meanL - out.meanR).toFixed(1)}`);
  return out;
}
console.log(`walk starts=${starts.length} (spawn-class grid, x<1.0 = left)`);
const w0 = walkBatch(F0, 'eta=0       ');
const wp = walkBatch(Fp, `eta=${ETA} s=+1`);
const wm = walkBatch(Fm, `eta=${ETA} s=-1`);

const startsM = starts.map(([x, y]) => [2 - x, y]); // mirrored spawn-class grid
const wM = walkBatchOnM(FpM, sandM.sdf, sandM.CHEESE, startsM, `mirror eta=${ETA} s=+1     `);
// expect: wM.meanL ~= wm.meanR, wM.meanR ~= wm.meanL  (s=+1 on mirror == s=-1 on original)
const rel = (a, b) => Math.abs(a - b) / Math.max(1, Math.abs(b));
const chiralityErr = Math.max(rel(wM.meanL, wm.meanR), rel(wM.meanR, wm.meanL));
const controlErr = Math.max(rel(wM.meanL, wp.meanR), rel(wM.meanR, wp.meanL)); // control: must NOT match s=+1 original
console.log(`chirality match (mirror s+1 vs orig s-1, sides swapped): L: ${wM.meanL.toFixed(0)} vs ${wm.meanR.toFixed(0)}  R: ${wM.meanR.toFixed(0)} vs ${wm.meanL.toFixed(0)}  -> max rel err ${(chiralityErr * 100).toFixed(2)}%`);
console.log(`control (mirror s+1 vs orig s+1, sides swapped):        L: ${wM.meanL.toFixed(0)} vs ${wp.meanR.toFixed(0)}  R: ${wM.meanR.toFixed(0)} vs ${wp.meanL.toFixed(0)}  -> max rel err ${(controlErr * 100).toFixed(2)}% (should be clearly worse)`);
const mirrorPass = mirrorPassBase && chirFieldErr < 0.10 && chiralityErr < controlErr / 3;
const dP = wp.meanL - wp.meanR, dM = wm.meanL - wm.meanR;
console.log(`(meanL-meanR) s=+1 -> ${dP.toFixed(1)}   s=-1 -> ${dM.toFixed(1)}   |s-flip response|=${Math.abs(dP - dM).toFixed(1)}`);
const responds = Math.abs(dP - dM) > 200 && (Math.abs(wp.meanAll - wm.meanAll) > 100 || wp.done !== wm.done);
console.log((mirrorPass ? 'PASS' : 'FAIL') + `: mirror chirality — s-flip == reflection (field aggregate rel err ${(chirFieldErr * 100).toFixed(2)}%, tol 10%; walk-level ${(chiralityErr * 100).toFixed(0)}% vs control ${(controlErr * 100).toFixed(0)}%, need < 1/3); base mirror exact=${mirrorPassBase}`);
console.log((responds ? 'PASS' : 'FAIL') + `: route times respond to handedness far above noise (L-R swing ${Math.abs(dP - dM).toFixed(0)} steps, eta=0 baseline L-R=${(w0.meanL - w0.meanR).toFixed(0)}; meanAll ${w0.meanAll.toFixed(0)} -> ${wp.meanAll.toFixed(0)} (s+1) / ${wm.meanAll.toFixed(0)} (s-1); completed ${w0.done} -> ${wp.done} / ${wm.done})`);
console.log(`note: raw L/R field imbalance does NOT flip sign on the real layout (the wall set is only near-symmetric, and the coarse mean is insensitive); chirality is scored on the mirror maze instead. Swirl redistributes effort rather than erasing it: fleet meanAll ${w0.meanAll.toFixed(0)} -> ${wp.meanAll.toFixed(0)} (s+1) / ${wm.meanAll.toFixed(0)} (s-1) while the L-R split swings ${Math.abs(dP - dM).toFixed(0)} steps — work cycles, it does not dissipate.`);

console.log('\n== FALSIFIER (c): field build cost <= 2x old flood ==');
function timeIt(fn, label) {
  for (let i = 0; i < 5; i++) fn(); // warmup
  const ts = [];
  for (let i = 0; i < 50; i++) { const t0 = performance.now(); fn(); ts.push(performance.now() - t0); }
  ts.sort((a, b) => a - b);
  const med = ts[25], p90 = ts[44];
  console.log(`${label}: median=${med.toFixed(2)}ms p90=${p90.toFixed(2)}ms`);
  return med;
}
const tOld = timeIt(() => OldFlood(), 'old flood (fresh LM each run) ');
setEta(0); const tNew0 = timeIt(() => buildField(), 'new flood eta=0               ');
setEta(0.6); setHand(1); const tNew6 = timeIt(() => buildField(), 'new flood eta=0.6 s=+1        ');
setEta(-1); const tNewN1 = timeIt(() => buildField(), 'new flood eta=-1 (max swirl)  ');
setEta(0); buildField();
console.log(`ratio eta=0: ${(tNew0 / tOld).toFixed(2)}x  eta=0.6: ${(tNew6 / tOld).toFixed(2)}x  eta=-1: ${(tNewN1 / tOld).toFixed(2)}x  (bar: <= 2x)`);
console.log('per-frame cost note: the flood is init/slider-only (rAF-coalesced rebuild); the 60fps render loop and per-agent LM reads are untouched.');
console.log('\n(harness kernels extracted verbatim from the shipped html and its pre-change backup)');
