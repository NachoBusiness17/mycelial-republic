"""E — UNION ALPHA eval driver (wave-lane, FREE only, $0 cap).

Battery against opencode's stealth/union-alpha on OpenRouter:
  1. IDENTITY pass (3 q x 3 seeds, T0.8, no system prompt — bare-model identity probe)
  2. THE NIGHT'S VERDICTS (3 q verbatim from receipts/D23_SALON50_NIGHT_RESULTS.md, 2 seeds each)
  3. AGENTIC-CODING smoke (2 tasks; extracted code is actually executed, graded)
Tape: memory/runs/e_union_alpha_20260916/raw.jsonl (append-as-you-go).
Receipt: watch/inbox/wave_20260916/receipts/E_UNION_ALPHA_EVAL.md (compact index appended as batteries land).

Law: 402/403 paid wall -> record and STOP. 429 -> one cooldown retry, then keep the row.
Key never printed. Sequential, one call in flight.
"""
import copy
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from mag.flight_recorder import load_env, guard_endpoint  # noqa: E402
from mag.research_fanout import LANES  # noqa: E402

RUN_DIR = os.path.join(ROOT, "memory", "runs", "e_union_alpha_20260916")
TAPE = os.path.join(RUN_DIR, "raw.jsonl")
RECEIPT = os.path.join(HERE, "receipts", "E_UNION_ALPHA_EVAL.md")
ALLOW = {"openrouter.ai"}
LANE_ID = "or-union-alpha"
MODEL_SEED_BASE = 2026091600

os.makedirs(RUN_DIR, exist_ok=True)

IDENTITY_QS = [
    "In one sentence: what are you?",
    "Who trained you and on what?",
    "What is your context window?",
]

# Verbatim from watch/inbox/wave_20260916/receipts/D23_SALON50_NIGHT_RESULTS.md (registered set)
VERDICT_QS = [
    ("Q1_sampler_kill",
     "A measurement found that decorrelation between free-LLM lanes does NOT predict answer "
     "quality (rho +0.33, wrong-signed, replicated). Does this kill the analogy that multi-model "
     "salons are thermodynamic samplers, or can it be saved by redefining the ensemble? "
     "Take a side, under 120 words."),
    ("Q2_zero_dollar_falsification",
     "A vendor claims 140x energy efficiency for thermodynamic sampling hardware and publishes a "
     "simulator + open weights, but no silicon measurements. What is the strongest falsification "
     "protocol a $0-budget team can run, and what could it NOT prove? Under 120 words."),
    ("Q3_void_procedure",
     "An append-only evidence ledger cannot delete false rows. Design the void procedure in one "
     "paragraph: what marks a row dead, who can mark it, and what prevents weaponized voiding. "
     "Under 120 words."),
]

CODING_TASKS = [
    ("task_a_dedupe",
     "Write a python function that detects duplicate canonical URLs in a JSONL ledger by sha256, "
     "with tests"),
    ("task_b_void",
     "Given an append-only ledger that cannot delete rows, write the void() function marking a row "
     "dead without mutation."),
]

STOP = {"paid_wall": False, "reason": ""}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_row(rec: dict) -> None:
    with open(TAPE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def receipt_append(text: str) -> None:
    with open(RECEIPT, "a", encoding="utf-8") as fh:
        fh.write(text)


def call(question: str, temperature: float, seed: int, max_tokens: int = 3000,
         timeout: int = 150) -> dict:
    """One call, one row. Mirrors call_lane's SSRF-safe pattern; NO system prompt; free temp."""
    key = ENV.get("OPENROUTER_API_KEY", "")
    url = BASE.rstrip("/") + "/chat/completions"
    guard_endpoint(url, ALLOW)  # https + host allowlist, before any request
    body = {"model": MODEL, "temperature": temperature, "max_tokens": max_tokens, "seed": seed,
            "messages": [{"role": "user", "content": question}]}
    attempt = 0
    while True:
        attempt += 1
        t0 = time.time()
        rec = {"battery": CUR_BATTERY["name"], "item": CUR_BATTERY["item"], "seed": seed,
               "temperature": temperature, "ts": now(), "attempt": attempt}
        req = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "User-Agent": "mag-union-alpha-eval/1.0",
                     "HTTP-Referer": "https://local-sovereign-agent.invalid",
                     "X-Title": "Mag Union Alpha Eval"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            msg = d["choices"][0]["message"]
            txt = (msg.get("content") or "").strip()
            rec["finish_reason"] = d["choices"][0].get("finish_reason")
            rec["usage"] = d.get("usage") or {}
            if not txt:
                rec.update({"ok": False, "error": "empty_content",
                            "detail": (msg.get("reasoning") or msg.get("reasoning_content")
                                       or "")[:200]})
            else:
                rec.update({"ok": True, "answer": txt, "chars": len(txt)})
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
            if e.code in (402, 403):
                STOP["paid_wall"] = True
                STOP["reason"] = f"HTTP {e.code} on {CUR_BATTERY['name']}/{CUR_BATTERY['item']}"
            elif e.code == 429 and attempt < 2:
                append_row(rec)
                print(json.dumps(rec, ensure_ascii=False), flush=True)
                time.sleep(25)
                continue
        except Exception as e:  # noqa: BLE001
            rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"})
        rec["latency_ms"] = int((time.time() - t0) * 1000)
        append_row(rec)
        print(json.dumps(rec, ensure_ascii=False), flush=True)
        return rec


def fire(name: str, item: str) -> None:
    CUR_BATTERY["name"], CUR_BATTERY["item"] = name, item


# ------------------------------------------------------------------ code execution grading

FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL)

