"""Cartographer cycle 20261011: fold indexed + unindexed codex walks into one shelf map.

Emits seat_pools_thread_map.jsonl: one row per codex thread, thread -> decision ->
filed-law-or-debt classification, all fields derived from the two walker outputs.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA10 = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261010_data"
DATA11 = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261011_data"

REPO_PREFIX = "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent"
DURABLE = ("mag/", "mag\\", "tests/", "tests\\", "docs/", "docs\\", "state/", "state\\",
           "memory/", "memory\\", "watch/", "watch\\", "scripts/", "scripts\\",
           "queue/", "queue\\", "configs/", "configs\\", "deploy/", "deploy\\",
           "tools/", "tools\\", "jobs/", "jobs\\")

SMOKE_PREFIX = ("Reply with exactly",)


def norm_target(t):
    t2 = t.replace("\\\\", "\\")
    inside = REPO_PREFIX.lower() in t2.lower() or any(t2.startswith(d) for d in DURABLE)
    return {"target": t2[:200], "in_repo": bool(inside)}


def durable_targets(targets):
    out = []
    for t in targets:
        n = norm_target(t)
        if n["in_repo"]:
            out.append(n["target"])
    return out


def classify(first_user, shape, dtargets, debt_signal):
    if any((first_user or "").startswith(s) for s in SMOKE_PREFIX):
        return "SMOKE"
    if dtargets:
        return "FILED_LAW"
    if shape == "patched":
        return "FILED_OUTSIDE"
    if shape == "audit":
        return "DEBT_NAMED" if debt_signal else "AUDIT_VERDICT"
    return "BARE"


def main():
    out_rows = []
    with (DATA10 / "codex_walk.jsonl").open("r", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            out_rows.append({
                "id": r["id"], "source": "indexed", "label": r.get("thread_name"),
                "day": (r.get("updated_at") or "")[:10], "bytes": r.get("bytes"),
                "shape": None, "patch_calls": r.get("apply_patch_calls"),
                "tool_calls": r.get("tool_calls"), "filed_markers": r.get("filed_markers"),
                "first_user": (r.get("first_user") or "")[:300],
                "decision_extract": (r.get("last_assistant") or "")[:400],
                "note": "walked cycle 20261010 (codex_walk.jsonl); classification added cycle 20261011",
            })
    with (DATA11 / "unindexed_walk.jsonl").open("r", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            dt = durable_targets(r.get("sample_patch_targets") or [])
            verdict = classify(r.get("first_user"), r.get("shape"), dt, r.get("debt_signal") or [])
            out_rows.append({
                "id": r["id"], "source": "unindexed", "label": None,
                "day": (r.get("first_ts") or "")[:10], "bytes": r.get("bytes"),
                "shape": r.get("shape"), "patch_calls": r.get("apply_patch_calls"),
                "tool_calls": r.get("tool_calls"), "filed_markers": r.get("filed_markers"),
                "durable_targets_in_repo": dt,
                "debt_signal": r.get("debt_signal"), "law_signal": r.get("law_signal"),
                "first_user": (r.get("first_user") or "")[:300],
                "decision_extract": (r.get("last_assistant") or "")[:400],
                "verdict": verdict,
                "note": "walked cycle 20261011 (unindexed_walk.jsonl)",
            })
    # Titan override: walked and read in segments this cycle; status law filed in-repo.
    for row in out_rows:
        if row["id"].startswith("01a052ca"):
            row["verdict"] = "FILED_LAW"
            row["shape"] = "patched"
            row["note"] = ("titan; segment-walked cycle 20261011; status law organ_map.py + "
                           "operational dirac_loop.py filed in-repo; retraction 2026-09-02T12:25:38Z")
            row["decision_extract"] = (
                "Retraction: 'I'm stopping all action here. I won't touch Mag, OpenClaw, or spend "
                "further remote-model tokens unless you explicitly tell me to resume.' Filed: "
                "mag/organ_map.py status law (DECLARED..GHOST), mag/dirac_loop.py operational scope, "
                "context admission receipts, OpenClaw timeout/compaction config, "
                "BASECAMP_ORGAN_AUDIT_2026-08-30.md (cwd outputs).")

    out_path = DATA11 / "seat_pools_thread_map.jsonl"
    with out_path.open("w", encoding="utf-8") as out:
        for row in out_rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    from collections import Counter
    verdicts = Counter(r.get("verdict") for r in out_rows if r.get("verdict"))
    print(json.dumps({"rows": len(out_rows),
                      "indexed": sum(1 for r in out_rows if r["source"] == "indexed"),
                      "unindexed": sum(1 for r in out_rows if r["source"] == "unindexed"),
                      "unindexed_verdicts": dict(verdicts)}, indent=2))


if __name__ == "__main__":
    main()
