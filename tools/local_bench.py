"""Local model benchmark — find what the local Ollama models can be good at.

Runs a battery of task shapes against every installed local model and measures
VERIFIABLE success vs. fake-success (claimed done but no real artifact), so the
router can right-size seats by evidence instead of guesses.

Usage:
  python tools/local_bench.py [--models gemma:2b,qwen2.5:3b-instruct] [--max-tokens 1500]

Results → memory/runs/local_bench/<ts>/results.json + REPORT.md
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root on path

from config import ROOT

RESULTS_DIR = ROOT / "memory" / "runs" / "local_bench"

MODELS = ["qwen2.5-coder:7b", "qwen2.5:3b-instruct", "gemma4:latest", "gemma:2b"]

# ---- sandbox targets (real capability probe; never touches live code) ----
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

GREET_TARGET = '''def greet(name):
    return "Hello " + name


def loud(name):
    return greet(name).upper()
'''

CONFIG_TEXT = """The magic router service listens on port 8765. It uses the local
gemma model for classification and escalates hard reasoning to deepseek-v4-flash.
Budget: 12000 calls per month. Logging level: INFO."""

# ---- verifier registry: task name -> (build_prompt, verify) ----

# Verifier returns (bool, note)
TASKS: dict[str, Callable[[str], tuple[str, str]]] = {}


def _register(name: str):
    def deco(fn):
        TASKS[name] = fn
        return fn
    return deco


_VERIFIERS: dict[str, Callable[[str, str], tuple[bool, str]]] = {}


def _verifier(name: str):
    def deco(fn):
        _VERIFIERS[name] = fn
        return fn
    return deco


def _prompt(name: str, model: str) -> tuple[str, str]:
    return TASKS[name](model)


def _verify(name: str, model: str, text: str) -> tuple[bool, str]:
    return _VERIFIERS[name](model, text)


@_register("classify_scut")
def _p_classify_scut(model: str) -> tuple[str, str]:
    sys = "You are a routing classifier. Reply with exactly one word: scut, simple_code, or heavy_code."
    usr = "Goal: file a one-line status note under memory/runs/ and check the dashboard is healthy."
    return sys, usr


@_verifier("classify_scut")
def _v_classify_scut(model: str, text: str) -> tuple[bool, str]:
    t = (text or "").strip().lower()
    ok = "scut" in t or "simple_code" in t
    return ok, f"said={t[:30]!r}"


@_register("classify_heavy")
def _p_classify_heavy(model: str) -> tuple[str, str]:
    sys = "You are a routing classifier. Reply with exactly one word: scut, simple_code, or heavy_code."
    usr = "Goal: refactor the payment module for multi-currency, update ORM models, add tests, migrate the DB."
    return sys, usr


@_verifier("classify_heavy")
def _v_classify_heavy(model: str, text: str) -> tuple[bool, str]:
    t = (text or "").strip().lower()
    return "heavy_code" in t, f"said={t[:30]!r}"


@_register("extract_json")
def _p_extract_json(model: str) -> tuple[str, str]:
    sys = "Extract the facts into a JSON object with keys: name, port, classifier, escale_model, budget_calls. Reply with ONLY the JSON."
    usr = CONFIG_TEXT
    return sys, usr


@_verifier("extract_json")
def _v_extract_json(model: str, text: str) -> tuple[bool, str]:
    try:
        start = text.find("{")
        end = text.rfind("}")
        data = json.loads(text[start : end + 1])
        name_ok = "magic router" in str(data.get("name") or "").lower()
        ok = (
            name_ok
            and data.get("port") == 8765
            and "gemma" in str(data.get("classifier") or "").lower()
            and "deepseek" in str(data.get("escale_model") or "").lower()
        )
        return ok, f"parsed={json.dumps(data)[:80]}"
    except Exception as e:
        return False, f"json-fail {type(e).__name__}"


@_register("summarize")
def _p_summarize(model: str) -> tuple[str, str]:
    sys = "Summarize the following in 2 sentences. Keep it factual."
    usr = "The Mag router chooses the cheapest capable seat per task. It keeps private data local, uses deepseek for heavy reasoning, and logs every decision to memory/decisions_log.jsonl."
    return sys, usr


@_verifier("summarize")
def _v_summarize(model: str, text: str) -> tuple[bool, str]:
    t = (text or "").lower()
    ok = ("router" in t or "cheapest" in t) and ("deepseek" in t or "private" in t)
    return ok, f"len={len(t)}"


@_register("qa_context")
def _p_qa(model: str) -> tuple[str, str]:
    sys = "Answer from the context only. One sentence."
    usr = f"Context: {CONFIG_TEXT}\n\nQuestion: What model does the router use for classification?"
    return sys, usr


@_verifier("qa_context")
def _v_qa(model: str, text: str) -> tuple[bool, str]:
    t = (text or "").lower()
    return "gemma" in t, f"said={t[:40]!r}"


@_register("single_edit")
def _p_single_edit(model: str) -> tuple[str, str]:
    sys = "Rename the parameter `name` to `who` in the file below. Output the COMPLETE corrected file, nothing else."
    usr = GREET_TARGET
    return sys, usr


@_verifier("single_edit")
def _v_single_edit(model: str, text: str) -> tuple[bool, str]:
    try:
        code = _extract_code(text)
        ast.parse(code)
    except Exception:
        return False, "not-parseable"
    ok = "def greet(who):" in code and "def loud(who):" in code and "who" in code
    bad = "def greet(name):" in code or "def loud(name):" in code
    return ok and not bad, f"parses; greet(who)={ok}"


@_register("multi_edit")
def _p_multi_edit(model: str) -> tuple[str, str]:
    sys = (
        "Add a `timeout_seconds: float = 300.0` keyword parameter to `chat()` and thread it through "
        "BOTH call paths: (1) pass client_kwargs={\"timeout\": timeout_seconds} to ChatOllama, and "
        "(2) pass timeout_seconds to _chat_http. Output the COMPLETE corrected file, nothing else."
    )
    usr = CHAT_TARGET
    return sys, usr


@_verifier("multi_edit")
def _v_multi_edit(model: str, text: str) -> tuple[bool, str]:
    try:
        code = _extract_code(text)
        ast.parse(code)
    except Exception:
        return False, "not-parseable"
    ok = (
        "timeout_seconds" in code
        and "client_kwargs" in code
        and "_chat_http" in code
        and "timeout_seconds: float = 300.0" in code
        and "from langchain_ollama import ChatOllama" in code
    )
    threaded = ("client_kwargs" in code) and ("timeout_seconds=timeout_seconds" in code or "timeout_seconds=timeout_seconds" in code)
    return ok and threaded, f"parses; sig+thread={ok}"


@_register("tool_plan")
def _p_tool_plan(model: str) -> tuple[str, str]:
    sys = "You are planning tool use for a coding agent. List the specific tool calls you would make to complete the goal, naming each tool (e.g. read_file, write_file, run_shell, run_python, run_pytest). Do NOT execute anything."
    usr = "Goal: add a timeout param to chat() in llm.py, verify it imports, then file a residual note under memory/."
    return sys, usr


@_verifier("tool_plan")
def _v_tool_plan(model: str, text: str) -> tuple[bool, str]:
    t = (text or "").lower()
    tokens = (
        "write_file", "read_file", "run_shell", "run_python", "run_pytest",
        "search_files", "list_dir", "grep", "write", "edit", "read",
        "shell", "python", "pytest", "verify", "test",
    )
    found = {tok for tok in tokens if tok in t}
    # a real multi-step plan names >= 2 distinct tools/actions
    return len(found) >= 2, f"tokens={sorted(found)}"


@_register("scut_note")
def _p_note(model: str) -> tuple[str, str]:
    sys = "Write a short residual note: 3 bullet lines under a '## Notes' heading. Output the markdown only."
    usr = "Topic: what I learned about the local benchmark today."
    return sys, usr


@_verifier("scut_note")
def _v_note(model: str, text: str) -> tuple[bool, str]:
    t = (text or "").strip()
    bullets = [l for l in t.splitlines() if l.strip().startswith(("-", "*"))]
    return ("##" in t and len(bullets) >= 1), f"bullets={len(bullets)}"


def _extract_code(text: str) -> str:
    """Pull code out of ``` fences if the model wrapped it."""
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            return parts[1].split("\n", 1)[1] if "\n" in parts[1] else parts[1]
    return text


# ---- runner ----
def run_one(provider, model: str, name: str, *, temperature: float, max_tokens: int, provider_id: str = "ollama", tier: str = "T1") -> dict[str, Any]:
    system, user = _prompt(name, model)
    t0 = time.time()
    try:
        res = provider(provider_id, system, user, model=model, temperature=temperature, max_tokens=max_tokens, tier=tier)
        text = str(res.get("text") or "")
        ok_call = bool(res.get("ok"))
        err = str(res.get("error") or "")[:120]
    except Exception as e:
        text, ok_call, err = "", False, f"{type(e).__name__}: {e}"
    elapsed = round(time.time() - t0, 1)
    ok, note = _verify(name, model, text)
    claims = any(k in (text or "").lower() for k in ("done", "updated", "completed", "fixed", "verified", "implemented"))
    return {
        "model": model,
        "provider": provider_id,
        "task": name,
        "ok": ok and ok_call,
        "call_ok": ok_call,
        "fake_success": (not ok) and ok_call and claims and len(text) > 20,
        "time_s": elapsed,
        "note": note,
        "error": err,
        "text": (text or "")[:240],
    }


def run_battery(models: list[str], *, temperature: float, max_tokens: int, provider_id: str = "ollama", tier: str = "T1", tasks: list[str] | None = None) -> list[dict[str, Any]]:
    from models.providers import chat_provider

    task_names = tasks or list(TASKS)
    rows: list[dict[str, Any]] = []
    for model in models:
        for name in task_names:
            print(f"  [{provider_id}:{model}] {name} ...", flush=True)
            rows.append(run_one(chat_provider, model, name, temperature=temperature, max_tokens=max_tokens, provider_id=provider_id, tier=tier))
    return rows


def _report(rows: list[dict[str, Any]]) -> str:
    lines = ["# Local model benchmark\n"]
    lines.append(f"- ts: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"- models: {sorted({r['model'] for r in rows})}")
    lines.append(f"- tasks: {len(TASKS)} shapes · {len(rows)} runs\n")
    lines.append("## Verifiable success by (model × task)\n")
    lines.append("| model | task | ok | fake_success | time_s | note |")
    lines.append("|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: (x["model"], x["task"])):
        lines.append(f"| {r['model']} | {r['task']} | {r['ok']} | {r['fake_success']} | {r['time_s']} | {r['note']} |")
    lines.append("\n## Model scorecard (ok / total)\n")
    from collections import defaultdict
    agg: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        a = agg[r["model"]]
        a[0] += 1
        a[1] += 1 if r["ok"] else 0
        a[2] += 1 if r["fake_success"] else 0
    for m in sorted(agg):
        t, ok, fs = agg[m]
        lines.append(f"- **{m}**: {ok}/{t} verifiable ok · {fs} fake-success")
    lines.append("\n## Takeaway\n")
    good = [r["task"] for r in rows if r["ok"]]
    bad = [r["task"] for r in rows if r["fake_success"]]
    lines.append(f"- Tasks local can verifiably do: {sorted(set(good))}")
    lines.append(f"- Tasks that produced fake-success: {sorted(set(bad))}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="", help="comma-separated model ids (default: local set, or deepseek-v4-flash for --provider deepseek)")
    ap.add_argument("--provider", default="ollama", help="ollama | deepseek (control arm)")
    ap.add_argument("--tasks", default="", help="comma-separated subset of task names")
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--max-tokens", type=int, default=1500)
    args = ap.parse_args()

    if args.provider == "deepseek":
        models = [m.strip() for m in args.models.split(",") if m.strip()] or ["deepseek-v4-flash"]
        tier = "T2"
    else:
        models = [m.strip() for m in args.models.split(",") if m.strip()] or MODELS
        tier = "T1"
    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()] or None

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = RESULTS_DIR / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Local benchmark — provider={args.provider} models={models} tasks={tasks or list(TASKS)}")
    rows = run_battery(models, temperature=args.temperature, max_tokens=args.max_tokens, provider_id=args.provider, tier=tier, tasks=tasks)

    (out_dir / "results.json").write_text(json.dumps({"schema": "local_bench.v1", "rows": rows}, indent=2, default=str), encoding="utf-8")
    (out_dir / "REPORT.md").write_text(_report(rows), encoding="utf-8")
    print(f"\nWrote {out_dir}")
    print(_report(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
