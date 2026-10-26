# swarm1-kimi-scripts__handoff_escalation_watcher (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: _write_result truncates deliverable to 20000 chars silently losing data | EVIDENCE: scripts/handoff_escalation_watcher.py:140 | FIX: stream large deliverables to separate file with reference, or raise when truncation would occur

DEFECT 2: _ingest uses errors="replace" corrupting non-UTF8 output silently | EVIDENCE: scripts/handoff_escalation_watcher.py:147 | FIX: use errors="backslashreplace" and log replacement events, or capture raw bytes

DEFECT 3: _ollama_chat hardcodes 8192 context without model-aware limits | EVIDENCE: scripts/handoff_escalation_watcher.py:78 | FIX: read model card or env OLLAMA_ESCALATE_CONTEXT, warn if prompt exceeds 80% of limit

DEAD-CODE: "HTTP-Referer" header in _cloud_chat uses hardcoded localhost URL | EVIDENCE: scripts/handoff_escalation_watcher.py:108

ONE-SITTING FIX: Add timeout and retry with exponential backoff for _ollama_chat | EVIDENCE: scripts/handoff_escalation_watcher.py:56-86
