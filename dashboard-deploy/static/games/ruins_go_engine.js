"use strict";
// RUINS GO engine v1 — canonical module. The HTML loads this file; tests require it.
// One engine, no inline copies (FX5: canonical flows to derived, never backward).
//
// LAWS (stolen from the -GO line, translated to programming):
//   L1 step-clock: the world ticks exactly when the player displaces. A blocked bump is not a move.
//   L2 ledges: step up or down exactly one height. Two is a fall you cannot take.
//   L3 pushes: blocks move same-height or slide down one; never up; never through anything.
//   L4 cranks flip the bridges; plates hold them while weight (you or a block) remains.
//   L5 thin ledges ('x') collapse to void the moment you leave them. There is no way back.
//   L6 spears arm on odd ticks. Land on them only when the count is even.
//   L7 snakes step toward you once per your step, same height only. They cannot be killed, only denied.
//   L8 lizards patrol their line, turn at the ends or when denied.
//   L9 the other self mirrors your step; denied, it waits. It fears nothing.
//  L10 the exit admits the body that reaches it. Gems are optional sealed bits.
//
// Terrain legend (row strings): ' ' void · '.' floor h0 · '1' h1 · '2' h2 · '#' pillar
//   'b' bridge(h0) · 'p' plate(h0) · 'k' crank(h0) · 'x' collapse(h0) · 's' spear(h0) · 'E' exit(h0)
// Level extras: player [x,y] · blocks [[x,y]] · snakes [[x,y]] · lizards [[ax,ay,bx,by]] ·
//   twin [x,y] (mirrors you) · gems [[x,y]] · hint "" · ins "" (inscription shown on win)

const RUINS_GO_VERSION = "1.0.0";
const DIRS = { U:[0,-1], D:[0,1], L:[-1,0], R:[1,0] };
const FLOOR_H = { ".":0, "1":1, "2":2, "b":0, "p":0, "k":0, "x":0, "s":0, "E":0 };

