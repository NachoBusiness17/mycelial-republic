// Q_038_wallwalkers_probe.js — FW-38 evidence probe: what crosses a sealed door.
// Fifty-harness style: shim the DOM, load dashboard/static/games/mud.html, drive window.MUD.
// Probes (evidence for FW38_wallwalkers.md):
//   1. a SEALED door stops the player's body (resolveWalls includes doorRects)
//   2. a projectile FLIES THROUGH the sealed door (update()'s wall test loops `walls` only)
//   3. an enemy AGGROES through the sealed door (rebuildVision builds visionSegs from `walls` only)
//   4. a plain walker that saw the player is still BLOCKED by the sealed door
//   5. a runner (bell-ringer body) SLIPS the sealed door — the deliberate bell-passage
//   6. no tunneling: max-speed enemy (220 u/s) into a 40px wall for 120 frames never crosses
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..', '..', '..');
const GAME = path.join(ROOT, 'dashboard', 'static', 'games', 'mud.html');
const html = fs.readFileSync(GAME, 'utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) { console.error('no script block found'); process.exit(1); }
const code = m[1];

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
const shimWindow = { innerWidth: 960, innerHeight: 600, addEventListener: () => {}, AudioContext: undefined, webkitAudioContext: undefined };
const shimDocument = { getElementById: () => fakeCanvas, createElement: () => ({ width: 0, height: 0, getContext: () => makeCtx() }) };
const shimStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
const shimFetch = () => Promise.resolve({ json: () => Promise.resolve({ ok: true, others: [] }) });
const shimInterval = () => 0;
const shimRaf = () => 0;

let MUD = null;
try {
  const fn = new Function('window', 'document', 'localStorage', 'location', 'fetch', 'setInterval', 'requestAnimationFrame', 'performance', 'URLSearchParams', code);
  fn(shimWindow, shimDocument, shimStorage, { search: '' }, shimFetch, shimInterval, shimRaf, performance, URLSearchParams);
  MUD = shimWindow.MUD;
} catch (e) { console.error('COMPILE/RUN ERROR:', e.stack); process.exit(1); }
if (!MUD) { console.error('window.MUD missing'); process.exit(1); }

const results = [];
let laneN = 0;
function lane(name, fn) {
  laneN++;
  try { const detail = fn(); results.push([laneN, name, true, '', detail === undefined ? '' : detail]); }
  catch (e) { results.push([laneN, name, false, e.message, '']); }
}
function assert_(c, msg) { if (!c) throw new Error(msg); }

MUD.startGame(20260928, 0);   // fixed seed, ascension 0

// ---- shared facts ----
const D2 = MUD.DOORS.d2;      // refectory's north door: x300-390, y400-440
const inRect = (x, y, w) => x > w.x && x < w.x + w.w && y > w.y && y < w.y + w.h;

lane('0. setup: startGame(seed 20260928) leaves d2 SEALED (after-room uncleared)', () => {
  assert_(D2.locked === true, `d2 should be locked at boot, got ${D2.locked}`);
  assert_(MUD.doorRects.some(w => w.door && w.x === D2.x && w.y === D2.y), 'd2 rect should be in doorRects');
  return `d2 locked=${D2.locked}, doorRects=${MUD.doorRects.length}`;
});

lane('1. player body BLOCKED by sealed d2: walks north into it, never enters the rect', () => {
  MUD.G.state = 'play';
  MUD.player.x = 345; MUD.player.y = 470; MUD.player.hp = 100; MUD.player.iframes = 99;
  MUD.keys['KeyW'] = true;
  for (let i = 0; i < 90; i++) MUD.step(1 / 60);   // 1.5s of pushing north
  MUD.keys['KeyW'] = false;
  assert_(!inRect(MUD.player.x, MUD.player.y, D2), `player crossed the sealed door: player at ${MUD.player.x},${MUD.player.y}`);
  assert_(MUD.player.y > 440, `player ended north of the door line (y=${MUD.player.y.toFixed(1)})`);
  return `player y ends ${MUD.player.y.toFixed(1)} (door north face y=400..440)`;
});

lane('2. projectile FLIES THROUGH the sealed d2 (wall test loops `walls` only)', () => {
  MUD.player.x = 250; MUD.player.y = 470; MUD.player.iframes = 99;   // player west, out of the bolt line
  MUD.projectiles.length = 0;
  MUD.projectiles.push({ x: 345, y: 470, vx: 0, vy: -260, r: 6, dmg: 5, life: 3, color: '#f44' });
  let minY = 470, crossed = false;
  for (let i = 0; i < 240 && MUD.projectiles.length; i++) {
    MUD.step(1 / 60);
    for (const p of MUD.projectiles) { if (p.y < minY) minY = p.y; if (p.y >= 400 && p.y <= 440) crossed = true; }
  }
  assert_(crossed, `projectile never entered the sealed door rect; minY=${minY.toFixed(1)}`);
  assert_(minY < 400, `projectile never got NORTH of the sealed door; minY=${minY.toFixed(1)}`);
  assert_(D2.locked === true, 'door must still be sealed during the crossing');
  return `bolt crossed sealed d2, minY=${minY.toFixed(1)} (north face y=400)`;
});

lane('3. enemy AGGROES through the sealed d2 (vision built from `walls` only)', () => {
  // player south of d2 (refectory), walker north of it (infirmary), 170px apart, only the sealed door between
  MUD.enemies.length = 0;
  MUD.player.x = 345; MUD.player.y = 470; MUD.player.iframes = 99; MUD.player.hp = 100;
  const e = MUD.spawnEnemy('walker', 345, 300, 'infirmary');
  e.aggroR = 260; e.aggro = false;
  let aggroAt = -1;
  for (let i = 0; i < 30; i++) { MUD.step(1 / 60); if (e.aggro) { aggroAt = i; break; } }
  assert_(e.aggro, 'enemy never aggroed — sight WAS blocked (would refute the memo)');
  assert_(D2.locked === true, 'door must be sealed for this lane to mean anything');
  return `aggro at frame ${aggroAt}, sight crossed the sealed door`;
});

lane('4. CONTROL: that same walker is then BLOCKED by the sealed door body', () => {
  const e = MUD.enemies.find(x => x.type === 'walker');
  assert_(!!e, 'walker missing');
  let maxSide = 0;   // closest approach to the door line = the LARGEST y it reaches
  for (let i = 0; i < 240; i++) {   // 4s of chasing
    MUD.step(1 / 60);
    maxSide = Math.max(maxSide, e.y);
    assert_(e.y < 440, `walker entered the sealed door rect: y=${e.y.toFixed(1)}`);
  }
  assert_(D2.locked === true, 'door must stay sealed');
  assert_(maxSide <= 400, `walker got past the door north face: y=${maxSide.toFixed(1)}`);
  return `walker pinned at y=${maxSide.toFixed(1)} = door face (400) - r(14): seal exact`;
});

lane('5. the FEATURE: a routing escort escapes THROUGH the sealed d5 (bell-passage)', () => {
  // Real trigger: champion died -> surviving escorts with hp<60% get rout=3.5 (mud.html killEnemy).
  // Ossuary is north-flush (room y840, band wall y800-840): without the door skip, resolveWalls
  // pins a router at y=854 INSIDE the ossuary forever — roomOf never flips, re-home never fires.
  // Escort made unkillable so a spike/trap kill can't be mistaken for the re-home splice.
  MUD.enemies.length = 0;
  MUD.player.x = 200; MUD.player.y = 1050;   // park the player in the courtyard
  MUD.player.iframes = 99;
  const D5 = MUD.DOORS.d5;                   // ossuary's north door: x940-1030, y800-840, sealed (crypt uncleared)
  assert_(D5.locked === true, 'd5 must be sealed for this lane');
  const chronBefore = MUD.chron.length;
  const rw = MUD.spawnEnemy('walker', 985, 900, 'ossuary');
  rw.rout = 3.5;                             // the exact value killEnemy assigns on champion death
  rw.hp = rw.maxHp = 1e9;                    // unkillable: the ONLY way off the field is the re-home splice
  let crossed = false, gone = -1;
  for (let i = 0; i < 300 && gone < 0; i++) {
    MUD.step(1 / 60);
    if (inRect(rw.x, rw.y, D5)) crossed = true;
    if (!MUD.enemies.includes(rw)) gone = i;
  }
  const fled = MUD.chron.slice(chronBefore).some(c => /fled/.test(c.text));
  assert_(rw.hp > 0, 'escort was killed — lane invalid');
  assert_(crossed, `router never entered the sealed d5 rect (last pos ${rw.x.toFixed(1)},${rw.y.toFixed(1)})`);
  assert_(gone >= 0, 'router never left the field — re-home never fired');
  assert_(fled, 'no "fled — takes them in" chronicle — splice was not the re-home');
  return `router crossed sealed d5, re-homed at frame ${gone} (bell-passage, resolveWalls door skip)`;
});

lane('6. no tunneling: 220 u/s enemy into the 40px wall column, 120 frames, never crosses', () => {
  MUD.enemies.length = 0;
  MUD.player.x = 800; MUD.player.y = 500;   // east of the x660-700 wall (scriptorium side)
  MUD.player.iframes = 99;
  const e = MUD.spawnEnemy('walker', 640, 500, 'crypt');
  e.speed = 220; e.aggro = true;            // the spawn cap (speed <= 220), chasing the player
  let maxX = 0, maxStep = 0, prevX = e.x;
  for (let i = 0; i < 120; i++) {
    MUD.step(1 / 60);
    maxStep = Math.max(maxStep, Math.abs(e.x - prevX)); prevX = e.x;
    maxX = Math.max(maxX, e.x);
    assert_(e.x < 660, `enemy tunneled east of the wall column: x=${e.x.toFixed(1)}`);
  }
  assert_(maxStep <= 275 / 60 + 0.5, `frame step above the cap math: ${maxStep.toFixed(2)}px`);
  return `held at x<=${maxX.toFixed(1)} (wall west face x=660), max step ${maxStep.toFixed(2)}px`;
});

let fails = 0;
for (const [n, name, ok, err, detail] of results) {
  if (!ok) fails++;
  console.log(`PASS ${n}`.padEnd(9) + name + (ok ? (detail ? `  [${detail}]` : '') : `\n         FAIL -> ${err}`));
}
console.log(`${results.length - fails}/${results.length} lanes green`);
process.exit(fails ? 1 : 0);
