"""F1 code duel - flash vs prime on a real code-building task (phase 2).

Mission clause 3: "also run both on a code-building task ... to compare
functional quality beyond adversarial prose". Both contenders write the
same stdlib CLI tool from f1_code_spec.md (duelsum, a duel-ledger
summarizer; dogfood: the exact tool class the F1 receipt itself needs).
Functional verification is BYTE truth, not vibes: each contender file
runs on four fixtures and its stdout must match f1_ref_impl.py (the
lane owner's reference, not a model) exactly. Pass counts are a hard
metric banked in the receipt independent of the judge.

The ember judge then scores the two codes blind (A/B slots, harness
v1.1) with the factual test results as shared context, phrased in SLOT
terms so blinding holds. Rubric: correctness, edge-case handling, spec
compliance, code quality.

Laws: $0.30 lane cap shared with f1_series.py (phase 1 spend is read
from the contender cache + ledger); idempotent via the same cache keys;
width 1; no em-dash below.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402
from f1_series import call_long, cache_load, cache_bank  # noqa: E402

BUDGET_CAP = 0.30            # shared with phase 1 (the whole F1 lane)
PROJECTED = 0.075            # 2 contenders + judge, worst case
DUEL_ID = "f1ab-code-flash-prime"
A_MODEL = "z-ai/glm-5.3-flash"
B_MODEL = "z-ai/glm-5.3-prime"
JUDGE = dh.DEFAULT_JUDGE
RUBRIC = ["correctness", "edge-case handling", "spec compliance", "code quality"]
SPEC_PATH = HERE / "f1_code_spec.md"
REF_PATH = HERE / "f1_ref_impl.py"
FIXTURES = [
    HERE / "f1_fixtures" / "a_in_ask.jsonl",
    HERE / "f1_fixtures" / "b_empty.jsonl",
    HERE / "f1_fixtures" / "c_edges.jsonl",
    HERE / "f1_fixtures" / "no_such_file.jsonl",
]
OUT_DIR = HERE / "f1_code_out"
RESULTS_PATH = OUT_DIR / "results.json"

FENCE_RE = re.compile(r"```[a-zA-Z0-9_+-]*\n(.*?)```", re.DOTALL)


def extract_code(text: str) -> str:
    """Longest fenced block if fenced, else the raw reply."""
    blocks = FENCE_RE.findall(text or "")
    if blocks:
        return max(blocks, key=len).strip() + "\n"
    return (text or "").strip() + "\n"


def run_tool(py: Path, fixture: Path) -> tuple[str, str, bool]:
    """Run one contender file on one fixture. Returns (stdout, stderr, ok)."""
    proc = subprocess.run(
        [sys.executable, str(py), str(fixture)],
        capture_output=True, text=True, timeout=20, cwd=str(OUT_DIR))
    return proc.stdout, proc.stderr, proc.returncode == 0


def grade(py: Path, expected: dict[str, str]) -> dict:
    """Per-fixture byte comparison against the reference outputs."""
    out: dict = {}
    for fx, want in expected.items():
        try:
            got, err, rc_ok = run_tool(py, Path(fx))
            out[Path(fx).name] = {
                "pass": rc_ok and got.strip() == want.strip(),
                "got": got.strip()[:400], "want": want.strip()[:200],
                "stderr_head": err.strip()[:200], "rc_ok": rc_ok}
        except subprocess.TimeoutExpired:
            out[Path(fx).name] = {"pass": False, "got": "(timeout 20s)",
                                  "want": want.strip()[:200], "stderr_head": "",
                                  "rc_ok": False}
    out["pass_count"] = sum(1 for k, v in out.items()
                            if k != "pass_count" and v["pass"])
    return out


def build_context(task: str, slot_results: dict) -> str:
    """Factual test results in SLOT terms (blind-safe)."""
    lines = ["FUNCTIONAL TEST RESULTS (byte-exact stdout comparison against "
             "a reference implementation on 4 fixtures; same fixtures for "
             "both contenders):"]
    for slot in ("A", "B"):
        r = slot_results[slot]
        fx = {k: v for k, v in r.items() if k != "pass_count"}
        for name, v in fx.items():
            lines.append(f"SLOT {slot} fixture {name}: "
                         f"{'PASS' if v['pass'] else 'FAIL'}"
                         + ("" if v["pass"] else
                            f" (got: {v['got'][:150]!r})"))
        lines.append(f"SLOT {slot} TOTAL: {r['pass_count']}/4 passed")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="F1 code duel (phase 2)")
    p.add_argument("--dry", action="store_true")
    p.add_argument("--out", type=Path, default=dh.OUT_DEFAULT)
    args = p.parse_args(argv)

    task = SPEC_PATH.read_text(encoding="utf-8")
    # expected outputs computed live from the reference (trust bytes)
    expected: dict[str, str] = {}
    for fx in FIXTURES:
        proc = subprocess.run([sys.executable, str(REF_PATH), str(fx)],
                              capture_output=True, text=True, timeout=20)
        expected[str(fx)] = proc.stdout

    if args.dry:
        print(json.dumps({"run": DUEL_ID, "a_model": A_MODEL, "b_model": B_MODEL,
                          "judge": JUDGE, "rubric": RUBRIC,
                          "spec_chars": len(task), "fixtures": list(expected),
                          "cache": sorted(cache_load())}, indent=2))
        return 0

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2

    # lane spend so far: contender cache costs (phase 1 + probes) + judge
    # costs of banked f1 rows (approx lane accounting; cap check is a gate)
    spent = sum(r.get("cost", 0.0) for r in cache_load().values())
    banked = [json.loads(l) for l in open(args.out, encoding="utf-8") if l.strip()]
    spent += sum(r.get("judge_cost", 0.0) for r in banked
                 if str(r.get("ask_id", "")).startswith("f1ab-"))
    print(f"lane spent so far (cache + f1 judges): ${spent:.4f}")
    if spent + PROJECTED > BUDGET_CAP:
        print(f"BUDGET HOLD: ${spent:.4f} + ${PROJECTED} exceeds ${BUDGET_CAP:.2f}")
        return 2

    OUT_DIR.mkdir(exist_ok=True)
    cache = cache_load()
    answers: dict[str, tuple[str, float]] = {}
    for fam, model in (("flash", A_MODEL), ("prime", B_MODEL)):
        key = f"{fam}#{DUEL_ID}"
        if key in cache:
            answers[fam] = (cache[key]["content"], 0.0)
            print(f"reuse cached {key}")
            continue
        text, cost = dh.fire(model, task, keys, f"{DUEL_ID}:{fam}", caller=call_long)
        cache_bank(key, model, text, cost)
        answers[fam] = (text, cost)
        spent += cost

    codes = {fam: extract_code(answers[fam][0]) for fam in ("flash", "prime")}
    (OUT_DIR / "flash.py").write_text(codes["flash"], encoding="utf-8")
    (OUT_DIR / "prime.py").write_text(codes["prime"], encoding="utf-8")
    (OUT_DIR / "flash_raw.md").write_text(answers["flash"][0], encoding="utf-8")
    (OUT_DIR / "prime_raw.md").write_text(answers["prime"][0], encoding="utf-8")

    graded = {
        "flash": grade(OUT_DIR / "flash.py", expected),
        "prime": grade(OUT_DIR / "prime.py", expected),
    }
    print(json.dumps({f: graded[f]["pass_count"] for f in graded}))

    swap = dh.ledger_row_count(args.out) % 2 == 1  # harness parity rule
    slot_results = {
        "A": graded["flash"] if not swap else graded["prime"],
        "B": graded["prime"] if not swap else graded["flash"],
    }
    context = build_context(task, slot_results)
    row = dh.run_duel(
        DUEL_ID, task, A_MODEL, B_MODEL,
        a_text=codes["flash"], b_text=codes["prime"],
        a_cost=answers["flash"][1], b_cost=answers["prime"][1],
        judge_model=JUDGE, rubric=list(RUBRIC), context=context,
        out_path=args.out, keys=keys, mode="f1-flash-vs-prime", swap=swap,
    )
    spent += row["judge_cost"]
    RESULTS_PATH.write_text(json.dumps({
        "duel_id": DUEL_ID, "swap": swap, "winner_logical": row["winner"],
        "graded": graded, "criteria": row["criteria"],
        "rationale": row["rationale"], "a_chars": row["a_chars"],
        "b_chars": row["b_chars"], "judge_cost": row["judge_cost"],
        "spent_lane_est": round(spent, 4)}, indent=2), encoding="utf-8")
    print(json.dumps({"winner": row["winner"], "flash_pass": graded["flash"]["pass_count"],
                      "prime_pass": graded["prime"]["pass_count"],
                      "spent_lane_est": round(spent, 4)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
