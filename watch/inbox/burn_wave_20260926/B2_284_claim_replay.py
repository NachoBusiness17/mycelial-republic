#!/usr/bin/env python
"""B2-284 claim-law extension replay: shared TEST file as the claim surface.

The B2-245 interleave's most visible symptom was a targeted pytest reading
another lane's half-written bytes mid-verification ("25 passed, 13 errors",
then "38 passed") over tests/test_census_drift_patrol.py co-edited in the
same hour - but the codified Shared-file claim law named only modules, so a
second lane editing the shared suite had NO claim to detect. This replay
puts the test file itself on the claim surface, on temp copies built from
today's live bytes (the live test file plus a live queue stand-in), under
both regimes:

  Scenario A, law as first codified (modules only, tests/ silent): lane A
    writes a half-written test file (truncated mid-function, the shape a
    whole-file write interrupted mid-buffer produces), lane B then runs a
    targeted pytest collection against it; collection ERRORS on the
    half-written bytes (the observed errors shape) and B had no claim to
    detect because the surface is a test file.

  Scenario B, extended law (B2-284): lane A claims the tests/ path BEFORE
    touching it; lane B re-reads the queue, detects the foreign claim on
    the shared test surface, re-reads the file bytes, and applies its edit
    on the completed bytes; both lanes' edits survive and the targeted
    collection passes.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_284_claim_replay.py
Exit 0 = the falsifier holds: the undetected half-write collision
reproduces only while tests/ is silent, under the extended convention the
second lane detects the claim and re-reads.
Exit 1 = the extension failed its own replay.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LIVE_TEST = ROOT / "tests" / "test_census_drift_patrol.py"

CLAIM_RE = re.compile(r"- CLAIM \S+ (?P<path>\S+) \S+ \(")


def queue_claims(queue_text: str) -> set:
    return {m.group("path") for m in CLAIM_RE.finditer(queue_text)}


def main() -> int:
    original = LIVE_TEST.read_text(encoding="utf-8").replace("\r\n", "\n")
    if "def test_" not in original:
        print("live test file unexpected shape")
        return 1
    # lane A's whole-file rewrite, truncated mid-signature: a real
    # interrupted write can stop anywhere, so use the unambiguous
    # mid-statement shape (unclosed def signature) that provably fails
    # compile at any cut point, never a lucky complete-looking tail.
    cut = None
    for pos in [m.start() for m in re.finditer(r"\ndef test_", original)
                if m.start() > int(len(original) * 0.5)][::-1]:
        cand = original[:pos] + "\ndef test_lane_a_new_pin(:\n"
        try:
            compile(cand, "half", "exec")
        except SyntaxError:
            cut = pos
            break
    if cut is None:
        print("no provable half-write cut point found")
        return 1
    half = original[:cut] + "\ndef test_lane_a_new_pin(:\n"

    ok = True

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        test_file = tdp / "test_census_drift_patrol.py"
        queue = tdp / "queue.md"
        queue.write_text("# queue\n## Open\n", encoding="utf-8")

        # ---- Scenario A: tests/ silent (law as first codified) ----
        test_file.write_text(half, encoding="utf-8")
        # lane B re-reads the queue per the law, but the law names modules:
        # the tests path is not in the claim grammar, no claim exists, so B
        # proceeds straight to its targeted pytest on the shared bytes
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q",
             str(test_file)],
            capture_output=True, text=True, timeout=120,
            env={"SYSTEMROOT": __import__("os").environ.get("SYSTEMROOT", ""),
                 "PATH": __import__("os").environ.get("PATH", "")},
        )
        errored = (r.returncode != 0) or ("error" in (r.stdout + r.stderr).lower())
        print("scenario A (tests/ silent): targeted pytest on half-written "
              "shared test bytes ->", "ERROR shape" if errored else "collected clean")
        if not errored:
            print("  !! expected the half-written file to error collection")
            ok = False
        # and B had nothing to detect:
        if queue_claims(queue.read_text(encoding="utf-8")):
            print("  !! scenario A unexpectedly saw a claim")
            ok = False
        print("scenario A: lane B had no claim to detect (tests/ outside the "
              "grammar): detection surface empty -> True")

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        test_file = tdp / "test_census_drift_patrol.py"
        queue = tdp / "queue.md"
        queue.write_text("# queue\n## Open\n", encoding="utf-8")

        # ---- Scenario B: extended law, tests/ claimable ----
        test_file.write_text(original, encoding="utf-8")
        # lane A claims the TEST path first
        q = queue.read_text(encoding="utf-8")
        queue.write_text(q + "- CLAIM lane-A tests/test_census_drift_patrol.py "
                         "2026-09-26T21:00:00Z (B2-x pin lands in the shared suite)\n",
                         encoding="utf-8")
        test_file.write_text(half, encoding="utf-8")  # A's write completes
        test_file.write_text(original.replace(
            "def test_",
            "def test_lane_a_new_pin():\n    assert True\n\n\ndef test_", 1),
            encoding="utf-8")  # A's full rewrite lands
        # lane B re-reads the queue per the extended law: the tests/ path is
        # a claim surface now
        foreign = "tests/test_census_drift_patrol.py" in queue_claims(
            queue.read_text(encoding="utf-8"))
        print("scenario B (extended law): lane B detects foreign claim on the "
              "shared test surface ->", foreign)
        if not foreign:
            ok = False
        # B rebases: re-reads current bytes (A's completed rewrite) before
        # its own edit
        current = test_file.read_text(encoding="utf-8")
        b_edit = current.replace("def test_", "def test_", 1)  # no-op rebase
        b_edit = b_edit + "\n\ndef test_lane_b_followup():\n    assert True\n"
        test_file.write_text(b_edit, encoding="utf-8")
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q",
             str(test_file)],
            capture_output=True, text=True, timeout=120,
            env={"SYSTEMROOT": __import__("os").environ.get("SYSTEMROOT", ""),
                 "PATH": __import__("os").environ.get("PATH", "")},
        )
        clean = r.returncode == 0
        both = "test_lane_a_new_pin" in current and "test_lane_b_followup" in \
            test_file.read_text(encoding="utf-8")
        print("scenario B: targeted pytest on rebased bytes ->",
              "collected clean" if clean else "ERROR", "; both edits survive ->", both)
        if not (clean and both):
            ok = False

    print("---")
    print("extension replay:", "HOLDS" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
