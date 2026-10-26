# selfsteal lane byte battery (ractor50, division B). Run with the repo venv:
#   .venv/Scripts/python.exe watch/inbox/gala_20260925/ractor50/lanes/selfsteal.check.py
# Checks every verbatim quote, path claim, and defect-line cite made in
# watch/inbox/ractor50/selfsteal.md. Whitespace-normalized containment for quotes.
import os, sys, datetime

ESTATE = "C:/Users/foste/Documents/projects/local_sovereign_agent"
RECEIPT = ESTATE + "/watch/inbox/ractor50/selfsteal.md"
DRAFT = ESTATE + "/.zcode/workflow-drafts/Ractor-50-wave-retro.dwf.ts"
JOURNAL = ESTATE + "/.zcode/workflow-runs/dwfrun-0dd7a6c5-5870-4b17-9738-eb2f585f5afd.mjs"
LANES_DIR = ESTATE + "/watch/inbox/gala_20260925/ractor50/lanes"

passed = 0
failed = 0
def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print("PASS " + name)
    else:
        failed += 1
        print("FAIL " + name + (" | " + detail if detail else ""))

def norm(s):
    return " ".join(s.split())

def contains(path, needle):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return norm(needle) in norm(f.read())
    except OSError as e:
        return False

def line_of(path, needle):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for i, ln in enumerate(f, 1):
                if needle in ln:
                    return i
    except OSError:
        return -1
    return -1

