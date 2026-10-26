"""_sweff_x_fx_fetch.py - adhoc sweep seat (inference-efficiency): resolve X posts
through the fxtwitter door (the ask's named resolution door; JSON, no login).
Discovery came from grok X search (_sweff_x_grok_search.py); fxtwitter is the
quote source of record. Saves raw JSON under sweep/raw/x_grok/.
"""
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

# (handle, status_id, tag) - surfaced by the grok X searches this sitting
POSTS = [
    # specdec cluster
    ("sebastavar", "2107803719815291333", "ngram"),
    ("ghulamurtaza_", "2108674475344462013", "saluki-mtp"),
    ("CryptoBandit100", "2108589868192600376", "dgx-serving"),
    ("CryptoBandit100", "2109329938474266650", "dgx-acceptance"),
    ("Sametheus", "2109070344627843240", "batch-caveat"),
    ("roy_eisenstadt", "2104624416726409646", "switchsd"),
    ("liquidai", "2103131179100819783", "dspark-3b"),
    ("SJRonanMD", "2109301440170823775", "realtext"),
    ("spheron", "2104764045052305644", "eagle3-vendor"),
    ("cudanexus", "2109340558812697037", "vllm-mtp"),
    ("sunsetsyntax", "2108465254246355148", "tokenizer"),
    ("ainotesus", "2109331002250101127", "akamai-fail"),
    ("omkarchebale", "2107692247684890795", "battleground"),
    # sched cluster
    ("SupersocksIntel", "2098310560253165822", "prefix-aware"),
    ("brockerorg", "2108269077798019417", "dynamo-session"),
    ("awais_khawar", "2108973336025792815", "dynamo-ep"),
    ("anilkalm", "2109333671052521682", "sglang-role"),
    ("MizanAl19145045", "2108264890712633799", "llm-d"),
    ("Zero_to_MVP", "2106727628661018980", "gridcore"),
    ("bountyAIhunter", "2106783910071795846", "kev-router"),
    ("CalatheaAI", "2108814812738392281", "rarecache"),
    ("BoboLinNotes", "2108778403486896499", "queueing"),
    ("ardadev", "2107969024432763035", "llmkube"),
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
            txt = (t.get("text") or "").replace("\n", " ")[:130]
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
