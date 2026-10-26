"""p2_demo_salon_20260916 -- showcase salon for the ractor-salon plugin README.

Mission (operator, verbatim): "run the showcase salon that the ractor-salon plugin's
README will quote as example output."

QUESTION (registered verbatim in receipt BEFORE firing):
  "Should a sovereign agent fleet open-source its orchestration layer? Steelman both
   sides, then give the deciding argument. Under 150 words."

Lanes: every live lane from the D22 rotation table (receipts/D22_PROVIDER_PROBE_20260916.md)
plus stealth/union-alpha (free window, 2 seeds at different temperatures).
Uses the repo's own fanout plumbing (mag/research_fanout LANES/_env/_now) UNMODIFIED;
driver pattern follows d23_salon50_night_20260916.py (SSRF allowlist + resolved-IP guard).
Repo code is not edited. Free lanes + free-window stealth lane only, $0.
zai-air / zai-47 are PAID WALLS — never called, probe included (standing order).

Wave-lane law: rows append to raw.jsonl AS THEY LAND (survives interruption);
failures are preserved as rows; partial width is still width.
Schema: p2_demo_salon.v1
"""
from __future__ import annotations

import ipaddress, json, socket, sys, threading, time, urllib.parse, urllib.request, urllib.error, hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "mag"))
from research_fanout import LANES, _env, _now  # repo tooling, unmodified

OUT = ROOT / "memory" / "runs" / "p2_demo_salon_20260916"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

PAID_WALL_LANES = {"zai-air", "zai-47"}  # standing order: never call, not even a probe

# D22 rotation-table lanes (+ cerebras-oss, documented ALIVE in D22 pass-2, sparse use)
ROTATION_LANES = [
    "cerebras-qwen", "mistral-min8", "groq-oss", "groq-oss20", "groq-qwen",
    "cerebras-oss", "or-ling3", "or-nemotron", "or-glm52", "mistral-small",
]
STEALTH_LANE = "or-union-alpha"

# same free-base allowlist as mag/scale_salon.py (SSRF guard)
ALLOWED_BASES = {
    "https://api.groq.com/openai/v1",
    "https://api.cerebras.ai/v1",
    "https://api.mistral.ai/v1",
    "https://openrouter.ai/api/v1",
}

LANE_OVERRIDES = {
    # D22: groq-qwen OTPM sub-limit 1000 -> max_tokens <= ~800 or it intermittently 429s
    "groq-qwen": {"max_tokens": 780},
    # D22: or-nemotron heavy reasoning burn, background only, timeout >= 90 s
    "or-nemotron": {"timeout": 180, "max_tokens": 3000},
}

QUESTION = ("Should a sovereign agent fleet open-source its orchestration layer? "
            "Steelman both sides, then give the deciding argument. Under 150 words.")
QUESTION_DIGEST = hashlib.sha256(QUESTION.encode("utf-8")).hexdigest()[:16]

SALON_TEMP = 0.5
UNION_SEEDS = [(0.2, 2026091601), (0.9, 2026091602)]  # 2 seeds, different temperatures
SEED_BASE = 2026091600

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


def call(lane: dict, prompt: str, key: str, temperature: float, seed: int,
         timeout: int = 120, max_tokens: int = 2600, attempt: int = 1,
         tag: str = "salon") -> dict:
    t0 = time.time()
    rec: dict = {"lane": lane["id"], "model": lane["model"], "ts": _now(),
                 "attempt": attempt, "tag": tag,
                 "temperature": temperature, "api_seed": seed}
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
                 "User-Agent": "mag-p2-demo-salon/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "P2 Demo Salon"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        if txt:
            rec.update({"ok": True, "answer": txt, "chars": len(txt),
                        "words": len(txt.split()), "usage": d.get("usage") or {}})
        else:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200],
                        "finish_reason": d["choices"][0].get("finish_reason")})
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
        low = detail.lower()
        if e.code in (401, 402, 403) or any(s in low for s in _paidsig):
            with _lane_gate_lock:
                _aborted_lanes.add(lane["id"])
            rec["lane_status"] = "ABORTED_PAID_WALL"
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:140]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    rec["question_digest"] = QUESTION_DIGEST
    return rec


