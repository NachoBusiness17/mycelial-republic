# FULL AUDIT 2026-09-08 — THE MAP OF THE TERRITORY

**Commission (operator):** "go through everything contained in our databanks, memory,
skills, dashboards, dogfooding them all and creating the map of the territory. So we
may design the next one." · **GO:** 2026-09-08 ~16:1xZ · **Executed by:** zcode seat
(mechanical walker + 2 read-only judgment workers + browser dogfood + 1 external witness).

**Headline finding: the fleet says ~500 files; the territory has 60,261 (≈1.06 GB).**
The next system is designed from THIS number, not from the map's self-image.

---

## Method (so the map can itself be audited)

- `audit_walk.py` (this dir) — mechanical pass: 60,261 files, per-file size/mtime/parse,
  outbound path refs, chain integrity, nav integrity, dup-cluster sample. Output:
  `audit_records.json`.
- **Walker bug, honestly recorded:** the inbound-reference field never populated
  (`.get()`-skip error — every record skipped). Both judgment workers DETECTED it and
  recomputed inbound independently from the out-ref graph. Artifact field broken,
  worker recomputes authoritative.
- W1 (read-only Explore): watch/ cards triage, stale-pointer sweep, spot reads.
- W2 (read-only Explore): mag/ smoke tests (imports), kill pool, docstring census.
- Browser (IAB): all 84 rooms loaded + error-banner probe; tavern_brawl deep dogfood,
  dfhack-style (in-page event driver; see method note §7).
- Astra witness #5 (gpt-5.6-sol via codex_seat, read-only commission, 794 words,
  sha256 5b98513a34ad68b0): attacked the planetary standing wave AND ran the
  false-receipt falsifier against the grounding ledger. ANSWER at
  `memory/runs/salons/astra_standing_wave_20260908/ANSWER.md`.

---

## The census (what IS)

| Batch | Files | MB | Parse fails | Zero-byte | Notes |
|---|---:|---:|---:|---:|---|
| watch/ + inbox | 1,023 | 32.1 | 1 | 0 | 934 md: 678 tri-stated, 355 falsifier-marked |
| dashboard/static | 121 | 7.5 | 0 | 0 | 84 html, 16 js |
| mag/ | 987 | 11.7 | 0 | 0 | 98.6% docstring coverage |
| memory/biography | 36,404 | 305.7 | — | 37 | 32,531 json + 3,784 md |
| memory/runs | 21,028 | 584.5 | — | 140 | 17,879 json; 34 dup clusters |
| configs/state/handoff | 117 | 16.1 | 0 | 2 | all YAML parse |
| corpus | 302 | 121.3 | — | 0 | 246 txt |
| aux (root drafts/scripts) | 279 | 1.4 | **63** | 1 | BOM-broken `_afk*.py` drafts |
| **TOTAL** | **60,261** | **≈1,060** | 64 | 180 | |

**Chain: 7,377 rows, index-contiguous, zero anomalies, tip d0a798c29722 (09-06 23:08Z).
PASS as a linkage structure.** (But see §6: linkage-PASS is not truth-PASS.)

---

## 1. KILL LIST (marked, not executed — deletion is operator-gated)

- **17 byte-identical inbox duplicates** of watch/ cards (all dated 09-01): AUDIT_A/B/C/D,
  ECONOMIST_ROUTE, ECONOMIST_SPEND_AUDIT, EXP002B_RECEIPT, FLEET_AUDIT, FLEET_STRUCTURE,
  HARDWARE_RADAR, HOT_JURY_F1F2, LANE_SLOT_MAP, OPS_RESEARCH_001, OPS_RESEARCH_LOOP,
  STEERING_LINEAGE, STEERING_SYNTHESIS, SWARM_DOCTRINE. The inbox copy dies; the watch copy lives.
- **2 drafts:** watch/inbox/X_DRAFT_WRONG_WORLD_PARABLE_20260907.md, watch/DAY_LEDGER_2026-09-07.md (29 words).
- **63 root `_afk*.py`/`_*.py` drafts** with UTF-8 BOM (unparseable since birth — never ran): pre-history sediment.
- **mag/ kill pool: 566 of 987 modules unreferenced for >3 weeks** (W2 recompute; top-50
  smallest listed in W2 report — table_turn_cli, wave_cache, game_dice, sense.py, test_dummy…).
