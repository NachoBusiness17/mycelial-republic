"""FULL AUDIT 2026-09-08 — mechanical walker (batch skeleton builder).

Walks the four surfaces + aux dirs once, records per-file facts:
  exists, size, mtime, type, parse_ok (py/yaml/js/html-ref integrity),
  path-refs (outbound references and whether they resolve),
  inbound reference count (how many other files mention this path/basename),
  tri-state / falsifier marker presence (.md cards).

Output: audit_records.json (all records) + summary per batch printed.
Secrets law: this script NEVER reads .env values — .env key NAMES only.
No file is modified. Read-only over the whole tree.
"""
from __future__ import annotations
import ast, csv, hashlib, json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # .../local_sovereign_agent
OUT = Path(__file__).resolve().parent
NOW = time.time()
WEEK = 7 * 86400

SURFACES = {
    "B1_watch": ["watch/*.md", "watch/inbox/*.md", "watch/*.json", "watch/inbox/*"],
    "B2_dashboard": ["dashboard/static/*.html", "dashboard/static/*.js", "dashboard/static/*.css", "dashboard/static/*.json"],
    "B3_mag": ["mag/*.py"],
    "B4_biography": ["memory/biography/**/*"],
    "B5_runs": ["memory/runs/**/*"],
    "B6_configs_state": ["configs/*", "state/*", "queue/handoff/**"],
    "B7_corpus": ["memory/corpus/**/*"],
    "AUX": ["docs/**", "scripts/*", "artifacts/**", "*.md", "*.py", "*.yaml", "*.yml", "*.toml", "*.txt", "Dockerfile*", "docker-compose*"],
}

PATH_REF = re.compile(r"(?:watch|mag|memory|dashboard|configs|state|queue|docs|scripts|artifacts)/[\w./\-]+\.(?:py|md|html|js|json|jsonl|yaml|yml|css|png|webm|mp3|csv|txt|bak|log)")
TRI = re.compile(r"\b(SUPPORTED|DISPUTED|UNPROVEN|VERIFIED|CONFIRMED)\b", re.I)
FALS = re.compile(r"\b(falsifier|F-\w+-\d+)\b", re.I)

records: list[dict] = []
all_files: list[Path] = []

def iter_surface(patterns):
    seen = set()
    for pat in patterns:
        for p in ROOT.glob(pat):
            if p.is_file() and not p.is_symlink():
                rp = p.relative_to(ROOT).as_posix()
                if rp not in seen:
                    seen.add(rp)
                    yield p

DEEP_BATCHES = {"B4_biography", "B5_runs", "B7_corpus"}
REF_SCAN_SUFFIX = (".py", ".md", ".html", ".js", ".yaml", ".yml", ".css", ".txt")
MAX_REF_BYTES = 512 * 1024

for batch, pats in SURFACES.items():
    deep = batch in DEEP_BATCHES
    for p in iter_surface(pats):
        all_files.append(p)
        rel = p.relative_to(ROOT).as_posix()
        rec = {"path": rel, "batch": batch, "bytes": p.stat().st_size,
               "mtime_age_days": round((NOW - p.stat().st_mtime) / WEEK, 2)}
        suffix = p.suffix.lower()
        if deep:
            rec["inbound_n"] = None  # deep batches: stat-only, no content scan
            records.append(rec)
            continue
        try:
            if suffix == ".py":
                try:
                    ast.parse(p.read_text(encoding="utf-8", errors="replace"))
                    rec["parse_ok"] = True
                except SyntaxError as e:
                    rec["parse_ok"] = False
                    rec["parse_err"] = f"line {e.lineno}: {e.msg}"
            elif suffix in (".yaml", ".yml"):
                import yaml
                try:
                    yaml.safe_load(p.read_text(encoding="utf-8", errors="replace"))
                    rec["parse_ok"] = True
                except Exception as e:
                    rec["parse_ok"] = False
                    rec["parse_err"] = str(e)[:120]
            elif suffix == ".json":
                try:
                    json.loads(p.read_text(encoding="utf-8", errors="replace"))
                    rec["parse_ok"] = True
                except Exception as e:
                    rec["parse_ok"] = False
                    rec["parse_err"] = str(e)[:120]
            elif suffix in (".html", ".js", ".css", ".md", ".txt"):
                text = p.read_text(encoding="utf-8", errors="replace")
                refs = sorted(set(PATH_REF.findall(text)))
                rec["n_out_refs"] = len(refs)
                rec["out_refs"] = refs
                if suffix == ".md":
                    rec["tri_state"] = bool(TRI.search(text))
                    rec["falsifier"] = bool(FALS.search(text))
                    rec["words"] = len(text.split())
        except Exception as e:
            rec["read_err"] = str(e)[:120]
        records.append(rec)

