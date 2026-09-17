// MUD replay CI (FX4, gen-2) — the replay-law falsifiers for dashboard/static/games/mud.html.
// Pattern: scripts/test_toy.js (toy = reference impl); DOM shim from scripts/test_mud_fifty.js.
//   FALSIFIER 1: same seed + same input tape, run twice -> byte-identical event log (evlog)
//                AND byte-identical per-step state trace (sha256 of canonical snapshot, 60fps).
//   FALSIFIER 2: flip ONE tape entry -> named fork at the exact step (INPUT_FORK @ step/t) with
//                the input pair and the first differing state path + first differing event.
//   Guard lanes: seed sensitivity (different seed -> different run) + stream law (lcg reset/advance).
// RNG law under test: seeded LCG (toy.html constants: 1664525 / 1013904223), startGame(forcedSeed)
// auto-seeds + records runSeed and resets the actors (toy start() law); cosmetic draws (particles,
// shake, names, ghost ph) stay on Math.random and are excluded from log/snapshot — they cannot
// change game state (FX4 receipt). Each replay loads a FRESH game instance = page-reload semantics
// (lore persists per machine, and a fresh page starts with the shim's empty lore).
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const GAME = path.join(__dirname, '..', 'dashboard', 'static', 'games', 'mud.html');
const html = fs.readFileSync(GAME, 'utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) { console.error('no script block found'); process.exit(1); }
const code = m[1];

// ---- DOM shim (fifty-lane pattern) ----
function makeCtx() {
  return new Proxy({}, {
    get(t, k) {
      if (k === 'canvas') return fakeCanvas;
      return (...a) => makeCtx();
    },
    set() { return true; },
  });
}
const fakeCanvas = {
  width: 0, height: 0, style: {},
  getContext: () => makeCtx(),
  addEventListener: () => {},
  getBoundingClientRect: () => ({ left: 0, top: 0, width: 960, height: 600 }),
};
const shimDocument = {
  getElementById: () => fakeCanvas,
  createElement: () => ({ width: 0, height: 0, getContext: () => makeCtx() }),
};
const shimStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
const shimFetch = () => Promise.resolve({ json: () => Promise.resolve({ ok: true, others: [] }) });
const shimRaf = () => 0;

// one fresh game instance per replay — a page load, not a session carry-over
function loadGame() {
  const shimWindow = {
    innerWidth: 960, innerHeight: 600,
    addEventListener: () => {},
    AudioContext: undefined, webkitAudioContext: undefined,
  };
  const fn = new Function('window', 'document', 'localStorage', 'location', 'fetch', 'setInterval', 'requestAnimationFrame', 'performance', 'URLSearchParams', code);
  fn(shimWindow, shimDocument, shimStorage, { search: '' }, shimFetch, () => 0, shimRaf, performance, URLSearchParams);
  return shimWindow.MUD;
}

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

const DT = 1 / 60;
const SEED = 20260916;
const STEPS = 1800;   // 30s at 60fps

// ---- the frozen input tapes (static, byte-stable; entries are [step, code, down] at 60fps) ----
// TAPE_A: courtyard walk east then north through d1 (crosses the d1 spike line), into the
// refectory; swing volleys at the drip horde, one shout (KeyF), one dodge roll (ShiftLeft); late
// KeyR pokes are dead keys while alive but respawn the run if death happened — every path stays
// deterministic. Facetanks the drip pack on purpose: hurts/death/respawn belong in the log.
const TAPE_A = [
  [0, 'KeyD', 1], [40, 'KeyD', 0],
  [40, 'KeyW', 1], [150, 'KeyW', 0],
  [160, 'Space', 1], [162, 'Space', 0],
  [200, 'Space', 1], [202, 'Space', 0],
  [240, 'Space', 1], [242, 'Space', 0],
  [300, 'KeyF', 1], [302, 'KeyF', 0],
  [360, 'Space', 1], [362, 'Space', 0],
  [420, 'ShiftLeft', 1], [422, 'ShiftLeft', 0],
  [500, 'Space', 1], [502, 'Space', 0],
  [600, 'Space', 1], [602, 'Space', 0],
  [700, 'Space', 1], [702, 'Space', 0],
  [800, 'Space', 1], [802, 'Space', 0],
  [900, 'Space', 1], [902, 'Space', 0],
  [1000, 'Space', 1], [1002, 'Space', 0],
  [1100, 'Space', 1], [1102, 'Space', 0],
  [1200, 'KeyR', 1], [1202, 'KeyR', 0],
  [1200, 'Space', 1], [1202, 'Space', 0],
  [1300, 'Space', 1], [1302, 'Space', 0],
  [1400, 'Space', 1], [1402, 'Space', 0],
  [1500, 'KeyR', 1], [1502, 'KeyR', 0],
  [1500, 'Space', 1], [1502, 'Space', 0],
  [1600, 'Space', 1], [1602, 'Space', 0],
  [1700, 'Space', 1], [1702, 'Space', 0],
];
// TAPE_B: TAPE_A with ONE entry flipped — the swing press at step 160 becomes a sidestep (KeyA,
// never released: constant westward drift for the rest of the run).
const TAPE_B = TAPE_A.map(r => (r[0] === 160 && r[1] === 'Space' && r[2] === 1) ? [160, 'KeyA', 1] : r);
const FORK_STEP = 160;
const SEED_ALT = 987654321;

// ---- replay driver: fresh instance + seed + tape -> per-step digests (+ snapshots for forensics) ----
function replay(seed, tape, keepSnaps) {
  const G2 = loadGame();
  G2.startGame(seed);
  const t = tape.slice().sort((a, b) => a[0] - b[0]);
  let ti = 0;
  const trace = [], snaps = [];
  for (let s = 0; s < STEPS; s++) {
    while (ti < t.length && t[ti][0] === s) {
      const [, cKey, down] = t[ti++];
      if (down) { if (!G2.keys[cKey]) G2.keys[cKey + '_p'] = true; G2.keys[cKey] = true; }
      else G2.keys[cKey] = false;
    }
    G2.pump(1, DT);
    const sn = snap(G2);
    if (keepSnaps) snaps.push(sn);
    trace.push(crypto.createHash('sha256').update(sn).digest('hex'));
  }
  return { trace, snaps, evlog: JSON.parse(JSON.stringify(G2.evlog)), runSeed: G2.runSeed, lcg: G2.lcg, M: G2 };
}

// canonical mechanical-state snapshot — the whitelisted, replay-relevant game state.
// EXCLUDED on purpose (cosmetic, Math.random-fed, cannot change game state): particles,
// damage numbers, loot beams, chronicle text, enemy names, ghost render phase (ph), G.msg text,
// G.shoutTxt (kabuki flavor), relay identity. Everything gameplay reads is IN.
function snap(M) {
  const g = M.G, p = M.player;
  return JSON.stringify({
    g: [g.time, g.state, g.curRoom, g.deaths, g.ng, g.super, g.shoutCd, g.hitStop, g.msgT, g.naveEverActive ? 1 : 0, g.rewindOffer ? 1 : 0,
      g.boonDraft ? g.boonDraft.map(b => b.id) : null, g.cam.x, g.cam.y],
    sig: M.SIGILS.count,
    p: [p.x, p.y, p.hp, p.maxHp, p.stamina, p.maxStamina, p.xp, p.xpNext, p.level, p.souls, p.weaponIdx,
      p.weapons.map(w => [w.name, w.dmg, w.speed, w.rarity]), p.facing, p.iframes, p.rollT, p.rollCd,
      p.attackT, p.attackCd, p.snared, p.statPoints, p.might, p.vigor, p.swiftness, p.bonusSpeed,
      p.lifeOnKill, p._riposte, p.hasLostSouls ? p.soulsLost : 0, p.respawnX, p.respawnY,
      p.boons ? Object.keys(p.boons).sort().join(',') : ''],
    e: M.enemies.map(e => [e.type, e.room, e.x, e.y, e.vx, e.vy, e.hp, e.maxHp, e.speed, e.dmg,
      e.aggro ? 1 : 0, e.windup || 0, e.telegraph || 0, e.stun || 0, e.snare || 0, e.rout || 0,
      e.mourn == null ? -1 : e.mourn, e.attackCd, e.dodgeCd, e.stealth ? 1 : 0, e.hitsSurvived || 0,
      e.grudged ? 1 : 0, e.homeSeed, e.isBoss ? 1 : 0, e.isChampion ? 1 : 0, e.runner ? 1 : 0,
      e.phase2 ? 1 : 0, e.pattern, e.patternT, e._sumT == null ? -1 : e._sumT, e.engaged ? 1 : 0]),
    pr: M.projectiles.map(q => [q.x, q.y, q.vx, q.vy, q.dmg, q.life, q.trap ? 1 : 0]),
    so: M.soulOrbs.map(q => [q.x, q.y, q.vx, q.vy, q.value, q.life]),
    su: M.superOrbs.map(q => [q.x, q.y, q.vx || 0, q.vy || 0, q.life]),
    lo: M.lootDrops.map(l => [l.x, l.y, l.w.name, l.w.dmg, l.w.speed, l.w.rarity]),
    mi: M.mines.map(q => [q.x, q.y, q.arm, q.life]),
    fz: M.fireZones.map(f => [f.x, f.y, f.tel, f.life]),
    dc: M.deathClouds.map(c => [c.x, c.y, c.r, c.life]),
    al: M.allies.map(a => [a.x, a.y, a.t]),   // ph excluded — render alpha only
    co: M.corpses.map(c => [c.x, c.y, c.r]),
    tr: M.trail.map(q => [q.x, q.y, q.a]),
    rs: Object.keys(M.ROOM_STATE).sort().map(k => { const s = M.ROOM_STATE[k];
      return [k, s.activated ? 1 : 0, s.cleared ? 1 : 0, s.idx || 0, s.spawned || 0, s.champOut ? 1 : 0, s.prepop ? 1 : 0, s.t || 0]; }),
    dr: Object.keys(M.DOORS).sort().map(k => [k, M.DOORS[k].locked ? 1 : 0]),
    pz: [M.puzzle.key ? [M.puzzle.key.x, M.puzzle.key.y] : null, M.puzzle.chest ? [M.puzzle.chest.x, M.puzzle.chest.y] : null,
      M.puzzle.plates.map(pl => (pl.on ? 1 : 0)), M.puzzle.gateOpen ? 1 : 0, M.puzzle.chimeT],
    bt: M.BEARTRAPS.map(b => [b.armed ? 1 : 0, b.rearm || 0]),
    da: M.DARTS.map(d => d.cd || 0),
    sk: M.SPIKES.map(s => [s.phase || 0, s.up ? 1 : 0]),
    ve: M.VENTS.map(v => [v.hot ? 1 : 0, v.warn ? 1 : 0]),
    ch: M.CHANDS.map(c => (c.dropped ? 1 : 0)),
    lr: [M.lore.kite || 0, M.lore.swarm || 0, M.lore.traps ? 1 : 0, M.lore.pack ? 1 : 0, M.lore.brawler || 0,
      M.lore.rolls || 0, M.lore.fires || 0, M.lore.wall ? 1 : 0, M.lore.wait ? 1 : 0],
  });
}

// first differing JSON path between two snapshot strings (for naming the fork)
function firstPath(a, b) {
  const ja = JSON.parse(a), jb = JSON.parse(b);
  const walk = (x, y, pth) => {
    if (x === y) return null;
    if (Array.isArray(x) && Array.isArray(y)) {
      const n = Math.max(x.length, y.length);
      for (let i = 0; i < n; i++) {
        if (i >= x.length) return { path: `${pth}[+]`, a: undefined, b: y[i] };
        if (i >= y.length) return { path: `${pth}[-]`, a: x[i], b: undefined };
        const d = walk(x[i], y[i], `${pth}[${i}]`);
        if (d) return d;
      }
      return null;
    }
    if (x && y && typeof x === 'object' && typeof y === 'object') {
      for (const k of Object.keys(x)) { const d = walk(x[k], y[k], `${pth}.${k}`); if (d) return d; }
      return null;
    }
    return { path: pth, a: x, b: y };
  };
  return walk(ja, jb, '$');
}
function firstDiffIndex(a, b) {
  const n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i++) if (a[i] !== b[i]) return i;
  return -1;
}
function firstDiffEvent(a, b) {
  const n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i++) {
    if (JSON.stringify(a[i]) !== JSON.stringify(b[i])) return { i, x: a[i], y: b[i] };
  }
  return null;
}

