# s2-22 instrument: census of every markdown file under watch/inbox/
# Read-only over the repo except its own JSON dump in flash50/.
# Emits: _s2_22_raw.json (aggregates + per-file rows) and a stdout summary.
import os, re, sys, json, subprocess, datetime, collections

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
ROOT = os.path.dirname(os.path.abspath(__file__))
while os.path.basename(ROOT) not in ("local_sovereign_agent",) and os.path.basename(ROOT):
    ROOT = os.path.dirname(ROOT)
INBOX = os.path.join(ROOT, "watch", "inbox")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s2_22_raw.json")
CENSUS_MOMENT = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

MODE = sys.argv[1] if len(sys.argv) > 1 else "draft"   # draft | full

# ---------- 1. collect md files ----------
SELF_NAMES = {"s2-22.md", "inbox-genre-census.md"}  # twin outputs, written after the scan
rows = []
for dp, dns, fs in os.walk(INBOX):
    dns.sort()
    for fn in sorted(fs):
        if not fn.lower().endswith(".md"):
            continue
        if fn in SELF_NAMES and os.path.abspath(dp) == os.path.dirname(os.path.abspath(__file__)):
            continue
        p = os.path.join(dp, fn)
        try:
            st = os.stat(p)
            size = st.st_size
            mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
        except OSError:
            continue
        rel = os.path.relpath(p, INBOX).replace("\\", "/")
        rows.append({"rel": rel, "size": size, "mtime": mtime})

# ---------- 2. git facts ----------
def run_git(args):
    return subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          creationflags=CREATE_NO_WINDOW)

tracked = set()
g = run_git(["ls-files", "--", "watch/inbox"])
for line in g.stdout.splitlines():
    line = line.strip().replace("\\", "/")
    if line.lower().endswith(".md"):
        tracked.add(line[len("watch/inbox/"):])

first_add = {}
g = run_git(["log", "--diff-filter=A", "--date=short", "--format=@%ad@", "--name-only", "--", "watch/inbox"])
cur = None
for line in g.stdout.splitlines():
    line = line.strip()
    if line.startswith("@") and line.endswith("@"):
        cur = line.strip("@")
        continue
    if not line or cur is None:
        continue
    if not line.lower().endswith(".md"):
        continue
    rel = line[len("watch/inbox/"):] if line.startswith("watch/inbox/") else line
    rel = rel.replace("\\", "/")
    if rel not in first_add or cur < first_add[rel]:
        first_add[rel] = cur  # log is newest-first; keep the oldest date seen

# ---------- 3. classification ----------
MONTH_RE = re.compile(r"(2026-?\d{2}-?\d{2})")
PROFANITY = re.compile(r"\b(shit|fuck|fucking|bitch|bullshit)\b", re.I)

NUMBERED = re.compile(r"^(B2|FW|W[0-9]|Q)[-_]?[0-9]")
LAWWORD = re.compile(r"(?<![A-Za-z])(LAW|LAWS|RIB|CLIPPY|CONSTITUTION|MAXIM)(?![a-z])")

