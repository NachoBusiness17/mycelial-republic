#!/usr/bin/env python3
"""reverse_map.py - wide-exploration engine: N cheap answers on ONE hard
question, clustered by SOLUTION STRATEGY to mine the tails (F3, 2026-09-30).

Principle (operator: "fifty wide to reverse-map novel solutions from higher
dimensions"): 50 parallel cheap answers on the same hard question sample the
solution space in a way one expensive answer cannot; the novel solutions
live in the tails of the strategy distribution, not the mean. Stages: (1)
question loader (the estate's open problems as data in
configs/reverse_map_questions.json: parity deep-cuts, route open design
questions, the 52-question inventory's NONE-instrument items); (2)
dispatcher (SAME ask to N models in parallel: flash bulk 20-50 wide + prime
judgment + contrast families; temperature varies per shard, ask bytes
identical; call shapes from W8 receipts: qwen3.7-flash 400s on the
reasoning param, ds flash needs thinking-off, duel_harness.py); (3)
analyzer (one funded-tier call clusters BY STRATEGY: same mechanism, not
similar prose; strict JSON, marked lexical fallback); (4) output (strategy
map: head = consensus, tail = minority = the novel candidates; model
composition; spend; under logs/reverse_map/<id>/).

Laws: worst-case projection vs budget cap before any fire; probes drop dead
models (V9 law 5, never rotate a shard mid-run); idempotent resume off
answers.jsonl; every paid dispatch banks cost (RIB_DRIVING_LADDER); no
em-dashes in anything this file writes; free lanes are NOT used - every
shard is the funded Nous tier (sensing never substitutes for judgment).

Usage: tools/reverse_map.py questions | run --question q39_quota_ledger
[--dry | --width 20] | analyze --run-dir logs/reverse_map/<id>
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402 - estate dispatch core (keys, base, metering)

OUT_ROOT = ROOT / "logs" / "reverse_map"
# question bank as data so the bank grows without touching this tool
QUESTIONS_PATH = ROOT / "configs" / "reverse_map_questions.json"
BUDGET_CAP = 3.00          # absolute cap for one run (operator scale, W8 class)
ANSWER_TOKENS = 6000       # bounds flash worst case; answers run 1-2k tokens
ANALYZE_TOKENS = 4500
TEMP_LADDER = [0.5, 0.7, 0.85, 1.0, 1.15]
MINORITY_FRAC = 0.15       # cluster size <= ceil(frac*N) = tail (the novel ones)
PRICES = {  # metered fallbacks, USD per 1M in/out; real metering prefers usage.cost
    "qwen/qwen3.7-flash": (0.13, 0.13), "deepseek/deepseek-v4.1-flash": (0.63, 0.63),  # W8
    "z-ai/glm-5.3-prime": (3.0, 15.0), "openai/gpt-6-luna": (0.10, 0.50),  # dh list, V9
    "google/gemma-4-31b-it": (0.09, 0.34), "mistralai/ministral-3b-2512": (0.10, 0.10),
    "fireworks/ember-1": (0.3, 1.2),
}
FLASH = "qwen/qwen3.7-flash"
FLASH2 = "deepseek/deepseek-v4.1-flash"
PRIME = "z-ai/glm-5.3-prime"
CONTRAST = ["openai/gpt-6-luna", "google/gemma-4-31b-it", "mistralai/ministral-3b-2512"]
# call shape per model: reasoning = capped-reasoning body (dh.call shape),
# plain = body without the reasoning param, ds = reasoning disabled + 8000 cap
SHAPES = {PRIME: "reasoning", FLASH: "plain", FLASH2: "ds", "x-ai/grok-4.3": "reasoning",
          "fireworks/ember-1": "reasoning", "qwen/qwen3.8-max-prime": "reasoning"}
LAWS = ("Laws: no em-dashes in your output. Be concrete: data structures, APIs, "
        "numbers, test predicates. Mark anything uncertain UNPROVEN. No preamble.")
def load_questions() -> dict[str, dict]:
    return json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))

def price_of(model: str) -> tuple[float, float]:
    return PRICES.get(model, dh.PRICE.get(model, (3.0, 15.0)))

def body_for(shape: str, model: str, prompt: str, max_tokens: int, temp: float) -> bytes:
    """Request body per call shape (W8 receipts; see module docstring)."""
    base = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "temperature": temp}
    if shape == "reasoning":
        base["reasoning"] = {"max_tokens": dh.REASONING_CAP}
    elif shape == "ds":
        base["reasoning"], base["max_tokens"] = {"enabled": False}, min(max_tokens, 8000)  # W8 diag 5
    return json.dumps(base).encode()


def call(model: str, prompt: str, key: str, shape: str,
         max_tokens: int, temp: float, timeout: int = 600) -> dict:
    req = urllib.request.Request(
        dh.BASE, data=body_for(shape, model, prompt, max_tokens, temp),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def probe_model(model: str, key: str, known_shape: str | None) -> str | None:
    """Tiny call: liveness + shape autodetect. HTTP 400 on the reasoning
    param demotes to plain; other HTTP errors drop the model (V9 law 5)."""
    for shape in ([known_shape] if known_shape else ["reasoning", "plain"]):
        try:
            call(model, "Reply with the single word ok.", key, shape, 48, 0.2, 120)
            return shape
        except urllib.error.HTTPError as e:
            if e.code == 400 and shape == "reasoning":
                continue
            print(f"probe {model}: HTTP {e.code} shape={shape} -> dropped")
            return None
        except Exception as e:  # noqa: BLE001 - network hiccup, not a verdict
            print(f"probe {model}: inconclusive ({e}) at shape={shape}")
            return None
    return None


def build_fleet(width: int) -> list[dict]:
    """Fleet composition: flash bulk + judgment prime + contrast families."""
    n_contrast = min(3, len(CONTRAST)) if width >= 10 else 1
    n_prime = 2 if width >= 8 else 1
    rest = width - n_contrast - n_prime
    n_ds = max(1, round(rest * 0.2)) if rest >= 5 else 0
    models = [FLASH] * (rest - n_ds) + [FLASH2] * n_ds + [PRIME] * n_prime + CONTRAST[:n_contrast]
    out = []
    for i, model in enumerate(models[:width]):   # judgment tier kept stable
        t = 0.6 if model == PRIME and TEMP_LADDER[i % 5] > 0.7 else TEMP_LADDER[i % 5]
        out.append({"sid": f"s{i+1:02d}", "model": model, "temp": t})
    return out


def worst_case_cost(shards: list[dict], ask_chars: int) -> float:
    return sum((ask_chars / 4 / 1e6) * price_of(s["model"])[0] + (ANSWER_TOKENS / 1e6) * price_of(s["model"])[1] for s in shards)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

class Ledger:
    """answers.jsonl: append-per-shard, resume-safe (W8 cache law)."""

    def __init__(self, path: Path):
        self.path, self.lock, self.rows, self.spent = path, threading.Lock(), {}, 0.0
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    self.rows[row["sid"]] = row
                    self.spent += row.get("cost", 0.0)

    def bank(self, row: dict) -> None:
        with self.lock:
            self.rows[row["sid"]] = row
            self.spent += row.get("cost", 0.0)
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")


def fire_shard(shard: dict, ask: str, keys: list[str], shapes: dict, ledger: Ledger,
               stop_flag: threading.Event) -> None:
    if shard["sid"] in ledger.rows or stop_flag.is_set():
        return
    sid, model, last = shard["sid"], shard["model"], None
    for attempt in (1, 2):
        try:
            t0 = time.time()
            # SW1-03 (SWARM_1.md row 3, kimi+glm converged): hash() is salted
            # per process (PYTHONHASHSEED), so rotation keyed on it picked a
            # different key order every run and retry key choice could not be
            # reasoned about post-hoc. sha256 of f"{sid}:{attempt}" is stable.
            key_idx = int(hashlib.sha256(f"{sid}:{attempt}".encode()).hexdigest(), 16) % len(keys)
            resp = call(model, ask, keys[key_idx],
                        shapes[model], ANSWER_TOKENS, shard["temp"])
            content = (resp.get("choices") or [{}])[0].get("message", {}).get("content") or ""
            cost = dh.cost_of(model, resp.get("usage", {}))
            if not content.strip():
                raise ValueError("empty content")
            row = {"sid": sid, "model": model, "temp": shard["temp"], "ok": True, "content": content,
                   "chars": len(content), "cost": round(cost, 5), "secs": round(time.time() - t0, 1),
                   "ts": now_iso()}
            ledger.bank(row)
            print(f"shard {sid} {model} temp={shard['temp']} ${cost:.4f} {row['secs']}s chars={row['chars']}")
            return
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            time.sleep(2 * attempt)          # provider backoff, then same model
        except Exception as e:  # noqa: BLE001 - shard error is banked, not fatal
            last = str(e)[:200]
    ledger.bank({"sid": sid, "model": model, "temp": shard["temp"], "ok": False,
                 "error": last, "chars": 0, "cost": 0.0, "ts": now_iso()})
    print(f"shard {sid} FAILED: {last}")


def digest_of(row: dict, head_chars: int = 900, tail_chars: int = 250) -> str:
    """Analyzer-visible digest: structure first (headers), then head+tail."""
    text = row.get("content") or ""
    headers = [ln.strip() for ln in text.splitlines() if re.match(r"^\s{0,3}#{1,6}\s+\S", ln)][:12]
    body = re.sub(r"\n{2,}", "\n", text).strip()
    tail = body[-tail_chars:] if len(body) > head_chars + tail_chars else ""
    parts = [f"[sid {row['sid']} model={row['model']} temp={row['temp']} chars={len(text)}]"]
    if headers:
        parts.append("sections: " + " | ".join(h.lstrip('# ') for h in headers))
    parts.append(body[:head_chars] + (("...tail: " + tail) if tail else ""))
    return "\n".join(parts)


ANALYZER_CONTRACT = (
    "Cluster these N answers to ONE design question BY SOLUTION STRATEGY, "
    "not by prose similarity or quality. Two answers share a strategy iff "
    "they would build recognizably the SAME mechanism: same core data "
    "structure or algorithmic idea and the same update rule, even if the "
    "wording differs completely. Different strategy = the mechanisms differ "
    "in kind (e.g. ring-buffer sliding window vs token bucket vs event "
    "sourced replay are THREE strategies). Quality does not matter. OUTPUT "
    "CONTRACT (strict JSON only, no prose, no code fences): "
    "{\"strategies\": [{\"name\": \"<2-4 words>\", \"core_mechanism\": \"<one "
    "sentence naming the actual structure/rule>\", \"answer_ids\": [\"s01\", ...]}], "
    "\"consensus_sketch\": \"<the largest cluster's answer, 2 sentences>\", "
    "\"notes\": \"<under 40 words>\"}. Every sid in exactly one strategy; order "
    "by size descending. No em-dashes.\n\n")


def parse_strategies(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text or "", re.DOTALL)
    try:
        obj = json.loads(m.group(0)) if m else None
        strat = (obj or {}).get("strategies")
        ok = isinstance(strat, list) and strat and all(
            isinstance(s.get("answer_ids"), list) for s in strat)
    except json.JSONDecodeError:
        return None
    return obj if ok else None


LEXICON = ["ring", "bucket", "token", "event.sourc", "replay", "log", "ewma", "counter",
           "window", "heap", "queue", "merkle", "hash chain", "mutex"]


def lexical_fallback(rows: list[dict]) -> list[dict]:
    """Marked fallback: keyword-vote clusters. Never silent (mode recorded)."""
    groups: dict[str, list[str]] = {}
    for r in rows:
        votes = [k for k in LEXICON if k in (r.get("content") or "").lower()]
        key = "+".join(sorted(votes[:2])) or "unlabeled"
        groups.setdefault(key, []).append(r["sid"])
    return [{"name": k, "core_mechanism": f"lexical fallback bucket: {k}", "answer_ids": v}
            for k, v in groups.items()]


def analyze_rows(rows: list[dict], ask: str, keys: list[str], out_dir: Path) -> dict:
    digests = [digest_of(r) for r in rows]
    prompt = (ANALYZER_CONTRACT + "<QUESTION>\n" + ask + "\n</QUESTION>\n\n"
              + "\n\n".join(digests) + "\n\nJSON now.")
    # param MUST be named max_tokens: dh.fire passes it as a keyword (F3 proof)
    judge = lambda m, p, k, max_tokens=0: call(m, p, k, "reasoning", ANALYZE_TOKENS, 0.3)  # noqa: E731
    t0 = time.time()
    text, cost = dh.fire(PRIME, prompt, keys, "analyze", caller=judge)
    parsed = parse_strategies(text)
    strat = parsed["strategies"] if parsed else lexical_fallback(rows)
    mode = "judge" if parsed else "lexical-fallback"
    ids, by_sid = {r["sid"] for r in rows}, {r["sid"]: r for r in rows}
    covered = {i for s in strat for i in s.get("answer_ids", [])}
    for s in strat:
        s["size"] = len(s.get("answer_ids", []))
        s["models"] = sorted({by_sid[i]["model"] for i in s.get("answer_ids", []) if i in by_sid})
    strat.sort(key=lambda s: -s["size"])
    minority = -(-len(rows) * MINORITY_FRAC // 1)  # ceil(frac*N)
    for i, s in enumerate(strat):
        s["is_head"], s["is_tail"] = i == 0 and s["size"] > 1, s["size"] <= minority
    result = {"question_chars": len(ask), "n_answers": len(rows),
              "analyzer_model": PRIME, "analyzer_cost": round(cost, 5),
              "analyzer_secs": round(time.time() - t0, 1), "analyzer_mode": mode,
              "digest_chars": sum(len(d) for d in digests), "orphan_ids": sorted(ids - covered),
              "minority_threshold": minority, "strategies": strat,
              "consensus_sketch": (parsed or {}).get("consensus_sketch", ""),
              "notes": (parsed or {}).get("notes", ""), "ts": now_iso()}
    (out_dir / "analyzer_raw.txt").write_text(text, encoding="utf-8")  # provenance
    return result


def write_map_md(out_dir: Path, qid: str, source: str, res: dict, rows: list[dict],
                 budget: float, spent: float) -> Path:
    lines = [f"# REVERSE MAP {qid} - {res['ts']}", "", f"source: {source}",
             f"answers: {res['n_answers']} ok, cap ${budget:.2f}, spent ${spent:.4f}",
             f"analyzer: {res['analyzer_model']} mode={res['analyzer_mode']} "
             f"cost=${res['analyzer_cost']} digests={res['digest_chars']} tail<= {res['minority_threshold']}", ""]
    for i, s in enumerate(res["strategies"], 1):
        tag = "HEAD" if s.get("is_head") else "TAIL" if s.get("is_tail") else "mid"
        lines += [f"## S{i} {s['name']} - {s['size']} answers - {tag}",
                  f"mechanism: {s.get('core_mechanism', '')}",
                  f"ids: {' '.join(s.get('answer_ids', []))}",
                  f"models: {', '.join(s.get('models', []))}", ""]
    if res.get("consensus_sketch"):
        lines.append(f"consensus (head sketch): {res['consensus_sketch']}")
    if res.get("notes"):
        lines.append(f"notes: {res['notes']}")
    novel = [s for s in res["strategies"] if s.get("is_tail")]
    lines += ["", f"NOVEL CANDIDATES (tail strategies): {len(novel)}"]
    for s in novel:
        ex = next((r for r in rows if r["sid"] in s.get("answer_ids", [])), None)
        extra = f" exemplar {ex['sid']} chars={ex['chars']}" if ex else ""
        lines.append(f"- {s['name']} ({s['size']}) via {', '.join(s.get('models', []))}{extra}")
    if res["orphan_ids"]:
        lines.append(f"orphan ids (analyzer missed): {res['orphan_ids']}")
    p = out_dir / "strategy_map.md"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def run(args: argparse.Namespace) -> int:
    if args.ask_file:
        q = {"source": f"custom ask file {Path(args.ask_file).name}",
             "ask": Path(args.ask_file).read_text(encoding="utf-8")}
    else:
        bank = load_questions()
        if args.question not in bank:
            print(f"unknown question {args.question}; see 'questions'")
            return 2
        q = bank[args.question]
    ask = q["ask"].strip() + "\n\n" + LAWS
    shards = build_fleet(args.width)
    worst = worst_case_cost(shards, len(ask))
    if args.dry:
        fleet = {m: sum(1 for s in shards if s["model"] == m)
                 for m in sorted({s["model"] for s in shards})}
        print(json.dumps({"question": args.question, "width": len(shards), "ask_chars": len(ask),
                          "worst_case_cost": round(worst, 4), "budget_cap": args.budget_cap,
                          "fleet": fleet}, indent=2))
        return 0
    if worst > args.budget_cap:
        print(f"REFUSED: worst-case ${worst:.2f} exceeds cap ${args.budget_cap:.2f}")
        return 2
    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2
    run_id = f"{args.question}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    ledger = Ledger(out_dir / "answers.jsonl")
    shapes = {m: probe_model(m, keys[0], SHAPES.get(m))
              for m in sorted({s["model"] for s in shards})}
    for s in shards:      # dead-model swap happens BEFORE dispatch, never mid-run
        if shapes.get(s["model"]) is None:
            print(f"model {s['model']} dropped: shard falls back to {FLASH}")
            s["model"], s["temp"] = FLASH, min(s["temp"], 1.0)
    shapes.setdefault(FLASH, "plain")
    stop = threading.Event()
    workers = max(1, min(args.concurrency, len(shards)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(fire_shard, s, ask, keys, shapes, ledger, stop) for s in shards]
        for f in concurrent.futures.as_completed(futs):
            f.result()
            if ledger.spent > args.budget_cap:    # first contact = HOLD, not widen
                stop.set()
                print(f"BUDGET HALT at ${ledger.spent:.4f}")
    ok_rows = [r for r in ledger.rows.values() if r.get("ok")]
    meta = {"run_id": run_id, "question": args.question, "source": q["source"], "ask": ask,
            "width": len(shards), "ok": len(ok_rows), "failed": len(ledger.rows) - len(ok_rows),
            "spent": round(ledger.spent, 5), "corr_id": dh.series_corr_id(), "ts": now_iso()}  # AH14
    (out_dir / "run.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    if len(ok_rows) < 6:                   # sample too thin to cluster honestly
        print(f"only {len(ok_rows)} ok answers; banked in {out_dir}")
        return 1
    res = analyze_rows(ok_rows, ask, keys, out_dir)
    (out_dir / "strategy_map.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    spent = ledger.spent + res["analyzer_cost"]
    md = write_map_md(out_dir, args.question, q["source"], res, ok_rows, args.budget_cap, spent)
    novel = sum(1 for s in res["strategies"] if s.get("is_tail"))
    print(f"MAP {md} - {len(res['strategies'])} strategies, novel(tail) {novel}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub_p = p.add_subparsers(dest="cmd", required=True)
    sub_p.add_parser("questions", help="list registry questions + sources")
    r = sub_p.add_parser("run", help="dispatch wide + analyze")
    r.add_argument("--question", default="q39_quota_ledger")
    r.add_argument("--ask-file", help="custom ask text file (overrides --question)")
    r.add_argument("--width", type=int, default=20)
    r.add_argument("--concurrency", type=int, default=20)
    r.add_argument("--budget-cap", type=float, default=BUDGET_CAP)
    r.add_argument("--dry", action="store_true")
    a = sub_p.add_parser("analyze", help="re-analyze banked answers (no re-pay)")
    a.add_argument("--run-dir", type=Path, required=True)
    args = p.parse_args(argv)
    if args.cmd == "questions":
        for qid, qq in load_questions().items():
            print(f"{qid} - {qq['source']}")
        return 0
    if args.cmd == "analyze":
        rd = args.run_dir
        run_json = json.loads((rd / "run.json").read_text(encoding="utf-8"))
        rows = [json.loads(l) for l in (rd / "answers.jsonl").read_text(encoding="utf-8").splitlines()
                if l.strip() and json.loads(l).get("ok")]
        res = analyze_rows(rows, run_json["ask"], dh.load_keys(), rd)
        (rd / "strategy_map.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
        spent = sum(x.get("cost", 0.0) for x in rows) + res["analyzer_cost"]
        print("MAP", write_map_md(rd, run_json["question"], run_json["source"],
                                  res, rows, BUDGET_CAP, spent))
        return 0
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
