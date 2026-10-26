import sys, os, json, re, datetime, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def mt(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).isoformat()
    except Exception as e:
        return "ERR " + str(e)

print("=== JUDGE burnaudit: raw byte verification of both candidates' cited receipts ===")
print("machine now (start):", now())

# ---------- S1: BURN_WAVE_STATE.json ----------
SP = os.path.join(ROOT, "memory", "burns", "BURN_WAVE_STATE.json")
print("\n=== S1 BURN_WAVE_STATE.json ===")
print("mtime:", mt(SP))
try:
    with open(SP, encoding="utf-8") as f:
        raw = f.read()
    print("raw first 300 chars:", repr(raw[:300]))
    st = json.loads(raw)
    print("top keys:", sorted(st.keys()))
    print("born:", repr(st.get("born")))
    holds = st.get("holds", [])
    print("holds count:", len(holds))
    for i, h in enumerate(holds, 1):
        print("hold %d: %s" % (i, json.dumps(h, ensure_ascii=True)))
    print("laws verbatim:", json.dumps(st.get("laws"), ensure_ascii=True))
    disp = st.get("dispensed", [])
    lnd = st.get("landed", [])
    print("dispensed count:", len(disp), "landed count:", len(lnd))
    print("literal '[' junk entries in dispensed:", sum(1 for d in disp if d == "["))
    for num in ("B2-247", "B2-373"):
        print("%s in dispensed x%d" % (num, sum(1 for d in disp if d == num)))
    for num in ("B2-104", "B2-155", "B2-475", "B2-239", "B2-139", "B2-181", "B2-151", "B2-202", "B2-217", "B2-342"):
        print("%s: dispensed=%d landed=%d" % (num, sum(1 for d in disp if d == num), sum(1 for d in lnd if d == num)))
except Exception as e:
    print("STATE LOAD ERR:", repr(e))

