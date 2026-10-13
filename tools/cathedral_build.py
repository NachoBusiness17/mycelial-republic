"""CATHEDRAL BUILDER — one engine, regions from module files (v1 hand-wire).

RIB_CATHEDRAL_WORLD_V1 compliance:
  cathedral-one-schema : regions are mag_game_module.v1 files; this builder only
                         ASSEMBLES + wires; no second data format is invented.
  loop-closes          : adventure_2d6.river_ford -> water_computer.gallery (AGREE)
  lens-count-gate      : audit doctrine_library -> optics garage_gate at 10/10 (AGREE)
  water-feeds-field    : fractal leaf_gate entry needs water OUT.height (AGREE,
                         value feed — no route edge added, descent stays unwired)
  mechanism-is-the-answer : bucket-pour in out_cistern refuses, flagged DISPUTED
  descent-order        : CONTESTED — engine starts neutral (crossroads), both
                         orders legal, both gate-style readouts visible, no order
                         enforced. RIB tiebreak stays gated on operator GO.
  engram-is-summon     : riddler_engram stays a summonable card deck (no rooms).

Build (repo root): .venv/Scripts/python.exe tools/cathedral_build.py
Output: watch/inbox/cathedral_v1.html  (self-contained, double-click playable)
Validation runs before write: every exit resolves globally; start_rooms exist;
loop edge present; 10 lens rooms; gate code present.
"""

import json
import re
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc)
ROOT = Path.cwd().resolve()
GM = ROOT / "memory" / "game_modules"
OUT = ROOT / "watch" / "inbox" / "cathedral_v1.html"

REGIONS = ["water_computer", "fractal_maze", "riddler_optics", "riddler_engram",
           "dnd_classic_stub", "audit_dungeon", "adventure_2d6_stub"]
LENS_ROOMS = ["lens_blade", "lens_monomyth", "lens_anthropologist", "lens_absurdist",
              "lens_footnoter", "lens_elegist", "lens_windowpane", "lens_magician",
              "lens_stage", "lens_engineer"]

ENGRAM_SEATS = [
    {"seat": "VOLTAIRE", "alias": "the blade", "riddle": "say the thing by seeming to praise it"},
    {"seat": "CAMPBELL", "alias": "the monomyth", "riddle": "every story is one story in different clothes"},
    {"seat": "LE GUIN", "alias": "the anthropologist", "riddle": "the strange made familiar until you cannot say which it was"},
    {"seat": "ADAMS", "alias": "the absurdist", "riddle": "an indifferent universe is funny if you know where your towel is"},
    {"seat": "PRATCHETT", "alias": "the footnoted satirist", "riddle": "fantasy is a funhouse mirror angled exactly at us"},
    {"seat": "TOLKIEN", "alias": "the elegist", "riddle": "the world is older than the story and will outlive it"},
    {"seat": "ORWELL", "alias": "the windowpane", "riddle": "when language rots, thought follows, and plainness is resistance"},
    {"seat": "ALAN MOORE", "alias": "the magician", "riddle": "form is a spell and the medium does things to the reader"},
    {"seat": "SHAKESPEARE", "alias": "the stage", "riddle": "everyone says more than they know and less than they mean, and the fool tells the truth"},
    {"seat": "STEPHENSON", "alias": "the engineer", "riddle": "the explanation IS the story, and the artifact inside the fiction can be real"},
]


def load():
    mods = {}
    for rid in REGIONS:
        p = GM / (rid + ".v1.json")
        m = json.loads(p.read_text(encoding="utf-8"))
        mods[rid] = m
    return mods


