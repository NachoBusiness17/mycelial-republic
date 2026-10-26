# STEAL PASS — paste-checkable invariant falsifiers (2026-09-04)

**Target**: the `lattice_check.html` pattern, operator: "do a steal on this to
find inspiration."
**Landscape receipt**: swept the archetype space — **nobody has unified
"mathematical invariant paste-checkers" into one surface.** The niche is open.
Nearest analog = CyberChef. The components exist scattered; the unification is
the open territory (Supported by search; one engine, not proof).

## The archetype map (what exists, what to steal from each)

**1. CyberChef (GCHQ, Apache-2.0) — THE crown steal.** gchq.github.io/CyberChef.
The "Cyber Swiss Army Knife": paste anything, chain operations into RECIPE
pipelines, auto-detect via the "Magic" operation, runs fully offline as a
single HTML file.
→ **Steal: falsifiers as composable recipe OPS, not isolated pages.**
lattice→chain-hash→claim-check as a draggable chain: paste a room.jsonl slice,
run three invariants in order, get one combined verdict. The Magic pattern:
"paste anything, the workbench guesses which invariant applies."

**2. jwt.io / salcode/jwt — the UX standard.** Single self-contained HTML,
split-pane: paste left, live decode right, signature verdict color-coded
(green/red) AS YOU TYPE.
→ Steal: live-as-you-paste verdicts, color-coded PASS/BROKEN panels. Our
pages already half-do this; make it instantaneous.

**3. OEIS — the oracle inversion.** Paste an integer sequence, get its name
and family.
→ **Steal: the DETECTOR mode.** Inverse of a checker: paste an observed
number (a distance, a hash prefix, a token count), the page names the
invariant family it belongs to ("2.6 miles = √7 world — impossible on-grid;
you measured something curved"). Checker says pass/fail; detector says WHAT
YOU'RE LOOKING AT. Dungeon-tutor gold.

**4. regex101 — the test-bench pattern.** Multiple test vectors run live +
an explanation pane that parses each token.
→ Steal: batch test-vector panel per falsifier (paste N cases, see N
verdicts in a table) + an "explain the invariant" pane in plain words —
the teaching-panel shelf gets a home in every falsifier.

**5. Compiler Explorer (godbolt) — permalinks.** Whole session state encoded
in the URL hash.
→ **Steal: shareable falsifier state.** Paste coordinates + verdict encoded
in the URL — the link IS the receipt. Ties directly into the x:game:image
playable-card steal: a falsifier link embedded in a post carries its own
evidence. Public-turn pattern.

**6. TLA+/Alloy web runners — counterexample rendering.** When a model check
fails, the witness is displayed, not just "false."
→ Steal: formalize what lattice_check already does — EVERY falsifier must
render its counterexample (the violating pair, the broken link index).
"Failure shows its witness" as a house law for falsifier surfaces.

**7. Luhn/IBAN/UUID validators (gentools, dCode) — proof of posture.**
Consumer-grade paste-checkers at scale: instant, free, no signup.
→ Steal: nothing technical — confirmation that the POSTURE is right and
ordinary. Our falsifiers are normal tech done for unusual invariants.

## The public-turn shape (assembled from the steals)
An "Invariant Workbench": one CyberChef-style surface, our invariants as
chained ops, detector mode, witness rendering, URL-permalinks that carry
verdicts. Nobody has built this for mathematical invariants. It is the
playable-card demo surface for the public turn — paste a claim, watch it
falsify live, share the link as the receipt.

## Routing
1. **REMEMBER**: the seven steals filed; falsifiers.html (in build now)
   should absorb #2 (color-coded live verdicts) and #6 (witness rendering)
   as house law immediately — they're cheap.
2. **BUILD WINDOWED**: the workbench (recipe-chain composition + detector
   mode + URL permalinks) — a real build, CyberChef-scale ambition on our
   invariant set. Parked behind the two in-flight falsifier builds; this
   card is its spec seed.
3. **REMEMBER**: niche-unification finding — public-turn claim "the fleet
   built an invariant workbench; no off-the-shelf equivalent exists" is
   Supported by one search engine, needs a second pass before it goes in a
   post (tri-state discipline).

Tri-state: archetype descriptions Supported (well-documented tools); "niche
is open" Supported-by-one-search (Unproven as proof); workbench feasibility
Supported (every component exists; composition is ours).