// ================= LANE 1: compiles, seeds, stream law =================
lane('R: game compiles + window.MUD live + startGame(forcedSeed) records runSeed', () => {
  const M = loadGame();
  M.startGame(SEED);
  eq(M.runSeed, SEED, 'runSeed not recorded');
  M.startGame(SEED);
  eq(M.runSeed, SEED, 're-seed lost');
});
lane('R: stream law — post-seed LCG state is a function of the seed alone', () => {
  const M = loadGame();
  M.startGame(SEED);
  const l1 = M.lcg;
  M.startGame(SEED);
  eq(M.lcg, l1, 'same seed, different stream state after start (puzzle draws not deterministic)');
  M.startGame(SEED === 20260916 ? 20260917 : SEED);   // different seed -> different post-start state
  assert(M.lcg !== l1, 'different seed produced identical post-start stream state');
});
lane('R: stream law — the LCG advances during play and reseeds on startGame', () => {
  const M = loadGame();
  M.startGame(SEED);
  const l0 = M.lcg;
  M.pump(10, DT);
  assert(M.lcg !== l0, 'lcg never advanced — the stream would be frozen');
  M.startGame(SEED);
  eq(M.lcg, l0, 're-seed did not restore the stream');
});

// ================= FALSIFIER 1: same seed + same tape twice =================
const rA1 = replay(SEED, TAPE_A, true);
const rA2 = replay(SEED, TAPE_A, false);
lane('F1: same seed + same tape twice -> byte-identical event log (evlog)', () => {
  eq(JSON.stringify(rA1.evlog), JSON.stringify(rA2.evlog), 'event logs differ');
});
lane('F1: same seed + same tape twice -> byte-identical state trace (all ' + STEPS + ' step digests)', () => {
  eq(JSON.stringify(rA1.trace), JSON.stringify(rA2.trace), 'state traces differ');
});
lane('F1: the run actually lived — event log is non-vacuous (activation + combat/hazard events)', () => {
  const kinds = new Set(rA1.evlog.map(ev => ev.e));
  assert(rA1.evlog.length >= 5, `event log too thin: ${rA1.evlog.length} events`);
  assert(kinds.has('room'), 'no room activation logged');
  assert(kinds.has('hurt') || kinds.has('kill') || kinds.has('loot'), 'no combat/hazard events logged');
  console.log(`    evlog: ${rA1.evlog.length} events over ${STEPS} steps (${[...kinds].sort().join(', ')})`);
});

