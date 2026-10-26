"""w4-18 field probe: scatter the estate's flat JSONL receipts into cells of a
labeled measurement space and print the marginals. Read-only; no subprocess.

Surfaces (all cited in w4-18.md):
  S1 memory/workflows/REGISTRY.jsonl   (gate receipts, tools/workflow_gate.py:307-317)
  S2 memory/trajectory/steps.jsonl     (trajectory_step.v1 tape, mag/trajectory_step.py:61-83)
  S3 catalog/catalog.jsonl             (corpus catalog rows)
  S4 watch/inbox/index_events.jsonl    (the log INDEX.json is folded from)
  T1 twin pairs: byte-identity as a diagonal constraint
  C1 census-claim carrier vs tape count: two instruments, two denominators
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FLASH = Path(__file__).resolve().parent

def rows(path):
    out = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                out.append(json.loads(ln))
            except Exception:
                pass
    return out

print("== S1 REGISTRY.jsonl ==")
reg = rows(ROOT / "memory/workflows/REGISTRY.jsonl")
print(f"rows={len(reg)}")
print(f"verdict={dict(Counter(r.get('verdict') for r in reg))}")
print(f"key_union={sorted(set().union(*(r.keys() for r in reg)))}")
day_verdict = defaultdict(int)
for r in reg:
    day_verdict[(str(r.get("ts", ""))[:10], r.get("verdict"))] += 1
days = sorted({d for d, _ in day_verdict})
print("day x verdict marginal:")
for d in days:
    line = "  " + d + "  "
    for v in ("PASS", "FAIL"):
        line += f"{v}={day_verdict.get((d, v), 0):3d}  "
    print(line)
print("FAIL row names (the dense cells):")
for r in reg:
    if r.get("verdict") == "FAIL":
        fails = [c["id"] for c in r.get("checks", []) if not c.get("ok")]
        print(f"  {str(r.get('ts'))[:16]}  {r.get('name')}  digest={r.get('digest')}  failed={fails}")
gate_ok = Counter()
for r in reg:
    for c in r.get("checks", []):
        gate_ok[(c.get("id"), bool(c.get("ok")))] += 1
gates = sorted({g for g, _ in gate_ok})
print("gate x ok marginal (ok=True / ok=False):")
for g in gates:
    print(f"  {g:22s} ok={gate_ok.get((g, True), 0):4d}  fail={gate_ok.get((g, False), 0):4d}")
checks_per_row = [len(r.get("checks", [])) for r in reg]
print(f"nested rank-2 'checks' array: rows_with_checks={sum(1 for n in checks_per_row if n)} max={max(checks_per_row)}")

print("== S2 steps.jsonl (live tape) ==")
tape = ROOT / "memory/trajectory/steps.jsonl"
n = ok = 0
schemas = Counter()
faces = Counter()
per_day = Counter()
import datetime as dt
today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
with open(tape, encoding="utf-8", errors="replace") as f:
    for ln in f:
        ln = ln.strip()
        if not ln:
            continue
        try:
            r = json.loads(ln)
        except Exception:
            continue
        n += 1
        schemas[r.get("schema_version", "<absent>")] += 1
        faces[r.get("face", "<absent>")] += 1
        d = str(r.get("ts", ""))[:10]
        per_day[d] += 1
        try:
            basis = "|".join([r["session_id"], r["ts"], r["command"], r["result"]["output_excerpt"]])
            if hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16] == r["step_hash"]:
                ok += 1
        except Exception:
            pass
print(f"rows={n} hash_clean={ok}/{n} bytes={tape.stat().st_size}")
print(f"schema_version census={dict(schemas)}")
print(f"face census={dict(faces)}")
print("last 5 UTC days of tape rows (day marginal):")
for d in sorted(per_day)[-5:]:
    print(f"  {d}  {per_day[d]:5d}  {'<== today' if d == today else ''}")

print("== S3 catalog.jsonl ==")
cat = rows(ROOT / "catalog/catalog.jsonl")
print(f"rows={len(reg)} (registry) vs catalog rows={len(cat)}")
print(f"catalog key_union={sorted(set().union(*(r.keys() for r in cat)))}")
print(f"catalog id_len census={dict(Counter(len(str(r.get('id',''))) for r in cat))}")
print(f"catalog zone census (top6)={dict(Counter(r.get('zone') for r in cat).most_common(6))}")

print("== S4 index_events.jsonl ==")
ev = rows(ROOT / "watch/inbox/index_events.jsonl")
print(f"events={len(ev)}")
print(f"event key_union={sorted(set().union(*(r.keys() for r in ev)))}")
wc = Counter(str(r.get("writer", r.get("who", "<absent>"))) for r in ev)
print(f"writer census (top8)={dict(wc.most_common(8))}")

print("== T1 twin diagonal (byte identity as structure) ==")
pairs = [
    ("s2-06.md", "secret-gate-gaps.md", "4560df0720f8b8bb", 16725),
    ("s2-24.md", "decorator-census.md", "446f921b1a58f0d6", 15107),
]
for a, b, claimed_sha, claimed_bytes in pairs:
    pa, pb = FLASH / a, FLASH / b
    ba, bb = pa.read_bytes(), pb.read_bytes()
    ha, hb = hashlib.sha256(ba).hexdigest(), hashlib.sha256(bb).hexdigest()
    print(f"  {a} vs {b}: identical={ba == bb} bytes={len(ba)} (commit claimed {claimed_bytes}) "
          f"sha256[:16]={ha[:16]} (commit claimed {claimed_sha}) match={ha[:16] == claimed_sha and len(ba) == claimed_bytes}")

print("== C1 two instruments, two denominators (comparability as shape check) ==")
sys.path.insert(0, str(ROOT))
from tools.census_drift_patrol import parse_carrier  # noqa: E402
agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
claim = parse_carrier(agents)
print(f"instrument=pytest--collect-only cell: collected={claim['collected']} files={claim['files']} moment={claim['date']}")
print(f"instrument=trajectory-tape    cell: steps_total={n} moment={today}")
print("B2-216: differencing these two numbers is ILLEGAL (different instrument, moment, tree); "
      "in a typed tensor this is a shape error, not an operator discipline.")
