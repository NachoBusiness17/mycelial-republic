# seats-inventory lane instrument (gala_20260925 librarian-expedition, division B)
# Inventory every primary source added in the last 48h; classify fetched-by, bytes,
# format (magic bytes, not extension), catalog registration, INDEX registration,
# durable vs scratch. Librarian diseases: exact-path match (no id-substring match),
# self-inclusive dedupe, magic-bytes-before-trust.
import json, os, sys, sqlite3, hashlib, datetime

ROOT = "C:/Users/foste/Documents/projects/local_sovereign_agent"
os.chdir(ROOT)
WIN_START = datetime.datetime(2026, 9, 29, 22, 56, 0, tzinfo=datetime.timezone.utc)

out = sys.stdout

def L(*a, **kw):
    print(*a, file=out, flush=kw.pop("flush", False), **kw)

# ---------- gather artifacts ----------
arts = []  # dicts: path, size, mtime(epoch), trail

def add_art(path, size, mtime_epoch, trail):
    arts.append({"path": path.replace("\\", "/"), "size": size, "mtime": mtime_epoch, "trail": trail})

def in_win(mtime_epoch):
    return mtime_epoch >= WIN_START.timestamp()

# 1) trails from trail_listing_raw.txt (find rows; skip mangled corpus rows)
for line in open("watch/inbox/librarian_exp/trail_listing_raw.txt", encoding="utf-8", errors="replace"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) != 3 or parts[2].startswith("corpus/"):
        continue
    try:
        size = int(parts[0])
    except ValueError:
        continue
    p = parts[2]
    # parse mtime like 2026-09-30T11:52:40.3578004000Z
    try:
        mt = datetime.datetime.strptime(parts[1].split(".")[0], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)
    except Exception:
        continue
    if in_win(mt.timestamp()):
        add_art(p, size, mt.timestamp(), p.split("/")[2] if p.startswith("watch/inbox/") else p.split("/")[0])

# 2) adds_all.txt: stat fresh, window filter, exclude already-listed trail paths
listed = {a["path"] for a in arts}
added = 0
for line in open("watch/inbox/librarian_exp/adds_all.txt", encoding="utf-8", errors="replace"):
    p = line.strip()
    if not p or p in listed:
        continue
    if not os.path.isfile(p):
        continue
    st = os.stat(p)
    mt = datetime.datetime.fromtimestamp(st.st_mtime, tz=datetime.timezone.utc)
    if in_win(mt.timestamp()):
        trail = p.split("/")[0] if "/" in p else "(root)"
        add_art(p, st.st_size, mt.timestamp(), trail)
        added += 1
L(f"# gathered: {len(arts)} artifacts ({added} from adds_all.txt)", flush=True)

