# cross-gap lane: verify 15 claims from the ractor corpus (the 7 ractor50 chapters,
# MCP_PARITY_R20, vonnegut-final, lyric-workover) against estate bytes.
# Run: .venv/Scripts/python.exe watch/inbox/gala_20260925/ouroboros/lanes/cross_gap_check.py
# Moment: 2026-10-02 (post-deadline probe for the selfsteal G1-G3 forecasts).
# House laws: ascii only, no em/en dashes, every count names instrument + moment.
import json
import hashlib
import os
import re
import subprocess
import sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
GALA = os.path.join(ROOT, "watch", "inbox", "gala_20260925")
R50 = os.path.join(ROOT, "watch", "inbox", "ractor50")
RESULTS = []

def head(label):
    print("")
    print("=" * 78)
    print(label)
    print("=" * 78)

def done(n, claim, verdict, detail):
    RESULTS.append((n, verdict))
    print("CLAIM %s: %s" % (n, claim))
    print("  VERDICT: %s" % verdict)
    print("  %s" % detail)

# CHECK 1: accuracy.md header census "213 gala lane JSONs under
# watch/inbox/gala_20260925/*/lanes/" with parenthesized per-dir figures
# (48h-synthesis 16, afterparty 197, ball-20260929 26, ball3-suite-green 8,
# ball4-luncheon-follow 24, gala-rung0 4, w1 22, w2 26, w3 65, wave5-repair 50).
head("CHECK 1: accuracy.md header lane-JSON census (claimed 213 + per-dir figures)")
lanes_root = GALA
per_dir = {}
total_json = 0
for d in sorted(os.listdir(lanes_root)):
    lanes_dir = os.path.join(lanes_root, d, "lanes")
    if not os.path.isdir(lanes_dir):
        continue
    n = len([f for f in os.listdir(lanes_dir) if f.endswith(".json")])
    per_dir[d] = n
    total_json += n
paren_sum = 16 + 197 + 26 + 8 + 24 + 4 + 22 + 26 + 65 + 50
print("per-dir .json counts now: %s" % json.dumps(per_dir, sort_keys=True))
print("TOTAL .json under */lanes/ now: %d" % total_json)
print("sum of accuracy.md's own parenthesized per-dir figures: %d" % paren_sum)
print("accuracy.md header claim: 213")
if paren_sum != 213:
    print("INTERNAL-ARITHMETIC DEFECT: accuracy.md's own parenthesized figures sum to")
    print("  %d, not the 213 its header claims (both from the same 09-30 moment)." % paren_sum)
else:
    print("arithmetic consistent at claim moment")

# CHECK 2: accuracy.md supporting observation: REGISTRY.jsonl 45 rows, PASS 34 / FAIL 11
head("CHECK 2: memory/workflows/REGISTRY.jsonl census (accuracy.md claimed 45 rows, PASS 34 / FAIL 11)")
reg = os.path.join(ROOT, "memory", "workflows", "REGISTRY.jsonl")
rows = [l for l in open(reg, encoding="utf-8", errors="replace").read().splitlines() if l.strip()]
pass_n = fail_n = other_n = 0
for l in rows:
    try:
        v = json.loads(l).get("verdict")
    except Exception:
        v = "UNPARSEABLE"
    if v == "PASS":
        pass_n += 1
    elif v == "FAIL":
        fail_n += 1
    else:
        other_n += 1
print("rows now: %d (PASS %d / FAIL %d / other %d)" % (len(rows), pass_n, fail_n, other_n))
print("accuracy.md moment 2026-09-30 claimed 45 rows PASS 34 / FAIL 11; operations.md")
print("same day claimed 40 rows with 4 seatlaw_* Temp rows; both moment-typed.")

# CHECK 3: accuracy.md incident 10: w4-20.md and w4-singularity.md identical,
# sha256 f873a43aaf1d241f..., 18,212 bytes
head("CHECK 3: flash50 double-landing (accuracy.md incident 10)")
f1 = os.path.join(ROOT, "watch", "inbox", "burn_reset_20260927", "flash50", "w4-20.md")
f2 = os.path.join(ROOT, "watch", "inbox", "burn_reset_20260927", "flash50", "w4-singularity.md")
h1 = hashlib.sha256(open(f1, "rb").read()).hexdigest()
h2 = hashlib.sha256(open(f2, "rb").read()).hexdigest()
s1 = os.path.getsize(f1)
s2 = os.path.getsize(f2)
print("w4-20.md          sha256=%s bytes=%d" % (h1, s1))
print("w4-singularity.md sha256=%s bytes=%d" % (h2, s2))
print("identical: %s (claimed sha prefix f873a43aaf1d241f, 18,212 bytes each)" % (h1 == h2))