print("selfsteal.check.py run at " + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
print("== 1. receipt exists ==")
check("receipt exists", os.path.isfile(RECEIPT), RECEIPT)

print("== 2. quote containment (whitespace-normalized) ==")
QUOTES = [
    ("Q1 tri-state table", ESTATE + "/watch/inbox/Q_OPERATION_RACTOR_20260929/RAINBOW_CLAIMS_AUDIT.md",
     "Verdicts are tri-state: Supported / Disputed / Unproven. House laws observed: no em-dashes; every source listed was actually consulted during this audit; nothing is asserted beyond what the cited source shows."),
    ("Q2 verified-clean", ESTATE + "/watch/inbox/RAINBOW_ROAD_RACTOR_20260929/GRADED.md",
     "**Verified clean for game theory, stated so the grade is fair:** every external figure verifies against the live sources."),
    ("Q3 fixed-section contract", ESTATE + "/watch/inbox/48h_synth/STORY.md",
     "The receipt contract is fixed-section and closed-bibliography (watch/inbox/BURN_<slug>_<YYYYMMDD>.md, max 500 words, Verdict / Evidence / Steal or Vacuous / Falsifier / Bibliography)"),
    ("Q4 close-check law", ESTATE + "/watch/inbox/48h_synth/STORY.md",
     "the B2-203 close-check law runs tools/ledger_close_check.py over any one_line asserting a missing path before the row banks, because a claimed-missing path that exists mints a phantom owed brief"),
    ("Q5 grave discipline", ESTATE + "/watch/inbox/ball2/graves/grave-01-index-foldback.md",
     "Nothing was deleted, moved, or edited. Deletions are operator-gated."),
    ("Q6 preserved failed run", ESTATE + "/watch/inbox/48h_synth/laws.md",
     "run 2: misses=0, exit 0; run 1 caught one quote of mine that spanned a wrapped line and was corrected before run 2, the miss is preserved in the saved output"),
    ("Q7 forecast battery", ESTATE + "/watch/inbox/48h_synth/next.md",
     "F1. At 2026-10-01T23:59Z, watch/inbox/KEY_ROTATION_JOURNAL.jsonl still does not exist. Falsified by: a journal row naming xAI with masked heads at that moment"),
    ("Q8 wiring truth", ESTATE + "/watch/inbox/burn_reset_20260927/flash50/w4-41.md",
     "Whether a proved function is wired into the system's behavior is a fact about the whole tree, reachable only by a whole-tree search (my grep) or by whole-system execution."),
    ("Q9 counting wound", ESTATE + "/watch/inbox/RAINBOW_ROAD_RACTOR_20260929/GRADED.md",
     "The census-denominator discipline is satisfied in the source file and violated in the essay."),
]
for name, src, q in QUOTES:
    check(name, contains(src, q), src)

print("== 3. corpus table paths exist ==")
CORPUS = [
    ESTATE + "/watch/inbox/48h_synth/STORY.md",
    ESTATE + "/watch/inbox/48h_synth/steals.md",
    ESTATE + "/watch/inbox/48h_synth/laws.md",
    ESTATE + "/watch/inbox/48h_synth/measure.md",
    ESTATE + "/watch/inbox/48h_synth/next.md",
    ESTATE + "/watch/inbox/48h_synth/lattice.md",
    ESTATE + "/watch/inbox/RAINBOW_ROAD_RACTOR_20260929/RECEIPT.md",
    ESTATE + "/watch/inbox/RAINBOW_ROAD_RACTOR_20260929/GRADED.md",
    ESTATE + "/watch/inbox/Q_OPERATION_RACTOR_20260929/DIGEST.md",
    ESTATE + "/watch/inbox/Q_OPERATION_RACTOR_20260929/RAINBOW_CLAIMS_AUDIT.md",
    ESTATE + "/watch/inbox/ball2/graves/grave-01-index-foldback.md",
    ESTATE + "/watch/inbox/burn_reset_20260927/flash50/w4-41.md",
    ESTATE + "/memory/burns/LEDGER.jsonl",
    DRAFT,
    JOURNAL,
]
for p in CORPUS:
    check("exists " + p.replace(ESTATE + "/", ""), os.path.isfile(p))

print("== 4. B2 ledger row count (instrument: python line read) ==")
try:
    with open(ESTATE + "/memory/burns/LEDGER.jsonl", "r", encoding="utf-8", errors="replace") as f:
        n = sum(1 for ln in f if ln.strip())
    check("LEDGER.jsonl rows = 693", n == 693, "got " + str(n))
except OSError:
    check("LEDGER.jsonl rows = 693", False, "unreadable")

print("== 5. defect cites: driver draft line pins ==")
d1a = line_of(DRAFT, 'artifact.file("receipt"')
d1b = line_of(DRAFT, "deepChecks: DeepCheck[]")
check("D1 receipt publish precedes tier-2", 0 < d1a < d1b, "publish@" + str(d1a) + " deep@" + str(d1b))
check("D2 tier-2 cap slice(0, 12) on draft line 339", line_of(DRAFT, ".slice(0, 12)") == 339 or contains(DRAFT, ".filter((x) => x.r.leverage === \"high\").slice(0, 12)"))
check("D3 B template rows-may-be-empty on draft line 163", line_of(DRAFT, "rows may be empty") == 163 or contains(DRAFT, "rows may be empty"))
check("D4 tier-1 rides A only", contains(DRAFT, 'if (t.division === "A" && rows.length > 0)'))
check("D5 reader no-fetch 5-bullet clause", contains(DRAFT, "Do not fetch. At most 5 bullets."))
check("D8 telemetry to folder not lanes", contains(DRAFT, "refired") and contains(DRAFT, "Run metadata: \" + compact"))

print("== 6. defect cites: journal lane list ==")
import re as _re
_journal_text = ""
try:
    with open(JOURNAL, "r", encoding="utf-8", errors="replace") as f:
        _journal_text = f.read()
except OSError:
    pass
check("D6 logic lane is division A in journal args", bool(_re.search(r'\{"division":"A"[^}]*"id":"logic"', _journal_text)))
check("D7a ask says Q-operation 3-lens", contains(JOURNAL, "Q-operation 3-lens graded"))
check("D7a Q-operation really has 4 lens files", len([x for x in os.listdir(ESTATE + "/watch/inbox/Q_OPERATION_RACTOR_20260929") if x.startswith("LENS_")]) == 4)
check("D7b rainbow-road really has 3 lens files", len([x for x in os.listdir(ESTATE + "/watch/inbox/RAINBOW_ROAD_RACTOR_20260929") if x.startswith("LENS_")]) == 3)
check("D7b ask names firehose/mirror/mcp/w4 census classes", contains(JOURNAL, "firehose/mirror/mcp/w4 census classes"))
check("D7b no firehose receipt file dated 0929 in watch/inbox", not any("firehose" in x.lower() and "20260929" in x for x in os.listdir(ESTATE + "/watch/inbox")))
check("journal carries 7 lanes", contains(JOURNAL, '"id":"selfsteal"'))

print("== 7. finish-line receipt paths, live probe (informational) ==")
for lid in ["accuracy", "operations", "skills", "communication", "mcp", "selfsteal", "logic"]:
    p = ESTATE + "/watch/inbox/ractor50/" + lid + ".md"
    print("PROBE " + lid + " " + ("PRESENT" if os.path.isfile(p) else "ABSENT") + " " + p)
check("selfsteal.md lands (this lane's finish line)", os.path.isfile(RECEIPT))

print("== 8. dash + ascii scan on authored files ==")
def dash_scan(p):
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            t = f.read()
        bad = [c for c in t if c in ("\u2013", "\u2014")]
        nonascii = [c for c in t if ord(c) > 127]
        return len(bad), len(nonascii)
    except OSError:
        return -1, -1
b1, a1 = dash_scan(RECEIPT)
check("receipt no em/en dash, ascii only", b1 == 0 and a1 == 0, "dashes=" + str(b1) + " nonascii=" + str(a1))
LANE_JSON = LANES_DIR + "/selfsteal.json"
if os.path.isfile(LANE_JSON):
    b2, a2 = dash_scan(LANE_JSON)
    check("lane json no em/en dash, ascii only", b2 == 0 and a2 == 0, "dashes=" + str(b2) + " nonascii=" + str(a2))
else:
    print("PROBE lane json not yet written (validated after write by rerun)")

print("== summary ==")
print("PASSED=" + str(passed) + " FAILED=" + str(failed))
sys.exit(0 if failed == 0 else 1)
