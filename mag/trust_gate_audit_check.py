#!/usr/bin/env python3
"""Audit sanity checks for trust_gate module.
Runs a minimal set of asserts to verify that:
1. Novel content is ACCEPTed.
2. Duplicate content is REJECTed.
3. Low‑trust source is REJECTed.
4. Low‑entropy spam is QUARANTINEd.
These checks are executed before external audit.
"""
import json, sys
from pathlib import Path
# Ensure repository root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from mag.trust_gate import gate, SEEN_FILE

def reset_seen():
    if SEEN_FILE.is_file():
        SEED = SEEN_FILE.parent / "seen.json"
        SEED.unlink()
    # clear any quarantine files
    qdir = Path(__file__).resolve().parent / "memory" / "trust_gate" / "quarantine"
    if qdir.is_dir():
        for p in qdir.iterdir():
            p.unlink()

def run():
    reset_seen()
    # 1. Novel
    res1 = gate("unique content example", source="operator")
    assert res1["verdict"] == "ACCEPT", f"Expected ACCEPT, got {res1['verdict']}"
    # 2. Duplicate
    res2 = gate("unique content example", source="operator")
    assert res2["verdict"] == "REJECT", f"Expected REJECT duplicate, got {res2['verdict']}"
    # 3. Low trust
    res3 = gate("another unique content", source="unknown")
    assert res3["verdict"] == "REJECT", f"Expected REJECT low‑trust, got {res3['verdict']}"
    # 4. Low entropy spam -> quarantine
    spam = "spam " * 20
    res4 = gate(spam, source="operator")
    assert res4["verdict"] == "QUARANTINE", f"Expected QUARANTINE, got {res4['verdict']}"
    print(json.dumps({"status": "all checks passed"}, indent=2))

if __name__ == "__main__":
    run()
