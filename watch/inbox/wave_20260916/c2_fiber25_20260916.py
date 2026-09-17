"""c2_fiber25_20260916 -- CONCERT 002: a 25-segment battery on fiber-optic I/O into mycelium.

Mission (operator, verbatim): "go 25 wide, scale the ask via our gap analysis" — fiber optics fed
into the mycelial network after complete colonization, as optical I/O for the cube program
(WRITE = pulses, READ = photometry/transmission, routing — the Dirac layer's optical analog).

Driver pattern: wave_20260916/d23_salon50_night_20260916.py (probe -> run -> cooldown retry ->
summarize; rows appended to raw.jsonl AS THEY LAND; failures preserved; SSRF allowlist +
resolved-IP guard). Uses mag/research_fanout LANES/_env/_now UNMODIFIED. Repo code not edited.

D22 rotation table adopted: groq-qwen capped at max_tokens=780 (OTPM gate); or-nemotron gets
timeout 300 s (37 s for READY); stealth or-union-alpha called non-streaming, timeout >=180 s (U8).
zai-lite held OUT of the carrier rotation (law 15: burst lane, never a default carrier) — reserve
only. $0: free lanes + free-window stealth if alive.

Schema: c2_fiber25.v1
"""
from __future__ import annotations

import ipaddress, json, socket, sys, threading, time, urllib.parse, urllib.request, urllib.error, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "mag"))
from research_fanout import LANES, _env, _now  # repo tooling, unmodified

OUT = ROOT / "watch" / "inbox" / "physical_computing" / "receipts" / "concert002_fiber25"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

PAID_WALL_LANES: set[str] = set()      # zai-47 retired from registry; none left to pre-filter
RESERVE_LANES = {"zai-lite"}           # law 15: burst lane, never a default carrier — retry reserve only

