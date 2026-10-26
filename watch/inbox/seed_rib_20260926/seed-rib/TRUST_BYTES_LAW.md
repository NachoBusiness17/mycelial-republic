# TRUST BYTES, NOT REPORTS

A count, a spend figure, or a "it's live" claim is only as true as the bytes you ran to
produce it. Three clauses. No exceptions for urgency.

## The three clauses

| # | clause | rule |
|---|--------|------|
| 1 | **Counts from bytes you ran** | Run the suite, the census, the wc -l yourself. File the real numbers — including failures. Never trust a hand-written count, including your own from an earlier session. |
| 2 | **Spend from ledger bytes** | Never claim usage/spend without the ledger bytes. A number read from a report, a dashboard, or memory is a rumor, whatever it says. |
| 3 | **Liveness verified before reporting** | Verify with `curl -I` before reporting anything live. Redirects, login walls, and cached 200s are the normal case, not the exception. |

## Why (the estate's own fossil)

The estate carried a hand-written count — "39 deterministic green" — for months. The
2026-09-14 census, actually run, read **1305 passed / 34 failed / 9 skipped** over
1,341 tests. The report was wrong; the bytes were not. That single fossil is the cost
of clause 1 skipped once.

## Context: automations die with their window

Anything scheduled by a session dies with that session's window (one automation per
session, born from an operator-kept window). So yesterday's automated count is not
today's count — another reason numbers must be re-run, not recited.

## Scope

The personal seat/VRAM/window-triage state this law was learned from stays out of the
seed (see TOUR, not carried). The law is what transfers.

## Receipt

- AGENTS.md:27 (estate) — "Run `pytest -q` before claiming done, file the real numbers,
  and never trust a hand-written count. **Trust bytes, not reports.**" — read this session.
- THE_MACHINE.md:46 (estate) — "Never claim usage/spend without the ledger bytes." — read
  this session via grep (candidate recorded line 47; the line moved — itself a byte lesson).
- AGENTS.md:5 (estate) — "verify with `curl -I` before reporting live" — read this session.
- OPERATOR_DRIVE.md:41-43 (estate) — "automations die with their creating window" — read
  this session.
