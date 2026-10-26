"""SW-00 lane helpers: anchored QUEUE row landing-note appender + LEDGER row appender.

Usage:
  python SW00_lane_helpers.py queue <B2-XXX> <landing-note text>
  python SW00_lane_helpers.py ledger <json-fields as key=value ...>
Anchored edit: asserts exactly one row start match, asserts note present after write.
"""
import sys, os, json, datetime, io

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
QUEUE = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926", "QUEUE.md")
LEDGER = os.path.join(ROOT, "memory", "burns", "LEDGER.jsonl")


def queue_note(bid, note):
    with io.open(QUEUE, "r", encoding="utf-8") as f:
        q = f.read()
    start_tag = "- [x] " + bid + " "
    starts = [i for i in range(len(q)) if q.startswith(start_tag, i)]
    # restrict to line starts
    starts = [i for i in starts if i == 0 or q[i-1] == "\n"]
    assert len(starts) == 1, "anchor count %d for %s" % (len(starts), bid)
    s = starts[0]
    # row ends at next line starting with "- [" (row or CLAIM)
    nxt = len(q)
    for i in range(s + 1, len(q)):
        if q.startswith("- [", i) and (q[i-1] == "\n"):
            nxt = i
            break
    row = q[s:nxt]
    assert "Landed 2026-09-26" not in row, "row %s already carries a landing note" % bid
    addition = " Landed 2026-09-26 (SW-00): " + note + "\n"
    newq = q[:nxt-1] + addition + q[nxt:]
    with io.open(QUEUE, "w", encoding="utf-8", newline="") as f:
        f.write(newq)
    with io.open(QUEUE, "r", encoding="utf-8") as f:
        check = f.read()
    assert note in check, "post-write assert failed for %s" % bid
    print("queue row %s annotated" % bid)


def ledger_row(fields):
    row = {}
    for kv in fields:
        k, v = kv.split("=", 1)
        row[k] = v
    row.setdefault("ts", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    with io.open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("ledger row %s appended" % row.get("slug", "?"))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "queue":
        queue_note(sys.argv[2], sys.argv[3])
    elif cmd == "ledger":
        ledger_row(sys.argv[2:])
    else:
        raise SystemExit("unknown cmd")
