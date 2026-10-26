#!/usr/bin/env bash
# Tortoise DBC verification: sha256 every extracted .dbc in /data against the
# repo's own EXPECTED_HASHES manifest (tools/dbc_verification/dbc_verifier.py).
# Standalone because the verifier script itself is host-side read-only; this
# re-implements its check in pure sha256sum so the container needs no python.
set -u
VER_DIR="/ver"
DATA_DIR="/data"
python3 - "$VER_DIR" "$DATA_DIR" <<'EOF'
import hashlib, json, sys, glob, os
ver, data = sys.argv[1], sys.argv[2]
expected = json.load(open(os.path.join(ver, "manifest.json"))) if os.path.exists(os.path.join(ver, "manifest.json")) else None
# fall back to parsing EXPECTED_HASHES from the script itself
if not expected:
    expected = {}
    for line in open(os.path.join(ver, "dbc_verifier.py"), encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith('"') and '": "' in line and line.endswith('",'):
            name, h = line[1:].split('": "', 1)
            expected[name] = h.rstrip('",')
ok = bad = miss = 0
files = glob.glob(os.path.join(data, "**", "*.dbc"), recursive=True)
for f in files:
    name = os.path.basename(f)
    if name not in expected:
        continue
    h = hashlib.sha256(open(f, "rb").read()).hexdigest()
    if h == expected[name]:
        ok += 1
    else:
        bad += 1
        print("MISMATCH:", name, h[:16], "!=", expected[name][:16])
for name in expected:
    if not any(os.path.basename(f) == name for f in files):
        miss += 1
        if miss <= 5:
            print("MISSING:", name)
print(f"VERDICT: {ok} match, {bad} mismatch, {miss} missing of {len(expected)} expected")
EOF
