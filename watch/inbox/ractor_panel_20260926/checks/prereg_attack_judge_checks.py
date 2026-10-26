"""Judge checks for ractor card prereg-attack. Read-only; prints labeled sections."""
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
RUN = ROOT / "memory" / "runs" / "interference_replication_20260925"


def sec(t):
    print("\n" + "=" * 10 + " " + t + " " + "=" * 10)


def jload(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


# A. armC_budget50_complete.jsonl census (candidate one claim 3)
sec("A armC_budget50_complete.jsonl census")
rows = jload(RUN / "armC_budget50_complete.jsonl")
print("row count:", len(rows))
print("any row has a token field:", any(("token" in r) or ("tokens" in r) for r in rows))
print("sample problem-row fields:", sorted(rows[0].keys()))
print("summary row verbatim:", json.dumps(rows[-1]))

# B. armA census (candidate one contrast claim)
sec("B armA_gemma2b_cot.jsonl census")
rowsA = jload(RUN / "armA_gemma2b_cot.jsonl")
toks = [r.get("tokens", 0) for r in rowsA]
print("row count:", len(rowsA), "total tokens:", sum(toks), "avg:", round(sum(toks) / len(toks), 1))

# C. eval_count appearance across the run dir (candidate one claim: only run_armA.py:50)
sec("C eval_count grep across run dir py files")
for f in sorted(RUN.glob("*.py")):
    hits = [(i + 1, l.strip()) for i, l in enumerate(f.read_text(encoding="utf-8").splitlines())
            if "eval_count" in l]
    if hits:
        print(f.name, hits)

# D. receipt greps: tok and parse (candidate one claims 4 + amendment-1 clause-2 fold)
sec("D receipt greps (tok, parse)")
for rel in ["watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md",
            "watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md"]:
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    tok = [(i + 1, l.strip()) for i, l in enumerate(lines) if re.search(r"tok", l, re.I)]
    par = [(i + 1, l.strip()) for i, l in enumerate(lines) if re.search(r"parse", l, re.I)]
    print(rel)
    print("  tok hits:", tok if tok else "NONE")
    print("  parse hits:", par if par else "NONE")

# E. ALREADY-COVERED kill test for candidate one: any filing that mentions Arm C
#    AND tokens/eval_count (which would either refute the break or cover it)
sec("E already-covered scan: Arm C/armC co-mentioned with token/eval_count")
bases = [ROOT / "watch", ROOT / "queue", ROOT / "memory" / "runs" / "interference_replication_20260925"]
co = 0
for base in bases:
    if not base.exists():
        continue
    for f in base.rglob("*"):
        if f.suffix.lower() not in (".md", ".txt", ".json", ".jsonl") or not f.is_file():
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        has_armc = any(re.search(r"arm\s*c\b|armc", l, re.I) for l in lines)
        if not has_armc:
            continue
        hits = [(i + 1, l.strip()) for i, l in enumerate(lines)
                if re.search(r"token|eval_count", l, re.I)]
        if hits:
            co += 1
            print("FILE:", f.relative_to(ROOT))
            for n, l in hits[:12]:
                print(f"  :{n} {l[:200]}")
if co == 0:
    print("NO file mentioning Arm C/armC also mentions token or eval_count")

# F. provider_usage gemma:2b meter (candidate one claim 5: no recovery rows)
sec("F provider_usage.jsonl gemma rows")
pu = ROOT / "logs" / "provider_usage.jsonl"
gem = []
if pu.exists():
    for l in pu.read_text(encoding="utf-8", errors="replace").splitlines():
        if not l.strip():
            continue
        try:
            r = json.loads(l)
        except Exception:
            continue
        if "gemma" in str(r.get("model", "")).lower():
            gem.append(r)
print("gemma rows total:", len(gem))
if gem:
    print("sample row:", json.dumps(gem[-1])[:300])
    keys = list(gem[-1].keys())
    tkey = next((k for k in keys if "ts" in k.lower() or "time" in k.lower() or "date" in k.lower()), None)
    if tkey:
        dates = sorted(str(r.get(tkey, ""))[:10] for r in gem)
        print("ts field:", tkey, "| first:", dates[0], "| last:", dates[-1])
        on = [d for d in dates if d in ("2026-09-25", "2026-09-26")]
        print("rows dated 2026-09-25/26:", len(on))

# G. run dir listing (mtimes for candidate two provenance claims)
sec("G run dir listing")
for f in sorted(RUN.iterdir()):
    if f.is_file():
        mt = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"{mt}  {f.stat().st_size:>9}  {f.name}")

