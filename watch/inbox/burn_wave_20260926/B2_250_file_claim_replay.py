"""B2-250 shared-file claim law replay probe (2026-09-26).

Replays the 2026-09-26 B2-244 + B2-245 same-hour interleave on the shared
uncommitted tools/census_drift_patrol.py, on temp copies built from today's
live bytes (this burn wave's live QUEUE.md plus the live uncommitted module),
under both regimes:

  Scenario A, no convention: both lanes read the module at the same moment
  and each applies a whole-file write from its own snapshot, so the second
  write erases the first lane's bytes (the stale-write shape of the disease).
  Today's actual interleave survived by clean-apply luck, see the B2-245
  receipt Evidence mid-lane paragraph: targeted pytest read "25 passed, 13
  errors" on half-written shared bytes, an immediate rerun read "38 passed".

  Scenario B, claim law (the codified convention): lane B2-244 appends
    - CLAIM B2-244 tools/census_drift_patrol.py <ts> (<reason>)
  to the QUEUE Open section BEFORE touching the module; lane B2-245 re-reads
  the queue before its edit, detects the foreign claim on the same file,
  re-reads the module bytes, and rebases its edit on them; both lanes'
  edits survive.

Claim grammar codified in the QUEUE.md header (Shared-file claim law):
  - CLAIM <lane-id> <repo-relative-path> <YYYY-MM-DDTHH:MM:SSZ> (<reason>)
Retirement renames the leading CLAIM token to CLAIMED in place, which also
removes the line from active detection (the regex requires "- CLAIM ").

  Scenario C, the stale-base whole-file restore (added by B2-343,
2026-09-26): replays the 16:35:35Z B2-328 byte-identical host restore that
erased B2-329's landed edit for about two minutes. Lane R (playing B2-328)
snapshots the module BEFORE any claim; lane E (playing B2-329) files its
claim (the real 16:31:01Z ts), lands its edit, and retires the claim to
CLAIMED; lane R then restores the whole file from the pre-claim snapshot.
Unguarded, the erase reproduces and the claim law's active-only detection
sees NOTHING (the claim is retired by restore time: the exact gap the
restore guard exists to close). Under the guard
(tools/restore_guard.py check, the pre-write arm), the restore is NAMED
before it lands: the guard matches retired claims too, sees the snapshot
predates the claim, and fails while the landed bytes still stand. Snapshot
ts in the replay is the reconstructed pre-claim moment 16:25:00Z (the
receipts fix the ordering, after B2-279's landing and before B2-329's
16:31:01Z claim; the exact snapshot minute is not on record).

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_250_file_claim_replay.py
Exit 0 = the falsifier holds: the collision reproduces only without the
convention, under it the second lane detects the claim and re-reads, and
the stale-base restore is named by the guard before it lands.
Exit 1 = the law failed its own replay.
"""

import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
QUEUE = REPO / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
MODULE = REPO / "tools" / "census_drift_patrol.py"
MODULE_REL = "tools/census_drift_patrol.py"

CLAIM_LINE_RE = re.compile(rb"(?m)^- CLAIM (\S+) (\S+) (\S+)")

# Live foreign claims on the replay target ride into the staged board copy and
# conflate the scenario's own interleave (caught live by the B2-343 rerun:
# B2-338's 17:02:30Z claim on the module made scenario B detect ['B2-338',
# 'B2-244'] and scenario C see a non-empty active set for the wrong reason),
# so staging strips every live claim line for the target path first.
CLAIM_TARGET_STRIP_RE = re.compile(
    rb"(?m)^- CLAIM(?:ED)? \S+ " + re.escape(MODULE_REL.encode()) + rb" [^\r\n]*\r?\n?"
)

A_MARKER = b"# B2-244 collect deep-check landing (B2-250 replay marker)"
B_MARKER = b"# B2-245 parser hardening landing (B2-250 replay marker)"

CLAIM_LINE = (
    b"- CLAIM B2-244 tools/census_drift_patrol.py "
    b"2026-09-26T14:05:00Z (collect deep-check in flight, re-read before editing)\r\n"
)

