# B2-269 receipt: opencode serve arm-or-decline (2026-09-26)

## Verdict

DECLINED, consciously and on the record. The opencode serve daemon (1.18.23, port 4096 loopback) will NOT be armed through the window. Rationale on bytes: the free lane behind it is client-locked (403 FreeTierError either way, the B2-261 receipt's own "the task buys state history, not lane access" finding), so serve=up would change rows from "serve=down (refused)" to "serve=up but 403" while adding an always-running daemon serving a closed free lane plus a second delete-at-close cleanup obligation. State history continues regardless: the armed MagMimoWatchHourly task (B2-261, landed ARMED) records the honest serve=down row on every fire (latest 2026-09-26T19:58:13+00:00, refused class). End-of-life binding: there is nothing to remove (no daemon was started, no scheduler entry created); the falsifier's decline arm is satisfied by this receipt.

## Evidence file:line quotes

- tools/mimo_watch.py:67: `SERVE_BASE = "http://127.0.0.1:4096"  # hardcoded loopback: the transport itself, no input ever reaches this string`.
- watch/inbox/mimo_watch.jsonl tail (this lane): "2026-09-26T19:58:13+00:00 | serve: down | status: None | err: <urlopen error [WinError 10061] No connection could be made" (plus 15:15:48 and 15:18:49 rows; the row 7 WinError 10061 the brief cites continues).
- curl probe this lane: `http://127.0.0.1:4096/` -> 000 (serve down right now, matching the rows).
- opencode --version -> 1.18.23 (the binary the brief names; present, not armed).
- watch/inbox/burn_wave_20260926/QUEUE.md:362 (B2-261 row, landed tail): "ARMED: MagMimoWatchHourly installed + paired MagMimoWatchClose delete-at-close 21:25Z bound in same decision" and "the probe stays 403 either way (FreeTierError client-lock, B2-236 battery ...), so the task buys state history, not lane access".
- MagMimoWatchClose task XML (this lane): Arguments = `/c schtasks /delete /tn MagMimoWatchHourly /f & schtasks /delete /tn MagMimoWatchClose /f` (close-half cleanup exists for the watch; no serve daemon referenced, consistent with this decline).

## Work done

1. Measured the live state (serve down, curl 000; watch rows serve=down with the refused error class from B2-307's spec) and confirmed the binary exists (1.18.23) so the decline is a choice, not an absence.
2. Read the paired B2-261 decision (ARMED watch + delete-at-close 21:25Z) and its 403-either-way finding; took the coordinated decision this brief asks for: the watch half is armed, the serve half is declined, one covers the other's gap.
3. Verified the close-half task touches only the two watch tasks, so the decline leaves zero cleanup debt at window close 2026-09-28T21:19Z.
4. No daemon started, no scheduler entry created, no code changed.

## Falsifier

The brief's falsifier, both arms now closed: (a) "a serve=up row lands after 2026-09-28T21:19Z with no decline receipt" - the decline receipt now exists (this file), so any post-close serve=up row would additionally violate THIS receipt and must be treated as an unauthorized daemon: kill it and file an incident; (b) "every row until close reads serve=down with neither arm nor decline filed" - rows may keep reading serve=down because the decline is now filed; the remaining watch behavior (rows continuing to close) is owned by MagMimoWatchClose's own delete-at-close. If serve is found running before close without a superseding receipt, this decline is void and the arm half becomes a same-day obligation.

## Bibliography closed

All read this lane: tools/mimo_watch.py (SERVE_BASE, window-close block 110-125, OUT/LEDGER paths), watch/inbox/mimo_watch.jsonl (tail rows), QUEUE.md rows B2-269 and B2-261 (landed arm decision), MagMimoWatchClose + MagMimoWatchHourly task XML, opencode --version, live curl probe of 127.0.0.1:4096.
