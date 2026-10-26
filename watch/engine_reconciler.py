"""Fleet conductor law: the bay holds exactly what the spec declares.

watch/engine_reconciler.py serves the law of engine convergence: for every
engine declared in watch/engine_spec.json, the number of live resident
sessions must equal `replicas` -- no fewer (launch churn subprocesses with
spec-derived env), no more (kill extras newest-first). Outputs under 150
bytes are considered starved and requeued -- but only after a grace window
(BAY_STARVE_GRACE_S, default 30 min): a young state file is warming up, not
starved. Engines absent from the spec are never touched, regardless of what
roams the bay.

Leg-1 organs wired here (SHERPA_ROUTE v2):
  * lockfiles now carry {pid, seat, ts} JSON (written by the churn CHILD at
    startup via CHURN_LOCK, or by the `adopt` action for hand-launched
    engines). Legacy bare-int locks still parse. Writers are attributable.
  * `adopt ENGINE SLOT PID [--seat NAME]` writes that lockfile so a
    hand-launched engine can be killed/attributed without relaunching it.
"""

import json
import os
import re
import signal
import subprocess
import sys
import time

SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine_spec.json")
BAY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bay")
STATE_DIR = os.path.join(BAY_DIR, "state")
LOCK_DIR = os.path.join(BAY_DIR, "locks")
LOG_DIR = os.path.join(BAY_DIR, "logs")
CHURN_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overnight_churn.py")
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
from mag import bay_organs  # noqa: E402  (stdlib-only; shares the pid probe)

STARVE_BYTES = 150
STARVE_GRACE_S = int(os.environ.get("BAY_STARVE_GRACE_S", "1800"))  # 30 min
ENV_KEYS = ("CHURN_QUEUE", "CHURN_MODEL", "CHURN_SESS", "CHURN_STATE", "CHURN_LOG",
            "CHURN_LOCK")


def fail(msg):
    raise RuntimeError("engine_reconciler: " + msg)


def _session_pattern(engine, cfg):
    """Synthesize session_pattern from spec v1 'sessions' forms.

    "seat-g{1..4}" -> "seat-g{slot}"; "seat-b1" (replicas 1) -> "seat-b{slot}".
    Slots are 1-based so launches reproduce the live session names exactly.
    """
    sessions = str(cfg.get("sessions", engine + "-{slot}"))
    if "{1.." in sessions:
        return sessions.split("{1..")[0] + "{slot}"
    digits = re.match(r"^(.*?)(\d+)$", sessions)
    if digits and int(cfg.get("replicas", 1)) >= 1:
        return digits.group(1) + "{slot}"
    return sessions + "-{slot}"


