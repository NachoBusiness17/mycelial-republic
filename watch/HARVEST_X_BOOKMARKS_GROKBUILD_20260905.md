# HARVEST — X BOOKMARKS VIA GROK BUILD (Sep 5, 2026)

*Operator: bookmark folder 1876313041077145771 — "can you harvest all these? and their
subthreads and comments? use grok build cli, output to a file you can read, with its
trajectory and shit, verbose mode, dogfood style."*

## WHAT RAN
grok build CLI 1.0.13 headless (`-p` one-shot, `--always-approve --max-turns 80`), capturing
its OWN vendor envelope while it worked: **trajectory_stream.ndjson (2.1MB)** +
**trajectory_debug.log (3.5MB)**. Grok built its own tooling mid-run (_chrome_folder.py,
_cookie_copies, _copy_locked.py, _build_harvest.py — 40KB of harvest scaffolding) and wrote
the wall ledger itself. 15 minutes wall-clock.

## THE TRAJECTORY ENVELOPE (first read — second vendor format for the thought-bank)
1,254 thought events · 859 text events · 109 tool calls · 39 usage events · 1 plan · 1 end.
`thought` is a first-class streaming event type in grok's ACP wire — the FT-001
frontier-thinking-ingest law applies verbatim: grok's thinking deltas are harvestable
verbatim, same as the z.ai export. Two vendor envelopes now in the bank (z.ai, xAI).

## HAUL (honest)
- **8/11 known items** — root texts complete via fxtwitter (200 OK each). Includes the
  operator's own Riddler Protocol tweet (receipt: "Every AI but mine i feed it flat out
  refuses to think about it") and the Alex Finn Omarchy/Hermes OS-integration thread.
- **Reply trees:** 4 complete, 4 partial (32/185, 13/22, 22/109, 21/64) — capped by
  grok's x_thread_fetch/x_keyword_search 10-per-query tool limit, NOT by a wall.
- **3 items unharvestable:** scout items 9–11 from 09-04, URLs never filed.

## THE FIVE WALLS (grok's own ledger, verified)
1. Live folder listing = **login wall** (private bookmarks; logged-out shell rendered).
2. Operator Chrome cookies = **file lock** (Chrome open; sharing violation; it did NOT kill
   Chrome — correct).
3. X OAuth on disk = **wrong account** (@GHOST_HANDLE, not @NachoQuixotic) + dead token +
   scope lacks `bookmark.read`.
4. CDP 9222 = **Docker Desktop squatting the port** (it refused to steal the port —
   docker-not-desktop law respected).
5. fxtwitter fetches the public roots fine; private folder enumeration is the only true wall.

## WHAT UN-WALLS IT (operator hand, one pass)
Either: (a) close Chrome once → grok re-runs the cookie-copy door with the real
@NachoQuixotic session; or (b) mint an X API token with `bookmark.read` on NachoQuixotic and
drop it in the fuel state; or (c) scroll the folder once on screen while a capture runner
watches — the phone-runner pattern. Then re-run the SAME prompt: the tooling is on disk, the
second pass only enumerates + fills the reply trees past the 10/query cap (fxtwitter
conversation endpoints per reply).

## DOGFOOD NOTES
- The prompt pattern (harvest + no-fabricate + no-stop + wall-ledger) worked first try;
  grok self-organized 5 doors and 4 scaffold scripts without further steering.
- Its envelope joins the trajectory program: same lens, second vendor — duplication is
  emphasis, and the envelope grammar now has two independent witnesses.
