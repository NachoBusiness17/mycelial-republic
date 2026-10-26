#!/usr/bin/env python
# cross-librarian (division B, ouroboros): CROSS-DOGFOOD 3, the librarian rides the fleet.
# Applies the librarian-expedition holdings doctrine (HOLD-BOTH-DIRECTIONS,
# LIVENESS-IS-NOT-TRUTH, no verdict=LANDED without the primary in holdings) to every
# standing workflow's cited primaries in the last 48h.
# Method follows the cited-missing lane's instruments (extract_citations.py + holdings_check.py),
# widened to the fleet surfaces the prior sweep did not see (music, salon_mine, ractor_engine,
# fillball, gap register + its 15 run lanes, 48h_synth gala ball, mickey17-v2 addendum) plus the
# music program's genius.com citation class.
# v2 perf notes: v1 burned CPU in per-citation x per-file held loops (530k estate files) and
# unused os.path.getsize stats; v2 extracts first, then resolves all holdings in ONE walk pass
# against a compiled alternation of the citation tokens. All reads stay inside ROOT (containment
# check on the one ABS surface).
# No em-dashes in emitted records (record law). Read-only over the estate except its own lanes dir.
import os, re, json, glob, time, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = lambda *a: print(*a, flush=True)

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
INBOX = ROOT + "/watch/inbox"
LANES = ROOT + "/watch/inbox/gala_20260925/ouroboros/lanes"
NOW = time.time()
WINDOW_48H = NOW - 48 * 3600
NOW_ISO = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW))
WINDOW_ISO = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(WINDOW_48H))

# ---------- fleet surface map (workflow, glob) ----------
# "ABS:" prefix = path is absolute (root-anchored), still containment-checked against ROOT.
def G(pat):
    if pat.startswith("ABS:"):
        p = os.path.realpath(pat[4:])
        root_real = os.path.realpath(ROOT)
        if not p.lower().startswith(root_real.lower()):
            return []
        return sorted(glob.glob(p, recursive=True))
    return sorted(glob.glob(INBOX + "/" + pat, recursive=True))

