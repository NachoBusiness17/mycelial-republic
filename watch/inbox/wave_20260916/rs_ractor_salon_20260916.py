"""rs_ractor_salon_20260916 -- free-lane salon on THE RACTOR ENGINE (wave 20260916, lane RS).

Mission (operator, verbatim): "burn our free lanes — we have prior art for all of this,
self steal" — run the free-lane salon on the fleet's newest design, THE RACTOR ENGINE,
using prior art as context (OCEAN-conditioned LLM agents, DeGroot consensus, generative
agents, Geiping et al. 2502.05171 recurrent-depth).

Driver pattern: d23_salon50_night_20260916.py — imports mag.research_fanout LANES/_env/_now
UNMODIFIED; probes first; or-union-alpha used only if the probe says alive. Repo code is
not edited. Free lanes only, $0. zai-lite (the coding-plan/Lite seat) is a PAID-WALL seat
by mission order — filtered out before any call, probe included (do-not-retry law; the
Lite lane is burst-only, never a default carrier — mag/lite_guard law 15).

Wave-lane law: receipt FIRST (watch/inbox/wave_20260916/receipts/RS_RACTOR_ENGINE_SALON.md,
appended as results land); rows append to raw.jsonl AS THEY LAND; failures are preserved
as rows; partial width is still width. 2 seeds/question minimum across distinct lanes
(this driver fires 4/question when lanes allow). Schema: rs_ractor_salon.v1
"""
from __future__ import annotations

import ipaddress, json, socket, sys, threading, time, urllib.parse, urllib.request, urllib.error, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "mag"))
from research_fanout import LANES, _env, _now  # repo tooling, unmodified

OUT = ROOT / "memory" / "runs" / "rs_ractor_salon_20260916"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

# Mission order: never the zai paid walls. zai-lite rides the coding-plan Lite seat —
# burst-only by law, excluded BEFORE any call (probe included). or-union-alpha stays in
# the candidate list but is used only if the probe says alive (time-boxed stealth lane).
PAID_WALL_LANES = {"zai-lite"}

# same free-base allowlist as mag/scale_salon.py (SSRF guard)
ALLOWED_BASES = {
    "https://api.groq.com/openai/v1",
    "https://api.cerebras.ai/v1",
    "https://api.mistral.ai/v1",
    "https://api.z.ai/api/paas/v4",
    "https://openrouter.ai/api/v1",
}