# 3) load catalog paths (exact-path index; NO id-substring matching)
cat = {}   # path -> list[(bytes, mtime, id)]
cat_stem = {}  # basename-without-ext -> list[paths]  (one-pass stem index; no per-artifact rescan)
with open("catalog/catalog.jsonl", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        try:
            r = json.loads(line)
        except Exception:
            continue
        p = r.get("path", "")
        cat.setdefault(p, []).append((r.get("bytes"), r.get("mtime"), r.get("id")))
        b = os.path.basename(p)
        s = os.path.splitext(b)[0]
        cat_stem.setdefault(s, []).append(p)
L(f"# catalog loaded: {sum(len(v) for v in cat.values())} rows, {len(cat)} distinct paths, {len(cat_stem)} stems", flush=True)

# 4) load INDEX.json (watch/inbox shared surface)
idx = json.load(open("watch/inbox/INDEX.json", encoding="utf-8", errors="replace"))
idx_by_path = {}
for it in idx.get("items", []):
    idx_by_path.setdefault(it.get("path", ""), []).append(it)
L(f"# INDEX loaded: {len(idx.get('items', []))} items, {len(idx_by_path)} distinct paths")

# 5) magic/format classifier (magic bytes BEFORE trust)
def sniff(path, size):
    try:
        with open(path, "rb") as fh:
            head = fh.read(16)
            fh.seek(0)
            if size > 3000000:
                sample = fh.read(65536)
            else:
                sample = fh.read()
    except Exception as e:
        return "unreadable", f"ERR {e}"
    ext = os.path.splitext(path)[1].lower()
    fmt = None
    if head.startswith(b"%PDF"):
        fmt = "pdf"
    elif head.startswith(b"PAR1"):
        fmt = "parquet"
    elif head.startswith(b"\x1f\x8b"):
        fmt = "gzip"
    elif len(sample) > 262 and sample[257:262] == b"ustar":
        fmt = "tar"
    elif head.startswith(b"PK"):
        fmt = "zip"
    elif head.startswith(b"SQLite format 3\x00"):
        fmt = "sqlite"
    elif head.startswith(b"MZ"):
        fmt = "mz-binary"
    elif len(head) >= 4 and head[1:3] == b"\x0d\x0a" and head[2] == 0x0d:
        fmt = "pyc"
    else:
        try:
            txt = sample.decode("utf-8")
            s = txt.lstrip()
            if s[:1] in ("{", "["):
                # json vs jsonl
                try:
                    json.loads(txt)
                    fmt = "json"
                except Exception:
                    fmt = "jsonl?"
            elif s[:9].lower().startswith("<!doctype") or s[:5].lower() == "<html":
                fmt = "html"
            elif b"\x00" in sample[:4096]:
                fmt = "binary-unknown"
            else:
                fmt = "text"
        except UnicodeDecodeError:
            fmt = "binary-unknown"
    # extension agreement
    agree = {"pdf": [".pdf"], "parquet": [".parquet"], "gzip": [".gz", ".tar.gz", ".tgz"],
             "tar": [".tar"], "zip": [".zip", ".docx", ".xlsx"], "sqlite": [".sqlite", ".db"],
             "json": [".json"], "jsonl?": [".jsonl", ".json"], "html": [".html", ".htm"],
             "text": [".md", ".txt", ".py", ".log", ".csv", ".tsv", ".ps1", ".mjs", ".js",
                      ".json", ".yaml", ".yml", ".cfg", ".ini", ".gitignore", ".sh"],
             "pyc": [".pyc"]}.get(fmt, [])
    health = "ok" if ext in agree else ("mismatch" if fmt else "?")
    return fmt, health

# 6) fetched-by attribution
def fetched_by(p):
    if p.startswith("watch/inbox/burn_reset_20260927/flash50/"): return "flash50 stealth burn lane (2026-09-27 reset, f-seats)"
    if p.startswith("watch/inbox/burn_reset_20260927/work/"): return "burn_reset work lanes (hermes/openrouter/impfeed/verify by filename)"
    if p.startswith("watch/inbox/localfirst/"): return "localfirst dig (stealth lane digests)"
    if p.startswith("watch/inbox/gala_20260925/localfirst-steal/"): return "localfirst-steal gala lanes (herald seat; clones/tarball/readmes)"
    if p.startswith("watch/inbox/gala_20260925/music-ractor/"): return "music-ractor gala lanes"
    if p.startswith("watch/inbox/music/"): return "music-ai folder (music ractor digests)"
    if p.startswith("watch/inbox/librarian_exp/"): return "seats-inventory lane (this inventory)"
    if p.startswith("corpus/papers_reference_nonredistributable/"): return "report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md)"
    if p.startswith("corpus/steal/"): return "descent day1 carrier (hermes_burn receipt mining)"
    if p.startswith("data/mimo_v26/"): return "mimo_v26 dataset download"
    if p.startswith("docs/report_v1/sources/receipts/"): return "report_v1 desk (per-source retrieval receipts)"
    if p.startswith("memory/behavioral/animals/"): return "animal tape collector (seat session tapes)"
    if p.startswith("memory/artifacts/console_render/"): return "console render instrument"
    if p.startswith("tools/flock_parity_out/"): return "flock parity instrument"
    if p.startswith("%TMPDIR%/"): return "mangled-env scratch copy (literal %TMPDIR% dir)"
    if p.startswith("Usersfoste"): return "mangled-path temp copy (path separators eaten)"
    base = os.path.basename(p)
    if base.startswith(("as_", "pp_", "kvarn_", "pc_")) or base.startswith(("pullpush_", "selftext", "sweep_llama", "_sweep_pp")):
        return "pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin)"
    return "unattributed"

# 7) durable vs scratch
def location_class(p):
    if p.startswith("corpus/"): return "durable-holdings"
    if p.startswith(("catalog/", "data/", "docs/", "memory/", "dashboard/")): return "durable-repo"
    if p.startswith("watch/inbox/"): return "scratch-inbox"
    return "scratch-root"

# 8) per-artifact checks
rows = []
for a in arts:
    p = a["path"]
    full = os.path.join(ROOT, p.replace("/", os.sep))
    fmt, health = sniff(p, a["size"])
    crows = cat.get(p, [])
    cat_state = "no"
    cat_note = ""
    if crows:
        byb = [c for c in crows if c[0] == a["size"]]
        if byb:
            cat_state = "yes"
            cat_note = f"{len(crows)} row(s), bytes match"
        else:
            cat_state = "stale"
            cat_note = f"{len(crows)} row(s), recorded bytes {[c[0] for c in crows]} != disk {a['size']}"
    ipath = p[len("watch/inbox/"):] if p.startswith("watch/inbox/") else None
    irows = idx_by_path.get(ipath, []) if ipath else idx_by_path.get(p, [])
    idx_state = "no"
    idx_note = ""
    if irows:
        idx_state = "yes"
        shas = [i.get("sha256") for i in irows if i.get("sha256")]
        if shas and a["size"] < 20 * 1024 * 1024:
            h = hashlib.sha256()
            try:
                with open(full, "rb") as fh:
                    for chunk in iter(lambda: fh.read(1 << 20), b""):
                        h.update(chunk)
                if h.hexdigest() in shas:
                    idx_note = "sha match"
                else:
                    idx_note = "SHA MISMATCH"
                    idx_state = "sha-stale"
            except Exception as e:
                idx_note = f"sha err {e}"
        elif shas:
            idx_note = f"sha recorded, not recomputed (size {a['size']})"
    # stem-shadow check: dedupe-detector-excludes-itself trap (one-pass stem index lookup)
    stem = os.path.splitext(os.path.basename(p))[0]
    shadow = [cp for cp in cat_stem.get(stem, []) if cp != p]
    rows.append({**a, "fmt": fmt, "health": health, "cat": cat_state, "cat_note": cat_note,
                 "idx": idx_state, "idx_note": idx_note, "by": fetched_by(p),
                 "loc": location_class(p), "shadow": shadow[:3]})

# 9) FTS freshness check (catalog_fts.sqlite last built 2026-09-30 09:00 per logs/fts_index.log)
L("\n## catalog_fts.sqlite check")
try:
    con = sqlite3.connect("file:catalog/catalog_fts.sqlite?mode=ro", uri=True)
    cur = con.cursor()
    tabs = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    L("tables:", tabs)
    # find fts table + path column
    probes = ["DESCENT_DAY1_STEAL_20261001.md", "continuous-ai-main.tar.gz",
              "persona_priorart_2310.10158.pdf", "ownmem", "lyric-archaeology.md"]
    for t in tabs:
        cols = [c[1] for c in cur.execute(f"PRAGMA table_info({t})")]
        L(f"table {t} cols: {cols[:12]}")
    con.close()
except Exception as e:
    L("FTS open FAILED:", e)

# 10) summary
L("\n## SUMMARY")
L("total artifacts:", len(rows))
from collections import Counter
L("by fetched-by:", dict(Counter(r["by"] for r in rows)))
L("by location:", dict(Counter(r["loc"] for r in rows)))
L("by format:", dict(Counter(r["fmt"] for r in rows)))
L("format health:", dict(Counter(r["health"] for r in rows)))
L("catalog state:", dict(Counter(r["cat"] for r in rows)))
L("INDEX state:", dict(Counter(r["idx"] for r in rows)))
unreg = [r for r in rows if r["cat"] == "no"]
L("UNREGISTERED (no exact-path catalog row):", len(unreg))
scratch_unreg = [r for r in unreg if r["loc"].startswith("scratch")]
L("unregistered AND scratch:", len(scratch_unreg))
stale = [r for r in rows if r["cat"] == "stale"]
L("catalog rows stale-bytes:", len(stale))
mm = [r for r in rows if r["health"] == "mismatch"]
L("MAGIC-BYTES MISMATCH:", len(mm))
for r in mm:
    L("  mismatch:", r["path"], r["fmt"])
shamis = [r for r in rows if r["idx"] == "sha-stale"]
L("INDEX sha mismatches:", len(shamis))
for r in shamis:
    L("  sha-stale:", r["path"])
shadowed = [r for r in rows if r["cat"] == "no" and r["shadow"]]
L("unregistered but stem-shadowed in catalog (dedupe self-exclusion trap):", len(shadowed))
for r in shadowed[:10]:
    L("  shadow:", r["path"], "<->", r["shadow"])

tot = sum(r["size"] for r in rows)
L(f"total bytes: {tot:,}")
big = sorted(rows, key=lambda r: -r["size"])[:15]
L("largest:")
for r in big:
    L(f"  {r['size']:>12,}  {r['path']}")

json.dump(rows, open("watch/inbox/librarian_exp/inventory_rows.json", "w", encoding="utf-8"), indent=1)
L("\nrows written: watch/inbox/librarian_exp/inventory_rows.json")
