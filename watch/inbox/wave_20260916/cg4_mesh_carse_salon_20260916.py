"""cg4_mesh_carse_salon_20260916 -- MESH salon on James P. Carse (finite vs infinite games).

Mission (wave lane CG4): fire the 3-question Carse set across LIVE free lanes, 2 seeds each.
Embed the registered CONTEXT (<=200 tokens, verbatim) in every call. Fold afterwards in the
receipt: per-question convergence/divergence (no averaging), 5 best lines, the ONE mechanic
the mesh unanimously wants added to the estate, poetic-without-mechanism witnesses flagged.

Uses the repo's own fanout plumbing (mag/research_fanout LANES/_env/_now) UNMODIFIED; driver
pattern follows watch/inbox/wave_20260916/d23_salon50_night_20260916.py (temperature/seed
parameterized call, SSRF allowlist + resolved-IP guard, per-lane pacing, append-only tape).
Repo code is not edited. Free lanes only, $0. Paid walls never called, probe included.
Stealth lane or-union-alpha probed first (free window ends ~2026-09-23). zai-lite rides
lite_guard (burst lane law 15) -- paced before a single token leaves.

Wave-lane law: rows append to raw.jsonl AS THEY LAND (survives interruption); failures are
preserved as rows; partial width is still width.
Schema: cg4_mesh_carse.v1
"""
from __future__ import annotations

import ipaddress, json, socket, sys, threading, time, urllib.parse, urllib.request, urllib.error, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "mag"))
from research_fanout import LANES, _env, _now  # repo tooling, unmodified

OUT = ROOT / "memory" / "runs" / "cg4_mesh_carse_salon_20260916"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

PAID_WALL_LANES = {"zai-47", "zai-air"}  # retired paid-wall lanes; never called, not even probed

# free-base allowlist (SSRF guard) -- the z.ai coding-plan endpoint per the LANES registry note
ALLOWED_BASES = {
    "https://api.groq.com/openai/v1",
    "https://api.cerebras.ai/v1",
    "https://api.mistral.ai/v1",
    "https://api.z.ai/api/coding/paas/v4",
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


SYSTEM = ("You are an independent witness in a multi-model salon on James P. Carse's "
          "finite and infinite games, convened by a software estate. Answer from your own "
          "knowledge and judgment. Take the side you actually believe — argue it, do not "
          "fence-sit, do not summarize both sides. No preamble. Hard limit: 100 words.")

# MISSION VERBATIM: CONTEXT (<=200 tokens) + question set, registered in the receipt BEFORE firing
CONTEXT = (
    "James P. Carse: finite games are played to win within rules that cannot change, with "
    "titles and an end; infinite games are played so the play continues — rules must change, "
    "boundaries become horizons, and there are no titles. A fleet runs an append-only "
    "hash-chained ledger, pre-registers falsifiers before experiments, and refuses to let "
    "software mint its verdicts. Its parts: a deterministic game referee, a living mycelium "
    "block being instrumented as a memory substrate, a multi-model debate salon, and a public "
    "parable register."
)

QUESTIONS = [
    ("Q1-ledger",
     "Is an append-only ledger a finite or infinite game? Defend with one Carse-style "
     "distinction and one failure mode of getting it wrong. 100 words."),
    ("Q2-salon-mechanic",
     "Design ONE mechanic that would make a multi-model AI salon an infinite game rather "
     "than a tournament. 100 words."),
    ("Q3-mycelium",
     "Carse: 'finite players play to win; infinite players play to make play possible.' "
     "What is the mycelium-block-as-game-system doing — finite play, infinite play, or is "
     "the category breaking? Take a side. 100 words."),
]

QUESTION_DIGEST = hashlib.sha256(
    json.dumps({"context": CONTEXT, "questions": QUESTIONS}, ensure_ascii=False)
    .encode("utf-8")).hexdigest()[:16]

N_SEEDS_PER_LANE = 2          # mission: 2 seeds each
TEMPS = [0.3, 0.9]            # one per seed slot
SEED_BASE = 2026091660
# D22 rotation laws, structural here:
LANE_MAX_TOKENS = {"groq-qwen": 800}           # OTPM 1000 sub-gate: <= ~800 or intermittent 429
LANE_MIN_INTERVAL = {"cerebras-oss": 13.0}     # 5 req/min lane: >= 13 s spacing
DEFAULT_INTERVAL = 1.2

_lane_gate: dict[str, float] = {}
_lane_gate_lock = threading.Lock()
_write_lock = threading.Lock()
_aborted_lanes: set[str] = set()
_paidsig = ("credit", "balance", "billing", "insufficient", "quota_exceeded",
            "payment", "upgrade", "subscription")


def _pacing(lane_id: str, min_interval: float) -> None:
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
         timeout: int = 300, attempt: int = 1) -> dict:
    t0 = time.time()
    max_tokens = LANE_MAX_TOKENS.get(lane["id"], 3000)
    rec: dict = {"lane": lane["id"], "model": lane["model"], "ts": _now(), "attempt": attempt}
    if lane["id"] in PAID_WALL_LANES:
        rec.update({"ok": False, "error": "paid_wall_never_called", "latency_ms": 0})
        return rec
    lite = str(lane.get("key", "")) == "ZAI_API_KEY_Lite"
    if lite:
        # law 15 made structural: the Lite seat is paced before a single token leaves
        try:
            from mag import lite_guard
        except Exception:
            import lite_guard  # type: ignore
        g = lite_guard.check("cg4_mesh_carse")
        if not g.get("ok"):
            rec.update({"ok": False, "error": "LITE_PACED", "detail": g.get("deny", ""),
                        "latency_ms": 0})
            return rec
    try:
        url = _guard(lane["base"]).rstrip("/") + "/chat/completions"
    except ValueError as e:
        rec.update({"ok": False, "error": f"ssrf_guard: {e}", "latency_ms": 0})
        return rec
    _pacing(lane["id"], LANE_MIN_INTERVAL.get(lane["id"], DEFAULT_INTERVAL))
    body = {"model": lane["model"], "temperature": temperature, "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]}
    if "mistral" not in lane["base"]:
        # Mistral rejects OpenAI-style `seed` (HTTP 422 extra_forbidden) — api_seed stays in the receipt row
        body["seed"] = seed
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-cg4-mesh-carse/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "CG4 Mesh Carse Salon"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        if txt:
            rec.update({"ok": True, "answer": txt, "chars": len(txt), "usage": d.get("usage") or {}})
            if lite:
                try:
                    from mag import lite_guard
                except Exception:
                    import lite_guard  # type: ignore
                lite_guard.record("cg4_mesh_carse",
                                  int((d.get("usage") or {}).get("total_tokens") or 0),
                                  note=f"lane {lane['id']}")
        else:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200],
                        "finish_reason": d["choices"][0].get("finish_reason")})
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
        low = detail.lower()
        if e.code in (401, 402, 404) or any(s in low for s in _paidsig):
            with _lane_gate_lock:
                _aborted_lanes.add(lane["id"])
            rec["lane_status"] = "ABORTED_PAID_WALL_OR_GONE"
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:140]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


