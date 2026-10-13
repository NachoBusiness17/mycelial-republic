import os, signal
killed = []
for pid in os.listdir("/proc"):
    if not pid.isdigit():
        continue
    try:
        cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\x00", b" ").decode("utf-8", "replace")
    except Exception:
        continue
    if "main.py dashboard" in cmd and "kill_dash" not in cmd:
        os.kill(int(pid), signal.SIGKILL)
        killed.append(pid)
print("killed", killed)
