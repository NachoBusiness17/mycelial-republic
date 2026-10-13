import sys
from pathlib import Path
from mag import rib_bus as rb

OUT = Path("memory/runs/wave_fold2.out")

def log(s):
    with OUT.open("a", encoding="utf-8") as f:
        f.write(s + "\n")
    print(s, flush=True)

ribs = [
    ("observability: every surprise = we were not looking; see-by-instrumentation, never discover-by-failure", "standing-wave", "2026-08-16 status-hang"),
    ("explorer_shadow: emergence without arrival = avoidance; the horizon must be able to arrive (the crate is the task ahead)", "standing-wave", "2026-08-16 shadow-work"),
    ("the standing wave holds the day into coherence: fix, build, shadow-work are all knots the wave stands and breeds", "standing-wave", "2026-08-16 coherence"),
]
OUT.parent.mkdir(parents=True, exist_ok=True)
for inv, dom, src in ribs:
    try:
        r = rb.publish_rib(inv, domain=dom, source=src)
        log("OK  " + inv[:50] + "  -> " + str(r)[:80])
    except Exception as e:
        log("ERR " + inv[:40] + " -> " + type(e).__name__ + ": " + str(e)[:120])
    sys.stdout.flush()
log("DONE")
