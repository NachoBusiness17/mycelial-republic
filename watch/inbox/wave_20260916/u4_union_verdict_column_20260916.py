"""u4_union_verdict_column_20260916 -- SOLO judgment column: 3 verdict questions x 10 seeds
through stealth/union-alpha (OpenRouter), temperature ladder 0.2 x3 / 0.8 x4 / 1.3 x3.

Mission (operator, verbatim excerpt): "the solo judgment column for the night's three
verdicts — 3 questions × 10 seeds, temperature ladder (0.2 ×3, 0.8 ×4, 1.3 ×3), through
stealth/union-alpha". Questions verbatim from receipts/D23_SALON50_NIGHT_RESULTS.md
(question_digest lineage d12721eea078491b). Receipt:
watch/inbox/wave_20260916/receipts/U4_UNION_VERDICT_COLUMN.md (written BEFORE any call).

Plumbing: imports LANES/_now from mag/research_fanout UNMODIFIED; key via
mag.flight_recorder.load_env (never printed, never in a row); own urllib call mirroring
the D23 driver (SSRF allowlist + resolved-IP guard). Repo code untouched. $0 — union-alpha
is a TIME-BOXED free stealth lane; 402/403/paid-signal => append row and STOP.

Wave-lane law: rows append to raw.jsonl AS THEY LAND; failures preserved as rows.
Schema: u4_verdict_column.v1
"""
from __future__ import annotations

import ipaddress, json, socket, sys, threading, time, urllib.parse, urllib.request, urllib.error, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "mag"))
from research_fanout import LANES, _now          # repo tooling, unmodified
from flight_recorder import load_env, guard_endpoint  # repo tooling, unmodified

OUT = ROOT / "memory" / "runs" / "u4_union_verdict_column_20260916"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

LANE_ID = "or-union-alpha"          # TIME-BOXED free stealth lane (registered in LANES)
ALLOWED_BASES = {"https://openrouter.ai/api/v1"}
ALLOWED_HOSTS = {"openrouter.ai"}   # repo guard_endpoint takes HOSTNAMES (probe-caught bug #1)

# MISSION VERBATIM question set (identical strings to D23 — registered in the receipt)
QUESTIONS = [
    ("Q1-sampler-verdict",
     "A measurement found that decorrelation between free-LLM lanes does NOT predict answer "
     "quality (rho +0.33, wrong-signed, replicated). Does this kill the analogy that "
     "multi-model salons are thermodynamic samplers, or can it be saved by redefining the "
     "ensemble? Take a side, under 120 words."),
    ("Q2-extropic-seat",
     "A vendor claims 140x energy efficiency for thermodynamic sampling hardware and "
     "publishes a simulator + open weights, but no silicon measurements. What is the "
     "strongest falsification protocol a $0-budget team can run, and what could it NOT "
     "prove? Under 120 words."),
    ("Q3-ledger-void",
     "An append-only evidence ledger cannot delete false rows. Design the void procedure in "
     "one paragraph: what marks a row dead, who can mark it, and what prevents weaponized "
     "voiding. Under 120 words."),
]

