# STATE_BRIEF.V1 — the $0 boot brief

Orientation is **computed from state, never generated**. A seat coming back cold reads
one short brief that tells it where things stand — at zero model spend, deterministically,
on every boot.

## The contract

| element | rule |
|---|---|
| schema tag | first line carries `state_brief.v1` + a timestamp + the words "deterministic, $0" |
| section 1 — what's running | live loops (or their loud absence + the wake command), current goal, current status |
| section 2 — what's queued | queue total + live fleet count + the head entry (id, status, tag, goal) |
| section 3 — landed while away | recent arrivals (title + one bounded excerpt each) + last run summary path |
| section 4 — health | inbox pending, frustration total, auto-run flags |
| footer — transfer measures | the brief rates ITS OWN handoff quality (table below) |
| last line | the regen command |

## The transfer-measure block (what makes it honest)

The brief reports, about itself:

| measure | example value (the brief this seed was forged from) |
|---|---|
| rendered bytes | `1854` |
| freshness | `1914s` |
| chain root | `2fcda5356b9f1953` |
| cost | `$0.0` |
| LLM calls | `0` |

A reader can judge the handoff instead of trusting it: if bytes are tiny, freshness is
stale, or the cost is nonzero, the brief says so about itself.

## The law inside it

- Deterministic: same state → same brief. No model is asked anything, ever.
- Loud absence beats silence: "nothing is draining the queue" with the wake command is
  a section, not an error.
- Instance data is per-estate (the queue rows below the sections are yours to regrow;
  see TOUR, not carried).

## Receipt

- state/START_BRIEF.md:3-31 (estate) — read this session; example values above are its
  actual transfer measures. Regen footer verbatim: `python -m mag.state_brief`.
- The regenerator was not run by the candidate; this card ships the contract and the
  footer, both read directly.
