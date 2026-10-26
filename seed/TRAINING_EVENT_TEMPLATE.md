# TRAINING EVENT TEMPLATE (mag_training_event.v1)

One JSONL envelope for every agent action worth training on. Its one design decision
does all the work: **join keys, evidence, and verdict live in separate fields**, and the
export gate rides on the row itself.

## Field dictionary

| field | holds | why separate |
|---|---|---|
| `schema`, `event_id`, `ts` | `mag_training_event.v1`, `evt-<hex12>`, ISO UTC | identity — never merged into payload |
| `pattern` | the event type (~9 in the source: route_decision, arena_match, autorun_cycle, task_lifecycle, three_body_episode, …) | the join axis for training corpora |
| `join` | boot_id / run_id / session_id / seat / actor — the KEYS other tables join on | identity ≠ evidence |
| `input` | what the world looked like (the evidence) | observed before acting |
| `action` | what was done | decided on the evidence |
| `outcome` | what happened (the verdict — measured numbers, winner, status) | judged after acting |
| `pattern_tags` | free tag list | coarse corpus slicing |
| `tier_max`, `exportable` | data-tier ceiling (`T2`) + gate flag (`true`) | the export stage filters on these AT ROW LEVEL |

## Route_decision sub-schema (routing policy as replayable data)

- `input`: probe readings (local tps, gpu %, latency, ok-flags, candidate list)
- `action`: the decision — `route_primary` or `winner`
- `outcome`: measured A/B results array `[{model, tps, gpu_pct, elapsed_ms, ok}, …]` + a
  plain `reason` string

Real rows from the source head (lines 34-35): a probe down (local 21.5 tps, GPU 100%,
latency 534 ms, probe ok=false → route to remote, reason logged) and a desk A/B
(gemma 28.8 tps ok=false vs qwen 69.2 tps ok=true, same GPU → winner recorded with both
results). The routing policy became data a later session can replay or re-fit.

## The league row (line 40)

Arena matches record per-model standings in `outcome.league_top`: wins/losses/games,
`illegal_move_rate`, `value_score`, strengths/weaknesses — training signal and honest
failure accounting in one row.

## Receipt

- training/events.jsonl:1-3, :34-35, :40 (estate) — read this session; `wc -l` →
  **542,763** (grew from 542,694 last session — append-by-design). See TRAINING_SPINE_LAW:
  rows ≠ training until the join→export→eval spine exists.
