# DAILY COST LEDGER — 2026-09-01 (day 1 of the running record)
Schema: append-only, one day per block. Sources: water_ledger (cash), archivist telemetry (provider invoices), subagent run ledger (openclaw), xai sandbox arithmetic (labeled). ESTIMATED ≠ MEASURED, always labeled. Purpose: cost today, profit someday — the record must be good enough to price products against.

## Cash spent today (MEASURED)
| item | amount | receipt |
|---|---|---|
| zai billed-API session (3254… lane, before 01:21Z route fix) | **$0.743** | archivist `zai_billing_telemetry` (236 calls, 4.29M in / 11.3M cache / 374k out) |
| deepseek swarm/subagent lane (20 gopher+research runs, 723k tok, 150k out) | **≈$0.09** ESTIMATED (in $0.14/M, out $0.28/M, 50% cache-hit assumed; range $0.05–0.15) | openclaw run ledger + xai sandbox math 05:57Z |
| **TOTAL CASH — fleet autonomy work (00:00–06:00Z)** | **≈$0.83** | |
| carried debt from 08-31 (water_ledger OCTANT correction) | $3.40 lifetime | B1 water_ledger |

## $0-marginal capacity consumed (quota burn, not dollars)
| lane | used | ceiling | notes |
|---|---|---|---|
| zai-pro Max | session lane 00:55→now | 1600 prompts/5h · 8000/wk | funded 08-31; $0 marginal |
| zai Lite | 0 (law filed, calibration probe pending) | 2k credits/5h · 10k/wk | unlocked today; zcode primary consumer |
| groq | gopher overflow only | 30 RPM / 1K RPD / 200K TPD | 87.4% fuel ok |
| cerebras | activated | 1M TPD | |
| grok_a/grok_b + codex | idle | subscription sunk | surfaces: paste.rs RIB bus live (yYX0f + ntfy topic) |
| ollama | T0 janitor | electricity | |

## Cost-per-outcome (the line that becomes pricing later)
| outcome | cash | mechanism receipt |
|---|---|---|
| 42 operator links triaged, inbox 53→0, 4/4 gaps closed | ~$0.05 (5 gopher lanes, 111k tok) | GOPHER_DIGEST_20260901_0410Z.md |
| live steering demonstrated (Brain→Tail, D-lerp 2→3, 26/26 verify) | ~$0.02 (est) | steer_exp_001_receipts.jsonl |
| INDEX race-kill + invariant root (2 experiments, PASSED) | ~$0.03 | EXP002A/002B receipts |
| fleet audit (33 attempts census, 9 LIVE) | ~$0.04 | FLEET_AUDIT_20260901.md |
| full day's governance + digest + laws + surfaces | ≈$0.83 all-in | this file |

**Economics verdict:** autonomy cost ≈ **$3.3/day run-rate** (DeepSeek $1.33 + zai-API residue + incidentals) against a $20 water pool; the $1/hr operator-active law held ($0.83 for ~6h active window = $0.14/hr actual — 7× under the cap). No billed-lane regressions after 01:21Z route fix. Profit side of the ledger: pending (vault venture + verified-restore are the first candidates; not yet revenue).

## Ladder (better-by-default)
- Weekly roll-up every 7 days: cash by lane, cost-per-outcome trending, top waste source.
- Meter gaps to close: per-lane burn rows in water_ledger (11/12 reservoirs unmeasured — economist honest gap), zai Lite calibration probe (real mults), Together/DS batch pricing test.
- If weekly autonomy cash > $5 while operator cash-pool untouched by agents: flag lane consolidation (herd gophers onto cerebras/groq TPD before DeepSeek).
