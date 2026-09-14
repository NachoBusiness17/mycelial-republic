# G5-6 — FREE-LANE COST CURVE (deepseek-flash paid vs OrcaRouter free)

Date: 2026-09-10 | Seat: zcode | Source: logs/provider_usage.jsonl tail 100 rows + watch/inbox/v41_paces/LANE1_api_sweep.md

## THE POINT
The fleet's nightly shape is 95% cache-hit refeed (confirms B1 REFEED_HEAVY), so even at paid
off-peak rates 100 calls cost two cents — the paid bill is already near-floor. Free-lane routing
(OrcaRouter deepseek-flash, pending the identity canary) therefore saves real but SMALL dollars
(~$200/yr at measured burst rate). Its actual value is headroom, not pennies: no per-seat quota
clamp, no peak-window 2x, and capacity pressure rising after V4 Pro retires to flash on 09-14.
Route bulk to free, keep judgment-adjacent work on official paid off-peak as the sweep card
already assigns.

## SAMPLE (last 100 rows, 2026-09-10 20:41–21:33Z, 52 min burst)
- 100 calls, 99 ok: 97 deepseek-v4-flash (paid), 2 glm-4.7-flash (z_ai3, free lane), 1 ollama (failed, local)
- Input 1,257,130 tok — cache-hit 1,193,677 (95.0%), cache-miss 63,453; output 11,302 tok
- Measured burn at burst rate: ~2,770 calls/day (burst is not steady-state; conservative bands below)

## COST PER 100 CALLS
| Scenario | Cache-miss in ($0.15/M) | Cache-hit in ($0.003/M) | Out ($0.60/M) | **$/100 calls** |
|---|---|---|---|---|
| (a) All paid deepseek-flash, off-peak | $0.0095 | $0.0036 | $0.0068 | **$0.0199** |
| (a') All paid, peak window (2x) | $0.0190 | $0.0072 | $0.0136 | **$0.0398** |
| (b) All free (OrcaRouter) | — | — | — | **$0.0000** |
| (c) Current mix (97 paid / 3 free-lane) | $0.0094 | $0.0036 | $0.0068 | **$0.0198** |

Current mix ≈ full-paid because 97% of the window already rode paid deepseek; the free lanes
carried 3 calls.

## ANNUALIZED SAVINGS (free vs paid off-peak; paid peak = 2x these)
| Volume | Calls/yr | Paid $/yr | Free $/yr | **Saved $/yr** |
|---|---|---|---|---|
| 100/day (floor) | 36,500 | $7.26 | $0 | **$7.26** |
| 500/day | 182,500 | $36.28 | $0 | **$36.28** |
| 1,000/day | 365,000 | $72.56 | $0 | **$72.56** |
| 1,400/day (live clamp) | 511,000 | $101.59 | $0 | **$101.59** |
| 2,770/day (measured burst) | 1,010,905 | $201.17 | $0 | **$201.17** |

HEADLINE: **free-lane routing saves ~$0.02 per 100 calls (off-peak) — $7–101/yr at clamped
volumes, ~$201/yr at measured burst rate; peak-window exposure avoided doubles it.**

Caveats (tri-state): OrcaRouter free serve is SUPPORTED (listed) / UNPROVEN (live) — the
served-model identity canary from the ractor strike gates any fleet traffic; xplabs at $0.042/$0.085
is the cheaper paid fallback if the canary fails. Costs computed at official off-peak rates; night
waves land off-peak by timezone, day bursts would ride peak (2x input/out, miss rate unchanged).
