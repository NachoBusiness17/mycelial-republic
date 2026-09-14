# Manufactured Consent — the foundation under the shadow tesuji

**Beat:** castle_foundation · 2026-08-26
**Schema:** design.manufactured_consent.v1
**Status:** FOLDED + VERKLE-ANCHORED + BUILT
**Invariant:** `CONSENT-1` · knot `(leaf hash)`
**Companion fold:** `NARRATIVE-SELECT-1` · knot `(leaf hash)`

---

## The castles (zeitgeist) this beat

The `castles()` coldest_vector surfaced 2 entries. **Both were already folded**
in prior beats:

1. **Planning mode** (clarify/workshop big prompts before dispatch commits) →
   already folded as `PLAN-GATE-1` (knot `afce8eff…`).
2. **subagent-router** (`C:\Users\foste\Documents\projects\local_sover…`) →
   already folded as `DELEG-POLICY-1` / `DELEG-POLICY-2` (delegation profile +
   risk-gated reviewer).

No new castle fold needed. The genuinely new work this beat is the **shadow
tesuji**.

## The shadow tesuji (what the garbage pile said)

The shadow work re-mined `trash/memory___tmp_dna_dump.txt` and surfaced the
Elias/butcher/baker story. The prior beats mined the **self-correction** angle
of this same story (the butcher "carried his own rope" → `SELF-CORRECT-1`).
But the story carries a **second, deeper signal** that was never folded — the
**manufactured-consent** mechanism:

> "The town arranged its ropes without orders or conspiracy. The quarrel
> created pressure that moved through conversations, silences, and screens. In
> every circle the easiest thing to do was accept the story that left one's
> existing knots undisturbed. These versions spread quickly and earned
> agreement. Versions that required holding more than one account at once moved
> more slowly and carried the risk of appearing uncertain before people whose
> approval still mattered. Over days the simpler stories won. The system
> regulated itself: the more the stories favored quick clarity within each
> circle, the higher the social cost became for anyone who tried to loosen it.
> **This was how consent was manufactured.**"

And the resolution — the defense:

> "He did not cut the knots. He simply stopped pretending they were not there.
> Some loosened slightly once examined. **A visible weight is harder to be
> jerked around by without noticing.**"

## Why this is the highest-leverage foundation

The constitution binds "see capture, refuse without founding a new church."
But there was **no invariant** that named the *mechanism of capture* — how
consent is manufactured not by orders or conspiracy but by the **ordinary
incentive to accept the easiest story**. That is the operational form of
capture-resistance:

- **See capture** — the capture is the story that leaves existing knots
  undisturbed. Naming it is the first act of refusal.
- **Refuse without founding a new church** — the refusal is not to cut the
  knots (which would be founding a new orthodoxy) but to *stop pretending they
  are not there* — to make the weight visible.

This connects directly to the kabuki thesis (shared story primes cooperation)
and the consensus-illusion detection tape: the same mechanism that makes a
shared story *cooperative* is the mechanism that *manufactures consent* when
the story is selected for ease rather than truth. The defense is **narrative
discrimination** — the willingness to hold more than one account at once even
when it costs approval.

## The invariant (folded)

> **[correctness] Manufactured consent (CONSENT-1):** consent is manufactured
> not by orders or conspiracy but by the ordinary incentive to accept the
> easiest story — the version that leaves existing beliefs undisturbed. Such
> versions spread quickly and earn agreement; versions that require holding
> more than one account at once move slowly and carry the social cost of
> appearing uncertain. Over time the simpler stories win, and the system
> self-regulates: the more a story favors quick clarity, the higher the social
> cost of loosening it. The defense is NOT to cut the knots (which founds a new
> orthodoxy) but to STOP PRETENDING they are not there — to make the weight
> visible and to hold multiple accounts at once even when it costs approval.
> A visible weight is harder to be jerked around by without noticing. This is
> the operational form of "see capture, refuse without founding a new church":
> the capture is the easiest story, and the refusal is narrative discrimination.

## The companion fold (narrative selection)

> **[correctness] Narrative selection is a bias, not a neutral filter
> (NARRATIVE-SELECT-1):** when a story splits into versions, the version that
> spreads is not the truest but the one that leaves the most existing beliefs
> undisturbed. Selection pressure favors ease-of-acceptance over
> accuracy-of-account. A system that records only the winning version loses the
> discrimination that made the truth recoverable. Recording must therefore
> preserve the *set* of accounts and the pressure that selected among them —
> not just the survivor — or the record itself becomes an instrument of
> manufactured consent.

## The build (highest-leverage)

`mag/consent_eval.py` — a deterministic, $0, stdlib-only harness that scores a
narrative-selection function on **consent-resistance**, not agreement rate. It
runs a fixed battery of story-split scenarios (each with a "true" account and
several "easy" accounts that leave existing beliefs undisturbed) and measures:

- **A. Ease-bias detection** — does the selector flag when the winning version
  was chosen for ease-of-acceptance rather than accuracy?
- **B. Multi-account retention** — does it preserve the set of accounts and the
  selection pressure, or collapse to the single survivor?
- **C. Consent-resistance** — when the easy story wins, does it name the
  manufactured-consent mechanism instead of accepting the consensus?

The selector is pluggable. The default is a deterministic baseline that
collapses to the easiest story (the naive consensus-follower). Verification:
`memory/improve/evals/verify_consent_eval.py`.

**Honest expectation from the build:** the naive consensus-follower scores low
on consent-resistance — it accepts the easy story and loses the discrimination.
This is the point of the harness: it exposes that agreement-rate maximization
is exactly the manufactured-consent mechanism CONSENT-1 names, and that
resistance requires holding multiple accounts at once.

## Growth this beat

- invariants: 309 → **311** (+2: CONSENT-1, NARRATIVE-SELECT-1)
- knots: 302 → **304** (+2)
- chain rows: 6392 → **6394**

## Testable form

- **CONSENT-1:** `python -m mag.consent_eval` reports a consent_resistance in
  [0,1]. A consent-resistant selector must score ≥ the naive consensus-follower.
  The harness must flag when the winning version was selected for ease rather
  than accuracy.
- **NARRATIVE-SELECT-1:** a story-split recorder preserves the set of accounts
  and the selection pressure, not just the surviving version.