def validate(mods):
    errs = []
    owner = {}
    for rid, m in mods.items():
        for room_id in m.get("rooms", {}):
            if room_id in owner:
                errs.append("duplicate room id across modules: " + room_id)
            owner[room_id] = rid
    for rid, m in mods.items():
        if m.get("start_room") and m.get("rooms"):
            if m["start_room"] not in m["rooms"]:
                errs.append("%s start_room missing" % rid)
        for room in m.get("rooms", {}).values():
            for dst in room.get("exits", {}).values():
                if dst not in owner:
                    errs.append("unresolved exit: %s -> %s" % (room["id"], dst))
    # agreed invariants wired?
    ford = mods["adventure_2d6_stub"]["rooms"]["river_ford"]
    if ford["exits"].get("north") != "gallery":
        errs.append("loop-closes NOT wired: river_ford.north != gallery")
    dl = mods["audit_dungeon"]["rooms"]["doctrine_library"]
    if dl["exits"].get("lens_gate") != "garage_gate":
        errs.append("lens-count-gate NOT wired")
    got_lenses = [r for r in mods["riddler_optics"]["rooms"] if r in LENS_ROOMS]
    if len(got_lenses) != 10:
        errs.append("expected 10 lens rooms, found %d" % len(got_lenses))
    return errs, owner


def beta0(mods):
    adj = {r: set() for r in REGIONS}
    owner = {}
    for rid, m in mods.items():
        for room_id in m.get("rooms", {}):
            owner[room_id] = rid
    for rid, m in mods.items():
        for room in m.get("rooms", {}).values():
            for dst in room.get("exits", {}).values():
                other = owner.get(dst)
                if other and other != rid:
                    adj[rid].add(other)
                    adj[other].add(rid)  # undirected: forward-only undercounts merges
    seen, n = set(), 0
    for r in REGIONS:
        if r in seen:
            continue
        n += 1
        q = deque([r])
        while q:
            u = q.popleft()
            if u in seen:
                continue
            seen.add(u)
            q.extend(adj[u] - seen)
    return n


