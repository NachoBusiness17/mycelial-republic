#!/usr/bin/env python3
"""CACHE KPI v0 (2026-09-22, mickey lane A3) — prompt-cache hit-rate per provider, read
from the estate's usage log, so cache economics become a measured number instead of a
guess. Companion to mag/flight_recorder.py, whose record_call() now normalises cached
tokens across providers (openai cached_tokens / deepseek prompt_cache_hit_tokens /
anthropic cache_read_input_tokens).

Stdlib only. Read-only: this tool never writes, never calls the network, never reads
.env. A row with no cache telemetry is counted as "no telemetry", never as a miss.

LOG SHAPES ACCEPTED (auto-detected per row):
  logs/provider_usage.jsonl  (estate usage log, primary):
    provider, model, prompt_tokens, ok, and cache telemetry under any of
    cache_hit_tokens/cache_miss_tokens, cache_read_tokens (legacy deepseek rows),
    prompt_cache_hit_tokens/prompt_cache_miss_tokens, cached_tokens,
    prompt_tokens_details.cached_tokens, cache_read_input_tokens.
  watch/flight_recorder.jsonl  (flight recorder, via --log or fallback):
    model, in_tok, cached_tok, cache_miss_tok; provider inferred from model prefix
    (marked "inferred:*").

KPI DEFINITIONS (per provider, ok rows only):
  hit_call%  = rows with cached>0 / rows carrying cache telemetry
  tok_hit%   = sum(cached) / sum(denominator), where the denominator is
               (cached + miss) when the vendor splits hit/miss, else prompt_tokens.
               This is the NOMINAL rate: every claimed cached token counts.
  recv_tok   = receipt-verified cached tokens. Only rows stamped by the
               strict-prefix receipt gate (mag/context_checkpoint.py:
               cache_receipt.ok / receipt_ok plus receipt_verified_tokens)
               contribute, clamped to the row's own claimed cached tokens.
  recv_hit%  = recv_tok / same denominator - the USABLE-cache share.
               The tok_hit% vs recv_hit% gap is the claimed-but-unproven
               cache (arXiv 2609.15030: no hit KPI that counts unreceipted
               hits). A row with no receipt verdict counts nominally only.

Usage:
    python tools/cache_kpi.py                     # default log resolution + table
    python tools/cache_kpi.py --since 2026-09     # rows whose ts starts with prefix
    python tools/cache_kpi.py --provider deepseek # one provider
    python tools/cache_kpi.py --json              # machine-readable summary
"""
import argparse
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CANDIDATES = (
    os.path.join(ROOT, "logs", "provider_usage.jsonl"),      # estate usage log (primary)
    os.path.join(ROOT, "watch", "flight_recorder.jsonl"),    # flight recorder (fallback)
)

# provider inference for flight-recorder rows (model prefix -> provider label)
_MODEL_PROVIDER = (
    ("deepseek", "deepseek"), ("claude", "anthropic"), ("gpt-", "openai"),
    ("o1", "openai"), ("o3", "openai"), ("glm", "z_ai"), ("grok", "xai"),
    ("gemini", "gemini"), ("llama", "groq"), ("kimi", "moonshot"),
)


def _first(*vals):
    for v in vals:
        if v is not None:
            return v
    return None


def _nested_cached(details):
    if isinstance(details, dict):
        return details.get("cached_tokens")
    return None


def _extract(row):
    """-> (provider, prompt, cached, miss, ok). Accepts every known log shape."""
    provider = row.get("provider")
    inferred = provider is None
    if inferred:
        model = str(row.get("model") or "?").lower()
        provider = next((p for pre, p in _MODEL_PROVIDER if model.startswith(pre)
                         or (" " + pre) in model), "unknown")
    prompt = _first(row.get("prompt_tokens"), row.get("in_tok"))
    cached = _first(row.get("cache_hit_tokens"), row.get("prompt_cache_hit_tokens"),
                    row.get("cache_read_tokens"), row.get("cache_read_input_tokens"),
                    row.get("cached_tokens"), _nested_cached(row.get("prompt_tokens_details")),
                    row.get("cached_tok"))
    miss = _first(row.get("cache_miss_tokens"), row.get("prompt_cache_miss_tokens"),
                  row.get("cache_miss_tok"))
    return provider, prompt, cached, miss, row.get("ok")