def classify(rel, stem, head):
    u = stem.upper()
    hl = head.lower()
    h1 = ""
    for line in head.splitlines():
        if line.lstrip().startswith("#"):
            h1 = line.strip().lower()
            break
    first80 = h1[:110]
    head600 = head[:600].lower()
    numbered = bool(NUMBERED.match(u)) or u.startswith(("THE50", "THE_50"))
    # 1 numbered burn receipts outrank everything (the number is the receipt id)
    if numbered:
        if "## verdict" in hl or "receipt" in head600:
            return "receipt"
        if rel.startswith("burn_reset_20260927/queue/"):
            return "brief"  # banked work ask
        return "receipt"    # numbered seat output / numbered law receipt
    # 2 law (word-boundary LAW: OPENCLAW/FLAW must not match)
    if (LAWWORD.search(u) or u.startswith("RIB_") or "CLIPPY" in u or "CONSTITUTION" in u
            or h1.startswith("# law") or "law-candidate" in first80 or "law:" in first80
            or "maxim" in h1):
        return "law"
    # 3 brief / handoff / prompt / ask
    if any(k in u for k in ("BRIEF", "HANDOFF", "ONBOARD", "PROMPT", "DISPATCH", "ASK_",
                            "NEXT-WINDOW", "ORDER_", "MEMO")):
        return "brief"
    # 4 shitpost / whim: explicit markers on the heading line only
    if ("SHITPOST" in u or "WHIM" in u or "shitpost" in first80 or "roast" in first80
            or "dream" in first80 or "vision, verbatim" in first80
            or rel.startswith("journal_mark_202609/")):
        return "shitpost"
    # 5 finding: research deliverable signatures (before generic receipt word)
    if (("research" in first80 and "receipt" in first80) or any(k in u for k in (
            "CENSUS", "ANALYSIS", "GAP_", "DECODE", "DISSECTOR", "FOLD", "THEORY", "LENS",
            "STEAL", "PLAYBOOK", "DIGEST", "THREAD", "UNPACK", "SOURCE", "STUDY",
            "DEEP-", "DEEP_", "MAP", "RESEARCH", "SURVEY", "NOTES", "REVIEW", "PROBE"))):
        return "finding"
    # 6 receipt: work receipts (burn passes, verdict receipts, closes, checkpoints)
    if ("RECEIPT" in u or u.startswith("BURN") or "CLOSE_" in u or "VERDICT" in u
            or "receipt" in first80 or "## verdict" in hl or "verdict receipt" in first80
            or "checkpoint" in hl or "salon" in hl or "constraint ledger" in hl
            or "bank:" in head600 or "status: banked" in hl):
        return "receipt"
    # 7 stage-2 refinement of the residue
    whim_words = ("shitpost", "roast", "dream", "vision, verbatim", "operator's vision")
    if any(w in first80 for w in whim_words):
        return "shitpost"
    if any(w in hl for w in ("receipt", "verdict", "checkpoint", "salon", "status:",
                             "delivered")):
        return "receipt"
    if any(w in hl for w in ("reconciliation", "analysis", "eval", "study", "survey",
                             "inventory", "mapping", "notes", "riddle", "spec", "proposal",
                             "corpus", "research", "landscape", "review", "unpack",
                             "decoder", "primer", "audit", "experiment")):
        return "finding"
    if (rel.startswith(("mickey/", "burn_reset_20260927/work/", "burn_reset_20260927/flash50/"))
            or any(rel.startswith(pfx) for pfx in
                   ("burn_wave_20260926/", "wave_20260916/", "physical_computing/"))):
        return "receipt"  # lane seat output / work artifact
    if rel.startswith("burn_reset_20260927/flash50/") and any(
            w in hl for w in ("deep", "theory", "census", "map")):
        return "finding"
    return "other"

for r in rows:
    stem = os.path.basename(r["rel"])[:-3]
    r["stem"] = stem
    m = MONTH_RE.search(stem)
    if m:
        d = m.group(1)
        if "-" not in d:
            d = "%s-%s-%s" % (d[0:4], d[4:6], d[6:8])
        r["fdate"] = d
    else:
        r["fdate"] = ""
    r["tracked"] = r["rel"] in tracked
    r["git_add"] = first_add.get(r["rel"], "")
    r["group"] = r["rel"].split("/")[0] if "/" in r["rel"] else "(top)"
    p = os.path.join(INBOX, r["rel"])
    try:
        with open(p, "rb") as fh:
            head = fh.read(4096).decode("utf-8", "replace")
    except OSError:
        head = ""
    r["head"] = head
    r["class"] = classify(r["rel"], stem, head)
    r["h1"] = ""
    for line in head.splitlines():
        if line.lstrip().startswith("#"):
            r["h1"] = line.strip()[:140]
            break
    del r["head"]

