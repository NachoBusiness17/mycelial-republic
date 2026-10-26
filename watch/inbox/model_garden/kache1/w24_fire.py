"""KACHE-1 PART B: the Z.AI 24-wide single-family concurrent flash test.

Operator order: "z.ai allows 50 concurrent flash - launch 24 at once in a
window" - verify the claim cheaply by stagger-firing 24 concurrent
glm-5.3-flash asks (the B6-shape frozen format ask, identical contracts)
through the gated garden runner (tools/model_garden.run_ask), measuring
first-attempt land rate, latency distribution, and any 429s.

Laws honored: gated rail only (plan_call applies the glm-5.3-flash recipe:
thinking enabled + reasoning_effort low, uncapped per the row-17 law; the
operator-remembered 12000 cap is superseded by the gate and the ask.json
carries 12000 as a no-op floor the recipe overrides), evidence preflight,
per-attempt telemetry at the transport layer, serialized ledger appends,
width-table law (first contact = HOLD signal, no width cut mid-run).
$0 staging; metered spend banked per fire in the usage ledger.
"""
from __future__ import annotations

import json
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import tools.model_garden as mg  # noqa: E402

W24 = ROOT / "watch" / "inbox" / "model_garden" / "kache1" / "w24"
QUEUE = W24 / "q"
N = 24
CONTRACT = ("Reply with EXACTLY these 3 lines and nothing else: no markdown "
            "fences, no text before or after, no trailing spaces.\n\n"
            "BATTERY-ACK garden v1\nB1,B2,B3,B4,B5,B6,B7,B8\nEND")
EVIDENCE = "memory/plans/garden_battery/series/cheapgrid1/_frozen/B6_ASK_TEXT.md"

TL = threading.local()
TEL: list[dict] = []
RESULTS: list[dict] = []
LOCK = threading.Lock()
BANK_LOCK = threading.Lock()
SPEND = {"cost": 0.0, "rows": 0}
ORIG_BANK = mg._bank


def locked_bank(row: dict) -> None:
    with BANK_LOCK:
        ORIG_BANK(row)
        if str(row.get("id", "")).startswith("kache1-w24-"):
            SPEND["cost"] += float(row.get("cost_usd", 0) or 0)
            SPEND["rows"] += 1


