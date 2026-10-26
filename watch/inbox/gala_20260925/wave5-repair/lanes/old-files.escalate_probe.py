"""Before/after probe for the agents/escalate_grok.py ROOT defect (s2-17).

Patches harness.grok_cli so the harness path runs without a real Grok CLI,
then calls escalate_grok_node and prints whether the cwd=ROOT reference
resolves. Run from anywhere:
  .venv/Scripts/python.exe watch/inbox/gala_20260925/wave5-repair/lanes/old-files.escalate_probe.py

Side effects are the node's normal runtime writes: queue/handoff/<id>.json,
logs router line, CURRENT.md refresh (all gitignored).
"""
import json
import os
import sys
from pathlib import Path


def repo_root() -> Path:
    p = Path(__file__).resolve()
    while p != p.parent and not (p / "AGENTS.md").exists():
        p = p.parent
    return p


ROOT = repo_root()
sys.path.insert(0, str(ROOT))

import harness.grok_cli as grok_cli  # noqa: E402
from config import ROOT as CONFIG_ROOT  # noqa: E402

print("config.ROOT:", CONFIG_ROOT)
print("MAG_ESCALATE_HARNESS set to 1 for probe")
os.environ["MAG_ESCALATE_HARNESS"] = "1"

CALLS = []


def fake_escalate(goal, context, cwd, max_turns, handoff_id, timeout):
    CALLS.append({"cwd": str(cwd), "max_turns": max_turns, "timeout": timeout})
    return {
        "ok": True,
        "summary": "probe run (fake harness)",
        "result_path": None,
        "error": None,
        "exit_code": 0,
    }


grok_cli.harness_available = lambda: True
grok_cli.escalate_via_harness = fake_escalate

import agents.escalate_grok as eg  # noqa: E402

state = {"goal": "old-files probe", "tier": "T3", "brief": "probe brief"}
out = eg.escalate_grok_node(state)

harness = out.get("grok_harness") or {}
err = harness.get("error") or ""
print("status:", out["status"])
print("grok_harness:", json.dumps(harness, default=str))
if CALLS:
    print("cwd forwarded:", CALLS[0]["cwd"])
    print("cwd == config.ROOT:", Path(CALLS[0]["cwd"]).resolve() == CONFIG_ROOT.resolve())
if "ROOT" in err:
    print("PROBE_RESULT: NAMEERROR_SWALLOWED")
elif harness.get("ok"):
    print("PROBE_RESULT: HARNESS_PATH_EXECUTED")
else:
    print("PROBE_RESULT: HARNESS_PATH_FAILED:", err)
