"""deep-verkle-formal evidence run: recompute every committed invariant of the
living verkle chain from disk. Read-only over memory/biography/; no writes."""
import json
import sys
import time
import collections

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
from mag import verkle_knot as vk

rows = vk._load_chain_rows()
print("rows_loaded:", len(rows))
hashes = [str(r["leaf_hash"]) for r in rows if r.get("leaf_hash")]
print("hashes:", len(hashes))
root_all = vk._merkle_root(hashes)
last = rows[-1]
tip = json.loads(vk.TIP.read_text(encoding="utf-8"))
print("recomputed_root:", root_all)
print("last_row_root:  ", last.get("verkle_root"), "match:", last.get("verkle_root") == root_all)
print("tip_root:       ", tip.get("root"), "match:", tip.get("root") == root_all)
print("tip_n_leaves:", tip.get("n_leaves"), "chain_n:", len(hashes))

# P-link property: parent_verkle_root[i] == verkle_root[i-1]
viol_parent = []
bad_order = 0
for i in range(1, len(rows)):
    p = rows[i].get("parent_verkle_root")
    prev = rows[i - 1].get("verkle_root")
    if p != prev:
        viol_parent.append((i, str(p)[:12], str(prev)[:12]))
    try:
        if int(rows[i].get("index")) != i:
            bad_order += 1
    except (TypeError, ValueError):
        bad_order += 1
print("parent_link_violations:", len(viol_parent), viol_parent[:5])
print("index_field_violations:", bad_order)

# full prefix-root re-derivation: row[i].verkle_root == prefix_root(i)
t0 = time.time()
pref = vk._merkle_prefix_roots(hashes)
print("prefix_derivation_seconds:", round(time.time() - t0, 2))
mism = [(i, str(rows[i].get("verkle_root"))[:12], pref[i][:12])
        for i in range(len(hashes)) if rows[i].get("verkle_root") != pref[i]]
print("prefix_root_mismatches:", len(mism), mism[:5])

# evidence / orphans / duplicates
ev = sum(1 for r in rows if r.get("evidence_lost"))
print("rows_flagged_evidence_lost:", ev)
missing = 0
for r in rows:
    f = r.get("filename")
    if not f or not (vk.KNOTS / str(f)).is_file():
        missing += 1
print("rows_whose_knot_file_missing_on_disk:", missing)
sid_counts = collections.Counter(str(r.get("session_id") or "") for r in rows)
dups = {s: c for s, c in sid_counts.items() if c > 1}
print("duplicate_session_ids:", len(dups), list(dups.items())[:5])
ts_list = [r.get("ts") for r in rows if r.get("ts")]
out_of_order = sum(1 for a, b in zip(ts_list, ts_list[1:]) if a > b)
print("ts_out_of_order_pairs:", out_of_order, "of", len(ts_list) - 1)
