# AA4 — Estate doctor after the night burn (2026-09-30)

Operator: AA4 seat (ZCode), venv `.venv/Scripts/python.exe`. Five checks, one pass, four RED-tinged. Numbers below are byte-read from the commands, not hand-copied.

## 1. mag.cmd doctor — DEGRADED (exit 0, `ok: false`, `status: degraded`)

- Integral heartbeat: **alive** — age 4.2s, pid 13, status `mag_loop`, watch ok (5.0s interval), catch_up ok, "Integral process is up."
- BUT `pid_alive: false` and `up: false` while `port_8765`, `board_api`, `port_8000`, `backend_api` all true. Cause: pid 13 is a container-namespace PID (mag-sovereign cage) not visible from the host venv; the heartbeat file + all four ports prove the service is up. The doctor's host-side pid probe is what reads dead.
- `missing_while_down: ["integral Mag process (watch+companion heartbeat)"]` — same phantom, listed even while heartbeat is alive.
- Lanes: L0_ollama ok (18 models incl. gemma:2b, gemma4, qwen2.5:32b), L1_openrouter ok/configured, L2_grok ok (CLI on PATH).
- Recording: live_stale=false (live age 4.7s), digest_age 19,642s (~5.5h), dossier/visual/brief all present. Active session `01a0f0b6-…` last hook `stop` at 05:09Z.

## 2. Census (`pytest --collect-only -q`) — 3,211 collected, 1 ERROR (collection interrupted)

- `ERROR tests/test_behavioral_awareness.py` — SyntaxError line 70: unresolved git merge conflict marker `<<<<<<< Updated upstream` baked into the file. This is real tree damage from a conflicted merge, not a flaky collect. Count matches the ~3,200 expectation but the error blocks both census completeness and any full run until the conflict is resolved.

## 3. Shared-surface validate — `ok: false`

- 9 hash mismatches vs INDEX.json: `DESK_DSV41FLASH_20260911.md`, `frontier_olm_20260928/sweep/quantization-compression-reddit.md`, `frontier_olm_20260928/sweep/agent-memory-continuity-x.md`, `TASK_WALL_REPORT_20260923.md`, `STEALTH_SWEEP_LATEST.md`, `wave5_repair/suite-burn.md`, `STEALTH_MINED_FINDINGS.jsonl`, `PACK_OFFLOAD.jsonl`, `gala_20260925/wave5-repair/lanes/suite-burn.json`.
- Warning: 37 unindexed inbox files (W1–W3 receipts, luncheon watchlists, STEER.md, TIE_IT_ALL_20260930.md, etc.).
- Mitigating context: the gate canary's own WARN observed live sibling-lane writes to `PACK_OFFLOAD.jsonl` / `index_events.jsonl` during the run — at least one mismatch is an actively-mutating file, not tamper.

## 4. Gate canary (`tools/gate_canary.py`) — 9/10 ALIVE, refold_gate DEAD

- ALIVE: violation_ratchet (NEW violation in changed tools/ file), config_seal (fired at HEAD), secret_gate (fake ghp_ token), census_drift_patrol, freshness_gate, checkbox_receipt_gate, description_pin, caption_ledger_verify, workflow_gate_scenarios (red-card enforcing).
- **DEAD: refold_gate** — rc=2 SILENT on its known-bad (B2-279 tier-swap fold mutation); should fire WARN, fired nothing. Canary already filed the attention alert.
- Canary also WARNed real-tree movement during run (expected, sibling lanes) and snapshotted 41,802 tracked paths.

## 5. Violation ratchet (`check --changed`) — PASS

- scope=1 changed file; hits=0; registered=0; NEW=0; expired-exceptions=0; rc=0.

## Triage order

1. `tests/test_behavioral_awareness.py` line 70 merge conflict — blocks the census law and any full pytest run.
2. refold_gate DEAD — repair or retire per B2-279 contract; alert is in memory/attention.md.
3. 9 index hash mismatches — re-hash via the sanctioned writer after confirming no lane holds the file open; index the 37 orphans.
4. Doctor phantom-pid — the container-namespace pid probe reads dead from host; heartbeat+ports are the truth.
