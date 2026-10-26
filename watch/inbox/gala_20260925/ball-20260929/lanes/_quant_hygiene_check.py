#!/usr/bin/env python3
"""Finish-line byte checks for the quantizer-hygiene lane (ball-20260929).

Instrument only: READS estate files, writes nothing outside its stdout.
Raw stdout is captured to quantizer-hygiene.check.txt by the caller.
Run: .venv/Scripts/python.exe watch/inbox/gala_20260925/ball-20260929/lanes/_quant_hygiene_check.py
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
QT = ROOT / "memory" / "corpus" / "quantized_thought"


def section(title: str) -> None:
    print("")
    print("=" * 72)
    print(title)
    print("=" * 72)


# ---- 1. fresh compile (the finish line demands a FRESH compile) -------------
section("CHECK 1: fresh compile (v0.4) + fossil arm")
r = subprocess.run([sys.executable, str(ROOT / "tools" / "thought_quantizer.py"), "compile"],
                   capture_output=True, text=True)
print("$ .venv/Scripts/python.exe tools/thought_quantizer.py compile")
print(r.stdout.strip())
if r.stderr.strip():
    print("STDERR:", r.stderr.strip())
print(f"exit={r.returncode}")
r = subprocess.run([sys.executable, str(ROOT / "tools" / "thought_quantizer.py"), "--check"],
                   capture_output=True, text=True)
print("$ .venv/Scripts/python.exe tools/thought_quantizer.py --check")
print(r.stdout.strip())
print(f"exit={r.returncode}")

# ---- 2. zero shell-error fragments in any pack ------------------------------
section("CHECK 2: zero shell-error fragments in any pack")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import thought_quantizer as tq  # noqa: E402

total_hits = 0
for tier in ("frontier", "flash", "local"):
    rows = [json.loads(x) for x
            in (QT / f"instructions_{tier}.jsonl").read_text(encoding="utf-8").splitlines()
            if x.strip()]
    hits = []
    for row in rows:
        for field in ("frontier", "flash", "local"):
            txt = row.get(field)
            if txt and tq.SHELL_ERROR_RE.search(txt):
                hits.append((row["id"], field, txt[:100]))
    for frag_id in ("de7eaa711459", "d536890f0abc", "ae3af609ff99"):
        if any(row["id"] == frag_id for row in rows):
            hits.append((frag_id, "id", "baseline errno row still packed"))
    total_hits += len(hits)
    print(f"{tier}: rows={len(rows)} shell_error_hits={len(hits)}")
    for h in hits:
        print(f"  HIT {h}")
print(f"TOTAL shell-error fragments across all packs: {total_hits} (finish line requires 0)")

# ---- 3. decay constant defined exactly once, imported at three sites --------
section("CHECK 3: PACK_STALE_DAYS defined once, imported at all three sites")
const_rel = "mag/constants.py"
defs = [i + 1 for i, line in enumerate((ROOT / const_rel).read_text(encoding="utf-8").splitlines())
        if re.match(r"^PACK_STALE_DAYS\s*=", line)]
print(f"{const_rel} assignment lines: {defs} (require exactly 1)")
for site in ("tools/thought_quantizer.py", "mag/context_pack.py", "tools/freshness_check.py"):
    lines = [i + 1 for i, line in enumerate((ROOT / site).read_text(encoding="utf-8").splitlines())
             if re.match(r"^from mag\.constants import PACK_STALE_DAYS", line)]
    print(f"{site}: import at lines {lines}")
# stale-bar legacy values must be gone from the two retargeted sites
for site, legacy in [("mag/context_pack.py", "if age_d > 7.0"),
                     ("tools/thought_quantizer.py", "max_age_hours"),
                     ("tools/freshness_check.py", "^STALE_DAYS = 7")]:
    body = (ROOT / site).read_text(encoding="utf-8").splitlines()
    found = [i + 1 for i, line in enumerate(body)
             if (line.strip() == legacy if legacy.startswith("^")
                 else legacy in line)]
    print(f"{site}: legacy bar {legacy!r} occurrences: {found} (require 0)")

# live parity: producer, consumer, boot resolve the SAME constant object
from mag.constants import PACK_STALE_DAYS as DEFINED  # noqa: E402
from mag import context_pack as cp  # noqa: E402
spec = importlib.util.spec_from_file_location(
    "freshness_check_live", ROOT / "tools" / "freshness_check.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print(f"mag.constants.PACK_STALE_DAYS = {DEFINED}")
print(f"producer parity (tq.PACK_STALE_DAYS is DEFINED): {tq.PACK_STALE_DAYS is DEFINED}")
print(f"consumer parity (cp.PACK_STALE_DAYS is DEFINED): {cp.PACK_STALE_DAYS is DEFINED}")
print(f"boot parity (freshness.STALE_DAYS is DEFINED): {mod.STALE_DAYS is DEFINED}")

# ---- 4. kept-laws == packed-laws across tiers -------------------------------
section("CHECK 4: kept == packed across tiers")
rep = json.loads((QT / "compile_report.json").read_text(encoding="utf-8"))
stats = rep["stats"]
print(f"report v{rep['v']} stats: {json.dumps(stats)}")
sum_rows = 0
for tier in ("frontier", "flash", "local"):
    n = sum(1 for x in (QT / f"instructions_{tier}.jsonl").read_text(encoding="utf-8").splitlines() if x.strip())
    sum_rows += n
    print(f"instructions_{tier}.jsonl rows: {n} (report packs: {rep['packs'].get(tier)})")
print(f"sum of pack rows: {sum_rows} | report kept: {stats['kept']} | report packed: {stats['packed']}")
print(f"kept == packed: {stats['kept'] == stats['packed'] == sum_rows} (finish line requires True)")

# ---- 5. pytest: quantizer + context-pack + bridge suites --------------------
section("CHECK 5: pytest suites touched by this lane")
for args in (
    ["tests/test_thought_quantizer.py", "tests/test_context_pack_quantized_laws.py"],
    ["tests/test_mcp_bridge_r1.py"],
):
    r = subprocess.run([sys.executable, "-m", "pytest", *args, "-q"],
                       capture_output=True, text=True, cwd=ROOT)
    tail = [ln for ln in r.stdout.strip().splitlines() if ln.strip()][-1:]
    print(f"$ pytest {' '.join(args)} -q")
    print(f"  {tail[0] if tail else '<no output>'}")
    print(f"  exit={r.returncode}")

# ---- 6. em/en dash scan over the files this lane wrote ----------------------
section("CHECK 6: em/en dash scan over lane-written sources")
for rel in ("tools/thought_quantizer.py", "tools/freshness_check.py",
            "mag/constants.py", "mag/context_pack.py", "mag/estate_bridge.py",
            "tests/test_thought_quantizer.py"):
    body = (ROOT / rel).read_text(encoding="utf-8")
    print(f"{rel}: em={body.count(chr(0x2014))} en={body.count(chr(0x2013))}")

print("")
print("CHECKS COMPLETE")
