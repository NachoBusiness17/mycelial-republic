# MASTER GSTD RUNGS 20261011

- run: `gstd-rungs-20261011` (genre: execute)
- folded_at: 2026-10-11T04:52:22Z (fold script sha256 58bd72c79c6d)
- lane archive: `memory/runs/mickey17_v2/runs/gstd-rungs-20261011/lanes` (3 lanes, 12 rows, 0 parse errors, all read in full for this fold)
- lanes fired: `finding7-honesty-edits` (3 rows), `device-runner-onepagers` (5 rows), `gps-wilson-tests` (4 rows)
- every count below is the fold script's (FOLD_SECTIONS.md); prose verdicts cite the lane JSONs and the persisted `.checks.json` deep verdicts. Nothing seat-carried appears untagged.

## CASUALTY HEADER (verbatim from the script)

- fired: 3
- landed (parseable files): 3
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## PRISMA FLOW (verbatim from the script)

- identified: 12
- screened: 12 (all rows carry the six rubric fields or their gap notes)
- excluded: 9 verifier-unconfirmed (deep_tier2): 1
- included: 11
- invariant: identified == included + excluded **HOLDS** (12 = 11 + 1)

The single exclusion is `gps-wilson-tests#3` (deep verdict `unconfirmed`); it is also the run's one `blocked` row, so BLOCKED and the PRISMA exclusion coincide on the same row.

## SCOREBOARD (verbatim from the script)

- rows: 12
- estate_status: executed 10, executed-with-deviation 1, blocked 1
- leverage: high 7, medium 5

## EXECUTIONS (the script's TOP-K, with proof quotes)

Script ranking order preserved. Status per row: estate_status / deep_tier2 verdict / quote-level supports. A lane-claimed top steal outside this list files as DISPUTED; none was claimed (disputed_count = 0).

