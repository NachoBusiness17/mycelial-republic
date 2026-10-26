# DELIVERABLE — LAW-CANDIDATE 059 FALSIFIER INSTRUMENT (restful watch, 2026-09-06)

Built by: worker `restful` (concurrency probe group 2, width 8, operator GO). $0, local files only.

## THE INSTRUMENT
**Ledger:** `watch/falsifiers/RESTFUL_WATCH_LEDGER.md`
- Append-only 7-day tally for law-candidate 059 REPAIR-ON-SIGHT
  (canonical: `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`).
- Append convention is at the top of the ledger: any seat appends a row the
  moment it catches something, citing evidence; corrections are NEW rows citing
  the old row id; nothing is ever edited or deleted in place.

## SEEDED TALLY (day 1, 2026-09-05 — the receipted day)
- **Vision-catches: 7 (V-01…V-07), every one evidence-cited** — openalex 429
  (CONVO row ~16:2xZ), pin drift 5.3-full (CONVO row ~20:4xZ), concurrency
  failover (CONVO row ~16:2xZ), night-watch automation death (CONVO rows
  ~16:2xZ + ~08:5xZ, CronList), inbox drift (CONVO row ~16:2xZ item 3),
  Lite 73.2M burn (CONVO row ~05:1xZ), art 404 / wiring orphans (canonical card
  row 7; repair continuation `watch/WIRING_AUDIT_20260906.md`).
- **Timer-caught-failures: 0 (T rows: none).** The night shift (a5e12eea) had
  not yet had its first fire; nothing scheduled saw anything that day.
- Running tally after seed: **7:0**.

## PROMOTION GATE (decided at 2026-09-11 EOD)
1. Cumulative 7-day ratio **vision:timer >= 5:1**.
2. **Every row evidence-cited** — one UNEVIDENCED row blocks promotion until
   fixed via a correction row.
3. **A single fabricated row kills the law** for the window — if any row's
   evidence fails verification, 059 does not promote, period.
4. Inverse (from the canonical card): scheduled fires OUT-CATCH looks over the
   week → REPAIR-ON-SIGHT dies and the cron teeth were right.
Clocks keep their right-sized residue either way: night shift = opportunity
anchor only (decks/seals/cheap window); deadlines stay deadlines.

## WHAT COUNTS AS A TIMER-CAUGHT-FAILURE (strict — no strawmen)
ALL four must hold, or the row does not enter the timer column:
1. **Clock-origin** — a scheduled process detected the defect on its own fire,
   not during a steering pass and not because a human/seat looked at its output.
2. **Novel sight** — the defect was NOT already caught/filed/visible to any seat
   at detection time (a timer re-reporting a look's find counts for the look).
3. **Repair path** — detection led to a landed fix or recorded disposition
   within the window.
4. **Evidence** — fire log / automation id + defect receipt, cited in the row.
Explicit NON-counts: opportunity work with nothing caught (decks, seals,
rotations); checks a seat ran by hand; a timer that fired and found nothing; a
defect a seat saw first then handed to a timer to fix; a timer report nobody
read until a look tripped over it.

## HOW TO USE
When any seat catches a defect on sight → append a `V-nn` row to the ledger with
1-line + evidence path. When a scheduled fire genuinely catches a defect nobody
had seen → append a `T-nn` row the same way (honesty cuts both ways; a real T-row
is data, not defeat). Window verdict gets written at the bottom of the ledger on
2026-09-11, promotion is the operator's call.