def _guard(base: str) -> str:
    if base not in ALLOWED_BASES:
        raise ValueError(f"base not allowlisted: {base!r}")
    if urllib.parse.urlparse(base).scheme != "https":
        raise ValueError(f"non-https base: {base!r}")
    host = urllib.parse.urlparse(base).hostname
    for _fam, _typ, _proto, _canon, sa in socket.getaddrinfo(host, 443):
        ip = ipaddress.ip_address(sa[0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise ValueError(f"resolved address blocked: {ip}")
    return base


SYSTEM = ("You are an independent witness in a multi-model salon on agent architecture "
          "(THE RACTOR ENGINE). Answer from your own knowledge and judgment. Take the side "
          "you actually believe — argue it, do not fence-sit, do not summarize both sides. "
          "Be concrete: name the mechanism. No preamble. Respect the word limit in the "
          "question exactly.")

# CONTEXT block (mission, verbatim, <=250 tokens) embedded in EVERY segment prompt.
CONTEXT = (
    "A fleet is building ractor witnesses for multi-model deliberation: each witness is a "
    "small local model (2B-class) whose 'mind' is a graph of belief nodes "
    "(memory/values/perception/verdict) evolving by Laplacian diffusion, parameterized by "
    "an OCEAN personality vector (openness = boundary conductance, neuroticism = negative "
    "feedback gain, etc.); decisions fire on threshold crossings; reasoning depth = a "
    "recurrent latent loop (a 3.6B model looping its state 64x matched a 103B model — "
    "Geiping et al. 2502.05171); prior art: OCEAN-conditioned LLM agents, DeGroot "
    "consensus, generative agents."
)

# MISSION VERBATIM question set (registered in the receipt BEFORE firing)
QUESTIONS = [
    ("Q1-diffusion-break",
     "What breaks first when a witness's 'thinking' is graph diffusion on beliefs instead "
     "of token generation — and is that break fatal or fixable? Take a side, 120 words."),
    ("Q2-recursion-vs-breadth",
     "Does recurrence depth substitute for parameter breadth in judgment tasks — can a 2B "
     "model looping 64x produce verdicts indistinguishable from a 70B single pass? What is "
     "the first measurable difference? 120 words."),
    ("Q3-ocean-falsifier",
     "Design the cheapest falsifier: how do you prove a witness's OCEAN parameters actually "
     "change its verdicts, beyond prompt costume? Name the control. 100 words."),
]

QUESTION_DIGEST = hashlib.sha256(
    json.dumps(QUESTIONS, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
CONTEXT_DIGEST = hashlib.sha256(CONTEXT.encode("utf-8")).hexdigest()[:16]

N_PER_Q = 4          # 2/question minimum required; 4 fired when lanes allow
SEED_BASE = 2026091600
TEMPS = [0.2, 0.7, 1.2]

_lane_gate: dict[str, float] = {}
_lane_gate_lock = threading.Lock()
_write_lock = threading.Lock()
_aborted_lanes: set[str] = set()
_paidsig = ("credit", "balance", "billing", "insufficient", "quota_exceeded",
            "payment", "upgrade", "subscription")


def _pacing(lane_id: str, min_interval: float = 1.2) -> None:
    """Per-lane min interval between call starts (rotation, not flood — §6.5 law)."""
    while True:
        with _lane_gate_lock:
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


def call(lane: dict, prompt: str, key: str, temperature: float, seed: int,
         timeout: int = 300, max_tokens: int = 2600, attempt: int = 1) -> dict:
    t0 = time.time()
    rec: dict = {"lane": lane["id"], "model": lane["model"], "ts": _now(), "attempt": attempt}
    if lane["id"] in PAID_WALL_LANES:
        rec.update({"ok": False, "error": "paid_wall_never_called", "latency_ms": 0})
        return rec
    try:
        url = _guard(lane["base"]).rstrip("/") + "/chat/completions"
    except ValueError as e:
        rec.update({"ok": False, "error": f"ssrf_guard: {e}", "latency_ms": 0})
        return rec
    _pacing(lane["id"])
    body = {"model": lane["model"], "temperature": temperature, "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]}
    if "mistral" not in lane["base"]:
        # Mistral rejects OpenAI-style `seed` (HTTP 422 extra_forbidden) — api_seed stays in the receipt row
        body["seed"] = seed
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-rs-ractor-salon/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "RS Ractor Engine Salon"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        if txt:
            rec.update({"ok": True, "answer": txt, "chars": len(txt), "usage": d.get("usage") or {}})
        else:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200],
                        "finish_reason": d["choices"][0].get("finish_reason")})
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
        low = detail.lower()
        if e.code in (401, 402) or any(s in low for s in _paidsig):
            with _lane_gate_lock:
                _aborted_lanes.add(lane["id"])
            rec["lane_status"] = "ABORTED_PAID_WALL"
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:140]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


def build_jobs(live_ids: list[str]) -> list[dict]:
    """4 seeds per question across distinct lanes; deterministic frozen map."""
    jobs = []
    for qi, (qid, q) in enumerate(QUESTIONS):
        prompt = f"{CONTEXT}\n\nQUESTION: {q}"
        for si in range(N_PER_Q):
            lane_id = live_ids[(qi * N_PER_Q + si) % len(live_ids)]
            lane = next(l for l in LANES if l["id"] == lane_id)
            temp = TEMPS[(si + qi) % 3]
            seed = SEED_BASE + qi * N_PER_Q + si
            jobs.append({"s": seed - SEED_BASE, "qid": qid, "q": prompt, "raw_q": q,
                         "lane": lane, "temp": temp, "seed": seed})
    return jobs


def probe() -> dict:
    """One READY ping per candidate lane (zai-lite excluded BEFORE any call)."""
    env = _env()
    cands = [l for l in LANES if l["id"] not in PAID_WALL_LANES and env.get(l["key"])]
    skipped = [l["id"] for l in LANES if l["id"] in PAID_WALL_LANES]
    nokey = [l["id"] for l in LANES if not env.get(l["key"])]
    rows = []
    for lane in cands:
        r = call(lane, "Reply with exactly: READY", env[lane["key"]],
                 temperature=0.0, seed=0, timeout=120, max_tokens=2600)
        rows.append({"lane": lane["id"], "ok": bool(r.get("ok")), "error": r.get("error"),
                     "latency_ms": r.get("latency_ms"),
                     "sample": (r.get("answer") or "")[:40],
                     "detail": (r.get("detail") or "")[:120],
                     "lane_status": r.get("lane_status")})
        _append({"schema": "rs_ractor_salon.v1", "kind": "probe", "ts": _now(),
                 "question_digest": QUESTION_DIGEST, **rows[-1]})
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    live = [r["lane"] for r in rows if r["ok"] and r["lane"] not in _aborted_lanes]
    dead = [r["lane"] for r in rows if not r["ok"]]
    return {"ok": True, "schema": "rs_ractor_salon.v1", "kind": "probe", "ts": _now(),
            "question_digest": QUESTION_DIGEST, "context_digest": CONTEXT_DIGEST,
            "skipped_paid_wall": skipped, "no_key": nokey,
            "live": live, "dead": dead, "rows": rows}


def run(live_ids: list[str], workers: int = 6) -> dict:
    env = _env()
    jobs = build_jobs(live_ids)
    print(json.dumps({"kind": "run", "question_digest": QUESTION_DIGEST,
                      "context_digest": CONTEXT_DIGEST,
                      "seeds": len(jobs), "live_lanes": live_ids,
                      "map": [{"s": j["s"], "qid": j["qid"], "lane": j["lane"]["id"],
                               "temp": j["temp"], "seed": j["seed"]} for j in jobs]},
                     ensure_ascii=False), flush=True)
    _append({"schema": "rs_ractor_salon.v1", "kind": "run", "ts": _now(),
             "question_digest": QUESTION_DIGEST, "context_digest": CONTEXT_DIGEST,
             "live_lanes": live_ids,
             "map": [{"s": j["s"], "qid": j["qid"], "lane": j["lane"]["id"],
                      "temp": j["temp"], "api_seed": j["seed"]} for j in jobs]})
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, j["lane"], j["q"], env[j["lane"]["key"]],
                          j["temp"], j["seed"]): j for j in jobs}
        for f in futs:
            j = futs[f]
            try:
                r = f.result()
            except Exception as e:
                r = {"ok": False, "error": f"worker:{type(e).__name__}: {str(e)[:120]}",
                     "latency_ms": 0, "lane": j["lane"]["id"], "model": j["lane"]["model"]}
            with _lane_gate_lock:
                if j["lane"]["id"] in _aborted_lanes:
                    r["lane_status"] = "lane_aborted_paid_wall_midrun"
            r.update({"schema": "rs_ractor_salon.v1", "kind": "seed", "s": j["s"],
                      "qid": j["qid"], "question": j["raw_q"], "temperature": j["temp"],
                      "api_seed": j["seed"], "pass": 1, "question_digest": QUESTION_DIGEST})
            _append(r)
            done += 1
            print(json.dumps({"s": j["s"], "qid": j["qid"], "lane": j["lane"]["id"],
                              "temp": j["temp"],
                              "ok": r.get("ok"), "chars": r.get("chars"),
                              "ms": r.get("latency_ms"), "err": (r.get("error") or "")[:60],
                              "progress": f"{done}/{len(jobs)}"}, ensure_ascii=False),
                  flush=True)
    return summarize()


