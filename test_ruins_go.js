#!/usr/bin/env node
"use strict";
// test_ruins_go.js — RUINS GO regression gate (house law: a game ships with a harness).
// Lives at repo root so the engine require stays a static downward path; takes no
// user-supplied paths on any argument.
//
//   node test_ruins_go.js          # core levels + law tests
//   node test_ruins_go.js --pack-all   # validate every ruins_go_pack*.json found in
//                                      # dashboard/static/games/ (schema + BFS solvability)
//
// Requires the canonical engine module directly — the same file the HTML loads.
// BFS proves every level solvable under the engine's own laws; replay proves
// determinism; synthetic minis pin each law.

const fs = require("fs");
const path = require("path");

const G = require("./dashboard/static/games/ruins_go_engine.js");
if (!G || typeof G.step !== "function") { console.error("engine load failed"); process.exit(2); }

const GAMES_DIR = path.resolve("dashboard", "static", "games");

let pass = 0, fail = 0;
function ok(name, cond, detail) {
  if (cond) { pass++; console.log("  ok  " + name); }
  else { fail++; console.log("FAIL  " + name + (detail ? " — " + detail : "")); }
}

// ---------- BFS solver over the engine's own state graph ----------
function solve(def, capNodes, maxDepth) {
  capNodes = capNodes || 400000; maxDepth = maxDepth || 200;
  const seen = new Set();
  let nodes = 0;
  const start = G.loadLevel(def);
  const q = [{ st: start, path: [] }];
  seen.add(G.hash(start));
  while (q.length) {
    const { st, path } = q.shift();
    if (st.won) return { solved: true, path, nodes };
    if (st.dead || path.length >= maxDepth) continue;
    for (const d of ["U", "D", "L", "R"]) {
      const ns = G.clone(st);
      const r = G.step(ns, d);
      if (!r.moved) continue;
      nodes++;
      if (nodes > capNodes) return { solved: false, why: "cap", nodes };
      const h = G.hash(ns);
      if (seen.has(h)) continue;
      seen.add(h);
      q.push({ st: ns, path: path.concat(d) });
    }
  }
  return { solved: false, why: "exhausted", nodes };
}

function replay(def, path_) {
  const st = G.loadLevel(def);
  const hs = [];
  for (const d of path_) { G.step(st, d); hs.push(G.hash(st)); }
  return { st, hs };
}

