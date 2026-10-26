# garden-v1-kimi1-B2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

IMPROVEMENT 1: _GRANTED_EVENT_IDS is an in-memory set with no persistence, allowing replay attacks across process restarts | EVIDENCE: mag/switchboard_v2.py:56 | FIX: Persist _GRANTED_EVENT_IDS to disk and load on module init, or use TRAIL file for replay detection

IMPROVEMENT 2: _rewrite_inbox_rec has TOCTOU race condition on INBOX read-modify-write with no file locking | EVIDENCE: mag/switchboard_v2.py:320-335 | FIX: Use atomic rename with file locking (fcntl/lockf on Windows via msvcrt or portalocker) or SQLite for inbox storage

IMPROVEMENT 3: grant() adds to _GRANTED_EVENT_IDS after trail_append, so crash between trail_append and set-add allows replay | EVIDENCE: mag/switchboard_v2.py:228-230 | FIX: Add to _GRANTED_EVENT_IDS before trail_append, or use single atomic operation for both

DIFFERENT-BUILD: Replace JSON line files with SQLite for TRAIL/INBOX to get ACID guarantees, concurrent access safety, and queryable history without full file scans.