SYSTEM = ("You are an independent witness in a multi-model salon on sovereign agent "
          "fleets. Answer from your own knowledge and judgment. No preamble, no "
          "meta-commentary. Hard limit: 150 words.")


def probe() -> dict:
    """One READY ping per candidate lane (paid walls excluded BEFORE any call)."""
    env = _env()
    cand_ids = ROTATION_LANES + [STEALTH_LANE]
    cands = [l for l in LANES if l["id"] in cand_ids and l["id"] not in PAID_WALL_LANES
             and env.get(l["key"])]
    skipped = [l for l in LANES if l["id"] in PAID_WALL_LANES]
    nokey = [l["id"] for l in cand_ids if not env.get(next((x["key"] for x in LANES
             if x["id"] == l), ""))]
    rows = []
    for lane in cands:
        ov = LANE_OVERRIDES.get(lane["id"], {})
        r = call(lane, "Reply with exactly: READY", env[lane["key"]],
                 temperature=0.0, seed=SEED_BASE, timeout=ov.get("timeout", 90),
                 max_tokens=ov.get("max_tokens", 2600), tag="probe")
        _append(r | {"kind": "probe"})
        rows.append({"lane": lane["id"], "ok": bool(r.get("ok")), "error": r.get("error"),
                     "latency_ms": r.get("latency_ms"),
                     "sample": (r.get("answer") or "")[:40],
                     "detail": (r.get("detail") or "")[:120],
                     "lane_status": r.get("lane_status")})
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    live = [r["lane"] for r in rows if r.get("ok")]
    dead = [r["lane"] for r in rows if not r.get("ok")]
    return {"ok": True, "schema": "p2_demo_salon.v1", "kind": "probe", "ts": _now(),
            "question_digest": QUESTION_DIGEST,
            "skipped_paid_wall": [l["id"] for l in skipped], "no_key": nokey,
            "live": live, "dead": dead, "rows": rows}


def salon(live_ids: list[str], workers: int = 6) -> dict:
    """One showcase answer per live rotation lane + 2 union-alpha seeds (T0.2/T0.9)."""
    env = _env()
    jobs = []
    for i, lid in enumerate([l for l in ROTATION_LANES if l in live_ids]):
        lane = next(l for l in LANES if l["id"] == lid)
        ov = LANE_OVERRIDES.get(lid, {})
        jobs.append({"lane": lane, "temp": SALON_TEMP, "seed": SEED_BASE + 10 + i,
                     "tag": "salon", "timeout": ov.get("timeout", 150),
                     "max_tokens": ov.get("max_tokens", 2600)})
    if STEALTH_LANE in live_ids:
        lane = next(l for l in LANES if l["id"] == STEALTH_LANE)
        for temp, seed in UNION_SEEDS:
            jobs.append({"lane": lane, "temp": temp, "seed": seed, "tag": "salon",
                         "timeout": 150, "max_tokens": 2600})
    print(json.dumps({"kind": "run", "question": QUESTION,
                      "question_digest": QUESTION_DIGEST, "n": len(jobs),
                      "map": [{"lane": j["lane"]["id"], "temp": j["temp"],
                               "seed": j["seed"]} for j in jobs]}, ensure_ascii=False),
          flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, j["lane"], QUESTION, env[j["lane"]["key"]],
                          j["temp"], j["seed"], j["timeout"], j["max_tokens"],
                          1, j["tag"]): j for j in jobs}
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
            r.update({"kind": "salon", "schema": "p2_demo_salon.v1"})
            _append(r)
            results.append(r)
            print(json.dumps({"lane": j["lane"]["id"], "temp": j["temp"],
                              "ok": r.get("ok"), "chars": r.get("chars"),
                              "words": r.get("words"), "ms": r.get("latency_ms"),
                              "err": (r.get("error") or "")[:60]}, ensure_ascii=False),
                  flush=True)
    return {"ok": True, "kind": "salon_done", "ts": _now(),
            "question_digest": QUESTION_DIGEST, "results": results}


