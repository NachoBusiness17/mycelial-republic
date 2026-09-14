# BOT B — CLAIM-EXTRACTION ENGINES (ELICIT / CONSENSUS / SCITE)

STEAL-BOT B, zero-shared-context wave, 2026-09-10. Sources: their own docs/blogs +
method pages + one independent teardown (Aaron Tay 2025 on Consensus). Public only.
Context: we surface "invariant" lines from our own corpus; we want a better truth-meter.

## THE POINT

These three tools all turn a paper pile into rows where every claim carries three
things: the value, the exact quote it came from, and a class (supports / contradicts /
neutral). The truth-meter part is mostly a cheap vote count over those rows — scite
counts who cites you against you, Consensus counts yes/no votes, Elicit just shows
cells and leaves the judging to you. What we are missing is the CONTRASTING signal:
scite's whole product is classifying disagreement, and our corpus has no disagreement
detector, only accumulation.

## MECHANISM TABLE

| Mechanism | How it works | Steal cost | Our current equivalent |
|---|---|---|---|
| SCITE: sentence-level citation classification | Parse full text of citing papers, extract each "citation statement" (the sentence containing a citation + context). A deep learning model, trained on 40k+ hand-labeled statements, classifies each into supporting / contrasting / mentioning. 1.6B+ statements classified at scale. Per-paper tallies = trust profile. | LOW-MED. Classifier is the only hard part; few-shot prompting of a local/free lane gets most of the value. No training set needed to start. | cite_gate.py verifies primary sources exist; nothing classifies whether a later card SUPPORTS or CONTRADICTS an earlier one. Percolator counts repeats but never counts refutations. This is our biggest hole. |
| ELICIT: column = one extraction task, cell = value + quote + reasoning | A column is a named field with an editable instruction prompt (a schema the user authors). RAG retrieves snippets per paper, LLM fills cells; every cell carries the verbatim source excerpt (clickable) plus the model's reasoning. No numeric confidence — audit is "show the why" + human edit + prompt refinement and re-run. Accuracy measured by sampling (internal 94-99% claims; independent eval found ~46% partial extractions on hard RCT fields). High-accuracy mode exists. | LOW. It is just schema + RAG + provenance fields. We already have the pieces (topic_index, grounding_wave hash-chain); we lack the per-cell quote + reasoning + prompt-version provenance. | Invariant lines land in cards and the tesuji/ground ledgers with evidence attached (tri-state), but there is no uniform cell schema — no fixed {value, quote, reasoning, extraction-prompt-version} row you can query or diff. |
| CONSENSUS: the meter as visible vote count | Yes/no question → retrieve top ~20 relevant papers → LLM tags each paper's finding yes / no / possibly / mixed → render the distribution (e.g. 94% yes / 6% mixed). Disabled under 5 relevant papers. Each vote is visible and clickable; per-category context shown (avg year, journal quartile, citations). Aaron Tay's verdict: vote counting, "not a mini meta-analysis" — the meter's honesty is that every vote is inspectable. | LOW. One classification call per paper over an existing retrieval set. The threshold rule (no meter under n<5) is a one-liner and is the honest part. | No agreement meter at all. When 8 night workers converge, disagreement is treated as the finding, but nothing computes "6 supporting / 1 mixed / 1 contradicting" across the corpus. |
| CONSENSUS: quality badges per vote (not per meter) | The meter itself does NOT weight votes. Quality lives one level down, as per-paper fields: LLM-assigned study-design badge (RCT / meta-analysis / cohort), sample size, population/methods/outcomes "Study Snapshot", journal-rigor tier (SciScore: top-50% / top-10% rigor criteria — randomization, blinding, sample-size justification), source-depth icon (title/abstract read vs full text read). The teardown's key flaw: n=50 counts same as n=5,000; effect sizes ignored. | LOW. Same shape as the meter, one field per claim row. The steal is the SEPARATION: agreement computed on unweighted votes, quality stored as per-vote fields so weighting is a later, explicit choice. | Tri-state claims (Supported/Disputed/Unproven) have no quality dimension. No notion of "this invariant is held up by 1 deep verified row vs 9 shallow cache reads" — though refeed_guard already computes depth for free lanes; the idea transfers. |
| SCITE: aggregated report schema | Per paper: counts of supporting / contrasting / mentioning citations, drill-down to each statement's sentence in context. Trust profile = ratio, not just a number. | Trivial once statements are classified — it is a GROUP BY. | topic_index.py (1,040 cards / 23 buckets) already indexes the corpus; a class+count roll-up over it is one reducer. |

