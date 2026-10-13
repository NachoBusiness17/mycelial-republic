# CFMBT v5 — Conflict-First Municipal Bond Transparency (public build)

A one-page conflict audit that answers three questions in ten minutes:

1. **How much does this debt cost the General Fund per year?**
2. **Who was paid to advise or underwrite the issue?**
3. **Did any covered official, vendor, or family member self-disclose holdings above the threshold?**

…while refusing to publish a live list of natural-person bondholders. The
market was never built to produce one, and privacy law will not permit it.
Decision-speed conflict file + fund-level sunlight + threshold self-disclosure
— that combination is the product.

## Read it

Open `app/index.html` in a browser (serve the folder, or open directly — the
page degrades to placeholders with `not-proven` chips when `data/case.json`
cannot be fetched). Print-ready: every section survives print with the same
scores.

## Honesty labels

Every field carries **we-have-a-record / not-proven / people-disagree** and a
basis of **Evidence / Inference / Assumption**. Primary record beats
commentary. Software never auto-truths. Blank is allowed; invented complete is
not. Forecasts are labeled Forecast, never Record.

## Local bind (host only)

`app/` reads `data/case.json`. The public copy ships with nulls. Local names
and live figures live in `local/bind.json` **on the host only** — not in this
tree, not committed, not shared. Until a bind exists, every figure reads
`{{PLACEHOLDER}}` + `not-proven`.

## Tree

- `app/index.html` — the one-page audit (4 sections, print-friendly)
- `app/styles.css`, `app/app.js`
- `data/case.json` — the case, nulls in the public copy
- `data/sources.json` — every source: url, retrieve date, score, basis
- `data/schema.json` — field list, allowed scores, amount bands
- `forms/self-disclosure.md` — the one-page sworn statement
- `legal/privacy-posture.md` — CJEU / Tower / KYC boundaries, over-collection control
- `conversation/beats.md` — the six spoken beats

## The three pillars

- **A — Decision-speed conflict file.** The vote, the contract, the yearly
  General Fund hit, the advisor/underwriter/counsel file, G-17 excerpts —
  public at the vote or assembled from the public record immediately after.
- **B — Fund-level sunlight.** CUSIPs, registered owner (Cede & Co., nominee
  of DTC), EMMA trade snapshot, public fund filings. Never a natural-person
  holder list.
- **C — Threshold self-disclosure.** Covered persons swear Yes/No + amount
  band at issuance, at material amendment, and annually. Non-response
  publishes. Enforcement: existing ethics-commission penalties.

## Method statement (public)

The county borrowed in public and pays from the General Fund in public.
Current lenders sit behind a book-entry market built in the 1980s and 1990s.
Sunlight that matches the speed of county government is the vote, the yearly
payment, the advisor file, and a targeted conflict rule — not a claim that
nothing is known until every bond fund is named.
