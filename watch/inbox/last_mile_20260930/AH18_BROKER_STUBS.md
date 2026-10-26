# AH18 — effect_broker model_call + lane_spawn de-stub (2026-09-29)

Seat: AH18 (ZCode), venv `.venv/Scripts/python.exe`. Audit §3.5
(`watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md`): `mag/effect_broker.py`
claims "every side effect routes through me" while `_broker_model_call` and
`_broker_lane_spawn` returned `ok=True stub=True` — fake passes. Mission:
make them REAL-but-narrow (authorize + meter + dispatch to the existing
owner; DISPATCH-EXTERNAL only if the delegate is too entangled).

## Delegates found (read-first, per mission)

- Provider layer: `models/providers.py::chat_provider(provider_id, system,
  user, *, model, max_tokens, tier, session_id, timeout, allow_peak) ->`
  `{ok, text, provider, model, usage{prompt_tokens, completion_tokens},
  budget_after}`. (The task brief's `models.providers.chat_provider` path is
  this module — there is no `models/providers/` package.) It already runs the
  quota gate, key failover, degenerate-output and empty-reasoning honesty.
- Lane spawner: `mag/seat_dispatch.py::task(goal, *, seat, model, tag)` —
  owns HEADLESS subprocess launchers + MAILBOX inbox writes + orchestrator
  register/finalize. Clean callable, no entanglement forcing
  DISPATCH-EXTERNAL: both effects got a REAL dispatch (option 2, not 3).

## Changes (mag/effect_broker.py)

- `_broker_model_call`: params `provider` (required), `user` (required
  non-empty), `system`, `model`, `max_tokens` (broker narrows default to
  2048; the provider layer's own default is the 65k ceiling), `tier`
  (default `T2` — a brokered model_call is by definition an
  explicitly-authorized remote-capable effect; free_local/ollama lanes are
  unaffected by the tier gate), `session_id` (defaults
  `broker:<corr_id>` so quota rows correlate), `timeout`, `allow_peak`,
  and the budget field **`max_cost_usd`**.
  Flow: authority gate (execute) → pre-call worst-case cost gate →
  `chat_provider` → metered effect row. Post-call actual cost from real
  usage tokens; if actual crosses the cap the receipt stays COMPLETED with
  `budget_exceeded_post: True` flagged (the call already happened — a
  denial there would misreport a completed effect).
- Cost rate: single conservative ceiling `USD_PER_MTOK` (default 15.0,
  env `MAG_MODEL_USD_PER_MTOK`). The estate has NO per-model price table
  (models/quota.py meters tokens; its only dollar figure is the DeepSeek
  cache comment $0.14/M miss vs $0.0028/M hit); inventing per-model prices
  would fabricate precision. One blended rate over-estimates → fails
  CLOSED on the pre-call gate and keeps the ledger internally consistent.
- `_broker_lane_spawn`: params `task` (goal, required non-empty), `seat`
  (default `auto` → offerings.route), `model`, `tag` (defaults
  `broker-<corr_id>`). Delegates to `mag.seat_dispatch.task`; MAILBOX
  `queued` status counts as dispatched; a failed dispatch returns
  `ok=False` and meters NO row (receipts carry the failure trail).
- `_append_effect_row` + `EFFECTS_LOG_NAME`: append-only meter
  `memory/runs/effect_broker/effects.jsonl`, one JSON line per dispatched
  effect: `{ts, effect, corr_id, model/provider or seat/task_id, tokens,
  cost_usd, estimated_cost_usd}`. Lives under `RECEIPTS_DIR` so tests (and
  any future redirection) move ledger and receipts together.
- `_postcondition_evidence` for both effects now carries real evidence
  (delegate ref, tokens/cost/corr_id, task_id/status) instead of
  `{"stub": True}`. Module docstring names both delegates (spec travels
  with the behavior).

## Tests (tests/test_effect_broker_ah18.py — 7 tests, all monkeypatch the
delegate so no live provider/subprocess is spent; broker path is real)

1. unauthorized model_call → authority-gate FAILED receipt, delegate never
   called, no meter row; same for lane_spawn.
2. authorized model_call → delegate called with broker defaults (tier T2,
   `broker:<corr_id>` session), receipt COMPLETED, effect row on
   effects.jsonl with model/tokens/cost/corr_id.
3. budget exceeded (`max_cost_usd` 1e-6 vs ~$0.03 worst case) → denied
   PRE-CALL, delegate never called, no meter row.
4. authorized lane_spawn → seat_dispatch.task delegated (goal/seat/tag),
   row logged with seat/task_id/goal_head; failed dispatch → FAILED
   receipt, no row.

## Evidence

- `pytest tests/test_effect_broker_ah18.py tests/test_effect_broker_fix.py -q`
  → 12 passed (7 new + 5 AG3 regression).
- Neighborhood `pytest tests/ -q -k "effect_broker or switchboard or policy"`
  → 44 passed, 3248 deselected.
- Broker self-test `.venv/Scripts/python.exe -m mag.effect_broker test` →
  5/5 passed.

## Honest boundaries

- Cost metering is token-count × one blended ceiling, not per-model USD
  truth; the pre-call gate is worst-case (chars/4 + full max_tokens), so it
  denies some calls that would have come in under the cap — fail-closed by
  design.
- No live provider/subprocess was spent proving the delegates (monkeypatched
  in tests); the delegation seams are the same lazy-import pattern
  `_broker_board_write` already uses with switchboard_v2.
