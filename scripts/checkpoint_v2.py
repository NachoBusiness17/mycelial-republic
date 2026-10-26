#!/usr/bin/env python3
"""v2 checkpoints + proof export (decision 6 / 8).

  python scripts/checkpoint_v2.py                 # append an UNSIGNED checkpoint (with extends-proof)
  python scripts/checkpoint_v2.py --proof I [--full] --out FILE   # export a knot proof
  python scripts/checkpoint_v2.py --proof latest --out FILE
  python scripts/checkpoint_v2.py --sign [--publish]   # DEFAULT OFF: needs mag.yaml chain_v2_signing /
        chain_v2_publish true AND env MAG_CHAIN_V2_SIGNING=1 / MAG_CHAIN_V2_PUBLISH=1; never runs git.
Hourly: schedule this script (no scheduler is installed by the v2 build).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from mag import bintree_v2 as bt  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--v2-dir")
    ap.add_argument("--proof", help="row index or 'latest'")
    ap.add_argument("--full", action="store_true", help="embed v1 row + knot body (opt-in)")
    ap.add_argument("--out")
    ap.add_argument("--sign", action="store_true")
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args(argv)
    st = bt.Store(a.v2_dir)
    if not st.exists():
        print(json.dumps({"ok": False, "error": "no v2 chain"}))
        return 2
    if a.proof is not None:
        ch = st.load()
        i = ch.n - 1 if a.proof == "latest" else int(a.proof)
        doc = bt.build_proof(st, ch, i, full=a.full)
        text = json.dumps(doc)
        if a.out:
            Path(a.out).write_text(text, encoding="utf-8")
        else:
            print(text)
        print(json.dumps({"ok": True, "index": i, "n": ch.n, "root": doc["root"], "mode": doc["mode"],
                          "bytes": len(text)}), file=sys.stderr)
        return 0
    with bt.v2_lock(st, timeout=60):
        cp = bt.make_checkpoint(st, st.load(), sign=a.sign)
    out = {"ok": True, "n": cp["n"], "root": cp["root"], "status": cp["status"]}
    if a.publish:
        out["published"] = str(bt.publish_checkpoint(cp))
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (bt.SigningDisabled, RuntimeError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        sys.exit(2)