# Scenario C constants: the real 16:35:35Z restore replayed on temp copies.
RESTORE_GUARD = REPO / "tools" / "restore_guard.py"
RESTORE_SNAP_TS = "2026-09-26T16:25:00Z"  # reconstructed pre-claim snapshot moment
RESTORE_CLAIM_LINE = (
    b"- CLAIM B2-329 tools/census_drift_patrol.py "
    b"2026-09-26T16:31:01Z (B2-329 replay claim, the real B2-329 fold-host claim ts)\r\n"
)
E_MARKER = b"# B2-329 dump-purity landing (B2-343 replay marker)"


def claims_for(queue_bytes, path, own_lane):
    """Active foreign CLAIM lane ids for one repo-relative path."""
    found = []
    for m in CLAIM_LINE_RE.finditer(queue_bytes):
        lane = m.group(1).decode("utf-8")
        claimed = m.group(2).decode("utf-8").replace("\\", "/")
        if claimed == path and lane != own_lane:
            found.append(lane)
    return found


def stage(workdir):
    workdir.mkdir(parents=True, exist_ok=True)
    q = workdir / "QUEUE.md"
    m = workdir / "census_drift_patrol.py"
    q.write_bytes(CLAIM_TARGET_STRIP_RE.sub(b"", QUEUE.read_bytes()))
    shutil.copyfile(MODULE, m)
    return q, m


def scenario_a(workdir):
    """No convention: same-moment snapshots, whole-file writes, last wins."""
    q, m = stage(workdir)
    snapshot_a = m.read_bytes()
    snapshot_b = m.read_bytes()
    # lane B2-244 edits and writes first
    m.write_bytes(snapshot_a + b"\r\n" + A_MARKER + b"\r\n")
    # lane B2-245 writes from its same-moment snapshot without re-reading
    m.write_bytes(snapshot_b + b"\r\n" + B_MARKER + b"\r\n")
    final = m.read_bytes()
    a_survived = A_MARKER in final
    b_survived = B_MARKER in final
    print("SCENARIO A (no convention): B2-244 bytes survived: %s" % a_survived)
    print("SCENARIO A (no convention): B2-245 bytes survived: %s" % b_survived)
    collision = (not a_survived) and b_survived
    print("SCENARIO A (no convention): stale-write collision reproduced: %s" % collision)
    return collision


def scenario_b(workdir):
    """Claim law: claim line first, second lane detects, re-reads, rebases."""
    q, m = stage(workdir)
    # lane B2-244 claims the file BEFORE touching it
    q.write_bytes(q.read_bytes() + CLAIM_LINE)
    # only after the claim is on disk does lane B2-244 read and edit the module
    a_bytes = m.read_bytes()
    m.write_bytes(a_bytes + b"\r\n" + A_MARKER + b"\r\n")
    # lane B2-245, before its edit: re-read the queue, look for foreign claims
    detected = claims_for(q.read_bytes(), MODULE_REL, "B2-245")
    print("SCENARIO B (claim law): B2-245 detected foreign claims: %s" % detected)
    if detected != ["B2-244"]:
        print("SCENARIO B FAILED: foreign claim not detected")
        return False
    # detection forces the re-read; the edit rebases on fresh bytes
    fresh = m.read_bytes()
    if A_MARKER not in fresh:
        print("SCENARIO B FAILED: re-read did not see the first lane's bytes")
        return False
    m.write_bytes(fresh + b"\r\n" + B_MARKER + b"\r\n")
    final = m.read_bytes()
    both = A_MARKER in final and B_MARKER in final
    print("SCENARIO B (claim law): both lanes' bytes survive: %s" % both)
    return both


def retire_first_claim(q):
    """Flip the scenario claim line to CLAIMED in place (the retirement law)."""
    data = q.read_bytes()
    flipped = data.replace(b"- CLAIM B2-329 ", b"- CLAIMED B2-329 ", 1)
    q.write_bytes(flipped)


