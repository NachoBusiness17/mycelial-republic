"""f-24 post-run verifier: prints facts from f-24_data.json for the receipt.

Read-only. Run: ./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_f24_verify.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "f-24_data.json"), encoding="utf-8"))
mods = {m["file"]: m for m in d["modules"]}
t = d["totals"]

print("totals:", json.dumps(t, indent=None))
for f in ("mag/context_pack.py", "mag/cli/core.py", "mag/game_campaign.py"):
    m = mods[f]
    print("---", f)
    print("  lines=%d fns=%d classes=%d tests=%d readers=%d"
          % (m["lines"], len(m["fns"]), len(m["classes"]),
             len(m["test_files"]), len(m["readers"])))
    print("  test_files:", m["test_files"])
    print("  readers[:8]:", m["readers"][:8])
    print("  fns:", m["fns"])
    print("  last_commit:", m["last_commit"], "| mtime:", m["mtime"])

# distribution of test-file counts
zero = [m["file"] for m in d["modules"] if not m["test_files"]]
one_plus = [m for m in d["modules"] if len(m["test_files"]) >= 1]
five_plus = [m for m in d["modules"] if len(m["test_files"]) >= 5]
print("modules with >=5 test files:", len(five_plus))
print("zero-test modules [:20]:", zero[:20])
orph = [m["file"] for m in d["modules"]
        if not m["test_files"] and not m["readers"]]
print("orphans (%d): %s" % (len(orph), ", ".join(orph[:40])))
# subpackage module check: relative readers of cli/core include cli/__init__
cc = mods["mag/cli/core.py"]
print("cli/__init__ is a reader of cli/core:",
      "mag/cli/__init__.py" in cc["readers"])
# newest and oldest last-commit dates
dates = sorted(m["last_commit"].split(" ", 1)[1] for m in d["modules"]
               if not m["last_commit"].startswith("never"))
print("oldest last-commit:", dates[0], "| newest last-commit:", dates[-1])
