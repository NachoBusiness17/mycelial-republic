#!/usr/bin/env python
"""B2-306 falsifier probe (B2_256 pattern): deleting a 0.5 cipher keeper row
must fail verifier check7.

Copies the live ledger to a temp file, drops the 147434025 / 2017-11-03
"11.3 - Podesta indicted" 0.5 row, points the verifier at the temp copy, and
runs its main(). Checks 1-5 stay green by construction (the row is well
formed and traces), so the delete is exactly the class the pin exists for.
The live ledger is never modified; its sha256 is re-verified after the run.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_306_falsifier_probe.py
Exits 0 when the pin FIRED (falsifier satisfied), 1 when it did not.
"""
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LIVE = ROOT / "watch" / "inbox" / "qdrop_export" / "q_caption_ledger.jsonl"
VER = ROOT / "scripts" / "the50_t21_q_caption_ledger_verify.py"

sha_before = hashlib.sha256(LIVE.read_bytes()).hexdigest()

spec = importlib.util.spec_from_file_location("t21ver", VER)
ver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ver)

with tempfile.TemporaryDirectory() as td:
    tmp = Path(td) / "q_caption_ledger.jsonl"
    rows = [json.loads(l) for l in LIVE.open(encoding="utf-8") if l.strip()]
    kept = [r for r in rows
            if not (r["id"] == "147434025" and r["date"] == "2017-11-03"
                    and r["confidence"] == 0.5)]
    assert len(kept) == len(rows) - 1, "target row not found"
    tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in kept) + "\n",
                   encoding="utf-8")
    ver.OUT = tmp  # verify against the mutilated copy
    rc = ver.main()

sha_after = hashlib.sha256(LIVE.read_bytes()).hexdigest()
print("---")
print("pin fired:", rc == 1)
print("live ledger untouched:", sha_before == sha_after)
sys.exit(0 if rc == 1 and sha_before == sha_after else 1)