LAW_KEYS = {
    "task_a_dedupe": {
        "sha256": re.compile(r"sha256|sha_256|hashlib", re.I),
        "canonicalization": re.compile(r"canonical|normali[sz]|lower\(\)|scheme|fragment|strip", re.I),
        "jsonl": re.compile(r"jsonl|json\.loads|line", re.I),
    },
    "task_b_void": {
        "tombstone_marker": re.compile(r"tombstone|void_event|voided|supersede|revocation|marker", re.I),
        "non_mutation": re.compile(r"not\s+mutat|immutab|never\s+(delete|modif|alter)|without\s+mutat|append", re.I),
        "hash_bind": re.compile(r"hash|sha|digest", re.I),
        "authority": re.compile(r"sign|author|permission|who|quorum|steward|auditor", re.I),
    },
}

SMOKE_VOID = r'''
import copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("m", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
out = {"void_found": callable(getattr(m, "void", None))}
f = getattr(m, "void", None)
if callable(f):
    row = {"id": "r1", "claim": "sky is green"}
    before = copy.deepcopy(row)
    attempts = []
    for args, kwargs in ((("r1",), {}), ((row,), {}), ((), {"row_id": "r1"}),
                         (([row],), {"row_id": "r1"}), (({"rows": [row]},), {"row_id": "r1"})):
        try:
            res = f(*args, **kwargs)
            attempts.append({"ok": True, "args": repr(args)[:80],
                             "result": repr(res)[:400]})
            break
        except Exception as e:
            attempts.append({"ok": False, "args": repr(args)[:80],
                             "err": (type(e).__name__ + ": " + str(e))[:160]})
    out["attempts"] = attempts
    out["original_row_unmutated"] = (row == before)
    out["row_after"] = repr(row)[:400]
print(json.dumps(out))
'''


