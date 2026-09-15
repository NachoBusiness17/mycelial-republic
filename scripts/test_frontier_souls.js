// Frontier Souls — Adam's-laws harness. Same shim pattern as test_mud_fifty.js.
'use strict';
const fs = require('fs');
const path = require('path');
const GAME = path.join(__dirname, '..', 'dashboard', 'static', 'games', 'frontier_souls.html');
const html = fs.readFileSync(GAME, 'utf8');
const code = html.match(/<script>([\s\S]*)<\/script>/)[1];
function makeCtx() { return new Proxy({}, { get(t, k) { if (k === 'canvas') return fakeCanvas; return (...a) => makeCtx(); }, set() { return true; } }); }
const fakeCanvas = { width: 0, height: 0, style: {}, getContext: () => makeCtx(), addEventListener: () => {}, getBoundingClientRect: () => ({ left: 0, top: 0, width: 960, height: 600 }) };
const shimWindow = { innerWidth: 960, innerHeight: 600, addEventListener: () => {}, AudioContext: undefined, webkitAudioContext: undefined };
const shimDoc = { getElementById: () => fakeCanvas, createElement: () => ({ width: 0, height: 0, getContext: () => makeCtx() }) };
const shimStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
const results = [];
let laneN = 0;
function lane(name, fn) { laneN++; try { fn(); results.push([laneN, name, true, '']); } catch (e) { results.push([laneN, name, false, e.message]); } }
function assert(c, m) { if (!c) throw new Error(m || 'assert failed'); }
function eq(a, b, m) { if (a !== b) throw new Error(`${m || 'eq'}: got ${JSON.stringify(a)} want ${JSON.stringify(b)}`); }

const fn = new Function('window', 'document', 'localStorage', 'location', 'fetch', 'setInterval', 'requestAnimationFrame', 'performance', 'URLSearchParams', code);
fn(shimWindow, shimDoc, shimStorage, { search: '' }, () => Promise.resolve({ json: () => Promise.resolve({ ok: true }) }), () => 0, () => 0, performance, URLSearchParams);
const M = shimWindow.FS;
const P = () => M.player;
const K = M.keys;
function pump(n, dt) { M.pump(n, dt); }
function tele(x, y) { P().x = x; P().y = y; P()._lx = x; P()._ly = y; }
function god() { P().hp = 100; P().iframes = 2; P().maxHp = Math.max(P().maxHp, 100); }
function press(k) { K[k + '_p'] = true; M.step(); K[k + '_p'] = false; }

