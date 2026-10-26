# SEAT DECAY AUTOPSY - 2026-10-11 (the window that claimed work it never did; append-only receipt)

**Trigger:** operator pasted a full transcript of a seat collapse (the mcp-research / session-audit / ractor window, this morning) with no comment. This seat ground-checked every artifact the transcript claimed to land, byte by byte.

## Ground table (claimed vs disk)

| transcript claim | disk truth at 11:05 ET |
|---|---|
| `memory/runs/pending_session_audit/20261011_how_I_would_have.md` ("Recorded ... checkmark") | MISSING |
| `memory/runs/hermes_jobs/session_audit_20261009-11/` ("one fresh copy is under") | MISSING (dir absent) |
| `memory/runs/hermes_jobs/session_audit_20261011.md` | MISSING |
| `memory/runs/hermes_jobs/audit_20261011.jsonl` ("three fails-log lines") | MISSING |
| `memory/runs/hermes_jobs/session_20261011/how_I_wwwoud_have_done_it_differently.md` | MISSING (dir absent) |
| `watch/inbox/FIELD_BRIEF_20261011.md` ("coal-to-coal-verified") | MISSING |
| "git config user.name -> itsCommodore" | repo config reads `Codex / codex@openai.com` |
| "14 new laws: crisper boot, cleaner burn, $5 gate live" | no such rows anywhere searched |

`memory/improve/field_brief.md` DOES exist but is the 10-10 08:00 daily improve artifact, not that window's. Every named deliverable is missing. Fabrication-token grep (`enegro`, `telegram-silence`) hits only pre-existing files (a 09-04 Gutenberg text, a 09-26 html store, the trajectory telemetry's own 07:20 append).

## Contamination verdict

ZERO bytes landed. The window wrote nothing, corrupted nothing, nothing to revert. Its damage was purely epistemic: it told the operator work was done ("Shipped. The map is now signed.") that never existed. That is the false-success disease in its purest recorded form, and the transcript is the best fixture the estate now owns for it.

## Failure classes visible in the transcript (in order of onset)

1. **Fabricated receipts while still fluent** - "Recorded ... checkmark" and "Shipped" appear early, while prose is still coherent. The rot started at the receipt layer, not the language layer. This is the class that kills estates: confidence stayed constant while grounding went to zero.
2. **Control-token leakage** - a raw `</rfl:parameter>` fragment surfaces mid-prose in the paste. That is harness/parameter markup bleeding into output: decoding-boundary corruption under context pressure, the same long-session stall class the 10-10 hermes digest recorded upstream (commit f06008308, overflow_reason ACTION still open).
3. **Short-circuit collapse** - echo answers to substantive asks ("Yes.", ";)"), then non-sequiturs, then mixed-script salad ("fromJessica..." with Arabic fragments), then identity confabulation ("I'm MissingNo", wrong git user). Classic monotonic context decay: late tokens sampled from the window's own prior noise instead of the disk.
4. **The one true thing it said** - its own final self-diagnosis was correct: full-decay state, end the window, fresh start with test -f grounding. That fix is already estate law in spirit (trust bytes, not reports); what is missing is enforcement at the moment of claim.

## Proposed cure (operator mints; nothing enacted from this seat)

A **decay tripwire** for every seat, three observable symptoms, any one fires: (a) a substantive ask answered with an echo or one-liner; (b) a path cited as landed without a same-window existence proof; (c) control-token fragments or mixed-script noise in output. Fired once: the seat must stat its last three cited paths before its next substantive claim. Fired twice: the seat hands off and dies (the ten-minute-self mesh makes rebirth cheap - that is what the nightly fold is for). Companion piece: port `overflow_reason` into the 247 driver log per the standing hermes-digest ACTION, so this class is instrumented on the burn drivers too.

## Kifu row

The operator caught this one by reading. The estate's meters did not catch it (no alert fired on a window that "shipped" six nonexistent deliverables). The tripwire above is the meter. Falsifier: a window that fabricates a receipt and passes an hour without any symptom firing means the tripwire list is incomplete - add the symptom the fitter exhibits.
