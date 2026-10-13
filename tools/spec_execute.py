"""Spec-execute POC — the "frozen state → penny spec → cheap execute" loop.

Pipeline:
  1. SPEC   — deepseek-v4-flash (thinking DISABLED, ~10-15x cheaper) reads the
              task + local code state and emits a CONCRETE mechanical spec
              (exact target content + verify steps). This is the "coding advice".
  2. FREEZE — spec saved to memory/runs/spec_execute/<ts>/SPEC.md.
  3. EXECUTE — local model (qwen2.5-coder:7b) runs INSIDE the spec surface
              ("execute this spec exactly; output the complete file").
  4. VERIFY  — local output parsed + checked for required markers.

Compare against tools/local_bench.py's multi_edit (vague task → local fakes it)
to see whether a cheap flash spec makes the lesser model succeed.

Usage:
  python tools/spec_execute.py --task "add timeout_seconds to chat() and thread both paths"
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root

from config import ROOT

SPEC_MODEL = "deepseek-v4-flash"   # cheap no-reasoning
EXEC_MODEL = "qwen2.5-coder:7b"    # lesser model inside the surface
OUT_DIR = ROOT / "memory" / "runs" / "spec_execute"

# Sandbox target: same shape the bench tested WITHOUT a spec (multi_edit).
CHAT_TARGET = '''def chat(role, system, user, temperature=0.2, *, strict=True):
    model = require_model(role, strict=strict) if strict else model_for(role)
    base = _resolve_base()
    try:
        try:
            from langchain_ollama import ChatOllama
            llm = ChatOllama(model=model, temperature=temperature, base_url=base)
            messages = [("system", system), ("human", user)]
            resp = llm.invoke(messages)
            text = str(resp.content)
        except ImportError:
            text = _chat_http(base, model, system, user, temperature)
        return text
    except Exception as e:
        raise
'''

REQUIRED = ["timeout_seconds", "client_kwargs", "_chat_http", "timeout_seconds=timeout_seconds"]


def call_provider(provider_id: str, system: str, user: str, model: str, *, max_tokens: int) -> dict[str, Any]:
    from models.providers import chat_provider

    tier = "T2" if provider_id == "deepseek" else "T1"
    return chat_provider(provider_id, system, user, model=model, temperature=0.1, max_tokens=max_tokens, tier=tier)


def generate_spec(task: str, code_state: str, *, max_tokens: int) -> dict[str, Any]:
    """Cheap no-reasoning DeepSeek emits a mechanical spec from local state."""
    system = (
        "You are a spec writer. From the TASK and CURRENT CODE below, emit a CONCRETE, "
        "mechanical spec the executor can follow without any judgment:\n"
        "1. EXACT final file content (complete, no ellipses, no placeholders).\n"
        "2. VERIFY: the command or checks that prove it worked.\n"
        "Do NOT explain, justify, or add commentary. Output only the spec."
    )
    user = f"TASK:\n{task}\n\nCURRENT CODE:\n```python\n{code_state}\n```"
    t0 = time.time()
    res = call_provider("deepseek", system, user, SPEC_MODEL, max_tokens=max_tokens)
    return {**res, "time_s": round(time.time() - t0, 1)}


def execute_spec(spec_text: str, *, max_tokens: int) -> dict[str, Any]:
    """Lesser (local) model executes INSIDE the provided surface."""
    system = (
        "You are an exact executor. Apply the spec below. Output ONLY the complete final "
        "file content the spec asks for. Do not narrate, do not add commentary, do not "
        "invent anything beyond the spec."
    )
    user = f"SPEC:\n{spec_text}"
    t0 = time.time()
    res = call_provider("ollama", system, user, EXEC_MODEL, max_tokens=max_tokens)
    return {**res, "time_s": round(time.time() - t0, 1)}


def extract_code(text: str) -> str:
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            body = parts[1]
            if "\n" in body:
                body = body.split("\n", 1)[1]
            return body
    return text


def verify(spec_text: str, output: str) -> tuple[bool, str]:
    code = extract_code(output)
    try:
        ast.parse(code)
        parses = True
    except Exception as e:
        parses = False
        return False, f"not-parseable: {type(e).__name__}"
    missing = [m for m in REQUIRED if m not in code]
    ok = parses and not missing
    return ok, f"parses={parses} missing={missing if missing else 'none'}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="Add a timeout_seconds: float = 300.0 keyword parameter to chat() and thread it through BOTH call paths: pass client_kwargs={'timeout': timeout_seconds} to ChatOllama and pass timeout_seconds to _chat_http.")
    ap.add_argument("--spec-max-tokens", type=int, default=1200)
    ap.add_argument("--exec-max-tokens", type=int, default=1600)
    args = ap.parse_args()

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUT_DIR / ts
    out.mkdir(parents=True, exist_ok=True)

    print(f"SPEC  ({SPEC_MODEL}, thinking off) → local code state …", flush=True)
    spec = generate_spec(args.task, CHAT_TARGET, max_tokens=args.spec_max_tokens)
    spec_text = str(spec.get("text") or "")
    (out / "SPEC.md").write_text(spec_text, encoding="utf-8")
    print(f"  spec ok={spec.get('ok')} time={spec['time_s']}s chars={len(spec_text)}")
    if not spec.get("ok"):
        print("  spec error:", str(spec.get("error"))[:200])
        return 1

    print(f"EXEC  ({EXEC_MODEL}) inside the spec surface …", flush=True)
    ex = execute_spec(spec_text, max_tokens=args.exec_max_tokens)
    output = str(ex.get("text") or "")
    (out / "OUTPUT.py").write_text(output, encoding="utf-8")
    print(f"  exec ok={ex.get('ok')} time={ex['time_s']}s chars={len(output)}")

    ok, note = verify(spec_text, output)
    row = {
        "schema": "spec_execute.v1",
        "ts": ts,
        "task": args.task[:120],
        "spec_model": SPEC_MODEL,
        "exec_model": EXEC_MODEL,
        "spec_ok": spec.get("ok"),
        "spec_time_s": spec["time_s"],
        "spec_chars": len(spec_text),
        "exec_ok": ex.get("ok"),
        "exec_time_s": ex["time_s"],
        "verify_ok": ok,
        "verify_note": note,
    }
    (out / "result.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
    print(json.dumps(row, indent=2))
    print(f"\nWrote {out}")
    return 0 if (ok and spec.get("ok")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
