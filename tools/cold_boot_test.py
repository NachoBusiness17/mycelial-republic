"""cold_boot_test — the ractor's overturning run, automated.
Copies seed/ to a fresh temp dir, then runs FIRST_BOOT steps 0-7 verbatim with no
estate environment. Scorecard: exit 0, or readable nonzero message — never a
traceback, never a missing module. Cleans up after itself.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "seed"

CHECKS = [
    ("step0 verify_seal", [sys.executable, "verify_seal.py"]),
    ("step0b sha256sum -c", None),  # special-cased (stock tool, subprocess shell=off)
    ("step2 smith chart", [sys.executable, "engines/estate_smith_chart.py", "--no-plot"]),
    ("step3 key audit", [sys.executable, "engines/key_law.py", "--audit"]),
    ("step4 atlas empty dir", [sys.executable, "engines/estate_atlas.py", "empty_dir_probe"]),
    ("step6 cooker status", [sys.executable, "engines/cooker.py", "status"]),
    ("step6b cooker fire --due", [sys.executable, "engines/cooker.py", "fire", "--due"]),
    ("claritas demo", [sys.executable, "engines/claritas.py"]),
    ("librarian catalog", [sys.executable, "engines/librarian_catalog.py"]),
    ("phone_relay no-env (readable fail)", [sys.executable, "engines/phone_relay.py", "test"]),
    ("stealth_sweep no keys (readable)", [sys.executable, "engines/stealth_sweep.py"]),
    ("task_wall no keys (readable)", [sys.executable, "engines/task_wall.py", "--budget-minutes", "0"]),
    ("bakeoff no keys (readable)", [sys.executable, "engines/model_bakeoff.py"]),
    ("step7 smith again (daily meter)", [sys.executable, "engines/estate_smith_chart.py", "--no-plot"]),
]

TRACEBACK_MARKS = (b"Traceback (most recent call last):", b"ModuleNotFoundError", b"NameError")

# Pre-zip gate verdicts that block the builder's zip emission (build book t7 spec).
# READABLE-FAIL passes by design: the contract is "exit 0, or readable nonzero
# message". A TIMEOUT blocks too: a step that hangs is not a boot a stranger survives.
GATE_BLOCKERS = ("CRASH", "ERROR", "TIMEOUT")




def _run(*args, **kw):
    # HEADLESS law (spawn_sites_no_window): every spawn is windowless.
    kw.setdefault("creationflags", getattr(subprocess, "CREATE_NO_WINDOW",
                  0x08000000) if sys.platform == "win32" else 0)
    return _run(*args, **kw)

def run_one(cold: Path, name: str, cmd) -> tuple[str, str]:
    if cmd is None:  # sha256sum -c via the stock tool
        try:
            p = _run(["sha256sum", "-c", "MANIFEST.sha256"], cwd=cold,
                               capture_output=True, timeout=120)
            out = p.stdout[-200:].decode("utf-8", "replace")
            return ("PASS" if p.returncode == 0 else "FAIL"), out or f"rc={p.returncode}"
        except FileNotFoundError:
            return "SKIP", "sha256sum not on PATH"
    try:
        p = _run(cmd, cwd=cold, capture_output=True, timeout=180,
                           env={"PATH": "", "SYSTEMROOT": __import__("os").environ.get("SYSTEMROOT", ""),
                                "TEMP": __import__("os").environ.get("TEMP", ""),
                                "LOCALAPPDATA": str(cold / "no_hermes_here")})
        out = (p.stdout + p.stderr)[-400:].decode("utf-8", "replace")
        rc = p.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ">180s"
    except Exception as e:  # noqa: BLE001
        return "ERROR", str(e)[:200]
    if rc == 0:
        return "PASS", out[-160:].replace("\n", " | ")
    if any(m in (p.stdout + p.stderr) for m in TRACEBACK_MARKS):
        return "CRASH", out[-220:].replace("\n", " | ")
    return "READABLE-FAIL", out[-200:].replace("\n", " | ")


def gate() -> tuple[bool, str]:
    """Pre-zip gate for tools/seed_v2.py (build book t7 spec, t28 refire).
    Runs the full cold-boot suite against a fresh temp copy of seed/ and returns
    (ok, scorecard_line). ok is False when any check ends CRASH, ERROR, or TIMEOUT.
    Fix receipt (cause + evidence): V1 shipped 2-of-7 first-boot steps working
    (ractor ruling, SEED_V2_BUILD_BOOK_20260925.md) and Desktop still held the stale
    3-pyc seed-3.3.0 zip on 2026-09-25 because nothing between build and zip ever
    ran the cold boot. The gate is that missing run."""
    tmp = Path(tempfile.mkdtemp(prefix="seed_cold_gate_"))
    cold = tmp / "seed"
    shutil.copytree(SEED, cold)
    (cold / "empty_dir_probe").mkdir()
    print(f"cold copy: {cold}")
    results = []
    try:
        for name, cmd in CHECKS:
            verdict, detail = run_one(cold, name, cmd)
            results.append((name, verdict, detail))
            print(f"  [{verdict:>13}] {name} - {detail[:150]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    passed = sum(1 for _, v, _ in results if v == "PASS")
    readable = sum(1 for _, v, _ in results if v == "READABLE-FAIL")
    blocked = [f"{n}={v}" for n, v, _ in results if v in GATE_BLOCKERS]
    line = (f"GATE SCORECARD: {passed} PASS / {readable} readable-fail / "
            f"{len(results)} total; blockers: {', '.join(blocked) if blocked else 'NONE'}")
    print(line)
    return (not blocked), line


def main() -> int:
    ok, _ = gate()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
