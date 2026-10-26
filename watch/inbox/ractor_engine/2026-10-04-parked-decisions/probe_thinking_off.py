# probe_thinking_off.py - hermes_burn-merge lane probe leg, 2026-10-04
# Verdict item 2 (watch/inbox/ractor_engine/2026-10-04-parked-decisions/
# SYNTHESIS.md:243-250, honest residue 2): GLM prime's thinking wire shape on
# the nous gateway is UNVERIFIED; probe the funded lanes with
# thinking:{type:disabled} in the body to catch (a) 400 rejections and
# (b) ignore-lanes (openrouter/auto is the known one, providers.yaml:219-223).
# Bank per lane: HTTP status + whether reasoning_content came back.
# Budget: one ~32-token call per lane, total far under the $0.05 lane cap.
import json
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BANK = ROOT / "memory" / "runs" / "hermes_burn" / "thinking_off_probe_20261004.jsonl"

NOUS = "inference-api.nousresearch.com"
KEY_NAMES = ("HERMES_API_KEY_2", "HERMES_API_KEY_1", "DEEPSEEK_API_KEY",
             "XAI_SD_API_KEY", "OPENROUTER_API_KEY")


def load_key(name):
    for line in open(ROOT / ".env", encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith(name + "="):
            val = line.split("=", 1)[1].strip().strip('"').strip("'")
            if val:
                return val
    return None


def assert_public(host):
    for info in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP):
        import ipaddress
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise RuntimeError(f"endpoint fence: {host} resolves to {ip}")


LANES = [
    # (lane, model, host, key_env, max_tokens_key, headers)
    ("nous-glm-prime", "z-ai/glm-5.3-prime", NOUS, "HERMES_API_KEY_2",
     "max_tokens", {}),
    ("nous-qwen-prime", "qwen/qwen3.8-max-prime", NOUS, "HERMES_API_KEY_2",
     "max_tokens", {}),
    ("nous-claude-haiku", "anthropic/claude-haiku-4.5", NOUS,
     "HERMES_API_KEY_2", "max_tokens", {}),
    ("deepseek", "deepseek-v4-flash", "api.deepseek.com", "DEEPSEEK_API_KEY",
     "max_tokens", {}),
    ("xai-grok-4.7", "grok-4.7", "api.x.ai", "XAI_SD_API_KEY",
     "max_completion_tokens", {}),
    ("openrouter-auto", "openrouter/auto", "openrouter.ai",
     "OPENROUTER_API_KEY", "max_tokens",
     {"HTTP-Referer": "http://127.0.0.1:8765",
      "X-Title": "Mag Resource Harness"}),
]


def probe(lane, model, host, key_env, tok_key, headers):
    key = load_key(key_env)
    if not key:
        return {"lane": lane, "model": model, "host": host, "key_env": key_env,
                "status": "NO_KEY", "ok": False,
                "note": f"{key_env} absent from .env; lane unprobed"}
    assert_public(host)
    body = {"model": model,
            "messages": [{"role": "user",
                          "content": "Reply with exactly one word: pong"}],
            tok_key: 32,
            "thinking": {"type": "disabled"}}
    req = urllib.request.Request(
        f"https://{host}/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json", **headers})
    t0 = time.time()
    row = {"ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
           "lane": lane, "model": model, "host": host, "key_env": key_env,
           "tok_key": tok_key, "ask": "thinking:{type:disabled} in body"}
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            resp = json.loads(r.read())
        row["status"] = r.status
        row["ok"] = True
        msg = resp["choices"][0]["message"]
        usage = resp.get("usage", {})
        rc = msg.get("reasoning_content")
        row["finish_reason"] = resp["choices"][0].get("finish_reason")
        row["content_chars"] = len(msg.get("content") or "")
        row["reasoning_content_present"] = rc is not None
        row["reasoning_content_chars"] = len(rc or "")
        row["reasoning_tokens"] = ((usage.get("completion_tokens_details") or {})
                                   .get("reasoning_tokens"))
        row["completion_tokens"] = usage.get("completion_tokens")
        row["note"] = ("IGNORE-CANDIDATE: 200 with reasoning bytes despite the"
                       " disabled key" if (row["reasoning_tokens"] or 0) > 0
                       else "clean: 200, no reasoning bytes")
    except urllib.error.HTTPError as exc:
        snippet = ""
        try:
            snippet = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:  # noqa: BLE001 - bank what we can
            pass
        row.update({"status": exc.code, "ok": False,
                    "error_snippet": snippet,
                    "note": ("400 ON THE KEY: lane keeps its old shape,"
                             " capability-attestation note instead (never"
                             " forced)" if exc.code == 400
                            else f"HTTP {exc.code}")})
    except Exception as exc:  # noqa: BLE001 - transport/timeout rows bank too
        row.update({"status": "TRANSPORT", "ok": False,
                    "error_snippet": repr(exc)[:300],
                    "note": "transport/timeout: lane unprobed on this shape"})
    row["elapsed_s"] = round(time.time() - t0, 1)
    return row


def main():
    rows = []
    for lane in LANES:
        row = probe(*lane)
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False))
        BANK.parent.mkdir(parents=True, exist_ok=True)
        with open(BANK, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        time.sleep(2)
    bad = [r for r in rows if not r.get("ok")]
    print(f"PROBE DONE: {len(rows) - len(bad)}/{len(rows)} lanes accepted the"
          f" disabled key; bank {BANK.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
