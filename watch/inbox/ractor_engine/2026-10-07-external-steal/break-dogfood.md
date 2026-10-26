# BREAK-DOGFOOD: hostile second pass on the external-steal lens (2026-10-07)

Pass: break-dogfood (hostile byte-check of the lens report). Every cite below was
read or run THIS sitting unless marked OWED. No em-dashes. Shell: Git-bash grep +
.venv python from the repo root. The lens report handed to me truncates mid
finding-4 evidence ("with Per"); findings for gaps 5/6/7 and the moonshot ranking
were not in evidence and could NOT be byte-checked (see OWED).

## Verdicts

### f1 memory-propagation (gaps 1+6): CONFIRMED, move acceptance amended, falsifier partially refuted

Verified byte-level this sitting:
- "Steal from Microsoft LLMLingua" is at mag/context_compression.py:3, NOT :6
  as cited (line 6 is the Ghost Friedman quote). Cite erratum, substance holds.
- The second LLMLingua filing is mag/frontier_scout.py:204-205 ("Context
  Compression - LLMLingua / prompt compaction", "Microsoft LLMLingua paper"),
  NOT mag/context_admission.py as the lens said. context_admission.py:1-11 is a
  dispatch-admission preflight rib ("does not call a model"), verified by read.
  So "filed twice and wired nowhere" is TRUE but the lens named the wrong twin.
- Import census (the check the lens reported as "grep exit 1, zero hits"):
  `grep -nE "^(from|import) " mag/context_pack.py` returns hashlib, json, os,
  re, time, datetime, pathlib, typing, config.ROOT, mag.constants.PACK_STALE_DAYS.
  Zero imports of context_compression / context_admission / thought_quantizer
  (import-scoped grep exit 1). Erratum on the lens's instrument: the plain
  "admission|compression" grep is NOT zero (1 comment hit, context_pack.py:722);
  the true statement is "zero imports".
- Primary source, not just the d01 receipt: watch/inbox/PACK_OFFLOAD.jsonl row
  `{"ts": "2026-10-07T08:29:23.620900Z", ... "mode": "full", "max_chars": 7200,
  "total_chars": 9471, "shed_sections": ["L0d rib vault amendments"], "stage": 3}`
  byte-exact.
- Render state on disk: memory/context_pack_latest.md mtime 2026-10-07 13:40:36
  -0400, 7277 bytes; grep counts: MEASURED ON 0, Sybil 0, max_concurrency 0,
  marathon 0 (L0d 1, as a shed-receipt echo). The shed persists on renders made
  AFTER the d01 lane's 08:29Z run.
- Suite reproduced (the check the lens flagged not-run): I ran
  `.venv/Scripts/python.exe -m pytest -q tests/test_context_pack_quantized_laws.py
  tests/test_rib_boot_amendments.py tests/test_boot_regen.py tests/test_thought_quantizer.py`
  = **1 failed, 41 passed in 11.30s**, failing
  tests/test_context_pack_quantized_laws.py:23
  test_quantized_laws_section_renders_in_default_budget, AssertionError
  "no known compiled law rode the pack". Matches the d01 receipt (1 failed /
  41 passed in 10.76s) plus my own in-process render at 13:44:36Z.
- FLASH_MAX_CHARS = 220 at tools/thought_quantizer.py:118 verified; my scan of
  memory/corpus/quantized_thought/instructions_flash.jsonl (12 rows) shows
  rib1:RIB_MOD and rib2:RIB_INF flash fields at exactly 220 chars with no law
  bytes while their frontier fields (1796 / 2065) carry MEASURED ON. The
  day-lag-is-shedding clause is confirmed: the compiler is healthy (d01:
  schtasks Ready, Last Result 0) and the fresh pack still ships no mechanism
  bytes to a flash seat.
- External leg re-verified by fetch: microsoft/LLMLingua is MIT and supports
  protected spans via `<llmlingua, compress=False>` in
  structured_compress_prompt. The estate module wires none of it.

Move verdict: the PROTECTED_SECTIONS L0d move targets a real organ (the stage-3
shed that kills MEASURED ON via the L0d amendment-body carrier,
mag/context_pack.py:1350-1351), but its second acceptance is WRONG:
- I reproduced the render in-process (`build_context_pack()` +
  `format_context_pack_text()`, mode=full default): render 7196 chars,
  "Verify with git diff" False, "Elevate with a deliberate ask" False.
- The phrases DO exist in the flash pack: row a77444ced5ab (flash field 63
  chars) carries "Verify with git diff", row 212719f4b54d (flash field 120)
  carries "Elevate with a deliberate ask". They survive the 220 field cut.
- They die at the compiled-laws SLICE: _quantized_laws() returns 1642 chars
  WITH both phrases, but full mode caps the render at
  `max_laws: 1200` (mag/context_pack.py:161-167) applied at mag/context_pack.py:1264.
  Byte-experiment: s[:1000] no, s[:1200] no, s[:1800] yes for both phrases.
- A memory-wide grep finds the phrases in NO law carrier outside
  quantized_thought (only memory/agent_sessions/orc-*.json echo rows), so L0d
  protection cannot add them. The red test will stay red after the lens's move.
Falsifier verdict: partially refuted. The falsifier's relocation target
(FLASH_MAX_CHARS=220) is NOT the red test's organ (the fields carry the
phrases); the real organ for the test is the full-mode max_laws=1200 slice.
FLASH_MAX_CHARS=220 remains the true organ for why MEASURED ON-class law never
rides the L0b flash slice. Amended one-sitting cure for the test (~10 min):
raise full-mode max_laws to >=1700 at mag/context_pack.py:167, or reorder
quantizer output so the two short law rows precede the five 220-char amendment
headers; acceptance: rerun the same 4-file pytest set, expect 42 passed.