const CORE_LEVELS = [
{ id:"L01", name:"first steps", chapter:1, ins:"Receipts before work.",
  hint:"Walk. The gem is a sealed bit; the exit does not demand it.",
  rows:["       ",
        "  ...  ",
        " ..... ",
        " ..E.. ",
        " ..... ",
        "  ...  ",
        "       "],
  player:[1,3], gems:[[5,1]] },

{ id:"L02", name:"the ledge", chapter:1, ins:"Canonical flows to derived, never backward.",
  hint:"Step up one height, or down one. Never two.",
  rows:[" 11111 ",
        " 1...1 ",
        " 1.E.1 ",
        " 1...1 ",
        " 11111 ",
        "   .   ",
        "       "],
  player:[3,5], gems:[[1,1]] },

{ id:"L03", name:"the weight", chapter:1, ins:"Two banks, one river, never merged.",
  hint:"Push the block onto the plate. Weight holds what hands cannot.",
  rows:["       ",
        "       ",
        " ...   ",
        " ..pb.E.",
        " ...  . ",
        "       ",
        "       "],
  player:[0,3], blocks:[[1,3]], gems:[[5,4]] },

{ id:"L04", name:"the crank", chapter:1, ins:"A hash by itself does not prove when.",
  hint:"Step onto the crank. It flips every bridge in the room.",
  rows:["       ",
        "       ",
        "  .    ",
        " .kb.E.",
        "  .  . ",
        "       ",
        "       "],
  player:[1,3], gems:[[5,4]] },

{ id:"L05", name:"thin ledges", chapter:1, ins:"The ledger constrains future accounts of the past, not the past itself.",
  hint:"What you leave behind falls. Choose the order of your wanting.",
  rows:["       ",
        "       ",
        "   xx  ",
        " .xxxE.",
        "   x . ",
        "       ",
        "       "],
  player:[1,3], gems:[[3,2]] },

{ id:"L06", name:"the snake", chapter:2, ins:"The keeper calls his own by name.",
  hint:"It steps when you step, and it will not touch the way out. Let it guard the wrong side.",
  rows:["       ",
        " ..... ",
        " . . . ",
        " . E . ",
        " ..... ",
        "       ",
        "       "],
  player:[1,1], snakes:[[5,4]], gems:[[5,1]] },

{ id:"L07", name:"the sentry", chapter:2, ins:"An unexamined no is a silent skip.",
  hint:"The sentry walks its line. Cross at the far end, behind its back.",
  rows:["       ",
        "  ...  ",
        " ..... ",
        " ..... ",
        "     E ",
        "       ",
        "       "],
  player:[1,3], lizards:[[3,3,5,3]], gems:[[4,1]] },

{ id:"L08", name:"the rhythm", chapter:2, ins:"The falsifier constrains the analysis, not the experiment.",
  hint:"Spears arm on odd counts. Land on them only when your count is even.",
  rows:["       ",
        "       ",
        "       ",
        " .s.s.s",
        "     .E",
        "       ",
        "       "],
  player:[0,3], gems:[[6,2]] },

{ id:"L09", name:"the blockade", chapter:2, ins:"Charcoal is free.",
  hint:"A snake cannot be killed. It can be walled off. Feed it a block.",
  rows:["       ",
        "  .E   ",
        " ...   ",
        " ..... ",
        "       ",
        "       ",
        "       "],
  player:[1,3], blocks:[[2,3]], snakes:[[5,3]], gems:[[0,3]] },

{ id:"L10", name:"two rivers", chapter:3, ins:"Trespass is a title that arrived late.",
  hint:"The crank latches every bridge it owns. Cross both; the sealed bit waits above.",
  rows:["       ",
        "  ...  ",
        " .kbbE.",
        "  .    ",
        "       ",
        "       ",
        "       "],
  player:[1,2], gems:[[3,1]] },

{ id:"L11", name:"the other self", chapter:3, ins:"The minimal honest stone commits beforehand to what would make it wrong.",
  hint:"Your mirror walks with you. Deny it, and it waits. It can hold a plate forever.",
  rows:["       ",
        "  ...# ",
        "  ...p ",
        "  ...  ",
        " ...b. ",
        "     E ",
        "       "],
  player:[2,2], twin:[4,2], gems:[[4,1]] },

{ id:"L12", name:"the queen of venom", chapter:4, ins:"The world only moves when you move. It has never moved without you.",
  hint:"They both step toward you, and the ledges fall behind you. Climb, do not circle.",
  rows:["       ",
        " Exxxx ",
        " x.x.x ",
        " x...x ",
        " x.x.x ",
        " xx.xx ",
        "       "],
  player:[3,5], snakes:[[1,4],[5,4]], gems:[[1,2]] },
];

const INSCRIPTIONS = {};
CORE_LEVELS.forEach(l => { INSCRIPTIONS[l.id] = l.ins; });