// ================= FALSIFIER 2: flip ONE input -> named fork =================
const rB = replay(SEED, TAPE_B, true);
lane('F2: flipped input -> state trace diverges (the tape is load-bearing)', () => {
  assert(firstDiffIndex(rA1.trace, rB.trace) >= 0, 'one flipped input changed nothing');
});
lane('F2: the fork is NAMED at the exact step of the flipped input', () => {
  const d = firstDiffIndex(rA1.trace, rB.trace);
  eq(d, FORK_STEP, `fork at unexpected step ${d}`);
  const pd = firstPath(rA1.snaps[d], rB.snaps[d]);
  assert(pd, 'first divergent step has no snapshot diff (impossible)');
  console.log(`    INPUT_FORK @ step ${d} (t=${(d * DT).toFixed(3)}s): Space press -> KeyA press`);
  console.log(`    STATE_FORK ${pd.path}: ${JSON.stringify(pd.a)} -> ${JSON.stringify(pd.b)}`);
});
lane('F2: event logs diverge too — first differing event named', () => {
  const fe = firstDiffEvent(rA1.evlog, rB.evlog);
  assert(JSON.stringify(rA1.evlog) !== JSON.stringify(rB.evlog), 'event logs identical despite fork');
  if (fe) console.log(`    EVENT_FORK @ evlog[${fe.i}]: ${JSON.stringify(fe.x)} -> ${JSON.stringify(fe.y)}`);
  else console.log('    EVENT_FORK beyond the run horizon (state fork is positional only) — logs still differ in content');
});
lane('F2: both forked runs keep their recorded seed — inputs never touch the stream seed', () => {
  eq(rA1.runSeed, SEED, 'run A seed mutated');
  eq(rB.runSeed, SEED, 'run B seed mutated');
});

