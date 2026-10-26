# ROW · tape_facts

## ROW A — trajectory tape: scope
- **pointer**: /board/openclaw_traj.jsonl (17 lines, read fully)
- **claim**: ts range 2026-08-30T12:13:03Z → 2026-08-31T10:37:36Z (~22.4h). 17 compaction records across **5 distinct sessions**:
  - agent:main:dashboard:b5da3adc — lines 1-10, 14 (11 records)
  - agent:main:dashboard:c77a34ee — lines 11-12, 15 (3)
  - agent:main:dashboard:ce9089a0 — line 13 (1)
  - agent:main:dashboard:a73bf4e3 — line 16 (1)
  - agent:worker:subagent:2e50ad22 — line 17 (1)
- **type**: gopher · **confidence**: H · **status**: VERIFIED
- **evidence**: full read of 17-line tape.

## ROW B — event/schema types present
- **claim**: homogeneous compaction-event shape per line: `{ts, session, tokensBefore, tokensAfter, compactedCount}`. Line 17 is the ONLY record carrying `metadata` with `schema: "trajectory_span.v1"` (spanId 753bdebb…, lineRange [17,17], byteRange [2638,0], bodySha256 d07813d9…, pathsTouched [], tokenCount 10610). Lines 1-16 carry metadata-free minimal schema. No other event types present.
- **type**: gopher · **confidence**: H · **status**: VERIFIED

## ROW C — physics-level facts (raw, no cast)
- **claim**:
  1. **Compaction counts** span 0–164; total compacted across tape = 851. Lows: 0 (line 7), 3 (lines 2,5); highs: 164 (line 14), 142 (line 16), 109 (line 13).
  2. **Token deltas (tokensBefore→tokensAfter)**: drops range −21108 (line 6) to −92734 (line 12, 69773→2039). Largest absolute compaction all-session crash: line 12 (session c77a34ee, −933 high-compact), line 13 (ce9089a0, −92940).
  3. **Repeated same-session session** b5da3adc spans two disjoint time blocks: 08-30 12:13–13:05 (10 records) then 08-31 00:52 (1 record); across-tape it accumulates up to tokensBefore=147723 at line 14.
  4. **tokensAfter baseline/drift**: post-compaction floors stay near ~10.6k–26.4k (median ~22.5k) except 3 collapses below 20k: line 12 (2039), line 13 (1352), line 17 (10610). Systemically, floor drifts upward over session life; line 14 breaks pattern with floor 14206.
  5. **Heaviest single compaction** = line 14: 147723→14206, compactedCount 164 (session b5da3adc, 08-31T00:52:43Z) — largest before-count and count on tape.
  6. **Two sub-2k collapses** cluster at 08-30 15:36 / 16:08 (lines 12-13) across DIFFERENT sessions (c77a34ee, ce9089a0) — near-total wipe pattern, not session-specific.
  7. **Time gaps / span gaps**: largest inter-record gap = 08-30 13:05 → 15:14 (~2h 9m, lines 10→11); second gap 16:08 → 00:52 (~8.7h overnight); last gap 01:15 → 10:37 (~9.4h) rolling to line 17.
  8. **Metadata lineage fact**: only line 17 (worker subagent, tail of tape) is a verified `trajectory_span.v1` block with bodySha256 chain anchor d07813d9…; lines 1-16 are unanchored pre-schema compacts — the tape transitions from bare compaction events to a hash-chained span record at its tail.
- **type**: gopher · **confidence**: H · **status**: VERIFIED (arithmetic on tape values, no host read)

## Per-line summaries
1. b5da3adc 1207→24561, 🗜97 (first, largest local drop −82.6k)
2. b5da3adc 39557→22875, c3
3. b5da3adc 37323→23299, c5
4. b5da3adc 53715→25219, c13
5. b5da3adc 46134→24867, c3
6. b5da3adc 68203→21108, c54
7. b5da3adc 42267→22489, c0 (no-op compact)
8. b5da3adc 47566→22572, c6
9. b5da3adc 56360→23976, c15
10. b5da3adc 46715→26440, c5 (block ends)
11. c77a34ee 77961→21067, c30 (new session)
12. c77a34ee 69773→**2039**, c91 (near-total collapse #1)
13. ce9089a0 94292→**1352**, c109 (near-total collapse #2)
14. b5da3adc **147723**→14206, **c164** (heaviest on tape)
15. c77a34ee 75284→16028, c84
16. a73bf4e3 116260→17288, c142
17. subagent:2e50ad22 47543→10610, c30 · metadata trajectory_span.v1 spanId 753bdebb, sha d07813d9 (only schema'd/hash-chained record)
