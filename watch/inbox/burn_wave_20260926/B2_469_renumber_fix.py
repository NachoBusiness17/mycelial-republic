# B2-469 renumber correction (2026-09-26): the drafted band 495..497 was
# overtaken by concurrent self-feed numbering (B2-498..B2-512 landed from
# B2-465/B2-489/B2-490/B2-491/B2-464 while these rows were pending), so the
# briefs refiled highest+1 as B2-513..B2-515 per the B2-167 law. This script
# aligns every artifact that still cites the drafted band: the board CLAIMED
# line, the landing note, the LEDGER one_line (seconds-old own row, erratum
# named in place), and the receipt tail (followed by an AMENDMENT event).
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
QUEUE = HERE / "QUEUE.md"
LEDGER = REPO / "memory" / "burns" / "LEDGER.jsonl"
EVENTS = REPO / "watch" / "inbox" / "index_events.jsonl"
RECEIPT = HERE / "B2_469_dated_meters_20260926.md"


def guard(text: str) -> str:
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in correction text")
    return text


def sub_once(text: str, old: str, new: str, what: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one occurrence of {what}, found {text.count(old)}")
    return text.replace(old, guard(new), 1)


def main() -> None:
    # 1. board: the CLAIMED line gains the band-move note
    q = QUEUE.read_text(encoding="utf-8", errors="replace")
    q = sub_once(
        q,
        "(B2-469 self-feed band B2-495..B2-497; highest id on fresh bytes B2-494; foreign active CLAIMs honored, appends only, no rewrite)",
        "(B2-469 self-feed band B2-495..B2-497; highest id on fresh bytes B2-494; foreign active CLAIMs honored, appends only, no rewrite; band overtaken: concurrent self-feeds landed B2-498..B2-512 while these rows were pending, 495..497 left unfiled, briefs refiled highest+1 B2-513..B2-515 per the B2-167 lane-id claim law)",
        "board CLAIMED line",
    )
    # 2. board: the landing note names the true brief numbers
    q = sub_once(
        q,
        'wire-pull arm filed forward as B2-495; receipt watch/inbox/burn_wave_20260926/B2_469_dated_meters_20260926.md; self-fed B2-495 B2-496 B2-497 UNCHECKED.',
        'wire-pull arm filed forward as B2-513; receipt watch/inbox/burn_wave_20260926/B2_469_dated_meters_20260926.md; self-fed B2-513 B2-514 B2-515 UNCHECKED (drafted band 495..497 overtaken by concurrent numbering 498..512 mid-close, refiled highest+1 per the B2-167 law).',
        "board landing note",
    )
    with QUEUE.open("w", encoding="utf-8", newline="") as f:
        f.write(q)

    # 3. LEDGER: correct the seconds-old own row in place, erratum named
    led = LEDGER.read_text(encoding="utf-8", errors="replace")
    led = sub_once(
        led,
        "band B2-495..497 claimed on fresh-bytes census B2-494); falsifier",
        "band B2-495..497 claimed on fresh-bytes census B2-494, overtaken by concurrent numbering 498..512 mid-close, briefs refiled highest+1 B2-513..B2-515 per the B2-167 law, erratum: this row corrected in place at close to name the true numbers); falsifier",
        "LEDGER claim clause",
    )
    led = sub_once(
        led,
        "wire-pull arm owed filed as B2-495; self-fed B2-495 B2-496 B2-497 UNCHECKED",
        "wire-pull arm owed filed as B2-513; self-fed B2-513 B2-514 B2-515 UNCHECKED",
        "LEDGER self-feed clause",
    )
    with LEDGER.open("w", encoding="utf-8", newline="") as f:
        f.write(led)

    # 4. receipt tail + AMENDMENT event for the new sha
    r = RECEIPT.read_text(encoding="utf-8", errors="replace")
    r = sub_once(
        r,
        "the wire-pull arm is filed forward as owed (self-feed B2-495). Closed 2026-09-26.",
        "the wire-pull arm is filed forward as owed (self-feed B2-513; the drafted band 495..497 was overtaken by concurrent self-feed numbering 498..512 mid-close, so the briefs refiled highest+1 as B2-513..B2-515 per the B2-167 lane-id claim law, and 495..497 stand as named holes). Closed 2026-09-26.",
        "receipt tail",
    )
    with RECEIPT.open("w", encoding="utf-8", newline="") as f:
        f.write(r)

    new_sha = hashlib.sha256(RECEIPT.read_bytes()).hexdigest().upper()
    seq = int(time.time() * 1e6)
    event = {
        "seq": str(seq),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "op": "amend",
        "file": "burn_wave_20260926/B2_469_dated_meters_20260926.md",
        "sha256": new_sha,
        "class": "AMENDMENT",
        "purpose": "B2-469 erratum: receipt tail renumber correction, drafted self-feed band 495..497 overtaken by concurrent numbering 498..512, briefs refiled B2-513..B2-515 per the B2-167 law; supersedes the register event sha for this file only, landing content unchanged",
        "writer": "zcode-b2-469-dated-meters",
    }
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(guard(json.dumps(event, ensure_ascii=False)) + "\n")
    print("corrections applied: board CLAIMED + landing note, LEDGER row in place, receipt tail; AMENDMENT event sha " + new_sha[:12])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
