"""deep-verkle-formal: empirical test of the verkle_lock liveness probe on win32.

verkle_knot.verkle_lock uses os.kill(owner_pid, 0) as a POSIX-style liveness
probe. On Windows, sig=0 IS signal.CTRL_C_EVENT, so CPython routes the call to
GenerateConsoleCtrlEvent(CTRL_C_EVENT, pid), which MSDN documents as invalid
for a nonzero process-group id. Question: does the probe (a) return cleanly
(live holder proven), (b) raise, or (c) harm the holder?

Harmless test: the holder is a sacrificial python child we spawn ourselves
(CREATE_NO_WINDOW). Parent probes it, then checks whether it is still alive.
"""
import subprocess
import sys
import time
import signal

CHILD = (
    "import time,sys\n"
    "print('alive-start', flush=True)\n"
    "time.sleep(8)\n"
    "print('alive-end', flush=True)\n"
)

proc = subprocess.Popen(
    [sys.executable, "-c", CHILD],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    creationflags=0x08000000,  # CREATE_NO_WINDOW
)
line = proc.stdout.readline().strip()  # wait until the child is provably running
print("child_first_line:", line)

result_kind = None
err_repr = None
try:
    rc = os_kill_rc = None
    import os
    os.kill(proc.pid, 0)
    result_kind = "returned_cleanly (POSIX-style probe semantics)"
except Exception as e:  # noqa: BLE001 - we want the exact class and winerror
    result_kind = type(e).__name__
    err_repr = repr(e)
    we = getattr(e, "winerror", None)
    err_repr += f" winerror={we}"

time.sleep(0.5)
still_running = proc.poll() is None
print("probe_result:", result_kind)
print("probe_error:", err_repr)
print("ctrl_c_event_value:", signal.CTRL_C_EVENT)
print("child_still_alive_after_probe:", still_running)
if not still_running:
    print("child_returncode:", proc.returncode)
proc.kill()
proc.wait()
print("VERDICT:",
      "probe-is-harmless-liveness-check" if (result_kind and still_running and "returned" in str(result_kind))
      else "probe-raises-or-harms: liveness check CANNOT prove a live holder on win32")
