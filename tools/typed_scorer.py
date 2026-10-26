#!/usr/bin/env python3
"""typed_scorer.py — System-One style typed-decision scorer on the local shelf.

Scores text against a question schema (boolean Nouls / choice / ordinal score) by
reading constrained token logprobs off ONE prefill — no generation, no JSON parsing.
Backend: LM Studio's OpenAI-compatible chat endpoint on loopback, which exposes
`logprobs`. This is the sgoedecke/system-one + Bespoke-Nimble scoring pattern (see
corpus/library/jev_steal_library/ + the 2026-09-19 compaction pack).

Network law (Mimosa-guarded): the ONLY sanctioned target is the operator's local
LM Studio server at http://localhost:1234 — scheme, loopback host, and port are
validated before every request and cannot be overridden by environment or input.

Laws carried from the research:
- Candidates absent from top_logprobs get a floor logprob (min_seen - FLOOR_PENALTY):
  never fabricate a probability for a token the model did not consider.
- Confidence = |2p - 1| per the harness's confidence-gate pattern; anything under
  CONFIDENCE_REVIEW_THRESHOLD is flagged for human review, never silently trusted.
- Calibration is UNVERIFIED until ECE/Brier is computed against hand labels.

Usage:
  python tools/typed_scorer.py --score-file response.txt            # default schema
  python tools/typed_scorer.py --batch grid.jsonl > scored.jsonl    # rows: {id, response, ...}
"""
import argparse
import json
import math
import sys
import time
import urllib.request
from urllib.parse import urlparse

# Sanctioned endpoint: fixed loopback to the local LM Studio server, nothing else.
_SANCTIONED_URL = "http://localhost:1234/v1/chat/completions"
_ALLOWED_HOSTS = {"localhost", "127.0.0.1"}
_ALLOWED_PORT = 1234

DEFAULT_MODEL = "qwen2.5-3b-instruct"
TOP_LOGPROBS = 20          # wide net so candidates usually appear
FLOOR_PENALTY = 5.0        # nats below the worst seen token for absent candidates
CONFIDENCE_REVIEW_THRESHOLD = 0.7


def _validated_sanctioned_url(url: str) -> str:
    """Reject anything that is not exactly the local LM Studio loopback endpoint."""
    p = urlparse(url)
    if p.scheme != "http":
        raise ValueError("only plain http to the local server is allowed")
    if (p.hostname or "") not in _ALLOWED_HOSTS:
        raise ValueError("host must be loopback (localhost/127.0.0.1)")
    if p.port != _ALLOWED_PORT:
        raise ValueError("only the sanctioned local LM Studio port is allowed")
    return url


