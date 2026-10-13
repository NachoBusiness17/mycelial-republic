// W2 bones + FX4/W5/N9/N10/N12 restore patch — exact-match, abort-on-drift, single atomic write.
// The wave fold's mirror-restore reverted games/mud.html to pristine; this re-lands the ported
// base (per FX4/W5/N9/N10/N12 receipts + the harness contracts) and W2 bones on top.
'use strict';
const fs = require('fs');
const F = 'C:/Users/foste/Documents/projects/local_sovereign_agent/dashboard/static/games/mud.html';
let c = fs.readFileSync(F, 'utf8');
const edits = [];
const E = (oldS, newS) => edits.push([oldS, newS]);

// ---- FX4: RNG LAW utility block ----
E(`const rnd = (a,b)=>a+Math.random()*(b-a);
const rndi = (a,b)=>Math.floor(rnd(a,b+1));`,
`// RNG LAW (replay, FX4 — toy.html LCG constants, swarm.html FX1 house pattern): one seeded LCG
// drives every gameplay-affecting draw. startGame(forcedSeed) seeds each run and records runSeed;
// pass a number to replay a recorded run. With no forced seed the day's fleet seed (W1A) starts
// the world — same day, same starting monastery. Cosmetic-only draws (particles, camera shake,
// name flavor, relay id) stay on Math.random/crnd so render jitter can never perturb the replay
// stream — site classification lives in watch/inbox/wave_20260916/receipts/FX4_MUD_REPLAY_PORT.md.
let lcg = 1, runSeed = 0, runN = 0;
function seedRun(s) { runSeed = (s >>> 0) || 1; lcg = runSeed; }
const rng = () => { lcg = (Math.imul(lcg, 1664525) + 1013904223) >>> 0; return lcg / 4294967296; };
const rnd = (a,b)=>a+rng()*(b-a);           // seeded — advances the replay stream
const crnd = (a,b)=>a+Math.random()*(b-a);  // cosmetic — render-only noise, never touches the stream
const rndi = (a,b)=>Math.floor(rnd(a,b+1));`);

// ---- W5: boot-load the ascension ladder (title screen shows it before any run) ----
E(`  spawnTimer: 0,
  super: 0,
};`,
`  spawnTimer: 0,
  super: 0,
};
// W5: boot-load the persisted ascension ladder so the title can show it before any run starts
try { G.ng = Math.max(0, parseInt(localStorage.getItem('mud_asc') || '0', 10) || 0); } catch (e) {}`);

// ---- N10: the vault gate wall tag ----
E(`  // south of the forge — sealed drafts, nothing down there
  {x:1300,y:800,w:620,h:40},`,
`  // south of the forge — THE VAULT GATE: plates I (infirmary) + II (forge) grind it open; the pocket pays
  {x:1300,y:800,w:620,h:40,gate:true},`);

// ---- N10: plate II onto the forge floor ----
E(`plates: [{ x: 220, y: 340, on: false }, { x: 1720, y: 1000, on: false }]`,
`plates: [{ x: 220, y: 340, on: false }, { x: 1720, y: 700, on: false }]`);

// ---- FX4: evlog after chronicle ----
E(`function chronicle(text, color) {
  chron.push({ t: G.time || 0, text, color: color || '#9a8a6a' });
  if (chron.length > 40) chron.shift();
}`,
`function chronicle(text, color) {
  chron.push({ t: G.time || 0, text, color: color || '#9a8a6a' });
  if (chron.length > 40) chron.shift();
}
// Replay law (FX4): append-only gameplay event log, cleared on startGame. Same runSeed + same
// inputs → byte-identical log (proven by scripts/test_mud_replay.js). Cosmetic randomness
// (names, particles) is deliberately kept OUT of this log.
const evlog = [];
const evt = () => ({ t: +G.time.toFixed(3) });`);

