# Next-window handoff — frozen spec (executed by any new window)

_This file did not exist until 2026-09-15 (Clippy cited a fossil). This IS the spec now.
Keep it short. Update the STATE section, not the procedure._

## Procedure (every new window, in order)

1. **Load:** `docs/FRAMEWORK_LOAD.md` → `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md` → `AGENTS.md` (already injected as workspace instructions).
2. **Warm:** `memory/briefs/latest.md` → `state/CURRENT.md` → `./mag.cmd context-pack` → `queue/todo.md`.
3. **Check inbox:** `watch/inbox/index_events.jsonl` tail (last 10 events) — what landed since last window.
4. **One job** from the operator or the board (`queue/todo.md` / newest `memory/plans/fifty_wide_*.md`).
5. **FILE before close:** durable writes to `watch/inbox/` + register event in `index_events.jsonl`; checkpoint commit; `python main.py state-snapshot` if session was heavy.

## Standing laws (do not re-derive)

- Python: `.venv\Scripts\python.exe` or `mag.cmd` — never bare `python` (Hermes venv on PATH).
- T0/T1 local only. Janitor first. Pack+goal to remotes, never chat history.
- Residual on disk is truth; chat is heat. Append events, never rewrite the INDEX fold.
- "Launch N wide" = seed N lane tasks (board file in memory/plans/ + queue/todo.md section).
- Operator signs as Mark; journals arrive as photos → transcribe faithfully [? for uncertain], copy jpgs to watch/inbox, full plain-language decode.

## STATE (update this section only)

- **NIGHT FOLD 2026-09-18 (committed 45c66ee42):** **THOUGHT QUANTIZER v0.2
  SHIPPED** — percolator invariants compile to tiered instruction packs
  (memory/corpus/quantized_thought/: 24 frontier / 12 flash / 12 local;
  weight = recency × shape, raw counts demoted — **percolator echo PROVEN,
  142×/event inflation**). v0.3 owed: two-pass classification (over-refuses
  error-quoting laws), source-distinct weighting, wire into wave rebuilds.
  Shadow strata decoded (march = Mimosa finding batches; sea = 25-shape era
  board; octant = seat_contract.v1 briefs — steal for lane handoffs).
  Elder-lens skill forged. Night receipt: **watch/inbox/NIGHT_FOLD_20260918.md**
  (registered 64E6B1353CB6). LINKS at 249.
- **SESSION CLOSE 2026-09-18 (~06:40Z):** checkpoint commit **e692b2259**
  landed (whole window: catalog v3, askability tools, shadow steal, watch
  mining, context OS, wave protocol, skill forge, audits, graph v2, gaps
  UF-119..130). 12 files remain dirty (trail/telemetry churn — normal).
  Operator signing off; TOMORROW'S DECISIONS LEFT FOR HIM: (1) trunk order —
  say "go trunk" and windows serve Sep-20 (Astra I2/I3, HOLD 3 rehearsal,
  seal); (2) junction `training` policy (mirror vs duplicate); (3) netlify
  deploy auth + Discord token rotation, whenever. Lanes drain UF-119..130
  autonomously; receipts in union raw.jsonl. Drift patrol sweeps at 08:00.
- **2026-09-18 (cathedral-map window):** **THE_CATHEDRAL_MAP_20260918.md**
  filed — go player = evolution-loop genome over the code layer (board=catalog
  zones, moves=TOOL_MAP actions under RUINS GO's ten laws, kifu=trajectory,
  fitness=gates); 4 stones (player shell → kifu → self-play vs best genome →
  composing games leave estate stones). **TRACK LAW adopted: one trunk =
  state/CURRENT board, led in every boot; each window declares trunk or
  branch work in its first receipt.** Sep-20 in 2 days → next windows should
  be TRUNK windows (Astra I2/I3, HOLD rehearsal, seal) unless the operator
  orders otherwise.
- **2026-09-18 (research-gap window):** knowledge graph UPDATED — 19 families
  / 158 edges (5 new harvest families: skills-engine, askability-layer,
  shadow-corpus, operating-doctrine, audits-lenses; 8 new successions) +
  Librarian annotation with **8 build orders** (standing receipt writer,
  edge→doctrine compiler, imprint refresher, lane registry, audit→amendment
  loop, canon↔shadow diff...). RESEARCH_GAP_ANALYSIS_20260918.md: domain
  coverage mined (X-intel 56% of 245 links; thin: swarm 4, windows 4,
  steering 9, security 9) → **8 gaps mapped to operations, dispatched as
  UF-124..130** (steering prior art, multiagent comms schemas, swarm
  economics, per-provider cache invalidation = the kernel amendment
  ceremony's research floor, Windows reparse law, secret-scanning, QLoRA
  small-corpus for Rocinante).
