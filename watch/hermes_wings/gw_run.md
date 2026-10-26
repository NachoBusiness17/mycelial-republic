# gateway/run.py — the gateway main loop

via cage beat ext-56e0c55f46 folded=True

Report:

**What the source does:** `gw_run.txt` is a trimmed extract of a gateway runner that manages messaging-platform adapters and their agent lifecycle. Beyond platform wiring, it focuses on "session hygiene" context compression â running compaction against live cached agents (including a spec