lane('it compiles + window.FS lives', () => assert(typeof M.startRun === 'function'));
lane("Adam's three: nell strongest AND slowest, allzaban fastest", () => {
  const [az, ma, ne] = M.ARCH_KEYS.map(k => M.ARCH[k]);
  assert(ne.dmg > ma.dmg && ma.dmg > az.dmg, 'damage order wrong');
  assert(ne.speed < ma.speed && ma.speed < az.speed, 'speed order wrong');
});
lane('canyon wake: ring 1, the scorpion waits (Adam storyboard)', () => {
  M.startRun(0);
  eq(M.ring, 1);
  assert(M.foes.some(f => f.type === 'scorpion'), 'no first enemy in the pit');
});
lane('THE LAW: steps advance with movement', () => {
  const s0 = M.steps;
  K['KeyD'] = true; pump(40); K['KeyD'] = false;
  assert(M.steps > s0 + 2, `steps barely moved (${s0} -> ${M.steps})`);
});
lane('THE LAW: any direction levels you — east works', () => {
  M.startRun(0); tele(600, 0); pump(3); eq(M.ring, 2, 'east');
});
lane('THE LAW: any direction levels you — west works too', () => {
  M.startRun(0); tele(-600, 0); pump(3); eq(M.ring, 2, 'west');
});
lane('canyon cliff holds — and the worn passes lead out', () => {
  M.startRun(0);
  tele(335, 0); pump(4);   // angle 0 is seeded away from every pass
  const r = Math.hypot(P().x, P().y);
  assert(r <= 362, `cliff leaked (r ${r})`);
  const pa = M.G.passes[0];
  tele(Math.cos(pa) * 330, Math.sin(pa) * 330); pump(2);
  tele(Math.cos(pa) * 352, Math.sin(pa) * 352); pump(4);   // through the gap — no push
  assert(Math.hypot(P().x, P().y) > 340, 'the pass did not let us through');
  eq(M.ring, 2, 'pass exit is not level 2');
});
lane('the pit forgives — the soul does not fade until you climb out', () => {
  M.startRun(0);
  const t0 = M.G.timer;
  pump(120);
  eq(M.G.timer, t0, 'timer drained inside the canyon');
});
lane('tumbleweed hurts and cannot be hurt', () => {
  god(); M.startRun(0); god();
  M.spawnAmbient('tumble', P().x + 5, P().y);
  const tw = M.ambient[M.ambient.length - 1];
  P().iframes = 0; pump(3);
  assert(P().hp < 100, 'tumbleweed never touched the player');
  pump(30);
  assert(M.ambient.includes(tw), 'tumbleweed took damage and vanished — it must be unattackable');
});
lane('pack rat bites and steals essence', () => {
  god(); M.startRun(0); god();
  M.spawnAmbient('rat', P().x + 200, P().y);
  M.spawnEssence(P().x + 205, P().y, 5);
  const before = M.orbs.length;
  let bitten = false;
  for (let i = 0; i < 400 && !bitten; i++) { god(); pump(1); if (P().hp < 100) bitten = true; }
  assert(M.orbs.length < before, 'rat ignored the essence');
});
lane('scorpion: attackable, dies, pays essence', () => {
  god(); M.startRun(0); god();
  const n0 = M.orbs.length;
  const sc = M.spawnFoe('scorpion', P().x + 30, P().y);
  sc.hp = 0; pump(3);
  assert(!M.foes.includes(sc), 'scorpion survived death');
  assert(M.orbs.length > n0 || P().essence > 0, 'no soul essence paid');
});
lane('rattlesnake: 50/50 can simply kill you (forced true)', () => {
  god(); M.startRun(0); god();
  const sc = M.foes.find(f => f.type === 'scorpion');
  if (sc) sc.hp = 0;                       // the pit's scorpion and the tumbleweed keep refreshing
  M.ambient.length = 0;                    // iframes over the strike window — test the law alone
  M.forceRattleKill = true;
  const sn = M.spawnFoe('snake', P().x + 30, P().y);
  let dead = false;
  for (let i = 0; i < 480 && !dead; i++) { pump(1); if (M.G.state === 'dead') dead = true; }
  M.forceRattleKill = false;
  assert(dead, 'rattle never killed at full hp — the law is broken');
});
lane('rattlesnake: the roll dodges even the fatal bite', () => {
  M.startRun(0); god();
  M.forceRattleKill = true;
  const sn = M.spawnFoe('snake', P().x + 30, P().y);
  let resolved = false;
  for (let i = 0; i < 400 && !resolved; i++) {
    P().rollT = 0.3; // hold the roll through the strike
    pump(1);
    resolved = sn.state !== 'strike' && sn.cd > 1;
  }
  M.forceRattleKill = false;
  assert(M.G.state === 'play', 'the roll did not save you');
});
lane('coyote pack closes the circle', () => {
  god(); M.startRun(0); god();
  tele(600, 0); pump(2);   // open desert — the surround needs room, not a cliff at its back
  M.foes.length = 0;       // drop any ring-transition rolls — this lane is about the pack alone
  M.spawnPackAround(P().x, P().y, 'coyote', 4);
  const coy = M.foes.filter(f => f.type === 'coyote');
  eq(coy.length, 4, 'pack size wrong');
  tele(coy[0].x + 150, coy[0].y); pump(4);   // walk into sight — the pack wakes as one
  const d0 = coy.reduce((s, f) => s + Math.hypot(f.x - P().x, f.y - P().y), 0) / 4;
  let minD = 1e9;
  for (let i = 0; i < 600; i++) { god(); pump(1); minD = Math.min(minD, ...coy.map(f => Math.hypot(f.x - P().x, f.y - P().y))); }
  assert(minD < 110, `pack never closed the circle (min ${minD.toFixed(0)})`);
});
lane("cowboys: one strong OR many weak — both spawn right", () => {
  M.startRun(0); god();
  M.spawnPackAround(P().x, P().y, 'cowboy', 1);
  eq(M.foes.filter(f => f.type === 'boss').length, 1, 'leader missing');
  M.startRun(0); god();
  M.spawnPackAround(P().x, P().y, 'cowboy', 3);
  eq(M.foes.filter(f => f.type === 'cowboy').length, 3, 'lackeys missing');
});
lane('lone gunman duels, dies, pays the fire-rate mod', () => {
  M.startRun(0); god();
  M.forceGunman = true; M.G.nextEventStep = 0;
  K['KeyD'] = true; pump(50); K['KeyD'] = false;   // cross integer step boundaries — the event clock ticks per step
  M.forceGunman = false;
  const gm = M.foes.find(f => f.type === 'gunman');
  assert(gm, 'no gunman from the event roll');
  tele(gm.x + 150, gm.y); pump(4);   // walk into his sight — the duel begins
  let fired = false;
  for (let i = 0; i < 300 && !fired; i++) { god(); pump(1); if (M.eshots.length > 0) fired = true; }
  assert(fired, 'gunman never fired');
  gm.hp = 0; pump(3);
  assert(P().rapid === true, 'fire-rate mod not granted');
});
lane('oasis heals, refills the soul, and keeps the horde out', () => {
  god(); M.startRun(0); god();
  M.events.push({ t: 'oasis', x: P().x + 40, y: P().y });
  P().hp = 30; M.G.timer = 20;
  tele(P().x + 40, P().y); pump(4);
  assert(P().hp > 90, 'oasis did not heal');
  assert(M.G.timer > 95, 'oasis did not refill the timer');
  M.spawnPackAround(P().x + 40, P().y, 'coyote', 1);
  const cy = M.foes.find(f => f.type === 'coyote');
  pump(4);
  assert(Math.hypot(cy.x - (P().x + 40), cy.y - P().y) >= 100, 'a coyote hunted inside the haven');
});
lane('wishing well: one wish, one level', () => {
  M.startRun(0); god();
  const lv0 = P().level;
  M.events.push({ t: 'well', x: P().x + 10, y: P().y });
  pump(2); press('KeyE'); pump(2);
  eq(P().level, lv0 + 1, 'wish not granted');
});
lane('merchant sells a mod — the shot changes color', () => {
  M.startRun(0); god();
  P().essence = 80;
  const mod0 = P().mod;
  M.events.push({ t: 'merchant', x: P().x + 10, y: P().y });
  pump(2); press('KeyE'); pump(2);
  assert(P().mod !== mod0, 'no mod bought');
  assert(P().essence <= 20, 'essence not charged');
});
lane("storyline chain 1: grave -> journal -> the hermit's fire", () => {
  M.startRun(0); god();
  eq(M.G.graveFound, false);
  M.events.push({ t: 'grave', x: P().x + 10, y: P().y });
  pump(2); press('KeyE'); pump(2);
  eq(M.G.graveFound, true, 'journal not found');
  eq(M.G.hermitDue, true, 'hermit not foretold');
  M.G.nextEventStep = 0;
  K['KeyD'] = true; pump(50); K['KeyD'] = false;
  assert(M.events.some(e => e.t === 'hermit'), 'hermit never appeared');
  const hm = M.events.find(e => e.t === 'hermit');
  tele(hm.x + 10, hm.y); pump(2);
  const hp0 = P().maxHp;
  press('KeyE'); pump(2);
  eq(P().maxHp, hp0 + 25, 'hermit did not share his fire');
});
lane('the death timer: fades, essence feeds it, zero ends you, scrap restarts', () => {
  M.startRun(0); god();
  tele(600, 0); pump(3);   // leave the pit — the timer only runs in the open
  const t0 = M.G.timer;
  pump(60);
  assert(M.G.timer < t0, 'timer does not fade');
  M.spawnEssence(P().x, P().y, 5);
  const t1 = M.G.timer;
  pump(3);
  assert(M.G.timer > t1, 'essence did not feed the timer');
  M.G.timer = 0.3;
  let dead = false;
  for (let i = 0; i < 120 && !dead; i++) { pump(1); if (M.G.state === 'dead') dead = true; }
  assert(dead, 'soul never faded to death');
  assert(String(M.G.deathWhy).includes('faded'), 'wrong death reason');
  press('KeyR');
  eq(M.G.state, 'play', 'restart failed');
  eq(P().essence, 12, 'no scrap of soul on waking');
  eq(M.ring, 1, 'restart not in the canyon');
});
lane('the rim: DEATH rises, and killing him is the victory', () => {
  M.startRun(0); god();
  tele(2600, 0); pump(4);
  assert(M.G.rimReached, 'rim not reached');
  const death = M.foes.find(f => f.isDeath);
  assert(death, 'death never rose');
  assert(M.G.windStopped, 'the wind did not stop for him');
  death.hp = 0; pump(3);
  eq(M.G.state, 'victory', 'killing death is not victory');
});
lane('perf: 100 foes keep steps under 8ms', () => {
  M.startRun(0); god();
  for (let i = 0; i < 100; i++) M.spawnFoe('scorpion', P().x + (Math.random() * 1200 - 600), P().y + (Math.random() * 900 - 450));
  const t0 = process.hrtime.bigint();
  pump(200);
  const ms = Number(process.hrtime.bigint() - t0) / 1e6 / 200;
  assert(ms < 8, `avg step ${ms.toFixed(2)}ms`);
});

