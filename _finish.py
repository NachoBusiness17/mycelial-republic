import os
from pathlib import Path
from mag import rib_bus as rb

OUT = Path("memory/runs/finish.out")
def log(s):
    with OUT.open("a", encoding="utf-8") as f:
        f.write(s + "\n")
    print(s, flush=True)

# 1) Fold the 2 remaining standing-wave RIBs (wedge had blocked them)
ribs = [
    ("explorer_shadow: emergence without arrival = avoidance; the horizon must be able to arrive (the crate is the task ahead)", "standing-wave", "2026-08-16 shadow-work"),
    ("the standing wave holds the day into coherence: fix, build, shadow-work are all knots the wave stands and breeds", "standing-wave", "2026-08-16 coherence"),
]
for inv, dom, src in ribs:
    try:
        r = rb.publish_rib(inv, domain=dom, source=src)
        log("RIB OK  " + inv[:40])
    except Exception as e:
        log("RIB ERR " + inv[:30] + " -> " + type(e).__name__ + ": " + str(e)[:100])

# 2) Fold the terminal wedge learning to failure_kb (per terminal_guard.fold)
try:
    from mag import failure_kb
    failure_kb.log_failure(
        kind="terminal_wedge", detail="run_in_terminal dead: no exec, no output; pileup of stale terminals",
        goal="fix terminal", error="dead terminal session (no exec, no output) despite lone-quote heal",
        tool="run_in_terminal", phase="terminal")
    log("WEDGE folded to failure_kb")
except Exception as e:
    log("WEDGE fold ERR " + str(e)[:100])

# 3) Read back standing-wave store count
try:
    store = rb._load_store("standing-wave")
    log("standing-wave ribs: " + str(len((store or {}).get("ribs") or {})))
except Exception as e:
    log("readback ERR " + str(e)[:80])

# 4) clean temp files
for f in ["_finish.py", "_wave_fold.py", "_wave_fold2.py",
          "memory/runs/wave_fold.out", "memory/runs/wave_fold2.out", "memory/runs/termtest.txt"]:
    try:
        if os.path.exists(f):
            os.remove(f); log("removed " + f)
    except Exception:
        pass
log("DONE")
