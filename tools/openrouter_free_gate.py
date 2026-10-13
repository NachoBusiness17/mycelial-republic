"""openrouter_free_gate -- verify-then-add gate for :free rotation ids (B2-295).

The law this tool enforces: CATALOG PRESENCE IS NOT LIVENESS (B2-61:
qwen/qwen3.8-27b:free sat in the catalog and 429'd on the shared upstream
pool), so a candidate :free id earns its configs/providers.yaml line only
after ONE live chat gate passes. This script runs that gate.

Gate: POST /api/v1/chat/completions, max_tokens 16, the literal prompt
"Reply with the single word: ALIVE". PASS = HTTP 200 with non-empty content.
Everything else (429 shared-pool, 404 gone, 401/402 key-class, empty content)
is FAIL and the id does NOT earn a line.

Usage:
  OPENROUTER_API_KEY=... .venv/Scripts/python.exe tools/openrouter_free_gate.py \
      [--ids id1 id2 ...] [--from-catalog] [--spacing 4] [--out results.json]

--from-catalog pulls the current :free id list from GET /api/v1/models.
Results are written as JSON rows {id, status, http, detail, ts} so the
providers.yaml edit can cite byte evidence per id.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://openrouter.ai/api/v1"
KEY_ENVS = ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2", "OR_API_KEY", "OR_API_KEY_2")
PROMPT = "Reply with the single word: ALIVE"


def key() -> str:
    for name in KEY_ENVS:
        v = os.environ.get(name)
        if v and v.strip():
            return v.strip()
    # repo .env fallback (host seats load_dotenv; a bare run may not have)
    env = Path(__file__).resolve().parents[1] / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith(f"{KEY_ENVS[0]}="):
                v = line.split("=", 1)[1].strip().strip('"')
                if v:
                    return v
    raise SystemExit("no OpenRouter key in env or .env")


def catalog_free_ids() -> list[str]:
    req = urllib.request.Request(f"{BASE}/models",
                                 headers={"Authorization": f"Bearer {key()}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    return sorted(m["id"] for m in data.get("data", []) if m["id"].endswith(":free"))


def _chat(model: str, max_tokens: int) -> dict:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key()}",
                 "Content-Type": "application/json",
                 "HTTP-Referer": "https://localhost.local/mag-free-gate",
                 "X-Title": "mag-free-gate"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            data = json.loads(r.read().decode("utf-8"))
        text = ((data.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
        return {"http": 200, "text": text.strip()}
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")[:160]
        except Exception as e2:  # noqa: BLE001
            # body already consumed/unreadable: name the loss instead of a
            # silent pass (ratchet except-pass fix 2026-09-27)
            detail = f"(detail unreadable: {type(e2).__name__})"
        return {"http": e.code, "text": "", "detail": detail}
    except Exception as e:  # noqa: BLE001
        return {"http": 0, "text": "", "detail": f"{type(e).__name__}: {e}"[:160]}


def gate_one(model: str) -> dict:
    """One id, one live verdict.

    A 200-with-empty-content is retried ONCE at max_tokens 2000 before FAIL:
    reasoning :free models burn a tiny budget on thinking and return empty
    content while fully alive (the B2-62 scar: completion=600, content empty).
    Failing such a lane would deny a working id its rotation line.
    """
    row = {"id": model, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    r = _chat(model, 16)
    if r["http"] == 200 and not r["text"]:
        r2 = _chat(model, 2000)
        r2.setdefault("detail", "")
        r.update(r2, detail=(r2.get("detail", "") + " [200-empty retried at 2000 tokens]").strip())
    text = r.get("text", "")
    row.update(http=r["http"], status="PASS" if text else "FAIL",
               detail=(row.get("detail", "") + (" " if row.get("detail") else "") + text[:40]).strip())
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--from-catalog", action="store_true")
    ap.add_argument("--spacing", type=float, default=4.0,
                    help="seconds between calls; the shared :free pool 429s on bursts")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    ids = list(args.ids)
    if args.from_catalog or not ids:
        ids = catalog_free_ids()
        print(f"catalog :free ids: {len(ids)}", file=sys.stderr)

    rows = []
    for i, mid in enumerate(ids):
        row = gate_one(mid)
        rows.append(row)
        print(f"{row['status']}: {mid} (http {row['http']}) {row['detail'][:80]}",
              flush=True)
        if i + 1 < len(ids):
            time.sleep(args.spacing)

    passed = [r["id"] for r in rows if r["status"] == "PASS"]
    print(f"\n{len(passed)}/{len(rows)} ids EARNED a providers.yaml line:")
    for mid in passed:
        print(f"      - {mid}")
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=1), encoding="utf-8")
        print(f"rows written: {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
