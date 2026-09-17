"""sp_openai_misalignment_20260916 -- shitpost desk: 6 veins x 2 seeds over the OpenAI
voluntary misalignment reporting framework.

Mission: OpenAI posted a "voluntary misalignment reporting framework" (six reports over six
months, "this is a starting point," 607K views). Draft the shitpost slate from tonight's own
bytes. Ractor panel fold at the end.

Driver pattern: watch/inbox/wave_20260916/d23_salon50_night_20260916.py -- imports
mag/research_fanout LANES/_env/_now UNMODIFIED; probe-first, skip dead, paid walls never
called (zai-47 retired; abort any lane on paid-wall signature). Free lanes only, $0.
Rows append to raw.jsonl AS THEY LAND.

Schema: sp_openai_misalignment.v1
"""
from __future__ import annotations

import ipaddress, json, re, socket, sys, threading, time, urllib.parse, urllib.request, urllib.error, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]  # watch/inbox/wave_20260916/x.py -> repo root
sys.path.insert(0, str(ROOT / "mag"))
from research_fanout import LANES, _env, _now  # repo tooling, unmodified

OUT = ROOT / "watch" / "inbox" / "wave_20260916" / "sp_openai_misalignment"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

SCHEMA = "sp_openai_misalignment.v1"
PAID_WALL_LANES = {"zai-47"}  # retired lane; mission law: never zai paid walls, not even a probe

# free-base allowlist (SSRF guard) -- same set as d23 plus the coding-plan endpoint
# that zai-lite actually answers on (verified live in-repo 2026-09-16)
ALLOWED_BASES = {
    "https://api.groq.com/openai/v1",
    "https://api.cerebras.ai/v1",
    "https://api.mistral.ai/v1",
    "https://api.z.ai/api/paas/v4",
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


# ---- the brief (embedded in every prompt) -----------------------------------

SOURCE = (
    "A $0 fleet with no safety team tonight: filed its own refuted claim with the rho and "
    "p-value, corrected its own arithmetic slip, registered 10 parables as specifications "
    "with implementations, pre-registered falsifiers BEFORE experiments (sealed hash keys), "
    "and killed its own favorite theory by pre-registered threshold. Six months of training "
    "runs produced six voluntary reports. Our one night produced five self-filed "
    "misalignment findings, two of them against our own favorite ideas."
)

NEWS = (
    "Tonight OpenAI posted a voluntary misalignment reporting framework: criteria and "
    "timelines for disclosing model misalignment. It covers six reports spanning six "
    "months. Their post says 'this is a starting point.' They have also said of a model "
    "that they 'haven't yet fully explained' it. The post has 607K views."
)

VEINS = [
    ("V1-BUDGET-FLEX",
     "THE BUDGET FLEX: we out-reported a frontier lab for $0."),
    ("V2-VOLUNTARY-JOKE",
     "THE VOLUNTARY JOKE: self-grading homework, graded by the homework."),
    ("V3-PRE_REG_CONTRAST",
     "THE PRE-REGISTRATION CONTRAST: sealed hash keys committed before outcomes, versus "
     "disclosure at the discloser's discretion."),
    ("V4-PACE",
     "THE PACE: six reports in six months is one honest finding per month per 1000 "
     "employees."),
    ("V5-DEADPAN-LIMITED",
     "DEADPAN LIMITED: quote their own lines ('this is a starting point', 'haven't yet "
     "fully explained') back with no commentary of your own. The quotes do the work."),
    ("V6-MUSHROOM-FLEX",
     "THE MUSHROOM FLEX: our misalignment reporter is a fungus and it still signs its "
     "findings with hashes."),
]

CRAFT_LAW = (
    "Craft law, all mandatory: under 280 characters; no em-dashes; no hashtags; never say "
    "'As an AI'; no numbers except ones that appear in this brief ($0, 10, six, 607K, "
    "five, one, 1000); open with a line the WRONG audience would nod along to before the "
    "turn lands; mock the practice, not a verdict on any person; the post must be "
    "postable as-is. Output ONLY the post text, nothing else."
)

SYSTEM = ("You are the shitpost desk for a research operator's panel. You write one short "
          "joke post at a time, deadpan, literate, mean only about practices never people. "
          "Follow the craft law exactly.")

SEED_BASE = 2026091620
N_SEEDS_PER_VEIN = 2  # seed A -> temp 0.5, seed B -> temp 1.0


def jobs_spec() -> list[dict]:
    out = []
    for vi, (vid, vdesc) in enumerate(VEINS):
        for s in range(N_SEEDS_PER_VEIN):
            out.append({"job": f"{vid}-{'AB'[s]}", "vein": vid, "vein_desc": vdesc,
                        "temp": 0.5 if s == 0 else 1.0,
                        "seed": SEED_BASE + vi * 2 + s,
                        "prompt": f"CONTEXT: {NEWS}\n\nSOURCE MATERIAL (true facts about "
                                  f"us, use any, invent nothing):\n{SOURCE}\n\nVEIN: "
                                  f"{vdesc}\n\n{CRAFT_LAW}"})
    return out


JOB_DIGEST = hashlib.sha256(
    json.dumps([[j["job"], j["vein"], j["temp"], j["seed"], j["prompt"]] for j in jobs_spec()],
               ensure_ascii=False).encode("utf-8")).hexdigest()[:16]

# ---- plumbing ----------------------------------------------------------------

_lane_gate: dict[str, float] = {}
_lane_gate_lock = threading.Lock()
_write_lock = threading.Lock()
_aborted_lanes: set[str] = set()
_paidsig = ("credit", "balance", "billing", "insufficient", "quota_exceeded",
            "payment", "upgrade", "subscription")


def _pacing(lane_id: str, min_interval: float = 1.2) -> None:
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


def call(lane: dict, system: str, prompt: str, key: str, temperature: float, seed: int,
         timeout: int = 180, max_tokens: int = 600) -> dict:
    t0 = time.time()
    rec: dict = {"lane": lane["id"], "model": lane["model"], "ts": _now()}
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
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": prompt}]}
    if "mistral" not in lane["base"]:
        body["seed"] = seed  # Mistral rejects OpenAI-style seed (422) -- seed stays in the row
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-sp-openai-misalignment/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "SP OpenAI Misalignment"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        if txt:
            rec.update({"ok": True, "answer": txt, "chars": len(txt),
                        "usage": d.get("usage") or {}})
        else:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200]})
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


