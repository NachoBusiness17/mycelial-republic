"""_entropy_budget_census.py - one-shot measurer for the deep-entropy-budget deep item.

Counts the estate's order-structures (ledgers, invariants, debt register, receipts)
and peeks the basal-metabolism logs. Read-only except nothing: pure reads.
Generator/receipt: watch/inbox/burn_reset_20260927/flash50/deep-entropy-budget.md
"""
import json
import pathlib
import subprocess
import sys

R = pathlib.Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


def rows(rel):
    p = R / rel
    if not p.exists():
        return None
    n = 0
    with p.open("rb") as f:
        for _ in f:
            n += 1
    return n


out = {}

# --- order structures (ledgers of landed work) ---
out["burn_ledger_rows"] = rows("memory/burns/LEDGER.jsonl")
out["workflow_registry_rows"] = rows("memory/workflows/REGISTRY.jsonl")
out["catalog_rows"] = rows("catalog/catalog.jsonl")
out["estate_index_rows"] = rows("dashboard/data/ESTATE_INDEX.jsonl")
out["behavioral_facts_rows"] = rows("memory/facts/behavioral.jsonl")
out["trajectory_rows"] = rows("memory/trajectory/steps.jsonl")

# --- invariants (the percolator's distilled order) ---
p = R / "memory/percolator/invariants.json"
try:
    d = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(d, dict):
        out["invariants"] = {k: len(v) for k, v in d.items() if isinstance(v, list)}
        out["invariants_keys"] = list(d.keys())
    else:
        out["invariants_count"] = len(d)
except Exception as e:
    out["invariants_err"] = repr(e)

# --- registered debt (the ratchet's entropy ledger) ---
p = R / "configs/violation_baseline.json"
try:
    d = json.loads(p.read_text(encoding="utf-8"))
    out["baseline_keys"] = list(d.keys())
    for k, v in d.items():
        if isinstance(v, list):
            out["baseline_" + k + "_len"] = len(v)
        elif isinstance(v, dict):
            out["baseline_" + k + "_len"] = len(v)
except Exception as e:
    out["baseline_err"] = repr(e)

# --- receipt estate (watch/inbox) ---
wb = R / "watch/inbox"
files = [f for f in wb.rglob("*") if f.is_file() and "__pycache__" not in str(f)]
out["inbox_files"] = len(files)
out["inbox_bytes"] = sum(f.stat().st_size for f in files)
out["inbox_md_receipts"] = sum(1 for f in files if f.suffix == ".md")

# --- this burn lane ---
q = R / "watch/inbox/burn_reset_20260927/queue"
out["burn_reset_queue_files"] = len([f for f in q.iterdir() if f.is_file()]) if q.exists() else None
fl = R / "watch/inbox/burn_reset_20260927/flash50"
flf = [f for f in fl.iterdir() if f.is_file()]
out["flash50_files"] = len(flf)
out["flash50_bytes"] = sum(f.stat().st_size for f in flf)

# --- tests tree (the verification estate) ---
t = R / "tests"
out["test_files"] = len(list(t.glob("test_*.py")))

# --- repo tracked files (subprocess with CREATE_NO_WINDOW per estate law) ---
try:
    r = subprocess.run(
        ["git", "ls-files"], cwd=str(R), capture_output=True, text=True,
        timeout=60, creationflags=CREATE_NO_WINDOW,
    )
    out["git_tracked_files"] = len(r.stdout.splitlines())
except Exception as e:
    out["git_err"] = repr(e)

# --- basal metabolism: did the daily pumps run? (log tails) ---
for name in ("logs/census_patrol.log", "logs/fts_index.log"):
    p = R / name
    if p.exists():
        lines = p.read_text(encoding="utf-8", errors="replace").strip().splitlines()
        out["tail_" + name.replace("/", "_")] = lines[-2:]
    else:
        out["tail_" + name.replace("/", "_")] = "MISSING"

print(json.dumps(out, indent=1))