ALLOWED_BASES = {  # same free-base allowlist as mag/scale_salon.py (SSRF guard)
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


SYSTEM = ("You are an independent witness in a multi-model research salon on a mycelium-hardware "
          "experiment (fiber optics as optical I/O into living mycelium). Answer from your own "
          "knowledge and judgment. Take the position you actually believe; do not fence-sit. Give "
          "concrete, checkable specifics — mechanisms, numbers, materials, citations you are "
          "confident of. If unsure, say which part is uncertain. No preamble. Hard limit: 160 words.")

CONTEXT = ("CONTEXT (shared): The cube is an instrumented block of living mycelium (oyster/"
           "Pleurotus on sawdust substrate); electrodes read its electrical spiking. Program "
           "ladder: sensing -> memory -> compute. NEW HYPOTHESIS under test: after complete "
           "colonization, optical fibers inserted into the block give light-based I/O — WRITE "
           "(light pulses into the network), READ (photometry of transmission/return light), and "
           "routing between points — the optical analog of the cube's electrode layer. Budget is "
           "hobby tier (~$40 add-on). Answer as an independent expert witness: give concrete "
           "mechanisms, numbers, and materials where you can; state uncertainty honestly instead "
           "of inventing numbers.")

# THE 25 SEGMENTS (5 families x 5) — registered in the receipt BEFORE firing.
# PR4/PR5 derived to fill the 5x5 grid (mission listed 3 PROGRAM asks) — marked in the receipt.
SEGMENTS = [
    # A. OPTICAL PHYSICS
    ("OP1", "A-optical-physics",
     "Does living mycelium transmit or guide light? Is there credible evidence of waveguiding "
     "along individual hyphae, or does the tissue act as a diffuser/scatterer? State the strongest "
     "published evidence you know."),
    ("OP2", "A-optical-physics",
     "What reduced scattering coefficient (mm^-1) would you expect for dense living mycelium at "
     "visible wavelengths (~500-650 nm), given tissue optics? What does that imply for how far a "
     "beam survives inside a colonized block?"),
    ("OP3", "A-optical-physics",
     "Does living fungal mycelium autofluoresce under visible/UV excitation? Which fluorophores "
     "(e.g., chitin, NADH, flavins), what excitation/emission bands, and could autofluorescence "
     "serve as an optical READ signal?"),
    ("OP4", "A-optical-physics",
     "Do fungi show phototropic or photo-spiking responses — measurable electrical or growth "
     "responses to light pulses? What timescale and light dose would you expect — can light act as "
     "a stimulus equivalent to an electrode pulse?"),
    ("OP5", "A-optical-physics",
     "What light intensity/dose risks damaging living mycelium (thermal or photochemical) at "
     "fiber-tip powers? Estimate a safe pulse regime for a hobby source (650 nm or 520 nm) inside "
     "a colonized block."),
    # B. ENGINEERING
    ("EN1", "B-engineering",
     "For a hobby-tier (~$40) build: PMMA plastic optical fiber vs glass/silica fiber into living "
     "mycelium — which and why? Consider cost, sterilization tolerance, flexibility, coupling ease."),
    ("EN2", "B-engineering",
     "Design a sterile optical feedthrough into an already-colonized fruiting tub (still-air-box "
     "constraints): how do you insert fiber after colonization without contamination? Ports, "
     "filters, adhesives, heat?"),
    ("EN3", "B-engineering",
     "Does fiber insertion traumatize a fully colonized mycelial block, and should you wait ~2 "
     "weeks after insertion before recording? What wound response (regrowth, melanization, "
     "contamination) would you expect?"),
    ("EN4", "B-engineering",
     "What coupling/alignment tolerance does a hobby build need between PMMA fiber (1 mm core) and "
     "LED/photodiode/laser? How much does misalignment and bending cost in coupling loss (numbers)?"),
    ("EN5", "B-engineering",
     "What is the practical maximum fiber count for a $40 array into one tub, and how should "
     "fibers be arranged (grid, co-located with electrodes, 1:1 mapping)? Cheap mux/demux options?"),
    # C. MEMORY
    ("ME1", "C-memory",
     "Could a light pulse through an inserted fiber WRITE state into a mycelial network the way an "
     "electrode pulse can (cross-modality equivalence)? What mechanism would carry optical "
     "excitation into the electrical/spiking state?"),
    ("ME2", "C-memory",
     "If optical energy changes mycelial state (photobleaching, local heating, photochemical "
     "products), how long would that state persist? Is there any plausible optical memory trace, "
     "and what are the photobleaching limits?"),
    ("ME3", "C-memory",
     "Design a read-after-write fidelity test for the optical channel: write with fiber A (pulse), "
     "read with fiber B (transmission/photometry). What signal change counts as a successful "
     "write, and what SNR/drift pitfalls?"),
    ("ME4", "C-memory",
     "Can writes be addressed by fiber position — is the write local to the illuminated volume, or "
     "does the network integrate globally? What spatial resolution (mm) is plausible through a "
     "scattering block?"),
    ("ME5", "C-memory",
     "Estimate the information capacity per fiber channel (bits): given photometric/electrical "
     "readout bandwidth (~Hz) and reliably distinguishable states, what order of magnitude is "
     "defensible, and why?"),
    # D. COMPUTE
    ("CO1", "D-compute",
     "For an optical-hyphal hybrid (light in fibers, computation in the network), what routing "
     "architecture is coherent? Is there any mechanism by which the network could route light "
     "between fibers, or must routing be fiber-side?"),
    ("CO2", "D-compute",
     "Compare latency: optical I/O (fiber + photodiode, ~ns) vs mycelial electrical signaling "
     "(~mm/s-cm/s) vs observed spike timescales. Where is the real bottleneck for any compute "
     "claim?"),
    ("CO3", "D-compute",
     "Can multiple optical channels (different fibers, WDM colors) coexist through a scattering "
     "mycelial block? Quantify expected crosstalk given speckle/diffusion — is multi-channel "
     "coherent I/O plausible at hobby tier?"),
    ("CO4", "D-compute",
     "Are there plausible hybrid electro-optic gates in mycelium — light modulating electrical "
     "response, or electrical state modulating light transmission (electro-absorption, swelling)? "
     "Rank by physical plausibility; name analogs in other media."),
    ("CO5", "D-compute",
     "What is the honest scaling path and wall for optical I/O on mycelial compute (channels x "
     "states x speed) vs electrode arrays? At what point does the substrate stop mattering and the "
     "optoelectronics dominate?"),
    # E. PROGRAM
    ("PR1", "E-program",
     "What can an optical fiber layer do for the cube that electrodes cannot? Identify the ONE "
     "unique capability (spatially resolved read/write? no electrochemical artifact? telemetry "
     "through the wall?) and argue it."),
    ("PR2", "E-program",
     "Design the falsifier for a $40 optical add-on on the instrumented cube: what pre-registered "
     "measurement distinguishes 'optical channel carries real signal' from artifact (heating, "
     "ambient light, photodiode drift)? State the null."),
    ("PR3", "E-program",
     "Break down a $40 budget for the optical add-on: sources, PMMA fiber, photodiodes, feedthrough "
     "hardware — realistic unit costs and where the build fails first at $0 vs $40 vs $100."),
    ("PR4", "E-program",
     "Specify the v1 protocol: what to log (pulse schedule, photodiode trace, electrode spikes, "
     "temperature), for how long, and what data schema makes the result falsifiable and reusable?"),
    ("PR5", "E-program",
     "Decision gate: after the $40 add-on runs, what result promotes the optical layer into the "
     "program ladder (sensing -> memory -> compute) as a real channel, and what result kills it?"),
]

QUESTION_DIGEST = hashlib.sha256(
    json.dumps(SEGMENTS, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
CONTEXT_TOKENS = len(CONTEXT.split())  # transparency: context size in words (~tokens)

N_SEGMENTS = len(SEGMENTS)  # 25
SEED_BASE = 2026091600
TEMPERATURE = 0.2  # research battery, fixed (not a temperature ladder salon)

# D22 rotation table: groq-qwen OTPM gate -> cap output tokens; or-nemotron slow -> long timeout
LANE_MAX_TOKENS = {"groq-qwen": 780}
LANE_TIMEOUT = {"or-nemotron": 300, "or-union-alpha": 300}  # U8: union-alpha >=180 s

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


def call(lane: dict, question: str, key: str, temperature: float, seed: int,
         timeout: int | None = None, max_tokens: int | None = None, attempt: int = 1) -> dict:
    lid = lane["id"]
    timeout = timeout or LANE_TIMEOUT.get(lid, 300)
    max_tokens = max_tokens or LANE_MAX_TOKENS.get(lid, 2600)
    t0 = time.time()
    rec: dict = {"lane": lid, "model": lane["model"], "ts": _now(), "attempt": attempt}
    if lid in PAID_WALL_LANES:
        rec.update({"ok": False, "error": "paid_wall_never_called", "latency_ms": 0})
        return rec
    try:
        url = _guard(lane["base"]).rstrip("/") + "/chat/completions"
    except ValueError as e:
        rec.update({"ok": False, "error": f"ssrf_guard: {e}", "latency_ms": 0})
        return rec
    _pacing(lid)
    body = {"model": lane["model"], "temperature": temperature, "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": f"{CONTEXT}\n\nSEGMENT: {question}"}]}
    if "mistral" not in lane["base"]:
        # Mistral rejects OpenAI-style `seed` (HTTP 422 extra_forbidden) — api_seed stays in the row
        body["seed"] = seed
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-c2-fiber25/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "CONCERT002 Fiber25"})
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
                _aborted_lanes.add(lid)
            rec["lane_status"] = "ABORTED_PAID_WALL"
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:140]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


