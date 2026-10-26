#!/usr/bin/env python3
"""run_asks - fire the 8 frontier asks through the lensing carrier (2026-10-01).

Operator GO: "design the claude asks and run them go 20 wide". Budget cap $8.00
total; sequential (one call at a time - the 402 floor and the streaming carrier
both prefer it); every result banked beside its ask."""
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # root/watch/inbox/frontier_asks/run_asks.py
ASKS = Path(__file__).resolve().parent
OUT = ASKS / "results"
OUT.mkdir(exist_ok=True)
CAP = 8.0
spent = 0.0

for ask in sorted(ASKS.glob("ASK*.md")):
    stem = ask.stem
    res = OUT / f"{stem}_RESULT.md"
    if res.exists():
        print(f"skip {stem} (result present)")
        continue
    if spent >= CAP:
        print(f"HOLD at cap ${spent:.2f}")
        break
    print(f"fire {stem} (prior spend ${spent:.2f})...", flush=True)
    p = subprocess.run(
        [str(ROOT / ".venv/Scripts/python.exe"), "tools/lensing_ask.py",
         "--brief", str(ask), "--fire", "--prior-spend", f"{spent:.4f}",
         "--budget-cap", str(CAP),
         "--out-prefix", str(OUT / stem)],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=1800)
    out = (p.stdout or "") + (p.stderr or "")
    res.write_text(out[-40000:], encoding="utf-8")
    for tok in out.split():
        if tok.startswith("cost=$"):
            try:
                spent = float(tok[6:])
                print(f"  done {stem} ${spent:.4f} cumulative")
            except ValueError:
                pass
    print(f"  {stem} exit {p.returncode}, result banked", flush=True)
    time.sleep(5)

print(f"RUN COMPLETE total=${spent:.2f} of ${CAP}")
