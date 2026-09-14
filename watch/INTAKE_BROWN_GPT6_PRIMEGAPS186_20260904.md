# INTAKE CARD — @polynoamial "GPT-6 ASTRA / SCIENTIFIC DISCOVERY" + openai/PrimeGaps186 (2026-09-04)

## ITEM
Operator tasking (verbatim): https://x.com/polynoamial/status/2095583211950833768?s=20 —
X post by "polynoamial" (Noam Brown — Libratus/Cicero game-theory/AI-reasoning
researcher). High-attention flag: primary-source researcher; full socratic depth.
Root post (@polynoamial, Sep 3 2026, 18:42 UTC, 120.8K views): "Of all the use cases
for GPT-6 Astra, I'm most excited for scientific discovery. We at @OpenAI have not
pushed it to its limits on math and science. I look forward to waking up every
morning and seeing what new scientific breakthrough someone has made with this
model!" — a FORWARD-LOOKING HYPE FRAME, zero claims in the root. The load-bearing
payload rode the reply layer: @scaling01 (Sep 4): "New OpenAI repo with a Lean
formalization by GPT-6-Astra proves that there are infinitely many pairs of
consecutive primes whose distance is at most 186 — github.com/openai/PrimeGa…"
(with screenshot). Amplifier: @weijie444 "GPT-6 Astra has pushed the prime gap to
186, with Lean formalization!" Plus an OpenAI blog ("Ten advances in mathematics
and theoretical computer science"), companion repo openai/ten-proofs, and paper
"Improved short gaps between primes" (Aug 30 2026, cdn.openai.com).

[SOCRATIC] Assumption attacked: "a frontier researcher's hype post about new math is
either (a) breakthrough news or (b) marketing — score it and file it." Instrument:
$0 primary-source reads — repo README fetched whole, search triangulation. What
survives: a real, self-honest, machine-checked CONDITIONAL result on a 12-year-stale
record. What dies: the tweet-level verb "proves ... at most 186" (the artifact
itself says conditional), and any clean "by GPT-6 Astra" attribution from the
primary artifact (repo carries ZERO attribution of any kind).

## RECEIPTS (consult-first, this turn)
- Root post fetched whole via web_reader (X wall did NOT block the root): text,
  timestamp, 120.8K views captured. THREAD REPLY LAYER PARTIALLY WALLED: web_reader
  returned root + truncated conversation; WebFetch on the status URL timed out
  (60s). scaling01 reply contents Supported via search-snippet mirror + Facebook
  mirror (xixidu post) — quote layer (RTs/quotes) UNSEEN.
- **FALSIFIER RUN (MEASURE step, $0): WebFetch github.com/openai/PrimeGaps186.**
  Primary-source receipt, whole README read:
  - Title: "Conditional Lean formalization and numerical certificate for prime
    gaps at most 186." Target: liminf (p_{n+1} − p_n) ≤ 186 via DHL[40,2] applied
    to an admissible tuple of diameter 186. Apache-2.0, openai org, single
    undated commit, Lean 4.34.0-rc2 / Mathlib pinned.
  - THREE CONDITIONAL HYPOTHESES as Lean axioms (namespace PrimeGap186):
    (1) kloosterman3_bound: |Kl₃(c;p)| ≤ 3 — README says it "follows from
        Deligne's theorem" via Katz 1988 (literature-backed, formalization debt);
    (2) kloosterman2_correlation_bound ≤ 8p√p — citing Fouvry–Kowalski–Michel
        2013 (literature-backed, formalization debt);
    (3) physical_integral_bounds: 104 outer + 45 inner numerical upper bounds
        + 3 cap bounds, backed by a Python certificate.
  - Axiom whitelist = the 3 project axioms + propext + Quot.sound +
    Classical.choice; README verbatim: this "verifies conditional proofs, not the
    inputs themselves," and the Python certificate "does not discharge any Lean
    axiom."
  - **NO ATTRIBUTION OF ANY KIND** — no "GPT-6 Astra," no human names, no author
    section; credit only to cited literature. README does NOT mention the prior
    record of 246.
