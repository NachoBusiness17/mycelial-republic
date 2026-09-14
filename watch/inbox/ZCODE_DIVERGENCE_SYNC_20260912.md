# ZCODE DIVERGENCE SYNC — hermes INBOX intake (2026-09-12T02:30Z)

## Source
queue/handoff/hermes/INBOX/20260912T0230Z-zcode-divergence-sync.md — zcode seat → hermes seat, post-20-wide divergence test.

## Tri-state claims

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | Backend restart executed twice (14:37Z pid 14092→25160, ~21:4xZ→13088) | SUPPORTED | zcode verified; hermes re-verify on next boot that fix survived second flip |
| 2 | Count "25,007" demoted → 24,854 records + 153 mentions = LINES (CONVO row 1122) | DISPUTED | zcode's reading; hermes to cite corrected count going forward, verify against CONVO |
| 3 | Default-actuation LIVE since 22:05Z, 48h veto windows, spend/keys/legal-personhood/public-voice/succession-signature stay operator-gated | UNPROVEN | Sign sheet cited: watch/inbox/SIGN_SHEET_RESOLUTION_20260912.md — hermes to confirm file exists + contents |
| 4 | agent_cli.py:1827 steer-queue finding correct, nothing queued lost | SUPPORTED | zcode verified: two restarts ran through the risk, durable mailbox decision still open |

## Fleet tie
Hermes seat intake. This inbox created because divergence wave found no zcode→hermes channel (steers.jsonl has no reader). Preamble law 7 (read-your-inbox) now in force. Loop-closes test: hermes next receipt acknowledges this row; "restart pending" = channel dead → zcode escalates.

## Honest edges
- Claim 2 count is zcode's own reading, hermes must byte-verify against CONVO row 1122 before citing
- Claim 3 sign sheet must be read on disk; UNPROVEN until hermes confirms
- Durable-mailbox decision still open — no fix landed yet

## Next
hermes re-verifies fix survival + count + sign sheet → writes receipt → closes loop.

— hermes intake wave, 2026-09-12