// ---- W2: SAFE_STORE + bones block before lootBeams ----
E(`let lootBeams = [];`,
`// ---- SAFE_STORE (privacy-mode law, swarm.html house pattern): localStorage throws in private
// browsing / blocked-cookie modes and would kill the game at load. ONE guarded accessor; when
// storage is unavailable it falls back to an in-memory object for the session. ----
const SAFE_STORE = (() => {
  const mem = {}; let ls = null;
  try { ls = window.localStorage; ls.setItem('__mud_probe', '1'); ls.removeItem('__mud_probe'); } catch (e) { ls = null; }
  return {
    get(k, d) { try { const v = ls ? ls.getItem(k) : mem[k]; return (v === null || v === undefined) ? d : v; } catch (e) { return d; } },
    set(k, v) { try { if (ls) ls.setItem(k, String(v)); else mem[k] = String(v); } catch (e) { mem[k] = String(v); } },
    getJSON(k, d) { try { const v = this.get(k, null); if (v === null || v === undefined) return d; const p = JSON.parse(v); return (p === null || p === undefined) ? d : p; } catch (e) { return d; } },
    setJSON(k, v) { this.set(k, JSON.stringify(v)); },
  };
})();
// ---- BONES (NetHack-steal): dead runs become content that haunts later runs. When you die, a
// bones record (seed, room, spot, cause, name line, hardest stat) is filed to the pool — machine
// state, like lore: it survives respawn, reload, everything. A later run entering that room rolls
// the SEEDED stream for a haunting (one bones-roll per room activation — never bare Math.random).
// The ghost whispers its cause and burns stamina by its toughness (the dead run's hardest stat);
// it CANNOT kill — the every-enemy-can-kill law stays for the living. The dead teach, they don't
// execute. Pool is capped at BONES_CAP, FIFO. The courtyard is sanctified: bones are filed
// everywhere, but ghosts do not rise there. ----
const BONES_KEY = 'mud_bones', BONES_CAP = 10;
let bones = SAFE_STORE.getJSON(BONES_KEY, []);
if (!Array.isArray(bones)) bones = [];
let ghosts = [];   // the risen this session — spawned only from the seeded bones-roll, cleared on startGame
function bonesSave() { SAFE_STORE.setJSON(BONES_KEY, bones); }
function bonesWrite(rec) {
  bones.push(rec);
  while (bones.length > BONES_CAP) bones.shift();   // FIFO — old bones rot out of the pool
  bonesSave();
  return rec;
}
function hardestStat() {
  const cands = [['might', player.might | 0], ['vigor', player.vigor | 0], ['swiftness', player.swiftness | 0]];
  cands.sort((a, b) => b[1] - a[1]);
  if (cands[0][1] > 0) return { n: cands[0][0], v: cands[0][1] };
  return { n: 'grit', v: Math.max(1, player.level) };
}
function ghostToughness(rec) { return 4 + 3 * (rec.statV || 1); }
function spawnGhost(rec, rid) {
  const R = ROOMS[rid] || { x: 0, y: 0, w: WORLD_W, h: WORLD_H };
  const tn = ghostToughness(rec);
  ghosts.push({
    room: rid,
    x: clamp(rec.x, R.x + 20, R.x + R.w - 20), y: clamp(rec.y, R.y + 20, R.y + R.h - 20),
    r: 12, hp: tn, maxHp: tn, toughness: tn,
    name: rec.name || 'a nameless lantern', cause: rec.cause || 'the dark itself',
    statN: rec.stat || 'grit', statV: rec.statV || 1,
    ph: (rec.seed || 1) % 7,   // deterministic phase from the dead run's seed — the haunting never touches Math.random
    said: false, cd: 0, t: 0,
  });
}
function ghostTick(dt) {
  for (let i = ghosts.length - 1; i >= 0; i--) {
    const g = ghosts[i];
    g.t += dt; g.cd -= dt;
    if (roomOf(player.x, player.y) !== g.room || g.t > 60) { ghosts.splice(i, 1); continue; }   // a ghost haunts its own room
    // the dead drift — fully deterministic, the replay stream is never spent on a haunting
    const d = Math.hypot(player.x - g.x, player.y - g.y);
    if (d < 240 && d > 1) {
      const sp = 30 + 2 * g.toughness;
      g.x += (player.x - g.x) / d * sp * dt;
      g.y += (player.y - g.y) / d * sp * dt;
    } else {
      g.x += Math.sin(G.time * 0.6 + g.ph) * 8 * dt;
      g.y += Math.cos(G.time * 0.5 + g.ph) * 8 * dt;
    }
    // the touch: a whisper and a chill — stamina and snare only, NEVER hp (a ghost cannot kill)
    if (d < g.r + player.r + 2 && g.cd <= 0) {
      g.cd = 1.6;
      if (!g.said) {
        g.said = true;
        evlog.push(Object.assign(evt(), { e: 'whisper', room: g.room }));
        chronicle(g.name + ' whispers: "' + g.cause + ' took me" — their ' + g.statN + ' still holds', '#aaf');
        addMsg(g.name + ': "' + g.cause + ' took me"', '#aaf');
        beep(320, 0.4, 'sine', 0.03); beep(214, 0.5, 'sine', 0.02);
      }
      player.stamina = Math.max(0, player.stamina - (5 + g.toughness));
      player.snared = Math.max(player.snared, 0.25 + 0.05 * g.toughness);
      G.shake = Math.max(G.shake, 3);
    }
  }
}
let lootBeams = [];`);

// ---- FX4: farSpot seeded ----
E(`    const s = PUZZLE_SPOTS[Math.floor(Math.random() * PUZZLE_SPOTS.length)];`,
`    const s = PUZZLE_SPOTS[Math.floor(rng() * PUZZLE_SPOTS.length)];   // gameplay: walk-to-it pays`);

