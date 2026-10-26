# B2-199 2026-09-26: drift-patrol-cron living-law adoption.
# The patrol (ZCode automation automation-a7c71ad1-f43f-403d-8677-105f5176df2b
# in %USERPROFILE%/.zcode/v2/tasks-index.sqlite, cron 0 8 * * *, enabled) last
# re-registered /board/inbox/LINKS.jsonl whole-file at 2026-09-26T12:03:24Z
# (index_events.jsonl line 3054), predating the living law (B2-156 migration
# register 13:30:57.884Z, line 3091, living:true). Its prompt drove daily
# whole-file hash refreshes of living rows, which LIVING_HASH_LAW_20260926.md
# section 6 forbids. This script swaps the prompt: verify living-ok counts as
# pass, living re-seals go through add --living / --living-open, only static
# rows keep whole-file refresh, and the patrol's own receipt registers through
# the fold host (kills the hand-minted seq=epoch-ms composed-path events,
# B2-211 charter debt).
import sqlite3
import sys

DB = r"C:/Users/foste/.zcode/v2/tasks-index.sqlite"
AID = "automation-a7c71ad1-f43f-403d-8677-105f5176df2b"

OLD_PROMPT = """Morning drift patrol for the Mag harness at C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent. Run these five checks and file one receipt:

1. Backup exposure: count unpushed commits with `git rev-list --count origin/run-beta1-factory-audit-20260914..HEAD 2>/dev/null || git rev-list --count local/run-beta1-factory-audit-20260914..HEAD` \u2014 if greater than 0, run `git push local HEAD:refs/heads/run-beta1-factory-audit-20260914`.
2. Fleet vitals: `docker ps --format "{{.Names}} {{.Status}}"` \u2014 confirm mag-sovereign, mag-worker, mag-redis are Up and healthy. If any is down: `docker compose restart mag`, then re-check and note the restart in the receipt.
3. Inbox fold staleness: read watch/inbox/INDEX.json derivations.derived_at, count lines in watch/inbox/index_events.jsonl, report the gap in days/events.
4. Surface integrity: run `.venv/Scripts/python.exe -m mag.shared_surface validate`, report error count vs the 2026-09-14 baseline of 73; flag any NEW error hashes.
5. Link ledger: run `.venv/Scripts/python.exe -m mag.link_library dupes`, report the count.

Write all findings to watch/inbox/DRIFT_PATROL_<YYYYMMDD>.md (class RECEIPT, writer drift-patrol-cron), append one register event for that file to watch/inbox/index_events.jsonl (schema: seq=epoch-ms, ts ISO UTC, op register, file /board/inbox/<name>, sha256, class RECEIPT, purpose, writer drift-patrol-cron, nonce 1). If the working tree changed, commit with message "drift-patrol <date>: <one-line verdict>" and push to the backup branch. Keep the whole patrol under 5 minutes of tool calls; skip pytest (too slow for a patrol). Final message: the top 3 risks found today, one line each, boldest first."""

NEW_PROMPT = """Morning drift patrol for the Mag harness at C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent. Run these five checks and file one receipt:

1. Backup exposure: count unpushed commits with `git rev-list --count origin/run-beta1-factory-audit-20260914..HEAD 2>/dev/null || git rev-list --count local/run-beta1-factory-audit-20260914..HEAD` - if greater than 0, run `git push local HEAD:refs/heads/run-beta1-factory-audit-20260914`.
2. Fleet vitals: `docker ps --format "{{.Names}} {{.Status}}"` - confirm mag-sovereign, mag-worker, mag-redis are Up and healthy. If any is down: `docker compose restart mag`, then re-check and note the restart in the receipt.
3. Inbox fold integrity: from watch/inbox run `node ../../scripts/index_fold_host.mjs verify` and read its summary line (X hash-clean, Y living-ok, Z living-open, W mismatched, M missing, U living-unverified). Living rows PASS by design: living-ok (append growth past a prefix seal) and living-open (edit-shaped board, no byte seal) are never failures and never reasons to re-register (law: watch/inbox/LIVING_HASH_LAW_20260926.md). Report the counts, then read watch/inbox/INDEX.json derivations.derived_at and count lines in watch/inbox/index_events.jsonl for the staleness gap in days/events.
4. Surface integrity: run `.venv/Scripts/python.exe -m mag.shared_surface validate`, report error count vs the 2026-09-14 baseline of 73; flag any NEW error hashes. Living-file law section 6: whole-file hash refreshes of living rows are FORBIDDEN. Triage any hash failure: LIVING PREFIX MISMATCH or LIVING TRUNCATED means sealed bytes were mutated or truncated (tampering, not growth) - report it as a hard failure and file it as owed, never auto-refresh it. A HASH MISMATCH on a static (non-living) row is the only case a whole-file refresh may fix. If a living file genuinely needs a re-seal (semantic rewrite, never mere growth), run from watch/inbox: `INDEX_WRITER=drift-patrol-cron node ../../scripts/index_fold_host.mjs add --living <file> <class> <purpose>` for append-only originals (LINKS.jsonl, phone_relay_log.jsonl, EVENTS.jsonl) or `--living-open` for edit-shaped boards (burn_wave QUEUE.md).
5. Link ledger: run `.venv/Scripts/python.exe -m mag.link_library dupes`, report the count.

Write all findings to watch/inbox/DRIFT_PATROL_<YYYYMMDD>.md (class RECEIPT, writer drift-patrol-cron), then from watch/inbox register it with `INDEX_WRITER=drift-patrol-cron node ../../scripts/index_fold_host.mjs add DRIFT_PATROL_<YYYYMMDD>.md RECEIPT "daily patrol receipt <date>"` (the fold host mints seq, ts, sha256 and nonce; hand-appended seq=epoch-ms events are retired, they were the composed-path phantom source of B2-157). If the working tree changed, commit with message "drift-patrol <date>: <one-line verdict>" and push to the backup branch. Keep the whole patrol under 5 minutes of tool calls; skip pytest (too slow for a patrol). Final message: the top 3 risks found today, one line each, boldest first."""

if "\u2014" in NEW_PROMPT or "\u2013" in NEW_PROMPT:
    sys.exit("em-dash or en-dash found in NEW_PROMPT, refusing to write")

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("SELECT prompt FROM automations WHERE automation_id = ?", (AID,))
row = cur.fetchone()
if row is None:
    sys.exit(f"automation {AID} not found")
current = row[0]
if current.strip() != OLD_PROMPT.strip():
    print("WARNING: current prompt differs from expected OLD_PROMPT")
    print("current length:", len(current), "expected length:", len(OLD_PROMPT))
    if "--living" in current:
        print("already amended, aborting")
        con.close()
        sys.exit(0)
cur.execute("UPDATE automations SET prompt = ? WHERE automation_id = ?", (NEW_PROMPT, AID))
con.commit()
cur.execute("SELECT prompt FROM automations WHERE automation_id = ?", (AID,))
back = cur.fetchone()[0]
con.close()
assert back == NEW_PROMPT, "readback mismatch"
assert "\u2014" not in back and "\u2013" not in back, "em-dash in stored prompt"
print("prompt updated, readback ok, chars:", len(back))
