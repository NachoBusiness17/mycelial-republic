"""lensing_ask - the MC6 paid-ask carrier (THE MOUNTAIN CLIMB Phase 2).

Generalized from the AA1-proven streaming-SSE carrier
(watch/inbox/last_mile_20260930/aa1_refire_opus_stream.py), which is the only
transport that has delivered a max-effort Opus return on this gateway:
whole-response reads die when generation outlives the socket window (AA1
attempts 1-2, 1800s/3600s, zero bytes; streaming landed in 362.4s). Per-read
timeout fires only when tokens STOP flowing.

Standing order: DO NOT FIRE. This tool spends real money on a frontier model.
The default mode is a zero-network dry run; the network path opens ONLY when
--fire is passed, and the plan's gate (watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md
Phase 2) requires operator GO before anyone passes it (the AA1 law: paid asks
never fire unilaterally).

Guards (all checked before any spend):
  - brief exists and reads as UTF-8
  - em-dash law: no U+2014 bytes in the fired prompt
  - size ceiling: prompt <= PROMPT_CEILING_BYTES (the 40KB brief envelope)
  - budget: worst-case cost (prompt + max_tokens at metered rates) + prior
    spend <= --budget-cap ($5.00 default, the mission absolute)
  - optional --expect-sha asserts the assembled brief's sha256 (the guard that
    caught AA1's sibling-lane drift with zero spend)

Usage:
    .venv/Scripts/python.exe tools/lensing_ask.py --dry
    .venv/Scripts/python.exe tools/lensing_ask.py --dry --brief path/to/brief.md
    # operator GO only, ever:
    .venv/Scripts/python.exe tools/lensing_ask.py --fire
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERMES_ENV = Path(r"C:\Users\foste\AppData\Local\hermes") / ".env"
BASE = "https://inference-api.nousresearch.com/v1/chat/completions"
KEY_ENVS = ("NOUS_SDD_API_KEY", "HERMES_API_KEY_1", "HERMES_API_KEY_2")

PROMPT_CEILING_BYTES = 40960  # MC6 skeleton envelope: 40KiB hard ceiling
BUDGET_CAP_DEFAULT = 5.00  # mission absolute for the lensing ask
RATE_IN_DEFAULT = 4.0  # Opus 5.5 catalog $/M input (V9 + COST_MODEL receipts)
RATE_OUT_DEFAULT = 20.0  # Opus 5.5 catalog $/M output
PER_READ_TIMEOUT = 300  # fires only when tokens stop flowing for 5 min

DEFAULT_BRIEF = ROOT / "watch" / "inbox" / "mountain_climb" / "OPUS_BRIEF.md"
OUT_DIR = ROOT / "watch" / "inbox" / "mountain_climb"
RAW_FILE = OUT_DIR / "LENSING_ASK_raw.json"
CONTENT_FILE = OUT_DIR / "THE_LENSING.md"
FIRE_LOG = OUT_DIR / "lensing_fire_log.txt"
# SINGLE-SLOT GUN FIX (2026-10-01, the 8-ask incident): --out-prefix P routes the
# full return to P.md + raw to P_raw.json instead of the hardcoded lensing slots.
# Eight sequential asks overwrote each other in THE_LENSING.md - seven verdicts
# spent and lost. A carrier built for one ask is a single-slot gun; never again.
OUT_PREFIX: str | None = None


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def read_brief(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"brief not found: {path} (assemble it per the MC6 skeleton first)")
    return path.read_text(encoding="utf-8")


def dry_checks(prompt: str, max_tokens: int, rate_in: float, rate_out: float,
               prior_spend: float, cap: float) -> dict:
    """Zero-network guard pass. Returns a plan dict; never spends."""
    prompt_bytes = len(prompt.encode("utf-8"))
    sha = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    est_in_tokens = prompt_bytes // 4
    worst_case = est_in_tokens / 1e6 * rate_in + max_tokens / 1e6 * rate_out
    emdash = prompt.count("\u2014")
    checks = {
        "em_dash_zero": emdash == 0,
        "size_under_ceiling": prompt_bytes <= PROMPT_CEILING_BYTES,
        "budget_headroom": worst_case + prior_spend <= cap,
    }
    per_section: dict[str, int] = {}
    for chunk in prompt.split("\n## ")[1:]:
        name = chunk.splitlines()[0][:60]
        per_section[name] = len(chunk.encode("utf-8"))
    return {
        "prompt_bytes": prompt_bytes,
        "prompt_sha256": sha,
        "est_in_tokens": est_in_tokens,
        "max_tokens": max_tokens,
        "worst_case_usd": round(worst_case, 6),
        "prior_spend_usd": prior_spend,
        "budget_cap_usd": cap,
        "em_dash_count": emdash,
        "checks": checks,
        "all_green": all(checks.values()),
        "section_bytes": per_section,
    }


def fire(prompt: str, max_tokens: int, temperature: float, rate_in: float,
         rate_out: float, prior_spend: float, cap: float, model: str,
         expect_sha: str | None) -> int:
    plan = dry_checks(prompt, max_tokens, rate_in, rate_out, prior_spend, cap)
    if not plan["all_green"]:
        print("GUARD FAILED (no spend): " + json.dumps(plan["checks"]))
        return 4
    if expect_sha and plan["prompt_sha256"] != expect_sha:
        print(f"PROMPT DRIFT: sha {plan['prompt_sha256']} != expected {expect_sha}; aborting without spend")
        return 4

    load_dotenv(HERMES_ENV)
    keys = [k for k in (os.environ.get(e) for e in KEY_ENVS) if k]
    if not keys:
        print("NO KEYS - aborting without spend (Nous 402 caveat: see watch/inbox/last_mile_20260930/AJ9_NOUS_402.md)")
        return 2

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
        "stream_options": {"include_usage": True},
        # NO reasoning cap on the Anthropic route (the AA1 fix, kept)
    }).encode()
    req = urllib.request.Request(
        BASE, data=body,
        headers={"Authorization": "Bearer " + keys[0], "Content-Type": "application/json"},
    )

    t0 = time.time()
    status = "ok"
    parts: list[str] = []
    reasoning_parts: list[str] = []
    usage: dict = {}
    finish = None
    chunks_seen = 0
    err_body = ""
    try:
        with urllib.request.urlopen(req, timeout=PER_READ_TIMEOUT) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue
                chunks_seen += 1
                choices = chunk.get("choices") or [{}]
                delta = choices[0].get("delta") or {}
                if delta.get("content"):
                    parts.append(delta["content"])
                if delta.get("reasoning") or delta.get("reasoning_content"):
                    reasoning_parts.append(delta.get("reasoning") or delta.get("reasoning_content"))
                if choices[0].get("finish_reason"):
                    finish = choices[0]["finish_reason"]
                if chunk.get("usage"):
                    usage = chunk["usage"]
    except urllib.error.HTTPError as e:
        status = f"http_{e.code}"
        try:
            err_body = e.read().decode("utf-8", "replace")[:4000]
        except Exception:  # noqa: BLE001
            err_body = "unreadable"
    except Exception as e:  # noqa: BLE001
        status = f"error_{type(e).__name__}"
        err_body = str(e)[:4000]
    secs = round(time.time() - t0, 1)

    metered = usage.get("cost") if isinstance(usage, dict) else None
    predicted = None
    if isinstance(usage, dict) and usage.get("completion_tokens") is not None:
        predicted = (
            usage.get("prompt_tokens", 0) / 1e6 * rate_in
            + usage.get("completion_tokens", 0) / 1e6 * rate_out
        )
    cost_usd = float(metered) if metered is not None else (predicted if predicted is not None else 0.0)

    content = "".join(parts) or None
    reasoning_tail = "".join(reasoning_parts)[-600:] or None
    if status == "ok" and content is None and finish is None and not usage:
        status = "empty_stream"

    row = {
        "id": "MC6-lensing-ask",
        "model": model,
        "status": status,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "transport": f"sse-stream per-read timeout {PER_READ_TIMEOUT}s",
        "plan": plan,
        "usage": usage,
        "cost_usd": round(cost_usd, 6),
        "predicted_cost_usd": round(predicted, 6) if predicted is not None else None,
        "seconds": secs,
        "chunks_seen": chunks_seen,
        "finish_reason": finish,
        "error_body": err_body or None,
        "content_chars": len(content) if content else 0,
        "content": content,
        "reasoning_tail": reasoning_tail,
    }
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    RAW_FILE.write_text(json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8")

    if content:
        head = (
            "# THE_LENSING: frontier judgment on the route (MC6 paid ask)\n\n"
            f"Status: {status}. Metered cost: ${cost_usd:.4f}. Seconds: {secs}. "
            f"Usage: {json.dumps(usage)}. Finish: {finish}.\n"
            f"Prompt sha256: {plan['prompt_sha256']} ({plan['prompt_bytes']}B).\n"
            "Full return below, verbatim. Em-dash count in return body: "
            f"{(content or '').count(chr(8212))}.\n\n---\n\n"
        )
        CONTENT_FILE.write_text(head + content, encoding="utf-8")

    log = (
        f"MC6 status={status} secs={secs} cost=${cost_usd:.4f} usage={json.dumps(usage)} "
        f"prompt_sha={plan['prompt_sha256'][:8]} max_tokens={max_tokens} stream=True "
        f"finish={finish} chunks={chunks_seen} content_chars={len(content) if content else 0}\n"
    )
    with open(FIRE_LOG, "a", encoding="utf-8") as f:
        f.write(log)
    print(log)
    return 0 if (status == "ok" and content) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="MC6 lensing-ask carrier (default: zero-network dry run)")
    ap.add_argument("--brief", type=Path, default=DEFAULT_BRIEF, help="assembled brief markdown (the prompt)")
    ap.add_argument("--out-prefix", type=Path, default=None,
                    help="route full return to <prefix>.md + <prefix>_raw.json (single-slot-gun fix; default = the lensing slots)")
    ap.add_argument("--dry", action="store_true", help="zero-network guard pass (default behavior anyway)")
    ap.add_argument("--fire", action="store_true",
                    help="NETWORK + SPEND. Operator GO only (THE_MOUNTAIN_CLIMB_PLAN Phase 2 gate)")
    ap.add_argument("--model", default="anthropic/claude-opus-5.5")
    ap.add_argument("--max-tokens", type=int, default=64000,
                    help="64k per the plan (AA1 burned 29.5k reasoning on a smaller ask at 32k)")
    ap.add_argument("--temperature", type=float, default=0.4)
    ap.add_argument("--budget-cap", type=float, default=BUDGET_CAP_DEFAULT, help="hard cap USD")
    ap.add_argument("--prior-spend", type=float, default=0.0,
                    help="already-spent USD on this mission line, counted against the cap")
    ap.add_argument("--rate-in", type=float, default=RATE_IN_DEFAULT, help="$ per M input tokens")
    ap.add_argument("--rate-out", type=float, default=RATE_OUT_DEFAULT, help="$ per M output tokens")
    ap.add_argument("--expect-sha", default=None, help="assert brief sha256 before firing (drift guard)")
    args = ap.parse_args(argv)

    global RAW_FILE, CONTENT_FILE, FIRE_LOG
    if args.out_prefix is not None:
        RAW_FILE = args.out_prefix.with_name(args.out_prefix.name + "_raw.json")
        CONTENT_FILE = args.out_prefix.with_name(args.out_prefix.name + ".md")
        FIRE_LOG = args.out_prefix.with_name(args.out_prefix.name + "_fire.log")

    prompt = read_brief(args.brief)
    if args.fire and not args.dry:
        return fire(prompt, args.max_tokens, args.temperature, args.rate_in,
                    args.rate_out, args.prior_spend, args.budget_cap, args.model,
                    args.expect_sha)

    plan = dry_checks(prompt, args.max_tokens, args.rate_in, args.rate_out,
                      args.prior_spend, args.budget_cap)
    if args.expect_sha and plan["prompt_sha256"] != args.expect_sha:
        plan["checks"]["sha_matches"] = False
        plan["all_green"] = False
    elif args.expect_sha:
        plan["checks"]["sha_matches"] = True
    plan["mode"] = "dry (zero network, zero spend)"
    plan["brief"] = str(args.brief)
    plan["generated_utc"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    print("DRY ONLY - no spend. Firing requires --fire and operator GO (the AA1 law).")
    return 0 if plan["all_green"] else 4


if __name__ == "__main__":
    sys.exit(main())
