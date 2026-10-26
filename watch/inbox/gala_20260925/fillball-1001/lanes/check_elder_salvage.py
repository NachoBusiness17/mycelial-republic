"""Byte checks for the fill-elder-salvage lane (gala fillball-1001).

Verifies every claim the receipt watch/inbox/fillball/elder-salvage.md makes.
Run with the repo venv python. Output is appended to
watch/inbox/gala_20260925/fillball-1001/lanes/fill-elder-salvage.check.txt
(the file already carries the BEFORE ls -la of the 0-byte Sep 4 inbox).
"""
import json
import os
import sys

FAILURES = []


def check(name, ok, detail):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}: {detail}")
    if not ok:
        FAILURES.append(name)


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def count_sub(path, needle, encoding="utf-8"):
    return read_bytes(path).decode(encoding, errors="replace").count(needle)


REPO = "."
INBOX = "queue/lanes/elder/inbox.jsonl"
TRAIL = "queue/lanes/elder/trail.jsonl"
RECEIPT = "watch/inbox/fillball/elder-salvage.md"
CARD = ".agents/skills/elder-lens/SKILL.md"
LEDGER = "watch/inbox/SELF_STEAL_DEEP_20260918.md"
SURFACE = "queue/lanes/elder/surface.md"
SKILLS = "watch/inbox/ractor50/skills.md"
STORY = "watch/inbox/48h_synth/STORY.md"
REGISTER = "watch/inbox/gap_analysis_20261001/GAP_REGISTER.md"

print("=" * 72)
print("CHECK BLOCK: fill-elder-salvage (gala fillball-1001), run at", end=" ")
print(__import__("datetime").datetime.utcnow().isoformat() + "Z")
print("=" * 72)

# 1. The falsifier organ is live (was 0 bytes mtime Sep 4; see BEFORE block above).
st = os.stat(INBOX)
check("inbox-banked", st.st_size > 0, f"{INBOX} now {st.st_size} bytes, mtime {st.st_mtime}")

# 2. The banked row parses and carries lens + question + clock.
rows = [json.loads(line) for line in read_bytes(INBOX).decode("utf-8").splitlines() if line.strip()]
check("inbox-one-row", len(rows) == 1, f"{len(rows)} row(s) in {INBOX}")
row = rows[0] if rows else {}
check("row-kind", row.get("kind") == "lens-pointer", f"kind={row.get('kind')!r}")
check(
    "row-question-clock",
    "OBLIGED" in row.get("question", "") and "2026-10-09" in row.get("falsifier", ""),
    "question carries the cadence-answerability ask; falsifier carries the 10-09 clock",
)

# 3. Trail row honest and appended.
trail_lines = [l for l in read_bytes(TRAIL).decode("utf-8").splitlines() if l.strip()]
last = json.loads(trail_lines[-1])
check(
    "trail-lens-banked",
    last.get("event") == "LENS_BANKED" and last.get("actor") == "seat-salvage-fillball-1001",
    f"last trail row event={last.get('event')!r} actor={last.get('actor')!r}",
)

# 4. Receipt exists and carries lens + question + clocks.
rsz = os.path.getsize(RECEIPT)
check(
    "receipt-shape",
    rsz > 3000
    and count_sub(RECEIPT, "LENS, NOT CLAIM") >= 1
    and count_sub(RECEIPT, "THE ELDER'S QUESTION") >= 1
    and count_sub(RECEIPT, "2026-10-09T04:05:56Z") >= 1,
    f"{RECEIPT} {rsz} bytes; lens label + question + new clock present",
)

# 5. Card intake widened (salvage term 2).
card_txt = read_bytes(CARD).decode("utf-8")
check(
    "card-intake",
    "Intake:" in card_txt
    and "gala/window synthesis output" in card_txt
    and "watch/inbox/fillball/elder-salvage.md" in card_txt,
    "SKILL.md carries the widened intake step 0 naming gala synthesis outputs",
)

# 6. Question ledger row 10-01 filed.
check(
    "ledger-row",
    count_sub(LEDGER, "| 10-01 |") == 1 and count_sub(LEDGER, "2026-10-09T04:05Z") == 1,
    "SELF_STEAL_DEEP_20260918.md carries exactly one 10-01 question row with the clock",
)

# 7. Surface RECEIPT-003 appended.
check(
    "surface-receipt",
    count_sub(SURFACE, "RECEIPT-003") == 1
    and count_sub(SURFACE, "LENS BANKED, Salvage honored") == 1,
    "surface.md carries exactly one RECEIPT-003 salvage block",
)

# 8. No em/en dash in anything authored this lane (scoped to authored bytes,
#    since the card, surface, and ledger legitimately carry pre-existing dashes).
authored = {
    RECEIPT: read_bytes(RECEIPT).decode("utf-8"),
    "inbox-row": json.dumps(row, ensure_ascii=True),
    "SKILL.md-added-block": card_txt[
        card_txt.index("## Procedure") : card_txt.index("1. **Read the day's")
    ],
    "ledger-added-row": [
        l for l in read_bytes(LEDGER).decode("utf-8").splitlines() if l.startswith("| 10-01 |")
    ][0],
    "surface-added-block": read_bytes(SURFACE).decode("utf-8")[
        read_bytes(SURFACE).decode("utf-8").index("RECEIPT-003") :
    ],
}
for name, txt in authored.items():
    bad = [ch for ch in ("\u2014", "\u2013") if ch in txt]
    check("no-emdash:" + name, not bad, "clean" if not bad else f"found {bad!r}")

# 9. Quote byte-checks: every quote the receipt carries exists verbatim in its
#    named source (no-fabrication law). Two sources wrap the quote across a
#    line break (STORY.md:171-172, SKILL.md:37-38); those are checked as
#    per-line fragments, and the receipt documents the newline normalization.
quotes = [
    (STORY, "The renderer is the demo; the cadence layer is the asset"),
    (STORY, "Green, it turns out, is not a place; it is a"),
    (STORY, "moment you must re-earn and re-attribute daily."),
    (STORY, "instead of a one-time hand heal"),
    (STORY, "things without cadence die"),
    (STORY, "has never fired in production"),
    (SURFACE, "A named instrument nobody is obliged to answer is a grimoire, not a witness."),
    (SKILLS, "resurrect by its own falsifier - bank ONE lens into"),
    (SKILLS, "If no lens lands by the falsifier clock (~10-02), the kill stands and"),
    (SKILLS, "a lens is dead if no organ acts on its question within one week"),
    (CARD, "a lens is dead if no organ acts on its question within one"),
    (CARD, "the question ledger's answer-rate is the lens's own meter."),
    (REGISTER, "elder-lens salvage lens unbanked while the card's own falsifier clock"),
]
for path, needle in quotes:
    n = count_sub(path, needle)
    check("quote-exact:" + os.path.basename(path), n >= 1, f"{n} exact hit(s) for {needle[:52]!r}")

# 10. The falsifier organ received its drop before the card's shelf deadline terms
#     could execute: mtime day vs the ~10-02 window (documented, not asserted).
import datetime
mt = datetime.datetime.utcfromtimestamp(st.st_mtime)
check(
    "clock-honored",
    (mt.year, mt.month, mt.day) <= (2026, 10, 2),
    f"inbox mtime {mt.isoformat()}Z is inside the card's (~10-02) window",
)

print("-" * 72)
print(f"TOTAL: {len(FAILURES)} failure(s)" + ("" if FAILURES else "; all checks PASS"))
sys.exit(1 if FAILURES else 0)