# CHECK 4: communication.md breakage 1: estate-wide 03:00Z census, exactly three
# in-record citations + a fourth echo (W3S_ORAL_DEDUPE.md)
head("CHECK 4: 03:00Z citation census (communication.md claimed exactly 3 citations + 1 echo)")
targets = [
    "AGENTS.md",
    os.path.join("memory", "rib", "RIB_DRIVING_LADDER_20260928.md"),
    os.path.join("watch", "inbox", "48h_synth", "laws.md"),
    os.path.join("watch", "inbox", "operator_model", "W3S_ORAL_DEDUPE.md"),
]
for t in targets:
    p = os.path.join(ROOT, t)
    if not os.path.exists(p):
        print("%s: MISSING" % t)
        continue
    txt = open(p, encoding="utf-8", errors="replace").read()
    n = txt.count("03:00Z")
    lines = [i + 1 for i, l in enumerate(txt.splitlines()) if "03:00Z" in l]
    print("%s: %d hit(s) at line(s) %s" % (t, n, lines))
print("communication.md moment 2026-09-30: 3 citations + 1 echo; recount above is the")
print("moment-typed census (growth since = later citations, not a contradiction).")

# CHECK 5: communication.md CHECK 5 / w4-09: attention_flag.txt zero readers,
# only mag/act.py writes it
head("CHECK 5: attention_flag.txt reader census (claimed zero readers, one writer)")
hits = []
for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "mag")):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__",)]
    for fn in filenames:
        if fn.endswith(".py"):
            p = os.path.join(dirpath, fn)
            try:
                t = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if "attention_flag" in t:
                hits.append(os.path.relpath(p, ROOT))
for sub in ("tools", "scripts", "dashboard"):
    full = os.path.join(ROOT, sub)
    if not os.path.isdir(full):
        continue
    for dirpath, dirnames, filenames in os.walk(full):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "node_modules")]
        for fn in filenames:
            if fn.endswith((".py", ".ps1", ".mjs", ".js")):
                p = os.path.join(dirpath, fn)
                try:
                    t = open(p, encoding="utf-8", errors="replace").read()
                except Exception:
                    continue
                if "attention_flag" in t:
                    hits.append(os.path.relpath(p, ROOT))
for fn in ("main.py",):
    p = os.path.join(ROOT, fn)
    if os.path.exists(p) and "attention_flag" in open(p, encoding="utf-8", errors="replace").read():
        hits.append(fn)
print("files under mag/ tools/ scripts/ dashboard/ main.py mentioning attention_flag:")
for h in sorted(set(hits)):
    print("  %s" % h)
act = os.path.join(ROOT, "mag", "act.py")
act_txt = open(act, encoding="utf-8", errors="replace").read()
print("mag/act.py present: %s; mentions: %d" % (os.path.exists(act), act_txt.count("attention_flag")))

# CHECK 6: logic.md check 1: workflow_gate scenario suite 7 cards, exit 0
head("CHECK 6: workflow_gate scenario suite re-run (logic.md claimed 7 cards G1-G7 exit 0)")
venv_py = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
r = subprocess.run([venv_py, "tools/workflow_gate.py", "check", "--scenarios",
                    "configs/workflow_gate_scenarios"],
                   cwd=ROOT, capture_output=True, text=True, timeout=300)
print("exit=%d" % r.returncode)
print(r.stdout[-3000:])
if r.stderr.strip():
    print("stderr tail: %s" % r.stderr[-800:])

# CHECK 7: logic.md check 4: 'uncollapsed|never-disproven' ZERO hits in
# corpus/steal + memory/corpus (the propagation finding)
head("CHECK 7: uncollapsed/never-disproven propagation census (logic.md claimed ZERO hits)")
pat = re.compile(r"uncollapsed|never-disproven", re.IGNORECASE)
for sub in ("corpus/steal", "memory/corpus"):
    full = os.path.join(ROOT, sub.replace("/", os.sep))
    n_files = n_hits = 0
    hit_files = []
    for dirpath, dirnames, filenames in os.walk(full):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "node_modules", ".git")]
        for fn in filenames:
            if fn.endswith((".md", ".txt", ".rst", ".json", ".jsonl", ".py", ".ts")):
                p = os.path.join(dirpath, fn)
                try:
                    t = open(p, encoding="utf-8", errors="replace").read()
                except Exception:
                    continue
                k = len(pat.findall(t))
                if k:
                    n_files += 1
                    n_hits += k
                    hit_files.append("%s (%d)" % (os.path.relpath(p, ROOT), k))
    print("%s: %d hit file(s), %d total hit(s)%s" % (
        sub, n_files, n_hits, (" -> " + "; ".join(hit_files[:10])) if hit_files else ""))