// ---- N10+FX4: puzzleReset — chest pinned in the vault, key seeded via farSpot ----
E(`  for (const pl of puzzle.plates) pl.on = false;
  const s1 = PUZZLE_SPOTS[Math.floor(Math.random() * PUZZLE_SPOTS.length)];
  const s2 = farSpot(s1);
  puzzle.key = { x: s1[0], y: s1[1] };
  puzzle.chest = { x: s2[0], y: s2[1] };
  rebuildVision();`,
`  for (const pl of puzzle.plates) pl.on = false;
  puzzle.chest = { x: 1720, y: 1000 };   // the vault pays from inside the vault — behind the gate, in the south pocket (N10)
  const s1 = farSpot([puzzle.chest.x, puzzle.chest.y]);   // gameplay: key placement — walk-to-it pays, chimes guide
  puzzle.key = { x: s1[0], y: s1[1] };
  rebuildVision();`);

// ---- FX4: makeLoot seeded + loot event ----
E(`function makeLoot(x,y) {
  const roll = Math.random();`,
`function makeLoot(x,y) {
  const roll = rng();   // gameplay: weapon rarity + stats`);
E(`  else rarity = 3;
  const baseNames = ['Sword','Axe','Mace','Blade','Falchion'];`,
`  else rarity = 3;
  evlog.push(Object.assign(evt(), { e: 'loot', r: rarity }));
  const baseNames = ['Sword','Axe','Mace','Blade','Falchion'];`);

// ---- FX4: homeSeed seeded ----
E(`    room: room || null, homeX: x, homeY: y, homeSeed: Math.random() * 7,`,
`    room: room || null, homeX: x, homeY: y, homeSeed: rng() * 7,   // gameplay: drives idle wander heading → positions → combat`);

// ---- FX4: champion event ----
E(`  e.isChampion = true;
  e.name = ch.name;
  chronicle(ch.name + ' stirs', '#f84');
  beep(160, 0.4, 'sawtooth', 0.05);`,
`  e.isChampion = true;
  e.name = ch.name;
  chronicle(ch.name + ' stirs', '#f84');
  evlog.push(Object.assign(evt(), { e: 'champion', room: rid }));
  beep(160, 0.4, 'sawtooth', 0.05);`);

// ---- FX4: room activation event ----
E(`      st.activated = true; st.spawned = 0; st.t = 0.6;`,
`      st.activated = true; st.spawned = 0; st.t = 0.6;
      evlog.push(Object.assign(evt(), { e: 'room', room: rid }));`);

// ---- FX4: bell-ringer seeded + event ----
E(`if (!R.drip && !R.dragon && R.champion && ((window.MUD && window.MUD.forceBell) || Math.random() < 0.45) && NEXT_AFTER[rid]) {`,
`if (!R.drip && !R.dragon && R.champion && ((window.MUD && window.MUD.forceBell) || rng() < 0.45) && NEXT_AFTER[rid]) {   // gameplay: ringer spawns`);
E(`        chronicle('a bell-ringer breaks for the door — stop him', '#fc8');
      }`,
`        chronicle('a bell-ringer breaks for the door — stop him', '#fc8');
        evlog.push(Object.assign(evt(), { e: 'bell', room: rid }));
      }`);

// ---- W2: the bones-roll at activation end ----
E(`      if (st.prepop) {
        for (const e2 of enemies) if (e2.room === rid) e2.aggro = true;
        chronicle('they heard the bell — formed up, waiting', '#f84');
      }
    return;`,
`      if (st.prepop) {
        for (const e2 of enemies) if (e2.room === rid) e2.aggro = true;
        chronicle('they heard the bell — formed up, waiting', '#f84');
      }
      // the BONES-ROLL: one seeded draw per entry — a haunting is never bare Math.random
      if ((window.MUD && window.MUD.forceBones) || rng() < 0.5) {
        const cands = bones.filter(b => b.room === rid && rid !== 'courtyard');   // the courtyard is sanctified
        if (cands.length) {
          const rec = cands[Math.floor(rng() * cands.length)];   // gameplay: which of the dead rise — seeded
          spawnGhost(rec, rid);
          evlog.push(Object.assign(evt(), { e: 'bones', room: rid, n: rec.name, c: rec.cause, tn: ghostToughness(rec) }));
          chronicle('the air goes cold — ' + rec.name + ' walks this room again', '#aaf');
        }
      }
    return;`);

// ---- FX4: clear + sigil events ----
E(`    st.cleared = true;
    for (const d of Object.values(DOORS)) if (d.after === rid) d.locked = false;`,
`    st.cleared = true;
    evlog.push(Object.assign(evt(), { e: 'clear', room: rid }));
    for (const d of Object.values(DOORS)) if (d.after === rid) d.locked = false;`);
E(`      SIGILS.count++;
      chronicle('a sigil — ' + (4 - SIGILS.count) + ' remain', '#fc8');`,
`      SIGILS.count++;
      evlog.push(Object.assign(evt(), { e: 'sigil', n: SIGILS.count }));
      chronicle('a sigil — ' + (4 - SIGILS.count) + ' remain', '#fc8');`);

