import io, os, sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
RECEIPT = os.path.join(ROOT, "watch", "inbox", "ractor50", "skills.md")
CHECKS = []
fails = []

def check(name, ok, detail):
    CHECKS.append((name, ok, detail))
    if not ok:
        fails.append(name)
    print(("PASS" if ok else "FAIL") + " " + name + " :: " + detail)

text = io.open(RECEIPT, encoding="utf-8", errors="replace").read()
check("receipt-exists", os.path.isfile(RECEIPT) and len(text) > 8000,
      "skills.md bytes=" + str(len(text)))

# 1. all 18 census skills each carry a verdict in the section-1 table
skills18 = ["operator-corrections","chan","agent-harness","mesh-comms","zai-reference",
            "salon","fireball-cycle","frontier-researcher","frontier-hr","light-operator",
            "verb-genomes","memweave","memlance","retrocausal-steering","corpus-harvest",
            "code-agent-data","elder-lens","show-me"]
sec1 = text.split("## 2. Dead-but-buildable")[0]
missing_verdict = []
for s in skills18:
    row_ok = any(("| " + s + " |") in line and ("PROMOTE" in line or "DEMOTE" in line or "KILL" in line)
                 for line in sec1.splitlines())
    if not row_ok:
        missing_verdict.append(s)
check("18-verdicts", not missing_verdict,
      "18 census skills with promote/demote/kill verdict rows; missing=" + str(missing_verdict))
n_promote = sec1.count("| PROMOTE |")
n_demote = sec1.count("| DEMOTE |")
n_kill = sec1.count("| KILL")
check("verdict-score", n_promote + n_demote + n_kill == 18,
      "PROMOTE=" + str(n_promote) + " DEMOTE=" + str(n_demote) + " KILL=" + str(n_kill) + " sum=18 expected")

# 2. five wave protocol specs
protocols = ["Gala divisions", "Mickey17 partition", "Firehose census",
             "Mirror mine", "Stealth-wide fetch-verify"]
missing_p = [p for p in protocols if ("### 3." not in text or p not in text)]
spec_count = text.count("One-sitting card spec")
check("5-protocol-specs", not missing_p and spec_count >= 5,
      "protocols missing=" + str(missing_p) + " one-sitting card specs=" + str(spec_count))

# 3. dead-but-buildable: wave proof + build spec per named skill
for s in ["code-agent-data", "elder-lens", "salon"]:
    in_sec2 = s in text.split("## 3. The wave-invented")[0].split("## 2. Dead-but-buildable")[-1]
    check("dead-but-buildable:" + s, in_sec2 and "build spec" in text, "named in section 2 with build spec")
check("show-me-honest-kill", "NOT a dead-but-buildable" in text.replace("not a dead-but-buildable", "NOT a dead-but-buildable") or "no wave proof exists" in text,
      "show-me killed with the honest no-wave-proof note")

# 4. cited evidence paths exist on disk
paths = [
    "watch/inbox/burn_reset_20260927/flash50/skill-census.md",
    "watch/inbox/burn_reset_20260927/flash50/skill-liveness.md",
    "watch/inbox/burn_reset_20260927/flash50/f-06.md",
    "watch/inbox/burn_reset_20260927/flash50/ladder-02.md",
    ".zcode/workflow-drafts/firehose.dwf.ts",
    ".zcode/workflow-drafts/mickey17-wave3.dwf.ts",
    ".zcode/workflow-drafts/mirror-mine.dwf.ts",
    ".zcode/workflow-drafts/stealth-wide.dwf.ts",
    ".zcode/workflow-drafts/Ractor-50-wave-retro.dwf.ts",
    ".zcode/workflow-drafts/ractor_panel_20260926.dwf.ts",
    ".agents/skills/frontier-mine/SKILL.md",
    ".agents/skills/ractor-essay/SKILL.md",
    ".agents/skills/corpus-harvest/SKILL.md",
    "tools/stealth_fanout.py",
    "tools/workflow_gate.py",
    "mag/chan.py", "tests/test_chan.py", "mag/water_computer.py",
    "mag/memweave.py", "mag/ghost_memlance.py",
    "queue/lanes/elder/inbox.jsonl",
    "watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md",
    "watch/inbox/gala_20260925/48h-synthesis_RECEIPT.md",
    "configs/skills.yaml",
]
missing_paths = []
for rel in paths:
    if not os.path.exists(os.path.join(ROOT, rel.replace("/", os.sep))):
        missing_paths.append(rel)
check("evidence-paths", not missing_paths,
      str(len(paths)) + " cited paths exist; missing=" + str(missing_paths))

# 5. em-dash law on the record file
em = [i for i, ch in enumerate(text) if ch == "\u2014"]
check("no-em-dash", not em, "U+2014 count in skills.md = " + str(len(em)))

# 6. census drift numbers restated (18 -> 20, bytes)
check("drift-named", "65,826" in text and "20 files" in text and "frontier-mine 2,398" in text,
      "instrument/moment/delta named for the 18-to-20 drift")

print("")
print("CHECKS: " + str(len(CHECKS)) + "  FAILS: " + str(len(fails)) + (" -> " + ",".join(fails) if fails else ""))
sys.exit(0 if not fails else 1)
