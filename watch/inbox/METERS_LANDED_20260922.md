# METERS LANDED — the dogfood wiring is live · 2026-09-22

_The "self steal" GO: the wiring bill from DOGFOOD_OPERATING_ENVIRONMENT_20260922.md,
executed in bytes, not prose. The meters are now the default cockpit._

## What changed (files, all receipted)

1. **`mag/session_state_brief.py`** — every seat's boot brief now carries a
   **METERS block**: Γ per organ with DELIVERING ticks, the no-prose list, curvature
   (saddle count / β0 / descent vote), and the dumb floor (meters stale >24h = RED,
   no readings = DARK). The brief is generated at SessionStart by the sancho boot hook,
   so home PC, tablet/MagRemote, and every remote seat get the cockpit with zero new
   surfaces. Verified: `--dry` render shows the block with tonight's readings.
2. **`mag/peer_handoff.py`** — handoffs now carry the entanglement check: `claimed` /
   `delivered` / `receiver_can_act_on` (writer fields, CLI flags, formatter lines).
   All three empty = unmetered handoff (Γ=1.00 by default). Existing handoffs
   unaffected (fields default empty).
3. **`tools/meters_nightly.py`** (new) — the cron-ready unit: runs both meters, then
   appends register events for every output (the seal-the-cron lesson, encoded).
   Smoke-tested end to end: both meters ok, 3 files sealed.

## Receipts

- Wrapper run: `[meters] sealed 3: ESTATE_SMITH_CHART_20260922.json,
  CATHEDRAL_CURVATURE_SCAN_20260922.json, CATHEDRAL_CURVATURE_SCAN_20260922.png`
- Brief METERS block (01:54Z): Γ supervisor=1.00 · flash_lane_zai3=0.62 ·
  deepseek=0.00 ✓ · ollama=0.93 · queue=0.00 ✓ · day_work=0.88 · handoffs=1.00 ·
  checkpoint_apply=1.00 — 5/6 saddle · β0 wired=3 · descent vote: water-first · floor ok.
- The seal loop closed: the wrapper's own register events are what keep the audit CLEAN
  after unattended runs.

## What is still owed (small, honest)

- **One schedule line:** point the estate's daily task (e.g. MagImproveDaily) at
  `tools/meters_nightly.py` — operator-side, one edit in the scheduler.
- **Fleet Lyapunov V** stays a candidate until its bar is named (GO list, unchanged).
- The 12 existing pending handoffs predate the entanglement fields; they stay
  unmetered (Γ=1.00) until their senders backfill or re-file.
- No checkpoint commit made this window — code changes are on disk; fold into the
  window-close commit per standing procedure.

---
_Filed by the ZCode seat, 2026-09-22 ~01:55Z. Lineage: curvature worlds + estate smith
chart (09-21) → render the system (09-22) → dogfood map (09-22) → this landing. The
fleet now boots into its own instruments._
