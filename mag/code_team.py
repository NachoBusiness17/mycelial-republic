"""code_team — dedicated coding lane from organs we already have.

Schema: mag_code_team.v1
Law: Mag owns the chain. Models are interchangeable. Grok is scarce judgment,
not a code mill. Hermes is a tool-loop seat, never the router, never residual.
GLM Coding Plan (Lite first) is an optional Hermes brain when GLM_API_KEY exists;
it is not Mag's default provider (coding-plan TOS is supported tools only).

Compose, do not throne:
  L0  qwen2.5-coder:7b     local files (Continue twin, sequential VRAM)
  L1  deepseek agent       multi-file / pytest when local insufficient
  L2  hermes               tool loop (zai/GLM Lite if key, else local custom)
  L2  cursor               IDE surface (cursor_bridge / launch_cursor_seat)
  L2  grok                 [priority] architecture only
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

SCHEMA = "mag_code_team.v1"

_CODE = re.compile(
    r"\b("
    r"code|coding|refactor|pytest|implement|patch|fix (the )?(bug|test)|"
    r"typecheck|lint|pr\b|pull request|vscode|copilot|cursor|hermes"
    r")\b",
    re.I,
)
_FRONTIER = re.compile(
    r"\b(architecture|invariant|verkle|doctrine|moonshot|promote)\b", re.I
)


def _glm_key() -> bool:
    if os.environ.get("GLM_API_KEY"):
        return True
    env = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / ".env"
    if env.is_file():
        try:
            t = env.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return False
        for line in t.splitlines():
            s = line.strip()
            if s.startswith("GLM_API_KEY=") and len(s) > 12:
                return True
    return False


def hermes_brain() -> dict[str, Any]:
    if _glm_key():
        return {
            "provider": "zai",
            "model": "glm-5.2",
            "base_url": "https://api.z.ai/api/coding/paas/v4",
            "plan": "lite",
            "note": "GLM Coding Plan on Hermes only — not Mag janitor, not lantern",
        }
    return {
        "provider": "custom",
        "model": "gemma4-hermes",
        "base_url": "http://127.0.0.1:11434/v1",
        "plan": "local",
        "note": "no GLM_API_KEY — Hermes stays on local custom until Lite key exists",
    }


def pick(goal: str) -> dict[str, Any]:
    g = (goal or "").strip()
    brain = hermes_brain()
    if _FRONTIER.search(g) and not _CODE.search(g):
        seat = "grok"
        why = "architecture/doctrine — scarce grok, not the code mill"
    elif _CODE.search(g) and re.search(r"\b(multi[- ]?file|refactor|pytest|implement)\b", g, re.I):
        seat = "deepseek_agent"
        why = "multi-file/exec — DeepSeek agent before grok; Hermes if tools needed"
    elif _CODE.search(g):
        seat = "local_coder"
        why = "cheap code — qwen2.5-coder:7b sequential, one model hot"
    else:
        seat = "local_coder"
        why = "default code-team cheap; escalate only on failure"
    return {
        "ok": True,
        "schema": SCHEMA,
        "goal": g[:240],
        "seat": seat,
        "why": why,
        "hermes_brain": brain,
        "team": [
            "local_coder:qwen2.5-coder:7b",
            "deepseek_agent",
            "hermes_tools",
            "cursor_ide",
            "grok_priority_only",
        ],
        "never": ["janitor cadence", "lantern/game", "roundtable default", "private residual on Hermes"],
    }


def status() -> dict[str, Any]:
    from harness.hermes_cli import hermes_status

    hs = hermes_status()
    return {
        "ok": True,
        "schema": SCHEMA,
        "hermes_available": bool(hs.get("available")),
        "hermes_brain": hermes_brain(),
        "glm_key": _glm_key(),
        "note": "dedicated code team is a lane, not a purchase",
    }
