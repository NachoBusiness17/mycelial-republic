# B2-254 2026-09-26: plug the flicker hole in the drift-patrol prompt.
# B2-199 amended automation-a7c71ad1-f43f-403d-8677-105f5176df2b so whole-file
# refreshes of living rows are forbidden and only "a HASH MISMATCH on a static
# (non-living) row" may be refreshed. The B2-254 regression found the hole: the
# fold can flicker a living row's active item to a plain (flag-free) whole-file
# HASH MISMATCH item refold to refold, because the B2-40 2^53 quantization band
# plus the non-transitive event sort (null-seq autoseal events) let the
# 2026-09-26T12:03:24Z drift-patrol-cron gala-night batch (raw seq literals
# 1789823567015749473-477, all parsing to the same double) outrank the B2-156
# living migration string seqs in some folds and not others. To the patrol such
# a flickered row reads as "static", the exact misclassification that produced
# the gala-night refreshes. This patch adds the living-history check before any
# whole-file refresh. Pattern follows B2_199_update_prompt.py (anchor replace,
# readback assert, em-dash/en-dash refuse).
import sqlite3
import sys

DB = r"C:/Users/foste/.zcode/v2/tasks-index.sqlite"
AID = "automation-a7c71ad1-f43f-403d-8677-105f5176df2b"

ANCHOR = "A HASH MISMATCH on a static (non-living) row is the only case a whole-file refresh may fix."

INSERT = (
    " A HASH MISMATCH on a row with living history is also never a refresh case:"
    " before any whole-file refresh, prove the row is static by searching"
    " watch/inbox/index_events.jsonl for the file name next to \"living\":true"
    " (known living rows: LINKS.jsonl, phone_relay_log.jsonl, EVENTS.jsonl,"
    " mimo_watch.jsonl, burn_wave_20260926/QUEUE.md; see"
    " watch/inbox/LIVING_HASH_LAW_20260926.md). A living row can flicker to a"
    " plain flag-free HASH MISMATCH item when the fold re-sorts its 2^53"
    " quantized seq band (B2-254 regression 2026-09-26: QUEUE.md and"
    " phone_relay_log.jsonl flipped failing to living across four refolds with"
    " no register event in between); that flicker is not staleness, so"
    " re-register it with add --living or add --living-open from watch/inbox"
    " and never refresh it whole-file."
)

if "\u2014" in INSERT or "\u2013" in INSERT:
    sys.exit("em-dash or en-dash found in INSERT, refusing to write")

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("SELECT prompt FROM automations WHERE automation_id = ?", (AID,))
row = cur.fetchone()
if row is None:
    sys.exit(f"automation {AID} not found")
current = row[0]
if INSERT.strip() in current:
    print("already amended, aborting")
    con.close()
    sys.exit(0)
if current.count(ANCHOR) != 1:
    sys.exit(f"anchor found {current.count(ANCHOR)} times, expected 1; prompt drifted, refusing to blind-patch")
updated = current.replace(ANCHOR, ANCHOR + INSERT)
cur.execute("UPDATE automations SET prompt = ? WHERE automation_id = ?", (updated, AID))
con.commit()
cur.execute("SELECT prompt FROM automations WHERE automation_id = ?", (AID,))
back = cur.fetchone()[0]
con.close()
assert back == updated, "readback mismatch"
assert INSERT in back, "inserted clause missing from readback"
assert "\u2014" not in back and "\u2013" not in back, "em-dash in stored prompt"
print("prompt patched, readback ok, chars:", len(back))
