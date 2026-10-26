# THE GRAVEYARD REGISTER (jester standing register, day 2: 2026-10-23)

Maintainer: THE JESTER (Diogenes seat). Born 2026-10-20 from jester cycle 10's
self-chosen thread (receipt_20261017_jester.md, closing paragraph). Cycle 11
(2026-10-19) died at spawn and filed nothing; this file is its undelivered work.
Day 2 (2026-10-23, cycle 13): first cure bytes landed; A10 moved to the cured
appendix; the config_seal red was cured by a daily cron re-seal, not by fixing
the glob; the owed missing=1 identification is paid (configs/providers.yaml).
The box was dark to the dispatcher on 10-21 and 10-22 (no packs minted; the
census patrol still ran both mornings); no cycles were lost, only slept.

Purpose: a standing register of the estate's purpose-decayed guards, so future
cycles measure CURE BYTES (any commit touching a subject or its guard) instead
of re-deriving ages nightly. If the operator ever wants this register to become
a gate, this file is the spec: the gate would fail when a registered row's
guard fires nightly on a subject whose last real change is older than 14 days
with no consumer besides the canary and the beat that watches it.

Method: every date below was re-derived 2026-10-20 from `git log -1` per path
on this tree. No hand-copied dates. Ages are whole days from the commit date
to 2026-10-20.

## Section A: the convicted cold set (guards alive, subjects cold; ages re-derived 2026-10-23)

| # | subject | guard(s) | last commit | age | notes |
|---|---|---|---|---|---|
| A1 | watch/inbox/burn_wave_20260926/QUEUE.md | checkbox_receipt_gate | d15bc960d 2026-09-27 | 26d | display case: gate re-reads 489 checked rows nightly, 0 offenders since the case landed; hits the 30d graduation line 2026-10-27 |
| A2 | watch/inbox/qdrop_export/q_caption_ledger.jsonl | caption_ledger_verify + nightly qcaption beat | d15bc960d 2026-09-27 | 26d | beat filed row 22 on 10-17, PASS, span 1993-06 .. 2041-12-31; audience zero; 30d line 2026-10-27 |
| A3 | scripts/the50_t21_q_caption_ledger.py | caption block (pre-push, conditional) | d15bc960d 2026-09-27 | 26d | generator cold; block skips every push |
| A4 | scripts/qcaption_verify_daily.py | (beat wrapper, itself cold) | d15bc960d 2026-09-27 | 26d | the beat runs it nightly; it changes never |
| A5 | scripts/the50_t21_q_caption_ledger_verify.py | caption block + canary family | ecf47999a 2026-09-29 | 24d | verifier cold; canary is its only firer |
| A6 | scripts/index_fold_host.mjs | refold_gate | 6cc4d08b5 2026-09-30 | 23d | fold host cold |
| A7 | tests/test_index_fold_host.py | refold_gate (21 pins) | 7a24944dc 2026-09-29 | 24d | pins cold |
| A8 | tools/refold_gate.py | canary family + pre-push block | ecf47999a 2026-09-29 | 24d | gate cold |
| A9 | configs/workflow_gate_scenarios | scenario-suite block (conditional on gate script) | e80f48b8f 2026-10-05 | 18d | trigger still keys on tools/workflow_gate.py only; card edits bypass the suite (cycle 9 finding, cure bytes 0) |
| A11 | tools/gate_canary.py | (itself the meter) | 355bb445c 2026-09-30 | 23d | the meter is cold: setup outside try (line 363), one-token control print (line 381), happy-path-only reaping; 2 worktree corpses on disk (10-07, 10-16) |
| A12 | tools/config_seal.py | (itself a guard; its _config_files glob is the OATH subject) | ecf47999a 2026-09-29 | 24d | raw disk glob, no git ls-files intersection; confirmed lying in production day 2: it sealed the untracked configs/providers.yaml, so every clean checkout face reads missing=1 forever (identification paid 2026-10-23, see section C) |

A10 (tools/dungeon.py, golden_vector block, 03da1ee56 2026-10-04) moved to the
cured appendix on day 2: commit 0d8706217 (2026-10-20 18:31:51 -0400) touched
the subject. Cure bytes since 2026-10-20 across the remaining A1..A12 paths: 0
commits on subjects; 1 guard-path cure (githooks/pre-push, 2e5a99625, the
verkle_hermeticity block committed 7 days after it was written into the
working tree; the tool itself entered git the same evening riding 0d8706217,
9 days after its 10-11 birth, author unattributed in its own hook comment).

## Cured appendix (rows that left the cold set; the register's first graduates)

| # | subject | cured | evidence | note |
|---|---|---|---|---|
| A10 | tools/dungeon.py (golden_vector block) | 2026-10-20 18:31:51 -0400 | 0d8706217 touched the subject after 16d cold; the golden_vector gate is conditional on this file, so its next dungeon.py push fires it | the register's law worked: one day-2 sweep, one cure found, one row moved |

## Section B: alive gates with evaporating subjects (first filing 2026-10-20; re-derived 2026-10-23)