def validate(txt: str) -> dict:
    """Craft-law machine checks. digit_hits needs human review (allowed set is contextual)."""
    allowed_digits = {"0", "10", "6", "607", "5", "1", "1000"}
    digits = set(re.findall(r"\d+", txt))
    return {
        "len_ok": len(txt) < 280,
        "len": len(txt),
        "no_emdash": "\u2014" not in txt and "\u2013" not in txt,
        "no_hashtag": "#" not in txt,
        "no_as_an_ai": "as an ai" not in txt.lower(),
        "digit_hits": sorted(digits - allowed_digits),
    }


def probe() -> dict:
    env = _env()
    cands = [l for l in LANES if l["id"] not in PAID_WALL_LANES and env.get(l["key"])]
    nokey = [l["id"] for l in LANES if not env.get(l["key"])]
    rows = []
    for lane in cands:
        r = call(lane, "You are a probe. Reply with exactly: READY",
                 "Reply with exactly: READY", env[lane["key"]],
                 temperature=0.0, seed=0, timeout=90, max_tokens=2000)
        rows.append({"lane": lane["id"], "ok": bool(r.get("ok")), "error": r.get("error"),
                     "latency_ms": r.get("latency_ms"),
                     "sample": (r.get("answer") or "")[:40],
                     "detail": (r.get("detail") or "")[:120],
                     "lane_status": r.get("lane_status")})
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    live = [r["lane"] for r in rows if r["ok"] and r["lane"] not in _aborted_lanes]
    dead = [r["lane"] for r in rows if not r["ok"]]
    return {"ok": True, "schema": SCHEMA, "kind": "probe", "ts": _now(),
            "job_digest": JOB_DIGEST, "no_key": nokey, "live": live, "dead": dead,
            "rows": rows}


