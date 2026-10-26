# U9 one-shot worker call: stealth/union-alpha drafts the real MCP server.py (free window, $0).
# Law: OPENROUTER_API_KEY via mag.flight_recorder.load_env, never printed, never logged.
# Degrade law: on 429/402 storm, back off twice, then file what landed.
import json, sys, time, urllib.request, urllib.error

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, ROOT)
from mag.flight_recorder import load_env  # noqa: E402

PROMPT_PATH = ROOT + r"\watch\inbox\wave_20260916\drafts\u9_union_prompt.md"
OUT_PATH = ROOT + r"\watch\inbox\wave_20260916\drafts\u9_union_draft_server.py"

env = load_env(ROOT)
key = env.get("OPENROUTER_API_KEY", "")
if not key:
    print("STATUS: NO_KEY")
    sys.exit(2)

prompt = open(PROMPT_PATH, encoding="utf-8").read()
body = {
    "model": "stealth/union-alpha",
    "temperature": 0.2,
    "max_tokens": 16000,
    "stream": True,
    "messages": [
        {"role": "system", "content": "You are a precise Python systems worker. Output only what is asked: one raw Python file, no fences, no prose."},
        {"role": "user", "content": prompt},
    ],
}

rows = []
text = None
for attempt in (1, 2, 3):
    t0 = time.time()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "mag-u9-union-mcp/1.0",
            "HTTP-Referer": "https://local-sovereign-agent.invalid",
            "X-Title": "Mag U9 Union MCP Server",
            "Accept": "text/event-stream",
        })
    try:
        chunks = []
        finish = None
        usage = None
        err_head = ""
        with urllib.request.urlopen(req, timeout=300) as r:
            for raw_line in r:
                line = raw_line.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                try:
                    ev = json.loads(payload)
                except Exception:
                    if not err_head:
                        err_head = payload[:200]
                    continue
                if ev.get("error"):
                    err_head = json.dumps(ev["error"])[:300]
                    break
                if ev.get("usage"):
                    usage = ev["usage"]
                ch = (ev.get("choices") or [{}])[0]
                delta = ch.get("delta") or {}
                if delta.get("content"):
                    chunks.append(delta["content"])
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
        text = "".join(chunks).strip()
        rows.append({"attempt": attempt, "ok": bool(text), "stream": True,
                     "chars": len(text), "finish_reason": finish,
                     "usage": usage, "err_head": err_head,
                     "latency_ms": int((time.time() - t0) * 1000)})
        if text:
            break
        time.sleep(10)  # whitespace storm: brief back off, then degrade to next attempt
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:200]
        rows.append({"attempt": attempt, "ok": False, "status": e.code, "detail": detail,
                     "latency_ms": int((time.time() - t0) * 1000)})
        if e.code in (429, 402):
            time.sleep(20 * attempt)  # storm law: back off, degrade gracefully
            continue
        break
    except Exception as e:  # noqa: BLE001
        rows.append({"attempt": attempt, "ok": False, "status": None,
                     "detail": f"{type(e).__name__}: {str(e)[:160]}",
                     "latency_ms": int((time.time() - t0) * 1000)})
        break

print(json.dumps({"model": "stealth/union-alpha", "attempts": rows}, indent=1))
if text:
    open(OUT_PATH, "w", encoding="utf-8", newline="\n").write(text)
    print(f"STATUS: DRAFT_FILED chars={len(text)} -> {OUT_PATH}")
else:
    print("STATUS: NO_CONTENT (file what landed)")
