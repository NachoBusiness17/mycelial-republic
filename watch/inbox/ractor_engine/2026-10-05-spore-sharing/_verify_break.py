# break-economics verification script, 2026-10-05.
# Byte-checks every evidence cite in the spore-sharing lens report.
# Prints masked output only: no secret VALUES are ever printed.
import glob
import json
import os
import re
import sqlite3
import subprocess
from collections import defaultdict

CREATE_NO_WINDOW = 0x08000000  # win32 law: no console window on spawned subprocesses
MASK = re.compile(r"[A-Za-z0-9_\-]{12,}")


def mask(s, keep=4):
    return MASK.sub(lambda m: m.group(0)[:keep] + "...MASK", s)


def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True,
                       creationflags=CREATE_NO_WINDOW, encoding="utf-8", errors="replace")
    return r.stdout


print("=" * 70)
print("CHECK-01 blob census: git ls-tree -r -l HEAD, blobs > 100 MiB (untruncated)")
out = git("ls-tree", "-r", "-l", "HEAD")
rows = []
for l in out.splitlines():
    parts = l.split(None, 4)
    if len(parts) == 5 and parts[1] == "blob" and parts[3].isdigit():
        rows.append((int(parts[3]), parts[4], parts[2]))
big = sorted([b for b in rows if b[0] > 104857600], reverse=True)
print("blobs total in HEAD tree:", len(rows))
print("blobs over 104857600 bytes:", len(big))
for size, path, sha in big[:25]:
    print("  ", round(size / 1048576, 1), "MB", path)
if big:
    top_sha = big[0][2]
    dups = [p for s, p, sh in rows if sh == top_sha]
    print("paths sharing top blob sha", top_sha[:12], ":", dups)

print("=" * 70)
print("CHECK-02 tracked file counts (git ls-files, untruncated)")
files = git("ls-files").splitlines()
print("tracked total:", len(files))
print("under memory/:", sum(1 for f in files if f.startswith("memory/")))
print("under watch/:", sum(1 for f in files if f.startswith("watch/")))
print("under memory/+watch/:", sum(1 for f in files if f.startswith(("memory/", "watch/"))))
print("tracked .mimosa (ext):", sum(1 for f in files if f.endswith(".mimosa")))
print("tracked containing 'mimosa':", sum(1 for f in files if "mimosa" in f.lower()))
print("tracked cdx_rar paths:", [f for f in files if "cdx_rar" in f])
print("tracked boe003 paths:", [f for f in files if "boe003" in f])
print("tracked .env.example-ish:", [f for f in files if "env.example" in f.lower() or f.endswith(".env.sample")])
print("tracked .gitattributes:", [f for f in files if f == ".gitattributes"])
print("tracked memory/warm_state.json:", [f for f in files if f == "memory/warm_state.json"])
print("tracked gps_ledger:", [f for f in files if "gps_ledger" in f])
print("tracked paths with 'season':", [f for f in files if "season" in f.lower()][:25])
print("tracked paths with 'gwap':", [f for f in files if "gwap" in f.lower()][:25])
print("memory/rib/*.md count:", len(glob.glob("memory/rib/*.md")))
print("memory/rib RIB_* count:", len(glob.glob("memory/rib/RIB_*.md")))
print("corpus/steal/*.md count:", len(glob.glob("corpus/steal/*.md")))

print("=" * 70)
print("CHECK-03 .env history and ignore rule")
r = subprocess.run(["git", "log", "--all", "--oneline", "--", ".env"], capture_output=True,
                   text=True, creationflags=CREATE_NO_WINDOW, encoding="utf-8", errors="replace")
print("commits touching .env across --all:", len(r.stdout.splitlines()))
i = subprocess.run(["git", "check-ignore", "-v", ".env"], capture_output=True,
                   text=True, creationflags=CREATE_NO_WINDOW, encoding="utf-8", errors="replace")
print("check-ignore -v .env:", i.stdout.strip(), "rc=", i.returncode)
if os.path.exists(".gitignore"):
    lines = open(".gitignore", encoding="utf-8", errors="replace").read().splitlines()
    print(".gitignore line 272:", repr(lines[271]) if len(lines) >= 272 else "FILE SHORTER THAN 272 LINES (" + str(len(lines)) + ")")

