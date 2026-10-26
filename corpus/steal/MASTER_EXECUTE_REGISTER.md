# MASTER EXECUTE REGISTER — fold of run 2026-10-05-exec

Folded 2026-10-05 by the fold seat. Written twice, byte-identical:

- estate copy: `corpus/steal/MASTER_EXECUTE_REGISTER.md`
- workspace copy: `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_EXECUTE_REGISTER.md`

**Law of this document.** The register is the statute; the twelve lanes are its administration; the script (`tools/mickey17_v2_fold.py`) is the census; this fold is the record. Every count below is the script's, verbatim. Every claim and proof quote comes from the lane archive `memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/` (13 parseable files, read in full this sitting). Anything from neither source is tagged `carried` and names what it rode in on. Contradictions are never averaged; they are ruled with conditions, in place.

## CASUALTY HEADER (scripted, verbatim)

- fired: 12
- landed (parseable files): 13
- landed-empty (0 rows): 1 — e11-catalog-research.measure.out
- parse errors: 0
- missing (no file): -1
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## PRISMA FLOW (scripted, verbatim)

- identified: 59
- screened: 59 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 59
- invariant: identified == included + excluded **HOLDS** (59 = 59 + 0)

## SCOREBOARD (scripted, verbatim)

- rows: 59
- estate_status: executed 50, executed-with-deviation 8, blocked 1
- leverage: high 35, medium 21, low 3

## EXECUTIONS — the script's TOP-K with proof quotes

