"""B2-167 step 2: board landing on QUEUE.md (mtime-guarded anchored surgery,
the B2-358/B2-373 pattern). One write applies: the four later-claimant
renumbers with dated collision notes, the lane-id claim law paragraph in the
header block, the B2-167 row landing note plus earned flip, three self-feed
briefs UNCHECKED at the Open tail, and retirement of this lane's two CLAIM
lines. Re-reads fresh bytes on every attempt and refuses on any anchor that is
missing or non-unique. Everything appended passes the em-dash guard.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_167_queue_dedupe_20260926.md"
CENSUS = "watch/inbox/burn_wave_20260926/B2_167_census_results.json"
CLAIM_TS = "2026-09-26T19:06:46Z"

ROW_ID = re.compile(r"^-[ \t]+\[[ x]\] B2-(\d+)\b", re.M)

# (old id, unique row-start prefix identifying the LATER claimant to move)
MOVES = [
    (407, "- [ ] B2-407 Matched-copy identity audit:"),
    (408, "- [ ] B2-408 Reconcile the 314 recovered media into the caption ledger:"),
    (427, "- [ ] B2-427 File the LAW-12 clause verdict on or before 2026-10-10:"),
    (428, "- [ ] B2-428 Verify the B2-164 scenario-suite-at-pre-push landing"),
]
# unique row-start prefixes of the KEPT earlier claims (must exist, untouched)
KEPT = [
    "- [ ] B2-407 Census and pin the writer set of logs/seat_crashes.log:",
    "- [ ] B2-408 _log_seat_crash swallows write failures silently:",
    "- [ ] B2-427 Pin the append-only line contract of REGISTRY.jsonl:",
    "- [ ] B2-428 Automate the fixture-citation sunset:",
]

LAW = (
    "Lane-id claim law (B2-167, 2026-09-26): the shared-file claim law protects "
    "file bytes; this one protects NUMBERS, because two lanes drafting "
    "self-feeds from the same board read can file different briefs under one id "
    "and neither sees it until both land (the disease: 24 ids each claimed by "
    "two different briefs at the B2-255 sweep, four more doubled by evening, "
    "watch/inbox/burn_wave_20260926/B2_255_double_spend_20260926.md). Before a "
    "lane appends any brief row to Open (self-feed or refile), it first appends "
    "one claim line under Open with the exact shape `- CLAIM <lane-id> "
    "watch/inbox/burn_wave_20260926/QUEUE.md <YYYY-MM-DDTHH:MM:SSZ> (<reason>)` "
    "naming every id it is about to file, a contiguous band as `<first>..<last>`; "
    "only then does it append the rows. A concurrent lane drafting self-feeds "
    "re-reads QUEUE.md per the shared-file claim law, treats a foreign band as "
    "taken, and numbers past it (highest+1). Retirement is in place, never a "
    "delete: flip the leading CLAIM token to CLAIMED with `-> <receipt-path>` in "
    "the same breath as the landing receipt. A row filed without its claim line "
    "is a silent collision and takes the renumber treatment: the earlier "
    "claimant's row stays byte-untouched, the later claimant moves highest+1 "
    "with a dated collision note on the row (B2-255 sweep precedent). A checked "
    "row with no receipt stays the B2-238 disease: self-feed enters UNCHECKED "
    "and only the landing lane flips its own checkbox with the receipt pointer "
    "(watch/inbox/burn_wave_20260926/B2_238_checkbox_law_20260926.md). Related "
    "landed pieces: the B2-255 double-spend sweep (renumber precedent) and the "
    "B2-238 checkbox law (earned flips)."
)

NOTE_407 = (
    " (renumbered from B2-407 to B2-{n} by the B2-167 queue-dedupe lane "
    "2026-09-26: B2-407 was claimed by two different briefs, the earlier "
    "B2-373 self-feed kept untouched (LEDGER 18:02:01Z, its row sits above "
    "this one), this later B2-89 self-feed (LEDGER 18:04:32Z) moved "
    "highest+1 per the B2-167 law)"
)
NOTE_408 = (
    " (renumbered from B2-408 to B2-{n} by the B2-167 queue-dedupe lane "
    "2026-09-26: B2-408 was claimed by two different briefs, the earlier "
    "B2-373 self-feed kept untouched (LEDGER 18:02:01Z, its row sits above "
    "this one), this later B2-89 self-feed (LEDGER 18:04:32Z) moved "
    "highest+1 per the B2-167 law)"
)
NOTE_427 = (
    " (renumbered from B2-427 to B2-{n} by the B2-167 queue-dedupe lane "
    "2026-09-26: B2-427 was claimed by two different briefs, the earlier "
    "B2-162 self-feed kept untouched (byte-layout proof: its rows sit above "
    "the B2-94/B2-96/B2-99 CLAIMED lines of 18:31:20Z-18:33:30Z while this "
    "row sits below them; B2-162's receipt records highest brief row B2-423 "
    "at its apply time), this later B2-163 self-feed moved highest+1 per the "
    "B2-167 law)"
)
NOTE_428 = (
    " (renumbered from B2-428 to B2-{n} by the B2-167 queue-dedupe lane "
    "2026-09-26: B2-428 was claimed by two different briefs, the earlier "
    "B2-162 self-feed kept untouched (byte-layout proof: its rows sit above "
    "the B2-94/B2-96/B2-99 CLAIMED lines of 18:31:20Z-18:33:30Z while this "
    "row sits below them; B2-162's receipt records highest brief row B2-423 "
    "at its apply time), this later B2-163 self-feed moved highest+1 per the "
    "B2-167 law)"
)

BRIEFS = [
    (
        "Automate the queue double-claim census: the B2-167 dedupe ran "
        "B2_167_census.py by hand and found four post-sweep doubles "
        "(B2-407, B2-408, B2-427, B2-428, later claimants renumbered in the "
        "same landing) that no gate saw, so the census must bite on its own; "
        "promote the census into tools/queue_dupes_check.py (strict plus "
        "tolerant row-start ids, exit 1 on any id claimed by two or more "
        "briefs, warn on malformed row-start forms the strict regex misses) "
        "and ride it in the tools/refold_gate.py payload next to the "
        "restore-guard audit (the B2-343 payload pattern); falsifier: append "
        "a second Open row under an existing id and the fold gate payload "
        "stays green; pointers watch/inbox/burn_wave_20260926/B2_167_census.py, "
        "tools/refold_gate.py, watch/inbox/burn_wave_20260926/"
        "B2_343_restore_guard_20260926.md."
    ),
    (
        "Fold the CLAIM ghost and band-vs-row check into a board audit: the "
        "claim law declares an active CLAIM whose lane already has a receipt "
        "on disk a ghost (the B2-238 treatment) and B2-162 retired the "
        "long-stale B2-86 ghost by hand, the B2-167 census ran the ghost "
        "check once by hand (zero ghosts at 18:58Z, active claim lanes B2-102, "
        "B2-103, B2-104, B2-106, B2-107, B2-165 all receipt-less then), and "
        "nothing sweeps it again; add a --board mode to tools/restore_guard.py "
        "audit that censuses active CLAIM and CLAIMED lines per lane, flags an "
        "active CLAIM whose lane id matches a B2_<id>_*.md receipt in the wave "
        "dir, and flags a claimed band whose ids never landed as rows, so the "
        "daily patrol or the refold gate names ghosts; falsifier: land a "
        "receipt, leave its CLAIM line active, run the audit, nothing names "
        "it; pointers tools/restore_guard.py, watch/inbox/burn_wave_20260926/"
        "B2_167_census.py ghost_claims field, watch/inbox/burn_wave_20260926/"
        "B2_162_g1_tripwire_20260926.md Work done item 5."
    ),
    (
        "Normalize the malformed queue row starts: the Open section carries "
        "brief rows the strict census regex cannot see (the live form is a "
        "double space after the dash on the B2-369, B2-370 and B2-371 rows, "
        "present on the board at 18:58Z), so strict-id census tools silently "
        "undercount and the B2-167 census needed a second tolerant regex to "
        "catch them; either run one dated normalizer pass to the canonical "
        "checkbox shape with a receipt, or extract one shared tolerant row "
        "parser into tools/ and point every queue census consumer at it, plus "
        "a tripwire naming any row-start that deviates from the canonical "
        "shape; falsifier: a malformed row-start filed tomorrow changes the "
        "tolerant census but leaves every strict consumer blind with no "
        "surface naming it; pointers watch/inbox/burn_wave_20260926/"
        "B2_167_census.py STRICT_ROW vs TOLERANT_ROW, "
        "watch/inbox/burn_wave_20260926/QUEUE.md Open section."
    ),
]


def guard(text):
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in appended text")
    return text


def apply(text: str) -> str:
    for marker in (
        "- CLAIM B2-167 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS,
        "- CLAIM B2-470..B2-476 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS,
    ):
        if text.count(marker) != 1:
            raise SystemExit("own claim line not unique on fresh bytes: %s" % marker[:70])

    for prefix in KEPT:
        hits = [l for l in text.splitlines() if l.startswith(prefix)]
        if len(hits) != 1:
            raise SystemExit("kept row not unique (%d): %s" % (len(hits), prefix[:60]))

    top = max(int(m) for m in ROW_ID.findall(text))
    renum_start = top + 1
    feed_ids = [top + 5, top + 6, top + 7]

    # 1. renumbers: replace the id in the row-start prefix, append note at row end
    notes = [NOTE_407, NOTE_408, NOTE_427, NOTE_428]
    for i, (old, prefix) in enumerate(MOVES):
        new_id = renum_start + i
        old_prefix = "- [ ] B2-%d " % old
        hits = [l for l in text.splitlines() if l.startswith(prefix)]
        if len(hits) != 1:
            raise SystemExit("move row not unique (%d): %s" % (len(hits), prefix[:60]))
        line = hits[0]
        moved = old_prefix + line[len(prefix):] + guard(notes[i].format(n=new_id))
        text = text.replace(line, guard(moved), 1)

    # 2. header law paragraph before Dispensed
    if text.count("\n## Dispensed") != 1:
        raise SystemExit("Dispensed anchor not unique")
    text = text.replace("\n## Dispensed", "\n" + guard(LAW) + "\n\n## Dispensed", 1)

    # 3. B2-167 row landing note + earned flip (row found in either checkbox
    # state: a concurrent writer pre-checked it between the 19:06:46Z claim
    # and the first landing attempt, the B2-238 disease; this landing earns
    # the check, sequence named in the receipt)
    hits = [
        l for l in text.splitlines()
        if l.startswith("- [ ] B2-167 De-duplicate QUEUE B2 numbers:")
        or l.startswith("- [x] B2-167 De-duplicate QUEUE B2 numbers:")
    ]
    if len(hits) != 1:
        raise SystemExit("B2-167 row not unique (%d)" % len(hits))
    row = hits[0]
    pre_checked = row.startswith("- [x]")
    note = guard(
        " Landed 2026-09-26: final byte census (watch/inbox/burn_wave_20260926/"
        "B2_167_census.py, results B2_167_census_results.json, pre sha256 "
        "e02e5c050378e93567912d363f53b9fb30b0bae3d429098716b0e1ab403a8666) "
        "found four post-sweep doubles (B2-407, B2-408, B2-427, B2-428), each "
        "resolved by the standing renumber law, earlier claim kept untouched, "
        "later claimant moved highest+1 with a dated collision note: "
        "B2-407/B2-408 to the B2-89 self-feed (B2-373's 18:02:01Z self-feed "
        "kept, B2-89's 18:04:32Z moved) and B2-427/B2-428 to the B2-163 "
        "self-feed (B2-162's rows kept on byte-layout proof, B2-163's moved); "
        "the brief's own B2-92/B2-93 pair verified single-claimed, no "
        "renumber owed there; lane-id claim-row convention codified in this "
        "header block (the lane-id claim law) naming the B2-255 double-spend "
        "sweep and the B2-238 checkbox law as the related landed pieces; "
        "band B2-470..B2-476 pre-claimed before filing rows per that law at "
        "19:06:46Z and still invaded: B2-470..B2-472 rows from the B2-178 "
        "self-feed landed after the claim line, so actuals rebase past them "
        "per first-lander-keeps-bytes, renumbers land at "
        "B2-%d..B2-%d and self-feeds at B2-%d..B2-%d, disclosed here and in "
        "the receipt; receipt " % (
            renum_start, renum_start + 3, feed_ids[0], feed_ids[2]
        )
    ) + RECEIPT + guard(
        "; self-fed B2-%d, B2-%d, B2-%d UNCHECKED." % tuple(feed_ids)
    )
    if pre_checked:
        earned = guard(
            " (row found pre-checked [x] with no receipt between the "
            "19:06:46Z claim and this landing, the B2-238 disease; this "
            "landing earns the check)"
        )
        text = text.replace(row, row + earned + note, 1)
    else:
        text = text.replace(
            row, "- [x]" + row[len("- [ ]"):] + note, 1
        )

    # 4. self-feed briefs UNCHECKED at the Open tail
    tail = "".join(
        "\n- [ ] B2-%d %s" % (feed_ids[i], guard(b)) for i, b in enumerate(BRIEFS)
    )
    if not text.endswith("\n"):
        tail = "\n" + tail
    text = text + tail + "\n"

    # 5. retire both claim lines
    for marker in (
        "- CLAIM B2-167 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS,
        "- CLAIM B2-470..B2-476 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS,
    ):
        line = [l for l in text.splitlines() if l.startswith(marker)]
        if len(line) != 1:
            raise SystemExit("claim line lost mid-edit: %s" % marker[:70])
        retired = line[0].replace("- CLAIM ", "- CLAIMED ", 1) + " -> " + RECEIPT
        text = text.replace(line[0], guard(retired), 1)

    return text


def main() -> int:
    for attempt in range(8):
        mtime_before = BOARD.stat().st_mtime_ns
        text = BOARD.read_bytes().decode("utf-8")
        if "Lane-id claim law (B2-167, 2026-09-26)" in text:
            print("already applied by a prior run; nothing to do")
            return 0
        try:
            new_text = apply(text)
        except SystemExit as e:
            print("anchor failure: %s" % e)
            return 1
        time.sleep(0.2)
        if BOARD.stat().st_mtime_ns != mtime_before:
            print("attempt %d: board moved mid-edit, re-reading" % attempt)
            continue
        BOARD.write_bytes(new_text.encode("utf-8"))
        print(
            "board landing applied on attempt %d: 4 renumbers, header law, "
            "B2-167 flip, claims retired" % attempt
        )
        return 0
    print("FAILED: board too hot after 8 attempts; re-run this script")
    return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
