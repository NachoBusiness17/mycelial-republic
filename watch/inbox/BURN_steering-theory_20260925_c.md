# BURN steering-theory 2026-09-25 _c

## Verdict
steal

## Evidence
- tools/drift.py docstring: "Pure computation. Reads nothing, writes nothing." There is no registry in drift.py. A registered pair is a call: drift_check(metric, referent, window=0, label=""), two same-length float series, oldest first. Return fields: ok, tool, label, verdict, corr_dm_dr, deltas_used, metric_moved, referent_moved, note, law.
- Verdict code (lines 62-78): VACUOUS fires when referent_moved is False, computed as any(d != 0 for d in dr); ALIGNED corr >= +0.5; INVERTED corr <= -0.5 ("stop trusting the metric"); else DRIFTING; DEGENERATE = "zero variance in one series' deltas"; INSUFFICIENT = "need >= 3 deltas after windowing".
- drift_check_cmd: "Comma-separated numeric series version for MCP/CLI callers" (zero-code landing path).
- Path precedent: GPS battery lived at watch/inbox/GPS_BATTERY_20260918.jsonl (FOLD.json artifacts); run outputs at memory/runs/gps_50/. Shared-surface law: durable writes land in watch/inbox.
- Freshness: one search, no new late-September 2026 judge-calibration work beyond the already-anchored arXiv 2508.06225. GitHub LLM-Confidence-Calibration-Benchmark shows "6 Commits", no visible dates, ECE/MCE/Brier on 8 small open models, no logprob-vs-verbalized split. Field quiet; no freshness theater filed.

## Steal or Vacuous
Steal: land-ability confirmed, zero edits to drift.py needed.

(a) No registry exists in drift.py; a pair is label + two series + window at call time. Persistence is caller-side.
(b) One change lands pair A: a series runner (new tools/probe20_run.py or main.py command) that per cycle computes mean verdict-token logprob margin and correct/20, appends one row, and after >= 5 rows calls drift_check on the tails. Zero-code alternative: drift_check_cmd with comma-joined series from a shell loop.
(c) Probe set: watch/inbox/PROBE20_steering_v1.jsonl (battery precedent, version hash in filename and per row). Series: memory/runs/probe20/<lane>_<pair>_series.jsonl (run-output precedent).
(d) Kill translation: VACUOUS is native (referent flat); pair A "probe saturated" and pair B "overturn flat" both land exactly. DRIFTING covers -0.5 < corr < 0.5; receipt _b "0 < corr < 0.5" undercounts, mildly negative corr also lands DRIFTING. INVERTED native, matches _b. INSUFFICIENT (< 4 points) and DEGENERATE (metric frozen while referent moves) are neither kill nor pass; pre-register both as re-instrument, not filed. Trap: the VACUOUS gate is any(delta != 0), so one 0.05 task flip defeats it; the runner must enforce the noise-floor law, drift.py will not.

Draft registry rows (caller-side JSONL, drift.py untouched):
{"pair":"A","label":"lane=gemma4:A-conf-margin-vs-correctness","probe":"watch/inbox/PROBE20_steering_v1.jsonl","series":"memory/runs/probe20/gemma4_A_series.jsonl","row_schema":{"cycle":0,"probe_version_hash":"sha256","margin":0.0,"correct":0},"min_points":5,"expect_corr":[0.3,0.8],"kill":["VACUOUS","DRIFTING","INVERTED"],"pass":["ALIGNED"],"reinstrument":["INSUFFICIENT","DEGENERATE"]}
{"pair":"B","label":"lane=gemma4:B-escalate-rate-vs-overturn-rate","series":"memory/runs/probe20/gemma4_B_series.jsonl","row_schema":{"cycle":0,"escalated":0,"total":0,"overturns":0},"derived":{"metric":"escalated/total","referent":"overturns/escalated"},"den_min":{"metric":20,"referent":5},"min_points":5,"expect_corr":[0.0,0.6],"kill":["VACUOUS","DRIFTING","INVERTED"],"pass":["ALIGNED"],"reinstrument":["INSUFFICIENT","DEGENERATE"]}

## Falsifier
Pre-registered, translated to drift.py: >= 4 probe cycles per lane (gemma:2b, gemma4), both pairs. Runner reads verdicts from drift_check only. Kill: if BOTH pairs on BOTH lanes return only VACUOUS, DRIFTING, or INVERTED, the confidence-as-drift-pair build is demoted VACUOUS and stops. Any ALIGNED keeps it alive. INSUFFICIENT or DEGENERATE counts as neither; on pair A DEGENERATE or VACUOUS the probe is re-versioned immediately and the refresh logged. Runner additionally rejects any window whose referent moved by a single 0.05 flip only (one-flip VACUOUS escape).

## Bibliography
- tools/drift.py (repo, read 2026-09-25)
- memory/runs/gps_50/FOLD.json (repo, read 2026-09-25)
- watch/inbox/BURN_steering-theory_20260925.md and _b (repo, read 2026-09-25)
- https://github.com/NIKHIL0VERMA/LLM-Confidence-Calibration-Benchmark (fetched 2026-09-25)
- Web search 2026-09-25 (arxiv 2508.06225v2, aclanthology 2025.emnlp-main.530, emergentmind, academia.edu ConfidenceBench, langchain.com: snippet level only, unread beyond snippets, uncited above)
