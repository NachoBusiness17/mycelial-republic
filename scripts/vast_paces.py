"""vast_paces — put the rented GPU through the paces (operator order 09-05:
"really put that 5090 through the paces... serious fun shit that would give us
good data").

Given a live ollama endpoint (the vast box's public port), runs:
  1. MODEL LADDER  — pull + bench qwen2.5:7b, glm4:9b, qwen2.5:32b (3 runs x
     512 tok each): tok/s per size = the Rocinante inference economics row.
  2. CONCURRENCY LADDER — 1 / 4 / 16 parallel 256-tok generations on 7b and 32b:
     aggregate tok/s = the wall-of-256 row at consumer scale.
  3. typed receipts -> state/vast/experiment_receipts.jsonl (append-only).

No teardown here — teardown stays the explicit kill-word. $-safe: box is on the
clock the whole time, so the suite front-loads pulls and prints progress.

  python scripts/vast_paces.py --endpoint http://IP:PORT
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "state" / "vast" / "experiment_receipts.jsonl"
LADDER = ["qwen2.5:7b-instruct-q4_K_M", "glm4:9b-instruct-q4_K_M", "qwen2.5:32b-instruct-q4_K_M"]
PROMPT = "Write a dense paragraph about why verification must be independent of generation."
BENCH_TOKENS = 512
CONC_TOKENS = 256


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _rec(event: str, **kw) -> None:
    row = {"ts": _now(), "event": event, **kw}
    with RECEIPTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    print(json.dumps(row, ensure_ascii=False, default=str)[:320], flush=True)


def _pull(ep: str, model: str) -> None:
    t0 = time.time()
    r = requests.post(f"{ep}/api/pull", json={"name": model, "stream": False},
                      timeout=3600, allow_redirects=False)
    _rec("pull", model=model, seconds=round(time.time() - t0, 1),
         ok=(r.status_code == 200))


def _gen_once(ep: str, model: str, tokens: int) -> dict:
    r = requests.post(f"{ep}/api/generate", json={
        "model": model, "stream": False, "prompt": PROMPT,
        "options": {"num_predict": tokens}}, timeout=900, allow_redirects=False)
    return r.json()


def _bench_model(ep: str, model: str, runs: int = 3) -> dict:
    tps = []
    for _ in range(runs):
        d = _gen_once(ep, model, BENCH_TOKENS)
        n = int(d.get("eval_count") or 0)
        if n and d.get("eval_duration"):
            tps.append(n / (d["eval_duration"] / 1e9))
    med = sorted(tps)[len(tps) // 2] if tps else 0.0
    out = {"model": model, "runs": len(tps), "tok_s_median": round(med, 1),
           "tok_s_all": [round(t, 1) for t in tps]}
    _rec("pace_model", **out)
    return out


def _conc_ladder(ep: str, model: str, levels=(1, 4, 16)) -> list[dict]:
    out = []
    for n in levels:
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=n) as ex:
            ds = list(ex.map(lambda _: _gen_once(ep, model, CONC_TOKENS), range(n)))
        wall = time.time() - t0
        total = sum(int(d.get("eval_count") or 0) for d in ds)
        gen_s = max((float(d.get("eval_duration") or 0) / 1e9) for d in ds) or 1.0
        row = {"model": model, "parallel": n, "wall_s": round(wall, 1),
               "aggregate_tok_s": round(total / wall, 1),
               "single_stream_tok_s": round(total / n / gen_s, 1)}
        out.append(row)
        _rec("pace_concurrency", **row)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", required=True, help="http://IP:PORT of the box's ollama")
    ap.add_argument("--models", type=str, default=",".join(LADDER))
    args = ap.parse_args()
    ep = args.endpoint.rstrip("/")
    models = [m for m in args.models.split(",") if m]

    tags = requests.get(f"{ep}/api/tags", timeout=10, allow_redirects=False)
    if tags.status_code != 200:
        print("endpoint not answering /api/tags — refusing", file=sys.stderr)
        return 2
    _rec("paces_start", endpoint_kind="ollama", models=models)

    results = {}
    for m in models:
        _pull(ep, m)
        results[m] = _bench_model(ep, m)
    # concurrency ladders on the smallest and biggest
    for m in (models[0], models[-1]):
        results[f"{m}#conc"] = _conc_ladder(ep, m)

    _rec("paces_done", summary=json.dumps(results, default=str)[:900])
    return 0


if __name__ == "__main__":
    sys.exit(main())