SURFACES = [
    ("olm-mine",            "frontier_olm_2026-09-30/steal/*.md"),
    ("olm-mine",            "frontier_olm_2026-10-01/steal/*.md"),
    ("olm-mine",            "frontier_olm_2026-10-01/DIGEST.md"),
    ("olm-mine",            "frontier_olm_2026-10-01/RECEIPT.md"),
    ("wide-dig",            "spiking_wide/*.md"),
    ("wide-dig",            "gala_20260925/spiking-wide/**/*.md"),
    ("wide-dig",            "gala_20260925/spiking-wide/**/*.json"),
    ("wide-dig",            "gala_20260925/spiking-wide_RECEIPT.md"),
    ("drop-dig",            "localfirst/*.md"),
    ("drop-dig",            "LOCALFIRST_MEMORY_LANDSCAPE_20261001.md"),
    ("drop-dig",            "SPIKINGBRAIN_DROP_20261001.md"),
    ("drop-dig",            "STRATA_DROP_20261001.md"),
    ("drop-dig",            "DOUBLE_DROP_20261001.md"),
    ("drop-dig",            "x_intel_drop_20261001.md"),
    ("drop-dig",            "x_intel_deepgemm_20261001.md"),
    ("drop-dig",            "model_mating_paper_dig_20261001.md"),
    ("drop-dig",            "ABLITERATUS_DROP_20260929.md"),   # boundary: 09-29T09:51Z, prior sweep's window, kept for continuity
    ("drop-dig",            "gala_20260925/localfirst-steal/**/*.md"),
    ("drop-dig",            "gala_20260925/localfirst-steal/**/*.json"),
    ("drop-dig",            "gala_20260925/localfirst-steal_RECEIPT.md"),
    ("music program",       "music/*.md"),
    ("music program",       "gala_20260925/music-ractor/**/*.md"),
    ("music program",       "gala_20260925/music-ractor/**/*.json"),
    ("music program",       "gala_20260925/music-ractor_RECEIPT.md"),
    ("music program",       "gala_20260925/lyric-workover/**/*.md"),
    ("music program",       "gala_20260925/lyric-workover/**/*.json"),
    ("music program",       "gala_20260925/lyric-workover_RECEIPT.md"),
    ("music program",       "gala_20260925/vonnegut-final/**/*.md"),
    ("music program",       "gala_20260925/vonnegut-final/**/*.json"),
    ("music program",       "gala_20260925/vonnegut-final_RECEIPT.md"),
    ("salon-mine",          "salon_mine/*.md"),
    ("salon-mine",          "salon_mine/*.txt"),
    ("salon-mine",          "gala_20260925/salon-mine/**/*.md"),
    ("salon-mine",          "gala_20260925/salon-mine/**/*.json"),
    ("gap-analysis",        "gap_analysis_20261001/GAP_REGISTER.md"),
    ("gap-analysis",        "ABS:C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/*.json"),
    ("fill-ball",           "fillball/*.md"),
    ("fill-ball",           "gala_20260925/fillball-1001/**/*.md"),
    ("fill-ball",           "gala_20260925/fillball-1001/**/*.json"),
    ("fill-ball",           "gala_20260925/fillball-1001_RECEIPT.md"),
    ("ractor-engine",       "ractor50/*.md"),
    ("ractor-engine",       "ractor_engine/**/*.md"),
    ("ractor-engine",       "gala_20260925/ractor50/**/*.md"),
    ("ractor-engine",       "gala_20260925/ractor50/**/*.json"),
    ("ractor-engine",       "gala_20260925/ractor50_RECEIPT.md"),
    ("librarian-expedition","librarian_exp/cited-missing.md"),
    ("librarian-expedition","librarian_exp/foundational-gaps.md"),
    ("librarian-expedition","librarian_exp/instrument-audit.md"),
    ("librarian-expedition","librarian_exp/integration.md"),
    ("librarian-expedition","librarian_exp/gathering-log.md"),
    ("librarian-expedition","gala_20260925/librarian-expedition/**/*.md"),
    ("librarian-expedition","gala_20260925/librarian-expedition/**/*.json"),
    ("48h-synth",           "48h_synth/*.md"),
    ("48h-synth",           "gala_20260925/48h-synthesis/**/*.md"),
    ("48h-synth",           "gala_20260925/48h-synthesis/**/*.json"),
    ("48h-synth",           "gala_20260925/48h-synthesis_RECEIPT.md"),
    ("the-gala",            "gala_20260925/GALA_20260925.md"),
    ("mickey17-v2",         "MICKEY17_V2_RUN_SPEC_ADDENDUM.md"),
    ("ADJACENT model_garden (not a standing card workflow)", "model_garden/*.md"),
]

# ---------- extraction regexes (arxiv/github/bare byte-copied from cited-missing extract_citations.py; genius added) ----------
ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?", re.I)
GH    = re.compile(r"github\.com/([A-Za-z0-9_.\-]+)/([A-Za-z0-9_.\-]+)", re.I)
BARE  = re.compile(r"(?<![\w.])2[0-9](0[1-9]|1[0-2])\.[0-9]{4,5}(?![.\d])")
GENIUS = re.compile(r"genius\.com/([A-Za-z0-9_.\-]+)", re.I)

# github.com/<first-segment> values that are URL paths, not owner slugs (observed artifacts:
# api.github.com/repos/<owner>, github.com/users/<owner>, github.com/sponsors/<owner>)
GH_OWNER_BLACKLIST = {"repos", "users", "orgs", "sponsors", "raw", "assets", "gist", "gists",
                      "topics", "features", "marketplace", "explore", "trending", "search",
                      "notifications", "settings", "security", "apps", "account", "new",
                      "import", "dashboard", "watching", "labels", "pricing", "contact",
                      "about", "site", "events", "issues", "pulls", "blog", "careers",
                      "customer-stories", "login", "join", "session", "archive", "collections",
                      "licenses", "license", "user-attachments", "rest", "invitations",
                      "discussions", "organizations", "enterprise", "team", "org"}

def gh_norm(owner, repo):
    """normalize a github owner/repo capture; returns None for URL-path artifacts.
    strips .git suffixes and trailing punctuation; case preserved for display."""
    if owner.lower() in GH_OWNER_BLACKLIST:
        return None
    owner = owner.rstrip(".")
    repo = repo.rstrip(".")
    if repo.lower().endswith(".git"):
        repo = repo[:-4].rstrip(".")
    if not owner or not repo:
        return None
    return owner + "/" + repo

