"""prepush_paths_changed -- the changed-path decision as one helper (B2-272).

githooks/pre-push had TWO hand-rolled changed-path gates (the violation
ratchet's changed_files and the B2-260 caption block's inline arms), and the
next hand-run verifier would want the same decision a third time. This is the
extracted decision, covering the five cases the B2-260 block tests:

  (a) dirty vs HEAD for any pathspec
  (b) untracked file under any pathspec
  (c) pushed-commit range touches any pathspec
  (d) branch deletion (local sha all-zeros) -> no range to test
  (e) unborn remote (remote sha all-zeros) -> no range to test

INPUT CONTRACT: pre-push hands refs on stdin (per ref: local_ref local_sha
remote_ref remote_sha). The helper NEVER reads stdin -- another consumer may
own it (the caption block consumes it once and passes the already-read text
via --refs). Verdict mirrors `git diff --quiet`: exit 0 = UNCHANGED,
exit 1 = CHANGED, exit 2 = git broke (fail-closed like the ratchet's None).

CLI:
  tools/prepush_paths_changed.py --refs "$PUSH_INPUT" -- pathA pathB
  tools/prepush_paths_changed.py --selftest      # the five-case battery
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

ZERO = "0" * 40
# HEADLESS law (spawn_sites_no_window): every spawn carries CREATE_NO_WINDOW
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def _git(cwd: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=True, timeout=60, creationflags=HEADLESS)


def paths_changed(cwd: str, refs_text: str, pathspecs: list[str]) -> int:
    """Return 1 if any pathspec is changed by any arm, 0 if none, 2 on git failure."""
    if not pathspecs:
        print("UNCHANGED (no pathspecs)")
        return 0
    # (a) dirty vs HEAD
    r = _git(cwd, "diff", "--quiet", "HEAD", "--", *pathspecs)
    if r.returncode == 2 or (r.returncode not in (0, 1)):
        print(f"UNCHANGED? git failed: {(r.stderr or '').strip()[:160]}")
        return 2
    if r.returncode == 1:
        print("CHANGED (differs from HEAD)")
        return 1
    # (b) untracked
    r = _git(cwd, "ls-files", "--others", "--exclude-standard", "--", *pathspecs)
    if r.returncode != 0:
        print(f"UNCHANGED? git failed: {(r.stderr or '').strip()[:160]}")
        return 2
    if r.stdout.strip():
        print(f"CHANGED (untracked: {r.stdout.splitlines()[0]})")
        return 1
    # (c)/(d)/(e) pushed ref ranges, zero-sha guards
    toks = refs_text.split()
    for i in range(0, len(toks) - 3, 4):
        lsha, rsha = toks[i + 1], toks[i + 3]
        if lsha == ZERO or lsha == "":   # (d) branch deletion
            continue
        if rsha == ZERO or rsha == "":   # (e) unborn remote
            continue
        r = _git(cwd, "diff", "--quiet", rsha, lsha, "--", *pathspecs)
        if r.returncode == 2 or (r.returncode not in (0, 1)):
            print(f"UNCHANGED? git failed: {(r.stderr or '').strip()[:160]}")
            return 2
        if r.returncode == 1:
            print(f"CHANGED (pushed range {rsha[:8]}..{lsha[:8]})")
            return 1
    print("UNCHANGED")
    return 0


def selftest() -> int:
    """Build the five cases in a throwaway repo and assert the verdicts."""
    if shutil.which("git") is None:
        print("SELFTEST SKIP: no git")
        return 2
    tmp = tempfile.mkdtemp(prefix="prepush_paths_selftest_")
    results: list[tuple[str, int, int]] = []

    def git(*a: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *a], cwd=tmp, capture_output=True, text=True,
                              creationflags=HEADLESS)

    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    open(os.path.join(tmp, "gen.txt"), "w").write("v1\n")
    open(os.path.join(tmp, "ver.txt"), "w").write("v1\n")
    git("add", "-A")
    base = git("commit", "-q", "-m", "base")
    base_sha = git("revparse", "HEAD").stdout.strip() if base.returncode else git("rev-parse", "HEAD").stdout.strip()

    def run(refs: str) -> tuple[int, str]:
        r = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--refs", refs, "--",
             "gen.txt", "ver.txt"],
            cwd=tmp, capture_output=True, text=True, timeout=60,
            creationflags=HEADLESS)
        return r.returncode, (r.stdout + r.stderr)

    # case 1: dirty vs HEAD
    open(os.path.join(tmp, "gen.txt"), "a").write("dirty\n")
    rc, out = run("")
    results.append(("dirty-vs-HEAD", rc, 1))
    git("checkout", "-q", "--", "gen.txt")

    # case 2: untracked (a pathspec naming a file that was never committed)
    open(os.path.join(tmp, "new.txt"), "w").write("brand new\n")
    r2 = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--refs", "", "--",
         "gen.txt", "ver.txt", "new.txt"],
        cwd=tmp, capture_output=True, text=True, timeout=60,
        creationflags=HEADLESS)
    results.append(("untracked", r2.returncode, 1))
    os.remove(os.path.join(tmp, "new.txt"))

    # case 3: pushed range touches
    open(os.path.join(tmp, "gen.txt"), "a").write("committed\n")
    git("add", "-A")
    git("commit", "-q", "-m", "touch")
    new_sha = git("rev-parse", "HEAD").stdout.strip()
    rc, out = run(f"refs/heads/x {new_sha} refs/heads/x {base_sha}")
    results.append(("range-hit", rc, 1))

    # case 4: branch deletion (local sha zeros) on a clean tree
    rc, out = run(f"refs/heads/x {ZERO} refs/heads/x {base_sha}")
    results.append(("branch-deletion-zero-local", rc, 0))

    # case 5: unborn remote (remote sha zeros) on a clean tree
    rc, out = run(f"refs/heads/x {new_sha} refs/heads/x {ZERO}")
    results.append(("unborn-remote-zero-remote", rc, 0))

    ok = True
    for name, got, want in results:
        flag = "PASS" if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"{flag} {name}: rc={got} want={want}")
    shutil.rmtree(tmp, ignore_errors=True)
    print("ALL PASS (5 cases)" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Changed-path decision for pre-push gates (B2-272)")
    ap.add_argument("--refs", default="", help="already-consumed pre-push stdin text; never read stdin here")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("pathspecs", nargs="*")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    cwd = os.getcwd()
    return paths_changed(cwd, a.refs, a.pathspecs)


if __name__ == "__main__":
    raise SystemExit(main())
