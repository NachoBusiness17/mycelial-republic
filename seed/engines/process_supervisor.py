#!/usr/bin/env python3
"""PROCESS SUPERVISOR — one-shot sub-agent processes, crash containment, file-mailbox steering.

Standalone stdlib module (no estate imports). Steal-shape rebuild of the sub-agent
orchestrator pattern. THE PROBLEM it solves: one window/process running every task means
one runaway loop or hung provider kills the whole session. THE FIX: each task is a FRESH
one-shot agent process; this supervisor spawns, monitors, steers, and reaps them. A
sub-agent crash kills ONLY that process — the supervisor survives, records the failure,
and the operator retries or escalates.

Design laws (each earned the hard way in the source estate):
  - stdin is DEVNULL in every child. Sub-agents never read stdin; else they hang on input().
  - Steering is a FILE MAILBOX (mail/<task_id>/inbox.txt), not a pipe, not a timer:
    children that know the protocol read the inbox and touch mail/<task_id>/heartbeat;
    for arbitrary children, the log file's mtime is the heartbeat proxy. Any output = alive.
  - Heartbeat staleness with NUDGE-BEFORE-KILL: silence past stale_after_s posts a nudge
    line into the inbox; still silent past nudge_grace_s -> kill as "stalled". The hard
    timeout is only the final backstop.
  - Per-seat reap exceptions: pid-less "external" seats (GUI/mailbox work registered by
    other surfaces) are reaped on stale heartbeat AFTER external_stale_s — EXCEPT seats
    in no_reap_seats (human-paced work, closed explicitly via `done`).
  - Terminal states: done / failed / timeout / stalled / killed / died. Nothing else.

Children are any one-shot entrypoint: cmd is a list; "{goal}" is substituted.
    Supervisor(root).spawn([sys.executable, "agent.py", "--query", "{goal}"], goal="...")

CLI:
    python engines/process_supervisor.py spawn --cmd "python agent.py --query {goal}" --goal "..." [--timeout N] [--tag T]
    python engines/process_supervisor.py list | status ID | watch ID | steer ID "text" | pause ID | continue ID | kill ID | reap
    python engines/process_supervisor.py queue add --cmd "..." --goal "..." [--tier mission|research|maintenance|filler] [--priority N]
    python engines/process_supervisor.py queue list | queue status | drain [--once]
    python engines/process_supervisor.py self-test
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TERMINAL = {"done", "failed", "timeout", "stalled", "killed", "died"}
TIER_RANK = {"mission": 0, "research": 1, "maintenance": 2, "filler": 3}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Supervisor:
    def __init__(self, root=None, *, stale_after_s: float = 90.0, nudge_grace_s: float = 60.0,
                 poll_s: float = 1.0, external_stale_s: float = 300.0,
                 no_reap_seats=None, default_timeout: float = 900.0):
        self.root = Path(root) if root else ROOT / "state" / "supervisor"
        self.tasks_dir = self.root / "tasks"
        self.queue_dir = self.root / "queue"
        self.logs_dir = self.root / "logs"
        self.mail_dir = self.root / "mail"
        self.trail_path = self.root / "trail.jsonl"
        self.stale_after_s = float(stale_after_s)
        self.nudge_grace_s = float(nudge_grace_s)
        self.poll_s = float(poll_s)
        self.external_stale_s = float(external_stale_s)
        self.no_reap_seats = set(no_reap_seats or ())
        self.default_timeout = float(default_timeout)

    # ------------------------------------------------------------------ plumbing
    def _ensure(self) -> None:
        for d in (self.tasks_dir, self.queue_dir, self.logs_dir, self.mail_dir):
            d.mkdir(parents=True, exist_ok=True)

    def _task_path(self, task_id: str) -> Path:
        return self.tasks_dir / (task_id + ".json")

    def _load(self, task_id: str):
        p = self._task_path(task_id)
        if not p.is_file():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _save(self, task: dict) -> None:
        self._ensure()
        task["updated_at"] = _now()
        self._task_path(task["task_id"]).write_text(
            json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")

    def _trail(self, event: str, task_id: str, **meta) -> None:
        self._ensure()
        row = {"ts": _now(), "event": event, "task_id": task_id, **meta}
        with self.trail_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    def mailbox(self, task_id: str) -> Path:
        return self.mail_dir / task_id / "inbox.txt"

    def heartbeat_path(self, task_id: str) -> Path:
        return self.mail_dir / task_id / "heartbeat"

    def read_mailbox(self, task_id: str) -> str:
        p = self.mailbox(task_id)
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    def _post_mail(self, task_id: str, line: str) -> None:
        p = self.mailbox(task_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as fh:
            fh.write(line.rstrip("\n") + "\n")

    # ------------------------------------------------------------------ lifecycle
    def spawn(self, cmd, *, goal: str = "", timeout: float | None = None,
              tag: str = "", seat: str | None = None) -> dict:
        """Spawn ONE one-shot child process. Returns the task record immediately."""
        if not cmd:
            return {"ok": False, "error": "empty cmd"}
        self._ensure()
        timeout = float(timeout or self.default_timeout)
        task_id = "t" + uuid.uuid4().hex[:10]
        cmd = [str(c).replace("{goal}", goal or "") for c in cmd]
        log_path = self.logs_dir / (task_id + ".out.log")
        log_fh = log_path.open("a", encoding="utf-8", errors="replace")
        log_fh.write("--- %s spawn: %s\n" % (_now(), " ".join(cmd)))
        log_fh.flush()
        task = {
            "task_id": task_id, "tag": tag, "goal": goal[:500], "cmd": cmd,
            "status": "running", "source": "local", "seat": seat,
            "created_at": _now(), "started_at": None, "ended_at": None,
            "exit_code": None, "timeout_s": timeout, "log": str(log_path),
            "mailbox": str(self.mailbox(task_id)), "pid": None, "paused": False,
            "detail": "",
        }
        self._save(task)
        flags = 0
        if sys.platform == "win32":
            flags = (getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
                     | getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000))
        try:
            proc = subprocess.Popen(
                cmd, stdout=log_fh, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,  # sub-agents never read stdin
                cwd=str(self.root), creationflags=flags)
        except Exception as e:
            log_fh.close()
            return self._finalize(task_id, "failed", detail="spawn error: " + str(e)) or task
        task = self._load(task_id) or task
        task["pid"] = proc.pid
        task["started_at"] = _now()
        self._save(task)
        self._trail("spawn", task_id, pid=proc.pid, timeout_s=timeout)
        threading.Thread(target=self._monitor, args=(task_id, proc, log_fh, timeout),
                         daemon=True).start()
        return self._load(task_id) or task

    def _kill_tree(self, pid: int) -> None:
        if sys.platform == "win32":
            try:
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                               capture_output=True, timeout=30)
            except Exception:
                pass
        else:
            try:
                os.kill(pid, 9)
            except (ProcessLookupError, PermissionError):
                pass

    def _heartbeat_age(self, task: dict) -> float | None:
        """Seconds since the last sign of life: newest of log mtime, mailbox heartbeat
        mtime, started_at. None = nothing to read from (treat as healthy-unknown)."""
        stamps = []
        started = task.get("started_at")
        if started:
            stamps.append(_parse(started))
        log = task.get("log")
        if log and os.path.isfile(log):
            stamps.append(os.path.getmtime(log))
        hb = self.heartbeat_path(task["task_id"])
        if hb.is_file():
            stamps.append(hb.stat().st_mtime)
        if not stamps:
            return None
        return max(0.0, time.time() - max(stamps))

    def _monitor(self, task_id: str, proc, log_fh, timeout: float) -> None:
        """Exit -> done/failed. Hard timeout -> kill. Heartbeat silence -> nudge once,
        then kill as stalled. A paused task is not judged for staleness."""
        started = time.time()
        nudged_at: float | None = None
        while True:
            rc = proc.poll()
            if rc is not None:
                log_fh.close()
                self._finalize(task_id, "done" if rc == 0 else "failed", exit_code=rc,
                               detail="exit" if rc == 0 else "non-zero exit %s" % rc)
                return
            elapsed = time.time() - started
            if elapsed > timeout:
                self._kill_tree(proc.pid)
                log_fh.close()
                self._finalize(task_id, "timeout", detail="exceeded %ss" % timeout)
                return
            task = self._load(task_id) or {}
            if task.get("paused"):
                nudged_at = None
                time.sleep(self.poll_s)
                continue
            age = self._heartbeat_age(task)
            if age is not None and age > self.stale_after_s:
                if nudged_at is None:
                    nudged_at = time.time()
                    self._post_mail(task_id, "→ %s supervisor: STALL NUDGE — no heartbeat for "
                                    "%.0fs; re-anchor and write your heartbeat file, or this "
                                    "task is killed as stalled." % (_now(), age))
                    self._trail("stall-nudge", task_id, age_s=round(age, 1))
                elif time.time() - nudged_at > self.nudge_grace_s:
                    self._kill_tree(proc.pid)
                    log_fh.close()
                    self._finalize(task_id, "stalled", detail="no heartbeat for %.0fs (nudged)" % age)
                    return
            else:
                nudged_at = None
            time.sleep(self.poll_s)

    def _finalize(self, task_id: str, status: str, exit_code=None, detail: str = ""):
        task = self._load(task_id)
        if not task or task.get("status") in TERMINAL:
            return task
        task["status"] = status
        task["exit_code"] = exit_code
        task["detail"] = detail
        task["ended_at"] = _now()
        self._save(task)
        self._trail(status, task_id, exit_code=exit_code, detail=detail[:200])
        return task

    # ------------------------------------------------------------------ steering
    def steer(self, task_id: str, text: str) -> dict:
        task = self._load(task_id)
        if not task:
            return {"ok": False, "error": "no such task"}
        self._post_mail(task_id, "→ %s supervisor: %s" % (_now(), text))
        self._trail("steer", task_id, chars=len(text))
        return {"ok": True, "task_id": task_id, "mailbox": str(self.mailbox(task_id))}

    def pause(self, task_id: str) -> dict:
        task = self._load(task_id)
        if not task:
            return {"ok": False, "error": "no such task"}
        task["paused"] = True
        self._save(task)
        self._post_mail(task_id, "→ %s supervisor: PAUSE (staleness judgment suspended)" % _now())
        self._trail("pause", task_id)
        return {"ok": True, "task_id": task_id, "paused": True}

    def continue_(self, task_id: str) -> dict:
        task = self._load(task_id)
        if not task:
            return {"ok": False, "error": "no such task"}
        task["paused"] = False
        self._save(task)
        self._post_mail(task_id, "→ %s supervisor: CONTINUE" % _now())
        self._trail("continue", task_id)
        return {"ok": True, "task_id": task_id, "paused": False}

    def touch(self, task_id: str) -> dict:
        """External seats renew their liveness through here."""
        task = self._load(task_id)
        if not task:
            return {"ok": False, "error": "no such task"}
        task["last_seen_at"] = _now()
        self._save(task)
        return {"ok": True, "task_id": task_id}

    def watch(self, task_id: str) -> str:
        task = self._load(task_id)
        if not task:
            return "no such task %s" % task_id
        age = self._heartbeat_age(task)
        alive = "?"
        if task.get("pid"):
            alive = "yes" if _pid_alive(task["pid"]) else "no"
        tail = ""
        log = task.get("log")
        if log and os.path.isfile(log):
            lines = open(log, encoding="utf-8", errors="replace").read().splitlines()
            tail = "\n".join(lines[-5:])
        return ("[%s] status=%s paused=%s pid=%s alive=%s heartbeat_age=%s\nmailbox: %s\n%s"
                % (task_id, task.get("status"), task.get("paused"), task.get("pid"), alive,
                   "n/a" if age is None else "%.0fs" % age,
                   task.get("mailbox"), tail))

    def kill(self, task_id: str) -> dict:
        task = self._load(task_id)
        if not task:
            return {"ok": False, "error": "no such task"}
        if task.get("pid") and task.get("status") not in TERMINAL:
            self._kill_tree(int(task["pid"]))
        self._finalize(task_id, "killed", detail="killed by operator")
        return {"ok": True, "task_id": task_id, "status": "killed"}

    # ------------------------------------------------------------------ reaping
    def register_external(self, *, goal: str = "", seat: str = "gui", tag: str = "") -> dict:
        """Register a pid-less seat (GUI/mailbox work on another surface) so it is
        visible to list/reap. It renews liveness via touch(); reap() judges staleness."""
        self._ensure()
        task_id = "ext-" + uuid.uuid4().hex[:8]
        task = {"task_id": task_id, "tag": tag or (seat + "-external"), "goal": goal[:500],
                "cmd": [], "status": "running", "source": "external", "seat": seat,
                "created_at": _now(), "started_at": _now(), "ended_at": None,
                "exit_code": None, "timeout_s": None, "log": "",
                "mailbox": str(self.mailbox(task_id)), "pid": None, "paused": False,
                "last_seen_at": _now(), "detail": "registered external seat"}
        self._save(task)
        self._trail("register_external", task_id, seat=seat)
        return task

    def done_external(self, task_id: str, detail: str = "closed by operator") -> dict:
        """The explicit close for mailbox seats (their designed exit, not a reap)."""
        task = self._finalize(task_id, "done", detail=detail)
        return {"ok": bool(task), "task_id": task_id}

    def reap(self) -> dict:
        """Dead-pid local tasks -> died. External seats: stale heartbeat -> stalled,
        EXCEPT seats in no_reap_seats (human-paced; closed via done_external)."""
        reaped = []
        for task in self.list_tasks():
            if task.get("status") in TERMINAL:
                continue
            tid = task["task_id"]
            if task.get("source") == "external":
                seen = _parse(task.get("last_seen_at") or task.get("created_at") or "")
                if time.time() - seen > self.external_stale_s:
                    if str(task.get("seat") or "") in self.no_reap_seats:
                        continue  # mailbox-seat exception: humans are slow, not dead
                    self._finalize(tid, "stalled", detail="external seat heartbeat stale")
                    reaped.append(tid)
                continue
            pid = task.get("pid")
            if pid and not _pid_alive(int(pid)):
                self._finalize(tid, "died", detail="pid %s gone without a terminal record" % pid)
                reaped.append(tid)
        return {"ok": True, "reaped": reaped}

    def list_tasks(self, limit: int = 100):
        self._ensure()
        rows = []
        for p in self.tasks_dir.glob("*.json"):
            try:
                rows.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                continue
        rows.sort(key=lambda r: (r.get("updated_at") or r.get("created_at") or ""), reverse=True)
        return rows[:limit]

    # ------------------------------------------------------------------ queue
    def queue_add(self, cmd, *, goal: str = "", tier: str = "mission",
                  priority: int = 0, timeout: float | None = None, tag: str = "") -> dict:
        self._ensure()
        q = {"queue_id": "q" + uuid.uuid4().hex[:10], "cmd": list(cmd), "goal": goal[:500],
             "tier": tier if tier in TIER_RANK else "mission", "priority": max(0, int(priority)),
             "timeout": float(timeout or self.default_timeout), "tag": tag,
             "created_at": _now(), "status": "queued", "task_id": None, "detail": ""}
        (self.queue_dir / (q["queue_id"] + ".json")).write_text(
            json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
        self._trail("queue-add", q["queue_id"], goal=q["goal"][:120], tier=q["tier"])
        return q

    def queue_list(self):
        self._ensure()
        out = []
        for p in sorted(self.queue_dir.glob("*.json"), reverse=True):
            try:
                out.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                continue
        return out

    def queue_status(self) -> dict:
        entries = self.queue_list()
        counts = {}
        for q in entries:
            counts[q.get("status") or "?"] = counts.get(q.get("status") or "?", 0) + 1
        return {"total": len(entries), "counts": counts}

    def drain_once(self, *, force: bool = False) -> dict:
        self.reap()
        self._reconcile_queue()
        if not force:
            live = [t for t in self.list_tasks()
                    if t.get("status") not in TERMINAL and t.get("source") == "local"]
            if live:
                return {"ok": True, "action": "busy", "detail": live[0]["task_id"]}
        nxt = None
        for q in self.queue_list():
            if q.get("status") != "queued":
                continue
            if nxt is None or (TIER_RANK.get(q.get("tier"), 99), -int(q.get("priority") or 0),
                               q.get("created_at") or "") < (
                    TIER_RANK.get(nxt.get("tier"), 99), -int(nxt.get("priority") or 0),
                    nxt.get("created_at") or ""):
                nxt = q
        if nxt is None:
            return {"ok": True, "action": "empty"}
        rec = self.spawn(nxt["cmd"], goal=nxt.get("goal", ""), timeout=nxt.get("timeout"),
                         tag=nxt.get("tag", ""))
        if not rec.get("task_id") or rec.get("status") not in ("running",):
            nxt["status"] = "failed"
            nxt["detail"] = str(rec.get("error") or "spawn failed")
            self._save_queue(nxt)
            return {"ok": False, "action": "spawn_failed", "queue_id": nxt["queue_id"]}
        nxt["status"] = "running"
        nxt["task_id"] = rec["task_id"]
        self._save_queue(nxt)
        self._trail("queue-start", nxt["queue_id"], spawned_task_id=rec["task_id"])
        return {"ok": True, "action": "started", "queue_id": nxt["queue_id"],
                "task_id": rec["task_id"]}

    def _save_queue(self, q: dict) -> None:
        (self.queue_dir / (q["queue_id"] + ".json")).write_text(
            json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")

    def _reconcile_queue(self) -> int:
        fixed = 0
        for q in self.queue_list():
            if q.get("status") != "running" or not q.get("task_id"):
                continue
            t = self._load(q["task_id"])
            if t and t.get("status") in TERMINAL:
                q["status"] = "done" if t.get("status") == "done" else "failed"
                q["detail"] = t.get("detail") or t.get("status")
                self._save_queue(q)
                self._trail("queue-end", q["queue_id"], task_status=t.get("status"))
                fixed += 1
        return fixed

    def drain(self, *, once: bool = False, interval_s: float = 2.0) -> None:
        while True:
            try:
                res = self.drain_once()
                if res.get("action") not in ("busy", "empty"):
                    print("[queue] %s" % res, flush=True)
            except Exception as e:
                print("[queue] drain error: %s" % e, flush=True)
            if once:
                return
            time.sleep(interval_s)


def _parse(stamp: str) -> float:
    try:
        return datetime.fromisoformat(stamp).timestamp()
    except Exception:
        return 0.0


def _pid_alive(pid: int) -> bool:
    if not pid:
        return False
    if sys.platform == "win32":
        # os.kill(pid, 0) is NOT a liveness probe on Windows (sig 0 ~= TerminateProcess);
        # tasklist is the authoritative check without psutil.
        try:
            r = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/NH"],
                               capture_output=True, text=True, timeout=15)
            return str(pid) in (r.stdout or "")
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, OSError):
        return False


# ---------------------------------------------------------------- self-test (offline)

def _self_test() -> int:
    import tempfile
    checks = []

    def check(name, ok):
        checks.append((name, bool(ok)))
        print("  %-34s %s" % (name, "PASS" if ok else "FAIL"))

    root = Path(tempfile.mkdtemp(prefix="supervisor_selftest_"))
    fast = dict(stale_after_s=0.6, nudge_grace_s=0.8, poll_s=0.2, external_stale_s=1.0)
    sup = Supervisor(root, **fast)

    # 1. clean exit -> done
    t = sup.spawn([sys.executable, "-c", "print('hello from child')"], goal="greet")
    ok = _wait_terminal(sup, t["task_id"], 20)
    rec = sup._load(t["task_id"])
    check("clean exit -> done/exit0", ok and rec["status"] == "done" and rec["exit_code"] == 0)

    # 2. non-zero exit -> failed with the code
    t = sup.spawn([sys.executable, "-c", "import sys; sys.exit(3)"], goal="fail")
    _wait_terminal(sup, t["task_id"], 20)
    rec = sup._load(t["task_id"])
    check("non-zero exit -> failed/3", rec["status"] == "failed" and rec["exit_code"] == 3)

    # 3. silence -> nudge into the mailbox -> killed as stalled
    child = ("import time,sys\n"
             "for i in range(5):\n"
             "    print('beat', i, flush=True); time.sleep(0.2)\n"
             "time.sleep(600)\n")
    t = sup.spawn([sys.executable, "-c", child], goal="hang")
    ok = _wait_terminal(sup, t["task_id"], 30, want="stalled")
    rec = sup._load(t["task_id"])
    mail = sup.read_mailbox(t["task_id"])
    check("silence -> nudged then stalled", ok and rec["status"] == "stalled")
    check("nudge landed in mailbox", "STALL NUDGE" in mail)

    # 4. steering: mailbox write + pause/continue flags
    t = sup.spawn([sys.executable, "-c", "import time; time.sleep(30)"], goal="steerable")
    time.sleep(0.4)
    sup.steer(t["task_id"], "re-anchor on the spec file")
    sup.pause(t["task_id"])
    paused = sup._load(t["task_id"]).get("paused")
    sup.continue_(t["task_id"])
    resumed = not sup._load(t["task_id"]).get("paused")
    check("steer/pause/continue via mailbox",
          "re-anchor on the spec file" in sup.read_mailbox(t["task_id"]) and paused and resumed)
    sup.kill(t["task_id"])
    check("kill -> terminal killed", sup._load(t["task_id"])["status"] == "killed")

    # 5. queue: tier order honored, drain advances, reconcile closes entries
    sup.queue_add([sys.executable, "-c", "print('filler work')"], goal="f",
                  tier="filler")
    sup.queue_add([sys.executable, "-c", "print('mission work')"], goal="m",
                  tier="mission")
    deadline = time.time() + 40
    order = []
    while time.time() < deadline:
        res = sup.drain_once()
        if res.get("action") == "started":
            order.append(sup._load(res["task_id"]).get("goal"))
        if sup.queue_status()["counts"].get("running") in (None, 0) and \
           sup.queue_status()["counts"].get("queued", 0) == 0 and not order:
            break
        if all(q["status"] in TERMINAL | {"done", "failed"} for q in sup.queue_list()) and len(order) >= 2:
            break
        time.sleep(0.3)
    check("queue drains in tier order", order == ["m", "f"])
    finals = {q["queue_id"]: q["status"] for q in sup.queue_list()}
    check("queue reconciles to done", set(finals.values()) == {"done"})

    # 6. reap: dead-pid local -> died; external stale -> stalled; no-reap seat survives
    t = sup.spawn([sys.executable, "-c", "print('ghost')"], goal="ghost")
    time.sleep(0.8)  # let it finish; then fake a lost terminal record
    rec = sup._load(t["task_id"])
    rec["status"] = "running"
    rec["ended_at"] = None
    sup._save(rec)
    r = sup.reap()
    check("dead pid reaped as died", t["task_id"] in r["reaped"])

    ext = sup.register_external(goal="human-paced GUI work", seat="gui")
    dead = sup.register_external(goal="abandoned kiosk", seat="kiosk")
    row = sup._load(dead["task_id"])
    row["last_seen_at"] = _now()[:-1]  # backdate
    row["last_seen_at"] = "2020-01-01T00:00:00+00:00"
    sup._save(row)
    sup.reap()
    check("stale external reaped", sup._load(dead["task_id"])["status"] == "stalled")
    check("no-reap seat survives", sup._load(ext["task_id"])["status"] == "running"
          and "gui" not in sup.no_reap_seats)
    slow = Supervisor(root, **fast, no_reap_seats={"human-mail"})
    ext2 = slow.register_external(goal="mailbox thread", seat="human-mail")
    row = slow._load(ext2["task_id"])
    row["last_seen_at"] = "2020-01-01T00:00:00+00:00"
    slow._save(row)
    slow.reap()
    check("no-reap exception honored", slow._load(ext2["task_id"])["status"] == "running")

    bad = [n for n, ok in checks if not ok]
    print("process_supervisor self-test: %d/%d PASS" % (len(checks) - len(bad), len(checks)))
    return 0 if not bad else 1


def _wait_terminal(sup: Supervisor, task_id: str, timeout_s: float, want: str | None = None):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        t = sup._load(task_id)
        if t and t.get("status") in TERMINAL:
            return want is None or t["status"] == want
        time.sleep(0.2)
    return False


# ---------------------------------------------------------------- CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="process_supervisor")
    ap.add_argument("--root", default=None, help="state root (default <seed>/state/supervisor)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("spawn")
    p.add_argument("--cmd", required=True, help='entrypoint, {goal} substituted, e.g. "python agent.py --query {goal}"')
    p.add_argument("--goal", default="")
    p.add_argument("--timeout", type=float, default=None)
    p.add_argument("--tag", default="")
    sub.add_parser("list")
    p = sub.add_parser("status"); p.add_argument("task_id")
    p = sub.add_parser("watch"); p.add_argument("task_id")
    p = sub.add_parser("steer"); p.add_argument("task_id"); p.add_argument("text")
    p = sub.add_parser("pause"); p.add_argument("task_id")
    p = sub.add_parser("continue"); p.add_argument("task_id")
    p = sub.add_parser("kill"); p.add_argument("task_id")
    sub.add_parser("reap")
    p = sub.add_parser("queue")
    qsub = p.add_subparsers(dest="qcmd", required=True)
    qp = qsub.add_parser("add")
    qp.add_argument("--cmd", required=True); qp.add_argument("--goal", default="")
    qp.add_argument("--tier", default="mission"); qp.add_argument("--priority", type=int, default=0)
    qp.add_argument("--timeout", type=float, default=None); qp.add_argument("--tag", default="")
    qsub.add_parser("list"); qsub.add_parser("status")
    p = sub.add_parser("drain"); p.add_argument("--once", action="store_true")
    sub.add_parser("self-test")

    a = ap.parse_args(argv)
    if a.cmd == "self-test":
        return _self_test()
    sup = Supervisor(a.root)
    if a.cmd == "spawn":
        print(json.dumps(sup.spawn(shlex.split(a.cmd), goal=a.goal,
                                   timeout=a.timeout, tag=a.tag), indent=2))
    elif a.cmd == "list":
        for t in sup.list_tasks(20):
            print("%-14s %-8s %-6s %s" % (t["task_id"], t.get("status"),
                                          t.get("source"), (t.get("goal") or "")[:60]))
    elif a.cmd == "status":
        print(json.dumps(sup._load(a.task_id), indent=2))
    elif a.cmd == "watch":
        print(sup.watch(a.task_id))
    elif a.cmd == "steer":
        print(json.dumps(sup.steer(a.task_id, a.text)))
    elif a.cmd == "pause":
        print(json.dumps(sup.pause(a.task_id)))
    elif a.cmd == "continue":
        print(json.dumps(sup.continue_(a.task_id)))
    elif a.cmd == "kill":
        print(json.dumps(sup.kill(a.task_id)))
    elif a.cmd == "reap":
        print(json.dumps(sup.reap()))
    elif a.cmd == "queue":
        if a.qcmd == "add":
            print(json.dumps(sup.queue_add(shlex.split(a.cmd), goal=a.goal, tier=a.tier,
                                           priority=a.priority, timeout=a.timeout, tag=a.tag), indent=2))
        elif a.qcmd == "list":
            for q in sup.queue_list():
                print("%-12s %-8s %-11s %s" % (q["queue_id"], q.get("status"),
                                               q.get("tier"), (q.get("goal") or "")[:50]))
        else:
            print(json.dumps(sup.queue_status()))
    elif a.cmd == "drain":
        sup.drain(once=a.once)
    return 0


if __name__ == "__main__":
    sys.exit(main())
