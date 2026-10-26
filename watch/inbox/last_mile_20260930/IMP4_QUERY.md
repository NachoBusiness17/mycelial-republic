# IMP4 — estate_query: the join-key reader riding AH14's corr_ids (AE5 wishlist #1)

**2026-09-30 · owner seat: corr-id lane · status: LANDED (refire)**

## The law

AH14 minted the join field (`corr_id`, uuid4 hex8, env `MAG_CORR_ID`) on the
three provenance writers. This is the reader that spends it: one tool, one
merged timeline, three joins — corr (the new key), path (the legacy grep),
time+model (the rollup).

## What landed

- **`tools/estate_query.py`** — `query` subcommand with `--corr`, `--path`,
  `--since`, `--model` (filters AND together; the unfiltered dump is refused
  exit 2 on purpose). Output: per-surface matched rollup + ONE merged
  timeline, oldest first, one line per event: `ts surface kind summary`.
- **Surfaces** (missing file reads as empty, never an error):
  `trajectory` memory/trajectory/steps.jsonl (37,469 rows live) · `burns`
  memory/burns/LEDGER.jsonl (693; pre-AH14, no corr field — joins by
  path/time) · `gameflow` memory/game/FLOW_LEDGER.jsonl (183; AH14's
  corr-carrying burns writer, `mag/game_flow.py` line 46) · `duel`
  logs/duel/duels.jsonl (63). Bad JSONL lines are skipped and counted (34
  live in steps), never fatal.
- **Old corr-less rows still surface**: absent `corr_id` reads as null
  (AH14 law); every row's compact JSON is the `--path`/`--model` match
  basis, so pre-AH14 steps and burn receipts join the same timeline by
  path — the legacy surface is not orphaned by the new key.
- **ts handling**: ISO-8601 parsed to aware UTC (`Z` and naive both);
  date-only `--since` means midnight UTC; `--since` drops rows with
  unparseable ts (an unverifiable time is not a match); ts-less rows sort
  deterministically after dated rows.

## Live smoke (instrument: `.venv/Scripts/python.exe tools/estate_query.py`,
moment 2026-09-30)

    query --corr c0b2a0d0   → 1 row: duel ah10-r1 (the live non-null corr
                              lane; steps carry corr_id null until lanes set
                              MAG_CORR_ID — the tool reports the honest
                              1-surface join, it does not invent neighbors)
    query --path AH14_CORR_ID → 1 trajectory step (the git add of the receipt)
    query --since 2026-09-30 --model glm-5.3-prime → 54 rows, rollup
                              trajectory 6 | duel 48
    query --corr 00000000   → "0 rows matched — no fabricated rows"

## Tests

`tests/test_estate_query.py` — corr join binds fixture rows across the AH14
writers into one ordered timeline (case-insensitive hex); path join surfaces
pre-corr rows (2026-09-28 step, burns receipt ledger); since+model rollup;
empty-honesty (explicit 0-rows line, exit 0, no invented timeline);
unfiltered dump refused exit 2; missing surface file reads as empty; bad
JSONL skipped-not-fatal; CLI end-to-end + limit reporting. Run: 14 passed
test_estate_query, 19 passed with test_corr_id_ah14 together. Instrument
`.venv/Scripts/python.exe -m pytest -q`, moment 2026-09-30.

## Refire note

The prior attempt landed code + tests but died at the 1302 before filing
this receipt (same pattern AH14's own refire closed). This session verified
the bytes (14/14 green), smoked all three joins against the live estate,
and filed the paper trail.
