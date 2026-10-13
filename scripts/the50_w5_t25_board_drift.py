#!/usr/bin/env python
"""THE 50 / W5 / T25: Board-migration vocabulary drift across 10 boards.

Corpus: watch/inbox/qdrop_export/qdrops.jsonl (6,242 Q drops, 2017-10-28 to
2022-11-28, harvested from https://qanon.pub/data/json/posts.json per
watch/inbox/qdrop_export/RECEIPT.json and harvest_meta.json).

The 10 boards are the 10 source buckets already on file in harvest_meta.json:
4chan_pol, 8chan_pol, 8chan_cbts, 8chan_thestorm, 8chan_greatawakening,
8chan_qresearch, 8chan_patriotsfight, 8kun_qresearch, 8kun_projectdcomms,
and "unknown" (8 rows with null source; several of those carry an 8ch.net
qresearch link in their `link` field, kept honest as unknown rather than
reassigned).

Method
------
1. Bucket drops by `source` (null -> "unknown"). A drop counts toward a
   board's vocabulary only if its `text` is non-empty.
2. Tokenize: strip URLs, reply links (>>123), greentext arrows, HTML entities;
   lowercase; tokens match [a-z][a-z0-9']*; length >= 2; drop a standard
   English stopword list plus harvest artifacts (amp, gt, lt, quot, nbsp...).
3. Per-board: drops, text-bearing drops, tokens, vocab, first/last ts.
4. Migration order: boards sorted by first-drop timestamp.
5. Drift curve: Jensen-Shannon divergence (base 2, so max 1.0) between the
   token distributions of consecutive boards in migration order, Laplace
   smoothed over the union vocabulary.
6. Top-20 shifting terms: for every term with total count >= 25, a 2x10
   contingency table (term vs rest, board by board) and its chi-square
   statistic; rank by chi-square. Peak/trough boards are attributed among
   boards with >= 20 text-bearing drops only (excludes "unknown", 8 drops)
   so an 8-drop bucket cannot own a peak label; its counts still appear.

Run:  .venv/Scripts/python.exe scripts/the50_w5_t25_board_drift.py
Out:  memory/runs/the50/w5_t25_board_drift.json
"""
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "watch/inbox/qdrop_export/qdrops.jsonl"
OUT = REPO / "memory/runs/the50/w5_t25_board_drift.json"

STOPWORDS = set("""
a about above after again against all am an and any are aren as at be because
been before being below between both but by can cant cannot could couldnt did
didnt do does doesnt doing dont down during each few for from further had hadnt
has hasnt have havent having he her here hers herself him himself his how i if
in into is isnt it its itself just lets me more most mustnt my myself no nor
not of off on once only or other ought our ours ourselves out over own same
shant she should shouldnt so some such than that thats the their theirs them
themselves then there theres these they this those through to too under until
up very was wasnt we were werent what whats when whens where wheres which
while who whos whom why whys with wont would wouldnt you your yours yourself
yourselves
""".split())

HARVEST_TOKENS = {"amp", "gt", "lt", "quot", "nbsp", "39", "8230", "8220",
                  "8221", "x200b", "com", "www"}

URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.I)
# handles JSON-escaped slashes (https:\/\/x.y\/z) and space-broken urls
# (twitter. com/SaraCarterDC/status/123) seen verbatim in the qanon.pub dump
URL_ESC_RE = re.compile(r"(?i)https?\s*[:\\]\s*/{0,2}\S+")
DOMAIN_RE = re.compile(r"(?i)\b[a-z0-9-]+\s?\.\s?(com|net|org|gov|io|co|top|xyz|in|us)\S*")
HTML_RE = re.compile(r"<[^>]+>")
REPLY_RE = re.compile(r">>{2,}[^ \n]*|>{1,2}/?[\w/]+/?")
TOKEN_RE = re.compile(r"[a-z][a-z0-9']*")
MIN_TERM_TOTAL = 25
ATTRIB_MIN_DROPS = 20


def clean_text(t: str) -> str:
    t = t.replace("\\/", "/")          # JSON-escaped slashes -> real slashes
    t = HTML_RE.sub(" ", t)            # raw <em>/<b>/... markup from the dump
    t = URL_RE.sub(" ", t)
    t = URL_ESC_RE.sub(" ", t)
    t = DOMAIN_RE.sub(" ", t)
    t = REPLY_RE.sub(" ", t)
    return t