# H. byte-identity armC_gemma2b_judge.jsonl vs armC_budget50_complete.jsonl (cand two B)
sec("H sha256 of the two 50-leg jsonl copies")
import hashlib
for name in ["armC_gemma2b_judge.jsonl", "armC_budget50_complete.jsonl"]:
    p = RUN / name
    if p.exists():
        print(name, hashlib.sha256(p.read_bytes()).hexdigest())

# I. DIRECTIVE_WATCHERS receipt: keep_alive + double-start evidence (cand two B)
sec("I DIRECTIVE_WATCHERS_20260926.md greps")
dw = ROOT / "watch" / "inbox" / "DIRECTIVE_WATCHERS_20260926.md"
if dw.exists():
    lines = dw.read_text(encoding="utf-8").splitlines()
    for pat in [r"keep_alive", r"06:07", r"double"]:
        hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if re.search(pat, l, re.I)]
        print(f"  /{pat}/:", hits if hits else "NONE")
else:
    print("FILE NOT FOUND")

# J. sha256/digest pinning in the four governing docs (cand two claim: none exist)
sec("J pinning scans in governing docs")
for rel in ["watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md",
            "watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md",
            "watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md",
            "watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md"]:
    txt = (ROOT / rel).read_text(encoding="utf-8")
    print(rel, "| sha256:", len(re.findall(r"sha256", txt, re.I)),
          "| digest:", len(re.findall(r"digest", txt, re.I)))

# K. queue/todo.md around line 196 (candidate one claim 4)
sec("K queue/todo.md lines 192-200")
todo = ROOT / "queue" / "todo.md"
if todo.exists():
    for i, l in enumerate(todo.read_text(encoding="utf-8").splitlines()[191:200], start=192):
        print(f"  :{i} {l.strip()[:200]}")

# L. git checks (candidate two A + claim 5)
sec("L git checks")
def sh(cmd):
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, shell=True)
    print("$", cmd)
    print((r.stdout or r.stderr).strip()[:1200])
    print("exit:", r.returncode)
    return r.returncode

sh('git check-ignore -v memory/runs/interference_replication_20260925/run_armC.py '
   'memory/runs/interference_replication_20260925/armC_budget50_complete.jsonl '
   'corpus/library/interference-search/results/fleet_replication_20260925.json')
sh('git ls-files corpus/library/interference-search/ | find /c /v ""')
sh('git ls-files memory/runs/ | find /c /v ""')
sh('git ls-files memory/runs/')
sh('git log --oneline -- memory/runs/interference_replication_20260925/run_armC.py')
sh('git log --oneline -- memory/runs/interference_replication_20260925/run_armA.py')
sh('git log -1 --format="%H %s" a5dd96176')
sh('git ls-tree -r a5dd96176 --name-only | findstr /c:"corpus/library/interference-search" | find /c /v ""')

# M. gitignore lines 92 and 197
sec("M .gitignore lines 90-94 and 195-199")
gi = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
for n in range(90, 95):
    print(f"  :{n} {gi[n-1]}")
for n in range(195, 200):
    if n <= len(gi):
        print(f"  :{n} {gi[n-1]}")

# N. ESTATE_INDEX rows for run_armC (cand two: path/mtime/size only, no hash)
sec("N ESTATE_INDEX rows naming run_armC")
ei = ROOT / "watch" / "ESTATE_INDEX" / "ESTATE_INDEX.jsonl"
if ei.exists():
    n = 0
    for l in ei.read_text(encoding="utf-8", errors="replace").splitlines():
        if "run_armC" in l:
            n += 1
            print("  ", l[:300])
    if n == 0:
        print("  NO rows naming run_armC")
else:
    print("FILE NOT FOUND")

print("\nDONE")
