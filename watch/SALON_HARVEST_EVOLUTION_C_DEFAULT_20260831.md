# SALON HARVEST EVOLUTION – LANE C (Better‑by‑Default) – 2026‑08‑31

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: a four-week self-tuning ladder (hit-rate monitor, dedupe pruning, hot-hit promotion, operator confirmation gate) improves harvest automatically each week at negligible CPU/storage cost — UNPROVEN (no week1–week4 metric files cited in card) · falsifier: implemented metrics showing hit_rate stuck <0.70 or dedupe_rate >0.10, or pruning/promotion degrading stack quality

**Goal:** self‑tuning harvest system that improves automatically each week.

1. **Week 1 – Automated Hit‑Rate Monitor**
   - *Change:* Add a daily metric `hit_rate = stacked_receipts / total_hits` stored in `/board/metrics/week1.json`.
   - *Proof‑meter:* Log entry `"hit_rate": 0.xx` for each run; alert if < 0.70.
   - *Cost:* ~2 CPU‑seconds per run, ~5 KB storage.

2. **Week 2 – Dedupe‑Rate Pruning**
   - *Change:* Introduce `dedupe_rate = duplicates / total_items` threshold (≤ 0.10) and auto‑prune items exceeding it.
   - *Proof‑meter:* Append `"dedupe_rate": 0.xx` to `/board/metrics/week2.json` and count pruned entries.
   - *Cost:* ~3 CPU‑seconds/run, additional ~10 KB log.

3. **Week 3 – HOT‑Hit Promotion**
   - *Change:* Track `hot_hits = flagged_hot / total_hits`; promote handles with `hot_hits > 0.15` to priority queue.
   - *Proof‑meter:* Record `"hot_hits": 0.xx` in `/board/metrics/week3.json` and list promoted handles.
   - *Cost:* ~4 CPU‑seconds/run, ~15 KB metrics.

4. **Week 4 – Operator Confirmation Gate**
   - *Change:* Require explicit operator approval for any handle addition/removal that impacts the `kit` file; generate proposal `/board/proposals/handle_update_<date>.md`.
   - *Proof‑meter:* Store `"operator_approved": true/false` in `/board/metrics/week4.json`.
   - *Cost:* Minimal extra CPU; human time for approval.

These four findings constitute the default self‑tuning ladder for the harvest system.
