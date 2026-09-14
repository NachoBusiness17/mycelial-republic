// keeper_voice_harness.js — node verification for keeper_voice.html (Knock-out #10)
// Extracts the page JS between //<<JS and //JS>>, syntax-checks it, then:
//   1. generates 3 sample narrations (the-world, law:0, chunk with slab 24-ish)
//   2. emits state/shadow_work/keeper_lines.json (one narration per shadow_walk chunk)
// Usage: node keeper_voice_harness.js
const fs = require("fs"), path = require("path"), vm = require("vm");
const ROOT = path.resolve(__dirname, "..", "..");
const HTML = path.join(__dirname, "keeper_voice.html");
const DATA = path.join(__dirname, "keeper_voice_data.json");
const OUT = path.join(ROOT, "state", "shadow_work", "keeper_lines.json");
const TMP = path.join(__dirname, "_keeper_voice_js.tmp.js");

const html = fs.readFileSync(HTML, "utf8");
const m = html.match(/\/\/<<JS\n([\s\S]*?)\/\/JS>>/);
if (!m) { console.error("FAIL: JS markers not found"); process.exit(1); }
fs.writeFileSync(TMP, m[1]);
const { execFileSync } = require("child_process");
execFileSync(process.execPath, ["--check", TMP], { stdio: "inherit" });
console.log("node --check: PASS");

const eng = require(TMP);
const d = JSON.parse(fs.readFileSync(DATA, "utf8"));
const ts = new Date().toISOString().replace(/\.\d+Z$/, "Z");

// pick a chunk that maps to slab 24 if present, else first with an agg
const c24 = d.chunks.find(c => c.slab_agg && c.slab_agg.slab === 24) || d.chunks.find(c => c.slab_agg);
const samples = [
  { topic: "the-world", lines: eng.narrate(d, "the-world") },
  { topic: "law:0", lines: eng.narrate(d, "law:0") },
  { topic: "chunk:" + c24.id, lines: eng.narrate(d, "chunk:" + c24.id) },
];
for (const s of samples) {
  console.log("\n--- SAMPLE [" + s.topic + "] ---");
  for (const l of s.lines) console.log("  " + l.text + "\n      src: " + l.src);
}

const out = eng.keeperLinesFor(d, ts);
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
fs.unlinkSync(TMP);
console.log("\nkeeper_lines.json: " + out.lines.length + " lines over " + d.chunks.length + " chunks -> " + path.relative(ROOT, OUT));
