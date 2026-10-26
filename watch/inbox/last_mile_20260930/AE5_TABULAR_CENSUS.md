# AE5 — Tabular surface census (2026-09-30)

Owner seat: ZCode subagent (AE5). Mission: raw material inventory for a TabFM-Auto-shaped
model. All counts byte-derived with `.venv/Scripts/python.exe` streaming reads this session;
no hand-counted numbers. No commit (per order).

## Table census

| # | Surface | Rows | Columns | Dtype mix | Span / growth |
|---|---------|------|---------|-----------|---------------|
| 1 | `tools/gps_mcp/gps_ledger.db3` — `capability` | 2 | 7 | 3 num (pass_rate REAL, sample_size INT, cost_usd_per_call NULL), 4 text/ts | 2026-09-30 01:24→03:20 UTC; new today |
| 1b | same db — `verdict_log` | 10 | 5 | verdict INT 0–1, ts, model/task text, evidence_hash sha1 | same window; ~2.5 verdicts/hr burst |
| 2 | `logs/duel/duels.jsonl` | 38 | 18 | 7 num (a/b/judge_cost, a/b_chars, a/b_headers), enums (winner A15/B22/TIE1; mode live29/retro2/multifamily7), rubric list[text], criteria list[nested] | ALL rows 2026-09-30 (00:25→11:04); 85.7/day burst — new surface |
| 3 | `dashboard/static/trails/*.jsonl` (12 files) | 6,491 total | 5 shared: ts/actor/event/detail/artifacts | ts + enum-ish actor/event, free text detail, artifacts list | 09-04→09-30 (26d); research 2,842 (~109/d), day_work 1,976 (~76/d), builder 1,384 (~53/d); 5 cage trails dormant since ~09-05 |
| 4 | `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` | 93 (matches brief) | 7: thread_id, thread_name, ts, extracted{decisions,laws_or_debts,confidence}, model, cost_usd, pool | UUID text, ts, nested extracted (text lists + confidence enum), cost numeric | 08-04→09-09; file NOT ts-sorted (first row 08-30, last 08-17); ~3.7/day over 36d, quiescent since 09-09 |
| 5 | `memory/burns/LEDGER.jsonl` | 693 | 10: ts, slug, verdict, fresh_failure_mode, landing, one_line, failure_class, lane, restore, note | ts, bool, path text, long text; **verdict is free-text pseudo-enum** (~60 distinct: LANDED 310+19, steal 200, ERRATUM 7+5, OWED* 8, CORRECTION…) | 09-25→09-28 (3.2d); ~220/day |
| 6 | `memory/trajectory/steps.jsonl` | 37,005 (+33 malformed lines) | 7: schema_version, step_hash, ts, session_id, face, command, result{exit,output_excerpt,truncated} | sha256 hash, ts, face enum (bash 36,983 / milestone 22), command text, nested result | 09-05→09-30 (24.8d); ~1,495/day — largest behavioral table |
| 7 | `tools/legality_dataset.py` (synthetic, on demand) | default n=20,000 → 18,000 train / 2,000 val; verified live at n=200 → 180/20, 5 labels (illegal_unknown_target 46, illegal_dry_pool 51, illegal_unknown_verb 17, legal_no_gain 82, legal_gain 4) | row = engine state + verb + target + label | fully enumerated labels over real water-graph engine; regenerated per run, not append-growth | n/a (generator; out `logs/legality_ds`) |
| 8 | `catalog/catalog.jsonl` | 691,788 (194 MB) | 8: id, path, bytes, mtime, zone, ext, title, age_days | id 12-hex hash, 2 num, ts, zone/ext enums, path/title text | mtime range → 2026-09-30; snapshot churn not append (09-26 rebuild receipt cites 757,667 → now 691,788; trees pruned) |

## Query wishlist — 5 operator questions current tools answer badly

1. **"Has this failure shape happened before, and who hit it?"** No join key links
   `steps.jsonl` (session_id/command/result) to burns LEDGER (slug/landing path) or duels
   (ask_id) — provenance joins are grep-by-path, not SQL.
2. **"Is quality trending up?"** gps capability keeps only 2 live aggregate rows
   (overwritten); verdict_log n=10. Trends need the full verdict history the aggregate
   destroys, plus duels winner-rates over time (38 rows, one day).
3. **"Which rows are anomalous?"** 33 malformed steps lines, unsorted ORAL ts, ~60
   free-text verdict values: no tool flags schema-drift rows before analysis.
4. **"What did today cost, per model?"** cost fields live in three tables
   (ORAL_LAW_INDEX.cost_usd, duels a/b/judge_cost, capability.cost_usd_per_call NULL)
   with no shared model-day rollup.
5. **"What changed on disk since the last catalog?"** catalog is a full snapshot; delta
   queries re-scan 692K rows (FTS helps search, not freshness diffing).

## Notes

- legality dataset class balance: illegal:dry_pool and unknown_target dominate, legal_gain
  rare (2% at n=200) — a TabFM trained here will see gain as the minority class.
- Verdict enum normalization is the single highest-value cleanup for burns LEDGER.
