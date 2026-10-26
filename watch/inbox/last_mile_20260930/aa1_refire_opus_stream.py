"""AA1 refire attempt 3: same ask, STREAMING SSE transport (2026-09-30).

Fix receipt: attempts 1 and 2 (whole-response reads, socket timeouts 1800s and
3600s) both died with ZERO bytes delivered while W4's 16k non-streaming call on
the same route returned in 194.6s. Same disease the V1 duel diagnosed on
grok-4.7 (v1_multifamily_duel.py call_long): the gateway holds the whole
connection for the entire generation and a max-effort Opus with a 32k budget
outlives any whole-response window. Streaming keeps the socket alive per-read
(timeout fires only when tokens STOP flowing). Params byte-same as AA1: prompt
sha256 b805548a93fddb575af09c77c84a013398f6aa2ed0a558af79079183e002f4f7
asserted, model anthropic/claude-opus-5.5, temperature 0.4, max_tokens 32000,
NO reasoning cap. Usage from the final chunk (stream_options include_usage).

One call. If this fails: stop, bank, report; 64k is an operator decision.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/aa1_refire_opus_stream.py
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
MAX_TOKENS = 32000
TEMPERATURE = 0.4
BUDGET_USD = 2.0
W4_SPENT = 0.370916
EXPECTED_SHA = "b805548a93fddb575af09c77c84a013398f6aa2ed0a558af79079183e002f4f7"
EXPECTED_BYTES = 31070
RATE_IN, RATE_OUT = 4.0, 20.0
PER_READ_TIMEOUT = 300  # fires only when tokens stop flowing for 5 min

OUT_DIR = ROOT / "watch" / "inbox" / "last_mile_20260930"
RAW_FILE = OUT_DIR / "AA1_OPUS_REFIRE_raw3.json"
CONTENT_FILE = OUT_DIR / "W4_OPUS_RETURN_20260930.md"
FIRE_LOG = OUT_DIR / "W4_fire_log.txt"


def load_dotenv(path: Path) -> None:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def build_prompt() -> str:
    """Rebuild the exact W4 prompt from its own template + the W4-era baseline.

    Fix receipt: at 08:06 on 2026-09-30 a sibling lane landed AMENDMENT 5 into
    the working-tree BASELINE_SPEC.md (34678 bytes), which drifted the prompt
    to sha 2f43d2d9 (40578 bytes) and tripped this script's guard with zero
    spend. The byte-stable W4 target is the c72a49d65 blob (25170 bytes,
    verified: rebuilds sha b805548a exactly), so the baseline is loaded from
    git, not the moving working tree.
    """
    import ast
    import subprocess

    src = (OUT_DIR / "w4_fire_opus.py").read_text(encoding="utf-8")
    tmpl = None
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if getattr(t, "id", None) == "PROMPT_TEMPLATE":
                    tmpl = node.value.value
    assert tmpl is not None, "PROMPT_TEMPLATE not found in w4_fire_opus.py"
    blob = subprocess.run(
        ["git", "show", "c72a49d65:watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md"],
        capture_output=True,
        check=True,
        cwd=ROOT,
    ).stdout.decode("utf-8")
    return tmpl.replace("__BASELINE__", blob)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt()
    assert "\u2014" not in prompt, "em-dash law violated in fired prompt"
    prompt_bytes = len(prompt.encode("utf-8"))
    sha = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if sha != EXPECTED_SHA or prompt_bytes != EXPECTED_BYTES:
        print(f"PROMPT DRIFT: sha {sha} {prompt_bytes}B; aborting without spend")
        return 4

    load_dotenv(HERMES_DIR / ".env")
    keys = [k for k in (os.environ.get(e) for e in KEY_ENVS) if k]
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2

    est_in_tokens = prompt_bytes // 4
    worst_case = est_in_tokens / 1e6 * RATE_IN + MAX_TOKENS / 1e6 * RATE_OUT
    if worst_case + W4_SPENT > BUDGET_USD:
        print(f"BUDGET GUARD hit, worst case ${worst_case:.4f}; aborting without spend")
        return 3

    body = json.dumps(
        {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "stream": True,
            "stream_options": {"include_usage": True},
            # NO reasoning cap on the Anthropic route (the AA1 fix, kept)
        }
    ).encode()
    req = urllib.request.Request(
        BASE, data=body, headers={"Authorization": "Bearer " + keys[0], "Content-Type": "application/json"}
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
            usage.get("prompt_tokens", 0) / 1e6 * RATE_IN
            + usage.get("completion_tokens", 0) / 1e6 * RATE_OUT
        )
    cost_usd = float(metered) if metered is not None else (predicted if predicted is not None else 0.0)

    content = "".join(parts) or None
    reasoning_tail = "".join(reasoning_parts)[-600:] or None
    if status == "ok" and content is None and finish is None and not usage:
        status = "empty_stream"

    row = {
        "id": "AA1-opus-refire-attempt3-stream",
        "model": MODEL,
        "status": status,
        "max_tokens": MAX_TOKENS,
        "transport": "sse-stream per-read timeout 300s",
        "params_note": "identical prompt bytes to W4 (sha asserted); reasoning cap dropped; max_tokens 32000; streaming",
        "usage": usage,
        "cost_usd": round(cost_usd, 6),
        "predicted_cost_usd": round(predicted, 6) if predicted is not None else None,
        "prompt_bytes": prompt_bytes,
        "prompt_sha256": sha,
        "seconds": secs,
        "chunks_seen": chunks_seen,
        "finish_reason": finish,
        "error_body": err_body or None,
        "content_chars": len(content) if content else 0,
        "content": content,
        "reasoning_tail": reasoning_tail,
    }
    RAW_FILE.write_text(json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8")

    if content:
        head = (
            "# W4/AA1 OPUS RETURN: anthropic/claude-opus-5.5 (Nous), 2026-09-30 refire (stream)\n\n"
            f"Status: {status}. Metered cost: ${cost_usd:.4f}. Seconds: {secs}. "
            f"Usage: {json.dumps(usage)}. Finish: {finish}.\n"
            "Full return below, verbatim. Em-dash count in return body: "
            f"{(content or '').count(chr(8212))}.\n\n---\n\n"
        )
        CONTENT_FILE.write_text(head + content, encoding="utf-8")

    log = (
        f"AA1a3 status={status} secs={secs} cost=${cost_usd:.4f} usage={json.dumps(usage)} "
        f"prompt_sha={sha[:8]} max_tokens={MAX_TOKENS} stream=True finish={finish} "
        f"chunks={chunks_seen} content_chars={len(content) if content else 0}\n"
    )
    with open(FIRE_LOG, "a", encoding="utf-8") as f:
        f.write(log)
    print(log)
    return 0 if (status == "ok" and content) else 1


if __name__ == "__main__":
    raise SystemExit(main())
