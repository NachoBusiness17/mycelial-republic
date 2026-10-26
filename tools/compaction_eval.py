#!/usr/bin/env python3
"""compaction_eval.py — context-compaction eval per the hermes PR #116246 bar, on a
REAL fleet trajectory (memory/trajectory/steps.jsonl).

The bar (from the 2026-09-19 compaction pack):
  1. matched budgets + a recency null (keep-recent-N) that any learned arm must beat
  2. closed-book recall exams over the real transcript, per-question
  3. threshold/mechanism ablation (report the scorer's keep-rate — Jev's 100%-drop
     degeneracy is the cautionary tale)
  4. retained-bytes economics per arm

Arms:
  recency  — keep the tail up to budget (the null)
  scorer   — typed boolean "keep this exchange for the standing task?" over the older
             region (tools/typed_scorer.py law: constrained logprobs, floor for absent
             candidates, confidence flags), tail always kept
  summary  — fold the older region into one summary via the local shelf + tail verbatim

Deterministic question generation (no model in the loop): facts are (question, answer)
pairs built from rows in the to-be-dropped region whose command output contains a
distinctive number or identifier; the answer must NOT appear in the kept tail.

Usage:
  python tools/compaction_eval.py --transcript memory/trajectory/steps.jsonl \
      --rows 600 --budget-chars 8000 --out memory/runs/compaction_eval/
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from typed_scorer import _post, _first_token_logprobs, _renormalize  # noqa: E402
from config import ROOT  # noqa: E402

_REPO_ROOT = os.path.realpath(str(ROOT))


def _safe_path(p: str) -> str:
    """Contain user-supplied paths inside the repo; reject traversal out of it."""
    resolved = os.path.realpath(os.path.join(_REPO_ROOT, p))
    if os.path.commonpath([_REPO_ROOT, resolved]) != _REPO_ROOT:
        raise ValueError(f"path escapes repo root: {p}")
    return resolved

CHAT_URL = "http://localhost:1234/v1/chat/completions"
GEN_MODEL = "qwen2.5-3b-instruct"
JUDGE_MODEL = "qwen2.5-3b-instruct"


def _validated(url):
    p = urlparse(url)
    if p.scheme != "http" or (p.hostname or "") not in {"localhost", "127.0.0.1"} or p.port != 1234:
        raise ValueError("only the sanctioned local LM Studio loopback endpoint is allowed")
    return url


def generate(messages, model=GEN_MODEL, max_tokens=400):
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens,
               "temperature": 0.2, "stream": False}
    import time as _time
    last_err = None
    for attempt in range(4):  # 09-20 receipt: 400s when another job swaps models mid-load
        try:
            return _post(payload)["choices"][0]["message"]["content"]
        except Exception as e:  # noqa: BLE001
            last_err = e
            _time.sleep(5 * (attempt + 1))
    raise last_err


def load_transcript(path, rows):
    out = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            res = d.get("result") or {}
            output = ""
            if isinstance(res, dict):
                output = str(res.get("output", res.get("stdout", "")) or "")
            elif res is not None:
                output = str(res)
            cmd = str(d.get("command") or d.get("face") or "?")
            out.append({
                "i": len(out),
                "ts": d.get("ts", ""),
                "face": d.get("face", "?"),
                "command": cmd[:200],
                "output": output[:600],
            })
    return out[-rows:]


def keep_score(row, standing_task):
    """Typed boolean via the same constrained-logprob law as typed_scorer."""
    q = {"type": "boolean",
         "instructions": "The standing task is described first. Then a tool exchange from "
                         "an agent session. Would this exchange be needed again to continue "
                         "the standing task (contains its commands, results, ids, or "
                         "decisions)? Answer only true or false."}
    text = f"STANDING TASK: {standing_task}\n\nEXCHANGE [{row['face']}] {row['command']}\nresult: {row['output'][:300]}"
    payload = {
        "model": JUDGE_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise judge. Answer with ONLY true or false."},
            {"role": "user", "content": f"{q['instructions']}\n\n---\n{text}\n---\nAnswer:"},
        ],
        "max_tokens": 1, "temperature": 0, "logprobs": True, "top_logprobs": 20,
    }
    toks = None
    last_err = None
    import time as _time
    for attempt in range(4):  # retry across model-swap races
        try:
            toks = _first_token_logprobs(_post(payload))
            break
        except Exception as e:  # noqa: BLE001
            last_err = e
            _time.sleep(5 * (attempt + 1))
    if toks is None:
        if last_err:
            print(f"[warn] scorer retry exhausted: {last_err}", file=sys.stderr)
        return 0.5, True
    best = {"yes": -1e9, "no": -1e9}
    floor = min(toks.values())
    for tok, lp in toks.items():
        v = tok.strip().lower()
        if v in ("true", "yes"):
            best["yes"] = max(best["yes"], lp)
        elif v in ("false", "no"):
            best["no"] = max(best["no"], lp)
    for k in ("yes", "no"):
        if best[k] <= -1e8:
            best[k] = floor - 5.0
    p = _renormalize({"yes": __import__("math").exp(best["yes"]),
                      "no": __import__("math").exp(best["no"])})["yes"]
    return p, abs(2 * p - 1) < 0.7


def build_questions(transcript, tail_idx, n_questions=15):
    """Closed-book questions from the dropped region. v2 laws (STAGED_RUN_RECEIPT_20260920):
    number from row OUTPUT only (never the command); unique command prefixes; question
    grounded in a redacted output excerpt (answer never shown); discriminators only."""
    qs = []
    seen_prefixes = set()
    tail_blob = " ".join(r["command"] + r["output"] for r in transcript[tail_idx:])
    for row in transcript[:tail_idx]:
        prefix = row["command"][:80]
        if prefix in seen_prefixes:
            continue
        out = row["output"] or ""
        for m in re.finditer(r"\b\d[\d,]{2,}\b", out):
            ans = m.group(0).replace(",", "")
            if ans in tail_blob or ans in prefix:
                continue  # in tail = not a discriminator; in prefix = leaked by the question
            start, end = max(0, m.start() - 110), min(len(out), m.end() + 110)
            excerpt = out[start:end].replace(m.group(0), "____").replace("\n", " ").strip()
            seen_prefixes.add(prefix)
            qs.append({
                "q": (f"In the session record, a step ran `{prefix}` and its result included "
                      f"this passage: \"...{excerpt}...\". What number fills the blank? "
                      f"Answer with the number only."),
                "a": ans,
                "source_idx": row.get("i"),
            })
            break
        if len(qs) >= n_questions:
            break
    return qs


def sanity_gate(model):
    """Judge must pass one fixed verbatim-fact probe before any exam is legal.
    Synthetic record — deterministic, no dependence on transcript contents."""
    ctx = ("The workshop log entry: the kiln fired for 14 hours and consumed 2847 kilograms "
           "of softwood; the apprentice noted the temperature held steady. A separate ledger "
           "row recorded delivery of 96 tiles and the invoice number 55-2091.")
    q = ("A log passage reads: \"...the kiln fired for 14 hours and consumed ____ kilograms of "
         "softwood...\". What number fills the blank? Answer with the number only.")
    ans_text = closed_book(ctx, q, model)
    ok = "2847" in ans_text.replace(",", "")
    return ok, {"probe_answer": ans_text.strip()[:60], "expected": "2847"}


def closed_book(context, question, model):
    msg = [
        {"role": "system", "content": "Answer ONLY from the provided session record. "
                                      "If it is not present, say 'unknown'."},
        {"role": "user", "content": f"SESSION RECORD:\n{context}\n\nQUESTION: {question}"},
    ]
    return generate(msg, model=model, max_tokens=60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", default="memory/trajectory/steps.jsonl")
    ap.add_argument("--rows", type=int, default=600)
    ap.add_argument("--budget-chars", type=int, default=8000)
    ap.add_argument("--tail", type=int, default=20)
    ap.add_argument("--out", default="memory/runs/compaction_eval")
    ap.add_argument("--skip-scorer", action="store_true")
    ap.add_argument("--arms", default="recency,scorer,summary",
                    help="comma subset of recency,scorer,summary for staged runs")
    args = ap.parse_args()

    args.out = _safe_path(args.out)
    args.transcript = _safe_path(args.transcript)
    os.makedirs(args.out, exist_ok=True)
    arms_requested = [a.strip() for a in args.arms.split(",") if a.strip()]

    T = load_transcript(args.transcript, args.rows)
    print(f"[transcript] {len(T)} rows loaded")

    # Standing task = what the tail is doing (the LiteLLM 'latest question' analog).
    standing_task = " | ".join(r["command"][:60] for r in T[-3:])
    print(f"[standing task] {standing_task[:160]}")

    def row_text(r):
        return f"[{r['face']}] {r['command']}\n{r['output']}"

    tail = T[-args.tail:]
    tail_chars = sum(len(row_text(r)) for r in tail)

    # --- recency arm (the null) ---
    recency = list(tail)
    used = tail_chars
    for r in reversed(T[:-args.tail]):
        t = row_text(r)
        if used + len(t) > args.budget_chars:
            break
        recency.insert(0, r)
        used += len(t)
    recency_ctx = "\n\n".join(row_text(r) for r in recency)

    # --- scorer arm ---
    if "scorer" not in arms_requested:
        scorer_ctx, keep_rate = None, None
    elif args.skip_scorer:
        scorer_ctx, keep_rate = recency_ctx, None
    else:
        kept, scored, flags = [], 0, 0
        budget = args.budget_chars - tail_chars
        for r in T[:-args.tail]:
            p, review = keep_score(r, standing_task)
            scored += 1
            flags += review
            t = row_text(r)
            if p >= 0.5 and sum(len(x) for x in kept) + len(t) <= budget:
                kept.append(r)
        keep_rate = len(kept) / max(scored, 1)
        scorer_ctx = "\n\n".join(row_text(r) for r in kept) + "\n\n" + "\n\n".join(row_text(r) for r in tail)
        print(f"[scorer] scored {scored}, kept {len(kept)} (keep-rate {keep_rate:.0%}), "
              f"{flags} low-confidence rows flagged")

    # --- summary arm ---
    if "summary" in arms_requested:
        older = T[:-args.tail]
        older_blob = "\n\n".join(row_text(r) for r in older)[:20000]
        summary = generate([
            {"role": "system", "content": "You compress an agent session record for a future "
                                          "continuation. Keep every command, number, id, decision, "
                                          "and error. Terse ledger, no prose."},
            {"role": "user", "content": f"SESSION RECORD:\n{older_blob}\n\nCOMPRESSED LEDGER:"},
        ], max_tokens=600)
        summary_ctx = summary + "\n\n" + "\n\n".join(row_text(r) for r in tail)
    else:
        summary, summary_ctx = None, None

    # --- questions from the dropped region (vs recency arm's cutoff) ---
    tail_start_idx = len(T) - args.tail
    gate_ok, gate_detail = sanity_gate(JUDGE_MODEL)
    print(f"[sanity] judge {'PASS' if gate_ok else 'FAIL'} {gate_detail}")
    if not gate_ok:
        print("[sanity] judge failed verbatim-fact probe — no arm comparison is legal; aborting")
        return
    qs = build_questions(T, tail_start_idx)
    print(f"[questions] {len(qs)} closed-book from dropped region (v2)")

    arms = {}
    if "recency" in arms_requested:
        arms["recency"] = recency_ctx
    if "scorer" in arms_requested and scorer_ctx is not None:
        arms["scorer"] = scorer_ctx
    if "summary" in arms_requested and summary_ctx:
        arms["summary"] = summary_ctx

    results = {arm: [] for arm in arms}
    for arm, ctx in arms.items():
        for i, qa in enumerate(qs):
            ans = closed_book(ctx[: args.budget_chars * 3], qa["q"], JUDGE_MODEL)
            hit = qa["a"] in ans.replace(",", "")
            results[arm].append({"q": i, "hit": hit, "expected": qa["a"], "said": ans.strip()[:80]})
        print(f"[{arm}] recall {sum(r['hit'] for r in results[arm])}/{len(qs)}, ctx {len(ctx)} chars")

    out = {
        "transcript": args.transcript, "rows": len(T), "budget_chars": args.budget_chars,
        "keep_rate_scorer": keep_rate, "questions": qs, "results": results,
        "summary_ledger": summary,
    }
    with open(os.path.join(args.out, "eval_20260920.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"[out] {args.out}/eval_20260920.json")


if __name__ == "__main__":
    main()
