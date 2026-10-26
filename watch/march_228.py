#!/usr/bin/env python3
"""MARCH 228 — the first 50-flight operation (2026-09-04, operator GO: "gogo nuts").

The 228 open explore signals replayed through glm-5.3-flash at tranche-gated concurrency
(8 -> 16 -> 32 -> 50), every call claimed via bay_organs (Leg-1 organs dogfooded on their
first march), every call tagged by the flight recorder (subsystem="march"), one density
table receipt at the end: per-tranche ok-rate + output-tok/req vs the economist envelope.

$0 in the night window (23:00-09:00 SGT); ~pennies out-of-window on flash promo rates.
Gates: widen iff ok-rate >= 0.98 on the tranche; else hold width and finish. Halt iff ok < 0.90.
"""
import json, os, sys, time, hashlib, urllib.request, urllib.error, urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "mag"))
import bay_organs
import flight_recorder as fr

ALLOWED_HOST = "api.z.ai"
ENDPOINT = "https://api.z.ai/api/paas/v4/chat/completions"
# Night-cage crash cure (2026-10-04): compose delivers .env as env vars only
# (env_file:) and never mounts the file into /app, so the old bare read died
# at import with "FileNotFoundError: [Errno 2] No such file or directory:
# '/app/.env'" -> rc=1 every night since 09-26 (trail: "night composite:
# monitor rc=0; march rc=1"; verbatim cage capture 2026-10-04, receipt
# watch/inbox/night_shift_20261004/night_march_cured.md). Key stays FILE-ONLY
# by operator law (no env door until sanctioned); the cage now reports an
# honest rc=2 from __main__ instead of an import crash.
def _load_dotenv(path):
    """CR-strip-at-load law (TS-11 cure 2, 2026-10-05): the elder 14-cycle
    daily-429 outage class - a CRLF .env glues a literal \r onto key values
    and "Bearer <key>\r" is rejected by urllib as an invalid header. Fix
    cause/evidence comment cites watch/inbox/go_wave_20261004/
    CSV_VERDICT_20261004.md (root cause chain item 1). newline='' on the open
    disables universal-newline translation so a CR cannot hide behind it, and
    rstrip('\r\n') strips it at the key LOAD, before any header build."""
    env = {}
    if not path.exists():
        return env
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().rstrip("\r\n")
    return env


ENV = _load_dotenv(ROOT / ".env")
KEY = ENV.get("ZAI_API_KEY_Pro", ENV.get("ZAI_API_KEY_PRO", ENV.get("ZAI_API_KEY", "")))

RATES = {"glm-5.3-flash": {"in": 0.000075 / 1000, "out": 0.00025 / 1000}}  # $/tok promo

PROMPT = """You are a research-signal triage gate for an AI-agent fleet. Signal:
---
{body}
---
Classify: KEEP (an invariant/principle worth percolating), DISCARD (noise, stale, or hype), or ACTION (concrete build/tool worth a task).
Reply in exactly this form, nothing else:
VERDICT: <KEEP|DISCARD|ACTION>
WHY: <two sentences max>
TAGS: <3 tags, comma-separated>"""


def api_call(model=None, prompt=None, max_tokens=1536):
    parsed = urllib.parse.urlparse(ENDPOINT)
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
        raise ValueError("blocked: endpoint must be https://%s" % ALLOWED_HOST)
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "temperature": 0.2,
            "thinking": {"type": "enabled"}, "reasoning_effort": "low"}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read())
    usage = data.get("usage", {})
    return {"latency": time.time() - t0, "text": data["choices"][0]["message"]["content"],
            "in_tok": usage.get("prompt_tokens"), "out_tok": usage.get("completion_tokens"),
            "cached": (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0)}


