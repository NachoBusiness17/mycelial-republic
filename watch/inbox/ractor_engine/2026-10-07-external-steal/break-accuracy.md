# BREAK-ACCURACY - hostile second pass on the external-steal lens (2026-10-07)

Pass rule: every evidence cite re-derived from estate bytes or re-run this
sitting; anything not re-derivable named as such. Commands run this sitting:
`git --version && git worktree list && git stash list`, `git stash list
--format="%gd %H"`, `cmd //c "schtasks /Query /FO CSV /NH"` (full dump,
252 rows), token census on memory/corpus/quantized_thought/
instructions_flash.jsonl via .venv/Scripts/python.exe (case-sensitive
whole-row AND flash-field instruments), input census on memory/percolator/
invariants.json, pytest -q tests/test_context_pack_quantized_laws.py (1
failed, 2 passed in 5.78s, AssertionError "no known compiled law rode the
pack" at tests/test_context_pack_quantized_laws.py:23), grep sweeps for
absolute-path hardcoding (15 hits in tools/+mag/), live fetches:
github.com/microsoft/LLMLingua, github.com/dbos-inc/dbos-transact-py,
github.com/healthchecks/healthchecks, healthchecks.io/docs/http_api/,
github.com/iamlukethedev/Herald-OS, plus reads of the installed litellm
1.98.0 source in .venv/Lib/site-packages/.

## VERDICTS

### F1 law-pack day-lag = "tier capacity and shape, not scheduling" - WEAKENED

Every byte cite reproduced:
- 12 rows in instructions_flash.jsonl (wc -l = 12). compile_report.json:2,9,17-18:
  compiled 2026-10-07T09:10:05Z, in 648 / kept 625 / flash 12. Exact.
- Census reproduces EXACTLY under a case-sensitive whole-row instrument:
  MEASURED ON 2, stash 0, TERMINAL 0, 402 0, Sybil 0, max_concurrency 0,
  worktree 0. (My first pass read TERMINAL 1 - that was my own
  case-insensitive grep matching lowercase "terminal" in row 0's frontier
  field. The lens's instrument is case-sensitive; its numbers are byte-exact.)
  Note the instrument split: in the rendered `flash` FIELD all seven tokens
  are 0; "MEASURED ON 2" comes from whole rows (frontier fields of rows 2-3).
  The conclusion survives both instruments: the rendered tier carries zero.
- FLASH_MAX_CHARS = 220 tools/thought_quantizer.py:118, applied :196
  (to_flash first-sentence slice). max_chars 7200 mag/context_pack.py:165.
  9471>7200 stage-3 L0d shed: memory/runs/mickey17_v2/runs/dogfood2-20261007/
  lanes/d01-seat-boot-pack.checks.json:15. Acceptance test exists
  tests/test_context_pack_quantized_laws.py:17 and is RED at this sitting:
  1 failed / 2 passed, AssertionError "no known compiled law rode the pack".
- Flash=12 is a config knob, not emergent: tools/thought_quantizer.py:375
  `--flash` default 12; mag/estate_bridge.py:416 defaults flash=12, clamped
  :434 (COMPILE_SIZE_CAP). The lens's "raise the tier" move is a one-flag cost.
- LLMLingua external verified live: MIT; `<llmlingua, compress=False>`
  protect tags; rate= and target_token= params; LLMLingua-2 force_tokens and
  use_llmlingua2 PromptCompressor. All as the lens stated.

Why weakened, not confirmed: the headline drops a verified stage. The compile
INPUT, memory/percolator/invariants.json (mtime 2026-10-07T12:59:36Z today,
260,067 bytes), contains ZERO hits for stash, TERMINAL, max_concurrency,
worktree, MEASURED ON, Sybil ('402' substring-hits only). The last-48h
mechanism laws have not reached the percolator input at all - so "no
scheduling component" is unsupported: the producer-ingestion lag IS part of
the measured gap, and it is the stage the original day-lag diagnosis named.
Capacity+shape is real (12/625 at 220 chars; 9471>7200 render shed; test red)
but it is at minimum a TWO-gate gap: (1) laws absent from invariants.json,
(2) tier cap + render budget shed what exists (MEASURED ON proves stage 2 -
those laws ride the pack JSONL and die at render).

The lens's falsifier is vacuous as written: "recompile and re-run the census;
if stash/TERMINAL/402/max_concurrency go nonzero, the diagnosis is wrong."
Those tokens cannot go nonzero from a recompile while absent from the input -
the falsifier passes without testing capacity. To make it test capacity, first
put the laws in the input (producer leg), then recompile, then census.

### F2 worktrees installed, lanes on primary, detector cannot prevent - CONFIRMED (one clause weakened)

- git 2.55.0.windows.2 exact. FOUR worktrees exact: main tree,
  Temp/recovery_pack/baseline (detached e0344fe39), lsa_reboot_staging
  (37e2fba7e), worktrees/salon-arena-mvp (1e92a7012, codex/salon-arena-mvp).
- 3 stashes, SHAs 8b45fe97..., 2902e0d3..., 8baa166e... matching the
  tools/stash_sweep_watch.py:9-10 docstring exactly. No drop/pop verb by
  design: :19-20 and census() :215-238 ("No verb in this tool can drop or
  pop a stash"). Detector uses repo-relative ROOT (:34) and
  CREATE_NO_WINDOW (:48) per the win32 law.
- Weakened clause: "ALL seat lanes still land on the ONE primary checkout."
  The salon-arena-mvp worktree is a live seat checkout owned by
  CodexSandboxOffline (my `git -C ... log` probe failed with "detected dubious
  ownership ... owned by DESKTOP-7C70KSC/CodexSandboxOffline"). At least one
  seat already works from a worktree - the doctrine row the lens wants to
  write partially exists in practice, on a branch the lens did not look at.
- The lens's own falsifier fires: 15 files in tools/ and mag/ hardcode
  C:/Users/foste absolute paths (grep; spot-verified mag/boot_check.py:33 -
  a .zcode per-project memory path keyed to the primary checkout - and
  tools/path_lint.py:24 STRAY_PREFIX). Migration friction is real: a
  worktree seat gets a different per-project session-memory key, and
  cross-user worktrees hit dubious-ownership. The 45-min probe underprices
  this; the detector remains a needed defense alongside migration, as the
  lens concluded.

### F3 402 wall computable in advance; LiteLLM shape = ADAPT not adopt - CONFIRMED (one imprecision corrected, one OWED cured)

- watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md:37-44 verbatim: A1
  sonnet reserve 0.0999 + 24000x1e-5 = ~0.34 vs balance bounded [0.16, 0.17);
  A2/A3 haiku ~0.13 paid. "8 hourly MagHermesBurn247 fires" independently
  byte-backed at tools/hermes_burn.py:443 ("The 10-06 402 wall burned 8
  hourly fires on A1") and :371 ("~8h").
- tools/hermes_burn.py:69 exact import line (guard_terminal, plan_call,
  skip_terminal). TERMINAL mint :259-261 exact (marker = ask_dir / "TERMINAL"
  at :259). Entry half + mint halves inside :368-443 confirmed.
  spend_balance.v1 at tools/cost_rollup.py:305-335 (schema string :319).
- LiteLLM 1.98.0 installed in this venv. BudgetExceededError raised in
  litellm/proxy/auth/auth_checks.py (:3927 key-budget check; also 536, 832,
  1278, 3967, 4203); soft_budget is alert-only, verified :3989-4015
  (asyncio.create_task budget_alerts, no raise); License-Expression: MIT
  (dist-info METADATA:108).
- OWED CURED by this pass: the exact HTTP status is 429 -
  .venv/Lib/site-packages/litellm/exceptions.py:972
  `self.status_code = 429` (v1.98.0), with unified rate-limit category
  fields at :982-983. The "401 vs 429" conflict in the lens's search
  summaries resolves to 429 in the installed version.
- Imprecision corrected: "the estate already imports (plan_call/guard_terminal)
  but does not wire as a dispatch gate" is loose. plan_call IS wired per call
  (tools/hermes_burn.py:434-437: plan feeds max_tokens into _call). What is
  missing is the reserve-vs-balance leg - and it cannot be live-computed:
  all 8 provider balance endpoints returned 404 (HERMES_402_WALL_20261007.md
  lines 20-25), so the probed-floor design in the lens's move is the only
  computable form. The conclusion stands; the wording was wrong about which
  leg is unwired.

### F4 FullScan 429 storm = outcome-signal class; dead-man's switch = the 10x - CONFIRMED (scope narrowed per its own falsifier)

- queue/todo.md:233 verbatim: 20,578 parsed rows 09-24 to 10-06, zero ok:true,
  20,432 "[429]" fail rows, 47 TimeoutError rows, Last Result 0 = exited-not-
  classified. Live this sitting: my schtasks dump reads
  "\Estate FullScan","N/A","Disabled" - consistent with the ask's 10-07 disable.
- All five named scripts exist: census_patrol_daily.ps1, fts_index_daily.ps1,
  hermes_burn_247.ps1, improve_daily.ps1, lawpack_daily.ps1 (scripts/ ls).
- The pre-registered falsifier fires exactly: scripts/census_patrol_daily.ps1
  :14-29 carry COLLECT-DRIFT / STALE / cannot-verify outcome semantics with
  attention.md alert blocks, and scripts/fts_index_daily.ps1:12-22 carries an
  exit-code contract (alert block lands in memory/attention.md, nonzero exit
  carried to Last Result). Two estate tasks are NOT dark. My fleet census:
  21 active Mag*/estate tasks (schtasks dump); 2 verified outcome-gated; the
  remainder not individually read - the exact blind count is OWED, but
  "at least 5 more" is directionally safe and an undercount.
- External verified live: healthchecks BSD-3-Clause, per-check Period and
  Grace, SQLite default store, 3,956 commits (active); /fail endpoint now
  verified against healthchecks.io/docs/http_api/ ("Signals to
  Healthchecks.io that the job has failed") - the lens's fetch is confirmed
  where my first repo-page fetch could not see it.
- Sharpening: the estate already owns the pattern in two tasks (exit-code
  contract + log verdict + attention.md alert). The 10x is GENERALIZING the
  in-house census-patrol outcome grammar across the ~19 unverified tasks -
  zero new dependencies - with healthchecks as the design reference, not an
  import. Also: the FullScan re-seed decision already exists as a queue item
  (queue/todo.md:234, kill-or-repair, groq lanes wrote 18,327 fail rows,
  nvidia TimeoutError 47) - the zero-ok tripwire should hook that item, not
  duplicate it.

### F5 fold gate / DBOS - CONFIRMED on the evidence present; REPORT TRUNCATED

- tools/fold_gate.py:24 exact ("On wait timeout acquire exits 4 and LOGS
  it"); :41 exact ("SCOPE (2026-10-07, morning-block m5)"). Confirmed live.
- DBOS verified live (github.com/dbos-inc/dbos-transact-py): MIT license
  label; "checkpointing its state in Postgres"; "entirely contained in this
  open-source library, there's no additional infrastructure" (embedded
  library vs Temporal's externally orchestrated server); resume-from-
  checkpoint and exactly-once event semantics per README. The lens's exact
  copyright line "(c) 2024 DBOS, Inc." I did NOT byte-verify (LICENSE file
  not opened; page shows MIT only) - carried as the lens's fetch.
- The finding and move fields for this item never arrived in the report as
  received (evidence string cuts mid-sentence at "embedded library"). The
  verdict is on evidence bytes only; no finding-level claim is assessable.
  On the DBOS evidence gathered: ADAPT (checkpoint-resume semantics), not
  wholesale adoption - the estate's 200-line fold_gate already implements
  acquire/stale-break/release/wait-timeout logging; the missing piece vs
  DBOS is checkpoint-resume of the fold WORK, partially covered by
  FOLD_SECTIONS + receipt trails.

## ADDITIONS (what the lens missed)

1. HERALD-OS BYTE-CHECKED - the ask named it; the lens never covered it.
   github.com/iamlukethedev/Herald-OS exists: MIT ("builds on Hermes Agent
   by Nous Research, also MIT"), approval gates real ("Every action that
   changes something goes through a permission system you control"; mutate
   tools ask first with allow-once/always; destructive tools ask EVERY time;
   four permission tiers, read/act run straight away; audit log + Hermes
   approval card). The ask's "token-tier implementation" reading is WRONG:
   there is no per-agent token budget mechanism - only a Usage view with "a
   warning at 90%". Verdict shift vs the ask's framing: ADAPT the gate
   taxonomy (read/act/mutate/destructive + destructive-asks-always), STEAL
   nothing on the token side. Falsifier: read the gate implementation files;
   a hard budget threshold beyond the 90% display upgrades it to STEAL.
   Move (30 min): map the four tiers onto the estate's effect-broker verbs.

2. WINDOWS DUBIOUS-OWNERSHIP is a named worktree hazard the lens missed:
   the CodexSandboxOffline-owned salon-arena-mvp worktree refuses cross-user
   git ops ("detected dubious ownership", this sitting). A worktree-per-seat
   doctrine needs safe.directory policy or per-seat ownership or seats lock
   each other out. Rides F2's move as a required test case.

3. THE 402/429 CONVERGENCE: BudgetExceededError carries status_code 429 and
   unified rate-limit category fields (litellm/exceptions.py:972,982-983,
   v1.98.0) - a budget wall and the FullScan 429 storm are the SAME
   downstream signal class. The F3 TERMINAL-marker pattern and the F4
   zero-ok tripwire should share one outcome-row schema so one tripwire
   grammar covers both walls. Move (15 min): spec the shared row schema
   before writing the FullScan tripwire.

4. PRODUCER LEG FOR F1: mine the 10-06/10-07 receipts (stash_sweep_watch.py
   docstring, HERMES_402_WALL_20261007.md, the max-concurrency envelope law)
   into memory/percolator/invariants.json or a vault amendment BEFORE the
   recompile - otherwise the census stays zero and the acceptance test stays
   red for reasons no prefix touches (verified: 0/7 token hits in the input
   at 12:59:36Z today). Falsifier for this addition: if tonight's recompile
   renders stash/TERMINAL nonzero without touching the percolator (laws
   entering via rib-vault amendments on the L0d carrier path instead), my
   producer-leg claim is wrong for that path.

5. WHAT NOT TO BUILD (convergent with the lens where it said it): no
   LiteLLM proxy import - spend_balance.v1 + plan_call already carry the
   shape in ~100 lines; no Temporal/Airflow server for folds - the DBOS
   evidence itself shows embedded-library is the only shape that fits a solo
   desktop, and fold_gate.py already holds the mutex semantics.

## MOONSHOT FRAME (ask)

The outcome-signal class (F4) is the 10x: it converts ~19 dark schtasks into
self-alarming surfaces with one shared row grammar and retires the recurring
"dark for N days" incident species estate-wide; every other steal is a
single-surface fix. Honest scope: 2 of 21 tasks verified gated, the exact
blind count OWED.

## NOT RUN / OWED (disclosure)

- Did not run the full test suite or the ratchet/citation gates - not in
  this pass's mandate; the one test the lens's move names WAS run (red,
  confirmed).
- LLMLingua verified via repo README fetch (the lib is not installed here);
  its compress_prompt internals not executed.
- DBOS copyright line, healthchecks latest-release date, and the exact
  count of dark estate tasks: OWED, marked as such, not asserted.
- The lens's F5 finding/move fields: not received; nothing fabricated about
  what they said.