WIDE_PAT = re.compile(r"(DIGEST\.md$|RECEIPT\.md$|LANDSCAPE|_DROP_|SYNTHESIS\.md$|GAP_REGISTER\.md$"
                      r"|48h_synth/|steals\.md$|STORY\.md$|laws\.md$|lattice\.md$|measure\.md$|next\.md$|ERRATA\.md$)", re.I)

# ---------- pass 1: extract citations (no walk needed) ----------
raw = {}
missing_files = []
for wf, pat in SURFACES:
    for path in G(pat):
        if os.path.normpath(path).replace("\\", "/").lower().endswith("ouroboros/"):
            continue  # never mine this lane's own ball
        if not os.path.isfile(path):
            missing_files.append((wf, path))
            continue
        mt = os.path.getmtime(path)
        mtime_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(mt))
        if mt < WINDOW_48H and "ABLITERATUS" not in path:
            continue  # outside the 48h window
        try:
            lines = open(path, encoding="utf-8", errors="replace").readlines()
        except Exception:
            continue
        wide = bool(WIDE_PAT.search(path))
        for lineno, line in enumerate(lines, 1):
            hits = [("arxiv", m.group(1)) for m in ARXIV.finditer(line)]
            for m in GH.finditer(line):
                nv = gh_norm(m.group(1), m.group(2))
                if nv:
                    hits.append(("github", nv.lower()))  # github slugs are case-insensitive; lowercase = dedupe
            hits += [("genius", m.group(1)) for m in GENIUS.finditer(line)]
            for m in BARE.finditer(line):
                v = m.group(0)
                if not any(k == "arxiv" and val == v for k, val in hits):
                    hits.append(("arxiv-bare", v))
            for kind, val in hits:
                k = (wf, kind, val)
                if k not in raw:
                    raw[k] = {"locs": [], "wide": False}
                raw[k]["locs"].append((os.path.relpath(path, ROOT).replace("\\", "/"), lineno, mtime_iso))
                raw[k]["wide"] = raw[k]["wide"] or wide

# prior-sweep registry for delta reporting
prior = set()
try:
    pj = json.loads(open(INBOX + "/gala_20260925/librarian-expedition/unique_citations.json", encoding="utf-8").read())
    rows = pj if isinstance(pj, list) else pj.get("citations", pj.get("rows", []))
    for r in rows:
        kk = r.get("kind", "")
        vv = str(r.get("value", r.get("citation", "")))
        prior.add((kk, vv.lower() if kk == "github" else vv))
except Exception as e:
    P("prior registry read note: %s" % type(e).__name__)

# ---------- pass 2: ONE walk, resolve all holdings ----------
SCRATCH_MARKERS = ("appdata", "%temp%", "%tmpdir%", "tmpdir", "/.git/", "__pycache__", ".mimosa")

ledgers = sorted(glob.glob(ROOT + "/memory/runs/**/*LANDING*.json", recursive=True))
ledger_rows_total = 0
landed = []
for lg in ledgers:
    try:
        d = json.loads(open(lg, encoding="utf-8").read())
    except Exception as e:
        P("LEDGER-PARSE-FAIL %s: %s" % (os.path.basename(lg), type(e).__name__))
        continue
    for r in (d.get("rows") or []):
        ledger_rows_total += 1
        if str(r.get("status", "")).startswith("LANDED") and r.get("landed"):
            landed.append((str(r["landed"]).replace("\\", "/").lower(),
                           str(r.get("title", "")).lower(),
                           str(r.get("ident", "")).lower(),
                           os.path.relpath(lg, ROOT).replace("\\", "/")))
gath = [l for l in landed if "gathering_expedition" in l[3].lower()]

arxiv_ids = sorted({v for (_, k, v) in raw if k in ("arxiv", "arxiv-bare")}, key=len, reverse=True)
genius_slugs = sorted({v for (_, k, v) in raw if k == "genius"}, key=len, reverse=True)
repo_tails = sorted({v.rsplit("/", 1)[-1] for (_, k, v) in raw if k == "github"}, key=len, reverse=True)