# ---------- 4. reference resolution (full mode: one git grep pass) ----------
if MODE == "full":
    t0 = datetime.datetime.now()
    GENERIC = {"readme", "license", "changelog", "index", "todo", "notes"}
    stems_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s2_22_stems.txt")
    with open(stems_path, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            if r["stem"].lower() not in GENERIC:
                fh.write(r["stem"] + "\n")
    PATHSPECS = ["docs", "queue", "state", "configs", "mag", "tools", "scripts", "githooks",
                 "tests", "corpus/steal", "roblox/docs", ".agents",
                 "memory/rib", "memory/briefs", "memory/improve", "memory/workflows",
                 "memory/boot", "memory/attention.md", "memory/live_from_grok.md",
                 "AGENTS.md", "CONSTITUTION.md", "README.md", "LOAD.md",
                 "HANDOFF_MAG_AGENT_TODOS.md"]
    g = run_git(["grep", "-oI", "-F", "-f", stems_path, "--"] + PATHSPECS)
    print("git grep exit", g.returncode, "lines", len(g.stdout.splitlines()), file=sys.stderr)
    stem_refs = {}
    for line in g.stdout.splitlines():
        if ":" not in line:
            continue
        path, _, matched = line.partition(":")
        stem_refs.setdefault(matched, set()).add(path)
    # generic-named files: resolve by full relative path needle instead of bare stem
    for r in rows:
        if r["stem"].lower() not in GENERIC:
            continue
        needle = "watch/inbox/" + r["rel"]
        gg = run_git(["grep", "-oI", "-F", "-e", needle, "--"] + PATHSPECS)
        stem_refs[r["rel"]] = set(l.partition(":")[0] for l in gg.stdout.splitlines() if l)
    try:
        with open(os.path.join(INBOX, "INDEX.json"), "rb") as fh:
            idx_text = fh.read().decode("utf-8", "replace")
    except OSError:
        idx_text = ""
    for r in rows:
        key = r["stem"] if r["stem"].lower() not in GENERIC else r["rel"]
        refs = sorted(stem_refs.get(key, ()))
        r["ext_refs"] = len(refs)
        r["ref_by"] = refs[:5]
        r["reg_ref"] = 1 if r["stem"] in idx_text else 0
    print("ref pass took", round((datetime.datetime.now() - t0).total_seconds(), 1),
          "s; stems with refs:", len(stem_refs), file=sys.stderr)

# ---------- 5. aggregates ----------
def agg():
    out = {}
    out["moment"] = CENSUS_MOMENT
    out["mode"] = MODE
    out["md_total"] = len(rows)
    out["md_bytes"] = sum(r["size"] for r in rows)
    out["tracked_md"] = sum(1 for r in rows if r["tracked"])
    out["git_dated"] = sum(1 for r in rows if r["git_add"])
    out["fdated"] = sum(1 for r in rows if r["fdate"])
    out["class_counts"] = dict(collections.Counter(r["class"] for r in rows))
    out["class_bytes"] = {c: sum(r["size"] for r in rows if r["class"] == c)
                          for c in out["class_counts"]}
    months = collections.Counter(r["fdate"][:7] for r in rows if r["fdate"])
    out["by_month"] = dict(sorted(months.items()))
    fd = sorted(r["fdate"] for r in rows if r["fdate"])
    out["fdate_min"] = fd[0] if fd else ""
    out["fdate_max"] = fd[-1] if fd else ""
    ga = sorted(r["git_add"] for r in rows if r["git_add"])
    out["git_add_min"] = ga[0] if ga else ""
    out["git_add_max"] = ga[-1] if ga else ""
    mt = sorted(r["mtime"] for r in rows)
    out["mtime_min"] = mt[0]
    out["mtime_max"] = mt[-1]
    out["by_group"] = dict(collections.Counter(r["group"] for r in rows).most_common(40))
    out["undated"] = [r["rel"] for r in rows if not r["fdate"]][:200]
    if MODE == "full":
        out["ext_ref_files"] = sum(1 for r in rows if r.get("ext_refs"))
        out["reg_ref_files"] = sum(1 for r in rows if r.get("reg_ref"))
        out["zero_ref_files"] = sum(1 for r in rows
                                    if not r.get("ext_refs") and not r.get("reg_ref"))
        out["ref_by_top"] = dict(collections.Counter(
            n for r in rows for n in r.get("ref_by", [])).most_common(25))
        for r in rows:
            r.pop("head", None)
    return out

summary = agg()
if MODE == "full":
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"summary": summary, "rows": rows}, fh, indent=1)
else:
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"summary": summary, "rows": rows}, fh, indent=1)

print(json.dumps({k: v for k, v in summary.items() if k != "undated"}, indent=1))
if MODE == "draft":
    import random
    rnd = random.Random(22)
    for cls in ("other", "law", "shitpost", "receipt", "finding", "brief"):
        pool = [r for r in rows if r["class"] == cls]
        print("\n#### SAMPLE", cls, len(pool))
        for r in rnd.sample(pool, min(12, len(pool))):
            print(" ", r["rel"], "|", r["h1"][:110])
