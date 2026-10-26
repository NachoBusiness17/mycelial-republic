"""Probe of RAG-OS anti-pattern 5 (BUILD-GUIDE.md:220): "prepend a deterministic
worktree-fingerprint stamp to every worker report and tell the synthesizer to
trust the stamp over the prose."

Spec is theirs (csnyder256/RAG-OS, MIT); this minimal implementation is this
lane's probe, stdlib-only, run with the estate venv. A tool-less worker claims
a file edit; the stamp must catch the fabrication because the bytes did not
change, and must pass a real edit.

Usage: python probe_ragos_fingerprint.py
"""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


def fingerprint(worktree: Path) -> str:
    """Deterministic hash over the tracked file set: rel path + content bytes."""
    h = hashlib.sha256()
    for p in sorted(worktree.rglob("*")):
        if p.is_file():
            rel = p.relative_to(worktree).as_posix()
            h.update(rel.encode("utf-8"))
            h.update(b"\0")
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def init_worktree(root: Path) -> None:
    (root / "app.py").write_text("print('v1')\n", encoding="utf-8")
    (root / "notes.md").write_text("# notes\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@x",
                    "commit", "-qm", "base"], cwd=root, check=True)


def fake_worker_report(worktree: Path) -> str:
    """A completion engine with no tools: claims an edit, changes nothing."""
    before = fingerprint(worktree)
    report = (
        "EDIT COMPLETE: app.py now prints 'v2'.\n"
        "  before: print('v1')\n"
        "  after:  print('v2')\n"
    )
    return f"[worktree-fingerprint {before}]\n{report}"


def main() -> int:
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "wt"
        root.mkdir()
        init_worktree(root)

        base = fingerprint(root)
        report = fake_worker_report(root)
        after = fingerprint(root)
        claimed_changed = "EDIT COMPLETE" in report
        disk_changed = base != after
        fabricated = claimed_changed and not disk_changed
        print(f"base stamp      : {base}")
        print(f"report stamp    : {report.splitlines()[0]}")
        print(f"disk changed    : {disk_changed}")
        print(f"prose claims    : edit complete")
        print(f"FABRICATION CAUGHT: {fabricated}")
        ok = ok and fabricated

        # real edit: the stamp must move
        (root / "app.py").write_text("print('v2')\n", encoding="utf-8")
        after2 = fingerprint(root)
        print(f"stamp after real edit: {after2} (moved={base != after2})")
        ok = ok and (base != after2)

    print("PROBE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
