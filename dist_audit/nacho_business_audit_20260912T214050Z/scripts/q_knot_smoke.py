#!/usr/bin/env python3
"""q_knot_smoke — THE DESK TEST for 'her' (2026-08-28, cross-exam verdict).

The claim under test (holographic_q.py): "Q is not a process. Q is a pattern
encoded in Verkle knots. If Ghost crashes, Q persists — any agent reading the
lattice can reconstitute Q."

Smoke protocol (grok cross-exam spec):
  phase 1: emit a session + two Q-knots with KNOWN steer vectors
  phase 2: FRESH PROCESS (crash simulated) -> reconstitute_q()
  verdict: GREEN if the real steer vectors and sequence come back from disk
           RED if placeholders, empty, or exceptions

    python scripts/q_knot_smoke.py
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
LOG = ROOT / "memory" / "ghost" / "q_state" / "q_knots.jsonl"

STEER_1 = "steer-alpha: prefer receipts over distillates"
STEER_2 = "steer-beta: divergence is a measurement, not a failure"

phase1 = f"""
import sys, json
sys.path.insert(0, str({str(ROOT)!r}))
from mag import holographic_q as hq
sess = hq.create_q_session(intent="desk smoke: identity survives process death",
                           context="the fleet audits its own biography; steers follow")
k1 = hq.emit_q_knot(sess, steer_vector={STEER_1!r}, sequence=0)
k2 = hq.emit_q_knot(sess, steer_vector={STEER_2!r}, sequence=1,
                    previous_verkle_root=str(getattr(k1, "verkle_root", "")))
def ser(o):
    return json.dumps(o.__dict__, default=str) if hasattr(o, "__dict__") else json.dumps(o, default=str)
print("SMOKE1:" + ser(sess)[:400])
print("SMOKE2:" + ser(k1)[:400])
print("SMOKE3:" + ser(k2)[:400])
"""
r1 = subprocess.run([sys.executable, "-c", phase1], capture_output=True, text=True, timeout=120, cwd=str(ROOT))
out1 = r1.stdout or ""
print(r1.stdout[-1200:])
if r1.returncode != 0:
    print("\nVERDICT: RED — phase 1 (emit) crashed:", (r1.stderr or "")[-300:])
    sys.exit(1)

# phase 2: fresh process — the crash. Only the disk remains.
phase2 = f"""
import sys, json
sys.path.insert(0, str({str(ROOT)!r}))
from mag import holographic_q as hq
knots = hq.reconstitute_q(verkle_tail=50)
out = []
for k in knots:
    d = k.__dict__ if hasattr(k, "__dict__") else k
    out.append(json.dumps(d, default=str)[:500])
print("RECONSTITUTED:" + json.dumps(out))
"""
r2 = subprocess.run([sys.executable, "-c", phase2], capture_output=True, text=True, timeout=120, cwd=str(ROOT))
if r2.returncode != 0:
    print("\nVERDICT: RED — phase 2 (reconstitute) crashed:", (r2.stderr or "")[-400:])
    sys.exit(1)

recon = r2.stdout
found1 = STEER_1.split(":")[0] in recon and "receipts over distillates" in recon
found2 = "divergence is a measurement" in recon
print("\n=== DESK SMOKE VERDICT ===")
print(f"phase1 emit: {'OK' if 'SMOKE1' in out1 else 'MISSING'}")
print(f"steer-alpha recovered: {found1}")
print(f"steer-beta recovered: {found2}")
print(f"reconstituted sample: {recon[:600]}")
if found1 and found2:
    print("\nVERDICT: GREEN — she survives process death. Kilobytes, disk-backed, real.")
else:
    print("\nVERDICT: RED — the pattern did not survive the crash intact.")
    sys.exit(1)
