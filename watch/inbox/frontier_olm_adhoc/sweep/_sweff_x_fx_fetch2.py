"""_sweff_x_fx_fetch2.py - second batch: dskoff-topic posts through fxtwitter."""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / "AGENTS.md").is_file() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
RAW = ROOT / "watch" / "inbox" / "frontier_olm_adhoc" / "sweep" / "raw" / "x_grok"
RAW.mkdir(parents=True, exist_ok=True)

POSTS = [
    ("rohanpaul_ai", "2108772007282200658", "inertia-paper"),
    ("dan3458", "2108905528210628862", "dsk-recipe-1"),
    ("dan3458", "2108906541512569269", "dsk-recipe-5"),
    ("janmm_va", "2108656759523168641", "blind-cost"),
    ("janmm_va", "2108656761968414975", "blind-empty"),
    ("cozybearlog", "2101006279510827440", "empty-gw"),
    ("cozybearlog", "2102052987334209707", "empty-cap"),
    ("TinyRouterHQ", "2102220262548689021", "empty-budget-json"),
    ("aakashgupta", "2109372782257844256", "thinking-off-bill"),
    ("yume_arasaki", "2099485624395088185", "flash-local-grid"),
    ("DevRico003", "2105577524361150925", "flash-local-toks"),
    ("Eldan_nomad", "2108059947984699620", "stop-signal"),
    ("0xsacreddev", "2106630869662486729", "glm-empty"),
    ("OneMuxAPI", "2108710046561603806", "reasoning-400"),
]


def main() -> int:
    ok = fail = 0
    for handle, pid, tag in POSTS:
        dest = RAW / f"_sweff_fx_{tag}_{handle}_{pid}.json"
        if dest.exists():
            print(f"CACHED {tag} {handle} {pid}")
            ok += 1
            continue
        url = f"https://api.fxtwitter.com/{handle}/status/{pid}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (mag sweep gopher)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read().decode("utf-8", "replace")
            dest.write_text(data, encoding="utf-8")
            j = json.loads(data)
            t = j.get("tweet", {}) or {}
            txt = (t.get("text") or "").replace("\n", " ")[:120]
            print(f"OK {tag} {handle} {pid} {t.get('created_at','?')} likes={t.get('likes')} views={t.get('views')} | {txt}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {tag} {handle} {pid}: {type(e).__name__} {e}")
            fail += 1
        time.sleep(0.7)
    print(f"done ok={ok} fail={fail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
