# filing.law (kernel section 5, extracted 2026-09-27T04:39:02Z)

Handoff procedure (memories/session/next-window-handoff.md):
5. **FILE before close:** durable writes to `watch/inbox/` + register event in `index_events.jsonl`; checkpoint commit; `python main.py state-snapshot` if session was heavy.

Standing law lines:
- Residual on disk is truth; chat is heat. Append events, never rewrite the INDEX fold.

Shared surface: durable writes land on watch/inbox/ with a receipt + INDEX register (watch/inbox/SHARED_SURFACE_CONTRACT.json, pointer row).