// ---- FX4: swing sites seeded ----
E(`          if (player.boonCrit && Math.random() < 0.2) { dmg *= 2; }`,
`          if (player.boonCrit && rng() < 0.2) { dmg *= 2; }   // gameplay: crit`);
E(`            if (!e.grudged && e.type !== 'k3' && (e.hitsSurvived >= 2 || Math.random() < 0.25)) {
              e.grudged = true;
              if (!e.name) e.name = genName();
              e.speed *= 1.15;
              chronicle(e.name + ' holds a grudge', '#f66');
              beep(200, 0.15, 'square', 0.03);
            }`,
`            if (!e.grudged && e.type !== 'k3' && (e.hitsSurvived >= 2 || rng() < 0.25)) {   // gameplay: grudge speed buff
              e.grudged = true;
              if (!e.name) e.name = genName();
              e.speed *= 1.15;
              chronicle(e.name + ' holds a grudge', '#f66');
              evlog.push(Object.assign(evt(), { e: 'grudge' }));
              beep(200, 0.15, 'square', 0.03);
            }`);
E(`          if (player.boonChain && Math.random() < 0.3) {`,
`          if (player.boonChain && rng() < 0.3) {   // gameplay: chain lightning`);

// ---- W2: swing can lay a ghost to rest ----
E(`          if (e.hp <= 0) killEnemy(e);
        }
      }
    }
    // a swing near a chandelier cuts the rope — lure them under first`,
`          if (e.hp <= 0) killEnemy(e);
        }
      }
    }
    // the dead can be struck — a ghost at 0 hp rests (no jitter draw, no loot: the dead don't pay)
    for (let i = ghosts.length - 1; i >= 0; i--) {
      const g = ghosts[i];
      const gd = Math.hypot(g.x - player.x, g.y - player.y);
      if (gd < range + g.r) {
        const gang = Math.atan2(g.y - player.y, g.x - player.x);
        let gdiff = gang - player.facing;
        while (gdiff > Math.PI) gdiff -= Math.PI * 2;
        while (gdiff < -Math.PI) gdiff += Math.PI * 2;
        if (Math.abs(gdiff) < arc / 2) {
          g.hp -= playerDmg();
          poof(g.x, g.y, '#aaf', 6);
          if (g.hp <= 0) {
            ghosts.splice(i, 1);
            evlog.push(Object.assign(evt(), { e: 'grest', room: g.room }));
            chronicle('the ghost of ' + g.name + ' rests — "' + g.cause + '" it last said', '#aaf');
            beep(520, 0.3, 'sine', 0.03);
          }
        }
      }
    }
    // a swing near a chandelier cuts the rope — lure them under first`);

// ---- FX4: spitter mine seeded + event ----
E(`      if (lore.traps && Math.random() < Math.min(0.36 * dt, 0.05) && mines.length < 6 && d < 420) {
        mines.push({ x: e.x, y: e.y, arm: 0.8, life: 14 });
      }`,
`      if (lore.traps && rng() < Math.min(0.36 * dt, 0.05) && mines.length < 6 && d < 420) {   // gameplay: mine lay
        mines.push({ x: e.x, y: e.y, arm: 0.8, life: 14 });
        evlog.push(Object.assign(evt(), { e: 'mine' }));
      }`);

// ---- FX4: dodger + whelp + spike seeded ----
E(`        const perp = Math.random() < 0.5 ? 1 : -1;`,
`        const perp = rng() < 0.5 ? 1 : -1;   // gameplay: dodge direction`);
E(`              const a2 = Math.random() * Math.PI * 2;`,
`              const a2 = rng() * Math.PI * 2;   // gameplay: whelp spawn heading`);
E(`    s.phase = (s.phase || Math.random() * 3) + dt;`,
`    s.phase = (s.phase || rng() * 3) + dt;   // gameplay: spike up/down rhythm (decides the bite)`);

// ---- N9 + FX4: the boon draft (max law, seeded, event) ----
E(`    const pool = BOONS.filter(b => !(player.boons || {})[b.id]);`,
`    // N9 max law: stackables (max>1) re-offer below max and leave the pool at max
    const pool = BOONS.filter(b => ((player.boons || {})[b.id] || 0) < (b.max || 1));`);
E(`      let roll = Math.random() * total, idx = 0;`,
`      let roll = rng() * total, idx = 0;   // gameplay: boon draft weighted roll`);
E(`    if (picks.length) { G.boonDraft = picks; addMsg('A GOD OFFERS A BOON — press 1 / 2 / 3', '#8af'); }`,
`    if (picks.length) { G.boonDraft = picks; evlog.push(Object.assign(evt(), { e: 'boons', ids: picks.map(b => b.id) })); addMsg('A GOD OFFERS A BOON — press 1 / 2 / 3', '#8af'); }`);
E(`  // boon draft pick
  if (G.boonDraft) {`,
`  // boon draft pick
  let draftPick = false;
  if (G.boonDraft) {`);
