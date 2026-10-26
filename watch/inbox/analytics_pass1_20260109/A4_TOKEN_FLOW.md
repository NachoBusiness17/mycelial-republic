# A4 TOKEN FLOW - analytics pass 1: where tokens go

lane A4 (token flow) | read-only analysis | aggregation via .venv\Scripts\python.exe

## Instruments and moments
- memory/runs/hermes_burn/usage.jsonl - 3,038 rows, ts span 2026-10-01T13:11:41Z to 2026-10-07T09:21:35Z, read this session
- watch/inbox/disk_audit_20261009/evidence_pack/exec_forensics.json + digest.md - exec forest walk, moment 2026-10-09T01:28:25Z, 667s walk, 11,079 files, 309.12 GiB, 0 stat errors
- watch/inbox/disk_audit_20261009/PROBE1 receipt - searched for, not present

## Paid side: by model (usage.jsonl)
| model | calls | ok | tokens | cost | $/call | $/1Mtok |
|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | 1,248 | 765 | 7,478,062 | $59.83 | 0.0479 | 8.00 |
| anthropic/claude-fable-5.1 | 418 | 254 | 1,328,797 | $18.30 | 0.0438 | 13.77 |
| anthropic/claude-sonnet-5.5 | 693 | 616 | 3,480,239 | $12.31 | 0.0178 | 3.54 |
| anthropic/claude-haiku-4.5 | 672 | 672 | 2,211,844 | $2.67 | 0.0040 | 1.21 |
| z-ai/glm-5.3-prime | 7 | 5 | 341,081 | $1.64 | 0.2340 | 4.80 |
| TOTAL | 3,038 | 2,312 | 14,840,023 | $94.74 | 0.0312 | 6.38 |

- Anthropic models carry 3,031 of 3,038 rows and $93.10 of $94.74 (98.3% of spend).
- ok=False rows: 726 (23.9%) but only $0.58 and 101,066 tokens; 993 rows carry doubled_key:true worth $15.67.

## Paid side: by day, joined to exhaust (GiB by mtime from per_day)
| day | calls | tokens | cost | exhaust GiB |
|---|---|---|---|---|
| 10-01 | 236 | 4,368,123 | $37.76 | 2.30 |
| 10-02 | 5 | 241,281 | $1.17 | 18.72 |
| 10-03 | 1,034 | 4,340,905 | $25.62 | 32.19 |
| 10-04 | 1,448 | 5,011,722 | $26.29 | 61.20 |
| 10-05 | 287 | 760,394 | $3.76 | 45.86 |
| 10-06 | 2 | 17,380 | $0.03 | 11.01 |
| 10-07 | 26 | 100,218 | $0.10 | 45.74 |

- 10-08 (13.18 GiB) and 10-09 (0.00 GiB) have no ledger rows; ledger ends 10-07T09:21Z.
- Big GiB days before the ledger window: 09-28 23.77, 09-29 22.72, 09-30 12.55, 09-25 12.38.

## Exhaust side: who deposited the GiB (top_sess, exec_forensics.json)
- All 40 top_sess entries are sess_dwf-dwfrun-* sessions (ZCode dynamic-workflow exec logs): 230.2 GiB in 94 files = 74% of the whole 309.12 GiB walk.
- Top dwfrun ids by GiB: 27c7e7b2 34.86, 0da272a1 24.80, ab8d406e 23.62, a5abb24e 12.52, aa9969b0 11.62, cda8c867 10.73.
- Largest single files are call_*-stdout.log: 12.42 GiB (0da272a1/actor_3_5), 10.46 GiB (27c7e7b2/actor_3_6), 8.32 GiB (a5abb24e/actor_3_21).
- Extension split: 4,975 .log files carry 331.90 GB of the 331.91 GB walk total (99.997%); 6,100 shell-snapshot .sh files carry only 10.18 MB.
- Secondary surfaces (same pack): temp 51.4 GiB (recovery_pack 28.3, lsarchive 19.8), hermes_local 32.3 GiB (cache 20.6), zcode_cli non-exec 7.7 GiB.