- **2026-09-18 (context-os window):** **CONTEXT OS spec filed**
  (**watch/inbox/CONTEXT_OS_20260918.md**, anchor: Ueki linkages via Pickover
  — one crank, many patterns). Kernel=FROZEN_RIB (99.4% measured hit), cache
  RAM=prompt mining, scheduler=lane ladder, power=law-15, ground=verkle+beads,
  syscall log=receipts. **Linkage law:** energy/behavior → 0 as prefix
  stability → 1. History+zeitgeist loaded as boot record (era-003 THE POUR,
  DNA residual, ouroboros→Rocinante). Loaded via rib warm (cached 7/850) +
  trajectory dadfc563aee2ac46 + registration 819A1735BC45.
- **2026-09-18 (watch-mining window):** watch folder mined COMPLETE — 8,354
  files / 12 strata → `memory/corpus/watch_mining/` (inventory, digest
  aggregates, **card_timeline.json: 770 cards since 09-01** = the surviving
  operator-voice arc). Shadow strata named: `octant_20260831/` (swarm
  governance CHARTER — founding doctrine in a dated folder, promote or
  supersede), `march/` (3rd card pipeline, dormant?), `sea/` (era-board
  ancestor), `organs/` (2,328 files of code in intake — kimodo.cpp; relocate).
  Debt: three card pipelines one job — fold or tombstone two. Digest:
  **watch/inbox/WATCH_MINING_20260918.md**. `.mimosa/` = machinery, exclude
  from future corpora counts. Canon name-search finds the corpus; CONTENT
  search still awaits the FTS5 projection (UF-120 justified it).
- **2026-09-18 (capability-surface window):** research corpus ASKABLE —
  `research_search/sources/stats` tools live (registry 31; links 245 + packs
  107 + **20 canon lanes / 22,390 primary files** incl. shadertoy21k; verified
  live; MCP scout roundtrip; 27/27 tests). Capability brief:
  **watch/inbox/SEAT_CAPABILITIES_20260918.md** (skills inventory, primary
  evidence register by canon lane, runbook). Operational gain: prior-art and
  canon questions are now one tool call; cite the file, not the summary.
- **2026-09-18 (deep self-steal window):** one recursion down
  (**watch/inbox/SELF_STEAL_DEEP_20260918.md**): unanswered-question ledger —
  13 elder questions scored **3 answered / 5 partial / 4 unanswered / 1
  never-asked**; deepest 3 converge on ONE question: *who holds interpretive
  authority over the record?* Verb signature: `evaluate` is the seat's #1
  verb (judging outnumbers building — closure tax on recursion proposed).
  RECURSION STEAL v1 named (touch→extract→file→load→falsify; steals that skip
  file+load die, cf. 0915 receipts). Law proposed: elder questions are
  primary data — owned, ledged, answer-rate metered.
- **2026-09-18 (self-audit window):** standing wave protocol STOLEN as a spec
  (**watch/inbox/STANDING_WAVE_PROTOCOL_20260918.md** — 7 laws from 143
  receipts/16 lanes/88.8% ok). Self-audit filed
  (**watch/inbox/SELF_AUDIT_ZCODE_20260918.md**): 7 tri-state findings —
  headline = **derived/primary boundary missing** (map replace-without-backup
  incident ↔ correspondence attrition are the same blindness); verify-before-
  replace law + witness pass filed as WANTS. Audit findings stand Unproven
  until witnessed (deliberate, per honesty law). MEMORY.md prune to 24.4KB
  still owed.
- **2026-09-18 ("next" — execution window):** catalog REBUILT through v3 walk
  inline: **757,667 rows** (was 946,773; −189K = junction `training` duplicate
  trees v2 counted, attribution Unproven), deduped, fresh (ruins_go_engine +
  today's files searchable; tags retagged; zcode_history corpus discoverable
  kind=ledger). Elder trail defect FIXED (CYCLE_FAIL on lane-down in
  lane_runner). UF-120 verdict: **SQLite FTS5 migration justified** (30–80ms
  vs 3.5s) — the next build is the FTS5 projection + corpus_search rewrite.
  UF-119/122/123 still draining. Module `mag/catalog_rebuild.py` still
  unlanded (hook) — logic lives in CORPUS_MAP_SALON_20260918.md Appendix A +
  execution receipt. organ_map test failure = pre-existing (ask_router drift).
- **2026-09-18 (shadow-steal window):** zcode correspondence+trajectory stolen
  LOCAL-ONLY → `memory/corpus/zcode_history/` (sessions.jsonl, agent_tasks.jsonl
  1,161 rows, 3 correspondence files) + digest **watch/inbox/ZCODE_SHADOW_STEAL_20260918.md**
  (7-room taxonomy, gap list). HEADLINE: operator voice does NOT survive in
  `.zcode/cli` (model-io strips requests) — export law proposed, `export-log-stage`
  still unwired. Loaded via organs: trajectory milestone 88dffa817867c717, rib
  warm cached=7/850, snapshot dedup. Corpus-map program still open (v3 scanner
  landing, UF-119..123 draining).