QUESTION_DIGEST = hashlib.sha256(
    json.dumps(QUESTIONS, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]

N_SEEDS_PER_Q = 10
SEED_BASE = 2026091600
# interleave ladder so seed order is not confounded with temperature;
# counts per question: 0.2 x3, 0.8 x4, 1.3 x3 (mission-verbatim)
LADDER = [0.2, 0.8, 1.3, 0.2, 0.8, 1.3, 0.2, 0.8, 0.8, 1.3]

# D23 salon SYSTEM verbatim (comparability with the fleet's filed verdicts)
SYSTEM = ("You are an independent witness in a multi-model salon on scientific method and "
          "institutions. Answer from your own knowledge and judgment. Take the side you "
          "actually believe — argue it, do not fence-sit, do not summarize both sides. "
          "No preamble. Hard limit: 120 words.")

_write_lock = threading.Lock()
_stop = threading.Event()            # paid-wall tripwire: stops pass-1 submission
_lane_gate: dict[str, float] = {}
_gate_lock = threading.Lock()
_paidsig = ("credit", "balance", "billing", "insufficient", "quota_exceeded",
            "payment", "upgrade", "subscription")


def _pacing(lane_id: str, min_interval: float = 1.2) -> None:
    while True:
        with _gate_lock:
            now = time.time()
            last = _lane_gate.get(lane_id, 0.0)
            wait = last + min_interval - now
            if wait <= 0:
                _lane_gate[lane_id] = now
                return
        time.sleep(min(wait, 2.0))


def _append(row: dict) -> None:
    with _write_lock:
        with RAW.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _guard(base: str) -> str:
    if base not in ALLOWED_BASES:
        raise ValueError(f"base not allowlisted: {base!r}")
    guard_endpoint(base, ALLOWED_HOSTS)  # https + allowlist, repo law
    host = urllib.parse.urlparse(base).hostname
    for _fam, _typ, _proto, _canon, sa in socket.getaddrinfo(host, 443):
        ip = ipaddress.ip_address(sa[0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise ValueError(f"resolved address blocked: {ip}")
    return base


def call(prompt: str, key: str, temperature: float, seed: int,
         timeout: int = 300, max_tokens: int = 3000, attempt: int = 1) -> dict:
    t0 = time.time()
    rec: dict = {"lane": LANE_ID, "model": "stealth/union-alpha", "ts": _now(),
                 "attempt": attempt}
    lane = next(l for l in LANES if l["id"] == LANE_ID)
    try:
        url = _guard(lane["base"]).rstrip("/") + "/chat/completions"
    except ValueError as e:
        rec.update({"ok": False, "error": f"ssrf_guard: {e}", "latency_ms": 0})
        return rec
    _pacing(LANE_ID)
    body = {"model": lane["model"], "temperature": temperature, "max_tokens": max_tokens,
            "seed": seed,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-u4-verdict-column/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "U4 Union Verdict Column"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        if txt:
            rec.update({"ok": True, "answer": txt, "chars": len(txt),
                        "usage": d.get("usage") or {},
                        "finish_reason": d["choices"][0].get("finish_reason")})
        else:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200],
                        "finish_reason": d["choices"][0].get("finish_reason")})
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
        low = detail.lower()
        if e.code in (401, 402, 403) or any(s in low for s in _paidsig):
            rec["lane_status"] = "ABORTED_PAID_WALL"
            _stop.set()  # mission interrupt law: record and stop
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:140]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


def jobs() -> list[dict]:
    out = []
    for qi, (qid, q) in enumerate(QUESTIONS):
        for s in range(N_SEEDS_PER_Q):
            out.append({"qid": qid, "q": q, "temp": LADDER[s],
                        "seed": SEED_BASE + qi * 10 + s})
    return out


def probe() -> dict:
    env = load_env()
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        print(json.dumps({"ok": False, "error": "no OPENROUTER_API_KEY"}, flush=True))
        sys.exit(1)
    r = call("Reply with exactly: READY", key, temperature=0.0, seed=0,
             timeout=120, max_tokens=2600)
    row = {"ok": bool(r.get("ok")), "error": r.get("error"),
           "latency_ms": r.get("latency_ms"),
           "sample": (r.get("answer") or "")[:40],
           "detail": (r.get("detail") or "")[:120],
           "lane_status": r.get("lane_status")}
    _append({"schema": "u4_verdict_column.v1", "kind": "probe", "ts": _now(),
             "question_digest": QUESTION_DIGEST, **row})
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return row