def retry_failed(cooldown: float = 45.0) -> dict:
    """Pass 2: refire failed seeds once, same seed->lane map, after a cooldown. Append-only."""
    env = _env()
    allowed = [l["id"] for l in LANES if l["id"] not in PAID_WALL_LANES]
    seen = {r["lane"] for r in _iter_rows()
            if r.get("kind") == "seed" and r.get("lane") in allowed}
    live_ids = [l["id"] for l in LANES if l["id"] in seen]
    got_ok: set[int] = {r["s"] for r in _iter_rows()
                        if r.get("kind") == "seed" and r.get("ok")}
    todo = [j for j in build_jobs(live_ids) if j["s"] not in got_ok]
    todo = [j for j in todo if j["lane"]["id"] not in _aborted_lanes]
    print(json.dumps({"kind": "retry", "refiring": [j["s"] for j in todo]}, ensure_ascii=False), flush=True)
    if not todo:
        return summarize()
    time.sleep(cooldown)
    with ThreadPoolExecutor(max_workers=min(4, len(todo))) as ex:
        futs = {ex.submit(call, j["lane"], j["q"], env[j["lane"]["key"]],
                          j["temp"], j["seed"], max_tokens=3600, attempt=2): j for j in todo}
        for f in futs:
            j = futs[f]
            try:
                r = f.result()
            except Exception as e:
                r = {"ok": False, "error": f"worker:{type(e).__name__}: {str(e)[:120]}",
                     "latency_ms": 0}
            r.update({"schema": "rs_ractor_salon.v1", "kind": "seed", "s": j["s"],
                      "qid": j["qid"], "question": j["raw_q"], "temperature": j["temp"],
                      "api_seed": j["seed"], "pass": 2, "question_digest": QUESTION_DIGEST})
            _append(r)
            print(json.dumps({"s": j["s"], "pass": 2, "lane": j["lane"]["id"],
                              "ok": r.get("ok"), "err": (r.get("error") or "")[:60]},
                             ensure_ascii=False), flush=True)
    return summarize()


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


