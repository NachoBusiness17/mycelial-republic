"""f-19 recheck + final classify.

Takes v1 raw ref map (basename substring matching) and re-verifies every hit
with boundary-correct regexes, only re-reading the ~2.3k files that matched.
Then classifies each html/js/css file into SERVER / INDEX / PAGE / CODE / ORPHAN.
"""
import json, re
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent
ROOT = HERE.parents[3]
d = json.loads((HERE / "_f19_census_raw.json").read_text(encoding="utf-8"))
files = d["files"]

def bpat(name):
    return re.compile(r"(?<![\w.-])" + re.escape(name) + r"(?![\w.-])")

# key: rel file -> ordered list of (regex, keyname) to verify
PAT = {}
for rel in files:
    b = Path(rel).name
    if rel == "dashboard/static/index.html":
        PAT[rel] = [(re.compile(r"(?<![\w./-])(?:static/)?index\.html(?![\w.-])"), "root")]
    elif rel.endswith("/index.html"):
        parent = rel[len("dashboard/static/"):-len("index.html")]
        PAT[rel] = [(re.compile(r"(?<![\w./-])" + re.escape(parent + "index.html") + r"(?![\w.-])"), "dir")]
    else:
        PAT[rel] = [(bpat(b), "base")]

# union of refs to re-read
all_refs = set()
for rel, v in files.items():
    all_refs.update(v["refs"])
print(f"recheck_corpus={len(all_refs)}", file=open(0, 'w')) if False else None
import sys
print(f"recheck_files={len(all_refs)}", file=sys.stderr)

# verify: for each ref file, for each claimed target, does a boundary match exist?
true_hits = {rel: set() for rel in files}   # target rel -> set of ref rels
# invert: ref file -> targets claimed
claim = {}
for rel, v in files.items():
    for s in v["refs"]:
        claim.setdefault(s, set()).add(rel)

nref = 0
for ref_rel in claim:
    p = ROOT / ref_rel
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    nref += 1
    for target in claim[ref_rel]:
        if target == ref_rel:
            continue
        for rx, kind in PAT[target]:
            if rx.search(text):
                true_hits[target].add(ref_rel)
                break
print(f"rechecked={nref}", file=sys.stderr)

NOISE = (".mimosa", "_archaeology_out/", "dashboard-deploy/", "dist_audit/", "site/")
SERVER_TARGETS = {
    "dashboard/static/chan.html", "dashboard/static/wave.html",
    "dashboard/static/index.html", "dashboard/static/sovereign_shell.html",
    "dashboard/static/cast-voice.html", "dashboard/static/seat.html",
    "dashboard/static/fleet.html", "dashboard/static/health.html",
    "dashboard/static/aos.html",
}
STUBS = {
    "dashboard/static/mud.html": "games/mud.html",
    "dashboard/static/arrakis.html": "games/arrakis.html",
    "dashboard/static/arena_operator_field.html": "games/arena_operator_field.html",
    "dashboard/static/maze_arena.html": "games/maze_arena.html",
}

def live(s):
    if s.startswith("dashboard-deploy/") or "_archaeology_out/" in s or "dist_audit/" in s \
       or ".mimosa" in s or s.startswith("site/"):
        return False
    return True

def is_live_page(s):
    return (s.startswith("dashboard/static/") and ".bak" not in s
            and not s.endswith(".retired")
            and not s.startswith("dashboard/static/museum/")
            and live(s))

CODE_PREFIX = ("mag/", "tools/", "scripts/", "tests/", "configs/", "docs/",
               "state/", "queue/", "main.py", "mag.cmd", "githooks/")

rows = []
for rel, v in sorted(files.items()):
    refs = {s for s in true_hits[rel] if live(s) and s != rel}
    stub_of = STUBS.get(rel)
    if stub_of:
        refs = {s for s in refs if stub_of not in s}
    code = sorted(s for s in refs if s.startswith(CODE_PREFIX))
    page = sorted(s for s in refs if is_live_page(s))
    server_py = sorted(s for s in refs if s in ("dashboard/server.py", "dashboard/rest.py"))
    weak = sorted(s for s in refs if s not in code and s not in page and s not in server_py)

    if rel in SERVER_TARGETS:
        cls = "SERVER"
    elif rel.endswith("/index.html"):
        cls = "INDEX"
    elif rel == "dashboard/static/index.html":
        cls = "SERVER"
    elif page:
        cls = "PAGE"
    elif code or server_py:
        cls = "CODE"
    else:
        cls = "ORPHAN"

    rows.append({
        "rel": rel, "size": v["size"], "title": v["title"], "out": v["out"], "cls": cls,
        "n_code": len(code), "n_page": len(page), "n_weak": len(weak),
        "code_refs": code[:8], "page_refs": page[:8], "weak_refs": weak[:8],
        "n_true_refs": len(true_hits[rel]),
    })

(HERE / "_f19_final.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
print(Counter(r["cls"] for r in rows))
print()
print("=== ORPHANS (zero live refs of any kind) ===")
for r in rows:
    if r["cls"] == "ORPHAN":
        print(f"{r['rel']} ({r['size']}B) title={r['title']!r}")
        print(f"   weak_mentions={r['weak_refs'][:4]} n_weak={r['n_weak']}")
print()
print("=== CODE-only (no page links it) ===")
for r in rows:
    if r["cls"] == "CODE":
        print(f"{r['rel']} ({r['size']}B) code={r['code_refs'][:5]} serverpy={bool([s for s in r['weak_refs'] if 'rest.py' in s])}")
