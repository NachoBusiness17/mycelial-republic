"""Contained Python execution for the shell door (tools/__init__.py TOOL_MAP "run_python").

Port-order lane P4 (2026-10-07, watch/inbox/port_wave_20261007/p4_shell_door.md).
The old door was a five-pattern substring ban plus a tempdir cwd, self-described
"still not a full sandbox" (tools/code_execution.py:42-47 of the old revision).
The steal round measured the boundary ABSENT: a snippet using only open() with a
literal absolute path wrote a marker OUTSIDE the tempdir with ok=True, exit 0
(probe runner: watch/inbox/frontier_olm_2026-10-07/steal/shell_escape_probe_runner.py,
banked marker: shell_escape_probe.txt). This revision moves enforcement from the
prompt-shaped ban into the spawn. Containment layers, in order:

  L1 pre-exec static allowlist (tools/exec_gate.py): parse the snippet AST,
     resolve + normalize every literal path used in a write-capable call,
     refuse any absolute path outside the owned run root (exit 125). Closes
     the original exploit class before any process exists.
  L2 secondary lint (DEMOTED): the five substring bans stay as a cheap lint,
     exit 126. They are redundancy, NOT the containment; computed paths, plain
     open(), os.popen and friends sailed past them, which is why L1/L3/L4 exist.
  L3 spawn containment (tools/exec_job.py, win32): child runs with
     CREATE_NO_WINDOW in a filtered env (inherited) inside OUR owned run root
     (tempdir/lsa_exec_root/<id>), bound to a Job Object (pywin32 if present,
     ctypes otherwise) with KILL_ON_JOB_CLOSE + a process memory cap + UI
     restrictions (clipboard, global atoms, exit windows). On timeout the
     whole job tree is terminated. Job Objects give memory + kill semantics
     only; they do NOT sandbox the filesystem, network, or registry on Windows
     without a container, so:
  L4 post-exec audit: a random-byte canary is placed beside the run (sibling of
     the tempdir) and hash-checked after the run; the run root top level is
     walked and any entry that is not a live run dir or its canary is flagged.
     Any L4 hit (or job setup failure) fails LOUD: exit 125, violation row in
     the result dict and appended to logs/exec_shell_violations.jsonl.

Authorization stays one level up: mag/effect_broker.py authorizes effects
(model_call / lane_spawn / board_write classes); it is read here as the
authorization layer and intentionally NOT modified by this lane. The broker
authorizes WHAT runs; this door constrains WHERE the shell can reach.

Honest limits (measured, not claimed): assignment of the child to the job is
Popen-then-AssignProcessToJobObject, leaving a microseconds race before the job
binds (the static gate runs before any process exists, so the exploit class the
steal proved is refused pre-exec regardless); the static gate sees only literal
paths (computed paths fall to L4 and the job caps); the canary detects writes to
its own path and run-root pollution, not arbitrary far-field writes; on
non-win32 there is no Job Object (gate + audit still run and the containment
metadata says so).
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

from config import MAX_TOOL_OUTPUT, ROOT

from tools.exec_gate import static_path_gate
from tools.exec_job import Job, mem_cap_bytes


# Exit codes: 124 timeout (historical), 125 containment violation (this lane),
# 126 banned-pattern lint (demoted secondary layer, historical code kept).
_EXIT_TIMEOUT = 124
_EXIT_CONTAINMENT = 125
_EXIT_LINT = 126

# Run root: everything the shell door spawns lives inside this owned directory,
# including the canary that sits beside each run. This is also the L1 gate's
# declared writable root.
_RUN_ROOT_NAME = "lsa_exec_root"
_RUN_DIR_PREFIX = "lsa_exec_"

_VIOLATION_LOG = ROOT / "logs" / "exec_shell_violations.jsonl"


# ---------------------------------------------------------------------------
# Preamble injected into every snippet so agents don't re-implement file I/O
# boilerplate (the dominant PATCH-VERIFY loop from session mining 2026-08-03).
_PREAMBLE = r'''
import os, sys, json
from pathlib import Path
ROOT = Path(r"{root}")
def P(*parts):
    """Join path parts under ROOT."""
    return str(ROOT.joinpath(*parts))
def dump_lines(path, line_from=None, line_to=None):
    """Print a numbered region of a file (1-indexed, clamps to EOF)."""
    p = Path(path) if os.path.isabs(path) else ROOT.joinpath(path)
    if not p.is_file():
        print(f"[dump_lines] missing: {{p}}")
        return
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    total = len(lines)
    lo = (line_from or 1) - 1
    hi = (line_to or total) if line_to else total
    lo = max(0, lo); hi = min(total, hi)
    for i in range(lo, hi):
        print(f"{{i+1}}: {{lines[i]}}")
    print(f"[dump_lines] {{p}} total={{total}} shown={{hi-lo}}")
'''.format(root=str(ROOT).replace("\\", "\\\\"))


# ---------------------------------------------------------------------------
# L2 secondary lint (DEMOTED). These five substrings were the OLD door's entire
# containment ("Soft refuse ... still not a full sandbox", old :42-47). They are
# kept only as a cheap redundancy layer: a snippet that trips them never needs
# the heavier machinery, but nothing about the estate's safety rides on them.
# A snippet using plain open(), os.popen, computed paths or double-quoted
# __import__("os") passes this lint by construction (steal round evidence).
_BANNED_PATTERNS = ("socket.socket", "subprocess", "os.system", "shutil.rmtree",
                    "__import__('os')")


def banned_pattern_lint(code: str) -> list[str]:
    """Return the demoted lint hits. Redundancy layer, never load-bearing."""
    return [b for b in _BANNED_PATTERNS if b in code]


# ---------------------------------------------------------------------------
# L4 post-exec audit plumbing + loud failure
def _append_violation(row: dict) -> None:
    """Bank the violation row where a human/patrol can find it. Never masks."""
    try:
        _VIOLATION_LOG.parent.mkdir(parents=True, exist_ok=True)
        with _VIOLATION_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as exc:
        row["ledger_error"] = str(exc)


def _violation_result(row: dict, code_head: str) -> dict:
    row["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    row["code_head"] = code_head[:200]
    _append_violation(row)
    return {
        "ok": False,
        "exit_code": _EXIT_CONTAINMENT,
        "error": f"containment violation: {row['kind']}: {row.get('detail', '')}",
        "violation": row,
    }


def _run_root() -> Path:
    root = Path(tempfile.gettempdir()) / _RUN_ROOT_NAME
    root.mkdir(parents=True, exist_ok=True)
    return root


def _audit_run(root: Path, run_dir: Path, canary_path: Path, canary_sha: str) -> Optional[dict]:
    """L4: canary hash + run-root pollution walk. First hit wins (loud)."""
    try:
        digest = hashlib.sha256(canary_path.read_bytes()).hexdigest()
    except OSError:
        digest = None
    if digest != canary_sha:
        return {
            "kind": "canary_tamper" if digest is not None else "canary_missing",
            "detail": f"canary beside the run was touched: {canary_path.name}",
        }
    for entry in root.iterdir():
        if entry == run_dir:
            continue
        if entry.is_dir() and entry.name.startswith(_RUN_DIR_PREFIX):
            continue  # a sibling live run (or a stale one), pattern-legit
        if entry.is_file() and entry.name.startswith(_RUN_DIR_PREFIX) and entry.name.endswith(".canary"):
            continue  # a sibling canary
        return {
            "kind": "run_root_pollution",
            "detail": f"unexpected entry beside the run: {entry.name}",
        }
    return None


# ---------------------------------------------------------------------------
# The door.
def run_python(code: str, timeout: int = 30) -> dict:
    if not code or not code.strip():
        return {"ok": False, "exit_code": 1, "error": "empty code"}
    code_head = code.strip()

    # L1 pre-exec static allowlist (containment, exit 125).
    gate_hits = static_path_gate(code, str(_run_root()))
    if gate_hits:
        return _violation_result(gate_hits[0], code_head)

    # L2 demoted lint (exit 126). Redundant with L1/L3/L4, kept cheap-first.
    for b in banned_pattern_lint(code):
        return {
            "ok": False,
            "exit_code": _EXIT_LINT,
            "error": f"banned pattern (secondary lint, not the containment): {b}",
        }

    root = _run_root()
    run_dir = Path(tempfile.mkdtemp(prefix=_RUN_DIR_PREFIX, dir=str(root)))
    canary_path = root / f"{run_dir.name}.canary"
    canary_bytes = secrets.token_bytes(32)
    canary_sha = hashlib.sha256(canary_bytes).hexdigest()
    canary_path.write_bytes(canary_bytes)
    pre_names = {e.name for e in root.iterdir()}  # snapshot for the post-audit sweep

    script = run_dir / "snippet.py"
    script.write_text(_PREAMBLE + "\n" + code, encoding="utf-8")

    # HEADLESS (2026-08-10): use the REAL interpreter (not the venv shim,
    # which doubles + windows) and CREATE_NO_WINDOW so run_python never pops
    # a console window in the stateless auto-loop.
    try:
        from mag.headless import PYTHON as _PY
    except Exception:
        _PY = sys.executable

    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0
    env = {
        # TEMP/TMP/SYSTEMDRIVE ride along so the child's own tempfile.gettempdir()
        # resolves to the SAME root the parent used to build the run dir; without
        # them the child falls back to C:\\Windows\\Temp and computed paths in
        # snippets silently diverge from the audited root.
        **dict(**{k: v for k, v in os.environ.items() if k in ("SYSTEMROOT", "SYSTEMDRIVE", "TEMP", "TMP", "PATH", "PYTHONPATH") or k.startswith("PYTHON")}),
    }

    job: Optional[Job] = None
    if sys.platform == "win32":
        try:
            job = Job(mem_cap_bytes())
        except (ImportError, OSError) as exc:
            # Containment promised but not deliverable: fail LOUD, no silent
            # degrade to the uncontained spawn (no fallback-branch creep).
            result = _violation_result({
                "kind": "job_setup_failed",
                "detail": f"job object could not be created: {exc}",
            }, code_head)
            result["cleanup_errors"] = _cleanup_run(root, run_dir, canary_path)
            return result

    violation: Optional[dict] = None
    cleanup_errors: list[str] = []
    out: Optional[str] = ""
    err: Optional[str] = ""
    returncode = 1
    try:
        proc = subprocess.Popen(
            [_PY, str(script)],
            cwd=str(run_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            text=True,
            env=env,
            creationflags=creationflags,
        )
        if job is not None:
            job.assign(proc._handle)  # type: ignore[attr-defined] # pywin32/ctypes take the win handle
        try:
            out, err = proc.communicate(timeout=timeout)
            returncode = proc.returncode
        except subprocess.TimeoutExpired:
            if job is not None:
                job.terminate()  # kills the WHOLE tree, grandchildren included
            out, err = proc.communicate()
            returncode = _EXIT_TIMEOUT
    except Exception as e:
        # Spawn machinery broke in an unknown state: refuse loud instead of
        # returning a maybe-clean result for a child that may have run.
        violation = {"kind": "spawn_error", "detail": str(e)}
    finally:
        if job is not None:
            job.close()  # KILL_ON_JOB_CLOSE backstop: tree dies with the handle
        if violation is None:
            violation = _audit_run(root, run_dir, canary_path, canary_sha)
        cleanup_errors = _cleanup_run(root, run_dir, canary_path, pre_names)

    if violation is not None:
        result = _violation_result(violation, code_head)
        if cleanup_errors:
            result["cleanup_errors"] = cleanup_errors
        return result

    out = (out or "") + (err or "")
    result = {
        "ok": returncode == 0 and returncode != _EXIT_TIMEOUT,
        "exit_code": returncode,
        "output": out[:MAX_TOOL_OUTPUT],
    }
    if cleanup_errors:
        result["cleanup_errors"] = cleanup_errors
    return result


def _cleanup_run(root: Path, run_dir: Path, canary_path: Path,
                 pre_names: Optional[set] = None) -> list[str]:
    """Post-audit sweep. Audit already banked any violation; this keeps the
    owned root clean so one caught escape cannot poison later audits. Entries
    that appeared during the run and are not pattern-legit run dirs or canaries
    are attacker bytes in OUR root: remove them. Sweep failures are returned,
    never swallowed (the caller surfaces them on the result)."""
    import shutil
    errors: list[str] = []

    def _rm(target: Path, what: str) -> None:
        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        except OSError as exc:
            errors.append(f"cleanup {what} failed: {exc}")

    for entry in list(root.iterdir()):
        if entry == run_dir or entry == canary_path:
            _rm(entry, entry.name)
            continue
        if pre_names is not None and entry.name not in pre_names:
            legit = (entry.name.startswith(_RUN_DIR_PREFIX)
                     and (entry.is_dir() or entry.name.endswith(".canary")))
            if not legit:
                _rm(entry, entry.name)
    return errors
