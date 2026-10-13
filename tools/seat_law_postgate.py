"""Seat law post-gate - PostToolUse hook: gate .dwf.ts files after partial Edits.

Companion to tools/seat_law_gate.py rule 3: a full Write of a workflow script
is gated BEFORE it lands, but an Edit payload carries only new_string, so the
resulting file can only be judged after the fact. This hook runs
tools/workflow_gate.py on every edited .dwf.ts file and prints the verdict
loudly into the seat's tool feedback, so a RED gate is impossible to miss
before the next AmendWorkflow. PostToolUse cannot block; it witnesses.

Fail-open: any internal error exits 0 (a broken gate never blocks the fleet).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

VENV_PY = str(Path(__file__).resolve().parent.parent / ".venv" / "Scripts" / "python.exe")
GATE = str(Path(__file__).resolve().parent / "workflow_gate.py")
HOOK = "seat_law_postgate"


def _lawlog(law: str, tool: str, path: str, reason: str) -> bool:
    """Append one block row to memory/runs/lawlog.jsonl via tools/lawlog.py.

    Never raises; never logs the command text or payload (no secrets ride the log).
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import lawlog
        return lawlog.record(law, tool, path, reason, hook=HOOK)
    except Exception:
        return False


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0
    ti = data.get("tool_input", {}) or {}
    try:
        path = str(ti.get("file_path", "")).replace("\\", "/")
        if data.get("tool_name") != "Edit" or not path.endswith(".dwf.ts"):
            return 0
        if not Path(path).exists():
            return 0
        flags = os.CREATE_NO_WINDOW if hasattr(os, "CREATE_NO_WINDOW") else 0
        r = subprocess.run(
            [VENV_PY, GATE, "check", "--script", path],
            capture_output=True, text=True, timeout=60, creationflags=flags,
        )
        if r.returncode == 2:
            lines = [ln.strip() for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
            fails = [ln for ln in lines if "FAIL" in ln[:20]][:4]
            sys.stderr.write(
                "SEAT LAW POST-GATE RED on " + path + ": "
                + (" | ".join(fails) or f"exit 2") + " - fix before any AmendWorkflow.\n")
            _lawlog("workflow-gate-post", "Edit", path, "post-edit gate RED (witness): " + " | ".join(fails))
            return 2
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
