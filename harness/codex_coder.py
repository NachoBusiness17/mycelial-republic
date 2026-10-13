"""codex_coder — the Codex backchannel: headless coder via the Codex CLI (OpenAI).

WHY THIS EXISTS (2026-08-25): the operator built a GLM coding backchannel (harness/glm_coder.py)
and asked for the same with codex. Codex = the `codex` CLI (OpenAI Codex, the operator's
authenticated CODEX_HOME), driven non-interactively with `codex exec`.

Pattern (mirrors glm_coder, the LLM-last doctrine):
  1. FROZEN instruction block leads the prompt (byte-identical every call = cache mining). Codex
     has no --system-prompt flag, so the strict coding-lane contract is the prompt's first block.
  2. codex exec runs with -s read-only: it CANNOT write the workspace, so it returns code in its
     final message (LLM-last). The harness reads that message (-o file), extracts the LAST fenced
     block, writes it to write_to, and runs verify_cmd. State-first, deterministic wrapper.
  3. FAIL-CLOSED: refuses without the codex binary; never guesses, never logs secrets.

CLI: python -m harness.codex_coder [goal] --write-to <path> --verify-cmd "<cmd>"
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import RESULTS_DIR, ROOT


def find_codex() -> str | None:
    """Locate the Codex CLI binary (.cmd on Windows — subprocess handles it like claude.cmd)."""
    env = os.environ.get("CODEX_BIN")
    if env and Path(env).is_file():
        return env
    which = shutil.which("codex")
    if which:
        return which
    return None


def harness_available() -> dict[str, bool]:
    """Readiness, honestly: tool present? (no secrets)."""
    return {"codex_cli": find_codex() is not None}


def code_ask(
    *,
    goal: str,
    context: str = "",
    cwd: Path | None = None,
    model: str | None = None,
    timeout: int = 900,
    write_to: str | None = None,
    verify_cmd: str | None = None,
) -> dict[str, Any]:
    """Run ONE headless coding task through the Codex CLI.

    LLM-last: the model returns the file content in ONE fenced code block (read-only sandbox
    forces it); the harness extracts the LAST block, writes it, runs verify_cmd.
    """
    codex = find_codex()
    if not codex:
        return {"ok": False, "error": "codex CLI not found — Codex backchannel unavailable"}

    cwd = cwd or ROOT
    # FROZEN contract = the first block of every prompt, byte-identical every call (cache
    # mining). Codex has no --system-prompt flag, so this rides at the top of the prompt.
    frozen = (
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
    prompt = f"{frozen}\n\n## TASK\n{task}"

    # Read the final message from this file (-o); LLM-last extraction happens on it.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_file = RESULTS_DIR / f"codex_coder_last_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}.txt"

    cmd = [codex, "exec", "-", "-C", str(cwd), "-s", "read-only", "--json",
           "-o", str(out_file), "--skip-git-repo-check", "--ephemeral"]
    if model:
        cmd += ["-m", model]

    t0 = datetime.now(timezone.utc)
    try:
        # Prompt via stdin ("-" reads instructions from stdin — avoids arg-length limits).
        p = subprocess.run(cmd, cwd=str(cwd), input=prompt, capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout after {timeout}s", "lane": "codex"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}", "lane": "codex"}

    ms = int((datetime.now(timezone.utc) - t0).total_seconds() * 1000)
    # The final agent message (preferred): read the -o file.
    body = ""
    if out_file.is_file():
        body = out_file.read_text(encoding="utf-8", errors="replace").strip()
    if not body:
        # Fallback: parse the JSONL events for the last assistant text.
        for line in reversed((p.stdout or "").splitlines()):
            try:
                ev = json.loads(line)
                msg = (ev.get("payload") or {}).get("message") or {}
                txt = (msg.get("content") or "")
                if isinstance(txt, list):
                    txt = "".join(c.get("text", "") for c in txt if isinstance(c, dict))
                if txt and txt.strip():
                    body = txt.strip()
                    break
            except Exception:  # noqa: BLE001
                continue

    rec = {"schema": "codex_coder.v1", "ts": t0.isoformat(), "ok": p.returncode == 0,
           "lane": "codex", "model": model, "latency_ms": ms, "exit_code": p.returncode,
           "body_head": body[:400], "stderr": (p.stderr or "")[:400]}

    # LLM-last: extract the LAST fenced code block, write it, verify it.
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

    fname = f"codex_coder_{t0.strftime('%Y%m%dT%H%M%S%f')}.json"
    (RESULTS_DIR / fname).write_text(json.dumps(rec, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
    rec["result_file"] = str(RESULTS_DIR / fname)
    return rec


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="codex-coder")
    ap.add_argument("goal", nargs="?", help="the coding task (omit for readiness check)")
    ap.add_argument("--context", default="")
    ap.add_argument("--model", default=None, help="codex model override (default: codex config)")
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