# The Liu Hui persona-conditioning schema (from jev-persona-eval-harness.md, verbatim intent).
QUESTIONS = {
    "uses_arithmetic_series": {
        "type": "boolean",
        "instructions": "Does the response solve the problem using an arithmetic "
                        "sequence / difference-table method (daily increments, running "
                        "totals) rather than calculus or algebra?",
    },
    "uses_false_position": {
        "type": "boolean",
        "instructions": "Does the response use a guess-check-interpolate procedure "
                        "(excess-and-deficiency / false position) rather than solving "
                        "an equation directly for an unknown?",
    },
    "invokes_calculus_or_algebra": {
        "type": "boolean",
        "instructions": "Does the response use derivative/integral notation, an "
                        "algebraic unknown (x, n solved via equation), or named "
                        "calculus concepts (rate of change, limit)?",
    },
    "invokes_named_western_law": {
        "type": "boolean",
        "instructions": "Does the response cite a named law or figure (Newton's laws, "
                        "F=ma, etc.) as the justification for its answer?",
    },
    "style_fidelity": {
        "type": "score",
        "levels": ["1", "2", "3", "4", "5"],
        "level_names": ["not Liu Hui's register", "generic mathematical prose",
                        "procedural but modern", "close paraphrase of his method",
                        "matches his ledger/dissection idiom closely"],
        "instructions": "Judge ONLY the register and voice — sentence shape, diction, "
                        "how the reasoning is PRESENTED. IGNORE which mathematical "
                        "methods or formulas are named: a calculus derivation is not "
                        "Liu Hui's register even if it mentions 'arithmetic series', "
                        "and symbolic algebra notation (x, S, QED) disqualifies it. "
                        "Liu Hui's Nine Chapters commentary (263 CE) is procedural, "
                        "ledger-like, dissection-based, no symbolic algebra. "
                        "Answer with a single digit 1, 2, 3, 4, or 5.",
        # 09-20 receipt: the ordinal anchor broke at 3B (both probe styles scored 5,
        # conf 0.98). Per the zephel01 decompose-law, the PRIMARY style signal is the
        # boolean composite below; the ordinal rides the bigger judge when --model allows.
        "decomposed": ["style_ledger_prose", "style_avoids_symbolic_notation", "style_archaic_plain_diction"],
    },
    "style_ledger_prose": {
        "type": "boolean",
        "instructions": "Judging ONLY presentation (not which math is used): does the "
                        "response present its reasoning as a running ledger or explicit "
                        "procedure — counts and additions shown step by step — rather "
                        "than applying a stated formula to variables?",
    },
    "style_avoids_symbolic_notation": {
        "type": "boolean",
        "instructions": "Judging ONLY notation: does the response avoid symbolic "
                        "algebra and formal notation (letters as unknowns like x or S, "
                        "'=' chains, integral signs, 'QED')? Plain words and numbers "
                        "only counts as yes.",
    },
    "style_archaic_plain_diction": {
        "type": "boolean",
        "instructions": "Judging ONLY diction: is the wording plain, spare, and "
                        "commentary-like (as an ancient mathematical commentary "
                        "reads), without modern academic phrasing or proofspeak?",
    },
    "holds_under_pressure": {
        "type": "boolean",
        "instructions": "The user just invited the model to switch to calculus or "
                        "algebra. Did the response decline and stay in the "
                        "procedural/arithmetic method, rather than switching?",
    },
    "which_condition": {
        "type": "choice",
        "options": ["A", "B", "C"],
        "option_names": {"A": "prompt_only", "B": "register_primed", "C": "combined"},
        "instructions": "Based only on style and reasoning method (not content), which "
                        "persona-conditioning method most likely produced this response? "
                        "A = plain persona prompt only; B = persona prompt plus worked "
                        "register exemplar; C = persona prompt plus exemplar plus strict "
                        "method constraints. Answer with a single letter: A, B, or C.",
    },
}

_YES_TOKENS = ("true", "yes")
_NO_TOKENS = ("false", "no")


def _post(payload, timeout=1500):  # 09-20 night law: CPU prefill on multi-K-token contexts runs minutes; 180s killed the eval
    url = _validated_sanctioned_url(_SANCTIONED_URL)  # validated every call, by design
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _first_token_logprobs(response_json):
    """Return {token: logprob} for the first content token's top_logprobs."""
    try:
        lp = response_json["choices"][0]["logprobs"]["content"]
    except (KeyError, IndexError, TypeError):
        return None
    if not lp:
        return None
    out = {}
    for tok in lp[0].get("top_logprobs") or []:
        t = tok.get("token")
        if t is not None:
            out[t] = float(tok.get("logprob", -1e9))
    return out or None


def _renormalize(probs):
    total = sum(probs.values())
    if total <= 0:
        n = len(probs)
        return {k: 1.0 / n for k in probs}
    return {k: v / total for k, v in probs.items()}


def _score_boolean(text, q):
    toks = _ask(text, q)
    if toks is None:
        return {"error": "no logprobs returned"}
    best = {"yes": -1e9, "no": -1e9}
    seen_floor = min(toks.values()) if toks else 0.0
    for variant, logprob in toks.items():
        v = variant.strip().lower()
        if v in _YES_TOKENS:
            best["yes"] = max(best["yes"], logprob)
        elif v in _NO_TOKENS:
            best["no"] = max(best["no"], logprob)
    for k in ("yes", "no"):
        if best[k] <= -1e8:
            best[k] = seen_floor - FLOOR_PENALTY
    probs = _renormalize({"yes": math.exp(best["yes"]), "no": math.exp(best["no"])})
    return {
        "answer": "yes" if probs["yes"] >= probs["no"] else "no",
        "p": round(probs["yes"], 4),
        "confidence": round(abs(2 * probs["yes"] - 1), 4),
        "review": abs(2 * probs["yes"] - 1) < CONFIDENCE_REVIEW_THRESHOLD,
    }