# CHECK 8: mcp.md section 2: state/mcp_pins.jsonl 397 records
head("CHECK 8: state/mcp_pins.jsonl census (mcp.md claimed 397 records 2026-10-01)")
pins = os.path.join(ROOT, "state", "mcp_pins.jsonl")
plines = [l for l in open(pins, encoding="utf-8", errors="replace").read().splitlines() if l.strip()]
print("records now: %d (mcp.md moment 2026-10-01 claimed 397; append-only growth expected)" % len(plines))

# CHECK 9: MCP_PARITY R2.0: tools/mcp_parity.py (claimed 400 lines) +
# tests/test_mcp_parity.py (claimed 16 tests, all pass)
head("CHECK 9: MCP-2 parity instrument landed (MCP_PARITY_R20 claims 400 lines / 16 tests)")
mp = os.path.join(ROOT, "tools", "mcp_parity.py")
tp = os.path.join(ROOT, "tests", "test_mcp_parity.py")
print("tools/mcp_parity.py exists: %s, lines: %s" % (
    os.path.exists(mp),
    len(open(mp, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(mp) else "n/a"))
print("tests/test_mcp_parity.py exists: %s" % os.path.exists(tp))
if os.path.exists(tp):
    r = subprocess.run([venv_py, "-m", "pytest", "tests/test_mcp_parity.py", "-q",
                        "-p", "no:cacheprovider", "--collect-only"],
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    tail = [l for l in r.stdout.splitlines() if l.strip()]
    print("collect-only exit=%d, tail: %s" % (r.returncode, tail[-1] if tail else "(no output)"))

# CHECK 10: skills.md section 0: wc -c .agents/skills/*/SKILL.md = 65,826 over 20 files
head("CHECK 10: skills census re-run (skills.md 2026-09-30 claimed 65,826 bytes over 20 files)")
sk = os.path.join(ROOT, ".agents", "skills")
files = []
for d in sorted(os.listdir(sk)):
    p = os.path.join(sk, d, "SKILL.md")
    if os.path.isfile(p):
        files.append((d, os.path.getsize(p)))
total = sum(s for _, s in files)
print("files now: %d, total bytes now: %d" % (len(files), total))
print("delta vs skills.md moment: %+d bytes, %+d files" % (total - 65826, len(files) - 20))

# CHECK 11: skills.md 2.2 + GAP_REGISTER rank 2: elder inbox.jsonl 0 bytes mtime Sep 4;
# salvage lens owed before ~10-02
head("CHECK 11: elder-lens salvage state (inbox.jsonl claimed 0 bytes, mtime Sep 4)")
ei = os.path.join(ROOT, "queue", "lanes", "elder", "inbox.jsonl")
st = os.stat(ei)
print("queue/lanes/elder/inbox.jsonl: size=%d bytes, mtime=%s" % (
    st.st_size,
    __import__("datetime").datetime.utcfromtimestamp(st.st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ")))
print("GAP_REGISTER rank 2 + skills.md 2.2 owed ONE lens banked before ~10-02.")

# CHECK 12: selfsteal.md forecasts G1+G2+G3, past their 2026-10-01T23:59Z deadline
head("CHECK 12: selfsteal forecasts G1/G2/G3 evaluated at 2026-10-02 (deadline was 10-01T23:59Z)")
chapters = ["accuracy.md", "operations.md", "skills.md", "communication.md",
            "mcp.md", "selfsteal.md", "logic.md"]
g1 = all(os.path.isfile(os.path.join(R50, c)) for c in chapters)
print("G1 all 7 chapter paths exist: %s" % g1)
for c in chapters:
    print("  %-18s %d bytes" % (c, os.path.getsize(os.path.join(R50, c))))
receipt = os.path.join(GALA, "ractor50_RECEIPT.md")
print("G2 ractor50_RECEIPT.md exists: %s" % os.path.isfile(receipt))
lane_dir = os.path.join(GALA, "ractor50", "lanes")
lane_jsons = [f for f in os.listdir(lane_dir) if f.endswith(".json") and not f.endswith(".checks.json")]
print("G2 fresh lane JSON count: %d (receipt header claims lanes_json_count 7)" % len(lane_jsons))
rows_sum = 0
checks_sum = 0
divs = {"A": 0, "B": 0}
for lj in lane_jsons:
    try:
        j = json.loads(open(os.path.join(lane_dir, lj), encoding="utf-8", errors="replace").read())
    except Exception as e:
        print("  %s UNPARSEABLE: %s" % (lj, e))
        continue
    rows_sum += len(j.get("rows") or [])
    checks_sum += len(j.get("checks") or [])
    d = j.get("division")
    if d in divs:
        divs[d] += 1
print("G2 fresh sums over the 7 lane JSONs: mined rows=%d (receipt claims 30)," % rows_sum)
print("   byte checks cited=%d (receipt claims 37), by_division=%s (receipt claims B6/A1)" % (checks_sum, divs))
rtxt = open(receipt, encoding="utf-8", errors="replace").read() if os.path.isfile(receipt) else ""
em = len(re.findall(u"[\u2014\u2013]", rtxt))
print("G3 em/en-dash count in ractor50_RECEIPT.md: %d (forecast demanded 0)" % em)

# CHECK 13: vonnegut-final + lyric-workover receipts: LINKS ledger claims
head("CHECK 13: memory/corpus/LINKS.jsonl census (vonnegut receipt claimed 235 lines;")
print("      lyric receipt claimed 231 -> 234 with 3 lyric rows; ractor50 filing claimed 7 rows)")
lk = os.path.join(ROOT, "memory", "corpus", "LINKS.jsonl")
llines = [l for l in open(lk, encoding="utf-8", errors="replace").read().splitlines() if l.strip()]
vonn = sum(1 for l in llines if "GALA-vonnegut-final-vonnegut" in l)
lyric = sum(1 for l in llines if "GALA-lyric-workover" in l)
r50rows = sum(1 for l in llines if "slug=ractor50" in l or '"ractor50"' in l)
print("ledger lines now: %d" % len(llines))
print("GALA-vonnegut-final rows: %d (vonnegut receipt claims exactly 1 at ledger 235)" % vonn)
print("GALA-lyric-workover rows: %d (lyric receipt claims 3, ledger 231->234)" % lyric)
print("ractor50 rows: %d (ractor50 filing claims 7, ledger 210->217)" % r50rows)

# CHECK 14: lyric-workover review defect (b): lyric-archaeology.md:216 header says
# "In-folder tracks (20):" while listing 22 titles
head("CHECK 14: lyric-archaeology.md:216 stale hand-written count (review defect b)")
la = os.path.join(ROOT, "watch", "inbox", "music", "lyric-archaeology.md")
la_lines = open(la, encoding="utf-8", errors="replace").read().splitlines()
line216 = la_lines[215] if len(la_lines) >= 216 else "(file shorter than 216 lines)"
print("line 216: %s" % line216)
m = re.search(r"In-folder tracks \((\d+)\)", "\n".join(la_lines))
if m:
    declared = int(m.group(1))
    start = None
    for i, l in enumerate(la_lines):
        if "In-folder tracks (%d)" % declared in l:
            start = i + 1
            break
    count = 0
    if start is not None:
        for l in la_lines[start:]:
            if re.match(r"^\s*\d+\.\s", l):
                count += 1
            elif count and not l.strip():
                break
    print("declared count: %d; numbered titles actually listed under the header: %d" % (declared, count))
    print("defect status: %s" % ("STILL LIVE (declared != listed)" if declared != count else "FIXED"))

# CHECK 15: operations.md failure 4 owed build: provider_error_tally.py --dwf-run
head("CHECK 15: provider_error_tally.py --dwf-run attribution mode (claimed 0 hits, owed)")
pet = os.path.join(ROOT, "tools", "provider_error_tally.py")
if os.path.exists(pet):
    t = open(pet, encoding="utf-8", errors="replace").read()
    print("tools/provider_error_tally.py exists, dwf-run hits: %d" % t.count("dwf-run"))
    print("dwf_run hits: %d" % t.count("dwf_run"))
else:
    print("tools/provider_error_tally.py MISSING")

print("")
print("=" * 78)
print("SUMMARY: %d checks executed, verdicts:" % len(RESULTS))
for n, v in RESULTS:
    print("  CHECK %s: %s" % (n, v))
print("exit 0 (execution complete; verdicts are per-claim above)")