print("=" * 70)
print("CHECK-04 cdx_rar.json line 616 + boe003.html line 257 (MASKED, values never printed)")
cdx = [f for f in files if "cdx_rar" in f]
for p in cdx:
    if os.path.exists(p):
        ln = open(p, encoding="utf-8", errors="replace").read().splitlines()
        print(p, "total lines:", len(ln))
        if len(ln) >= 616:
            l616 = ln[615]
            print("  line616 len:", len(l616),
                  "secretish:", bool(re.search(r"(client_secret|AIza|GOCSPX|secret|token|oauth)", l616, re.I)))
            print("  masked head:", mask(l616[:140]))
boe = [f for f in files if "boe003" in f]
for p in boe:
    if os.path.exists(p):
        ln = open(p, encoding="utf-8", errors="replace").read().splitlines()
        print(p, "total lines:", len(ln))
        if len(ln) >= 257:
            l257 = ln[256]
            print("  line257 len:", len(l257),
                  "pk_live_present:", "pk_live" in l257,
                  "stripeish:", bool(re.search(r"(pk_live|sk_live|stripe)", l257, re.I)))
            print("  masked head:", mask(l257[:140]))
mim = [f for f in files if f.endswith(".mimosa")]
if mim:
    p0 = mim[0]
    head = open(p0, encoding="utf-8", errors="replace").readline()
    print("first .mimosa:", p0, "head masked:", mask(head[:80]))

print("=" * 70)
print("CHECK-05 mag/route_chat.py lines 40-75")
src = open("mag/route_chat.py", encoding="utf-8", errors="replace").read().splitlines()
for n in range(39, min(75, len(src))):
    print(str(n + 1).rjust(4), src[n])
print("route_chat total lines:", len(src))
print("operator-ish lines in route_chat.py:")
for n, l in enumerate(src, 1):
    if re.search(r"operator|owner|seat", l, re.I):
        print(str(n).rjust(4), l.strip())

print("=" * 70)
print("CHECK-06 memory/runs/route_chat/usage.jsonl field census (all rows, untruncated)")
RC = "memory/runs/route_chat/usage.jsonl"
if os.path.exists(RC):
    keys = set()
    n = ok = bad = cost_rows = op_rows = 0
    first_raw = None
    for l in open(RC, encoding="utf-8", errors="replace"):
        l = l.strip()
        if not l:
            continue
        r = json.loads(l)
        n += 1
        keys |= set(r.keys())
        if r.get("ok") is True:
            ok += 1
        elif r.get("ok") is False:
            bad += 1
        if any("cost" in k.lower() for k in r):
            cost_rows += 1
        if any(("operator" in k.lower()) or ("owner" in k.lower()) or k in ("id", "seat", "session_id") for k in r):
            op_rows += 1
        if first_raw is None:
            first_raw = l
    print("rows:", n, "ok_true:", ok, "ok_false:", bad)
    print("rows with a cost field:", cost_rows)
    print("rows with operator/owner/id/seat/session_id field:", op_rows)
    print("union of all keys across ALL rows:", sorted(keys))
    print("first row raw:", first_raw)
else:
    print("MISSING:", RC)

print("=" * 70)
print("CHECK-07 tools/gps_mcp/gps_ledger.db3: tracked size + schema (operator column census)")
gp = "tools/gps_mcp/gps_ledger.db3"
if os.path.exists(gp):
    print("size bytes:", os.path.getsize(gp))
    con = sqlite3.connect("file:" + gp.replace("\\", "/") + "?mode=ro", uri=True)
    for name, sql in con.execute("select name, sql from sqlite_master where sql is not null"):
        if sql.startswith("CREATE TABLE"):
            print("TABLE", name)
            cols = [r[1] for r in con.execute("pragma table_info(" + name + ")")]
            print("  cols:", cols)
            print("  operator-ish cols:", [c for c in cols if re.search(r"oper|owner|seat|user|party", c, re.I)])
            cnt = con.execute("select count(*) from " + name).fetchone()[0]
            print("  rows:", cnt)
    con.close()
else:
    print("MISSING:", gp)

print("=" * 70)
print("CHECK-08 D7 receipt: haiku 10-fail -> 0.030")
D7 = "watch/inbox/D7_PHEROMONE_METABOLISM_20261005.md"
if os.path.exists(D7):
    for n, l in enumerate(open(D7, encoding="utf-8", errors="replace"), 1):
        if re.search(r"0\.030|haiku|10[- ]fail|streak", l, re.I):
            print(str(n).rjust(4), l.strip()[:200])
else:
    print("MISSING:", D7)

