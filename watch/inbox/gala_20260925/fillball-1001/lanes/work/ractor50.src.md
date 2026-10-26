== operations.md ==
# OPERATIONS RETRO + DOCTRINE DELTA (ractor50 operations lane, division B, 2026-09-30)

Moment note: the lane ran on local date 2026-09-30; its check battery's UTC
stamp reads 2026-10-01T01:20:38Z (one clock, two zones; both named here).

The owed waltz: mine the gala/mine waves for operational failures and their
landed-or-owed mechanism fixes, then write the ask-shape and fold-shape rules
the next 50 waves run under. Every claim below cites a receipt path or a
command run in this lane's session (raw output:
watch/inbox/gala_20260925/ractor50/lanes/operations.check.txt). Lane JSON:
watch/inbox/gala_20260925/ractor50/lanes/operations.json.

## The eight failures

### 1. fold_gate 127 (the fold that never ran)

- Wave: gala wave5-repair (dwfrun-1357d4f7, 2026-09-29).
- Failed: the fold gate spawn `world.run("bash", [FOLD_SH, LANES, N])`
  (the-gala.dwf.ts:269 pre-edit) exited 1 with a WSL execvpe error; a later
  variant exited 127. Bare `bash` resolves to System32's WSL launcher before
  PATH; WSL bash cannot exec the gate's Windows venv python.
