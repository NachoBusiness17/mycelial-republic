"""B2-421 caption_via invariant pin (run after any CAPTION_LEDGER rebuild).

Invariant: every non-empty caption_via in CAPTION_LEDGER_20260926.jsonl names
a carrier anchor @MrPool_Q#N whose ledger_full.jsonl row N is grouped=True,
carries non-empty text, and sits on the same calendar date as the pointing
row. B2-12's +/-3 search order cannot re-derive the 9 B2-90 v2 carriers
(widened-window album runs), so a plain rebuild regresses them to empty;
this pin is the gate that names such a regression instead of letting it pass
green.

Usage:
  .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_421_caption_via_verify.py \
      [--ledger watch/inbox/CAPTION_LEDGER_20260926.jsonl] [--full .../ledger_full.jsonl]

Two failure classes, both named:
  1. a present caption_via whose carrier is not grouped=True / non-empty text /
     same calendar date;
  2. a PINNED caption_via that went empty or changed (the rebuild-regression
     class: B2-12's +/-3 order cannot re-derive the 9 B2-90 v2 carriers, so a
     plain rebuild blanks them and an unpinned count check would read the
     smaller set as clean). Pin file: B2_421_caption_via_pin.json, an object
     {"msg_id": "caption_via", ...} frozen from the 2026-09-26 landed ledger
     (111 rows). Update the pin only with a receipt naming why a carrier moved.

Exit 0 prints "CAPTION_VIA ok <n>/<n>"; exit 1 prints one CAPTION_VIA FAIL
line per violating row and a final count. --ledger accepts any path so the
falsifier can run the pin against a regressed COPY without touching bytes.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEDGER = ROOT / "watch" / "inbox" / "CAPTION_LEDGER_20260926.jsonl"
FULL = ROOT / "watch" / "inbox" / "mrpool_export" / "ledger_full.jsonl"
PIN = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_421_caption_via_pin.json"
VIA_RE = re.compile(r"@MrPool_Q#(\d+)$")


def load_full(path: Path) -> dict:
    src = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            src[int(r["msg_id"])] = r
    return src


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--full", default=str(FULL))
    ap.add_argument("--pin", default=str(PIN))
    a = ap.parse_args()

    full = load_full(Path(a.full))
    pinned = {}
    pin_path = Path(a.pin)
    if pin_path.is_file():
        pinned = json.loads(pin_path.read_text(encoding="utf-8"))

    checked = failed = 0
    seen = {}
    with open(a.ledger, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            mid = int(row["msg_id"])
            via = row.get("caption_via") or ""
            seen[mid] = via
            if not via:
                if str(mid) in pinned:
                    print(f"CAPTION_VIA FAIL msg {mid}: pinned carrier lost "
                          f"(pin says {pinned[str(mid)]!r}, ledger row is empty)")
                    failed += 1
                continue
            checked += 1
            m = VIA_RE.match(via)
            cite = row.get("cite") or f"msg {row.get('msg_id')}"
            if not m:
                print(f"CAPTION_VIA FAIL {cite}: anchor not parseable: {via!r}")
                failed += 1
                continue
            carrier = full.get(int(m.group(1)))
            why = None
            if carrier is None:
                why = "carrier msg_id absent from ledger_full"
            else:
                same_date = str(carrier.get("date", ""))[:10] == str(row.get("date", ""))[:10]
                if not carrier.get("grouped"):
                    why = "carrier grouped is not True"
                elif not str(carrier.get("text") or "").strip():
                    why = "carrier text empty"
                elif not same_date:
                    why = f"carrier date {str(carrier.get('date'))[:10]} != row date {str(row.get('date'))[:10]}"
            if why:
                print(f"CAPTION_VIA FAIL {cite} via {via}: {why}")
                failed += 1
    # pinned rows that vanished from the ledger entirely (row removed/reordered out)
    for mid, via in sorted(pinned.items()):
        if int(mid) not in seen:
            print(f"CAPTION_VIA FAIL msg {mid}: pinned row absent from ledger (pin says {via!r})")
            failed += 1
    print(f"CAPTION_VIA {'ok' if failed == 0 else 'FAIL'} {checked - failed}/{checked}"
          f" (rows with caption_via: {checked}, pinned: {len(pinned)}, violations: {failed})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
