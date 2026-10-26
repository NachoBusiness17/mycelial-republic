---
name: delete-label-protocol
description: "Use in Roster Swap Phase 5 and before handing over any delete list."
---

# Delete-label protocol (Phase 5, list for Phase 9)
- Bots can't delete bots. The user deletes from the sidebar.
- Before assigning numbers, scan ALL bot names for D## numbers already in use, including hidden bots and ones only the roster manager can see (ask the roster manager for the highest number in use). Your own teammate list may be incomplete. Also check the record of numbers already used (the roster manager's log and past PROGRESS.md / CLOSE-OUT files), because deleted bots no longer show their numbers. Start at the highest number from either source + 1. Never reuse a number, even after a rollback.
- After YES, the user or their roster manager renames each old bot (Roster Swap only guides) to "D## DELETE <old name>" (two digits or more, zero-padded, sequential).
- Collision: if a name is already taken, or the rename fails, stop, rescan and take the next free number. Record it in PROGRESS.md.
- After the rename, re-read the actual names. If the roster manager used different numbers than planned, record the real ones and use those in the delete list.
- Rooms can't be renamed: list them by current name, with the bots in each, and say which bots to remove or re-add to the new copies.
- Rename before handing over the list. Never give an unmarked delete list.
- Only release the list once archives are verified, routines confirmed and the handoff is done.
Check: every old bot shows its D## name and the new copy answers. Stop: show the list, "Reply YES to continue."
Rollback: rename D## DELETE <name> back to <name>. The number stays retired.