## The join: do paid-token days correlate with exhaust-GiB days?
- Pearson r over the 7 shared days (10-01 to 10-07): r(cost, GiB) = -0.107, r(tokens, GiB) = +0.137. No correlation; money slightly negative.
- Extremes: 10-01 is the most expensive day ($37.76, 39.9% of the week) and the leanest exhaust day (2.30 GiB); 10-07 spends $0.10 on 26 calls yet deposits 45.74 GiB.
- Interpretation: the two ledgers ride disjoint lanes. usage.jsonl banks paid hermes-burn dispatches; the GiB are local dwf workflow children writing stdout logs under .zcode\cli\exec. Byte mass tracks shell fan-out width and log verbosity, not provider tokens. Disk exhaustion is a free-lane symptom the money ledger cannot see, and vice versa.

## Price table (per-model $/call, derived cost / calls)
| rank | model | $/call | $/1Mtok | ok rate |
|---|---|---|---|---|
| 1 | z-ai/glm-5.3-prime | $0.2340 | 4.80 | 71.4% |
| 2 | anthropic/claude-opus-5.5 | $0.0479 | 8.00 | 61.3% |
| 3 | anthropic/claude-fable-5.1 | $0.0438 | 13.77 | 60.8% |
| 4 | anthropic/claude-sonnet-5.5 | $0.0178 | 3.54 | 88.9% |
| 5 | anthropic/claude-haiku-4.5 | $0.0040 | 1.21 | 100% |

- glm-5.3-prime tops $/call at 4.9x opus because its 7 calls are single huge deliberate-ask turns (34k to 216k tokens each).
- haiku is the only 100% ok model; fable is the worst ok rate (60.8%) AND the priciest per token (13.77 $/1Mtok).
- 11.93M of 14.84M tokens (80.4%) are prompt tokens: both lanes pay for context, not output.

## STRANGE FINDINGS
1. ONE ASK = A QUARTER OF THE WEEK: id A1_steer_antiforgery alone banked $21.85 of $94.74 (23.1%) across 52 calls; the runner-up id (T1W1_stranger_shared_surface, $1.72) is 12.7x smaller.
2. LEDGER CONTRADICTS THE FUNDING MAP: the DRIVING LADDER rib (2026-09-28) says Anthropic keys are UNFUNDED and the Nous primes are the funded workhorse, yet 98.3% of dollars in this window went to Anthropic models and the prime saw 7 calls in 7 days.
3. MONEY AND BYTES ARE DECOUPLED AT THE EXTREMES: r(cost, GiB) = -0.107; the top-dollar day deposited the least GiB (2.30) while a $0.10 day deposited 45.74 GiB.
4. FAILURES ARE FREE, SUCCESS IS EXPENSIVE: 726 failed calls cost $0.58 total (0.6% of spend) and 89 refused rows cost exactly $0.00; the entire bill is ok=True traffic.
5. THE 999x UNDER-BANK: row PROBE_A1PAYLOAD_20261007_K2 (10-07T09:21Z) carries cost_correction_for noting the 09:14Z row banked $0.0001 while provider usage cost $0.0999 - the correction probe exists because single rows can under-report cost by 3 orders of magnitude.
6. BIGGEST DEPOSITOR ALREADY GONE: the 12.42 GiB call_91ae...-stdout.log no longer exists at read time; .zcode\cli\exec now measures ~75 GB vs 309.12 GiB at the 01:28Z scan moment - cleanup reclaimed roughly 234 GiB inside the audit window (du vs walk differ; magnitude only).
7. FEW FILES, ALL MASS: 94 files among 11,079 carry 74% of the walk's bytes - single-digit workflow stdout logs, each a call_ record, are the exhaustion unit; no cleanup that skips dwf session dirs touches the mass.

lane A4 done. All numbers derived from the two instruments named above; no hand-copied counts.
