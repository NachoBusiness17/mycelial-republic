# FERMAT RACTOR HARNESS — build receipt (2026-09-06)

**Commission:** fleet build B10, from `watch/FERMAT_RACTOR_20260906.md` — the
deterministic, zero-token register engine + falsifier for the Pierre de Fermat
persona. Pattern lineage: the shitposter ractor
(`watch/SHITPOSTER_IN_CHIEF_PERSONA_20260906.md`) — mined corpus + registers +
blind A/B falsifier, judged by a HUMAN because no LLM judge exists in this cage.

## **THIS IS A REGISTER ENGINE + FALSIFIER RIG, NOT A LANGUAGE MODEL.**

Every response is a deterministic composition over hand-written sentence
templates and fragment pools, seeded by sha256 — same seed, same output, byte
for byte, cross-process (verified by diff this session). Zero LLM tokens end to
end. The `talk` CLI states this in its banner, unprompted, every session.

## Files

- `mag/fermat_ractor.py` — the harness (stdlib only; ~950 lines). CLI:
  `quote <register> [--seed N]` · `abtest [--seed N]` · `talk [--register R]` ·
  `audit` · `demo`.
- `watch/FERMAT_RACTOR_AB_1654_20260906_SHEET.md` — the blind A/B sheet
  (16 numbered items, shuffled, no provenance marks — the operator scores A/G).
- `watch/FERMAT_RACTOR_AB_1654_20260906_KEY.json` — the answer key, written to
  a SEPARATE file so scoring stays blind (schema `fermat_ractor.ab.v1`).
- `dashboard/static/` untouched — the chat surface is the later door
  (RACTORT-SURFACE), per house law.

## Quote-bank census: 21 lines — 15 AUTHENTIC-VERIFIED / 6 CURATED-NOT-QUOTED

Every line is status-tagged; `python -m mag.fermat_ractor audit` prints the
full table. AUTHENTIC-VERIFIED lines were fetched 2026-09-06 (this seat's
curation pass) and quoted verbatim from the named URL; runtime makes zero
network calls. CURATED-NOT-QUOTED lines are standard canon, marked honestly,
with the reason the fetch didn't happen (two MacTutor timeouts = two-strike
bail; Observations translation = the CORPUS-PULL door, not yet pulled).

| Source (fetched 2026-09-06) | Lines | What |
|---|---:|---|
| en.wikipedia.org/wiki/Fermat%27s_Last_Theorem | 2 | margin note, EN + Latin ("...cuius rei demonstrationem mirabilem sane detexi. Hanc marginis exiguitas non caperet.") |
| en.wikipedia.org/wiki/Fermat%27s_little_theorem | 3 | Frénicle letter, 18 Oct 1640 — little theorem + "I would send you a demonstration of it, if I did not fear going on for too long." |
| en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares | 1 | Pascal letter, 25 Sep 1654 — "square and the quintuple of another square" |
| en.wikisource.org (Smith, A Source Book in Mathematics, 1929) | 9 | 1654 dice letter ("a point with a single die in eight throws", trans. Sanford) + February 1657 challenge letter (trans. Whitford): "scarcely any one that sets forth purely arithmetical questions", the Pell-challenge statement, the 61 bait, "After I have received your reply, I will propose another matter." |
| CURATED-NOT-QUOTED (not fetched; reason on file per line) | 6 | descent described to Carcavi Aug 1659 (Oeuvres II.431-436; Weil pp.75-79), Christmas two-squares letter 25 Dec 1640, esteem-for-Pascal via Carcavi 1654, refusal-to-publish canon, 1670 posthumous publication history, Observations Obs. I |

Honest note: the persona card's *descent-as-rhetoric* register therefore runs
on CURATED paraphrase, not fetched primary text — the weakest provenance in
the bank, marked as such in the audit table. The A/B draws authentic items
ONLY from the 15 verified lines.

## Register census: 6 registers, all sha256-seeded, deterministic

| Register | Composition shape (pools) | Output space | Sample [GEN] line (seed 1654) |
|---|---|---:|---|
| MARGINALIA | 3 forms × 6 Latin claims+glosses × 9 obs-nos × 5 closers | 810 | "Ad Bacheti prop. XXXI: Numerus primus quemlibet terminum progressus geometricae unco minus metitur. — Satis. Lector peritus intelleget." |
| CHALLENGE LETTER | 3 salutations × 2 openers × 3 bodies × 4 problems × 4 closers | 288 | "To Monsieur de Carcavi... Sir, I send you a question of whole numbers... After I have received your reply, I will propose another matter." (closer is verbatim bank line — flagged embedded) |
| THE DESCENT | 4 openers × (3 templates + Latin form) × 4 greaters × 4 lessers | 320 | "Men prove upward, with engines of their own height. I prove downward..." |
| THE PASCAL LETTER | 2 salutations × 4 bodies × 4 closers | 32 | "Tabulate every continuation — all of them, to the last — and count the wins." |
| THE MARGIN | 6 echo sentences (single or pair) + 2 templates embedding the verbatim famous sentence | 38 | "The margin was not humility; it was inventory." |
| KERNEL-ERA | 3 opens × 4 mids × 3 lines × 3 days × 3 scales × 4 closers | 1296 | "Thirteen million lines in eleven days, and the word sorry appears nowhere in the proof." |