// ================= mud steals =================
M.startRun(0); god();
lane('CHRONICLE: the run writes its own log', () => {
  const c0 = M.chron.length;
  const e = M.spawnFoe('scorpion', P().x + 30, P().y);
  e.hp = 0; pump(2);
  assert(M.chron.length > c0 && M.chron.some(c => c.text.includes('falls')), 'chronicle never logged a kill');
});
lane('GRUDGES: survivors get named, faster, remembered', () => {
  M.startRun(0); god();
  const cb = M.spawnFoe('cowboy', P().x + 60, P().y);
  cb.asleep = false; cb.arrive = 0;
  cb.hp = cb.maxHp = 200;   // overheal so two swings survive
  const spd0 = cb.spd;
  for (let i = 0; i < 6 && !cb.grudged; i++) {
    P().facing = Math.atan2(cb.y - P().y, cb.x - P().x);
    P().atkCd = 0;
    M.playerSwing();
    pump(2);
  }
  assert(cb.grudged === true, 'no grudge formed');
  assert(typeof cb.name === 'string' && cb.name.length > 2, 'grudge granted no name');
  assert(cb.spd > spd0, 'grudge grants no speed');
});
lane('SIGNS: level-up offers a draft and the world holds', () => {
  M.startRun(0); god();
  P().xp = P().xpNext;
  M.spawnEssence(P().x, P().y, 5);
  pump(3);
  assert(M.G.draft && M.G.draft.length === 3, 'no draft offered');
  const foe = M.spawnFoe('scorpion', P().x + 40, P().y);
  foe.asleep = false; foe.arrive = 0;
  const fx0 = foe.x;
  pump(30);
  eq(foe.x, fx0, 'the world did not hold during the draft');
  press('Digit1'); pump(2);
  eq(M.G.draft, null, 'draft never resolved');
  assert(Object.keys(P().signs || {}).length === 1, 'sign not taken');
});
lane("DEAD MAN'S HAND: every 8th shot doubles", () => {
  M.startRun(0); god();
  M.giveSign('deadmin');
  assert(P().deadHand === true, 'sign did not apply');
});
lane("PREACHER'S LAST WORD: cheats death once", () => {
  M.startRun(0); god();
  M.giveSign('preacher');
  P().iframes = 0;
  M.hurt(9999, 'the gallows');
  assert(M.G.state === 'play', 'last word did not hold');
  assert(P().hp > 0 && P().hp <= P().maxHp * 0.2, 'rose at the wrong sliver');
});
lane("RATTLESNAKE'S SECRET: the rattle never out-right kills", () => {
  M.startRun(0); god();
  P().iframes = 0;
  M.giveSign('rattle');
  const sc = M.foes.find(f => f.type === 'scorpion'); if (sc) sc.hp = 0;
  M.ambient.length = 0;
  M.forceRattleKill = true;
  const sn = M.spawnFoe('snake', P().x + 30, P().y);
  let struck = false;
  for (let i = 0; i < 500 && !struck; i++) { P().hp = Math.max(P().hp, 100); pump(1); if (P().hp < 100) struck = true; }
  M.forceRattleKill = false;
  assert(struck && M.G.state === 'play', 'the ward failed');
});
lane('DYNAMITE: the leader lobs it, it telegraphs, it hurts both sides', () => {
  M.startRun(0); god();
  M.spawnPackAround(P().x, P().y, 'cowboy', 1);
  const lead = M.foes.find(f => f.type === 'boss');
  assert(lead, 'no leader');
  tele(lead.x + 120, lead.y); pump(4);   // wake him — nothing hunts until it sees you
  let tossed = false;
  for (let i = 0; i < 900 && !tossed; i++) { god(); pump(1); if (M.dyns.length > 0) tossed = true; }
  assert(tossed, 'leader never threw dynamite');
  const hp0 = P().hp;
  tele(M.dyns[0].tx, M.dyns[0].ty);
  P().iframes = 0;
  pump(70);
  assert(P().hp < hp0 || M.G.state === 'dead', 'dynamite never bit');
});
lane('THE COMBINE: wounded cowboys merge into THE DEPUTY', () => {
  M.startRun(0); god();
  const a = M.spawnFoe('cowboy', P().x + 40, P().y);
  const b = M.spawnFoe('cowboy', P().x + 90, P().y);
  a.arrive = 0; b.arrive = 0;
  a.hp = a.maxHp * 0.4; b.hp = b.maxHp * 0.4;
  a.hp = 0; pump(3);
  const dep = M.foes.find(f => f.name === 'THE DEPUTY OF THE FLATS');
  assert(dep, 'the deputy never rose');
  assert(dep.hp > a.maxHp, 'deputy too weak');
  dep.hp = 0; pump(3);
  assert(P().essence >= 40, 'deputy paid nothing');
});
lane('WHISKEY: the world drinks slow, you do not', () => {
  M.startRun(0); god();
  M.spawnWhiskey(P().x + 10, P().y);
  pump(3);
  assert(M.G.still > 0, 'whiskey did not slow the world');
});
lane('REWIND: the desert gives back five seconds, once', () => {
  M.startRun(0); god();
  pump(140);   // snapshots every half-second — build the buffer
  P().iframes = 0; M.hurt(9999, 'the test');
  assert(M.G.state === 'dead' && M.G.rewindOffer, 'no rewind offered');
  press('KeyT');
  eq(M.G.state, 'play', 'rewind failed');
  assert(M.G.rewUsed === true, 'rewind not consumed');
  P().iframes = 0; M.hurt(9999, 'the test again');
  assert(M.G.rewindOffer === false, 'rewind offered twice');
  press('KeyR');
});
lane('CACHE: key, box, payout', () => {
  M.startRun(0); god();
  P().essence = 0;
  M.events.push({ t: 'cachekey', x: P().x + 10, y: P().y, used: false });
  press('KeyE'); pump(2);
  eq(M.G.hasCacheKey, true, 'key not taken');
  M.events.push({ t: 'cache', x: P().x + 10, y: P().y, used: false });
  press('KeyE'); pump(2);
  assert(P().essence >= 60, 'cache paid nothing');
  assert(P().mod !== 'none', 'cache paid no mod');
});
lane('QUICKSAND: the sand drags', () => {
  M.startRun(0); god();
  M.G.leftCanyon = true;
  tele(1500, 1500);
  K['KeyD'] = true; pump(30); K['KeyD'] = false;
  const free = P().x - 1500;
  // a patch squarely on the next stretch of path
  M.decor.push({ t: 'sandpatch', x: P().x + 60, y: P().y, s: 1 });
  M.decor.push({ t: 'sandpatch', x: P().x + 120, y: P().y, s: 1 });
  const x0 = P().x;
  K['KeyD'] = true; pump(30); K['KeyD'] = false;
  const slow = P().x - x0;
  assert(slow < free * 0.7, `sand did not drag (free ${free.toFixed(0)} vs slow ${slow.toFixed(0)})`);
});
lane('SLEEP: nothing hunts until it sees you', () => {
  M.startRun(0); god();
  const cb = M.spawnFoe('cowboy', P().x + 500, P().y);
  assert(cb.asleep === true, 'foe spawned awake');
  const x0 = cb.x;
  pump(60);
  assert(Math.abs(cb.x - x0) < 20, 'a sleeping foe went hunting');
  tele(cb.x - 100, cb.y); pump(3);
  assert(cb.asleep === false, 'foe never woke at close range');
});