// ================= GUARD: seed sensitivity =================
lane('G: different seed + same tape -> different run (the seeded stream is load-bearing)', () => {
  const rS = replay(SEED_ALT, TAPE_A, false);
  const d = firstDiffIndex(rA1.trace, rS.trace);
  assert(d >= 0, 'seeds did not matter — law not wired in');
  // NOTE: cross-seed evlog EQUALITY is legal (event shapes can coincide); the law lives in state.
  // The evlog still carries the seed + seeded puzzle placement (run event), so logs self-identify.
  const evSame = JSON.stringify(rA1.evlog) === JSON.stringify(rS.evlog);
  const ra = rA1.evlog.find(e => e.e === 'run'), rb = rS.evlog.find(e => e.e === 'run');
  assert(ra && rb && JSON.stringify(ra) !== JSON.stringify(rb), 'run events not seed-stamped');
  console.log(`    first divergence vs alt seed at step ${d}; evlog run stamps differ${evSame ? ' (remaining events coincide — legal)' : ', full logs differ'}`);
});

// ================= BOON-DRAFT LANES (N9): seeded drafts, max law, pick/swap isolation, mine dilation =================
// The draft draws offers through the seeded LCG (mud.html level-up block: `let roll = rng() * total`,
// comment-tagged gameplay), so offers replay under the same seed+tape law as everything else — and the
// snapshot `g` field already carries boonDraft ids, so F1 pins them byte-for-byte. These lanes pin the
// N9 fixes on top: the max-stacks pool law, pick-never-swaps isolation, and mine timing inside the
// SUPERHOT dilation.
const BOON_IDS = ['chain', 'wave', 'torch', 'crit', 'cloud', 'hermes', 'time', 'leech', 'thorns', 'berserk', 'arc', 'dash'];
const BOON_MAX = { torch: 3, hermes: 3, time: 3 };   // the stackables (mud.html BOONS max fields)
function forceDraft(M) { M.player.xp = M.player.xpNext; M.pump(1, DT); return M.boonDraft ? M.boonDraft.map(b => b.id) : null; }

