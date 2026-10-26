#!/usr/bin/env python3
"""refold_gate.py - fold-order mutation tripwire (B2-328, 2026-09-26).

The disease this meters (brief: watch/inbox/burn_wave_20260926/QUEUE.md row
B2-328, self-fed by the B2-279 sort-totality landing): the fold-order pins
exist (tests/test_index_fold_host.py, 21 tests, and the production-log
falsifier watch/inbox/burn_wave_20260926/B2_279_refold_falsifier.py) but
nothing ran either one when scripts/index_fold_host.mjs changed, so a future
comparator edit could reintroduce sort luck with no gate firing. The gap was
executed for real on 2026-09-26: seqOrderKey mutated so the 2^53 quantization
band (tier 1) outranked exact seqs (tier 2), file saved, `git push --dry-run`
fired the whole pre-push gate, and zero lines named the mutation.

Load-bearing falsifier finding this script encodes: the mutation is
REFOLD-STABLE. The swapped comparator is still a deterministic total order,
so test_refold_stability_with_dummy_appends_between alone PASSES on it. What
names the mutation is the demotion and total-order pin set
(test_inexact_band_register_loses_to_later_exact_register,
test_total_order_breaks_the_old_cycle, test_fold_orders_string_missing_and_legacy_seq
plus three composed-shape tests: 6 failures on the mutated tree). So this
gate runs the WHOLE pin file, never the stability test alone.

Payload: the throwaway-inbox pytest pins, not the production-log falsifier.
The production falsifier appends dummy note events to the shared
watch/inbox/index_events.jsonl on every run; wiring it into pre-push would
write log garbage on every push. The pytest pins carry the same pathological
event mix (band doubles, exact strings, same-file competing registers,
null-seq interleaves) against throwaway inboxes via INDEX_INBOX_DIR, so the
durable inbox is never touched by this gate.

Fail-closed by construction: a missing node binary is exit 2 (the pytest
module skips itself silently without node, which would print a lying ok;
node is a test dependency per the brief and its absence must be named).

Exit codes: 0 = pins green; 1 = pins red (a fold-order behavior changed;
the failing test names below are the operator response input); 2 = cannot
verify (node missing, pytest missing, or the run died).

B2-343 restore-guard audit (2026-09-26): the gate now also runs the
tools/restore_guard.py audit for the fold host before the pin run, so a
stale-base whole-file restore whose bytes still stand on claimed work
(the 16:35:35Z B2-328 restore shape that erased B2-329's landed edit) is
named by the same --changed shape that meters comparator mutations. The
audit is fail-closed: its exit 2 (cannot verify) maps to this gate's exit 2,
never to a green ok. Owning receipt:
watch/inbox/burn_wave_20260926/B2_343_restore_guard_20260926.md.

Usage: python tools/refold_gate.py [--root PATH]
Prints "REFOLD-GATE: ok ..." on success; the pre-push hook pattern-matches
that prefix the same way it matches "CENSUS-PATROL: ok".
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

PINS = Path("tests") / "test_index_fold_host.py"
HOST = Path("scripts") / "index_fold_host.mjs"
TIMEOUT_S = 300




def _run(*args, **kw):
    # HEADLESS law (spawn_sites_no_window): every spawn is windowless.
    # Fix 2026-09-29 (Mickey17 W3): this body called `_run` recursively (the
    # name had been rebound away from subprocess.run), so the first spawn --
    # the B2-343 restore-guard audit -- died with RecursionError and the gate
    # fail-closed every run since the B2-343 landing; the gate_canary
    # refold_gate family proved it BLIND at HEAD (traceback, no
    # REFOLD-GATE verdict). Same bug class the secret-gate fix took
    # (tools/secret_gate_scan.py _run, 2026-09-28 drift-patrol receipt);
    # mirrored here. args is always an argv list --
    # subprocess.run(list, shell=False), no shell, no string interpolation.
    kw.setdefault("shell", False)
    kw.setdefault("creationflags", getattr(subprocess, "CREATE_NO_WINDOW",
                  0x08000000) if sys.platform == "win32" else 0)
    return subprocess.run(*args, **kw)

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    root = Path(args.root).resolve()
    pins = root / PINS
    host = root / HOST
    if not pins.exists() or not host.exists():
        print(f"REFOLD-GATE: FAIL, cannot verify, missing {PINS} or {HOST}")
        return 2
    if shutil.which("node") is None:
        print(
            "REFOLD-GATE: FAIL, node unavailable: the pins skip silently without "
            "node, so a green run here would be a lie; install node or the gate "
            "is disarmed"
        )
        return 2
    # B2-343 restore-guard audit, run before the pins spend their seconds: a
    # stale-base whole-file restore standing on claimed work names now, not
    # after the pytest wait. Fail-closed: exit 2 (cannot verify) stays exit 2.
    guard = _run(
        [
            sys.executable,
            str(root / "tools" / "restore_guard.py"),
            "audit",
            "--path",
            HOST.as_posix(),
            "--root",
            str(root),
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=120,
    )
    guard_tail = (guard.stdout or "") + (guard.stderr or "")
    if guard.returncode != 0:
        print("REFOLD-GATE: FAIL, restore-guard audit for the fold host:")
        for ln in guard_tail.strip().splitlines():
            print(f"  {ln}")
        print(
            "  operator response: a whole-file restore put the host back to "
            "bytes a claim predates; rebase the host past the claim per the "
            "QUEUE.md claim law, or re-record the restore with its true "
            "snapshot ts (watch/inbox/burn_wave_20260926/"
            "B2_343_restore_guard_20260926.md)"
        )
        return 2 if guard.returncode == 2 else 1
    guard_lines = guard_tail.strip().splitlines()
    guard_ok = guard_lines[-1].strip() if guard_lines else ""
    # B2-486 queue-dupes census, run beside the restore-guard audit: the
    # B2-167 census found four post-sweep double-claimed ids no gate saw, and
    # the 2026-09-26 board-restore disease then minted 20 verbatim duplicate
    # rows in one evening. Fail-closed same shape as the arm above: exit 1 on
    # any double-claimed id (operator response: dedupe the verbatim restore
    # artifacts or renumber per the B2-167 law), exit 2 if the board cannot
    # be read. Malformed row-start forms print as warnings, never fail.
    dupes = _run(
        [
            sys.executable,
            str(root / "tools" / "queue_dupes_check.py"),
            "--root",
            str(root),
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=120,
    )
    dupes_tail = (dupes.stdout or "") + (dupes.stderr or "")
    if dupes.returncode != 0:
        print("REFOLD-GATE: FAIL, queue-dupes census for the burn-wave board:")
        for ln in dupes_tail.strip().splitlines():
            print(f"  {ln}")
        print(
            "  operator response: verbatim duplicate rows are restore "
            "artifacts, dedupe them keeping one row each; two DIFFERENT "
            "briefs on one id is a B2-167 double-spend, renumber the later "
            "claimant highest+1 (tools/queue_dupes_check.py, "
            "watch/inbox/burn_wave_20260926/B2_486_queue_dupes_gate_20260926.md)"
        )
        return 2 if dupes.returncode == 2 else 1
    for ln in dupes_tail.strip().splitlines():
        if ln.startswith("QUEUE-DUPES: WARN") or ln.startswith("QUEUE-DUPES: ok"):
            print(f"  {ln}")
    cmd = [sys.executable, "-m", "pytest", str(pins), "-q", "--no-header"]
    try:
        r = _run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        print(f"REFOLD-GATE: FAIL, pin run exceeded {TIMEOUT_S}s")
        return 2
    tail = (r.stdout or "") + (r.stderr or "")
    if r.returncode == 0:
        m = re.search(r"(\d+) passed", tail)
        passed = m.group(1) if m else "?"
        skipped = re.search(r"(\d+) skipped", tail)
        skip_note = f", {skipped.group(1)} skipped" if skipped else ""
        print(
            f"REFOLD-GATE: ok ({PINS.as_posix()} ran against {HOST.as_posix()}: "
            f"{passed} passed{skip_note}; {guard_ok})"
        )
        return 0
    failed = sorted(set(re.findall(r"FAILED (\S+)", tail)))
    print(
        "REFOLD-GATE: FAIL, fold pins red on the current tree (the pin set "
        f"covers fold order, the B2-279 comparator law, the living law and the "
        f"events dump shape over {HOST.as_posix()}); failing pins:"
    )
    for name in failed:
        print(f"  {name}")
    print("  pytest tail:")
    for ln in tail.strip().splitlines()[-15:]:
        print(f"  {ln}")
    print(
        "  operator response: revert or fix the comparator edit until this gate "
        "prints ok; the law is B2-279 sort totality (tier 0 null-seq below all "
        "seq events, past-2^53 doubles demoted below every exact seq with the "
        "counted fold warning, exact seqs by BigInt) plus refold stability; "
        "production-log falsifier if needed: "
        "watch/inbox/burn_wave_20260926/B2_279_refold_falsifier.py before/after"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