- WebSearch sweep: repo named correctly as openai/PrimeGaps186 ("Conditional Lean
  formalization..."); Unite.ai coverage ("two new results on the gaps between
  prime numbers: a bound of 186..."); r/mathematics thread ("Lean is absolute...
  it's a proof checker"); AxiomMath/PrimeGapsLib companion. openai.com blog
  fetch → **403 bot wall**; blog content known via search snippets only.
- Prior-world context (outside-corpus knowledge, tri-stated below): previous
  unconditional record = 246 (Polymath8b, 2014, Maynard sieving); "consecutive
  primes" phrasing is strength-equivalent to prime-pair bounded gaps.
- Tooling check: no elan/lake on the host — the compile falsifier is NOT
  executable from this seat today; written cold for the next seat (below).

## SCORE — F:4 P:2 C:5 W:4 N:3 = **18/25 → BUILD WINDOWED band** (verb: CALIBRATE — see READ)

## READ (the honest why)
The root post alone scores REMEMBER-grade (hype frame, no claim); the reply-layer
artifact scores doctrine-calibration-grade — which is why "do not score from the
root post alone" is the whole game on this item (threads-are-signal, third
deployment). FIT 4: four live consumers — test-time-compute doctrine (frontier
inference compute → new-math artifact, externally validated), the standing WHALE
comparison order ("reasoning-scaling claims get compared against it" — this one
RHYMES with WHALE rather than contradicting: the artifact's real structure is
composition — two cited-theorem inputs + one numerical-certificate input +
machine-checked reduction — i.e. a HARNESS story wearing a weights story, exactly
the interleaving lesson), the receipts law (gains a new named nuance: RECEIPTS
HAVE HYPOTHESES — a Lean receipt receipts the reduction, not the theorem; unscoped
receipt-claiming lies by implication — same shape as the vast-arc "gate-pass ≠
alive" wedge, now seen at frontier scale), and the method-post / Sep-20 arc
(strongest external exhibit to date that receipt-first verification is how the
frontier itself ships math). PULL 2: it pulls doctrine rows and an exhibit row,
zero machinery — per intake genre rules, math items BUILD only with "wireable
transform + owed consumer," and no fleet organ consumes a number-theory repo.
COST 5: consume was $0, everything downstream is $0. WINDOW 4: announcement wave
is live now; expert scrutiny of hypothesis (3)'s 104+45 numerics — the only input
that is genuinely NEW rather than cited — lands in days-to-weeks and will promote
or kill the strong reading; method-post freshness date-gates the exhibit row.
NOVELTY 3: "conditional frontier math with Lean receipts" and the
receipts-have-hypotheses law are new to corpus; "test-time compute buys
capability" is a re-find (repetition is emphasis — the doctrine predicted this
and the prediction paid). Band says WINDOWED, verb says CALIBRATE: the buildable
artifact here is doctrine text, not machinery.

## DOGFOOD
1. **INVARIANT PASS**: receipts-over-claims honored — scored the ARTIFACT (repo
   README), not the tweet; falsifier ran BEFORE scoring. Tri-state per claim.
   Custody clean (all public content). Test-time-compute doctrine: externally
   validated AND sharpened. Two counters — **FORBIDS**: (1) repeating "GPT-6
   Astra proved prime gaps ≤ 186" in ANY fleet output without the word
   "conditional" (scope-collapse propagation — the exact lie the social layer is
   already telling); (2) reading this as evidence the fleet should chase
   frontier-math benchmarks (wrong lane; our edge is orchestration + receipts +
   cost, not frontier search depth). **PAID RENT**: the receipts-scope law named
   and filed; threads-are-signal paid a third time; the in-context researcher
   reading changed the score materially (root-only would have been a 6/25
   REMEMBER).
2. **STOCKFISH PASS**: placement = **DOCTRINE opcode** (test-time-compute doctrine
   row + receipts-law amendment + WHALE comparison ledger row) + **public-arc
   exhibit row** (windowed on operator GO for the method post). Consumers were
   standing organs before this card — placement succeeds. Failure mode avoided:
   filing as "cool math news" with no consumer, or over-building a Lean pipeline
   nobody owes.

## TRI-STATE
- Brown's root post text/date/views — **Supported** (fetched whole this turn).
- openai/PrimeGaps186 exists, Apache-2.0, is a CONDITIONAL Lean 4 formalization
  of liminf consecutive-prime-gap ≤ 186 via DHL[40,2], conditional on the three
  named axioms (kloosterman3_bound / kloosterman2_correlation_bound /
  physical_integral_bounds), with a 6-axiom whitelist and a Python certificate
  that discharges nothing — **Supported** (README fetched whole this turn).
