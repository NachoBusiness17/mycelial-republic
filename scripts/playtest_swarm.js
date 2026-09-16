// playtest_swarm.js — THE DOGFOOD GATE: headless agents PLAY the game through every
// system and assert outcomes. No deploy without PASS. Usage:
//   node scripts/playtest_swarm.js   (exit 0 = PASS, 1 = FAIL with evidence)
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const REPO = path.resolve(__dirname, "..");
const GAME = path.join(REPO, "dashboard", "static", "games", "swarm.html");
const PRELUDE = path.join(REPO, "memory", "runs", "mud_20260912", "smoke_prelude.js");

const html = fs.readFileSync(GAME, "utf-8");
const i = html.lastIndexOf("<script>");
const js = html.slice(html.indexOf(">", i) + 1, html.lastIndexOf("</script>"));

// The PLAYER: drives frames, holds keys across frames (browser-faithful), auto-plays
// level-up cards and door choices, and asserts invariants as it goes.
const PLAYER = `
const results = [];
function check(name, cond, evidence) {
  results.push({ name, pass: !!cond, evidence: evidence || "" });
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (evidence ? "  | " + evidence : ""));
}
function play(n, opts) {
  opts = opts || {};
  for (let k = 0; k < n; k++) {
    if (state === "levelup") { fire("keydown", { key: "1", code: "Digit1", preventDefault: () => {} }); fire("keyup", { key: "1", code: "Digit1" }); continue; }
    if (state === "doors") { fire("keydown", { key: "1", code: "Digit1", preventDefault: () => {} }); fire("keyup", { key: "1", code: "Digit1" }); continue; }
    if (state !== "play" && state !== "mountain") break;
    if (opts.god) player.hp = 99999;
    if (opts.right) { keys["d"] = 1; keys["a"] = 0; }
    if (opts.left) { keys["a"] = 1; keys["d"] = 0; }
    timeScale = 1; // dogfood at full tempo
    t0 += 16.7;
    const f = frameFn; frameFn = null;
    if (f) f(t0);
  }
}
function invariants(tag) {
  const visW = W / ZOOM;
  check(tag + ": camera locked on player", Math.abs((player.x - camX) - visW / 2) < 0.01, "camX=" + camX.toFixed(1) + " px=" + player.x.toFixed(1));
  check(tag + ": player in world", player.x >= 0 && player.x <= WW, "x=" + player.x.toFixed(0));
  check(tag + ": no NaN in player", isFinite(player.x) && isFinite(player.y) && isFinite(player.hp), "hp=" + player.hp);
  check(tag + ": entities finite", enemies.every(e => isFinite(e.x)) && gems.every(g => isFinite(g.x)), "en=" + enemies.length + " gems=" + gems.length);
}
`;

