"""LANE2 harness-sensitivity test (v41_paces wave, 2026-09-10).

DeepSeek's own eval says V4.1 Flash peaks in MINIMAL harnesses. Our stack IS a
minimal harness. Fire the same task through three harness weights (BARE /
MINIMAL / LOADED system prompts), two runs each, all other knobs constant.

Apparatus: models/providers.py chat_provider, provider_id="deepseek",
tier="T2". Results -> _v41_lane2_results.json (root, scratch receipt).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from models.providers import chat_provider  # noqa: E402

TASK = "Write a Python function that finds the longest palindromic substring in O(n\u00b2) time."

ARMS = {
    "A_bare": "",
    "B_minimal": "You are a helpful coding assistant.",
    "C_loaded": (
        "You are an expert senior software engineer with 20 years of experience "
        "specializing in algorithm optimization, clean code practices, and "
        "production-ready Python development. Think step by step, consider edge "
        "cases, write docstrings, include type hints, and follow PEP 8 style "
        "guidelines."
    ),
}

RUNS = 2


def fire() -> list[dict]:
    out = []
    for arm, system in ARMS.items():
        for run in range(1, RUNS + 1):
            t0 = time.perf_counter()
            r = chat_provider(
                "deepseek",
                system,
                TASK,
                tier="T2",
                max_tokens=4096,
                session_id="v41_paces_lane2",
            )
            lat = int((time.perf_counter() - t0) * 1000)
            row = {
                "arm": arm,
                "run": run,
                "ok": r.get("ok", False),
                "error": r.get("error", ""),
                "latency_ms": lat,
                "provider": r.get("provider", ""),
                "model": r.get("model", ""),
                "usage": r.get("usage", {}),
                "text": r.get("text", "") if r.get("ok") else "",
            }
            out.append(row)
            u = r.get("usage") or {}
            print(f"{arm} run{run}: ok={row['ok']} lat={lat}ms "
                  f"pt={u.get('prompt_tokens')} ct={u.get('completion_tokens')} "
                  f"err={row['error'][:80]}")
    return out


def extract_code(text: str) -> str:
    """Pull the biggest fenced python block, else the whole text."""
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    if not blocks:
        return text.strip()
    return max(blocks, key=len).strip()


def run_battery(code: str) -> dict:
    """Execute the extracted function against a palindrome battery."""
    cases = [
        ("babad", {"bab", "aba"}),
        ("cbbd", {"bb"}),
        ("a", {"a"}),
        ("ac", {"a", "c"}),
        ("", {""}),
        ("bananas", {"anana"}),
        ("forgeeksskeegfor", {"geeksskeeg"}),
        ("aaaa", {"aaaa"}),
        ("abacdfgdcaba", {"aba"}),
        ("abc", {"a", "b", "c"}),
    ]
    ns: dict = {}
    fn = None
    try:
        exec(compile(code, "<arm>", "exec"), ns)  # noqa: S102 - controlled test input
    except Exception as e:  # noqa: BLE001
        return {"compiles": False, "error": f"{type(e).__name__}: {e}"[:200]}
    import types
    for v in ns.values():
        if isinstance(v, types.FunctionType) and v.__name__ != "<lambda>":
            # prefer a function whose name mentions palindrome/longest
            if "pal" in v.__name__.lower() or "longest" in v.__name__.lower():
                fn = v
                break
            if fn is None:
                fn = v
    if fn is None:
        return {"compiles": True, "error": "no function defined"}
    fails = []
    for s, want in cases:
        try:
            got = fn(s)
        except Exception as e:  # noqa: BLE001
            fails.append(f"{s!r}: raised {type(e).__name__}: {e}"[:120])
            continue
        gotset = {got} if isinstance(got, str) else got
        if gotset not in (want,) and not (gotset & want and len(gotset) == 1):
            # accept: exact set, or single answer that is a member of the accept set
            fails.append(f"{s!r}: got {got!r}, want one of {sorted(want)}")
    # soft perf check: O(n^2) should eat n=2000 in a few seconds
    import random
    random.seed(7)
    big = "".join(random.choice("ab") for _ in range(2000))
    t0 = time.perf_counter()
    try:
        fn(big)
    except Exception as e:  # noqa: BLE001
        fails.append(f"n=2000 raised {type(e).__name__}"[:120])
    perf_s = round(time.perf_counter() - t0, 2)
    return {
        "compiles": True,
        "fn_name": fn.__name__,
        "fails": fails,
        "n2000_seconds": perf_s,
        "code_lines": len([ln for ln in code.splitlines() if ln.strip()]),
    }


def main() -> None:
    rows = fire()
    for row in rows:
        if row["ok"]:
            row["battery"] = run_battery(extract_code(row["text"]))
            b = row["battery"]
            print(f"  battery: compiles={b.get('compiles')} "
                  f"fails={len(b.get('fails', []))} "
                  f"lines={b.get('code_lines')} perf={b.get('n2000_seconds')}s")
    out = ROOT / "_v41_lane2_results.json"
    out.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