# ---------- S2: LEDGER.jsonl ----------
LP = os.path.join(ROOT, "memory", "burns", "LEDGER.jsonl")
print("\n=== S2 LEDGER.jsonl ===")
print("mtime:", mt(LP))
rows = []
with open(LP, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        line = line.rstrip("\n")
        if line.strip():
            rows.append((i, line))
print("total nonempty rows:", len(rows))
byno = dict(rows)

def show_substr(sub, label, maxn=4, width=420):
    print("--- rows containing %s ---" % label)
    n = 0
    for i, l in rows:
        if sub in l:
            print("row %d: %s" % (i, l[:width]))
            n += 1
            if n >= maxn:
                break
    if n == 0:
        print("(none)")

for sub, lab in [
    ("b2-239-line-endings", "b2-239-line-endings"),
    ("b2-139-ask3-source-repair", "b2-139-ask3-source-repair"),
    ("b2-181-seed-mcp-server", "b2-181-seed-mcp-server"),
    ("B2-155-seed-paired-harness", "B2-155-seed-paired-harness"),
    ("b2-151-pid-survivor", "b2-151-pid-survivor"),
    ("B2-202", "B2-202"),
    ("B2-217", "B2-217"),
    ("B2-475-real-limits", "B2-475-real-limits"),
    ("b2-427-registry-append-only", "b2-427-registry-append-only"),
    ("b2-181-selffeed-renumber", "b2-181-selffeed-renumber"),
]:
    show_substr(sub, lab)

print("\n-- named rows by line number --")
for r in (260, 356, 499, 510, 518):
    print("row %d: %s" % (r, byno.get(r, "(missing)")[:650]))
print("last row: %d: %s" % (rows[-1][0], rows[-1][1][:400]))
print("last three rows:")
for i, l in rows[-3:]:
    print("row %d: %s" % (i, l[:300]))

l518 = byno.get(518, "")
m518 = re.search(r'"ts":\s*"([^"]+)"', l518)
print("\nrow 518 contains a ts field:", '"ts"' in l518, "| first ts value:", m518.group(1) if m518 else None)
print("row 518 first 90 chars:", l518[:90])

print("\nrows containing exact stamp 2026-09-27T00:08:53Z:", sum(1 for i, l in rows if '"2026-09-27T00:08:53Z"' in l))
print("rows lacking any ts field:", sum(1 for i, l in rows if not re.search(r'"ts"', l)))
print("rows with ts in 2026-09-27T0[2-7]:", sum(1 for i, l in rows if re.search(r'"ts": "2026-09-27T0[2-7]', l)))

print("\n-- ts of rows 455..end (file order) --")
for i, l in rows:
    if i >= 455:
        m = re.search(r'"ts": "([^"]+)"', l)
        slug = re.search(r'"slug": "([^"]+)"', l)
        print(i, m.group(1) if m else "(no ts)", "|", slug.group(1) if slug else "?")

# ---------- S3: trajectory steps.jsonl ----------
TP = os.path.join(ROOT, "memory", "trajectory", "steps.jsonl")
print("\n=== S3 memory/trajectory/steps.jsonl ===")
print("size bytes:", os.path.getsize(TP), "mtime:", mt(TP))
want = {22365, 22468, 22482, 22492, 22493, 22496, 22559, 22592}
appends = []
b104, b155, b475, width_hits = [], [], [], []
total_lines = 0
with open(TP, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        total_lines = i
        if i in want:
            print("\nline %d raw (first 900): %s" % (i, line.strip()[:900]))
        if "holds'].append" in line or 'holds"].append' in line:
            appends.append((i, line))
        if "B2-104" in line and '"2026-09-26' in line:
            b104.append((i, line))
        if "B2-155" in line and '"2026-09-26' in line:
            b155.append((i, line))
        if "B2-475" in line and '"2026-09-26' in line:
            b475.append((i, line))
        if re.search(r"width", line, re.I) and '"2026-09-26' in line:
            width_hits.append((i, line))
print("\ntotal lines in steps.jsonl:", total_lines)
print("\n-- all hold-append commands (envelope ts vs authored stamp) --")
print("count:", len(appends))
for i, line in appends:
    env = re.search(r'"ts": "([^"]+)"', line)
    stamp = re.search(r"append\(\{'ts': '([^']+)'", line) or re.search(r'append\(\{"ts": "([^"]+)"', line)
    print("append line %d envelope_first_ts=%s stamped=%s" % (i, env.group(1) if env else "?", stamp.group(1) if stamp else "?"))
    print("   cmd excerpt: %s" % line.strip()[:340])

def dump_hits(lst, label, cap, w):
    print("\n-- %s hits on 2026-09-26 (cap %d, total %d) --" % (label, cap, len(lst)))
    for i, line in lst[:cap]:
        print("line %d: %s" % (i, line.strip()[:w]))

dump_hits(b104, "B2-104", 12, 260)
dump_hits(b155, "B2-155", 12, 260)
dump_hits(b475, "B2-475", 12, 260)
dump_hits(width_hits, "width (case-insensitive)", 25, 260)

# ---------- S4: greps, scoped roots ----------
print("\n=== S4 GREPS (scoped: corpus/ 6.9GB and bulk of memory/ skipped, scope noted per grep) ===")
EXCL_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", "corpus", "trajectory"}

def walkgrep(base_rel, pattern, maxbytes=30 * 1024 * 1024, flags=0, filecap=20000):
    rx = re.compile(pattern, flags)
    hits = {}
    base = os.path.join(ROOT, base_rel) if not os.path.isabs(base_rel) else base_rel
    if not os.path.isdir(base):
        return {"(missing dir " + base_rel + ")": 0}
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in EXCL_DIRS]
        for fn in filenames:
            scanned += 1
            if scanned > filecap:
                hits["(FILECAP HIT at %d files, scan incomplete)" % filecap] = -2
                return hits
            p = os.path.join(dirpath, fn)
            try:
                rel = os.path.relpath(p, ROOT)
            except Exception:
                continue
            try:
                if os.path.getsize(p) > maxbytes:
                    hits[rel + " (too big, skipped)"] = -1
                    continue
                with open(p, encoding="utf-8", errors="replace") as f:
                    txt = f.read()
            except Exception:
                continue
            n = len(rx.findall(txt))
            if n:
                hits[rel] = n
    return hits

print("-- BURN_WAVE_STATE refs, roots: mag tools scripts githooks configs docs watch queue tests memory(minus trajectory) + AGENTS.md LOAD.md main.py --")
agg = {}
for rootname in ("mag", "tools", "scripts", "githooks", "configs", "docs", "watch", "queue", "tests", "memory"):
    for k, v in sorted(walkgrep(rootname, "BURN_WAVE_STATE").items()):
        agg[k] = v
for fname in ("AGENTS.md", "LOAD.md", "main.py", "CONSTITUTION.md"):
    p = os.path.join(ROOT, fname)
    if os.path.exists(p):
        t = open(p, encoding="utf-8", errors="replace").read()
        n = t.count("BURN_WAVE_STATE")
        if n:
            agg[fname] = n
for k in sorted(agg):
    print(k, agg[k])

print("\n-- width-24 / width 24 / 24-wide, roots: watch queue logs docs memory/burns AGENTS.md --")
for rootname in ("watch", "queue", "logs", "docs", os.path.join("memory", "burns")):
    h = walkgrep(rootname, r"width-24|width 24|24-wide", flags=re.I)
    for k, v in sorted(h.items()):
        print("%s :: %s %d" % (rootname, k, v))
agt = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8", errors="replace").read()
print("AGENTS.md width-24/width 24/24-wide hits:", len(re.findall(r"width-24|width 24|24-wide", agt, re.I)))
print("AGENTS.md '50 workflow children' hits:", agt.count("50 workflow children"))

print("\n-- 2026-09-27T0[2-7], roots: logs memory/burns memory/trajectory/steps.jsonl watch/inbox queue --")
for rootname in ("logs", os.path.join("memory", "burns"), "watch/inbox", "queue"):
    h = walkgrep(rootname, r"2026-09-27T0[2-7]")
    for k, v in sorted(h.items()):
        p = os.path.join(ROOT, k)
        snip = ""
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                for line in f:
                    mm = re.search(r".{0,50}2026-09-27T0[2-7].{0,60}", line)
                    if mm:
                        snip = mm.group(0)
                        break
        except Exception:
            pass
        print("%s :: %d hits | first: %s" % (k, v, snip))
ntj = 0
with open(TP, encoding="utf-8", errors="replace") as f:
    for line in f:
        if re.search(r"2026-09-27T0[2-7]", line):
            ntj += 1
print("memory/trajectory/steps.jsonl :: %d echo lines" % ntj)

print("\n-- '8 surfaced', roots: watch queue logs docs memory/burns --")
for rootname in ("watch", "queue", "logs", "docs", os.path.join("memory", "burns")):
    for k, v in sorted(walkgrep(rootname, r"8 surfaced").items()):
        print("%s :: %s %d" % (rootname, k, v))

# ---------- S5: QUEUE ----------
print("\n=== S5 queue ===")
for path in ("queue/todo.md", "queue/QUEUE.md"):
    p = os.path.join(ROOT, path.replace("/", os.sep))
    if os.path.exists(p):
        print("FILE:", path, "mtime:", mt(p))
        with open(p, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        print("total lines:", len(lines))
        if len(lines) >= 533:
            print("line 533:", lines[532].rstrip()[:300])
        for n, l in enumerate(lines, 1):
            if "B2-155" in l or "B2-475" in l or ("B2-104" in l and "CLAIM" in l):
                print("line %d: %s" % (n, l.rstrip()[:230]))

# ---------- S6: RACTOR_PANEL ----------
RP = os.path.join(ROOT, "watch", "inbox", "RACTOR_PANEL_20260926.md")
print("\n=== S6 watch/inbox/RACTOR_PANEL_20260926.md ===")
print("mtime:", mt(RP))
with open(RP, encoding="utf-8", errors="replace") as f:
    for n, l in enumerate(f, 1):
        if n <= 15:
            print("line %d: %s" % (n, l.rstrip()[:260]))

# ---------- S7: B2_442_out_waves.json ----------
WP = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926", "B2_442_out_waves.json")
print("\n=== S7 B2_442_out_waves.json ===")
print("mtime:", mt(WP))
try:
    wj = json.load(open(WP, encoding="utf-8"))
    if isinstance(wj, dict):
        print("keys:", sorted(wj.keys()))
        for k in ("last_event_ts", "absorbed_retries"):
            if k in wj:
                print(k, "=", repr(wj[k]))
except Exception as e:
    print("ERR", repr(e))

# ---------- S8: receipts mtimes + 1302 content ----------
print("\n=== S8 receipts ===")
BW = os.path.join(ROOT, "watch", "inbox", "burn_wave_20260926")
for name in (
    "B2_427_registry_append_only_20260926.md",
    "B2_475_real_limits_20260926.md",
    "B2_155_seed_paired_harness_20260926.md",
    "B2_151_pid_survivor_20260926.md",
):
    p = os.path.join(BW, name)
    print(name, "mtime:", mt(p) if os.path.exists(p) else "(missing)", "size:", os.path.getsize(p) if os.path.exists(p) else "-")
p475 = os.path.join(BW, "B2_475_real_limits_20260926.md")
if os.path.exists(p475):
    with open(p475, encoding="utf-8", errors="replace") as f:
        lines475 = f.readlines()
    print("B2_475 receipt line 16 verbatim:", repr(lines475[15].rstrip()) if len(lines475) >= 16 else "(short file)")
print("\n-- 1302 mentions per casualty receipt --")
pat = re.compile(r"B2_(239|139|155|181|151|202|217|475)_")
for fn in sorted(os.listdir(BW)):
    if pat.search(fn):
        p = os.path.join(BW, fn)
        if os.path.getsize(p) > 5 * 1024 * 1024:
            continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        n = txt.count("1302")
        m = re.search(r".{0,60}1302.{0,80}", txt)
        print("%s: 1302 count=%d | first: %s" % (fn, n, m.group(0) if m else ""))

# ---------- S9: git ----------
print("\n=== S9 git ===")
r1 = subprocess.run(["git", "-C", ROOT, "status", "--porcelain", "--", "memory/burns"], capture_output=True, text=True)
print("git status --porcelain -- memory/burns exit", r1.returncode)
print(r1.stdout.strip() or "(clean)")
r2 = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%H %cI", "6d417abd5"], capture_output=True, text=True)
print("git log -1 6d417abd5:", r2.stdout.strip(), "exit", r2.returncode)

# ---------- S10: live-writer logs ----------
print("\n=== S10 live writer files: mtime + tail ===")
for rel in (
    "logs/lane_scheduler.log", "logs/kpi.jsonl", "logs/provider_usage.jsonl",
    "logs/docker_ops.jsonl", "logs/memory_events.jsonl", "logs/failure_kb.jsonl",
    "memory/runs/swarm_health/trail.jsonl", "memory/runs/governor_autorun_trail.jsonl",
    "logs/supervisor.jsonl",
):
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(p):
        print(rel, "(missing)")
        continue
    try:
        with open(p, "rb") as f:
            f.seek(max(0, os.path.getsize(p) - 400), 0)
            tail = f.read().decode("utf-8", errors="replace").strip().splitlines()
        print("%s | mtime=%s | tail: %s" % (rel, mt(p), tail[-1][:180] if tail else "(empty)"))
    except Exception as e:
        print(rel, "ERR", repr(e))

# ---------- S11: fold + stego receipts ----------
print("\n=== S11 misc quotes ===")
FP = os.path.join(ROOT, "watch", "inbox", "BURN_b2-wave-fold_20260926_e.md")
if os.path.exists(FP):
    t = open(FP, encoding="utf-8", errors="replace").read()
    print("BURN_b2-wave-fold_20260926_e.md 'nothing wired live' hits:", t.count("nothing wired live"))
    m = re.search(r".{0,80}nothing wired live.{0,80}", t)
    if m:
        print("snippet:", m.group(0))
else:
    print("fold receipt missing")
GP = os.path.join(ROOT, "watch", "inbox", "BURN_stego-canon-pipeline_20260926_g.md")
if os.path.exists(GP):
    with open(GP, encoding="utf-8", errors="replace") as f:
        glines = f.readlines()
    print("stego receipt line 13:", glines[12].rstrip()[:300] if len(glines) >= 13 else "(short)")
    print("stego 07:07:19 hits:", sum(1 for l in glines if "07:07:19" in l))
else:
    print("stego receipt missing")

print("\nmachine now (end):", now())
print("=== END JUDGE SCRIPT ===")
