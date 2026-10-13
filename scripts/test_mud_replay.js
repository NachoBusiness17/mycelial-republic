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
// ASCENSION LAW (W5 consumer): ascension is part of run identity — startGame(seed, asc) pins the
// StS ladder for replays; winning a run persists mud_asc = ng+1 so the NEXT run starts ascended
// (title screen shows it; spawnEnemy/spawnBoss/spawnCascade scale by deterministic ng-multipliers
// — the seeded draw stream is NOT reshuffled). Same seed+asc replays identical; same seed, asc
// 0 vs 1 -> deterministically harder with identical puzzle placement.
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
// `storage` (optional): a localStorage shim to boot the game with (W5 ascension lanes use a
// recording storage to prove the victory -> mud_asc -> next-boot ladder round-trip).
function loadGame(storage, search) {
  const shimWindow = {
    innerWidth: 960, innerHeight: 600,
    addEventListener: () => {},
    AudioContext: undefined, webkitAudioContext: undefined,
  };
  const fn = new Function('window', 'document', 'localStorage', 'location', 'fetch', 'setInterval', 'requestAnimationFrame', 'performance', 'URLSearchParams', code);
  fn(shimWindow, shimDocument, storage || shimStorage, { search: search || '' }, shimFetch, () => 0, shimRaf, performance, URLSearchParams);
  return shimWindow.MUD;
}
// recording localStorage shim (W5): preseed with { mud_asc: '7' } to simulate a machine that has
// already won runs; _dump() reads back what the game persisted.
function makeStorage(initial) {
  const kv = Object.assign({}, initial || null);
  return {
    getItem: (k) => (k in kv ? kv[k] : null),
    setItem: (k, v) => { kv[k] = String(v); },
    removeItem: (k) => { delete kv[k]; },
    _dump: () => kv,
  };
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

// ---- replay driver: fresh instance + seed (+ optional ascension pin) + tape -> per-step digests ----
// `asc` (optional, W5): passed straight to startGame(seed, asc); undefined keeps the storage-fed
// ladder path (which under the shim is always ascension 0 — exactly a fresh browser profile).
function replay(seed, tape, keepSnaps, asc) {
  const G2 = loadGame();
  G2.startGame(seed, asc);
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
    gh: M.ghosts.map(g => [g.room, g.x, g.y, g.hp, g.maxHp, g.toughness, g.said ? 1 : 0, Math.round(g.cd * 1000), Math.round(g.t * 1000), g.ph, g.statN, g.statV]),   // bones ghosts — ph derives from the dead run's seed, so it IS pinned (no Math.random in the ghost path)
    bn: M.bones.map(b => [b.v, b.seed, b.room, b.x, b.y, b.causeClass || '', b.name, b.stat, b.statV]),   // the bones pool — machine state, pinned like lore (causeClass: the flavored cause is whisper-only, never pinned)
    cg: Object.keys(M.champGhosts || {}).sort().map(k => [k, M.champGhosts[k].n, M.champGhosts[k].grudges.map(r => [r.v, r.by, r.style, r.seed, r.date])]),   // W4: the champions' grudge ledgers — machine state, pinned like lore
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

// ================= LOOT (N12): the inventory loop replays — pickup -> inventory-add -> inventory-use =================
// The Diablo-loop (seeded makeLoot roll -> update-loop walk-over pickup -> lootScore auto-compare
// equip -> Digit swap) had ZERO fleet consumers (R2 orphan #3). This lane drives the whole loop
// through the real gameplay path — the seeded stream rolls rarity/stats, the drop lands at the
// bearer's feet and is taken by the actual walk-over check in update(), the auto-compare equips
// it into the active slot, and a Digit2 press wields the other slot — then pins the loop under
// the replay law: same seed + same inputs -> byte-identical evlog AND byte-identical state trace
// (snap() already carries weapons[] + weaponIdx, so pickup/add/use are all inside the digest).
const LOOT_STEPS = 240;   // 4s at 60fps
function lootReplay(withSwap) {
  const M = loadGame();
  M.startGame(SEED);
  M.player.iframes = 999;   // the tester does not die mid-loop (BD-lane precedent)
  M.player.weapons[0] = { name: 'Nerf Bat', dmg: 1, speed: 1.0, rarity: 0 };   // trash both slots so
  M.player.weapons[1] = { name: 'Nerf Bat', dmg: 1, speed: 1.0, rarity: 0 };   // ANY seeded roll wins the compare
  const walker = M.spawnEnemy('walker', M.player.x + 40, M.player.y, 'courtyard');   // live melee pressure: the loop runs inside a real fight
  const t = [[10, 'KeyD', 1], [19, 'KeyD', 0],       // face east — the walker is dead ahead of the arc
             [20, 'Space', 1], [22, 'Space', 0]];    // swing on the trash weapon BEFORE the drop
  if (withSwap) t.push([100, 'Digit2', 1], [102, 'Digit2', 0]);   // inventory-use AFTER the pickup
  let ti = 0;
  const trace = [];
  for (let s = 0; s < LOOT_STEPS; s++) {
    if (s === 40) M.makeLoot(M.player.x + 8, M.player.y);   // seeded roll, dropped inside pickup radius (r+18)
    while (ti < t.length && t[ti][0] === s) {
      const [, cKey, down] = t[ti++];
      if (down) { if (!M.keys[cKey]) M.keys[cKey + '_p'] = true; M.keys[cKey] = true; }
      else M.keys[cKey] = false;
    }
    M.pump(1, DT);
    trace.push(crypto.createHash('sha256').update(snap(M)).digest('hex'));
  }
  return { trace, evlog: JSON.parse(JSON.stringify(M.evlog)), M, walker, withSwap };
}
const lrA = lootReplay(true), lrB = lootReplay(true), lrNoSwap = lootReplay(false);
lane('LOOT: pickup -> inventory-add -> inventory-use replays byte-identical (the N12 consumer loop)', () => {
  // the loop actually lived, in both runs
  for (const r of [lrA, lrB]) {
    const lootEv = r.evlog.filter(ev => ev.e === 'loot');
    eq(lootEv.length, 1, 'seeded drop did not roll exactly once');
    assert(typeof lootEv[0].r === 'number' && lootEv[0].r >= 0 && lootEv[0].r <= 3, 'loot event carried no table rarity');
    assert(r.M.player.weapons[0].name !== 'Nerf Bat', 'walk-over never equipped the drop (pickup/add dead)');
    assert(r.M.player.weapons[0].dmg > 1, 'auto-compare equipped stats worse than the trash baseline');
    eq(r.M.player.weaponIdx, r.withSwap ? 1 : 0, 'Digit2 never wielded slot 1 (use dead)');
    assert(r.walker.hp < r.walker.maxHp, 'the opening swing never landed — no live combat around the loop');
  }
  eq(lrA.M.player.weapons[0].name, lrB.M.player.weapons[0].name, 'rolled weapon names differ across identical runs');
  // the replay law, on the loot loop
  eq(JSON.stringify(lrA.evlog), JSON.stringify(lrB.evlog), 'event logs differ across identical loot runs');
  eq(JSON.stringify(lrA.trace), JSON.stringify(lrB.trace), 'state traces differ across identical loot runs');
  // the swap is load-bearing: dropping the Digit2 press forks the run at the swap step
  const d = firstDiffIndex(lrA.trace, lrNoSwap.trace);
  assert(d >= 0, 'removing the swap press changed nothing — the use-path is not load-bearing');
  console.log(`    loop: seeded ${RARITY_OF(lrA)} picked up + equipped @ step 41, Digit2 swap @ step 100 (first use-fork @ step ${d}); evlog ${lrA.evlog.length} events x2 byte-identical`);
});
function RARITY_OF(r) {
  const w = r.M.player.weapons[0];
  return ['Common', 'Magic', 'Rare', 'Legendary'][w.rarity] + ' "' + w.name + '" (dmg ' + w.dmg + ')';
}

// ================= STS ASCENSION (W5): the R2 orphan #2 gets its first consumers =================
// The ladder (G.ng, persisted mud_asc) was hand-playable only: raised solely by a KeyR on the
// victory screen, consumed solely by a browser localStorage read that every harness boot nulls.
// Wiring under test: victory -> ascendForNextRun() persists ng+1; boot + title read it back;
// startGame(seed, asc) pins the ladder for replays; spawnEnemy/spawnBoss scale by formula.
const ASC_WALKER = { hp: 40, dmg: 14 };   // canonical spawnEnemy walker base
const ascHp = (ng) => ASC_WALKER.hp * (1 + Math.min(ng, 20) * 0.15 + ng * 0.05);
const ascDmg = (ng) => ASC_WALKER.dmg * (1 + Math.min(ng, 20) * 0.22 + ng * 0.08);

lane('ASC: replay law holds at ascension — same seed + same tape + asc=1 twice -> identical trace + evlog', () => {
  const a = replay(SEED, TAPE_A, false, 1), b = replay(SEED, TAPE_A, false, 1);
  eq(a.runSeed, b.runSeed, 'ascended runs drew different seeds');
  eq(JSON.stringify(a.trace), JSON.stringify(b.trace), 'ascended run not replay-identical (state)');
  eq(JSON.stringify(a.evlog), JSON.stringify(b.evlog), 'ascended run not replay-identical (events)');
  eq(a.evlog.find(e => e.e === 'run').asc, 1, 'run receipt does not stamp ascension');
});

const rAsc1 = replay(SEED, TAPE_A, false, 1);
lane('ASC: ascension 0 vs 1, same seed -> deterministically different AND harder (ladder formula)', () => {
  // rooms spawn on activation, so the lane summons through the REAL spawners (spawnEnemy/spawnBoss)
  function horde(asc) { const M = loadGame(); M.startGame(SEED, asc);
    M.spawnEnemy('walker', 100, 100, 'courtyard'); M.spawnBoss();
    const w = M.enemies.find(e => e.type === 'walker'); const b = M.enemies.find(e => e.isBoss);
    assert(w && b, 'walker/boss did not spawn'); return { hp: w.maxHp, dmg: w.dmg, boss: b.maxHp }; }
  const h0 = horde(0), h1 = horde(1);
  eq(h0.hp, 40, 'asc-0 walker baseline drifted');
  eq(h1.hp, ascHp(1), 'asc-1 walker hp off-formula');
  eq(h1.dmg, ascDmg(1), 'asc-1 walker dmg off-formula');
  eq(h1.boss, 500 * (1 + 0.15 + 0.05), 'asc-1 boss hp off-formula (spawnBoss ignores the ladder)');
  assert(h1.hp > h0.hp && h1.dmg > h0.dmg && h1.boss > h0.boss, 'asc-1 horde not strictly harder');
  const d = firstDiffIndex(rA1.trace, rAsc1.trace);
  assert(d >= 0, 'ascension did not change the replayed run — consumer dead');
  console.log(`    asc 0->1 @ seed ${SEED}: walker hp ${h0.hp} -> ${h1.hp}, dmg ${h0.dmg.toFixed(1)} -> ${h1.dmg.toFixed(1)}; boss hp ${h0.boss} -> ${h1.boss}; first run divergence @ step ${d}`);
});

lane('ASC: ladder math at the cap — G.ng=20 -> walker hp/dmg exactly on the StS-steal formula (R2 falsifier)', () => {
  const M = loadGame(); M.startGame(SEED, 20);
  M.spawnEnemy('walker', 100, 100, 'courtyard');
  const w = M.enemies.find(e => e.type === 'walker');
  eq(w.maxHp, ascHp(20), 'cap hp off-formula');
  eq(w.dmg, ascDmg(20), 'cap dmg off-formula');
  console.log(`    ng=20 (a capped): walker hp ${w.maxHp} (want ${ascHp(20)}), dmg ${w.dmg.toFixed(1)} (want ${ascDmg(20).toFixed(1)})`);
});

lane('ASC: victory consumer — a win persists ng+1; a fresh boot reads it back and spawns ascended', () => {
  const st = makeStorage();
  const M = loadGame(st); M.startGame(SEED, 2);
  M.ascendForNextRun();   // exactly what the victory gate calls
  eq(st.getItem('mud_asc'), '3', 'win did not raise the persisted ladder');
  const M2 = loadGame(st);
  eq(M2.G.ng, 3, 'fresh boot did not read the persisted ladder (title would show nothing)');
  M2.startGame(SEED);   // no asc pin: the storage-fed ladder must drive the run
  M2.spawnEnemy('walker', 100, 100, 'courtyard');
  const w = M2.enemies.find(e => e.type === 'walker');
  eq(w.maxHp, ascHp(3), 'next run did not spawn ascended');
  eq(M2.evlog.find(e => e.e === 'run').asc, 3, 'run receipt missing the ascension stamp');
  console.log(`    win @ asc 2 -> mud_asc=3 -> fresh boot: title G.ng=3, walker hp ${w.maxHp} (want ${ascHp(3)}), run receipt asc=3`);
});

lane('ASC: no double-bump — victory persist then the KeyR nextLoop keeps the ladder at ng+1', () => {
  const st = makeStorage();
  const M = loadGame(st); M.startGame(SEED, 0);
  M.ascendForNextRun();
  M.nextLoop();
  eq(M.G.ng, 1, 'nextLoop did not raise the in-session ladder');
  eq(st.getItem('mud_asc'), '1', 'victory + KeyR double-bumped the persisted ladder');
});

lane('ASC: ascension is a difficulty dial, not a reseed — same seed, asc 0 vs 1 -> identical stream + placement', () => {
  function walker(asc) { const M = loadGame(); M.startGame(SEED, asc);
    M.spawnEnemy('walker', 100, 100, 'courtyard'); return M; }
  const a = walker(0), b = walker(1);
  eq(a.runSeed, b.runSeed, 'ascension touched the stream seed');
  const ra = a.evlog.find(e => e.e === 'run'), rb = b.evlog.find(e => e.e === 'run');
  eq(JSON.stringify(ra.key), JSON.stringify(rb.key), 'ascension moved the seeded puzzle placement');
  eq(JSON.stringify(ra.chest), JSON.stringify(rb.chest), 'ascension moved the seeded chest placement');
  const wa = a.enemies.find(e => e.type === 'walker'), wb = b.enemies.find(e => e.type === 'walker');
  assert(wa.maxHp !== wb.maxHp || wa.dmg !== wb.dmg, 'control failed: ascension changed no stats');
});

lane('ASC: start UI — a persisted ladder is live on the title screen before any run starts', () => {
  const st = makeStorage({ mud_asc: '7' });
  const M = loadGame(st);
  eq(M.G.ng, 7, 'boot never read the ladder — the title screen has nothing to show');
  eq(M.evlog.length, 0, 'boot read polluted the run log');
});

// ================= FLEET SEED LAW (W1A): same UTC day -> same starting world =================
// THE WEAVE build order #58 (the fleet ritual): one date-derived constant seeds the run so every
// fleet member loading mud the same day shares a starting world. Explicit seeds always win.
// The harness re-derives the FNV-1a 32 expectation itself — it never trusts the game's arithmetic.
function fleetSeedOfHarness(ds) {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < ds.length; i++) { h ^= ds.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return (h >>> 0) || 1;
}
lane('FLT: auto run (no seed) derives the seed from the reported UTC day — fleet-YYYY-MM-DD -> LCG seed', () => {
  const M = loadGame();
  M.startGame();
  eq(M.runSeed, fleetSeedOfHarness('fleet-' + M.fleetDate), 'auto run seed is not fleet-derived');
  eq(M.fleetSeed, M.runSeed, 'exposed fleetSeed disagrees with the auto run seed');
});
lane('FLT: two fresh same-day runs share the fleet seed — the shared starting world', () => {
  const A = loadGame(), B = loadGame();
  A.startGame(); B.startGame();
  eq(A.fleetDate, B.fleetDate, 'UTC day differs across loads');
  eq(A.runSeed, B.runSeed, 'same-day auto runs do not share the seed');
});
lane('FLT: explicit seeds always win — startGame(SEED) ignores the fleet seed', () => {
  const M = loadGame();
  M.startGame(SEED);
  eq(M.runSeed, SEED, 'explicit seed was overridden by the fleet seed');
  assert(SEED !== fleetSeedOfHarness('fleet-' + M.fleetDate), 'control broken: harness SEED equals today fleet seed');
});
lane('FLT: derivation is date-bounded — a different day hashes to a different seed', () => {
  const d = loadGame().fleetDate;
  assert(fleetSeedOfHarness('fleet-' + d) !== fleetSeedOfHarness('fleet-1999-01-01'), 'date does not move the seed');
});

// ================= BONES (W2): NetHack bones files — dead runs haunt later runs =================
// On death a bones record (seed, room, spot, cause, name line, hardest stat) is filed to a
// localStorage pool via the game's SAFE_STORE (cap 10, FIFO). A later run entering that room rolls
// the SEEDED stream once (the bones-roll per room activation; forceBones short-circuits the chance
// draw house-style) and may raise the dead run's ghost: it whispers the cause, chills stamina by
// its toughness (the dead run's hardest stat), and CANNOT kill — the ghost path never touches hp.
// The pool is machine state (like lore): two replays with equal pools must be byte-identical
// INCLUDING the ghost fields (gh/bn joined snap()). A Math.random-fed haunting would break that
// byte-identity — F1 here is also the no-bare-Math.random falsifier for the spawn path.
const BONES_POOL = [
  { v: 1, seed: 11, room: 'refectory', x: 220, y: 560, cause: 'a walker', name: 'UR-VABOK', stat: 'might', statV: 3 },
  { v: 1, seed: 33, room: 'crypt',     x: 900, y: 560, cause: 'the dragon', name: 'MELBONEWIND', stat: 'swiftness', statV: 5 },
  { v: 1, seed: 22, room: 'courtyard', x: 300, y: 980, cause: 'a bear trap', name: 'KEL-DOOMLAMP', stat: 'grit', statV: 2 },
];
function bonesStorage() { return makeStorage({ mud_bones: JSON.stringify(BONES_POOL) }); }

lane('BN: die in run A -> run B entering the room meets A\'s ghost (name, cause, toughness carried)', () => {
  const st = makeStorage();
  const A = loadGame(st, '?name=UR-VABOK'); A.startGame(SEED);
  // teleport onto the refectory floor (activation fires on the next tick), strip iframes every step,
  // and let the drip pack kill through the REAL hurtPlayer -> playerDie -> bonesWrite path
  A.player.x = 300; A.player.y = 560;
  let guard = 0;
  while (!A.evlog.some(e => e.e === 'tomb') && guard++ < 3600) {
    A.player.iframes = 0;
    A.pump(1, DT);
  }
  const tomb = A.evlog.find(e => e.e === 'tomb');
  assert(tomb, 'run A never died in 60s of facetanking — no bones filed');
  eq(tomb.room, 'refectory', 'A died outside the refectory');
  const pool = JSON.parse(st.getItem('mud_bones'));
  const rec = pool.find(b => b.room === 'refectory' && b.name === 'UR-VABOK');
  assert(rec, 'bones pool has no UR-VABOK refectory record');
  assert(rec.cause && rec.cause.length > 0, 'bones record carries no cause');
  eq(rec.statV, 1, 'hardest stat fallback wrong (fresh bearer -> grit 1)');
  // run B: a fresh bearer, same machine storage — the room remembers
  const B = loadGame(st); B.startGame(SEED);
  B.forceBones = true;                 // house affordance: skip the chance draw, spawn guaranteed
  B.player.x = 300; B.player.y = 560;
  B.pump(3, DT);
  eq(B.ghosts.length, 1, 'run B room entry did not raise the dead');
  const g = B.ghosts[0];
  eq(g.name, 'UR-VABOK', 'ghost does not wear the dead run\'s name');
  eq(g.cause, rec.cause, 'ghost does not carry the dead run\'s cause');
  eq(g.toughness, 4 + 3 * rec.statV, 'ghost toughness is not the dead run\'s hardest stat');
  // the whisper, on touch
  B.player.iframes = 999;   // hazards off; the ghost touch is not damage — it must still whisper
  let g2 = 0, minSt = B.player.stamina;   // the touch may already have fired during the spawn pumps — anchor the floor here
  while (!B.evlog.some(e => e.e === 'whisper') && g2++ < 600) { B.pump(1, DT); minSt = Math.min(minSt, B.player.stamina); }
  assert(B.evlog.some(e => e.e === 'whisper'), 'the ghost never whispered');
  assert(minSt < 100, 'ghost touch carried no chill (stamina burn dead)');
  console.log('    A died to "' + rec.cause + '" in the refectory; B met ' + g.name + ' (toughness ' + g.toughness + '); whisper: "' + rec.cause + ' took me" — stamina bottomed at ' + minSt.toFixed(1));
});

lane('BN: a ghost cannot kill — touching a 1-hp bearer leaves hp 1, state play, zero death events', () => {
  const M = loadGame(bonesStorage()); M.startGame(SEED);
  M.forceBones = true;
  M.player.x = 300; M.player.y = 560; M.player.iframes = 999;   // hazards off — ONLY the ghost haunts
  M.player.hp = 1;
  M.pump(3, DT);
  eq(M.ghosts.length, 1, 'no ghost to test');
  let guard = 0;
  while (M.ghosts.length && !M.ghosts[0].said && guard++ < 600) M.pump(1, DT);
  assert(M.ghosts.length && M.ghosts[0].said, 'ghost never reached the bearer');
  eq(M.player.hp, 1, 'the ghost touched hp — the dead executed (LAW VIOLATION)');
  eq(M.G.state, 'play', 'the ghost killed the player');
  assert(!M.evlog.some(e => e.e === 'death'), 'a death event fired from a ghost touch');
  assert(M.player.snared > 0, 'touch left no chill at all (flavor-hazard dead)');
  console.log('    ghost (toughness ' + M.ghosts[0].toughness + ') touched a 1-hp bearer: hp ' + M.player.hp + ', state ' + M.G.state + ', snare ' + M.player.snared.toFixed(2) + 's');
});

lane('BN: ghost spawning is seeded — same seed + pool -> identical haunt/no-haunt across 24 seeds x2', () => {
  function roll(seed) {
    const M = loadGame(bonesStorage()); M.startGame(seed);
    M.player.x = 300; M.player.y = 560;
    M.pump(3, DT);
    return { n: M.ghosts.length, g: M.ghosts[0] ? [M.ghosts[0].x, M.ghosts[0].y, M.ghosts[0].toughness] : null };
  }
  let spawned = 0;
  for (let i = 0; i < 24; i++) {
    const seed = 1000 + i * 7919;
    const a = roll(seed), b = roll(seed);
    eq(JSON.stringify(a), JSON.stringify(b), 'same seed + same pool gave different hauntings (spawn not stream-fed)');
    if (a.n) spawned++;
  }
  assert(spawned > 2 && spawned < 22, 'bones-roll not probabilistic: ' + spawned + '/24 hauntings');
  console.log('    24 seeds x2 boots: haunt/no-haunt is a pure function of (seed, pool); hauntings rose ' + spawned + '/24');
});

lane('BN: replay law with bones — same seed + tape + pool twice -> byte-identical trace INCLUDING ghost fields', () => {
  function pooled(force) {
    const M = loadGame(bonesStorage()); M.startGame(SEED);
    M.forceBones = force;
    const t = TAPE_A.slice().sort((a, b) => a[0] - b[0]);
    let ti = 0; const trace = [];
    for (let s = 0; s < STEPS; s++) {
      while (ti < t.length && t[ti][0] === s) {
        const [, k, d2] = t[ti++];
        if (d2) { if (!M.keys[k]) M.keys[k + '_p'] = true; M.keys[k] = true; }
        else M.keys[k] = false;
      }
      M.pump(1, DT);
      trace.push(crypto.createHash('sha256').update(snap(M)).digest('hex'));
    }
    return { trace, evlog: JSON.parse(JSON.stringify(M.evlog)), haunts: M.evlog.filter(e => e.e === 'bones').length };
  }
  const p1 = pooled(true), p2 = pooled(true), p3 = pooled(false), p4 = pooled(false);
  eq(JSON.stringify(p1.trace), JSON.stringify(p2.trace), 'forced-haunt run not byte-identical (ghost state leaked nondeterminism)');
  eq(JSON.stringify(p1.evlog), JSON.stringify(p2.evlog), 'forced-haunt evlogs differ');
  assert(p1.haunts >= 1, 'no haunting ever fired — pool wiring dead');
  eq(JSON.stringify(p3.trace), JSON.stringify(p4.trace), 'bones-roll run not byte-identical');
  console.log('    pooled TAPE_A x2 (forced + natural roll): byte-identical incl gh/bn; hauntings fired ' + p1.haunts + 'x forced, ' + p3.haunts + 'x rolled');
});

lane('BN: bones are room-bound — the crypt dead do not haunt the refectory', () => {
  const st = makeStorage({ mud_bones: JSON.stringify([{ v: 1, seed: 33, room: 'crypt', x: 900, y: 560, cause: 'the dragon', name: 'CRYPT-ONLY', stat: 'grit', statV: 1 }]) });
  const M = loadGame(st); M.startGame(SEED);
  M.forceBones = true;
  M.player.x = 300; M.player.y = 560;   // refectory
  M.pump(3, DT);
  eq(M.ghosts.length, 0, 'a crypt bone rose in the refectory');
});

lane('BN: the courtyard is sanctified — bones are filed there but no ghost rises', () => {
  const M = loadGame(bonesStorage()); M.startGame(SEED);
  M.forceBones = true;
  M.pump(10, DT);   // the bearer loiters where KEL-DOOMLAMP fell
  eq(M.ghosts.length, 0, 'a ghost rose on sanctified ground');
  eq(M.bones.filter(b => b.room === 'courtyard').length, 1, 'the courtyard bone vanished — filing must still happen everywhere');
});

lane('BN: the pool is capped at 10, FIFO — bone #0 rots out first', () => {
  const st = makeStorage();
  const M = loadGame(st); M.startGame(SEED);
  for (let i = 0; i < 12; i++) M.bonesWrite({ v: 1, seed: i, room: 'refectory', x: i, y: i, cause: 'c' + i, name: 'N' + i, stat: 'might', statV: 1 });
  eq(M.bones.length, 10, 'pool cap broken');
  eq(M.bones[0].name, 'N2', 'FIFO dropped the wrong end');
  eq(M.bones[9].name, 'N11', 'FIFO lost the freshest bone');
  eq(JSON.parse(st.getItem('mud_bones')).length, 10, 'persisted pool exceeds the cap');
});

// ================= GHOST PERSONALITIES (W4, THE WEAVE #4): the champions remember =================
// Each ROOMS.*.champion keeps a capped grudge ledger in the SAFE_STORE ('mud_ghosts') — machine
// state like lore/bones: one record per recorded encounter (verdict slain|took, killer name,
// style word, run seed, date). On a rematch the champion (a) opens with a telegraph line picked
// by a pure function of the record from its class lexicon — one line, no free text, no stream
// draws — and (b) shifts its opening stance one seeded step per prior encounter, on top of the
// normal seeded draw. The ledger rides the snapshot (cg) but never feeds the replay stream.
const GHOST_SEED = 20260916;
function ghostStorage(extra) { return makeStorage(Object.assign({}, extra || null)); }

lane('GP: a first encounter is memoryless — no telegraph; a slain champion files a dated grudge', () => {
  const M = loadGame(ghostStorage()); M.grudgeReset(); M.startGame(GHOST_SEED);
  eq(M.grudgeTelegraph('crypt'), null, 'a fresh ghost spoke');
  const ch = M.spawnChampion('crypt');
  assert(ch.opening >= 0, 'no opening stance was drawn for a champion');
  assert(!M.evlog.some(e => e.e === 'telegraph'), 'a memoryless encounter carried a telegraph event');
  ch.hp = 0; M.pump(3, DT);   // the REAL killEnemy -> recordGrudge path
  const g = M.champGhosts.crypt;
  assert(g && g.n === 1 && g.grudges.length === 1, 'slain champion filed no grudge');
  const r = g.grudges[0];
  eq(r.v, 'slain', 'wrong verdict on a champion kill');
  eq(r.by, 'lantern', 'the grudge does not name the killer');
  eq(r.seed, GHOST_SEED, 'the grudge does not stamp the run seed');
  assert(r.style && r.style.length > 0, 'the grudge carries no style word');
  assert(/^\d{4}-\d{2}-\d{2}$/.test(r.date), 'the grudge carries no date');
});

lane('GP: kill the champion twice — the rematch telegraph speaks, and the second differs deterministically', () => {
  function scenario() {
    const M = loadGame(ghostStorage()); M.grudgeReset();
    M.startGame(GHOST_SEED);
    let ch = M.spawnChampion('crypt'); ch.hp = 0; M.pump(3, DT);   // first blood
    M.startGame(GHOST_SEED);                                       // the rematch: same page, same store
    ch = M.spawnChampion('crypt');
    const t1 = M.grudgeTelegraph('crypt'), open1 = ch.opening;
    ch.hp = 0; M.pump(3, DT);                                      // second blood
    M.startGame(GHOST_SEED);
    ch = M.spawnChampion('crypt');
    return { t1, t2: M.grudgeTelegraph('crypt'), open1, open2: ch.opening };
  }
  const a = scenario(), b = scenario();
  assert(a.t1 && a.t2, 'a lived grudge did not speak on the rematch');
  eq(a.t1.n, 1, 'first rematch telegraph did not count one grudge');
  eq(a.t2.n, 2, 'second rematch telegraph did not count two grudges');
  assert(a.t1.line.includes('lantern') && a.t2.line.includes('lantern'), 'the telegraph is not derived from the stored record');
  assert(a.t2.line !== a.t1.line, 'the second encounter\'s telegraph did not differ from the first');
  eq(JSON.stringify(a), JSON.stringify(b), 'same seed + same two-kill history gave different telegraphs/stances');
  console.log('    after kill #1: ' + a.t1.line);
  console.log('    after kill #2: ' + a.t2.line);
});

lane('GP: the opening stance shifts exactly one seeded step per prior encounter', () => {
  function openingAt(n) {
    const M = loadGame(ghostStorage()); M.startGame(GHOST_SEED);
    M.champGhosts.crypt = { n, grudges: [{ v: 'slain', by: 'lantern', style: 'kiting', seed: 5, date: '2026-09-16' }] };
    const ch = M.spawnChampion('crypt');
    const t = M.grudgeTelegraph('crypt');
    return { open: ch.opening, line: t && t.line };
  }
  const o0 = openingAt(0), o1 = openingAt(1), o2 = openingAt(2);
  eq((o1.open - o0.open + 3) % 3, 1, 'one prior encounter did not shift the opening by one seeded step');
  eq((o2.open - o1.open + 3) % 3, 1, 'a second prior encounter did not shift the opening by one seeded step');
  assert(o0.line && o1.line && o2.line, 'a lived grudge did not speak');
});

lane('GP: same seed + same injected history -> byte-identical rematch (telegraph, stance, events)', () => {
  function rematch() {
    const M = loadGame(ghostStorage()); M.startGame(GHOST_SEED);
    M.champGhosts.crypt = { n: 2, grudges: [
      { v: 'slain', by: 'lantern', style: 'kiting', seed: 111, date: '2026-09-15' },
      { v: 'took', by: 'lantern', style: 'brawling', seed: 222, date: '2026-09-16' }] };
    const ch = M.spawnChampion('crypt');
    const t = M.grudgeTelegraph('crypt');
    return { line: t.line, i: t.i, open: ch.opening, ev: JSON.stringify(M.evlog.filter(e => e.e === 'champion' || e.e === 'telegraph')) };
  }
  const a = rematch(), b = rematch();
  eq(JSON.stringify(a), JSON.stringify(b), 'same seed + same history gave a different rematch');
  assert(a.line.includes('lantern'), 'the telegraph dropped the killer name');
  console.log('    crypt rematch (two lived grudges): ' + a.line + ' (lexicon ' + a.i + ', stance ' + a.open + ')');
});

lane('GP: the ledger is capped (5, newest kept); a champion victory files "took" through the real kill path', () => {
  const M = loadGame(ghostStorage()); M.startGame(GHOST_SEED);
  for (let i = 0; i < 8; i++) M.recordGrudge('forge', 'slain');
  eq(M.champGhosts.forge.grudges.length, M.GRUDGE_CAP, 'the ledger exceeded the cap');
  eq(M.champGhosts.forge.n, 8, 'the encounter count lost its history');
  // a champion that puts the lantern down files its own grudge — real hurtPlayer -> playerDie path.
  // The duel is held private: the crypt's escorts are outside this law, and the ghost is held to
  // its body (a rogue champion kites between backstabs — the duel must not become a chase).
  const M2 = loadGame(ghostStorage()); M2.grudgeReset(); M2.startGame(GHOST_SEED);
  const ch = M2.spawnChampion('crypt');
  M2.player.x = ch.x; M2.player.y = ch.y;
  M2.pump(2, DT);   // let the crypt activate and its queue walk in
  let guard = 0;
  while (M2.G.state === 'play' && guard++ < 3600) {
    M2.player.iframes = 0;
    for (const e of M2.enemies) if (e !== ch && e.hp > 0) e.hp = 0;   // escorts are not the duelist
    if (ch.hp > 0) { ch.x = M2.player.x + 30; ch.y = M2.player.y; }   // hold the ghost to its body
    M2.pump(1, DT);
  }
  const g = M2.champGhosts.crypt;
  assert(g && g.grudges.some(r => r.v === 'took'), 'the champion kept no grudge for the lantern it put down');
  console.log('    forge ledger capped at ' + M.champGhosts.forge.grudges.length + '/8 filed; VERAK\'s ledger holds a ' + JSON.stringify(g.grudges[g.grudges.length - 1].v) + ' grudge after ' + guard + ' frames');
});

lane('GP: replay law with lived ghosts — same seed + tape + ledger twice -> byte-identical trace + evlog', () => {
  function run() {
    const M = loadGame(ghostStorage({ mud_ghosts: JSON.stringify({ crypt: { n: 1, grudges: [{ v: 'slain', by: 'lantern', style: 'kiting', seed: 5, date: '2026-09-16' }] } }) }));
    M.startGame(GHOST_SEED);
    const t = TAPE_A.slice().sort((x, y) => x[0] - y[0]);
    let ti = 0; const trace = [];
    for (let s = 0; s < 900; s++) {
      while (ti < t.length && t[ti][0] === s) {
        const [, k, d2] = t[ti++];
        if (d2) { if (!M.keys[k]) M.keys[k + '_p'] = true; M.keys[k] = true; }
        else M.keys[k] = false;
      }
      M.pump(1, DT);
      trace.push(crypto.createHash('sha256').update(snap(M)).digest('hex'));
    }
    return { trace, evlog: JSON.parse(JSON.stringify(M.evlog)) };
  }
  const a = run(), b = run();
  eq(JSON.stringify(a.trace), JSON.stringify(b.trace), 'a lived grudge ledger broke the replay law (state)');
  eq(JSON.stringify(a.evlog), JSON.stringify(b.evlog), 'a lived grudge ledger broke the replay law (events)');
});

const fails = results.filter(r => !r[2]);
for (const [n, name, ok, err] of results) {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${String(n).padStart(2)} ${name}${ok ? '' : '  — ' + err}`);
}
console.log(`\n${results.length - fails.length}/${results.length} lanes green${fails.length ? `, ${fails.length} RED` : ''}`);
console.log(`mud: ${html.split('\n').length} lines, seed ${SEED}, ${STEPS} steps @ 60fps, tape A ${rA1.evlog.length} events, runSeed ${rA1.runSeed}`);
process.exit(fails.length ? 1 : 0);
