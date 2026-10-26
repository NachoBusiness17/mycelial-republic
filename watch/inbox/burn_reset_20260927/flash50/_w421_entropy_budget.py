#!/usr/bin/env python3
"""w4-21 entropy-budget instrument.

Read-only census + gate-chain clock. Every subprocess carries
creationflags=CREATE_NO_WINDOW on win32 per the harness law.
Prints one JSON blob of measured numbers.
"""
import json
import os
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
OUT = {}

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def run_timed(label, args, timeout=300, cwd=ROOT):
    t0 = time.perf_counter()
    try:
        r = subprocess.run(
            args, cwd=str(cwd), capture_output=True, text=True,
            timeout=timeout, creationflags=CREATE_NO_WINDOW,
        )
        wall = time.perf_counter() - t0
        out = (r.stdout or "").strip().splitlines()
        head = out[:2]
        tail = out[-2:] if len(out) > 2 else []
        return {"label": label, "rc": r.returncode, "wall_s": round(wall, 3),
                "head": head, "tail": tail}
    except subprocess.TimeoutExpired:
        return {"label": label, "rc": None, "wall_s": round(time.perf_counter() - t0, 3),
                "head": ["TIMEOUT"], "tail": []}
    except OSError as e:
        return {"label": label, "rc": None, "wall_s": round(time.perf_counter() - t0, 3),
                "head": [f"OSError: {e}"], "tail": []}


def fbytes(p: Path) -> int:
    try:
        return p.stat().st_size
    except OSError:
        return -1


# --- 1. boot-tax stack sizes -------------------------------------------------
boot = {}
for rel in [
    "AGENTS.md", "CONSTITUTION.md", "state/CURRENT.md", "queue/todo.md",
    "docs/FRAMEWORK_LOAD.md", "docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md",
    "docs/ref/MYCELIAL_SCIENCE_MAP.md", "memory/briefs/latest.md",
    "memory/warm_state.json",
]:
    boot[rel] = fbytes(ROOT / rel)
OUT["boot_stack_bytes"] = boot
OUT["boot_stack_total_bytes"] = sum(v for v in boot.values() if v > 0)

ribs = sorted((ROOT / "memory/rib").glob("*.md"))
OUT["rib_files"] = len(ribs)
OUT["rib_bytes"] = sum(fbytes(p) for p in ribs)

# --- 2. watch/inbox landfill census -----------------------------------------
inbox = ROOT / "watch/inbox"
n_files = 0
n_bytes = 0
n_md = 0
md_bytes = 0
today = datetime.now().date()
n_today = 0
today_bytes = 0
for dirpath, dirnames, filenames in os.walk(inbox):
    for fn in filenames:
        p = Path(dirpath) / fn
        try:
            st = p.stat()
        except OSError:
            continue
        n_files += 1
        n_bytes += st.st_size
        if fn.lower().endswith(".md"):
            n_md += 1
            md_bytes += st.st_size
        if datetime.fromtimestamp(st.st_mtime).date() == today:
            n_today += 1
            today_bytes += st.st_size
OUT["inbox_files"] = n_files
OUT["inbox_bytes"] = n_bytes
OUT["inbox_md_files"] = n_md
OUT["inbox_md_bytes"] = md_bytes
OUT["inbox_files_touched_today"] = n_today
OUT["inbox_bytes_touched_today"] = today_bytes
OUT["flash50_md_count"] = len(list((inbox / "burn_reset_20260927/flash50").glob("*.md")))

# --- 3. index + events -------------------------------------------------------
OUT["INDEX_json_bytes"] = fbytes(ROOT / "watch/inbox/INDEX.json")
ev_path = ROOT / "watch/inbox/index_events.jsonl"
OUT["index_events_bytes"] = fbytes(ev_path)
hist = Counter()
n_ev = 0
first_keys = []
if ev_path.is_file():
    with ev_path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n_ev += 1
            if n_ev == 1:
                try:
                    first_keys = sorted(json.loads(line).keys())
                except ValueError:
                    first_keys = ["<unparseable>"]
            try:
                row = json.loads(line)
            except ValueError:
                hist["<unparseable>"] += 1
                continue
            op = row.get("op") or row.get("event") or row.get("type") or "<none>"
            hist[str(op)] += 1
OUT["index_event_rows"] = n_ev
OUT["index_event_op_histogram"] = dict(hist.most_common(12))
OUT["index_event_first_row_keys"] = first_keys