def scenario_c(workdir):
    """Restore replay: the 16:35:35Z stale-base restore vs the guard.

    Unguarded branch: the restore erases the landed edit and the active-only
    claim detection is blind (the claim is retired by restore time).
    Guarded branch: tools/restore_guard.py check names the restore BEFORE it
    lands and the landed bytes still stand afterwards.
    """
    import hashlib
    import subprocess

    # -- unguarded: the disease reproduces and the active law sees nothing --
    q, m = stage(workdir)
    snapshot = m.read_bytes()
    snap_sha = hashlib.sha256(snapshot).hexdigest()
    # lane E (B2-329) files its claim, lands its edit, retires the claim
    q.write_bytes(q.read_bytes() + RESTORE_CLAIM_LINE)
    m.write_bytes(snapshot + b"\r\n" + E_MARKER + b"\r\n")
    retire_first_claim(q)
    # the claim law's active-only detection at restore time
    active_now = claims_for(q.read_bytes(), MODULE_REL, "B2-328")
    # lane R (B2-328) restores the whole file from the pre-claim snapshot
    m.write_bytes(snapshot)
    erased = E_MARKER not in m.read_bytes()
    print("SCENARIO C (unguarded): restore reproduced the erase: %s" % erased)
    print(
        "SCENARIO C (unguarded): active-claim detection at restore time: %s"
        % (active_now or "empty (blind)")
    )
    if not erased:
        print("SCENARIO C FAILED: the erase did not reproduce")
        return False
    if active_now:
        print(
            "SCENARIO C FAILED: expected the active-only law to be blind to "
            "the retired claim, it named %s" % active_now
        )
        return False

    # -- guarded: the same interleave under the pre-write check --
    with tempfile.TemporaryDirectory() as td2:
        q2, m2 = stage(Path(td2) / "guarded")
        snapshot2 = m2.read_bytes()
        snap_sha2 = hashlib.sha256(snapshot2).hexdigest()
        q2.write_bytes(q2.read_bytes() + RESTORE_CLAIM_LINE)
        m2.write_bytes(snapshot2 + b"\r\n" + E_MARKER + b"\r\n")
        retire_first_claim(q2)
        r = subprocess.run(
            [
                sys.executable,
                str(RESTORE_GUARD),
                "check",
                "--path",
                MODULE_REL,
                "--file",
                str(m2),
                "--snapshot-sha",
                snap_sha2,
                "--snapshot-ts",
                RESTORE_SNAP_TS,
                "--board",
                str(q2),
            ],
            capture_output=True,
            text=True,
        )
        out = (r.stdout or "") + (r.stderr or "")
        for ln in out.strip().splitlines():
            print("SCENARIO C (guarded):   %s" % ln)
        named = r.returncode == 1 and "B2-329" in out
        still_standing = E_MARKER in m2.read_bytes()
        print(
            "SCENARIO C (guarded): guard named the restore before it lands: %s"
            % named
        )
        print(
            "SCENARIO C (guarded): landed edit still standing after the blocked "
            "restore: %s" % still_standing
        )
        return named and still_standing


def main():
    if not QUEUE.is_file() or not MODULE.is_file():
        print("live bytes missing: %s / %s" % (QUEUE, MODULE))
        return 1
    live_active = len(CLAIM_LINE_RE.findall(QUEUE.read_bytes()))
    print("live QUEUE.md active CLAIM lines at probe time: %d" % live_active)
    with tempfile.TemporaryDirectory() as td:
        a_ok = scenario_a(Path(td) / "a")
    with tempfile.TemporaryDirectory() as td:
        b_ok = scenario_b(Path(td) / "b")
    if not RESTORE_GUARD.is_file():
        print("restore guard missing: %s" % RESTORE_GUARD)
        return 1
    with tempfile.TemporaryDirectory() as td:
        c_ok = scenario_c(Path(td) / "c")
    ok = a_ok and b_ok and c_ok
    print("PROBE VERDICT: %s" % ("HOLDS" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
