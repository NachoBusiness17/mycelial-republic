#!/usr/bin/env python3
# prior_art: tools/lens_packet.py, tools/ractor_salon.py, tools/burn_lanes.py --
#   all three run one prompt-shape across lanes; none runs six different tests.
"""six_tests -- the six lens tests, run unattended, one receipt each.

Operator: "do it all, going to bed." So: every test runs to completion without a
human, each writes its own JSON, and the morning summary is written even if some
tests fail. A failing test is recorded as a failing test, never as a silent miss.

    python tools/six_tests.py            # all six
    python tools/six_tests.py --only t4  # one
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from burn_lanes import LANES, http_lane  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "memory" / "runs" / "six_tests"
LANE = {l["id"]: l for l in LANES}


def lane(name: str) -> dict:
    return LANE[name]


def ask(lane_id: str, prompt: str, max_tokens: int = 900) -> str:
    res = http_lane(lane(lane_id), prompt, max_tokens)
    return (res.get("text") or "").strip() if res.get("ok") else ""


def local_ask(prompt: str, model: str = "qwen2.5-coder:7b", timeout: int = 180) -> str:
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 700, "stream": False}
    req = urllib.request.Request("http://127.0.0.1:11434/v1/chat/completions",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            d = json.loads(resp.read().decode("utf-8", "replace"))
        return ((d.get("choices") or [{}])[0].get("message") or {}).get("content", "").strip()
    except Exception as exc:  # noqa: BLE001
        return f"__ERR__ {type(exc).__name__}: {str(exc)[:80]}"


def write(name: str, payload: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


# ── T4 JUNG: what returns because it was disowned (no LLM) ─────────────────
def t4_shadow() -> dict:
    try:
        raw = subprocess.run(["schtasks", "/query", "/fo", "CSV", "/v"],
                             capture_output=True, text=True, timeout=120).stdout
    except Exception as exc:  # noqa: BLE001
        return {"test": "T4", "ok": False, "error": str(exc)}

    import csv
    import io
    rows = list(csv.DictReader(io.StringIO(raw)))
    mag = [r for r in rows if "mag" in (r.get("TaskName") or "").lower()]
    git_writers, chain_touchers, others = [], [], []
    for r in mag:
        cmd = (r.get("Task To Run") or "")
        name = r.get("TaskName")
        script = ""
        m = re.search(r'"([^"]+\.(ps1|py|bat|cmd))"', cmd)
        if m:
            script = m.group(1)
        body = ""
        if script and Path(script).is_file():
            try:
                body = Path(script).read_text(encoding="utf-8", errors="replace")[:20000]
            except OSError:
                body = ""
        blob = (cmd + "\n" + body).lower()
        entry = {"task": name, "script": Path(script).name if script else "",
                 "state": r.get("Status")}
        if re.search(r"git\s+(add|commit|push|reset|checkout)", blob):
            git_writers.append(entry)
        elif re.search(r"verkle|chain|biography", blob):
            chain_touchers.append(entry)
        else:
            others.append(entry)
    return {"test": "T4", "ok": True, "mag_tasks": len(mag),
            "git_writers": git_writers, "chain_touchers": chain_touchers,
            "others": len(others),
            "note": "a scheduled task that writes git is a second scheduler unless it holds the sweeper's lease"}


# ── T2 ELLUL: chosen vs procedure ──────────────────────────────────────────
STEPS = [
    "Read the current state file before acting",
    "Check git status for uncommitted work",
    "Run the test suite before claiming done",
    "Write a receipt for the wave",
    "Re-run the audit after a fix",
    "Compare the new count to the last count",
    "Open the falsifier ledger and check dates",
    "Re-derive a fix that already exists",
    "Add a new tool instead of extending an existing one",
    "Ask a panel of lenses for an opinion",
    "Cluster the panel's answers before counting",
    "Record the cost of a run",
    "Check whether a key answers before using the lane",
    "Retry an empty answer with a bigger budget",
    "Write a map of the system before deciding",
    "Number the premises in a map",
    "Plant a known falsehood to test an auditor",
    "Count duplicates in a queue",
    "Check who reads a file before building a consumer",
    "Read the queue's actual composition instead of its size",
    "Add a status value to separate instrumentation from work",
    "Make a rewrite atomic",
    "Take a lock before a read-modify-write",
    "Add a gate to pre-commit",
]


def t2_inertia() -> dict:
    janitor = "\n".join(f"{i+1}. {s}" for i, s in enumerate(STEPS))
    prompt = ("Classify each step of an engineering session as either CHOSEN (someone decided it "
              "for this situation) or PROCEDURE (it happened because the method says so). "
              "Reply with one line per step: N=CHOSEN or N=PROCEDURE. No commentary.\n\n" + janitor)
    a = ask("groq-nacho", prompt, 700)
    b = ask("ollama-sd", prompt, 700)

    def parse(text: str) -> dict[int, str]:
        out = {}
        for m in re.finditer(r"(\d+)\s*[=:.-]\s*(CHOSEN|PROCEDURE)", text.upper()):
            out[int(m.group(1))] = m.group(2)
        return out

    pa, pb = parse(a), parse(b)
    common = sorted(set(pa) & set(pb))
    agree = [i for i in common if pa[i] == pb[i]]
    proc = [i for i in agree if pa[i] == "PROCEDURE"]
    return {"test": "T2", "ok": bool(common), "steps": len(STEPS),
            "labelled": len(common), "agreement": len(agree),
            "agreement_pct": round(100 * len(agree) / len(common), 1) if common else 0,
            "procedure_steps": [STEPS[i - 1] for i in proc if 1 <= i <= len(STEPS)],
            "procedure_share_pct": round(100 * len(proc) / len(agree), 1) if agree else 0,
            "raw_a": a[:600], "raw_b": b[:600]}


# ── T3 McLUHAN: surface effect ─────────────────────────────────────────────
FINDING = ("The explore queue holds 2,388 open rows; 62.5% are probe_* model chatter; "
           "~750 distinct live observations remain; sixteen code files already read it.")
SURFACES = {
    "prose": f"Note from the estate:\n\n{FINDING}",
    "receipt": ("RECEIPT 2026-10-24\n" + "-" * 40 + "\n" + FINDING +
                "\n" + "-" * 40 + "\nstatus: measured\n"),
    "cockpit": f"WARN queue   open 2388 | probe 62.5% | live ~750 | readers 16",
    "json": json.dumps({"open": 2388, "probe_share": 0.625, "live_est": 750, "readers": 16}),
}


def t3_surface_run() -> dict:
    lanes = ["groq-nacho", "ollama-sd", "deepseek-flash", "nous-longcat"]
    rows = []
    for surface, body in SURFACES.items():
        for ln in lanes:
            ans = ask(ln, body + "\n\nWhat is the next action? One sentence, start with a verb.", 300)
            rows.append({"surface": surface, "lane": ln, "answer": ans[:200]})

    def key(t: str) -> str:
        t = t.lower()
        if re.search(r"filter|exclude|stop.*probe|remove.*chatter", t):
            return "filter probe"
        if re.search(r"dedup|distinct|cluster", t):
            return "dedup"
        if re.search(r"read|consumer|reader|inspect", t):
            return "read/consume"
        if re.search(r"measure|count|audit", t):
            return "measure"
        return "other"
    per = {}
    for surface in SURFACES:
        c = Counter(key(r["answer"]) for r in rows if r["surface"] == surface)
        per[surface] = c.most_common()
    return {"test": "T3", "ok": True, "surface_modal": per,
            "agreement_across_surfaces": len({per[s][0][0] for s in per if per[s]}),
            "rows": rows}


# ── T5 FERMAT: route cost ──────────────────────────────────────────────────
TASKS = {
    "parable": "Write a 100-word parable about a lock that nobody owns. One paragraph.",
    "summary": "Summarise in 5 bullets why a queue can look like a backlog.",
    "code": "Write a Python function that returns True if a path is a stale lock (older than 60s).",
    "census": "Given 2388 open rows, 62.5% probe chatter, what is the live count? Show arithmetic.",
    "synthesis": "In 120 words: what do prohibitions and gates do differently to a language model?",
}


def t5_routes() -> dict:
    rows = []
    for name, prompt in TASKS.items():
        t0 = time.time()
        out_local = local_ask(prompt)
        rows.append({"task": name, "route": "local-7b", "secs": round(time.time() - t0, 1),
                     "chars": len(out_local), "text": out_local[:400],
                     "error": out_local.startswith("__ERR__")})
        for route, ln in (("free", "groq-nacho"), ("paid", "deepseek-flash")):
            t0 = time.time()
            out = ask(ln, prompt, 900)
            rows.append({"task": name, "route": route, "secs": round(time.time() - t0, 1),
                         "chars": len(out), "text": out[:400], "error": not out})
    # blind quality: judge sees only texts, not routes
    judged = []
    for name in TASKS:
        cands = [(r["route"], r["text"]) for r in rows if r["task"] == name and r["text"]]
        if not cands:
            continue
        listing = "\n\n".join(f"[{i+1}] {t}" for i, (_, t) in enumerate(cands))
        verdict = ask("ollama-sd", f"Rate each answer 1-5 for correctness and directness. "
                                   f"Reply as lines like 1=4. No commentary.\n\n{listing}", 300)
        scores = {int(m.group(1)): int(m.group(2))
                  for m in re.finditer(r"(\d+)\s*=\s*(\d)", verdict)}
        for i, (route, _) in enumerate(cands):
            judged.append({"task": name, "route": route, "score": scores.get(i + 1)})
    return {"test": "T5", "ok": True, "runs": rows, "scores": judged}


# ── T6 HALL: intended vs actual reader ────────────────────────────────────
ARTIFACTS = {
    "receipt": "WAVE RECEIPT: 848 decay classifications appended; live backlog 916 of 2,877 (31.8%); "
               "queue file byte-identical before and after. Audit 5/6 green. I5 leaf-set gate still red.",
    "cockpit": "WARN percolator 5/6 gates; live 1517/3478; failing I5\nNEXT [i5-leaf-gate] redesign I5 as leaf-or-declared",
    "census": "QUEUE 2388 open of 3503 rows\n  probe_* chatter 1492 (62.5% of open)\n  live 896\n"
              "  distinct texts 844\n  => real backlog ~750",
}


def t6_readers() -> dict:
    readers = ["groq-nacho", "ollama-sd", "deepseek-flash"]
    rows = []
    for name, body in ARTIFACTS.items():
        for rd in readers:
            ans = ask(rd, f"{body}\n\nYou are reading this cold, with no other context. "
                          f"What action does it imply? One sentence, start with a verb.", 250)
            rows.append({"artifact": name, "reader": rd, "answer": ans[:200]})

    def key(t: str) -> str:
        t = t.lower()
        if re.search(r"fix|redesign|gate|i5", t):
            return "fix the gate"
        if re.search(r"filter|probe|chatter", t):
            return "filter probe"
        if re.search(r"read|consume|build", t):
            return "build consumer"
        if re.search(r"verify|measure|check", t):
            return "verify"
        return "other"
    per = {}
    for name in ARTIFACTS:
        c = Counter(key(r["answer"]) for r in rows if r["artifact"] == name)
        per[name] = c.most_common()
    return {"test": "T6", "ok": True, "per_artifact": per, "rows": rows}


# ── T1 BERNAYS: manufacture demand (artifact + clock) ─────────────────────
def t1_demand() -> dict:
    import json as _json
    q = ROOT / "memory" / "percolator" / "explore.jsonl"
    rows = [_json.loads(l) for l in q.read_text(encoding="utf-8").splitlines() if l.strip()]
    live = [r for r in rows if r.get("status") == "open"
            and not str(r.get("domain") or "").startswith("probe_")][:60]
    out = ROOT / "watch" / "inbox" / "demand_probe_20261024"
    out.mkdir(parents=True, exist_ok=True)
    digest = ["# Demand probe A — digest of 60 live observations", ""]
    for r in live[:40]:
        digest.append(f"- {str(r.get('signal'))[:160]}")
    (out / "A_digest.md").write_text("\n".join(digest), encoding="utf-8")
    spec = ["# Demand probe B — candidate spec from the same 60 rows", "",
            "A candidate is: one distinct live observation, with a citation, a proposed",
            "consumer, and a kill condition. Schema:", "",
            "```json", '{"canonical": "…", "observation": "…", "consumer": "…", "falsifier": "…"}',
            "```", "", "## Sample rows", ""]
    for r in live[:15]:
        spec.append(f"- {str(r.get('signal'))[:120]}")
    (out / "B_spec.md").write_text("\n".join(spec), encoding="utf-8")
    (out / "CLOCK.txt").write_text(
        f"started {datetime.now(timezone.utc).isoformat()}\n"
        "count citations of A_digest vs B_spec in receipts/state/queue hints after 48h\n"
        "control: the 60 rows cited without either artifact\n", encoding="utf-8")
    return {"test": "T1", "ok": True, "rows": len(live), "dir": str(out),
            "artifacts": ["A_digest.md", "B_spec.md"],
            "note": "48h clock started; count with tools/demand_probe_count.py"}


TESTS = {"t1": t1_demand, "t2": t2_inertia, "t3": t3_surface_run,
         "t4": t4_shadow, "t5": t5_routes, "t6": t6_readers}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    args = ap.parse_args(argv)
    names = [args.only] if args.only else list(TESTS)
    results = {}
    for name in names:
        t0 = time.time()
        try:
            res = TESTS[name]()
        except Exception as exc:  # noqa: BLE001
            res = {"test": name.upper(), "ok": False, "error": f"{type(exc).__name__}: {exc}"}
        res["secs"] = round(time.time() - t0, 1)
        write(name, res)
        results[name] = {"ok": res.get("ok"), "secs": res["secs"]}
        print(f"{name}: ok={res.get('ok')} {res['secs']}s")
    write("_index", {"ts": datetime.now(timezone.utc).isoformat(), "results": results})
    return 0


if __name__ == "__main__":
    sys.exit(main())