esc = lambda s: re.escape(s.lower())
PATTERNS = {}
if arxiv_ids:
    PATTERNS["arxiv"] = re.compile("|".join(esc(x) for x in arxiv_ids))
if genius_slugs:
    PATTERNS["genius"] = re.compile("|".join(esc(x) for x in genius_slugs))
if repo_tails:
    PATTERNS["repo"] = re.compile("|".join(esc(x) for x in repo_tails))

tok_files = {"arxiv": {}, "genius": {}, "repo": {}}   # token -> [relpath lower]
dir_hits = {}                                          # repo tail (exact dir segment) -> [dir relpath lower]
clone_dirs = set()                                     # dirs containing a .git subdir
files_all = []                                         # every walked relpath (lower)
n_files = n_dirs = 0
WALK_ROOTS = ["corpus", "memory", "state", "docs", "mag", "tools", "watch/inbox"]
for w in WALK_ROOTS:
    wp = os.path.join(ROOT, w.replace("/", os.sep))
    for dp, dns, fns in os.walk(wp):
        keep = []
        for d in dns:
            dl = d.lower()
            if dl == ".git":
                clone_dirs.add(os.path.relpath(dp, ROOT).replace("\\", "/").lower())
            elif dl not in ("__pycache__", ".mimosa", "node_modules"):
                keep.append(d)
        dns[:] = keep
        rel = os.path.relpath(dp, ROOT).replace("\\", "/").lower()
        n_dirs += 1
        seg = rel.rsplit("/", 1)[-1] if "/" in rel else rel
        if "repo" in PATTERNS:
            m = PATTERNS["repo"].fullmatch(seg)
            if m:
                dir_hits.setdefault(m.group(0), []).append(rel)
        for fn in fns:
            n_files += 1
            bn = fn.lower()
            full = rel + "/" + bn
            files_all.append(full)
            for cls, rx in PATTERNS.items():
                for m in rx.finditer(bn):
                    tok_files[cls].setdefault(m.group(0), []).append(full)

# one post-pass: files-under-dir counts for every matched dir (no per-repo rewalks)
matched_dirs = sorted({d for ds in dir_hits.values() for d in ds})
dir_file_counts = {d: 0 for d in matched_dirs}
if matched_dirs:
    prefixes = [(d, d + "/") for d in matched_dirs]
    for f in files_all:
        for d, pre in prefixes:
            if f.startswith(pre):
                dir_file_counts[d] += 1

P("HOLDINGS INDEX: %d LANDING ledgers, %d rows scanned, %d LANDED claims (gathering_expedition %d); "
  "walk %d files + %d dirs under corpus/memory/state/docs/mag/tools/watch-inbox; %d clone dirs"
  % (len(ledgers), ledger_rows_total, len(landed), len(gath), n_files, n_dirs, len(clone_dirs)))

def is_scratch(rel_lower):
    return any(m in rel_lower for m in SCRATCH_MARKERS)

def arxiv_hold(cid):
    ev_d, ev_w = [], []
    c = cid.lower()
    for lp, ti, idl, lgn in landed:
        if c in lp or c in idl:
            (ev_d if not is_scratch(lp) else ev_w).append("ledger:%s:%s" % (lgn, lp))
    for f in tok_files["arxiv"].get(c, []):
        (ev_d if not is_scratch(f) else ev_w).append("file:" + f)
    if ev_d:
        return "held-durable", ev_d[:3]
    if ev_w:
        return "held-weak", ev_w[:3]
    return "not-held", []

def genius_hold(slug):
    c = slug.lower()
    hits = tok_files["genius"].get(c, [])
    if hits:
        return "held-durable", ["file:" + f for f in hits[:3]]
    return "not-held", []

