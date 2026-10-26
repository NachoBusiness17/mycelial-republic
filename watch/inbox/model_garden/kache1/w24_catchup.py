"""KACHE-1 PART B catch-up: re-fire the 7 DNF asks from the 24-wide burst at
width 3 (the SWARM_1 recovery shape: conditions changed = lower width, not a
same-params refire; no terminal markers were minted, the 429s raised before
any banking). Gated path unchanged (tools.model_garden.run_ask)."""
from __future__ import annotations

import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import tools.model_garden as mg  # noqa: E402

QUEUE = ROOT / "watch" / "inbox" / "model_garden" / "kache1" / "w24" / "q"
DNF = ["K03", "K06", "K11", "K12", "K13", "K15", "K24"]
RESULTS: list[dict] = []
LOCK = threading.Lock()


def work(kid: str) -> None:
    d = QUEUE / kid.lower()
    t0 = time.time()
    try:
        row = mg.run_ask(d)
        res = {"id": f"kache1-w24-{kid}", "ok": True,
               "run_s": round(time.time() - t0, 2), "row": row}
    except Exception as exc:  # noqa: BLE001
        res = {"id": f"kache1-w24-{kid}", "ok": False,
               "run_s": round(time.time() - t0, 2), "err": repr(exc)[:300]}
    with LOCK:
        RESULTS.append(res)
    print(f"[catchup] {kid}: {'OK' if res['ok'] else 'FAIL'} {res['run_s']}s",
          flush=True)


def main() -> None:
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = []
        for i, kid in enumerate(DNF):
            futs.append(pool.submit(work, kid))
            time.sleep(6)  # width-3 submission stagger
        for f in futs:
            f.result()
    out = {"schema": "kache.w24_catchup.v1",
           "moment": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
           "width": 3, "results": RESULTS,
           "wall_clock_s": round(time.time() - t0, 1)}
    path = ROOT / "watch" / "inbox" / "model_garden" / "kache1" / "w24" / "catchup.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    ok = sum(1 for r in RESULTS if r["ok"])
    print(f"[catchup] {ok}/{len(DNF)} landed, {out['wall_clock_s']}s", flush=True)


if __name__ == "__main__":
    main()