def job_for_segment(n: int, live_ids: list[str]) -> dict:
    qid, family, q = SEGMENTS[n]
    lane_id = live_ids[n % len(live_ids)]
    lane = next(l for l in LANES if l["id"] == lane_id)
    return {"n": n, "qid": qid, "family": family, "q": q, "lane": lane,
            "seed": SEED_BASE + n}


def probe() -> dict:
    """One READY ping per candidate carrier (reserves + paid walls excluded BEFORE any call)."""
    env = _env()
    cands = [l for l in LANES
             if l["id"] not in PAID_WALL_LANES and l["id"] not in RESERVE_LANES and env.get(l["key"])]
    skipped = [l["id"] for l in LANES if l["id"] in PAID_WALL_LANES]
    reserved = [l["id"] for l in LANES if l["id"] in RESERVE_LANES]
    nokey = [l["id"] for l in LANES if not env.get(l["key"])]
    rows = []
    for lane in cands:
        r = call(lane, "Reply with exactly: READY", env[lane["key"]],
                 temperature=0.0, seed=0, timeout=min(LANE_TIMEOUT.get(lane["id"], 120), 300),
                 max_tokens=LANE_MAX_TOKENS.get(lane["id"], 2600))
        rows.append({"lane": lane["id"], "ok": bool(r.get("ok")), "error": r.get("error"),
                     "latency_ms": r.get("latency_ms"),
                     "sample": (r.get("answer") or "")[:40],
                     "detail": (r.get("detail") or "")[:120],
                     "lane_status": r.get("lane_status")})
        print(json.dumps(rows[-1], ensure_ascii=False), flush=True)
    live = [r["lane"] for r in rows if r["ok"] and r["lane"] not in _aborted_lanes]
    dead = [r["lane"] for r in rows if not r["ok"]]
    out = {"ok": True, "schema": "c2_fiber25.v1", "kind": "probe", "ts": _now(),
           "question_digest": QUESTION_DIGEST, "context_words": CONTEXT_TOKENS,
           "skipped_paid_wall": skipped, "reserve_lanes": reserved, "no_key": nokey,
           "live": live, "dead": dead, "rows": rows}
    (OUT / "probe.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def run(live_ids: list[str], workers: int = 8) -> dict:
    env = _env()
    jobs = [job_for_segment(n, live_ids) for n in range(N_SEGMENTS)]
    print(json.dumps({"kind": "run", "question_digest": QUESTION_DIGEST,
                      "segments": len(jobs), "live_lanes": live_ids,
                      "map": [{"n": j["n"], "qid": j["qid"], "lane": j["lane"]["id"],
                               "seed": j["seed"]} for j in jobs]}, ensure_ascii=False), flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, j["lane"], j["q"], env[j["lane"]["key"]],
                          TEMPERATURE, j["seed"]): j for j in jobs}
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
            r.update({"schema": "c2_fiber25.v1", "kind": "segment", "n": j["n"], "qid": j["qid"],
                      "family": j["family"], "question": j["q"], "temperature": TEMPERATURE,
                      "api_seed": j["seed"], "pass": 1, "question_digest": QUESTION_DIGEST})
            _append(r)
            done += 1
            print(json.dumps({"n": j["n"], "qid": j["qid"], "lane": j["lane"]["id"],
                              "ok": r.get("ok"), "chars": r.get("chars"),
                              "ms": r.get("latency_ms"), "err": (r.get("error") or "")[:60],
                              "progress": f"{done}/{len(jobs)}"}, ensure_ascii=False),
                  flush=True)
    return summarize()


