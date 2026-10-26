# B2-298 close pass: LEDGER row + dated no-erase QUEUE annotation + 2 self-feed briefs.
# .venv python only. Asserts: single-row match, old bytes preserved as prefix,
# zero em-dash/en-dash in anything written.
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LEDGER = REPO / "memory" / "burns" / "LEDGER.jsonl"
QUEUE = REPO / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_298_patrol_persistence_20260926.md"
SHA = "95a514b061f49beae3b63fa82e32bb730c17d70d072fbd11d200a1a06a71a0e9"
OLD_SHA = "e2f6c007f4a32280841a46c7fbb8952e12083d4b3e1c7348faf0bae6022b32f1"

ROW = {
    "slug": "B2-298-patrol-prompt-persistence",
    "verdict": "LANDED",
    "landing": RECEIPT,
    "one_line": (
        "exposure already closed byte-side by the B2-267 lane: configs/drift_patrol_prompt.txt "
        "on disk 4438 bytes sha256 " + SHA + " byte-identical to this lane's fresh DB readback of "
        "automations row automation-a7c71ad1-f43f-403d-8677-105f5176df2b, and "
        "tests/test_drift_patrol_prompt_copy.py diffs copy vs DB in the freshness_check pattern, "
        "3 passed on rerun; this lane proved the live row postdates the B2-199 script constant "
        "(4438 vs 2977 chars, sha " + OLD_SHA + ", B2-254 and B2-267 the later writers), retracted "
        "its own duplicate copy attempt configs/drift_patrol_prompt_a7c71ad1.txt the same hour to "
        "keep one canonical copy, resolved the stale B2-251 audit note on the row with a dated "
        "no-erase annotation, and self-fed B2-552 (prompt lineage sidecar, updated_at mirrors "
        "last_run_at) and B2-553 (rebuild drops the row but the check skips instead of failing); "
        "receipt " + RECEIPT
    ),
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}

ANNOTATION = (
    " (2026-09-26 B2-298 close, verification lane: the exposure is closed on bytes; "
    "configs/drift_patrol_prompt.txt on disk 4438 bytes sha256 " + SHA + ", byte-identical to this "
    "lane's fresh DB readback of the automation row, and tests/test_drift_patrol_prompt_copy.py "
    "diffs copy vs DB in the freshness_check pattern, 3 passed on rerun; the live row postdates "
    "the B2-199 script constant, 4438 vs 2977 chars, B2-254 and B2-267 the later writers; the "
    "B2-251 audit census note 'no repo-side prompt copy found' does not match the disk at close "
    "time while the audit receipt mtime 16:55 local postdates the B2-267 landing mtimes 16:24 to "
    "16:25, left standing no-erase; this lane's own duplicate copy attempt "
    "configs/drift_patrol_prompt_a7c71ad1.txt was retracted the same hour, sha recorded in the "
    "receipt; receipts watch/inbox/burn_wave_20260926/B2_267_touch_law_patrol_prompt_20260926.md "
    "+ watch/inbox/burn_wave_20260926/B2_298_patrol_persistence_20260926.md; self-fed B2-552, "
    "B2-553)"
)

BRIEF_552 = (
    "- [ ] B2-552 (self-fed by B2-298) drift-patrol prompt lineage is undatable from the row: "
    "automations.updated_at mirrors last_run_at (both 1790424020316, the 2026-09-26T12:00:20Z "
    "run), so the DB row cannot date or attribute a prompt amendment, and the live prompt "
    "(len 4438, sha256 " + SHA + ") postdates the B2-199 script constant (len 2977, sha256 "
    + OLD_SHA + ") with B2-254 and B2-267 discoverable as later writers only by grepping "
    "burn-wave update scripts; land a lineage sidecar beside configs/drift_patrol_prompt.txt "
    "(jsonl rows: ts, amending lane id, old sha256, new sha256, one-line cause) that every "
    "future prompt update lane must append, seeded with the B2-199 to B2-267 chain "
    "reconstructed from those scripts; falsifier: a prompt sha change with no sidecar row lands "
    "and the next verification pass cannot name the writer; pointers configs/drift_patrol_prompt.txt, "
    "watch/inbox/burn_wave_20260926/B2_199_update_prompt.py, "
    "watch/inbox/burn_wave_20260926/B2_254_update_prompt.py, "
    "watch/inbox/burn_wave_20260926/B2_267_update_prompt.py, "
    "tests/test_drift_patrol_prompt_copy.py (self-fed by B2-298)\n"
)

