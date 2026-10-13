"""GLM Coding lane — headless coder via a SUPPORTED coding tool (Claude Code CLI).

WHY THIS EXISTS (2026-08-24): the operator got GLM Coding Lite (starts 2026-08-25). The plan
is STRICTLY limited to officially supported tools (Claude Code, Cline, Roo, Kilo, OpenCode,
OpenClaw, Crush, Goose, Cursor). This harness therefore drives the Claude Code CLI
(`claude -p`, headless) pointed at the GLM Coding endpoint — a supported tool, compliant.

CONFIG (set by the operator — secrets NEVER pass through the model):
  GLM_CODING_API_KEY   = the Individual Coding Plan API key (z.ai/manage-apikey)
  ANTHROPIC_BASE_URL   = https://api.z.ai/api/anthropic   (Claude Code / Goose endpoint)
  ANTHROPIC_MODEL      = glm-5.3 | glm-5-turbo | glm-4.7   (default glm-5.3)

FAIL-CLOSED: if the key or the claude binary is missing, code_ask returns ok=False with a
clear reason. It never guesses, never fires into the wrong pool, never logs the key.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import RESULTS_DIR, ROOT

CODING_BASE_URL = "https://api.z.ai/api/anthropic"
SUPPORTED_MODELS = ("glm-5.3", "glm-5-turbo", "glm-4.7")
DEFAULT_MODEL = "glm-5.3"


def find_claude() -> str | None:
    """Locate the Claude Code CLI binary (a supported GLM Coding tool)."""
    env = os.environ.get("CLAUDE_BIN")
    if env and Path(env).is_file():
        return env
    which = shutil.which("claude")
    if which:
        return which
    return None


def coding_key() -> str:
    """Coding Plan key. VERIFIED 2026-08-25: the existing ZAI_API_KEY works on both coding
    endpoints (api/coding/paas/v4 + api/anthropic returned 200 with glm-4.7). GLM_CODING_API_KEY
    (if ever set) wins; ZAI_API_KEY is the working fallback. Loads .env first (the keys live
    there, not in the bare terminal environment)."""
    try:
        from models.env_load import load_dotenv
        load_dotenv()
    except Exception:  # noqa: BLE001
        pass
    return (os.environ.get("GLM_CODING_API_KEY", "").strip()
            or os.environ.get("ZAI_API_KEY", "").strip())


def harness_available() -> dict[str, bool]:
    """Readiness, honestly: tool present? key present? (never the key itself)."""
    return {
        "claude_cli": find_claude() is not None,
        "glm_coding_key": bool(coding_key()),
    }


def code_ask(
    *,
    goal: str,
    context: str = "",
    cwd: Path | None = None,
    model: str = DEFAULT_MODEL,
    timeout: int = 900,
    write_to: str | None = None,
    verify_cmd: str | None = None,
) -> dict[str, Any]:
    """Run ONE headless coding task through the supported tool at the GLM coding endpoint.

    LLM-LAST pattern (2026-08-25): the model RETURNS the file content in ONE fenced code
    block; the harness extracts it, writes it to write_to, and runs verify_cmd if given.
    (The first attempt relied on claude's agentic file tools; the GLM endpoint narrated
    instead of calling them. Deterministic wrapper wins.)

    Cache-mining discipline: stable byte-identical instruction block (frozen prefix) up
    front, only the task riding at the end.
    """
    claude = find_claude()
    if not claude:
        return {"ok": False, "error": "claude CLI not found — install a supported tool "
                                      "(npm i -g @anthropic-ai/claude-code) for the coding lane"}
    if not coding_key():
        return {"ok": False, "error": "no coding key — set GLM_CODING_API_KEY or ZAI_API_KEY "
                                      "in .env (ZAI_API_KEY verified working 2026-08-25)"}
    if model not in SUPPORTED_MODELS:
        return {"ok": False, "error": f"unsupported model {model!r} — must be one of "
                                      f"{SUPPORTED_MODELS}"}

    cwd = cwd or ROOT
    # FROZEN SELF = the stable system prompt, byte-identical every call (cache mining).
    # claude -p injects its default Claude Code system prompt by default — that makes the
    # model narrate about the repo instead of coding (observed 2026-08-25). We REPLACE it
    # with the strict coding-lane contract via --system-prompt.
    system = (
        "You are the coding lane of Sovereign Mag. You write real, working code.\n"
        "You have NO file tools. You do NOT write files. You return code; the harness writes it.\n"
        "Rules:\n"
        "1. Do NOT greet. Do NOT ask questions. Do NOT describe the project. Do NOT narrate.\n"
        "2. Begin your response with ```python IMMEDIATELY. The first characters of your response "
        "must be the fence. Nothing before it.\n"
        "3. Return the COMPLETE file content in that ONE fenced code block, then close it.\n"
        "4. Nothing after the closing fence. No SUMMARY. No prose.\n"
        "5. Concrete, idiomatic, minimal. Match the codebase's existing style.\n"
        "6. If blocked, return a fenced block containing only: # BLOCKED: <reason>.\n"
    )
    task = goal
    if write_to:
        task += f"\n\nOUTPUT FILE: {write_to}"
    if context:
        task += f"\n\nCONTEXT:\n{context[:12000]}"

    env = dict(os.environ)
    env["ANTHROPIC_BASE_URL"] = CODING_BASE_URL
    env["ANTHROPIC_AUTH_TOKEN"] = coding_key()
    env["ANTHROPIC_MODEL"] = model
    env.setdefault("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "1")
    env.setdefault("CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WARNINGS", "1")

    cmd = [claude, "-p", task, "--output-format", "json", "--system-prompt", system]
    t0 = datetime.now(timezone.utc)
    try:
        p = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout after {timeout}s", "model": model}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}", "model": model}

    ms = int((datetime.now(timezone.utc) - t0).total_seconds() * 1000)
    text = (p.stdout or "").strip()
    # claude -p --output-format json returns {type:result, result, ...}
    try:
        parsed = json.loads(text)
        body = (parsed.get("result") or "").strip() if isinstance(parsed, dict) else text
    except Exception:  # noqa: BLE001
        body = text

    rec = {"schema": "glm_coder.v1", "ts": t0.isoformat(), "ok": p.returncode == 0,
           "model": model, "latency_ms": ms, "exit_code": p.returncode,
           "body_head": body[:400], "stderr": (p.stderr or "")[:400]}

    # LLM-last: extract the LAST fenced code block (models often put a prose intro first,
    # then the code — observed 2026-08-25), write it, verify it.
    if write_to:
        blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", body, re.DOTALL)
        code = blocks[-1].strip() if blocks else (body or "").strip()
        target = (cwd / write_to) if not Path(write_to).is_absolute() else Path(write_to)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(code, encoding="utf-8")
            rec["file_written"] = str(target)
            rec["code_chars"] = len(code)
        except Exception as e:  # noqa: BLE001
            rec["write_error"] = f"{type(e).__name__}: {str(e)[:200]}"
        if verify_cmd and rec.get("file_written"):
            try:
                vp = subprocess.run(verify_cmd, cwd=str(cwd), capture_output=True,
                                    text=True, timeout=120, shell=True)
                rec["verify"] = {"ok": vp.returncode == 0, "exit_code": vp.returncode,
                                 "stdout": (vp.stdout or "")[:400],
                                 "stderr": (vp.stderr or "")[:200]}
            except Exception as e:  # noqa: BLE001
                rec["verify"] = {"ok": False, "error": str(e)[:150]}

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fname = f"glm_coder_{t0.strftime('%Y%m%dT%H%M%S%f')}.json"
    (RESULTS_DIR / fname).write_text(json.dumps(rec, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
    rec["result_file"] = str(RESULTS_DIR / fname)
    return rec


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="glm-coder")
    ap.add_argument("goal", nargs="?", help="the coding task (omit for readiness check)")
    ap.add_argument("--model", default=DEFAULT_MODEL, choices=SUPPORTED_MODELS)
    ap.add_argument("--context", default="")
    ap.add_argument("--write-to", default="", help="relative path to write the returned code to")
    ap.add_argument("--verify-cmd", default="", help="shell command to run after writing")
    a = ap.parse_args()
    if not a.goal:
        print(json.dumps(harness_available(), indent=2))
    else:
        print(json.dumps(code_ask(goal=a.goal, context=a.context, model=a.model,
                                  write_to=a.write_to or None,
                                  verify_cmd=a.verify_cmd or None),
                         indent=2, ensure_ascii=False, default=str))
