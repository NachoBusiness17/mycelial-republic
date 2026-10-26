# THE BROWSERLESS GATE — broken-layer fix + chair ruling · 2026-09-22

**Operator order:** "fix it — summon lessig, elder and ponytail."

## The fix (landed, verified)

`mag/browser_driver.py::connect()` — the seat's gateway to the Playwright
browser — now carries the **browserless gate**: with the browser container
retired (docker stop, 09-22), every connect attempt returns a stated
degradation — `{"ok": false, "browserless": true, "error": "browser CDP
disabled — browser container retired 2026-09-22…"}` — instead of reaching for
a dead socket whose uncaught EPIPE killed the whole agent (the crash behind
34 lost backfill lanes: playwright node driver v24.18.1, EPIPE on write,
exit 1).

**Verified:** `connect()` returns browserless gracefully, no crash, syntax
clean. Seats now run browserless — web tools degrade to fetch-only — while
everything else keeps working. `MAG_BROWSER_CDP=1` re-enables when a browser
container returns.

## THE CHAIRS

**LESSIG (law):** PASS — the fix encodes the correct rule: *a missing
capability must degrade to a stated lesser mode, never kill the carrier.*
The error names the state and the remedy in the same sentence. Extend the
standard fleet-wide: every layer (seat browser, drainer spawn template,
container paths) degrades with a stated reason — one rule, three layers.

**ELDER (judicial):** the broken-layer arc closes with three receipts —
the browserless gate (this fix), the direct-to-API bypass (backfill completed
40/40, zero failures, ~$0.30), and loop-close (the 504-spawn suppression).
The standing rule re-affirmed: **capability loss is a mode, not a death
sentence.** Still binding from tonight's earlier ruling: meters read NOW;
LAW-HOLD is not REFLECTING.

**PONYTAIL (nameplate + GO list):** "browserless" is now a first-class house
word — a mode with a name, a reason, and a re-enable path. GO list refresh:
(1) Shadowbonk repair (full fault list filed — dead script, wrong boss array,
silent no-op upgrades); (2) graft pass on the 9 verified polish drafts;
(3) r05-games lane split re-seed (2nd strike — per-family lanes next);
(4) z_ai3 recharge (operator); (5) the two-build diff offer stands for AOS.

## Receipts

- EPIPE crash trace: failed task logs, logs/orchestrator (34 lanes, exit 1)
- Direct bypass: tools/backfill_direct.py — 40/40 batches, ~$0.30
- Loop-close: mag/ghost.py diagnosis-exists suppression
- Preflight-flat: mag/agent_cli.py nested-payload unwrap
- Fold v2: watch/inbox/FOLD_V2_DIRECTIONS_20260922.json — healing, zero rot

## THE IMPORT LAW (operator call: "that zcode import of claude shit fucked us")

Post-mortem on the day's breaks, attributed honestly:

- **Ours (pre-import estate choices):** the container-era spawn template (our own
  docker era), the unhashed constitution (our own filing gap), Shadowbonk's dead
  script (our own vis lab), the diverged backup remote (our own sync discipline).
- **Imported (harness/foreign defaults):** the Playwright browser layer whose
  socket EPIPE killed 34 seats (the harness's browser tooling — Claude Code
  lineage ships it), the pro-tier verifier default written by a foreign seat's
  checkpoint (Codex, Sep 14, 29,881-file sweep), deprecation-by-alias on
  provider model names we don't control (deepseek renamed under us).

**The law:** anything imported from a foreign harness gets a DEFAULTS AUDIT
before it runs — every default that spends money, spawns processes, or opens
sockets gets named, gated, and priced by OUR meters first. Imported convenience
is imported risk until metered. (Nothing-enters-untamed, applied to harnesses.)
