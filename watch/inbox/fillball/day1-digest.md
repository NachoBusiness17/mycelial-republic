# RECEIPT: day-1 frontier_olm fold backfill (fillball lane fill-day1-digest, division B)

Written 2026-10-01 23:53 EDT / 2026-10-02 UTC. Lane JSON: `watch/inbox/gala_20260925/fillball-1001/lanes/fill-day1-digest.json`. Check log: `watch/inbox/gala_20260925/fillball-1001/lanes/fill-day1-digest.check.txt`.

## The owed work (GAP_REGISTER rank 7, `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:80,116-119`)

The day-1 window (`watch/inbox/frontier_olm_2026-09-30/`, the 2026-09-30 frontier olm mine) was uncitable: 6 steal cards and 32 sweep write-ups on disk, but the fold step never ran, so no DIGEST, no register, no percolator candidates existed. This lane folded the window retroactively, backfilled only, nothing backdated.

## Files written (new, this lane's ownership only)

| File | Bytes | Content |
|---|---|---|
| `watch/inbox/frontier_olm_2026-09-30/DIGEST.md` | 16,401 | Fold digest, BACKFILL BANNER at top naming the moment, the gap, and the selection rule |
| `watch/inbox/frontier_olm_2026-09-30/register.jsonl` | 33,037 | 23 confirmed-find rows (8-key schema matching the 10-01 window convention), one per find the six cards carried |
| `watch/inbox/frontier_olm_2026-09-30/percolator_candidates.jsonl` | 16,791 | 6 rows, one per steal card (claim / source_url / estate_map / probe), per fill spec 7 which names this third file |
| `watch/inbox/fillball/day1-digest.md` | (this file) | Receipt |

No existing file was edited. Nothing under `mag/` or `tools/` was touched, so the violation ratchet is not applicable and was not run (ask step 3 does not trigger).

## Selection rule (stated because the original adjudication artifact never landed)

The register carries exactly the confirmed finds the six cards name as carried from the day-1 ask: 5 agent-memory-continuity + 6 kv-cache-context-engineering + 3 open-and-local-language-models + 1 olm-x + 4 olm-reddit + 4 quantization-compression = 23 rows, 23 unique sources. This is a reconstruction from the cards' evidence, not byte-recovery of the dead fold step. The sweeps bank additional items beyond these 23 (quant-arxiv banks 8, memory-arxiv 8, olm-arxiv 8); those stay citable in their sweep files.

## Checks run (all raw output in the check file, script exit 0)

- Byte verification: all 23 register quotes contained in the on-disk holding named in the row's `source` field (21 hit their first-named holding; rows 12 and 13 hit their second-named holding, the `state/arxiv` abstract snapshots, which is where the quote lives). QUOTE_FAILS 0.
- JSONL parse + schema: register 23 rows, percolator 6 rows, 0 key mismatches against the window's key sets.
- Card paths named in the percolator estate_maps: 6 of 6 exist on disk. CARD_PATH_FAILS 0.
- Em-dash / en-dash scan over all three new files: 0 and 0.
- One quote correction made during verification: the 2609.37902 register row uses the snapshot's byte truth (lowercase "higher-priced"), where the day-1 card had capitalized the sentence start.

## Not done, stated plainly

- INDEX heal (fill spec 8, the sanctioned `mag.shared_surface` rebuild): NOT done; the three new files are unindexed until that separate fill runs. This lane's ownership was the day-1 folder's new files plus its own receipt, and it did not touch the shared index.
- The day-1 unconfirmed trio (GAP_REGISTER rank 10: U2 r/LocalLLaMA 1sy7srk KV table, U3 arXiv 2609.21341): NOT recoverable from this folder; greps found zero hits for 2609.21341 and only a held-09-28 reference for 1sy7srk (`sweep/kv-cache-context-engineering-reddit.md:34`). Not registered; remains a rank-10 fill for a seat that can re-fetch.
- No source re-fetch, no probe execution, no re-adjudication: this backfill reads and registers what day-1 banked.

## Decision ledger

Closes GAP_REGISTER rank 7 (day-1 window uncitable): the 09-30 window now cites like 09-28 and 10-01 - DIGEST, register, percolator candidates, all sourced to on-disk holdings. No other decision changed.
