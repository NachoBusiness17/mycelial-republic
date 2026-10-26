# B2-298 2026-09-26: land the repo-side copy of the drift-patrol prompt.
# The amended living-law patrol prompt lives only in
# %USERPROFILE%/.zcode/v2/tasks-index.sqlite automations row
# automation-a7c71ad1-f43f-403d-8677-105f5176df2b (written by
# B2_199_update_prompt.py). A harness rebuild or DB reset would silently
# revert the patrol to whole-file hash refreshes. This script reads the DB
# row (authoritative bytes), compares it against the NEW_PROMPT recorded in
# B2_199_update_prompt.py (parsed via ast, never imported: that module
# executes an UPDATE at import time), and lands the exact DB bytes as a
# repo-side copy for tools/drift_patrol_prompt_check.py to diff against.
import ast
import hashlib
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DB = Path.home() / ".zcode" / "v2" / "tasks-index.sqlite"
AID = "automation-a7c71ad1-f43f-403d-8677-105f5176df2b"
UPDATER = REPO / "watch" / "inbox" / "burn_wave_20260926" / "B2_199_update_prompt.py"
DEST = REPO / "configs" / "drift_patrol_prompt_a7c71ad1.txt"


def db_prompt() -> str:
    con = sqlite3.connect(str(DB))
    try:
        cur = con.cursor()
        cur.execute("SELECT prompt FROM automations WHERE automation_id = ?", (AID,))
        row = cur.fetchone()
    finally:
        con.close()
    if row is None:
        sys.exit(f"FATAL: automation {AID} not in {DB}")
    return row[0]


def script_prompt() -> str:
    tree = ast.parse(UPDATER.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "NEW_PROMPT":
                    return ast.literal_eval(node.value)
    sys.exit(f"FATAL: NEW_PROMPT not found in {UPDATER}")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    live = db_prompt()
    amended = script_prompt()
    print("DB   prompt: len", len(live), "sha", sha(live))
    print("B2-199 NEW: len", len(amended), "sha", sha(amended))
    if live == amended:
        print("MATCH: DB row is byte-identical to the B2-199 amended prompt")
    else:
        print("DIFFER: DB row has drifted from the B2-199 script constant (DB wins, it is authoritative)")
    for marker in ("index_fold_host.mjs verify", "--living-open",
                   "LIVING PREFIX MISMATCH", "hand-appended seq=epoch-ms events are retired"):
        print(f"  marker {'ok ' if marker in live else 'MISSING '} {marker!r}")
    if "\u2014" in live or "\u2013" in live:
        sys.exit("FATAL: dash-of-shame in DB prompt, refusing to land it")
    if "LIVING PREFIX MISMATCH" not in live:
        sys.exit("FATAL: DB prompt lost the living-law clauses, refusing to land it")
    DEST.write_bytes(live.encode("utf-8"))
    back = DEST.read_bytes().decode("utf-8")
    assert back == live, "repo copy readback mismatch"
    print(f"LANDED: {DEST.relative_to(REPO)} len {len(back)} sha {sha(back)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