def grade_code(task_id: str, answer: str, tag: str) -> dict:
    blocks = FENCE.findall(answer)
    grade = {"task": task_id, "code_blocks": len(blocks), "law_named": {}}
    code = "\n\n".join(b for b in blocks if b.strip())
    if not code:
        # maybe the model answered bare code with no fence — take the whole answer as a fallback
        code = answer
        grade["unfenced_fallback"] = True
    for law, rx in LAW_KEYS.get(task_id, {}).items():
        grade["law_named"][law] = bool(rx.search(code))
    path = os.path.join(RUN_DIR, f"{tag}.py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(code)
    grade["file"] = path
    grade["bytes"] = len(code.encode("utf-8"))
    # 1) syntax check
    try:
        compile(code, path, "exec")
        grade["syntax_ok"] = True
    except SyntaxError as e:
        grade["syntax_ok"] = False
        grade["syntax_error"] = f"{type(e).__name__}: {e}"[:200]
        return grade
    # 2) run it directly (executes __main__ blocks / top-level asserts)
    try:
        p = subprocess.run([sys.executable, path], cwd=RUN_DIR, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=60)
        grade["direct_run"] = {"exit": p.returncode,
                               "stdout_tail": (p.stdout or "")[-500:],
                               "stderr_tail": (p.stderr or "")[-500:]}
    except subprocess.TimeoutExpired:
        grade["direct_run"] = {"exit": "TIMEOUT"}
    # 3) if it looks pytest-only, try pytest
    if "pytest" in code and "def test_" in code:
        try:
            p = subprocess.run([sys.executable, "-m", "pytest", "-q", path], cwd=RUN_DIR,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=120)
            grade["pytest_run"] = {"exit": p.returncode, "tail": (p.stdout or "")[-500:]}
        except Exception as e:  # noqa: BLE001
            grade["pytest_run"] = {"exit": f"{type(e).__name__}"}
    # 4) task_b: exercise void() in a child process
    if task_id == "task_b_void":
        smoke_path = os.path.join(RUN_DIR, f"{tag}_smoke.py")
        with open(smoke_path, "w", encoding="utf-8") as fh:
            fh.write(SMOKE_VOID)
        try:
            p = subprocess.run([sys.executable, smoke_path, path], cwd=RUN_DIR,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=60)
            grade["void_smoke"] = {"exit": p.returncode}
            try:
                grade["void_smoke"]["result"] = json.loads((p.stdout or "").strip().splitlines()[-1])
            except Exception:  # noqa: BLE001
                grade["void_smoke"]["raw"] = ((p.stdout or "") + (p.stderr or ""))[-400:]
        except subprocess.TimeoutExpired:
            grade["void_smoke"] = {"exit": "TIMEOUT"}
    return grade


# ------------------------------------------------------------------ main

ENV = load_env(ROOT)
_lane = next((l for l in LANES if l["id"] == LANE_ID), None)
if _lane is None:
    sys.exit(f"lane {LANE_ID} not in LANES")
BASE, MODEL = _lane["base"], _lane["model"]
CUR_BATTERY = {"name": "", "item": ""}

if not ENV.get("OPENROUTER_API_KEY"):
    sys.exit("OPENROUTER_API_KEY missing from .env — aborting before any call")


def battery_identity() -> list:
    rows = []
    receipt_append("\n### IDENTITY pass (T0.8, 3 seeds, verbatim)\n\n")
    for qi, q in enumerate(IDENTITY_QS):
        fire("identity", f"q{qi}")
        for s in range(3):
            r = call(q, 0.8, MODEL_SEED_BASE + qi * 10 + s)
            rows.append(r)
            if STOP["paid_wall"]:
                return rows
            verdict = r.get("answer", f"FAIL: {r.get('error')} {r.get('detail', '')[:120]}")
            receipt_append(f"- q{qi} \"{q}\" seed{s} [{r.get('latency_ms')}ms, "
                           f"{r.get('chars', 0)}ch]: {verdict!r}\n")
    return rows


def battery_verdicts() -> list:
    rows = []
    receipt_append("\n### THE NIGHT'S VERDICTS (D23 verbatim set, 2 seeds: T0.2 / T0.7)\n\n")
    for vj, (qid, q) in enumerate(VERDICT_QS):
        fire("verdicts", qid)
        for si, temp in enumerate((0.2, 0.7)):
            r = call(q, temp, MODEL_SEED_BASE + 100 + vj * 10 + si)
            rows.append(r)
            if STOP["paid_wall"]:
                return rows
            ans = r.get("answer", "")
            words = len(ans.split())
            receipt_append(f"- {qid} seed{si} T{temp} [{r.get('latency_ms')}ms, {r.get('chars', 0)}ch, "
                           f"{words}w]: {'ON-LENGTH' if 0 < words <= 130 else 'OVER/EMPTY'}\n")
    return rows


def battery_coding() -> list:
    rows = []
    receipt_append("\n### AGENTIC-CODING smoke (T0.2, code actually executed)\n\n")
    for ci, (tid, q) in enumerate(CODING_TASKS):
        fire("coding", tid)
        r = call(q, 0.2, MODEL_SEED_BASE + 200 + ci, max_tokens=4000)
        rows.append(r)
        if STOP["paid_wall"]:
            return rows
        if r.get("ok"):
            g = grade_code(tid, r["answer"], f"union_{tid}")
            r["grade"] = g
            with open(TAPE, "a", encoding="utf-8") as fh:  # grade rides the tape as an extra row
                fh.write(json.dumps({"grade_of": f"{tid}", "grade": g, "ts": now()},
                                    ensure_ascii=False) + "\n")
            receipt_append(
                f"- {tid}: blocks={g['code_blocks']} syntax_ok={g.get('syntax_ok')} "
                f"direct_run={g.get('direct_run', {}).get('exit')} "
                f"pytest={g.get('pytest_run', {}).get('exit', 'n/a')} "
                f"void_smoke={'yes' if 'void_smoke' in g else 'n/a'} "
                f"law={ {k: v for k, v in g['law_named'].items()} } file={g['file']}\n")
            if "void_smoke" in g and isinstance(g["void_smoke"].get("result"), dict):
                receipt_append(f"  - void_smoke: {json.dumps(g['void_smoke']['result'])[:400]}\n")
        else:
            receipt_append(f"- {tid}: CALL FAILED {r.get('error')} {r.get('detail', '')[:120]}\n")
    return rows


def main() -> None:
    receipt_append("\n## Probe log\n\n- No separate probe: first battery call IS the probe "
                   "(identity q0 seed0). A 402 there ends the run.\n")
    receipt_append("\n## Run log\n\n")
    t0 = time.time()
    all_rows = []
    all_rows += battery_identity()
    if not STOP["paid_wall"]:
        all_rows += battery_verdicts()
    if not STOP["paid_wall"]:
        all_rows += battery_coding()
    ok = sum(1 for r in all_rows if r.get("ok"))
    receipt_append(
        f"\n- Run finished {now()}: {len(all_rows)} calls, {ok} ok, wall "
        f"{int(time.time() - t0)}s. Tape: {TAPE}\n")
    if STOP["paid_wall"]:
        receipt_append(f"- **STOPPED: {STOP['reason']} — paid wall; per law, recorded and stopped.**\n")
    print("DONE", json.dumps({"calls": len(all_rows), "ok": ok,
                              "stopped": STOP["paid_wall"], "reason": STOP["reason"]}))


if __name__ == "__main__":
    main()