### f2 multi-seat contention (gap 2): CONFIRMED, falsifier premise mischaracterizes R3, probe needs a guard

Verified byte-level this sitting:
- `git worktree list` shows exactly the two cited trees with exact hashes:
  lsa_reboot_staging 37e2fba7e [reboot-staging-20261003],
  worktrees/salon-arena-mvp 1e92a7012 [codex/salon-arena-mvp]. ADDITION the
  lens missed: a THIRD linked worktree exists,
  C:/Users/foste/AppData/Local/Temp/recovery_pack/baseline e0344fe39 (detached).
- tools/stash_sweep_watch.py:4-11 carries the R3 incident bytes (a `git stash`
  mid-landing captured another lane's eleven executor files on HEAD ebcd2583d;
  three sweep stashes HOLD-RECONCILE), :12-23 the check/census contract with no
  drop/pop verb. Verified by read. Live: `git stash list` = 3 entries
  (stash@{0..2}), matching the header census.
- Falsifier cite verified: mag/agent_cli.py:2251 `_sync_current` mirrors seat
  state into state/CURRENT.md (shared header surface exists).
- cr-sqlite steal confirmed at watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md:47-52
  ("kills the stash-sweep class for ledgers").
- Falsifier FLAW: the lens calls R3 "the untracked-drift class", but the
  detector's own bytes say the sweep captured working-tree MODIFICATIONS
  (tracked; stash_paths surfaces "tracked changes only, the sweep surface",
  tools/stash_sweep_watch.py:83). R3 was a tracked-modification sweep.
- Probe refinement (my census): `git stash show --name-only` on the three live
  stashes shows captured paths catalog/, configs/, AGENTS.md, .gitignore,
  Dockerfile, dashboard trails. A fresh worktree has NO detector state file, so
  all 3 stashes re-evaluate on first check; if the probe lane's "real edit"
  touches any of those surfaces inside the 900s window, check FIRES as a
  false positive. The probe should run census first or edit outside the
  captured set. Deeper mechanism note: `git rev-parse --git-common-dir` = .git
  and the 3 stashes are repo-global, so worktrees isolate the working
  tree/index (the actual R3 damage surface) but NOT the stash namespace; the
  detector stays valid inside a worktree because it reads the shared stash
  list and window-scopes mtimes to the given root.

### f3 judgment-tier blindness (gap 3): CONFIRMED, port cheaper than priced

Verified byte-level this sitting:
- tools/hermes_burn.py:34-43 carries TERMINAL IS TERMINAL (2-consecutive
  transport-failure mint, evidence-preflight instant mint, data-row banking,
  402 wall context). Cite :34-41 is accurate for the law block.
- watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md:59-70 verified:
  spend_balance.v1 writer + "grand_total_usd 231.0322 over 28,553 calls".
  Attribution nuance: the writer lives in tools/cost_rollup.py (receipt item 2),
  not in hermes_burn itself.
- Sibling zeros verified with TWO instruments so the lens's zero is not a
  dialect artifact: `grep -cE "TERMINAL|spend_balance"` = 0 and plain-BRE
  `grep -c "TERMINAL|spend_balance"` = 0 for both tools/grok_burn.py and
  tools/box_burn_watch.py. Also zero 402/balance/paid-skipped lines in
  grok_burn.py. The class gap is real.
