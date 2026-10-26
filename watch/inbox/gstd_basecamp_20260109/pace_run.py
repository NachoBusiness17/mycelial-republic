"""VOCAB lane pace run (2026-10-09): bank honest gstd evidence, then route
3 real cheap asks through the gps router with the new gstd tier live.

Instrument for receipt ROUTER_VOCAB_LANDED.md. Every verdict cites real
bytes (Q28 evidence-resolution gate); every route lands a receipts.jsonl
row. No em-dashes.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.gps_mcp.ledger import CapabilityLedger  # noqa: E402
from tools.gps_mcp.providers import build_registry, load_config  # noqa: E402
from tools.gps_mcp.router import Router  # noqa: E402

GW = "http://localhost:8080/v1"
BUILDOUT = ROOT / "watch" / "inbox" / "gstd_desktop_buildout_20260109.md"
SRC = "gstd-node-live-20261009"

ledger = CapabilityLedger(ROOT / "tools" / "gps_mcp" / "gps_ledger.db3")
registry = build_registry(load_config(ROOT / "tools" / "gps_mcp" / "config.gstd.json"))
router = Router(registry, ledger, ROOT / "tools" / "gps_mcp" / "receipts.jsonl")


def gw_post(model: str, prompt: str, task_shape: str, tries: int = 8) -> dict:
    """POST the node gateway sovereign path with 429 backoff."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "task_shape": task_shape,
    }).encode("utf-8")
    last = ""
    for i in range(tries):
        req = urllib.request.Request(
            GW + "/chat/completions", data=body,
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:200]}"
            if exc.code != 429:
                raise
        print(f"  429 ({last[:60]}), backoff 25s", flush=True)
        time.sleep(25)
    raise RuntimeError(f"gateway never opened the bucket: {last}")


def content(resp: dict) -> str:
    return str((resp.get("choices") or [{}])[0].get("message", {}).get("content", ""))


# -- Part A: pre-existing documented evidence (buildout receipt section 5) ----
r1 = ledger.record_verdict(
    "gemma:2b", "probe", True,
    evidence_path=str(BUILDOUT),
    evidence_source=f"{SRC}: buildout receipt section 5c smoke (Router OK, tier gstd, sovereignty true)",
)
print("A1 buildout-smoke verdict:", r1.as_dict()["evidence_status"],
      "rate", round(r1.pass_rate, 3), "n", r1.sample_size)

# -- Part B: three real shapes, evidence-farm then router route ---------------

SUMMARY_TEXT = (
    "The gstd desktop build-out on 2026-10-09 registered our node with the "
    "platform, started a cloudflared quick tunnel, wired GSTD_PUBLIC_URL into "
    "the docker compose override, and proved inference three ways: a direct "
    "Ollama passthrough inside the container, the same endpoint through the "
    "public tunnel, and the gstd router path which answered with tier gstd "
    "and sovereignty true."
)
CLASSIFY_LINES = "\n".join([
    "tools/gps_router_v0.py",
    "watch/inbox/ml_moonshot_20261007/ml3_route_table.json",
    "tools/gps_mcp/gps_ledger.db3",
    "watch/inbox/gstd_desktop_buildout_20260109.md",
    "configs/longrunner_policy.json",
])
CLASSIFY_KEY = {
    "tools/gps_router_v0.py": "tool",
    "watch/inbox/ml_moonshot_20261007/ml3_route_table.json": "receipt",
    "tools/gps_mcp/gps_ledger.db3": "ledger",
    "watch/inbox/gstd_desktop_buildout_20260109.md": "receipt",
    "configs/longrunner_policy.json": "config",
}

ASKS = [
    {
        "shape": "summarize",
        "model": "gemma2:2b-instruct-q5_K_M",
        "prompt": f"Summarize in exactly one sentence:\n\n{SUMMARY_TEXT}",
        "grade": lambda ans: (
            len([s for s in ans.split(".") if s.strip()]) <= 2
            and any(k in ans.lower() for k in ("tunnel", "gstd", "node"))
        ),
    },
    {
        "shape": "classify",
        "model": "qwen2.5:3b-instruct",
        "prompt": (
            "Classify each path into exactly one label: tool, receipt, "
            "ledger, or config. Answer as 'path -> label' lines, nothing else.\n"
            + CLASSIFY_LINES
        ),
        "grade": lambda ans: sum(
            1 for p, want in CLASSIFY_KEY.items()
            if want in ans and p.split("/")[-1].split(".")[0] in ans
        ) >= 4,
    },
    {
        "shape": "extract",
        "model": "qwen2.5:7b",
        "prompt": (
            "Extract the stated facts into a JSON object with keys "
            "node_name, model_count, tunnel_type. Output ONLY the JSON "
            "object, no prose. Facts: the node is named gstd-desktop, it "
            "hosts 15 models, and its public URL is a trycloudflare quick "
            "tunnel."
        ),
        "grade": lambda ans: _extract_ok(ans),
    },
]


def _extract_ok(ans: str) -> bool:
    text = ans.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    try:
        obj = json.loads(text)
    except Exception:
        return False
    return (
        obj.get("node_name") == "gstd-desktop"
        and obj.get("model_count") == 15
        and "trycloudflare" in str(obj.get("tunnel_type", "")).lower()
    )


results = {}
for ask in ASKS:
    shape, model = ask["shape"], ask["model"]
    print(f"\n== {shape} -> {model}", flush=True)
    resp = gw_post(model, ask["prompt"], shape)
    ans = content(resp)
    gstd = resp.get("_gstd", {})
    ok = bool(ask["grade"](ans))
    print(f"  direct answer ({gstd.get('latency_ms')}ms, tier {gstd.get('tier')}, "
          f"sovereignty {gstd.get('sovereignty')}): {ans[:220]!r}")
    print(f"  mechanical grade: {'PASS' if ok else 'FAIL'}")
    ev = json.dumps({
        "request": {"model": model, "task_shape": shape, "prompt": ask["prompt"]},
        "response_content": ans,
        "_gstd": gstd,
        "grade": "pass" if ok else "fail",
    }, sort_keys=True, ensure_ascii=True)
    vr = ledger.record_verdict(
        model, shape, ok,
        evidence_bytes=ev,
        evidence_source=f"{SRC}: pace run direct gateway call, receipt "
                        "watch/inbox/gstd_basecamp_20260109/ROUTER_VOCAB_LANDED.md",
    )
    print(f"  verdict banked: {vr.evidence_status} rate {round(vr.pass_rate,3)} n {vr.sample_size}")
    time.sleep(8)

    # the routed ask: same shape, same payload, through the Router machinery
    for attempt in range(4):
        try:
            dec = router.ask(shape, ask["prompt"])
            break
        except urllib.error.HTTPError as exc:
            if exc.code != 429:
                raise
            print("  routed ask 429, backoff 25s", flush=True)
            time.sleep(25)
    chosen = dec.chosen
    print(f"  ROUTER chose: {chosen} (exploration={dec.exploration})")
    for reason in dec.reasons:
        print(f"    reason: {reason}")
    print(f"  routed answer: {(dec.answer or '')[:220]!r}")
    tier = registry.get(chosen).tier if chosen else None
    results[shape] = {
        "model": model, "direct_grade": "pass" if ok else "fail",
        "direct_latency_ms": gstd.get("latency_ms"),
        "router_chosen": chosen, "router_tier": tier,
        "router_exploration": dec.exploration,
        "router_reasons": dec.reasons,
        "router_answer_head": (dec.answer or "")[:220],
    }
    time.sleep(8)

print("\n== pace summary ==")
print(json.dumps(results, indent=2))
ledger.close()
