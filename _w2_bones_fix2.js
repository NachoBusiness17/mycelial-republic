// W2 fix pass 2 (post-W4 merge): FX4 hurt event + deterministic causeClass for replay surfaces.
// W4 kept the (possibly genName-fed) killer name in the SAFE_STORE record + whisper — legal
// cosmetic surfaces — but the evlog 'bones' receipt and the snapshot's bn pin must stay
// deterministic, so records gain causeClass (type-based) and those surfaces read it.
'use strict';
const fs = require('fs');
const F = 'C:/Users/foste/Documents/projects/local_sovereign_agent/dashboard/static/games/mud.html';
const H = 'C:/Users/foste/Documents/projects/local_sovereign_agent/scripts/test_mud_replay.js';
let c = fs.readFileSync(F, 'utf8');
const edits = [];
const E = (oldS, newS) => edits.push([oldS, newS]);

// 1. FX4: the hurt event (still missing after the W4 merge)
E(`  player.hp -= dmg;
  player.hitFlash = 0.2;
  player.iframes = 0.5;
  G.shake = 8;
  addDmgNum(player.x, player.y - player.r, dmg, '#f44');`,
`  player.hp -= dmg;
  player.hitFlash = 0.2;
  player.iframes = 0.5;
  G.shake = 8;
  evlog.push(Object.assign(evt(), { e: 'hurt', d: Math.round(dmg * 1000) / 1000, hp: Math.round(player.hp * 1000) / 1000 }));
  addDmgNum(player.x, player.y - player.r, dmg, '#f44');`);

// 2. W2+W4: the record gains a deterministic class cause alongside the flavored one
E(`  bonesWrite({ v: 1, seed: runSeed, room: dRoom, x: Math.round(player.x), y: Math.round(player.y), cause: dCause, name: ME.name, stat: hs.n, statV: hs.v });`,
`  bonesWrite({ v: 1, seed: runSeed, room: dRoom, x: Math.round(player.x), y: Math.round(player.y), cause: dCause, causeClass: dCauseLog, name: ME.name, stat: hs.n, statV: hs.v });`);

// 3. W2: the evlog bones receipt carries the deterministic class cause
E(`          evlog.push(Object.assign(evt(), { e: 'bones', room: rid, n: rec.name, c: rec.cause, tn: ghostToughness(rec) }));`,
`          evlog.push(Object.assign(evt(), { e: 'bones', room: rid, n: rec.name, c: rec.causeClass || rec.cause, tn: ghostToughness(rec) }));`);

let i = 0;
for (const [oldS, newS] of edits) {
  i++;
  const parts = c.split(oldS);
  if (parts.length !== 2) {
    console.error('ABORT game: anchor ' + i + ' matched ' + (parts.length - 1) + ' times: ' + JSON.stringify(oldS.slice(0, 80)));
    process.exit(1);
  }
  c = parts[0] + newS + parts[1];
}
fs.writeFileSync(F, c);

// 4. harness: snap's bn pins causeClass (deterministic), never the flavored cause
let h = fs.readFileSync(H, 'utf8');
const hOld = `bn: M.bones.map(b => [b.v, b.seed, b.room, b.x, b.y, b.cause, b.name, b.stat, b.statV]),   // the bones pool — machine state, pinned like lore`;
const hNew = `bn: M.bones.map(b => [b.v, b.seed, b.room, b.x, b.y, b.causeClass || '', b.name, b.stat, b.statV]),   // the bones pool — machine state, pinned like lore (causeClass: the flavored cause is whisper-only, never pinned)`;
if (h.split(hOld).length !== 2) { console.error('ABORT harness: snap bn anchor drifted'); process.exit(1); }
h = h.replace(hOld, hNew);
fs.writeFileSync(H, h);
console.log('fix pass 2: 3 game edits + 1 harness edit applied');
