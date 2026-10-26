"""Suite-wide isolation gate (B2-336, 2026-09-26).

Autouse fixture: every test runs with MAG_GAPS_LOG pointing at a tmp_path
file, so a test (or a future refactor of one) calling track_loop_gap without
a local monkeypatch lands its row in tmp and leaves
memory/training/loop_gaps.jsonl byte-still. This makes pollution structurally
impossible instead of per-test discipline (the B2-79 fix isolated one test via
its own monkeypatch; this closes the class).

Cause-and-evidence live in mag/temperature_stack.py _gaps_log (the seam the
fixture aims) and watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md.

Future sibling env overrides (MAG_SEAT_CRASH_LOG and the next isolation seam
per mag/env_redirect.py REDIRECT_VARS) belong here as they land - one fixture
per seam, same tmp_path discipline. Tests that deliberately exercise the
production-path seam (test_env_redirect_tripwire.py) override the override
locally with monkeypatch.delenv or setenv; the fixture does not fight them
because it runs before the test body sets its own env.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

# HEADLESS DEFAULT (2026-09-28, operator: "I've been asking you for months,
# whenever you invent a new test you forget") — the session-wide cure, not
# per-call discipline: every subprocess spawn launched under pytest gets
# CREATE_NO_WINDOW by default on win32.
#
# FIX (2026-09-29, wave5 suite-burn): this used to be a LOCAL function wrapper
# replacing subprocess.Popen, and that parallel mechanism broke the suite:
# mag/headless.py:24 captures subprocess.Popen at first import under pytest
# (the function wrapper), then install_no_window_defaults' `class
# _Popen(_REAL_Popen)` (mag/headless.py:72) raised "TypeError: function()
# argument 'code' must be code, not str" for every caller - f-15 + s2-19
# full-suite runs 2026-09-28: casualties tests/test_swarm_quota_gate.py x2
# (via mag/swarm_worker.py:380/:553) and tests/test_write_strip.py x1 (via
# main.py:39). headless.py:66-69 documents why the wrapper MUST be a class
# (asyncio.windows_utils subclasses subprocess.Popen). Root fix: ONE
# mechanism at the choke point - delegate to the estate's canonical
# installer (2026-08-10) instead of keeping a drifted copy. It is
# idempotent, wraps the TRUE originals captured at its own module import,
# ORs CREATE_NO_WINDOW into explicit flags (same guarantee the function
# wrapper gave), and additionally covers subprocess.run. The headless-law
# ratchet test counts debt downward separately; this call is what makes the
# operator's desktop quiet TONIGHT.
if sys.platform == "win32":
    from pathlib import Path as _Path

    _ROOT = _Path(__file__).resolve().parents[1]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))
    from mag.headless import install_no_window_defaults

    install_no_window_defaults()

# CHAIN_XDIST_GROUP (2026-09-27): these modules read/append SHARED on-disk
# state — the verkle chain (CHAIN_RACE_REPAIR_20260927) and the supervisor
# pipe registry (supervision soak: PIPE_DIR races across workers, found in
# the 2026-09-27 evening full-suite verification: 1 failed at -n auto,
# green solo). One xdist_group serializes exactly these modules across
# workers; the rest of the suite stays parallel. No-op when xdist is
# absent or running single-worker.
_SERIAL_STATE_MODULES = frozenset({
    "test_memlang",
    "test_party_subchain",
    "test_verkle_artifact",
    "test_verkle_audit",
    "test_verkle_compaction",
    "test_verkle_lock",
    "test_wave_driver",
    "test_falsifier_ledger",
    "test_frontier_council",
    "test_desk_baseline_probe",
    "test_supervision_soak",
})


def pytest_collection_modifyitems(config, items):
    try:
        import xdist  # noqa: F401
    except ImportError:
        return
    for item in items:
        mod = item.module.__name__.rsplit(".", 1)[-1]
        if mod in _SERIAL_STATE_MODULES:
            item.add_marker(pytest.mark.xdist_group(name="verkle-chain"))


@pytest.fixture(autouse=True)
def _isolate_gap_log(tmp_path, monkeypatch):
    log = tmp_path / "loop_gaps.jsonl"
    monkeypatch.setenv("MAG_GAPS_LOG", str(log))
    yield log


# LIVE-ESTATE WRITE FENCE (2026-10-14/15, after the verkle chain overwrite):
# tests/test_merkle_cure_p4b_sized.py called _hand_chain() without its
# `estate` fixture, so vk.CHAIN/vk.TIP stayed on the LIVE memory/biography/
# paths and every pytest run reset the real provenance chain to a 3-row
# fixture (first seen 2026-10-07 ~15:12-15:29 ET; at least twice; receipt
# watch/inbox/mates_leave_protocol/receipts/receipt_20261010_archaeologist.md,
# restore plan /workspace/mag-archaeology-oct/CHAIN_RESTORE_PLAN.md).
# Per-test discipline failed, so this closes the class: a Python audit hook
# (fires beneath open(), Path.write_*, os.open, os.rename/replace/remove,
# shutil.rmtree) refuses any WRITE under the real memory/biography,
# memory/biography_backup, memory/runs and state/ while a test runs. Reads
# stay allowed. Tests that need those paths must redirect them to tmp_path
# (monkeypatch the module constants), exactly like the `estate` fixture.
# Escape hatch for a deliberate, operator-approved run: MAG_ALLOW_LIVE_WRITES=1.
import os as _os
from pathlib import Path as _FencePath

_FENCE_ROOT = _FencePath(__file__).resolve().parents[1]
_FENCED_DIRS = tuple(
    (_FENCE_ROOT / rel).resolve()
    for rel in ("memory/biography", "memory/biography_backup", "memory/biography_v2",
                "memory/runs", "state")
)
_FENCE_ON = {"on": False}
_WRITE_FLAGS = _os.O_WRONLY | _os.O_RDWR | _os.O_APPEND | _os.O_CREAT | _os.O_TRUNC
_FS_EVENTS = {"os.rename", "os.replace", "os.remove", "os.rmdir", "shutil.rmtree", "shutil.move"}


def _is_fenced(p) -> bool:
    if p is None or isinstance(p, int):
        return False
    try:
        rp = _FencePath(_os.fsdecode(p)).resolve()
    except Exception:  # noqa: BLE001
        return False
    return any(rp == d or d in rp.parents for d in _FENCED_DIRS)


def _live_estate_audit(event, args):
    if not _FENCE_ON["on"] or (event != "open" and event not in _FS_EVENTS):
        return
    if _os.environ.get("MAG_ALLOW_LIVE_WRITES") == "1":
        return
    if event == "open":
        path, mode, flags = args
        writes = (isinstance(mode, str) and any(c in mode for c in "wax+")) or bool((flags or 0) & _WRITE_FLAGS)
        if writes and _is_fenced(path):
            raise PermissionError(f"live-estate write fence: a test tried to write {path!s}")
    else:
        for a in args[:2]:
            if isinstance(a, (str, bytes, _os.PathLike)) and _is_fenced(a):
                raise PermissionError(f"live-estate write fence: {event} on {a!s}")


sys.addaudithook(_live_estate_audit)  # audit hooks cannot be removed; gated by _FENCE_ON


@pytest.fixture(autouse=True, scope="session")
def _live_estate_write_fence():
    _FENCE_ON["on"] = True
    yield
    _FENCE_ON["on"] = False
