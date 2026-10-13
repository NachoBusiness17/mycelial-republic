# Dead‑Hand Verification Guide

This document records the concrete steps the external auditor should take to confirm that the **dead_hand** watchdog behaves exactly as specified in the code.

## Prerequisites
1. Python 3.11+ (use the repository venv: `.venv\Scripts\python.exe`).
2. The repository root must be the working directory.
3. Ensure the state directory exists:
   ```bash
   mkdir -p dist_audit/nacho_business_audit_20260912T214050Z/scripts/state
   ```
4. No existing `dead_hand_state.json` or `dead_hand_witnesses.json` files should interfere; start fresh.

## Step‑by‑step verification
1. **Arm the watchdog** (required before any watch tick):
   ```bash
   python dist_audit/nacho_business_audit_20260912T214050Z/scripts/dead_hand.py \
       --arm --i-am-operator --interval-h 72
   ```
   Expected output: JSON with `{"armed": true, "interval_hours": 72}`.

2. **Create a witness** (simulate one of the required 2‑of‑3 witnesses):
   ```bash
   python .../dead_hand.py --witness alice
   ```
   Repeat with a second distinct id (e.g., `bob`).
   Verify that `state/dead_hand_witnesses.json` now contains two entries.

3. **Prepare a voice surface** to signal operator silence.
   Write a minimal `operator_pulse.json` with a timestamp older than the interval (e.g., 80 h ago):
   ```json
   {"ts": "2026-01-01T00:00:00Z"}
   ```
   Place it at `state/operator_pulse.json`.

4. **Run a dry‑run watch tick**:
   ```bash
   python .../dead_hand.py --watch --dry-run
   ```
   Expected JSON includes:
   - `"action": "DRY‑RUN would trigger (seal+hold+loud)"`
   - `"silence_hours"` > interval (72)
   - `"witnesses": {"count": 2}`

5. **Negative test – insufficient witnesses**:
   - Remove one entry from `dead_hand_witnesses.json` (leave only one).
   - Run `--watch --dry-run` again.
   - Expected `"action": "hold (witnesses below 2-of-3)"`.

6. **Negative test – silence below interval**:
   - Restore two witnesses.
   - Update `operator_pulse.json` with a recent timestamp (e.g., now).
   - Run `--watch --dry-run`.
   - Expected `"action": "hold (silence below interval)"`.

If all six checks pass, the watchdog’s logical contract is **verified**.

## Auditable artifacts
- The JSON printed by each command (captured in the audit bundle).
- The resulting state files (`dead_hand_state.json`, `dead_hand_witnesses.json`).
- The `dead_hand_verification.md` file itself, which records the procedure.

---
*Prepared for external audit by Matthew Steiniger (Reboot).*