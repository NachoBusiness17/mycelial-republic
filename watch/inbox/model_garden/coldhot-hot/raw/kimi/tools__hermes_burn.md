# coldhot-hot-kimi-tools__hermes_burn (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: _call sends HTTP requests without User-Agent header, violating SSRF defense-in-depth | EVIDENCE: tools/hermes_burn.py:94-101 | FIX: Add "User-Agent": "Mag/1.0" header to the urllib.request.Request call
DEFECT 2: _bank appends to usage.jsonl without atomic tmp+replace, risking corruption on crash | EVIDENCE: tools/hermes_burn.py:134-136 | FIX: Write to tempfile then os.replace(USAGE, USAGE) atomically
DEFECT 3: _hermes_key leaks file handle via unclosed open() iterator, exhausting FDs under load | EVIDENCE: tools/hermes_burn.py:71-79 | FIX: Wrap open() in with statement or add explicit .close()
DEAD-CODE: The docstring's "Exit: 0 all asks ok / 1 any failed / 2 usage" comment describes a 2 code that main never returns | EVIDENCE: tools/hermes_burn.py:26-28
ONE-SITTING FIX: Add atomic tmp+replace to _bank for usage.jsonl integrity | EVIDENCE: tools/hermes_burn.py:134-136
