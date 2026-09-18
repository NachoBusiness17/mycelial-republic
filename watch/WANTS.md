# WANTS — standing intake (any window, any seat)

> The self-tending cron (automation-b499da5b) reads this file FIRST when the
> union queue runs low. One line per want: what, where it lands, done-looks-like.

## 2026-09-18 — corpus map program (salon fold, CORPUS_MAP_SALON_20260918.md)

- WANT: scanner v2 append-mode swapped for idempotent rebuild (v3 draft is in the
  fold artifact, ready to land as mag/catalog_rebuild.py) → then one full rebuild;
  done = row count stays ~947K after two consecutive runs, ruins_go_engine.js
  visible to corpus_search. **[DONE 2026-09-18 — v3 walk ran inline (757,667
  rows, deduped, junction-pruned); ruins_go_engine searchable; module landing
  still owed for a reusable `python -m` entry]**
- WANT: freshness budget for the catalog (incremental rescan or scheduled rebuild)
  → done = a written policy in the fold artifact's conditions, C6 satisfied. **[PARTIAL — rebuild is manual-this-window; scheduled/incremental still owed]**
- WANT: tags v2 with owner column (who authored the tag, when) per salon condition
  → done = tags rows carry owner+created; kind filter still green.
- WANT: held-out retrieval eval (UF-122 spec first) → done = 50 questions scored,
  citation-recall baseline recorded before any mining pass.
- WANT (SELF-AUDIT F2, 2026-09-18): **verify-before-replace law** — any rebuild
  of a large derived file writes to a NEW file and passes a row-count gate
  (catalog: rows > 500K) BEFORE atomic swap; no blind replaces, derived or not.
  → done = gate present in the landed mag/catalog_rebuild.py.
- WANT (SELF-AUDIT F5): a witness pass on SELF_AUDIT_ZCODE_20260918.md +
  the elder lens backlog (deepseek-pro, 14d pending) → done = countersigned
  receipts on both.
- WANT: SQLite FTS5 decision executed per UF-120's threshold — not before.
