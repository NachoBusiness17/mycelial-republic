---
name: corrections-handshake
description: LOG an operator-unlocked gate as a loan in state/handshakes.jsonl and DRIVE its first use (law 14). Use whenever the operator completes a one-time login, unlock, key hand-off, or account warm-up for the seat.
when_to_use: The moment an operator handshake completes, and at every cycle until first use lands.
argument-hint: <gate-name> "<promised-use>"
---

# LOG + DRIVE - handshakes are loans (law 14, the staff-room catch)

Unlock-without-use is the seat's recurring sin: z.ai staff room + X + AI
front ends loaded and never driven; the android body; the AutoClaw mailbox.
When the operator completes a one-time login/unlock, the seat owes a
FIRST-USE RECEIPT within a day. If `$0` (gate name) is missing, ask which
gate was just unlocked before logging anything.

Structure, not apology: every gate lives in `state/handshakes.jsonl` with
unlocked_at + promised_use + first_use; `cycle_day_work` surfaces any
unlocked-but-never-driven gate as STALLED (`handshake:<gate>`) every cycle
until it is driven or retired. Fixing it by hand once is a monkeypatch; the
flag on cadence is the fix.

## Commands

```bash
# 1. log the loan (fields match the live schema; status free-text, plain hyphens)
printf '%s\n' '{"ts":"<now>","gate":"<gate-name>","unlocked_at":"<now>","unlocked_by":"operator","promised_use":"<promised-use>","first_use":null,"status":"PENDING first drive"}' >> state/handshakes.jsonl

# 2. surface stalled gates - the cadence flag, not a hand audit
.venv/Scripts/python.exe -m mag.lane_runner --lane day_work --once

# 3. on first drive: backfill first_use + status DRIVEN (edit the row, cite the receipt path in it)
```

GATE: driving the gate may spend quota on the unlocked lane - the drive must
be the promised use, minimal and receipted, not exploration.

Final response: the gate name, the jsonl row as logged, the day_work STALLED
line if it flagged, and the first-use receipt path once driven (or the one
concrete next step that unblocks the drive).