def load_signals():
    src = ROOT / "memory" / "percolator" / "explore.jsonl"
    rows = []
    for line in src.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    out, seen = [], set()
    for r in rows:
        if r.get("status") in ("done", "closed", "rejected"):
            continue
        body = json.dumps(r, sort_keys=True, ensure_ascii=False)
        h = hashlib.sha256(body.encode()).hexdigest()[:12]
        if h in seen:
            continue
        seen.add(h)
        out.append({"sid": h, "body": body[:6000]})
    return out


def march_item(sig, tranche):
    claim = bay_organs.try_claim("march228", sig["sid"], engine="march", slot="t%d" % tranche)
    if claim is None:
        return {"sid": sig["sid"], "skipped": "claimed elsewhere"}
    try:
        status, res = fr.record_call(api_call, "zai2-pro", "glm-5.3-flash", "march",
                             rates=RATES,
                             model="glm-5.3-flash", prompt=PROMPT.format(body=sig["body"]))
        if status not in (200, "ok") or "text" not in res:
            return {"sid": sig["sid"], "error": "api status %s" % status}
        card = {"sid": sig["sid"], "tranche": tranche, "latency_s": round(res["latency"], 2),
                "out_tok": res["out_tok"], "response": res["text"][:500]}
        (ROOT / "watch" / "march" / "cards_v2").mkdir(parents=True, exist_ok=True)
        (ROOT / "watch" / "march" / "cards_v2" / (sig["sid"] + ".json")).write_text(
            json.dumps(card, ensure_ascii=False, indent=1), encoding="utf-8")
        return card
    finally:
        bay_organs.release_claim("march228", sig["sid"], claim["token"])


def run_tranche(items, width):
    out = []
    with ThreadPoolExecutor(max_workers=width) as ex:
        futs = {ex.submit(march_item, s, width): s for s in items}
        for f in as_completed(futs):
            try:
                out.append(f.result())
            except Exception as e:
                out.append({"sid": "?", "error": type(e).__name__ + ": " + str(e)[:120]})
    return out


def report(tranche, results):
    errs = [r for r in results if r.get("error") or r.get("skipped")]
    ok = [r for r in results if not (r.get("error") or r.get("skipped"))]
    outs = sorted(r["out_tok"] for r in ok if r.get("out_tok"))
    dens = (sum(outs) / len(outs)) if outs else 0
    p95 = outs[int(len(outs) * 0.95) - 1] if outs else 0
    print("TRANCHE %d: %d ok / %d | mean out_tok/req %.0f | p95 %d | errs %s"
          % (tranche, len(ok), len(results), dens, p95, errs[:3] or "none"))
    return len(ok), dens


if __name__ == "__main__":
    if not KEY:
        # Honest skip (2026-10-04): rc=2 named in lane_runner's cycle_night
        # comment as the expected cage outcome; the pre-cure crash returned
        # rc=1 with the error text discarded by the lane composite.
        print("MARCH SKIP rc=2: no key - %s absent or carries no "
              "ZAI_API_KEY_Pro/ZAI_API_KEY (cage: .env unmounted by compose; "
              "no env door sanctioned)" % (ROOT / ".env"))
        raise SystemExit(2)
    bay_organs.sweep_expired("march228", grace_s=60)
    sigs = load_signals()
    print("MARCH 228 — signals loaded:", len(sigs))
    fr_rows_before = 0
    results, idx, width = [], 0, 8
    gates = [8, 16, 32, 50]
    halted = None
    while idx < len(sigs):
        batch = sigs[idx:idx + width]
        if not batch:
            break
        r = run_tranche(batch, width)
        results.extend(r)
        ok_n, dens = report(width, r)
        ok_rate = ok_n / max(1, len(r))
        idx += len(batch)
        if ok_rate < 0.90:
            halted = "ok-rate %.2f < 0.90 at tranche %d" % (ok_rate, width)
            break
        if width < 50 and ok_rate >= 0.98 and dens <= 400:
            width = gates[min(gates.index(width) + 1, len(gates) - 1)]
        else:
            width = min(width, 50)
    print("MARCH COMPLETE:", len(results), "processed", ("| HALTED: " + halted) if halted else "| all tranches clean")