lane('BD: draft offers are seeded — same seed + same level-up presses -> identical offer sequence', () => {
  function offers() {
    const M = loadGame(); M.startGame(SEED); M.player.iframes = 999;
    const seq = [];
    for (let i = 0; i < 6; i++) { const o = forceDraft(M); if (o) seq.push(o); M.pump(1, DT); }
    return seq;
  }
  const a = offers(), b = offers();
  assert(a.length >= 5, `drafts did not open reliably: ${a.length}`);
  eq(JSON.stringify(a), JSON.stringify(b), 'offer sequence is not a function of the seed');
});
lane('BD: offers are legal — known ids only, at most 3 cards, no duplicate within one offer', () => {
  const M = loadGame(); M.startGame(SEED); M.player.iframes = 999;
  for (let i = 0; i < 6; i++) {
    const o = forceDraft(M);
    if (o) {
      assert(o.length >= 1 && o.length <= 3, `offer size out of range: ${o.length}`);
      assert(o.every(id => BOON_IDS.includes(id)), `unknown boon id offered: ${o}`);
      eq(new Set(o).size, o.length, 'duplicate id within one offer');
    }
    M.pump(1, DT);
  }
});
lane('BD: max law — stackables re-offer below max, and a maxed boon leaves the offered pool', () => {
  const M = loadGame(); M.startGame(SEED); M.player.iframes = 999;
  const taken = {};
  let sawRepeat = false, offers = 0;
  for (let lv = 0; lv < 40; lv++) {
    const o = forceDraft(M);
    if (!o) break;   // pool drained — every boon at max stacks
    offers++;
    for (const id of o) assert((taken[id] || 0) < (BOON_MAX[id] || 1), `maxed boon ${id} was offered again`);
    const si = o.findIndex(id => BOON_MAX[id]);          // prefer a stackable to drive stacks up
    const pickIdx = si >= 0 ? si : 0;
    const pickId = o[pickIdx];
    if ((taken[pickId] || 0) >= 1) sawRepeat = true;     // offered again after a prior take
    taken[pickId] = (taken[pickId] || 0) + 1;
    for (const id of Object.keys(taken)) assert(taken[id] <= (BOON_MAX[id] || 1), `${id} passed its max`);
    M.keys['Digit' + (pickIdx + 1) + '_p'] = true; M.pump(1, DT);
    assert(M.boonDraft === null, 'draft did not close on pick');
  }
  assert(offers >= 10, `too few drafts opened: ${offers}`);
  assert(sawRepeat, 'no stackable was ever re-offered below max — restored semantics not live');
  const counts = M.player.boons || {};
  for (const id of Object.keys(counts)) assert(counts[id] <= (BOON_MAX[id] || 1), `${id} past max in player state`);
  eq(forceDraft(M), null, 'a draft still opens after the pool drained — max law dead');
});
lane('BD: picking a boon never swaps the weapon (both digit paths, with a live-swap control)', () => {
  let M = loadGame(); M.startGame(SEED); M.player.iframes = 999; M.player.weaponIdx = 1;
  assert(forceDraft(M), 'no draft opened');
  M.keys['Digit1_p'] = true; M.pump(1, DT);
  eq(M.player.weaponIdx, 1, 'Digit1 pick fell through to weapon swap');
  assert(M.boonDraft === null, 'draft did not close on pick');
  M = loadGame(); M.startGame(SEED); M.player.iframes = 999; M.player.weaponIdx = 0;
  assert(forceDraft(M), 'no draft opened');
  M.keys['Digit2_p'] = true; M.pump(1, DT);
  eq(M.player.weaponIdx, 0, 'Digit2 pick fell through to weapon swap');
  // control: with NO draft open, the same presses DO swap — the guard is not over-strong
  M = loadGame(); M.startGame(SEED); M.player.iframes = 999; M.player.weaponIdx = 1; M.pump(1, DT);
  M.keys['Digit1_p'] = true; M.pump(1, DT);
  eq(M.player.weaponIdx, 0, 'control: plain Digit1 no longer swaps — draft guard is over-strong');
});
lane('BD: mines dilate under SUPERHOT with the rest of the world (idle 0.06x law)', () => {
  function mineRun(withSuper) {
    const M = loadGame(); M.startGame(SEED); M.player.iframes = 999;
    M.mines.push({ x: M.player.x + 600, y: M.player.y + 600, arm: 0.8, life: 14 });   // far: nothing detonates it
    if (withSuper) M.G.super = 4;
    const arm0 = M.mines[0].arm, life0 = M.mines[0].life;
    M.pump(60, DT);   // 1.0s real time, no input -> world still
    return { dArm: arm0 - M.mines[0].arm, dLife: life0 - M.mines[0].life, superLeft: M.G.super, alive: M.mines.length > 0 };
  }
  const off = mineRun(false), on = mineRun(true);
  assert(off.alive, 'control mine vanished (world interference) — lane invalid');
  assert(off.dArm > 0.79, 'control mine did not tick in real time');
  assert(on.alive, 'superhot mine vanished (detonated?) — lane invalid');
  assert(Math.abs(on.dArm - 0.06) < 0.005, `mine laughed at SUPERHOT: ${on.dArm.toFixed(3)}s decay in a 1s idle window (law: 0.06s)`);
  assert(Math.abs(on.dLife - 0.06) < 0.005, `mine life ignored the dilation: ${on.dLife.toFixed(3)}s (law: 0.06s)`);
  assert(Math.abs((4 - on.superLeft) - 1.0) < 1e-3, 'super window did not tick in real time');
  console.log(`    mine under superhot: ${on.dArm.toFixed(3)}s arm decay vs ${off.dArm.toFixed(3)}s control (0.06x law); window ticked ${(4 - on.superLeft).toFixed(3)}s real`);
});

// ================= report =================
const fails = results.filter(r => !r[2]);
for (const [n, name, ok, err] of results) {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${String(n).padStart(2)} ${name}${ok ? '' : '  — ' + err}`);
}
console.log(`\n${results.length - fails.length}/${results.length} lanes green${fails.length ? `, ${fails.length} RED` : ''}`);
console.log(`mud: ${html.split('\n').length} lines, seed ${SEED}, ${STEPS} steps @ 60fps, tape A ${rA1.evlog.length} events, runSeed ${rA1.runSeed}`);
process.exit(fails.length ? 1 : 0);