def prompt_for(q: str) -> str:
    return f"{CONTEXT}\n\n{q}"


def job_for(qi: int, lane_idx: int, slot: int, live_ids: list[str]) -> dict:
    qid, q = QUESTIONS[qi]
    lane_id = live_ids[lane_idx % len(live_ids)]
    lane = next(l for l in LANES if l["id"] == lane_id)
    temp = TEMPS[slot % len(TEMPS)]
    seed = SEED_BASE + qi * 100 + lane_idx * 2 + slot
    return {"qi": qi, "qid": qid, "q": q, "lane": lane, "temp": temp, "seed": seed, "slot": slot}


def probe() -> dict:
    """One READY ping per candidate lane (paid walls excluded BEFORE any call)."""
    env = _env()
    cands = [l for l in LANES if l["id"] not in PAID_WALL_LANES and env.get(l["key"])]
    skipped = [l["id"] for l in LANES if l["id"] in PAID_WALL_LANES]
    nokey = [l["id"] for l in LANES if not env.get(l["key"])]
    rows = []
    for lane in cands:
        r = call(lane, "Reply with exactly: READY", env[lane["key"]],
                 temperature=0.0, seed=0, timeout=120)
        rows.append({"lane": lane["id"], "ok": bool(r.get("ok")), "error": r.get("error"),
                     "latency_ms": r.get("latency_ms"),
                     "sample": (r.get("answer") or "")[:40],
                     "detail": (r.get("detail") or "")[:120],
                     "lane_status": r.get("lane_status")})
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    live = [r["lane"] for r in rows if r["ok"] and r["lane"] not in _aborted_lanes]
    dead = [r["lane"] for r in rows if not r["ok"]]
    out = {"ok": True, "schema": "cg4_mesh_carse.v1", "kind": "probe", "ts": _now(),
           "question_digest": QUESTION_DIGEST,
           "skipped_paid_wall": skipped, "no_key": nokey,
           "live": live, "dead": dead, "rows": rows}
    (OUT / "probe.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def run(live_ids: list[str], workers: int = 8) -> dict:
    env = _env()
    jobs = [job_for(qi, li, slot, live_ids)
            for qi in range(len(QUESTIONS))
            for li in range(len(live_ids))
            for slot in range(N_SEEDS_PER_LANE)]
    print(json.dumps({"kind": "run", "question_digest": QUESTION_DIGEST,
                      "jobs": len(jobs), "live_lanes": live_ids,
                      "map": [{"qid": j["qid"], "lane": j["lane"]["id"], "slot": j["slot"],
                               "temp": j["temp"], "seed": j["seed"]} for j in jobs]},
                     ensure_ascii=False), flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, j["lane"], prompt_for(j["q"]), env[j["lane"]["key"]],
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
            r.update({"schema": "cg4_mesh_carse.v1", "kind": "seed", "qid": j["qid"],
                      "question": j["q"], "slot": j["slot"], "temperature": j["temp"],
                      "api_seed": j["seed"], "pass": 1, "question_digest": QUESTION_DIGEST})
            _append(r)
            done += 1
            print(json.dumps({"qid": j["qid"], "lane": j["lane"]["id"], "slot": j["slot"],
                              "temp": j["temp"], "ok": r.get("ok"), "chars": r.get("chars"),
                              "ms": r.get("latency_ms"), "err": (r.get("error") or "")[:60],
                              "progress": f"{done}/{len(jobs)}"}, ensure_ascii=False),
                  flush=True)
    return summarize()


def retry_failed(cooldown: float = 45.0) -> dict:
    """Pass 2: refire failed (qid, lane, slot) cells once, same seed map, after a cooldown."""
    env = _env()
    allowed = [l["id"] for l in LANES if l["id"] not in PAID_WALL_LANES]
    seen_cells = {(r["qid"], r["lane"], r.get("slot")) for r in _iter_rows()
                  if r.get("kind") == "seed" and r.get("lane") in allowed}
    live_ids = [l["id"] for l in LANES if l["id"] in {c[1] for c in seen_cells}]
    got_ok = {(r["qid"], r["lane"], r.get("slot")) for r in _iter_rows()
              if r.get("kind") == "seed" and r.get("ok")}
    todo = [job_for(qi, li, slot, live_ids)
            for qi in range(len(QUESTIONS))
            for li in range(len(live_ids))
            for slot in range(N_SEEDS_PER_LANE)
            if (QUESTIONS[qi][0], live_ids[li % len(live_ids)], slot) not in got_ok
            and (QUESTIONS[qi][0], live_ids[li % len(live_ids)], slot) in seen_cells]
    todo = [j for j in todo if j["lane"]["id"] not in _aborted_lanes]
    print(json.dumps({"kind": "retry",
                      "refiring": [{"qid": j["qid"], "lane": j["lane"]["id"], "slot": j["slot"]}
                                   for j in todo]}, ensure_ascii=False), flush=True)
    if not todo:
        return summarize()
    time.sleep(cooldown)
    with ThreadPoolExecutor(max_workers=min(4, len(todo))) as ex:
        futs = {ex.submit(call, j["lane"], prompt_for(j["q"]), env[j["lane"]["key"]],
                          j["temp"], j["seed"], attempt=2): j for j in todo}
        for f in futs:
            j = futs[f]
            try:
                r = f.result()
            except Exception as e:
                r = {"ok": False, "error": f"worker:{type(e).__name__}: {str(e)[:120]}",
                     "latency_ms": 0}
            r.update({"schema": "cg4_mesh_carse.v1", "kind": "seed", "qid": j["qid"],
                      "question": j["q"], "slot": j["slot"], "temperature": j["temp"],
                      "api_seed": j["seed"], "pass": 2, "question_digest": QUESTION_DIGEST})
            _append(r)
            print(json.dumps({"qid": j["qid"], "lane": j["lane"]["id"], "slot": j["slot"],
                              "pass": 2, "ok": r.get("ok"), "err": (r.get("error") or "")[:60]},
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
    best: dict[tuple, dict] = {}  # latest attempt wins per (qid, lane, slot)
    for r in rows:
        k = (r["qid"], r["lane"], r.get("slot"))
        cur = best.get(k)
        if cur is None or (r.get("ok") and not cur.get("ok")) or r.get("pass", 1) >= cur.get("pass", 1):
            best[k] = r
    latest = sorted(best.values(), key=lambda r: (r["qid"], r["lane"], str(r.get("slot"))))
    ok = [r for r in latest if r.get("ok")]
    summary = {"ok": True, "schema": "cg4_mesh_carse.v1", "kind": "summary", "ts": _now(),
               "question_digest": QUESTION_DIGEST,
               "cells": len(latest), "answered": len(ok),
               "failed": len(latest) - len(ok),
               "per_question": {}, "per_lane": {}, "diversity": {}}
    for qid, _q in QUESTIONS:
        qrows = [r for r in latest if r.get("qid") == qid]
        qok = [r for r in qrows if r.get("ok")]
        pairs = [_jaccard(a["answer"], b["answer"])
                 for i, a in enumerate(qok) for b in qok[i + 1:]]
        pairs.sort()
        summary["per_question"][qid] = {
            "cells": len(qrows), "answered": len(qok),
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
                                                "cells": summary["cells"]}, ensure_ascii=False),
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
