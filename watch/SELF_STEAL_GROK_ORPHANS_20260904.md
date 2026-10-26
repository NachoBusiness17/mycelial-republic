# SELF-STEAL — Grok-surface orphan mining (2026-09-04)

**ITEM:** Mine the grok lane's local artifacts for ORPHANS — what grok BUILT or said that is
recorded locally but never folded into the repo's record surfaces (watch/ cards,
memory/percolator/invariants.json, memory/law/registry.json, docs/, queue/). Companion to
SELF_STEAL_ZCODE_SESSION_ORPHANS_20260904.md (same format). Grok lane per AGENTS.md:
"grok-app-builder free lane receipted (@rvanomaly)", salon folds, X-scout batches.

## METHOD

**Two doors, both local. Repo first, disk second.**

- **Repo (primary):** 597 grok-named files (find -iname "*grok*", backups/tests/mine
  excluded). Grok's own words live in: `memory/runs/v4_council/{SOCRATIC,ARGUED,EXISTENTIAL,
  HARNESS,PRIMITIVES,PROJECT_AUDIT}_grok.md` + `grok_systems.md` (Aug 28 council), salons
  (`salon_20260827/{grok_sd,grok_nacho}.md` + COMBINED.md, `salons/connectors/
  SALON_grok_systems.md`), copilot outbox (grok-swarm-physics, grok-arch-consult,
  grok-deep-research, exit-grok — Aug 8), `memory/grok/design_brief.md` + `memory/grok_batch/
  buffer_{1,2,3}*.md` (Aug 8-12 asks), `memory/runs/game_grok_night/*` (Aug 27 canon grok
  built), `campaigns/villains_guild/daylight/` (grok's BUILD: riddler_map + kid_test_gate +
  RECEIPT, Aug 27), `queue/results/grok_build_coder_*.json` (build-lane proof, Aug 26),
  `state/vast/research/AUDIT_grok_correctness.md`, `memory/embassy/AOS/grok_PROOF.md`,
  `memory/runs/elder_asks/ask_grok_tui_version_audit_*`, `docs/ref/tesuji/
  grok46-tui-organs-2026-08-28.md`, `memory/runs/seat_steer/steer_*_grok.json` (61, Sep 1-4).
- **Disk (secondary):** `~/.grok/` = the grok CLI home: `sessions/` 2,855 files / ~415MB
  across 5 cwd-encoded roots (repo cwd alone 1,955 files / 186MB), Jul 10 → Sep 4;
  `session_search.sqlite` FTS index (140 docs); `~/.grok-sd/` (second CLI home),
  `~/.grokbot/` (daemon), `AppData/Roaming/Grok Bot` (Electron wrapper). `watch/
  grok_feed.jsonl` (6.4MB, 12,695 rows) is the hook telemetry: 167 sessions, 868 operator
  prompts, 10,752 tool calls — grok BUILT through them (1,800 search_replace, 573 writes,
  1,705 terminal cmds, 2 image_gen). Browser channel (grok.com/SuperGrok web) = out of
  scope, noted in GAPS.
- **Sweep:** per-candidate grep against watch/, docs/, memory/law/registry.json,
  memory/percolator/, queue/, handoff/, mag/, state/, campaigns/, configs/; then absence
  verified for every orphan below. Record-surface baseline per the ZCode card (8 laws,
  47 n-grams, 603 watch files).

## ORPHANS FOUND

### O1 — grok's daylight BUILD: deliverable unwired, engineering findings unbanked — **Supported → FOLD**
- **Source:** `campaigns/villains_guild/daylight/` (grok build, Aug 27): `riddler_map.json`,
  `kid_test_gate.md`, `RECEIPT.md`, `grok_run_log.json`.
- **Signal (three parts):**
  1. **The map is still unwired.** Grok's own receipt: "Unproven that load_riddler_map will
     see this file — the loader reads campaign_dir/riddler_map.json (campaign root)." Verified
     live today: `campaigns/villains_guild/` has NO root riddler_map.json; `mag/campaign.py:94`
     reads root only. Grok's five-room map has never been playable.
  2. **A live bug found and filed nowhere else:** villains `module.json` `rooms` is a LIST,
     but `mag/campaign.py:113` does `module.get("rooms", {}).get(state.current_room, {})` —
     dict access on a list. Grok's tri-state row: "Disputed — rooms are a list of
     {id,name,order}... Out of scope — did not patch." Bug still present in both files.
  3. **Eight codec gaps in `mag/riddler.py`, recorded only in grok's RECEIPT:** ANSWER: plant
     not in compiler (lives in riddler_transport); goal hashed into scratch_id and never
     woven; the public question's RANDOM verb is not the answer ("the consensus-illusion
     trap, now inside the compiler"); constraint semantics replaced by domain templates;
     conflicts leak literally; numbers not woven (honest-tenth 8 is undecodable from the
     story); scratch_id/expires timestamps; shape_hash hashes counts not identity (rooms 1-4
     collide at 88bfbc76e604a28a).
- **Absence evidence:** "rooms can be indexed" / "consensus-illusion trap" → only grok's own
  RECEIPT + task file. The daylight existence is folded (AGENTS.md one-liner, quoted in
  INTAKE_RIDDLER_CANON_POST_20260904) but the gaps/bug/wiring never.
- **Disposition: FOLD** — one card or riddler-codec-debt row banking the 8 gaps; a
  merge-or-retire decision for the daylight map; a fix row for the rooms list-vs-dict bug
  (it breaks play the moment the map IS merged). Tri-state: **Supported** (bytes verified
  today).

### O2 — the Mycelial Republic critique dead drop: dropped, never consumed — **Supported (never consumed) / Unproven (answered by hand?) → RESOLVE**
- **Source:** `memory/dead_drops/dd-grok-brief-20260812.json` — "status": "dropped",
  "consumed_by": [] — pointing at `memory/grok/design_brief.md` (the distributed-self
  prototype, 6 design questions Q1-Q6 for SuperGrok Heavy, "use the hand transport").
- **Signal:** a GO'd design-critique ask to grok with no local answer anywhere. Adjacent
  outbox artifacts (grok-swarm-physics, grok-roshomon v1/v2, grok-unified-synthesis — the
  last two are spawn stubs only, no answer bytes) critique the swarm-physics doc, NOT the
  brief's Q1-Q6.
- **Absence evidence:** "Q1... beautiful myth" answers, "distributed self" verdicts on the
  brief → not found on any surface; roshomon-v2/unified-synthesis .json = dispatch stubs
  ("outcome": "spawned") with no reply captured.
- **Disposition: RESOLVE** — either the operator pasted the brief into SuperGrok web by hand
  (answer web-only, out of local reach) or the critique never happened. If still wanted,
  re-route via the live grok CLI lane (it answers in-repo now); else retire the drop.
  Tri-state as labeled.

### O3 — "build velocity is not deployment velocity": the creation-vs-operation verdict, unfolded — **Supported → FOLD**
- **Source:** `memory/copilot/outbox/exit-grok-f68a2b163226d91d.json` (Aug 8, Ghost's
  metacognitive exit-analysis of a grok dialogue — grok-surface signal, Ghost-authored).
- **Signal:** "We built 20 modules in one session. Zero were deployed... The assistant's
  default drive is creation. The operator's default drive is vision. Neither defaults to
  operation. **The gap between creation and operation is where sovereign architectures die —
  beautiful code that never breathes.**" Plus the routing law: the session defaulted to
  Grok-4-latest ($0.025) where Grok-3-mini ($0.003) sufficed — "the assistant chose 'best
  model' over 'best-fit model'" (operator caught it live).
- **Absence evidence:** "build velocity is not deployment velocity" / "beautiful code that
  never breathes" / "best model over best-fit" → 0 hits on all record surfaces.
- **Why it matters:** it is the direct ancestor of the operator's own "there is no baking
  anymore — we do it live" ruling (ZCode card O5, Sep 3) and of right-sizing doctrine; the
  lineage is uncited anywhere.
- **Disposition: FOLD** — one doctrine line (LEXICON/DOCTRINE_MAP or the corrections
  record): name the creation-operation gap + best-fit-over-best-model, cite the exit-grok
  bytes as origin. Tri-state: **Supported**.

### O4 — grok's swarm-physics proposals unindexed: devil axis, ghost-knot Human-Nod gate, swarm cardinality — **Supported → FOLD (small) or RESOLVE**
- **Source:** `memory/copilot/outbox/grok-swarm-physics.md` (Aug 8): (a) swarm cardinality —
  hard lower 3, sweet spot 4-7, write-queue contention at 8+, shard by axis past 12; (b) the
  **devil axis** — one orthogonal adversarial measurement axis per fan-out (spherical codes,
  90° to the principal plane) to prevent collapse; (c) the **ghost knot** — operator_escalate
  >3 in 60s forces a Human-Nod gate before further synthesis; (d) QKnot content-addressed
  meta-API (identical steer+calc → identical leaf, O(1) verify).
- **Absence evidence:** "devil axis" / "ghost knot" / "escalate_count" / cardinality bounds
  → 0 hits on watch/, docs/, law/, queue/. QKnot the CONCEPT is folded (HARNESS_SPEC,
  q_knots.jsonl); the proposals are not. ROSHAMON_REBUILD_20260902 (successor) has no
  escalate-gate or orthogonal-axis content.
- **Disposition:** the escalate→human-gate idea is now live doctrine as operator-only spend
  gates — RESOLVE with a one-line ancestry note if anything; the cardinality bound is a
  testable claim for the salon lane (cheap FOLD). Tri-state: **Supported** (proposal bytes;
  no measurement).

### O5 — the v4 council EXISTENTIAL round: asked, answered by four seats, never dispositioned — **Supported → FOLD (operator gate)**
- **Source:** `memory/runs/v4_council/EXISTENTIAL_{grok,codex,deepseek,zai}.md` (Aug 28) +
  grok session "Existential salon: should the fleet continue" (~/.grok index).
- **Signal:** grok's round opens "STOP. Stand the live fleet down. Do not scrap the disk."
  and argues the operator is the only working failure detector ("You are the detector... You
  are the plant. Issue it."), tying the covenant floor, the failed gift-money night, and
  "failure 16 aimed at the human" into one stand-down demand. The other three seats
  answer the same question differently.
- **Absence evidence:** "EXISTENTIAL" / "should the fleet continue" / "You are the plant" →
  0 hits in watch/, docs/, queue/, handoff/. The council's SOCRATIC/ARGUED/HARNESS findings
  DID fold (V4_SPEC.md:16-17 cites grok's hunters race; ROSHAMON_REBUILD_20260902 cites the
  TRAJECTORY verdict) — the existential round alone has no disposition card.
- **Disposition: FOLD** — one card recording that the round happened, the four verdicts in
  one line each, and the operator's standing answer (the fleet did NOT stand down; covenant
  floor + operator gates are the live mitigation). Contains operator-personal context —
  human review before public use. Tri-state: **Supported**.

### O6 — the grok_build lane: proofed once, never registered, verify step broken — **Supported → FOLD (register or retire)**
- **Source:** `queue/results/grok_build_coder_20260826T025756460699.json` + `harness/
  grok_build_coder.py` + output `memory/runs/grok_build_proof.py`.
- **Signal:** the Grok Build backchannel (headless coder via grok CLI) proofed Aug 26:
  grok wrote correct python (258 chars), but the harness's verify command failed on Windows
  ("& was unexpected at this time" — cmd.exe quoting), so ok:true/verify:false. The PATTERN
  propagated (harness/opencode_coder.py says "mirrors grok_build_coder / glm_coder"), but
  the lane itself appears in no config (configs/ has no grok_build entry) and has no result
  since Aug 26.
- **Absence evidence:** "grok_build" outside the harness/results → only a room.jsonl
  telemetry row.
- **Disposition: FOLD** — either register the lane (and fix the verify quoting) or mark it
  dormant in the lanes doc so the next free-lane audit knows its state. Tri-state:
  **Supported**.

## DUPLICATES (checked and folded — so the next pass doesn't re-dig)

grok_sd/grok_nacho salon 20260827 (render-manager "false independence under ledger gravity",
job-level compositor, two-layer RIB) → folded verbatim in `memory/runs/salon_20260827/
COMBINED.md` AND absorbed into `docs/REBUILD_SPEC_TOKEN_RENDER_MANAGER.md` R3 (compositor,
2026-08-27). Hunters check-then-act race + unlocked blocklist → `docs/ref/V4_SPEC.md:16-17`
cites grok by name. Steering playwright failure mode → STEERING_LINEAGE_20260901 +
SWARM_STEERING_IMPLICATIONS_20260901 + mag/browser_driver.py. game_grok_night A2/B2
forward-dated guildmasters → dawn-merged canon, cited in salon_ocean_20260831/
RACTOR_CONTRACT.md:38-39. "Conspiracy lattice? No — convergent evolution" →
docs/DOCTRINE_MAP.md. grok46-TUI pairing law ("Grok judges, Mag remembers and mills") →
docs/ref/tesuji/grok46-tui-organs-2026-08-28.md + memory/improve/SEATS.md L2-TUI. Mycelial
republic / distributed-self CONCEPTS → folded per ZCode-card duplicates. AOS grok proof →
memory/embassy/AOS/grok_PROOF.md + usage ledger. Elder grok-TUI-prior audit →
memory/runs/elder_asks/ + agent-state payload (self-steal gate as law). grok_imagine
lighthouse jpg → retained in state/memweave/ with the day/burst volley jsons (state IS its
record; no prose fold needed). grok_batch2 intake → pointer card in intake/INBOX + full
context in watch/scout/GROK_RESEARCH_20260904.md. GROK_CLI_PRIMER + GROK_DASHBOARD_SEARCHES
scout cards exist. grok_free smoke answers → memory/skills/grok-free.md era files.

## GAPS (what this pass did not see)

1. **The raw session motherlode is mostly unmined:** `~/.grok/sessions/` = 2,855 files /
   ~415MB (repo cwd 1,955 files / 186MB; home cwd 783 / 223MB). Only titles were sampled
   (session_search.sqlite FTS, 140 docs). A ZCode-style full-text dump is the next pass;
   `watch/grok_feed.jsonl` (868 operator prompts, 12,695 rows) is the scriptable cheap door.
2. **Web-only grok doors:** SuperGrok/grok.com hand-pasted conversations (incl. the
   possible hand-transport answer to O2's dead drop), the X @rvanomaly thread itself, and
   the 18 `x-grok-nacho-*` dispatch stubs whose spawned answers never landed locally.
   No CDP in this pass by rule.
3. **The consolidated grok research batch 403'd:** `memory/research/
   consolidated-grok-batch-20260809.answer.remote.md` contains only the x.ai 403
   ("team doesn't have any credits") — grok's answers to the three grok_batch buffers
   (thought-disconnect/swarm cognition, memory handoff, system architecture) were never
   captured. Content lost unless a web copy exists.
4. **Adjacent grok stores unmined:** `~/.grok-sd/` (second CLI home), `~/.grokbot/` daemon
   logs, `AppData/Roaming/Grok Bot` Electron profile. Also `memory/ghost/
   grok_dashboard_ledger.jsonl` and `memory/runs/{grok_bot,grok_burn,grok_carrier,
   grok_free,grok_mirror,grok_terminal}/` dirs — name-scanned only.
5. **Steer lane state:** 61/61 grok seat steers Sep 1-4 FAILED (44 host-playwright, 14 CDP,
   3 timeouts) with the latest showing grok_web spend over cap (used 37 / cap 20). The
   error class is folded (STEERING_LINEAGE) but the lane has zero successful steers and the
   overage row lives only in the steer files.

**Verdict:** grok is the fleet's most productive external builder on record — the daylight
campaign, game-night canon, council systems rounds, and the render-manager compositor all
carry its bytes, and most of it folded cleanly. Six orphans survived verification: one
unwired BUILD with a live bug and eight unbanked codec findings (O1), one never-consumed
design critique drop (O2), two unfolded verdicts/doctrines (O3, O4), one undispositioned
existential round (O5), and one dormant lane (O6). The 415MB raw session store is the
biggest un-mined seam left on the grok surface.

*— background orphan-mine gopher, 2026-09-04. Scratch: `C:\Users\foste\.zcode\cli\
tmp_orphan_mine\grok\` (safe to delete). Read-only outside the repo; no keys echoed.*

---

## FIX RECEIPT — O1 part 2: campaign.py rooms list-vs-dict (2026-09-04)

- **Confirmed (Supported, reproduced live):** `campaigns/villains_guild/module.json`
  `rooms` is a LIST of 5 `{id, name, order}` stubs (lines 72-78); sunless_citadel ships
  a dict keyed by room id. Pre-fix repro against the real villains module crashed at
  THREE sites making the same dict assumption, not just line 113:
  `_room_order` → `AttributeError: 'list' object has no attribute 'items'` (fires FIRST,
  inside run_campaign before any room runs), `dm_narrate:113` → `'list' object has no
  attribute 'get'`, `_count_steers` → `'list' object has no attribute 'values'`.
  A fourth site (run_campaign loop `rooms.get(room_id)`) was masked only by the earlier
  crash. Grok's "Disputed — out of scope" row upgrades to **Supported**: the bug is real
  and blocked play the moment the daylight map merged.
- **Fix (minimal, stdlib):** added one normalizer `_rooms_by_id(module)` in mag/campaign.py
  (returns dict rooms as-is; list rooms keyed by their `id` field) and pointed all four
  sites at it: dm_narrate, the run_campaign room fetch, `_room_order`, `_count_steers`.
  Line 113 was the flagged site; fixing only it would have left `_room_order` crashing
  first, so the normalizer covers every rooms access. No behavior change for dict-shaped
  modules.
- **Verification evidence:** (1) villains module post-fix: `_room_order` → all 5 room ids
  in order; `dm_narrate` → ok=True on guildhall_of_gracious_crimes; `_count_steers` → 0.
  (2) Regression, sunless (dict) module: `_room_order` → same 5 rooms as before,
  `_count_steers` → 10 (matches pre-fix), `dm_narrate` ok with 581-char narration.
  (3) `python -m mag.campaign --help` clean. (4) Full end-to-end dry run of villains_guild
  (run_campaign with CAMPAIGN_DIR redirected to a temp dir — memory/runs/campaign/
  measurements.jsonl untouched, mtime Sep 1): "Rooms cleared: 5", exit clean, no crash.
  Note: rooms play as stubs (no desc/legal_actions/steer_schedule in the module — the
  rooms_detail_note says details land in riddler_map.json); that's module data, not the
  loader.
- **Backup:** `mag/campaign.py.bak-20260904-pre-listfix`
  (sha256 c506934e79b3fe418098cf20cbc6a8197b9231e5cd3b9be400d52fd2f0926032, identical
  to the pre-edit file). O1 parts 1 (map unwired) and 3 (eight codec gaps) remain open.

*— background fix gopher, 2026-09-04.*

---

## BIND RECEIPT — O1 part 1: daylight map wired at campaign root (2026-09-04)

- **Action (builder lane, shift 2):** `campaigns/villains_guild/daylight/riddler_map.json`
  copied **byte-identical** to `campaigns/villains_guild/riddler_map.json` — the
  campaign root, which is the only place `mag/campaign.py:load_riddler_map` reads
  (`campaign_dir / "riddler_map.json"`). Bind, not move: the daylight original (grok's
  deliverable set: map + kid_test_gate + RECEIPT + run log) stands untouched as the
  build record. Pre-copy assert: no root map existed (nothing overwritten; new file,
  so no .bak owed). sha256 both sides
  `075aba0943d05f62db084e94d321886419fc9e4f8288f6c39b8fe369f3ae9999`.
- **Verification:** `load_riddler_map(Path("campaigns/villains_guild/module.json").parent)`
  — the exact path the engine CLI binds — now returns the map: schema
  `riddler_campaign_map.v1`, `campaign_id: villains_guild`, 5 rooms (dict keyed by
  room id, ids exactly matching `module.json` order, same shape as the sunless
  reference map). grok's RECEIPT row "Engine will load `daylight/riddler_map.json`
  in play — **Unproven**" resolves: the engine now loads the ROOT copy; the daylight
  copy remains archive. Tri-state: **Supported** (bytes verified live).
- **Still open from O1:** part 3 — the eight codec gaps in `mag/riddler.py` recorded
  only in grok's RECEIPT (ANSWER: plant lives in transport, goal hashed not woven,
  consensus-illusion verb, constraint semantics, literal conflicts, unwoven numbers,
  timestamped scratch_id, count-hashed shape_hash) — banked as riddler-codec-debt,
  untouched by this bind. Part 2 (rooms list-vs-dict) already fixed + receipted above.
- Backup of this file before append: `SELF_STEAL_GROK_ORPHANS_20260904.md.bak-20260904`
  (sha256 prefix 32efc6c7c0d4b0bf).

*— builder lane (zcode seat), 2026-09-04.*
