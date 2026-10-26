"""_x_fx_fetch.py - adhoc sweep seat: resolve X posts through the fxtwitter door.

Door: https://api.fxtwitter.com/<user>/status/<id> (the ask's named resolution
door; JSON, no login). Saves raw JSON per post under sweep/raw/x_grok/ and
prints compact fields. Discovery came from the grok X search; fxtwitter is the
quote source of record (grok output is discovery only).
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

# (handle, status_id) - all surfaced by the grok X searches this sitting
POSTS = [
    # the_posterior VeriHarness/voting thread
    ("the_posterior", "2107055377489789035"),
    ("the_posterior", "2107055379981176943"),
    ("the_posterior", "2107055384406184399"),
    ("rakeshsahni_", "2107060667958309188"),
    ("omarsar0", "2106700905051746803"),
    # Vals AI teams vs solo cluster
    ("AIQuanting", "2109315478133088380"),
    ("Tesla_Optimus_K", "2109337054639444063"),
    ("XSeyvion", "2109358443408544040"),
    # Agensh / DeLM / width economics
    ("omarsar0", "2104377054829613473"),
    ("Mao_Yuzhen", "2108261216473014498"),
    ("assumebreach", "2109258667308753376"),
    ("scaling01", "2102806864178135051"),
    ("deeepakbagada", "2108030622664982840"),
    ("BenToFound", "2108174123100729830"),
    ("rvaniaaaa", "2101296533899510266"),
    # emergence
    ("PrimeIntellect", "2108672479007047952"),
    ("askalphaxiv", "2102707295717036507"),
    ("Skoorbkaz", "2103696139283210729"),
    ("ProfBuehlerMIT", "2102337582159835512"),
    # consensus / judge failure set
    ("toomij99", "2108452213899382881"),
    ("jaenanft", "2108390620834529399"),
    ("wfouaaad", "2109053677080039611"),
    ("builderleader", "2108310331147645031"),
    ("RahilVerma13", "2107491286139977867"),
    ("winzheng_lab", "2108548727820657129"),
    ("SaadAmmrun", "2109245714391818255"),
    ("youshenlim", "2108375051288371480"),
    # production failure / harness shape
    ("theagenticdaily", "2107497375556411398"),
    ("arpit_bhayani", "2100444191876903215"),
    ("heman10x", "2108241801056563514"),
    ("Arindam_1729", "2109347836433519007"),
    ("arpit_bhayani", "2102388569449140316"),
]


def main() -> int:
    ok = fail = 0
    for handle, pid in POSTS:
        dest = RAW / f"_fx_{handle}_{pid}.json"
        if dest.exists():
            print(f"CACHED {handle} {pid}")
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
            txt = (t.get("text") or "").replace("\n", " ")[:110]
            print(f"OK {handle} {pid} {t.get('created_at','?')} likes={t.get('likes')} rt={t.get('retweets')} views={t.get('views')} | {txt}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {handle} {pid}: {type(e).__name__} {e}")
            fail += 1
        time.sleep(0.8)
    print(f"done ok={ok} fail={fail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