def repo_hold(slug):
    """held = the repo's bytes survive offline: a .git clone of it in the estate walk, or an
    archive file named after it. A directory merely NAMED like the repo inside another clone
    (lmcache/integration/vllm), or an unrelated filename containing the tail (a mamba test file),
    is NOT a holding - v3 spot-check caught both inflating held counts."""
    last = slug.rsplit("/", 1)[-1].lower()
    ev = []
    for d in dir_hits.get(last, []):
        if d in clone_dirs:
            ev.append("dir:%s files=%d clone(.git)" % (d, dir_file_counts.get(d, 0)))
    for f in tok_files["repo"].get(last, []):
        bn = f.rsplit("/", 1)[-1]
        if bn.endswith((".zip", ".tar.gz", ".tgz", ".whl", ".tar")):
            ev.append("archive:" + f)
    if ev:
        return "held-durable", ev[:3]
    return "not-held", []

# ---------- held-check every unique citation ----------
per_wf = {}
fleet_uniques = {}
detail = []
for (wf, kind, val), info in sorted(raw.items()):
    if kind in ("arxiv", "arxiv-bare"):
        status, ev = arxiv_hold(val)
        url = "https://arxiv.org/abs/" + val
    elif kind == "genius":
        status, ev = genius_hold(val)
        url = "https://genius.com/" + val
    else:
        status, ev = repo_hold(val)
        url = "https://github.com/" + val
    in_prior = ((kind, val) in prior or
                (("arxiv" if kind == "arxiv-bare" else kind), val.lower() if kind == "github" else val) in prior)
    detail.append({"workflow": wf, "kind": kind, "value": val, "status": status, "evidence": ev,
                   "url": url, "locs": info["locs"], "wide": info["wide"], "in_prior_sweep": in_prior})
    s = per_wf.setdefault(wf, {"held": set(), "weak": set(), "cited_only": set(), "missing": set()})
    s["held" if status == "held-durable" else "weak" if status == "held-weak" else "cited_only"].add((kind, val))
    fu = fleet_uniques.setdefault((kind, val), {"kinds": set(), "wfs": set(), "locs": 0, "wide": False,
                                                "status": status, "ev": ev, "url": url})
    fu["kinds"].add(kind); fu["wfs"].add(wf); fu["locs"] += len(info["locs"]); fu["wide"] = fu["wide"] or info["wide"]
    if status == "held-durable" and fu["status"] != "held-durable":
        fu["status"], fu["ev"] = status, ev

# ---------- probes for the not-held set ----------
not_held = [(k, v) for k, v in fleet_uniques.items() if v["status"] != "held-durable"]
def probe(url):
    try:
        out = subprocess.run(["curl", "-s", "-o", "NUL", "-w", "%{http_code}", "-I", "-L", "-m", "12", url],
                             capture_output=True, text=True, timeout=20)
        return out.stdout.strip() or "ERR"
    except Exception:
        return "ERR"
P("PROBING %d not-held citations (12s cap each, 12-wide pool)..." % len(not_held))
with ThreadPoolExecutor(max_workers=12) as ex:
    codes = list(ex.map(lambda kv: probe(kv[1]["url"]), not_held))
probe_map = {kv[0]: c for kv, c in zip(not_held, codes)}

for (kind, val), fu in fleet_uniques.items():
    if fu["status"] != "held-durable":
        c = probe_map.get((kind, val), "UNPROBED")
        fu["probe"] = c
        fu["final"] = "cited-only" if c == "200" else ("missing" if c not in ("UNPROBED", "ERR") else "unprobed/unknown")
    else:
        fu["final"] = "held"

# ---------- report ----------
order = ["olm-mine", "wide-dig", "drop-dig", "music program", "salon-mine", "gap-analysis",
         "fill-ball", "ractor-engine", "librarian-expedition", "48h-synth", "the-gala",
         "mickey17-v2", "ADJACENT model_garden (not a standing card workflow)"]
P()
P("=== HOLDINGS-OF-THE-FLEET (per workflow, snapshot %s, window since %s) ===" % (NOW_ISO, WINDOW_ISO))
P("%-16s %7s %6s %6s %8s %8s %6s" % ("workflow", "cited", "held", "weak", "cited-", "missing", "LEAK"))
P("%-16s %7s %6s %6s %8s %8s %6s" % ("", "uniques", "", "", "only", "", "count"))
for wf in order:
    if wf not in per_wf:
        P("%-16s %7d %6d %6d %8d %8d %6d" % (wf, 0, 0, 0, 0, 0, 0))
        P("%-16s   (active in window but 0 id/repo-class external-primary citations)" % "")
        continue
    s = per_wf[wf]
    leak = len(s["cited_only"]) + len(s["missing"])
    P("%-16s %7d %6d %6d %8d %8d %6d" % (wf, len(s["held"]) + len(s["weak"]) + len(s["cited_only"]) + len(s["missing"]),
                                         len(s["held"]), len(s["weak"]), len(s["cited_only"]), len(s["missing"]), leak))

