"""riddler_veil_gate - pre-push wiring for the Riddler Protocol.

Scans changed-and-untracked prose files for the RIDDLER-PARABLE marker (first 5
lines). Every marked file must pass the riddler_veil mechanical check. No marked
files = trivial pass, so the gate never touches normal pushes.

Fail-loud rules: a marked parable with missing state/riddler registries fails
(you cannot publish a parable past unbuilt machinery). Exit 1 blocks the push.

Wired into githooks/pre-push 2026-10-12 per the operator's code-as-law order
("built into the machinery; it needs to have truth"). Enforcement from first
landing: the scope is only self-declared parables, so the classic t40
lockout risk does not apply - unmarked files never trigger this gate.

Git calls mirror the citation_lint_io sanctioned shape: literal argument lists,
HEADLESS creationflags. The veil check itself runs by direct module import, no
subprocess.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "RIDDLER-PARABLE"
PROSE = (".md", ".txt", ".rst")
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def _git_diff_head() -> list:
    """Changed tracked files vs HEAD (literal args, sanctioned shape)."""
    try:
        r = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(ROOT), capture_output=True, text=True,
            timeout=30, creationflags=HEADLESS,
        )
        return r.stdout.splitlines() if r.returncode == 0 else []
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"PUSH-GATE: riddler_veil WARN diff unavailable: {exc}")
        return []


def _git_others() -> list:
    """Untracked files (literal args, sanctioned shape)."""
    try:
        r = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=str(ROOT), capture_output=True, text=True,
            timeout=30, creationflags=HEADLESS,
        )
        return r.stdout.splitlines() if r.returncode == 0 else []
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"PUSH-GATE: riddler_veil WARN ls-files unavailable: {exc}")
        return []


def _changed_prose() -> list:
    lines = set(_git_diff_head()) | set(_git_others())
    keep = []
    for line in sorted(lines):
        p = ROOT / line
        if p.suffix.lower() in PROSE and p.is_file():
            keep.append(p)
    return keep


def _is_marked(p: Path) -> bool:
    try:
        head = "\n".join(p.read_text(encoding="utf-8", errors="replace").splitlines()[:5])
    except OSError:
        return False
    return MARKER in head


def main() -> int:
    marked = [p for p in _changed_prose() if _is_marked(p)]
    if not marked:
        print("PUSH-GATE: riddler_veil ok (no marked parables in changed set)")
        return 0

    sys.path.insert(0, str(ROOT / "tools"))
    import riddler_veil as rv

    fails = 0
    for p in marked:
        rc = rv.main(["check", "--parable", str(p), "--grade", "sensing"])
        if rc != 0:
            fails += 1
            print(f"PUSH-GATE: riddler_veil BLOCKED {p.name} (rc={rc})")
    if fails:
        print(f"PUSH-GATE: riddler_veil FAIL ({fails} marked parable(s) failed the veil)")
        return 1
    print(f"PUSH-GATE: riddler_veil ok ({len(marked)} marked parable(s) passed the veil)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
