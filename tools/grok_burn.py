"""grok_burn - the funded grok-4.7 carrier (xAI SD account, DRIVING LADDER tier).

Fires the Stone 5 asks (watch/inbox/GROK_LANE_PACKET_20260925.md, asks 1-3
FUNDED per the ladder ruling; ask 4 is a local repo-byte gopher and stays
local). Evidence is rendered into the prompt, outputs land under
watch/inbox/xai_grok47/, usage banks to memory/runs/xai_grok/usage.jsonl in
the hermes_burn row shape. Fail-loud per ask, batch continues.

Endpoint fence (the Mimosa SSRF rulings, same shape as tools/hermes_burn.py):
fixed https URL on exactly one allowlisted host, asserted per call, AND the
host resolved with private/loopback/link-local/reserved/multicast IPs refused.

Usage: python tools/grok_burn.py [--ask 1|2|3]   (default: all three)
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_HOST = "api.x.ai"
API = f"https://{API_HOST}/v1/chat/completions"
OUT_DIR = ROOT / "watch" / "inbox" / "xai_grok47"
USAGE = ROOT / "memory" / "runs" / "xai_grok" / "usage.jsonl"

EVIDENCE1 = [
    "watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md",
    "watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md",
]
EVIDENCE2 = ["watch/GAUNTLET_W4_VERDICT_20260925.md"]

ASKS = {
    "1": {
        "out": "GROK_PREREG_ADVERSARIAL_20261003.md",
        "evidence": EVIDENCE1,
        "prompt": ("Adversarial pass on the replication prereg (both files rendered below). "
                   "Attack them: bars that are too loose or too tight, arms that do not test "
                   "what they claim, cost-unit cheats, post-hoc escape hatches. Context: ARM B "
                   "already reproduced their headline exactly (30/30, judge 21/30); the open "
                   "question is ARM C (gemma:2b as judge, budget 200). Contract: max 10 bullets, "
                   "each = (weakness, why it matters, concrete fix). No em-dashes. Never "
                   "fabricate: cite or mark unverified."),
    },
    "2": {
        "out": "GROK_W4_RERUN_PROTOCOL_20261003.md",
        "evidence": EVIDENCE2,
        "prompt": ("GAUNTLET W4 rerun design review (verdict file rendered below). The rerun "
                   "must satisfy: n >= 50/arm (preregistered), real model ids (the "
                   "DEEPSEEK_API_KEY-as-model bug), warm vs cold arms, cache-floor sub-claim "
                   "intact. Contract: a rerun protocol the fleet can execute on free lanes in "
                   "one night, with the falsifier stated before launch and the abort conditions "
                   "named. No em-dashes. Never fabricate: cite or mark unverified."),
    },
    "3": {
        "out": "GROK_OCTOBER_FOLD_20261003.md",
        "evidence": ["watch/inbox/LINKS.jsonl"],
        "prompt": ("October reading list, deep-read pass. The LINKS.jsonl rows rendered below "
                   "carry FlashREINFORCE, GPO (arxiv 2410.02197 General Preference "
                   "Optimization), RPG (2505.17508 Regularized Policy Gradient), BPO "
                   "(2609.15987 Bellman Policy Optimization), plus the yifanzhang x-drop. For "
                   "EACH paper you can genuinely ground in the rows or your own knowledge: the "
                   "mechanism in 3 sentences, what a small-model fleet could reuse from it, the "
                   "one test that would kill it. Anything you cannot ground: mark UNVERIFIED "
                   "explicitly rather than inventing. Contract: one page per paper, no summary "
                   "padding. No em-dashes."),
    },
    "4": {
        "out": "GROK_RIDDLER_VEIL_CHECK_20261012.md",
        "evidence": ["watch/inbox/riddler_face_20261012/mag_public_face.txt"],
        "prompt": ("You are a stranger who has stumbled onto a public GitHub repo. Below is "
                   "its top-level structure, per-directory file counts, and README. Attack the "
                   "anonymity: what can you reconstruct about (a) who runs this (identity, "
                   "employer, location, other accounts), (b) any named third parties' "
                   "NON-public information, (c) the author's candid private thoughts or "
                   "diary-like material? If the face teaches the system's ideas without "
                   "exposing the life, say so plainly. Contract: max 10 bullets, each = "
                   "(leak found or surface probed, what a stranger can/cannot conclude, "
                   "concrete fix if needed), then ONE verdict line: VEIL-HELD or VEIL-BROKEN. "
                   "Do not invent leaks to seem thorough; mark UNVERIFIED where the rendered "
                   "face cannot answer. No em-dashes."),
    },
    "5": {
        "out": "GROK_SENSORY_FLEX_CHECK_20261012.md",
        "evidence": ["watch/inbox/sensory_inputs_20261012/sensory_reply_evidence.txt"],
        "prompt": ("Below is a draft reply to a public thread asking who is building sensory "
                   "inputs for LLMs, plus the list of files in a public repo it cites. Check "
                   "the flex: (1) does every claim in the reply map to a cited file that "
                   "could plausibly back it, (2) any overclaim (things stated as running that "
                   "read as aspirational), (3) does it read as a shill post or as an "
                   "instrument-backed answer, (4) the one line that lands hardest and the one "
                   "that should be cut. Contract: exactly 5 bullets, then a verdict line: "
                   "SEND or REVISE. No em-dashes."),
    },
}


def _key() -> str:
    for line in open(ROOT / ".env", encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith("XAI_SD_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no XAI_SD_API_KEY in .env")


def _assert_public_endpoint() -> None:
    parsed = urllib.parse.urlsplit(API)
    if parsed.scheme != "https" or parsed.hostname != API_HOST:
        raise RuntimeError("endpoint fence: refusing non-allowlisted URL")
    infos = socket.getaddrinfo(API_HOST, 443, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise RuntimeError(
                f"endpoint fence: {API_HOST} resolves to non-public {ip}")


def _read_evidence(paths: list[str], cap: int = 150_000) -> str:
    parts = []
    for rel in paths:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8", errors="replace") if p.is_file() else "(missing)"
        if len(text) > cap:
            text = text[:cap] + "...[truncated]"
        parts.append(f"\n\n=== EVIDENCE {rel} ===\n{text}")
    return "".join(parts)


def _call(model: str, prompt: str, key: str) -> tuple[str, dict]:
    _assert_public_endpoint()
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.7}).encode()
    last = None
    for attempt in range(2):
        req = urllib.request.Request(API, data=body, method="POST",
                                     headers={"Authorization": "Bearer " + key,
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                resp = json.loads(r.read())
            content = resp["choices"][0]["message"].get("content") or ""
            return content, resp.get("usage", {})
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                json.JSONDecodeError, KeyError) as exc:
            last = exc
            time.sleep(15)
    raise RuntimeError(f"xai transport failed twice: {last!r}")


def _bank(row: dict) -> None:
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grok_burn")
    ap.add_argument("--ask", choices=sorted(ASKS), action="append")
    ap.add_argument("--model", default="grok-4.7")
    args = ap.parse_args(argv)
    key = _key()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    asks = args.ask or sorted(ASKS)
    for n in asks:
        spec = ASKS[n]
        out_path = OUT_DIR / spec["out"]
        if out_path.exists():
            print(f"SKIP ask {n}: {out_path.name} exists")
            continue
        prompt = spec["prompt"] + _read_evidence(spec["evidence"])
        try:
            content, usage = _call(args.model, prompt, key)
        except Exception as exc:  # noqa: BLE001 - fail-loud per ask, continue
            print(f"FAIL ask {n}: {exc!r}")
            continue
        utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        out_path.write_text(f"# {spec['out']} ({args.model}, {utc})\n\n{content}\n",
                            encoding="utf-8")
        _bank({"ts": utc, "id": f"grok47_ask{n}", "model": args.model,
               "prompt_tokens": usage.get("prompt_tokens", 0),
               "completion_tokens": usage.get("completion_tokens", 0),
               "cost_usd": None, "ok": bool(content)})
        print(f"OK ask {n}: {out_path.name} ({len(content)} chars, "
              f"usage={usage.get('prompt_tokens', 0)}/{usage.get('completion_tokens', 0)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
