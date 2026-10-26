"use strict";
// s2-14 playability probe: compile every inline <script> block of each game HTML
// with vm.Script (syntax check only, no execution) and report pass/fail per block.
// Location-independent: resolves the repo root from this file's own path
// (flash50 sits at watch/inbox/burn_reset_20260927/flash50/).
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..", "..", "..", "..");
const GAMES_DIR = path.join(ROOT, "dashboard", "static", "games");
const targets = [
  "arena_operator_field.html",
  "arrakis.html",
  "frontier_souls.html",
  "index.html",
  "maze_arena.html",
  "mud.html",
  "ruins_go.html",
  "skifree.html",
  "swarm.html",
  "toy.html",
  path.join("soul_frontier", "soul_frontier.html"),
  "oracle_dice.js",
  "ruins_go_engine.js",
];

let totalBlocks = 0, failedBlocks = 0;
for (const t of targets) {
  const full = path.join(GAMES_DIR, t);
  const src = fs.readFileSync(full, "utf8");
  let blocks;
  if (t.endsWith(".js")) {
    blocks = [src];
  } else {
    blocks = [];
    const re = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
    let m;
    while ((m = re.exec(src)) !== null) blocks.push(m[1]);
  }
  let ok = 0, bad = 0;
  blocks.forEach((body, i) => {
    if (!body.trim()) return;
    totalBlocks++;
    try {
      new vm.Script(body, { filename: t + "#block" + i });
      ok++;
    } catch (e) {
      failedBlocks++;
      bad++;
      console.log("SYNTAX-FAIL " + t + " block " + i + ": " + e.message);
    }
  });
  console.log(t + " blocks=" + blocks.length + " nonempty-ok=" + ok + " failed=" + bad);
}
console.log("TOTAL blocks=" + totalBlocks + " failed=" + failedBlocks);