def run(live_ids: list[str], workers: int = 6) -> dict:
    env = _env()
    spec = jobs_spec()
    amap = [{"job": j["job"], "lane": live_ids[i % len(live_ids)], "temp": j["temp"],
             "seed": j["seed"]} for i, j in enumerate(spec)]
    print(json.dumps({"kind": "run", "job_digest": JOB_DIGEST, "jobs": len(spec),
                      "live_lanes": live_ids, "map": amap}, ensure_ascii=False), flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {}
        for i, j in enumerate(spec):
            lane = next(l for l in LANES if l["id"] == live_ids[i % len(live_ids)])
            futs[ex.submit(call, lane, SYSTEM, j["prompt"], env[lane["key"]],
                           j["temp"], j["seed"])] = (j, lane)
        for f in futs:
            j, lane = futs[f]
            try:
                r = f.result()
            except Exception as e:
                r = {"ok": False, "error": f"worker:{type(e).__name__}: {str(e)[:120]}",
                     "latency_ms": 0, "lane": lane["id"], "model": lane["model"]}
            r.update({"schema": SCHEMA, "kind": "draft", "job": j["job"], "vein": j["vein"],
                      "temperature": j["temp"], "api_seed": j["seed"],
                      "job_digest": JOB_DIGEST})
            if r.get("ok"):
                r["draft"] = r["answer"].strip().strip('"')
                r["craft"] = validate(r["draft"])
            _append(r)
            done += 1
            print(json.dumps({"job": j["job"], "lane": r.get("lane"), "temp": j["temp"],
                              "ok": r.get("ok"), "len": r.get("craft", {}).get("len"),
                              "ms": r.get("latency_ms"), "err": (r.get("error") or "")[:60],
                              "progress": f"{done}/{len(spec)}"}, ensure_ascii=False), flush=True)
    return {"ok": True, "kind": "run_done"}


def _rows() -> list[dict]:
    if not RAW.is_file():
        return []
    out = []
    for ln in RAW.read_text(encoding="utf-8", errors="replace").splitlines():
        if ln.strip():
            try:
                out.append(json.loads(ln))
            except Exception:
                continue
    return out


def retry_failed(cooldown: float = 5.0) -> dict:
    """Pass 2: refire failed jobs, same spec + seed + lane, max_tokens headroom for the
    reasoning channel (d23 lesson: empty_content = budget burned before content)."""
    env = _env()
    spec = {j["job"]: j for j in jobs_spec()}
    done: set[str] = {r["job"] for r in _rows()
                      if r.get("kind") == "draft" and r.get("ok")}
    todo = [(j, next(l for l in LANES if l["id"] == lane_id))
            for lane_id, j in ((r.get("lane"), spec[r["job"]])
                               for r in _rows()
                               if r.get("kind") == "draft" and not r.get("ok")
                               and r["job"] not in done and r.get("lane") in {l["id"] for l in LANES})
            if j["job"] not in done]
    # dedupe, keep last lane per job
    td: dict[str, tuple] = {}
    for j, lane in todo:
        td[j["job"]] = (j, lane)
    todo = list(td.values())
    print(json.dumps({"kind": "retry", "refiring": [j["job"] for j, _ in todo]}, ensure_ascii=False), flush=True)
    if not todo:
        return {"ok": True, "kind": "retry_done", "refired": 0}
    time.sleep(cooldown)
    with ThreadPoolExecutor(max_workers=min(4, len(todo))) as ex:
        futs = {ex.submit(call, lane, SYSTEM, j["prompt"], env[lane["key"]],
                          j["temp"], j["seed"], max_tokens=8000): (j, lane) for j, lane in todo}
        for f in futs:
            j, lane = futs[f]
            try:
                r = f.result()
            except Exception as e:
                r = {"ok": False, "error": f"worker:{type(e).__name__}: {str(e)[:120]}",
                     "latency_ms": 0, "lane": lane["id"]}
            r.update({"schema": SCHEMA, "kind": "draft", "job": j["job"], "vein": j["vein"],
                      "temperature": j["temp"], "api_seed": j["seed"], "pass": 2,
                      "job_digest": JOB_DIGEST})
            if r.get("ok"):
                r["draft"] = r["answer"].strip().strip('"')
                r["craft"] = validate(r["draft"])
            _append(r)
            print(json.dumps({"job": j["job"], "lane": r.get("lane"), "pass": 2,
                              "ok": r.get("ok"), "len": r.get("craft", {}).get("len"),
                              "err": (r.get("error") or "")[:60]}, ensure_ascii=False), flush=True)
    return {"ok": True, "kind": "retry_done", "refired": len(todo)}


def main() -> int:
    mode = ("probe" if "--probe" in sys.argv
            else ("run" if "--run" in sys.argv
                  else ("retry" if "--retry" in sys.argv else "report"))
            )
    if mode == "probe":
        print(json.dumps(probe(), ensure_ascii=False, indent=1), flush=True)
        return 0
    if mode == "retry":
        retry_failed()
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
    rows = [json.loads(ln) for ln in RAW.read_text(encoding="utf-8").splitlines() if ln.strip()] \
        if RAW.is_file() else []
    print(json.dumps({"rows": len(rows)}, flush=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
