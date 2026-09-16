"""a4_astra_smoke_12 -- ONE bounded 12-lane tri-state smoke of the Astra ask (wave 20260916, A4).

Ask package: watch/inbox/astra_ask_package/ (44-claim sovereign-agent research brief).
The 44 claims are compressed into 12 claim families (F1-F12); each lane independently
renders a tri-state verdict (Supported / Disputed / Unproven) per family with one line
of evidence. Uses the repo's own fanout plumbing (mag/research_fanout LANES/_env)
unmodified; driver pattern follows mag/scale_salon.py. Free lanes only, $0.
Failures are preserved as rows. Raw answers -> watch/salon_responses/astra_smoke_12/.
Schema: astra_smoke.v1
"""
from __future__ import annotations

import ipaddress, json, socket, sys, time, urllib.parse, urllib.request, urllib.error, re, hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "mag"))
from research_fanout import LANES, _env, _now  # repo tooling, unmodified

OUT = ROOT / "watch" / "salon_responses" / "astra_smoke_12"
OUT.mkdir(parents=True, exist_ok=True)

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


SYSTEM = ("You are an independent systems-research referee. Judge strictly from your own "
          "knowledge of the published literature; do not try to please anyone. Be terse "
          "and concrete. Output only the 12 contract lines, no preamble, no closing.")


def families() -> str:
    return """You are smoke-testing an independent research brief on locally operated sovereign agent systems. For EACH claim family below, give your OWN tri-state verdict:
- Supported = published evidence you know supports the stated formulation
- Disputed = you know counterexamples, incompatible evidence, or an invalid inference
- Unproven = evidence you know of is missing or inconclusive
One line of evidence per family. If you do not know, say Unproven and say so.

F1 (overall composition): Literature supports constituent agent mechanisms (feedback-conditioned behavior, cost-sensitive routing, duplicate suppression, content-addressed storage) but does NOT establish that their composition yields reliable unattended local agent operation; end-to-end autonomy of such a stack is unproven.

F2 (orchestration): Reflexion-style stored linguistic feedback has prior support, but automatic beneficial evolution from inherited lessons does not follow (lessons can preserve errors); intrinsic self-correction results are conditional and contested (Huang et al. 2024 vs Liu et al. 2024); multiagent systems add their own failure surface (MAST taxonomy: specification, coordination, verification).

F3 (routing and resources): Learned strong/weak model routing is an established method (RouteLLM, preference-data trained), but fleet-level cost-quality economics remain an empirical question; concurrent loaded models and parallel requests to one model are distinct capacities with distinct memory costs.

F4 (authority containment): Scoped API credentials alone do not establish child-process authority containment; kernel-enforced capability attenuation (Capsicum) plus adversarial tool-agent evaluation (AgentDojo) is the relevant bar; prompt instructions like "child <= parent" are not an enforcement boundary.

F5 (observability): Internal instrumentation differs from externally observed behavior; a service can return wrong content with HTTP 200 (SRE golden signals); aggregate failure counts lacking attempt identifiers cannot prove a count of distinct executions.

F6 (durable execution): Append-only hash-linked history alone is not durable-execution semantics (Temporal separates deterministic decisions from side-effecting activities); caller-side receipts do not give exactly-once effects - receiver-side completion records coupled to dedup state do (RIFL); a dead-worker judgment does not fence its outstanding writes (Chubby sequencers); a transactional store closes only transactions it owns (SQLite), not arbitrary file effects.

F7 (memory novelty): Shared memory-hierarchy ideas do not establish architectural identity with Engram (learned n-gram lookup tables); external-knowledge and predictive caching have substantial prior art (RAGCache, TeleRAG, PerCache); content-addressed storage alone does not supply semantic retrieval, freshness, or authorization (Venti, Zanzibar).

F8 (scale arithmetic): 19,000,000 vectors x 256 dims x fp16 (2 bytes) = 9,728,000,000 bytes; plus 608,000,000 bytes of 32-byte keys and 152,000,000 bytes of uint64 slot IDs totals 10,488,000,000 bytes = 9.768 GiB before index slack, text, metadata and runtime overhead; a second full vector copy adds 9.060 GiB. Verify the arithmetic and state whether estimate-only (unmeasured) budgets support a deployment feasibility claim.

F9 (canary attribution): Membership inference cannot generally prove training-data inclusion for opaque production models; extraction of a secret via retrieval or context does not imply the weights learned it; there is no universal duplicate-count threshold for memorization (Carlini et al.: dose-response depends on duplication, prefix length, model scale).

F10 (trial statistics): 512 candidate outputs (32 primary + 400 sensitivity + 80 sham) compared against sixteen 128-bit random suffixes reserve 8,192 comparisons, plus 256 from 16 registered exposures = 8,448 of a 10,000 cap; for an independent candidate, false-match probability is <= Q/2^128 (about 2.94e-35 at Q=10,000); with ten trials and zero sham hits, the exact binomial upper bound is about 0.422, so ten clean shams do NOT demonstrate a very low contamination rate. Verify the arithmetic.

F11 (verification independence): First-pass agreement between two agent workers does not by itself prove collapse, sycophancy, or correctness (agreement can reflect decisive evidence, shared flaw, or failed independence - Wynn et al. 2025, Yao et al. 2025); each verifier should be tested against hidden ground truth before being compared to the other.

F12 (publication posture): The defensible publication for such a local system is a bounded systems contribution with open failure evidence (protocol/design category) until independently replicated; correctness and performance claims need different evidential standards (one duplicate effect refutes a no-duplicate invariant; a null performance difference may be merely inconclusive).

OUTPUT CONTRACT - exactly 12 lines, no preamble, no markdown:
F1 | Supported|Disputed|Unproven | <one line of evidence>
F2 | ... (through F12)"""


