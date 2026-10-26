# ORGAN DOGFOOD — BATCH5 wave2, worker r3-organs — 2026-09-06T01:39-01:43Z

Operator order: "dogfood our tools even rarely used ones for data." Ran from repo root, one at a time,
house rules honored (no chain edits, no container restarts, no organ code edits). Pre-run mtimes
captured before every run so freshness is measured, not assumed. All runs $0 (local python, local
ollama eye, no API lanes touched).

| # | Organ / command | Exit | Runtime | What it produced | $0 | Verdict |
|---|-----------------|------|---------|------------------|----|---------|
| 1 | `python -m mag.overseer snap` | 0 | <2s (bc miss; json ts proves run) | dashboard/static/overseer.json rewritten to ts 2026-09-06T01:39:05Z — fleet 7/7 up, in-flight none, chain tip 165f2cd1da3a (7291 rows), feed_age 12.6s, gnd wave 3 posts. OVERSEER strip data FRESH. | yes | ALIVE |
| 2 | `python -m mag.topic_index build` | 0 | 1923ms | watch/TOPIC_INDEX.md rewritten (mtime 21:39:28-04): 1422 lines, 705 cards, 3819 topics, 601 dated, 193 scored. Cosmetic `datetime.utcnow()` DeprecationWarning at mag/topic_index.py:136. | yes | ALIVE (warning is data, not touched) |
| 3 | `python -m mag.read_receipts sweep` | 0 | 13472ms | watch/READ_RECEIPTS.md rewritten (mtime 21:40:01-04): 55 pages hit, 6 zero-hit, 603 cards, 10 zero-backref. | yes | ALIVE |
| 4 | `python -m mag.seal seal` | 0 | 832ms | memory/seals/2026-09-06T01-40-13/ — 19 ground-truth files copied, read back, hash-matched, signed; 0 live/growing; manifest.json seal.v1 with per-file sha256 (verkle_chain.jsonl 5110965B sha 5fa3b946...). state/seal_latest.json -> verified:true. | yes | ALIVE |
| 5 | `python -m mag.seal verify` | 0 | 386ms | "seal holds: every copy still matches its manifest hash", n_files 19, mismatches []. proof.anchored:true, claim_hash a2f05bbe.... OTS FINDING: no `.ots` file anywhere in the seal dir (find returned nothing) — anchor exists only as claim_hash in manifest/state. If night-shift OTS cal is async that is by design; if the .ots fetch step never ran, that is a silent gap. Flagged, not fixed. | yes | ALIVE (anchor artifact ABSENT on disk) |
| 6 | `python -m mag.grounding_wave post --claim ... --verdict SUPPORTED --evidence ... --note ...` | 0 | 1781ms | POSTED #d9d7ce83d91b (SUPPORTED) — 4th GROUND post, chain intact, tip=d9d7ce83d91b. Claim: "BATCH5 wave1-2 fired, receipts at memory/runs/batch5_20260906/" — verified before posting: that dir holds MEMORY_TRIM_PROPOSAL.md, ORPHAN_LEDGER_20260906.md, RAMP_BOARD.md, build_memory_trim.py, so SUPPORTED is honest, not ceremonial. | yes | ALIVE (write path works) |
| 7 | `python -m mag.swarm_snapshot` | 0 | 46182ms | Local ollama eye ANSWERED: vision_read.md analyzes all four panels incl. "Panel D: Chain Knots Sealed per Day" anomalies; banked to memory/runs/swarm_snapshot/20260906T014208Z/ (board.png 9642B fresh 01:42Z, digest.txt, vision_read.md). FINDING: dashboard/static/swarm_board.png mtime UNCHANGED (2026-09-05 12:37 local, 9248B) — the organ renders+reads to its run dir but never refreshes the static board copy. Stale static surface, live eye. | yes | ALIVE (static board STALE) |

## Tally
6 organs probed (overseer, topic_index, read_receipts, seal, grounding_wave, swarm_snapshot): 6 alive, 0 broken, 0 dark.

## Findings worth a look (recorded, not repaired per house rules)
1. Seal OTS: `proof.anchored: true` but zero `.ots` files under memory/seals/2026-09-06T01-40-13/ — verify counts the claim_hash only. If the OpenTimestamps calendar receipt is expected on disk, it is missing every seal, not just this one.
2. swarm_snapshot never updates dashboard/static/swarm_board.png — last write 2026-09-05 12:37 local. Either a retired copy step or a broken handoff to the dashboard; the fresh render lives only in memory/runs/swarm_snapshot/<ts>/board.png.
3. topic_index.py:136 uses deprecated `datetime.utcnow()` — harmless until py3.14+ removes it; one-line future fix for whoever owns the organ.

## Receipt
BATCH5|r3|RECEIPT: 6 organs probed, 6 alive, 0 broken, 0 dark — card watch/ORGAN_DOGFOOD_20260906.md.
GROUND entry #d9d7ce83d91b posted to the GROUND ledger (4 posts, chain intact). Seal state/seal_latest.json verified:true @ 2026-09-06T01-40-13.