print("=" * 70)
print("CHECK-09 mag/rib_bus.py: claim/lock/owner census + lines 4 and 195")
rb = open("mag/rib_bus.py", encoding="utf-8", errors="replace").read().splitlines()
print("rib_bus.py total lines:", len(rb))
for n, l in enumerate(rb, 1):
    if re.search(r"claim|lock|owner|writer|lease|reserv|ticket", l, re.I):
        print(str(n).rjust(4), l.strip()[:180])
print("--- line 4:", rb[3].strip()[:180] if len(rb) >= 4 else "SHORT")
print("--- line 195:", rb[194].strip()[:180] if len(rb) >= 195 else "SHORT")

print("=" * 70)
print("CHECK-10 memory/runs/hermes_burn/usage.jsonl recomputed (all rows)")
HB = "memory/runs/hermes_burn/usage.jsonl"
if os.path.exists(HB):
    rows = []
    for l in open(HB, encoding="utf-8", errors="replace"):
        l = l.strip()
        if l:
            try:
                rows.append(json.loads(l))
            except Exception as e:
                pass
    print("rows:", len(rows), "unparseable skipped:", "see count below")
    if rows:
        print("row0 keys:", sorted(rows[0].keys()))
        cf = [k for k in rows[0] if "cost" in k.lower()]
        mf = [k for k in rows[0] if "model" in k.lower()]
        print("cost field candidates:", cf, "model field candidates:", mf)
        if cf:
            c = cf[0]
            tot = sum(float(r.get(c) or 0) for r in rows)
            print("TOTAL cost:", round(tot, 4))
            agg = defaultdict(lambda: [0, 0.0])
            for r in rows:
                m = r.get(mf[0]) if mf else "?"
                agg[m][0] += 1
                agg[m][1] += float(r.get(c) or 0)
            for m, (k, s) in sorted(agg.items(), key=lambda kv: -kv[1][1])[:12]:
                print("  ", m, "rows:", k, "cost:", round(s, 4))
else:
    print("MISSING:", HB)

print("=" * 70)
print("CHECK-11 memory/runs/ds_batches/delta_judge_results_v3.jsonl recomputed")
DJ = "memory/runs/ds_batches/delta_judge_results_v3.jsonl"
if os.path.exists(DJ):
    rows = []
    for l in open(DJ, encoding="utf-8", errors="replace"):
        l = l.strip()
        if l:
            try:
                rows.append(json.loads(l))
            except Exception:
                pass
    print("rows:", len(rows))
    if rows:
        print("row0 keys:", sorted(rows[0].keys()))
        cf = [k for k in rows[0] if "cost" in k.lower()]
        print("cost field candidates:", cf)
        if cf:
            c = cf[0]
            tot = sum(float(r.get(c) or 0) for r in rows)
            print("TOTAL cost:", round(tot, 6), "per ask:", round(tot / max(len(rows), 1), 6))
else:
    print("MISSING:", DJ)

print("=" * 70)
print("CHECK-12 key-material scan over the spore candidate set (MASKED counts only)")
patterns = {
    "sk-ant": r"sk-ant-[A-Za-z0-9_\-]{8,}",
    "sk-proj": r"sk-proj-[A-Za-z0-9_\-]{8,}",
    "openai-sk": r"sk-[A-Za-z0-9]{20,}",
    "google-AIza": r"AIza[A-Za-z0-9_\-]{20,}",
    "xai": r"xai-[A-Za-z0-9]{16,}",
    "stripe-pk_live": r"pk_live_[0-9A-Za-z]{16,}",
    "stripe-sk_live": r"sk_live_[0-9A-Za-z]{16,}",
    "github-ghp": r"ghp_[A-Za-z0-9]{20,}",
    "github-pat": r"github_pat_[A-Za-z0-9_]{20,}",
    "goczs": r"GOCSPX-[A-Za-z0-9_\-]{10,}",
    "aws-akia": r"AKIA[0-9A-Z]{16}",
    "postgres-conn": r"postgres(ql)?://[^\s\"']{10,}",
}
scan_set = (glob.glob("memory/rib/*.md")
            + ["configs/providers.yaml", "state/GENOME.md", "queue/STANDING_RAILS.md",
               "docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md",
               "watch/inbox/THE_FIRST_SEASON_story_20261003.md",
               "mag/route_chat.py", "mag/rib_bus.py", ".env.example"]
            + glob.glob("tools/gps_mcp/*.py")
            + glob.glob("tools/ds_workhorse*")
            + glob.glob("tools/arena_gwap*")
            + glob.glob("tools/secret_gate*"))
