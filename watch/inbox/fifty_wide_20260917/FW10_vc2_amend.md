# FW-10 — VC2_CHAIN_STATE amendment: 15 "dead paths" → 1 rotated backup, 14 truncation phantoms (2026-09-28)

- Ask: the VC2_CHAIN_STATE receipt's 15 dead state/ + memory/biography paths — append a
  correction row, never rewrite.
- Original left byte-identical. Correction row appended at
  `watch/inbox/wave_20260916/receipts/VC2_CHAIN_STATE.md` (after its footer, under a
  `## CORRECTION ROW — 2026-09-28 (FW-10...)` header).
- Evidence (all run this session):
  - The receipt cites `.jsonl` everywhere (e.g. `memory/trajectory/steps.jsonl` line 41,
    `state/art_queue.jsonl` line 87, `state/fuel/lite_pacing.jsonl` line 26); the census's
    dead list showed `.json` — the old `_REF_RE` alternation `json|jsonl` truncated every
    `*.jsonl` ref to `*.json` (same leftmost-first defect as FW-07's `md|mdx`). Fixed in
    `mag/prose_census.py` (jsonl now precedes json), fix comment cites this receipt.
  - Re-audit of the receipt with the fixed instrument: 30 refs total, **1 dead** (was 15):
    `memory/biography_backup/biography_backup_20260916/verkle_chain.jsonl` — the daily backup
    dir rotated away (oldest surviving dir today: `biography_backup_20260921`, newest
    `biography_backup_20260928`; `ls memory/biography_backup/`). True at write time (the
    receipt's own line 73 saw it 09-16), gone by the designed rotation — not a loss.
  - All seven named ledgers exist as `.jsonl` today (ls output in session):
    memory/biography/verkle_chain.jsonl, memory/trajectory/steps.jsonl, state/art_queue.jsonl,
    state/capacity_ladder.jsonl, state/decisions_done.jsonl, state/fuel/lite_pacing.jsonl,
    state/fuel/lite_quota_log.jsonl.
- Net: VC2's chain-state audit needed no correction of substance — its paths were live when
  written and mostly still are; the census finding was instrument error, and the one real
  absence is routine backup rotation.
