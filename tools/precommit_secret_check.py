#!/usr/bin/env python3
"""precommit_secret_check — staged-secret gate (P0 containment, audit 2026-09-30 #1).

Law: no live .env VALUE may be committed in any staged blob. The method is the
audit's own: substring match of live .env values against staged content.

Laws obeyed:
  - Values are NEVER printed, logged, or embedded in output — env var NAMES only.
  - Fail closed: exit 2 (cannot verify) when there is no repo, no parsable .env,
    or git itself fails — the same fail-closed contract as the census patrol.
  - Parser is imported from mag.trajectory_step (the hook's own redaction parser):
    one law, no drift between write-side redaction and commit-side gate.

Exits: 0 = clean · 1 = live value staged (blocks the commit) · 2 = cannot verify.

Env override MAG_ENV_FILE: alternate env file (absolute path). Exists so tests
run against a synthetic fake-key fixture, never a real value.

Wired by githooks/pre-commit (core.hooksPath=githooks makes .git/hooks inert).
Receipt: watch/inbox/last_mile_20260930/AG1_SECRETS_CONTAINMENT.md
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # reuse the hook's parser: one law, no drift
from mag.trajectory_step import redactions  # noqa: E402

# Non-secret env names (audit 2026-09-30 §7 classed these as non-secret values;
# hosts/uris/client-ids/model-names appear legitimately in config defaults).
# Suffix conventions cover future additions; exact names are the audit's list.
NON_SECRET_SUFFIXES = ("_HOST", "_URI", "_URL", "_MODEL", "_ClientID")
# 2026-10-20: public identity values, not credentials. GHOST_X_HANDLE is an X
# (Twitter) handle quoted verbatim inside two sealed receipts; the gate treated
# it as a live secret and refused every commit that touched watch/inbox.
NON_SECRET_NAMES = {"OLLAMA_HOST", "X_ClientID", "X_REDIRECT_URI", "AOS_AGENT_MODEL",
                    "GHOST_X_HANDLE"}


def _is_non_secret(name: str) -> bool:
    return name in NON_SECRET_NAMES or name.endswith(NON_SECRET_SUFFIXES)


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def main() -> int:
    here = _git(["rev-parse", "--show-toplevel"], Path.cwd())
    if here.returncode != 0:
        print("precommit_secret_check: cannot verify — not a git repo (exit 2)")
        return 2
    repo_dir = Path(here.stdout.strip())

    env_file = Path(os.environ.get("MAG_ENV_FILE") or (ROOT / ".env"))
    pairs = [(n, v) for n, v in redactions(env_file) if not _is_non_secret(n)]
    if not pairs:
        # .env missing or empty of parsable values: the gate would silently
        # pass everything. Fail closed (exit 2), never vacuous-pass.
        print(f"precommit_secret_check: cannot verify — no live values parsed from {env_file.name} (exit 2)")
        return 2

    staged = _git(["diff", "--cached", "--name-only", "-z", "--diff-filter=d"], repo_dir)
    if staged.returncode != 0:
        print("precommit_secret_check: cannot verify — git diff failed (exit 2)")
        return 2
    paths = [p for p in staged.stdout.split("\0") if p]
    if not paths:
        return 0  # nothing staged — nothing to leak

    # Large-blob gate (2026-10-24). The repo was carrying 15 GB of >32MB blobs
    # (a 4.6 GB crawl list, 2.5 GB indexes, a 2.3 GB tar). Every repack died on
    # them: one aborted pack went corrupt, 25 tmp_packs were left behind
    # (6.6 GB), and `git gc --auto` thrashed for days. A commit surface that
    # accepts a 4.6 GB text file is not a commit surface.
    max_blob = int(os.environ.get("MAG_MAX_BLOB_MB", "32")) * 1_000_000
    big = []
    for p in paths:
        fp = repo_dir / p
        if fp.is_file():
            size = fp.stat().st_size
            if size > max_blob:
                big.append((size, p))
    if big:
        for size, p in sorted(big, reverse=True)[:8]:
            print(f"precommit_secret_check: REFUSED — {size / 1e6:.0f} MB blob: {p}")
        print(f"large-file gate: {len(big)} staged blob(s) over {max_blob // 1_000_000} MB. "
              f"Data lakes stay on disk; set MAG_MAX_BLOB_MB to override deliberately.")
        return 1

    hits: list[tuple[str, str]] = []
    # 2026-10-20: two failed shapes before this one.
    #  (a) `git show :<path>` PER STAGED FILE: 13k subprocesses, 40+ min, held
    #      index.lock and starved every later sweep.
    #  (b) `git grep --cached <value>`: scans the WHOLE index (~150k entries),
    #      not just staged paths - still minutes per value.
    # One `git cat-file --batch` reads exactly the staged blobs, binary-safe.
    import subprocess as _sp
    req = "".join(f":{p}\n" for p in paths).encode("utf-8")
    proc = _sp.run(["git", "cat-file", "--batch"], cwd=str(repo_dir),
                   input=req, capture_output=True)
    if proc.returncode != 0:
        print("precommit_secret_check: cannot verify — cat-file failed (exit 2)")
        return 2
    data = proc.stdout
    offset = 0
    for path in paths:
        nl = data.find(b"\n", offset)
        if nl < 0:
            break
        header = data[offset:nl].split()
        offset = nl + 1
        if len(header) < 3:  # "<spec> missing"
            continue
        try:
            size = int(header[2])
        except ValueError:
            continue
        content = data[offset:offset + size]
        offset += size + 1  # skip the trailing newline after the blob
        for name, value in pairs:
            if value and value.encode("utf-8", "replace") in content:
                hits.append((path, name))

    if hits:
        print("precommit_secret_check: FAIL — live secret value(s) staged (names only, never values)")
        for path, name in hits:
            print(f"  {path}: contains live value of {name}")
        print("  Fix: git rm --cached / unstage the file, redact, re-add.")
        print("  Rotate any key that already touched history (operator call; no history rewrite).")
        return 1

    print(f"precommit_secret_check: PASS — {len(paths)} staged file(s) clean "
          f"against {len(pairs)} live env value(s) from {env_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
