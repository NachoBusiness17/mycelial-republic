# prereg-attack revision verification (revise-prereg-attack seat, 2026-09-26)
# Re-runs every check the final card cites, so the revision's claims are
# checked in the revising ask itself, raw output saved to prereg-attack.revise.txt.
# Companion to checks/prereg_attack_revise_checks.py's judge run:
# watch/inbox/ractor_panel_20260926/checks/prereg-attack.judge.txt (sections A-F).
import hashlib
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
RUN = ROOT / "memory" / "runs" / "interference_replication_20260925"
OUT = ROOT / "watch" / "inbox" / "ractor_panel_20260926" / "checks" / "prereg-attack.revise.txt"

buf = io.StringIO()


def emit(line=""):
    print(line)
    buf.write(line + "\n")


def numbered(path, lo, hi):
    lines = path.read_text(encoding="utf-8").splitlines()
    return [(i + 1, lines[i]) for i in range(lo - 1, min(hi, len(lines)))]


emit("========== R1 prereg cost-unit law, exact line pin (watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md) ==========")
for n, t in numbered(ROOT / "watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md", 45, 48):
    emit(f"  :{n} {t}")
l = dict(numbered(ROOT / "watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md", 45, 48))
emit(f"  'LLM tokens counted and' on line 47: {'LLM tokens counted and' in l[47]}")
emit(f"  line 48 starts 'reported for Arm A/C': {l[48].startswith('reported for Arm A/C')}")

emit("========== R2 amendment 1 clauses 2-3, exact line pin ==========")
for n, t in numbered(ROOT / "watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md", 29, 33):
    emit(f"  :{n} {t}")

emit("========== R3 instrument lines (run_armC.py / run_armA.py) ==========")
for n, t in numbered(RUN / "run_armC.py", 26, 31):
    emit(f"  run_armC.py:{n} {t}")
for n, t in numbered(RUN / "run_armC.py", 35, 35):
    emit(f"  run_armC.py:{n} {t}")
for n, t in numbered(RUN / "run_armC.py", 59, 59):
    emit(f"  run_armC.py:{n} {t}")
for n, t in numbered(RUN / "run_armC.py", 81, 81):
    emit(f"  run_armC.py:{n} {t}")
for n, t in numbered(RUN / "run_armC.py", 7, 9):
    emit(f"  run_armC.py:{n} {t}")
for n, t in numbered(RUN / "run_armA.py", 50, 50):
    emit(f"  run_armA.py:{n} {t}")

emit("========== R4 armC_budget50_complete.jsonl census ==========")
rows = [json.loads(x) for x in (RUN / "armC_budget50_complete.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
emit(f"  row count: {len(rows)}")
emit(f"  any row has a token field: {any('tokens' in r or 'eval_count' in r for r in rows)}")
emit(f"  summary row verbatim: {json.dumps(rows[-1], ensure_ascii=False)}")

emit("========== R5 armA_gemma2b_cot.jsonl census ==========")
arows = [json.loads(x) for x in (RUN / "armA_gemma2b_cot.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
toks = [r.get("tokens", 0) for r in arows]
emit(f"  row count: {len(arows)} total tokens: {sum(toks)} avg: {round(sum(toks) / len(toks), 1)}")

emit("========== R6 receipt greps (tok / parse) ==========")
for rel in [r"watch\inbox\BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md",
            r"watch\inbox\burn_wave_20260926\B2_140_armc_closeout_20260926.md"]:
    p = ROOT / rel
    hits_tok = [(i + 1, ln.rstrip()) for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines()) if "tok" in ln.lower()]
    hits_parse = [(i + 1, ln.rstrip()) for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines()) if "parse" in ln.lower()]
    emit(f"  {rel}")
    emit(f"    tok hits (case-insensitive): {hits_tok if hits_tok else 'NONE'}")
    emit(f"    parse hits (case-insensitive): {hits_parse if hits_parse else 'NONE'}")

emit("========== R7 eval_count grep across run dir py files ==========")
for p in sorted(RUN.glob("*.py")):
    hits = [(i + 1, ln.rstrip()) for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines()) if "eval_count" in ln]
    if hits:
        emit(f"  {p.name} {hits}")
emit("  (files with no hit omitted; full listing in judge.txt section C)")

emit("========== R8 provider_usage.jsonl gemma:2b meter rows ==========")
pu = ROOT / "logs" / "provider_usage.jsonl"
gem = []
for x in pu.read_text(encoding="utf-8").splitlines():
    if not x.strip():
        continue
    try:
        r = json.loads(x)
    except Exception:
        continue
    if r.get("model") == "gemma:2b":
        gem.append(r)
dates = sorted(r["ts"][:10] for r in gem)
last = gem[-1]
emit(f"  gemma:2b rows total: {len(gem)}")
emit(f"  first: {dates[0]} last: {dates[-1]}")
emit(f"  rows dated 2026-09-25: {dates.count('2026-09-25')}  2026-09-26: {dates.count('2026-09-26')}")
emit(f"  last row carries prompt_tokens={last.get('prompt_tokens')} completion_tokens={last.get('completion_tokens')} ts={last.get('ts')}")

emit("========== R9 digest/sha256 pinning scan in the four governing docs ==========")
for rel in [r"watch\inbox\INTERFERENCE_REPLICATION_PREREG_20260925.md",
            r"watch\inbox\INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md",
            r"watch\inbox\BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md",
            r"watch\inbox\burn_wave_20260926\B2_140_armc_closeout_20260926.md"]:
    txt = (ROOT / rel).read_text(encoding="utf-8").lower()
    emit(f"  {rel} | sha256: {txt.count('sha256')} | digest: {txt.count('digest')} | b50d6c: {txt.count('b50d6c')}")

emit("========== R10 live ollama gemma:2b digest probe (read-only GET loopback) ==========")
try:
    with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=10) as r:
        tags = json.loads(r.read())
    for m in tags.get("models", []):
        if m.get("name") == "gemma:2b":
            emit(f"  name: {m['name']} | digest: {m['digest']} | modified: {m['modified']}")
except Exception as e:
    emit(f"  PROBE FAILED: {type(e).__name__}: {e}")
    emit("  (fallback evidence: judge.txt section Q, digest b50d6c999e592ae4f79acae23b4feaefbdfceaa7cd366df2610e3072c052a160)")

emit("========== R11 sha256 of current instrument bytes (pre-patch reference for amendment 2) ==========")
for name in ["run_armC.py", "run_armA.py"]:
    b = (RUN / name).read_bytes()
    emit(f"  {name} {hashlib.sha256(b).hexdigest()} ({len(b)} bytes)")

emit("========== R12 queue/todo.md line 196 verbatim ==========")
for n, t in numbered(ROOT / "queue" / "todo.md", 196, 196):
    emit(f"  :{n} {t}")

OUT.write_text(buf.getvalue(), encoding="utf-8")
print(f"\nWROTE {OUT}")
