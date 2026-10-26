#!/usr/bin/env python3
"""moonshot-2 probe runner (ouroboros R3 trust, 2026-10-05).

Re-runnable evidence for every probe claim in
watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/moonshot-2.md.
Each probe prints PROBE <name>: <observed> and the runner exits 1 if any
observed value disagrees with the value the fold banked (the fold's claims
are falsifiable by running this file). Run from the repo root:

  .venv/Scripts/python.exe watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/probes/moonshot2_probes.py

No repo file is modified: all fixtures live in a temp dir removed on exit.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]  # probes/ -> r3 dir -> ractor_engine -> inbox -> watch -> repo
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0
EXPECT: list[tuple[str, object, object]] = []  # (name, expected, observed) filled by probes


def run_py(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True,
                          text=True, timeout=300, creationflags=HEADLESS)


def probe_phantom(tmp: Path) -> None:
    """P1: the founding 191.8M class passes when the source carries any
    incidental substring of the claim's integer part, and P2: the unit M is
    never enforced (an unscaled decimal certifies the scaled claim)."""
    src_a = tmp / "SOURCE_A.md"
    src_a.write_text("audit row 1914 carried no hits\n", encoding="utf-8")
    rec_weak = tmp / "REC_WEAK.md"
    rec_weak.write_text(f"We spent 191.8M tokens on the sweep ({src_a.name} carries the number).\n", encoding="utf-8")
    r = run_py(["tools/citation_lint.py", "check", "--files", str(rec_weak)], ROOT)
    EXPECT.append(("P1-weak-int-form lint exit (0 = phantom certified)", 0, r.returncode))

    src_b = tmp / "SOURCE_B.md"
    src_b.write_text("latency 287.6 observed\n", encoding="utf-8")
    rec_unit = tmp / "REC_UNIT.md"
    rec_unit.write_text(f"We spent 287.6M tokens on the sweep ({src_b.name} carries the number).\n", encoding="utf-8")
    r = run_py(["tools/citation_lint.py", "check", "--files", str(rec_unit)], ROOT)
    EXPECT.append(("P2-unit-blind lint exit (0 = scaled claim certified by unscaled source)", 0, r.returncode))

    rec_ctrl = tmp / "REC_CTRL.md"
    rec_ctrl.write_text(f"We spent 287.6M tokens on the sweep ({src_a.name} carries the number).\n", encoding="utf-8")
    r = run_py(["tools/citation_lint.py", "check", "--files", str(rec_ctrl)], ROOT)
    EXPECT.append(("P3-control lint exit (1 = the check still has teeth when no form matches)", 1, r.returncode))


def probe_g6(tmp: Path) -> None:
    """P4: G6-receipts hard-passes naming a receipt that does not exist on
    disk and carries a dated stamp, with no soft warn."""
    sys.path.insert(0, str(ROOT))
    import tools.workflow_gate as wg  # noqa: E402
    text = ("const x = 1; // receipt lands in watch/inbox/NEVER_LANDED_20261099.md\n"
            "// fetched: 2026-10-05\n")
    row = [r for r in wg.run_checks(text) if r["id"] == "G6-receipts"][0]
    EXPECT.append(("P4-G6 ok on nonexistent receipt (True = no filesystem check at all)", True, row["ok"]))
    EXPECT.append(("P4-G6 soft flag absent", False, bool(row.get("soft"))))


def probe_control_skip(tmp: Path) -> None:
    """P5: the scenario suite returns 0 with zero mention when the all-pass
    control fixture is absent (LAW-12's control contract silently degrades)."""
    cards = tmp / "cards"
    shutil.copytree(ROOT / "configs" / "workflow_gate_scenarios", cards)
    (cards / "fixtures" / "pass_control.dwf.ts").unlink()
    r = run_py(["tools/workflow_gate.py", "check", "--scenarios", str(cards)], ROOT)
    silent = "pass_control" not in r.stdout
    EXPECT.append(("P5-suite exit without control (0 = green with no control)", 0, r.returncode))
    EXPECT.append(("P5-suite silent about missing control (True = no mention)", True, silent))


def probe_cred_fp(tmp: Path) -> None:
    """P6: two different secrets sharing 4-char head + length in one file mint
    the SAME fingerprint, so baselining one silently accepts the other."""
    sys.path.insert(0, str(ROOT))
    from tools.prepush_credential_shape import scan_text  # noqa: E402
    a = scan_text('k1 = "sk-abcd1111222233334444"', "watch/inbox/X.md")[0]
    b = scan_text('k2 = "sk-abcd9999888877776666"', "watch/inbox/X.md")[0]
    EXPECT.append(("P6-fingerprint collision (True = second key auto-accepted)", True, a["fp"] == b["fp"]))


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="r3moon2_"))
    try:
        probe_phantom(tmp)
        probe_g6(tmp)
        probe_control_skip(tmp)
        probe_cred_fp(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    bad = 0
    for name, exp, obs in EXPECT:
        flag = "ok  " if exp == obs else "DRIFT"
        if exp != obs:
            bad += 1
        print(f"PROBE {flag} {name}: expected={exp!r} observed={obs!r}")
    print(f"moonshot2_probes: {len(EXPECT) - bad}/{len(EXPECT)} expectations reproduced")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