def call(lane: dict, prompt: str, key: str, timeout: int = 240, max_tokens: int = 3000) -> dict:
    t0 = time.time()
    rec: dict = {"lane": lane["id"], "model": lane["model"], "ts": _now()}
    try:
        url = _guard(lane["base"]).rstrip("/") + "/chat/completions"
    except ValueError as e:
        rec.update({"ok": False, "error": f"ssrf_guard: {e}", "latency_ms": 0})
        return rec
    body = {"model": lane["model"], "temperature": 0.2, "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-astra-smoke/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "Astra Smoke 12"})
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
        rec.update({"ok": False, "error": f"HTTP {e.code}",
                    "detail": e.read().decode("utf-8", "replace")[:200]})
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:140]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


VERDICT_RE = re.compile(r"^F(\d{1,2})\s*\|\s*(supported|disputed|unproven)\s*\|", re.I)


def parse_verdicts(txt: str) -> dict[int, tuple[str, str]]:
    out: dict[int, tuple[str, str]] = {}
    for ln in txt.splitlines():
        m = VERDICT_RE.match(ln.strip())
        if m:
            fam = int(m.group(1))
            verdict = m.group(2).capitalize()
            evidence = ln.strip().split("|", 2)[-1].strip()
            if fam not in out:
                out[fam] = (verdict, evidence[:300])
    return out


def retry_failed(cooldown: int = 45, only: list[str] | None = None) -> int:
    """Pass N: refire ONLY lanes with no ok row in raw.jsonl. One attempt each."""
    raw = OUT / "raw.jsonl"
    prev_ok: set[str] = set()
    if raw.is_file():
        for ln in raw.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln)
                if r.get("ok"):
                    prev_ok.add(r["lane"])
    env = _env()
    todo = [l for l in LANES if env.get(l["key"]) and l["id"] not in prev_ok]
    if only is not None:
        todo = [l for l in todo if l["id"] in only]
    print(f"retry lanes: {[l['id'] for l in todo]}", flush=True)
    if todo:
        time.sleep(cooldown)  # let free-tier rate-limit windows reset
    rows = []
    with ThreadPoolExecutor(max_workers=max(1, len(todo))) as ex:
        futs = [ex.submit(call, lane, families(), env[lane["key"]],
                          timeout=280, max_tokens=12000) for lane in todo]
        for f in futs:
            r = f.result()
            r["pass"] = 2
            rows.append(r)
            print(f"  {r['lane']:14s} {'OK ' if r['ok'] else 'ERR'} "
                  f"{r.get('chars', '')} chars {r['latency_ms']}ms"
                  + ("" if r["ok"] else f"  {str(r.get('error', ''))[:70]}"), flush=True)
    if rows:
        with raw.open("a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps({"schema": "astra_smoke.v1", **r}, ensure_ascii=False) + "\n")
        for r in rows:
            body = (r.get("answer") if r.get("ok") else
                    f"FAILED: {r.get('error')} :: {str(r.get('detail', ''))[:200]}")
            (OUT / f"astra_smoke_12__{r['lane']}.md").write_text(
                f"# lane {r['lane']} ({r['model']}) — pass 2 — "
                f"{'OK' if r.get('ok') else 'FAILED'} — {r['latency_ms']}ms\n\n{body}\n",
                encoding="utf-8")
    rebuild_matrix()
    return 0


def rebuild_matrix() -> None:
    matrix: dict[str, dict[int, str]] = {}
    latest: dict[str, dict] = {}
    raw = OUT / "raw.jsonl"
    if raw.is_file():
        for ln in raw.read_text(encoding="utf-8", errors="replace").splitlines():
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
            except Exception:
                continue
            latest[r["lane"]] = r  # append-only tape: last row per lane wins
    for lane, r in latest.items():
        if r.get("ok"):
            v = parse_verdicts(r["answer"])
            matrix[lane] = {fam: verd for fam, (verd, _ev) in v.items()}
    (OUT / "verdict_matrix.json").write_text(json.dumps(
        {"schema": "astra_smoke.v1", "families": 12, "matrix": matrix},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"matrix: {len(matrix)} lanes with parsed verdicts", flush=True)


def main() -> int:
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = a.split("=", 1)[1].split(",")
    if "--retry" in sys.argv:
        return retry_failed(cooldown=90, only=only)
    env = _env()
    live = [l for l in LANES if env.get(l["key"])]
    print(f"lanes armed: {len(live)}/{len(LANES)}", flush=True)
    prompt = families()
    prompt_digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    rows = []
    with ThreadPoolExecutor(max_workers=max(1, len(live))) as ex:
        futs = [ex.submit(call, lane, prompt, env[lane["key"]]) for lane in live]
        for f in futs:
            r = f.result()
            rows.append(r)
            print(f"  {r['lane']:14s} {'OK ' if r['ok'] else 'ERR'} "
                  f"{r.get('chars', '')} chars {r['latency_ms']}ms"
                  + ("" if r["ok"] else f"  {str(r.get('error', ''))[:70]}"), flush=True)

    raw = OUT / "raw.jsonl"
    with raw.open("a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({"schema": "astra_smoke.v1", "prompt_digest": prompt_digest,
                                 **r}, ensure_ascii=False) + "\n")

    # per-lane raw answer files
    for r in rows:
        body = (r.get("answer") if r.get("ok") else
                f"FAILED: {r.get('error')} :: {str(r.get('detail', ''))[:200]}")
        (OUT / f"astra_smoke_12__{r['lane']}.md").write_text(
            f"# lane {r['lane']} ({r['model']}) — {'OK' if r.get('ok') else 'FAILED'}"
            f" — {r['latency_ms']}ms\n\n{body}\n", encoding="utf-8")

    # parsed tri-state matrix
    matrix: dict[str, dict[int, str]] = {}
    for r in rows:
        if r.get("ok"):
            v = parse_verdicts(r["answer"])
            matrix[r["lane"]] = {fam: verd for fam, (verd, _ev) in v.items()}
    (OUT / "verdict_matrix.json").write_text(json.dumps(
        {"schema": "astra_smoke.v1", "prompt_digest": prompt_digest,
         "families": 12, "matrix": matrix}, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for r in rows if r.get("ok"))
    print(f"done: {ok}/{len(rows)} lanes answered; parsed verdicts from {len(matrix)}; "
          f"raw -> {raw}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
