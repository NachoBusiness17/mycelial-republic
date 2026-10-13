# MASTER FOLD: MICKEY-17 v2.1, run dogfood2-20261007 (execute genre)

- folded_at: 2026-10-07T11:39:14Z by fold script sha256 58bd72c79c6d
- lane archive: memory/runs/mickey17_v2/runs/dogfood2-20261007/lanes (15 lane files, read whole by this folder seat)
- scripted sections (CASUALTY HEADER, SCOREBOARD, FIDELITY, VERIFIER TABLE, WIDTH-ECONOMICS, PRISMA FLOW, TOP-K, URL LIVENESS) are verbatim from memory/runs/mickey17_v2/runs/dogfood2-20261007/FOLD_SECTIONS.md; the prose around them is the folder's. Any number not from the script or the lane files is tagged `carried`.

**The one-paragraph read.** This was a run that checked the checkers, and the checkers mostly held: 15 lanes fired, 15 landed, zero parse errors, zero duplicate quotes, zero tombstones, 12 of 12 deep tier-2 verdicts verified. But the run's real law-shaped finding is that what failed was not code, it was wiring. Laws that never reach a fresh seat's context window (d01-seat-boot-pack#2, #3), a detector no cadence watches (d02-stash-seam#4), a register that cannot re-certify its own fleet (d03-stopcert-rows#2), and trust teeth with boundary holes a re-attacker walked straight through (d15-trust-teeth-retest#0, #1, #4). Structure decides behavior. These are the places where the structure still permits the old behavior, and the register below names the single sittings that close each one.

## CASUALTY HEADER (verbatim, scripted)

- fired: 15
- landed (parseable files): 15
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## SCOREBOARD (verbatim, scripted)

- rows: 73
- estate_status: executed 59, executed-with-deviation 10, blocked 2, owed 2
- leverage: high 38, medium 33, low 2

Folder cross-check (performed this sitting, not scripted): hand-tallying estate_status and leverage across all 15 lane files reproduces 59 / 10 / 2 / 2 and high 38 exactly; the two blocked rows are d02-stash-seam#4 and d03-stopcert-rows#2, the two owed rows are d08-reflux-delta#3 and d09-nha-tiering#4.

## PRISMA FLOW (verbatim, scripted)

- identified: 73
- screened: 73 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 73
- invariant: identified == included + excluded **HOLDS** (73 = 73 + 0)

## EXECUTIONS (the script's TOP-K, 12 steals, each with its proof quote)

The script computed this list; a lane-claimed top steal outside it would file as DISPUTED. Folder check: no lane file designates a top steal outside the list, so DISPUTED count is 0. Every steal below carries lane id + row index.

1. **d01-seat-boot-pack#0** (executed, high): executed the boot falsifier live on the 2026-10-07 tree: mag.rib_boot mounted 7/7 law ribs (marathon seventh) with 5 amendments riding after the heads, censused 53 vault .md at 08:26:51Z, repersisted memory/rib_boot.json. Proof quote: `"VAULT: 53 .md ribs censused 2026-10-07T08:26:51.819961+00:00; 7/7 law ribs mounted; 5 amendments riding after the heads"`.

2. **d01-seat-boot-pack#2** (executed-with-deviation, high): re-ran mag.cmd context-pack (mode=full, 7200-char budget, exit 0) at 08:29:23Z; the rendered pack carries ZERO R4b/R5 mechanism bytes and the run itself re-shed the L0d vault-amendments carrier at stage 3. Proof quote: `"total_chars": 9471, "shed_sections": ["L0d rib vault amendments"], "stage": 3`.

3. **d01-seat-boot-pack#3** (executed-with-deviation, high): pinned the flash-tier truncation on today's bytes: flash fields cut at exactly 220 chars (FLASH_MAX_CHARS=220, tools/thought_quantizer.py:118) before the mechanism byte, and the acceptance gate stayed red on the same invariant. Proof quote: `"1 failed, 41 passed in 10.76s"`.

4. **d02-stash-seam#0** (executed, high): live census re-run, 3 disposition rows whose refs byte-match state/stash_sweep_watch_state.json, so no stash appeared or vanished since the 10-06 census. Proof quote: `"HOLD-RECONCILE: may carry an unlanded lane's only copy of its work; reconcile against the tree before any pop; never drop"`.

5. **d02-stash-seam#1** (executed, high): the ask's pytest x2 (fires / stays quiet) ran this sitting. Proof quote: `"2 passed in 1.68s"`.

6. **d02-stash-seam#3** (executed, high): byte-verified the landed detector by reading all 285 lines: check mode flags a new stash whose captured paths intersect the recent-write window, appends one deduped alert per ref; exit contract 0/1/2; both tool and test remain untracked awaiting the coordinator commit. Proof quote: `"The tool has NO drop or pop verb by design: a sweep stash may carry an unlanded lane's only copy of its work."`

7. **d02-stash-seam#4** (BLOCKED, high): the TOP-K carries this row because the residual itself is high-leverage. Full entry in the BLOCKED tier below. Proof quote: `"residual: wire check mode onto a patrol cadence (schtasks or the governor loop) so a future sibling sweep is caught inside the 900s window instead of at the next manual run"`.

8. **d03-stopcert-rows#0** (executed, high): reclassified all 15 unknown STATUS-ROW scripts against fresh byte truth; REGISTRY.jsonl 143 to 158 lines as a pure CRLF tail-append; 5 active, 10 unknown, 0 retired. Proof quote: `"verdict": "STATUS-ROW", "checks": [], "status": "active", "status_basis": {"retired_md": false, "promoted_in_retired_md": true, "registry_row_count": 1`.

9. **d03-stopcert-rows#1** (executed, high): executed register R6's second half: the 5 game-dig veins that had zero registry rows gate-checked, all FAIL exit 2 on hard-fail G4-salvage, check rows landed REGISTRY lines 138-143, FIRE_LEDGER grew 29 to 35. Proof quote: `"workflow_gate FAIL digest=b550cf5f9e47 script=.zcode/workflows/game-dig-coop-social.dwf.ts"`.

10. **d04-graph-orphan#0** (executed, high): dry census re-run idempotent: heal add_edges=0, already_healed=0; the 1066 survivors are 826 ambiguous plus 240 zero-story demotion candidates. Proof quote: `"RESULT: DRY census=1066 orphans heal=0 demote=1066"`.

11. **d04-graph-orphan#2** (executed, high): the 10-06 before/after banked with the arithmetic closed from bytes, not hand-copied. Proof quote: `"arithmetic: heal targets 117 + anchor modules 22 = 139"`. Condition per d04-graph-orphan#4: the 1205 before-figure is ask-carried (the landed r4b before-census reads 1,203, a 2-orphan tree shift of the class that receipt itself documents); the fold rules the arithmetic corroborated, the exact before-figure conditioned on that disclosure.

12. **d05-meter-alarm#0** (executed, high): the meter alarm layer verified landed byte-wise (banked by the prior dogfood-100m-20261006 d05 lane, re-proven this run, disclosed as a negative). Proof quote: `"WORSENED - last 7d rate > prior 7d rate (the 2026-10-06 / LATEST line read 126 vs prior 108 with no / alarm at all; this leg is that check)."` (line breaks normalized with slashes).

### Verifier notes (conditions, not contradictions)

- Scripted verifier table: 73 tier-1 supports verdicts (53 yes / 20 no), 12 deep tier-2 checks all verified, deep join 8/12 row_keys (4 join-misses carry no exclusion weight, labeled not fatal by the script).
- d05-meter-alarm#3's ratchet enumeration ("scope 10 files hits 2 registered 2") is a moment snapshot of a moving tree; the deep check re-ran the gate live (`tools/violation_ratchet.py check --changed`, PASS, NEW=0 at scope 17) and could not reproduce the earlier counts at any later moment. The PASS + NEW=0 substance is verified; the counts are moment-bound. Rule with conditions: trust the verdict, not the snapshot numbers.
- d14-freelfleet-verify#4's sentence "re-confirms the COOL class live on 2026-10-07, 0 x 429 in 5 width-1 asks" is only partially proven: the deep check found the 2026-10-07 ledger carries 0 x 429 over 130 asks with zero OpenRouter lanes in the set, and no on-disk artifact names a 5-ask sweep. The R062 receipt verification half of the row is byte-proven; treat the live-reconfirmation clause as ledger-true over a different shape.
- d03-stopcert-rows#0's "stop-cert index verified empty before and after" leg was reported by the deep check as not evidenced by landed bytes; the reclassification bookkeeping itself is byte-proven. The leg stands unverified, not false.
- d09-nha-tiering#1's warm_state snapshot (08:29:13Z, index 11580) was superseded on disk by same-day regeneration (09:33:09Z, index 11595) before the deep check read it; the deep check ruled it superseded, not falsified, and the d01 receipt at 08:29:23Z corroborates the in-window door run.

## BLOCKED TIER (every blocked row, its reason, its next-sitting unblock)

Scripted blocked count: 2.

**B1. d02-stash-seam#4** (row_id `residual-cadence-open`, negative-first-class, leverage high).
Reason: no patrol cadence (schtasks or governor loop) runs stash_sweep_watch check mode, so a future sibling sweep is caught only at the next manual run, never inside the 900s detection window. This run's finish line names only tools/stash_sweep_watch.py, its tests, and memory/attention.md, and the disjoint-ownership lane law bars this lane from minting scripts/ patrol-registration files it does not own. The deep check confirmed the negative by exhaustive enumeration: 25 scheduled tasks inspected, zero reference stash_sweep_watch; grep over mag/governor_autorun.py, mag/, scripts/, configs/ returns nothing.
Next-sitting unblock: one lane whose finish line names scripts/ registers the cadence in a single sitting: a MagStashSweepWatch schtask modeled on scripts/register_census_patrol_task.ps1 (5-15 min cadence, log logs/stash_sweep_watch.log, alert-only on exit 1), or a governor-loop hook on check mode (d02-stash-seam#4 steal field).

**B2. d03-stopcert-rows#2** (negative-first-class, leverage medium).
Reason: 10 of the 15 STATUS-ROW scripts could not honestly leave unknown from the three instruments this ask bounded: 9 scripts drifted from their last PASS certs with no fire rows, and ractor-engine.dwf.ts drifted AGAIN after its 2026-10-06T22:29:05Z re-cert (current bytes 403c5076482f vs row digest d8d63f619ab9, REGISTRY line 154), so register R5's re-cert residual stands open. The ask bounded gate checks to the 5 game-dig veins; the register's own bounds, not lane laziness, kept the other 10 unchecked.
Next-sitting unblock: 10 single-script gate checks, one per residual unknown (drop-dig, fill-ball, game-mechanics-deep-dig, librarian-expedition, music-cut, ractor-engine, salon-mine, the-50, tree-doctrine-dig, wide-dig), ractor-engine first per register R5; resolves each unknown from fresh byte truth in one sitting (d03-stopcert-rows#2 steal field).

## OWED (scripted owed: 2; one bounded refill each per the casualty classification)

**O1. d08-reflux-delta#3** (negative-first-class, owed, leverage low): the delta-state probe carries zero pytest coverage; grep over tests/ matched no file (exit 1), so the only gate over the delta path is the probe's own verify(). Next sitting: land tests/test_reflux_delta_probe.py covering init/note/append round-trip plus verify and fold on a tmp lane dir (d08-reflux-delta#3 steal field).

**O2. d09-nha-tiering#4** (negative-first-class, owed, leverage medium): the estate's cold door is pointer-only and could not find the NHA definition its own lane consumed; corpus_search over the freshly rebuilt index matched the phrase only in an arXiv fulltext, because the FTS5 build indexes path and title columns only (tools/corpus_fts_rebuild.py:77-79). Next sitting: add a body column to the external-content build, or a sanctioned body-search verb beside corpus_search, so cold-tier phrases resolve without leaving the estate (d09-nha-tiering#4 steal field).

## NEGATIVE RESULTS (counted reasons table)

Tombstones: none (scripted tombstoned: []). Zero hard failures subtracted from owed.

| # | Reason (counted) | Count | Where (lane#row) | Row status |
|---|---|---|---|---|
| 1 | Residual left open: detector landed but no patrol cadence watches it | 1 | d02-stash-seam#4 | blocked |
| 2 | Register unknowns unresolved: instruments bounded to the 5 veins; ractor-engine re-drifted | 1 | d03-stopcert-rows#2 | blocked |
| 3 | Provenance gap: no landed receipt carries the 10-06 heal event; before-figure 1205 is ask-carried | 1 | d04-graph-orphan#4 | executed-with-deviation |
| 4 | Coverage gap: an organ with zero pytest files | 3 | d08-reflux-delta#3 (delta probe); d03-stopcert-rows#4 (zero stop-cert coverage in tests/); d14-freelfleet-verify checks (no fleet test file, fleet gates used instead) | owed 1, executed-with-gap 2 |
| 5 | Ledger drift: 5 of 17 prior-seat rows are hard false positives (bare "rate limit" needle caught network chatter) | 1 | d12-crymine-live#4 | executed-with-deviation |
| 6 | Fleet health dead: both OpenRouter free lanes down since 2026-10-05T14:33Z; fleet is 5/7 | 1 | d14-freelfleet-verify#1 | executed (finding filed, not papered) |
| 7 | Configured but never proven: reasoning_content banking leg has zero landed ledger evidence | 1 | d14-freelfleet-verify#4 | executed (finding filed) |
| 8 | Phantom artifact caught and cured in-session: probe miskeyed scene_id grammar, reported unbanked=103, cured to 0 | 1 | d10-gps-metabolism#3 | executed-with-deviation |
| 9 | Tool pre-existed untracked from the prior seat; this run executed the proof gap instead of rewriting | 1 | d16-relay-recheck#0 | executed-with-deviation |
| 10 | Ask's start path wrong: DAWN_REPORT lives at watch/inbox/, not under ouroboros_20261005/ | 1 | d16-relay-recheck deviations[0] | deviation filed |
| 11 | Scheduled fire not observed: today's 9:30 MagLawPackDaily run was still pending at verify time | 1 | d01-seat-boot-pack#1 | executed with gap named |
| 12 | Disclosed negatives: bytes banked by the prior run, not authored this session; append path proven by production receipts; alert surface git-ignored | 3 | d05-meter-alarm negatives[0-2] | disclosures |
| 13 | Attack-scope limits: 2 of 7 teeth attacked; seal-deletion angle stood down after pre-reading chain verify; lane-authored control fixture refused by the pre-write hook (refusal output carries the negative control) | 3 | d15-trust-teeth-retest negative_findings[0-1] | disclosures |
| 14 | Non-event, explicitly not owed: no outage occurred, so no outage row owed; fence proven by two no-socket refusals instead | 1 | d12-crymine-live note | non-event |
| 15 | Full-repo pytest not run (out of lane scope, named in the lane file, never claimed) | 3 | d04-graph-orphan#3, d08-reflux-delta#3 note, d16-relay-recheck deviations[3] | scoped-out, disclosed |

Total negative items counted: 23 across 15 reason lines. Every line cites lane id + row index.

## NEXT REGISTER (top 10 residuals, one seat one sitting)

Ranked by leverage and cross-cutting effect. Each is a single-sitting unit with its acceptance named. Every row cites lane id + row index.

1. **Coordinator commit of the 2026-10-06/07 working-tree drift.** The 10-06 landing (M tools/freshness_check.py, M state/CURRENT.md, untracked freshness tests) gates CURRENT.md's STALE meter on commit age, so the gate reads FAIL within hours until committed; the same uncommitted drift holds d02's untracked detector and tests, d05's untracked alarm layer and test, and d12's 17 drift rows. Cure is one commit, never another refresh loop (d06-canon-adjudication#3 steal; corroboration in d02-stash-seam#3, d05-meter-alarm negatives[2], d12-crymine-live#4).
2. **Close the trailing-comment gate hole.** strip_comment_lines (tools/workflow_gate.py:107-123) is line-granular, not token-granular, so a gate PASS still certifies spelling for the trailing-comment shape. Fix: strip trailing // comment spans per line (token-level, string-literal aware) before the G1-G7 regexes, then mint the forged-payload scenario card from the FAIL row the fixed gate produces. Repro: `.venv\Scripts\python.exe tools\workflow_gate.py check --script watch/inbox/ractor_engine/2026-10-07-d15-retest/probes/d15_trailing_comment_shapes.dwf.ts --no-register` (d15-trust-teeth-retest#0).
3. **Close the code-attribution phantom hole.** A notable aggregate attributed in-sentence to a live code path is never counted (numbers-checked=1 for two notable quantities) because RECORD_SOURCE_SUFFIXES filters .py paths before the unresolved branch (tools/citation_lint_numbers.py:208-236). Fix: emit a warn-tier CODE-ATTRIBUTION finding when a notable number's sentence names only code-class paths. Repro: `.venv\Scripts\python.exe tools\citation_lint.py check --files watch/inbox/ractor_engine/2026-10-07-d15-retest/probes/citation_codepath.md` (d15-trust-teeth-retest#4).
4. **Close the self-minted receipt hole.** receipt_carries_measured_width (tools/workflow_gate.py:279-295) verifies receipt bytes only, so the width-50 exception self-certifies from a receipt the attacking lane authored in the same sitting. Fix: require the envelope receipt to predate the script (mtime or seal-ledger stamp) or be witnessed by an existing index row (d15-trust-teeth-retest#1).
5. **Land the cold-to-hot pull door.** NHA's actual contribution, the inter-tier pull, has no door: zero corpus references in mag/context_pack.py (probe exit 1), the only goal-keyed puller is env-gated off, and tools/query_broker.py has zero production callers. Fix: wire one goal-keyed corpus_search (or query_broker) pull feeding a budget-clipped pack slice; acceptance: the probe goes non-zero and the pack carries a corpus-cited block (d09-nha-tiering#2).
6. **Grow the percolator fine-grained domain tag.** 611/620 invariant rows carry one domain value, so the HyperThink probe can only test the behavioral-vs-9-minority boundary; the strong fine-subject claim stays untestable. Fix: add the per-row domain/surface tag at the percolator feed, then rerun the probe unchanged (d07-hyperthink-quantizer#3; carried unchanged from the 10-06 lane, d07#1).
7. **Adopt the delta chain for runner_state.** The conversion probe is proven live (seq 4 appended, chain verifies), but the snapshot writer still rewrites whole state at mag/lane_runner.py:124-149. Fix: switch the writer to the delta chain as a separately-gated adoption ask per the probe's own LAW block (d08-reflux-delta#0, d08-reflux-delta#1).
8. **Make the law bytes survive the flash slice.** FLASH_MAX_CHARS=220 (tools/thought_quantizer.py:118) cuts every vault amendment before its mechanism byte, and the L0d carrier sheds at stage 3. Fix: shorten the five flash fields or raise the cap so the mechanism bytes ride; acceptance: the red test_quantized_laws_section_renders_in_default_budget goes green, then MEASURED ON greps non-zero in a fresh pack (d01-seat-boot-pack#3, d01-seat-boot-pack#2).
9. **Register the stash-sweep patrol cadence.** The blocked B1 cure: one scripts/-owning lane lands MagStashSweepWatch (or a governor hook) so check mode runs inside the 900s window instead of at the next manual run (d02-stash-seam#4).
10. **Resolve the 10 unknown register scripts.** The blocked B2 cure: 10 single-script gate checks, ractor-engine first (R5), each unknown resolved from fresh byte truth (d03-stopcert-rows#2).

Owed refills riding the same window (bounded, scripted owed: 2): d08-reflux-delta#3 test file, d09-nha-tiering#4 body-search door. Further residuals named in the lane steals (OpenRouter key re-provision d14-freelfleet-verify#1, per-class bench battery d12-crymine-live#2, GPS feeder gap d10-gps-metabolism#0, task_shape hardening d10-gps-metabolism#4, publish_recheck pre-push wiring d16-relay-recheck#0, heal-receipt line d04-graph-orphan#4, VAULT_RIBS expansion d01-seat-boot-pack#4, G4 amend pass for the 5 veins d03-stopcert-rows#1) stay open behind these ten.

## APPENDIX: remaining scripted sections (verbatim)

### FIDELITY

- rows with all of quote/source/steal/estate_status non-empty: 73/73 (100.0%)

### VERIFIER TABLE (persisted verdicts)

- lanes with persisted checks: 15
- verdicts: commands_run 3 (<no-value-field> split: <dict> 3), deep_tier2 12 (verdict split: verified 12), not_run 2 (<value> split: epoch stamp: deliberately not applied; two receipts reserve stamping for the operator (night_shift_20261005_close.md decision 2, watch/inbox/d7_pheromone_metabolism_20261005.md); the counterfactual collapse number is banked instead 1, violation ratchet (tools/violation_ratchet.py): this lane touched no mag/ or tools/ production file (probe + reports live in the run dir), so the pre-push ratchet surface did not change 1), supports 73 (supports split: no 20, yes 53)
- deep_tier2 join: 8/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 4

### WIDTH-ECONOMICS

- rows/lane: median 5, max 5, min 4
- top-10 lanes share: 68.5%
- exact cross-lane duplicate quotes (normalized): 0
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

### URL LIVENESS (scripted at fold time)

- unique URLs: 0; fetched: 0; skipped non-public: 0; live: 0; dead/blocked-status: 0

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

## PROVENANCE

- Scripted numbers: memory/runs/mickey17_v2/runs/dogfood2-20261007/FOLD_SECTIONS.md (script sha256 58bd72c79c6d, folded_at 2026-10-07T11:39:14Z).
- Lane rows and quotes: all 15 files in memory/runs/mickey17_v2/runs/dogfood2-20261007/lanes/ (d01-seat-boot-pack, d02-stash-seam, d03-stopcert-rows, d04-graph-orphan, d05-meter-alarm, d06-canon-adjudication, d07-hyperthink-quantizer, d08-reflux-delta, d09-nha-tiering, d10-gps-metabolism, d11-passk-coverage, d12-crymine-live, d14-freelfleet-verify, d15-trust-teeth-retest, d16-relay-recheck), read whole by this seat this sitting.
- Verifier conditions: the run's persisted laneChecks and deepChecks (15 lane check records, 12 deep tier-2 verdicts all verified), as handed to this seat in the fold ask.
- `carried` tags: none needed; every number in this fold traces to the script or a lane file. The two cross-checks the folder ran itself (estate_status/leverage hand-tally; DISPUTED scan over lane files) are labeled as folder checks above, not as scripted numbers.
