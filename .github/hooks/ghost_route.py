#!/usr/bin/env python3
"""Ghost routing hook — PreToolUse.

Denies ad-hoc `python main.py X` framework calls in the terminal so work routes
through the module/REST/queue path instead. Everything else continues.

Reads the PreToolUse JSON from stdin; writes the decision JSON to stdout.
"""
import json
import re
import sys


def _is_blocked_tool(tool_name: str) -> bool:
    return (tool_name or "").lower() in {
        "run_in_terminal",
        "terminal",
        "shell",
        "execute",
    }


def _is_main_py_call(cmd: str) -> bool:
    """True when the command invokes python/py on main.py (framework anti-pattern)."""
    if not cmd:
        return False
    # python main.py / py main.py / .venv\Scripts\python.exe main.py
    return bool(
        re.search(
            r"(?:python|pythonw|py)(?:\.exe)?(?:\s+[\w.\\/:\-]+)*(?:\s+)(?:\./|\.\\)?main\.py\b",
            cmd,
            re.IGNORECASE,
        )
    )


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        # If we can't parse, do not block.
        print(json.dumps({"continue": True}))
        return 0

    tool = data.get("toolName", "")
    tool_input = data.get("toolInput", {}) or {}
    # command may be nested under toolInput.command or a top-level 'command'
    cmd = tool_input.get("command") or data.get("command") or ""

    if _is_blocked_tool(tool) and _is_main_py_call(cmd):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            "Route through ghost: use `mag.<module>` / REST `/api/v1` / the "
                            "queue, not `python main.py X`. See copilot-instructions.md."
                        ),
                    }
                }
            )
        )
        return 0

    print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