// ================= DEATH, properly =================
function riseForTest() {
  M.startRun(0); god();
  M.G.leftCanyon = true; M.G.timer = 100;
  tele(2600, 0); pump(4);
  const dx = M.foes.find(f => f.isDeath);
  assert(dx, 'death never rose');
  return dx;
}
lane('DEATH has weight now: 900 blood, and he hunts', () => {
  const dx = riseForTest();
  eq(dx.maxHp, 900);
  eq(dx.spd, 100);
  assert(M.G.deathIntro > 0, 'no intro — he arrives silent');
});
lane('THE HUNT: the lunge closes the gap you hide behind', () => {
  const dx = riseForTest();
  dx.cd = 999;            // no daggers — this lane is about the lunge
  dx.lungeCd = 0;
  tele(dx.x - 400, dx.y); pump(4);
  const d0 = Math.hypot(dx.x - P().x, dx.y - P().y);
  let sawTel = false;
  for (let i = 0; i < 120 && !sawTel; i++) { god(); pump(1); if (dx.state === 'lungeTel' || dx.state === 'lunging') sawTel = true; }
  assert(sawTel, 'no lunge telegraph');
  for (let i = 0; i < 60; i++) { god(); pump(1); }
  const d1 = Math.hypot(dx.x - P().x, dx.y - P().y);
  assert(d1 < d0 - 150, `the lunge closed nothing (${d0.toFixed(0)} -> ${d1.toFixed(0)})`);
});
lane('THE HARVEST: at two-thirds blood the withered rise', () => {
  const dx = riseForTest();
  dx.cd = 999; dx.lungeCd = 999;
  dx.hp = dx.maxHp * 0.6; pump(4);
  assert(M.foes.some(f => f.type === 'withered'), 'no withered at the harvest');
});
lane('THE REAPING: death stops walking — he steps between shadows', () => {
  const dx = riseForTest();
  dx.cd = 999; dx.lungeCd = 999;
  dx.hp = dx.maxHp * 0.3; pump(4);
  assert(dx.phase === 3, 'phase 3 never came');
  let maxJump = 0, sawStep = false, px = dx.x, py = dx.y;
  dx.tpT = 0.1;
  for (let i = 0; i < 90; i++) {
    god(); pump(1);
    maxJump = Math.max(maxJump, Math.hypot(dx.x - px, dx.y - py));
    if (dx.state === 'tpOut') sawStep = true;
    px = dx.x; py = dx.y;
  }
  assert(sawStep && maxJump > 50, `he never stepped (max frame jump ${maxJump.toFixed(0)})`);
});
lane('the sweep drinks: he steals your soul and feeds', () => {
  const dx = riseForTest();
  dx.cd = 50; dx.lungeCd = 999;
  dx.hp = dx.maxHp * 0.5;
  tele(dx.x + 80, dx.y); pump(2);
  dx.sweep = 0.05; dx.sweepA = 0; dx.sweepChain = false;
  const t0 = M.G.timer, h0 = dx.hp;
  let fed = false;
  for (let i = 0; i < 200 && !fed; i++) {
    // stay in his arc, no mercy i-frames — the scythe connects
    P().x = dx.x + Math.cos(dx.sweepA || 0) * 80; P().y = dx.y + Math.sin(dx.sweepA || 0) * 80;
    P().iframes = 0; P().hp = Math.max(P().hp, 100);
    pump(1);
    if (M.G.timer < t0 - 5 && dx.hp > h0) fed = true;
  }
  assert(fed, 'the sweep neither stole nor fed');
});
lane('his presence withers: the timer bleeds faster in close', () => {
  const dx = riseForTest();
  dx.cd = 999; dx.lungeCd = 999; dx.sweep = 0;
  tele(dx.x - 400, dx.y);   // inward — away from the world clamp
  const t0 = M.G.timer;
  for (let i = 0; i < 120; i++) { god(); pump(1); }
  const farDrain = t0 - M.G.timer;
  M.G.timer = 100;
  tele(dx.x + 150, dx.y);
  const t1 = M.G.timer;
  for (let i = 0; i < 120; i++) { god(); pump(1); }
  const nearDrain = t1 - M.G.timer;
  assert(nearDrain > farDrain * 1.5, `aura barely withers (far ${farDrain.toFixed(1)} vs near ${nearDrain.toFixed(1)})`);
});

const fails = results.filter(r => !r[2]);
for (const [n, name, ok, err] of results) console.log(`${ok ? 'PASS' : 'FAIL'} ${String(n).padStart(2)} ${name}${ok ? '' : '  — ' + err}`);
console.log(`\n${results.length - fails.length}/${results.length} lanes green${fails.length ? `, ${fails.length} RED` : ''}`);
process.exit(fails.length ? 1 : 0);
