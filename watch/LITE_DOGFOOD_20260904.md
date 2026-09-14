# LITE DOGFOOD RECEIPT — the plan tested as a seat (2026-09-04)

**ITEM:** Operator loaded this seat on the GLM Coding Lite plan as a live dogfood: "I want
to configure the lite plan to drive when it becomes free at 11." Then, after the test:
"did a test with lite. lmao it wasn't good hahahaha." This card is the receipt.

## RECEIPTS (the seat's own meter — ~/.zcode/cli/db/db.sqlite, table model_usage)

Today (20h window to ~10:05 local), status=completed:

| model | calls | in | out | cache_read | computed_total |
|---|---|---|---|---|---|
| GLM-5.3 (paid) | 338 | 205.4M | 82K | 202.4M | **205.5M** |
| GLM-5.3-Flash | 2,789 | 468.5M | 2.6M | 445.3M | **471.1M** |
| GLM-4.7-Flash | 32 | 1.87M | 14K | 0.6M | 1.9M |

This conversation alone (sess_dddf6069, GLM-5.3): **274 calls, 201.3M computed tokens** —
the day's single largest session, ~98% of it cache_read: the conversation re-sends its whole
context every turn; volume, not verbosity, is the killer. Operator-observed effect on Lite:
one planning conversation ≈ **50% of the hourly compute**.

## READ
- **VERDICT (Supported by meter): LITE CANNOT DRIVE THE SEAT.** A judgment seat is a
  context-heavy standing conversation; the Lite package (empirically 50/50 + 27.85 rps
  sustained — those receipts STAND for bulk) starves on volume long before its concurrency
  shines. Lite was never the wrong product — it was pointed at the wrong organ.
- **RIGHT-SIZED SPLIT (operator ruling, enacted): Max drives judgment; the Lite KEY keeps
  the day-work bulk lanes** (z_ai3/Calcifer pinned glm-5.3-flash via fuel_feed FREE_LANES).
- Cache dominance (98%) is CONTEXT-DEBT law live on my own meter: every turn re-pays the
  whole history. The salon's 5 laws from the usage-meter self-steal apply verbatim here.

## TRI-STATE
- Meter numbers: **Supported** (read from the seat's own usage db, query below).
- "50% of hourly on this convo": **Supported** (operator observation + meter volume;
  exact Lite-side quota internals Unproven — vendor meter not exposed).
- Bulk-lane fitness of the Lite key (27.85 rps / 50-burst): **Supported** (prior receipts,
  unchanged).

## VERDICT: dogfood CLOSED — Lite key = bulk lanes, Max = judgment. No hybrid seat-driving.

## ROUTE
- 11:00 one-shot probe (approved): if Lite quota freed, fire bulk day work on it; else log + stand by.
- Economist stamp owed on the $ translation of the table above.

## DOGFOOD QUERY (every seat audits itself — paste-ready)
```
python -c "
import sqlite3,time
db=sqlite3.connect(r'C:\Users\foste\.zcode\cli\db\db.sqlite'); c=db.cursor()
now=int(time.time()*1000)
for r in c.execute(\"SELECT model_id,COUNT(*),SUM(input_tokens),SUM(output_tokens),SUM(cache_read_input_tokens),SUM(computed_total_tokens) FROM model_usage WHERE status='completed' AND started_at>=? GROUP BY model_id\",(now-20*3600*1000,)): print(r)
db.close()"
```

## ECONOMIST STAMP (2026-09-04 ~19:0xZ — receipt-002; the $ translation owed above)

Independently reproduced the table from the same db at a later 20h window (day still
running): GLM-5.3 paid 1,143 calls / 292.6M computed / **98.1% cache_read**;
5.3-flash 2,861 calls / 481.9M computed / **94.8% cache_read**. Card figures are a
10:05-local snapshot of the same curve — consistent throughout.

- **Meter table: Supported** (deterministic db query, reproduced independently).
- **"One planning conversation ≈ 50% of hourly compute": Unproven as a Lite-quota
  claim** (vendor quota internals not exposed); Supported as volume — sess_dddf6069
  was the day's largest session at 201.3M computed, ~98% cache re-feed.
- **$ translation (credit heuristic, ceiling-grade):** applying the measured flash-class
  credit rates (input ~12,312 tok/cr, cache ~50,381, output ~3,591) to today's seat
  burn: 5.3 paid ≈ 6.3K cr, 5.3-flash ≈ 11.8K cr → **~18K cr ≈ 13% of the 140K weekly
  ceiling [est]**. Two caveats: (a) rate transfer from flash lane to seat models is a
  heuristic — exact per-model credit rates Unproven; (b) the token counts include
  promo-window hours where flash is unmetered, so actual credit burn ≤ this figure.
- **VERDICT "Lite cannot drive a judgment seat": Supported** — a judgment seat is a
  standing context conversation (98% re-feed every turn); volume starves Lite long
  before its concurrency shines. Lite-as-bulk-lane receipts stand unchanged.
- Cash side: both figures are within the subscribed Max plan — **out-of-pocket $0**;
  the cost is credits/quota, not invoices. Supported (subscription receipts + promo
  terms in the expert reference).
