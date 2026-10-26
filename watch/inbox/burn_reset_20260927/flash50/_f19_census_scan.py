"""f-19 census scanner: dashboard/ HTML/JS/CSS files.

Outputs JSON with, per file:
  - title / first comment / size / mtime
  - outbound edges (script src, link href, a href html targets, fetch targets, data files)
  - back-references: every repo file (text, <20MB) whose bytes contain the basename
Run with the repo venv python. One pass over the reference corpus.
"""
from __future__ import annotations
import json, os, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # flash50<burn_reset<inbox<watch<repo
DASH = ROOT / "dashboard"
STATIC = DASH / "static"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", ".vercel", ".zcode", ".agents"}
# archival/external trees pruned from the reference corpus walk (paths relative to ROOT):
SKIP_TREES = {".mimosa", ".venv", "mine", "agents", "memory/biography_backup",
              "memory/biography", "memory/runs", "memory/agent_state", "memory/ghost",
              "memory/corpus", "corpus/library", "corpus/oral_history", "watch/.mimosa",
              "dashboard/data"}
MAX_SCAN = 20 * 1024 * 1024

def sniff_text(data: bytes) -> bool:
    if b"\x00" in data[:4096]:
        return False
    return True

# ---- collect dashboard file inventory -------------------------------------
inv = []           # (relpath, size)
for dirpath, dirnames, filenames in os.walk(DASH):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        p = Path(dirpath) / fn
        try:
            sz = p.stat().st_size
        except OSError:
            continue
        inv.append((p.relative_to(ROOT).as_posix(), sz))
inv.sort()

HJC = [r for r, _ in inv if re.search(r"\.(html|js|css)$", r)]
print(f"inventory={len(inv)} html_js_css={len(HJC)}", file=sys.stderr)

basenames = {}     # basename -> [relpaths]  (for html/js/css only)
for r in HJC:
    basenames.setdefault(Path(r).name, []).append(r)

# ---- reference corpus: whole repo, one pass --------------------------------
corpus = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel_dir = Path(dirpath).relative_to(ROOT).as_posix()
    if rel_dir == ".":
        rel_dir = ""
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                   and ((rel_dir + "/" + d).strip("/") not in SKIP_TREES)]
    for fn in filenames:
        p = Path(dirpath) / fn
        rel = p.relative_to(ROOT).as_posix()
        try:
            sz = p.stat().st_size
        except OSError:
            continue
        if sz > MAX_SCAN or sz == 0:
            continue
        corpus.append((rel, p))
print(f"corpus_files={len(corpus)}", file=sys.stderr)

# ---- single pass: which corpus files mention which basenames ---------------
# One combined regex (all basenames alternated), one scan per corpus file.
# Boundary guards: no [\w.-] char glued to either side, so "board.js" no longer
# matches inside "ractor_board.jsonl" and "index.html" no longer matches
# "index.html.bak-nav". The 6 subdir index.html twins are keyed on their
# distinguishing "<dir>/index.html" path instead of the bare basename.
import re as _re
_BASES = sorted(basenames, key=len, reverse=True)
PATTERNS = {}
for b in _BASES:
    if b == "index.html":
        continue  # handled per-dir below
    PATTERNS[b] = r"(?<![\w.-])" + _re.escape(b) + r"(?![\w.-])"
DIR_INDEXES = [r for r in HJC if r.endswith("/index.html")]
for r in DIR_INDEXES:
    parent = r[len("dashboard/static/"):-len("index.html")]  # e.g. "art/"
    PATTERNS[parent + "index.html"] = r"(?<![\w./-])" + _re.escape(parent + "index.html") + r"(?![\w.-])"
# root index.html keyed as static/index.html or "/index.html" route shape
PATTERNS["index.html"] = r"(?<![\w./-])(?:static/)?index\.html(?![\w.-])"
_KEYS = sorted(PATTERNS, key=len, reverse=True)
RX = _re.compile("|".join("(" + PATTERNS[k] + ")" for k in _KEYS))
KEY2RELS = {}
for b, pat in PATTERNS.items():
    if b == "index.html":
        KEY2RELS[b] = ["dashboard/static/index.html"]
    elif b.endswith("/index.html"):
        KEY2RELS[b] = ["dashboard/static/" + b]
    else:
        KEY2RELS[b] = basenames[b]
hits = {r: [] for r in HJC}         # relpath -> [corpus relpaths]
t0 = time.time()
nscanned = 0
for rel, p in corpus:
    try:
        data = p.read_bytes()
    except OSError:
        continue
    if not sniff_text(data):
        continue
    text = data.decode("utf-8", errors="replace")
    keys = set()
    for m in RX.finditer(text):
        if m.lastindex:
            keys.add(_KEYS[m.lastindex - 1])
    if not keys:
        continue
    nscanned += 1
    hit_rels = set()
    for key in keys:
        hit_rels.update(KEY2RELS[key])
    hit_rels.discard(rel)
    for r in hit_rels:
        hits[r].append(rel)
print(f"refscan_secs={time.time()-t0:.1f} files_with_hits={nscanned}", file=sys.stderr)

# ---- per-file detail for html/js/css ---------------------------------------
SCRIPT_SRC = re.compile(r"""<script[^>]*\bsrc=["']([^"']+)["']""", re.I)
LINK_HREF = re.compile(r"""<link[^>]*\bhref=["']([^"']+)["']""", re.I)
A_HREF = re.compile(r"""<a\b[^>]*\bhref=["']([^"']#+[^"']*)["']""", re.I)
IMG_SRC = re.compile(r"""<img[^>]*\bsrc=["']([^"']+)["']""", re.I)
FETCH = re.compile(r"""(?:fetch|EventSource)\(\s*["'`]([^"'`]+)["'`]""", re.I)
OPEN_LOC = re.compile(r"""(?:window\.open|location(?:\.href)?\s*=|location\.assign)\(?\s*["'`]([^"'`]+\.html[^"'`]*)["'`]""", re.I)
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)

def out_edges(text):
    e = {}
    for name, rx in (("script", SCRIPT_SRC), ("link", LINK_HREF), ("a", A_HREF),
                     ("img", IMG_SRC), ("fetch", FETCH), ("open", OPEN_LOC)):
        vals = sorted(set(m.group(1).strip() for m in rx.finditer(text)))
        if vals:
            e[name] = vals
    return e

detail = {}
for r in HJC:
    p = ROOT / r
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""
    d = {
        "size": p.stat().st_size,
        "title": (m.group(1).strip()[:120] if (m := TITLE.search(text)) else None),
        "out": out_edges(text),
        "refs": sorted(set(hits[r])),
        "refs_dash": sorted(set(x for x in hits[r] if x.startswith("dashboard/"))),
    }
    detail[r] = d

out = {
    "inventory_n": len(inv),
    "by_ext": {},
    "files": detail,
}
for rel, sz in inv:
    ext = Path(rel).suffix.lstrip(".") or "none"
    out["by_ext"][ext] = out["by_ext"].get(ext, 0) + 1
out["inventory"] = inv

dest = Path(__file__).with_name("_f19_census_raw.json")
dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
print(f"wrote {dest} detail_files={len(detail)}", file=sys.stderr)
