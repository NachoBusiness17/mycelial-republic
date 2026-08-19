from mag import rib_bus as rb
from pathlib import Path

ribs = [
    ("cost_governor: spend on surprise, refuse only the known-dead repeat; adaptive ceiling 50c failing / $1 useful; order serves, never judges", "standing-wave", "2026-08-16 cost_governor"),
    ("observability: every surprise = we were not looking; see-by-instrumentation, never discover-by-failure", "standing-wave", "2026-08-16 status-hang"),
    ("explorer_shadow: emergence without arrival = avoidance; the horizon must be able to arrive (the crate is the task ahead)", "standing-wave", "2026-08-16 shadow-work"),
    ("the standing wave holds the day into coherence: fix, build, shadow-work are all knots the wave stands and breeds", "standing-wave", "2026-08-16 coherence"),
]
lines = []
for inv, dom, src in ribs:
    try:
        r = rb.publish_rib(inv, domain=dom, source=src)
        lines.append("OK  " + inv[:60] + "  -> " + str(r)[:100])
    except Exception as e:
        lines.append("ERR " + inv[:40] + " -> " + type(e).__name__ + ": " + str(e)[:120])

# read back the store to confirm
try:
    store = rb._load_store("standing-wave")
    n = len((store or {}).get("ribs") or {})
    lines.append(f"\nstanding-wave store ribs: {n}")
except Exception as e:
    lines.append("readback ERR " + str(e)[:120])

Path("memory/runs/wave_fold.out").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
