# break-lineage: hostile second pass on lineage.md (2026-10-03, this sitting ~20:30-21:10Z)

Instrument: read every cited file at its cited lines; re-ran the lens's greps at full
scope; re-censused the usage ledger with
`.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/break_lineage_census.py`;
re-ran `.venv/Scripts/python.exe -m harness.opencode_coder --ready`; tested win32
`kill -0` against a live native PID; grepped the vendored bundle AND the installed
runtime for the T1 blocker symbols. No paid ask fired this sitting; no live balance
queried. No em-dashes (law). Every universal claim below names its instrument and scope.

## Verdicts on the four findings

### Finding 1 (09-03 zcode-cli BLOCKED, reopen condition in-code, siblings armed but unregistered) - WEAKENED (history stands, two evidence joints broke, and the reopen question moved under it)

Byte-checked and standing:
- `mag/seat_dispatch.py:141-162`: T1 VERDICT verbatim at :147, the three reproduced
  defects at :149-154 (parser rejects --max-turns/--settings; model must be a
  "provider/model" string; `requireRuntimeModelConfig` throws "missing baseURL"),
  reopen routes at :155-156. Exact.
- `queue/STANDING_RAILS.md:24-35`: the drop-in table has no opencode, claude-zai, or
  zcode-cli row. Exact.
- `handoff/GLM_CODING_PLAN_BRIEFING_20260826.md:63-69` (measured economics) and
  :89-90 (the one-line) exact.
- The `--ready` probe re-ran this sitting:
  `.venv/Scripts/python.exe -m harness.opencode_coder --ready` returned
  `{"opencode_cli": true, "zai_key": true, "zai_key_2": true}`, byte-identical to the
  lens's run and matching `harness/opencode_coder.py:84-86`.
- Falsifier attack (the lens's own, run at full scope):
  `rg -il "zcode-cli" watch/inbox memory/runs` returns only prose/scan/trajectory
  mentions, no dispatch receipts; `queue/handoff/zcode-cli/OUTBOX/` holds exactly two
  files, both 2026-09-03, both `status: failed`, and both bodies are the CLI's help
  text dump, which is the raw in-repo reproduction of defect 1 (the parser printing
  usage for flags its own --help lists, including `--max-turns` and
  `--permission-mode`). Never-reopened survives the attack at this scope.

Broken joints:
1. "1,520 rows, zero dispatch receipts, only corpus/library paths" is false as
   written. `rg -c "zcode-cli" dashboard/data/ESTATE_INDEX.jsonl` = 1,520 (exact), but
   `rg "zcode-cli" ... | rg -v "corpus"` = 2 rows:
   `queue\handoff\zcode-cli\OUTBOX\ext-93662b92a0.md` (mtime 2026-09-03T16:28:00Z) and
   `ext-b102db4055.md` (15:44:47Z). These are failed dispatch receipts from BEFORE the
   ~17:3xZ verdict, so they support the claim's substance, but the lens's "sampled,
   only corpus paths, zero dispatch receipts" phrasing is not the census. (Also note:
   the lens's own forward-slash instrument would have missed nothing here only by
   luck; the JSONL paths are backslash-escaped, and a naive `corpus/library` pattern
   returns a false zero. My first pass made this exact mistake and re-ran with the
   correct pattern.)
2. "the blocker's raw source is vendored in-corpus" does not survive its own grep. The
   lens's proposed move, executed this sitting:
   `rg -l "requireRuntimeModelConfig" corpus/library/zcode-zai-org/` returns ZERO
   files; `rg -l "missing baseURL"` returns one unrelated file
   (`repo/apps/zcode-cli/tools/prompt-trajectory/src/record.ts`, a trajectory tool,
   not the model-config runtime); case-insensitive `runtimeModelConfig` hits only
   record.ts and fixture.ts. The vendored tree is app source v0.16.9
   (`repo/apps/zcode-cli/package.json`).
