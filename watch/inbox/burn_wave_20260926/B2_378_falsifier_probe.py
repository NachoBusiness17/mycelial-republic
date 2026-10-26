"""B2-378 falsifier probe: a failed or skipped icon_drop row must not record
outcome "ok" in skill_ledger.

Executed 2026-09-26 with .venv/Scripts/python.exe. Disclosures:
- All four write paths are sandboxed to a temp dir: icon_drop.LEDGER and
  icon_drop.desktop_folder (the icons ledger and the Desktop surface), plus
  mag.skill_ledger.DECISIONS_PATH and mag.training_events.EVENTS_PATH, so the
  real Desktop folder and the real ledgers stay untouched; _fold_training and
  drop_shortcut (the mag.skill_ledger / mag.training_events imports, the ps_exe
  resolution, the powershell subprocess, the status decision) run as the real
  unchanged code.
- Arm B forces the powershell failure by pointing the SANDBOXED desktop
  surface at a regular FILE (not a directory), so the real WScript.Shell Save
  inside the real powershell throws (nonzero exit, no .lnk). The B2-354
  single-quote injection route was considered first but died mid-lane: the
  concurrent B2-377 escaping landing (drop_shortcut now filters the name and
  routes every literal through _ps_quote) turned that injection into a happy
  path by design, so the failure is forced at the filesystem level instead,
  which holds under both byte states.
- Arm C and arm D call _fold_training directly with synthetic rows
  (skipped_no_powershell, and a row with no status at all) to pin the else
  branch of the pass-through.
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

import mag.skill_ledger
import mag.training_events

spec = importlib.util.spec_from_file_location("icon_drop_under_probe", REPO / "mag" / "icon_drop.py")
icon_drop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(icon_drop)

tmp = Path(tempfile.mkdtemp(prefix="b2_378_probe_"))
tmp.mkdir(parents=True, exist_ok=True)
icon_drop.LEDGER = tmp / "icons_ledger.jsonl"
icon_drop.desktop_folder = lambda: tmp
mag.skill_ledger.DECISIONS_PATH = tmp / "skill_decisions.jsonl"
mag.training_events.EVENTS_PATH = tmp / "training_events.jsonl"

results: dict = {"schema": "b2_378_falsifier_probe.v1", "arms": []}


def last_decision() -> dict:
    lines = mag.skill_ledger.DECISIONS_PATH.read_text(encoding="utf-8").splitlines()
    return json.loads([ln for ln in lines if ln.strip()][-1])


# Arm A: happy path. A valid target, a valid name; the real powershell Save.
row_a = icon_drop.drop_shortcut("b2_378_probe_ok", str(REPO / "watch" / "inbox" / "burn_wave_20260926" / "B2_378_falsifier_probe.py"), desc="B2-378 happy arm")
dec_a = last_decision()
results["arms"].append({
    "arm": "A_happy",
    "row_status": row_a["status"],
    "decision_outcome": dec_a.get("outcome"),
    "decision_detail": dec_a.get("detail"),
    "lnk_existed": (tmp / "b2_378_probe_ok.lnk").is_file(),
})
assert row_a["status"] == "dropped", f"arm A regressed: {row_a}"
assert dec_a.get("outcome") == "ok", f"arm A: a dropped row must record outcome ok, got {dec_a.get('outcome')}"

# Arm B: THE FALSIFIER. The sandboxed desktop surface is now a regular file,
# so the real WScript.Shell Save has no directory to write into: powershell
# exits nonzero, no .lnk, drop_shortcut records failed.
blocker = tmp / "not_a_dir.txt"
blocker.write_text("desktop surface patched to a file for arm B", encoding="utf-8")
icon_drop.desktop_folder = lambda: blocker
row_b = icon_drop.drop_shortcut("b2_378_probe_fail", str(REPO / "watch" / "inbox" / "burn_wave_20260926" / "B2_378_falsifier_probe.py"), desc="B2-378 falsifier arm")
dec_b = last_decision()
results["arms"].append({
    "arm": "B_falsifier_failed_row",
    "row_status": row_b["status"],
    "row_error_head": (row_b.get("error") or "")[:160],
    "decision_outcome": dec_b.get("outcome"),
    "lnk_existed": (blocker / "b2_378_probe_fail.lnk").is_file(),
})
assert row_b["status"] == "failed", f"arm B: expected failed row, got {row_b}"
assert dec_b.get("outcome") != "ok", f"FALSIFIER TRIGGERED: failed row recorded outcome {dec_b.get('outcome')}"
assert dec_b.get("outcome") == "failed", f"arm B: outcome must carry the status string, got {dec_b.get('outcome')}"

# Arm C: the B2-85 skip arm folded directly (synthetic row, the real fold).
icon_drop._fold_training({"name": "b2_378_probe_skip", "status": "skipped_no_powershell", "path": "nul"})
dec_c = last_decision()
results["arms"].append({
    "arm": "C_skipped_no_powershell",
    "decision_outcome": dec_c.get("outcome"),
})
assert dec_c.get("outcome") == "skipped_no_powershell", f"arm C: expected status string, got {dec_c.get('outcome')}"
assert dec_c.get("outcome") != "ok", "FALSIFIER TRIGGERED: skipped row recorded outcome ok"

# Arm D: a row with no status at all must not fold as a win either.
icon_drop._fold_training({"name": "b2_378_probe_nostatus"})
dec_d = last_decision()
results["arms"].append({
    "arm": "D_no_status",
    "decision_outcome": dec_d.get("outcome"),
})
assert dec_d.get("outcome") == "unknown", f"arm D: expected unknown, got {dec_d.get('outcome')}"
assert dec_d.get("outcome") != "ok", "FALSIFIER TRIGGERED: statusless row recorded outcome ok"

# Bytes on disk: the decisions ledger carries the outcomes in order, and the
# training events still carry the row status per emit.
decisions_on_disk = [
    json.loads(ln) for ln in mag.skill_ledger.DECISIONS_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()
]
results["decisions_outcomes_on_disk"] = [d.get("outcome") for d in decisions_on_disk]
assert [d.get("outcome") for d in decisions_on_disk] == ["ok", "failed", "skipped_no_powershell", "unknown"]

events_on_disk = [
    json.loads(ln) for ln in mag.training_events.EVENTS_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()
]
results["training_event_statuses_on_disk"] = [e.get("outcome", {}).get("status") for e in events_on_disk]
assert results["training_event_statuses_on_disk"] == ["dropped", "failed", "skipped_no_powershell", None]

results["falsifier_holds"] = True

# Capture done; remove the temp dir (disclosed).
shutil.rmtree(tmp, ignore_errors=True)

out = REPO / "watch" / "inbox" / "burn_wave_20260926" / "B2_378_falsifier_probe_results.json"
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(results, indent=2, ensure_ascii=False))