def _ok_verdict(v):
    """Truthy-STRING guard (ouroboros R3 move 7, 2026-10-05): producers may
    stamp the receipt verdict as the string "false"/"true"; bool("false") is
    True, so truthiness counted refused rows as receipted (probe: 2 of 3
    rows). None passthrough; an unparseable string is no verdict, never ok."""
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("true", "1", "yes", "ok"):
            return True
        if s in ("false", "0", "no"):
            return False
    return None


def _receipt(row):
    """-> (ok, verified_tokens); (None, None) when the row carries no receipt verdict.

    Producers that reuse a frozen prefix through the strict-prefix gate
    (mag/context_checkpoint.py gate_skip_recompute) stamp the outcome on the
    usage row: cache_receipt.ok (bool) plus cache_receipt.verified_tokens,
    or the flat receipt_ok / receipt_verified_tokens twins. ok=False means
    the receipt gate REFUSED the reuse (measured rejection); absent means
    the row predates the law or the lane never stamped it - nominal only.
    Verdict values pass through _ok_verdict (string "false" refused, not
    receipted; unparseable strings carry no verdict).
    """
    rcpt = row.get("cache_receipt")
    if isinstance(rcpt, dict):
        ok = rcpt.get("ok")
        verified = rcpt.get("verified_tokens")
    else:
        ok = row.get("receipt_ok")
        verified = None
    ok = _ok_verdict(ok)
    if ok is None:
        return None, None
    verified = _first(verified, row.get("receipt_verified_tokens"))
    return ok, verified


def _denom(prompt, cached, miss):
    """Token denominator for the hit rate: vendor hit/miss split when present, else prompt."""
    if miss is not None:
        return (cached or 0) + (miss or 0)
    return prompt if isinstance(prompt, (int, float)) and prompt > 0 else None