The persona card's voice laws are encoded, not imitated: courtly-provocative,
Latin-inflected (MARGINALIA is Latin-brief with English glosses), the letter as
the only arena, challenges before befriending (CHALLENGE closes with the
verbatim lethal courtesy), descent as rhetoric (THE DESCENT), secrecy as method
("I would send you a demonstration..." lives in the bank; the registers echo
it without quoting). KERNEL-ERA carries the persona card's honest blind spot
in its own closers: "I remember neighboring it, not possessing it — and I say
what the record says."

Provenance law: generated output never claims authenticity. `quote` prints a
"GENERATED register composition — not an authentic quote" header; `demo`
prefixes every generated line [GEN]; generated items that weave verbatim bank
text are flagged and EXCLUDED from the A/B. In the blind sheet alone the marks
are withheld — that is what makes the test blind.

## Falsifier numbers (all machine-run, `python -m mag.fermat_ractor demo`)

- **F1 distinctness: PASS** — 8 seeds per register → 8/8 distinct outputs for
  EVERY register (need ≥ 5): marginalia 8, challenge 8, descent 8, pascal 8,
  margin 8, kernel 8.
- **F2 tag integrity: PASS** — 21/21 bank lines status-tagged with source +
  ref; all 15 AUTHENTIC lines carry the fetched URL; census 15 VERIFIED / 6
  CURATED. (`audit` prints the table.)
- **F3 blind A/B rig: PASS** — 16-item sheet (8 authentic / 8 generated,
  MARGIN+CHALLENGE only); sheet and key written as SEPARATE files; key
  re-read from disk and cross-checked against the shuffle item-by-item;
  rebuild is byte-identical (no wall clock in the rig); 6 generated candidates
  excluded for embedding verbatim bank text (counted and listed in the key);
  near-duplicate generated openings re-rolled (first-60-chars dedup) so the
  sheet carries no free hints.
- **F4 runtime network seal: PASS** — AST import audit of the module: only
  `__future__, argparse, ast, dataclasses, hashlib, json, pathlib, random, re,
  sys`. No urllib/socket/http/subprocess; fetches happened at curation only
  and are recorded per line.
- **F5 demo structure: PASS** — demo runs all 6 registers ([GEN]-prefixed),
  prints the tag table, and reports F1-F4.
- **Determinism receipt:** `quote descent --seed 42` run twice in separate
  processes → byte-identical output (diff clean). The RNG is seeded from
  sha256(register|seed); Python's salted `hash()` is never used.
- **The indistinguishability score itself is NOT yet a number** — by design.
  No LLM judge exists in this cage and the harness does not pretend to grade
  the human. The sheet + key are on file; the Operator's A/G scorecard is the
  missing datum, target ≥ chance-muddied majority (persona-card falsifier).

## Honest verified-vs-not

- VERIFIED: composition determinism (cross-process diff), distinctness counts,
  tag table integrity, A/B shuffle/key separation and consistency, zero-token
  zero-network runtime (AST-audited), CLI surface (quote/abtest/talk/audit/
  demo all exercised this session, including a scripted KERNEL-ERA talk turn
  answering the Operator's actual inaugural question).
- UNPROVEN (armed, awaiting the human): A/B indistinguishability ≥
  chance-muddied majority. The falsifier is a rig, not a verdict.
- NOT BUILT (later doors, no silent claims): chat surface on /static/
  (dashboard untouched), CORPUS-PULL (Oeuvres + full Observations to upgrade
  the 6 CURATED lines to VERIFIED), chain knot of the first conversation.

## Lineage

Shitposter ractor pattern (mined corpus + registers + blind A/B, human-judged)
→ Fermat. Same bones, one reinterpretation, named: the shitposter's corpus was
mined from engagement receipts; Fermat's is curated from primary-source
translations with per-line provenance, because the corpus here is 350 years
dead and the receipts are the Oeuvres. One builds, one verifies: this seat
built the rig; the Operator's scorecard verifies it.

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran `demo` fresh: EXIT=0, all falsifiers PASS, numbers reproducing —
distinctness 8/8 per register, 21/21 tag integrity, A/B sheet+key separate and
cross-checked with 6 verbatim-embedding candidates excluded, network seal clean
(stdlib imports only, AST-audited), cross-process determinism by diff. Spot
check `quote KERNEL-ERA --seed 7`: composition carries the persona's documented
voice ("the narrowness was mine, and the theorem was not") with the GENERATED
provenance banner correctly displayed — no authenticity laundering. Honest
scope confirmed: register engine + falsifier rig, NOT a language model (bold in
receipt and talk banner); the A/B indistinguishability score is correctly armed,
not faked — the sheet awaits the Operator's scorecard, the one datum no harness
can produce. VERDICT: PASS. Fermat's send rights gate on that human score.