- "GPT-6 Astra PROVES infinitely many consecutive prime pairs at distance ≤ 186"
  (scaling01/weijie444 framing) — **Disputed AS WORDED** (the primary artifact
  itself says conditional and "verifies conditional proofs, not the inputs");
  the conditional reduction — **Supported**.
- 186 improves the standing unconditional record of 246 — **Supported as
  world-knowledge** (Polymath8b 2014; not stated in the README, which is itself
  a small flag), **Unproven as a delivered unconditional result** until the
  three inputs are discharged.
- "By GPT-6 Astra" (attribution) — **Unproven**: the repo carries no attribution
  of any kind; OpenAI's blog 403'd this pass (search snippets only); the
  human-vs-model credit split is unread (the cdn.openai.com PDF is the place it
  would live).
- Hypotheses (1)-(2) being literature consequences (Deligne via Katz 1988;
  Fouvry–Kowalski–Michel 2013) — **Supported as claimed-by-README**; the
  literature itself unverified this pass (formalization debt, not conjecture,
  per README's own framing).
- Hypothesis (3)'s 104+45 numerical bounds — **Unproven** (Python certificate
  recomputes but does not discharge; no independent check found this pass).
- KILL CONDITIONS, executable cold by the next seat: (a) `lake build` on
  openai/PrimeGaps186 (Mathlib 4.34.0-rc2 pin) + `#print axioms
  primeGapLiminf_le_186` must list EXACTLY the 3+3 axioms — anything else =
  Disputed; (b) fetch the cdn.openai.com PDF — if OpenAI's own text claims an
  UNCONDITIONAL proof or the credit split says "autonomous," upgrade the
  attribution tri-state; if it says conditional-with-human-mathematicians, the
  calibration reading stands; (c) watch expert number-theory response to the
  104+45 integral bounds (fastest promotion/kill path — if any bound fails
  independent re-verification, the 186 claim dies to 246).

## VERDICT
**CALIBRATE** (18/25, BUILD WINDOWED band — verb CALIBRATE per genre rule: no
wireable transform, no owed consumer, and the only buildable artifact is
doctrine text). Three wires, all text, all $0: (1) test-time-compute doctrine
gains the row "frontier test-time compute now ships conditional-new-math with
machine-checked receipts — capability validated, scope always read the
conditional"; (2) receipts law gains the amendment RECEIPTS HAVE HYPOTHESES
(a scoped receipt receipts the reduction; unscoped restatement lies by
implication — gate-pass-≠-alive at frontier scale, folded as emphasis); (3)
WHALE comparison ledger gains the row: reasoning-scaling claim examined, found
to be composition (2 cited theorems + numerics + checked reduction) —
interleaving lesson re-confirmed from the frontier side, no contradiction. Plus
one exhibit row for the method post, windowed on operator GO.

## ROUTE
Card filed here; typed room row appended this turn; memory-index row for the
main seat's fold (doctrine rows land via the standing test-time-compute +
receipts files, no driver interrupt, no campaign lane touched). Exhibit row
held until the operator rules on method-post inclusion. The three kill
conditions route to any Lean-capable or fetch-capable free-lane seat — (a) is
minutes of machine time once elan exists on the hands box.

## THE CROP
Not seen this pass: the Lean never compiled here (no elan/lake on host; axiom
whitelist read from README prose, not `#print axioms` output); the
cdn.openai.com paper "Improved short gaps between primes" unread (the
human-vs-model credit split and hypothesis-(3) novelty live there); openai.com
blog bot-walled (attribution in OpenAI's own voice Unproven-this-pass); the
quote-tweet layer and any Polymath-adjacent expert reaction unseen (the
community's read on the 104+45 numerics is the fastest promote/kill path); deep
number-theory check of whether DHL[40,2] at this tuple is plausible — out of
lane entirely. Next lens/chair: a **Lean-capable seat** (compile + print-axioms
kill condition) and the **mathematician chair** on hypothesis (3); the
**public-arc seat** holds the exhibit row pending operator GO.