def read_rows(path):
    rows = []
    if not os.path.isfile(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:  # noqa: BLE001 - torn row must not kill the KPI
                continue
    return rows


def resolve_log(explicit=None):
    if explicit:
        return explicit
    for cand in DEFAULT_CANDIDATES:
        if os.path.isfile(cand):
            return cand
    return None


def compute(rows, since=None, provider=None):
    """-> {provider: kpi dict}; rows filtered by ts prefix and provider label first."""
    groups = defaultdict(lambda: {"rows": 0, "err": 0, "cache_rows": 0, "hit_calls": 0,
                                  "prompt_tok": 0, "cached_tok": 0, "miss_tok": 0,
                                  "denom_tok": 0, "no_telemetry": 0,
                                  "receipt_rows": 0, "receipt_ok_rows": 0,
                                  "receipt_tok": 0})
    for row in rows:
        prov, prompt, cached, miss, ok = _extract(row)
        if since and str(row.get("ts", "")) < since:
            continue
        if provider and prov != provider:
            continue
        g = groups[prov]
        g["rows"] += 1
        if ok is False:
            g["err"] += 1
            continue
        has_telemetry = cached is not None or miss is not None
        if not has_telemetry:
            g["no_telemetry"] += 1
            continue
        g["cache_rows"] += 1
        if (cached or 0) > 0:
            g["hit_calls"] += 1
        g["prompt_tok"] += prompt or 0
        g["cached_tok"] += cached or 0
        g["miss_tok"] += miss or 0
        r_ok, r_tok = _receipt(row)
        if r_ok is not None:
            g["receipt_rows"] += 1
            if r_ok:
                g["receipt_ok_rows"] += 1
                # verified tokens can never claim more cache than the row
                # itself claimed: clamp to the nominal cached count
                verified = r_tok if isinstance(r_tok, (int, float)) else (cached or 0)
                if cached is not None:
                    verified = min(verified, cached or 0)
                g["receipt_tok"] += verified
        d = _denom(prompt, cached, miss)
        if d:
            g["denom_tok"] += d
    for prov, g in groups.items():
        g["hit_call_rate"] = round(g["hit_calls"] / g["cache_rows"], 4) if g["cache_rows"] else None
        g["tok_hit_rate"] = round(g["cached_tok"] / g["denom_tok"], 4) if g["denom_tok"] else None
        g["tok_hit_receipted_rate"] = (round(g["receipt_tok"] / g["denom_tok"], 4)
                                       if g["denom_tok"] else None)
        g["unreceipted_tok"] = g["cached_tok"] - g["receipt_tok"]
    return dict(groups)


def _fmt_rate(r):
    return "%.1f%%" % (r * 100) if r is not None else "n/a"


def main(argv=None):
    ap = argparse.ArgumentParser(description="prompt-cache hit-rate KPI per provider")
    ap.add_argument("--log", help="usage JSONL path (default: logs/provider_usage.jsonl, "
                                  "then watch/flight_recorder.jsonl)")
    ap.add_argument("--since", help="only rows whose ts starts with this prefix")
    ap.add_argument("--provider", help="restrict to one provider label")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args(argv)

    path = resolve_log(args.log)
    if not path:
        sys.stderr.write("cache_kpi: NO USAGE LOG FOUND — looked for:\n  %s\n"
                         % "\n  ".join(DEFAULT_CANDIDATES))
        return 1
    if not os.path.isfile(path):
        sys.stderr.write("cache_kpi: log not found: %s\n" % path)
        return 1

    rows = read_rows(path)
    kpis = compute(rows, since=args.since, provider=args.provider)
    total = {"rows": 0, "err": 0, "cache_rows": 0, "hit_calls": 0,
             "prompt_tok": 0, "cached_tok": 0, "miss_tok": 0, "denom_tok": 0,
             "no_telemetry": 0, "receipt_rows": 0, "receipt_ok_rows": 0,
             "receipt_tok": 0}
    for g in kpis.values():
        for k in total:
            total[k] += g[k]
    total["hit_call_rate"] = (round(total["hit_calls"] / total["cache_rows"], 4)
                              if total["cache_rows"] else None)
    total["tok_hit_rate"] = (round(total["cached_tok"] / total["denom_tok"], 4)
                             if total["denom_tok"] else None)
    total["tok_hit_receipted_rate"] = (round(total["receipt_tok"] / total["denom_tok"], 4)
                                       if total["denom_tok"] else None)
    total["unreceipted_tok"] = total["cached_tok"] - total["receipt_tok"]

    if args.json:
        print(json.dumps({"log": path, "since": args.since, "provider": args.provider,
                          "providers": kpis, "TOTAL": total}, indent=2))
        return 0

    print("=== cache_kpi: %s | rows=%d | provider=%s | since=%s ===" % (
        os.path.basename(path), len(rows), args.provider or "*", args.since or "*"))
    hdr = "%-18s %7s %5s %10s %9s %9s %12s %11s %11s %9s %9s %9s" % (
        "provider", "rows", "err", "cache_rows", "hit_call%", "no_tel", "prompt_tok",
        "cached_tok", "miss_tok", "tok_hit%", "recv_tok", "recv_hit%")
    print(hdr)
    order = sorted(kpis, key=lambda p: -kpis[p]["rows"])
    for prov in order:
        g = kpis[prov]
        print("%-18s %7d %5d %10d %9s %9d %12d %11d %11d %9s %9d %9s" % (
            prov[:18], g["rows"], g["err"], g["cache_rows"], _fmt_rate(g["hit_call_rate"]),
            g["no_telemetry"], g["prompt_tok"], g["cached_tok"], g["miss_tok"],
            _fmt_rate(g["tok_hit_rate"]), g["receipt_tok"],
            _fmt_rate(g["tok_hit_receipted_rate"])))
    print("%-18s %7d %5d %10d %9s %9d %12d %11d %11d %9s %9d %9s" % (
        "TOTAL", total["rows"], total["err"], total["cache_rows"],
        _fmt_rate(total["hit_call_rate"]), total["no_telemetry"], total["prompt_tok"],
        total["cached_tok"], total["miss_tok"], _fmt_rate(total["tok_hit_rate"]),
        total["receipt_tok"], _fmt_rate(total["tok_hit_receipted_rate"])))
    if not kpis:
        print("no rows matched (since=%s provider=%s)" % (args.since or "*", args.provider or "*"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
