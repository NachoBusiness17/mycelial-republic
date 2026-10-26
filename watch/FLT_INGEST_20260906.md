# FLT INGEST RECEIPT — primary sources preserved 2026-09-06

The day the fleet's research stack gained a machine-checked Fermat.

## Preserved locally (this folder)

- `anthropic_flt_paper.pdf` — 181,893 bytes, PDF 1.7, Anthropic's "Formalizing
  Fermat's Last Theorem" paper (excerpts of Claude's reasoning released as PDF).
- `SOURCES.md` — primary numbers, quotes, and full URL list from the ingest pass.

## The verified facts (tri-state, from primary + named independent sources)

- **SUPPORTED (Anthropic research post + paper):** Claude worked "largely
  autonomously over 11 days"; 13M lines of Lean ("over 5x the size of Mathlib");
  30,300 theorems proved en route, 29,500 used in the final proof; ~6B output
  tokens from an internal research model ≈ Claude Fable 5.1; human math input
  "limited to occasional high-level instructions from Tianyi"; failed early agent
  attempts still contributed ~7% of non-boilerplate lines; platform = Prove2Me
  (Columbia group, DAG of theorem statements, statements split from proofs) +
  "a Claude Code-based multi-agent harness."
- **SUPPORTED (Lean kernel + comparator):** checked by Lean on three standard
  axioms, no `sorry`; comparator confirmed the statement matches Mathlib's own FLT
  statement. Buzzard reviewed; manually inspected every non-mathematical line;
  OpenAI models separately audited Lean and found no soundness issues.
- **SUPPORTED (Buzzard/Xena):** closes Wiedijk's 100-theorems benchmark (the last
  item); follows the 1995 Darmon–Diamond–Taylor exposition, not the modern proof;
  the Frey-curve gap is patched by the earlier flt-regular formalization
  (regularity hand-proved only for 3, 5, 7, 11, 13); "adds nothing" mathematically
  — the significance is autoformalization capability. His own human-led modern-
  proof project (ImperialCollegeLondon/FLT, R=T, blueprint) CONTINUES — do not
  conflate the two (the lean-lang.org page is his, not Anthropic's).
- **Public artifact:** github.com/anthropics/formal-math — self-contained Lake
  projects, toolchain pinned; one secondary source describes the public artifact
  as ~25k lines of distilled Lean + ~1.1k theorems/definitions + LaTeX blueprint
  (the distilled proof, vs the 13M-line full run). [UNVERIFIED split — check at
  clone]
- **Known gap (named, not hidden):** the **semantic review gap** — the kernel
  verifies derivation, not whether the statement means what mathematicians think
  it means. Buzzard's comparator + human review is the semantic half. This is
  LAW-061's frontier form: kernel-valid ≠ intent-valid.

## What it enables for THIS stack (the commission's answer)

1. **A zero-label-noise corpus** — 13M lines where every line is kernel-verified:
   the label IS the checker. Perfect training/eval material for
   verification-capable models on Rocinante; no human annotation anywhere.
   [SUPPORTED — artifact public, license-check at clone]
2. **cite_gate gains an artifact class that carries its own verification** — for
   machine-checked claims the citation check becomes "re-run the kernel," and the
   remaining human job is exactly tri-state's: does the statement mean what it
   claims to mean? [SUPPORTED as mechanism; UNPROVEN as pipeline until built]
3. **The verification-asymmetry pattern formalized** — Collatz row (announcement,
   no artifact, held at the door) vs FLT row (artifact + kernel + independent
   witnesses, waved through) on the same shelf, same day. The falsifier culture's
   two-row proof of itself. [SUPPORTED — both rows filed today]
4. **Wiedijk's 100-theorems benchmark is CLOSED** → a ready-made eval set: 100
   classic theorems, all formalized, ground truth by kernel. [SUPPORTED]
5. **The Vinogradov door** — Anthropic formalized Vinogradov's Three Primes
   Theorem in 3 days on 3 consumer Max plans, calling collaborative formalization
   with consumer subscriptions "achievable." The fleet runs consumer plans.
   [SUPPORTED as demonstrated by Anthropic; UNPROVEN for us until a theorem is
   chosen and the free lanes fire Prove2Me-style. ROCINANTE-prep proof-of-genre.]
6. **Buzzard's bottleneck is the market gap** — "mathlib won't accept AI reviews
   and reviewers avoid AI-generated code," so large AI corpora live as standalone
   repos "slowly upstreamed." Machine-checkable claims piling up with no review
   path = precisely the compiled-wiki + mechanical-verification + semantic-triage
   shape the fleet already is. [SUPPORTED as his stated bottleneck; our-fit
   UNPROVEN until tried]

## Doors (one word each)

- **FORMALIZE** — pick a Wiedijk-list theorem, fire the consumer lanes Prove2Me-
  style (the fleet's first formalization; $0 on promo pools).
- **CORPUS-PULL** — clone anthropics/formal-math, license-check, ingest into the
  eval lane (FLT-derived proof/repair cases with kernel ground truth).
- **DONE** — this receipt stands as the ingest.