1. **[high] device-runner-onepagers#0** - executed / deep verified / supports no (quote was conclusory; the deep check byte-read RUNNERS.md itself). Three per-device one-pagers (bob Windows 10, t90 Android/Termux, pixel Termux) each with exact install commands, the five-model run line against `http://100.96.161.76:11434`, per-device receipt-banking routes, and a banked-runs table pre-seeded with tonight's two proof runs; closes LOOP_CLOSED's cross-device-runner gap on paper.
   - quote: `These three one-pagers close it. Each is paste-ready: install, run, bank.`
   - deep check: all six claim elements byte-proven on `watch/inbox/gstd_perimeter_build_20261010/RUNNERS.md` (227 lines): sections A/B/C at lines 63/123/179, install commands at 75-78/129-132/198-205, the exact 5-model string at lines 46/92/155/204, banking routes at 107-110/167-175/207, table pre-seeded at 223-226; RUNNERS.md table row cross-checked against the banked `runs/20261011T022831Z/summary.json` on disk. Nuance kept: pixel's routes are incorporated by reference (line 207), and the second table row (20261011T023240Z) is attested, not estate-banked (see NEGATIVE RESULTS).
   - steal [device-runner-onepagers#0]: Operator pastes section A/B/C on each device; every device run appends one banked-runs table line (device, run_id, rate, verdict) and no claim stands without it.

2. **[high] device-runner-onepagers#1** - executed / deep verified / supports yes. The exact five-model paste line printed in RUNNERS.md ran against the tailnet Ollama host (estate venv python standing in for bare python per the repo env law): exit 0, verdict STRUCTURE, consensus 0.8571 vs dead-salmon 0.1539, receipts self-banked into the estate runs dir.
   - quote: `"run_id": "consensus-20261011T022831Z", "models": ["gemma:2b", "deepseek-r1:1.5b", "qwen2.5:3b-instruct", "gemma2:2b-instruct-q5_K_M", "qwen-desk:latest"], "tasks": 14`
   - deep check: every number independently recomputed from `receipt.jsonl` (12/14 consensus -> 0.8571; dead-salmon 0.1539 reproduced via the harness's own seeded function, `tools/consensus_harness.py:217-252`); exit-0 proven by control flow (receipts are written only on the success path ending `return 0`, `tools/consensus_harness.py:322-350`); the banked dir `watch/inbox/gstd_perimeter_build_20261010/runs/20261011T022831Z/` exists with all three artifacts.
   - steal [device-runner-onepagers#1]: The paste line is proven verbatim end to end; devices run it unchanged, only the launcher (py -3 / python) differs.

3. **[high] device-runner-onepagers#2** - executed / deep verified / supports yes. Coldest-vertex proof: the harness file alone in an empty temp tree (no repo, no LINKS.jsonl, the exact phone shape) ran the built-in fixtures fallback against the tailnet host with exit 0; the temp copy hash-compared identical to the repo file modulo CRLF/LF.
   - quote: `"tasks": 8, "distinct_truths": 8, "consensus_rate": 0.375, "dead_salmon_control_rate": 0.0394`
   - deep check: temp tree holds exactly 4 files (harness + 3 run artifacts, hidden files included); the 8-task count is the fixtures-fallback signature (vs 14 for LINKS-driven); ledger rows match the 8-fixture table byte-for-byte; LF-normalized SHA256 of repo and temp copies identical (`914c69b1...`); 16/16 chat calls answered with zero model_error rows.
   - steal [device-runner-onepagers#2]: The fixtures fallback is proven, not assumed: a device with zero estate data still banks a STRUCTURE-class run, which is LOOP_CLOSED's final-proof-of-portability precondition.

4. **[high] finding7-honesty-edits#0** - executed / deep verified / supports yes. Finding 7's honesty edit landed on the perimeter CARD headline block: unisub's within-shared-architectures qualifier restored at the cite, headline rescoped to CROSS-FAMILY BEHAVIORAL AGREEMENT with the no-cited-paper-claims framing; the overclaim can no longer enter the GB thread from this CARD.
   - quote: `disjoint models converge WITHIN SHARED ARCHITECTURES (the abstract's own qualifier, unisub_drop_20261010/CARD.md:13-14 - do not overclaim cross-architecture). A2's fleet runs K different models across families, so the garage measures CROSS-FAMILY`
   - deep check: quote contained verbatim across `watch/inbox/gstd_perimeter_design_20261010/CARD.md` lines 23-25; both cites verified at their targets (`watch/inbox/unisub_drop_20261010/CARD.md:13-14` carries the qualifier; `watch/inbox/ractor_engine/2026-10-10-singing-network/SYNTHESIS.md:47` carries finding 7 verbatim); full-file read finds no unqualified cross-architecture attribution anywhere in the bytes. Scope caveat kept: "cannot enter the GB thread" is forward-looking; actual GB usage unobservable from bytes.
   - steal [finding7-honesty-edits#0]: done: the qualifier restoration + cross-family rescope is byte-landed at CARD lines 22-31 with in-place receipt citing SYNTHESIS.md:47.

5. **[high] gps-wilson-tests#0** - executed / deep verified / supports no (quote covered 1 of 12 re-derivations; the deep check went beyond it). All 12 stale pre-Wilson assertions in `tools/gps_mcp/test_gps_mcp.py` re-derived to the honest Wilson lower bounds from `ledger.py` get_rate (z=1.96 over resolved evidence only), each commented with ractor finding 1; routing expectations moved summarize to flash-mid-1 (bound 0.8737 vs gemma-worker-4b 0.8391 under the 0.85 threshold) and the 0.95 code_review override falls back to yesno-tiny.
   - quote: `assert ledger.get_rate("m", "shape") == (pytest.approx(0.4618), 50)`
   - deep check: quote byte-exact at `tools/gps_mcp/test_gps_mcp.py:633`; git diff shows 23 assert statements re-derived across exactly 12 test functions, each carrying a "Ractor finding 1" comment (12 line anchors banked); every quoted bound reproduced under independent recomputation this session (0.8737 @ n=130, 0.8391 @ n=140, 0.4618, 0.3664, yesno-tiny 0.0475, etc.); routing asserts verified at :226-232 and :275-279. Count nuance: 12 test functions, 23 assert statements (more re-derivation than claimed, not less).
   - steal [gps-wilson-tests#0]: done: 12 assertions now assert the Wilson bound, not the inflated point rate; probe script derived every actual from the real code paths.

6. **[high] gps-wilson-tests#1** - executed / deep same-chain-verified / supports yes. Suite ends green: full `tools/gps_mcp/test_gps_mcp.py` run went from 12 failed / 30 passed to 42 passed, exit 0, via `.venv/Scripts/python.exe -m pytest tools/gps_mcp/test_gps_mcp.py -q`.
   - quote: `42 passed in 683.46s (0:11:23)`
   - deep check: quote banked 3x in the lane JSON (pytest_tail_final, verbatim tail, row quote); the verbatim tail is exactly 42 dots + `[100%]`; the file still contains exactly 42 test functions and all 12 baseline-failing names remain present (green not bought by deletion). Limitation kept: same-chain landed evidence, not an independent re-execution; the recorded 683.46s runtime exceeds the verifier's 600s single-command ceiling, so a fresh rerun was out of scope for that seat (NEXT REGISTER #8).
   - steal [gps-wilson-tests#1]: done: the Wilson floor is now test-enforced on the gps router surface; any future inflation of get_rate trips this suite.

7. **[high] gps-wilson-tests#3** - BLOCKED / deep unconfirmed / supports no (pattern proven, scope unproven) - **this is the run's 1 blocked row and the 1 PRISMA exclusion**; full treatment in BLOCKED tier below. Adjacent-surface finding (not caused by this lane's edit, which touched only `tools/gps_mcp/test_gps_mcp.py`): three sibling suites carry the same pre-Wilson expectation debt against the already-live ledger fix (10 + 5 + 5 failures).
   - quote: `assert (0.5101, 4) == (1.0, 4)`
   - deep check: the quote is a pytest runtime rendering (0.5101 occurs 0 times in `tests/test_verdict_feed.py`; the landed line is `:113 assert gps.get_rate(SERVER_ID, TASK_SHAPE) == (1.0, 4)`), and no pytest output for the three sibling suites exists anywhere in the estate; but every quantitative element (10/5/5 counts, the 0.5101 actual at n=4, phat=1.0) is exactly re-derivable from the live Wilson ledger plus the untouched sibling suites, and git status confirms the lane touched only `tools/gps_mcp/ledger.py` + `tools/gps_mcp/test_gps_mcp.py`. Consistent-with-bytes, not proven-by-bytes -> unconfirmed.
   - steal [gps-wilson-tests#3]: re-derive those 20 sibling assertions the same way (wilson(passes, n) with z=1.96; n=1 single pass = 0.2065); file ownership sits outside this lane's finish line.

8. **[medium] device-runner-onepagers#3** - executed / deep verified / supports yes. Negative test executed: the harness run with `--host http://example.com:11434` refused the public host with exit 2, byte-proving the closed-perimeter allowlist sentence printed in RUNNERS.md.
   - quote: `host refused: host resolves outside the closed perimeter (172.66.147.243); this tool reaches loopback/LAN/tailnet only`
   - deep check: the ValueError half is byte-present at RUNNERS.md:21-24; the `host refused:` prefix is the harness's own stderr format (`tools/consensus_harness.py:259`); 172.66.147.243 lies outside 172.16.0.0/12 so refusal is deterministic; the IP literal appears nowhere in the codebase (run-derived data, evidence a real resolution occurred); no receipt exists by design (check_host returns 2 before any banking).
   - steal [device-runner-onepagers#3]: RUNNERS.md can tell every device 'point it at nothing else; nothing else will run' as a proven fact, so the perimeter stays closed by code not by policy.

9. **[medium] device-runner-onepagers#4** - executed / deep same-chain-verified / supports yes. Verified the run line's host and model list are live facts: Ollama on the desktop tailnet IP answered /api/tags with 15 models including all five the paste line names.
   - quote: `CHECK {'gemma:2b': True, 'deepseek-r1:1.5b': True, 'qwen2.5:3b-instruct': True, 'gemma2:2b-instruct-q5_K_M': True, 'qwen-desk': True}`
   - deep check: the CHECK dict is unlanded (0 byte-for-byte hits repo-wide; the verifier's mandate was read+grep on estate paths, so the live curl was not re-run); the dict content recomputes byte-identically from `gstd_nodes_live.json` (15 capabilities) but that registry is hours older than the claimed tonight-check; the five named models are proven live on that host that night by the run receipts themselves (both run dirs' consensus_ledger.jsonl carry exactly those 5 rows). Execution facts proven by the same work-chain's landed receipts; the quoted proof artifact itself unlanded -> same-chain-verified.
   - steal [device-runner-onepagers#4]: The 15-model pool means a device can widen its model set later (deepseek-r1, qwen2.5:7b, gemma4 family) with zero infra change.

10. **[medium] finding7-honesty-edits#1** - executed / deep verified / supports no (quote proved only the one-liner; the deep check found the receipt block the quote missed). Finding 7's honesty edit landed on the GB reply addendum: the quoted one-liner keeps the paper's qualifier and names the perimeter's metric cross-family behavioral agreement, plus an edit receipt block so the qualifier travel is on the record before the message enters the GB thread.
    - quote: `today, with their qualifier kept: their convergence is within shared architectures, ours is cross-family behavioral agreement - a claim no cited paper makes. that's a better experiment, not a smaller claim.`
    - deep check: all 8 byte checks pass; the receipt block exists at CARD.md:97-100 (edit date, finding number, both citations), which the quote-level check could not see; the quote sits under the `## GB reply addendum` header at CARD.md:88.
    - steal [finding7-honesty-edits#1]: done: addendum lines 90-100 carry the qualifier-kept message and the receipt block.

11. **[medium] finding7-honesty-edits#2** - executed / deep verified / supports no (quote was the final-green line only). Adjacent-surface verification for the changed prose record: citation-lint gate (the pre-push class for changed prose) run on the CARD, green after healing one TOKEN-MISS warn by rewrap; dash-law byte check reads zero em/en dashes in the landed file.
    - quote: `CITATION-LINT: ok records=1 anchors=4 numbers-checked=0 blocking=0 warns=0 enforce-tokens=False`
    - deep check: both executable components re-run by the verifier on landed bytes and reproduced exactly (lint line byte-identical, exit 0; em-dash 0, en-dash 0). Disclosures kept: (a) the first-run TOKEN-MISS warn is not independently re-runnable (pre-heal state overwritten in place; rests on the lane's banked verbatim output); (b) minor drift - the lane's dash-check recorded `bytes: 6192`, the current CARD is 6264 bytes, the +72 lying outside this lane's two edited regions (see NEGATIVE RESULTS).
    - steal [finding7-honesty-edits#2]: done: gate output banked verbatim in this lane file (first run warn + final run green) so the heal is auditable.

12. **[medium] gps-wilson-tests#2** - executed-with-deviation / deep verified / supports no (one named gap visible in quote; deep check proved the rest in bytes). Coverage gaps named in-test rather than papered over: post-Wilson the gemma->flash escalation trace (escalated flag, ctx prior-answer carry), the 3-tier cascade cap, and a 2-attempt cascade are unreachable on the seeded fixtures; the earned-never-declared momentum law keeps its control arm on a self-attested upsert (momentum None, get_rate bounded at 0.21).
    - quote: `the escalate-path machinery (escalated flag, prior-answer ctx carry) is a named coverage gap, not a silent deletion`
    - deep check: quote byte-exact (normalized) at `tools/gps_mcp/test_gps_mcp.py:307-315`; the 3-tier-cap gap named at :329-336; the momentum control arm at :592-609 (asserted by `momentum(...) is None`); every cascade test asserts exactly 1 attempt. Caveat kept: the row's "any 2-attempt cascade unreachable" clause is right about exercised coverage but overstated as system impossibility - `Constraints(min_confidence=0.95)` with no cost cap leaves a seeded 2-attempt cascade constructible (`router.py:449-507`).
    - steal [gps-wilson-tests#2]: residual: a future lane can restore escalation-path coverage by recording a qualifying local-tier series on a custom shape (record_series with 0.85+ Wilson bounds) or minting fixture rates sized so bounds clear the threshold.

TOP-K tally: 12 entries (7 high, 5 medium); 11 included, 1 (entry 7) flows to BLOCKED/excluded. No lane claimed a top steal outside this list -> disputed_count = 0.

## BLOCKED TIER

Every blocked row (script count: 1), with reason and the next-sitting unblock.

**gps-wilson-tests#3** - 20 sibling-suite assertions carrying pre-Wilson expectation debt against the already-live Wilson ledger fix (`tools/gps_mcp/ledger.py` get_rate, z=1.96).

- Reason (lane): file ownership - `tests/test_verdict_feed.py` (10 failures), `tests/test_gps_dedupe.py` (5), `tests/test_gwap_to_gps.py` (5) sit outside this lane's finish line (`tools/gps_mcp/test_gps_mcp.py` only).
- Reason (verifier, why unconfirmed): the sibling-suite pytest run is recorded nowhere in the estate (targeted grep found the 0.5101 quote only in the chain's own claim restatements), and the quote itself is a pytest runtime rendering with 0 bytes in the source file. The finding stays consistent-with-bytes (10/5/5 counts and 0.5101 exactly re-derivable from the live ledger + untouched suites) but is not proven-by-bytes.
- Next-sitting unblock (NEXT REGISTER #1, one seat one sitting): re-derive all 20 sibling assertions to the Wilson lower bounds (wilson(passes, n), z=1.96; n=1 -> 0.2065), run all three suites, and bank the pytest tails verbatim in the lane file so the run is estate-recorded. That converts this row from blocked/unconfirmed to executed/verified and restores the PRISMA invariant headroom.

## NEGATIVE RESULTS (counted reasons table)

| # | reason | count | where it lives |
|---|---|---|---|
| 1 | Sibling-suite pytest output unbanked anywhere in the estate; quote was runtime rendering, not file bytes -> row unconfirmed and PRISMA-excluded | 1 row | gps-wilson-tests#3 deep check |
| 2 | Pre-Wilson expectation debt in sibling suites, blocked on file ownership | 20 assertions across 3 suites (10 + 5 + 5) | gps-wilson-tests#3 claim |
| 3 | No Android runtime on the seat: Termux-side lines (pkg install, termux-setup-storage, device scp) unexecuted, paste-ready for the operator's hand | 2 of 3 one-pager sections (t90, pixel) | device-runner-onepagers gaps |
| 4 | Harness untracked in git: the git-clone transfer route is documented as post-commit only; tonight's route is the single-file Taildrop copy | 1 (`tools/consensus_harness.py`) | device-runner-onepagers gaps |
| 5 | scp banking route unexercised (sshd Running attested by service state only; Taildrop/paste fallbacks named) | 1 | device-runner-onepagers gaps |
| 6 | Coldest-vertex run banked under a temp copy, absent from the estate runs dir (RUNNERS.md table row discloses this itself) | 1 run (`20261011T023240Z`) | deep check on device-runner-onepagers#2 |
| 7 | /api/tags CHECK dict unlanded in the estate -> row downgraded to same-chain-verified | 1 row (device-runner-onepagers#4) | deep check |
| 8 | Register undercounted the failures (said 10; actual baseline 12, byte evidence: pytest tail) | 1 | gps-wilson-tests deviation_from_register |
| 9 | Coverage unreachable on seeded fixtures post-Wilson: escalation trace (escalated flag, ctx carry), 3-tier cascade cap, 2-attempt cascade | 3 named gaps | gps-wilson-tests#2 |
| 10 | Lint first-run TOKEN-MISS warn overwritten in place by the heal -> not independently re-runnable | 1 | finding7-honesty-edits#2 deep check disclosure |
| 11 | CARD byte drift +72 outside the lane's two edited regions (lane dash-check output `bytes: 6192`, memory/runs/mickey17_v2/runs/gstd-rungs-20261011/lanes/finding7-honesty-edits.json; deep check measured the current file at 6264 bytes, memory/runs/mickey17_v2/runs/gstd-rungs-20261011/lanes/finding7-honesty-edits.checks.json; both edited regions still byte-match) - sibling edit or off count, not retro-distinguishable | 1 | finding7-honesty-edits#2 deep check disclosure |
| 12 | First Edit call reported a harness timeout at 30000ms (execution note, memory/runs/mickey17_v2/runs/gstd-rungs-20261011/lanes/finding7-honesty-edits.json); byte re-read proved the edit had landed (no double-apply) | 1 | finding7-honesty-edits execution notes |
| 13 | Date-provenance quirk: run dir named gstd-rungs-20261011 while one session context stated 2026-10-10; unresolvable from bytes | 1 | gps-wilson-tests#3 deep check note |
| - | Tombstoned lanes | 0 (run metadata `tombstoned: []`) | run metadata |
| - | Refired lanes | 0 (run metadata `refired: []`) | run metadata |

## NEXT REGISTER (top 10 residuals, one seat one sitting)

1. **SIBLING-WILSON seat**: re-derive the 20 sibling assertions (`tests/test_verdict_feed.py` 10, `tests/test_gps_dedupe.py` 5, `tests/test_gwap_to_gps.py` 5) to Wilson lower bounds; run all three suites; bank the pytest tails verbatim. Unblocks gps-wilson-tests#3 and clears the run's only exclusion.
2. **COMMIT-HARNESS seat**: commit `tools/consensus_harness.py` (currently untracked) and flip RUNNERS.md's git-clone route from post-commit-only to live.
3. **REBANK-COLDEST seat**: rerun the bare-tree fixtures run with output rooted in the estate runs dir (or copy the temp run in) so `20261011T023240Z` is estate-banked, not attested.
4. **TAGS-ARTIFACT seat**: curl `http://100.96.161.76:11434/api/tags`, land the CHECK dict as an artifact beside RUNNERS.md; upgrades device-runner-onepagers#4 from same-chain-verified to verified.
5. **ESCALATION-COVERAGE seat**: restore escalate-path / 3-tier / 2-attempt coverage via a record_series seeded to Wilson bounds >= 0.85 (or a `Constraints(min_confidence=0.95)` no-cost-cap cascade), each gap kept named in-test (gps-wilson-tests#2 residual).
6. **TERMUX-HAND seat (operator hand)**: paste the t90 + pixel one-pagers on-device, append banked-runs table lines (device, run_id, rate, verdict); converts the cross-device-runner gap from on-paper to executed.
7. **SCP-ROUTE seat**: exercise one scp bank from any device to `foste@100.96.161.76` (or the Taildrop fallback) to prove the banking route end to end.
8. **GPS-RERUN seat**: fresh full run of `.venv/Scripts/python.exe -m pytest tools/gps_mcp/test_gps_mcp.py -q` (the 683s runtime exceeded the verifier seat's 600s single-command ceiling), bank tail + exit code; upgrades gps-wilson-tests#1 to fully verified.
9. **CARD-DRIFT seat**: audit the +72-byte drift on `watch/inbox/gstd_perimeter_design_20261010/CARD.md` outside finding7's two regions (lane recorded `bytes: 6192`, memory/runs/mickey17_v2/runs/gstd-rungs-20261011/lanes/finding7-honesty-edits.json; deep check read 6264, memory/runs/mickey17_v2/runs/gstd-rungs-20261011/lanes/finding7-honesty-edits.checks.json); name the sibling edit or correct the lane record.
10. **GB-SEND seat**: send the qualifier-kept addendum into the GB thread; the CARD bytes prove readiness only, usage is forward-looking (finding7-honesty-edits#0 scope caveat).

## INSTRUMENT APPENDIX (verbatim from the script)

### FIDELITY

- rows with all of quote/source/steal/estate_status non-empty: 12/12 (100.0%)

### VERIFIER TABLE (persisted verdicts)

- lanes with persisted checks: 3
- verdicts: deep_tier2 12 (verdict split: same-chain-verified 2, unconfirmed 1, verified 9), supports 12 (supports split: no 6, yes 6)
- deep_tier2 join: 12/12 row_keys match a lane row

### WIDTH-ECONOMICS

- rows/lane: median 4, max 5, min 3
- top-10 lanes share: 100.0%
- exact cross-lane duplicate quotes (normalized): 0
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

### URL LIVENESS (scripted at fold time)

- unique URLs: 1; fetched: 1; skipped non-public: 0; live: 1; dead/blocked-status: 0

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

---

Fold provenance: casualty header, PRISMA flow, scoreboard, TOP-K ranking, and all instrument counts copied verbatim from `memory/runs/mickey17_v2/runs/gstd-rungs-20261011/FOLD_SECTIONS.md` (script sha256 58bd72c79c6d). Claims, quotes, steals, gaps, and pytest tails quoted from the three lane JSONs in the same directory; deep-check evidence summarized from the persisted `.checks.json` verdicts (supports split and deep counts re-confirmed against the archive bytes this sitting). No number in this fold is seat-carried.