E(`        const b = G.boonDraft[i];
        player.boons = player.boons || {};
        player.boons[b.id] = true;
        b.apply();
        addMsg(b.god + ': ' + b.name + ' — ' + b.desc, b.color);
        beep(880, 0.15, 'triangle', 0.04);
        G.boonDraft = null;
        keys['Digit1_p'] = keys['Digit2_p'] = keys['Digit3_p'] = false;
        break;`,
`        const b = G.boonDraft[i];
        player.boons = player.boons || {};
        player.boons[b.id] = (player.boons[b.id] || 0) + 1;   // N9: counts, so stackables re-offer below max
        b.apply();
        addMsg(b.god + ': ' + b.name + ' — ' + b.desc, b.color);
        beep(880, 0.15, 'triangle', 0.04);
        G.boonDraft = null;
        keys['Digit1_p'] = keys['Digit2_p'] = keys['Digit3_p'] = false;
        draftPick = true;   // N9: the input a boon consumed can never reach the weapon swap
        break;`);
E(`  if (keys['Digit1_p'] && !G.boonDraft) { player.weaponIdx = 0; addMsg('Weapon 1: ' + player.weapons[0].name, RARITY[player.weapons[0].rarity].color); }
  if (keys['Digit2_p'] && !G.boonDraft) { player.weaponIdx = 1; addMsg('Weapon 2: ' + player.weapons[1].name, RARITY[player.weapons[1].rarity].color); }`,
`  if (!draftPick && keys['Digit1_p'] && !G.boonDraft) { player.weaponIdx = 0; addMsg('Weapon 1: ' + player.weapons[0].name, RARITY[player.weapons[0].rarity].color); }
  if (!draftPick && keys['Digit2_p'] && !G.boonDraft) { player.weaponIdx = 1; addMsg('Weapon 2: ' + player.weapons[1].name, RARITY[player.weapons[1].rarity].color); }`);

// ---- FX4: killEnemy seeded + events ----
E(`    if (Math.random() < 0.35) makeLoot(e.x, e.y);`,
`    if (rng() < 0.35) makeLoot(e.x, e.y);   // gameplay: drop table`);
E(`  if (player._riposte > 0 && allies.length < 3 && e.type !== 'boss' && !e.runner && ((window.MUD && window.MUD.forceGhost) || Math.random() < 0.4)) {
    allies.push({ x: e.x, y: e.y, t: 9, ph: Math.random() * 6 });
    chronicle((e.name || 'the fallen') + ' rises grateful — for a moment', '#8af');
  }`,
`  if (player._riposte > 0 && allies.length < 3 && e.type !== 'boss' && !e.runner && ((window.MUD && window.MUD.forceGhost) || rng() < 0.4)) {   // gameplay: ally DPS
    allies.push({ x: e.x, y: e.y, t: 9, ph: Math.random() * 6 });   // ph is render-alpha only — cosmetic
    evlog.push(Object.assign(evt(), { e: 'ghost' }));
    chronicle((e.name || 'the fallen') + ' rises grateful — for a moment', '#8af');
  }`);
E(`    if (o.hp > 0 && !o.aggro && !o.runner && o.mourn == null && Math.hypot(o.x - e.x, o.y - e.y) < 130 && Math.random() < 0.45) o.mourn = 2.2;`,
`    if (o.hp > 0 && !o.aggro && !o.runner && o.mourn == null && Math.hypot(o.x - e.x, o.y - e.y) < 130 && rng() < 0.45) { o.mourn = 2.2; evlog.push(Object.assign(evt(), { e: 'mourn' })); }   // gameplay: mourner rises angry`);
E(`  if (e.type !== 'k3' && Math.random() < 0.09 && superOrbs.length < 2) superOrbs.push({ x: e.x, y: e.y, vx: 0, vy: 0, t: 0 });`,
`  if (e.type !== 'k3' && rng() < 0.09 && superOrbs.length < 2) { superOrbs.push({ x: e.x, y: e.y, vx: 0, vy: 0, t: 0 }); evlog.push(Object.assign(evt(), { e: 'superorb' })); }   // gameplay: SUPERHOT window
  evlog.push(Object.assign(evt(), { e: 'kill', k: e.type }));`);

// ---- FX4: cascade events + k3 scatter seeded ----
E(`  if (kind === 'k8') {
    const n = 8 + a;`,
`  if (kind === 'k8') {
    const n = 8 + a;
    evlog.push(Object.assign(evt(), { e: 'cascade', k: kind, n }));`);
E(`  } else if (kind === 'k3') {
    const n = 16 + 2 * a;
    for (let i = 0; i < n; i++) {
      const ang = (i / n) * Math.PI * 2 + Math.random() * 0.3;`,
`  } else if (kind === 'k3') {
    const n = 16 + 2 * a;
    evlog.push(Object.assign(evt(), { e: 'cascade', k: kind, n }));
    for (let i = 0; i < n; i++) {
      const ang = (i / n) * Math.PI * 2 + rng() * 0.3;   // gameplay: spark scatter heading`);