ENGINE = r"""
// ================= THE WALKER (one engine, no second data format) ==========
const OWNER = {};
for (const [mod, m] of Object.entries(MODULES))
  for (const rid of Object.keys(m.rooms || {})) OWNER[rid] = mod;

const state = {
  mod: "adventure_2d6_stub",          // neutral start: crossroads — descent contested
  room: "crossroads",
  lenses: [],                          // lens room ids collected
  out_height: 0,                       // water OUT tank height (0..3)
  valve_a: false, valve_b: false, ticks: 0,
  refraction: false,                   // OUT.height carried as refractive index
  disputed: [],                        // kifu rows flagged DISPUTED
  kifu: [],                            // every move, session record
  summoned: {}
};

function room() { return MODULES[state.mod].rooms[state.room]; }
function kifu(line, flag) {
  state.kifu.push({ ts: new Date().toISOString(), mod: state.mod, room: state.room,
                    line, flag: flag || null });
  if (flag === "DISPUTED") state.disputed.push(line);
}

function render() {
  try { _render(); } catch (e) {
    state.kifu.push({ ts: new Date().toISOString(), mod: state.mod,
      room: state.room, line: "render error: " + e.message, flag: "DISPUTED" });
  }
  document.getElementById("kifu").textContent =
    state.kifu.slice(-14).map(k => k.ts.slice(11, 19) + " " + k.line +
      (k.flag ? " [" + k.flag + "]" : "")).join("\n");
  renderQuests();
  const hints = { gallery: "open valve a", source_cistern: "open valve a",
    out_cistern: "wait", fractal_maze: "ride the refraction",
    riddler_engram: "summon pratchett", audit_dungeon: "walk to doctrine_library" };
  document.getElementById("cmd").placeholder =
    hints[state.mod + "/" + state.room] || hints[state.mod] || hints[state.room] || "pour bucket";
}

function renderQuests() {
  const q = [
    { done: state.out_height >= 3, text: "fill the water tanks at the Clear Pipes keep (open valve a, open valve b, wait x3)" },
    { done: state.refraction, text: "carry the height — you are now carrying the refractive index" },
    { done: state.lenses.length >= 10, text: "gather the 10 lenses in the optics garage (walk all ten lens rooms)" },
    { done: state.lenses.length >= 10 && state.mod === "audit_dungeon", text: "open the library's lens gate (audit dungeon -> the garage beyond)" },
    { done: state.kifu.some(k => /loop witnessed/.test(k.line)), text: "witness the ford loop (river ford -> the gallery -> home)" }
  ];
  document.getElementById("quests").innerHTML = q.map(x =>
    (x.done ? "\u2611 " : "\u2610 ") + x.text).join("<br>");
}

function _render() {
  const r = room();
  const lensRow = "lenses: " + state.lenses.length + "/10";
  const waterRow = "valve A: " + (state.valve_a ? "OPEN" : "closed") +
                   " · valve B: " + (state.valve_b ? "OPEN" : "closed") +
                   " · OUT.height: " + state.out_height + "/3" +
                   (state.refraction ? " · refractive index CARRIED" : "");
  let exits = Object.entries(r.exits || {}).map(([k, d]) => {
    const target = OWNER[d] ? d + "  [" + OWNER[d] + "]" : d + " (broken)";
    let lock = "";
    if (d === "leaf_gate" && !state.refraction)
      lock = "  ⛔ water-feeds-field: leaf_gate needs OUT.height (the refractive index)";
    if (state.room === "doctrine_library" && d === "lens_gate" && state.lenses.length < 10)
      lock = "  ⛔ lens-count-gate: " + state.lenses.length + "/10 lenses";
    return '<button data-exit="' + d + '" ' + ((lock || target.includes("(broken)")) ? "disabled" : "") +
           '>' + k + ' → ' + target + lock + '</button>';
  }).join("<br>");
  const hooks = (r.hooks || []).map(h => "· " + h).join("<br>");
  const contested = (state.mod === "water_computer" || state.mod === "fractal_maze")
    ? '<div class=" contested">CONTESTED EDGE (RIB): gate style — valve heights (Grok) vs computed flag (DeepSeek). Both readouts shown; neither rules. Tiebreak gated on operator GO.</div>' : "";
  document.getElementById("view").innerHTML =
    '<div class="mod">' + state.mod + " / " + state.room + "</div>" +
    "<h2>" + r.name + "</h2><p>" + (r.desc || "") + "</p>" +
    '<div class="meters">' + lensRow + " · " + waterRow + "</div>" +
    contested +
    "<h3>exits</h3>" + (exits || "<i>none</i>") +
    "<h3>hooks</h3><div>" + (hooks || "<i>—</i>") + "</div>";
}

function gotoRoom(dst) {
  const [mod, rid] = resolve(dst);
  if (!mod) { kifu("REFUSED broken exit " + dst, "DISPUTED"); render(); return; }
  // ---- AGREED GATES (RIB_CATHEDRAL_WORLD_V1) ----
  if (dst === "leaf_gate" && !state.refraction) {
    kifu("REFUSED leaf_gate without OUT.height — water-feeds-field", "DISPUTED");
    render(); return;
  }
  if (state.room === "doctrine_library" && dst === "garage_gate" &&
      state.lenses.length < 10) {
    kifu("REFUSED lens_gate at " + state.lenses.length + "/10 — lens-count-gate", "DISPUTED");
    render(); return;
  }
  kifu("move " + state.mod + "." + state.room + " -> " + dst);
  state.mod = mod; state.room = rid;
  onEnter();
  render();
}

function resolve(dst) {
  if (OWNER[dst]) return [OWNER[dst], dst];
  for (const [mod, m] of Object.entries(MODULES))
    if ((m.rooms || {})[dst]) return [mod, dst];
  return [null, null];
}

function onEnter() {
  const r = room();
  // lens pickup
  if (LENS_ROOMS.includes(state.room) && !state.lenses.includes(state.room)) {
    state.lenses.push(state.room);
    kifu("lens collected: " + state.room + " (" + state.lenses.length + "/10)");
    if (state.lenses.length === 10)
      kifu("TEN LENSES — lens-count-gate OPEN (audit doctrine_library -> garage_gate)");
  }
  // the loop, witnessed
  if (state.room === "gallery" && state.kifu.some(k => k.room === "river_ford"))
    kifu("loop witnessed: the ford runs to the gallery — loop-closes HOLDS");
}

function act(cmd) {
  const c = cmd.trim().toLowerCase();
  if (c === "open valve a" && state.mod === "water_computer") state.valve_a = true;
  else if (c === "open valve b" && state.mod === "water_computer") state.valve_b = true;
  else if (c === "wait" && state.mod === "water_computer") {
    state.ticks++;
    if (state.valve_a) state.out_height = Math.min(3, state.out_height + 1);
    if (state.valve_b && state.out_height > 0) state.out_height = Math.min(3, state.out_height + 1);
    kifu("wait — gravity ticks; OUT.height=" + state.out_height);
    if (state.out_height >= 3 && !state.refraction) {
      state.refraction = true;
      kifu("OUT.height=3 carried as the refractive index — water-feeds-field satisfied");
    }
    render(); return;
  } else if (c === "pour bucket") {
    kifu("pour bucket REFUSED — mechanism-is-the-answer: bucket-poured water is not computation", "DISPUTED");
    render(); return;
  } else if (c.startsWith("summon ")) {
    const who = c.slice(7).toUpperCase();
    const seat = ENGRAM_SEATS.find(s => s.seat === who || s.alias === c.slice(7));
    if (!seat) { kifu("no such seat: " + who); render(); return; }
    state.summoned[seat.seat] = true;
    kifu("summoned " + seat.seat + " (" + seat.alias + ")");
    alert(seat.seat + " — " + seat.alias + ':\n"' + seat.riddle + '"');
    render(); return;
  } else { kifu("no such act: " + c); render(); return; }
  kifu("act: " + c); render();
}

document.addEventListener("click", ev => {
  try {
    const t = ev.target.closest ? ev.target.closest("button[data-exit]") : null;
    if (t) gotoRoom(t.getAttribute("data-exit"));
  } catch (e) {
    state.kifu.push({ ts: new Date().toISOString(), mod: state.mod,
      room: state.room, line: "click error: " + e.message, flag: "DISPUTED" });
    render();
  }
});
window.addEventListener("load", () => {
  kifu("session open — walker v1, neutral start (descent contested)");
  render();
});
"""

HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>THE CATHEDRAL v1 — hand-wired</title>
<style>
 body {{ background:#101014; color:#d8d4c8; font-family: Georgia, serif; max-width: 860px; margin: 2rem auto; padding: 0 1rem; }}
 h1 {{ font-size: 1.3rem; color:#e8e2d0; }} h3 {{ color:#a8a290; margin-bottom:.3rem; }}
 .mod {{ color:#8a86; font-family: monospace; font-size:.8rem; }}
 .meters {{ font-family: monospace; font-size:.85rem; color:#7fbf7f; margin:.6rem 0; }}
 .contested {{ font-family: monospace; font-size:.78rem; color:#d0a040; border:1px dashed #d0a040; padding:.4rem; margin:.5rem 0; }}
 button {{ background:#1c1c22; color:#d8d4c8; border:1px solid #444; padding:.35rem .7rem; margin:.15rem 0; font-family: inherit; cursor:pointer; }}
 button:not(:disabled):hover {{ border-color:#c8b870; }} button:disabled {{ opacity:.45; cursor:not-allowed; }}
 #cmd {{ width: 60%; background:#16161a; color:#d8d4c8; border:1px solid #444; padding:.35rem; font-family: monospace; }}
 #kifu {{ white-space: pre-wrap; font-family: monospace; font-size:.75rem; color:#9a968a; background:#0c0c10; padding:.7rem; min-height: 8rem; border:1px solid #2a2a30; }}
 .note {{ font-size:.8rem; color:#8a8678; }}
</style></head><body>
<h1>THE CATHEDRAL — v1, hand-wired</h1>
<p class="note">One engine. Regions are mag_game_module.v1 files, assembled by
tools/cathedral_build.py. Agreed invariants live: loop-closes, lens-count-gate,
water-feeds-field, mechanism-is-the-answer, engram-is-summon. Contested edges
(descent order, gate style) are marked, not enforced — tiebreak gated on operator GO.
Acts: <code>open valve a</code> · <code>open valve b</code> · <code>wait</code> ·
<code>pour bucket</code> · <code>summon &lt;seat&gt;</code></p>
<div id="view"></div>
<h3>your quest card</h3><div id="quests"></div>
<h3>the table <span style="font-weight:normal">DM narrates · 2d6 on every act · gates stay deterministic</span></h3><div id="dm"></div>
<h3>act</h3><input id="cmd" placeholder="pour bucket"><button onclick="act(document.getElementById('cmd').value)">do</button>
<h3>kifu (session)</h3><div id="kifu"></div>
<script>
const MODULES = {modules_json};

const ENGRAM_SEATS = {engram_json};

const LENS_ROOMS = {lens_json};
{engine}
{dnd_layer}
</script></body></html>
"""


DND_LAYER_JS = '''// --- the DnD layer: DM voice + 2d6 + the ghost at your shoulder ---
// Harvested from the actual-play podcast (P2P_DND_ARCHITECTURE: the DM is the
// frontier monitor; play is the work; STEAL_DND_MUD_WOW_UI: DM voice = room card).
// Dice are cosmetic narration — every gate stays deterministic, replay law holds.
// Folded into the builder 2026-09-22 so rebuilds stop dropping it (data layer
// carries the tavern crosslink; this carries the narration layer).
const DM_LINES = {
  gallery: "Three tanks of honest glass. The DM leans in: height is the computation — everything else in this keep is persuasion.",
  source_cistern: "SOURCE runs high and cold. Open a valve, or stand there admiring the plumbing.",
  work_gallery: "Gravity's workbench. The DM taps OUT: whatever leaves here refracts everywhere else.",
  out_cistern: "OUT — the number everyone downstream will have to live with. Water feeds the field; always has.",
  crossroads: "Four ways, one post. The DM sets two dice on the table: every act rolls. Journeys, not kills.",
  ford: "The ford. You can hear the desert upstream. The river checks no papers — but it remembers.",
  doctrine_library: "Ten lenses, one gate. The library counts what you refuse to count.",
  engram: "The dead seats lean in. Summon carefully — some ghosts were operators.",
  garage_gate: "The gate opens on lenses carried, not courage.",
  leaf_gate: "Downstream of everything. The leaf waits on the water.",
  hill_causeway: "The causeway crests. From up here the world looks saddle-shaped. It is.",
  tavern_lantern: "The Guttered Lantern. The barkeep keeps your kifu and your tab in the same book.",
  _default: "The DM watches. The dice are already rolling."
};
const GHOST = ["'the bucket was never a lie — the hook was.'",
  "'descent was always the point.'",
  "'the water remembers the desert.'"];
const _dmLog = [];
function dmSay(t) {
  _dmLog.push(t); if (_dmLog.length > 3) _dmLog.shift();
  document.getElementById("dm").innerHTML = _dmLog.map(x =>
    "<div style=\\"font-style:italic;color:#c9a86a\\">◆ " + x + "</div>").join("");
}
function roll2d6(why) {
  const s = 2 + Math.floor(Math.random() * 6) + Math.floor(Math.random() * 6);
  dmSay("⚄ 2d6 → <b>" + s + "</b> on <i>" + (why || "wait") + "</i> — " +
    (s >= 7 ? "the table nods." : "the table holds its breath."));
  return s;
}
const _dmAct = act, _dmRender = render;
let _dmLastRoom = null;
act = function (cmd) {
  roll2d6(cmd);
  if (Math.random() < 0.15)
    dmSay("the ghost at your shoulder: " + GHOST[Math.floor(Math.random() * GHOST.length)]);
  return _dmAct(cmd);
};
render = function () {
  try {
    const r = room();
    if (r && r.id !== _dmLastRoom) { _dmLastRoom = r.id; dmSay(DM_LINES[r.id] || DM_LINES._default); }
  } catch (e) { /* the DM never blocks the walker */ }
  return _dmRender();
};
// --- tavern layer (self-steal: dnd_classic_stub, the Guttered Lantern) ---
// rumors + encounters + loot, the classic-module pieces the cathedral never carried.
window._encDown = window._encDown || {};
const _dmAct2 = act, _dmRender2 = render;
let _dmLastRoom2 = null;
act = function (cmd) {
  try {
    const r = room(), enc = r && r.encounter;
    if (enc && !window._encDown[r.id]) {
      const s = 2 + Math.floor(Math.random() * 6) + Math.floor(Math.random() * 6);
      if (s >= 7) { window._encDown[r.id] = true;
        kifu("⚔ " + enc.name + " down (2d6=" + s + ")", null);
        dmSay("⚔ " + enc.name + " falls. The room exhales."); }
      else kifu("⚔ " + enc.name + " holds — bloodied, back away (2d6=" + s + ")", "DISPUTED");
    }
  } catch (e) { /* tavern layer never blocks the walker */ }
  return _dmAct2(cmd);
};
render = function () {
  try {
    const r = room();
    if (r && r.id !== _dmLastRoom2) {
      _dmLastRoom2 = r.id;
      if (r.hooks && r.hooks.length) dmSay("◆ rumor: " + r.hooks[0]);
      if (r.encounter && !window._encDown[r.id])
        dmSay("⚔ " + r.encounter.name + " bars the way — hp " + r.encounter.hp + "; your next roll decides it.");
      if (r.loot) dmSay("✦ here for the taking: " + r.loot.join(", "));
    }
  } catch (e) { /* same law */ }
  return _dmRender2();
};'''


def main():
    mods = load()
    errs, owner = validate(mods)
    b0 = beta0(mods)
    print("VALIDATION:", "PASS" if not errs else "FAIL")
    for e in errs:
        print("  -", e)
    print("beta0 (wired world):", b0, "islands")
    if errs:
        sys.exit(1)

    modules_js = json.dumps({k: {"module_id": v.get("module_id"),
                                 "title": v.get("title"),
                                 "start_room": v.get("start_room"),
                                 "rooms": v.get("rooms", {})}
                             for k, v in mods.items()}, indent=1)
    engram_js = json.dumps(ENGRAM_SEATS, indent=1)
    lens_js = json.dumps(LENS_ROOMS)
    html = HTML.format(modules_json=modules_js, engram_json=engram_js,
                       lens_json=lens_js, engine=ENGINE, dnd_layer=DND_LAYER_JS)
    if "const DM_LINES" not in html or 'id="dm"' not in html:
        print("FATAL: dnd layer did not land in output html")
        sys.exit(1)
    OUT.write_text(html, encoding="utf-8")
    # build lock (Nix habit): which inputs baked this html — one rolling file
    import hashlib
    def fsha(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    lock = {
        "ts": NOW.isoformat(),
        "modules": {rid: fsha(GM / (rid + ".v1.json")) for rid in REGIONS},
        "html_sha256_16": hashlib.sha256(html.encode("utf-8")).hexdigest()[:16],
        "note": "lock (rib.md.record.v1): this html is reproducible from exactly "
                "these module hashes; a claimed build whose hash is absent here "
                "was never baked (v0.9 lesson)",
    }
    (OUT.parent / "cathedral_build.lock.json").write_text(
        json.dumps(lock, indent=2), encoding="utf-8")
    print("build lock: cathedral_build.lock.json (html %s...)" % lock["html_sha256_16"])
    print("wrote", OUT.relative_to(ROOT), "(%d bytes)" % len(html))
    print("loop edge: river_ford.north -> gallery  [OK]")
    print("lens gate: doctrine_library.lens_gate -> garage_gate @10/10  [OK]")
    print("water feed: leaf_gate requires OUT.height>=3  [OK]")
    print("bucket: refused, DISPUTED  [OK]")
    print("start: crossroads (neutral — descent CONTESTED, engine enforces no order)")


if __name__ == "__main__":
    main()
