# B2-267 2026-09-26: wire the touch law into the drift-patrol prompt.
# The amended patrol prompt (B2-199, automation-a7c71ad1 in
# %USERPROFILE%/.zcode/v2/tasks-index.sqlite) predates the touch law
# (B2-237 receipt Work done item 1), so the patrol lacks: (1) the reader-open
# rule, (2) the size+seal-before-alarm triage rule, (3) the file-every-touch
# rule. This script appends the three clauses to the LIVE DB prompt and
# writes a repo-side copy at configs/drift_patrol_prompt.txt, which
# tests/test_drift_patrol_prompt_copy.py diffs against the DB (the
# freshness_check pattern: bytes vs report, no hand-written trust).
# Idempotent: aborts when the touch-law block is already present.
import sqlite3
import sys
from pathlib import Path

DB = r"C:/Users/foste/.zcode/v2/tasks-index.sqlite"
AID = "automation-a7c71ad1-f43f-403d-8677-105f5176df2b"
REPO_COPY = Path(__file__).resolve().parents[2] / "configs" / "drift_patrol_prompt.txt"
MARKER = "TOUCH LAW (B2-237,"  # prefix form: the block text continues ", binding on this patrol)"

TOUCH_BLOCK = """

TOUCH LAW (B2-237, binding on this patrol):
6a. Readers never open registered or living-sealed logs in write-capable mode: "rb" or "r" only. The modes "w", "w+", "r+", "a", "a+" belong to the file's named writer; a reader opening them is a defect even at zero bytes written.
6b. mtime is not tamper evidence. Triage checks size and prefix seal FIRST: a size-stable, seal-verifying file with a fresher mtime was touched, not tampered; file it as a touch observation, never alarm, never auto-refresh.
6c. A touch without a register event is still filed (paths, window, writer or "unattributed") so repeats correlate. Every touch observation lands in the day's DRIFT_PATROL receipt."""

if "\u2014" in TOUCH_BLOCK or "\u2013" in TOUCH_BLOCK:
    sys.exit("em-dash or en-dash found in TOUCH_BLOCK, refusing to write")

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("SELECT prompt FROM automations WHERE automation_id = ?", (AID,))
row = cur.fetchone()
if row is None:
    sys.exit(f"automation {AID} not found")
current = row[0]
if MARKER in current:
    print("already amended, aborting")
    con.close()
    sys.exit(0)
updated = current.rstrip("\n") + TOUCH_BLOCK + "\n"
cur.execute("UPDATE automations SET prompt = ? WHERE automation_id = ?", (updated, AID))
con.commit()
back = cur.execute("SELECT prompt FROM automations WHERE automation_id = ?", (AID,)).fetchone()[0]
con.close()
assert back == updated, "readback mismatch"
assert MARKER in back, "marker missing after write"
assert "\u2014" not in back and "\u2013" not in back, "em-dash in stored prompt"
REPO_COPY.parent.mkdir(parents=True, exist_ok=True)
REPO_COPY.write_text(back, encoding="utf-8", newline="")
print("prompt updated, readback ok, chars:", len(back))
print("repo copy written:", REPO_COPY)
