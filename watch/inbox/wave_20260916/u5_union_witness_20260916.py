"""U5 — UNION WAVE WITNESS driver (wave-lane, FREE only, $0 cap).

One call: the night's digest + outside-reviewer prompt -> stealth/union-alpha on OpenRouter.
Mirrors e_union_alpha_20260916.py's SSRF-safe call pattern (guard_endpoint, https, openrouter.ai only).
Key via mag.flight_recorder.load_env, never printed. Law: 402/403 -> record and stop. 429 -> one retry.
Tape: memory/runs/u5_union_witness_20260916/raw.jsonl (append-as-you-go).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from mag.flight_recorder import load_env, guard_endpoint  # noqa: E402

ENV = load_env()
RUN_DIR = os.path.join(ROOT, "memory", "runs", "u5_union_witness_20260916")
TAPE = os.path.join(RUN_DIR, "raw.jsonl")
ALLOW = {"openrouter.ai"}
BASE = "https://openrouter.ai/api/v1"
MODEL = "stealth/union-alpha"
os.makedirs(RUN_DIR, exist_ok=True)

DIGEST_PATH = os.path.join(HERE, "receipts", "U5_UNION_WAVE_WITNESS.md")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_digest() -> str:
    with open(DIGEST_PATH, encoding="utf-8") as fh:
        txt = fh.read()
    start = txt.index("## Digest")
    end = txt.index("## Witness prompt sent")
    block = txt[start:end]
    # keep only the digest body between the --- markers
    body = block.split("---", 1)[1].rsplit("---", 1)[0].strip()
    n = len(body) // 4  # rough token estimate
    print(f"[u5] digest chars={len(body)} est_tokens~{n}", file=sys.stderr)
    assert n <= 1500, f"digest too big: ~{n} tokens"
    return body


PROMPT_TMPL = """{digest}

---

You are an outside reviewer. Given this state, rank the next 5 highest-value actions for this project, name the single biggest unmanaged risk, and identify anything that looks like self-congratulation instead of evidence. Be blunt."""


def call(question: str, temperature: float, seed: int, max_tokens: int = 2500,
         timeout: int = 300) -> dict:
    key = ENV.get("OPENROUTER_API_KEY", "")
    url = BASE.rstrip("/") + "/chat/completions"
    guard_endpoint(url, ALLOW)
    body = {"model": MODEL, "temperature": temperature, "max_tokens": max_tokens, "seed": seed,
            "messages": [{"role": "user", "content": question}]}
    attempt = 0
    while True:
        attempt += 1
        t0 = time.time()
        rec = {"seat": "U5_union_wave_witness", "seed": seed, "temperature": temperature,
               "ts": now(), "attempt": attempt}
        req = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "User-Agent": "mag-u5-witness/1.0",
                     "HTTP-Referer": "https://local-sovereign-agent.invalid",
                     "X-Title": "Mag U5 Union Wave Witness"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            msg = d["choices"][0]["message"]
            txt = (msg.get("content") or "").strip()
            rec["finish_reason"] = d["choices"][0].get("finish_reason")
            rec["usage"] = d.get("usage") or {}
            if not txt:
                rec.update({"ok": False, "error": "empty_content",
                            "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200]})
            else:
                rec.update({"ok": True, "answer": txt, "chars": len(txt)})
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:400]
            rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
            if e.code in (402, 403):
                with open(TAPE, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f"[u5] PAID WALL HTTP {e.code} — record and stop. detail={detail}", file=sys.stderr)
                return rec
            if e.code == 429 and attempt < 2:
                _append(rec)
                print("[u5] 429, one cooldown retry (25s)...", file=sys.stderr)
                time.sleep(25)
                continue
        except Exception as e:  # noqa: BLE001
            rec.update({"ok": False, "error": type(e).__name__, "detail": str(e)[:400]})
        _append(rec)
        return rec


def _append(rec: dict) -> None:
    with open(TAPE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> None:
    digest = read_digest()
    prompt = PROMPT_TMPL.format(digest=digest)
    rec = call(prompt, temperature=0.4, seed=2026091615)
    if rec.get("ok"):
        print("=== ANSWER BEGIN ===")
        print(rec["answer"])
        print("=== ANSWER END ===")
        print(f"[u5] usage={rec.get('usage')} chars={rec.get('chars')}", file=sys.stderr)
    else:
        print(f"[u5] CALL FAILED: {rec.get('error')} {rec.get('detail', '')[:300]}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
