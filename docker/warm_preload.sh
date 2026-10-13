#!/bin/bash
# Read blade_templates.json at runtime and ollama-pull every named model.
# Registry changes do not require an image rebuild (bind mount or replace the JSON).
# status.json shape: boot_watcher.py parses "phase":"..."; SUCCESS = READY.
set -u
REG="${BLADE_TEMPLATES:-/opt/mag/blade_templates.json}"
if [ -f /root/blade_templates.json ]; then
  REG=/root/blade_templates.json
fi
mkdir -p /root
echo '{"phase": "pull"}' > /root/status.json
if [ ! -f "$REG" ]; then
  echo "warm_preload: registry missing at $REG" >&2
  echo '{"phase": "READY"}' > /root/status.json
  exit 0
fi
export BLADE_TEMPLATES="$REG"
python3 - <<'PY'
import json, os, re, subprocess, sys
path = os.environ["BLADE_TEMPLATES"]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
models = []
seen = set()
for t in data.get("templates") or []:
    named = list(t.get("models") or [])
    named += re.findall(r"ollama pull ([^\s|&;]+)", str(t.get("onstart_cmd") or ""))
    for m in named:
        m = m.strip().strip("\"'")
        if m and m not in seen:
            seen.add(m)
            models.append(m)
print("warm_preload models:", " ".join(models), flush=True)
for m in models:
    rc = subprocess.call(["ollama", "pull", m])
    if rc != 0:
        print("warm_preload WARN pull failed:", m, file=sys.stderr, flush=True)
PY
echo '{"phase": "READY"}' > /root/status.json
echo "warm_preload: READY"
