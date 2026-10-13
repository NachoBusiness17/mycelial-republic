"""Tier probe — DeepSeek right-sizing A/B (assumption testing).

The operator's hypothesis: "This conversation runs on deepseek-v4-flash high;
a lower tier would give similar results. Complex design/hypothesis work should
be HIGH (pro + thinking); running/execution should be LOW (flash, thinking
off)." This harness tests that empirically on REAL task shapes instead of
trusting the assumption — and records the verdict so we adopt assumption
testing going forward.

Task shapes (both real Mag workloads):
  design — hypothesis / test-plan design  (the "should be HIGH" case)
  exec   — runnable code generation        (the "should be LOW" case)

Matrix per task: flash/off · flash/on · pro/off · pro/on  (thinking toggle).

Scoring is OBJECTIVE — no LLM judge, no self-report:
  exec   — extract code, ast-compile, run a hidden unit test → pass/fail
  design — count concrete verifiable steps + PASS-if conditions vs prose

Cost uses real DeepSeek pricing (2026-08-07, per 1M tokens):
  flash: cache-hit $0.0028 · miss $0.14 · output $0.28
  pro:   cache-hit $0.003625 · miss $0.435 · output $0.87
  (reasoning tokens billed as output; cache-hit/miss fields read from usage
   when the API returns them.)

Run:
  python tools/tier_probe.py                  # both tasks, full matrix
  python tools/tier_probe.py --task design    # one task
  python tools/tier_probe.py --json           # machine-readable
  python tools/tier_probe.py --no-live        # scoring/cost dry-run (no API)

Report: memory/runs/tier_probe/<ts>/REPORT.md
Ledger: memory/assumptions.md  ← the adopted "test the assumption" habit
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

sys.stdout.reconfigure(encoding="utf-8")  # Windows cp1252 kills →/—

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import ROOT  # noqa: E402

RUN_DIR = ROOT / "memory" / "runs" / "tier_probe"
LEDGER = ROOT / "memory" / "assumptions.md"

# real prices, per 1M tokens (api-docs.deepseek.com/quick_start/pricing, 2026-08-07)
_PRICES = {
    "deepseek-v4-flash": {"hit": 0.0028, "miss": 0.14, "out": 0.28},
    "deepseek-v4-pro": {"hit": 0.003625, "miss": 0.435, "out": 0.87},
}

TIERS = [
    {"id": "flash-off", "model": "deepseek-v4-flash", "thinking": False, "label": "flash · thinking OFF (current low default)"},
    {"id": "flash-on", "model": "deepseek-v4-flash", "thinking": True, "label": "flash · thinking ON"},
    {"id": "pro-off", "model": "deepseek-v4-pro", "thinking": False, "label": "pro · thinking OFF"},
    {"id": "pro-on", "model": "deepseek-v4-pro", "thinking": True, "label": "pro · thinking ON (current high)"},
]


# ------------------------------------------------------------------ scoring
def score_exec(text: str) -> tuple[float, str]:
    """Extract the code block, compile, and run a hidden unit test."""
    m = re.search(r"```(?:python)?\s*(.*?)```", text or "", re.S)
    code = m.group(1) if m else (text or "")
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return 0.0, f"does not compile ({e.lineno})"
    if not any(isinstance(n, ast.FunctionDef) and n.name == "parse_ts" for n in ast.walk(tree)):
        return 0.0, "no parse_ts function"
    ns: dict[str, Any] = {}
    try:
        exec(compile(tree, "<tier>", "exec"), ns)
        from datetime import datetime

        r1 = ns["parse_ts"]("2026-08-07T20:00:00Z")
        r2 = ns["parse_ts"]("2026-08-07T22:00:00+02:00")
        if isinstance(r1, datetime) and isinstance(r2, datetime) and r1.hour == 20 and r2.hour == 22:
            return 1.0, "passes hidden test (Z + offset both parse)"
        return 0.5, f"runs but fails hidden assert (r1={r1!r} r2={r2!r})"
    except Exception as e:  # noqa: BLE001
        return 0.3, f"runs with error: {str(e)[:60]}"


def score_design(text: str) -> tuple[float, str]:
    """Objective rubric: numbered steps, PASS-if conditions, concrete commands."""
    t = text or ""
    lines = [l for l in t.splitlines() if l.strip()]
    steps = [l for l in lines if re.match(r"^\s*\d+[.)]\s", l)]
    passifs = len(re.findall(r"pass\s+if", t.lower()))
    commands = len(re.findall(r"`[^`]+`|python -m|pytest|curl |git |assert\b|==\s*['\"\w]", t))
    score = 0.0
    score += 0.4 if len(steps) >= 3 else round(0.15 * len(steps), 2)
    score += 0.3 if passifs >= 3 else round(0.1 * passifs, 2)
    score += 0.3 if commands >= 3 else round(0.1 * min(commands, 3), 2)
    return round(min(score, 1.0), 2), f"steps={len(steps)} pass_if={passifs} cmds={commands}"


def score_design_correct(text: str, *, domain: str = "") -> tuple[float, str]:
    """Reasoning-correctness judge — the missing half.

    Structural score (score_design) rewards FORMAT; thinking-on models that write
    reasoning instead of terse steps get penalized as 'prose'. This judge keeps the
    structural score but ALSO checks SEMANTIC COHERENCE: are the steps actually
    about the domain, actionable, and carrying a measurable condition? It captures
    thinking-on's value without a second LLM call (objective regex/lexicon, no judge).
    """
    t = text or ""
    structural, why = score_design(t)
    # domain relevance: does the plan actually address the prompt's subject?
    domain_terms = [w for w in (domain or "").lower().split() if len(w) > 3]
    hits = sum(1 for w in domain_terms if w in t.lower()) if domain_terms else 1
    relevant = min(1.0, hits / max(2, len(domain_terms)))
    # actionable + measurable: commands present AND at least one PASS-if with a measure
    commands = len(re.findall(r"`[^`]+`|python -m|pytest|curl |git |assert\b|==\s*['\"\w]", t))
    passifs = len(re.findall(r"pass\s+if", t.lower()))
    measurable = 1.0 if passifs >= 1 else 0.0
    actionable = 1.0 if commands >= 1 else 0.0
    # coherence = structural (0.5) + relevance (0.25) + measurable/actionable (0.25)
    score = 0.5 * structural + 0.25 * relevant + 0.25 * (0.5 * measurable + 0.5 * actionable)
    return round(min(score, 1.0), 2), f"{why} rel={relevant:.2f} meas={measurable:.0f} act={actionable:.0f}"


TASKS: dict[str, dict[str, Any]] = {
    "design": {
        "label": "design — hypothesis/test-plan (should be HIGH)",
        "system": "You are a senior test architect. Be concrete and terse. No preamble.",
        "user": (
            "Assumption under test: 'Routing routine execution work to a low DeepSeek tier "
            "(flash, thinking off) produces equivalent results to a high tier (pro, thinking on), "
            "while design/hypothesis work degrades when moved down.'\n"
            "Produce a test plan as EXACTLY 3 numbered test steps. Each step is one line: "
            "a concrete command or check, then 'PASS if:' and a measurable condition. "
            "Do not add prose paragraphs."
        ),
        "score": score_design,
    },
    "design_vague": {
        "label": "design_vague — vague RIB (the missing half: tier should MATTER)",
        "system": "You are a senior test architect. Be concrete and terse. No preamble.",
        "user": (
            "We need to make our agents more reliable. Figure out what that means and give us "
            "a concrete plan. (No further guidance.)\n"
            "Produce exactly 3 numbered test steps, each one line: a concrete command or check, "
            "then 'PASS if:' and a measurable condition. No prose paragraphs."
        ),
        "score": score_design,
    },
    "exec": {
        "label": "exec — runnable code generation (should be LOW)",
        "system": "You are a precise Python engineer. Output ONLY one fenced Python code block. No explanation.",
        "user": (
            "Write a Python function `parse_ts(iso: str)` that parses an ISO-8601 timestamp string "
            "into a `datetime` object. Handle a trailing 'Z' (UTC) and a timezone offset like '+02:00'. "
            "Return the datetime. Only code, in a ```python fenced block."
        ),
        "score": score_exec,
    },
}


# ------------------------------------------------------------------- cost
def cost_for(model: str, usage: dict[str, Any]) -> dict[str, Any]:
    p = _PRICES.get(model) or {"hit": 0.14, "miss": 0.14, "out": 0.28}
    pt = int(usage.get("prompt_tokens") or 0)
    ct = int(usage.get("completion_tokens") or 0)
    rt = int(usage.get("reasoning_tokens") or 0)
    hit = int(usage.get("prompt_cache_hit_tokens") or 0)
    miss = pt - hit if usage.get("prompt_cache_hit_tokens") is not None else pt
    out_tok = ct + rt  # reasoning billed as output
    return {
        "prompt_tokens": pt, "completion_tokens": ct, "reasoning_tokens": rt,
        "cache_hit": hit, "cache_miss": miss,
        "cost_miss": round(miss / 1e6 * p["miss"] + out_tok / 1e6 * p["out"], 6),
        "cost_hit": round(hit / 1e6 * p["hit"] + out_tok / 1e6 * p["out"], 6),
    }


# ------------------------------------------------------------------- live
def _deepseek_call(model: str, system: str, user: str, *, thinking: bool,
                   temperature: float = 0.2, max_tokens: int = 4096, timeout: float = 180.0) -> dict[str, Any]:
    from models.providers import get_provider, provider_base_url, provider_keys

    pcfg = get_provider("deepseek") or {}
    base = provider_base_url(pcfg)
    keys = provider_keys(pcfg)
    if not keys:
        return {"ok": False, "error": "no DEEPSEEK_API_KEY in env"}
    url = f"{base}/chat/completions"
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    payload["thinking"] = {"type": "enabled" if thinking else "disabled"}
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {keys[0]}"},
        method="POST",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)[:200]}
    ms = int((time.perf_counter() - t0) * 1000)
    text = ((data.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()
    return {"ok": True, "text": text, "usage": data.get("usage") or {}, "ms": ms}


def run_cell(task_id: str, tier: dict[str, Any], *, live: bool, cache: bool = False) -> dict[str, Any]:
    t = TASKS[task_id]
    warm_usage = None
    if live:
        if cache:
            # SW1-07 (SWARM_1.md row 7, kimi+glm converged): the warm-up call's
            # tokens were discarded, so --cache runs under-reported true spend -
            # the cache-hit savings looked free because the cache-fill cost
            # vanished. Count them in the row (warm_tokens); the measured call
            # stays the cold-after-warm measurement, uncontaminated.
            warm = _deepseek_call(tier["model"], t["system"], t["user"], thinking=tier["thinking"])
            if warm.get("ok"):
                u = warm.get("usage") or {}
                warm_usage = {
                    "prompt_tokens": u.get("prompt_tokens", 0),
                    "completion_tokens": u.get("completion_tokens", 0),
                    "cost": cost_for(tier["model"], u),
                }
        res = _deepseek_call(tier["model"], t["system"], t["user"], thinking=tier["thinking"])
        if not res.get("ok"):
            return {"tier": tier["id"], "ok": False, "error": res.get("error")}
        text = res["text"]
        usage = res["usage"]
        ms = res["ms"]
    else:
        text = "```python\ndef parse_ts(iso): return iso\n```" if task_id == "exec" else "1. `pytest -x` PASS if: 0 failed\n2. `python -m pytest tests/` PASS if: all green\n3. `git diff` PASS if: no unexpected change"
        usage = {"prompt_tokens": 400, "completion_tokens": 200}
        ms = 0
    score, note = t["score"](text)
    cost = cost_for(tier["model"], usage)
    # Thinking-mode axis (proven): also judge reasoning CORRECTNESS for design tasks,
    # not just format. score_design_correct blends structural + domain relevance +
    # measurable/actionable so thinking-on's value isn't penalized as 'prose'.
    correctness: float | None = None
    cnote: str | None = None
    if task_id in ("design", "design_vague"):
        try:
            correctness, cnote = score_design_correct(text, domain=task_id)
        except Exception:
            correctness, cnote = None, None
    return {
        "tier": tier["id"], "tier_label": tier["label"], "ok": True,
        "score": score, "note": note, "text": text[:160], "ms": ms,
        "usage": cost, "correctness": correctness, "cnote": cnote,
        "warm": warm_usage,  # SW1-07: cache-fill spend, counted not discarded
    }


def run_probe(*, tasks: list[str] | None = None, live: bool = True, runs: int = 1, cache: bool = False) -> list[dict[str, Any]]:
    import statistics

    want = [x for x in (tasks or list(TASKS)) if x in TASKS]
    out: list[dict[str, Any]] = []
    for tid in want:
        for tier in TIERS:
            cells = [run_cell(tid, tier, live=live, cache=cache) for _ in range(max(1, runs))]
            ok_cells = [c for c in cells if c.get("ok")]
            if not ok_cells:
                out.append({"task": tid, "task_label": TASKS[tid]["label"], **cells[0]})
                continue
            base = ok_cells[0]
            scores = [c["score"] for c in ok_cells]
            corr = [c.get("correctness") for c in ok_cells if c.get("correctness") is not None]
            out.append({
                "task": tid, "task_label": TASKS[tid]["label"],
                "tier": tier["id"], "tier_label": tier["label"], "ok": True,
                "score": round(sum(scores) / len(scores), 2),
                "score_sd": round(statistics.pstdev(scores), 2) if len(scores) > 1 else 0.0,
                "correctness": round(sum(corr) / len(corr), 2) if corr else None,
                "cnote": base.get("cnote"),
                "n": len(ok_cells),
                "note": base["note"], "text": base["text"],
                "ms": int(sum(c["ms"] for c in ok_cells) / len(ok_cells)),
                "usage": {k: round(sum(c["usage"][k] for c in ok_cells) / len(ok_cells), 2) for k in base["usage"]},
            })
    return out


# ----------------------------------------------------------------- report
def render_report(results: list[dict[str, Any]], *, live: bool) -> str:
    lines = [
        "# DeepSeek Tier Probe — right-size the router (assumption test)",
        "",
        f"- ts: {datetime.now(timezone.utc).isoformat()}",
        f"- mode: {'LIVE (real DeepSeek API calls)' if live else 'DRY-RUN (scoring only)'}",
        f"- prices: flash hit $0.0028/miss $0.14/out $0.28 · pro hit $0.003625/miss $0.435/out $0.87 (per 1M)",
        "",
        "## Quality by task × tier  (1.0 = passes objective check)",
        "",
        "| task | tier | score | correct | note | ms | in/out(tok) | cost(miss) | cost(hit) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        if not r.get("ok"):
            lines.append(f"| **{r['task']}** | {r['tier']} | — | ERROR {r.get('error','')[:60]} | — | — | — | — |")
            continue
        u = r["usage"]
        sd = r.get("score_sd")
        score_cell = f"**{r['score']:.2f}**±{sd:.2f}" if sd is not None else f"**{r['score']:.2f}**"
        n_cell = f" (n={r['n']})" if r.get("n") else ""
        corr_cell = f"{r['correctness']:.2f}" if r.get("correctness") is not None else "—"
        lines.append(
            f"| **{r['task']}** | {r['tier']} | {score_cell} | {corr_cell} | {r['note']}{n_cell} "
            f"| {r['ms']} | {u['prompt_tokens']}/{u['completion_tokens']}(+{u['reasoning_tokens']}r) "
            f"| ${u['cost_miss']:.5f} | ${u['cost_hit']:.5f} |"
        )
    lines += [
        "",
        "## What works / what does not (verdict)",
        "",
    ]
    by_task: dict[str, list[dict[str, Any]]] = {}
    for r in results:
        by_task.setdefault(r["task"], []).append(r)
    for tid, cells in by_task.items():
        best = max((c for c in cells if c.get("ok")), key=lambda c: c["score"], default=None)
        low = next((c for c in cells if c["tier"] == "flash-off"), None)
        high = next((c for c in cells if c["tier"] == "pro-on"), None)
        if best is None:
            continue
        verdict = "HIGH tier adds nothing here — LOW is fine." if low and best["score"] == low["score"] and low["score"] > 0 else "tier matters on this shape — check cells."
        lines.append(f"- **{tid}** ({TASKS[tid]['label']}): best {best['tier']} @ {best['score']:.2f}; flash-off {low['score'] if low else '—'} vs pro-on {high['score'] if high else '—'} → {verdict}")
    return "\n".join(lines)


def append_ledger(results: list[dict[str, Any]], *, assumption: str) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    if not LEDGER.is_file():
        LEDGER.write_text(
            "# Assumption Ledger — test it before you trust it\n\n"
            "Every time we assume a routing/tier/session property, we A/B it and record the "
            "verdict + the hidden insight ('the dot').\n\n"
            "| ts | assumption | task | flash-off | pro-on | verdict | cost | dot |\n"
            "|---|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rows = []
    for tid in sorted({r["task"] for r in results}):
        cells = [r for r in results if r["task"] == tid and r.get("ok")]
        low = next((c for c in cells if c["tier"] == "flash-off"), None)
        high = next((c for c in cells if c["tier"] == "pro-on"), None)
        ls = f"{low['score']:.2f}" if low else "err"
        hs = f"{high['score']:.2f}" if high else "err"
        verdict = "LOW fine" if low and high and low["score"] == high["score"] and low["score"] > 0 else "tier matters"
        cost = sum(c["usage"]["cost_miss"] for c in cells if c.get("ok"))
        rows.append(f"| {ts} | {assumption} | {tid} | {ls} | {hs} | {verdict} | ${cost:.5f} | see REPORT |")
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")


def write_report(results: list[dict[str, Any]], *, live: bool) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    d = RUN_DIR / ts
    d.mkdir(parents=True, exist_ok=True)
    (d / "REPORT.md").write_text(render_report(results, live=live), encoding="utf-8")
    (d / "raw.json").write_text(
        json.dumps({"ts": ts, "live": live, "results": results}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return d


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tier-probe", description="DeepSeek right-sizing A/B (assumption testing).")
    ap.add_argument("--task", action="append", choices=list(TASKS), help="task id; repeat or omit for all")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-live", action="store_true", help="dry-run scoring (no API calls)")
    ap.add_argument("--no-ledger", action="store_true")
    ap.add_argument("--runs", type=int, default=1, help="runs per cell → score±sd CI")
    ap.add_argument("--cache", action="store_true", help="double-call each cell (warm-up) to measure cache-hit economics")
    args = ap.parse_args(argv)

    live = not args.no_live
    results = run_probe(tasks=args.task, live=live, runs=args.runs, cache=args.cache)
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(render_report(results, live=live))
    if not args.no_ledger:
        append_ledger(results, assumption="DeepSeek tier A/B: design needs HIGH, execution is fine on LOW (flash/off)")
    d = write_report(results, live=live)
    print(f"\n[report] {d}")
    if not args.no_ledger:
        print(f"[ledger] {LEDGER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
