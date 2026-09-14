1. **EXPAND — Client harness fails first; slot safety is already DISPUTED at width 8.** `lightmap` held slot 0 from 01:55:37–02:02:34; `maze` acquired that same slot at 01:59:01. The [raw receipt](C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/overseer/conc_test_20260905.jsonl:11) contradicts clean ownership. The [gate](C:/Users/foste/Documents/projects/local_sovereign_agent/mag/concurrency_gate.py:88) uses non-atomic check/write, expires ownership after 120 seconds without renewal, and releases without checking owner identity.

Make this a controlled saturation program: cheapest first experiment is a zero-token, simulated-clock overlap/release test. After repair, run identical bounded requests at synchronized widths 8→12→16, first one seat, then two sharing the account; record actual request intervals, errors, tokens and independently accepted outputs. Worker overlap alone cannot establish vendor concurrency. **Prediction, UNPROVEN:** useful-throughput knee at 8–12, with less than 20% gain from 12→16; the dossier’s diminishing speedup motivates this weak prior, but workloads differ. **Falsifier:** matched 16-wide trials repeatedly beat 12-wide accepted outputs/second by ≥20% without lowering acceptance.

2. **ENHANCE — Three additions; operator benefit UNPROVEN.** The [overseer](C:/Users/foste/Documents/projects/local_sovereign_agent/mag/overseer.py:101) currently counts rows without verifying the wave, while its slot summary inherits the ownership defect.

- Reconcile request/worker events against leases: owner generation, overlapping grants, last progress, completion. Record heartbeats at existing tool boundaries; silence means UNKNOWN, never permission to steal.
- Read successive quota receipts: cache reads, fresh input, output, provider-accounted consumption, remaining allowance, and predicted versus actual next-batch cost. The dossier’s 94% refeed share makes aggregate token counts insufficient.
- Verify chain and pinned evidence; publish snapshot age and component observation times, so five-second browser polling cannot disguise old observations.

All execute during existing steering passes. **Falsifier:** replay overlapping ownership, missing quota data, and edited evidence; any clean/known display refutes adequacy.

3. **REDESIGN — Multi-seat adoption SUPPORTED; concurrent-append safety DISPUTED.** Seven posts verify, but [post()](C:/Users/foste/Documents/projects/local_sovereign_agent/mag/grounding_wave.py:56) reads the head before an unlocked append. Two writers can select the same predecessor.

```diff
  KEEP claim/verdict/evidence, previous-hash links, append-only corrections.
- CHANGE unlocked JSONL read-head/append as the authoritative write path.
+ ADD SQLite with FULL synchronous commits on a tested local lock domain.
+ EACH seat: BEGIN IMMEDIATE; validate head; deduplicate post_id;
+ append sequence + prev + payload hash; durable COMMIT; acknowledge.
+ ADD unique post_id and sequence, writer identity, evidence byte hashes,
+ schema version, and explicit supersedes links; hash all new fields.
+ KEEP existing rows unchanged as the imported prefix; version new rows.
+ CHANGE JSONL/dashboard into regenerable, tip-labelled projections.
```

No coordinator seat or daemon: every seat runs the same append transaction; storage supplies serialization. Unavailable storage blocks posting. This does not promise partition-tolerant distributed consensus. Present failure is predecessor collision; redesigned failure boundary is shared-storage locking/durability. **Falsifier:** synchronized writers, duplicate retries and process kills yield any lost acknowledged post, duplicate ID, divergent head or unverifiable prefix.

4. **TRAPS — Mistaking an intact record for verified truth. SUPPORTED mechanism; systemic extent UNPROVEN.** The [ledger’s final post](C:/Users/foste/Documents/projects/local_sovereign_agent/watch/GROUNDING_WAVE.jsonl:7) blesses clean leases despite the overlap above. [verify()](C:/Users/foste/Documents/projects/local_sovereign_agent/mag/grounding_wave.py:72) checks linkage and hashes, not evidence bytes or claim entailment; earlier entries cite the mutable `overseer_latest.json`. More seats can multiply the same unsupported conclusion without adding independent evidence. Count independently reproduced outcomes, track evidence ancestry, and retain contradictory verdicts. **Falsifier:** a blind audit of every SUPPORTED post reproduces its precise claim from preserved independent evidence, while seeded hash-valid false claims are rejected before acceptance.
