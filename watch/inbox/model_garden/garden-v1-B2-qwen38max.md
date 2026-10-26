# garden-v1-B2-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

IMPROVEMENT 1: Replay protection is volatile - `_GRANTED_EVENT_IDS` is a process-local set that resets to empty on every restart, so any previously-granted event_id can be replayed after a bounce | EVIDENCE: mag/switchboard_v2.py:84 | FIX: On module load, rebuild the set by scanning TRAIL for lines containing `"status": "AUTHORIZED"` and extracting their event_id fields; alternatively persist the set to a sibling file alongside TRAIL.

IMPROVEMENT 2: `confirm()` produces an AUTHORIZED decision but never records the event_id in `_GRANTED_EVENT_IDS`, so a confirmed event can be independently re-granted via `grant()` with the same event_id, bypassing replay protection entirely | EVIDENCE: mag/switchboard_v2.py:464-474 | FIX: After line 473 (`trail_append(decision)`), add `_GRANTED_EVENT_IDS.add(event_id)` mirroring the guard at line 291-292.

IMPROVEMENT 3: Top-level relative import `from . import policy_engine` crashes with `ImportError` when the module is invoked as a script (`python mag/switchboard_v2.py`), making the CLI entry point at `if __name__ == "__main__"` dead on arrival | EVIDENCE: mag/switchboard_v2.py:39 | FIX: Replace with a try/except pattern matching the one already used in `_confirm_window_open`: try relative import, fall back to `import policy_engine` (the sys.path insert at line 37 already enables this).

DIFFERENT-BUILD: Persist granted event_ids into the append-only trail itself (one field per AUTHORIZED record) and rebuild the replay set from trail on import. This eliminates the volatile-set class of bugs entirely, requires no new file, and makes the trail the single source of truth for the receipt chain - which it already claims to be.
