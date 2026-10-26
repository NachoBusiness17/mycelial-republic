"""deep-verkle-formal: probe semantics for a MISSING pid on win32 (the
stale-break path of verkle_lock) + interpreter identity."""
import os
import sys

print("python:", sys.version)
missing = 999999999
try:
    os.kill(missing, 0)
    print("missing_pid_probe: returned cleanly (BAD: cannot detect death)")
except Exception as e:  # noqa: BLE001
    print("missing_pid_probe:", type(e).__name__, "winerror=", getattr(e, "winerror", None), repr(e)[:120])
own = os.getpid()
try:
    os.kill(own, 0)
    print("self_probe: returned cleanly")
except Exception as e:  # noqa: BLE001
    print("self_probe:", type(e).__name__, repr(e)[:120])