The script ranked all 59 rows by (leverage, lane id, row index) and published the top 12. Nothing outside that list may be presented as a top steal of this run. Each entry carries lane id + row index, the executed claim, and the proof quote from the lane archive. Seven of the twelve also carry a tier-2 deep-check verdict (`carried`, from the fold gate's verification pass given to this fold).

1. **e01-index-compact#0 [high]** — Wrote `tools/estate_index_compact.py` (one read-only streaming pass, counters only) and ran `--check` on the live 4.15GB dashboard copy; every register-truth count byte-matched (rows 10,661,260; .source 9,524,538; file 4,150,418,528 bytes; bad 0), refinements banked (4,072 non-.source hook-state rows; single-root retire 86.0005; all-rows retire 89.376). Proof:

   ```
   PROFILE rows=10661260 source=9524538 named_root_source=9168740 mimosa_lane_source=350503 other_nested_source=5295 hookstate_rows=9528610 retire_single_root=86.0005 retire_two_roots=89.2882 retire_source=89.3378 file_size_bytes=4150418528 bad_rows=0
   ```

   Tier-2: verified (`carried`) — with the condition that the exact EXIT=0 pass is anchored by the byte-exact lane receipt, not re-executable today: the index was legitimately rewritten after the run (a fresh `--check` on the current tree reads different counts and exit 1).

2. **e01-index-compact#1 [high]** — Added the r04#1 skip list to the writer's walk and write path (SKIP constants :59-61, `prune_hookstate` wired :124, `is_skip_path` backstop wired :138, `skip_list_hits` into last_run.json :180 and the run print :208); an inline harness via .venv proved 4 prune + 7 backstop assertions; the full walk was never executed here (it would rewrite the 4.15GB watch master). Proof:

   ```
   if is_skip_path(rel_str):
                   skip_list_hits += 1
                   continue
   ```

   Tier-2: verified (`carried`). The probe also found, as a byte-caveat the row itself did not claim: the backstop over-matches lookalike `x.mimosa` paths the prune spares — it fails safe (over-skips), filed for the register, not a violation.

3. **e01-index-compact#2 [high]** — Stopped the :138 `shutil.copyfile(MASTER, DASH_MASTER)` that re-fattened the second 4.15GB copy every walk; the dashboard side now gets a small pointer file naming the watch master, receipt comment cites the two fsutil runs and the re-broken 09-30 dedup. Proof: `full master copyfile stopped per r04#2 2026-10-05; read the watch master`. Tier-2: verified (`carried`), with the disk-state condition that the dashboard copy was rewritten at 06:57 to 2,523,006,985 bytes by a writer the probe could not attribute from bytes; the execution claim holds (the copyfile is gone, the pointer is live, the indexer never writes the copy).

4. **e02-index-query#0 [high]** — Minted `/api/v1/estate/query` in `dashboard/server.py` (route in do_GET after the links/tail door, plus `_estate_query_payload`, `_raw_mimosa_component`, +153 lines), filters `?q=&proj=&rel=&temp=&limit=` (default 250, cap 2000, grep semantics, exact counts, no writer change), D10 skip list honored server-side, raw boundary fast-skip for the 9.5M-row mass with exact parsed-path re-check. Proof: `ESTATE_QUERY_SKIP_COMPONENTS = frozenset({".mimosa"})`. Tier-2: verified (`carried`; route at server.py:751, numstat 153/0, landing commit e80f48b8f, /data door untouched at :777).

5. **e02-index-query#1 [high]** — Repointed `the_index.html` (the line-118 whole-file fetch, 4.15GB per load) at the filtered door: server-side filters, 900ms debounce with Enter immediate, stale requests aborted; trade-off named honestly: each search is now a ~31-46s server grep instead of a 4.15GB browser download. Proof: `fetch("/api/v1/estate/query?" + params.toString(), { cache: "no-store", signal: aborter.signal })`.

6. **e02-index-query#2 [high]** — Named curl test against a locally-started instance of the changed code (repo venv, 127.0.0.1:8799; the operator's :8765 untouched): HTTP 200 in 31.5s; skip arithmetic closes exhaustively (9,524,538 + 11,098 + 4,072 = 9,539,708 skipped; + 1,121,552 kept = 10,661,260 scanned); zero returned rows carry a .mimosa component. Proof: `total_kept: 1121552 | scanned: 10661260 | skipped_mimosa: 9539708`.

7. **e03-rib-vault#0 [high]** — Gave `mag/rib_boot.py` a real vault mount (live census of memory/rib/*.md plus the five law ribs mounted as law-head bytes, read-only) beside the bus mount, and retired the stale "51 frozen ribs" constant to a quoted historical note, the count measured at every boot. Proof: `VAULT: 52 .md ribs censused 2026-10-05T06:07:35.497565+00:00; 5/5 law ribs mounted`.

8. **e03-rib-vault#1 [high]** — Appended the POST-DATUM 2026-10-04 amendment block to `RIB_INFERENCE_BUDGET_20261001.md` (mint untouched, append-never-rewrite), naming d4_thinking_probe.md and both cured code sites, so the rib stops carrying the refuted "thinking-off by construction" row unamended. Proof: `THE LAW IS NOW: omission is a MEASURED ON state.` Tier-2: verified (`carried`; diff 30 added / 0 deleted, pure tail append).

9. **e03-rib-vault#2 [high]** — Appended the POST-DATUM amendment riding the DEEPSEEK-V4.1-FLASH row (row untouched) so the boot-time distillation carries the settled HOW: sent-explicit off, omission is the ON state, thinking-on scoped to depth=design at 32K+ substance-gated, plus the conditions-suspect note. Proof: `SCOPED EXCEPTION (PRIORS row 8 / operations.md D3, POST-DATUM): thinking-on rides ONLY at`.

10. **e03-rib-vault#3 [high]** — Fired the FREE_USAGE resolving instrument for real (13 lanes, cool width-1 spaced vs heat 13-wide x3 waves, 52 asks, every outcome logged), resolving the 4-day D3 contradiction conditions-bound; verdict rows appended to both ribs, receipt banked in `watch/inbox/ribvault_20261005/`. Proof: `zero 429 at drip rate; 2 x 429 (poolside/laguna-xs-2.1:free, upstream rate-limit) at forced`.

11. **e04-width-gate#0 [high]** (archive row 1) — Added the G8-width-shape dispatch-shape check to `tools/workflow_gate.py`: every declared max_concurrency must be 3 or less unless the script carries an `envelope-receipt:` stamp naming an existing watch/inbox measured-envelope receipt; hard FAIL exit 2, no soft family; spec-first docstring lines and check body in the same edit set; stale "seven gate checks" docstring repaired to G1-G8. Proof: `dispatch shape is the retry strategy (TETHERED_LINK width law): declared max_concurrency <= 3 unless the script documents a measured envelope receipt`. Tier-2: verified (`carried`; the probe ran the landed predicate live: width 10 unstamped fails exit 2, stamped with an existing receipt passes, stamp naming a nonexistent file fails).

12. **e04-width-gate#1 [high]** (archive row 2) — Landed two scenario cards (G8_width_shape hard-fail, G8_width_exception receipt-exception pass) plus two fixtures, no existing card or fixture touched; deviation filed: the seat-law hook blocked the Write of the deliberately-red payload and Mimosa rejected the heredoc reroute, so the fixture landed via touch + Edit fill, final bytes proven by the mint run and the suite. Proof: `Script declares max_concurrency: 10 and carries no envelope-receipt stamp: under the 2026-10-05 G8 semantics the row fails hard (exit 2)`. Tier-2: verified (`carried`; all four files are pure git additions, and the cited FAIL row digest 8e41d0903ece recomputes from the committed fixture bytes).

**Finish-line note.** The archive evidence block (`carried`) shows e04-width-gate#3 ran the LAW-12 scenario suite twice, both exit 0: 9 cards validated read-only, pass_control clean with all 8 gates; the tier-2 pass on e04-width-gate#0 independently re-ran the same suite green.

### DISPUTED (the script's rule, applied)

The gate reads: a lane-claimed top steal outside the TOP-K list files as DISPUTED. The lanes claim 35 rows at high leverage (scripted scoreboard); the script's ranking kept 12. The other **23** file as DISPUTED — executed work, all carrying `executed` or `executed-with-deviation` in the archive, but not top steals of this run, and no prose here may promote them:

e04-width-gate#3; e05-transfer-debt#0, #3, #4; e06-fidelity-audit#0, #1; e07-receipt-bindings#0, #1; e08-writer-guard#0, #1, #2, #4; e09-cr-cure#0, #1, #3; e10-env-door#0, #1, #2; e11-catalog-research#0, #2; e12-falsification-gate#0, #1, #3.

Count: 23 (35 claimed high − 12 in the list). Verifier coverage condition (`carried`): e06-fidelity-audit's five rows carry no tier-1 verdicts (the verifier crashed on that lane), so its two disputed rows stand on the archive receipts alone.

## BLOCKED TIER

One row — the run's only `estate_status: blocked`:

- **e07-receipt-bindings#3** — The coordinator's push is red until 7 pre-existing citation-lint PHANTOM-NUMBER findings are fixed or accepted by name: 6 in `memory/rib/RIB_INFERENCE_BUDGET_20261001.md` and 1 in `memory/rib/RIB_MODEL_GARDEN_ROUTING.md:158`. **Reason:** append-never-rewrite forbids the lane rewriting 2026-10-01 mint prose, and `configs/citation_lint_baseline.json` carries 4 accepted entries (none covering these two rib files), so the 7 findings remain unregistered; the lint's prose class was tripped by `check --changed` on the working tree, which this .py-only lane did not mint. *(Sentence corrected at fold revision 2026-10-05: the original draft said the baseline had 0 entries — a phantom count of exactly the class this pipeline hunts, struck on fresh-reader critique; the file's 4 accepted entries date to commit 395e4aae6, 2026-10-04 08:05, verified against the file bytes at revision time.)* **Next-sitting unblock** (the row's own steal field): the rib owner or coordinator fixes the 7 citations, or accepts them by name via `--baseline configs/citation_lint_baseline.json`; the reproducing command is `.venv/Scripts/python.exe tools/citation_lint.py check --changed`. **Condition on the count, ruled not averaged:** e02-index-query#3 read 2 findings and e03-rib-vault read a 7-count with a coarser enumeration earlier the same morning, on the same moving working tree; the blocked row's 6 + 1 split is the figure this fold rules with.

## NEGATIVE RESULTS (counted reasons)

| # | Reason | n | Filed by (lane#row) |
|---|--------|---|---------------------|
| 1 | Citation-lint PHANTOM-NUMBER blockers in pre-existing mint prose | 7 findings (2 files) | e07-receipt-bindings#3 (blocked row); earlier moments: 2 read by e02-index-query#3, 7-counted by e03-rib-vault |
| 2 | Ratchet NEW debt, file-too-long, one working-tree file | 1 debt | e01-index-compact#4 (`mag/dirac_loop.py:415`, moment 01:47) and e03-rib-vault (`:405`, moment 02:11) — one moving 751-line sibling diff, two readings, never averaged |
| 3 | Pre-existing test reds, filed not fixed | 2 | e04-width-gate#4 (`test_every_pre_push_ok_consumer_is_enumerated`, CRED-SHAPE arm unpinned since d349ce7d2); e11-catalog-research#4 (`test_run_tags_writes_owner_column` frozen-clock time-bomb, crossed the fresh<7d boundary ~2026-10-02) |
| 4 | Live service negatives observed and filed, not fixed by the lane | 3 | e02-index-query#4 (:8765 serves pre-change code, 404s the new door; two PIDs); e10-env-door#3 (svchost iphlpsvc portproxy rule holds 8765, non-admin shell cannot delete; publish parked); e03-rib-vault r06#2 (providers.yaml `ling-3.0-flash-fin:free` now 404s) |
| 5 | Auth-saturated march fires inside the cage | 2 fires, 8 calls | e10-env-door#2 — all 8 tranche calls HTTP429 (account saturated by sibling lanes on the same plan); the halt gate stopped both runs by design; the 0-ok halt was refused as a hollow batch, never banked as success |
| 6 | Errno-22-class residuals on sibling write paths | 2 named | e08-writer-guard#4 — `_mirror` dashboard-copy write, live hit 2026-10-05T03:59:15Z (`carried`, tier-2: since cured by commit 3b271d44c); `mag/prose_census.py:145` (`carried`, tier-2: still live at verification) |
| 7 | Structural infidelities banked about the seed system | 3 | e06-fidelity-audit#1 (all 131 seeds' tape_ref points at the dead 102-row tape; seed-to-steps unwalkable), #2 (all 131 seeds minted 2026-10-03, 8 days post-run: intended side is a reconstruction), #3 (10 of 88 verifier check actors executed unseeded; intended count a bound <=100) |
| 8 | Honest fold-gate failure left standing on purpose | 13 findings | e12-falsification-gate#3 — `--check-master` exits 2 on the real master (`corpus/steal/MASTER_MICKEY17_V2.md`); two are the master's own admitted-phantom class; the gate was deliberately not tuned green |
| 9 | Dark scheduled surface | 1 | e11-catalog-research#0 — no MagCorpusRescanDaily 03:30 fire on 10-05 before the manual run (manifest gap noted as steal) |
| 10 | Harness hook friction, resolved but filed | 2 lanes | e04-width-gate#1 (seat-law hook blocks deliberately-red gate-regression fixtures; Mimosa rejected the heredoc reroute; landed via touch + Edit) and e03-rib-vault (Mimosa SSRF block on the first probe write; rewritten with literal URL + allowlist guard) |
| 11 | Tier-1 verifier coverage gap | 5 rows | e06-fidelity-audit (all five rows: verifier crashed, no supports verdicts; `carried`) |

**Tombstones:** [] — nothing was tombstoned this run; per the casualty header, hard failures would be tombstoned and subtracted from owed, and there were none (parse errors 0, hard failures 0).

**Condition on "landed" (`carried`, tier-2):** the e09-cr-cure strip-at-load cure (all four files, 57-test reproduction included) is verified in the working tree and **uncommitted** at fold time (HEAD 356c90634); the coordinator's commit is what turns it into history.

## NEXT REGISTER (top 10 residuals, one seat one sitting)

1. **dirac_loop ratchet debt.** `mag/dirac_loop.py` carries the run's only NEW ratchet debt (file-too-long over the 400-line cap; read at :415 by e01-index-compact#4 and at :405 by e03-rib-vault — one moving working-tree file, not two debts). Unblock: the owning seat trims under the cap, or the operator accepts by name (`violation_ratchet.py baseline-update --by <who>`). Until then any change set including it blocks pre-push.
2. **Citation-lint acceptance.** Cure the blocked row e07-receipt-bindings#3: fix the 7 phantom numbers in the two rib files, or accept them by name into `configs/citation_lint_baseline.json`; reproduce first with `tools/citation_lint.py check --changed`.
3. **prose_census write path.** tmp+replace `mag/prose_census.py:145` — the one errno-22-class in-place write path still live after 3b271d44c cured the `_mirror` half (`carried`, tier-2). Filed by e08-writer-guard#4.
4. **The --apply sitting.** The destructive rewrite of the 4.15GB estate index artifact runs as its own sitting, alone; the gate already exists (gated refuser, exit 3, touches nothing — e01-index-compact#0). Nothing else opens the data files for write.
5. **8765 admin cure.** Operator, one sitting: `netsh interface portproxy delete v4tov4 listenport=8765 listenaddress=0.0.0.0`, uncomment the parked publish line in docker-compose.yml, `docker compose up -d mag`. Filed by e10-env-door#3.
6. **Serve the query door.** Operator restart of :8765 so `/api/v1/estate/query` answers on the live instance (e02-index-query#4). Condition riding the same sitting: tonight's 23:00 local in-window daemon cycle re-fires the march with the once-per-night gate open; bank rc=0 only with ok-calls, or the hollow-batch refusal of e10-env-door#2 stands.
7. **Percolator review.** Promote-or-kill review of the 10 new candidates through `percolate()` on reviewed signal; the alpha-budget gate never self-compiles (mag/percolator.py:88-92). Filed by e05-transfer-debt#0.
8. **Dead-tape cure.** Point `mag/worldline_seed.py:84` TAPE at the live stream (or deprecate the tape_ref slab), land a regression test that a fresh seed's tape_ref holds its own session rows, then re-mint or annotate the 2,107 dead-tape seeds per the worldline_compact plan. Filed by e06-fidelity-audit#1.
9. **Fold-gate wiring + triage.** The fold seat, one sitting: wire `--check-master` into fold_run.sh and the mickey17-v2 runner (e12-falsification-gate#1), then triage the 13 real-master findings and file errata for the admitted-phantom lines 183, 98, 141 (e12-falsification-gate#3).
10. **providers.yaml retire.** Operator verify-then-retire edit for the 404'd `inclusionai/ling-3.0-flash-fin:free` line (its B2-202 earned line is dead; operators edit providers.yaml, not lanes). Filed by e03-rib-vault (r06#2).

Below the cut, filed and owned elsewhere (ride the negative table): MagCorpusRescanDaily health check (e11-catalog-research#0); the CRED-SHAPE consumers-map one-liner (e04-width-gate#4); the test_catalog_tags clock fix (e11-catalog-research#4); the seat-law fixture-exemption carve-out (e04-width-gate#1); the flight_recorder.load_env strip-at-use sweep, assigned by CSV_VERDICT_20261004 (e09-cr-cure); the FEED-NARROWED actioning (e11-catalog-research#3); the sqlite-spine repoint behind the query door (e02-index-query#0, #1); the seed-timing receipt-law field (e06-fidelity-audit#2).
