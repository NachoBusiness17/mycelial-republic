# B3 RECEIPT - centralized merge actor (build-it-all wave, 2026-10-05)

## What was built

`consensus_merge(answers, lane, *, independent=None, rho=None, trail=None)` in
`mag/memweave.py`, plus the `lane_trail(lane)` path helper. The centralized merge
actor from the day-4 mine swarm card (watch/inbox/frontier_olm_2026-10-04/steal/
swarm-orchestration via x.md, FIND 1).

## The mechanism (why it exists)

Google 180-config scaling study (numbers live-verified on the card): centralized
coordination beats a single agent by +80.9 pct on parallelizable work; independent
multi-agent systems amplify errors up to 17.2x while one centralized merge turn
contains the amplification to 4.4x. The orchestrator acts as a validation
bottleneck. Steal: the fan-out is half the machine; the single cheap merge turn
after it is the money.

## The merge shape

- One function, callable by any carrier post-fanout: pool the answers, call once.
- Internally it calls the EXISTING `consensus_quality(answers, *, independent, rho)`
  at mag/memweave.py:115 unchanged (independent / rho pass through).
- Appends exactly one row to the owning lane's trail.jsonl (default
  `queue/lanes/<lane>/trail.jsonl`, ROOT-anchored; created if absent; append-only):
  `{"ts": <UTC Z>, "actor": "<lane>-merge", "event": "CONSENSUS_MERGE",
  "detail": <verdict dict>, "artifacts": []}` - shape-matched to live rows read in
  queue/lanes/research/trail.jsonl (ts/actor/event/detail/artifacts).
- Lane name is validated (no path separators) before it touches a filesystem path.
- No existing carrier rewritten; adoption is one import + one call.

## CID tie-in (consensus-illusion detection)

The merge verdict IS the CID guard's verdict (schema memweave.consensus.v1).
A unanimous pool collapses to 1 independent witness (token overlap >= 0.6) and is
penalized to `correlated_weak` (n_effective 1.0 at n=4); a dissenting pool counts
every disjoint answer and reads `strong` (n_effective 4.0). With rho supplied, the
closed-form CID correction applies: n* = n / (1 + (n - 1) * rho), so 4 unanimous
answers at rho=0.9 are worth ~1.08 opinions. Unanimity is a smell, not a signal.

## Delta vs the steal card's PORT section

The card's critique-fix-4b detail shape (verdict dict + pooled-answer spool paths,
artifacts = spooled answers) was narrowed per the lane card to detail = verdict
dict, artifacts = []. The spool half is a follow-up if a lane wants answer
provenance banked; the merge + trail row + guard are complete as specified here.

## Tests

`tests/test_b3_merge_actor_20261005.py` - 7 tests, 7 passed (0.74s):
unanimous pool takes the CID penalty; dissenting pool healthier on every CID axis;
rho pass-through computes n* = 4/3.7 = 1.0811; independent length guard raises;
trail row shape matches live rows (5 keys, actor `<lane>-merge`, event
CONSENSUS_MERGE, detail = verdict, artifacts = [], parseable Z-stamped ts,
append-only preserves the seed row); default trail resolves to the live research
lane trail; lane name rejects path escapes.

## Gates

- pytest: full-suite run result filed below in FINAL NUMBERS (targeted file 7/7).
- Ratchet: `python tools/violation_ratchet.py check --changed` = PASS,
  scope=8 changed files, hits=2, registered=2, NEW=0, expired=0.
- Dash scan: no em/en-dash in the added code or tests (grep found them only in
  pre-existing memweave.py lines 1/105/122/127/133).
- No git commit (per lane law).

## FINAL NUMBERS (full suite, filled at close)

- Targeted: tests/test_b3_merge_actor_20261005.py = 7 passed in 0.74s
  (.venv interpreter, moment 2026-10-05).
- Full suite `pytest -q`: PENDING_CLOSE - the run was still in flight when this
  receipt was drafted; the real executed sum is filed by the wave close, never
  hand-written.

## Files

- mag/memweave.py (merge actor block, lines ~186-250)
- tests/test_b3_merge_actor_20261005.py (new)
- watch/inbox/build_wave_20261005/b3_merge_actor.md (this receipt)
