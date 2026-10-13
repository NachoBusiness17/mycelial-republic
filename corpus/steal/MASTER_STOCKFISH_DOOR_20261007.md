# MASTER FOLD - STOCKFISH DOOR 2026-10-07 (MICKEY-17 v2.1, genre: execute)

- folded_at: 2026-10-07T11:36Z (counting script sha256 58bd72c79c6d). Prose folded by the folder seat from `memory/runs/mickey17_v2/runs/stockfish-door-20261007/`: FOLD_SECTIONS.md plus all 8 lane `.json` files read in full this fold; tier-1 and deep_tier2 verdicts are the run's persisted verifier records (`<lane>.checks.json` on disk, spot-verified against the gate output this fold: s1-commit-organ 5 rows 3 yes/2 no, s7-pack-recompile 5 rows 1 yes/4 no) as carried in the gate's run metadata.
- Law of the fold: every number is the counting script's; quotes are verbatim lane-row bytes; anything the folder composed or generalized is tagged `carried`. Row indices are 0-based within each lane, matching the script's TOP-K. Every steal sentence carries lane id + row index. No em/en dashes anywhere in this document (run-family fold law).
- Copies: estate `corpus/steal/MASTER_STOCKFISH_DOOR_20261007.md` and workspace `~/.zcode/workspace/default/mickey17_v2/MASTER_STOCKFISH_DOOR_20261007.md`.
- FoldInfo: top_steal_count=12 (the script TOP-K), disputed_count=0 (grep instrument over the 8 lane files found no lane-claimed top steal outside the TOP-K list; the older all-high-rows reading is recorded as a condition under DISPUTED, not averaged).

## CASUALTY HEADER (script, verbatim)

- fired: 8
- landed (parseable files): 8
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## SCOREBOARD (script recount, verbatim)

- rows: 39
- estate_status: executed 33, executed-with-deviation 4, blocked 2
- leverage: high 21, medium 16, low 2

Folder note (`carried` arithmetic): 33 + 4 + 2 = 39, the scoreboard closes on the row count; the four executed-with-deviation rows are s1-commit-organ#0, s2-wire-endpoint#1, s5-dispatch-game#2, s8-golden-bouts#3; the two blocked rows are s1-commit-organ#2 and s1-commit-organ#3 (both in the BLOCKED tier below).

## PRISMA FLOW (script, verbatim)

- identified: 39
- screened: 39 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 39
- invariant: identified == included + excluded **HOLDS** (39 = 39 + 0)

## FIDELITY / VERIFIER TABLE / WIDTH-ECONOMICS / URL LIVENESS (script, verbatim)

- rows with all of quote/source/steal/estate_status non-empty: 39/39 (100.0%)
- lanes with persisted checks: 8
- verdicts: deep_tier2 12 (verdict split: verified 12), supports 39 (supports split: no 10, yes 29)
- deep_tier2 join: 10/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 2
- rows/lane: median 5, max 5, min 4
- top-10 lanes share: 100.0%
- exact cross-lane duplicate quotes (normalized): 0
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)
- unique URLs: 1; fetched: 1; skipped non-public: 0; live: 0; dead/blocked-status: 1
  - HTTP -1: https://arxiv.org/abs/2610.03695 (fresh urllib fetch this sitting, 42461 bytes, same size as audit a...
- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

