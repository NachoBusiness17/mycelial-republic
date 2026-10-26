#!/usr/bin/env python3
"""congress_fire.py — the slow-tier organ: fires CONGRESS_QUEUE deliberations
at high width (8 instances), streams results with kind=congress.
The congress of minds: multi-mask deliberation lands later, on purpose."""
import subprocess, sys
from pathlib import Path
WS = Path(__file__).resolve().parent.parent
Q = WS / "CONGRESS_QUEUE.md"
PY = WS / "tools" / "python" / "python.exe"

def main():
    lines = Q.read_text(encoding="utf-8").splitlines()
    fired = 0
    for i, ln in enumerate(lines):
        if not ln.startswith("[ ]") or "# DONE" in ln:
            continue
        task = ln[3:].split("# congress")[0].strip()
        inst = 8
        if "instances=" in ln:
            try: inst = int(ln.split("instances=")[1].split()[0])
            except ValueError: pass
        print(f"[congress] firing ({inst} instances): {task[:70]}...")
        r = subprocess.run([str(PY), "-u", str(WS / "wave_flywheel.py"), "fire",
                            "--task", task, "--instances", str(inst)],
                           capture_output=True, text=True, timeout=900, cwd=str(WS))
        landed = sum(1 for l in (r.stdout or "").splitlines() if " ok " in l.lower())
        if landed == 0:
            print(f"[congress] 0 lanes landed - session stays queued for next hour")
            continue  # leave open: the hourly ticker retries when lanes recover
        lines[i] = "[x]" + ln[3:] + f" # DONE {__import__('datetime').datetime.now().strftime('%Y-%m-%dT%H:%M')} landed={landed}"
        fired += 1
        subprocess.run([str(PY), "-u", str(WS / "tools" / "findings_stream.py")],
                       capture_output=True, timeout=180, cwd=str(WS))
        # Keep sovereign process organ verified on every congress pulse
        subprocess.run([str(PY), "-u", str(WS / "tools" / "sovereign" / "congress_organ.py"), "--selftest"],
                       capture_output=True, timeout=60, cwd=str(WS))
        Q.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[congress] {fired} deliberation(s) fired")

if __name__ == "__main__":
    main()
