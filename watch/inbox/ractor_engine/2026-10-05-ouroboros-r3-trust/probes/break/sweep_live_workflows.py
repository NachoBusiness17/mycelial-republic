"""BREAK-OPERATIONS sweep (lens blind spot 1, now measured): every saved
.zcode/workflows/*.dwf.ts (+ drafts if present), checked for
  (a) max_concurrency declarations whose RHS is not a bare literal digit
      (the G8 blind shape, tools/workflow_gate.py:176),
  (b) gates that pass ONLY through comment text (strip /*..*/ and // lines,
      re-run run_checks, report flips ok->not-ok),
  (c) FIRE_LEDGER rows and the max_concurrency value each joined (the row-7
      instrument inherits the same digit-only parser via max_declared_width).
Pure file ops + module import; no subprocess spawned.
"""
import glob
import json
import re
import sys
from pathlib import Path

REPO = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(REPO))
from tools.workflow_gate import run_checks, G8_MAX_CONCURRENCY_RE  # noqa: E402

files = sorted(glob.glob(str(REPO / ".zcode" / "workflows" / "*.dwf.ts")))
drafts = sorted(glob.glob(str(REPO / ".zcode" / "workflow-drafts" / "*.dwf.ts")))
print(f"sweep: {len(files)} saved + {len(drafts)} draft .dwf.ts files")

nonliteral = re.compile(r"max_concurrency\s*[:=]\s*(?!\d)([A-Za-z_][\w.]*)")

def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(?m)(?<!:)//[^\n]*", "", text)

width_report = []
flip_report = []
for f in files + drafts:
    text = Path(f).read_text(encoding="utf-8", errors="replace")
    rel = str(Path(f).relative_to(REPO)).replace("\\", "/")
    literal_widths = G8_MAX_CONCURRENCY_RE.findall(text)
    var_widths = nonliteral.findall(text)
    if var_widths or not literal_widths:
        width_report.append((rel, literal_widths, var_widths))
    full_failed = [r["id"] for r in run_checks(text) if not r["ok"] and not r.get("soft")]
    stripped_failed = [r["id"] for r in run_checks(strip_comments(text))
                       if not r["ok"] and not r.get("soft")]
    newly_failed = [g for g in stripped_failed if g not in full_failed]
    if newly_failed:
        flip_report.append((rel, newly_failed))

print("\n== (a) width declaration shapes (no literal digit found, or variable RHS) ==")
for rel, lw, vw in width_report:
    print(f"  {rel}: literal={lw or 'NONE'} variable_rhs={vw or 'none'}")
print(f"  ({len(width_report)} of {len(files) + len(drafts)} files declare no literal width"
      f" or use a variable RHS)")

print("\n== (b) gates that pass ONLY via comment text (would FAIL on stripped body) ==")
for rel, gates in flip_report:
    print(f"  {rel}: {', '.join(gates)}")
print(f"  ({len(flip_report)} of {len(files) + len(drafts)} files lean on comments for >=1 gate)")

fl = REPO / "memory" / "workflows" / "FIRE_LEDGER.jsonl"
print("\n== (c) FIRE_LEDGER rows (script, verdict, max_concurrency join) ==")
if fl.is_file():
    lines = fl.read_text(encoding="utf-8").strip().splitlines()
    for ln in lines[-12:]:
        r = json.loads(ln)
        print(f"  {r.get('ts')} {Path(r.get('script','?')).name} {r.get('verdict')} width={r.get('max_concurrency')}")
    print(f"  total rows: {len(lines)}")
else:
    print("  FIRE_LEDGER.jsonl absent")
