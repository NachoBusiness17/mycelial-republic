"""TOCTOU repro for scripts/descent_driver.sh pidfile guard (read-only test).

Copies the guard stanza VERBATIM from scripts/descent_driver.sh:13-22 into a
sandbox dir, launches pairs of bash children simultaneously (CREATE_NO_WINDOW
per win32 law), counts pairs where BOTH proceeded (both appended a marker).
Never touches the real state/descent_driver.pid or any paid queue.
"""
import os
import subprocess
import sys

CREATE_NO_WINDOW = 0x08000000
GUARD = r'''
PIDFILE="pid"
if [ -f "$PIDFILE" ]; then
  OLDPID=$(cat "$PIDFILE" 2>/dev/null)
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    exit 3
  fi
fi
echo $$ > "$PIDFILE"
echo "$$" >> markers
sleep 0.25
rm -f "$PIDFILE"
'''

def main():
    workdir = os.path.dirname(os.path.abspath(__file__))
    sandbox = os.path.join(workdir, "_race_sandbox")
    os.makedirs(sandbox, exist_ok=True)
    pidfile = os.path.join(sandbox, "pid")
    markers = os.path.join(sandbox, "markers")
    for p in (pidfile, markers):
        if os.path.exists(p):
            os.remove(p)
    pairs = 40
    doubles = 0
    refusals = 0
    for i in range(pairs):
        # fresh pidfile state per iteration is handled by the children themselves
        procs = [
            subprocess.Popen(
                ["bash", "-c", GUARD],
                cwd=sandbox,
                creationflags=CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            for _ in range(2)
        ]
        rcs = [p.wait() for p in procs]
        with open(markers) as f:
            n = sum(1 for _ in f)
        if n == 2:
            doubles += 1
        if 3 in rcs:
            refusals += 1
        # reset marker file for next pair
        os.remove(markers)
        if os.path.exists(pidfile):
            os.remove(pidfile)
    print(f"pairs={pairs} both_proceeded={doubles} at_least_one_refused_exit3={refusals}")

if __name__ == "__main__":
    sys.exit(main())
