"""B2-354 falsifier probe: drop_shortcut must not record "dropped" when the
powershell run fails.

Executed 2026-09-26 with .venv/Scripts/python.exe. Disclosures:
- icon_drop.LEDGER and icon_drop.desktop_folder are monkeypatched to a temp
  dir and icon_drop._fold_training to a no-op so the real Desktop folder and
  the real ledgers (memory/icons/ledger.jsonl, skill_ledger, training_events)
  stay untouched; the powershell subprocess itself runs for real via the
  unchanged ps_exe resolution from B2-85.
- Arm A is the happy path (valid target -> status dropped, .lnk on disk).
- Arm B is the brief falsifier: a target_path containing a single quote breaks
  the WScript.Shell single-quoted string in the generated PS script, forcing a
  powershell parse error; the probe asserts the resulting ledger row is NOT
  status "dropped".
- The temp dir is removed after states are captured (disclosed here).
"""
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

spec = importlib.util.spec_from_file_location("icon_drop_under_probe", REPO / "mag" / "icon_drop.py")
icon_drop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(icon_drop)

tmp = Path(tempfile.mkdtemp(prefix="b2_354_probe_"))
tmp_ledger = tmp / "ledger.jsonl"
icon_drop.LEDGER = tmp_ledger
icon_drop.desktop_folder = lambda: tmp
icon_drop._fold_training = lambda row: None

results = {"schema": "b2_354_falsifier_probe.v1", "arms": []}

# Arm A: happy path. Target is this probe file, which exists on disk.
row_a = icon_drop.drop_shortcut("b2_354_probe_ok", str(REPO / "watch" / "inbox" / "burn_wave_20260926" / "B2_354_falsifier_probe.py"), desc="B2-354 happy arm")
lnk_a = tmp / "b2_354_probe_ok.lnk"
results["arms"].append({
    "arm": "A_happy",
    "status": row_a["status"],
    "has_error_field": "error" in row_a,
    "lnk_existed": lnk_a.is_file(),
})
assert row_a["status"] == "dropped", f"arm A regressed: {row_a}"
assert lnk_a.is_file(), "arm A: no .lnk on disk despite status dropped"

# Arm B: the falsifier. A single quote in target_path terminates the PS string
# early and forces a powershell parse error (nonzero exit, no .lnk).
row_b = icon_drop.drop_shortcut("b2_354_probe_fail", "C:\\nonexistent'b354\\x.exe", desc="B2-354 falsifier arm")
lnk_b = tmp / "b2_354_probe_fail.lnk"
results["arms"].append({
    "arm": "B_falsifier_nonzero_or_missing_lnk",
    "status": row_b["status"],
    "error": row_b.get("error", ""),
    "lnk_existed": lnk_b.is_file(),
})

# THE FALSIFIER: a failing powershell run must not record "dropped".
assert row_b["status"] != "dropped", f"FALSIFIER TRIGGERED: failing run recorded {row_b}"
assert row_b["status"] == "failed", f"expected status failed, got {row_b['status']}"
assert row_b.get("error", "").strip() != "", "failed row must name the error"

# Ledger bytes check: what landed on disk matches what the function returned.
rows_on_disk = [json.loads(line) for line in tmp_ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
results["ledger_rows_on_disk"] = [
    {"name": r.get("name"), "status": r.get("status"), "has_error": "error" in r}
    for r in rows_on_disk
]
assert rows_on_disk[-1]["status"] == "failed", "ledger bytes do not carry the failed status"

results["falsifier_holds"] = True

# Capture done; remove the temp dir (disclosed).
shutil.rmtree(tmp, ignore_errors=True)

out = REPO / "watch" / "inbox" / "burn_wave_20260926" / "B2_354_falsifier_probe_results.json"
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(results, indent=2, ensure_ascii=False))
