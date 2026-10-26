# CORPUS FOLD LANDED (fillball-1001, fill-corpus-fold lane, division B) - 2026-10-01

Lane: fill-corpus-fold (the gala fillball-1001, meta-gap 2: corpus/steal and memory/research_polished had received nothing from the music, localfirst, spiking, olm-day-1/2, ractor50, 48h programs).

Moment note (one clock, two zones, both named, per the ractor50 operations precedent): run date and entry slugs are 2026-10-01 (the gala's date, UTC); the lane's file mtimes crossed midnight into local Oct 2 00:0x during the sitting. No count or claim here depends on which side of local midnight a file landed.

## What landed

Six corpus/steal entries, one per program, house format per `state/fuel/corpus_fold_prompt.md` (program + one-line verdict / Top mechanisms with estate organs / two falsifiable probes / Sources citing the watch/inbox receipts):

| program | entry |
|---|---|
| music | corpus/steal/CORPUS_FOLD_MUSIC_20261001.md |
| localfirst | corpus/steal/CORPUS_FOLD_LOCALFIRST_20261001.md |
| spiking | corpus/steal/CORPUS_FOLD_SPIKING_20261001.md |
| olm-day-1/2 | corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md |
| ractor50 | corpus/steal/CORPUS_FOLD_RACTOR50_20261001.md |
| 48h | corpus/steal/CORPUS_FOLD_48H_20261001.md |

## The DeepSeek drafts: exist, parse, REJECTED

The drafts DID exist and parse: `state/fuel/corpus_fold_out_w0.jsonl` (4 rows) and `corpus_fold_out_w1.jsonl` (3 rows), all `ok: true`, all with attempts 1 and sub-cent costs. Seat verification against the source digests (`corpus_fold_in_w*.jsonl`, same texts as `corpus_fold_items.jsonl`, all truncated at 14000 chars) failed 7 of 7:

- The workers hallucinated entirely different programs ("Adaptive Memory Retention" twice for olm-day1/olm-day2/music-adjacent ids, "Durable Execution" for music, "Semantic Routing" for spiking, "Salience-Gated Consolidation" for ractor50, and fold-prompt self-descriptions for localfirst/48h).
- Scripted check (lanes/work/seat_verify_drafts.py, output in the lane check file): every fabricated `estate://...`, `estate/corpus/...`, and `https://example.org/...` citation is absent from its source text (grounded citations: 0 for all path-bearing drafts), zero cited paths exist on disk, and draft-source word Jaccard is 0.000-0.089.
- The spiking source digest is itself 67 bytes: `== synthesis.md == (MISSING: watch/inbox/spiking_wide/synthesis.md)` (exact text in the check file); the spiking program's real content lives in the seven `watch/inbox/spiking_wide/` lane receipts, which the SPIKING entry folds from directly, with the missing synthesis stated as the negative result it is.

Per the owed-waltz contract (drafts are raw material only after seat verification), all 7 drafts were rejected and the fold was done directly from the source digests and the on-disk receipts they point to.

## Method notes

- Every mechanism, number, and probe in the six entries is traceable to a source digest read in the lane session (extracted to lanes/work/*.src.md) or to an on-disk receipt checked for existence this session (59-path existence sweep plus a 10-path supplement; 0 unexpected missing; one name drift found and recorded: STYLE_SPEC's `style-synthesis.profile.json` does not exist, the on-disk receipts are `style-synthesis.json` + `style-synthesis.check.txt`).
- Em-dash scan over all six entries: 0 (en-dash scan in the check file).
- Truncation honesty: the fold-input digests were hard-truncated at 14000 chars (a known wave disease; ractor50 operations raised fold caps 12000 to 24000 for exactly this). Entries fold from the on-disk receipts where the extract cut off mid-claim; no entry invents past a truncation.
- No code under mag/ or tools/ was touched by this lane, so the violation ratchet is not applicable (not run).

## Shared-surface note

`mag.shared_surface validate` was run per the machine contract. It exited 1 on sibling-owned drift (13 stale hashes, 1 invisible file; later a moving target as sibling lanes appended during the sitting). This lane ran the sanctioned writer (`mag.shared_surface rebuild`) twice: pass 1 healed 14 and folded 8467 events into 2513 active items; pass 2 reached 0 stale / 0 missing / 0 invisible. The irreducible residual is 8 NEW event-kind rows in LINKS.jsonl written by the free-resource-scout lane during this sitting (validator: LINKS.jsonl is link rows only past the B2-28 marker; events belong in watch/inbox/EVENTS.jsonl via mag.link_library.load_events). That is the scout lane's schema debt, named here for its owner; this lane did not rewrite another writer's rows. This lane's own files carry zero validate errors and zero warnings.

## Decision ledger

Closes meta-gap 2 for the six programs: corpus/steal now carries one entry per program with probes and receipt cites. Changes nothing else; no config, code, or manifest edits.

## Raw output

Finish-line command battery and the seat-verify run: watch/inbox/gala_20260925/fillball-1001/lanes/fill-corpus-fold.check.txt
