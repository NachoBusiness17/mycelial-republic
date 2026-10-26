# Lane next (division B) byte checks. Raw output: next.check.txt
# Verifies every status claim in watch/inbox/48h_synth/next.md against the tree.
import os, re, shutil, subprocess, sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
os.chdir(ROOT)
results = []

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def contains(path, needle, label=None):
    label = label or needle[:60]
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            ok = norm(needle) in norm(f.read())
    except OSError as e:
        results.append(("FAIL", label, "unreadable: %s" % e)); return
    results.append(("PASS" if ok else "FAIL", label, path))

def absent(path, label):
    ok = not os.path.exists(path)
    results.append(("PASS" if ok else "FAIL", label, path))

def count_lines(path, expected, label):
    try:
        with open(path, "rb") as f:
            n = sum(1 for _ in f)
    except OSError:
        results.append(("FAIL", label, "missing file")); return
    results.append(("PASS" if n == expected else "FAIL", "%s (rows=%d expected=%d)" % (label, n, expected), path))

# 1. the prime's 5-move order, quoted in the memo
P = "watch/inbox/HERMES_PRIME_JUDGMENT_20260929.md"
for q in ["Rotate the xAI key", "Freeze the green commit as the recovery pack",
          "Steal-map the top ~12 finds", "Build the heartbeat",
          "Injection-test the freshly-wired loops", "exports the leak off-machine"]:
    contains(P, q)

# 2. move 1: rotation journal still absent (PASS when absent)
absent("watch/inbox/KEY_ROTATION_JOURNAL.jsonl", "KEY_ROTATION_JOURNAL.jsonl ABSENT (rotation unlogged)")
contains("watch/inbox/burn_wave_20260926/B2_349_rotation_owed_20260926.md", "OWED, operator-gated")
contains("watch/inbox/burn_wave_20260926/B2_349_rotation_owed_20260926.md", "2 xAI")
contains("watch/inbox/last_mile_20260930/AJ9_NOUS_402.md", "old key still valid (not yet revoked)")
contains("watch/inbox/DAY_SYNTHESIS_20260930.md", "ROTATED.")

# 3. move 2: no tag, no restic, backup plan design-only
r = subprocess.run(["git", "tag"], capture_output=True, text=True)
tags = r.stdout.strip()
results.append(("PASS" if not tags else "FAIL", "git tag EMPTY (green commit unfrozen)", repr(tags)))
results.append(("PASS" if shutil.which("restic") is None else "FAIL", "restic NOT on PATH", "shutil.which"))
contains("watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md",
         "Nothing is scheduled, nothing has been run against any real repository")
contains("watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md", "test a restore")

# 4. move 3: cards exist, zero ports fired
absent("watch/inbox/frontier_olm_20260928/probe", "S1 probe dir ABSENT (frontier_olm_20260928/probe)")
absent("watch/inbox/ball2/abliterate_p1_runs_qwen25-3b.json", "S5 probe output ABSENT (abliterate_p1_runs_qwen25-3b.json)")
contains("watch/inbox/frontier_olm_20260928/DIGEST.md", "Not run by this fold")
contains("watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md", "Status: OWED, not run")
contains("mag/percolator.py", '"status": "repeat"')
contains("mag/percolator.py", '"compiled": True')
contains("mag/seed_percolator.py", "No scheduler wiring")

# 5. move 4: bake cadence armed with one fire, watchlist poll unscheduled
contains("scripts/estate_walk_daily.ps1", "memory\\attention.md")
log = ""
try:
    with open("logs/estate_walk_daily.log", "rb") as f:
        log = f.read().decode("utf-16-le", errors="replace")
except OSError:
    pass
ok = "END 2026-09-29T22:16:50Z exit=0" in log
results.append(("PASS" if ok else "FAIL", "estate_walk log one fire END 2026-09-29T22:16:50Z exit=0", "logs/estate_walk_daily.log"))
contains("mag/whale_patrol.py", "def cmd_watchlist")
contains("mag/whale_patrol.py", "def cmd_feed")
contains("configs/watched_channels.yaml", "handle: karpathy")

# 6. move 5: market stalled at 2 self-cast rows, bridge pinned, no injection receipt
count_lines("memory/attention_feedback.jsonl", 2, "attention_feedback.jsonl row count")
count_lines("state/mcp_pins.jsonl", 92, "mcp_pins.jsonl row count")
inj_hits = []
for d in ["watch/inbox/wave5_repair", "watch/inbox/ball2"]:
    for dirpath, _dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(dirpath, fn)
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    if "inject" in f.read().lower():
                        inj_hits.append(p)
            except OSError:
                pass
ok = inj_hits == ["watch/inbox/wave5_repair\\suite-burn.md"] or inj_hits == ["watch/inbox/wave5_repair/suite-burn.md"]
results.append(("PASS" if ok else "FAIL", "no injection-test receipt (only incidental suite-burn.md match)", repr(inj_hits)))

# 7. quota shape honest gap + elder park + schtasks shape
contains("watch/inbox/CYCLE_BRIEF_20260930.md", "[quota report empty - HONEST-GAP]")
contains("watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md", "Named re-raise conditions")
contains("watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md", "1,000,000 leaves")
r = subprocess.run(["cmd", "/c", "schtasks /Query /FO CSV"], capture_output=True, text=True)
st = r.stdout
ok = "EstateWalkDaily" in st and "\\MagLeaveProtocolDaily" in st and "whale" not in st.lower()
results.append(("PASS" if ok else "FAIL", "schtasks: EstateWalkDaily + MagLeaveProtocolDaily present, no whale task", "schtasks /Query /FO CSV"))
m = re.search(r'"\\EstateWalkDaily","([^"]+)","([^"]+)"', st)
results.append(("PASS" if m and m.group(2) == "Ready" else "FAIL", "EstateWalkDaily Ready, next run %s" % (m.group(1) if m else "?"), "schtasks"))

# 8. receipt self-check
contains("watch/inbox/48h_synth/next.md", "What the estate did right against the order")
contains("watch/inbox/48h_synth/next.md", "Falsifiable forecasts (named signals, named dates)")
contains("watch/inbox/48h_synth/next.md", "recovery-pack/20260930-green")
contains("watch/inbox/48h_synth/next.md", "Cost of the deferral")

fails = sum(1 for s, _l, _e in results if s == "FAIL")
for s, label, ev in results:
    print("%s | %s | %s" % (s, label, ev))
print("TOTAL %d checks, %d FAIL" % (len(results), fails))
sys.exit(1 if fails else 0)