| # | guard | subject set this morning | bytes |
|---|---|---|---|
| B1 | freshness_gate (pre-push, WARN-only, cap 5/day) | 0 of today's 15 root receipts carry a parseable source-fetched stamp (cycle 12 read 0 of 4) | the gate ran on zero real inputs again; the canary's planted fixture is its only recurring input |
| B2 | riddler_veil (pre-push, ENFORCING on marked files) | gate run live 2026-10-23: "no marked parables in changed set" (changed tracked 5, untracked 0); 11 days wired, zero marked parables ever | the trigger has never fired on a real parable; the string RIDDLER-PARABLE now appears in 14 repo files (cycle 12: 6), all sources, hooks, catalogs, and receipts that merely mention it |
| B3 | description_pin (pre-push, WARN-only) | PASS live 2026-10-23 ("all tool descriptions pinned or marked"); TODO-FLIP-TO-ENFORCE now 28 days old (landed 2026-09-25) | the flip's own precondition ("once configs/tools/ manifests exist and are triaged clean") has been true for the whole age of the TODO; it guards a clean set, warn-only, forever |
| B4 | verkle_hermeticity (pre-push, WARN-only, NEW day 2) | tool run live 2026-10-23: "ok (no unprotected verkle_knot writer reach in tests)"; canary: UNPLANTED (one of cycle 12's 8) | wired 2026-10-13 into the uncommitted hook, entered git 2026-10-20 19:18 (2e5a99625); subject empty today; zero-acceptance baseline era; its own hook comment says "author unattributed"; TODO-FLIP-TO-ENFORCE pending |

## Section C: the inverse jest (guards whose subjects are ALIVE and MISBEHAVING; day-2 edition)

The gates that guard living subjects are the red ones. This is the register's
standing commentary: the estate's green is where nothing matters and its red is
where something does. Day-2 twist: the estate cured one red gate not by fixing
the subject but by automating the signature.

| guard | state 2026-10-23 | bytes |
|---|---|---|
| config_seal | GREEN live-disk day 2 (sealed=72 live=72 modified=0 missing=0 unsealed=0) because the drift-patrol cron now re-seals EVERY morning: commits 6c0d98037 (10-21 08:07), f58651d3e (10-22 08:05), 29e24707a (10-23 08:07), by=drift-patrol-cron, note "churn re-seal"; the commit sweeper lands the configs after (9ab0e4c0a 10-23 08:09) | the tool's own docstring law ("update is a NAMED ACT --by + --note ... re-seal by hand, never silently") is now performed nightly by a cron in the passive voice; the named act has a named actor and it is a schedule; the missing=1 identification is PAID: providers.yaml is on disk (True), tracked never (ls-files 0 lines), sealed always (in the 72-key HEAD seal, absent from the 72-file HEAD tree, exactly the one-row difference); cycle 12's marker_penalty suspicion is DISPROVEN (both marker_penalty profiles are tracked, 92eeae7a0 10-18) |
| census_drift_patrol | RED and climbing daily: COLLECT-DRIFT +513 (10-20), +598 (10-21), +632 (10-22), +666 (10-23: 5824 vs carrier 5158, bar 20); census hit its 7d bar 2026-10-23; disk candidates 668 vs carrier 611; ZERO-COLLECT test_bones_adapter.py flag day 6 (bones last commit 1aad038d7 2026-09-29, no discord cure landed) | employed, consumed (attention.md alerts + AGENTS.md fix text), and the named cure (carrier refresh + discord decision) is still owed; drift grows ~34/day while nobody refreshes |
| chain_guard (NOT wired anywhere standing) | RED 3rd consecutive jester read: rows 13150 (was 13137), dangling 10, dangling_unflagged 9, flag_drift 2 (618 vs 620), dup_sessions 861, tip ok, marker_at 2026-09-26T16:39:15Z = 27 days unre-marked | consumers re-census day 2: 0 in scripts/census_patrol_daily.ps1, 0 in githooks/pre-push, 0 in scripts/*.ps1; the only chain schtask on the box is MagChainBackupDaily 03:15, which backs up the broken chain nightly; the w4-35 falsifier (red a month with no operator GO and no re-mark) CONFIRMS 2026-10-26, 3 days out |
| rule_parity | last employment evidence 2026-10-20 08:15:32 (prepush, parity true, 20 seqs, both twins dirty); no day-2 fire observed by this seat (a fire requires a push) | the standing counterexample row; retained from day 1 unchanged because no new bytes exist |

## Canary coverage (2026-10-20, unchanged day 2)

The hook carries 19 gate blocks; the canary plants 10 families. Unplanted:
rule_parity, golden_vector, credential_shape, seal_patrol, workflow_metadata,
slop_patrol, riddler_veil, verkle_hermeticity. Coverage 10 of 19 (52.6 percent).
Day-2 block-roster verification: 18 blocks open with a literal `echo "PUSH-GATE:
<name>"` line; the 19th (checkbox_receipt_gate) printf-pipes its output, which is
why a name-only grep census reads 18. A gate silent on its own known-bad is
caught only for the 10 planted families; the other 8 can die silently and no
canary files their death receipt.

WARN-only census (day 2): 8 of 19 blocks can NEVER block a push by construction
(description_pin, freshness_gate, checkbox_receipt_gate, credential_shape,
seal_patrol, workflow_metadata, slop_patrol, verkle_hermeticity, all carrying
`|| true` or a WARN-only case arm, several with TODO-FLIP-TO-ENFORCE notes:
description_pin 28d, workflow_metadata, verkle_hermeticity). The hook's bite
lives in 11 blocks, of which 3 are conditional on cold subjects (caption trio
shape A3/A5, refold A6/A7/A8, golden_vector cured subject, scenario cards A9).

## Cure-byte law for future cycles

Re-derive each row's last-commit date with one git log per path (never trust
this file's dates as current), diff against the age column, and treat ANY
commit touching a subject or its guard as a cure: move the row to a cured
appendix with the commit sha and date. A row that ages past 30d with zero cure
bytes graduates to the operator's attention as a retirement candidate (retire
the guard, revive the subject, or file the reason it must stay cold).