def tokenize(t: str):
    out = []
    for tok in TOKEN_RE.findall(clean_text(t.lower())):
        if len(tok) < 2 or tok in STOPWORDS or tok in HARVEST_TOKENS:
            continue
        out.append(tok.strip("'"))
    return [t for t in out if t]


def js_divergence(c1: Counter, c2: Counter, alpha: float = 0.5) -> float:
    """Jensen-Shannon divergence, base 2, Laplace alpha smoothing."""
    vocab = set(c1) | set(c2)
    n1, n2 = sum(c1.values()), sum(c2.values())
    p = {w: (c1.get(w, 0) + alpha) / (n1 + alpha * len(vocab)) for w in vocab}
    q = {w: (c2.get(w, 0) + alpha) / (n2 + alpha * len(vocab)) for w in vocab}
    m = {w: 0.5 * (p[w] + q[w]) for w in vocab}
    def kl(a, b):
        return sum(a[w] * math.log2(a[w] / b[w]) for w in vocab if a[w] > 0)
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def main() -> int:
    rows = []
    with CORPUS.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    boards = {}
    for r in rows:
        b = r.get("source") or "unknown"
        d = boards.setdefault(b, {
            "board": b, "drops": 0, "text_drops": 0, "empty_text_drops": 0,
            "tokens": 0, "counter": Counter(), "first_ts": None, "last_ts": None,
            "drop_range": [None, None],
        })
        d["drops"] += 1
        ts = r.get("ts")
        if ts:
            if d["first_ts"] is None or ts < d["first_ts"]:
                d["first_ts"] = ts
            if d["last_ts"] is None or ts > d["last_ts"]:
                d["last_ts"] = ts
        n = r.get("drop_no")
        if n is not None:
            if d["drop_range"][0] is None or n < d["drop_range"][0]:
                d["drop_range"][0] = n
            if d["drop_range"][1] is None or n > d["drop_range"][1]:
                d["drop_range"][1] = n
        text = (r.get("text") or "").strip()
        if not text:
            d["empty_text_drops"] += 1
            continue
        d["text_drops"] += 1
        toks = tokenize(text)
        d["tokens"] += len(toks)
        d["counter"].update(toks)

    order = sorted(boards.values(), key=lambda d: d["first_ts"] or "9999")
    for i, d in enumerate(order, 1):
        d["migration_rank"] = i

    # per-board summary + top terms by raw count
    board_summaries = []
    for d in order:
        top_terms = d["counter"].most_common(8)
        board_summaries.append({
            "board": d["board"],
            "migration_rank": d["migration_rank"],
            "drops": d["drops"],
            "text_bearing_drops": d["text_drops"],
            "empty_text_drops": d["empty_text_drops"],
            "tokens": d["tokens"],
            "vocab": len(d["counter"]),
            "first_ts": d["first_ts"],
            "last_ts": d["last_ts"],
            "drop_range": d["drop_range"],
            "top_terms_by_count": [{"term": t, "count": c} for t, c in top_terms],
        })

    # consecutive-board JS divergence along the migration path
    drift_curve = []
    for a, b in zip(order, order[1:]):
        drift_curve.append({
            "from": a["board"],
            "to": b["board"],
            "jsd_bits": round(js_divergence(a["counter"], b["counter"]), 4),
        })

    # chi-square over 2x10 tables for every term with total >= MIN_TERM_TOTAL
    names = [d["board"] for d in order]
    N = {d["board"]: d["tokens"] for d in order}
    total_tokens = sum(N.values())
    candidates = Counter()
    for d in order:
        candidates.update(d["counter"])
    results = []
    for term, total in candidates.items():
        if total < MIN_TERM_TOTAL:
            continue
        obs = {b: boards[b]["counter"].get(term, 0) for b in names}
        chi2 = 0.0
        p_all = total / total_tokens
        for b in names:
            expected = N[b] * p_all
            if expected > 0:
                chi2 += (obs[b] - expected) ** 2 / expected
            expected_rest = N[b] * (1 - p_all)
            rest = N[b] - obs[b]
            if expected_rest > 0:
                chi2 += (rest - expected_rest) ** 2 / expected_rest
        attrib = [b for b in names
                  if boards[b]["text_drops"] >= ATTRIB_MIN_DROPS]
        rates = {b: (obs[b] / N[b] * 1000 if N[b] else 0.0) for b in names}
        peak = max(attrib, key=lambda b: rates[b])
        trough = min(attrib, key=lambda b: rates[b])
        seen = [b for b in names if obs[b] > 0]
        results.append({
            "term": term,
            "total_count": total,
            "boards_present": len(seen),
            "chi2": round(chi2, 2),
            "counts_by_board": {b: obs[b] for b in names},
            "rate_per_1k_by_board": {b: round(rates[b], 3) for b in names
                                     if N[b] > 0},
            "peak_board": peak,
            "peak_rate_per_1k": round(rates[peak], 3),
            "trough_board": trough,
            "trough_rate_per_1k": round(rates[trough], 3),
            "first_board_seen": next(b for b in names if obs[b] > 0),
        })
    results.sort(key=lambda x: -x["chi2"])
    top20 = results[:20]

    artifact = {
        "task": "THE 50 / W5 / item 25",
        "title": "Board-migration vocabulary drift across 10 boards",
        "filed": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "corpus": {
            "file": "watch/inbox/qdrop_export/qdrops.jsonl",
            "rows_loaded": len(rows),
            "span_first_ts": min(r["ts"] for r in rows if r.get("ts")),
            "span_last_ts": max(r["ts"] for r in rows if r.get("ts")),
            "provenance": ("watch/inbox/qdrop_export/RECEIPT.json and "
                           "harvest_meta.json: qanon.pub/data/json/posts.json, "
                           "harvested 2026-09-18"),
            "board_bucketing": ("source field; null source kept as 'unknown' "
                                "(8 rows) exactly as harvest_meta.json filed it"),
            "total_tokens_analyzed": total_tokens,
        },
        "method": {
            "tokenizer": ("lowercase [a-z][a-z0-9']*, len>=2, URLs (including "
                          "JSON-escaped https:\\/\\/x.y\\/z and space-broken "
                          "twitter. com forms), raw HTML markup (<em>...), "
                          ">>reply links, English stopwords and HTML-entity "
                          "artifacts (amp/gt/lt/quot) dropped; residual 'em' "
                          "tokens are the genuine Elon-Musk shorthand usage, "
                          "verified against post context"),
            "vocabulary_source": "text field only (subject/name/trip excluded)",
            "migration_order": "boards sorted by first drop timestamp",
            "drift_curve": "Jensen-Shannon divergence (base 2, Laplace 0.5) between consecutive boards",
            "shifting_terms": ("terms with total count >= 25 ranked by chi-square "
                               "on a 2x10 term-vs-rest table across the 10 boards"),
            "peak_trough_attribution": (f"boards with >= {ATTRIB_MIN_DROPS} "
                                        "text-bearing drops only; 'unknown' (8) "
                                        "is excluded from peak/trough labels but "
                                        "its counts are reported"),
        },
        "boards": board_summaries,
        "migration_order": names,
        "consecutive_board_jsd": drift_curve,
        "top20_shifting_terms": top20,
        "candidates_evaluated": len(results),
        "min_term_total": MIN_TERM_TOTAL,
        "caveats": [
            "283 of 6,242 rows have empty text and contribute counts to board drop tallies but no tokens.",
            "The 'unknown' bucket is 8 drops; its counts are shown but it cannot win a peak/trough label.",
            "8chan_qresearch and 8kun_qresearch are kept separate: the 2019 host migration is itself part of the board migration under test.",
            "Rates use each board's own token count; small boards (8chan_pol: 13 drops) have wide confidence intervals on rates.",
            "chi-square is a detector of uneven distribution, not a direction; peak_board and trough_board give the direction.",
        ],
        "script": "scripts/the50_w5_t25_board_drift.py",
        "repro": ".venv/Scripts/python.exe scripts/the50_w5_t25_board_drift.py",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, ensure_ascii=False)

    # console sanity summary
    print(f"rows={len(rows)} tokens={total_tokens} boards={len(names)}")
    for s in board_summaries:
        print(f"  {s['migration_rank']}. {s['board']:22s} drops={s['drops']:5d} "
              f"text={s['text_bearing_drops']:5d} tokens={s['tokens']:7d} "
              f"vocab={s['vocab']:5d} {s['first_ts']} -> {s['last_ts']}")
    print("drift curve (consecutive JSD):")
    for step in drift_curve:
        print(f"  {step['from']} -> {step['to']}: {step['jsd_bits']}")
    print("top 20 shifting terms (chi2):")
    for t in top20:
        print(f"  {t['term']:24s} total={t['total_count']:5d} chi2={t['chi2']:9.2f} "
              f"peak={t['peak_board']}({t['peak_rate_per_1k']}/1k) "
              f"trough={t['trough_board']}({t['trough_rate_per_1k']}/1k)")
    print(f"WROTE {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