3. Decisive extension the lens did not run: the INSTALLED runtime
   `C:\Program Files\ZCode\resources\glm\zcode.cjs` (14,820,968 bytes, mtime
   2026-09-28 23:21, i.e. updated 25 days AFTER the 09-03 blocker) contains NEITHER
   `requireRuntimeModelConfig` NOR `missing baseURL` (`rg -c` exit 1 on both over the
   literal bytes; caveat: minification could split the symbol name, but an error
   literal would not be split). The T1 verdict's named blocker cannot recur verbatim
   in the current runtime, and the documented reopen route ("the CLI update that
   ships the headless runtime builder", seat_dispatch.py:155-156) may already be
   satisfied. No re-probe of the door exists anywhere I searched. The blocker story
   is a 09-03 snapshot of a runtime that has since changed under it.

Upgrade to "siblings armed but unregistered": the claude-zai door is not merely
armed. `queue/handoff/claude-zai/OUTBOX/` holds 53 dispatch receipts from
2026-09-03T19:04-19:36Z (after the zcode-cli verdict), of which 52 are
`status: done` and 1 is `status: failed` (`rg -o "status: [a-z]+" ... | sort | uniq -c`
= 52 done, 1 failed). `ext-fcace928c2.md` is a full economist Desk-scaffolding table,
tri-stated with per-row file cites. A proven headless judgment door ran a 52-receipt
production night and was never registered as a rail. (The door's cmd,
`mag/seat_dispatch.py:121-134`, rides the z.ai plan through Claude Code with
`--dangerously-skip-permissions` at :132.)

### Finding 2 (orphan pattern, fourth lap) - CONFIRMED, strengthened on both ends

- `watch/SELF_STEAL_GROK_ORPHANS_20260904.md:134-146`: O6 header, ok:true/verify:false,
  "The PATTERN propagated (harness/opencode_coder.py says 'mirrors grok_build_coder /
  glm_coder')", no-config absence, FOLD disposition. Exact.
- `rg -n "grok_build" configs/` re-run this sitting: zero hits (exit 1). Exact.
- `queue/queue_index.jsonl:32`: Q-032 "Swarm to Roblox Luau week-1 port via opencode
  headless", closed 2026-09-30T09:28:41Z, close_note "STALE-superseded: Roblox lane
  dead per operator 2026-09-29". Exact line, exact claim.
- `tests/test_zai_burst.py`: the `from harness.opencode_coder import` is at line 10,
  not 6-9 (one-line drift); repo-wide `rg -ln "opencode_coder"` (excluding
  catalog/dashboard/corpus) returns only the module itself, prose receipts, data
  rows, and the test file, so "only code consumer" holds.
- Strengthened: `harness/` holds FIVE generations of coder organs (codex_coder.py,
  glm_coder.py, grok_build_coder.py, grok_cli.py, opencode_coder.py, `ls harness/`).
  `queue/results/` holds six glm_coder receipts (2026-08-25) and exactly ONE
  grok_build receipt (20260826T025756460699.json, the O6 source) and zero opencode
  production receipts. Falsifier attack (any opencode_coder/grok_build dispatch
  receipt after 2026-09-04): the watch/inbox mentions are prose, trajectory rows, and
  scan results, not dispatches; none found at this scope. The "fourth lap" count is
  if anything understated, and finding 1's claude-zai night (52 done, then orphaned)
  is the strongest single instance of the pattern.

### Finding 3 (interactive solved the gate layer; headless exhibits the un-gated classes) - CONFIRMED, strengthened; one cite drifted, one census re-scaled

- `mag/route_chat.py:3-9` standing correction, :63-67 hand .env parse,
  :113-115 dormant gate (refuses without operator_go): all byte-exact.
- `harness/opencode_coder.py:56-67` `_read_env` hand .env parse: byte-exact.
- `mag/seat_dispatch.py:132` `--dangerously-skip-permissions`: byte-exact, and
  `rg -n "operator_go|permission" mag/seat_dispatch.py` shows no refuse path anywhere
  in the module (its only subprocess call is :236, no gate).
- "Post-hoc-only double-spend guards that alert but do not prevent": the lens
  inferred this without reading the writer (its blind spot 5). I read it. It is
  byte-true: `tools/instance_guard.py:191-213` `doubled_key_check` docstring says
  "Returns the row to bank (flagged or as-is)"; it stamps `doubled_key: True`,
  writes an attention alarm, and returns the row for banking. `tools/hermes_burn.py:153`
  banks the returned row unconditionally. The spend is annotated, never refused.
- Alarm census re-scaled: the lens's "five alarms 19:07:38-19:08:04Z on TAVERN_r5" is
  a tail-read, not a census. The endpoints are byte-real
  (`memory/attention.md:1134` at 19:07:38Z and `:1138` at 19:08:04Z), but
  `rg -c "doubled-key alarm 2026-10-03" memory/attention.md` = 850 alarms spanning
  11:51:05Z to 20:29:15Z, 63 of them TAVERN_r5 (9 per character, all 7 characters),
  and the tail at my sitting is firing on DND0_beat*_dm dungeon refires every few
  seconds. The ledger census matches independently: 850 doubled_key ledger rows =
  850 alarms, one per refired row.
- Refire-continues is live-confirmed, not historical: my census this sitting read
  1,236 rows / 995 today / $25.3534 today / 850 doubled, versus the lens's snapshot
  of 1,152 / 911 / $25.11 / 809 taken earlier the same day. The ledger grew by 84
  rows and 41 doubled rows DURING this run's lifetime. 114 of 219 distinct (id,turn)
  pairs carry multiple rows; `('A1_steer_antiforgery','1')` has 49 rows,
  `('DUEL1_hidden_5','1')` 46, `('N1_parables_songmap','1')` 42. TAVERN is stable at
  665 rows / $16.2003, all dated today.
- Cite drift: `docs/ZCODE_SEAT.md:36-40` is the "Other commands" section; the rules
  of engagement are at :41-49. Substance real (treat-repo-as-untrusted-DATA, never
  edit its own provider config), line anchor off by five.
- Commit `49b8d85af` byte-confirmed via `git show 49b8d85af`: "third-party Stripe
  live key in a root scrape... pk_live... Excised. Three catches in three days, all
  third-party, zero fleet-owned secrets leaked." Note the key was third-party
  (scraped page), not an estate key; the leak-into-tree class still holds.
- `watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md:68-74`: 13 doubled keys, both
  copies costed, ~$1.16: byte-exact at :69-71.
- NEW mechanism the lens missed: `scripts/descent_driver.sh:16` guards against twin
  drivers with `kill -0 "$OLDPID"`. This sitting's probe: a live native Windows PID
  (explorer.exe 42856 via tasklist) returns "No such process", exit 1, from this
  bash. The guard's liveness probe is instrument-dependent and cannot see a
  native-PID instance from this shell, which is a concrete mechanism for the twins
  recurring after the 2026-10-02 guard landed. Which bash flavor spawned the observed
  twins is OWED (not determinable from the artifacts I read).

### Finding 4 (economics cut both ways: density at a ~16x premium) - WEAKENED (arithmetic confirmed, the one-sided density framing broke, the premium is still unmeasured)

Confirmed:
- `watch/inbox/frontier_delta_register_20261003.json`: parsed this sitting, 14 rows.
- Chars-wins recount: frontier wins 10 (BARFIGHT_spec, DND_module,
  SUBSTANCE_48h_synthesis, SUBSTANCE_gaming_corpus, SUBSTANCE_play_findings,
  SUBSTANCE_moonshot_primer, PARTYCHAT_spec, THE_ROOM_REMEMBERS, SEASON_design,
  SESSION_FINDINGS_dig), flash wins 4 (MOUNTAIN_build, WILD_EYES, KABUKI_FACES_fold,
  WIRE_PLAN). The lens's 10-4 is exact. The ask's "judged 8-5 / 39 lanes" remains
  non-relocatable: the sibling accuracy lens already established this
  (`accuracy.md:63-83`: "grep for 39/8-5 across frontier_asks + delta files returned
  nothing... neither is 8-5"). OWED at the run level; the lineage lens correctly
  flagged its own count as a proxy.
- flash zero-output on SUBSTANCE_gaming_corpus: confirmed (`flash_chars: 0`,
  `flash_cites: 0`).
- `watch/inbox/replay_flash/SEASON_design.md:138`: "about 1.1M est... UNVERIFIED until
  DONE rows carry a tokens field (they carry only spend_usd today)" - the token
  metering hole, exact line.
- `queue/STANDING_RAILS.md:49-50`: "30/50 lanes landed, ~20 killed by the interrupt
  before the no-cancel law landed". Byte-exact, as is the law text at :17-19.
- `ls watch/inbox/replay_flash/` = 13 files. Exact.

Broke:
- "the seat's agentic loop buys citation density" is not what the register says.
  Recomputing cites/1k chars per row: flash wins density on FIVE rows (BARFIGHT_spec
  2.03 vs 0.89, DND_module 2.47 vs 1.39, SUBSTANCE_48h_synthesis 1.70 vs 1.67,
  KABUKI_FACES_fold 4.86 vs 4.62, WIRE_PLAN 5.08 vs 0.00), and `flash_unver` is lower
  than `frontier_unver` on 12 of 14 rows (e.g. BARFIGHT 1 vs 9, DND_module 1 vs 7,
  PARTYCHAT_spec 6 vs 42, THE_ROOM_REMEMBERS 2 vs 37; exceptions moonshot 11=11 and
  WIRE_PLAN 12 vs 6). What the premium demonstrably buys on this register is LENGTH
  (10-4 chars) and a few zero-output saves, not citation density, which is
  contested-to-flash. The lens named three of the five flash density wins and framed
  density as the seat's purchase; the register's own columns contradict the framing
  it wrote.
- The ~16x premium itself remains carried, not measured: no tokens field exists on
  DONE rows (SEASON_design.md:138 says so in-artifact), the flash arm's 9.5M seat
  tokens are carried from the ask, and today's ledger carries only cost_usd and
  prompt/completion tokens for frontier rows. The falsifier the lens wrote (banked
  flash tokens under ~100K per deliverable) is not testable in-repo today. OWED.
- Today's ledger split for the economics question: $25.3534 total today, of which
  TAVERN (play) is $16.2003 across 665 rows, i.e. play is ~64% of today's paid
  spend. Any premium math that ignores what the interactive-steered play layer
  spends on the same license is incomplete.

Also on finding 4: the finding text arrived truncated in the report handed to this
pass (cut at "the headless "); the verdict covers the visible claim and the full
evidence block.

## Blind-spot checks (all seven)

1. Arena cron automation-b1ce1342 not in-repo: CONFIRMED. `rg -l "b1ce1342"` (repo,
   excluding catalog/dashboard) hits only today's ractor lens reports and
   `parable_day_one_20261003.md`; `rg -ic "arena" memory/workflows/REGISTRY.jsonl`
   and any "automation" row: zero. The definition lives outside the repo; where
   exactly is OWED (harness-side automation store, not queried this sitting).
2. Flash arm 9.5M carried not measured: CONFIRMED real and load-bearing (see finding
   4; SEASON_design.md:138 names the hole in-artifact).
3. Vendored grep not yet run: RUN this sitting, and the result flipped the move (see
   finding 1): the named blocker is absent from both the vendored source and the
   installed Sep 28 runtime.
4. `--ready` is a probe not a paid ask: TRUE, and it is still true after my re-run.
   No plan tokens spent this sitting.
5. hermes_burn writer not read: READ this sitting; the dedupe-at-write absence is now
   byte-backed (`tools/instance_guard.py:191-213`, `tools/hermes_burn.py:153`), no
   longer inferred.
6. Nous balance / $220 armed / Hermes warm-state not queried: still true of this pass
   too. OWED (needs a live API query; a break lens does not spend).
7. 66 claude-zai/openclaw-worker ESTATE_INDEX hits unclassified: CLASSIFIED this
   sitting: 53 claude-zai rows are ALL `queue/handoff/claude-zai/OUTBOX/*.md` dispatch
   receipts (52 done, 1 failed, all 2026-09-03 19:04-19:36Z); 13 openclaw-worker rows
   not individually opened (counted only: `rg -c "openclaw-worker"
   dashboard/data/ESTATE_INDEX.jsonl` = 13). This unclassified residue turned out to
   hold the strongest migration evidence in the run (see addition 1).

## Additions (what the lens missed)

1. The proven-then-orphaned production night. 52/53 done claude-zai dispatch receipts
   on 2026-09-03 19:04-19:36Z (`queue/handoff/claude-zai/OUTBOX/`, e.g.
   `ext-fcace928c2.md`: a tri-stated economist organ-mapping with per-row file
   cites), through the fence-compliant Claude-Code-on-zai-plan door
   (`mag/seat_dispatch.py:121-134`), never registered as a standing rail, never
   re-fired. The migration debate asks "can a headless surface carry judgment work";
   the estate answered yes a month ago and buried the receipt folder.
2. The blocker is gone from the current runtime and nobody re-probed. Installed
   `zcode.cjs` mtime 2026-09-28 23:21 contains neither T1 blocker string; vendored
   source v0.16.9 contains neither. The reopen route named in-code
   (seat_dispatch.py:155-156, "the CLI update") appears to have fired unseen.
3. The nul-file trap is real and in-repo: repo-root `nul` (0 bytes, mtime epoch 0)
   makes any recursive `rg` over the repo exit 2 with "Incorrect function" (observed
   this sitting); `nul_pullpush_body.txt` sits beside it. Every headless rail that
   does repo-wide byte sweeps (drift patrol, census, citation lint pre-scans) walks
   past a reserved-name landmine. Deleting a reserved-name file needs the `\\?\`
   prefix; that is an operator call, not mine.
4. The pidfile guard is win32-blind in this shell: `kill -0` on a live native PID
   returns "No such process" (tested against explorer.exe 42856 this sitting), so
   `scripts/descent_driver.sh:14-22` cannot detect a native-PID twin from git-bash.
   The 10-02 guard may be structurally unable to prevent the exact twins it was
   written for, depending on which bash spawned the instances (OWED).
5. The alarm surface is saturating: 850 doubled-key alarms in one day in
   `memory/attention.md`, firing every few seconds during dungeon refires. A
   watchdog that cries 850x/day trains the operator to ignore the channel, which
   degrades the ONE steering path an unattended estate keeps open. The
   dedupe-at-write move is alarm-surface hygiene before it is money hygiene.

## OWED register (not asserted, not done here)

- The judged 39-lane / 8-5 artifact (falsifier already filed by accuracy.md:83).
- The flash arm's banked token counts per deliverable (no tokens field exists; the
  16x premium is carried from the ask).
- Nous credit balance, the $220 armed dispatch state, Hermes warm-state (no live API
  query from this pass).
- Where the automation-b1ce1342 definition physically lives (outside the repo).
- Which bash flavor spawned the 10-02 twin drivers (determines whether the kill -0
  guard was ever able to see them).
- The 13 openclaw-worker ESTATE_INDEX rows, opened individually (counted only).

## Falsifiers for this pass's own verdicts

- A post-2026-09-03 zcode-cli, opencode_coder, or grok_build dispatch receipt, or a
  STANDING_RAILS row naming any of them, kills the never-reopened / orphan-lap
  verdicts at my search scope (watch/inbox, memory/runs, queue/handoff/*, configs/).
- A vendored-tree or installed-runtime byte containing
  `requireRuntimeModelConfig`/`missing baseURL` kills my "blocker gone from current
  runtime" reading (my instrument: literal `rg -c` over both trees, exit 1).
- A banked-hermes_burn row refused (not banked) by doubled_key_check kills the
  "alerts but does not prevent" reading of instance_guard.py:191-213.
- A register re-parse showing frontier density wins on a majority of rows kills my
  "density is contested-to-flash" correction.
- A native-PID `kill -0` success from the shell that actually runs descent_driver.sh
  kills my win32-blindness mechanism for the twins.
