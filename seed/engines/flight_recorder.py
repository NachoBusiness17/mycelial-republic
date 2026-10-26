#!/usr/bin/env python3
"""FLIGHT RECORDER — every model call becomes one typed telemetry row.

Standalone stdlib module (no estate imports). Steal-shape rebuild of the flight-recorder
pattern: it WRAPS a call, it never changes call semantics. Fail-open by contract: a
telemetry error prints loudly to stderr and NEVER breaks the wrapped call.

ROW SCHEMA — JSONL append (default <seed>/watch/flight_recorder.jsonl), one row per call:
  {"ts", "lane", "model", "subsystem", "latency_ms", "status", "error_code",
   "in_tok", "out_tok", "cached_tok", "cache_miss_tok", "credits_est"}
  - status      "ok" | "error" (percentiles in summarize() use ok rows only)
  - error_code  vendor code, "HTTP<status>", or exception class name; None when ok
  - in/out/cached_tok  normalized across provider usage shapes (see _extract_tokens);
                None when the wrapped fn returns no usage block
  - credits_est computed ONLY from a caller-supplied rates dict
                ({"in_per_ktok","out_per_ktok","cached_per_ktok"}). NEVER hardcoded here.
  Keys/credentials are never logged and never written to any row — the recorder only
  ever holds the function you hand it. Key lookups belong to your one door (keys.py),
  not to this module.

Usage:
    status, result = record_call(chat_fn, "api", "glm-x-flash", "probe",
                                 rates=RATES["glm-x-flash"], model="glm-x-flash", prompt="hi")
    summarize(subsystem="probe")   # count / p50 / p95 / ok-rate / tokens / credits

Offline self-test (no network, no keys):
    python engines/flight_recorder.py
"""
from __future__ import annotations

import json
import math
import os
import sys
import threading
import time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG = os.path.join(ROOT, "watch", "flight_recorder.jsonl")
ROW_FIELDS = ("ts", "lane", "model", "subsystem", "latency_ms", "status", "error_code",
              "in_tok", "out_tok", "cached_tok", "cache_miss_tok", "credits_est")
_LOCK = threading.Lock()  # JSONL appends are lock-serialized (callers may be threaded)


# ---------------------------------------------------------------- row construction