- Changed: estate-root `bash.exe` shim (cwd-precedence interception to Git
  Bash, gitignored, receipt comment in .gitignore) + `wsl --set-default
  Ubuntu`; then fold_gate.sh gained a fail-loud guard (exit 2, "wrong bash:
  ... this gate is Windows Git Bash only"). Receipt:
  watch/inbox/gala_20260925/wave5-repair/fold-gate-repair.md (both defects,
  incl. Defect 2: 7 stray QC JSONs in the lanes archive broke the count,
  moved byte-preserving to lanes/_qc/). ball-20260929 fold-gate lane made the
  wrong-bash path exit 2 by script (fold_gate.sh:14-24, verified on disk).
- Byte checks this session: fold_gate.sh guard lines present (sed 1-30);
  bash.exe shim at estate root present (ls). Live gate re-run against this
  lane's archive: exit 0 GATE PASS (see check file).

### 2. OLM double-death: journal order + glob

- Wave: frontier olm-mine, dwfrun-279d66b4 (2026-09-29, journal-order death)
  and dwfrun-aa9969b0 (glob death, world-read failure after the fold had
  already written, killing a completed mine). Both run records exist on disk
  (.zcode/workflow-runs/, ls verified this session).
- Failed: (a) report() fired interleaved with agent settlement, so the journal
  replay hit InputHashMismatch on a deterministic-replay run; (b) a wide
  `files.glob(OUT + "/*.md")` after the fold rejected once at the exact
  receipt-existence site and the rejection killed the script.
- Changed (both wired into the saved script .zcode/workflows/olm-mine.dwf.ts,
  comments at lines 198-201 and 448-458): determinism law (agents created and
  asks issued in fixed array order; report() fires only AFTER allSettled, in
  fixed order) and the single-file receipt glob wrapped in catch that routes a
  missing/failed glob to a folder repair ask instead of script death, plus a
  digest publish failure routed to a rewrite-then-republish ask.
- Still owed: nothing in the script; the 2026-09-30 rewrite also made the run
  date a caller slug (replayable scripts cannot read clocks). Owner: none
  open.

### 3. Registry pollution (the seatlaw_* rows)

- Wave: the payload-gate work (commit 26eacaae7 era, 2026-09-29; receipts:
  watch/inbox/48h_synth/laws.md section 6, watch/inbox/frontier_olm_20260928/
  RECEIPT.md:79).
- Failed: every pre-write gate-check of in-flight workflow-script payloads
  called workflow_gate check, which appends a REGISTRY row, so every temp
  .dwf.ts Write minted a junk row pointing at a %TEMP% file that died
  milliseconds later. Census this session: memory/workflows/REGISTRY.jsonl
  holds 40 rows, 4 are seatlaw_*/t69dbg Temp rows (3 FAIL, 1 PASS).
- Changed: tools/workflow_gate.py `--no-register` flag (help text carries the
  cause; verified on disk at the argparse block, lines ~283-287) + early
  return keeping the exit contract; caller tools/seat_law_gate.py:50 passes
  it. The 4 junk rows STAY per append-only law. This lane followed the same
  law: baseline gate check ran --no-register (verdict only); only the landed
  script change minted its row (ts 2026-10-01T01:16:55Z, digest 2285b0104993,
  PASS).

### 4. 1302-burst lane deaths

- Waves: 50-wide Tree Doctrine dig dwfrun-15738edf (2026-09-25 18:59Z: 1,838
  429/1302 log lines, workflow children maxAttempts 0, every digger dies on
  first attempt; corpus/steal/TETHERED_LINK_STEAL_20260925.md); dwf child
  census 09-20..09-26: 896 model.network.failed, 850 429-retryable, 817 the
  1302 shape, 11 terminal actors in 2 runs invisible to the tally
  (watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md);
  afterparty width ~15: 2 rate-limit deaths, refired to completion;
  width 12 after a burst: 1302s until the window decays
  (watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md).
- Changed: the B2-476 source-cited envelope contract (proven-width table,
  clean rungs measured per transport; workflow children have NO measured
  clean rung, safe width strictly below the Task-agent rung of the same day;
  rolling throughput is the binding constraint; hold fires ~10 min on 1302),
  registered in AGENTS.md fan-out width law + max-concurrency standing law;
  the-gala's refire-once + evidence-banked burial (laneWithTiers). Wired this
  sitting: the-gala.dwf.ts now holds ~10 min before the single refire when a
  lane death carries the rate-limit shape (rateLimitHold, see section below).
- Still owed: (a) tools/provider_error_tally.py `--dwf-run` attribution mode
  (B2-443's registered owed build; grep for dwf-run in the tool: 0 hits this
  session) - owner: the next observability/operations wave; (b) the 15-16
  rung stays untested, probe armed NOT fired
  (watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md), fires
  only on explicit operator GO - owner: operator.

### 5. Shared-index commit races

- Waves: w1 b2-stone2b (a concurrent writer re-folded a verkle knot mid-run;
  flags survived, observed benign, watch/inbox/gala_20260925/w1/lanes/
  b2-stone2b.json fix 2); wave5-repair queue-closes (its surface rebuild
  absorbed other lanes' 130 concurrent registers; stale 11 + missing 2 were
  "minted by concurrent sibling-lane writes during the run"; validate's last
  error was a moving target of sibling live-append files,
  watch/inbox/wave5_repair/queue-closes.md:58-74); config-hygiene (a
  concurrent stealth_driver cycle re-drifted mirrors.json mid-lane, second
  named re-seal required); B2-108 (a stale rbxlx build rode commit 790145ab1
  and had to be re-committed scoped, 027baff4c).
- Changed: single-writer doctrine for shared ledgers (filer system prompt:
  "Sequential single-writer appends only; dedupe before appending",
  the-gala.dwf.ts; runner-side --read-only strip single-writer implementation,
  w3 a15-mag-organs.json row); the standing surface-rebuild verb (mag/
  surface_rebuild.py, `python -m mag.shared_surface rebuild [--dry]` and
  `mag.cmd surface-rebuild`, WO-10 closed: truly-invisible 93 to 0, stale 28
  to 0, missing 5 to 0, mag/estate_bridge.py:149 receipt pointer); drift-keyed
  batch flips abort on line+snippet mismatch (WO-12 sweep instrument);
  config_seal verify wired into pre-push (b2-stone2b fix 4).
- Still owed: a standing cadence for surface-rebuild (validate does not hold
  ok=True on a live tree while sibling lanes append; the verb re-reaches 0/0/0
  at any census moment; folding it into a daily patrol is an operator call -
  queue-closes.md residual) - owner: operator.

### 6. Fold invisible-items 224

- Wave: flash50 census (watch/inbox/burn_reset_20260927/flash50/s2-23.md:127):
  "Registered but unfolded: 224 items in the log beyond the stale materialized
  INDEX (1639 fresh vs 1415); flash50 alone 170 (184 vs 14)." Also: 17 amend
  events never applied their new sha; a python-copyfile twin bypassed the
  PostToolUse seal and was invisible to the fold entirely (postscript).
- Changed: w1 b2-stone2b fix 7 (`node scripts/index_fold_host.mjs rebuild`
  folded 2488 events into 730 active items; fold was one event stale at 729),
  then the standing verb (surface_rebuild, WO-10, heals invisible/stale/
  missing through the fold's own writer verbs, idempotent, 3 tests passed);
  the sanctioned-writer law (never hand-edit INDEX.json, register through
  index_fold_host add at final bytes).
- Still owed: the standing cadence (same item as failure 5; the two share one
  mechanism). Owner: operator call, named above.

### 7. Wave5 seal churn

- Wave: wave5-repair config-hygiene (watch/inbox/wave5_repair/config-hygiene.md).
- Failed: config-seal verify red at modified=4; after the sanctioned re-seal a
  concurrent stealth_driver cycle rewrote mirrors.json (a live-writer state
  file living inside a push-blocking configs/ seal) and the verify went red
  again mid-lane; a second named act re-sealed it.
- Changed: per-file verdict discipline before any restore-vs-reseal decision
  (restore-bytes rejected with reasons for all 4; "restoring would time-travel
  the estate" / "destroy a concurrent lane's registry work" / "corrupt driver
  state"); named re-seal notes carry per-file reasons; the two silent-soft
  config readers now fail loud (ProviderConfigError / FileNotFoundError, both
  with regression guards).
- Still owed: the structural fix - move mirrors.json out of configs/ or exempt
  live-state files by name; it will drift again on the next stealth cycle
  (config-hygiene.md "Owed / stated plainly") - owner: operator decision. Also
  the seal scope gap (config_seal.py:36-43 globs top-level only, subdirectory
  configs unsealed) recorded, not fixed.

### 8. Width envelope history 3 -> 12 -> 50

- Waves: the 50-wide dig (storm, 2026-09-25); gala widths 3-6-12 clean
  (2026-09-25/26, 36/36 lanes); afterparty ~15 (2 deaths, refired) and 12
  after a burst (1302s); burn wave width 10 x3 waves clean at 109.4M tok/h
  (watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md, B2-25
  amendment in AFTERPARTY_CLOSE).
- Changed: the envelope law is a function of (transport retry budget, width,
  window burst state), never a width constant; proven-width table with every
  row receipt-cited (AFTERPARTY_CLOSE B2-476 amendment); unanchored rows named
  as unanchored ("THE 50: 50-wide clean" and friends, do not cite as
  measured); blind spot named: "zero surfaced" is not "proven zero" (the
  main-session retry path can absorb silently).
- Still owed: the 15-16 rung (armed, operator GO gate) and the --dwf-run
  tally mode (both named in failure 4).

## What this lane wired this sitting (the mechanism change)

Saved script .zcode/workflows/the-gala.dwf.ts, two changes, both
receipt-commented in the file:

1. `rateLimitHold` (lane sizing / retry shape): a lane crash whose error
   carries the 1302/429/rate-limit shape now holds ~10 min
   (powershell Start-Sleep 600 via world.run, the same spawn surface the
   fold gate uses) before the single allowed refire, implementing B2-476
   contract item 2 in code ("even a clean width takes 1302s until the window
   decays; hold fires ~10 min on 1302"). Hold failure or timeout degrades to
   the old immediate refire, logged - worst case is the status quo. The
   powershell hold spawn shape was tested on this host this session (exit 0).
2. Truncation caps (ask template): gate sections reaching the fold ask raised
   12000 -> 24000 chars; gate sections + fold JSON reaching the herald ask
   raised 6000 -> 12000 each. Anti-example on file: wave5-repair's fold
   scoreboard closing sentence arrived truncated in the run handoff and the
   tail was "not recoverable from this session"
   (wave5-repair_RECEIPT.md section 2); ball-20260929 decision lines print
   "truncated at source".

3. fold_gate.sh shape guard (fold gate check surface, wired live): the live
   fold-gate dogfood at wave close (CHECK 16b) crashed with an AttributeError
   traceback on two sibling tool byproducts in the shared ractor50 archive
   (_bridge_list_raw.json and _full_list_raw.json are top-level JSON lists,
   the fold-gate-repair D

== skills.md ==
# RACTOR50 LANE: skills - SKILL-USE RETRO (division B, 2026-09-30)

Lane: skills (division B) of the ractor50 wave retro. Archive:
`watch/inbox/gala_20260925/ractor50/lanes/skills.json`. Check output:
`watch/inbox/gala_20260925/ractor50/lanes/skills.check.txt`.

Scope: the estate's 18 census skills (f-02/f-21, 2026-09-28) get a live-loop
verdict each (promote / demote / kill); the wave-invented protocols that
PROVABLY worked get named and specified as one-sitting SKILL.md cards or saved
workflows; every dead-but-buildable skill gets wave proof plus a one-sitting
build spec.

Instruments used this session (all commands logged in the instrument receipt
at the bottom): the two flash50 censuses read in full, the five wave workflow
drafts read, git log/show on the wave commits, steps.jsonl post-census scan,
existence checks on engines and loaders. Nothing under mag/ or tools/ was
modified by this lane.

## 0. Census drift first (name instrument, moment, delta)

f-02/f-21 counted 18 SKILL.md files, 56,713 bytes on 2026-09-28. Today
(2026-09-30) `wc -c .agents/skills/*/SKILL.md` = 65,826 bytes over 20 files.
Delta: +2 skills, +9,112 bytes in the two new cards (frontier-mine 2,398 B;
ractor-essay 6,574 B), +141 bytes across the old 18 (unattributed micro-drift,
below one commit of noise; not investigated further, named honestly). Both
arrivals landed 2026-09-29 and both are wave protocols converted to cards
(frontier-mine: commit 6a1c70ec9 "OLM MINE becomes a daily burn + a skill";
ractor-essay: commit f02fc2c33 "ractor-essay skill formalized from Q-operation
run"). The headline of this retro is therefore already half-proven by the
estate itself: the wave-to-card path works and has run twice since the census.

Second drift: f-02's "two disjoint skill stacks" finding (configs/skills.yaml
touches 0 of the 18) is now stale. Commit f02fc2c33 (09-29) registered the
repo skills into configs/skills.yaml (B1-era registration); byte-check today: