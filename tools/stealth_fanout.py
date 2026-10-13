"""stealth_fanout — Mickey17-style concurrent mining across ALL steal models.

Operator order 2026-09-28: "go wide and concurrent on all our steal models
and do mickey17 style." Per-item named gophers, ThreadPool concurrency,
every answer banked with lane+model provenance. Asks are REAL mining
targets from tonight's record (drops, stuck architecture, open loops).
Laws ride in every ask: no fabrication, OWED if unreachable, no em-dashes.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
try:
    from models.env_load import load_dotenv  # noqa: E402

    load_dotenv()
except Exception:
    pass

OUT_DIR = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "work"
HEARTBEAT = ROOT / "state" / "fuel" / "stealth_fanout.jsonl"

OR1 = os.environ.get("OPENROUTER_API_KEY")
OR2 = os.environ.get("OPENROUTER_API_KEY_2")
N1 = os.environ.get("HERMES_API_KEY_1")
N2 = os.environ.get("HERMES_API_KEY_2")

LANES = []
for key, model in [
    (OR1, "stealth/space-bunny-alpha"),
    (OR2, "inclusionai/ling-3.0-flash-sante:free"),
    (OR2, "meta/muse-spark-1.3"),
    (OR2, "meta/muse-spark-1.2"),
    (OR2, "meta/muse-glimmer-30b"),
    (OR2, "inclusionai/ling-3.0-flash-vl"),
    (OR2, "thinkingmachines/inkling-small:free"),
    (N1, "z-ai/glm-5.3-prime"),
    (N2, "qwen/qwen3.8-max-prime"),
]:
    if key:
        LANES.append({"base": "https://openrouter.ai/api/v1/chat/completions"
                      if "nous" not in model and "prime" not in model
                      else "https://inference-api.nousresearch.com/v1/chat/completions",
                      "key": key, "model": model})
if True:  # llm7 anon lane
    LANES.append({"base": "https://api.llm7.io/v1/chat/completions",
                  "key": "", "model": "gpt-4o-mini"})

ASKS = [
    ("moe-hotswap", "State of the art in MoE expert-weight offloading for llama.cpp on consumer AMD GPUs (Vulkan): how do --n-cpu-moe and -ot (override-tensor) page expert weights from RAM to GPU? What fraction of a MoE model fits in 8GB VRAM with attention hot? Cite llama.cpp discussions/docs by name. OWED if unverifiable."),
    ("contrastive-wm", "Contrastive world models learned via mutual-information objectives (no pixel decoder): key papers 2024-2026, methods, what a solo engineer can reproduce on consumer hardware. Cite titles/arXiv ids. OWED if unverifiable."),
    ("vortex-latent", "Neural networks compressing von Karman vortex-street flows into ~8-value latent loops: which architectures (autoencoders, POD+NN, neural ODEs)? Is the compression reproducible cheaply? Cite sources. OWED if unverifiable."),
    ("water-plasma", "Underwater plasma sterilization: real engineering parameters (kV, pulse microseconds, electrode geometry), what hobby-grade builds exist, and the sterilization mechanism (UV/shock/radicals). Cite sources. OWED if unverifiable."),
    ("auk-voice", "Tencent AuK voice generation model: params, license, VRAM needs, zero-shot voice cloning quality, how to wire it behind a game NPC HTTP gateway. Cite repo/docs. OWED if unverifiable."),
    ("selfplay-sota", "R-Zero, Absolute Zero, SCOPE self-play reasoning: measured benchmark gains, hardware hours per run, and whether any replication used a single consumer GPU. Cite papers. OWED if unverifiable."),
    ("belady-lruk", "Canonical references: Belady 1966 FIFO anomaly study, Mattson 1970 stack-distance evaluation, LRU-K (O'Neil 1993). Exact titles, venues, years, one defining quote each. OWED if unverifiable."),
    ("belt-cube-real", "Has anyone built the six-face-panel belt-driven forever-rotating cube as a REAL machine (not CGI)? Search kinetic sculpture, Zipper-ride carriage mechanics, escalator corner chains, planetary corner gears. Cite builds/patents. OWED if unverifiable."),
    ("eam-tracking", "Open sources that track US military EAM broadcasts (e.g. HF radio scanners, hobbyist networks): what is verifiably public, and what can/cannot be attributed. OWED if unverifiable."),
    ("solomonoff-pretrain", "Self-Play Pretraining with Zero Data (arXiv 2609.30063): replication status, compute used, community results. Cite repos/discussions. OWED if unverifiable."),
    ("or-cache-mechanics", "OpenRouter prompt caching: how cached_tokens accrue (TTL, prefix matching rules), pricing delta vs uncached, per-model differences for stealth/ling/muse models. Cite docs. OWED if unverifiable."),
    ("headless-agent-cli", "Best-practice patterns for wrapping headless CLI coding agents (Claude Code, aider, opencode, Hermes-style) as autonomous research workers: session persistence, banking, safety rails. Cite writeups/repos. OWED if unverifiable."),
]

# SSRF boundary (Mimosa-guarded 2026-09-28): the only POST bases allowed.
WORK_BASES = {
    "https://openrouter.ai/api/v1/chat/completions",
    "https://api.llm7.io/v1/chat/completions",
}


def _assert_public_host(hostname: str) -> None:
    import ipaddress
    import socket

    for info in socket.getaddrinfo(hostname, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise ValueError(f"{hostname} resolved to non-public {ip}")


def _check_base(base: str) -> None:
    if base not in {
        "https://openrouter.ai/api/v1/chat/completions",
        "https://inference-api.nousresearch.com/v1/chat/completions",
        "https://api.llm7.io/v1/chat/completions",
    }:
        raise ValueError(f"base not allowlisted: {base[:60]}")
    host = base.split("/", 3)[2]
    if host != "api.llm7.io":
        _assert_public_host(host)


NTFS_UNSAFE = '<>:"/\\|?*'


def slug(text: str, fallback: str = "unnamed") -> str:
    """Filesystem-safe name fragment (wave5-repair 2026-09-29).

    The write site below used to replace only "/", so model
    'inclusionai/ling-3.0-flash-sante:free' produced '...sante:free.md' and
    NTFS split at the colon: the answer went into an alternate data stream
    on a 0-byte base file (stealth-sw-15 finding 1, verified 2026-09-29 via
    Get-Item -Stream). Every NTFS-unsafe char and control char is replaced
    at the write site. Keep in sync with tools/stealth_driver.py slug.
    """
    cleaned = "".join("_" if (ch in NTFS_UNSAFE or ord(ch) < 32) else ch
                      for ch in text).strip(" .")
    return cleaned or fallback


LAWS = ("Never fabricate: if you could not verify something, say OWED with "
        "what you tried. No em-dashes. Cite sources by name or state none.")


def dispatch(lane: dict, ask: str, max_tokens: int = 3000):
    _check_base(lane["base"])
    body = json.dumps({
        "model": lane["model"],
        "messages": [{"role": "user", "content": ask + "\n\n" + LAWS}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        lane["base"], data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {lane['key']}"} if lane["key"] else
        {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
    msg = (d.get("choices") or [{}])[0].get("message") or {}
    text = (msg.get("content") or msg.get("reasoning_content") or "").strip()
    usage = d.get("usage") or {}
    return text, usage


def run_item(i: int, item_id: str, ask: str) -> dict:
    lane = LANES[i % len(LANES)]
    t0 = time.time()
    try:
        text, usage = dispatch(lane, ask)
        ok = bool(text.strip())
    except Exception as e:
        text, ok = f"DISPATCH-ERR {type(e).__name__}: {str(e)[:140]}", False
        usage = {}
    dt = round(time.time() - t0, 1)
    out = OUT_DIR / f"fan_{slug(item_id)}_{slug(lane['model'])}.md"
    out.write_text(
        f"# FAN {item_id}\n\nlane model: {lane['model']}\nts: "
        f"{datetime.now(timezone.utc).isoformat()}\ndt: {dt}s\n\n---\n\n{text}\n",
        encoding="utf-8")
    row = {"id": item_id, "model": lane["model"], "ok": ok, "dt_s": dt,
           "chars": len(text),
           "cached": (usage.get("prompt_tokens_details") or {}).get("cached_tokens")}
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    workers = min(8, len(LANES) * 2)
    print(f"stealth_fanout: {len(ASKS)} items x {len(LANES)} lanes, "
          f"workers={workers}", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_item, i, item_id, ask): item_id
                for i, (item_id, ask) in enumerate(ASKS)}
        for fut in as_completed(futs):
            results.append(fut.result())
    ok_n = sum(1 for r in results if r["ok"])
    print(f"DONE {ok_n}/{len(results)} banked to {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