def _utcnow() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (now.microsecond // 1000)


def _interpret(result):
    """-> (status, error_code, usage_dict). Accepts a parsed JSON dict (preferred), a
    legacy (http_status, latency, code) tuple, or anything (treated as ok)."""
    status, error_code, usage = "ok", None, {}
    if isinstance(result, dict):
        usage = result.get("usage") or {}
        err = result.get("error")
        if err:
            status = "error"
            if isinstance(err, dict):
                error_code = err.get("code", str(err.get("message", "unknown"))[:64])
            else:
                error_code = str(err)[:64]
    elif isinstance(result, (tuple, list)) and result and isinstance(result[0], int):
        status = "ok" if 200 <= result[0] < 300 else "error"
        if status == "error":
            error_code = result[2] if len(result) > 2 and result[2] is not None else "HTTP%d" % result[0]
    return status, error_code, usage


def _extract_tokens(usage):
    """-> (in_tok, out_tok, cached_tok, cache_miss_tok), normalized across providers.
    cached_tok = first non-None of:
      openai    usage.prompt_tokens_details.cached_tokens (or flat usage.cached_tokens)
      deepseek  usage.prompt_cache_hit_tokens   (its miss twin -> cache_miss_tok)
      anthropic usage.cache_read_input_tokens
    in/out_tok fall back to anthropic input_tokens/output_tokens so cache share stays
    computable on every vendor. Unknown shapes -> (None, None, None, None)."""
    if not isinstance(usage, dict):
        return None, None, None, None
    in_tok = usage.get("prompt_tokens")
    if in_tok is None:
        in_tok = usage.get("input_tokens")            # anthropic
    out_tok = usage.get("completion_tokens")
    if out_tok is None:
        out_tok = usage.get("output_tokens")          # anthropic
    details = usage.get("prompt_tokens_details")
    cached = None
    for cand in (details.get("cached_tokens") if isinstance(details, dict) else None,
                 usage.get("cached_tokens"),          # openai flat variant
                 usage.get("prompt_cache_hit_tokens"),    # deepseek
                 usage.get("cache_read_input_tokens")):   # anthropic
        if cand is not None:
            cached = cand
            break
    miss = usage.get("prompt_cache_miss_tokens")      # deepseek; None elsewhere
    return in_tok, out_tok, cached, miss


def _credits_est(in_tok, out_tok, cached_tok, rates):
    """credits = ((in-cached)*in_rate + cached*cached_rate + out*out_rate) / 1000.
    Missing cached rate defaults to the input rate (conservative). No rates -> None."""
    if not in_tok and not out_tok:
        return None
    in_rate = float(rates.get("in_per_ktok", 0) or 0)
    out_rate = float(rates.get("out_per_ktok", 0) or 0)
    cached_rate = float(rates.get("cached_per_ktok", in_rate) or in_rate)
    cached = cached_tok or 0
    billable_in = max((in_tok or 0) - cached, 0)
    return round((billable_in * in_rate + cached * cached_rate + (out_tok or 0) * out_rate) / 1000.0, 9)


def _emit(row, log_path=None):
    """Fail-open append: telemetry errors are loudly reported on stderr, never raised."""
    try:
        path = log_path or DEFAULT_LOG
        d = os.path.dirname(path)
        if d and not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
        line = json.dumps({k: row.get(k) for k in ROW_FIELDS}, ensure_ascii=True)
        with _LOCK:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
    except Exception as e:  # noqa: BLE001 - fail-open by design
        sys.stderr.write("[flight_recorder] EMIT FAILED (call result unaffected): %r\n" % (e,))


def record_call(fn, lane, model, subsystem, /, rates=None, log_path=None, **call_kwargs):
    """Wrap ONE call: run it, time it, emit a typed row, return (status, result).

    lane/model/subsystem are POSITIONAL-ONLY so a wrapped fn may keep its own
    model=/lane=/subsystem= kwarg without collision. rates and log_path belong to the
    recorder; every other kwarg is forwarded to fn untouched. If fn raises, the error
    row is emitted and the exception re-raises — the recorder observes, never swallows.
    """
    t0 = time.perf_counter()
    try:
        result = fn(**call_kwargs)
    except Exception as e:  # noqa: BLE001 - re-raised after the row is written
        latency_ms = round((time.perf_counter() - t0) * 1000.0, 1)
        code = ("HTTP%s" % e.code) if getattr(e, "code", None) else type(e).__name__
        _emit({"ts": _utcnow(), "lane": lane, "model": model, "subsystem": subsystem,
               "latency_ms": latency_ms, "status": "error", "error_code": code,
               "in_tok": None, "out_tok": None, "cached_tok": None,
               "cache_miss_tok": None, "credits_est": None}, log_path)
        raise
    latency_ms = round((time.perf_counter() - t0) * 1000.0, 1)
    status, error_code, usage = _interpret(result)
    in_tok, out_tok, cached_tok, cache_miss_tok = _extract_tokens(usage)
    est = _credits_est(in_tok, out_tok, cached_tok, rates) if rates else None
    _emit({"ts": _utcnow(), "lane": lane, "model": model, "subsystem": subsystem,
           "latency_ms": latency_ms, "status": status, "error_code": error_code,
           "in_tok": in_tok, "out_tok": out_tok, "cached_tok": cached_tok,
           "cache_miss_tok": cache_miss_tok, "credits_est": est}, log_path)
    return status, result


# ---------------------------------------------------------------- summarize

def _read_rows(log_path=None):
    path = log_path or DEFAULT_LOG
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
            except Exception:  # noqa: BLE001 - a torn row must not kill the summary
                continue
    return rows


def _pctl(sorted_xs, q):
    if not sorted_xs:
        return None
    idx = max(0, min(len(sorted_xs) - 1, int(math.ceil(q * len(sorted_xs))) - 1))
    return sorted_xs[idx]


def _agg(rows):
    lat = sorted(r["latency_ms"] for r in rows if r.get("status") == "ok"
                 and isinstance(r.get("latency_ms"), (int, float)))
    ok = sum(1 for r in rows if r.get("status") == "ok")
    return {
        "count": len(rows), "ok": ok,
        "ok_rate": round(ok / len(rows), 4) if rows else None,
        "p50_ms": _pctl(lat, 0.50), "p95_ms": _pctl(lat, 0.95),
        "in_tok": sum(r.get("in_tok") or 0 for r in rows),
        "out_tok": sum(r.get("out_tok") or 0 for r in rows),
        "cached_tok": sum(r.get("cached_tok") or 0 for r in rows),
        "credits_est": round(sum(r.get("credits_est") or 0 for r in rows), 9),
    }


def summarize(subsystem=None, since=None, log_path=None, out=None):
    """Per-lane / per-model / per-subsystem: count, p50/p95 (ok rows only), ok-rate,
    token totals, credits. `since` = ISO timestamp or prefix ("2026-09-25T09").
    Returns the summary dict and prints the same table."""
    out = out or sys.stdout
    rows = _read_rows(log_path)
    if since:
        rows = [r for r in rows if str(r.get("ts", "")) >= since]
    if subsystem:
        rows = [r for r in rows if r.get("subsystem") == subsystem]
    total = _agg(rows)
    out.write("=== flight_recorder: %s | rows=%d | subsystem=%s since=%s ===\n" % (
        os.path.basename(log_path or DEFAULT_LOG), total["count"], subsystem or "*", since or "*"))
    out.write("TOTAL: n=%d ok=%.1f%% p50=%sms p95=%sms in=%s out=%s cached=%s credits=%s\n" % (
        total["count"], (total["ok_rate"] or 0) * 100, total["p50_ms"], total["p95_ms"],
        total["in_tok"], total["out_tok"], total["cached_tok"], total["credits_est"]))
    summary = {"total": total, "by_lane": {}, "by_model": {}, "by_subsystem": {}}
    for dim, key in (("by_lane", "lane"), ("by_model", "model"), ("by_subsystem", "subsystem")):
        groups = {}
        for r in rows:
            groups.setdefault(r.get(key) or "?", []).append(r)
        out.write("-- %s --\n" % dim)
        for name in sorted(groups):
            a = _agg(groups[name])
            summary[dim][name] = a
            out.write("  %-22s n=%-4d ok=%6.1f%% p50=%-7s p95=%-7s in=%-8s out=%-7s cached=%-8s credits=%s\n" % (
                str(name)[:22], a["count"], (a["ok_rate"] or 0) * 100,
                a["p50_ms"], a["p95_ms"], a["in_tok"], a["out_tok"], a["cached_tok"], a["credits_est"]))
    return summary


# ---------------------------------------------------------------- offline self-test

def _self_test():
    """No network, no keys: a fake provider function runs through record_call under all
    three usage shapes + the failure paths; rows and summary are byte-checked."""
    import tempfile
    log = os.path.join(tempfile.mkdtemp(prefix="flight_recorder_selftest_"), "fr.jsonl")

    def vendor_openai(prompt="", model="m", cached=0):
        return {"choices": [], "usage": {"prompt_tokens": 1000, "completion_tokens": 100,
                "prompt_tokens_details": {"cached_tokens": cached}}}

    def vendor_deepseek(prompt="", model="m", **kw):
        return {"usage": {"prompt_tokens": 1000, "completion_tokens": 100,
                "prompt_cache_hit_tokens": 400, "prompt_cache_miss_tokens": 600}}

    def vendor_anthropic(prompt="", model="m", **kw):
        return {"usage": {"input_tokens": 1000, "output_tokens": 100,
                "cache_read_input_tokens": 250}}

    def vendor_error(prompt="", model="m", **kw):
        return {"error": {"code": 1302, "message": "rate limited"}}

    def vendor_boom(prompt="", model="m", **kw):
        raise RuntimeError("transport down")

    rates = {"in_per_ktok": 0.1, "out_per_ktok": 0.3, "cached_per_ktok": 0.05}
    checks = []

    # openai shape: in 1000 / out 100 / cached 300 ->
    # credits = ((1000-300)*0.1 + 300*0.05 + 100*0.3)/1000 = 0.115
    st, _ = record_call(vendor_openai, "api", "m-openai", "selftest",
                        prompt="x", model="m", cached=300, rates=rates, log_path=log)
    checks.append(("openai status ok", st == "ok"))
    row = _read_rows(log)[-1]
    checks.append(("openai tokens", (row["in_tok"], row["out_tok"], row["cached_tok"]) == (1000, 100, 300)))
    checks.append(("openai credits", abs(row["credits_est"] - 0.115) < 1e-9))

    # deepseek shape: cached 400 -> credits = (600*0.1 + 400*0.05 + 100*0.3)/1000 = 0.110
    st, _ = record_call(vendor_deepseek, "api", "m-ds", "selftest", prompt="x",
                        rates=rates, log_path=log)
    row = _read_rows(log)[-1]
    checks.append(("deepseek cached", row["cached_tok"] == 400 and row["cache_miss_tok"] == 600))
    checks.append(("deepseek credits", abs(row["credits_est"] - 0.110) < 1e-9))

    # anthropic shape: in/out fall back to input/output tokens; cached 250
    st, _ = record_call(vendor_anthropic, "api", "m-anth", "selftest", prompt="x",
                        rates=rates, log_path=log)
    row = _read_rows(log)[-1]
    checks.append(("anthropic fallback", (row["in_tok"], row["out_tok"], row["cached_tok"]) == (1000, 100, 250)))

    # vendor error body -> error row, no raise
    st, _ = record_call(vendor_error, "api", "m-err", "selftest", prompt="x", log_path=log)
    row = _read_rows(log)[-1]
    checks.append(("error row", st == "error" and row["error_code"] == 1302))

    # fn raises -> error row emitted, exception re-raised
    raised = False
    try:
        record_call(vendor_boom, "api", "m-boom", "selftest", prompt="x", log_path=log)
    except RuntimeError:
        raised = True
    row = _read_rows(log)[-1]
    checks.append(("raise re-raised + row", raised and row["status"] == "error"
                   and row["error_code"] == "RuntimeError"))

    # fail-open: unwritable log path prints loudly, never breaks the call
    st, _ = record_call(vendor_openai, "api", "m", "selftest", prompt="x", model="m",
                        log_path=os.path.join("NUL:", "x", "y", "fr.jsonl")
                        if os.name == "nt" else "/proc/self/x/fr.jsonl")
    checks.append(("fail-open emit", st == "ok"))

    # summarize math over the good log: 3 ok rows, 2 error rows, in_tok 3000 total
    # (the fail-open row was emitted to the broken path, not here)
    s = summarize(log_path=log, out=sys.stderr)
    checks.append(("summary count", s["total"]["count"] == 5 and s["total"]["ok"] == 3))
    checks.append(("summary tokens", s["total"]["in_tok"] == 3000))

    bad = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print("  %-24s %s" % (name, "PASS" if ok else "FAIL"))
    print("flight_recorder self-test: %d/%d PASS" % (len(checks) - len(bad), len(checks)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(_self_test())