Folder note on the liveness line (`carried`): the single "dead" URL is a fold-moment transport artifact, not a dead source - the citing lane's own fresh urllib fetch the same sitting pulled 42,461 bytes, the same size as the audit's curl (s4-queen-patch#4 source line and s4-queen-patch#0 quote). Ruled in NEGATIVE RESULTS row 6; the URL may not be cited as dead without a fresh fetch.

## EXECUTIONS - SCRIPT TOP-K, 12 STEALS WITH PROOF QUOTES

(The script's TOP-K is authoritative; its printed lines truncate at ~110 chars, so the full steal text below is the lane row's own, each headed by its lane id and row index. Verdicts are the persisted verifier records; "not deep-checked" = no deep_tier2 entry exists for that row.)

### 1. s1-commit-organ#0 [high] - move 1 executed: the bridge/test drift committed push-never
- Steal: done; deviation banked: first commit attempt failed exit 1 (no changes added) because a concurrent sibling emptied the index between a verified staging and the commit; re-staged and committed in one atomic chain (git add && ratchet && git commit -F), which any dawn lane on this live tree should copy; committed bridge bytes also carry sibling lane s2-wire-endpoint's endpoint wiring with in-code attribution (s1-commit-organ#0).
- Proof quote (row source: mag/llama_cpp_bridge.py): `[mag/run-beta1-factory-build-audi-20260806T231709Z 64178cf5d] BRIDGE+TEST DRIFT COMMITTED, D13 EVIDENCE NAMED`
- Verdict: supports=no at tier 1 (the one-line commit console output covers the commit leg only); deep_tier2=verified - the verifier reconstructed every byte from the commit object: full hash 64178cf5dd4bfad1c05cca67e7e59430a2c7166a, 2 files changed 123 insertions/16 deletions (numstat 64/16 mag/llama_cpp_bridge.py + 59/0 tests/test_selfplay_orchestrator.py), ancestor of HEAD, branch carries no upstream ref (push never fired), fresh ratchet re-run PASS NEW=0. Moment condition (`carried`): the claim's scope=11/hits=2 is bound to the 04:40 commit moment and reads scope=17/hits=10 at the verifier's later moment (sibling drift on the shared tree, all registered); NEW=0 is what reproduces, per the B2-216 snapshot law, never averaged.
- estate_status: executed-with-deviation.

### 2. s1-commit-organ#2 [high] - dawn push blocks at pre-push gate 2 (citation lint) [BLOCKED - full entry in the BLOCKED tier]
- Steal: dawn cure: fix the prose or regen the zknot pages via tools/zknot.py, else accept findings by name via --baseline configs/citation_lint_baseline.json before pushing (s1-commit-organ#2).
- Proof quote (row source: watch/inbox/ractor_engine/2026-10-07-stockfish-door/S1_COMMIT_ORGAN_DAWNLIST.md): `CITATION-LINT: FAIL records=43 anchors=494 numbers-checked=146 blocking=62 warns=157 enforce-tokens=False`
- Verdict: supports=yes; deep_tier2=verified - hook mechanics byte-read (githooks/pre-push:24-25 enforcing; tools/citation_lint_io.py:327-356 scans `git diff --name-only HEAD`, staged plus unstaged), commit 64178cf5d carries zero prose records so none of the findings are its bytes, and the verifier live-reproduced exit 1 (`blocking=70 records=49` at its later moment: same FAIL grammar, working-tree drift grew between moments, the block holds either way). The row's 62/43 is the figure this fold rules with.
- estate_status: blocked.

### 3. s1-commit-organ#3 [high] - dawn push blocks at pre-push gate 3 (config seal) [BLOCKED - full entry in the BLOCKED tier]
- Steal: dawn cure: .venv/Scripts/python.exe tools/config_seal.py update --by WHO --note WHY for each of the four named configs, then re-run verify (s1-commit-organ#3).
- Proof quote (row source: watch/inbox/ractor_engine/2026-10-07-stockfish-door/S1_COMMIT_ORGAN_DAWNLIST.md): `CONFIG-SEAL verify: sealed=64 live=66 modified=2 missing=0 unsealed=2`
- Verdict: supports=yes (the nonzero modified/unsealed counts are the failing verify's own output line); not deep-checked (the s1 gate deep verdict's evidence text adjudicates gate 2; the script's 2 join-misses are labeled not fatal).
- estate_status: blocked.

### 4. s2-wire-endpoint#0 [high] - generate_move() wired to the spawned server, per-call model load deleted
- Steal: done (s2-wire-endpoint#0).
- Proof quote (row source: mag/llama_cpp_bridge.py): `self._endpoint = f"http://{self.host}:{self.port}/v1/completions"`
- Verdict: supports=yes; deep_tier2=verified - file clean vs HEAD so read bytes are committed bytes; endpoint line at mag/llama_cpp_bridge.py:135, raw http.client POST at :211-220 (constant literal path, no URL assembly/DNS/redirects), shutdown() clears at :298; the old per-call `Llama(model_path=...)` construction proven deleted via `git show ac0b4374c:mag/llama_cpp_bridge.py` (old lines 169-176, exactly as claimed), the only remaining `Llama(` is the fix's own comment at :186; fresh ratchet PASS NEW=0 (hits 10 not the claimed 2 at the later moment - moment-dependent tallies, load-bearing NEW=0 reproduces).
- estate_status: executed.

### 5. s2-wire-endpoint#2 [high] - d13 session re-run on the wired endpoint, verdict re-banked with the fix named
- Steal: done (s2-wire-endpoint#2).
- Proof quote (row source: memory/runs/selfplay/evidence_latest.json): `"supersedes": "evidence_pre_wirefix_20261007.json (d13 verdict actor 3472.6ms vs scorer 2966.9ms measured the per-call model-load wiring defect)",`
- Verdict: supports=no at tier 1 (a supersedes string carries bookkeeping, not the re-run); deep_tier2=verified - the verifier read the full evidence bank across the estate paths: spawn line `ok: true, pid: 11328`, 16 samples all `ok: true` (8 actor, 8 scorer), `wall_s: 47.4` vs d13's 56.8, scorer usage costs summing 0.00074515 USD over 8 calls, both verdict averages recomputed from the 8 per_problem rows (actor 22107/8 = 2763.4, scorer 18862/8 = 2357.8, 5/8 = 0.625, Elo 1033.1), old verdict preserved and recomputed (3472.6/2966.9), provenance fields byte-read (writer, command, gguf digest c1864a5e...d12, measured_at). Nuance named, not a contradiction: verdict-level identity with d13 is byte-true (same n_correct/accuracy/Elo); at sample level 6/8 move strings are byte-identical and m002/m004 differ only by punctuation.
- estate_status: executed.

### 6. s3-reward-meter#0 [high] - a dead scorer leg is flagged at the measurement layer
- Steal: done (s3-reward-meter#0).
- Proof quote (row source: mag/selfplay_orchestrator.py:176-191): `scorer_ok = False` / `scorer_detail = str(e)` / `score_text = SelfPlayOrchestrator._fallback_score(scorer_prompt)`
- Verdict: supports=yes; deep_tier2=verified - quote byte-exact at mag/selfplay_orchestrator.py:186-188 inside the `except Exception` at :177 wrapping flash_call (:174-176); ok=True init at :172, fallback returns neutral 0.5 at :283, the sample appends the threaded values at :190-192. Named not-fatal gap: the historical "(was hard-coded ok=True)" parenthetical was not independently byte-verified (git unreachable in the verifier's environment); the current bytes prove the after-state only.
- estate_status: executed.

### 7. s3-reward-meter#1 [high] - SessionReport carries scorer_fallbacks + scorer_ok_ratio computed from the samples
- Steal: done (s3-reward-meter#1).
- Proof quote (row source: mag/selfplay_orchestrator.py:242-260): `scorer_fallbacks = sum(` / `1 for s in self.samples if s.leg == "scorer" and not s.ok` / `)` / `scorer_ok_ratio = round((n - scorer_fallbacks) / n, 3) if n else 1.0`
- Verdict: supports=yes; deep_tier2=verified - quote byte-present at :247-250, both values passed into the returned SessionReport at :260-261, zero-game early return at :231-232 keeps the vacuous-healthy defaults. Citation drift named, substance proven: the fields sit at :85-86 (claim's "79-85" off by one line) and the evidence JSON keys live at mag/selfplay_evidence.py:49-50 (claim's "main() lines 342-343" points at comment text in current bytes).
- estate_status: executed.

### 8. s3-reward-meter#2 [high] - main() refuses to write evidence on a degraded reward leg
- Steal (row residual carried): gate is a bare assert in main() only (skipped under python -O; in-process report() callers get the flagged degraded report, not a refusal); a live scorer returning unparseable text still reads neutral 0.5 via _parse_reward, distinct defect, not this move (s3-reward-meter#2).
- Proof quote (row source: mag/selfplay_orchestrator.py:320-328): `assert report.scorer_ok_ratio == 1.0, (` / `f"dead scorer: {report.scorer_fallbacks}/{report.n_games} games fell back "` / `f"to neutral 0.5 (scorer_ok_ratio={report.scorer_ok_ratio}); "` / `"refusing to write evidence"`
- Verdict: supports=yes; deep_tier2=verified - assert verbatim at :344-348, def main() at :315, the module's ONLY evidence write at :354 after the gate (grep over write paths). Caveats named, not falsifying: the write is now Move 6's append-only masters plus pointer, not a literal evidence_latest.json; python -O strips asserts; a rounding hole opens only near f/n <= 0.0005 (one fallback blocks at n=8 and n=1500, rounds back at n=2000). The strictest-threshold interpretation (task named none) is the lane's own disclosed deviation-by-interpretation.
- estate_status: executed.

### 9. s4-queen-patch#0 [high] - the QUEEN receipt patched in one pass
- Steal: done; residual: weights still OWED (no weights URL on the abs page this sitting), repo license + encoder identity check before any vendoring (S5) (s4-queen-patch#0).
- Proof quote (row source: watch/inbox/QUEEN_CHESS_LM_20261006.md): `Patched 2026-10-07 (lane s4-queen-patch, run stockfish-door-20261007): cause - the original receipt transcribed the abstract off the X figure-card image, not live bytes; evidence - curl of https://arxiv.org/abs/2610.03695 (42461 bytes) this sitting.`
- Verdict: supports=yes; not deep-checked. Lane deviations banked in the archive: a THIRD drifted Verbatim block (line 13 framework, `analogue` vs live `analog` plus a missing lead-in) was found and corrected beyond the audit's named two; S5's repo-drop watch amended to the resolved repo; weights and license stay OWED, not fabricated around.
- estate_status: executed.

### 10. s4-queen-patch#4 [high] - byte-proof of the correction, checked in both directions
- Steal: done (s4-queen-patch#4).
- Proof quote (row source: fresh urllib fetch of https://arxiv.org/abs/2610.03695, 42461 bytes): `block1: receipt-has-bytes=True | bytes-in-live-abstract=True` / `block2: receipt-has-bytes=True | bytes-in-live-abstract=True` / `block3a: receipt-has-bytes=True | bytes-in-live-abstract=True` / `block3b: receipt-has-bytes=True | bytes-in-live-abstract=True`
- Verdict: supports=yes; not deep-checked. Fold-time note (`carried`): the script's URL liveness probe read HTTP -1 on this URL at the fold moment while the lane's fetches pulled 42,461 bytes - transport artifact, see NEGATIVE RESULTS row 6.
- estate_status: executed.

### 11. s5-dispatch-game#0 [high] - the 3-move d13 dispatch game landed as a pytest file
- Steal: done (s5-dispatch-game#0).
- Proof quote (row source: tests/test_dispatch_game.py): `assert result["policies"] == 3 ** N_GAMES == 6561`
- Verdict: supports=no at tier 1 (a source line proves authorship, not execution); deep_tier2=verified - the verifier ran the landed file itself (`.venv/Scripts/python.exe -m pytest tests/test_dispatch_game.py -q` reading `14 passed in 1.05s`; the receipt's 1.76s is the recorded moment, same outcome), byte-located the assert at tests/test_dispatch_game.py:278, byte-checked the pinned reward table against both evidence files (all 16 per-game actor/scorer values match by grep needles), re-derived the session overheads independently (HTTP 47400 - 40969 = 6431.0; INPROC 56800 - 51516 = 5284.0), and byte-read the trivalent port's sources (tools/gps_mcp/coverage.py:170-172, :207, :224-241, :40). Caveats named: the pinned wall constants live in the lane artifacts and d13 receipt, not the two extract files the docstring names; the docstring's "same bytes as" duplicate-banking claims are byte-false (sha256 pairs differ) though all four digests recorded in the verdict match disk.
- estate_status: executed.

### 12. s5-dispatch-game#1 [high] - the first S2 receipt banked, falsifier PASSED on the same table
- Steal: done (s5-dispatch-game#1).
- Proof quote (row source: memory/runs/selfplay/s2_dispatch_game_verdict_20261007.json): `accuracy held at 0.625 vs 0.625 and wall 47400ms beats actual 56800ms beyond margin 0.05`
- Verdict: supports=yes (verdict-class text carrying the claim's load-bearing numbers); not deep-checked. Condition: the falsifier is adjudicated on the realizable uniform-route space, not the unrestricted search - the oracle leak is s5-dispatch-game#2, counted in NEGATIVE RESULTS row 4.
- estate_status: executed.

## DISPUTED (the script's rule, instrument applied)

The script's header reads: a lane-claimed top steal outside the TOP-K list files as DISPUTED. Instrument this fold ran: `grep -in "top steal|top_steal|topsteal"` over all 8 lane `.json` files - zero hits (exit 1), so **no lane claims a top steal outside the list: disputed_count = 0**.

Condition, recorded not averaged (`carried`, the older fold convention in corpus/steal/MASTER_EXECUTE_REGISTER.md): that fold read every high-leverage row as a claimed top steal. Under that reading the 9 high rows the script's (leverage, lane, index) sort left outside the first 12 would file as DISPUTED: s5-dispatch-game#2; s6-evidence-fence#0, #1; s7-pack-recompile#0, #1, #2; s8-golden-bouts#0, #1, #2 (21 claimed high minus 12 kept). This fold rules with the grep instrument (the run family's most recent precedent, corpus/steal/MASTER_OVERNIGHT_MESH_20261007.md) and does not promote their steal text. Coverage condition (`carried` from the script's verifier table): four of those nine rows carry verified deep_tier2 verdicts anyway (s5-dispatch-game#2, s7-pack-recompile#0, #1, #2) - verified execution sitting outside the headline list, not hidden, just not top steals of this run.

## BLOCKED TIER (2 rows, both s1-commit-organ; the run's only `estate_status: blocked`)

- **s1-commit-organ#2** - The dawn push blocks at pre-push gate 2 (githooks/pre-push:24): citation_lint check --changed exits 1 with 62 blocking PHANTOM-NUMBER findings across 43 records of working-tree prose drift (AGENTS.md:29, memory/zknot session pages), zero of it in commit 64178cf5d; the gate scans `git diff --name-only HEAD` (staged plus unstaged, tools/citation_lint_io.py:327-356), so it fires on drift outside the commit. **Reason it stays blocked:** the lane's bytes are the two committed files; the red findings live in prose the lane did not mint and append-never-rewrite forbids it from silently rewriting; accepting debt is an operator-class by-name act. **Next-sitting unblock** (the row's own steal field): fix the prose or regen the zknot pages via tools/zknot.py, else accept the findings by name via `--baseline configs/citation_lint_baseline.json` before pushing. Moment condition (`carried`, deep_tier2=verified): the verifier's live rerun read 70 blocking across 49 records at its later moment - the drift is growing on the shared tree; cure before dawn either way.

- **s1-commit-organ#3** - The dawn push blocks at pre-push gate 3 (githooks/pre-push:26): config_seal verify exits 1 with 2 modified (mirrors.json, violation_baseline.json) and 2 unsealed (lane_profiles.yaml, longrunner_policy.json); the drift predates this lane and is not in commit 64178cf5d; the hook header law is re-seal by NAME, never loosen the hook. **Reason it stays blocked:** sealing is a by-name acceptance act the lane defers to the operator/coordinator class; no lane may loosen the hook to get past it. **Next-sitting unblock** (the row's own steal field): `.venv/Scripts/python.exe tools/config_seal.py update --by WHO --note WHY` for each of the four named configs, then re-run verify to green.

## NEGATIVE RESULTS (counted reasons)

| # | Reason | n | Filed by (lane#row) |
|---|--------|---|---------------------|
| 1 | Quantizer acceptance negative: after the fresh 09:10:05Z compile (kept 625 == packed 625, flash sha byte-identical, deterministic over an unchanged feed) the flash pack still greps zero for queen, mira, token-cue, alodlm; the logic-lens census (4 terms + arXiv ids 2610.03695/02525/04198/06851) is zero on all three packs; A4's falsifier (a post-18:26Z stamp whose packs carry the rows) is unfired across two post-finding stamps today (08:51:19Z, 09:10:05Z) | 4 terms x 3 packs zero, 2 stamps | s7-pack-recompile#1 (root: s7-pack-recompile#0) |
| 2 | Root cause of row 1: the compile's feed is fed-but-deaf, not stale - memory/percolator/invariants.json greps zero for all four terms while live (648 rows, newest last_seen 2026-10-07T08:50:37.213877Z); the four 10-06 receipts reached watch/inbox and never the percolated invariant stream, so no compile can carry them; matches break-logic.md:39-40's same zero on 10-06 - the falsifier was structurally unreachable by recompile alone | 4 receipts undelivered upstream | s7-pack-recompile#2 |
| 3 | Prospective routing claim INSUFFICIENT: with 8 measured games the ported MIN_PROBLEMS_FLOOR 10 (tools/gps_mcp/coverage.py:40) is unmet; the head-to-head stands on paired same-problem deltas, route prediction for unseen problems waits for a 10-plus-game table | 1 verdict | s5-dispatch-game#3 |
| 4 | Oracle-policy leak: the unrestricted 3^8 search winner (32103.0ms) is an oracle policy, not realizable; falsifier re-adjudicated on the realizable space; the 15297.0ms gap banked as a leak class; first draft pinned a wrong golden vector (46603.0ms) and went red 2 failed before the cure | 1 leak class, 1 red-to-green cure | s5-dispatch-game#2 |
| 5 | First-class isolation-leak incident, found and cured in-seat: the first suite run (5 passed in 823.35s) wrote the LIVE surfaces - 11,000 spill rows into memory/training/arena_profiles.jsonl and the live arena game clobbered; cure byte-counted (11,301 to 301 rows, spill backed up at arena_profiles.jsonl.s8_spill_20261007.bak); one pre-run game_id (arena-7fea8f5df7) lost unrestorable, named in the erratum | 1 incident, 11,000 spill rows, 1 lost game | s8-golden-bouts#3 |
| 6 | Fold-time URL liveness negative: the fold's one unique URL read HTTP -1 (https://arxiv.org/abs/2610.03695) - ruled a transport artifact, not a dead source: the citing lane's own fetches the same sitting pulled 42,461 bytes, byte-stable across audit and lane | 1 URL, 1 moment | script URL LIVENESS section; s4-queen-patch#4, s4-queen-patch#0 |
| 7 | Transient test red, passed on rerun, not reproduced: test_spawn_without_llama flipped red (1 failed, 23 passed) because a live llama server held the bridge's shared DEFAULT_PORT 8081 (mag/llama_cpp_bridge.py:28) during a sibling rerun; green with the port free | 1 red | s1-commit-organ#1 |
| 8 | Transient test red, passed 3/3 reruns, not reproduced: TestLlamaCppBridgeEndpointWire (bridge-side, zero bytes of the fencing lane in that path) | 1 red | s6-evidence-fence#2 |
| 9 | Register drift found: the register's cited endpoint route `/completion` (operations.md:13, old mag/llama_cpp_bridge.py:129) is a dead route in llama-cpp-python 0.3.36 - all 8 POSTs 404'd on the preserved first probe; the wire rides /v1/completions | 1 stale citation, 8x 404 | s2-wire-endpoint#1 |
| 10 | Tier-1 supports=no verdicts standing in the record: 10 total; 7 of them adjudicated verified by deep_tier2 (s1-commit-organ#0, s2-wire-endpoint#2, s5-dispatch-game#0, s5-dispatch-game#2, s7-pack-recompile#0, s7-pack-recompile#1, s7-pack-recompile#2); 3 stand unadjudicated (s3-reward-meter#3 probe detail, s1-commit-organ#4 multi-leg dawnlist, s7-pack-recompile#4 flash census) | 10 no / 29 yes | script VERIFIER TABLE; laneChecks records |
| 11 | Kill criterion 2 not adjudicated: the bout battery's actors are deterministic sha256 dice-law policies, not LM seats, so the LM legal-move-rate leg is untried; bouts hitting the 100-ply cap mean the verdict rides full-ledger identity, not game outcomes | 1 criterion | s8-golden-bouts#2 |

**Tombstones:** [] - nothing was tombstoned this run; per the casualty header, hard failures would be tombstoned and subtracted from owed, and there were none (parse errors 0, missing 0).

## NEXT REGISTER (top 10 residuals, one seat one sitting)

1. **Percolate the four 10-06 paper receipts** (QUEEN_CHESS_LM, MIRA_METAREASONING, TOKEN_CUES_2610.06851, ALODLM_2610.04198) through the sanctioned percolate() path on reviewed signal (mag/percolator.py; the promote gate - never hand-edit invariants.json), then rerun `tools/thought_quantizer.py compile` and re-grep the four terms; the pack follows the feed, never the inbox. This fires A4's falsifier pass branch. (s7-pack-recompile#2)
2. **Cure dawn gate 2:** fix the PHANTOM-NUMBER prose or regen the zknot pages via tools/zknot.py, else accept the 62 blocking findings by name via `--baseline configs/citation_lint_baseline.json`; then `citation_lint check --changed` must exit 0. (s1-commit-organ#2)
3. **Cure dawn gate 3:** `tools/config_seal.py update --by WHO --note WHY` for mirrors.json, violation_baseline.json, lane_profiles.yaml, longrunner_policy.json; re-run verify to green. (s1-commit-organ#3)
4. **Kill criterion 2 with an LM seat in the loop:** rerun the bout battery with LM seats and bank the legal-move rate (>=90 percent within 3 tries); note bouts hitting the 100-ply cap ride full-ledger identity, not outcomes. (s8-golden-bouts#2)
5. **Actor-health fence beyond path-existence:** a configured model_path whose file exists but whose model is broken still emits per-move hash fallbacks (mag/llama_cpp_bridge.py:159-167 unspawned branch); the Move 3 scorer gate is the only remaining health fence - close the gap or name it law. (s6-evidence-fence#0)
6. **QUEEN vendoring preconditions:** weights still OWED (no weights URL on the abs page this sitting); repo license + encoder identity check on github.com/queen-project/queen before any vendoring (S5). (s4-queen-patch#0)
7. **Pin move 3 with regression tests:** no test locks the ok=False threading, the ratio math, or the main() refusal; a regression file locks the gate against -O strips and sibling edits. (s3-reward-meter#4)
8. **Ephemeral port for test_spawn_without_llama:** point it at a free port instead of the shared DEFAULT_PORT 8081 so no live organ can answer readiness and flip it red (the 1.81s red of s1-commit-organ#1 is the repro). (s1-commit-organ#1)
9. **Evidence provenance fields on the pre-Move-6 files:** the existing d13 evidence carries no writer/model/cmd provenance (break-dogfood.md A3 remains a separate register row, not landed). (s6-evidence-fence#4)
10. **Rerun the dispatch game on a 10-plus-game measured table** (one more measured session) so the route prediction for unseen problems clears MIN_PROBLEMS_FLOOR 10 and becomes bankable. (s5-dispatch-game#3)

Fold seat closing note: all numbers above are the counting script's; every quote is a lane-row byte; the only folder-composed machinery is the counted-reasons grouping, the DISPUTED condition, and the register ordering, each tagged where it rides. The fold adds no verdict of its own and overrides none.
