# B2-469 board fix (2026-09-26): the first close script printed "claims retired,
# row earned" but never wrote the modified board bytes (the q edits were
# discarded; only the brief append, LEDGER row, and event appends landed).
# This defect is named here and in the receipt erratum. Trust bytes, not prints.
# Now, in ONE read-modify-write of QUEUE.md: retire both CLAIM lines (with the
# band-move note), append the landing note with the true brief numbers.
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_469_dated_meters_20260926.md"
CLAIM_TS = "2026-09-26T19:20:17Z"


def guard(text: str) -> str:
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in board fix text")
    return text


def sub_once(text: str, old: str, new: str, what: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one occurrence of {what}, found {text.count(old)}")
    return text.replace(old, guard(new), 1)


def main() -> None:
    q = QUEUE.read_text(encoding="utf-8", errors="replace")

    # 1. retire the ps1 shared-file claim
    ps1_prefix = "- CLAIM B2-469 scripts/census_patrol_daily.ps1 " + CLAIM_TS
    hit = [ln for ln in q.splitlines() if ln.startswith(ps1_prefix)]
    if len(hit) != 1:
        raise SystemExit(f"ps1 CLAIM line not found or doubled: {len(hit)}")
    q = q.replace(hit[0], hit[0].replace("- CLAIM ", "- CLAIMED ", 1) + " -> " + RECEIPT, 1)

    # 2. retire the board claim with the band-move note
    board_prefix = "- CLAIM B2-469 watch/inbox/burn_wave_20260926/QUEUE.md " + CLAIM_TS
    hit = [ln for ln in q.splitlines() if ln.startswith(board_prefix)]
    if len(hit) != 1:
        raise SystemExit(f"board CLAIM line not found or doubled: {len(hit)}")
    retired = hit[0].replace("- CLAIM ", "- CLAIMED ", 1)
    retired += ("; band overtaken: concurrent self-feeds landed B2-498..B2-512 while these "
                "rows were pending, 495..497 left unfiled, briefs refiled highest+1 "
                "B2-513..B2-515 per the B2-167 lane-id claim law")
    retired += " -> " + RECEIPT
    q = q.replace(hit[0], guard(retired), 1)

    # 3. earn the pre-checked B2-469 row: append the landing note
    row_prefix = "- [x] B2-469 Wire dated meters"
    hit = [ln for ln in q.splitlines() if ln.startswith(row_prefix)]
    if len(hit) != 1:
        raise SystemExit(f"expected exactly one B2-469 row, found {len(hit)}")
    if hit[0].rstrip().endswith("UNCHECKED."):
        raise SystemExit("landing note already present; rebase instead of double-appending")
    landing = guard(
        " Landed 2026-09-26 (row sat pre-checked [x] with no receipt, the B2-238 "
        "disease; this landing earns the check): new organ tools/meter_patrol.py "
        "(314 lines, under the 400-line bar) appends one dated row per "
        "institutional-cluster meter class (rubric items 1-4, boundaries frozen "
        "from the pre-registered cards, both card hashes byte-identical to the "
        "B2-166 pins A76590AC../156CEF8F..) to watch/inbox/DATED_METERS.jsonl, "
        "state RECEIPT with candidate pointers or explicit NOBS, schema "
        "dated_meter_v1, boundary-true matching (case-sensitive EBS/MOEX, "
        "word-bounded phrases, website/ebs substring disease regression-tested), "
        "idempotent per day, gap days named and never backfilled (no fabrication), "
        "corrupt ledger fails closed exit 2; rides the existing "
        "MagCensusPatrolDaily cron body as a second step "
        "(scripts/census_patrol_daily.ps1, own GAP/cannot-verify alert path to "
        "memory/attention.md, worst-code-wins exit, PS parse clean); first live "
        "run 19:30:22Z landed 4 rows dated 2026-09-26 (sha256 "
        "80a6195f44c82378b43753cb2e8ac37ae13ec5e5b913a56e3b59853845d70dc9, all "
        "RECEIPT candidates 14/7/2/8, candidates explicitly never HIT verdicts); "
        "census tripwire untouched (sha FFE096BE.. pinned as zero-touch proof, the "
        "organ is a sibling module not an edit); 54 passed targeted (6 new tests "
        "+ 48 census patrol), self-test 7 check groups, ratchet NEW=0, em-dash 0; "
        "close defect caught and fixed same lane: the first close script printed "
        "claims-retired but never wrote the board bytes, this landing note and "
        "both CLAIMED retires are the repaired write (trust bytes, not prints); "
        "falsifier operationalized: a post-2026-09-26 scoring citing \"no "
        "receipt\" for items 1-4 without naming the DATED_METERS state for the "
        "window dates voids itself; wire-pull arm filed forward as B2-513; "
        f"receipt {RECEIPT}; self-fed B2-513 B2-514 B2-515 UNCHECKED (drafted band "
        "495..497 overtaken by concurrent numbering 498..512 mid-close, refiled "
        "highest+1 per the B2-167 law)."
    )
    q = q.replace(hit[0], hit[0] + landing, 1)

    with QUEUE.open("w", encoding="utf-8", newline="") as f:
        f.write(q)
    print("board fixed: 2 claims CLAIMED with receipt pointer, B2-469 row earned "
          "with landing note (true numbers B2-513..B2-515)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