tot_held = sum(1 for f in fleet_uniques.values() if f["final"] == "held")
tot_co   = sum(1 for f in fleet_uniques.values() if f["final"] == "cited-only")
tot_miss = sum(1 for f in fleet_uniques.values() if f["final"] == "missing")
tot_unk  = sum(1 for f in fleet_uniques.values() if f["final"] == "unprobed/unknown")
held_pairs = {(d["kind"], d["value"]) for d in detail if d["status"] == "held-durable"}
weak_vals = {(d["kind"], d["value"]) for d in detail
             if d["status"] == "held-weak" and (d["kind"], d["value"]) not in held_pairs}
P()
P("FLEET TOTALS (cross-workflow deduped): %d unique primaries cited | held %d | cited-only %d | "
  "missing %d | unprobed %d | weak(temp-only) %d" % (
      len(fleet_uniques), tot_held, tot_co, tot_miss, tot_unk, len(weak_vals)))
new_vs_prior = [d for d in detail if not d["in_prior_sweep"]]
new_pairs = {(d["kind"], d["value"]) for d in new_vs_prior}
P("vs prior cited-missing sweep registry: %d workflow-citation pairs, %d unique citations are on surfaces the prior sweep did not see" % (
      len(new_vs_prior), len(new_pairs)))

# ---------- top 10 for the next gathering expedition ----------
def weight(item):
    (kind, val), fu = item
    w = min(fu["locs"], 20)
    if fu["wide"]: w += 25
    w += 5 * len(fu["wfs"])
    if fu["final"] == "missing": w += 3
    return w
cands = [(k, v) for k, v in fleet_uniques.items() if v["final"] in ("cited-only", "missing", "unprobed/unknown")]
cands.sort(key=weight, reverse=True)
P()
P("=== TOP 10 FOR THE NEXT GATHERING EXPEDITION (not held, ranked by claim weight) ===")
for i, ((kind, val), fu) in enumerate(cands[:10], 1):
    wfs = "+".join(sorted(fu["wfs"]))
    P("%2d. %-28s %-8s wfs=%-40s locs=%2d probe=%s -> %s" % (
        i, val[:28], kind, wfs[:40], fu["locs"], fu.get("probe", "-"), fu["url"]))

P()
P("=== EVERY NOT-HELD PRIMARY (deterministic order) ===")
for (kind, val), fu in sorted(cands, key=lambda x: (x[1]["final"], -weight(x))):
    wfs = "+".join(sorted(fu["wfs"]))
    P("%-8s %-30s %-8s locs=%2d probe=%-4s %s" % (fu["final"], val[:30], kind, fu["locs"], fu.get("probe", "-"), wfs))

# ---------- bank raw detail ----------
out = {"ts": NOW_ISO, "window_since": WINDOW_ISO,
       "holdings_index": {"ledgers": len(ledgers), "ledger_rows": ledger_rows_total, "landed": len(landed),
                          "gathering_expedition_landed": len(gath),
                          "files_walked": n_files, "dirs_walked": n_dirs},
       "per_workflow": {wf: {k: sorted([list(x) for x in v]) for k, v in per_wf[wf].items()} for wf in order if wf in per_wf},
       "fleet_totals": {"uniques": len(fleet_uniques), "held": tot_held, "cited_only": tot_co,
                        "missing": tot_miss, "unprobed": tot_unk, "weak": len(weak_vals)},
       "probes": {"%s|%s" % k: v for k, v in probe_map.items()},
       "citations": detail}
with open(LANES + "/fleet_citations.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
P()
P("wrote " + LANES + "/fleet_citations.json")
if missing_files:
    P("MISSING SURFACE FILES: %d" % len(missing_files))
    for wf, pth in missing_files:
        P("  %s %s" % (wf, pth))