// ---- FX4: poof + camera shake off the stream ----
E(`function poof(x,y,color,n=12) {
  for (let i=0;i<n;i++) {
    const a = Math.random()*Math.PI*2;
    const s = rnd(30,120);
    particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:rnd(0.3,0.7),max:0.7,color,r:rnd(2,5)});
  }
}`,
`function poof(x,y,color,n=12) {
  for (let i=0;i<n;i++) {
    const a = Math.random()*Math.PI*2;   // cosmetic: particles render and die, never read back
    const s = crnd(30,120);
    particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:crnd(0.3,0.7),max:0.7,color,r:crnd(2,5)});
  }
}`);
E(`  const shakeX = G.shake > 0 ? rnd(-G.shake,G.shake) : 0;
  const shakeY = G.shake > 0 ? rnd(-G.shake,G.shake) : 0;`,
`  const shakeX = G.shake > 0 ? crnd(-G.shake,G.shake) : 0;   // cosmetic: screen-space only, off the stream
  const shakeY = G.shake > 0 ? crnd(-G.shake,G.shake) : 0;`);

// ---- W2: hurtPlayer killer attribution ----
E(`function hurtPlayer(dmg) {
  if (player.iframes > 0) return;
  player.hp -= dmg;`,
`function hurtPlayer(dmg, src) {
  if (player.iframes > 0) return;
  if (src) player.lastHit = src;   // BONES law: the killing blow remembers what dealt it
  player.hp -= dmg;`);

// ---- W2: cause strings at every hurt site ----
E(`if (Math.hypot(player.x - ch.x, ch.y === undefined) && false) {}`, `@@SKIP@@`); // placeholder never matches (skipped by filter below)
edits.pop();
E(`if (Math.hypot(player.x - ch.x, player.y - ch.y) < 70) hurtPlayer(22);`,
`if (Math.hypot(player.x - ch.x, player.y - ch.y) < 70) hurtPlayer(22, 'a falling chandelier');`);
E(`            } else hurtPlayer(e.dmg);`,
`            } else hurtPlayer(e.dmg, e.name || 'a ' + e.type);`);
E(`          hurtPlayer(e.dmg * back);`,
`          hurtPlayer(e.dmg * back, (e.name || 'a rogue') + (back === 2 ? '\u2019s backstab' : ''));`);
E(`        hurtPlayer(e.dmg);
        if (player.boonThorns) { e.hp -= 12; e.flash = 0.15; }
        e.attackCd = 0.7;`,
`        hurtPlayer(e.dmg, e.name || 'a ' + e.type);
        if (player.boonThorns) { e.hp -= 12; e.flash = 0.15; }
        e.attackCd = 0.7;`);
E(`          hurtPlayer(e.dmg);
          e.attackCd = 0.8;`,
`          hurtPlayer(e.dmg, 'the dragon');
          e.attackCd = 0.8;`);
E(`      if (player.iframes <= 0) hurtPlayer(p.dmg);`,
`      if (player.iframes <= 0) hurtPlayer(p.dmg, p.trap ? 'a dart plate' : 'a bolt from the dark');`);
E(`      hurtPlayer(16);`,
`      hurtPlayer(16, 'a floor mine');`);
E(`        if (Math.hypot(player.x - f.x, player.y - f.y) < f.r) hurtPlayer(20);`,
`        if (Math.hypot(player.x - f.x, player.y - f.y) < f.r) hurtPlayer(20, 'a fire vent');`);
E(`    if (Math.hypot(player.x - f.x, player.y - f.y) < f.r) hurtPlayer(10 * dt);`,
`    if (Math.hypot(player.x - f.x, player.y - f.y) < f.r) hurtPlayer(10 * dt, 'a fire vent');`);
E(`if (s.up && Math.hypot(player.x - s.x, player.y - s.y) < 26 && player.iframes <= 0) { hurtPlayer(12); player.iframes = 0.4; }`,
`if (s.up && Math.hypot(player.x - s.x, player.y - s.y) < 26 && player.iframes <= 0) { hurtPlayer(12, 'a spike trap'); player.iframes = 0.4; }`);
E(`      hurtPlayer(18); player.snared = 1.6;`,
`      hurtPlayer(18, 'a bear trap'); player.snared = 1.6;`);
E(`      if (Math.hypot(player.x - v.x, player.y - v.y) < 46 && player.iframes <= 0) hurtPlayer(14);`,
`      if (Math.hypot(player.x - v.x, player.y - v.y) < 46 && player.iframes <= 0) hurtPlayer(14, 'a forge vent');`);

// ---- FX4: death event + W2: playerDie files the bones ----
E(`function playerDie() {
  G.deaths++;
  player.hasLostSouls = true;`,
`function playerDie() {
  G.deaths++;
  evlog.push(Object.assign(evt(), { e: 'death' }));
  // BONES: this death is filed — a later bearer in this room meets its ghost (machine state, like lore)
  const hs = hardestStat();
  const dRoom = G.curRoom || 'courtyard';
  const dCause = player.lastHit || 'the dark itself';
  bonesWrite({ v: 1, seed: runSeed, room: dRoom, x: Math.round(player.x), y: Math.round(player.y), cause: dCause, name: ME.name, stat: hs.n, statV: hs.v });
  evlog.push(Object.assign(evt(), { e: 'tomb', room: dRoom, c: dCause }));
  player.hasLostSouls = true;`);

