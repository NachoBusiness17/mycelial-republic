# SOURCES — FLT ingest, 2026-09-06

## Primary

1. **Anthropic paper (PDF, preserved as anthropic_flt_paper.pdf)** — excerpts of
   Claude's reasoning during the run.
   https://www-cdn.anthropic.com/9e431dff043da6538d99d6c2d231b670aa3da263.pdf
2. **Anthropic research post** — "Formalizing Fermat's Last Theorem."
   https://www.anthropic.com/research/formalizing-fermats-last-theorem
   Key numbers: 11 days, largely autonomous; 13M lines Lean (>5× Mathlib);
   30,300 theorems proved (29,500 used in final proof); ~6B output tokens;
   internal research model ≈ "Claude Fable 5.1"; human input = occasional
   high-level instructions from Tianyi ("Jacobian as a scheme sounds high
   priority"); failed agent attempts = ~7% of non-boilerplate lines; Prove2Me
   (DAG of statements, statements/proofs split) + Claude Code multi-agent
   harness; Lean kernel check, three standard axioms; comparator vs Mathlib's
   FLT statement; Buzzard review. Side result: Vinogradov Three Primes in 3 days
   on 3 consumer Max plans.
3. **Public repo** — github.com/anthropics/formal-math (self-contained Lake
   projects, pinned toolchains; secondary source: ~25k lines distilled + ~1.1k
   theorems/definitions + LaTeX blueprint + rendered docs [check at clone]).

## Independent witnesses

4. **Xena Project (Kevin Buzzard)** — "FLT: Anthropic has beaten me to it."
   https://xenaproject.wordpress.com/2026/09/04/flt-anthropic-has-beaten-me-to-it/
   13.4M lines, ~20× mathlib compile time, 11 days; closes Wiedijk's 100
   theorems; follows Darmon–Diamond–Taylor 1995 exposition; Frey-curve gap
   patched via flt-regular (regularity hand-proved only for 3,5,7,11,13);
   "adds nothing" mathematically; autoformalization capability is the news;
   expects less-painful refereeing and exposed hidden assumptions; his EPSRC
   project continues (mathlib PRs + modern-proof dynamic document); £1M/5yr vs
   11-days cost quip; manual inspection of every non-math line; OpenAI models
   audited Lean, no soundness issues; near-term: mathlib won't take AI reviews —
   standalone repos "slowly upstreamed"; next: Langlands paranoia-checking.
5. **lean-lang.org/use-cases/flt/** — NOTE: this is the HUMAN-led Buzzard project
   page (ImperialCollegeLondon/FLT, R=T via blueprint software, Khare-
   Wintenberger/Kisin modern proof, "high-quality training data for AI systems"
   as beneficiary) — separate from Anthropic's run. Two FLT formalizations now
   exist; do not conflate.
6. Coverage cross-checks: AlphaSignal, AI Weekly (30,300 theorem split), Superpower
   Daily ("semantic review gap" framing, dozens of agents via Prove2Me), daily.dev.
7. Anthropic on X: https://x.com/AnthropicAI/status/2095947707605266436

## Fleet internal cross-refs

- watch/PURPLE_HARVEST_TRIAGE_02_20260906.md (TRIAGE 16 — the original cite-gate
  pass) · watch/TRIAGE_HAUL_BOT_01_20260906.md (Collatz-vs-FLT shelf context:
  the Collatz announcement was held at the door six hours before FLT waved
  through) · watch/FLT_INGEST_20260906.md (this receipt's parent card).
