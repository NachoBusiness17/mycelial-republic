"""deep-verkle-formal addendum: cross-tab evidence_lost flags vs on-disk knot
presence, plus the unreferenced-knot census. Snapshot at run time."""
import sys

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
from mag import verkle_knot as vk

rows = vk._load_chain_rows()
flagged_missing = flagged_present = unflagged_missing = unflagged_present = 0
referenced = set()
for r in rows:
    f = r.get("filename")
    present = bool(f) and (vk.KNOTS / str(f)).is_file()
    if f:
        referenced.add(str(f))
    if r.get("evidence_lost"):
        flagged_missing += 0 if present else 1
        flagged_present += 1 if present else 0
    else:
        unflagged_missing += 0 if present else 1
        unflagged_present += 1 if present else 0
knots_on_disk = sum(1 for _ in vk.KNOTS.glob("*.json"))
print("rows:", len(rows))
print("flagged_and_missing:", flagged_missing)
print("flagged_and_present:", flagged_present)
print("unflagged_and_missing:", unflagged_missing)
print("unflagged_and_present:", unflagged_present)
print("knot_files_on_disk:", knots_on_disk)
print("unreferenced_knot_files:", knots_on_disk - len(referenced))