def load_spec(path=SPEC_PATH):
    """Load engine_spec.json. Accepts the v1 list-of-engines shape (schema
    engine_spec.v1) or a plain {name: cfg} mapping; returns the mapping form."""
    with open(path, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    engines = spec.get("engines") if isinstance(spec, dict) else None
    if isinstance(engines, list):
        norm = {}
        for cfg in engines:
            name = cfg.get("id")
            if not name:
                fail("v1 engine entry missing 'id'")
            cfg = dict(cfg)
            cfg.setdefault("session_pattern", _session_pattern(name, cfg))
            norm[name] = cfg
        engines = norm
    if not isinstance(engines, dict) or not engines:
        fail("spec at %s lacks an 'engines' mapping" % path)
    for name, cfg in engines.items():
        for key in ("model", "replicas", "queue", "session_pattern"):
            if key not in cfg:
                fail("engine %r missing %r" % (name, key))
    return {"engines": engines}


def session_name(engine, cfg, slot):
    return cfg["session_pattern"].format(engine=engine, slot=slot, model=cfg["model"])


def state_path(engine, slot):
    return os.path.join(STATE_DIR, "%s.%d.json" % (engine, slot))


def lock_path(engine, slot):
    return os.path.join(LOCK_DIR, "%s.%d.lock" % (engine, slot))


def read_pid(lockfile):
    """Read a pid from a lockfile. Accepts the Leg-1 JSON shape
    {\"pid\": N, \"seat\": ..., \"ts\": ...} and the legacy bare-int shape."""
    try:
        with open(lockfile, "r", encoding="utf-8") as fh:
            txt = fh.read().strip()
    except OSError:
        return None
    if not txt:
        return None
    try:
        return int(txt)
    except ValueError:
        pass
    try:
        obj = json.loads(txt)
    except ValueError:
        return None
    try:
        return int(obj.get("pid"))
    except (AttributeError, TypeError, ValueError):
        return None


def pid_alive(pid):
    # delegated to mag.bay_organs.pid_alive (OpenProcess probe). Measured
    # 2026-09-04: os.kill(pid, 0) on win32/Python 3.11.15 NEVER raises — the
    # old probe here reported every pid alive, so a dead engine's slot could
    # never be relaunched and any adopted identity looked live forever.
    return bay_organs.pid_alive(pid)


def resident_slots(engine, declared_slots):
    """Slots for this engine with a state file, a live lockfile pid, or both."""
    live = []
    for slot in declared_slots:
        sp, lp = state_path(engine, slot), lock_path(engine, slot)
        has_state = os.path.isfile(sp)
        has_lock = pid_alive(read_pid(lp))
        if has_state or has_lock:
            live.append(slot)
    return live


def starved_slots(engine, slots):
    """Slots whose state output is under the starvation threshold AND old
    enough to actually be starved. Requeue grace: a state file younger than
    STARVE_GRACE_S is warming up, not starved -- requeueing it mid-run was
    the young-state kill class (seen in verify, never applied; now it can't
    be applied either)."""
    out = []
    for slot in slots:
        sp = state_path(engine, slot)
        try:
            if os.path.getsize(sp) < STARVE_BYTES:
                age = time.time() - os.path.getmtime(sp)
                if age < STARVE_GRACE_S:
                    continue  # grace: warming up
                out.append(slot)
        except OSError:
            out.append(slot)
    return out


def launch_env(engine, cfg, slot):
    env = dict(os.environ)
    values = {
        "CHURN_QUEUE": cfg["queue"],
        "CHURN_MODEL": cfg["model"],
        "CHURN_SESS": session_name(engine, cfg, slot),
        "CHURN_STATE": state_path(engine, slot),
        "CHURN_LOG": os.path.join(LOG_DIR, "%s.%d.log" % (engine, slot)),
        "CHURN_LOCK": lock_path(engine, slot),  # child writes {pid, seat, ts} itself
    }
    for key in ENV_KEYS:
        env[key] = str(values[key])
    return env


def launch(engine, cfg, slot, dry):
    plan = {"action": "launch", "engine": engine, "slot": slot,
            "session": session_name(engine, cfg, slot)}
    if dry:
        return plan
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(LOCK_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(lock_path(engine, slot), "a", encoding="utf-8") as _:
        pass
    subprocess.Popen(
        [sys.executable, CHURN_SCRIPT],
        env=launch_env(engine, cfg, slot),
        stdout=open(os.path.join(LOG_DIR, "%s.%d.log" % (engine, slot)), "ab"),
        stderr=subprocess.STDOUT,
    )
    plan["launched"] = True
    return plan


def kill(engine, slot, dry):
    plan = {"action": "kill", "engine": engine, "slot": slot}
    if dry:
        return plan
    pid = read_pid(lock_path(engine, slot))
    if pid_alive(pid):
        os.kill(pid, signal.SIGTERM)
    for path in (lock_path(engine, slot), state_path(engine, slot)):
        try:
            os.remove(path)
        except OSError:
            pass
    plan["pid"] = pid
    return plan


def requeue(engine, slot, dry):
    plan = {"action": "requeue", "engine": engine, "slot": slot}
    if dry:
        return plan
    sp = state_path(engine, slot)
    os.rename(sp, sp + ".requeued.%d" % int(time.time()))
    return plan


def reconcile(spec, dry=False):
    """Return the reconciliation plan for one pass. Converged bays yield []."""
    actions = []
    for engine, cfg in sorted(spec["engines"].items()):
        replicas = int(cfg["replicas"])
        slots = list(range(1, replicas + 1)) + list(range(100, 100 + replicas))
        live = resident_slots(engine, slots)
        declared_live = [s for s in live if s < 100]

        deficit = replicas - len(declared_live)
        if deficit > 0:
            free = [s for s in range(1, replicas + 1) if s not in declared_live]
            for slot in sorted(free)[:deficit]:
                actions.append(launch(engine, cfg, slot, dry))

        excess = len(declared_live) - replicas
        if excess > 0:
            for slot in sorted(declared_live, reverse=True)[:excess]:
                actions.append(kill(engine, slot, dry))

        for slot in starved_slots(engine, declared_live):
            actions.append(requeue(engine, slot, dry))
    return actions


def adopt(engine, slot, pid, seat="hand-launched", dry=False):
    """Lockfile-pid organ, adopt half: register a HAND-LAUNCHED engine's pid in
    its slot lockfile as {pid, seat, ts} so the reconciler can attribute and
    kill it without relaunching anything. This is the fix for the 8-banner
    slot (multiple engines sharing one slot's identity): identity is owned by
    a live pid on file."""
    plan = {"action": "adopt", "engine": engine, "slot": slot, "pid": int(pid), "seat": seat}
    if dry:
        return plan
    os.makedirs(LOCK_DIR, exist_ok=True)
    # atomic overwrite (temp + same-volume replace), same shape the churn
    # child writes for itself at startup.
    tmp = lock_path(engine, slot) + ".tmp-%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"pid": int(pid), "seat": seat, "ts": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, fh)
    os.replace(tmp, lock_path(engine, slot))
    plan["adopted"] = True
    return plan


def main(argv):
    # adopt subcommand: register a hand-launched engine's pid in a slot
    # lockfile. Never launches or kills anything.
    if argv[:1] == ["adopt"]:
        if len(argv) < 4:
            print("usage: engine_reconciler.py adopt ENGINE SLOT PID [--seat NAME]", file=sys.stderr)
            return 2
        engine, slot, pid = argv[1], int(argv[2]), int(argv[3])
        seat = "hand-launched"
        if "--seat" in argv:
            seat = argv[argv.index("--seat") + 1]
        print(json.dumps(adopt(engine, slot, pid, seat=seat), indent=2))
        return 0
    verify = "--apply" not in argv
    spec = load_spec()
    actions = reconcile(spec, dry=verify)
    print(json.dumps({"mode": "verify" if verify else "apply",
                      "starve_grace_s": STARVE_GRACE_S,
                      "plan": actions,
                      "converged": not actions}, indent=2))
    if not verify:
        print("engine_reconciler: apply is explicit-only. It kills/launches by bay "
              "lockfiles; engines launched by hand have none — adopt them first "
              "(adopt ENGINE SLOT PID) or you WILL double-launch.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