- ADDITION: the mechanism is already factored into a shared module the lens did
  not name: mag/inference_budget.py has plan_call (:268), skip_terminal (:339),
  guard_terminal (:349), and hermes_burn imports them (tools/hermes_burn.py:69).
  The port to grok_burn.py is import + wiring, likely under the 90-min estimate.
  The acceptance shape is already proven live at HERMES_402_WALL_20261007.md:71-77:
  the carrier self-minted TERMINAL at 09:11:39Z and the next fire printed
  "paid 0 skipped 3 failed 0" exit 0.
- External leg re-verified by fetch: LiteLLM virtual keys track per-key spend
  in LiteLLM_VerificationTokenTable via completion_cost(), max_budget +
  budget_duration (+ temp_budget_increase). Same self-accounting class as the
  lens claimed. Falsifier (burst-429 vs balance-402) is plausible, untested here.

### f4 scheduled-drain storms (gap 4): CONFIRMED as far as the evidence runs; in-estate prior art missed

Verified byte-level this sitting:
- Commit eb7e1529c (2026-10-07 08:06:06 -0400) message byte-contains
  "FullScan drain closed DRAIN DEAD - 20,578 rows zero ok true".
- tools/meter_patrol.py:1-30 verified (rides MagCensusPatrolDaily via
  scripts/census_patrol_daily.ps1 at :11-12; RECEIPT/NOBS states :15-22);
  `grep -inE "schtasks|stale|heartbeat"` exit 1, zero hits. The lens's absence
  claim is byte-true on those tokens.
- ADDITION (sharpening, not contradiction): meter_patrol DOES carry next-run
  GAP logic (exit 1 = a metered day with zero rows, :44-45, alert print :240),
  so "no stale logic" overstates; the honest organ split is: next-run gap
  naming exists, silence-while-dark detection does not. A dead task is invisible
  to every pull-based gate, which is exactly the FullScan disease (11 dark days).
- ADDITION (in-estate prior art the lens missed): the push-side darkness gate
  already exists for the lawpack surface: mag/boot_regen.py:26 "a dark task
  turns context-pack exit 2 within one" cycle + the operator card at
  scripts/lawpack_daily.ps1:26-30 ("no START stamp for today means the surface
  is dark", re-register + rerun). Gap 4's verdict should be ADAPT: wire
  FullScan and the burn crons into the proven boot_regen-style gate first;
  Healthchecks (BSD-3-Clause, ping + Period/Grace + sendalerts poller,
  re-verified by fetch this sitting) adds only the external silence leg for
  consumer-less tasks. Do not build a new watchdog from scratch.
- OWED (lens blind spot #4, still open after my pass): the computing-lane
  receipt with the per-row census behind 20,578. I searched watch/inbox for
  "20,578" and found only this run's sibling lane reports (accuracy.md,
  break-accuracy.md, break-economics.md, break-operations.md); the commit
  message is the strongest estate byte I verified.

## What the lens's blind spots I closed vs still open

Closed this sitting: estate suite run (4-file set, 1 failed / 41 passed,
11.30s, command above); live render path (in-process build + on-disk 13:40Z
render grep; I did NOT run the mag.cmd context-pack CLI itself since it rewrites
memory/context_pack_latest.md and the two renders above cover the render path);
LLMLingua license + protect-span mechanism; Healthchecks license + ping/grace
mechanics; LiteLLM budget mechanism. Still OWED (not verified by the lens nor
by me): Nomad / Ray / k3s licenses and dispatch mechanisms, OpenRouter limits,
Helicone, Herald-OS gate + token-tier file-level read, the moonshot economics
(detection-lag cost vs per-boot context tax; the only new datum I add is that
the per-boot tax is bounded and measurable: full renders sit at 7196-7277 chars
against the 7200 budget with the L0d carrier and the law slice lost every boot,
while detection lag has one banked 11-day incident). Gaps 5/6/7 findings and
the moonshot ranking were not present in the report text I was handed and are
OWED to any next pass.

## CONVERGENT flag

Findings f1, f2, f3 are CONVERGENT: each is independently carried by (a) the
ask's own gap inventory, (b) the d01/d02 lane receipts or the 402-wall receipt,
and (c) my re-verification this sitting. Three-source findings outrank
single-source ones per the duplication-is-emphasis law.

## Receipt

Banked at watch/inbox/ractor_engine/2026-10-07-external-steal/break-dogfood.md.
Instruments this sitting: git worktree list / git show -s / git stash list /
git stash show / git rev-parse --git-common-dir; grep (ERE and BRE dialects);
.venv python for the flash-pack scan, the _quantized_laws slice experiment, the
in-process render, and the 4-file pytest run. No files edited outside this
receipt; no renders of memory/context_pack_latest.md by the CLI.
