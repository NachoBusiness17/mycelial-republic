"""f-26 ledger census sweep.

Enumerates every *.jsonl under the repo (excluding .venv and .git), and for each:
  - row count (non-empty lines), empty-line count, size, mtime
  - schema: distinct top-level key tuples with counts (json parse; sampled when huge)
  - git: tracked? ignored? rows at HEAD, delta vs HEAD, last commit date
  - readers: literal basename hits in code/config dirs (mag tools scripts backend
    tests configs githooks + repo root files)

Raw facts land in _f26_raw.json next to this script. No fabrication: every number
is measured here.
"""
import os
import sys
import json
import time
import datetime
import subprocess
from collections import Counter

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
OUTDIR = os.path.join(REPO, "watch", "inbox", "burn_reset_20260927", "flash50")
SKIP = {".venv", ".git"}
FULLPARSE_LIMIT = 20_000_000  # bytes; above this, schema sampled from first SAMPLE_N rows
SAMPLE_N = 20_000
TEXT_EXTS = {".py", ".ps1", ".psm1", ".js", ".ts", ".cmd", ".bat",
             ".json", ".yaml", ".yml", ".toml", ".md", ".txt", ".cfg", ".ini"}
SCAN_DIRS = [d for d in ("mag", "tools", "scripts", "backend", "tests",
                         "configs", "githooks") if os.path.isdir(os.path.join(REPO, d))]
CF = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}

t0 = time.time()


def run(cmd, stdin_bytes=None, timeout=180):
    return subprocess.run(cmd, cwd=REPO, input=stdin_bytes,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=timeout, **CF)


def iso(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def head_row_count(rel):
    p = run(["git", "show", "HEAD:" + rel], timeout=300)
    if p.returncode != 0:
        return None
    return sum(1 for ln in p.stdout.split(b"\n") if ln.strip())


# ---------- 1. walk ----------
ledgers = []
for dp, dn, fns in os.walk(REPO):
    dn[:] = [d for d in dn if d not in SKIP]
    for fn in fns:
        if fn.lower().endswith(".jsonl"):
            ledgers.append(os.path.join(dp, fn))
ledgers.sort()
print("jsonl files found: %d" % len(ledgers), flush=True)

# ---------- 2. git bookkeeping ----------
tracked_set = set()
p = run(["git", "ls-files", "-z"], timeout=300)
for tok in p.stdout.split(b"\x00"):
    t = tok.decode("utf-8", "replace").strip()
    if t.lower().endswith(".jsonl"):
        tracked_set.add(t)

ignored_set = set()
paths_f = [lp.replace("\\", "/") for lp in ledgers]
p = run(["git", "check-ignore", "--stdin"],
        stdin_bytes=("\n".join(paths_f) + "\n").encode("utf-8"), timeout=300)
if p.returncode in (0, 1):
    for tok in p.stdout.decode("utf-8", "replace").splitlines():
        t = tok.strip()
        if t:
            ignored_set.add(t)

# ---------- 3. per-file facts ----------
records = []
for lp in ledgers:
    rel = os.path.relpath(lp, REPO).replace("\\", "/")
    st = os.stat(lp)
    rows = empty = ok = bad = nondict = 0
    first_bad = None
    keysets = Counter()
    sampled = False
    with open(lp, "rb") as f:
        for lineno, raw in enumerate(f, 1):
            s = raw.strip()
            if not s:
                empty += 1
                continue
            rows += 1
            if st.st_size <= FULLPARSE_LIMIT or rows <= SAMPLE_N:
                try:
                    obj = json.loads(s.decode("utf-8", "replace"))
                    ok += 1
                    if isinstance(obj, dict):
                        keysets[tuple(sorted(obj.keys()))] += 1
                    else:
                        nondict += 1
                        keysets[("<" + type(obj).__name__ + ">",)] += 1
                except Exception:
                    bad += 1
                    if first_bad is None:
                        first_bad = lineno
    if st.st_size > FULLPARSE_LIMIT:
        sampled = True

    tracked = rel in tracked_set
    ignored = rel in ignored_set
    head_rows = head_row_count(rel) if tracked else None
    delta = (rows - head_rows) if head_rows is not None else None
    last_commit = None
    if tracked:
        p = run(["git", "log", "-1", "--format=%cI", "--", rel], timeout=120)
        if p.returncode == 0 and p.stdout.strip():
            last_commit = p.stdout.decode("utf-8", "replace").strip()[:10]

    records.append({
        "path": rel,
        "size_bytes": st.st_size,
        "mtime": iso(st.st_mtime),
        "mtime_age_days": round((time.time() - st.st_mtime) / 86400.0, 2),
        "rows": rows,
        "empty_lines": empty,
        "parse_ok": ok,
        "parse_bad": bad,
        "first_bad_line": first_bad,
        "schema_sampled": sampled,
        "nondict_rows": nondict,
        "keysets": [[list(k), c] for k, c in keysets.most_common(8)],
        "tracked": tracked,
        "ignored": ignored,
        "head_rows": head_rows,
        "delta_vs_head": delta,
        "last_commit": last_commit,
    })
    print("%6d rows  %s" % (rows, rel), flush=True)

# ---------- 4. reader scan ----------
basenames = {}
for r in records:
    basenames.setdefault(os.path.basename(r["path"]).lower(), r["path"])

code_files = []
for d in SCAN_DIRS:
    for dp, dn, fns in os.walk(os.path.join(REPO, d)):
        dn[:] = [x for x in dn if x not in SKIP]
        for fn in fns:
            if os.path.splitext(fn)[1].lower() in TEXT_EXTS:
                code_files.append(os.path.join(dp, fn))
for fn in os.listdir(REPO):
    fp = os.path.join(REPO, fn)
    if os.path.isfile(fp) and os.path.splitext(fn)[1].lower() in TEXT_EXTS:
        code_files.append(fp)
print("code/config files scanned for readers: %d" % len(code_files), flush=True)

hits = {name: {"count": 0, "samples": []} for name in basenames}
for cf in code_files:
    try:
        with open(cf, "rb") as f:
            data = f.read()
    except OSError:
        continue
    text = data.decode("utf-8", "replace")
    if ".jsonl" not in text.lower():
        continue
    crel = os.path.relpath(cf, REPO).replace("\\", "/")
    for lineno, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if ".jsonl" not in low:
            continue
        for name, target in basenames.items():
            if name in low:
                h = hits[name]
                h["count"] += 1
                if len(h["samples"]) < 6:
                    snippet = line.strip()[:120].encode("ascii", "replace").decode("ascii")
                    h["samples"].append({"file": crel, "line": lineno, "snippet": snippet})

for r in records:
    r["reader_hits"] = hits.get(os.path.basename(r["path"]).lower(), {"count": 0, "samples": []})

# ---------- 5. dump ----------
head_sha = run(["git", "rev-parse", "--short=10", "HEAD"]).stdout.decode().strip()
blob = {
    "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "head_sha": head_sha,
    "repo": REPO,
    "n_files": len(records),
    "scan_dirs_for_readers": SCAN_DIRS,
    "records": records,
}
out = os.path.join(OUTDIR, "_f26_raw.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(blob, f, indent=1)
print("raw dumped to %s" % out, flush=True)
tot_rows = sum(r["rows"] for r in records)
tot_bytes = sum(r["size_bytes"] for r in records)
print("TOTAL: %d files, %d rows, %d bytes, elapsed %.1fs"
      % (len(records), tot_rows, tot_bytes, time.time() - t0), flush=True)
