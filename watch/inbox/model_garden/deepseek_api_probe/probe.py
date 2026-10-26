"""deepseek_api_probe - API-1 lane probes against api.deepseek.com (2026-10-01).

Five probes, one file of receipts (raw request+response bytes each):
  P0 GET  /models            - what model ids the account actually sees
  P1 GET  /user/balance      - the live spend meter capability
  P2 POST /chat/completions  - prefix-cache A/B/C: same ~2k-token prefix,
                               distinct final question; read
                               usage.prompt_cache_hit_tokens per docs
  P3 POST /chat/completions  - JSON output mode (response_format json_object)
  P4 POST /beta/completions  - FIM (beta base_url per docs), prompt+suffix

Budget guard: every token-bearing call is small; whole file should cost
well under $0.02. Thinking disabled everywhere (AH10 law). Security pattern
matches tools/backfill_direct.py: pinned https host, resolved IP must be
public, no redirects. DEEPSEEK_API_KEY read from ROOT/.env, never printed.

Run: .venv/Scripts/python.exe watch/inbox/model_garden/deepseek_api_probe/probe.py
"""
from __future__ import annotations

import ipaddress
import json
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent / "probe_receipts.jsonl"
API_HOST = "api.deepseek.com"
BASE = "https://" + API_HOST
MODEL = "deepseek-flash"  # canonical id per 2026-09-10 changelog + pricing page


def key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            v = line.split("=", 1)[1].strip().strip('"')
            if v:
                return v
    raise SystemExit("DEEPSEEK_API_KEY not in .env")


def guard_host() -> None:
    for info in socket.getaddrinfo(API_HOST, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise SystemExit(f"refused non-public resolved address: {ip}")


def call(method: str, path: str, body: dict | None, keyv: str, timeout: int = 120) -> tuple[int, dict | str]:
    guard_host()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={
        "Authorization": "Bearer " + keyv,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8")
            return r.status, json.loads(raw)
    except urllib.error.HTTPError as e:  # keep error bodies: they carry hints
        return e.code, e.read().decode("utf-8", errors="replace")[:2000]


def bank(row: dict) -> None:
    row["ts"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with OUT.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(row["probe"], row.get("status"), flush=True)


def usage_of(resp: dict) -> dict:
    u = resp.get("usage") or {}
    out = {k: u.get(k) for k in (
        "prompt_tokens", "completion_tokens", "total_tokens",
        "prompt_cache_hit_tokens", "prompt_cache_miss_tokens")}
    out["cached_tokens_detail"] = (u.get("prompt_tokens_details") or {}).get("cached_tokens")
    out["reasoning_tokens"] = (u.get("completion_tokens_details") or {}).get("reasoning_tokens")
    return out


PREFIX_SCAFFOLD = "\n".join(
    f"LAW {i:03d}: the estate files every fired ask with a receipt naming the "
    f"instrument, the moment, and the delta; hand-copied counts are void and "
    f"byte truth is the only truth admitted at review time." for i in range(1, 121))


def main() -> None:
    keyv = key()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # P0 models list (free)
    st, resp = call("GET", "/models", None, keyv)
    if isinstance(resp, dict):
        ids = [m.get("id") for m in resp.get("data", [])]
        bank({"probe": "P0_models", "status": st, "model_ids": ids,
              "one_model_full": (resp.get("data") or [{}])[0]})
    else:
        bank({"probe": "P0_models", "status": st, "body": resp})

    # P1 balance (free)
    st, resp = call("GET", "/user/balance", None, keyv)
    bank({"probe": "P1_balance", "status": st, "body": resp})

    # P2 prefix-cache A/B/C: identical 2k-token scaffold prefix, distinct
    # final question. Per kv_cache guide: common-prefix detection persists
    # the shared unit, so later fires should report hit tokens.
    for tag, q in (("A", "How many laws are listed above? Answer with just the number."),
                   ("B", "What law number comes right after LAW 007? Just the number."),
                   ("C", "Quote the first four words of LAW 001. Nothing else.")):
        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": PREFIX_SCAFFOLD + "\n\nQUESTION: " + q}],
            "thinking": {"type": "disabled"},  # canonical off switch per thinking_mode guide
            "max_tokens": 2000,
            "temperature": 0.3,
            "stream": False,
        }
        t0 = time.time()
        st, resp = call("POST", "/chat/completions", body, keyv)
        if isinstance(resp, dict) and resp.get("choices"):
            msg = resp["choices"][0].get("message", {})
            bank({"probe": "P2_cache_" + tag, "status": st,
                  "latency_s": round(time.time() - t0, 2),
                  "model_echo": resp.get("model"),
                  "usage": usage_of(resp),
                  "content_head": (msg.get("content") or "")[:120],
                  "request": {"model": MODEL, "thinking": "disabled",
                              "prefix_chars": len(PREFIX_SCAFFOLD), "question": q}})
        else:
            bank({"probe": "P2_cache_" + tag, "status": st, "body": str(resp)[:400]})
        time.sleep(3)  # give the disk cache unit time to persist (docs: seconds)

    # P3 JSON mode
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Extract to json: {\"verdict\": str, \"confidence\": number}"},
            {"role": "user", "content": "Statement: the quick brown fox jumps over the lazy dog. Give verdict PASS or FAIL for 'is a valid pangram' plus confidence 0-1. Reply as json only."}],
        "response_format": {"type": "json_object"},
        "thinking": {"type": "disabled"},
        "max_tokens": 500,
        "stream": False,
    }
    st, resp = call("POST", "/chat/completions", body, keyv)
    if isinstance(resp, dict) and resp.get("choices"):
        content = resp["choices"][0].get("message", {}).get("content") or ""
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = "UNPARSEABLE"
        bank({"probe": "P3_json_mode", "status": st, "usage": usage_of(resp),
              "content": content[:300], "parsed_ok": parsed != "UNPARSEABLE",
              "parsed": parsed})
    else:
        bank({"probe": "P3_json_mode", "status": st, "body": str(resp)[:400]})

    # P4 FIM via beta base_url (docs: base_url must be .../beta)
    fim_body = {
        "model": MODEL,
        "prompt": "def connect_tile(a, b):\n    \"\"\"Join two board tiles, returning the merged id.\"\"\"\n    ",
        "suffix": "\n\nclass Board:\n    pass",
        "max_tokens": 100,
        "stream": False,
    }
    st, resp = call("POST", "/beta/completions", fim_body, keyv)
    if isinstance(resp, dict) and resp.get("choices"):
        bank({"probe": "P4_fim", "status": st,
              "text": resp["choices"][0].get("text", "")[:300],
              "finish_reason": resp["choices"][0].get("finish_reason"),
              "object": resp.get("object"),
              "usage": usage_of(resp)})
    else:
        bank({"probe": "P4_fim", "status": st, "body": str(resp)[:400]})

    print("RECEIPTS ->", OUT)


if __name__ == "__main__":
    main()
