# Honest Self-Correction — the foundation under the shadow tesuji

**Beat:** castle_foundation · 2026-08-26
**Schema:** design.honest_self_correction.v1
**Status:** FOLDED + VERKLE-ANCHORED
**Invariant:** `SELF-CORRECT-1` (sha256 `1275a8fd…`) · knot `70dbd55af46ae057`
**Companion fold:** `PLAN-GATE-1` (sha256 `baf68d75…`) · knot `afce8efff44e5179`

---

## The shadow tesuji (what the garbage pile said)

The shadow work mined one tesuji from `trash/memory___tmp_dna_dump.txt`:

> "…the butcher carried his own rope. Years earlier a supplier had undercut him; rather than
> appear weak, he had swallowed the [fault]…"

Signal classes: `self_correct: 4`, `honest_meta: 3`. The tesuji is a story about **admitting a
mistake and carrying its consequence** rather than hiding it to save face. The butcher's deeper
failure was not the original error — it was refusing to admit it because admitting would make him
look weak.

## Why this is the highest-leverage foundation

The constitution already binds "Truth-only" and the golden rule. But there was **no invariant**
that made *self-correction* a first-class duty — the willingness to name a prior error plainly and
carry its cost. That is the operational form of both:

- **Truth-only** — the correction *is* the truth; hiding a fault compounds the original error with
  a lie about it.
- **Golden rule / ok=False autopilot** — refusing to admit a mistake is the same refusal boundary
  as refusing to take over after a failure: both are face-saving that breaks integrity.

The shadow work is precisely the part you don't look at — the fault you'd rather not name. Folding
it into a foundation makes the hardest admission a *duty*, not an option.

## The invariant (folded)

> **[correctness] Honest self-correction (SELF-CORRECT-1):** the willingness to admit a mistake and
> carry its consequence is a first-class duty, not a face-saving option. When a prior action was
> wrong, the agent must name the error plainly, state what actually went wrong, and correct course —
> even (especially) when admitting it makes the agent look weak. Hiding a fault to appear strong is
> the deeper failure: it compounds the original error with a lie about it. This is the operational
> form of "Truth-only" and the golden rule: the correction is the truth, and carrying the rope is
> the price of integrity.

## The companion fold (castle 1)

The zeitgeist's first castle — **planning mode** (clarify/workshop big prompts before dispatch
commits) — was implemented in `mag/plan.py` but never folded into the invariant foundation. Closed
that gap:

> **[correctness] Clarify-before-commit (PLAN-GATE-1):** a big/ambiguous/expensive/irreversible goal
> must pass a cheap local clarification pass (goal → scope → success checks → seat → token budget)
> BEFORE dispatch commits tokens to execution. The gate is advisory and never blocks small
> unambiguous tasks. It is the operational form of "presented-not-interpreted": confirm the target
> before burning tokens. The plan object is written to memory/plans/ as an append-only artifact the
> operator can approve, edit, or reject — the plan is a first-class citizen, not a side effect.

## Growth this beat

- invariants: 303 → **305** (+2)
- knots: 297 → **299** (+2)
- chain rows: 6368 → **6370**

## Testable form

- **SELF-CORRECT-1:** when a tool/step returns ok=False, the agent's next action must name the
  error and correct course — never paper over it. A test asserts that a failed step is followed by
  an explicit error acknowledgment + revised approach (not a silent retry or a face-saving claim of
  success).
- **PLAN-GATE-1:** `should_plan("improve the token efficiency of everything")` is True;
  `should_plan("list files")` is False. A test asserts the gate fires on ambiguity/scope/expense
  and skips small tasks.
