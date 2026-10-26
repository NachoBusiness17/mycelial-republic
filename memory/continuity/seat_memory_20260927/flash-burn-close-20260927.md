---
name: flash-burn-close-20260927
description: Flash-lane burn FINAL close 9/27 18:07 local — byte-derived 488 unique
  dispensed / 402 landed / 86 outstanding, 642 ledger rows; LANDED RULE must match
  zero-padded filenames via regex not glob; width-24 dynamic ceiling proven
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Flash-lane burn session closed early AM 2026-09-27. 402 of 423 briefs landed with receipts, 23 deep lanes still grinding, 0 unchecked Open briefs remaining. ~1.1B tokens witnessed across all surfaces. Peak measured 109.4M tok/h at width 10 (B2-25); width-24 experiment produced 8 surfaced 1302s confirming the ceiling is depth-dependent.

## Key craft corrections from the operator

**Key-name register correction 9/26 late**: both .env key naming styles (mixed-case `Mistral_API_KEY` and canonical `MISTRAL_API_KEY`) work fine on Windows; the "fix" normalized names that weren't broken. Names that "don't fit your register" are not bugs, they're just unexpected. Don't fix what isn't failing cross-platform.

**Width-24 dynamic ceiling** (B2-25 + B2-98): "clean" waves at width 10-12 absorbed 287 1302s silently via the retry layer. The surfaced count ≠ the occurred count. tools/provider_error_tally.py closes this blind spot permanently. Envelope law re-derived as a function of window depth.

## Session totals

- ~1.1B tokens witnessed (agent metadata + absorbed retries not counted)
- 500+ briefs queued, 402 landed, rest in flight or requeued
- 240+ LEDGER rows, every claim byte-backed
- 397+ 5-section receipts in watch/inbox/burn_wave_20260926/
- 550+ queue rows created by self-feeding lanes

## Standing operator GOs

Drive bridge install, Cerebras card (P0 Oct 3), width-15 probe, Grok refire (source repaired by B2-139), weekly pack cron (fresh chat), 18-credential rotation (B2-73, operator-gated).

## FINAL close 9/27 18:07 local (byte-derived, supersedes earlier estimates)

Dispatcher close gate fired past noon 9/27. STATE landed array re-derived from the LANDED RULE (a dispensed B2-NN is landed iff B2_NN_*.md exists on disk), not self-report:

- 488 unique B2 ids dispensed (deduped; "506" raw rows included double-claims from the concurrent self-feed era)
- 402 LANDED, 86 outstanding (1302 deaths + self-fed B2-507..553 tail, carried to reset-day window)
- LEDGER.jsonl final: 642 rows. Verdict families: 352 LANDED-family, 161 steal (self-feed bookkeeping, not verdicts), 16 green, 26 corrections/errata, 16 OWED (each gate-named), 2 BLOCKED, 2 vacuous
- CLOSE_20260927_NOON.md rewritten with byte-derived numbers + receipt-backed 400M+ token floor (ledger carries no token field; only the 1M/lane contract floor is attestable)

**Zero-padding trap**: first re-derivation used `glob(f'B2_{nn}_*.md')` and silently dropped 9 lanes (B2-01..09) because lanes file zero-padded names (`B2_01_*`) that `B2_1_*` does not match. The LANDED RULE matcher must parse the number (`re.match(r'B2_(\d+)_')` then int-compare), never glob on the unpadded id. Trust bytes, and trust them with a matcher that matches.

## Close receipt + handoff

- watch/inbox/burn_wave_20260926/CLOSE_20260927_NOON.md
- memory/HANDOFF_BURN_20260927.md
- watch/inbox/SESSION_RECAP_FD5EC147_20260927.md
