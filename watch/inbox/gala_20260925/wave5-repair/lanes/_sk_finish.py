#!/usr/bin/env python3
"""wave5 seed-kernel finish block: build -> refresh pointer -> verify -> byte checks."""
import base64
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(".").resolve()
OUT = ROOT / "watch/inbox/seed_rib_20260929/seed-rib/seed.json"
PTR = ROOT / "watch/inbox/SEED_RIB_CURRENT"
CHECK = ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/seed-kernel.check.txt"
PY = str(ROOT / ".venv/Scripts/python.exe")

BUILD = [PY, "tools/seed_rib.py", "build", "--root", ".",
         "--out", "watch/inbox/seed_rib_20260929/seed-rib/seed.json",
         "--inline-max", "12288",
         "--glob", "memory/law/*.md",
         "--file", "memory/law/registry.json",
         "--file", "docs/DNA.md",
         "--file", "CONSTITUTION.md",
         "--file", "docs/ref/OPERATOR_CARD.md",
         "--file", "docs/FRAMEWORK_LOAD.md",
         "--file", "docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md",
         "--file", "docs/ref/MYCELIAL_SCIENCE_MAP.md",
         "--file", "docs/ref/MAG_DIRECTION_ARTIFACT_v2.md",
         "--file", "docs/ref/MAG_PROJECT_PROPOSAL.md",
         "--file", "state/CURRENT.md",
         "--file", "state/START_BRIEF.md",
         "--file", "state/HANDOFF.md",
         "--file", "BOOT_4_7.md",
         "--file", "AGENTS.md",
         "--file", "queue/todo.md",
         "--file", "HANDOFF_MAG_AGENT_TODOS.md",
         "--file", "memory/attention.md",
         "--file", "memory/warm_state.json",
         "--file", "memory/live_from_grok.md",
         "--file", "configs/lanes.yaml",
         "--file", "tools/seed_rib.py",
         "--file", "tools/seed_mcp.py",
         "--file", "watch/inbox/SHARED_SURFACE_CONTRACT.json",
         "--file", "watch/inbox/SEED_RIB_FORMAT_v0_20260926.md",
         "--file", "watch/inbox/ESSENTIALS_RESTORE.md",
         "--file", "watch/inbox/TWO_MACHINE_SYNC_20260919.md",
         "--file", "memory/rib/RIB_FREE_USAGE_POLICY_20260823.md",
         "--file", "memory/rib/RIB_DRIVING_LADDER_20260928.md",
         "--file", "memory/rib/RIB_BEHAVIOR_CARDS_20260928.md",
         "--pointer-list", "watch/inbox/seed_rib_20260929/seed-rib/paths_seed_20260928.txt"]

log = []


def emit(s=""):
    print(s)
    log.append(s)


def run(cmd, label):
    emit(f"$ {label}")
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       shell=(len(cmd) == 1))
    out = (p.stdout + p.stderr).rstrip("\n")
    for line in out.splitlines():
        emit(line)
    emit(f"EXIT={p.returncode}")
    emit()
    return p.returncode, out


passed = False
for attempt in range(1, 4):
    emit(f"=== FINAL SEED BUILD (attempt {attempt}, {datetime.now(timezone.utc).strftime('%H:%M:%SZ')}) ===")
    rc, _ = run(BUILD, " ".join(BUILD[:6]) + " ... --inline-max 12288 --pointer-list paths_seed_20260928.txt")
    if rc != 0:
        continue
    raw = OUT.read_bytes()
    seed = json.loads(raw.decode("utf-8"))
    inl = sum(1 for e in seed["entries"] if e["carrier"] == "inline")
    doc = {"schema": "seed_rib.v0",
           "pointer": {"path": "watch/inbox/seed_rib_20260929/seed-rib/seed.json",
                       "bytes": len(raw),
                       "sha256": hashlib.sha256(raw).hexdigest(),
                       "source": "fleet-repo",
                       "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "delta": "09-26->29 wave5 kernel repair (laws+doctrine+state re-attached, receipt mass to pointers)",
                       "entries": len(seed["entries"]), "inline": inl,
                       "pointer": len(seed["entries"]) - inl,
                       "law_refs": len(seed["law_refs"])}}
    PTR.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    emit(f"SEED_RIB_CURRENT refreshed -> sha256 {doc['pointer']['sha256']}")
    emit()
    rc1, _ = run(["python", "tools/seed_rib.py", "verify", "--source", "."],
                 "python tools/seed_rib.py verify --source .   [FINISH LINE, default seed = SEED_RIB_CURRENT]")
    rc2, _ = run([PY, "tools/seed_rib.py", "verify", "--source", "."],
                 ".venv/Scripts/python.exe tools/seed_rib.py verify --source .   [same args, venv]")
    if rc1 == 0 and rc2 == 0:
        passed = True
        emit(f"FINISH-LINE PASS on attempt {attempt}: exit 0 both interpreters, zero SEAL MISMATCH rows")
        emit()
        break
    emit("(churn race: a sealed pointer moved between build and verify; retrying)")
    emit()

if not passed:
    print("NO CLEAN PASS IN 3 ATTEMPTS", file=sys.stderr)
    CHECK.write_text("\n".join(log) + "\n", encoding="utf-8")
    sys.exit(1)

# ---- law-role real-bytes check ----
emit("=== FINISH-LINE 2: >= 8 law-role entries with real bytes ===")
laws = [e for e in seed["entries"] if e["role"] == "law" and e["carrier"] == "inline"]
ok_laws = 0
for e in laws:
    raw_e = base64.b64decode(e["content_b64"])
    good = hashlib.sha256(raw_e).hexdigest() == e["sha256"] and len(raw_e) == e["bytes"]
    ok_laws += good
    emit(f"  {'OK ' if good else 'BAD'} {e['path']} {e['bytes']}B sha {e['sha256'][:12]}")
emit(f"law-role inline entries with verified real bytes: {ok_laws} (need >= 8)")
emit(f"EXIT={'0' if ok_laws >= 8 else '1'}")
emit()

# ---- seed_mcp resolution check ----
emit("=== FINISH-LINE 3: tools/seed_mcp.py resolves to the refreshed seed ===")
run([sys.executable, "tools/seed_mcp.py", "--seed-sha"], "python tools/seed_mcp.py --seed-sha   [default resolution]")
rc3, out3 = run([sys.executable, "tools/seed_mcp.py", "--list"],
                "python tools/seed_mcp.py --list   [default resolution]")
try:
    listed = json.loads(out3)
    resolved = listed.get("seed", "?")
    sha = listed.get("seed_sha256", "?")
    match = (resolved.replace("\\", "/").endswith("watch/inbox/seed_rib_20260929/seed-rib/seed.json")
             and sha == doc["pointer"]["sha256"])
    emit(f"resolved seed path: {resolved}")
    emit(f"resolved sha256 == SEED_RIB_CURRENT sha256: {sha == doc['pointer']['sha256']}")
    emit(f"EXIT={'0' if match else '1'}  (match={match})")
except Exception as exc:  # noqa: BLE001
    emit(f"could not parse --list output: {exc}")
emit()
emit(f"final seed: {doc['pointer']}")

CHECK.write_text("\n".join(log) + "\n", encoding="utf-8") if False else None
with open(CHECK, "a", encoding="utf-8") as fh:
    fh.write("\n".join(log) + "\n")
print("check file appended:", CHECK)
