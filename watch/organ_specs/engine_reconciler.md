# ORGAN SPEC: engine reconciler — desired-state control loop for the bay

```python
"""Fleet conductor law: the bay holds exactly what the spec declares.

watch/engine_reconciler.py serves the law of engine convergence: for every
engine declared in watch/engine_spec.json, the number of live resident
sessions must equal `replicas` -- no fewer (launch churn subprocesses with
spec-derived env), no more (kill extras newest-first). Outputs under 150
bytes are considered starved and requeued. Engines absent from the spec are
never touched, regardless of what roams the bay.
"""

import json
import os
import signal
import subprocess
import sys
import time

SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine_spec.json")
BAY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bay")
STATE_DIR = os.path.join(BAY_DIR, "state")
LOCK_DIR = os.path.join(BAY_DIR, "locks")
LOG_DIR = os.path.join(BAY_DIR, "logs")
CHURN_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "churn.py")

STARVE_BYTES = 150
ENV_KEYS = ("CHURN_QUEUE", "CHURN_MODEL", "CHURN_SESS", "CHURN_STATE", "CHURN_LOG")


def fail(msg):
    raise RuntimeError("engine_reconciler: " + msg)


def load_spec(path=SPEC_PATH):
    with open(path, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    if not isinstance(spec, dict) or "engines" not in spec:
        fail("spec at %s lacks an 'engines' mapping" % path)
    for name, cfg in spec["engines"].items():
        for key in ("model", "replicas", "queue", "session_pattern"):
            if key not in cfg:
                fail("engine %r missing %r" % (name, key))
    return spec


def session_name(engine, cfg, slot):
    return cfg["session_pattern"].format(engine=engine, slot=slot, model=cfg["model"])


def state_path(engine, slot):
    return os.path.join(STATE_DIR, "%s.%d.json" % (engine, slot))


def lock_path(engine, slot):
    return os.path.join(LOCK_DIR, "%s.%d.lock" % (engine, slot))


def read_pid(lockfile):
    try:
        with open(lockfile, "r", encoding="utf-8") as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return None


def pid_alive(pid):
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


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
    """Slots whose state output is under the starvation threshold."""
    out = []
    for slot in slots:
        sp = state_path(engine, slot)
        try:
            if os.path.getsize(sp) < STARVE_BYTES:
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
        slots = list(range(replicas)) + list(range(100, 100 + replicas))
        live = resident_slots(engine, slots)
        declared_live = [s for s in live if s < 100]

        deficit = replicas - len(declared_live)
        if deficit > 0:
            free = [s for s in range(replicas) if s not in declared_live]
            for slot in sorted(free)[:deficit]:
                actions.append(launch(engine, cfg, slot, dry))

        excess = len(declared_live) - replicas
        if excess > 0:
            for slot in sorted(declared_live, reverse=True)[:excess]:
                actions.append(kill(engine, slot, dry))

        for slot in starved_slots(engine, declared_live):
            actions.append(requeue(engine, slot, dry))
    return actions


def main(argv):
    verify = "--verify" in argv or "-v" in argv
    spec = load_spec()
    actions = reconcile(spec, dry=verify)
    print(json.dumps({"mode": "verify" if verify else "apply",
                      "plan": actions,
                      "converged": not actions}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```