found_any = False
for p in scan_set:
    if not os.path.exists(p):
        continue
    try:
        txt = open(p, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print(p, "UNREADABLE:", e)
        continue
    for name, pat in patterns.items():
        ms = re.findall(pat, txt)
        if ms:
            found_any = True
            print("  ", p, "PATTERN", name, "count:", len(ms), "masked sample:", mask(ms[0], keep=6))
if not found_any:
    print("  (no key-material patterns found in any scanned file)")

print("=" * 70)
print("CHECK-13 .env vs .env.example: key NAMES only (values never read)")


def keynames(p):
    out = []
    if os.path.exists(p):
        for l in open(p, encoding="utf-8", errors="replace"):
            l = l.strip()
            if l and not l.startswith("#") and ("=" in l or ":" in l):
                out.append(re.split("[=:]", l, 1)[0].strip())
    return out


envk = keynames(".env")
exk = keynames(".env.example")
print(".env exists:", os.path.exists(".env"), "key count:", len(envk))
print(".env.example exists:", os.path.exists(".env.example"), "key count:", len(exk))
print("keys in .env MISSING from .env.example:", sorted(set(envk) - set(exk)))
print("example values that look non-placeholder (heuristic on names only): check below")
if os.path.exists(".env.example"):
    for l in open(".env.example", encoding="utf-8", errors="replace"):
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            k, v = l.split("=", 1)
            v = v.strip()
            realish = bool(v) and not re.search(r"(your|xxx|<|>|placeholder|change|example|\.\.\.)", v, re.I) and len(v) >= 12
            if realish:
                print("   SUSPECT real value in example:", k.strip(), "value masked:", mask(v, keep=4))

print("=" * 70)
print("CHECK-14 existing operator-identity concept in code (git grep, untruncated scoping)")
g = git("grep", "-in", "operator_id", "--", "mag", "tools", "configs", "queue", "state")
print("git grep -in operator_id hits:", len(g.splitlines()))
print(g[:2000])
g2 = git("grep", "-in", "MAG_OPERATOR", "--", "mag", "tools", "configs", "queue", "state")
print("git grep -in MAG_OPERATOR hits:", len(g2.splitlines()))
print(g2[:1000])

print("=" * 70)
print("CHECK-15 configs/providers.yaml structure (values masked)")
if os.path.exists("configs/providers.yaml"):
    for n, l in enumerate(open("configs/providers.yaml", encoding="utf-8", errors="replace"), 1):
        print(str(n).rjust(4), mask(l.rstrip()[:150]))
else:
    print("MISSING configs/providers.yaml")

print("=" * 70)
print("CHECK-16 hardcoded personal absolute paths in spore candidates ('foste' census)")
cand = (["mag/route_chat.py", "mag/rib_bus.py", "configs/providers.yaml"]
        + glob.glob("tools/gps_mcp/*.py") + glob.glob("tools/ds_workhorse*") + glob.glob("tools/arena_gwap*"))
for p in cand:
    if os.path.exists(p):
        txt = open(p, encoding="utf-8", errors="replace").read()
        hits = [n for n, l in enumerate(txt.splitlines(), 1) if "foste" in l.lower()]
        if hits:
            print("  ", p, "lines with absolute personal path:", hits[:10])

print("=" * 70)
print("CHECK-17 scheduled tasks touching the estate (schtasks census)")
r = subprocess.run(["schtasks", "/Query", "/FO", "CSV", "/NH"], capture_output=True,
                   text=True, creationflags=CREATE_NO_WINDOW, encoding="utf-8", errors="replace")
task_hits = []
for l in r.stdout.splitlines():
    if re.search(r"mag|arena|gwap|hermes|census|fts|improve|spore", l, re.I):
        task_hits.append(l.split(",")[0].strip('"'))
print("tasks matching estate names:", sorted(set(task_hits)))
print("total tasks enumerated:", len(r.stdout.splitlines()))

print("=" * 70)
print("CHECK-18 sibling mycelial-republic tree + CONSTITUTION pointers")
for cand_dir in ("../mycelial-republic", "../mycelial_republic", "../../mycelial-republic"):
    print(cand_dir, "isdir:", os.path.isdir(cand_dir))
for p in ("CONSTITUTION.md", "docs/CONSTITUTION.md"):
    print(p, "exists:", os.path.exists(p))

print("DONE")
