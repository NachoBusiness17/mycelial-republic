"""sw-13 lane dispatch: free-lane SENSING for the Goedel-incompleteness/AI-safety ask.

Pattern stolen verbatim from tools/stealth_fanout.py (dispatch(), _check_base
SSRF allowlist, laws riding in the ask, provenance banked). Free stealth lanes
are a SENSING surface per RIB_DRIVING_LADDER_20260928: outputs banked as
findings, never as trusted work. Verification climbs to the funded tier.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
try:
    from models.env_load import load_dotenv  # noqa: E402

    load_dotenv()
except Exception:
    pass

OUT_DIR = Path(__file__).resolve().parent
HEARTBEAT = ROOT / "state" / "fuel" / "stealth_fanout.jsonl"

OR2 = os.environ.get("OPENROUTER_API_KEY_2")

LANES = []
for key, model in [
    (OR2, "inclusionai/ling-3.0-flash-sante:free"),
    (OR2, "meta/muse-spark-1.3"),
]:
    if key:
        LANES.append({"base": "https://openrouter.ai/api/v1/chat/completions",
                      "key": key, "model": model})
if True:  # llm7 anon lane, no key; model from live /v1/models catalog 2026-09-28
    LANES.append({"base": "https://api.llm7.io/v1/chat/completions",
                  "key": "", "model": "minimax-m2.7"})

ASK = (
    "Research question: What do Goedel's incompleteness theorems actually imply "
    "about AI systems that govern themselves (self-modifying agents, AI self-oversight)? "
    "Cover: (1) what the first and second theorems state and their required conditions "
    "(consistency, recursively axiomatizable, arithmetic capability); "
    "(2) Schmidhuber's Goedel machine and what it assumes/limits; "
    "(3) the Loebian obstacle / tiling agents problem for self-trust in self-modifying AI; "
    "(4) Rice's theorem and the halting problem as the stronger undecidability results "
    "for verifying an agent against a safety spec; "
    "(5) the Lucas-Penrose anti-mechanist argument and why logicians reject it; "
    "(6) what responsible AI-safety engineering should conclude (oversight layering, "
    "sandboxing, runtime monitoring vs pre-hoc formal proof). "
    "Name papers/authors where you can; OWED if you cannot verify something. "
    "No em-dashes."
)

LAWS = ("Never fabricate: if you could not verify something, say OWED with "
        "what you tried. No em-dashes. Cite sources by name or state none.")


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


def run_item(lane: dict) -> dict:
    t0 = time.time()
    try:
        text, usage = dispatch(lane, ASK)
        ok = bool(text.strip())
    except Exception as e:
        text, ok = f"DISPATCH-ERR {type(e).__name__}: {str(e)[:140]}", False
        usage = {}
    dt = round(time.time() - t0, 1)
    fname = lane["model"].replace("/", "_").replace(":", "-")
    out = OUT_DIR / f"_sw13_lane_{fname}.md"
    out.write_text(
        f"# SW13 LANE SENSING (unverified)\n\nlane model: {lane['model']}\nts: "
        f"{datetime.now(timezone.utc).isoformat()}\ndt: {dt}s\n"
        f"status: {'ok' if ok else 'FAILED'}\n\n---\n\n{text}\n",
        encoding="utf-8")
    row = {"id": "sw-13", "model": lane["model"], "ok": ok, "dt_s": dt,
           "chars": len(text),
           "cached": (usage.get("prompt_tokens_details") or {}).get("cached_tokens")}
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main() -> int:
    print(f"sw13 lanes: {len(LANES)}", flush=True)
    for lane in LANES:
        row = run_item(lane)
        print(json.dumps(row), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
