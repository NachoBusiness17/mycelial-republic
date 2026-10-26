"""Q-034 first video-input burn: one small corpus mp4 through stealth/space-bunny-alpha.

Ask: find one small corpus mp4, send it through space-bunny-alpha on OpenRouter
with a video-capable request. Bank the result or the OWED.

Lane spec per tools/stealth_driver.py:179-182 (openrouter, OPENROUTER_API_KEY,
model stealth/space-bunny-alpha). Request shape per OpenRouter docs
(guides/overview/multimodal/videos): content part
{"type": "video_url", "video_url": {"url": "data:video/mp4;base64,..."}}.
max_tokens >= 512 per watch/inbox/SPACE_BUNNY_BURN_20260924.md:33 (mandatory
reasoning eats small budgets). No subprocesses are spawned here; pure urllib.
"""
import base64
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VIDEO = ROOT / "corpus/library/openai-cookbook/examples/data/bison.mp4"
ENV = ROOT / ".env"
RAW_OUT = Path(__file__).with_name("Q_034_openrouter_raw.json")
MODEL = "stealth/space-bunny-alpha"
BASE = "https://openrouter.ai/api/v1"

PROMPT = (
    "You have been given a short video as a video_url content part. "
    "Watch it and answer in under 150 words: "
    "1) What animals appear and what are they doing? "
    "2) Describe the setting. "
    "3) What happens in the final seconds of the clip? "
    "If you cannot actually view video input, reply with exactly: CANNOT_VIEW_VIDEO"
)


def env_key(name: str) -> str:
    for line in ENV.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"')
    return ""


def http(method: str, path: str, key: str, payload: dict | None, timeout: int):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        method=method,
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = json.loads(r.read().decode())
            return r.status, body, round(time.time() - t0, 1)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}"), round(time.time() - t0, 1)


def main() -> int:
    key = env_key("OPENROUTER_API_KEY") or env_key("OPENROUTER_API_KEY_2")
    if not key:
        print("FATAL: no OPENROUTER_API_KEY in .env")
        return 2
    used = "OPENROUTER_API_KEY" if env_key("OPENROUTER_API_KEY") else "OPENROUTER_API_KEY_2"

    # 1. precheck: does the catalog declare video input for this model?
    st, models, dt = http("GET", "/models", key, None, 60)
    entry = next((m for m in models.get("data", []) if m.get("id") == MODEL), None)
    if entry is None:
        print(f"PRECHECK FAIL: {MODEL} not in /models (status {st})")
        return 2
    arch = entry.get("architecture", {})
    print(f"PRECHECK status={st} dt={dt}s id={entry.get('id')}")
    print("  input_modalities =", arch.get("input_modalities"))
    print("  output_modalities =", arch.get("output_modalities"))
    print("  context_length =", entry.get("context_length"))
    print("  pricing =", json.dumps(entry.get("pricing", {})))
    video_declared = "video" in (arch.get("input_modalities") or [])

    # 2. the burn: real corpus mp4 as base64 video_url content part
    raw = VIDEO.read_bytes()
    b64 = base64.b64encode(raw).decode()
    print(f"VIDEO {VIDEO.name} bytes={len(raw)} b64_chars={len(b64)}")
    payload = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "video_url",
                 "video_url": {"url": "data:video/mp4;base64," + b64}},
            ],
        }],
    }
    st2, body, dt2 = http("POST", "/chat/completions", key, payload, 300)
    print(f"BURN status={st2} dt={dt2}s key={used}")
    if st2 != 200:
        print("ERROR BODY:", json.dumps(body)[:2000])
        RAW_OUT.write_text(json.dumps(
            {"precheck": {"input_modalities": arch.get("input_modalities"),
                          "video_declared": video_declared},
             "request": {"model": MODEL, "video": VIDEO.name,
                         "video_bytes": len(raw), "shape": "video_url data:video/mp4;base64"},
             "response": {"status": st2, "dt_s": dt2, "body": body}},
            indent=1), encoding="utf-8")
        return 1

    choice = (body.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content") or ""
    reasoning = (choice.get("message") or {}).get("reasoning") or ""
    usage = body.get("usage", {})
    td = usage.get("prompt_tokens_details") or {}
    print("MODEL:", body.get("model"), "provider:", body.get("provider"))
    print("USAGE:", json.dumps(usage))
    print("COST:", json.dumps(body.get("usage", {}).get("cost") or usage.get("cost")))
    print("CONTENT_START>>>" + content + "<<<CONTENT_END")
    print(f"[reasoning_chars={len(reasoning)}]")
    RAW_OUT.write_text(json.dumps(
        {"precheck": {"input_modalities": arch.get("input_modalities"),
                      "video_declared": video_declared,
                      "context_length": entry.get("context_length"),
                      "pricing": entry.get("pricing")},
         "request": {"model": MODEL, "video": str(VIDEO.relative_to(ROOT)),
                     "video_bytes": len(raw), "b64_chars": len(b64),
                     "shape": "video_url data:video/mp4;base64",
                     "max_tokens": 1024, "key": used},
         "response": {"status": st2, "dt_s": dt2, "served_model": body.get("model"),
                      "provider": body.get("provider"), "usage": usage,
                      "content": content, "reasoning_chars": len(reasoning)}},
        indent=1), encoding="utf-8")
    print("RAW saved:", RAW_OUT.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
