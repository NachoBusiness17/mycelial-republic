# WIRING DEBT CENSUS 20261001

**Schema:** census.wiring_debt.v1 · **ts:** 2026-10-01 · **lane:** wiring-debt census (ZCode subagent)
**Disease (operator frame):** a proven fix/organ exists in ONE surface while sibling surfaces run
ungated. Patient zero: thinking-off lived at `tools/ds_workhorse.py:55` while `tools/hermes_burn.py`
+ `tools/model_garden.py` ran ungated for months (RIB_INFERENCE_BUDGET_20261001).
**Method:** every row below verified by bytes (grep + read of the named file:line); counts are
line-counts from `grep -rn` over `mag/ tools/ server/ scripts/` at census moment 2026-10-01, tree
state as-is, no commit. Instrument names accompany every number.

## Census rows

### Row 1. Bounded transport queues (CONFIRMED)

- **Organ:** `server/room.py:58` bounded `asyncio.Queue(maxsize=...)` + drop-on-slow publish (the
  Mickey17 W1 harvest, "so the next transport is a door and not a seventh copy").
- **Sibling ungated:** `server/server.py:442` `_grant_session` creates `asyncio.Queue()` UNBOUNDED;
  `server/rooms.py:136-137` broadcasts via `put_nowait` which can never raise QueueFull on an
  unbounded queue, so the drop-on-slow law structurally cannot fire on the LIVE TCP path. A stalled
  peer grows its queue without bound (memory leak + the exact head-of-line freeze shape room.py
  closes). room.py's only consumer is `server/ws_door.py:57`.
- **Cost/risk:** one wedged TCP client balloons server memory; the harvest that fixed this class
  never reached the main door.
- **One-sitting fix:** `_grant_session` passes `maxsize=64` (or delegates member plumbing to
  `server.room.Room`), plus a QueueFull -> drop-peer branch in the broadcast path mirroring
  room.py:128.

### Row 2. Frame MACs on broadcast ticks (CONFIRMED)

- **Organ:** R3 sealed replies, `server/server.py:737-741` `_reply` seals via
  `peer["mac_state"].seal_reply(msg)` (state armed at server.py:526).
- **Sibling ungated:** broadcast ticks "bypass _reply entirely (the encode-once law) and stay bare
  by design" (server.py:738-741 comment); `server/ws_door.py` has zero frame_mac references (the
  second live transport rides fully bare, not even sealed direct replies).
- **Cost/risk:** a tampering middleman edits ticks freely while direct replies are sealed; the
  MAC-sticky tamper detector (server.py:315-321) never sees tampered ticks because ticks carry no
  MAC to check.
- **One-sitting fix:** encode-once + seal-once are compatible: seal the tick bytes once per tick
  with the room-level key (or per-session seals applied at queue-enqueue time), and ws_door adopts
  `server.frame_mac` on its replies.

### Row 3. Atomic writes on shared jsonl/json surfaces (CONFIRMED, one sub-claim refuted)