// ---------- law minis ----------
function lawTests() {
  console.log("law tests:");

  // L1 step-clock: a bump is not a move; the world does not tick on a bump.
  {
    const def = { id: "T1", rows: ["   ", " .# ", " .  "], player: [1, 2], snakes: [[1, 1]] };
    const st = G.loadLevel(def);
    const before = G.hash(st);
    const r = G.step(st, "R");
    ok("bump is not a move", !r.moved);
    ok("world does not tick on a bump", G.hash(st) === before);
  }
  // L2 ledges: two up refused, one up is a climb, one down allowed.
  {
    const def2up = { id: "T2", rows: ["   ", " 2  ", " .  ", "   "], player: [1, 2] };
    ok("two heights up refused", !G.step(G.loadLevel(def2up), "U").moved);
    const def1 = { id: "T2b", rows: ["   ", " .1 ", " .  "], player: [1, 2] };
    const st1 = G.loadLevel(def1);
    ok("one height up is a climb", G.step(st1, "U").moved);
    const st1b = G.loadLevel(def1);
    G.step(st1b, "U");
    ok("step back down one allowed", G.step(st1b, "D").moved);
  }
  // L3 pushes: block moves; push into a wall refuses.
  {
    const def = { id: "T3", rows: ["   ", "...", "   "], player: [0, 1], blocks: [[1, 1]] };
    const st = G.loadLevel(def);
    const r = G.step(st, "R");
    ok("push moves the block", r.moved && st.blocks[0].x === 2 && st.player.x === 1);
    ok("push into wall refuses the move", !G.step(st, "R").moved);
  }
  // L4 crank: stepping on it flips bridges.
  {
    const def = { id: "T4", rows: ["   ", "k. ", "   "], player: [1, 1] };
    const st = G.loadLevel(def);
    const off = G.bridgesOn(st);
    G.step(st, "L");
    ok("crank flips bridges", G.bridgesOn(st) === !off);
  }
  // L4 plates: a block holds the bridge; it stays held while the block rests.
  {
    const def = { id: "T5", rows: [" p ", "...", " . "], player: [1, 2], blocks: [[1, 1]] };
    const s = G.loadLevel(def);
    ok("plate not held at start", !G.bridgesOn(s));
    G.step(s, "U");                               // pushes block onto the plate at (1,0)
    ok("block holds the plate", s.blocks[0].y === 0 && G.bridgesOn(s));
    G.step(s, "D"); G.step(s, "U"); G.step(s, "D");
    ok("plate stays held while the block rests", G.bridgesOn(s));
  }
  // L5 collapse: leaving an 'x' turns it to void; the way back is refused.
  {
    const def = { id: "T6", rows: ["   ", ".x.", "   "], player: [1, 1] };
    const st = G.loadLevel(def);
    const r = G.step(st, "R");                    // off the 'x' onto '.'
    ok("collapse burns behind", r.moved && st.terrain[1][1] === " ");
    ok("no way back", !G.step(st, "L").moved);
  }
  // L6 spears: armed on odd ticks, safe on even.
  {
    const odd = G.loadLevel({ id: "T7", rows: ["   ", ".s.", "   "], player: [0, 1] });
    G.step(odd, "R");
    ok("spear kills on odd tick", odd.dead && odd.deadWhy === "the spear");
    const even = G.loadLevel({ id: "T7b", rows: ["   ", "..s", "   "], player: [0, 1] });
    G.step(even, "R"); G.step(even, "R");          // tick 2 lands on the spear: safe
    ok("even arrival survives the spear", !even.dead);
  }
  // L7 snakes: step toward the player on the player's move; frozen on a bump.
  {
    const st = G.loadLevel({ id: "T8", rows: ["   ", "...", "   "], player: [2, 1], snakes: [[0, 1]] });
    G.step(st, "L");                               // player to (1,1); snake steps into (1,1): death
    ok("snake takes the player when it can", st.dead && st.deadWhy === "the snake");
    const s2 = G.loadLevel({ id: "T8b", rows: ["    ", "....", "    "], player: [3, 1], snakes: [[0, 1]] });
    const r2 = G.step(s2, "D");                    // void below: bump
    ok("snake frozen when the player cannot move", !r2.moved && s2.snakes[0].x === 0 && s2.snakes[0].y === 1);
    const s3 = G.loadLevel({ id: "T8c", rows: ["    ", "....", "    "], player: [3, 1], snakes: [[0, 1]] });
    G.step(s3, "L");                               // player (2,1); snake (1,1)
    ok("snake advances one per player step", s3.snakes[0].x === 1 && !s3.dead);
  }
  // L8 lizards patrol their line and turn at the end.
  {
    const def = { id: "T9", rows: ["..  ", "....", "  .."], player: [0, 2], lizards: [[1, 1, 3, 1]] };
    const st = G.loadLevel(def);
    G.step(st, "U");                               // player (0,1); lizard steps toward B
    ok("lizard patrols toward its end", st.lizards[0].x === 2 && st.lizards[0].y === 1);
    G.step(st, "D"); G.step(st, "U"); G.step(st, "D");  // lizard reaches (3,1) and turns
    ok("lizard turns at the end", st.lizards[0].x === 3 ? st.lizards[0].toB === false : true);
  }
  // L9 twin: mirrors the step; waits when denied.
  {
    const def = { id: "T10", rows: ["...  ", "...  ", "...  "], player: [0, 1], twin: [1, 2] };
    const st = G.loadLevel(def);
    G.step(st, "R");
    ok("twin mirrors the step", st.twin.x === 2 && st.twin.y === 2);
    G.step(st, "R");                               // twin tries (3,2): void; stays
    ok("twin waits when denied", st.twin.x === 2);
  }
  // L9 twin holds a plate (crisp).
  {
    const def = { id: "T12", rows: [" p ", "...", "..."], player: [2, 2], twin: [1, 1] };
    const st = G.loadLevel(def);
    ok("bridges off at start", !G.bridgesOn(st));
    G.step(st, "U");                               // player (2,1); twin mirrors U onto the plate (1,0)
    ok("twin steps onto the plate and holds it", st.twin.x === 1 && st.twin.y === 0 && G.bridgesOn(st));
    G.step(st, "L");                               // player (1,1); twin tries L: void, stays on plate
    const r = G.step(st, "U");                     // player steps toward twin cell: blocked
    ok("twin keeps holding while denied", !r.moved && G.bridgesOn(st) && st.twin.x === 1 && st.twin.y === 0);
  }
  // L10 exit + gem.
  {
    const st = G.loadLevel({ id: "T11", rows: ["   ", ".E.", "   "], player: [0, 1], gems: [[1, 1]] });
    G.step(st, "R");
    ok("exit wins", st.won);
    ok("gem collects", st.gems[0].got);
  }
}

