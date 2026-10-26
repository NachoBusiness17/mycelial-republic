# SOCRATIC GROUNDING — STEAL (2026-08-10)

**Operator:** "instead of delete we do a socratic flow" · then "steal" — ground the Socratic flow
in the real method, not an ad-hoc question list.

## External grounding (cited)
- **Vlastos, "The Socratic Elenchus"** — the elenctic examination (5 steps): the interlocutor
  asserts a thesis → we test whether it's false → secure agreement to further premises → show those
  premises imply the contrary → conclude. Most inquiries end in **aporia** (an improved state of
  not-knowing), NOT a forced conclusion. Frede: showing a thesis false is insufficient to conclude
  its negation true — the honest result is often "we don't yet know."
- **Guthrie, "The Greek Philosophers"** — the essence of the Socratic method is to convince the
  interlocutor that whereas they thought they knew, they do not; recognition of ignorance is the
  first step to knowledge.
- **Boghossian, "Socratic Pedagogy"** — cognitive dissonance is essential, but distinguish
  productive discomfort from harmful exposure; never humiliate.
- **Steelmanning (principle of charity, opposite of straw man)** — address the STRONGEST form of
  the argument, removing flawed assumptions, before refuting it.

## Self-steal (already inside the Republic)
- `mag/socratic.py` (prompt workshop), `mag/socratic_tree.py` (check what the tree already knows
  before asking), `voice_shadow.py` SOCRATIC (Plato: define · Bernays: who benefits · Jung: what's
  under the ask · end with ?), `AUDIT_SOCRATIC_STEAL` (proof-first Socratic sprint), `scrum.py`.

## The doctrine (folded, source=socratic_steal)
1. **elenchus-not-erasure** — challenge an ungrounded doctrine through elenctic questioning, never erase.
2. **aporia-is-progress** — hold a challenged doctrine as "unknown" (better than a false confident one).
3. **steelman-before-straw** — address the STRONGEST form before refuting; never attack a straw man.
4. **know-ignorance** — the first step is recognizing we don't know; surface the unexamined.
5. **productive-not-harmful** — challenge must be constructive, never humiliating.

## Build (ponytail-style grounding audit)
- `mag/ponytail_audit._scan_grounding()` now emits a **Socratic flow** for each ungrounded doctrine
  (via `_socratic_challenges`: define it / who benefits / what's under it / refute it — the
  voice_shadow + elenchus pattern) with `replacement: "Socratic flow: challenge to ground — do NOT
  delete"`. The audit CHALLENGES, never erases.
