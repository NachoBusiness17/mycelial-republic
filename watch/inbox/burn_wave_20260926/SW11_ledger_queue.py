"""SW-11 landing helper: LEDGER row + QUEUE row pointer + INDEX registration.

Usage:
  .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/SW11_ledger_queue.py \
      --lane B2-116 --slug B2-116-groq-nonchat-classification --verdict LANDED \
      --receipt watch/inbox/burn_wave_20260926/B2_116_..._20260926.md \
      --one-line "..." [--purpose "..."]

Laws honored: append-only LEDGER and INDEX; QUEUE edit is a single anchored
line replace on freshly-read bytes, never a whole-file content rewrite;
seq emitted as a decimal STRING past 2^53 (B2-40 scheme).
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEDGER = ROOT / "memory/burns/LEDGER.jsonl"
QUEUE = ROOT / "watch/inbox/burn_wave_20260926/QUEUE.md"
INDEX = ROOT / "watch/inbox/index_events.jsonl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--verdict", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--one-line", required=True)
    ap.add_argument("--purpose", default="")
    a = ap.parse_args()

    receipt = ROOT / a.receipt
    if not receipt.is_file():
        raise SystemExit(f"receipt missing on disk: {receipt}")
    landing = a.receipt.replace("\\", "/")
    sha = hashlib.sha256(receipt.read_bytes()).hexdigest().upper()

    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "slug": a.slug,
        "verdict": a.verdict,
        "landing": landing,
        "one_line": a.one_line,
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("ledger rows appended, ts", row["ts"])

    # QUEUE row pointer: single anchored line replace on freshly-read bytes.
    lines = QUEUE.read_text(encoding="utf-8").splitlines(keepends=True)
    marker = f"] {a.lane} "
    hit = -1
    for i, ln in enumerate(lines):
        if ln.startswith("- [") and marker in ln[:24]:
            hit = i
            break
    if hit < 0:
        raise SystemExit(f"queue row not found for {a.lane}")
    if landing in lines[hit]:
        print("queue row already carries the pointer")
    else:
        lines[hit] = lines[hit].rstrip("\r\n") + f" -> {landing}\n"
        QUEUE.write_text("".join(lines), encoding="utf-8", newline="")
        print("queue row pointer landed on line", hit + 1)

    # INDEX registration append (decimal STRING seq past 2^53).
    last = ""
    if INDEX.is_file():
        with INDEX.open("r", encoding="utf-8") as f:
            for ln in f:
                if ln.strip():
                    try:
                        last = json.loads(ln).get("seq", last)
                    except json.JSONDecodeError:
                        pass
    nxt = str(int(last) + 1) if last.isdigit() else "1790451700000000000"
    ev = {
        "seq": nxt,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "op": "register",
        "file": landing,
        "sha256": sha,
        "class": "receipt",
        "purpose": a.purpose or f"{a.lane} landing receipt ({a.verdict})",
        "writer": "zcode-sw-11",
        "nonce": 1,
    }
    with INDEX.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    print("index seq", nxt, "sha", sha[:12])


if __name__ == "__main__":
    main()
