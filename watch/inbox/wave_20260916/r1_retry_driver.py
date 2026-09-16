"""R1 wave_20260916 — bounded retry round for the myco battery (pass 2 of the same machinery).

Only unanswered qids; winner lanes only; free lanes only. Same OUT/RAW redirection as pass 1.
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
WAVE = ROOT / "watch" / "inbox" / "wave_20260916"
sys.path.insert(0, str(ROOT))

from mag import research_fanout as rf  # noqa: E402

rf.OUT = WAVE / "r1_fanout_runs"
rf.RAW = rf.OUT / "raw.jsonl"
rf.PACK = rf.OUT / "pack.md"

# CRITICAL: re-patch BATTERY in this fresh process. Load the myco battery from the
# pass-1 output (single source of truth) so retry only targets failed myco qids.
_prev = json.loads((WAVE / "r1_swarm_research_out.json").read_text(encoding="utf-8"))
rf.BATTERY = [(b["id"], b["theme"], b["q"]) for b in _prev["battery"]]

summary = rf.retry(workers=4, attempts=2, timeout=150, backoff=4.0)
print("PASS2 answered:", summary.get("answered"), "failed:", summary.get("failed"),
      "answered_this_pass:", summary.get("answered_this_pass"), flush=True)
print("failures:", json.dumps(summary.get("failures")), flush=True)
