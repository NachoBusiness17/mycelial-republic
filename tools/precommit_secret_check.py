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
NON_SECRET_NAMES = {"OLLAMA_HOST", "X_ClientID", "X_REDIRECT_URI", "AOS_AGENT_MODEL"}


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

    hits: list[tuple[str, str]] = []
    for path in paths:
        blob = _git(["show", f":{path}"], repo_dir)
        if blob.returncode != 0:
            continue  # e.g. rename source side; destination path is checked itself
        content = blob.stdout  # errors=replace keeps ASCII key chars intact
        for name, value in pairs:
            if value in content:
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
