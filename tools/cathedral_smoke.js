/* CATHEDRAL SMOKE (static) — validate the shipped cathedral_v1.html
 * WITHOUT executing page code: parse the inlined MODULES/ENGRAM_SEATS as JSON
 * (the builder emits them via json.dumps), assert the RIB wiring, and grep the
 * engine source for every gate. Run: node tools/cathedral_smoke.js
 */
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(
  path.join(__dirname, "..", "watch", "inbox", "cathedral_v1.html"), "utf8");

const fails = [];
const expect = (cond, name) =>
  cond ? console.log("  PASS " + name) : fails.push(name) ||
    console.log("  FAIL " + name);

// ---- parse the data blocks (pure JSON, no execution) ----
// CRLF-agnostic boundaries: the builder's template may land with \r\n endings.
const mStart = html.indexOf("const MODULES = ") + "const MODULES = ".length;
const iSeats = html.indexOf("const ENGRAM_SEATS");
const mEnd = html.lastIndexOf("}", iSeats) + 1;         // closing brace of MODULES
const modules = JSON.parse(html.slice(mStart, mEnd));
const eStart = iSeats + "const ENGRAM_SEATS = ".length;
const eEnd = html.indexOf(";", eStart);                  // seats JSON holds no ';'
const seats = JSON.parse(html.slice(eStart, eEnd));

// ---- ownership + exit resolution ----
const owner = {};
for (const [mod, m] of Object.entries(modules))
  for (const rid of Object.keys(m.rooms || {})) {
    if (owner[rid]) fails.push("dup room: " + rid);
    owner[rid] = mod;
  }
let unresolved = 0;
for (const m of Object.values(modules))
  for (const room of Object.values(m.rooms || {}))
    for (const dst of Object.values(room.exits || {}))
      if (!owner[dst]) { unresolved++; console.log("  broken exit ->", dst); }
expect(unresolved === 0, "every exit resolves globally (" +
  Object.keys(owner).length + " rooms)");

// ---- agreed invariants ----
expect(modules.adventure_2d6_stub.rooms.river_ford.exits.north === "gallery",
       "loop-closes wired: river_ford.north -> gallery");
expect(modules.audit_dungeon.rooms.doctrine_library.exits.lens_gate === "garage_gate",
       "lens-count-gate wired: doctrine_library.lens_gate -> garage_gate");
const lensRooms = Object.keys(modules.riddler_optics.rooms)
  .filter(r => r.startsWith("lens_"));
expect(lensRooms.length === 10, "10 lens rooms in optics");
expect(seats.length === 10 && seats.every(s => s.seat && s.riddle),
       "engram holds 10 seats with riddles (engram-is-summon, no rooms)");
expect(Object.keys(modules.riddler_engram.rooms || {}).length === 0,
       "engram has zero rooms (a card, not a maze)");

// ---- contested stays neutral ----
expect(!/descent_order|enforce.*order|FORCED.*descent/i.test(html.slice(html.indexOf("THE WALKER"))),
       "engine enforces no descent order (contested -> neutral)");

// ---- gates present in shipped engine source ----
const engine = html.slice(html.indexOf("THE WALKER"));
for (const gate of ["pour bucket REFUSED", "lens-count-gate", "water-feeds-field",
                    "loop witnessed", "lenses.length < 10", "refraction"]) {
  expect(engine.includes(gate), "engine contains gate marker: " + gate);
}

// ---- kifu footer present ----
expect(html.includes('id="kifu"'), "kifu panel present");

console.log(fails.length ? "SMOKE FAILED: " + fails.join("; ")
                         : "SMOKE PASS — wiring, invariants and gate markers verified (static)");
process.exit(fails.length ? 1 : 0);
