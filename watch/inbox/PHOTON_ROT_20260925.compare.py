# PHOTON_ROT_20260925.compare.py - byte-adjudication of the 4 stranded
# persistent-coding-agents quotes (rows 2-5, 1-indexed) against:
#   1. live Photon post bytes saved to PHOTON_ROT_20260925.live.html
#   2. AlphaSignal Sep-24 piece saved to PHOTON_ROT_20260925.alphasignal.html
# Re-run: .venv/Scripts/python.exe watch/inbox/PHOTON_ROT_20260925.compare.py
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
LANE = REPO / "memory/runs/mickey17_v2/lanes/persistent-coding-agents.json"
LIVE = REPO / "watch/inbox/PHOTON_ROT_20260925.live.html"
ASIG = REPO / "watch/inbox/PHOTON_ROT_20260925.alphasignal.html"


def decode_escapes(s: str) -> str:
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), s)


def to_text(raw: bytes) -> str:
    s = decode_escapes(raw.decode("utf-8", errors="replace"))
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    return s


def canon(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]", "-", s)
    s = re.sub(r"[\u2018\u2019\u02bc]", "'", s)
    s = re.sub(r"[\u201c\u201d]", '"', s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", canon(s).lower())


def tests(quote: str, page_text: str) -> dict:
    return {
        "exact": canon(quote) in canon(page_text),
        "slug": slug(quote) in slug(page_text),
    }


def main() -> None:
    rows = json.loads(LANE.read_text(encoding="utf-8"))
    live_raw = LIVE.read_bytes()
    asig_raw = ASIG.read_bytes()
    live_text = to_text(live_raw)
    asig_text = to_text(asig_raw)
    print(f"live bytes={len(live_raw)} chars={len(live_text)}")
    print(f"alphasignal bytes={len(asig_raw)} chars={len(asig_text)}")

    # rows 2-5 (1-indexed) = list items 1..4 ; item 0 is the swarm row (row 1)
    receipt = {"live_bytes": len(live_raw), "alphasignal_bytes": len(asig_raw), "quotes": []}
    for idx in range(1, 5):
        q = rows[idx]["quote"]
        r = {"row_1indexed": idx + 1, "quote": q}
        r["live"] = tests(q, live_text)
        r["alphasignal"] = tests(q, asig_text)
        receipt["quotes"].append(r)
        print(f"[row{idx + 1}] live.exact={r['live']['exact']} live.slug={r['live']['slug']} "
              f"asig.exact={r['alphasignal']['exact']} asig.slug={r['alphasignal']['slug']}")

    # row 1 swarm sentence: lane claims it survives the revision
    swarm = rows[0]["quote"]
    receipt["row1_swarm_live"] = tests(swarm, live_text)
    print(f"[row1-swarm] live.exact={receipt['row1_swarm_live']['exact']} "
          f"live.slug={receipt['row1_swarm_live']['slug']}")

    # corroboration keys
    keys = [
        "20% fewer machines", "fewer machines", "five months", "100% of live traffic",
        "shadow traffic", "resumable", "percentile", "index formats",
        "800", "65 ms", "65ms",
    ]
    receipt["keys"] = {}
    for k in keys:
        ck = canon(k)
        in_live = ck in canon(live_text) or slug(k) in slug(live_text)
        in_asig = ck in canon(asig_text) or slug(k) in slug(asig_text)
        receipt["keys"][k] = {"live": in_live, "alphasignal": in_asig}
        print(f"[key] {k!r}: live={in_live} alphasignal={in_asig}")

    out = REPO / "watch/inbox/PHOTON_ROT_20260925.compare.json"
    out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"receipt written: {out}")


if __name__ == "__main__":
    main()