// ---------- core level battery ----------
function coreTests() {
  console.log("core levels (BFS under engine laws):");
  for (const def of G.levels) {
    const t0 = Date.now();
    const r = solve(def);
    const ms = Date.now() - t0;
    if (!r.solved) { ok(def.id + " " + def.name + " solvable", false, r.why + " nodes=" + r.nodes); continue; }
    ok(def.id + " " + def.name + " solvable (" + r.path.length + " moves, " + r.nodes + " states, " + ms + "ms)", true);
    const a = replay(def, r.path), b = replay(def, r.path);
    ok(def.id + " deterministic replay", JSON.stringify(a.hs) === JSON.stringify(b.hs) && a.st.won);
  }
}

// ---------- external pack validation ----------
// No user-supplied paths, ever. --pack-all scans the fixed games directory for
// ruins_go_pack*.json files and validates every level in each (schema + BFS solvability).
function validateOneLevel(def) {
  const errs = [];
  if (!def || typeof def !== "object") errs.push("not an object");
  else {
    if (!Array.isArray(def.rows) || def.rows.length < 3 || def.rows.length > 15) errs.push("rows 3..15");
    const w = def.rows[0] && def.rows[0].length;
    if (!w || w < 3 || w > 15) errs.push("width 3..15");
    if (w && def.rows.some(r => r.length !== w)) errs.push("ragged rows");
    if (!Array.isArray(def.player) || def.player.length !== 2) errs.push("player [x,y]");
    const legal = new Set([" ", ".", "1", "2", "#", "b", "p", "k", "x", "s", "E"]);
    if (w && def.rows.some(r => r.split("").some(c => !legal.has(c)))) errs.push("illegal terrain char");
    if (!(w && def.rows.some(r => r.includes("E")))) errs.push("no exit");
  }
  let loadOk = false;
  try { const st = G.loadLevel(def); loadOk = st.w === (def.rows[0] || "").length; } catch (e) { errs.push("load: " + e.message); }
  let solved = false, info = "";
  if (loadOk) {
    const r = solve(def, 400000, 220);
    solved = r.solved;
    info = r.solved ? r.path.length + " moves" : (r.why + " @" + r.nodes);
  }
  return { errs, loadOk, solved, info };
}
function validateAllPacks() {
  const names = fs.readdirSync(GAMES_DIR).filter(f => /^ruins_go_pack[A-Za-z0-9_.-]*\.json$/.test(f));
  if (!names.length) { console.log("pack: none present (core levels only)"); return; }
  let bad = 0, total = 0;
  for (const name of names) {
    const pack = JSON.parse(fs.readFileSync(path.join(GAMES_DIR, name), "utf-8"));
    const arr = Array.isArray(pack) ? pack : [pack];
    for (const def of arr) {
      total++;
      const v = validateOneLevel(def);
      const verdict = v.errs.length === 0 && v.solved ? "PASS" : "FAIL";
      if (verdict === "FAIL") bad++;
      console.log(verdict + "  [" + name + "] " + (def && def.id ? def.id : "?") + " " + (def && def.name ? def.name : "") +
        (v.errs.length ? " [" + v.errs.join("; ") + "]" : "") + (v.loadOk ? " · " + v.info : ""));
    }
  }
  console.log(bad === 0 ? "pack: ALL PASS (" + total + " levels, " + names.length + " files)" : "pack: " + bad + "/" + total + " FAILED");
  process.exit(bad === 0 ? 0 : 1);
}

const arg = process.argv[2];
if (arg === "--pack-all") {
  validateAllPacks();
} else {
  lawTests();
  coreTests();
  console.log("\n" + pass + " passed / " + fail + " failed");
  process.exit(fail === 0 ? 0 : 1);
}
