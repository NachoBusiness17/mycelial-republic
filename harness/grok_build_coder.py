"""grok_build_coder — the Grok Build backchannel: headless coder via the grok CLI.

WHY THIS EXISTS (2026-08-25): the operator built a GLM coding backchannel (harness/glm_coder.py)
and asked for the same with grok build. Grok Build = the `grok` CLI binary (the operator's
authenticated Grok Build session), driven headless with `grok -p --output-format json`.

Pattern (mirrors glm_coder, the LLM-last doctrine):
  1. FROZEN system prompt via --system-prompt-override (byte-identical every call = cache mining),
     plus the WARM CACHE RIB (mag.grok_warm_rib) as the leading context block — same prefix every
     call, only the task rides at the end.
  2. grok returns ONE fenced code block; the harness extracts the LAST fenced block, writes it to
     write_to, and runs verify_cmd. Deterministic wrapper wins (state-first, LLM-last).
  3. FAIL-CLOSED: refuses without the grok binary; never guesses, never logs secrets.

CLI: python -m harness.grok_build_coder [goal] --write-to <path> --verify-cmd "<cmd>"
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


def find_grok() -> str | None:
    """Locate the grok build CLI binary (the operator's authenticated Grok Build session)."""
    env = os.environ.get("GROK_BIN")
    if env and Path(env).is_file():
        return env
    which = shutil.which("grok")
    if which:
        return which
    cand = Path.home() / ".grok" / "bin" / "grok.exe"
    if cand.is_file():
        return str(cand)
    return None


def harness_available() -> dict[str, bool]:
    """Readiness, honestly: tool present? warm rib present? (no secrets)."""
    warm = False
    try:
        import sys
        sys.path.insert(0, str(ROOT))
        from mag.grok_warm_rib import prefix
        warm = bool(prefix())
    except Exception:  # noqa: BLE001
        pass
    return {"grok_cli": find_grok() is not None, "warm_rib": warm}


def code_ask(
    *,
    goal: str,
    context: str = "",
    cwd: Path | None = None,
    max_turns: int = 8,
    timeout: int = 900,
    write_to: str | None = None,
    verify_cmd: str | None = None,
) -> dict[str, Any]:
    """Run ONE headless coding task through the grok build CLI.

    LLM-last: grok returns the file content in ONE fenced code block; the harness extracts the
    LAST block, writes it, runs verify_cmd. Same frozen-prefix discipline as the GLM lane.
    """
    grok = find_grok()
    if not grok:
        return {"ok": False, "error": "grok CLI not found — Grok Build backchannel unavailable"}

    cwd = cwd or ROOT
    # FROZEN system prompt = the strict coding-lane contract, byte-identical every call
    # (cache mining). Replaces grok's default agent system prompt for this lane.
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

    # WARM CACHE RIB — the frozen standing prefix rides ahead of the task (cache hit).
    warm_block = ""
    try:
        import sys
        sys.path.insert(0, str(ROOT))
        from mag.grok_warm_rib import inject as _warm_inject
        warm_block = _warm_inject("")
    except Exception:  # noqa: BLE001
        pass

    task = goal
    if write_to:
        task += f"\n\nOUTPUT FILE: {write_to}"
    if context:
        task += f"\n\nCONTEXT:\n{context[:12000]}"
    if warm_block:
        task = f"{warm_block}\n\n## TASK\n{task}"

    # --prompt-file avoids Windows arg-length/quoting issues on long tasks.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False,
                                     encoding="utf-8", dir=str(RESULTS_DIR)) as tf:
        tf.write(task)
        task_path = tf.name

    cmd = [grok, "--prompt-file", task_path, "--cwd", str(cwd),
           "--output-format", "json", "--max-turns", str(max_turns), "--no-auto-update",
           "--system-prompt-override", system]

    t0 = datetime.now(timezone.utc)
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout after {timeout}s", "lane": "grok_build"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}", "lane": "grok_build"}
    finally:
        try:
            Path(task_path).unlink(missing_ok=True)
        except OSError:
            pass

    ms = int((datetime.now(timezone.utc) - t0).total_seconds() * 1000)
    text = (p.stdout or "").strip()
    # grok --output-format json: parse defensively, find the assistant text.
    body = text
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            for k in ("result", "content", "output", "text", "message"):
                v = parsed.get(k)
                if isinstance(v, str) and v.strip():
                    body = v.strip()
                    break
                if k == "message" and isinstance(v, dict):
                    c = v.get("content")
                    if isinstance(c, str) and c.strip():
                        body = c.strip()
                        break
    except Exception:  # noqa: BLE001
        pass

    rec = {"schema": "grok_build_coder.v1", "ts": t0.isoformat(), "ok": p.returncode == 0,
           "lane": "grok_build", "latency_ms": ms, "exit_code": p.returncode,
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

    fname = f"grok_build_coder_{t0.strftime('%Y%m%dT%H%M%S%f')}.json"
    (RESULTS_DIR / fname).write_text(json.dumps(rec, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
    rec["result_file"] = str(RESULTS_DIR / fname)
    return rec


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="grok-build-coder")
    ap.add_argument("goal", nargs="?", help="the coding task (omit for readiness check)")
    ap.add_argument("--context", default="")
    ap.add_argument("--write-to", default="", help="relative path to write the returned code to")
    ap.add_argument("--verify-cmd", default="", help="shell command to run after writing")
    a = ap.parse_args()
    if not a.goal:
        print(json.dumps(harness_available(), indent=2))
    else:
        print(json.dumps(code_ask(goal=a.goal, context=a.context,
                                  write_to=a.write_to or None,
                                  verify_cmd=a.verify_cmd or None),
                         indent=2, ensure_ascii=False, default=str))