def _tokens(txt: str) -> set[str]:
    return set(hashlib.md5(w.encode("utf-8")).hexdigest()[:8] for w in
               "".join(c.lower() if c.isalnum() else " " for c in txt).split())


def _jaccard(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def summarize() -> dict:
    rows = [r for r in _iter_rows() if r.get("kind") == "seed"]
    best: dict[int, dict] = {}  # latest attempt wins per seed
    for r in rows:
        cur = best.get(r["s"])
        if cur is None or (r.get("ok") and not cur.get("ok")) or r.get("pass", 1) >= cur.get("pass", 1):
            best[r["s"]] = r
    latest = sorted(best.values(), key=lambda r: r["s"])
    ok = [r for r in latest if r.get("ok")]
    summary = {"ok": True, "schema": "rs_ractor_salon.v1", "kind": "summary", "ts": _now(),
               "question_digest": QUESTION_DIGEST, "context_digest": CONTEXT_DIGEST,
               "seeds": len(latest), "answered": len(ok),
               "failed": len(latest) - len(ok),
               "per_question": {}, "per_lane": {}, "diversity": {}}
    for qid, _q in QUESTIONS:
        qrows = [r for r in latest if r.get("qid") == qid]
        qok = [r for r in qrows if r.get("ok")]
        pairs = [_jaccard(a["answer"], b["answer"])
                 for i, a in enumerate(qok) for b in qok[i + 1:]]
        pairs.sort()
        summary["per_question"][qid] = {
            "seeds": len(qrows), "answered": len(qok),
            "lanes": sorted({r["lane"] for r in qok}),
            "pairwise_jaccard_mean": round(sum(pairs) / len(pairs), 4) if pairs else None,
            "pairwise_jaccard_median": pairs[len(pairs) // 2] if pairs else None,
        }
    for ln in sorted({r.get("lane") or "unknown" for r in latest}):
        lrows = [r for r in latest if (r.get("lane") or "unknown") == ln]
        summary["per_lane"][ln] = {
            "answered": sum(1 for r in lrows if r.get("ok")),
            "failed": sum(1 for r in lrows if not r.get("ok")),
            "errors": sorted({(r.get("error") or "")[:40] for r in lrows if not r.get("ok")})}
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(json.dumps(summary["per_question"] | {"answered": summary["answered"],
                                                "seeds": summary["seeds"]}, ensure_ascii=False),
          flush=True)
    return summary


def main() -> int:
    mode = "probe" if "--probe" in sys.argv else ("run" if "--run" in sys.argv
                                                  else ("retry" if "--retry" in sys.argv
                                                        else "report"))
    if mode == "probe":
        probe()
        return 0
    if mode == "run":
        live = None
        for a in sys.argv[1:]:
            if a.startswith("--live="):
                live = a.split("=", 1)[1].split(",")
        if not live:
            p = probe()
            live = p["live"]
        if not live:
            print(json.dumps({"ok": False, "error": "no live lanes"}, flush=True))
            return 1
        run(live)
        return 0
    if mode == "retry":
        retry_failed()
        return 0
    summarize()
    return 0


if __name__ == "__main__":
    sys.exit(main())