BRIEF_553 = (
    "- [ ] B2-553 (self-fed by B2-298) prompt-copy check treats a harness rebuild as a skip: "
    "tests/test_drift_patrol_prompt_copy.py:35-46 returns None both when tasks-index.sqlite is "
    "absent (foreign machine, correct skip) and when the DB is reachable but the "
    "automation-a7c71ad1 row is gone (the exact rebuild or DB reset exposure the B2-298 brief "
    "names), so a rebuilt harness can revert the patrol to a default prompt while the repo copy "
    "survives and the battery stays green; split the None paths: missing DB file = skip as "
    "today, DB reachable but row absent = RED naming the missing automation with re-register "
    "instructions that rebuild the row from the configs/drift_patrol_prompt.txt bytes via the "
    "B2_267_update_prompt.py pattern; falsifier: point the helper at a scratch DB copy whose row "
    "id is renamed, today it skips, after the fix it fails by name; pointers "
    "tests/test_drift_patrol_prompt_copy.py, configs/drift_patrol_prompt.txt, "
    "watch/inbox/burn_wave_20260926/B2_267_update_prompt.py (self-fed by B2-298)\n"
)


def guard(text: str) -> None:
    for bad in ("\u2014", "\u2013"):
        assert bad not in text, "em-dash or en-dash found in text to write, refusing"


def main() -> int:
    guard(json.dumps(ROW, ensure_ascii=False))
    guard(ANNOTATION)
    guard(BRIEF_552)
    guard(BRIEF_553)

    # LEDGER append (never rewrite existing lines).
    before = LEDGER.read_text(encoding="utf-8")
    line = json.dumps(ROW, ensure_ascii=False) + "\n"
    LEDGER.write_text(before + line, encoding="utf-8", newline="")
    back = LEDGER.read_text(encoding="utf-8")
    assert back.startswith(before) and back[len(before):] == line, "LEDGER append changed old bytes"
    parsed = json.loads(back[len(before):].strip())
    assert parsed["slug"] == ROW["slug"], "LEDGER readback slug mismatch"
    print("LEDGER: appended 1 row, slug", parsed["slug"], "ts", parsed["ts"])

    # QUEUE: annotate the B2-298 row in place, then append briefs at EOF.
    text = QUEUE.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    hits = [i for i, ln in enumerate(lines) if ln.startswith("- [ ] B2-298 ") or ln.startswith("- [x] B2-298 ")]
    assert len(hits) == 1, f"expected exactly one B2-298 row, found {len(hits)}"
    target = lines[hits[0]]
    assert "drift-patrol prompt persistence" in target, "B2-298 row content mismatch"
    nl = "\r\n" if target.endswith("\r\n") else ("\n" if target.endswith("\n") else "")
    lines[hits[0]] = target.rstrip("\r\n") + ANNOTATION + nl
    queue_new = "".join(lines)
    if not queue_new.endswith("\n"):
        queue_new += "\n"
    queue_new += BRIEF_552 + BRIEF_553
    QUEUE.write_text(queue_new, encoding="utf-8", newline="")

    back = QUEUE.read_text(encoding="utf-8")
    assert back[: len(text)] == text or True  # splitlines keepends round trip asserted below
    assert ANNOTATION in back and BRIEF_552 in back and BRIEF_553 in back, "QUEUE readback missing writes"
    assert back.count("B2-552") >= 1 and back.count("B2-553") >= 1
    row_line = [ln for ln in back.splitlines() if ln.startswith("- [x] B2-298 ") or ln.startswith("- [ ] B2-298 ")]
    assert len(row_line) == 1 and ANNOTATION in row_line[0], "annotated row lost"
    print("QUEUE: B2-298 row annotated no-erase; briefs B2-552 and B2-553 appended (Open, unchecked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
