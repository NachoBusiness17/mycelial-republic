#!/usr/bin/env python3
"""battery_rerun.py - frozen method-card battery, reusable regression harness.

Spec: watch/inbox/method_card_exp/RERUN_PREREG_20260926.md (the scoring
contract, marked non-editable). Its Section 5 graduates the battery to a
reusable regression harness once the premise survives (t53 run: 12/12 MATCH,
premise SURVIVES). This file is that harness, built by gala afterparty gopher
t71 on 2026-09-26.

What it wraps, per the t71 lane item:
- the STEP 1 seal gate: spine re-hash against FREEZE_SEAL.json, heldout hash
  pin against the prereg Section 1 byte-blind baselines, and spine shape
  drift (Section 4 abort condition 3);
- refusal semantics: any gate failure prints the failing lines and exits 2,
  writes no score-out, and reads no answer or ground-truth content
  (prereg Section 0: no scoring on a mismatched seal, no waiver path);
- the scoring invocation: prints the score outline for a human/agent scorer
  and scaffolds the score artifact. It NEVER opens GROUND_TRUTH_HELDOUT.md
  content unless --score is passed (score-phase seat). Hashing a heldout file
  stays byte-blind inside the gate, exactly as the prereg sealed it.

Exit codes: 0 gate passed; 2 gate refused (SEAL MISMATCH / HELDOUT DRIFT /
SHAPE DRIFT); 1 usage or IO problem.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
METHOD_CARD_DIR = ESTATE_ROOT / "watch" / "inbox" / "method_card_exp"
DEFAULT_SEAL = METHOD_CARD_DIR / "FREEZE_SEAL.json"
DEFAULT_BATTERY = METHOD_CARD_DIR / "BATTERY_HELDOUT.md"
DEFAULT_GROUND_TRUTH = METHOD_CARD_DIR / "GROUND_TRUTH_HELDOUT.md"

# Heldout integrity baseline: prereg Section 1, byte-blind sha256. The pinned
# files are never opened by this module in default mode; only bytes are hashed.
REAL_PINS = {
    "battery_sha256": "98a364293ec20aa3d05e43e569d316be8f1baff2dd99afe07b1c3477bd5ee82c",
    "ground_truth_sha256": "81aa08447f3d3ec31d5a78987adc393ec30c0730a908fcfc445ca7f4c9e46a7d",
}

# Spine as sealed in FREEZE_SEAL.json (paths relative to estate root),
# prereg STEP 1 table.
SPINE = (
    ("index_sha256", "dashboard/data/ESTATE_INDEX.jsonl"),
    ("last_run_sha256", "dashboard/static/index_data/last_run.json"),
    ("rollup_sha256", "dashboard/static/index_data/rollup.json"),
)

SCALE = (
    "Scoring scale (BATTERY.md): MATCH = fact + correct path/value; "
    "PARTIAL = right shape, wrong detail; MISS."
)

EXCLUSION = (
    "Scorer exclusion (prereg Section 3): a seat that has ever read "
    "GROUND_TRUTH_HELDOUT.md or any battery answers before its own scoring "
    "phase is EXCLUDED. Answer seat and score seat must be different sessions."
)

# Question marker scan: markdown heading, bullet, or bare Qn with optional
# trailing punctuation. Used only to lay out the scaffold; it never grades.
Q_MARKER = re.compile(r"^\s*(?:#{1,6}\s+|[-*]\s+)?\**Q(\d+)\**\s*[\.\):]?", re.MULTILINE)

EXIT_OK = 0
EXIT_IO = 1
EXIT_REFUSED = 2


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def count_newlines(path: Path) -> int:
    """wc -l semantics: number of newline bytes."""
    total = 0
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            total += chunk.count(b"\n")
    return total


def run_gate(
    seal_path: Path,
    estate_root: Path,
    battery_path: Path,
    ground_truth_path: Path,
    pins: dict,
) -> tuple[list[str], list[str]]:
    """Prereg STEP 1 + Section 4 condition 3. Returns (failures, gate_lines).

    gate_lines is the seal-status evidence block for the score scaffold and is
    only meaningful when failures is empty.
    """
    failures: list[str] = []
    gate_lines: list[str] = []
    if not seal_path.is_file():
        return [f"SEAL MISMATCH seal file missing: {seal_path}"], []
    try:
        seal = json.loads(seal_path.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"SEAL MISMATCH seal file unreadable as JSON: {e}"], []

    for key, rel in SPINE:
        p = estate_root / rel
        if not p.is_file():
            failures.append(f"SEAL MISMATCH {rel}: missing")
            continue
        got = sha256_file(p)
        want = str(seal.get(key, ""))
        if got != want:
            failures.append(f"SEAL MISMATCH {rel}: {got[:12]} != {want[:12]}")
        else:
            note = ""
            if key == "index_sha256":
                size = p.stat().st_size
                want_size = seal.get("index_bytes")
                want_rows = seal.get("index_rows")
                size_ok = want_size is None or size == want_size
                rows = count_newlines(p)
                rows_ok = want_rows is None or rows == want_rows
                if not size_ok:
                    failures.append(f"SHAPE DRIFT {rel}: {size} bytes != {want_size}")
                if not rows_ok:
                    failures.append(f"SHAPE DRIFT {rel}: {rows} rows != {want_rows}")
                if size_ok and rows_ok:
                    note = f" ({rows} rows, {size} bytes)"
            if not note and not any(f.startswith(("SEAL MISMATCH", "SHAPE DRIFT")) for f in failures):
                note = " OK"
            gate_lines.append(f"spine {rel} sha256 {got[:12]}{note}")

    for label, path, key in (
        ("BATTERY_HELDOUT.md", battery_path, "battery_sha256"),
        ("GROUND_TRUTH_HELDOUT.md", ground_truth_path, "ground_truth_sha256"),
    ):
        if not path.is_file():
            failures.append(f"HELDOUT DRIFT {label}: missing at {path}")
            continue
        got = sha256_file(path)
        if got != str(pins.get(key, "")):
            failures.append(f"HELDOUT DRIFT {label}: {got[:12]} != pin drift")
        else:
            gate_lines.append(f"heldout {label} pin {got[:12]} OK (byte-blind)")
    return failures, gate_lines


def split_sections(text: str) -> dict[int, str]:
    """Split text into Qn sections by marker scan. Later duplicates win."""
    marks = [(int(m.group(1)), m.start()) for m in Q_MARKER.finditer(text)]
    out: dict[int, str] = {}
    for i, (q, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        out[q] = text[start:end].strip()
    return out


def build_outline(
    answers_text: str,
    gt_text: str | None,
    gate_lines: list[str],
    answers_path: Path,
    ground_truth_path: Path,
) -> str:
    answers = split_sections(answers_text)
    truth = split_sections(gt_text) if gt_text is not None else {}
    lines: list[str] = []
    lines.append("# RERUN SCORE SCAFFOLD - method-card frozen battery")
    lines.append(f"generated: {datetime.now().astimezone().isoformat(timespec='seconds')} by tools/battery_rerun.py")
    lines.append("spec: watch/inbox/method_card_exp/RERUN_PREREG_20260926.md Section 5 harness")
    lines.append(f"answers artifact: {answers_path}")
    if gt_text is None:
        lines.append(f"ground truth: NOT OPENED by this tool (scorer opens {ground_truth_path} in the score phase)")
    else:
        lines.append(f"ground truth: opened for pairing ({ground_truth_path}), score-phase seat only")
    lines.append(SCALE)
    lines.append(EXCLUSION)
    lines.append(
        "Per prereg STEP 3: grade each row, re-verify every cited path/value "
        "against the sealed spine, then file RERUN_SCORE_<YYYYMMDD>.md with "
        "per-question verdicts, the tally, and seal status at score time."
    )
    lines.append("")
    lines.append("## seal status at scaffold time")
    lines.extend(gate_lines if gate_lines else ["(gate lines unavailable)"])
    lines.append("")
    lines.append("## rows to grade")
    if not answers:
        lines.append("(no Qn rows detected by the marker scan; grade manually from the answers artifact)")
    unpaired_truth: list[int] = []
    for q in sorted(answers):
        lines.append(f"### Q{q}")
        lines.append("VERDICT (MATCH/PARTIAL/MISS): ")
        lines.append("ANSWER:")
        lines.append(answers[q])
        if gt_text is None:
            lines.append("GROUND TRUTH: (not opened by tool; scorer pairs it in the score phase)")
        elif q in truth:
            lines.append("GROUND TRUTH:")
            lines.append(truth[q])
        else:
            lines.append(f"GROUND TRUTH: (no Q{q} section found by marker scan; grade manually)")
        lines.append("")
    if truth:
        unpaired_truth = sorted(q for q in truth if q not in answers)
    lines.append("## unpaired ground-truth sections (informational)")
    lines.append(", ".join(f"Q{q}" for q in unpaired_truth) if unpaired_truth else "(none)")
    lines.append("")
    lines.append("## tally")
    lines.append(f"MATCH= PARTIAL= MISS= of {len(answers)} rows")
    lines.append("")
    lines.append("## falsifier reminder (prereg Section 5)")
    lines.append(
        "MATCH <= 4 of 12 kills the premise; MATCH >= 8 with verifying citations "
        "confirms the card as a transferable skill unit; 5 to 7 is a graded finding."
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Seal-gated rerun scaffold for the frozen method-card battery "
        "(spec: watch/inbox/method_card_exp/RERUN_PREREG_20260926.md)."
    )
    ap.add_argument("--answers", required=True, type=Path, help="answers artifact (STEP 2 output)")
    ap.add_argument("--score-out", required=True, type=Path, help="path to write the score scaffold")
    ap.add_argument(
        "--score", action="store_true",
        help="score phase: also read GROUND_TRUTH and emit side-by-side pairs; "
        "default mode never opens ground-truth content",
    )
    ap.add_argument("--seal", type=Path, default=DEFAULT_SEAL)
    ap.add_argument("--estate-root", type=Path, default=ESTATE_ROOT)
    ap.add_argument("--battery", type=Path, default=DEFAULT_BATTERY)
    ap.add_argument("--ground-truth", type=Path, default=DEFAULT_GROUND_TRUTH)
    ap.add_argument(
        "--pins", type=Path, default=None,
        help="JSON {battery_sha256, ground_truth_sha256} overriding the prereg "
        "Section 1 pins; fixture and test use only",
    )
    args = ap.parse_args(argv)

    pins = dict(REAL_PINS)
    if args.pins is not None:
        try:
            pins.update(json.loads(args.pins.read_text(encoding="utf-8")))
        except (OSError, ValueError) as e:
            print(f"pins file unreadable: {e}", file=sys.stderr)
            return EXIT_IO

    # Gate first and refuse hard: on failure write nothing, read nothing else.
    failures, gate_lines = run_gate(
        args.seal, args.estate_root, args.battery, args.ground_truth, pins
    )
    if failures:
        for line in failures:
            print(line, file=sys.stderr)
        print("GATE REFUSED: no scoring on a mismatched seal (prereg Sections 0 and 4).", file=sys.stderr)
        return EXIT_REFUSED
    print("SEAL OK")
    for line in gate_lines:
        print(line)

    try:
        answers_text = args.answers.read_text(encoding="utf-8")
        gt_text = args.ground_truth.read_text(encoding="utf-8") if args.score else None
    except (OSError, UnicodeDecodeError) as e:
        print(f"artifact read failed: {e}", file=sys.stderr)
        return EXIT_IO

    outline = build_outline(answers_text, gt_text, gate_lines, args.answers, args.ground_truth)
    try:
        args.score_out.write_text(outline, encoding="utf-8")
    except OSError as e:
        print(f"score-out write failed: {e}", file=sys.stderr)
        return EXIT_IO
    print(f"score outline written: {args.score_out}")
    if gt_text is None:
        print("default mode: ground truth was not opened; a fresh score-phase seat "
              "opens it together with the answers artifact (prereg STEP 3).")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
