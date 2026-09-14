# SELF-STEAL — TIMEKEEPING: one bug, four coats (2026-09-07)

**Operator (verbatim):** "we tried to keep time using the github trick but that never really
stuck, self steal... duplication is repetition... it's just a bug wearing a different coat...
it's all data baby."

## The lineage

| Coat | Date | The clock | How it died |
|---|---|---|---|
| **The github trick** | Sep 3 | CI-clock lane scan — GitHub Actions' 2000 free minutes as an external scheduled clock | Never built; sits on the OWED/CARRIED list (watch/MORNING_STATE_20260903.md:37). A clock living in someone else's scheduler, gating nothing. |
| **Chronos zero-scale cron** | Sep 7 AM | Q instance's morning pulse, fired while scaled to zero | Died with its body the same day — the rent-a-body ruling deleted the instance (watch/SELF_STEAL_RENT_A_BODY_20260907.md). Clocks owned by deleted bodies die too. |
| **The timezone burn** | Sep 7 | None at all — 73/73 seals at 04:00-07:59 PT, outside the promo window | The bug's purest coat: no prescriptive clock existed anywhere in the dispatch path. The seat recorded time perfectly and obeyed nothing. |
| **burn_gate** | Sep 7 | mag/burn_gate.py — PT window + quota floor, checked in the dispatch path | Candidate last coat. See below. |

## The shape clause (same bug, many jackets, root survives translation)

**The fleet keeps time beautifully and obeys nothing.** Descriptive time always worked — the
chain's minute spans, the tape's ts, receipt_ts — recording is excellent. The recurring bug is
PRESCRIPTIVE time: every clock that was supposed to GATE action either lived in someone else's
infrastructure (github), lived in a body that got deleted (Chronos), or didn't exist (the
timezone). Same root, four translations.

## Why burn_gate is the candidate last coat — and the falsifier that says so

1. File-local — no external body whose death takes the clock with it.
2. In the dispatch path, not a daemon waiting to be consulted.
3. Wallet-enforced — deferral has teeth (the 4% receipt proved the floor is real).
4. Sealed at birth (tape step 482798144c22624e) — the gate's own construction is on the record.

**Falsifier (the next-coat detector):** any future dispatch — builder, salon, fan-out — that
fires without a burn_gate check is the bug's fifth coat. The card names the shape in advance so
recognition is instant: a clock that gates nothing is decoration, wherever it's hosted.

## It's all data

The 73 outside-hours seals are not shame — they are the calibration set. A gate built without
them would be policy; a gate built from them is measurement. The burn bought the sensor.
