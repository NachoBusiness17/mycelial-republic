# COST LEDGER TEMPLATE (cost_ledger.v1)

Per-task **estimate-vs-actual** cost accounting, with calibration error as a first-class
field. It tells you not just what you spent, but whether your estimates can be believed.

## The record (one JSONL line per finished task)

```json
{"schema": "cost_ledger.v1", "ts": "<ISO UTC>",
 "join": {"queue_id": "...", "task_id": "...", "session_id": "..."},
 "estimate": {"depth": "<plan|route|execute>", "context_need_tokens": N, "output_tokens": N,
              "price_band_usd": X, "seat": "...", "model": "..."},
 "actual":   {"prompt_tokens": N, "completion_tokens": N, "usd_est": X, "usd_fixed": X, "calls": N},
 "outcome":  {"success": true, "leaf_kind": "<test|terminal|...>", "waste_kind": null},
 "value":    {"usd_per_leaf": X, "estimate_error": R, "seat_efficient": true},
 "platform": {"provider": "...", "model": "...", "seat": "..."}}
```

## The two fields that make it a calibration instrument

| field | meaning |
|---|---|
| `estimate_error` | actual ÷ estimate. `1.0` = calibrated. `26.84` = a 27× underestimate. `-1.0` = came in at zero. |
| `usd_per_leaf` | spend per delivered unit of work — the number that survives "was it worth it" |

## The source ledger's own opening lesson (head rows 1-2, verbatim numbers)

| row | estimate | actual | estimate_error |
|---|---|---|---|
| execute-depth task | $0.0006 (1,200 ctx tokens) | **$0.0167** (56,998 prompt tokens, 7 calls) | **26.84** |
| route-terminal task | $0.0006 | $0.0 (0 tokens, 0 calls) | -1.0 |

Twenty-seven× off in one direction on deep tasks, all-the-way-off in the other on
terminal tasks — both visible only because error is a field, not a feeling. Any estimator
can be re-fit from a log shaped like this.

## Receipt

- training/cost_ledger.jsonl (estate) — head rows 1-2 read this session; `wc -l` →
  **2,233**. Numbers above are byte-read, not paraphrased.