# ---- inbound reference index (who mentions whom) ----
basename_idx: dict[str, set[str]] = {}
ref_srcs: list[tuple[str, str]] = []  # (source, text) for files worth scanning for refs
for p in all_files:
    if p.suffix.lower() in REF_SCAN_SUFFIX and p.stat().st_size <= MAX_REF_BYTES:
        try:
            ref_srcs.append((p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8", errors="replace")))
        except Exception:
            pass

for rec in records:
    if rec.get("inbound_n") is None:
        continue
    rel = rec["path"]
    base = Path(rel).name
    hits = set()
    for src, text in ref_srcs:
        if src == rel:
            continue
        if rel in text or base in text:
            hits.add(src)
    rec["inbound_refs"] = sorted(hits)
    rec["inbound_n"] = len(hits)

# ---- B4: verkle chain integrity ----
chain_rec: dict = {}
chain = ROOT / "memory/biography/verkle_chain.jsonl"
if chain.exists():
    prev_ok = idx_ok = 0
    last = None
    gaps = []
    n = 0
    prev_index = -1
    for line in chain.open(encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        n += 1
        try:
            row = json.loads(line)
        except Exception:
            gaps.append(("unparseable", n))
            continue
        i = row.get("index")
        if isinstance(i, int) and i == prev_index + 1:
            idx_ok += 1
        elif isinstance(i, int):
            gaps.append(("index_jump", n, i))
        prev_index = i if isinstance(i, int) else prev_index
        last = row
    chain_rec = {"rows": n, "contiguous_index_rows": idx_ok, "anomalies": gaps[:10],
                 "tip_index": last.get("index") if last else None,
                 "tip_leaf": (last.get("leaf_hash") or "")[:12] if last else None,
                 "tip_ts": last.get("ts") if last else None}
# orphaned knots: knot files vs chain rows
knot_dir = ROOT / "memory/biography"
knot_files = [p.name for p in knot_dir.glob("*.knot.json")]
chain_rec["knot_files"] = len(knot_files)

# ---- B6: .env key NAMES only (never values) ----
env_keys = []
envf = ROOT / ".env"
if envf.exists():
    env_keys = [ln.split("=", 1)[0].strip() for ln in envf.read_text(errors="replace").splitlines()
                if ln.strip() and not ln.startswith("#") and "=" in ln]
chain_rec["env_key_names_n"] = len(env_keys)

# ---- nav integrity (both nav lists resolve) ----
nav_report = []
for navf in list((ROOT / "dashboard/static").glob("*nav*.js")) + list((ROOT / "dashboard/static").glob("*nav*.json")):
    text = navf.read_text(encoding="utf-8", errors="replace")
    refs = sorted(set(PATH_REF.findall(text)) | set(re.findall(r"[\w\-]+\.html", text)))
    missing = []
    for r in set(refs):
        cand = r if (ROOT / r).exists() else (navf.parent / r)
        if not Path(cand).exists():
            missing.append(r)
    nav_report.append({"nav": navf.name, "refs": len(set(refs)), "missing": sorted(missing)})

# ---- write outputs ----
(OUT / "audit_records.json").write_text(json.dumps({
    "generated": datetime.now(timezone.utc).isoformat(),
    "n_files": len(records),
    "chain": chain_rec,
    "env_key_names": env_keys,
    "nav": nav_report,
    "records": records}, indent=1))

# per-batch summary
from collections import defaultdict, Counter
by_batch = defaultdict(list)
for r in records:
    by_batch[r["batch"]].append(r)
print(f"TOTAL FILES: {len(records)}")
for b in sorted(by_batch):
    rs = by_batch[b]
    parse_fail = [r for r in rs if r.get("parse_ok") is False]
    zero = [r for r in rs if r["bytes"] == 0]
    stale = [r for r in rs if r.get("inbound_n") == 0 and r["mtime_age_days"] > 2]
    hist = Counter(Path(r["path"]).suffix or "?" for r in rs)
    total_mb = sum(r["bytes"] for r in rs) / 1e6
    print(f"\n== {b}: {len(rs)} files | {total_mb:.1f} MB | parse_fail={len(parse_fail)} | zero_byte={len(zero)} | old_unreferenced={len(stale)}")
    print("   ext:", dict(hist.most_common(10)))
    for r in parse_fail[:12]:
        print(f"  PARSE_FAIL {r['path']} {r.get('parse_err','')}")
    for r in zero[:12]:
        print(f"  ZERO {r['path']}")
    # dup detection (sample: files <1MB, hash first 4KB)
    seen_hash = defaultdict(list)
    for r in rs:
        if 0 < r["bytes"] < 1_000_000:
            try:
                with open(ROOT / r["path"], "rb") as fh:
                    h = hashlib.sha256(fh.read(4096)).hexdigest()[:12]
                seen_hash[h].append(r["path"])
            except Exception:
                pass
    dups = {h: ps for h, ps in seen_hash.items() if len(ps) > 3}
    if dups:
        print(f"  DUP_CLUSTERS(>3 same head): {len(dups)}")
        for h, ps in list(dups.items())[:5]:
            print(f"    {h}: {len(ps)} files e.g. {ps[0]}")
print("\nCHAIN:", json.dumps(chain_rec, indent=1)[:900])
for nv in nav_report:
    print(f"NAV {nv['nav']}: {nv['refs']} refs, missing={nv['missing']}")