- **2026-09-18 (corpus-map window):** ractor salon folded the corpus-map ask →
  **the map existed (946,773-row catalog); the job is askability.** Shipped:
  corpus_search/get/tail/stats tools (tools/corpus.py → TOOL_MAP + mcp_server,
  read-only, sha256-echoed; MCP round-trip green; 27 tests pass), tag pass v1
  (catalog/tags.jsonl + TAG_REPORT.md). OPEN: land scanner v3 (append-mode
  doubling measured; draft + checklist in **watch/inbox/CORPUS_MAP_SALON_20260918.md**
  — Mimosa hook blocked walker-class .py writes, code filed as draft), freshness
  budget, tags v2 owner column, 50-question retrieval eval BEFORE any mining.
  Lanes: UF-119..123 on the union queue; wants in watch/WANTS.md. Elder lens for
  09-17 filed manually (cage 429) — trail-writes-success-on-failure defect named
  in queue/lanes/elder/surface.md; ghost-daemon still crashed/unrepaired.
- **2026-09-17 (pre-dawn, wave+1):** grounding_wave **v4 admission boundary BUILT** —
  `mag/grounding_wave.py` gates at write (row-122's bypass path physically refused), verbs
  `void/contest/witness/view`, 26 new tests, live row 122 untouched by design. VOID of rows
  122+123 STAGED as dry-run PROPOSAL — needs operator word + a named second seat, then
  verify returns LINKAGE-PASS. Rollback incident CLOSED: mechanism =
  `build_vislab_catalog.py::sync_games()` syncing dist→games backward (fired 2×, mtime-
  preserving); PERMANENTLY FIXED in FX5 (direction inverted to canonical→derived + drift
  guard; both stale mirrors synced; law: canonical flows to derived, never backward).
  Chain through #8: `5305a99b1 → 0f34a8f3e → 75c030d29 → 9546bb7f8 → 118333dd1 →
  2b85093f1 → b93c7521b → 7df23b916`. Master index:
  **`watch/inbox/wave_20260916/WAVE_STATE_20260916.md`** + warm receipt
  `receipts/WARM_START_20260916.md`. Morning harness check owed: mud replay port
  survival after the second rollback (expect test_mud_replay.js green or re-land per
  receipts/FX4 + receipts/W5 staged hunks).
- **2026-09-16 (end of wave night):** Standing wave DRAINED — 60 receipts filed across
  `watch/inbox/wave_20260916/receipts/` + `watch/inbox/physical_computing/receipts/`;
  master index: **`watch/inbox/wave_20260916/WAVE_STATE_20260916.md`** (start there).
  Board: referee chain green · sampler claim conditional-refuted (closure receipt still pending) ·
  cube program staged · ractor plugin packaged (`P1_RACTOR_PACKAGE.md`) · wave protocol 30+ lanes folded ·
  26-work physical-computing canon registered (`S4_CORPUS_STEAL.md`, filed via `mag.link_library`) ·
  salon_50 honest count 39/50 (fossil "50/50" corrected in F1).
  **Next stones:** (1) sampler closure receipt, (2) v4 VOID build to repair grounding chain row 122
  (verify FAIL: row 122 truncated, `prev` matches nothing, no `hash` key; rows 123–124 orphaned behind it;
  tonight's wave-trajectory row is drafted in `WARM_START_20260916.md`, do NOT hand-edit the JSONL),
  (3) publish ractor-salon standalone repo, (4) cube GO (build auditions in `V1_BUILD_AUDITIONS.md`).
  Warm-start receipt: `watch/inbox/wave_20260916/receipts/WARM_START_20260916.md`.
- **2026-09-15:** Discord bot LIVE (Mag#2124, guild NT-ACv2, token in `%LOCALAPPDATA%\hermes\.env`,
  gateway green, AGENTS.md truncation fixed via `context_file_max_chars: 40000` in Hermes config).
  Receipt: `watch/inbox/HERMES_DISCORD_SETUP_20260915.md`.
  Checkpoint `aa9bea1b7`. Fifty-wide board: `memory/plans/fifty_wide_20260915.md` (50 tasks, seeded in queue/todo.md).
  Goal horizon: **Sep-20 proof** — gate = operator beacon read (`watch/inbox/DAWN_READING_MIRROR_20260907.md`);
  Astra bundle fixes + retro-knotter GO are the big prep lanes.
- **Known warts:** inbox INDEX fold stale (pre-existing, append-only); hosted_room_worker sqlite
  lock (non-blocking); netlify deploy auth pending; token rotation for the Discord bot recommended
  (clipboard-only lander: `%TEMP%\discord_token_land.py`); **GROUNDING_WAVE chain verify FAIL at row 122
  (2026-09-16)** — posts land but nothing after 122 can verify until the v4 VOID build; gene pool still
  feeds on the frozen 2026-09-04 audit (`memory/audit/aud_*.json`, no regenerator exists).
