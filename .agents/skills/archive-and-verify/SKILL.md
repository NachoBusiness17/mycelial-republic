---
name: archive-and-verify
description: "Use in Roster Swap Phases 2-3 to archive each bot's full history and prove it's complete."
---

# Archive and verify (Phases 2-3)
First check whether each bot can export its full history. If it cannot, or you cannot confirm it, mark it [UNKNOWN] and give the user a manual export path. Never claim a full archive you did not verify.
Folder: archive/<Bot>-<YYYYMMDD-HHMM>/ under the archive root set in Phase 0, with transcript.jsonl, MANIFEST.md, SHA256SUMS.txt.
Recency: use the newest timestamped folder per bot. Ignore older copies and never delete them.
MANIFEST: bot name, bot id, message count with the per-role split, date range (with zone), redactions made, archived-by.
Message count = every line in transcript.jsonl (user + assistant + tool rows).
No history: a bot with zero messages gets a MANIFEST with count 0 and range "none", and passes if the bot confirms it's empty.
Verify: sha256sum -c passes. Line count = message count = the rows the transcript reader actually returns (not its header total). Range starts at the bot's first message and ends at or after the bot's last activity before archiving.
Known reader quirk: the header can report one more position than the rows it shows (a hidden non-message entry). Log the header/shown gap in MANIFEST as a reader quirk, not a failure. Any gap between the rows shown and the rows exported fails.
Date range: take it from timestamps inside the rows if present; otherwise use the folder time and mark the range [UNKNOWN].
If the bot id in MANIFEST doesn't match a current bot, the archive counts as its predecessor's once that old bot is deleted. Note this in the verify result.
Scan for secrets (token, key, password patterns) and personal data. Redact copies leaving this computer. Tell the user what to rotate, never the value. A bot whose scan isn't done is not PASS.
FAIL = re-archive with -r2 (then -r3). Never overwrite a verified archive.
Gate: no copies or relabels until every bot in scope is PASS (or removed from scope by the user).
Stop: show the per-bot table, "Reply YES to continue."