def tel_call(model, messages, max_tokens, key, base_url, retries=1,
             extra_body=None):
    """The runner's _call with per-attempt telemetry (same fence, same
    retry-once-after-20s estate shape)."""
    url, host = mg._endpoint(base_url)
    mg._assert_public_host(host)
    body: dict = {"model": model, "messages": messages}
    if max_tokens is not None:
        body["max_tokens"] = max_tokens
    if extra_body:
        body.update(extra_body)
    data = json.dumps(body).encode("utf-8")
    last = None
    for attempt in (1, 2):
        t0 = time.time()
        try:
            req = urllib.request.Request(
                url, data=data, method="POST",
                headers={"Authorization": "Bearer " + key,
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as r:
                resp = json.loads(r.read())
            _tel(attempt, t0, "ok")
            return resp
        except urllib.error.HTTPError as exc:
            snippet = ""
            try:
                snippet = exc.read()[:200].decode("utf-8", "replace")
            except Exception:  # noqa: BLE001
                pass
            _tel(attempt, t0, f"http-{exc.code}", status=exc.code,
                 snippet=snippet)
            last = exc
        except Exception as exc:  # noqa: BLE001
            _tel(attempt, t0, "transport", err=repr(exc)[:200])
            last = exc
        if attempt == 1:
            time.sleep(20)
    raise RuntimeError(f"w24 transport failed after 2 tries: {last!r}")


def _tel(attempt: int, t0: float, outcome: str, status=None, snippet="",
         err="") -> None:
    row = {"ask": getattr(TL, "ask_id", "?"), "attempt": attempt,
           "latency_s": round(time.time() - t0, 2), "outcome": outcome}
    if status is not None:
        row["http_status"] = status
    if snippet:
        row["snippet"] = snippet
    if err:
        row["err"] = err
    with LOCK:
        TEL.append(row)


def stage() -> None:
    for i in range(1, N + 1):
        d = QUEUE / f"k{i:02d}"
        d.mkdir(parents=True, exist_ok=True)
        meta = {
            "id": f"kache1-w24-K{i:02d}",
            "battery": "kache-e1-w24 (PART B width probe)",
            "axis": "concurrency-width-probe",
            "model": "glm-5.3-flash",
            "base_env": "ZAI_API_KEY_Pro",
            "base_url": "https://api.z.ai/api/coding/paas/v4",
            "evidence": [EVIDENCE],
            "contract": CONTRACT,
            "revision": False,
            "max_tokens": 12000,
            "rail_note": ("gated rail: plan_call applies the glm-5.3-flash "
                          "recipe (thinking enabled + reasoning_effort low, "
                          "uncapped per row-17 law); the 12000 here is the "
                          "operator-remembered cap, overridden by the gate"),
        }
        (d / "ask.json").write_text(json.dumps(meta, indent=1),
                                    encoding="utf-8")


def worker(d: Path, meta_id: str, stagger: float, gate: threading.Event) -> None:
    gate.wait()
    time.sleep(stagger)
    TL.ask_id = meta_id
    t0 = time.time()
    try:
        row = mg.run_ask(d)
        res = {"id": meta_id, "ok": True,
               "run_s": round(time.time() - t0, 2), "row": row}
    except Exception as exc:  # noqa: BLE001
        res = {"id": meta_id, "ok": False,
               "run_s": round(time.time() - t0, 2), "err": repr(exc)[:300]}
    with LOCK:
        RESULTS.append(res)


def main() -> None:
    mg._bank = locked_bank
    mg._call = tel_call
    stage()
    # offline preflight sanity: one dry run (evidence render + shape checks)
    dry = mg.run_ask(QUEUE / "k01", execute=False)
    print("[dry] k01 preflight ok:", json.dumps(dry)[:200], flush=True)
    rng = random.Random(20261002)
    gate = threading.Event()
    threads = []
    t_fire = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    for i in range(1, N + 1):
        d = QUEUE / f"k{i:02d}"
        th = threading.Thread(target=worker,
                              args=(d, f"kache1-w24-K{i:02d}",
                                    round(rng.uniform(0.0, 2.0), 2), gate))
        th.start()
        threads.append(th)
    gate.set()
    print(f"[fire] {N} threads released at {t_fire} (stagger 0-2s)", flush=True)
    for th in threads:
        th.join()
    first = {}
    for row in TEL:
        if row["attempt"] == 1:
            first[row["ask"]] = row
    lat = sorted(r["latency_s"] for r in first.values() if r["outcome"] == "ok")
    ok_first = sum(1 for r in first.values() if r["outcome"] == "ok")
    retries = [r for r in TEL if r["attempt"] == 2]
    codes = {}
    for r in TEL:
        codes[r["outcome"]] = codes.get(r["outcome"], 0) + 1
    summary = {
        "schema": "kache.w24_summary.v1",
        "fire_moment": t_fire,
        "n": N,
        "asks_landed_ok": sum(1 for r in RESULTS if r["ok"]),
        "first_attempt_lands": ok_first,
        "first_attempt_failures": {a: r["outcome"] for a, r in first.items()
                                   if r["outcome"] != "ok"},
        "retry_events": len(retries),
        "retry_detail": retries,
        "outcome_histogram": codes,
        "latency_first_ok_s": {"min": lat[0] if lat else None,
                               "median": lat[len(lat) // 2] if lat else None,
                               "p90": lat[int(len(lat) * 0.9)] if lat else None,
                               "max": lat[-1] if lat else None,
                               "n": len(lat)},
        "metered_cost_usd": round(SPEND["cost"], 4),
        "ledger_rows": SPEND["rows"],
        "results": RESULTS,
        "telemetry": TEL,
    }
    out = W24 / "telemetry.json"
    out.write_text(json.dumps(summary, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    slim = {k: v for k, v in summary.items()
            if k not in ("results", "telemetry", "retry_detail")}
    print(json.dumps(slim, indent=1), flush=True)


if __name__ == "__main__":
    main()
