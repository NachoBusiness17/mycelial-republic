"""premium_autopsy_local - the gemma4 leg of the PREMIUM AUTOPSY replay.

Lane AUTOPSY-1 (watch/inbox/model_garden/premium_autopsy/). HONEST DEVIATION
(the garden_battery_local.py pattern, verbatim reason):
tools/model_garden.py fences base_url to bare https on allowlisted remote
hosts and refuses loopback, so local ollama (http://127.0.0.1:11434/v1)
cannot ride the canonical runner. The fence is NOT weakened. This script
fires the SAME ask dirs (memory/plans/premium_autopsy/gemma4/<QID>/ask.json:
contract bytes identical to the original premium asks per
watch/inbox/model_garden/premium_autopsy/MANIFEST.json, evidence = the same
frozen right-sized copies every remote family received) against ollama's
OpenAI-compat endpoint, with the same prompt construction
model_garden.run_ask uses (system block single-sourced from
tools.hermes_burn._system_for, contract, appended EVIDENCE sections, same
closing line). Rows land in memory/runs/model_garden/usage.jsonl
(channel=lane-local-script, cost 0.0), replies land in
watch/inbox/model_garden/<id>.md.

Deviations, both named in the receipt: max_tokens 2048 local (12000 staged
for remote families; at the measured 15-41 tok/s CPU generation 12000 risks
hours per fire and the runtime ctx 8192 binds harder anyway - ask BYTES
unaffected, max_tokens is a request param); prompts over ctx get the
server-side tail-keep truncation (identical for this family on every ask,
per the local-20261001-a B7 precedent). Browser-style UA. No em-dash bytes
in any file this script writes; model replies are dumped as received (the
reply is the animal's byte truth, the authored-files law covers what the
seat writes). Budget: $0 (local)."""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

QUEUE = ROOT / "memory" / "plans" / "premium_autopsy" / "gemma4"
OUT_DIR = ROOT / "watch" / "inbox" / "model_garden"
USAGE = ROOT / "memory" / "runs" / "model_garden" / "usage.jsonl"

BASE_URL = "http://127.0.0.1:11434/v1"
MODEL = "gemma4:latest"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
MAX_TOKENS = 2048
TIMEOUT_S = 900.0


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _read_evidence(paths: list[str]) -> str:
    # verbatim construction from tools/model_garden.py _read_evidence
    parts = []
    for rel in paths:
        p = ROOT / rel
        if not p.is_file():
            parts.append(f"\n\n=== EVIDENCE {rel} (MISSING) ===\n")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        cap = 400_000
        if len(text) > cap:
            text = text[:cap] + f"\n... [truncated at {cap} chars]"
        parts.append(f"\n\n=== EVIDENCE {rel} ===\n{text}")
    return "".join(parts)


def build_prompt(model: str, meta: dict) -> str:
    # verbatim construction from tools/model_garden.py run_ask
    from tools.hermes_burn import _system_for
    ev = meta.get("evidence", [])
    prompt = (_system_for(model) + "\n\n=== CONTRACT ===\n" + meta["contract"]
              + ("\n\n=== EVIDENCE ===" + _read_evidence(ev) if ev else "")
              + "\n\nProduce the deliverable the CONTRACT demands. Positive AND "
                "negative examples where they clarify. Match the requested shape exactly.")
    return prompt


def preflight(meta: dict, prompt: str) -> None:
    # evidence preflight from model_garden._assert_evidence_in_body; every
    # autopsy ask carries evidence[] (frozen copies), so no self_contained arm
    evidence = meta.get("evidence") or []
    if not evidence:
        raise RuntimeError("EVIDENCE-PREFLIGHT: no evidence paths on " + meta["id"])
    for rel in evidence:
        p = ROOT / rel
        if not p.is_file():
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: missing {rel}")
        probe = p.read_text(encoding="utf-8", errors="replace")[:400].strip()
        if not probe:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: empty {rel}")
        if probe not in prompt:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: {rel} bytes absent from body")


def _bank(row: dict) -> None:
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    ask_dirs = sorted(p for p in QUEUE.iterdir() if (p / "ask.json").is_file())
    print(f"premium_autopsy_local: {len(ask_dirs)} asks, model {MODEL}")
    fails = 0
    for ad in ask_dirs:
        meta = json.loads((ad / "ask.json").read_text(encoding="utf-8"))
        out_path = OUT_DIR / f"{meta['id']}.md"
        if out_path.exists():
            print(f"SKIP {meta['id']} (landed)")
            continue
        prompt = build_prompt(MODEL, meta)
        preflight(meta, prompt)
        body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                "max_tokens": MAX_TOKENS}
        t0 = time.time()
        try:
            with httpx.Client(timeout=TIMEOUT_S) as cli:
                r = cli.post(BASE_URL + "/chat/completions", json=body,
                             headers={"User-Agent": UA})
                r.raise_for_status()
                resp = r.json()
        except Exception as exc:  # transport failure: bank and continue
            _bank({"ts": _now(), "id": meta["id"], "model": MODEL,
                   "model_family": "local-gemma4", "base_url": BASE_URL,
                   "turn": 1, "channel": "lane-local-script",
                   "ok": False, "error": repr(exc)[:200],
                   "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0.0})
            print(f"ERR  {meta['id']} {exc!r}")
            fails += 1
            continue
        usage = resp.get("usage", {})
        pin, pout = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        ch = resp["choices"][0]
        finish = ch.get("finish_reason")
        content = ch.get("message", {}).get("content") or ""
        _bank({"ts": _now(), "id": meta["id"], "model": MODEL,
               "model_family": "local-gemma4", "base_url": BASE_URL, "turn": 1,
               "channel": "lane-local-script", "ok": True,
               "prompt_tokens": pin, "completion_tokens": pout,
               "cost_usd": 0.0, "finish": finish,
               "wall_s": round(time.time() - t0, 1)})
        out_path.write_text(
            f"# {meta['id']} ({MODEL} @ local ollama, channel: lane-local-script)\n\n{content}\n",
            encoding="utf-8")
        print(f"OK   {meta['id']} finish={finish} pin={pin} pout={pout} "
              f"{time.time() - t0:.0f}s")
    print(f"premium_autopsy_local: done, {fails} transport failures")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