# --- 4. debt + law ledgers ---------------------------------------------------
try:
    base = json.loads((ROOT / "configs/violation_baseline.json").read_text(encoding="utf-8"))
    acc = base.get("accepted", {})
    OUT["baseline_claims"] = len(acc)
    OUT["baseline_rule_histogram"] = dict(Counter(v.get("rule", "?") for v in acc.values()).most_common())
    OUT["baseline_by_histogram"] = dict(Counter(v.get("by", "?") for v in acc.values()).most_common(8))
    OUT["baseline_with_expires"] = sum(1 for v in acc.values() if v.get("expires"))
except (OSError, ValueError) as e:
    OUT["baseline_error"] = str(e)

try:
    inv = json.loads((ROOT / "memory/percolator/invariants.json").read_text(encoding="utf-8"))
    if isinstance(inv, dict):
        inv = inv.get("invariants", inv)
    OUT["invariants_count"] = len(inv)
except (OSError, ValueError) as e:
    OUT["invariants_error"] = str(e)

reg_path = ROOT / "memory/workflows/REGISTRY.jsonl"
reg_hist = Counter()
n_reg = 0
if reg_path.is_file():
    with reg_path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n_reg += 1
            try:
                reg_hist[json.loads(line).get("verdict", "?")] += 1
            except ValueError:
                reg_hist["<unparseable>"] += 1
OUT["workflow_registry_rows"] = n_reg
OUT["workflow_registry_verdicts"] = dict(reg_hist)

# --- 5. quantizer delivery simulation ----------------------------------------
qt_flash = ROOT / "memory/corpus/quantized_thought/instructions_flash.jsonl"
qt_report = ROOT / "memory/corpus/quantized_thought/compile_report.json"
try:
    rows = [json.loads(x) for x in qt_flash.read_text(encoding="utf-8").splitlines() if x.strip()]
    rep = json.loads(qt_report.read_text(encoding="utf-8"))
    OUT["flash_laws_total"] = len(rows)
    OUT["compile_report_compiled"] = rep.get("compiled")
    OUT["compile_report_kept"] = rep.get("kept")
    # simulate the _quantized_laws 1800-char boot budget (mag/context_pack.py:343,387)
    total = len("[compile header]")
    delivered = 0
    for r in rows:
        law = str(r.get("flash") or r.get("frontier") or "").strip()
        if not law:
            continue
        entry = "- " + law
        if total + len(entry) > 1800:
            break
        total += len(entry)
        delivered += 1
    OUT["flash_laws_fit_1800char_pack"] = delivered
except (OSError, ValueError) as e:
    OUT["quantizer_error"] = str(e)

# --- 6. git rates + history mass ---------------------------------------------
def git(args):
    return subprocess.run(["git"] + args, cwd=str(ROOT), capture_output=True,
                          text=True, timeout=120, creationflags=CREATE_NO_WINDOW)

OUT["git_commits_total"] = len(git(["rev-list", "HEAD"]).stdout.splitlines())
OUT["git_commits_24h"] = len(git(["rev-list", "HEAD", "--since=24 hours ago"]).stdout.splitlines())
OUT["git_commits_7d"] = len(git(["rev-list", "HEAD", "--since=7 days ago"]).stdout.splitlines())
co = git(["count-objects", "-v"]).stdout
for line in co.splitlines():
    k, _, v = line.partition(":")
    if k.strip() in ("size-pack", "size", "in-pack", "count"):
        OUT["git_" + k.strip()] = int(v.strip())
OUT["git_tracked_files"] = len(git(["ls-files"]).stdout.splitlines())

# --- 7. THE GATE-CHAIN CLOCK --------------------------------------------------
py = sys.executable
clock = []
clock.append(run_timed("ratchet_check_changed", [py, "tools/violation_ratchet.py", "check", "--changed"]))
clock.append(run_timed("ratchet_check_full", [py, "tools/violation_ratchet.py", "check"]))
clock.append(run_timed("config_seal_verify", [py, "tools/config_seal.py", "verify"]))
clock.append(run_timed("census_drift_patrol", [py, "tools/census_drift_patrol.py"]))
clock.append(run_timed("checkbox_receipt_gate", [py, "tools/checkbox_receipt_gate.py"]))
clock.append(run_timed("workflow_scenarios_readonly", [py, "tools/workflow_gate.py", "check", "--scenarios", "configs/workflow_gate_scenarios"]))
clock.append(run_timed("secret_gate_changed", [py, "tools/secret_gate.py", "--changed", "--baseline", "configs/secret_gate_baseline.json"]))
clock.append(run_timed("freshness_check", [py, "tools/freshness_check.py"]))
clock.append(run_timed("pytest_collect_only_q", [py, "-m", "pytest", "--collect-only", "-q"], timeout=420))
OUT["gate_clock"] = clock

OUT["measured_at"] = datetime.now().isoformat(timespec="seconds")
print(json.dumps(OUT, indent=1, default=str))
