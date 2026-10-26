# W5 — WORLDGEN + ZONEGATE PORTED TO PYTHON

**Date:** 2026-09-30 · **Seat:** ZCode (Y1's second port, after Z4 section_stream)
**Mission:** roblox/src/shared/Worldgen.luau + roblox/src/server/ZoneGate.luau → Python (the DF wiki worldgen steal: Ages + 130 spheres; portal gating by per-soul sphere vs region alliance).
**Files (owned, no commit):** `mag/worldgen.py` (new) · `tests/test_worldgen.py` (new)
*Honesty note: this seat made no commit; a sibling lane's wave sweep (commit `e499972b0`, "40+ lanes landed") landed both files while this port was finishing — `git diff HEAD` against them is empty, so the committed bytes are this port's final versions.*

## What landed

`mag/worldgen.py` ports both Luau modules 1:1:

- **SeedRng** — bit-exact xorshift32 mirror of `shared/SeedRng.luau` (masks for bit32 wraparound; same fleet shape as the section_stream test mirror).
- **Worldgen** — Ages (Age of Myth → Heroes → Legends every 10 boss kills, ordinals recur, capped "Seventh"), `zone_alliance` (opposition outranks kin — law 4), `sphere_alignment`, forgotten beasts (dwarven-compound namer, kinship rows, `Kin: …/Foes: …` line; "none" is a fact).
- **ZoneGate** — per-soul sphere draw `SeedRng(UserId * 7919).int(1,130)` (deterministic per player, cached in the Soul's Sphere attribute); `alliance_for` over the region's whole row (first opposed decides, else any allied); `portal_gate`: allied → open + 1 VirtueMark per 300 s per zone, opposed → refused (ledger line rate-limited 5 s), independent → open no effect, unjoined zone → no gate. `init(regions)` is the t67 single-writer join; `attach` stamps the t46 `Gate_*` verdicts. Roblox Player → `Soul(user_id, attributes)`; ShadowLedger → gate ledger + optional recorder callback; PlayerAdded → pull-based attach.
- **Generated mirrors** — SPHERES (130), ALIGNMENT (31: 15 good / 16 evil), ALLIES/OPPOSED (130 keys), REGION_SPHERES (11 regions, NONE empty), DWARVEN (130 words: 50 adj / 80 noun), machine-extracted from the generated .luau artifacts and asserted **byte-identical incl. key order** (extraction + parity script, one shot, not hand-copied).
- **Seam kept open (not fallback creep):** `region_spheres` is constructor-injectable defaulting to the sourced table — the exact seam the ZoneGate.luau header names ("if the mine ever grows an aligned region row…"): every sourced row is unaligned spheres, so "opposed" is unreachable through sourced data; the test proves that fact and exercises the lock through the seam.

**Estate connection:** this is the CAMPAIGN layer's zone progression — WaterGraph is the physics, Worldgen is the geography.

## Tests — real counts, instrument named

- `pytest -q tests/test_worldgen.py` (repo venv): **39 passed** (2026-09-30, twice).
- Coverage: same-UserId determinism (fresh souls, fresh gates, golden anchors 1→LOYALTY, 42→VICTORY, 123456→DANCE, 999999999→PREGNANCY, 2147483647→AGRICULTURE via seed-wrap→1; all 130 reachable over 5000 ids); allied opens + marks per 300 s window and per zone; opposed refuses (no marks, rate-limited ledger); independent no-effect; unjoined open; join/attach attributes; `gate_attr` sanitize; age progression 0→630 kills; golden beasts seed 42 `alak nicat, "the Ace chain of THUNDER"` / seed 2026 `ilas nil, "the Absolute hammer of VOLCANOS"`; alliance-table symmetry + structural data laws (130 unique spheres, opposition = exact class complement, grounded rows, sourced-never-oppose).
- Full suite `pytest -q --ignore=tests/test_behavioral_awareness.py`, 2026-09-30 06:22–07:05 EDT, 2604.82 s: **7 failed, 3171 passed, 12 skipped, 3 errors** (executed outcome sum 3190; errors are collection errors). Pre-existing, not this port: `tests/test_behavioral_awareness.py` carries unresolved merge-conflict markers from another lane (excluded, not mine to fix); `test_oral_dedupe.py::test_live_index_census_and_founding_law` + 2 `test_organ_map.py` failures reproduced minutes later with zero worldgen involvement (live-memory-state tests; remaining failure names were cut by the tail pipe — the twin full run's lastfailed cache shows the same live-state/deleted-path neighborhood, no worldgen entries anywhere).
- Ratchet: `tools/violation_ratchet.py check --changed` → PASS (no new debt).

## Notes

- Cross-language determinism claim: xorshift32 uses only xor/shift (exact in big ints with masks); division by 2^32 is exact in both languages' IEEE doubles — same seed integer ⇒ same stream in Luau and Python. Luau itself was not executed here (no Roblox runtime); goldens pin the Python side against drift.
- A twin full-suite run with the identical command line ran concurrently (sibling lane); the shared box made both runs slow (43 min each). No interference beyond timing.
