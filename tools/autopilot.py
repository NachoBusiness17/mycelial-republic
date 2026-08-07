"""Autopilot: spawn a gpipes swarm, poll, optionally nudge, collect, and write summary.

Usage: python tools/autopilot.py goals.txt
or:    python tools/autopilot.py "Goal one" "Goal two"
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import gpipes
from mag import pigeonhole as ph


def run_autopilot(goals, provider="deepseek", timeout=300, poll=3, steer_nudge=None):
    print("AUTOPILOT: spawning gpipes for %d goals" % len(goals))
    res = gpipes.fan_out(goals, provider=provider, timeout=timeout, tags=["autopilot"] * len(goals))
    if not res.get("ok"):
        print("fan_out failed:", res)
        return res
    pipe = res.get("pipe") or {}
    pid = pipe.get("pipe_id")
    print("spawned pipe:", pid)

    # Poll & optionally nudge
    start = time.time()
    last_nudge = 0
    while True:
        st = gpipes.pipe_status(pid)
        print(json.dumps({"pipe_id": pid, "status": st.get("status")}, indent=2))
        # if running, optionally send a nudge steer every 30s
        if st.get("status") == "running":
            now = time.time()
            if steer_nudge and now - last_nudge > 30:
                for tid in st.get("task_ids", []):
                    try:
                        ph.post_steer(tid, steer_nudge)
                    except Exception:
                        pass
                last_nudge = now
            time.sleep(poll)
            # continue polling
            continue
        # terminal-ish
        coll = gpipes.collect(pid, wait=1, tail=50)
        out = {
            "pipe_id": pid,
            "status": coll.get("status"),
            "merged": coll.get("merged"),
            "results": coll.get("results"),
        }
        # write summary
        OUT = ROOT / "memory" / "runs" / "gpipes" / (pid + "-merged.json")
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
        print("collected ->", OUT)
        return out


def main(argv=None):
    argv = argv or sys.argv[1:]
    goals = []
    if not argv:
        print("usage: autopilot.py goals.txt  OR autopilot.py \"goal1\" \"goal2\"")
        return 2
    # single arg file?
    if len(argv) == 1 and Path(argv[0]).is_file():
        goals = [ln.strip() for ln in Path(argv[0]).read_text(encoding="utf-8").splitlines() if ln.strip()]
    else:
        goals = list(argv)
    if not goals:
        print("no goals")
        return 2
    print("goals:", goals)
    run_autopilot(goals, provider="deepseek", timeout=300, poll=3, steer_nudge="Please focus: concise, one-paragraph deliverable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