def retry_failed(live_ids: list[str], cooldown: float = 20.0) -> list[dict]:
    """Pass 2: refire failed salon rows once, same seed/temp map, after a cooldown."""
    env = _env()
    done: set[tuple] = set()
    got: dict[tuple, dict] = {}
    for r in _iter_rows():
        if r.get("kind") == "salon":
            k = (r["lane"], r.get("temperature"), r.get("api_seed"))
            done.add(k)
            if r.get("ok"):
                got[k] = r
    todo = []
    for lid in [l for l in ROTATION_LANES + [STEALTH_LANE] if l in live_ids]:
        lane = next(l for l in LANES if l["id"] == lid)
        temps = UNION_SEEDS if lid == STEALTH_LANE else [(SALON_TEMP, None)]
        for temp, seed in temps:
            if seed is None:
                idx = [l for l in ROTATION_LANES if l in live_ids].index(lid)
                seed = SEED_BASE + 10 + idx
            if (lid, temp, seed) in done and (lid, temp, seed) in got:
                continue
            ov = LANE_OVERRIDES.get(lid, {})
            todo.append({"lane": lane, "temp": temp, "seed": seed,
                         "timeout": ov.get("timeout", 150),
                         "max_tokens": ov.get("max_tokens", 2600)})
    todo = [j for j in todo if j["lane"]["id"] not in _aborted_lanes]
    if not todo:
        print(json.dumps({"kind": "retry", "refiring": []}, ensure_ascii=False), flush=True)
        return []
    print(json.dumps({"kind": "retry", "refiring": [j["lane"]["id"] for j in todo]},
                     ensure_ascii=False), flush=True)
    time.sleep(cooldown)
    out = []
    for j in todo:  # sequential, gentle
        r = call(j["lane"], QUESTION, env[j["lane"]["key"]], j["temp"], j["seed"],
                 j["timeout"], j["max_tokens"], attempt=2, tag="salon")
        r.update({"kind": "salon", "schema": "p2_demo_salon.v1"})
        _append(r)
        out.append(r)
        print(json.dumps({"lane": j["lane"]["id"], "pass": 2, "ok": r.get("ok"),
                          "err": (r.get("error") or "")[:60]}, ensure_ascii=False), flush=True)
    return out


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


def best_answers() -> dict:
    """Latest winning attempt per (lane, temp, seed) — for the receipt fold."""
    best: dict[tuple, dict] = {}
    for r in _iter_rows():
        if r.get("kind") != "salon":
            continue
        k = (r["lane"], r.get("temperature"), r.get("api_seed"))
        cur = best.get(k)
        if cur is None or (r.get("ok") and not cur.get("ok")) or r.get("attempt", 1) >= cur.get("attempt", 1):
            best[k] = r
    return {f"{k[0]}|T{k[1]}|s{k[2]}": v for k, v in sorted(best.items())}


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
        if live is None:
            p = probe()
            live = p["live"]
        live = [l for l in live if l not in _aborted_lanes]
        if not live:
            print(json.dumps({"ok": False, "error": "no live lanes"}, flush=True))
            return 1
        salon(live)
        return 0
    if mode == "retry":
        live = None
        for a in sys.argv[1:]:
            if a.startswith("--live="):
                live = a.split("=", 1)[1].split(",")
        if live is None:
            live = [r["lane"] for r in _iter_rows() if r.get("kind") == "probe" and r.get("ok")]
        retry_failed(live)
        return 0
    if mode == "report":
        print(json.dumps(best_answers(), ensure_ascii=False, indent=2))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
