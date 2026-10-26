# garden-x3-haiku-bare (anthropic/claude-haiku-4.5 @ nous, turn 1, channel: content)

IMPROVEMENT 1: Replay protection uses unbounded in-memory set that persists across process restarts, allowing replay attacks after service restart | EVIDENCE: mag/switchboard_v2.py:56-57 | FIX: Load _GRANTED_EVENT_IDS from trail.jsonl on startup and persist grants to trail before adding to set

IMPROVEMENT 2: Agent-source self-authorization gate rejects confirmation requests before operator confirmation gate runs, preventing operator override of agent-generated high-impact effects | EVIDENCE: mag/switchboard_v2.py:230-237 | FIX: Move agent-source self-authorization check to after operator confirmation gate so operator can explicitly authorize

IMPROVEMENT 3: Budget check in write_board_note recomputes remaining from used dict instead of calling check_budget consistently, creating divergent accounting | EVIDENCE: mag/switchboard_v2.py:579-585 | FIX: Always call policy_engine.check_budget with decrement parameter instead of manual budget arithmetic

DIFFERENT-BUILD: I would implement durable replay protection as a bounded bloom filter or hashset persisted to the trail file itself, loaded on each grant() call. The current in-memory approach loses all history on restart and creates a window where the same event_id can be granted twice. Persisting to trail ties replay protection to the audit log and survives restarts without added storage overhead.