- **180 zero-byte strays** (37 biography knots, 140 runs artifacts, state/art_queue.jsonl, mcp_err.txt).
- **1 broken json:** watch/inbox/FRONTIER_DISPATCH_001_20260905_SURFACE_CHECK.json.
- **34 dup clusters in runs/** — mostly `empty_recovery` boilerplate repeated across run dirs
  (23× pre_turn_messages.json identical) → the artifact schema repeats itself; compress, don't store.

## 2. PROSE LIST (prose wearing doctrine's clothes)

- **186 cards missing BOTH tri-state and falsifier markers**, clustered on the 08-31/09-01
  salon transcripts (PACK_RIB_COMPACTION, SALON_DIAMOND_AGE, RACTOR_A_LESSIG/B_BERNAYS/C_ELLUL
  + unversioned v1…). Need typing (mark the claims) or demotion (move to a transcripts shelf).
- **14 mag modules without docstrings** (gpipes, orchestrator, remedy, seat_guard, steer_bus + 9 `_probe/_diag`).
- **WEEKEND_BURN_BOARD_20260905: 7 of 8 build targets never landed** — a plan wearing a receipt's clothes.

## 3. RESURRECTION LIST (dark but load-bearing)

- **nav.js → `clear-ui.html` dead link**: the file exists as `index.clear-ui.html` — naming mismatch, one-line fix.
- **The deleted `mag/` tree**: STEERING_LINEAGE (8/8 dead refs), AUDIT_B_ELDER (8/8),
  PROSE_CENSUS (8/8), SELF_STEAL_GAME_ORGANS (8/8) point at a mag/ tree that was moved/deleted
  after 09-01 (incl. `mag/mag/` double-nesting — evidence of one bad move). Either the targets
  come back or the cards get re-pointed; today the doctrine's feet don't touch the ground.
- **control.html**: demoted 09-07 (cast_server down; port 8765 now serves the dashboard — recensus it).
- **9 mag modules with top-level side effects and no main-guard** (verkle_knot, bay_organs,
  lattice_distance, steer_bus, concurrency_gate, lite_guard, afk_loop, chord_lens, embassy_integrity) —
  import-risk; give them guards and they rejoin the testable core.
- **mag kill pool caveat**: inbound=0 is text-reference counting; orchestrator-dispatched organs
  (invoked by string name at runtime) are invisible to it. Spot-verify before any deletion.

## 4. DEPENDENCY GRAPH (the load-bearing skeleton)

- `nav.js` → 76/77 live refs → the rooms (84/84 render).
- The mag core: top-60 referenced modules, **51/51 import clean** (incl. mcp_server, overseer, switchboard).
- `verkle_chain.jsonl` ← knot gate ← sessions; → grounding_wave (46 posts, tip 8db528af29ca) → dashboard.
- MCP: 8001 (auth 401 correct, loopback) · dashboard: 8765 (live, /api/home 200).
- The `mag/mag/` double-nesting and the 09-01 deletion wave = the fleet's one bad move; the map says: name it.

## 5. THE MAP (what the fleet actually is)

**A live, verified core wrapped in 58,000-file sediment.**
- The core is REAL and PASSES: chain contiguous (7,377), 51 organ imports clean, 84 rooms render,
  678 cards tri-stated, tavern brawl fights, configs parse, MCP authenticated.
- The sediment is ACCRETION WITHOUT REAP: runs/ and biography/ grow append-only (by design),
  drafts never die (63 BOM files that never ran), inbox accumulates duplicates, cards cite
  files deleted months-of-fleet-time ago. **The corrective-gradient probe said the fleet never
  reaps its POLICY; the audit proves it never reaps its FILES either. Same root. The record
  grows; the body never shrinks.**
- The fleet is **only falsifiable from inside** (gap probe, confirmed): today that changed —
  witness #5 ran the fleet's own falsifier against the fleet and it FAILED HONESTLY (§6).
  This is the first cold-start witness receipt the fleet has.

## 6. THE ASTRA RECEIPT (witness #5 — the map's sharpest edge)

- **The false-receipt attack: verifier PASSED a false row** ("the ledger contains 1,000,000,000
  posts", real prev-hash, no second witness) → 0/1 false claims rejected. **The chain's PASS is a
  LINKAGE gate, not a TRUTH gate.** Every future reading of "chain verify PASS" must say which.
- Defects filed by the witness, confirmed in this audit's dogfood: `grounding_wave.py::post`
  rereads the full ledger per append with no append lock; `tavern_brawl.html` uses `Math.random()`
  and a 5-string in-memory log (the brawl screenshot shows exactly 5 log lines — witness CONFIRMED);
  admission accepts the caller's SUPPORTED label without entailment or second witness.
- Witness verdict (tri-state): components **SUPPORTED** · truth-gate reading **DISPUTED** ·
  planetary claims (admission, universal contribution, falling cost) **UNPROVEN**.
- Owe (build items, not wounds): append lock + second-witness gate or rename PASS → LINKAGE-PASS;
  seeded RNG + durable log in tavern_brawl; the toy falsifier Astra named is now the acceptance test.

## 7. Dogfood receipts (this audit ate its own cooking)

- 84/84 rooms HTTP-load with content; error-banner fixture caught ZERO failures.
- tavern_brawl deep dogfood PASS: insult-arm → provoke (agit 0→100 across 13 provocations) →
  threshold → brawl → projectiles → hits (FEN hp 100→98) → actor turns → THE ROOM log.
  Screenshot: watch/audit/FULL_AUDIT_20260908/ (brawl at peak, 09-08). Cosmetic: footer text
  overlap at 1280×720.
- **Driving-method correction (operator, mid-audit): "use them df hacks style"** — stop GUI
  puppeteering; drive the page's own event system from inside, one round-trip, read state.
  The dfhack driver found what clicking couldn't: rAF/timers throttle in background panes,
  synthetic mousemoves are free (SUPERHOT's clock is the mouse).
- `mag.run_python` is CAGED (sandboxed /tmp) — cannot see the host repo. Organ noted for what it is.
- F1-window deviation: mag-control-plane absent from `docker ps -a` (5 containers, not 6);
  restore door `docker start mag-control-plane` would fail. Function unaffected. DISPUTED-as-configured.

## 8. Design notes for the next system (the point of the dig)

1. **A reap law with teeth** — append-only is for the CHAIN, not for drafts. Kill list executes quarterly.
2. **A witness law** — every PASS names its gate (linkage vs truth); every organ gets a cold-start procedure a stranger can run.
3. **A naming law** — one file one name one place (`mag/mag/`, `index.clear-ui.html` are the diseases).
4. **A move law** — deletions/moves update pointers in the same commit (the 09-01 wave is the specimen).
5. **The harness is the unit of design** — same conclusion as the substrate synthesis (memory/corpus/substrate/substrate_native_computing_synthesis_20260908.md), reached from the other direction.

*Audit falsifier: any item above disprovable by reading the named artifact; if the census
numbers don't reproduce from audit_records.json, the map is wrong and says so here.*
