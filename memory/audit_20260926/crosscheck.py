"""Cross-lane contradiction detector for the 2026-09-26 network audit.

The repo's own law: "trust bytes, not reports" and "never trust a hand-written
count." This applies to OUR OWN children. When the 10 lanes report, this script
loads their JSON and flags numbers that disagree with each other or with
measured ground truth.

Run:  python memory/audit_20260926/crosscheck.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INBOX = HERE.parent.parent / "watch" / "inbox" / "audit_20260926"

LANES = {
    1: "lane1_claims.json",
    2: "lane2_tools.json",
    3: "lane3_gates.json",
    4: "lane4_unversioned.json",
    5: "lane5_composition.json",
    6: "lane6_laws.json",
    7: "lane7_tests.json",
    8: "lane8_canonical.json",
    9: "lane9_boundary.json",
    10: "lane10_adversarial.json",
}

# Ground truth measured by the parent seat with real commands, 2026-09-26.
TRUTH = {
    "collected_tests": 2288,
    "census_claim_in_agents_md": 1910,
    "ratchet_new_violations": 6,
    "ratchet_exit": 1,
    "census_patrol_exit": 1,
    "git_dir_bytes": 7.5,          # GB, du -sh .git
    "sibling_dirs": 35,
    "sibling_dirs_with_git": 10,
    "network_files": 1_946_684,
    "network_code_files": 94_730,
    "private_skipped": 18_733,
    "dirty_paths": 1_313,
    "untracked": 1_087,
    "modified": 225,
    "untracked_watch": 889,
    "estate_index_bytes": 590_246_188,
    "estate_index_sha256": "7f3b2bc447d0cc43bb06b8e616063bf1dc6542ba7f8944c98097cd68873d0d1b",
    "catalog_lines": 489_548,
    "disk_pytest_candidates": 348,
    "carrier_file_claim": 303,
}

# Numbers that must agree across every lane that mentions them. Any lane whose
# value differs from ground truth is flagged for human adjudication.
CONTENTIOUS = {
    "collected_tests": "the census denominator — lanes 1, 5, 7 may each report one",
    "dirty_paths": "working tree size — lanes 1, 3",
    "network_files": "total file count — lanes 1, 4, 5",
    "ratchet_new_violations": "lane 3 may recount",
}


def load(n):
    p = HERE / n
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"__error__": f"{n}: {e}"}


def main():
    report = {"ground_truth": TRUTH, "lanes": {}, "contradictions": [],
              "missing_lanes": [], "unreadable": []}

    for num, fname in LANES.items():
        data = load(fname)
        if data is None:
            report["missing_lanes"].append(num)
            continue
        if isinstance(data, dict) and "__error__" in data:
            report["unreadable"].append({"lane": num, "err": data["__error__"]})
            continue
        rows = data if isinstance(data, list) else [data]
        n = len(rows)
        # Pull any integer field that matches a truth key, to compare.
        hits = {}
        for r in rows:
            if not isinstance(r, dict):
                continue
            for k, v in r.items():
                if k in TRUTH and isinstance(v, (int, float)):
                    hits.setdefault(k, set()).add(v)
        report["lanes"][num] = {"file": fname, "rows": n,
                                "truth_keys_touched": {k: sorted(v) for k, v in hits.items()}}
        for k, vals in hits.items():
            if TRUTH[k] not in vals:
                report["contradictions"].append({
                    "lane": num, "key": k, "lane_says": sorted(vals),
                    "ground_truth": TRUTH[k], "why": CONTENTIOUS.get(k, ""),
                })

    print(json.dumps(report, indent=1)[:6000])
    out = HERE / "crosscheck_report.json"
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"\nlanes present: {sorted(report['lanes'])}")
    print(f"missing: {report['missing_lanes']}  unreadable: {len(report['unreadable'])}")
    print(f"CONTRADICTIONS: {len(report['contradictions'])}")
    for c in report["contradictions"]:
        print(f"  lane{c['lane']} {c['key']}: says {c['lane_says']} vs truth {c['ground_truth']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
