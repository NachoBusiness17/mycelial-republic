"""opencode_coder — the GLM Coding Plan backchannel: headless coder via the opencode CLI.

WHY THIS EXISTS (2026-08-26): the operator is taking the GLM Coding Plan (z.ai) at Pro.
opencode (1.18.23) is already configured with the `zai` provider pointing at the coding-plan
endpoint (https://api.z.ai/api/coding/paas/v4, models glm-5.3 / glm-4.7, key from env
ZAI_API_KEY). The plan's fence: quota works ONLY inside supported tools — and opencode IS a
supported tool. Driving `opencode run` headlessly is the COMPLIANT door (pointing our own
API harness at the key would violate the plan's usage policy and risk account freezing).

Pattern (mirrors grok_build_coder / glm_coder, the LLM-last doctrine):
  1. FROZEN context = the warm cache rib (mag.rib_cache.FROZEN_RIB) as the leading block —
     same prefix every call = cache mining (the plan rewards cache hits: 95-98% = top of the
     token allowance).
  2. `opencode run -m zai/glm-5.3 --format json "<task>"` — headless; parse the JSON events
     for the assistant's text. --session carries the reasoning ledger (continuation).
  3. Deterministic wrapper wins: optionally write the extracted output to write_to and run
     verify_cmd (cmd.exe syntax — same convention as the other backchannels).
  4. FAIL-CLOSED: refuses without the opencode binary and without ZAI_API_KEY; never logs
     secrets.

CLI: python -m harness.opencode_coder [goal] --write-to <path> --verify-cmd "<cmd>"
     [--model zai/glm-5.3] [--session <id>]
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import ROOT

_DEFAULT_MODEL = "zai/glm-5.3"
_DEFAULT_TIMEOUT = 45  # elder 2026-08-28: Max 45s hard; 126s handshake was a miss
_HANDSHAKE = (
    "what would you like me to do",
    "how can i help",
    "how can i assist",
    "ready to help",
    "want me to",
)


def is_handshake_noop(text: str) -> bool:
    """Max 4.7 ack-only: treat as miss, do not retry Max (elder flywheel)."""
    t = (text or "").strip().lower()
    if not t or len(t) > 280:
        return False
    return any(h in t for h in _HANDSHAKE)


def _read_env() -> dict[str, str]:
    """Load ZAI_API_KEY (+ ZAI_API_KEY_2 for the sd/Max second account) from .env
    (never printed). Returns the env delta to pass to the child."""
    env = dict(os.environ)
    env_file = ROOT / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            for name in ("ZAI_API_KEY", "ZAI_API_KEY_2"):
                if s.startswith(f"{name}=") and name not in env:
                    env[name] = s.split("=", 1)[1].strip().strip('"').strip("'")
    return env


def find_opencode() -> str | None:
    """Locate the opencode CLI (the operator's authenticated session)."""
    env = os.environ.get("OPENCODE_BIN")
    if env and Path(env).is_file():
        return env
    which = shutil.which("opencode")
    if which:
        return which
    return None


def harness_available() -> dict[str, bool]:
    """Readiness, honestly: tool present? keys present? (no secrets)."""
    env = _read_env()
    return {"opencode_cli": find_opencode() is not None,
            "zai_key": bool(env.get("ZAI_API_KEY")),
            "zai_key_2": bool(env.get("ZAI_API_KEY_2"))}


def code_ask(
    *,
    goal: str,
    context: str = "",
    model: str = _DEFAULT_MODEL,
    cwd: Path | None = None,
    timeout: int = _DEFAULT_TIMEOUT,
    write_to: str | None = None,
    verify_cmd: str | None = None,
    session_id: str | None = None,
    rib_first: bool = False,
) -> dict[str, Any]:
    """Run ONE headless coding task through the opencode CLI (the GLM Coding Plan door).

    FROZEN_RIB leads the message by default (cache mining); `rib_first=False` puts the TASK
    first and the rib as trailing STANDING CONTEXT — GLM-5.3 reads the rib as a contract
    handshake and waits for the task, so task-first is its register (measured 2026-08-26).
    `session_id` continues a prior session (the reasoning ledger; the prefix persists = cache).
    Deterministic wrapper wins (state-first, LLM-last).
    """
    bin_path = find_opencode()
    if not bin_path:
        return {"ok": False, "error": "opencode CLI not found"}
    env = _read_env()
    if not env.get("ZAI_API_KEY"):
        return {"ok": False, "error": "ZAI_API_KEY not set (subscribe to GLM Coding Plan + add "
                                       "ZAI_API_KEY to .env)"}

    try:
        from mag.rib_cache import FROZEN_RIB
        rib = FROZEN_RIB
    except Exception:  # noqa: BLE001
        rib = ""

    if rib and rib_first:
        msg = (rib + "\n\n" + (context + "\n\n" if context else "") + goal).strip()
    elif rib:
        msg = (goal + "\n\n" + (context + "\n\n" if context else "")
               + "STANDING CONTEXT (reference only):\n" + rib).strip()
    else:
        msg = (goal + ("\n\n" + context if context else "")).strip()

    cmd = [bin_path, "run", "--format", "json", "-m", model]
    if session_id:
        cmd += ["--session", session_id]
    cmd.append(msg)

    t0 = datetime.now(timezone.utc)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              env=env, cwd=str(cwd or ROOT), encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout after {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)[:200]}

    dt = (datetime.now(timezone.utc) - t0).total_seconds()

    # Parse the JSON event stream: `text` events carry the assistant's output (part.text);
    # `step_finish` carries cost + token telemetry (cache read/write — the cache-mine measure).
    # The first `sessionID` seen is returned so the caller can continue the SAME session on the
    # next call — the prefix persists across calls = the cache-mine payoff on this surface.
    parts: list[str] = []
    telemetry: dict[str, Any] = {}
    got_session: str | None = None
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(ev, dict):
            continue
        if not got_session:
            got_session = ev.get("sessionID") or None
        etype = ev.get("type")
        part = ev.get("part") or {}
        if etype == "text":
            text = part.get("text") or ""
            if text:
                parts.append(str(text))
        elif etype == "step_finish":
            telemetry = {"tokens": part.get("tokens") or {}, "cost": part.get("cost")}
    output = "\n".join(parts).strip()

    if not output and proc.returncode != 0:
        return {"ok": False, "error": f"opencode exit {proc.returncode}: "
                                      f"{(proc.stderr or '')[:300]}", "seconds": round(dt, 1)}
    if is_handshake_noop(output):
        return {"ok": False, "error": "handshake_noop: command, don't handshake",
                "output": output[:400], "seconds": round(dt, 1),
                "session_id": got_session, "telemetry": telemetry,
                "burst_hint": "deepseek"}

    # Deterministic wrapper: persist + verify if asked.
    verified = None
    if write_to and output:
        out_path = Path(write_to)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        if verify_cmd:
            v = subprocess.run(verify_cmd, shell=True, capture_output=True, text=True,
                               cwd=str(cwd or ROOT), timeout=120)
            verified = {"code": v.returncode, "out": (v.stdout or "")[:400],
                        "err": (v.stderr or "")[:200]}

    return {"ok": True, "model": model, "output": output[:6000],
            "chars": len(output), "seconds": round(dt, 1),
            "telemetry": telemetry, "session_id": got_session,
            "wrote": write_to if write_to and output else None,
            "verified": verified, "exit": proc.returncode}


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="opencode_coder")
    ap.add_argument("goal", nargs="?", default="", help="the coding task")
    ap.add_argument("--context", default="", help="extra context block")
    ap.add_argument("--model", default=_DEFAULT_MODEL)
    ap.add_argument("--write-to", default=None)
    ap.add_argument("--verify-cmd", default=None)
    ap.add_argument("--session", default=None, help="continue a session (reasoning ledger)")
    ap.add_argument("--ready", action="store_true", help="readiness check only")
    a = ap.parse_args()

    if a.ready:
        print(json.dumps(harness_available(), indent=2))
        return 0
    if not a.goal:
        print("goal required (or use --ready)")
        return 1

    r = code_ask(goal=a.goal, context=a.context, model=a.model, write_to=a.write_to,
                 verify_cmd=a.verify_cmd, session_id=a.session)
    print(json.dumps({k: v for k, v in r.items() if k != "output"}, indent=2, default=str))
    if r.get("output"):
        print("\n--- OUTPUT (first 2000) ---")
        print(r["output"][:2000])
    if r.get("verified"):
        print("\n--- VERIFY ---")
        print(r["verified"])
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
