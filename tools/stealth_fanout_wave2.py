"""stealth_fanout wave 2 — missed items on the two PROVEN lanes only.

Wave 1 (2026-09-28): 2/12 ok — muse-glimmer-30b and ling-3.0-flash-vl
delivered real content; the rest hit 403s/rate limits (pool hot, per
RIB_FREE_USAGE_POLICY). Wave 2: spaced retries of the 10 missed items
on those two proven lanes, workers=2 (reward patience, not pressure).
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from stealth_fanout import ASKS, OUT_DIR, HEARTBEAT, LANES, dispatch  # noqa: E402

PROVEN = [l for l in LANES if l["model"] in
          ("meta/muse-glimmer-30b", "inclusionai/ling-3.0-flash-vl")]
MISSED = {"vortex-latent", "water-plasma", "belady-lruk", "belt-cube-real",
          "solomonoff-pretrain", "contrastive-wm", "headless-agent-cli",
          "eam-tracking", "moe-hotswap", "or-cache-mechanics"}


def run_one(i: int, item_id: str, ask: str) -> dict:
    lane = PROVEN[i % len(PROVEN)]
    t0 = time.time()
    try:
        text, usage = dispatch(lane, ask)
        ok = bool(text.strip())
    except Exception as e:
        text, ok = f"DISPATCH-ERR {type(e).__name__}: {str(e)[:140]}", False
        usage = {}
    dt = round(time.time() - t0, 1)
    out = OUT_DIR / f"fan2_{item_id}_{lane['model'].replace('/', '_')}.md"
    out.write_text(
        f"# FAN2 {item_id}\n\nlane model: {lane['model']}\n\n---\n\n{text}\n",
        encoding="utf-8")
    row = {"id": item_id, "model": lane["model"], "ok": ok, "dt_s": dt,
           "chars": len(text),
           "cached": (usage.get("prompt_tokens_details") or {}).get("cached_tokens")}
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    asks = [(i, a) for i, a in ASKS if i in MISSED]
    print(f"wave 2: {len(asks)} items on {len(PROVEN)} proven lanes, workers=2",
          flush=True)
    rows = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_one, i, item_id, ask): item_id
                for i, (item_id, ask) in enumerate(asks)}
        for fut in as_completed(futs):
            rows.append(fut.result())
    ok_n = sum(1 for r in rows if r["ok"])
    print(f"WAVE2 DONE {ok_n}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