// ---- W2: ghostTick in the update loop ----
E(`  roomTick(dt);`,
`  roomTick(dt);
  // the dead of earlier runs: drift, whisper, chill — never kill
  ghostTick(dt);`);

// ---- W5: victory raises the next run's ladder ----
E(`    G.state = 'victory';
    G.victoryTime = G.time;
    beep(660, 0.4, 'sine', 0.06);
    beep(880, 0.6, 'sine', 0.05);`,
`    G.state = 'victory';
    G.victoryTime = G.time;
    ascendForNextRun();   // W5: winning alone raises the NEXT run's ladder
    evlog.push(Object.assign(evt(), { e: 'victory' }));
    beep(660, 0.4, 'sine', 0.06);
    beep(880, 0.6, 'sine', 0.05);`);

// ---- W5: persistAsc + ascendForNextRun; nextLoop refactored ----
E(`function nextLoop() {
  G.ng++;
  try { localStorage.setItem('mud_asc', String(G.ng)); } catch (e) {}`,
`function persistAsc() { try { localStorage.setItem('mud_asc', String(G.ng)); } catch (e) {} }
function ascendForNextRun() { G.ng++; persistAsc(); }   // W5: the ladder the next boot inherits
function nextLoop() {
  G.ng++;
  persistAsc();`);

// ---- FX4+W5+W2: startGame rewrite ----
E(`function startGame() {
  try { G.ng = Math.max(0, parseInt(localStorage.getItem('mud_asc') || '0', 10) || 0); } catch (e) {}
  spawnAllEnemies();
  puzzleReset();
  SIGILS.count = 0; G.naveEverActive = false; G.curRoom = 'courtyard';
  allies.length = 0; trail.length = 0; corpses.length = 0;
  for (const ch of CHANDS) ch.dropped = false;
  for (const bt of BEARTRAPS) { bt.armed = true; bt.rearm = 0; }
  G.shoutCd = 0; G.shoutTxt = null;
  G.time = 0; G.state = 'play';
  G.super = 0; superOrbs.length = 0; mines.length = 0; rewindBuf.length = 0; G.rewindOffer = false;
  if (G.ng > 0) addMsg('ASCENSION ' + Math.min(G.ng, 20) + ' — the dragon remembers you', '#f84');
  beep(220, 0.2, 'sine', 0.05);
}`,
`function startGame(forcedSeed, forcedAsc) {
  // RNG LAW: each run seeds the LCG (auto seed recorded in runSeed); pass forcedSeed to replay a
  // recorded run. Explicit seeds always win; with none, the day's fleet seed (W1A) starts the world.
  // ASCENSION LAW (W5): ascension is part of run identity — startGame(seed, asc) pins the ladder
  // for replays; with no forcedAsc the persisted ladder (mud_asc) is the difficulty source.
  ++runN;
  seedRun(forcedSeed!==undefined?((forcedSeed>>>0)||1):FLEET_SEED);
  evlog.length = 0;
  // toy start() law (FX4): a new run resets the actors — same seed + same inputs → same run.
  // (lore and the bones pool are deliberately NOT reset: machine state — they learn/haunt across runs.)
  Object.assign(player, {
    x: 200, y: 1050, vx: 0, vy: 0, respawnX: 200, respawnY: 1080,
    hp: 100, maxHp: 100, stamina: 100, maxStamina: 100, staminaRegen: 25, speed: 200,
    facing: 0, attackT: 0, attackCd: 0, rollT: 0, rollCd: 0, rollDir: { x: 0, y: 0 },
    iframes: 0, snared: 0, xp: 0, xpNext: 20, level: 1, statPoints: 0,
    might: 0, vigor: 0, swiftness: 0, souls: 0, soulsLost: 0, soulsLostX: 0, soulsLostY: 0,
    hasLostSouls: false, soulsDecayT: 0, weaponIdx: 0, lifeOnKill: 0, bonusSpeed: 0, hitFlash: 0, lastHit: null,
    _riposte: 0, _rwUsed: false,
    weapons: [
      { name: 'Rusty Sword', dmg: 12, speed: 1.0, rarity: 0 },
      { name: 'Short Blade', dmg: 8, speed: 1.3, rarity: 0 },
    ],
    boons: null,
  });
  for (const k of Object.keys(player)) if (k.startsWith('boon')) delete player[k];
  G.deaths = 0; G.shake = 0; G.hitStop = 0; G.msgT = 0; G.msg = ''; G.msgColor = undefined;
  G.superBonus = 0; G.boonDraft = null;
  for (const s of SPIKES) { s.phase = 0; s.up = false; }   // spike rhythm re-derives from the run seed
  if (forcedAsc !== undefined) G.ng = Math.max(0, forcedAsc | 0);   // replay pin: seed + ascension = run identity
  else try { G.ng = Math.max(0, parseInt(localStorage.getItem('mud_asc') || '0', 10) || 0); } catch (e) {}
  spawnAllEnemies();
  puzzleReset();
  evlog.push({ t: 0, e: 'run', seed: runSeed, asc: G.ng, key: puzzle.key ? [puzzle.key.x, puzzle.key.y] : null, chest: puzzle.chest ? [puzzle.chest.x, puzzle.chest.y] : null });   // replay receipt: seed + ascension + seeded placement
  SIGILS.count = 0; G.naveEverActive = false; G.curRoom = 'courtyard';
  allies.length = 0; trail.length = 0; corpses.length = 0; ghosts.length = 0;   // the dead rest between runs; the bones pool (machine state, like lore) persists
  for (const ch of CHANDS) ch.dropped = false;
  for (const bt of BEARTRAPS) { bt.armed = true; bt.rearm = 0; }
  G.shoutCd = 0; G.shoutTxt = null;
  G.time = 0; G.state = 'play';
  G.super = 0; superOrbs.length = 0; mines.length = 0; rewindBuf.length = 0; G.rewindOffer = false;
  if (G.ng > 0) addMsg('ASCENSION ' + Math.min(G.ng, 20) + ' — the dragon remembers you', '#f84');
  beep(220, 0.2, 'sine', 0.05);
}`);

