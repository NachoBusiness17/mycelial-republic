"""U5 continuation — witness answer hit max_tokens mid-sentence; one continuation call.

Continues verbatim from the last visible fragment. Same seat/model/laws. Tape: same raw.jsonl.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from mag.flight_recorder import load_env, guard_endpoint  # noqa: E402

ENV = load_env()
TAPE = os.path.join(ROOT, "memory", "runs", "u5_union_witness_20260916", "raw.jsonl")
ALLOW = {"openrouter.ai"}
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "stealth/union-alpha"

PROMPT = """You are the same outside reviewer. Your previous answer was cut off mid-sentence at the token limit. Your last visible text ended exactly here:

"9. ... - \\"49/50 answered, $0\\" — response rate is not validity. 49 answers to pre-registered questions —"

Continue from that exact point and finish your review: complete your self-congratulation list, then deliver the requested deliverables in order: (a) the ranked next 5 highest-value actions for this project, (b) the single biggest unmanaged risk, (c) a closing one-line verdict on whether this project's epistemic discipline is real or theater. Be blunt. Do not repeat what you already said."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    key = ENV.get("OPENROUTER_API_KEY", "")
    guard_endpoint(URL, ALLOW)
    body = {"model": MODEL, "temperature": 0.4, "max_tokens": 4000, "seed": 2026091616,
            "messages": [{"role": "user", "content": PROMPT}]}
    rec = {"seat": "U5_union_wave_witness", "mode": "continuation", "seed": 2026091616,
           "temperature": 0.4, "ts": now()}
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-u5-witness/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "Mag U5 Union Wave Witness"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        rec["finish_reason"] = d["choices"][0].get("finish_reason")
        rec["usage"] = d.get("usage") or {}
        rec.update({"ok": bool(txt), "answer": txt, "chars": len(txt),
                    "error": None if txt else "empty_content"})
    except urllib.error.HTTPError as e:
        rec.update({"ok": False, "error": f"HTTP {e.code}",
                    "detail": e.read().decode("utf-8", "replace")[:400]})
    except Exception as e:  # noqa: BLE001
        rec.update({"ok": False, "error": type(e).__name__, "detail": str(e)[:400]})
    with open(TAPE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if rec.get("ok"):
        print("=== CONTINUATION BEGIN ===")
        print(rec["answer"])
        print("=== CONTINUATION END ===")
        print(f"[u5] finish={rec.get('finish_reason')} usage_total={rec['usage'].get('total_tokens')}",
              file=sys.stderr)
    else:
        print(f"[u5] CONT FAILED: {rec.get('error')} {rec.get('detail', '')[:300]}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
