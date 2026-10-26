# seats-inventory reconciliation pass 2 (PRINT-ONLY: no file writes; stdout is tee'd)
#  (a) catalog exact-path match handles rows recorded under a "local_sovereign_agent/" prefix (mixed conventions observed)
#  (b) magic-health scoped to content class vs ext class
#  (c) FTS probes + fts row count
#  (d) arXiv-id overmatch quantified for persona_priorart_2310.10158
import json, os, sqlite3, sys

ROOT = os.path.abspath("C:/Users/foste/Documents/projects/local_sovereign_agent")
os.chdir(ROOT)
out = sys.stdout
def L(*a, **kw):
    print(*a, file=out, flush=kw.pop("flush", False), **kw)

PREFIX = "local_sovereign_agent/"

def strip_prefix(p):
    if p.startswith(PREFIX):
        return p[len(PREFIX):]
    return p

# 1) stream catalog once
cat2 = {}
n_rows = 0
n_prefixed = 0
id_hits = 0
id_file_rows = 0
with open("catalog/catalog.jsonl", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        try:
            r = json.loads(line)
        except Exception:
            continue
        n_rows += 1
        raw = r.get("path", "")
        p = strip_prefix(raw)
        if p != raw:
            n_prefixed += 1
        cat2.setdefault(p, []).append((r.get("bytes"), r.get("mtime"), r.get("id")))
        if "2310.10158" in p or "2310.10158" in str(r.get("title", "")):
            id_hits += 1
            if p.endswith("persona_priorart_2310.10158.pdf"):
                id_file_rows += 1
L(f"# catalog2: {n_rows} rows read, {n_prefixed} rows carried the prefix '{PREFIX}', {len(cat2)} distinct normalized paths")
L(f"# arXiv-id overmatch (2310.10158): {id_hits} row(s) mention the id; {id_file_rows} row(s) are the actual pdf path")

# 2) patch rows in memory
rows = json.load(open("watch/inbox/librarian_exp/inventory_rows.json", encoding="utf-8"))
L(f"# rows loaded: {len(rows)}")
for r in rows:
    p = strip_prefix(r["path"])
    crows = cat2.get(p, [])
    if crows:
        byb = [c for c in crows if c[0] == r["size"]]
        r["cat"] = "yes" if byb else "stale"
        r["cat_note"] = f"{len(crows)} row(s)" + (", bytes match" if byb else f", recorded bytes {[c[0] for c in crows]} vs disk {r['size']}")
    else:
        r["cat"] = "no"
        r["cat_note"] = ""

# 3) corrected magic-health
def health2(r):
    fmt = r["fmt"]; p = r["path"]; ext = os.path.splitext(p)[1].lower()
    base = os.path.basename(p)
    dotfile = base.startswith(".") and ext == ""
    noext_ok = {"Dockerfile","LICENSE","Makefile","CHANGELOG","NOTICE","VERSION","CONTRIBUTING",
                "PASTE-TO-YOUR-AGENT","RELEASE-REQUIRES","pre-commit","lbrain-mcp","config","HEAD",
                "description","packed-refs","shallow","exclude","ORIG_HEAD","FETCH_HEAD"}
    textish = {".md",".txt",".py",".log",".csv",".tsv",".ps1",".mjs",".js",".yaml",".yml",".cfg",
               ".ini",".sh",".toml",".sample",".tape",".xml",".rss",".lock",".env",".refire2",
               ".gitignore",".gitattributes",".dockerignore",".npmrc",".map",".jsonl"}
    if fmt in ("text","json","jsonl?"):
        if dotfile:
            return "ok"
        if ext == "":
            return "ok" if base in noext_ok else "check-noext"
        if ext == ".jsonl" and fmt == "json":
            return "mismatch-jsonl-as-json"
        if ext == ".json" and fmt in ("json", "jsonl?", "text"):
            return "ok"
        if ext == ".jsonl" and fmt == "jsonl?":
            return "ok"
        if fmt == "html" and ext in (".json", ".jsonl", ".md", ".xml", ".rss"):
            return "MISMATCH-CONTENT-IS-HTML"
        if fmt == "text" and ext == ".json":
            return "MISMATCH-CONTENT-IS-TEXT"
        if ext in textish:
            return "ok"
        return "check-ext"
    if fmt == "binary-unknown" and ext in (".png",".jpg",".jpeg",".gif",".ico",".webp",".woff",".woff2",".ttf",".pack",".idx",".pyc",".parquet",".pdf",".zip"):
        return "ok"
    if fmt == "binary-unknown":
        return "check-binary"
    agree = {"pdf": [".pdf"], "parquet": [".parquet"], "gzip": [".gz", ".tgz"], "tar": [".tar"],
             "zip": [".zip"], "sqlite": [".sqlite", ".db"]}
    if fmt in agree:
        return "ok" if ext in agree[fmt] else f"MISMATCH-{fmt}-as-{ext or 'noext'}"
    return "ok"

for r in rows:
    r["health2"] = health2(r)

# 4) FTS probes
L("\n## catalog_fts.sqlite probes")
fts_count = None
fts_norm = set()
try:
    con = sqlite3.connect("file:catalog/catalog_fts.sqlite?mode=ro", uri=True)
    cur = con.cursor()
    fts_count = cur.execute("SELECT COUNT(*) FROM crows").fetchone()[0]
    for (pth,) in cur.execute("SELECT path FROM crows"):
        fts_norm.add(strip_prefix(str(pth).replace("\\", "/")))
    con.close()
except Exception as e:
    L("FTS open FAILED:", e)
L(f"fts crows: {fts_count}; distinct normalized paths in fts: {len(fts_norm)}")

probes = ["corpus/steal/DESCENT_DAY1_STEAL_20261001.md",
          "watch/inbox/gala_20260925/localfirst-steal/continuous-ai-main.tar.gz",
          "corpus/papers_reference_nonredistributable/persona_priorart_2310.10158.pdf",
          "data/mimo_v26/music.parquet"]
for p in probes:
    hits = cat2.get(p, [])
    infts = p in fts_norm
    L(f"  probe {p}: catalog={'yes' if hits else 'no'} ({len(hits)} rows) | fts={'yes' if infts else 'no'}")
reg = [r for r in rows if r["cat"] == "yes"]
miss = [r for r in reg if strip_prefix(r["path"]) not in fts_norm]
L(f"registered artifacts: {len(reg)}; of those MISSING from fts: {len(miss)} (fts last rebuilt 2026-09-30 09:00 per logs/fts_index.log)")

# 5) summary v2
from collections import Counter
L("\n## SUMMARY v2")
L("catalog state:", dict(Counter(r["cat"] for r in rows)))
L("INDEX state:", dict(Counter(r["idx"] for r in rows)))
L("health2:", dict(Counter(r["health2"] for r in rows)))
L("location:", dict(Counter(r["loc"] for r in rows)))
L("total bytes:", f"{sum(r['size'] for r in rows):,}")
unreg = [r for r in rows if r["cat"] == "no"]
scratch_unreg = [r for r in unreg if str(r.get("loc", "")).startswith("scratch")]
L("UNREGISTERED (no catalog row either convention):", len(unreg))
L("unregistered AND scratch:", len(scratch_unreg))
shadowed = [r for r in rows if r["cat"] == "no" and r.get("shadow")]
L("unregistered but stem-shadowed:", len(shadowed))
real_mm = [r for r in rows if r["health2"].startswith("MISMATCH")]
L("REAL magic-vs-extension mismatches:", len(real_mm))
for r in real_mm:
    L(f"  {r['health2']}: {r['path']} ({r['size']} bytes)")
chk = [r for r in rows if r["health2"].startswith("check-")]
L("needs-eye files:", len(chk))
for r in chk[:25]:
    L(f"  {r['health2']}: {r['path']}")

# 6) emit patched rows as compact JSONL to stdout for downstream tee capture
L("\n## ROWS_JSONL_BEGIN")
for r in rows:
    L(json.dumps(r, ensure_ascii=False))
L("## ROWS_JSONL_END")
