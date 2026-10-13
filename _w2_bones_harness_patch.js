// W2 bones harness patch — exact-match, abort-on-drift, single atomic write.
'use strict';
const fs = require('fs');
const F = 'C:/Users/foste/Documents/projects/local_sovereign_agent/scripts/test_mud_replay.js';
let c = fs.readFileSync(F, 'utf8');
const edits = [];
const E = (oldS, newS) => edits.push([oldS, newS]);

// H1: loadGame gains a search param (bones lanes boot the dead bearer with a URL name)
E(`function loadGame(storage) {`, `function loadGame(storage, search) {`);
E(`fn(shimWindow, shimDocument, storage || shimStorage, { search: '' }, shimFetch, () => 0, shimRaf, performance, URLSearchParams);`,
  `fn(shimWindow, shimDocument, storage || shimStorage, { search: search || '' }, shimFetch, () => 0, shimRaf, performance, URLSearchParams);`);

// H2: snap() pins ghost + bones-pool state (both deterministic: the ghost path never touches Math.random)
E(`      M.lore.rolls || 0, M.lore.fires || 0, M.lore.wall ? 1 : 0, M.lore.wait ? 1 : 0],
  });
}`,
`      M.lore.rolls || 0, M.lore.fires || 0, M.lore.wall ? 1 : 0, M.lore.wait ? 1 : 0],
    gh: M.ghosts.map(g => [g.room, g.x, g.y, g.hp, g.maxHp, g.toughness, g.said ? 1 : 0, Math.round(g.cd * 1000), Math.round(g.t * 1000), g.ph, g.statN, g.statV]),   // bones ghosts — ph derives from the dead run's seed, so it IS pinned (no Math.random in the ghost path)
    bn: M.bones.map(b => [b.v, b.seed, b.room, b.x, b.y, b.cause, b.name, b.stat, b.statV]),   // the bones pool — machine state, pinned like lore
  });
}`);

// H3: bones lanes before the report
E(`const fails = results.filter(r => !r[2]);`,
`// ================= BONES (W2): NetHack bones files — dead runs haunt later runs =================
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

lane('BN: die in run A -> run B entering the room meets A\\'s ghost (name, cause, toughness carried)', () => {
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
  eq(g.name, 'UR-VABOK', 'ghost does not wear the dead run\\'s name');
  eq(g.cause, rec.cause, 'ghost does not carry the dead run\\'s cause');
  eq(g.toughness, 4 + 3 * rec.statV, 'ghost toughness is not the dead run\\'s hardest stat');
  // the whisper, on touch
  B.player.iframes = 999;   // hazards off; the ghost touch is not damage — it must still whisper
  let g2 = 0, minSt = 999;
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

const fails = results.filter(r => !r[2]);`);

let i = 0;
for (const [oldS, newS] of edits) {
  i++;
  const parts = c.split(oldS);
  if (parts.length !== 2) {
    console.error('ABORT: anchor ' + i + ' matched ' + (parts.length - 1) + ' times (want exactly 1): ' + JSON.stringify(oldS.slice(0, 80)));
    process.exit(1);
  }
  c = parts[0] + newS + parts[1];
}
fs.writeFileSync(F, c);
console.log('applied ' + edits.length + '/' + edits.length + ' harness edits atomically');
for (const k of ["BONES_POOL", "lane('BN:", "gh: M.ghosts", "bn: M.bones", "search: search || ''"]) {
  const n = c.split(k).length - 1;
  if (n === 0) { console.error('ABORT POST: missing ' + k); process.exit(1); }
  console.log('  ok ' + k + ' x' + n);
}