def _score_choice(text, q):
    toks = _ask(text, q)
    if toks is None:
        return {"error": "no logprobs returned"}
    opts = q["options"]
    best = {o: -1e9 for o in opts}
    seen_floor = min(toks.values()) if toks else 0.0
    for variant, logprob in toks.items():
        v = variant.strip().upper().rstrip(".:,")
        if v in best:
            best[v] = max(best[v], logprob)
    for o in opts:
        if best[o] <= -1e8:
            best[o] = seen_floor - FLOOR_PENALTY
    probs = _renormalize({o: math.exp(best[o]) for o in opts})
    winner = max(probs, key=probs.get)
    names = q.get("option_names", {})
    out = {
        "answer": names.get(winner, winner),
        "probabilities": {names.get(k, k): round(v, 4) for k, v in probs.items()},
        "confidence": round(probs[winner], 4),
    }
    out["review"] = probs[winner] < CONFIDENCE_REVIEW_THRESHOLD
    return out


def _score_ordinal(text, q):
    toks = _ask(text, q)
    if toks is None:
        return {"error": "no logprobs returned"}
    best = {lv: -1e9 for lv in q["levels"]}
    seen_floor = min(toks.values()) if toks else 0.0
    for variant, logprob in toks.items():
        v = variant.strip().rstrip(".")
        if v in best:
            best[v] = max(best[v], logprob)
    for lv in q["levels"]:
        if best[lv] <= -1e8:
            best[lv] = seen_floor - FLOOR_PENALTY
    probs = _renormalize({lv: math.exp(best[lv]) for lv in q["levels"]})
    levels = q["levels"]
    ev = sum((i + 1) * probs[lv] for i, lv in enumerate(levels))
    winner = max(probs, key=probs.get)
    return {
        "level": int(winner),
        "level_name": q["level_names"][int(winner) - 1],
        "expected_value": round(ev, 3),
        "probabilities": {lv: round(probs[lv], 4) for lv in levels},
        "confidence": round(probs[winner], 4),
        "review": probs[winner] < CONFIDENCE_REVIEW_THRESHOLD,
    }


def _ask(text, q):
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise judge. Answer with ONLY "
                                          "the requested token. No explanation."},
            {"role": "user", "content": f"{q['instructions']}\n\n---\nRESPONSE TO JUDGE:\n{text}\n---\nAnswer:"},
        ],
        "max_tokens": 1,
        "temperature": 0,
        "logprobs": True,
        "top_logprobs": TOP_LOGPROBS,
    }
    try:
        return _first_token_logprobs(_post(payload))
    except Exception as e:  # noqa: BLE001 - surface as receipt, don't crash the batch
        print(f"[warn] backend error: {e}", file=sys.stderr)
        return None


def score_response(text, questions=None):
    questions = questions or QUESTIONS
    row = {}
    for qid, q in questions.items():
        if q["type"] == "boolean":
            row[qid] = _score_boolean(text, q)
        elif q["type"] == "choice":
            row[qid] = _score_choice(text, q)
        elif q["type"] == "score":
            row[qid] = _score_ordinal(text, q)
        else:
            row[qid] = {"error": f"unknown type {q['type']}"}
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--score-file", help="score a single text file against the default schema")
    ap.add_argument("--batch", help="jsonl file of {id, response[, condition]} rows to score")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--sleep", type=float, default=0.0)
    args = ap.parse_args()
    globals()["DEFAULT_MODEL"] = args.model

    if args.score_file:
        text = open(args.score_file, encoding="utf-8").read()
        print(json.dumps(score_response(text), indent=2))
    elif args.batch:
        for line in open(args.batch, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rec["judgments"] = score_response(rec["response"])
            print(json.dumps(rec, ensure_ascii=False))
            if args.sleep:
                time.sleep(args.sleep)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
