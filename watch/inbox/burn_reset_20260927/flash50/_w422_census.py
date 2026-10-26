"""w4-22 instrument: record-bytes vs machine-bytes census for the map-territory item.

Record surfaces = the estate's descriptions of itself (receipts, doctrine, memory, docs).
Machine surfaces = the executable estate (python, hooks, configs, scripts).
Prints one JSON object. ASCII only. Stdlib only.
"""
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[4]
SKIP = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}


def dir_bytes(p: Path):
    total = 0
    files = 0
    if not p.is_dir():
        return total, files
    for x in p.rglob("*"):
        if x.is_file() and not (SKIP & set(x.parts)):
            try:
                total += x.stat().st_size
                files += 1
            except OSError:
                pass
    return total, files


def py_bytes(dirs):
    total = 0
    files = 0
    for d in dirs:
        p = ROOT / d
        if not p.is_dir():
            continue
        for x in p.rglob("*.py"):
            if x.is_file() and not (SKIP & set(x.parts)):
                try:
                    total += x.stat().st_size
                    files += 1
                except OSError:
                    pass
    return total, files


def lines(p: Path) -> int:
    if not p.is_file():
        return -1
    try:
        with p.open("r", encoding="utf-8", errors="replace") as f:
            return sum(1 for l in f if l.strip())
    except OSError:
        return -1


out = {"root": str(ROOT)}

# --- record surfaces
watch_inbox_b, watch_inbox_f = dir_bytes(ROOT / "watch" / "inbox")
memory_b, memory_f = dir_bytes(ROOT / "memory")
docs_b, docs_f = dir_bytes(ROOT / "docs")
state_b, state_f = dir_bytes(ROOT / "state")
corpus_b, corpus_f = dir_bytes(ROOT / "corpus")
queue_b, queue_f = dir_bytes(ROOT / "queue")
versions_b, versions_f = dir_bytes(ROOT / "versions")
record_total = watch_inbox_b + memory_b + docs_b + state_b + corpus_b + queue_b

md_total = 0
md_files = 0
for x in ROOT.rglob("*.md"):
    if x.is_file() and not (SKIP & set(x.parts)) and "versions" not in x.parts:
        try:
            md_total += x.stat().st_size
            md_files += 1
        except OSError:
            pass

# --- machine surfaces
code_b, code_f = py_bytes(["mag", "tools", "tests", "ijl", "models"])
scripts_b, scripts_f = 0, 0
for pat in ("*.py", "*.ps1", "*.cmd", "*.mjs"):
    for x in (ROOT / "scripts").glob(pat):
        if x.is_file():
            try:
                scripts_b += x.stat().st_size
                scripts_f += 1
            except OSError:
                pass
hooks_b = 0
hooks_f = 0
gh = ROOT / "githooks"
if gh.is_dir():
    for x in gh.rglob("*"):
        if x.is_file():
            hooks_b += x.stat().st_size
            hooks_f += 1
configs_b, configs_f = dir_bytes(ROOT / "configs")
machine_total = code_b + scripts_b + hooks_b + configs_b

out["record"] = {
    "watch_inbox_bytes": watch_inbox_b, "watch_inbox_files": watch_inbox_f,
    "memory_bytes": memory_b, "memory_files": memory_f,
    "docs_bytes": docs_b, "docs_files": docs_f,
    "state_bytes": state_b, "state_files": state_f,
    "corpus_bytes": corpus_b, "corpus_files": corpus_f,
    "queue_bytes": queue_b, "queue_files": queue_f,
    "record_total_bytes": record_total,
    "versions_bytes": versions_b, "versions_files": versions_f,
    "repo_md_bytes_excl_versions": md_total, "repo_md_files_excl_versions": md_files,
}
out["machine"] = {
    "py_mag_tools_tests_bytes": code_b, "py_files": code_f,
    "scripts_bytes": scripts_b, "scripts_files": scripts_f,
    "githooks_bytes": hooks_b, "githooks_files": hooks_f,
    "configs_bytes": configs_b, "configs_files": configs_f,
    "machine_total_bytes": machine_total,
}
if machine_total:
    out["record_to_machine_ratio"] = round(record_total / machine_total, 1)

# --- chain / catalog counters
out["counters"] = {
    "rib_md_files": len(list((ROOT / "memory" / "rib").glob("*.md"))),
    "index_events_jsonl_lines": lines(ROOT / "watch" / "inbox" / "index_events.jsonl"),
    "registry_jsonl_lines": lines(ROOT / "memory" / "biography" / "registry.jsonl"),
    "verkle_chain_jsonl_lines": lines(ROOT / "memory" / "biography" / "verkle_chain.jsonl"),
    "residual_json_files": len(list((ROOT / "memory" / "biography" / "residual").glob("*.json"))),
}
idx = ROOT / "watch" / "inbox" / "INDEX.json"
if idx.is_file():
    try:
        obj = json.loads(idx.read_text(encoding="utf-8", errors="replace"))
        if isinstance(obj, list):
            out["counters"]["index_items"] = len(obj)
        elif isinstance(obj, dict):
            out["counters"]["index_items"] = len(obj.get("items") or obj.get("entries") or [])
            out["counters"]["index_top_keys"] = sorted(obj.keys())[:12]
    except (OSError, ValueError):
        out["counters"]["index_items"] = -1

print(json.dumps(out, indent=1))
