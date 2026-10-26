# garden-v1-A1-haiku45-B2 (anthropic/claude-haiku-4.5 @ nous, turn 1, channel: content)

IMPROVEMENT 1: _GRANTED_EVENT_IDS persists only in memory; restart loses replay protection, allowing same event_id to authorize twice | EVIDENCE: mag/switchboard_v2.py:142-144 | FIX: Load and persist _GRANTED_EVENT_IDS to a durable file (e.g. .jsonl) on every add and at startup.

IMPROVEMENT 2: confirm() revalidates authority but does not re-check TTL expiry before advancing DEFERRED to AUTHORIZED, allowing a proposal to authorize after its ttl_seconds has elapsed | EVIDENCE: mag/switchboard_v2.py:339-371 | FIX: Add policy_engine.check_ttl(rec, pol) call before verdict validation at line 355 and deny if expired.

IMPROVEMENT 3: write_board_note() computes budget_remaining incorrectly when budget_consumed=True, dividing strings instead of ints | EVIDENCE: mag/switchboard_v2.py:447-451 | FIX: Cast used.get(effect, 0) and max_calls to int before arithmetic: remaining = int(budget.get("max_calls", 3)) - int(used.get(effect, 0)).

DIFFERENT-BUILD: Replace in-memory _GRANTED_EVENT_IDS and file-based inbox with a single append-only event log (decisions.jsonl) indexed by event_id. Replay protection, confirmation state, and audit trail would share one durable source, eliminating sync bugs between separate files and reducing restart-loss surface.