- **Organ:** `server/store_io.py` `atomic_write_text()` + `exclusive()` (Q21 fix); wired callers
  today: `mag/game_world.py:64,87`, `server/auth.py:74,89`, `server/auth_srp6.py:445,489`, plus
  verkle's own `mag/verkle_knot.py:491` `_write_tip_atomic` and `:545-559` atomic `_rewrite_chain`
  (today's ticket).
- **Siblings ungated (same organ, same file):** `mag/verkle_knot.py:509` EVOLUTION `write_text`,
  `:747/:753` LATEST `write_text` plain. **Siblings elsewhere:** `tools/workflow_gate.py:324`
  appends REGISTRY.jsonl with bare `open(REGISTRY, "a")` while the standing law (2026-09-26)
  licenses 5 CONCURRENT gated workflows each registering rows on every check (Windows concurrent
  append interleave); `mag/effect_broker.py` effects.jsonl append; `tools/hermes_burn.py:61` +
  `tools/model_garden.py:54` usage.jsonl appends; and a long tail of shared state writers on bare
  `write_text`: `mag/agent_knot.py:144,160` (STANDING, EVO_STATE), `mag/scrum.py:127` BOARD,
  `mag/operator_inbox.py:79` INBOX_PATH, `mag/board_tailer.py:56`, `mag/swarm_tools.py:344`,
  `mag/switchboard.py:593`, `mag/act.py:90,175,291,313`.
- **Idiom duplication count:** `os.replace` tmp-rename hand-rolled in 20+ files (verkle_knot x7,
  estate_index_dedup x5, catalog_rescan x4, bay_organs x4, store_io x3 itself, +12 more), i.e. the
  library exists and the estate keeps re-rolling it.
- **Cost/risk:** a torn EVOLUTION/LATEST/REGISTRY write is the same disease as the torn verkle tip
  that froze every chain append (verkle_knot.py:489-490 names that precedent).
- **REFUTED sub-claim:** `watch/inbox/INDEX.json` itself is NOT an ungated sibling: writers append
  to `index_events.jsonl` (append-only log) and INDEX.json is fold-derived
  (`scripts/index_fold_host.mjs:6-8` "KILLS the lost-update race structurally"). Safe by design.
- **One-sitting fix:** verkle EVOLUTION/LATEST switch to `_write_tip_atomic`'s helper; REGISTRY and
  usage appends route through `store_io.exclusive(path)` around read-modify-appends (plain appends
  of one line are tolerable on POSIX; on Windows wrap them).

### Row 4. Effect-broker metering (CONFIRMED, quantified)

- **Organ:** `mag/effect_broker.py:652` `execute()`; docstring law: "Every side effect in MAG must
  route through this broker."
- **Wired:** 3 production modules import it: `mag/harness.py:295`, `mag/state_snapshot.py:169`,
  `mag/swarm_cycle.py:129`. Meter: `memory/runs/effect_broker/effects.jsonl` = 3 rows at census
  moment (first board_write rows banked today per Q48), against 25,427 lifetime cost-rollup calls
  (Q48 receipt).
- **Siblings ungated:** 156 `subprocess` call sites in `mag/` outside the broker (grep
  subprocess.run|Popen|check_output, mag/ only, census moment) vs 2 inside it; direct board writers
  filing notes into watch/inbox/ without a broker receipt: `mag/seat_dispatch.py:275`,
  `mag/lane_runner.py:947,1041`, `mag/arxiv_harvest.py:170`, `mag/ghost.py:1201`,
  `mag/swarm_tools.py:344`, `mag/switchboard.py:593`, `mag/lane_runner.py` watcher crumbs, and the
  tools/ receipt-writers generally.
- **Cost/risk:** cost rollups cannot see unmetered effects; the broker's own founding law is
  unwired. (Many of the 156 are internal ops calls, not headless model effects; the meter that
  matters first is board_write + model_call classes.)
- **One-sitting fix:** enumerate the production-legal headless effect classes (board_write,
  model_call, lane_spawn) and route the ~10 standing producers of those classes through
  `execute()` with corr_ids; leave internal ops subprocesses explicitly exempt by NAME in the
  broker docstring so the census does not re-flag them.

### Row 5. Nonce continuity gate (CONFIRMED)

- **Organ:** per-writer nonce replay protection, checked at `scripts/index_fold_host.mjs:429-432`
  (gap -> warning) ONLY at fold time.
- **Sibling ungated:** the STANDING validate channel `mag/events_scan.py:scan_events_log` (behind
  `mag.shared_surface validate`, the command every client is contract-told to run) has zero nonce
  logic (grep nonce: no match). A nonce gap introduced between folds is invisible until someone
  happens to fold; nothing scheduled folds. `tools/md_record_seal.py:196-216` also reimplements
  nonce computation (last+1 scan) as a second, drifting implementation of the same rule.
- **Cost/risk:** replayed/dropped register events on the shared surface go unwatched on the one
  channel that runs regularly.
- **One-sitting fix:** port the mjs gap check into `scan_events_log` (it already walks every event
  line) so `validate` reports writer-nonce gaps; md_record_seal keeps its writer-side computation
  but the validator becomes the single enforcement truth.

### Row 6. Browser UA on remote fetches (CONFIRMED, quantified)

- **Organ:** the census lane's proven Cloudflare-1010 fix (browser UA header on fetches); carried
  by 44 of 141 files in mag/+tools/ that fetch remote URLs (grep urlopen|requests.get|requests.post|
  urllib.request per file; grep User-Agent per file; census moment).
- **Siblings ungated:** 97 fetching files ride bare library defaults, INCLUDING the patient-zero
  family itself: `tools/ds_workhorse.py` (no UA at its urlopen), `tools/hermes_burn.py`,
  `tools/model_garden.py`, plus `tools/stealth_fanout.py`, `tools/openrouter_free_gate.py`,
  `tools/lens.py`, `tools/duel_harness.py`, `tools/model_bakeoff.py`, ~90 more.
- **Cost/risk:** any of these hitting a Cloudflare-fronted surface eats a 1010 ban and the lane
  reads it as "source dead" (the exact false negative the census lane already paid for once).
- **One-sitting fix:** one `mag/fetch_util.py` (or a header constant) with the estate UA string,
  then a sed-able sweep adding it to the 97; API-key endpoints (deepseek etc.) are harmless to
  carry it too, so no per-file judgment needed.

### Row 7. Liveness/heartbeat for standing loops (CONFIRMED)

- **Organ:** `mag/census_liveness.py` (B2-314) darkness tripwire for logs/census_patrol.log; single
  consumer `main.py:3549`. A second, private heartbeat exists in `mag/agent_cli.py:2359`
  `_start_heartbeat` (pigeonhole liveness beads for sub-agents). The mission's "driver.beat" is
  `mag/compiler_flywheel.py:117` `beat()`.
- **Siblings ungated:** 12 registered standing task families (`scripts/register_{census_patrol,
  corpus_rescan, day_end, endpoint_news, fts_index, gap_sentinel, gate_canary, improve, leave,
  ratchet, tip_witness, x_radar}_task.ps1`) + `scripts/run_mate.ps1` mates runner: only census
  patrol has a darkness reader. The FTS task's darkness condition exists ONLY as AGENTS.md prose
  ("no START stamp for today means the surface is dark") with no attending reader. Bonus zero-caller:
  `compiler_flywheel.beat()` has zero callers (grep beat()/flywheel across mag/ tools/ main.py:
  only agent_cli's own unrelated `_beat`s), so the organ built to be the standing beat is never
  beaten.
- **Cost/risk:** machine-off, logout, or task deregistration silently reopens every "falsifier
  week" the ribs warn about (B2-314 states the class); a dead FTS/patrol/improve surface looks
  identical to a green one.
- **One-sitting fix:** generalize `census_liveness.patrol_status(log_path, max_age_hours)` into
  `tools/standing_task_liveness.py` with a table of {task, log, cadence} rows, wired into
  `mag.cmd doctor` / context-pack output; one row per registered task.

### Row 8. Skills Phase 7 self-feed + room echo writer (CONFIRMED, already receipted; listed)

- Mechanisms prescribed, code absent; receipted in `.agents/skills/ractor-essay/SKILL.md` v1.3
  ledger (Phase 7 gap flagged by DAY1_SKILLS_DOGFOOD) and the room-echo lane's receipt. No new
  bytes needed here; the wiring patrol below is what keeps row-class items from re-accumulating.

### Row 9. inference_budget: the class-kill organ wired into 2 of 184 fire paths (NEW, WORST)

- **Organ:** `mag/inference_budget.py` (RIB_INFERENCE_BUDGET_20261001: "the ONE source every fire
  path imports": FAMILY_TABLE, forbidden-param stripping, max_tokens floors, classify_empty).
- **Wired:** `tools/hermes_burn.py`, `tools/model_garden.py` (the rib's own amendment names these
  two). That is the complete list (grep inference_budget across mag/ tools/ server/).
- **Siblings ungated:** 184 files in mag/+tools/ touch LLM endpoints (grep
  chat/completions|/v1/|api.openai|api.deepseek|api.anthropic|openrouter per file); 182 do not
  import the organ. Standing loop carriers among them include `mag/lane_runner.py`,
  `mag/tesuji_fire.py`, `mag/gopher_lite.py`, `mag/brain.py`, `mag/janitor.py`, `mag/daemon.py`,
  `mag/research_fanout.py`, `mag/scale_salon.py` (one-shot probes make up much of the remainder;
  the patrol distinguishes standing carriers from dead probes). DUPLICATE HAND-ROLLS: 6 modules
  implement their own empty-content/finish-length guards outside the organ (corpus_gap_research,
  corpus_gap_repack, doctor, lane_runner, lite_scale, research_fanout, scale_salon by grep
  empty_content|EMPTY_REASONING), each a future drift copy of classify_empty.
- **Cost/risk:** this is patient zero at 100x breadth: the reasoning-channel burn bug recurred for
  months "in different jackets" (7 paying receipts listed in the rib); every unwired carrier is a
  fresh jacket waiting.
- **One-sitting fix:** wire the ~10 STANDING carriers (loop organs above) to import FAMILY_TABLE +
  classify_empty + guard_terminal; file the two dead-probe exempt classes by name.

### Row 10. claritas face: same shape as row 9 (NEW)

- **Organ:** `mag/claritas.py` (descent protocol leg 2: prompt = claritas face + estate-law block).
- **Wired:** hermes_burn, model_garden, seed tools (8 files reference claritas; 5 non-self).
- **Siblings ungated:** the same ~180 unwired fire paths hand-roll prompts without the face.
- **One-sitting fix:** fold into the row 9 sweep (same carriers, same sitting).

### Row 11. persona_key: zero-caller organ (NEW, w4-41 pattern)

- **Organ:** `mag/persona_key.py` implementing RIB_PERSONA_KEY_20260824 (personality-is-the-
  password gate).
- **Callers:** ZERO external (grep persona_key across mag/ tools/ server/ main.py: only the module
  itself). The gate doctrine is law in the rib; no gate runs anywhere, not even as the server's
  optional identity challenge sibling (server/identity_binding.py exists separately).
- **Cost/risk:** dormant doctrine; a stranger-audit seat cannot be challenged by the mechanism the
  estate believes protects it.
- **One-sitting fix:** either wire persona_key as an optional challenge factor in
  server/identity_binding.py, or mark the module FROZEN-dormant with a reason+date in the rib
  (the freshness-check convention) so the estate stops believing in an unrun gate.

### Row 12. Usage banking breadth (NEW)

- **Organ:** descent protocol leg 8: every paid turn banks tokens+cost; carriers
  `tools/hermes_burn.py:61` and `tools/model_garden.py:54` append usage.jsonl.
- **Siblings ungated:** every other fire path in the 184-file census banks nothing (grep
  hermes_burn/usage|bank_usage: only the two carriers).
- **Cost/risk:** the burn ledger undercounts spend; DRIVING LADDER receipts ("every paid dispatch
  banks usage in its receipt") are structurally unenforceable beyond the two carriers.
- **One-sitting fix:** shared `mag/usage_bank.py` append row (ts, model, tokens, cost, corr_id)
  called from the same 10 carriers as row 9.

### Row 13. RESOLVED counter-example: ram_cache (listed as proof the wiring CAN land)

- RIB_RAM_CACHE_STALE_SNAPSHOT_20260825 documented the frozen-snapshot bug; `mag/ram_cache.py:71`
  now auto-invalidates via `_fingerprint()` comparison inside `load_corpus()`, so the sole
  production caller (`mag/republic_loop.py:205`, still passing no refresh) is healed at the organ,
  not the caller. This is the shape every row above should end with: rib -> organ fix -> sibling
  census -> wiring.

## Counts

- **Known candidates confirmed:** 8 of 8 by bytes (rows 1-8; row 3's INDEX.json sub-claim refuted,
  INDEX.json is fold-protected by design).
- **New-found:** 5 (rows 9-12 incl. two zero-caller proofs: persona_key, compiler_flywheel.beat).
- **Total census rows filed:** 13 (12 disease instances + 1 resolved counter-example).

## PATROL DESIGN

The class is not "bugs"; it is "fixes that land in one place and stop." Three standing checks:

1. **Sibling-surface clause on every fix receipt (amend the receipt law, not the code).** A fix
   receipt is not complete until it carries a SIBLINGS section naming every other surface that runs
   the same risk (found by grepping the organ's export/entry name + the risk pattern), each marked
   WIRED / EXEMPT-BY-NAME / DEFERRED-WITH-DATE. A fix with an empty siblings section is a
   fabrication smell: the ds_workhorse fix had three siblings in its own tools/ directory and none
   were named. Enforce at wave close the way census_drift_patrol reads the carrier line: parse the
   SIBLINGS section shape, fail-closed exit 2 when missing.
2. **Wave-close wiring sweep lane.** One grep-packaged pass per wave close over the wave's touched
   organs: for each named organ export, count non-defining references across mag/ tools/ server/
   scripts/; zero external callers after N waves = dormant organ (persona_key, compiler_flywheel
   pattern); organ exists + risk-pattern grep still hits siblings = wiring debt row. Tool shape:
   `tools/wiring_sweep.py <organ-symbol> <risk-grep>` emitting the row automatically, so the
   census is byte-written, never hand-copied (the hand-written-count lesson, B2-216, applied to
   wiring).
3. **Monthly zero-caller census.** A scheduled task (the 13th standing task, with its OWN
   liveness row in the standing-task table from row 7) walking the organs named in memory/rib/*.md
   (the ribs already name them; parse organ paths from rib bodies) and reporting: imported-where,
   caller count, dormant verdict. Dormant-after-doctrine = either wire it or freeze it in the rib;
   never leave the estate believing in an unrun gate.

**The patrol law, one sentence:** no fix lands alone: its receipt must name every sibling surface
running the same risk, and nothing closes until each sibling is wired, exempted by name, or frozen
with a date.