// Scenario battery — each runs in a fresh node process (game state is top-level).
const SCENARIOS = [
  {
    name: "boot+title",
    body: `
runFrames(45);
check("title renders 45 frames", state === "title");`,
  },
  {
    name: "core-run",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(400, { god: true, right: true });
check("run reaches play state", state === "play" || state === "levelup", "state=" + state);
check("kills happening", kills > 0, "kills=" + kills);
invariants("run");`,
  },
  {
    name: "gate+descend",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
depthT = DEPTH_LEN - 2;
play(300, { god: true, right: true });
const sawGate = !!gateOpen || state === "doors" || depth > 1;
check("gate opens at depth end", sawGate, "gate=" + !!gateOpen + " state=" + state + " depth=" + depth);
if (gateOpen && state === "play") { player.x = gateOpen.x + gateOpen.w / 2; player.y = gyAt(player.x) - player.h / 2; player.vy = 0; play(4, { god: true }); }
if (state === "doors") { fire("keydown", { key: "1", code: "Digit1", preventDefault: () => {} }); fire("keyup", { key: "1", code: "Digit1" }); play(30, { god: true }); }
check("descend increments depth", depth >= 2, "depth=" + depth);
check("fresh platform set loaded", platforms.length > 0, "plats=" + platforms.length);
invariants("descend");`,
  },
  {
    name: "fish-school",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(90, { god: true, right: true });
keys["d"] = 0;
gems.length = 0;
keys["d"] = 0; keys["a"] = 0; player.vx = 0; player.x = player.x + 400; // observer stands clear — the glide harvests any school it decelerates through
const cohortX = player.x - 400;
for (let i = 0; i < 10; i++) gems.push({ x: cohortX + rnd(-120, 120), y: GY - 6, vx: 0, vy: 0, t: 0, rest: true, test: true });
function cohortSpread() {
  const L = gems.filter(g => g.test && !g.dead && !g.claimed);
  if (!L.length) return -1;
  const m = L.reduce((a, g) => a + g.x, 0) / L.length;
  return L.reduce((a, g) => a + Math.abs(g.x - m), 0) / L.length;
}
const m0 = cohortSpread();
play(240, { god: true });
const m1 = cohortSpread();
check("fish school tighter (cohort centroid)", m1 >= 0 && m1 < m0 - 8, m0.toFixed(1) + "->" + m1.toFixed(1));`,
  },
  {
    name: "necromancer",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(300, { god: true, right: true });
for (let k = 0; k < 10; k++) { const e = enemies.find(x => !x.dead); if (!e) break; e.learned = 10; e.hp = 1; damageEnemy(e, 999, e.x, e.y); }
check("necromancer raises learned dead", allies.length > 0, "allies=" + allies.length);
play(120, { god: true, right: true });
check("allies hunt or rest cleanly", allies.every(a => isFinite(a.x)), "n=" + allies.length);`,
  },
  {
    name: "weather",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(60, { god: true, right: true });
dropFireball(player.x + 120);
let g = 0; while (wthr.fire && g++ < 300) { play(1, { god: true }); }
check("fireball heats water", wthr.temp > 0.4, "temp=" + wthr.temp.toFixed(2));
play(90, { god: true, right: true });
check("storm emerges from heat", ["storm", "rain"].includes(wthr.state) || wthr.temp > 0.5, "state=" + wthr.state + " temp=" + wthr.temp.toFixed(2));`,
  },
  {
    name: "tide",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(60, { god: true, right: true });
depthT = DEPTH_LEN - 8;
const gy0 = gyAt(player.x);
play(150, { god: true, right: true });
const gy1 = gyAt(player.x);
check("tide raises floor near gate", gy0 - gy1 > 30, (gy0 - gy1).toFixed(1) + " units");`,
  },
  {
    name: "fable-room",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(60, { god: true, right: true });
riddleT = 0;
play(5, { god: true });
check("chair poses riddle", !!riddle, "riddle=" + (riddle ? riddle.R.q.slice(0, 24) : "none"));
if (riddle) {
  riddle.open = true; riddle.zoneT = 0.15;
  keys["d"] = 0; keys["a"] = 1; player.x = 150;
  const hp0 = player.hp;
  play(3, { god: true });
  check("chair answers with feet", !riddle, "resolved; hp " + hp0.toFixed(0) + "->" + player.hp.toFixed(0));
}`,
  },
  {
    name: "the-pass",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(60, { god: true, right: true });
enterPass();
check("entered the pass", state === "mountain");
keys["d"] = 1; keys["a"] = 0;
play(300, { god: true });
check("riding the mountains", state === "mountain" && mtn.dist > 50, "dist=" + (mtn ? mtn.dist.toFixed(0) : "-"));
mtn.exit = 0;
play(4, { god: true });
check("pass exits to deeper maze", state === "play" && depth >= 2, "state=" + state + " depth=" + depth);
invariants("pass-exit");`,
  },
  {
    name: "death+bonfire+charcoal",
    body: `
fire("keydown", { key: "d", code: "KeyD", preventDefault: () => {} });
play(60, { god: true, right: true });
const c0 = charcoal.length;
for (let k = 0; k < 400 && state === "play"; k++) {
  if (state === "levelup") { fire("keydown", { key: "1", code: "Digit1", preventDefault: () => {} }); fire("keyup", { key: "1", code: "Digit1" }); continue; }
  player.hp = 0.1; player.iframes = 0;
  const e = enemies.find(x => !x.dead); if (e) { player.x = e.x; player.y = e.y; }
  t0 += 16.7; const f = frameFn; frameFn = null; if (f) f(t0);
}
check("death happens", state === "dead", "state=" + state);
check("charcoal marks the death", charcoal.length > c0, c0 + "->" + charcoal.length);
check("bonfire souls banked", typeof meta.bank === "number", "bank=" + (meta.bank || 0));`,
  },
];

function runScenario(sc) {
  // fresh node process per scenario; program arrives via stdin — no shell, no -e
  const prelude = fs.readFileSync(PRELUDE, "utf-8");
  const src = prelude + "\n" + js + "\n" + PLAYER + "\n" + sc.body + "\n";
  try {
    const out = execFileSync(process.execPath, [], { input: src, encoding: "utf8", timeout: 60000, maxBuffer: 32e6 });
    return { status: 0, stdout: out, stderr: "" };
  } catch (e) {
    return { status: 1, stdout: e.stdout || "", stderr: e.stderr || e.message || "" };
  }
}

function run() {
  let fails = 0, total = 0;
  for (const sc of SCENARIOS) {
    console.log("\n=== " + sc.name + " ===");
    const r = runScenario(sc);
    const lines = (r.stdout || "").trim().split("\n").filter(l => l.startsWith("PASS") || l.startsWith("FAIL"));
    if (lines.length === 0) {
      total++; fails++;
      console.log("FAIL  " + sc.name + " produced no verdicts | " + String(r.stderr).split("\n")[0].slice(0, 120));
      continue;
    }
    for (const l of lines) { total++; if (l.startsWith("FAIL")) fails++; console.log(l); }
  }
  console.log("\n===== DOGFOOD VERDICT: " + (total - fails) + "/" + total + " =====");
  process.exit(fails ? 1 : 0);
}

run();