## CLAIM ROW SCHEMA (what makes a claim addressable, merged across all three)

The three tools converge on one row shape. Union of fields:

```
claim_id            (stable key — our hash-chain anchor)
question / column   (what was asked; the extraction instruction + its version)
subject             (paper / card / knot the claim was extracted FROM)
value               (the extracted answer: number, class, free text)
quote               (verbatim source excerpt the value came from — non-optional)
reasoning           (model's stated why, shown next to the quote)
class               (supports / contradicts / mentions   OR   yes / no / possibly / mixed)
evidence_depth      (title+abstract vs full text — scite/consensus both expose this)
quality_fields      (design badge, sample size, rigor tier, year, citations — per vote, not per meter)
human_flag          (edited / confirmed / unreviewed — Elicit's audit loop)
```

The two fields WE lack and they all have: QUOTE (value without its verbatim source is
not addressable) and SOURCE-DEPTH (was the full text actually read — Consensus marks
it with an icon per result).

## TOP-3 STEALABLE MECHANISMS (ranked)

1. **Scite's contrasting-citation classifier, pointed inward.** Classify relationships
   between our own records: does card B support, contradict, or merely mention
   invariant line A? Truth-meter value is highest here because it adds the MISSING
   axis — percolator counts repetition; it never counts refutation. A tri-state row
   that upgrades on contradiction (Supported → Disputed) is the falsifier-friendly
   version. Cost: LOW — prompt a free-lane model per relation pair, start with
   few-shot, no training set. Falsifier: seeded contradictions in the corpus must
   flip the ratio; rotation across models must agree.

2. **Elicit's cell schema: value + verbatim quote + reasoning + prompt version.**
   Make it the required shape of every extracted claim row (invariants, tri-state
   rows, grounding batches). No numeric confidence — they don't fake it; they show
   the why and let a human or a re-run arbitrate. That matches our own law (tri-state
   with evidence attached) but Elicit makes the quote NON-OPTIONAL and version-stamps
   the extraction instruction, so bad-prompt batches are diffable and re-runnable.
   Cost: LOW — schema change, not new infra; fits hash-chained ledger as-is.

3. **Consensus meter with its honesty rules: unweighted visible votes, n<5 no-meter,
   quality as per-vote fields.** The steal is not the vote count — Tay shows vote
   counting is the weak part — it is the CONTRACT: never render an agreement meter
   under 5 relevant rows, show every vote, keep quality weights out of the aggregate
   and visible beside it. For us: "N of 13,678 knots support this invariant" only
   renders above threshold, each vote click-through to its quote, depth badges
   (full-read vs cache-read) beside it. Cost: trivial on top of steal #1.

## SOURCES

- scite QSS founding paper (methodology, 40k hand labels, 1.6B statements): https://direct.mit.edu/qss/article/2/3/882/102990 (via search summary; page 403'd on direct fetch)
- Elicit extraction mechanics + accuracy evals: https://intuitionlabs.ai/articles/elicit-data-extraction-clinical-papers
- Consensus Meter (official help): https://help.consensus.app/en/articles/10069920-the-consensus-meter
- Consensus teardown (Aaron Tay, Nov 2025 — meter = vote counting, SciScore, snapshots, flaws): https://aarontay.substack.com/p/a-2025-deep-dive-of-consensus-promises
- Consensus Meter intro (their blog, via search): https://consensus.app/home/blog/introducing-the-consensus-meter/
