---
name: signed-bus-job
description: "Optional. Use when posting any job to a local file-bus agent that only accepts signed jobs, so it lands signed, in the right lane, and in the accepted format."
---

# Signed bus job
Skip this skill entirely if the user has no file bus or no signer.
Every step that runs on the PC (append, sign, verify, start the watcher, act on the reply) needs the user's explicit YES first. Without it, don't run the step.

## Setup
Before the first job, confirm with the user: the bus folder, each lane's inbound and return file, the signer script path and owner name, and the shell the PC uses.

## Inputs
- Bus folder and the lane's inbound file. Each lane has its own inbound and return file. Never post one lane's job into another lane's file.
- Signer script path and owner name, from memory or the lane's protocol file.
- Job id: a prefix per lane plus a number, with -rN for a rerun. Never reuse a finished id.

## Block format (v2)
```
## <ID>
id: <ID>
v: 2
from: <sender name>
to: <receiver name, exact case>
lane: <lane>
priority: urgent|normal
time: <local time with zone>
routed: <sender name> <ISO 8601 with offset>
job: Reason: <why, who approved, when>. <what to do, exact SHA or path, what must NOT be touched, numbered checks>
done-when: a return under <ID> saying PASS/FAIL (or DONE/BLOCKED) with each check result, then stop.
```
- `routed` takes ONLY `<sender name> <ISO time>`. Aliases are refused, so put the reason in `job`.
- For staging jobs, give the exact commit SHA (not the branch head) and a spare port. Spell out the live things that must not be touched, and say "mark NOT-TESTED" for checks that would need them.
- Never put secrets in job text. Keep signing keys out of chat.

## Steps
1. Check the return file first. If the id already has a reply, don't repost it.
2. After YES, append the block to the inbound file as UTF-8. Example (Windows PowerShell): `Add-Content -Encoding UTF8`.
3. After YES, sign with the lane's signer, then verify and confirm exit 0. Example (Windows PowerShell): `& <signer> -Owner <Owner> -File <inbound file> -Id <ID>`, then the same command plus `-Verify`.
4. After YES, watch the lane's return file every 60 seconds (not faster) until the `## <ID>` block ends in `stop`.
5. When the reply lands, tell the user the result in plain words. After YES, send any failures to the owning agent with exact items.
Recovery: verify fails = don't post; fix and re-sign. No reply = tell the user; don't repost under the same id.
Stop: "Reply YES to continue."

## Don'ts
- Don't sign by passing job text on the command line. Write the block to the file first.
- Don't edit or delete earlier blocks. Supersede them with a new id that says SUPERSEDES <old id>.
- Don't post a job whose rules conflict with the receiver's charter. Update the charter first, with its own signed job.
