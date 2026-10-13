"""Regression: gpipes/orchestrator supervision gap.

THE BUG (found live 2026-08-07): gpipes.fan_out() spawns workers then the
launcher exits immediately, killing the daemon _monitor threads that were
supposed to _finalize() tasks when the child process exited. The detached
supervisor only killed on timeout and never reaped, so finished workers stayed
in "running" forever and collectors waited until their cap.

THE FIX: orchestrator.reap_completed() marks running tasks whose pid is gone
as terminal, reading the seat's own mailbox status.json (phase/exit_code) to
classify done vs failed; gpipes.pipe_status() calls it first so status/collect/
supervise all surface terminal states promptly.

Hermetic: fake task records with dead pids + a temp TASK_DIR; no LLM/network.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mag import orchestrator as orc


def _isolate():
    tmp = tempfile.mkdtemp()
    old_tdir = orc.TASK_DIR
    old_logdir = orc.LOG_DIR
    old_trail = orc.TRAIL
    orc.TASK_DIR = orc.Path(tmp) / "tasks"
    orc.LOG_DIR = orc.Path(tmp) / "logs"
    orc.TRAIL = orc.Path(tmp) / "trail.jsonl"
    orc.TASK_DIR.mkdir(parents=True, exist_ok=True)
    orc.LOG_DIR.mkdir(parents=True, exist_ok=True)
    return old_tdir, old_logdir, old_trail, tmp


def _restore(old_tdir, old_logdir, old_trail):
    orc.TASK_DIR, orc.LOG_DIR, orc.TRAIL = old_tdir, old_logdir, old_trail


def _dead_task(task_id, pid=123456789):
    """Write a 'running' task whose pid is guaranteed dead (far-future pid)."""
    orc._save({
        "task_id": task_id,
        "status": "running",
        "pid": pid,
        "cmd": ["fake"],
        "created_at": orc._now(),
        "timeout_s": 900,
        "tag": "test",
        "detail": "",
    })
    assert orc._pid_alive(pid) is False, "test pid must be dead"


def test_reap_completed_classifies_done_from_status():
    """A finished worker that wrote status.json phase=done is reaped 'done'."""
    old_tdir, old_logdir, old_trail, tmp = _isolate()
    try:
        tid = "t-reap-done"
        _dead_task(tid)
        # Simulate the agent's own completion status in its mailbox.
        import mag.pigeonhole as ph
        ph.write_status(tid, phase="done", exit_code=0)

        res = orc.reap_completed()
        assert res.get("reaped") == 1, res
        assert res["classified"]["done"] == 1, res
        t = orc.task_status(tid)
        assert t.get("status") == "done", t
        assert t.get("exit_code") == 0, t
    finally:
        _restore(old_tdir, old_logdir, old_trail)


def test_reap_completed_classifies_failed_from_status():
    """A worker that reported phase=failed is reaped 'failed', not 'done'."""
    old_tdir, old_logdir, old_trail, tmp = _isolate()
    try:
        tid = "t-reap-fail"
        _dead_task(tid)
        import mag.pigeonhole as ph
        ph.write_status(tid, phase="failed", exit_code=1)

        res = orc.reap_completed()
        assert res["classified"]["failed"] == 1, res
        t = orc.task_status(tid)
        assert t.get("status") == "failed", t
        assert t.get("exit_code") == 1, t
    finally:
        _restore(old_tdir, old_logdir, old_trail)


def test_reap_completed_died_without_status():
    """No mailbox status -> reaped 'died' (still terminal, collector unblocks)."""
    old_tdir, old_logdir, old_trail, tmp = _isolate()
    try:
        tid = "t-reap-died"
        _dead_task(tid)

        res = orc.reap_completed()
        assert res["classified"]["died"] == 1, res
        t = orc.task_status(tid)
        assert t.get("status") == "died", t
        assert t.get("status") in orc.TERMINAL, t
    finally:
        _restore(old_tdir, old_logdir, old_trail)


def test_reap_completed_leaves_live_tasks_alone():
    """A running task with a live pid is NOT reaped."""
    old_tdir, old_logdir, old_trail, tmp = _isolate()
    try:
        import os as _os
        pid = _os.getpid()  # this test process is alive
        tid = "t-reap-live"
        orc._save({
            "task_id": tid,
            "status": "running",
            "pid": pid,
            "cmd": ["fake"],
            "created_at": orc._now(),
            "timeout_s": 900,
            "tag": "test",
            "detail": "",
        })
        res = orc.reap_completed()
        assert res.get("reaped") == 0, res
        t = orc.task_status(tid)
        assert t.get("status") == "running", t
    finally:
        _restore(old_tdir, old_logdir, old_trail)
