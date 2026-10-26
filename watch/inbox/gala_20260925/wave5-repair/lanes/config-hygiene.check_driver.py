"""config-hygiene lane finish-line command driver (gala wave5-repair, 2026-09-29).

Runs the finish-line commands in order and appends RAW stdout+stderr plus the
exit code of each to config-hygiene.check.txt. Stages:

  pre   : seal verify (baseline, expected RED with the known 4)
          + violation ratchet --changed
          + loader fail-loud checks (config-hygiene.check.py)
  reseal: sanctioned seal update --by --note, then verify (expected PASS)
  final : seal verify only (no new drift at lane close)

Run: .venv/Scripts/python.exe watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.check_driver.py <pre|reseal|final>
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
CHECK = ROOT / "watch" / "inbox" / "gala_20260925" / "wave5-repair" / "lanes" / "config-hygiene.check.txt"

NOTE = (
    "gala wave5-repair config-hygiene 2026-09-29 re-seal of the f-03/s2-10 modified=4 debt; "
    "per file: improve.yaml live bytes are HEAD caddaeb72 (Q-049 demote block landed 09-28 13:21 "
    "after the 12:24Z stamp) and git-clean; violation_baseline.json is HEAD d90bc8607 (ratchet "
    "prune 943 to 941, 09-28 15:09 post-stamp) and git-clean; fossil_registry.json carries an "
    "uncommitted working-tree registry edit adding recompile_cmd/check_cmd to the thought-quantizer "
    "entry (left for its author to commit); mirrors.json is live stealth_driver state rewritten "
    "every cycle and git-untracked (s2-10 F3 standing churn, structural fix owed); verify "
    "immediately before this re-seal showed modified=4 and nothing else, so no NEW drift is "
    "sealed over"
)

CHURN_NOTE = (
    "gala wave5-repair config-hygiene lane 2026-09-29 second named act: after the modified=4 "
    "re-seal, a concurrent stealth_driver cycle rewrote mirrors.json live state (s2-10 F3 churn, "
    "predicted in the lane receipt); verify showed modified=1 = mirrors.json only, a member of "
    "the known 4, zero NEW files; re-sealed so the pre-push seal gate stays open for concurrent "
    "lanes; structural fix (live-state file inside the configs/ seal) still owed to the operator"
)

STAGES = {
    "pre": [
        ("seal-verify-baseline", [PY, "tools/config_seal.py", "verify"]),
        ("violation-ratchet-changed", [PY, "tools/violation_ratchet.py", "check", "--changed"]),
        ("loader-fail-loud-checks", [PY, str(ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.check.py")]),
    ],
    "reseal": [
        ("seal-update-sanctioned", [PY, "tools/config_seal.py", "update", "--by", "gala-wave5-config-hygiene-lane", "--note", NOTE]),
        ("seal-verify-after-reseal", [PY, "tools/config_seal.py", "verify"]),
    ],
    "final": [
        ("seal-verify-final-at-lane-close", [PY, "tools/config_seal.py", "verify"]),
    ],
    "scan": [
        ("em-en-dash-and-nonascii-scan", [PY, str(ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.scan.py")]),
    ],
    "reseal2": [
        ("seal-update-churn-reseal", [PY, "tools/config_seal.py", "update", "--by", "gala-wave5-config-hygiene-lane", "--note", CHURN_NOTE]),
        ("seal-verify-after-churn-reseal", [PY, "tools/config_seal.py", "verify"]),
    ],
}


def main() -> int:
    stage = sys.argv[1] if len(sys.argv) > 1 else "pre"
    cmds = STAGES.get(stage)
    if cmds is None:
        print(f"unknown stage {stage!r}; use pre|reseal|final")
        return 2
    overall = 0
    with CHECK.open("a", encoding="utf-8") as fh:
        fh.write(f"\n===== STAGE {stage} =====\n")
        for name, argv in cmds:
            fh.write(f"\n--- {name}\n$ {' '.join(argv)}\n")
            fh.flush()
            p = subprocess.run(argv, cwd=str(ROOT), capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            fh.write(p.stdout or "")
            if p.stderr:
                fh.write("[stderr]\n" + p.stderr)
            fh.write(f"EXIT={p.returncode}\n")
            print(f"{name}: exit {p.returncode}")
            overall = overall or p.returncode
    return overall


if __name__ == "__main__":
    sys.exit(main())
