# FW-31 — Sep-20 demo script (operator gate packet; DATE-STALE disposition inside)

- Board item: `watch/inbox/FIFTY_WIDE_BOARD_20260917.md:57` — "bones referee on-air rehearsal plan + fallback if clicks land late"
- Directive source: `watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md` (the referee-on-air goal)
- Packet filed: 2026-09-28, Q-025 queue gopher.

## 0. Disposition first: the date is stale — recommend DROP-AS-SCHEDULED, RESCHEDULE-ON-CLICKS

- The event date passed 8 days ago. Verified 2026-09-28: 2026-09-20 was a SUNDAY
  (`date -d 2026-09-20 +%A` -> Sunday); today is Monday 2026-09-28.
- No demo receipt exists. The 09-27 queue-field audit already grepped watch/inbox and found none,
  nearest hit `SACRED_COW_AUDIT_SEP20_20260918.md` (an unrelated audit that merely shares the date)
  — `watch/inbox/BURN_queue-field_20260927.md:13`. This packet re-checked and found nothing newer.
- The queue-index roam verdict pre-registered exactly this fork: "should be confirmed dropped or
  rescheduled when the operator takes the bundle" (`queue/queue_index.jsonl:25`).
- Recommendation: mark the Sep-20 date DEAD (one word from the operator confirms it; the word is
  "dropped" or "reschedule"). The demo itself stays alive as a standing 15-minute rehearsal with a
  new trigger: **the two FW-30 clicks landing** (`watch/inbox/fifty_wide_20260917/FW30_discord_runbook.md`).
  No calendar commitment needed — the runbook IS the reschedule.

## 1. What the demo is (unchanged from the directive)

A stranger with a phone watches one end-to-end proof (HERMES_DIRECTIVE_BONES_REFEREE_20260916.md
"Why" section): human types in Discord -> Mag bot receives -> proposal goes to the deterministic
bones referee -> verdict receipted and replayable -> receipt lands on the durable surface.
Surface: `/bones start`, `/bones move`, `/bones status`, `/bones receipt` (+ `/bones verbs`) live
in #game-c-overview on NT-ACv2 (directive "THE ONE ARTIFACT" + D20_BONES_ADAPTER.md).

## 2. Chain status today (what this packet executed, 2026-09-28)

| Check | Command | Result |
|---|---|---|
| Session runner file exists | `ls mag/wow_bones_session.py tests/test_wow_bones_session.py` | both present |
| Referee session-runner tests | `./.venv/Scripts/python.exe -m pytest tests/test_wow_bones_session.py -q` | **11 passed in 0.80s** |
| Adapter dry-run | `./.venv/Scripts/python.exe -m mag.bones_adapter --check` | **EXIT=0**, 5 subcommands registered, guild 799817554549800982 / channel 1050760558883913780 |

Scope note, reported as what it is: the 11-test run covers the session-runner file only; the
09-17 handoff's "69 pytest + adapter green" claim spans the full referee chain (multiple files)
and was NOT re-run by this packet (`watch/inbox/HANDOFF_GOODNIGHT_20260917.md:11`).

## 3. The rehearsal plan (on-air script for the rescheduled date, ~15 min)

Preconditions: both FW-30 clicks done (token rotated, channel granted); gateway green.

1. **T-10 min, dry:** `.venv\Scripts\python.exe -m mag.bones_adapter --check` (expect EXIT=0).
2. **T-5 min, live:** `.venv\Scripts\python.exe -m mag.bones_adapter` in a terminal you can watch;
   wait for the guild sync line, bot shows online in #game-c-overview.
3. **On air, determinism beat:** `/bones start seed:20260928` -> play 3 legal moves via
   `/bones move <verb>` (discover legal verbs with `/bones verbs` if needed) -> `/bones receipt`.
   Save the receipt JSON it returns.
4. **The replay proof (the directive's own falsifier, live):** `/bones start seed:20260928` again
   -> play the SAME 3 moves -> `/bones receipt`. The two receipt sha256s must match
   byte-for-byte (HERMES_DIRECTIVE_BONES_REFEREE_20260916.md "Determinism falsifier": same seed +
   same moves -> byte-identical receipt; any difference = the directive failed).
5. **The divergence beat (optional, one command):** replay with one moved flipped ->
   receipt must name `RNG_DIVERGE` at the exact draw index (directive "Divergence falsifier").
6. **File:** drop the two matching receipts (or their sha256s) into a dated receipt under
   `watch/inbox/` — the "receipt lands on the durable surface" leg of the proof. An illegible or
   missing receipt fails the demo even if the chat looked good.

## 4. Fallback if the clicks land late (the board's "fallback" leg, updated)

- The demo degrades gracefully to **on-glass instead of on-air**: run the same beats 3-6 against
  the kernel CLI locally (`python -m mag.wow_bones session ...`, per the directive's session
  contract) and screen-share or paste the two receipts. The determinism proof survives; only the
  Discord leg (the "stranger with a phone" part) waits on the clicks. Date the fallback receipt
  honestly: "referee proof, Discord leg pending FW-30 clicks".
- If the operator says "dropped" instead: tombstone this packet's section 0 word into
  `queue/todo.md:151` and let the /bones surface live or die with the FW-30 clicks, whichever the
  operator prefers. No other work owes anything to the Sep-20 date.

## 5. What this packet did NOT do

No gateway boot, no Discord message sent, no live /bones session, no receipt minted. The pytest
run covered one file (11 tests), not the 69-test chain. Sep-20 itself is not claimed rescheduled —
that word belongs to the operator (one word: "dropped" or "reschedule").

Receipt: `watch/inbox/burn_reset_20260927/queue/Q-025.md` (FW-31 section).