def run(workers: int = 4) -> None:
    env = load_env()
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        print(json.dumps({"ok": False, "error": "no OPENROUTER_API_KEY"}, flush=True))
        sys.exit(1)
    J = jobs()
    print(json.dumps({"kind": "run", "question_digest": QUESTION_DIGEST,
                      "calls": len(J), "lane": LANE_ID,
                      "ladder": LADDER}, ensure_ascii=False), flush=True)
    todo = J
    pass_no = 1
    while todo and pass_no <= 2:
        fired = 0
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(call, j["q"], key, j["temp"], j["seed"],
                              max_tokens=3000 if pass_no == 1 else 4000,
                              attempt=pass_no): j for j in todo}
            for f in futs:
                j = futs[f]
                if _stop.is_set() and fired == 0:
                    break  # paid wall already tripped: stop submitting new calls
                try:
                    r = f.result()
                except Exception as e:
                    r = {"ok": False, "error": f"worker:{type(e).__name__}: {str(e)[:120]}",
                         "latency_ms": 0, "lane": LANE_ID,
                         "model": "stealth/union-alpha"}
                r.update({"schema": "u4_verdict_column.v1", "kind": "seed", "pass": pass_no,
                          "qid": j["qid"], "question": j["q"],
                          "temperature": j["temp"], "api_seed": j["seed"],
                          "question_digest": QUESTION_DIGEST})
                _append(r)
                fired += 1
                print(json.dumps({"pass": pass_no, "qid": j["qid"], "temp": j["temp"],
                                  "seed": j["seed"], "ok": r.get("ok"),
                                  "chars": r.get("chars"), "ms": r.get("latency_ms"),
                                  "err": (r.get("error") or "")[:60],
                                  "lane_status": r.get("lane_status"),
                                  "progress": fired}, ensure_ascii=False), flush=True)
                if r.get("lane_status") == "ABORTED_PAID_WALL":
                    _stop.set()
        if _stop.is_set():
            print(json.dumps({"kind": "halt", "reason": "paid_wall/interrupt law",
                              "pass": pass_no}, ensure_ascii=False), flush=True)
            break
        # retry pass: only failed seeds, one cooldown, single attempt each
        done_ok = {(r["qid"], r["api_seed"]) for r in _iter_rows()
                   if r.get("kind") == "seed" and r.get("ok")}
        todo = [j for j in J if (j["qid"], j["seed"]) not in done_ok]
        if todo:
            print(json.dumps({"kind": "retry-pending", "n": len(todo)}, ensure_ascii=False), flush=True)
            time.sleep(45.0)
        pass_no += 1
    summarize()


def _iter_rows() -> list[dict]:
    if not RAW.is_file():
        return []
    out = []
    for ln in RAW.read_text(encoding="utf-8", errors="replace").splitlines():
        if not ln.strip():
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out


def summarize() -> dict:
    rows = [r for r in _iter_rows() if r.get("kind") == "seed"]
    best: dict[tuple, dict] = {}  # latest attempt wins per (qid, seed)
    for r in rows:
        k = (r["qid"], r["api_seed"])
        cur = best.get(k)
        if cur is None or (r.get("ok") and not cur.get("ok")) or r.get("pass", 1) >= cur.get("pass", 1):
            best[k] = r
    latest = sorted(best.values(), key=lambda r: (r["qid"], r["api_seed"]))
    ok = [r for r in latest if r.get("ok")]
    summary = {"ok": True, "schema": "u4_verdict_column.v1", "kind": "summary", "ts": _now(),
               "question_digest": QUESTION_DIGEST, "lane": LANE_ID,
               "model": "stealth/union-alpha",
               "seeds": len(latest), "answered": len(ok), "failed": len(latest) - len(ok),
               "per_question": {}}
    for qid, _q in QUESTIONS:
        qrows = [r for r in latest if r.get("qid") == qid]
        qok = [r for r in qrows if r.get("ok")]
        summary["per_question"][qid] = {
            "seeds": len(qrows), "answered": len(qok),
            "temps": sorted({r["temperature"] for r in qrows}),
            "by_temp": {str(t): sum(1 for r in qok if r["temperature"] == t) for t in sorted({r["temperature"] for r in qrows})},
            "chars_mean": round(sum(r["chars"] for r in qok) / len(qok), 1) if qok else None,
            "latency_ms_mean": round(sum(r["latency_ms"] for r in qok) / len(qok), 1) if qok else None,
        }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return summary


def main() -> int:
    mode = "probe" if "--probe" in sys.argv else ("run" if "--run" in sys.argv
                                                  else ("report" if "--report" in sys.argv else "probe"))
    if mode == "probe":
        probe()
        return 0
    if mode == "run":
        run()
        return 0
    summarize()
    return 0


if __name__ == "__main__":
    sys.exit(main())