// --- D&D LAYER v1 (deterministic; seeded rolls so the replay law holds) -----------
// Self-steal provenance: traits ported from mud.html's boon system (thorns/chain/
// berserk/arc/vision); tales carry the tiny-story register; tables grow with the pack.
function mulberry32(a) {
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const MONSTER_TABLE = [
  { n: "Crypt Snake", hp: 2, trait: "thorns" },
  { n: "Barbed Sentry", hp: 1, trait: "berserk" },
  { n: "Ashen Lizard", hp: 1, trait: "arc" },
  { n: "Vault Husk", hp: 3, trait: "vision" },
  { n: "Grim Ferryman", hp: 2, trait: "chain" },
  { n: "Queen's Whelp", hp: 3, trait: "berserk" },
  { n: "Tomb Murmur", hp: 1, trait: "vision" },
  { n: "Venom Acolyte", hp: 2, trait: "arc" },
];
const TRAIT_TEXT = {
  thorns: "touching it costs you your next step",
  berserk: "it moves with an extra hunger",
  arc: "it bends its path at the corners",
  vision: "it remembers where you have been",
  chain: "it drags the room's rhythm",
};
const TALES = [
  "The keeper wrote your name on the door before you arrived.",
  "Somewhere below, a scale is weighing what you leave behind.",
  "The lantern you carry was returned once already.",
  "Every wall here remembers a different thief.",
  "The venom queen counts her rooms like coins.",
  "Two banks of the river never learned the other's name.",
  "A stranger read the ledger aloud and the walls listened.",
  "The charcoal is free. Nothing else is.",
];
function rollStatBlock(defId, seed) {
  const rng = mulberry32(hash32(defId + ":" + (seed || 0)));
  const m = MONSTER_TABLE[Math.floor(rng() * MONSTER_TABLE.length)];
  return {
    monster: m.n, hp: m.hp + Math.floor(rng() * 2), trait: m.trait,
    traitText: TRAIT_TEXT[m.trait],
    note: "rolled for " + defId + " seed " + (seed || 0),
  };
}
function rollTale(defId, seed) {
  const rng = mulberry32(hash32("tale:" + defId + ":" + (seed || 0)));
  return TALES[Math.floor(rng() * TALES.length)];
}
function hash32(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

function clone(o) { return JSON.parse(JSON.stringify(o)); }

function loadLevel(def) {
  const terrain = def.rows.map(r => r.split(""));
  const st = {
    id: def.id, name: def.name || def.id, chapter: def.chapter || 1,
    hint: def.hint || "", ins: def.ins || "",
    w: terrain[0].length, h: terrain.length,
    terrain,
    player: { x: def.player[0], y: def.player[1] },
    blocks: (def.blocks || []).map(b => ({ x: b[0], y: b[1] })),
    snakes: (def.snakes || []).map(s => ({ x: s[0], y: s[1] })),
    lizards: (def.lizards || []).map(l => ({ ax: l[0], ay: l[1], bx: l[2], by: l[3], x: l[0], y: l[1], toB: true })),
    twin: def.twin ? { x: def.twin[0], y: def.twin[1] } : null,
    gems: (def.gems || []).map(g => ({ x: g[0], y: g[1], got: false })),
    crank: false,             // crank flips this; plates hold while weighted
    tick: 0, moves: 0, deaths: 0,
    dead: false, deadWhy: "", won: false,
    log: [],
  };
  return st;
}

function bridgesOn(st) {
  const plateHeld = cellT(st, st.player.x, st.player.y) === "p" ||
                    st.blocks.some(b => cellT(st, b.x, b.y) === "p") ||
                    (st.twin && cellT(st, st.twin.x, st.twin.y) === "p");
  return st.crank || plateHeld;
}

function cellT(st, x, y) {
  if (y < 0 || y >= st.h || x < 0 || x >= st.w) return " ";
  return st.terrain[y][x];
}

function entityAt(st, x, y) {
  if (st.player.x === x && st.player.y === y) return "player";
  if (st.twin && st.twin.x === x && st.twin.y === y) return "twin";
  if (st.blocks.some(b => b.x === x && b.y === y)) return "block";
  if (st.snakes.some(s => s.x === x && s.y === y)) return "snake";
  if (st.lizards.some(l => l.x === x && l.y === y)) return "lizard";
  return null;
}

function walkHeight(t) { return FLOOR_H[t]; }  // undefined for ' ' and '#'

function bridgesOk(t, st) { return t !== "b" || bridgesOn(st); }

// Can `who` stand on (x,y)? who: "player"|"block"|"twin"
function standable(st, x, y, who) {
  const t = cellT(st, x, y);
  const hh = walkHeight(t);
  if (hh === undefined) return false;          // void or pillar
  if (!bridgesOk(t, st)) return false;         // retracted bridge is void to everyone
  if (who === "block" && (t === "k" || t === "E")) return false;  // blocks smash no cranks, sit on no exits
  return true;
}

function kill(st, why) { st.dead = true; st.deadWhy = why; st.deaths++; }

// One attempt. Mutates st. Returns {moved, dead, won, why}.
function step(st, dir) {
  if (st.dead || st.won) return { moved: false, dead: st.dead, won: st.won, why: "over" };
  const [dx, dy] = DIRS[dir] || [0, 0];
  if (!dx && !dy) return { moved: false, dead: false, won: false, why: "baddir" };
  const nx = st.player.x + dx, ny = st.player.y + dy;
  const fromT = cellT(st, st.player.x, st.player.y);
  const fromH = walkHeight(fromT) ?? 0;
  const toT = cellT(st, nx, ny);
  const toH = walkHeight(toT);
  const occupant = entityAt(st, nx, ny);

  // --- L2 ledges / movement ---
  if (toH === undefined || Math.abs(toH - fromH) > 1 || !bridgesOk(toT, st)) {
    return { moved: false, dead: false, won: false, why: "blocked" };   // L1: a bump is not a move
  }
  // --- L3 pushes ---
  if (occupant === "block") {
    const bx = nx + dx, by = ny + dy;
    const bT = cellT(st, bx, by);
    const bH = walkHeight(bT);
    if (bH === undefined || !bridgesOk(bT, st) || bH > toH ||
        entityAt(st, bx, by) || (bT === "k") || (bT === "E")) {
      return { moved: false, dead: false, won: false, why: "blocked" };
    }
    const blk = st.blocks.find(b => b.x === nx && b.y === ny);
    blk.x = bx; blk.y = by;   // slides down one freely (bH <= toH)
  } else if (occupant === "snake") {
    kill(st, "the snake");
    return { moved: false, dead: true, won: false, why: "death" };
  } else if (occupant === "lizard") {
    kill(st, "the sentry");
    return { moved: false, dead: true, won: false, why: "death" };
  } else if (occupant === "twin") {
    return { moved: false, dead: false, won: false, why: "blocked" };
  }

  // --- move ---
  if (fromT === "x") st.terrain[st.player.y][st.player.x] = " ";       // L5 collapse behind
  st.player.x = nx; st.player.y = ny;
  st.moves++; st.tick++;
  st.log.push(dir);
  if (toT === "k") st.crank = !st.crank;                                // L4 crank flips
  const g = st.gems.find(g => !g.got && g.x === nx && g.y === ny);
  if (g) g.got = true;                                                  // L10 sealed bit
  if (toT === "s" && st.tick % 2 === 1) { kill(st, "the spear"); return { moved: true, dead: true, won: false, why: "spear" }; }
  if (toT === "E") { st.won = true; return { moved: true, dead: false, won: true, why: "exit" }; }

  // --- L9 the other self ---
  if (st.twin) {
    const t2 = { x: st.twin.x + dx, y: st.twin.y + dy };
    const twT = cellT(st, t2.x, t2.y);
    const twH = walkHeight(twT);
    const tH = walkHeight(cellT(st, st.twin.x, st.twin.y)) ?? 0;
    const free = twH !== undefined && Math.abs(twH - tH) <= 1 && bridgesOk(twT, st) &&
                 !entityAt(st, t2.x, t2.y);
    if (free) { st.twin.x = t2.x; st.twin.y = t2.y; }
  }

  // --- L7 snakes (traits: vision → pathfind toward player's most-visited cell) ---
  for (const s of st.snakes) {
    const sH = walkHeight(cellT(st, s.x, s.y)) ?? 0;
    const cand = [];
    const sb = st.sb || {};
    if (sb.trait === "vision") {
      // pathfind: prefer the axis of greatest distance, but break ties toward
      // the player's start cell (where they've been)
      const ddx = st.player.x - s.x, ddy = st.player.y - s.y;
      const sx0 = def.player ? def.player[0] : st.player.x;
      const sy0 = def.player ? def.player[1] : st.player.y;
      const sdx = sx0 - s.x, sdy = sy0 - s.y;
      if (Math.abs(sdx) + Math.abs(sdy) > Math.abs(ddx) + Math.abs(ddy)) {
        if (Math.abs(sdx) >= Math.abs(sdy)) { if (sdx) cand.push([Math.sign(sdx), 0]); if (sdy) cand.push([0, Math.sign(sdy)]); }
        else { if (sdy) cand.push([0, Math.sign(sdy)]); if (sdx) cand.push([Math.sign(sdx), 0]); }
      } else {
        if (Math.abs(ddx) >= Math.abs(ddy)) { if (ddx) cand.push([Math.sign(ddx), 0]); if (ddy) cand.push([0, Math.sign(ddy)]); }
        else { if (ddy) cand.push([0, Math.sign(ddy)]); if (ddx) cand.push([Math.sign(ddx), 0]); }
      }
    } else {
      const ddx = st.player.x - s.x, ddy = st.player.y - s.y;
      if (Math.abs(ddx) >= Math.abs(ddy)) { if (ddx) cand.push([Math.sign(ddx), 0]); if (ddy) cand.push([0, Math.sign(ddy)]); }
      else { if (ddy) cand.push([0, Math.sign(ddy)]); if (ddx) cand.push([Math.sign(ddx), 0]); }
    }
    for (const [cx, cy] of cand) {
      const tx = s.x + cx, ty = s.y + cy;
      const t = cellT(st, tx, ty);
      const h = walkHeight(t);
      const occ = entityAt(st, tx, ty);
      if (h !== undefined && h === sH && bridgesOk(t, st) && (occ === "player" || occ === null)) {
        if (occ === "player") { kill(st, "the snake"); break; }
        if (t === "k" || t === "E") continue;
        s.x = tx; s.y = ty; break;
      }
    }
    if (st.dead) break;
  }
  if (st.dead) return { moved: true, dead: true, won: false, why: "snake" };

  // --- L8 lizards (traits: berserk → moves twice per player step) ---
  for (const l of st.lizards) {
    const lSteps = (st.sb && st.sb.trait === "berserk") ? 2 : 1;
    for (let li = 0; li < lSteps; li++) {
      const gx = l.toB ? l.bx : l.ax, gy = l.toB ? l.by : l.ay;
      const dx2 = Math.sign(gx - l.x), dy2 = Math.sign(gy - l.y);
      const tx = l.x + dx2, ty = l.y + dy2;
      if (dx2 === 0 && dy2 === 0) { l.toB = !l.toB; continue; }
      const occ = entityAt(st, tx, ty);
      const t = cellT(st, tx, ty);
      const lh = walkHeight(cellT(st, l.x, l.y)) ?? 0;
      const th = walkHeight(t);
      if (occ === "player" && th !== undefined && th === lh) { kill(st, "the sentry"); break; }
      if (th === undefined || th !== lh || (occ && occ !== "player")) { l.toB = !l.toB; }
      else { l.x = tx; l.y = ty; if (l.x === gx && l.y === gy) l.toB = !l.toB; }
      if (st.dead) break;
    }
    if (st.dead) break;
  }
  if (st.dead) return { moved: true, dead: true, won: false, why: "lizard" };

  return { moved: true, dead: false, won: false, why: "ok" };
}

function hash(st) {
  return JSON.stringify([st.terrain, [st.player.x, st.player.y],
    st.blocks.map(b => [b.x, b.y]).sort(),
    st.snakes.map(s => [s.x, s.y]).sort(),
    st.lizards.map(l => [l.x, l.y, l.toB ? 1 : 0]).sort(),
    st.twin ? [st.twin.x, st.twin.y] : null,
    st.crank, st.tick % 2, st.dead, st.won]);
}

const RUINS_GO = {
  version: RUINS_GO_VERSION, levels: CORE_LEVELS, loadLevel, step, hash, clone,
  bridgesOn, cellT, walkHeight, standable, entityAt, INSCRIPTIONS, DIRS,
  rollStatBlock, rollTale, mulberry32, MONSTER_TABLE, TRAIT_TEXT, TALES,
};
if (typeof window !== "undefined") window.RUINS_GO = RUINS_GO;
if (typeof module !== "undefined" && module.exports) module.exports = RUINS_GO;
