"""executor-sweep finish-line check battery (lane: gala_20260925/build-it-all).

Runs the byte checks for the routing-table sweep: consumer greps, empirical
production ledgers, the fail-closed proof for the killed verkle_link bucket,
and the doctrine_arbiter instrument census. Pure-read except the fail-closed
proof, which monkeypatches RECEIPTS_DIR to a temp dir so nothing lands in the
production receipt tree.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[5]
OUT = []
sys.path.insert(0, str(ROOT))


def check(name, body):
    OUT.append(f"### {name}")
    OUT.append(body)
    OUT.append("")


# CHECK 1: verkle_link references in code dirs (post-kill: only kill markers)
r = subprocess.run(
    ["grep", "-rln", "verkle_link", "mag/", "tools/", "tests/", "main.py",
     "scripts/", "configs/"],
    cwd=ROOT, capture_output=True, text=True)
files = [l for l in r.stdout.strip().splitlines() if "__pycache__" not in l]
check("CHECK 1: verkle_link references in code dirs (expected: 3 mag files, kill markers only)",
      "exit=" + str(r.returncode) + " files=" + json.dumps(files))

# CHECK 2: remaining occurrences are comment/status text only (no live route)
live = []
for f in files:
    for i, line in enumerate(
            (ROOT / f).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        s = line.strip()
        if "verkle_link" in s and not (s.startswith("#") or s.startswith("//")) \
                and not s.startswith('"') and '"' not in s.split("verkle_link")[0][-1:]:
            live.append(f"{f}:{i}: {s.strip()[:90]}")
check("CHECK 2: live (non-comment) verkle_link occurrences (expected: none)",
      "count=" + str(len(live)) + (" rows=" + json.dumps(live) if live else ""))

# CHECK 3: production meter rows by effect
rows = [json.loads(l) for l in
        (ROOT / "memory/runs/effect_broker/effects.jsonl").read_text(
            encoding="utf-8").splitlines() if l.strip()]
check("CHECK 3: memory/runs/effect_broker/effects.jsonl by effect (production meter)",
      f"total={len(rows)} by_effect={dict(Counter(r.get('effect') for r in rows))}")

# CHECK 4: broker receipt census per class, split test vs non-test
d = ROOT / "memory/runs/effect_broker"
census = {}
for p in d.glob("*.json"):
    name = p.name
    eff = name.split("_")[0]
    for e in ("board_write", "verkle_link", "tool_invoke", "model_call",
              "network_access", "fs_write", "lane_spawn"):
        if f"_{e}_" in name:
            key = e
            cls = "test" if name.startswith("test-") else "nontest"
            census.setdefault(e, {}).setdefault(cls, 0)
            census[e][cls] += 1
            break
check("CHECK 4: receipt census (test-prefixed vs non-test) by effect class",
      json.dumps(census, sort_keys=True))

# CHECK 5: switchboard trail census for the three reconcile-declared effects
trail = ROOT / "memory/runs/switchboard/trail.jsonl"
tc = {"verkle_link": Counter(), "tool_invoke": Counter(), "lane_spawn": Counter()}
for l in trail.read_text(encoding="utf-8").splitlines():
    if not l.strip():
        continue
    rj = json.loads(l)
    eff = rj.get("requested_effect") or rj.get("effect") or ""
    if eff in tc:
        tc[eff][rj.get("status", "?")] += 1
check("CHECK 5: switchboard trail rows by effect/status (reconcile proposals)",
      json.dumps({k: dict(v) for k, v in tc.items()}))

# CHECK 6: fail-closed proof for the killed bucket
from mag import effect_broker as eb  # noqa: E402
from mag import policy_engine as pe  # noqa: E402
tmp = Path(tempfile.mkdtemp(prefix="executor_sweep_"))
eb.ROOT = tmp
eb.RECEIPTS_DIR = tmp / "receipts"
auth = {"status": "AUTHORIZED", "granted_capabilities": ["verkle_link"],
        "event_id": "test-executor-sweep-failclosed"}
rec = eb.execute("verkle_link", {}, auth)
v = pe.validate_authority(auth, "verkle_link")
check("CHECK 6: fail-closed proof execute('verkle_link') + validate_authority",
      f"broker_status={rec.get('status')} broker_error={rec.get('error')!r} "
      f"authority_ok={v.get('ok')} authority_reason={v.get('reason')!r}")

# CHECK 7: BROKERS dict keys after the kill
check("CHECK 7: mag.effect_broker.BROKERS keys after kill",
      json.dumps(sorted(eb.BROKERS.keys())))

# CHECK 8: doctrine_arbiter instrument consumers (registrations in LEDGER)
drows = [json.loads(l) for l in
         (ROOT / "memory/doctrine/LEDGER.jsonl").read_text(
             encoding="utf-8").splitlines() if l.strip()]
regs = [r for r in drows if r.get("type") == "registration"]
check("CHECK 8: doctrine ledger registrations by instrument/kind/status",
      f"registrations={len(regs)} "
      f"instruments={dict(Counter(r.get('predicted_outcome', {}).get('instrument') for r in regs))} "
      f"kinds={dict(Counter(r.get('kind') for r in regs))} "
      f"statuses={dict(Counter(r.get('status') for r in regs))}")

# CHECK 9: doctrine_arbiter production consumer (cycle_brief scorecard call)
r = subprocess.run(["grep", "-n", "doctrine_arbiter", "tools/cycle_brief.py"],
                   cwd=ROOT, capture_output=True, text=True)
check("CHECK 9: doctrine_arbiter consumer in tools/cycle_brief.py",
      r.stdout.strip() or "NO MATCHES")

print("\n".join(OUT))