def retry_failed(cooldown: float = 60.0) -> dict:
    """Pass 2: refire failed segments once, same segment->lane map, after a cooldown. Append-only."""
    env = _env()
    allowed = [l["id"] for l in LANES
               if l["id"] not in PAID_WALL_LANES and l["id"] not in RESERVE_LANES]
    seen = {r["lane"] for r in _iter_rows()
            if r.get("kind") == "segment" and r.get("lane") in allowed}
    live_ids = [l["id"] for l in LANES if l["id"] in seen]  # LANES order -> identical map
    got_ok: set[int] = {r["n"] for r in _iter_rows()
                        if r.get("kind") == "segment" and r.get("ok")}
    todo = [job_for_segment(n, live_ids) for n in range(N_SEGMENTS) if n not in got_ok]
    todo = [j for j in todo if j["lane"]["id"] not in _aborted_lanes]
    print(json.dumps({"kind": "retry", "refiring": [j["n"] for j in todo]}, ensure_ascii=False), flush=True)
    if not todo:
        return summarize()
    time.sleep(cooldown)
    with ThreadPoolExecutor(max_workers=min(4, len(todo))) as ex:
        # pass-2 headroom for reasoning channels (d23 lesson: budget can burn in reasoning)
        futs = {ex.submit(call, j["lane"], j["q"], env[j["lane"]["key"]],
                          TEMPERATURE, j["seed"],
                          max_tokens=max(4000, LANE_MAX_TOKENS.get(j["lane"]["id"], 4000)),
                          attempt=2): j for j in todo}
        for f in futs:
            j = futs[f]
            try:
                r = f.result()
            except Exception as e:
                r = {"ok": False, "error": f"worker:{type(e).__name__}: {str(e)[:120]}",
                     "latency_ms": 0}
            r.update({"schema": "c2_fiber25.v1", "kind": "segment", "n": j["n"], "qid": j["qid"],
                      "family": j["family"], "question": j["q"], "temperature": TEMPERATURE,
                      "api_seed": j["seed"], "pass": 2, "question_digest": QUESTION_DIGEST})
            _append(r)
            print(json.dumps({"n": j["n"], "pass": 2, "lane": j["lane"]["id"],
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
    rows = [r for r in _iter_rows() if r.get("kind") == "segment"]
    best: dict[int, dict] = {}  # latest successful attempt wins per segment
    for r in rows:
        cur = best.get(r["n"])
        if cur is None or (r.get("ok") and not cur.get("ok")) or (r.get("ok") and r.get("pass", 1) >= cur.get("pass", 1)):
            best[r["n"]] = r
    latest = sorted(best.values(), key=lambda r: r["n"])
    ok = [r for r in latest if r.get("ok")]
    summary = {"ok": True, "schema": "c2_fiber25.v1", "kind": "summary", "ts": _now(),
               "question_digest": QUESTION_DIGEST,
               "segments": len(latest), "answered": len(ok),
               "failed": len(latest) - len(ok),
               "per_family": {}, "per_segment": {}, "per_lane": {}, "diversity": {}}
    fams = sorted({f for _q, f, _s in SEGMENTS})
    for fam in fams:
        frows = [r for r in latest if r.get("family") == fam]
        fok = [r for r in frows if r.get("ok")]
        pairs = [_jaccard(a["answer"], b["answer"])
                 for i, a in enumerate(fok) for b in fok[i + 1:]]
        summary["per_family"][fam] = {
            "segments": len(frows), "answered": len(fok),
            "lanes": sorted({r["lane"] for r in fok}),
            "pairwise_jaccard_mean": round(sum(pairs) / len(pairs), 4) if pairs else None,
        }
    for r in latest:
        summary["per_segment"][r["qid"]] = {
            "ok": bool(r.get("ok")), "lane": r.get("lane"), "pass": r.get("pass", 1),
            "chars": r.get("chars"), "error": r.get("error")}
    for ln in sorted({r.get("lane") or "unknown" for r in latest}):
        lrows = [r for r in latest if (r.get("lane") or "unknown") == ln]
        summary["per_lane"][ln] = {
            "answered": sum(1 for r in lrows if r.get("ok")),
            "failed": sum(1 for r in lrows if not r.get("ok")),
            "errors": sorted({(r.get("error") or "")[:40] for r in lrows if not r.get("ok")})}
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(json.dumps(summary["per_family"] | {"answered": summary["answered"],
                                              "segments": summary["segments"]}, ensure_ascii=False),
          flush=True)
    return summary


def answers_markdown() -> str:
    """Emit the full 25-answer tape as markdown (input to the Rashomon fold in the receipt)."""
    rows = [r for r in _iter_rows() if r.get("kind") == "segment"]
    best: dict[int, dict] = {}
    for r in rows:
        cur = best.get(r["n"])
        if cur is None or (r.get("ok") and not cur.get("ok")) or (r.get("ok") and r.get("pass", 1) >= cur.get("pass", 1)):
            best[r["n"]] = r
    lines = []
    for n in range(N_SEGMENTS):
        qid, fam, q = SEGMENTS[n]
        r = best.get(n)
        lines.append(f"### {qid} — {q}")
        if r and r.get("ok"):
            lines.append(f"*lane `{r['lane']}` · {r['model']} · pass {r.get('pass',1)} · "
                         f"{r.get('chars')} chars · seed {r.get('api_seed')}*")
            lines.append("")
            lines.append(r["answer"])
        else:
            lines.append(f"*FAILED on `{r.get('lane') if r else '?'}` — {r.get('error') if r else 'no attempt'}*")
        lines.append("")
    md = "\n".join(lines)
    (OUT / "answers.md").write_text(md, encoding="utf-8")
    return md


def main() -> int:
    mode = "probe" if "--probe" in sys.argv else ("run" if "--run" in sys.argv
                                                  else ("retry" if "--retry" in sys.argv
                                                        else ("answers" if "--answers" in sys.argv
                                                              else "report")))
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
    if mode == "answers":
        answers_markdown()
        return 0
    summarize()
    return 0


if __name__ == "__main__":
    sys.exit(main())