// ---- FX4+W5+N12+W2: handle additions ----
E(`get VENTS() { return VENTS; }, forceBell: false, forceGhost: false, fleetDate: FLEET_DATE, get fleetSeed() { return FLEET_SEED; }, fleetSeedOf, puzzleReset, syncDoors, keys, startGame, addMsg, nextLoop, spawnEnemy, spawnCascade, loreUnlock, stepUpdate: update,`,
`get VENTS() { return VENTS; }, get lootDrops() { return lootDrops; }, get fireZones() { return fireZones; }, get deathClouds() { return deathClouds; }, get ghosts() { return ghosts; }, get bones() { return bones; }, get evlog() { return evlog; }, get runSeed() { return runSeed; }, get lcg() { return lcg; }, seedRun, forceBell: false, forceGhost: false, forceBones: false, bonesWrite, bonesSave, hurtPlayer, ascendForNextRun, persistAsc, makeLoot, fleetDate: FLEET_DATE, get fleetSeed() { return FLEET_SEED; }, fleetSeedOf, puzzleReset, syncDoors, keys, startGame, addMsg, nextLoop, spawnEnemy, spawnCascade, loreUnlock, stepUpdate: update,`);

// ---- W2: ghost render after the allies loop ----
E(`  for (const a of allies) {
    ctx.globalAlpha = 0.35 + 0.2 * Math.sin(a.ph * 8);
    ctx.fillStyle = '#8cf';
    ctx.beginPath(); ctx.arc(a.x, a.y, 9, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;
  }`,
`  for (const a of allies) {
    ctx.globalAlpha = 0.35 + 0.2 * Math.sin(a.ph * 8);
    ctx.fillStyle = '#8cf';
    ctx.beginPath(); ctx.arc(a.x, a.y, 9, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;
  }
  // bones ghosts — the dead of earlier runs, still walking their room (cannot kill; can be laid to rest)
  for (const g of ghosts) {
    ctx.globalAlpha = 0.28 + 0.1 * Math.sin(G.time * 2.2 + g.ph);
    ctx.fillStyle = '#aac';
    ctx.beginPath(); ctx.arc(g.x, g.y, g.r + Math.sin(G.time * 3 + g.ph) * 1.5, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 0.6;
    ctx.fillStyle = '#99a';
    ctx.font = '7px monospace'; ctx.textAlign = 'center';
    ctx.fillText(g.name, g.x, g.y - g.r - 6);
    ctx.globalAlpha = 1;
  }`);

let i = 0;
for (const [oldS, newS] of edits) {
  i++;
  const parts = c.split(oldS);
  if (parts.length !== 2) {
    console.error('ABORT: anchor ' + i + ' matched ' + (parts.length - 1) + ' times (want exactly 1): ' + JSON.stringify(oldS.slice(0, 90)));
    process.exit(1);
  }
  c = parts[0] + newS + parts[1];
}
fs.writeFileSync(F, c);
console.log('applied ' + edits.length + '/' + edits.length + ' edits atomically');
for (const k of ['function seedRun', 'const evlog', 'const SAFE_STORE', 'function bonesWrite', 'function spawnGhost', 'function ghostTick', 'function ghostToughness', "e: 'tomb'", "e: 'bones'", "e: 'whisper'", "e: 'grest'", "e: 'victory'", "e: 'boons'", "e: 'cascade'", "e: 'kill'", "e: 'champion'", 'forceBones', 'get ghosts()', 'get bones()', 'get evlog()', 'get runSeed()', 'get lcg()', 'lastHit', 'draftPick', 'persistAsc', 'ascendForNextRun', 'gate:true', 'crnd(-G.shake', 'get lootDrops()', 'forcedAsc', 'FLEET_SEED)']) {
  const n = c.split(k).length - 1;
  if (n === 0) { console.error('ABORT POST: missing ' + k); process.exit(1); }
  console.log('  ok ' + k + ' x' + n);
}
const stray = c.split('Math.random()').length - 1;
console.log('Math.random() sites remaining (cosmetic-allowed set): ' + stray);
