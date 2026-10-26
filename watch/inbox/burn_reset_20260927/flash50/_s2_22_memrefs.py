# s2-22 reference passes v2 (line-mode, exact attribution).
# Why v2: rg -o with a 2,379-pattern -f file silently drops matches (rg 15.2.0; verified
# empirically: 'BURN_adversarial-self-probes_20260927_d' found by single-pattern -e and
# line-mode, never emitted by multi-pattern -o). Line-mode + python substring attribution
# is exact. Canonical pass redone the same way with git grep -n -F.
import os, re, json, subprocess, datetime, collections, sys

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "_s2_22_raw.json")
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, ".git")):
    ROOT = os.path.dirname(ROOT)
INBOX = os.path.join(ROOT, "watch", "inbox")

with open(RAW, encoding="utf-8") as f:
    data = json.load(f)
rows = data["rows"]
GENERIC = {"readme", "license", "changelog", "index", "todo", "notes"}

stems = sorted({r["stem"] for r in rows if r["stem"].lower() not in GENERIC})
by_first4 = collections.defaultdict(list)
for s in stems:
    by_first4[s[:4]].append(s)
TOK = re.compile(r"[A-Za-z0-9_\-]{4,}")
# stems with characters outside the token alphabet (e.g. dots) can never sit inside one
# token; test them directly against the line text
odd_stems = [s for s in stems if not re.fullmatch(r"[A-Za-z0-9_\-]+", s)]

def attribute(cmd, cwd, refs, tag):
    """stream `cmd` output lines 'path:lineno:content', credit refs[stem] |= {path}"""
    t0 = datetime.datetime.now()
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         text=True, encoding="utf-8", errors="replace", bufsize=1 << 20,
                         creationflags=CREATE_NO_WINDOW)
    nlines = 0
    for line in p.stdout:
        nlines += 1
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        path = parts[0].replace("\\", "/")
        content = parts[2]
        hit = None
        for tok in TOK.findall(content):
            grams = {tok[i:i + 4] for i in range(len(tok) - 3)}
            for g4 in grams:
                for s in by_first4.get(g4, ()):
                    if s in tok:
                        if hit is None:
                            hit = set()
                        hit.add(s)
        for s in odd_stems:
            if s in content:
                if hit is None:
                    hit = set()
                hit.add(s)
        if hit:
            for s in hit:
                refs.setdefault(s, set()).add(path)
    p.wait()
    print(tag, "exit", p.returncode, "lines", nlines,
          "took", round((datetime.datetime.now() - t0).total_seconds(), 1), "s",
          file=sys.stderr)
    return nlines

# pass 1: canonical roots (tracked files only, git grep -n -F)
PATHSPECS = ["docs", "queue", "state", "configs", "mag", "tools", "scripts", "githooks",
             "tests", "corpus/steal", "roblox/docs", ".agents",
             "memory/rib", "memory/briefs", "memory/improve", "memory/workflows",
             "memory/boot", "memory/attention.md", "memory/live_from_grok.md",
             "AGENTS.md", "CONSTITUTION.md", "README.md", "LOAD.md",
             "HANDOFF_MAG_AGENT_TODOS.md"]
stems_path = os.path.join(HERE, "_s2_22_stems.txt")
ext_refs = {}
attribute(["git", "grep", "-n", "-I", "-F", "-f", stems_path, "--"] + PATHSPECS,
          ROOT, ext_refs, "canonical git grep")

# pass 2: memory + watch minus inbox minus archival memory/corpus (ripgrep, line mode)
mem_refs = {}
n2 = attribute(["rg", "-n", "-F", "-f", stems_path, "--no-messages",
                "-g", "!watch/inbox/**", "-g", "!memory/corpus/**", "memory", "watch"],
               ROOT, mem_refs, "mem/watch rg line-mode")

# generic-named files: full-path needle, canonical pass only
for r in rows:
    if r["stem"].lower() in GENERIC:
        needle = "watch/inbox/" + r["rel"]
        g = subprocess.run(["git", "grep", "-n", "-I", "-F", "-e", needle, "--"] + PATHSPECS,
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", creationflags=CREATE_NO_WINDOW)
        hits = set(l.split(":", 1)[0] for l in g.stdout.splitlines() if l)
        ext_refs[r["rel"]] = hits

for r in rows:
    key = r["stem"] if r["stem"].lower() not in GENERIC else r["rel"]
    er = sorted(ext_refs.get(key, ()))
    mr = sorted(mem_refs.get(key, ()))
    r["ext_refs"] = len(er)
    r["ref_by"] = er[:5]
    r["mem_refs"] = len(mr)
    r["mem_by"] = mr[:3]

with open(os.path.join(ROOT, "watch", "inbox", "INDEX.json"), encoding="utf-8") as f:
    idx = json.load(f)
items = idx.get("items", [])
reg_class = {}
for it in items:
    reg_class[os.path.basename(it.get("path", ""))] = it.get("class", "")
matched = agree = 0
xtab = collections.defaultdict(lambda: collections.defaultdict(int))
clash = []
for r in rows:
    base = os.path.basename(r["rel"])
    if base in reg_class:
        matched += 1
        rc = reg_class[base]
        xtab[r["class"]][rc] += 1
        if rc == r["class"]:
            agree += 1
        elif len(clash) < 400:
            clash.append((r["rel"], r["class"], rc))
data["summary"]["registry_items"] = len(items)
data["summary"]["registry_classes"] = dict(collections.Counter(
    it.get("class", "") for it in items))
data["summary"]["xtab_matched"] = matched
data["summary"]["xtab_agree"] = agree
data["summary"]["xtab_dup_basename"] = 0
data["xtab"] = {k: dict(v) for k, v in xtab.items()}
data["xtab_clash_samples"] = clash
data["summary"]["ext_ref_files"] = sum(1 for r in rows if r["ext_refs"])
canon_count = collections.Counter()
for hits in ext_refs.values():
    for p in hits:
        canon_count[p] += 1
data["summary"]["ref_by_top"] = dict(canon_count.most_common(25))
data["summary"]["reg_ref_files"] = sum(1 for r in rows if r["reg_ref"])
data["summary"]["mem_ref_files"] = sum(1 for r in rows if r["mem_refs"])
data["summary"]["referenced_any"] = sum(1 for r in rows if r["ext_refs"] or r["reg_ref"]
                                        or r["mem_refs"])
data["summary"]["zero_ref_any"] = sum(1 for r in rows if not (r["ext_refs"] or r["reg_ref"]
                                                              or r["mem_refs"]))
canon_union = sum(1 for r in rows if r["ext_refs"] or r["reg_ref"])
mem_only = sum(1 for r in rows if r["mem_refs"] and not (r["ext_refs"] or r["reg_ref"]))
data["summary"]["canon_union"] = canon_union
data["summary"]["mem_only"] = mem_only
data["summary"]["mem_pass_lines"] = n2
data["summary"]["ref_pass_v2_moment"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
with open(RAW, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f)
print(json.dumps({k: data["summary"][k] for k in
                  ("ext_ref_files", "reg_ref_files", "mem_ref_files", "canon_union",
                   "mem_only", "referenced_any", "zero_ref_any", "registry_items",
                   "xtab_matched", "xtab_agree", "mem_pass_lines")}, indent=1))
