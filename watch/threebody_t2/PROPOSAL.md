# THREE-BODY T2 PROPOSAL — stack_recommendation_20260831.md (PROPOSER, 5.3)

## 1. Verdict: three independent fixes, not yet a governor loop

The rec's "they compose in order" is sequencing, not composition. Move 2 feeds Move 1 only
if outcomes written by the governed fan land in ask_router's ledger — but ask_router reads
`memory/runs/ask_router/ledger.jsonl` (/mag/mag/ask_router.py:20), and that file does not
exist; every lane's why is a neutral 0.5 prior (ask_router.py:84). Each move passes its
one-step test in isolation while the claimed loop stays open between them. A loop needs a
wire Move 3 never names: `--record` (ask_router.py:210) is the only write path, and no file
in /mag/mag calls it. Connection, not sequence, is the missing piece.

## 2. Three testable claims

1. **Fan-gating is paper today.** harness.py:282-305 executes without advancing the
   switchboard trail. *Test:* one `harness.run_once(dry=True)`, assert
   EXECUTING→COMPLETED→RECEIPT_COMMITTED appears. *Calibration: certain* it fails today,
   *likely* passes after patch 4 alone.
2. **Routing learns from nothing.** All receipts show `ledger_rows:0`, `dry:true`
   (/mag/memory/runs/ask_router/receipts.jsonl, 4 rows 04:42–04:54Z). *Test:* fire one live
   cascade, `echo '{"lane":"zai","ok":true}' | python -m mag.ask_router --record`, re-route,
   require `ledger_rows>0` and ok_rate≠0.50. *Calibration: certain* as bytes show, *likely*
   the pipe works untested.
3. **Cage rows are underef-able.** Board fan rows carry no receipt column. *Test:* POST one
   row with `receipt:` pointer, run `board_tailer --dispatch`, confirm deref. *Calibration:
   likely* fails (gap 6 dilution), *plausible* it derefs.

## 3. Biggest miss: outcome-binding is a missing organ, not a config fix

I byte-checked the receipts: all four show `dry:true` + `memlance.ok:false` — but that is
*by design* in dry mode ("dry: skipped", ask_router.py:110). The rec's proposed flag
`--dry --record-outcome` cannot exist: dry deliberately skips memlance/verkle (ask_router.py:108-146),
and `--record-outcome` isn't a flag — `--record` (ask_router.py:210) reads stdin, exists,
is correct, and has **zero callers**. `ledger_rows:0` is not a config toggle; the writer
organ is orphaned and the reader starves. Missing organ: fan → `--record` wire.
