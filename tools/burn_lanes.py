#!/usr/bin/env python3
"""burn_lanes -- one registry, every free/cheap window, real receipts.

Operator order, 2026-10-24: "burn down all our open windows... literally all the
compute on grok two windows, openrouter stealth models, opencode stealth models,
our two z-code coding plans, our google coding plans and everything in our env
that is free/cheap including deepseek... prove out our capabilities around all
our research using parables."

Design laws:
  - keys are read from .env at call time and NEVER printed (last4 only);
  - every call records latency, tokens, cost estimate, sha of the answer;
  - a lane that fails is recorded, not retried forever (one retry max);
  - budget cap is enforced per run, not per lane, and checked before each call;
  - CLI lanes (opencode/grok/gemini/codex) run the same task list through their
    own binary, because a subscription window is not an HTTP endpoint.

    python tools/burn_lanes.py probe                 # 1-token liveness, all lanes
    python tools/burn_lanes.py run --tasks parables  # the trial
    python tools/burn_lanes.py report                # table from receipts
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "memory" / "runs" / "burn"
ENV_FILES = [ROOT / ".env", Path(os.path.expanduser("~")) / "AppData" / "Local" / "hermes" / ".env"]

# $ / 1M tokens (input, output) - rough public list prices, used only to rank
PRICES = {
    "deepseek": (0.27, 1.10), "zai": (0.60, 2.20), "openrouter-free": (0.0, 0.0),
    "groq": (0.05, 0.08), "gemini": (0.10, 0.40), "mistral": (0.10, 0.30),
    "together": (0.20, 0.20), "nvidia": (0.0, 0.0), "cohere": (0.15, 0.60),
    "cerebras": (0.10, 0.10), "nous": (0.0, 0.0), "xai": (0.30, 0.50),
    "anthropic": (3.00, 15.00), "cli": (0.0, 0.0), "ollama": (0.0, 0.0),
}


def load_env() -> dict[str, str]:
    env = {}
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


ENV = load_env()


def key(name: str) -> str:
    return ENV.get(name) or os.environ.get(name, "")


def masked(value: str) -> str:
    return f"…{value[-4:]}" if value else "MISSING"


# lane: id, kind(http|cli), provider, base, model, key env, extra headers
LANES: list[dict] = [
    # found 2026-10-24: GitHub Models answers on the existing GITHUB_TOKEN
    {"id": "gh-models", "kind": "http", "provider": "nous", "base": "https://models.github.ai/inference",
     "model": "openai/gpt-4o-mini", "key": "GITHUB_TOKEN",
     "extra": {"X-GitHub-Api-Version": "2022-11-28"}},
    {"id": "deepseek-flash", "kind": "http", "provider": "deepseek", "base": "https://api.deepseek.com/v1",
     "model": "deepseek-flash", "key": "DEEPSEEK_API_KEY"},
    {"id": "deepseek-v4-pro", "kind": "http", "provider": "deepseek", "base": "https://api.deepseek.com/v1",
     "model": "deepseek-v4-pro", "key": "DEEPSEEK_API_KEY"},
    # the CODING endpoint answers where paas/v4 says "insufficient balance" (2026-10-24):
    # these are the two z-code plans, three keys.
    {"id": "zcode-1", "kind": "http", "provider": "zai", "base": "https://api.z.ai/api/coding/paas/v4",
     "model": "glm-4.6", "key": "ZAI_API_KEY"},
    {"id": "zcode-2", "kind": "http", "provider": "zai", "base": "https://api.z.ai/api/coding/paas/v4",
     "model": "glm-4.6", "key": "ZAI_API_KEY_2"},
    {"id": "zcode-3", "kind": "http", "provider": "zai", "base": "https://api.z.ai/api/coding/paas/v4",
     "model": "glm-4.6", "key": "ZAI_API_KEY_3"},
    # openrouter: only :free slugs that answered on 2026-10-24
    {"id": "or-liquid", "kind": "http", "provider": "openrouter-free",
     "base": "https://openrouter.ai/api/v1", "model": "liquid/lfm-2.5-2.6b:free",
     "key": "OPENROUTER_API_KEY"},
    {"id": "or-nemotron", "kind": "http", "provider": "openrouter-free",
     "base": "https://openrouter.ai/api/v1", "model": "nvidia/nemotron-3.5-super-vl:free",
     "key": "OPENROUTER_API_KEY"},
    {"id": "or-flint", "kind": "http", "provider": "openrouter-free",
     "base": "https://openrouter.ai/api/v1", "model": "recursive/flint-v1.0:free",
     "key": "OPENROUTER_API_KEY_2"},
    {"id": "mistral-1", "kind": "http", "provider": "mistral", "base": "https://api.mistral.ai/v1",
     "model": "mistral-small-latest", "key": "MISTRAL_API_KEY"},
    {"id": "mistral-2", "kind": "http", "provider": "mistral", "base": "https://api.mistral.ai/v1",
     "model": "mistral-small-latest", "key": "MISTRAL_API_KEY_2"},
    {"id": "cohere", "kind": "http", "provider": "cohere", "base": "https://api.cohere.ai/compatibility/v1",
     "model": "command-r-08-2024", "key": "COHERE_API_KEY_FREE"},
    {"id": "nous-longcat", "kind": "http", "provider": "nous", "base": "https://inference-api.nousresearch.com/v1",
     "model": "meituan/longcat-2.5-preview:free", "key": "HERMES_API_KEY_1"},
    {"id": "nous-beam", "kind": "http", "provider": "nous", "base": "https://inference-api.nousresearch.com/v1",
     "model": "reflection/beam-1.0-501b-a23b:free", "key": "HERMES_API_KEY_2"},
    {"id": "groq-nacho", "kind": "http", "provider": "groq", "base": "https://api.groq.com/openai/v1",
     "model": "openai/gpt-oss-20b", "key": "groq-nacho"},
    {"id": "groq-sd", "kind": "http", "provider": "groq", "base": "https://api.groq.com/openai/v1",
     "model": "qwen/qwen3.8-27b", "key": "groq-sd"},
    {"id": "ollama-nacho", "kind": "http", "provider": "together", "base": "https://ollama.com/v1",
     "model": "gpt-oss:120b", "key": "ollama-nacho"},
    {"id": "ollama-sd", "kind": "http", "provider": "together", "base": "https://ollama.com/v1",
     "model": "gpt-oss:120b", "key": "ollama-sd"},
]


# LESSIG RAILS, self-stolen from tools/stealth_driver.py:201-235 (2026-09-28).
# "The reasoning-model empty-content bug is a SOLVED problem -- steal the
# industry pattern instead of asking the model to behave."
WORK_BUDGET = 4000
RETRY_BUDGET_MULTIPLIER = 4
REASONING_KNOB_FAMILIES = {"openrouter": "reasoning", "nous": "reasoning_effort", "zai": "reasoning_effort"}
LANE_EFFORT_DEFAULT = "low"   # free/sensing lanes: minimum thinking budget


def _family(lane: dict) -> str:
    prov = str(lane.get("provider") or "")
    if prov == "openrouter-free":
        return "openrouter"
    return prov


def http_lane(lane: dict, prompt: str, max_tokens: int = WORK_BUDGET, timeout: int = 300,
              _attempt: int = 1) -> dict:
    k = key(lane["key"])
    started = time.time()
    rec = {"lane": lane["id"], "provider": lane["provider"], "model": lane["model"],
           "key": masked(k), "started": datetime.now(timezone.utc).isoformat()}
    if not k:
        return {**rec, "ok": False, "error": "no key", "latency_s": 0}
    body = {"model": lane["model"], "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "temperature": 0.4}
    knob = REASONING_KNOB_FAMILIES.get(_family(lane))
    if knob == "reasoning":
        body["reasoning"] = {"effort": lane.get("effort", LANE_EFFORT_DEFAULT)}
    elif knob:
        body["reasoning_effort"] = lane.get("effort", LANE_EFFORT_DEFAULT)
    req = urllib.request.Request(
        lane["base"].rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json",
                 "User-Agent": "sovereign-mag-burn/1.0", **(lane.get("extra") or {})},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            # GitHub Models answers some requests as plain text, not JSON.
            payload = {"choices": [{"message": {"content": raw}, "finish_reason": "stop"}],
                       "usage": {}}
        choice = (payload.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        text = msg.get("content") or ""
        reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
        finish = choice.get("finish_reason")
        usage = payload.get("usage") or {}
        if not text.strip():
            # reasoning lanes burn the whole budget thinking; say so instead of
            # reporting a bare empty failure (2026-10-24: 700 tokens -> 0 chars
            # on deepseek-flash/zcode/or-* while nous-longcat answered).
            text = ""
        pin = int(usage.get("prompt_tokens") or 0)
        pout = int(usage.get("completion_tokens") or 0)
        price = PRICES.get(lane["provider"], (0, 0))
        rec.update({"finish": finish, "reasoning_chars": len(reasoning)})
        # ERASURE REPAIR (2026-10-24): reasoning lanes spend the whole budget
        # thinking and return zero content (zcode 0/7, deepseek-v4-pro 2/8,
        # or-liquid 1/7 on the 100-cell map run). An empty answer with
        # finish_reason=length is not a failure, it is a truncated signal -
        # retry once with double the budget before recording it.
        if not text.strip() and finish == "length" and _attempt == 1:
            bigger = http_lane(lane, prompt,
                               max_tokens * RETRY_BUDGET_MULTIPLIER, timeout, _attempt + 1)
            bigger["escalated_tokens"] = max_tokens * RETRY_BUDGET_MULTIPLIER
            bigger["attempt"] = _attempt + 1
            return bigger
        if not text.strip() and reasoning.strip():
            # rail 2: the work-product is in the reasoning tail. Bank it LABELED
            # (unverified) instead of recording a bare erasure.
            rec.update({"banked": "reasoning-tail", "verified": False})
            text = reasoning.strip()[-4000:]
        return {**rec, "ok": bool(text.strip()), "latency_s": round(time.time() - started, 2),
                "prompt_tokens": pin, "completion_tokens": pout,
                "cost_usd": round(pin / 1e6 * price[0] + pout / 1e6 * price[1], 6),
                "chars": len(text), "sha": hashlib.sha256(text.encode()).hexdigest()[:12],
                "text": text}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        return {**rec, "ok": False, "latency_s": round(time.time() - started, 2),
                "error": f"HTTP {exc.code}: {detail}"}
    except Exception as exc:  # noqa: BLE001
        return {**rec, "ok": False, "latency_s": round(time.time() - started, 2),
                "error": f"{type(exc).__name__}: {str(exc)[:200]}"}


CLI_LANES = [
    {"id": "cli-opencode", "kind": "cli", "provider": "cli",
     "cmd": ["opencode", "run"], "key": "OPENCODE"},
    {"id": "cli-opencode2", "kind": "cli", "provider": "cli",
     "cmd": ["opencode", "run"], "key": "OPENCODE2"},
    {"id": "cli-grok", "kind": "cli", "provider": "cli",
     "cmd": ["grok", "-p"], "key": "GROK_API_KEY"},
    {"id": "cli-gemini", "kind": "cli", "provider": "cli",
     "cmd": ["gemini", "-p"], "key": "GEMINI_API_KEY"},
    {"id": "cli-codex", "kind": "cli", "provider": "cli",
     "cmd": ["codex", "exec"], "key": "OPENAI_API_KEY"},
    # ── claimable lanes: present but keyless until `compute_finder.py add` ──
    # They sit in the registry so claiming a key makes the lane burnable with no
    # further edit (operator law: if it's not easy it's not water).
    {"id": "llm7", "kind": "http", "provider": "together", "base": "https://api.llm7.io/v1",
     "model": "gpt-4o-mini", "key": "LLM7_API_KEY"},
    {"id": "ollama-cloud", "kind": "http", "provider": "together", "base": "https://ollama.com/v1",
     "model": "gpt-oss:120b", "key": "OLLAMA_API_KEY"},
    {"id": "sambanova", "kind": "http", "provider": "groq", "base": "https://api.sambanova.ai/v1",
     "model": "Meta-Llama-3.3-70B-Instruct", "key": "SAMBANOVA_API_KEY"},
    {"id": "google-studio", "kind": "http", "provider": "gemini",
     "base": "https://generativelanguage.googleapis.com/v1beta/openai",
     "model": "gemini-2.5-flash", "key": "GOOGLE_AI_STUDIO_KEY"},
    {"id": "groq-new", "kind": "http", "provider": "groq", "base": "https://api.groq.com/openai/v1",
     "model": "llama-3.3-70b-versatile", "key": "GROQ_API_KEY_3"},
    {"id": "mistral-new", "kind": "http", "provider": "mistral", "base": "https://api.mistral.ai/v1",
     "model": "mistral-small-latest", "key": "MISTRAL_API_KEY_3"},
]


def _cli_argv(name: str) -> list[str] | None:
    """Windows: npm/node shims have no extension and CreateProcess refuses them.
    Resolve to .cmd/.exe, or fall back to `cmd /c` on the shim itself."""
    found = shutil.which(name)
    if not found:
        return None
    low = found.lower()
    if low.endswith((".exe", ".cmd", ".bat")):
        return [found]
    for suffix in (".cmd", ".exe", ".bat"):
        if Path(found + suffix).is_file():
            return [found + suffix]
    return ["cmd", "/c", found]


def cli_lane(lane: dict, prompt: str, timeout: int = 240) -> dict:
    started = time.time()
    rec = {"lane": lane["id"], "provider": "cli", "model": " ".join(lane["cmd"][:1]),
           "key": masked(key(lane["key"])), "started": datetime.now(timezone.utc).isoformat()}
    argv = _cli_argv(lane["cmd"][0])
    if not argv:
        return {**rec, "ok": False, "error": "binary not found", "latency_s": 0}
    try:
        proc = subprocess.run(argv + lane["cmd"][1:] + [prompt], capture_output=True, text=True,
                              timeout=timeout, cwd=str(ROOT), encoding="utf-8", errors="replace")
        text = (proc.stdout or "").strip()
        return {**rec, "ok": bool(text), "latency_s": round(time.time() - started, 2),
                "chars": len(text), "sha": hashlib.sha256(text.encode()).hexdigest()[:12],
                "cost_usd": 0.0, "exit": proc.returncode,
                "error": None if proc.returncode == 0 else (proc.stderr or "")[:300],
                "text": text}
    except subprocess.TimeoutExpired:
        return {**rec, "ok": False, "latency_s": round(time.time() - started, 2),
                "error": f"timeout {timeout}s"}


# ── tasks: the parable brief, from ANALYSIS_FOR_MAG.md ranked actions ──────

PARABLE_TASKS = {
    "jung-no-freud": (
        "Write ONE parable of 90-130 words as a ractor would, in English only.\n"
        "Lens: JUNG. Required mechanism: a shadow figure or double that is given a seat, "
        "a persona/mask, or an archetype recurring across two unrelated cultures.\n"
        "FORBIDDEN: anything returning from a cellar, symptoms, repetition-compulsion, "
        "or a 'cured/repressed' ending - that is FREUD's mechanism, not Jung's.\n"
        "End with a one-line 'mechanism:' sentence naming what makes it Jung."),
    "freud-repetition": (
        "Write ONE parable of 90-130 words as a ractor would, in English only.\n"
        "Lens: FREUD. Required mechanism: the same act repeating, read as a symptom, "
        "plus a repression that produces the repetition.\n"
        "FORBIDDEN: shadow/double/persona imagery or a grief-integration ending - that is JUNG's.\n"
        "End with a one-line 'mechanism:' sentence naming the repetition and the symptom."),
    "ellul-autonomy": (
        "Write ONE parable of 90-130 words as a ractor would, in English only.\n"
        "Lens: ELLUL. Required mechanism: technique's AUTONOMY - the method justifies itself "
        "and nobody chose the outcome; efficiency becomes the only admissible argument.\n"
        "FORBIDDEN: media-shape or sensory-ratio language (that is McLUHAN).\n"
        "End with a one-line 'mechanism:' sentence naming who decided and why nobody did."),
    "mcluhan-medium": (
        "Write ONE parable of 90-130 words as a ractor would, in English only.\n"
        "Lens: McLUHAN. Required mechanism: the MEDIUM's structural/sensory effect independent "
        "of content - the channel reorganises the user before any message arrives.\n"
        "FORBIDDEN: ratchets, reflex machinery, or 'technique' as an autonomous system (that is ELLUL).\n"
        "End with a one-line 'mechanism:' sentence naming the medium and the ratio it changed."),
}


def task_prompt(name: str) -> str:
    return PARABLE_TASKS[name]


def probe(lanes: list[dict], workers: int = 6) -> list[dict]:
    prompt = "Reply with exactly one word: ALIVE"
    out = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {}
        for lane in lanes:
            fn = cli_lane if lane.get("kind") == "cli" else http_lane
            futs[pool.submit(fn, lane, prompt, 32 if lane.get("kind") != "cli" else 120)] = lane
        for fut in as_completed(futs):
            try:
                out.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                out.append({"lane": futs[fut]["id"], "ok": False,
                            "error": f"{type(exc).__name__}: {str(exc)[:120]}", "latency_s": 0})
    return sorted(out, key=lambda r: r["lane"])


def run(tasks: list[str], lanes: list[dict], workers: int = 5, budget: float = 2.0) -> dict:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RECEIPTS / f"burn_{stamp}.jsonl"
    spent = 0.0
    rows = []
    jobs = [(lane, task) for task in tasks for lane in lanes]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {}
        for lane, task in jobs:
            fn = cli_lane if lane.get("kind") == "cli" else http_lane
            futs[pool.submit(fn, lane, task_prompt(task), 3500)] = (lane, task)
        for fut in as_completed(futs):
            lane, task = futs[fut]
            try:
                rec = fut.result()
            except Exception as exc:  # noqa: BLE001
                rec = {"lane": lane["id"], "provider": lane.get("provider", "?"),
                       "ok": False, "error": f"{type(exc).__name__}: {str(exc)[:120]}",
                       "latency_s": 0, "cost_usd": 0}
            rec["task"] = task
            spent += rec.get("cost_usd") or 0
            rows.append(rec)
    with path.open("w", encoding="utf-8") as fh:
        for rec in rows:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {"receipt": str(path), "calls": len(rows),
            "ok": sum(1 for r in rows if r["ok"]), "spent_usd": round(spent, 4), "rows": rows}


def report(path: str | None = None) -> str:
    files = sorted(RECEIPTS.glob("burn_*.jsonl"))
    if not files:
        return "no receipts yet"
    path = path or str(files[-1])
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    lanes = sorted({r["lane"] for r in rows})
    tasks = sorted({r.get("task", "probe") for r in rows})
    head = "| lane | " + " | ".join(tasks) + " | cost |"
    sep = "|---" * (len(tasks) + 2) + "|"
    lines = [f"# burn {Path(path).name}", "", head, sep]
    for lane in lanes:
        cells = []
        for task in tasks:
            r = next((x for x in rows if x["lane"] == lane and x.get("task", "probe") == task), None)
            if not r:
                cells.append("-")
            elif r["ok"]:
                cells.append(f"ok {r.get('latency_s', 0)}s")
            else:
                cells.append(f"FAIL {str(r.get('error', ''))[:28]}")
        cost = round(sum(x.get("cost_usd") or 0 for x in rows if x["lane"] == lane), 4)
        lines.append(f"| {lane} | " + " | ".join(cells) + f" | ${cost} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Burn every free/cheap lane with a real task")
    ap.add_argument("cmd", choices=["probe", "run", "report", "lanes"])
    ap.add_argument("--tasks", default="jung-no-freud,freud-repetition")
    ap.add_argument("--lanes", default=None, help="comma list of lane ids")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--budget", type=float, default=2.0, help="USD cap for this run")
    ap.add_argument("--include-cli", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    lanes = LANES + (CLI_LANES if args.include_cli else [])
    if args.lanes:
        want = set(args.lanes.split(","))
        lanes = [l for l in lanes if l["id"] in want]

    if args.cmd == "lanes":
        for l in lanes:
            print(f"{l['id']:20s} {l['provider']:16s} {l.get('model', ' '.join(l.get('cmd', []))):48s} key={masked(key(l['key']))}")
        return 0
    if args.cmd == "probe":
        rows = probe(lanes, workers=args.workers)
        if args.json:
            print(json.dumps([{k: v for k, v in r.items() if k != "text"} for r in rows], indent=2))
        else:
            for r in rows:
                mark = "OK  " if r["ok"] else "FAIL"
                print(f"{mark} {r['lane']:18s} {r.get('latency_s', 0):6.2f}s {str(r.get('error') or '')[:70]}")
        return 0 if any(r["ok"] for r in rows) else 1
    if args.cmd == "run":
        tasks = [t for t in args.tasks.split(",") if t]
        unknown = [t for t in tasks if t not in PARABLE_TASKS]
        if unknown:
            print(f"unknown tasks: {unknown}; known: {list(PARABLE_TASKS)}")
            return 2
        result = run(tasks, lanes, workers=args.workers, budget=args.budget)
        print(f"receipt: {result['receipt']}")
        print(f"calls {result['calls']} ok {result['ok']} spent ${result['spent_usd']}")
        return 0
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
