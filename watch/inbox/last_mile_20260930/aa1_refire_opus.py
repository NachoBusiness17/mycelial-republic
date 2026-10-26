"""AA1 refire: the IDENTICAL W4 ask to anthropic/claude-opus-5.5, max_tokens 32000 (2026-09-30).

Mission (operator): W4 fired empty (finish_reason=length; all 16000 completion
tokens consumed as reasoning on the Anthropic-via-Nous route, which ignored the
reasoning {"max_tokens": 6000} cap). THE FIX: max_tokens 32000 and NO reasoning
cap on the Anthropic route. Prompt bytes must be IDENTICAL to W4 (sha256
b805548a93fddb575af09c77c84a013398f6aa2ed0a558af79079183e002f4f7, 31070 bytes);
the script asserts this before spending.

Budget: $2.00 absolute mission cap; W4 already spent $0.3709, so this lane's
worst case must fit the remaining headroom. Metered W4 input was 12729 tokens;
worst case here = 12729/1e6*$4 + 32000/1e6*$20 = $0.691. Fits with margin.

Driver pattern: byte-copy of w4_fire_opus.py with three changes only:
(1) MAX_TOKENS 16000 -> 32000; (2) the "reasoning" param dropped entirely
(no reasoning cap on Anthropic route); (3) output file names AA1_*. One call,
no retry, no model rotation. If the return is empty again: bank honestly and
report; the 64k escalation is an operator decision, not fired here.

Laws: no em-dashes in anything this file writes (asserted on the prompt);
artifacts land next to the W4 receipt in watch/inbox/last_mile_20260930/.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/aa1_refire_opus.py
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
HERMES_DIR = Path(r"C:\Users\foste\AppData\Local\hermes")
BASE = "https://inference-api.nousresearch.com/v1/chat/completions"
KEY_ENVS = ("NOUS_SDD_API_KEY", "HERMES_API_KEY_1", "HERMES_API_KEY_2")
MODEL = "anthropic/claude-opus-5.5"
MAX_TOKENS = 32000  # THE FIX: room for thinking + body both
TEMPERATURE = 0.4
BUDGET_USD = 2.0
W4_SPENT = 0.370916
EXPECTED_SHA = "b805548a93fddb575af09c77c84a013398f6aa2ed0a558af79079183e002f4f7"
EXPECTED_BYTES = 31070
RATE_IN, RATE_OUT = 4.0, 20.0  # per 1M, catalog rates (W4 receipt confirmed no markup)

OUT_DIR = ROOT / "watch" / "inbox" / "last_mile_20260930"
# Attempt 1 timed out client-side at 1800s socket read ($0 metered, transport
# stall, not an empty model return; banked in AA1_OPUS_REFIRE_raw.json). Fix
# receipt: doubled socket timeout to 3600s for attempt 2; output files get an
# "a2" suffix so the attempt-1 raw row is preserved byte-for-byte.
ATTEMPT = os.environ.get("AA1_ATTEMPT", "2")
TIMEOUT_S = int(os.environ.get("AA1_TIMEOUT", "3600"))
RAW_FILE = OUT_DIR / f"AA1_OPUS_REFIRE_raw{'2' if ATTEMPT == '2' else ''}.json"
CONTENT_FILE = OUT_DIR / "AA1_OPUS_RETURN_20260930.md"
FIRE_LOG = OUT_DIR / "W4_fire_log.txt"


def load_dotenv(path: Path) -> None:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def build_prompt() -> str:
    """Rebuild the exact W4 prompt from its own template + baseline file."""
    import ast

    src = (OUT_DIR / "w4_fire_opus.py").read_text(encoding="utf-8")
    tmpl = None
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if getattr(t, "id", None) == "PROMPT_TEMPLATE":
                    tmpl = node.value.value
    assert tmpl is not None, "PROMPT_TEMPLATE not found in w4_fire_opus.py"
    baseline = (ROOT / "watch" / "inbox" / "gps_baseline_ractor_20260929" / "BASELINE_SPEC.md").read_text(
        encoding="utf-8"
    )
    return tmpl.replace("__BASELINE__", baseline)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt()
    assert "\u2014" not in prompt, "em-dash law violated in fired prompt"
    prompt_bytes = len(prompt.encode("utf-8"))
    sha = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if sha != EXPECTED_SHA or prompt_bytes != EXPECTED_BYTES:
        FIRE_LOG.write_text(
            f"AA1 GUARD: prompt drifted (sha {sha}, {prompt_bytes} bytes) vs W4 "
            f"({EXPECTED_SHA}, {EXPECTED_BYTES}); aborted without spend\n",
            encoding="utf-8",
        )
        print(f"PROMPT DRIFT: sha {sha} {prompt_bytes}B; aborting without spend")
        return 4

    load_dotenv(HERMES_DIR / ".env")
    keys = [k for k in (os.environ.get(e) for e in KEY_ENVS) if k]
    if not keys:
        FIRE_LOG.write_text("AA1: NO KEYS - aborted without spend\n", encoding="utf-8")
        print("NO KEYS - aborting without spend")
        return 2

    est_in_tokens = prompt_bytes // 4
    worst_case = est_in_tokens / 1e6 * RATE_IN + MAX_TOKENS / 1e6 * RATE_OUT
    if worst_case + W4_SPENT > BUDGET_USD:
        FIRE_LOG.write_text(
            f"AA1 BUDGET GUARD: worst case ${worst_case:.4f} + W4 ${W4_SPENT:.4f} exceeds cap ${BUDGET_USD}\n",
            encoding="utf-8",
        )
        print(f"BUDGET GUARD hit, worst case ${worst_case:.4f}; aborting without spend")
        return 3

    body = json.dumps(
        {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            # THE FIX: no "reasoning" cap at all on the Anthropic route
        }
    ).encode()
    req = urllib.request.Request(
        BASE, data=body, headers={"Authorization": "Bearer " + keys[0], "Content-Type": "application/json"}
    )

    t0 = time.time()
    status = "ok"
    resp = {}
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        status = f"http_{e.code}"
        try:
            resp = {"error_body": e.read().decode("utf-8", "replace")[:4000]}
        except Exception:  # noqa: BLE001
            resp = {"error_body": "unreadable"}
    except Exception as e:  # noqa: BLE001
        status = f"error_{type(e).__name__}"
        resp = {"error_body": str(e)[:4000]}
    secs = round(time.time() - t0, 1)

    usage = resp.get("usage", {}) if isinstance(resp, dict) else {}
    metered = usage.get("cost") if isinstance(usage, dict) else None
    predicted = None
    if isinstance(usage, dict) and usage.get("completion_tokens") is not None:
        predicted = (
            usage.get("prompt_tokens", 0) / 1e6 * RATE_IN
            + usage.get("completion_tokens", 0) / 1e6 * RATE_OUT
        )
    cost_usd = float(metered) if metered is not None else (predicted if predicted is not None else 0.0)

    content = None
    reasoning_tail = None
    finish = None
    if status == "ok":
        msg = resp["choices"][0]["message"]
        content = msg.get("content")
        reasoning_tail = (msg.get("reasoning") or "")[-600:]
        finish = resp["choices"][0].get("finish_reason")

    row = {
        "id": f"AA1-opus-refire-attempt{ATTEMPT}",
        "model": MODEL,
        "status": status,
        "max_tokens": MAX_TOKENS,
        "attempt": ATTEMPT,
        "params_note": "identical prompt bytes to W4 (sha asserted); reasoning cap dropped; max_tokens 32000",
        "usage": usage,
        "cost_usd": round(cost_usd, 6),
        "predicted_cost_usd": round(predicted, 6) if predicted is not None else None,
        "prompt_bytes": prompt_bytes,
        "prompt_sha256": sha,
        "seconds": secs,
        "finish_reason": finish,
        "content": content,
        "reasoning_tail": reasoning_tail,
    }
    RAW_FILE.write_text(json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8")

    if content:
        head = (
            "# W4/AA1 OPUS RETURN: anthropic/claude-opus-5.5 (Nous), 2026-09-30 refire\n\n"
            f"Status: {status}. Metered cost: ${cost_usd:.4f}. Seconds: {secs}. "
            f"Usage: {json.dumps(usage)}. Finish: {finish}.\n"
            "Full return below, verbatim. Em-dash count in return body: "
            f"{(content or '').count(chr(8212))}.\n\n---\n\n"
        )
        CONTENT_FILE.write_text(head + content, encoding="utf-8")

    log = (
        f"AA1 status={status} secs={secs} cost=${cost_usd:.4f} usage={json.dumps(usage)} "
        f"prompt_sha={sha[:8]} max_tokens={MAX_TOKENS} finish={finish} "
        f"content_chars={len(content) if content else 0}\n"
    )
    with open(FIRE_LOG, "a", encoding="utf-8") as f:
        f.write(log)
    print(log)
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
