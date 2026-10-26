"""Seat law gate - PreToolUse hook enforcing the seat's own laws at the tool path.

Cause (2026-09-29, operator: "I keep fucking watching you ignore laws"): the
seat ran bare python on PATH all night (the exact misresolution class that
broke stealth_driver's selffeed), authored receipts without the dash scan, and
amended a workflow script twice without the gate. Self-audit caught them only
when run - and the field verdict (watch/inbox/burn_reset_20260927/flash50/
stealth-sw-10.md) is that agents cannot self-police. So the law moves into the
tool path, where skipping it is not an option.

Enforced:
  1. Bash invoking bare python/python3 (no path prefix, not pythonw) -> exit 2.
     Law: AGENTS.md python env - never bare python on PATH (Hermes).
  2. Write/Edit whose payload targets watch/inbox/ and carries an em-dash or
     en-dash -> exit 2. Law: the no-em-dash AI-tell rule.
  3. Write of a *.dwf.ts workflow script -> the payload is gated through
     tools/workflow_gate.py BEFORE the write lands. Cause: the seat amended a
     workflow script twice without ever running the gate; "no harness hook
     exists on AmendWorkflow" is not a reason to hand the law to the human -
     the submit-time artifact (the script content) is hookable, so it is.
     Gate PASS on the payload = allow; FAIL = exit 2 with the failing gate
     names. Partial Edits to .dwf.ts files cannot be gated pre-hoc (payload
     carries only new_string) - the companion PostToolUse entry runs the gate
     on the whole file after every such edit and surfaces the verdict.

Fail-open by design: a broken gate must never block the fleet - any internal
error exits 0 (house rule, same as scripts/hooks/prebuild_gate.py).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BARE_PY = re.compile(r"(?:^|[;&|(]\s*|&&\s*|\|\|?\s*)python(?:3)?(?:\.exe)?(?=\s|$)")
DASHES = re.compile(r"[\u2013\u2014]")
VENV_PY = str(Path(__file__).resolve().parent.parent / ".venv" / "Scripts" / "python.exe")
GATE = str(Path(__file__).resolve().parent / "workflow_gate.py")
HOOK = "seat_law_gate"


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


def gate_workflow_content(content: str):
    """Gate a workflow script payload. Returns None (pass) or a fail string."""
    tmp = Path(tempfile.gettempdir()) / f"seatlaw_{os.getpid()}.dwf.ts"
    try:
        tmp.write_text(content, encoding="utf-8")
        flags = os.CREATE_NO_WINDOW if hasattr(os, "CREATE_NO_WINDOW") else 0
        r = subprocess.run(
            [VENV_PY, GATE, "check", "--script", str(tmp), "--no-register"],
            capture_output=True, text=True, timeout=60,
            creationflags=flags,
        )
        if r.returncode == 2:
            lines = [ln.strip() for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
            fails = [ln for ln in lines if ln.startswith("FAIL") or "FAIL" in ln[:20]][:4]
            return "workflow gate RED on payload: " + (" | ".join(fails) or f"exit 2 ({r.returncode})")
        return None
    except Exception:
        return None  # fail-open: gate machinery broken -> do not block
    finally:
        try:
            tmp.unlink()
        except Exception:
            pass


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0
    tool = str(data.get("tool_name", ""))
    ti = data.get("tool_input", {}) or {}
    try:
        if tool == "Bash":
            cmd = str(ti.get("command", ""))
            if ".venv" not in cmd and "pythonw" not in cmd and BARE_PY.search(cmd):
                sys.stderr.write(
                    "SEAT LAW (AGENTS.md python env): bare python on PATH is "
                    "forbidden (Hermes resolution class). Use "
                    ".venv/Scripts/python.exe or mag.cmd.\n")
                _lawlog("python-env", tool, "", "bare python on PATH")
                return 2
        if tool in ("Write", "Edit"):
            path = str(ti.get("file_path", "")).replace("\\", "/")
            if "watch/inbox" in path:
                body = str(ti.get("content", "") or ti.get("new_string", ""))
                if DASHES.search(body):
                    # Only newly-introduced dashes block: re-saving a file that
                    # already carries historical dashes (quoted sources, older
                    # house prose) is lawful; writing new ones is not. An Edit
                    # fragment is always new ink; a full Write is judged against
                    # the file on disk.
                    if tool == "Edit":
                        introduced = True
                    else:
                        try:
                            old = Path(path).read_text(encoding="utf-8", errors="replace")
                        except Exception:
                            old = ""
                        introduced = (len(DASHES.findall(body))
                                      > len(DASHES.findall(old)))
                    if introduced:
                        sys.stderr.write(
                            "SEAT LAW (no-em-dash): authored watch/inbox content "
                            "introduces an em/en-dash. Use plain hyphens.\n")
                        _lawlog("no-em-dash", tool, path, "watch/inbox payload introduces em/en-dash")
                        return 2
            if tool == "Write" and path.endswith(".dwf.ts"):
                fail = gate_workflow_content(str(ti.get("content", "")))
                if fail:
                    sys.stderr.write("SEAT LAW (workflow gate): " + fail + "\n")
                    _lawlog("workflow-gate", tool, path, fail)
                    return 2
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
