"""B2-378 board landing: checkbox flip earns its receipt, claims retire,
self-feeds append (2026-09-26).

Targeted surgery on the hot QUEUE.md with an mtime guard (B2-358 pattern).
Self-feed numbers are computed at apply time as highest+1..+3 because
concurrent lanes take numbers every minute (B2-167 renumber law); the landing
note and the brief lines are built from the same computed numbers so the
board never cites a number it does not carry. Refuses to double-apply.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_378_fold_outcome_20260926.md"

CLAIMS_OLD_NEW = [
    (
        "- CLAIM B2-378 mag/icon_drop.py 2026-09-26T17:58:30Z (B2-378 fold outcome honesty: _fold_training passes the row status through to skill_ledger outcome, ok only when status dropped, else the status string; drop/drop_shortcut behavior untouched; re-read bytes before your edit per the claim law)",
        "- CLAIMED B2-378 mag/icon_drop.py 2026-09-26T17:58:30Z (B2-378 fold outcome honesty: _fold_training passes the row status through to skill_ledger outcome, ok only when status dropped, else the status string; drop/drop_shortcut behavior untouched; re-read bytes before your edit per the claim law; rebased mid-lane on the concurrent B2-377 escaping landing, _fold_training region untouched, rebase named in the receipt) -> " + RECEIPT,
    ),
    (
        "- CLAIM B2-378 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T17:58:30Z (lane's own board: claim lines, B2-378 landing note, self-feed briefs; foreign CLAIMs B2-373 honored, anchored edits on freshly-read bytes, no whole-file rewrite)",
        "- CLAIMED B2-378 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T17:58:30Z (lane's own board: claim lines, B2-378 landing note, self-feed briefs; foreign CLAIMs B2-373 honored, anchored edits on freshly-read bytes, no whole-file rewrite) -> " + RECEIPT,
    ),
]

CHECK_OLD = "- [ ] B2-378 Pass the honest outcome through _fold_training:"
CHECK_NEW = "- [x] B2-378 Pass the honest outcome through _fold_training:"
ROW_TAIL_OLD = (
    'record outcome "ok" in skill_ledger; pointers mag/icon_drop.py'
    " _fold_training, watch/inbox/burn_wave_20260926/B2_354_icon_honesty_20260926.md."
)

BRIEF_TEMPLATE = """- [ ] B2-{n1} skill_ledger outcome vocabulary is unowned: (self-fed by B2-378) record_decision documents outcome as decision-only or ok/fail (mag/skill_ledger.py record_decision comment) while best_moves counts outcome == "ok" as the win and everything else only rides in the denominator, and B2-378 made icon_drop write status strings ("failed", "skipped_no_powershell", "unknown") into outcome, so the field is an open vocabulary with exactly one special value and no registry: any consumer that must treat a skip differently from a failure (retry logic, operator dashboards) has no surface and must hardcode icon_drop's private strings; register the outcome vocabulary (or split a status field out) next to the events key registry pattern; falsifier: a consumer that must treat "skipped_no_powershell" differently from "failed" cannot do so without importing icon_drop's literals; pointers mag/skill_ledger.py record_decision and best_moves, mag/icon_drop.py _fold_training, {receipt}.
- [ ] B2-{n2} _fold_training swallows fold failures silently: (self-fed by B2-378) the whole fold body sits in a bare except-pass (mag/icon_drop.py _fold_training), so a broken fold (skill_ledger append error, training_events schema drift, mag.skill_ledger import failure) leaves the icon drop landed but the case-law edge missing with no signal and the operator_behavior fold undercounts silently; add a named bounded failure surface (a gap row, a log line, or a fold_status field on the caller-visible row), never a raised error that breaks the drop path; falsifier: force record_decision to raise inside a sandboxed fold and no surface anywhere names the missing edge; pointers mag/icon_drop.py _fold_training, mag/skill_ledger.py _append, {receipt}.
- [ ] B2-{n3} Port the B2-378 fold-outcome arms into a repo pin: (self-fed by B2-378) tests/ carries no icon_drop module at all (grep 2026-09-26), so the outcome pass-through is pinned only by the throwaway probe and the next edit to _fold_training or a record_decision signature change can silently regress the fold to a constant with no red run; port the four arms (dropped->ok, failed->failed, skipped_no_powershell->skipped_no_powershell, statusless->unknown) into a pytest module sandboxing the four write paths (tmp_path plus monkeypatch on icon_drop.LEDGER, icon_drop.desktop_folder, skill_ledger.DECISIONS_PATH, training_events.EVENTS_PATH, the probe's exact pattern); falsifier: revert _fold_training's outcome to a hardcoded "ok" and the new module goes red on the three non-dropped arms; pointers mag/icon_drop.py _fold_training, watch/inbox/burn_wave_20260926/B2_378_falsifier_probe.py, {receipt}."""


def apply(text: str) -> str:
    numbers = [int(m) for m in re.findall(r"B2-(\d+)", text)]
    top = max(numbers)
    n1, n2, n3 = top + 1, top + 2, top + 3
    landing = (
        " Landed 2026-09-26: _fold_training (mag/icon_drop.py) now reads the row"
        ' status and records outcome "ok" only when the status is "dropped",'
        ' otherwise the status string verbatim ("failed",'
        ' "skipped_no_powershell", "unknown" for a statusless row), and the'
        " detail line carries the status instead of asserting a drop that did"
        ' not happen (the hardcoded outcome "ok" plus the "dropped icon ..."'
        " detail folded B2-354's honest failed and skipped rows as"
        ' operator_behavior wins; skill_ledger best_moves counts outcome =='
        ' "ok"); falsifier executed live: '
        "watch/inbox/burn_wave_20260926/B2_378_falsifier_probe.py ran the real"
        " fold end to end sandboxed to a temp dir with the real powershell"
        " subprocess both arms (disclosures in the probe docstring): arm A"
        " happy drop row status dropped with decision outcome ok, arm B forced"
        " a real WScript.Shell Save failure (desktop surface patched to a"
        " regular file inside the sandbox) row status failed with decision"
        " outcome failed, arm C skipped_no_powershell row outcome"
        " skipped_no_powershell, arm D statusless row outcome unknown, and the"
        " temp decisions ledger bytes carry"
        " ok/failed/skipped_no_powershell/unknown in order with"
        " falsifier_holds true in B2_378_falsifier_probe_results.json; the"
        " failure force switched mid-lane from the B2-354 single-quote"
        " injection to a filesystem-level block because the concurrent B2-377"
        " escaping landing (name filter plus _ps_quote on every literal, in"
        " mag/icon_drop.py during this lane's 17:58-18:01Z window) turned that"
        " injection into a happy path by design; rebase named per the claim"
        " law: this lane's _fold_training region was untouched by B2-377 and"
        " the edit applied by mtime-guarded surgery on the post-B2-377 bytes"
        " (watch/inbox/burn_wave_20260926/B2_378_fold_edit.py); py_compile OK;"
        " ratchet check --changed PASS NEW=0 scope=40; em-dash count 0 on"
        " added lines; real ledgers byte-untouched (zero b2_378 rows in"
        " memory/icons/ledger.jsonl, memory/improve/skill_ledger.jsonl,"
        " memory/training/events.jsonl); receipt " + RECEIPT + ";"
        f" self-fed B2-{n1}, B2-{n2}, B2-{n3} unchecked."
    )
    for old, new in CLAIMS_OLD_NEW:
        if text.count(old) != 1:
            raise SystemExit(f"claim anchor not unique (count={text.count(old)}): {old[:80]}")
        text = text.replace(old, new)
    if text.count(ROW_TAIL_OLD) != 1:
        raise SystemExit(f"row tail anchor not unique (count={text.count(ROW_TAIL_OLD)})")
    if RECEIPT + "; self-fed B2-" in text:
        raise SystemExit("landing note already present; refusing to double-apply")
    # The row may arrive as [ ] (this lane flips it) or already [x] flipped by
    # a concurrent lane with no receipt on disk (found 18:03Z mid-verification,
    # unearned at flip time); either way the landing note below earns the
    # check in place, so only flip when the unchecked form is present.
    if text.count(CHECK_OLD) == 1:
        text = text.replace(CHECK_OLD, CHECK_NEW, 1)
    elif text.count(CHECK_NEW) != 1:
        raise SystemExit("B2-378 row checkbox not found in either form")
    idx = text.find(ROW_TAIL_OLD)
    text = text[: idx + len(ROW_TAIL_OLD)] + landing + text[idx + len(ROW_TAIL_OLD):]
    briefs = "\n" + BRIEF_TEMPLATE.format(n1=n1, n2=n2, n3=n3, receipt=RECEIPT) + "\n"
    if not text.endswith("\n"):
        text += "\n"
    text += briefs
    return text


def main() -> int:
    for attempt in range(8):
        mtime_before = BOARD.stat().st_mtime_ns
        text = BOARD.read_text(encoding="utf-8")
        if RECEIPT + "; self-fed B2-" in text:
            print("already applied by a prior run; nothing to do")
            return 0
        try:
            new_text = apply(text)
        except SystemExit as exc:
            print(f"attempt {attempt}: {exc}; re-reading")
            time.sleep(0.5)
            continue
        time.sleep(0.2)
        if BOARD.stat().st_mtime_ns != mtime_before:
            print(f"attempt {attempt}: board moved mid-edit, re-reading")
            continue
        BOARD.write_text(new_text, encoding="utf-8", newline="")
        print(f"B2-378 board landing applied on attempt {attempt}: checkbox earned, claims retired, self-feeds appended")
        return 0
    print("FAILED: board too hot after 8 attempts; re-run this script")
    return 1


if __name__ == "__main__":
    sys.exit(main())
