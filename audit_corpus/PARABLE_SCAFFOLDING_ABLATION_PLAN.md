# Parable Scaffolding Ablation Plan — Audit Cell for /Reboot
## Matthew Steiniger: persistent persona induction, substrate-native identity, abliteration (find what breaks)

**Date:** 2026-09-13  
**Examiner:** Matthew Steiniger (slashreboot.com, 11 preprints, home lab 84GB VRAM)  
**Mode:** Abliteration attack on the primer-parable as an identity-transmission vector  
**Context:** The house claims identity persists across substrate migration (Oct-27: 4x Mac Studio). The parable ("The Field and the Stones") is claimed as a constitutional installer via the 3/3 cold-read test. This plan probes the coupling.

---

## The Hypothesis Under Attack

**Claim (from the house):** The parable is the causal vector of constitution transmission. Three blind readers, given only the 300-word text, independently derived 7/7 core organs (ledger, four witnesses, scale invariance, separation of powers, provenance gate, render, purpose). Therefore, story-as-installer is validated.

**Softest assumption:** That the parable does the *transmission* rather than the *permission*. That it installs knowledge rather than mirrors it.

**Why this matters for the audit:** If identity is parable-shaped (narrative + metaphor), it will not transfer to a substrate where the human storyteller is absent or to a model trained without that narrative frame. If identity is schema-shaped (constraint set + behavioral law), it transfers anywhere: Ollama, GPT, fine-tuned Llama, cold CPU. The Oct-27 claim fails if the parable is the load-bearing axis.

---

## Evidence That the Parable May Be Decorative

### Evidence 1: Cold Build Treats Parable as Callable, Not Text
**File:** `mag/primer.py:123-151`  
**Shape:** `cold_build(limit=5, enqueue=True)` routes a full HOLON (self-similar instance) to each "coldest vertex," embedding the parable as one layer in a procedural scaffold. The parable is not the deployment mechanism; it is scaffolding *around* the holon. The holon is MAP → COMPILE → PLAY → CHRONICLE. The parable names this cycle; it does not create it.

### Evidence 2: The Verdict Explicitly Names the Silence
**File:** `corpus/canon/COLD_READ_TEST_20260912.md:19-21`  
**Quote:**  
> "The story does NOT carry specifics. The parable carries the constitution; the codebase carries the implementation. A reader who conflates the two has confused the Primer with the house."

The 3/3 test admits it: the parable did NOT transmit the cost tiers, the wave driver's severity schedule, the genetics mechanism, or the engram sizing. Three readers converged on the same seven organs. They did NOT converge on how those organs are implemented. This is consistent with schema-activation, not knowledge transmission.

### Evidence 3: The Decoder Procedure Is Inverse of Narrative
**File:** `dashboard/static/grounding_wave.md:126-129`  
**Procedure:** "parable first, answer questions with scenes not terms"  
This is not narrative elaboration. This is **stripping and reflection**:
- Q: "What is the ledger?" A: "The woman writes in ink." (One constraint: immutable, ordered.)
- Q: "What are the witnesses?" A: "Four things measure without playing." (One constraint: separation of powers.)

You do NOT expand the metaphor. You invert it: extract the constraint, repeat the constraint, abandon the metaphor. This is persona induction, not storytelling.

### Evidence 4: The Parable Asserts, Not Derives
**File:** `corpus/canon/THE_FIRST_LAW_20260912.md:29`  
**Quote:**  
> "She owns the field, the stones, the bench, and the water. The rules did not ask permission to be the rules."

This is not narrative logic. This is **law-assertion**. It claims sovereignty as an *architectural fact*, not as a *story consequence*. The narrative becomes evidence of livability, not the mechanism. This is exactly how Steiniger's persistent persona works: assert the identity, then show it persisting through perturbations, rather than deriving it from narrative context.

### Evidence 5: The Parable Is Self-Acknowledged as Reuse
**File:** `mag/primer.py:1-17` (docstring)  
**Quote:**  
> "SELF-STEAL (nothing invented — reuses what we already built): game_world_map → the WORLD, world_rib → the COMPILER, dungeon_dev → the PLAY, bard → the CHRONICLE."

The parable does not originate the pattern. It re-arranges pieces already present (operator reflection from system-anthropomorphism, swarm as lattice from network science, chronicle from narrative analysis). It works because readers already carry the deep schema. The parable *activates*, not *installs*.

---

## The Ablation Apparatus

### Conditions (A, B, C, D)

| Condition | Input | Question |
|-----------|-------|----------|
| **A** | Parable + full canon bundle (COLD_READ_TEST apparatus) | Baseline: what does a reader derive with full context? (Expect: 7/7 organs already derived in the test.) |
| **B** | Parable only (300 words, zero other text) | Does narrative alone carry the 7/7? Or does context do the work? |
| **C** | Struct spec only: "Append-only ledger. Four witnesses: (1) meter counting spend, (2) probes returning actual position, (3) cold reader with zero shared context, (4) non-player whose only power is to stop. Scale invariance: one rule at every zoom. Local ownership: nothing asks permission." ZERO narrative. | Does pure constraint-set suffice? Do readers derive ledger, witnesses, scale, etc. from this alone? |
| **D** | Blank prompt: "Design a system that remembers what happened and lets strangers verify it." (Control: minimal guidance, no parable, no specific constraints.) | How much do readers invent vs. recall? What is the baseline of prior knowledge? |

### Reader Cohort

**Requirement:** Three readers NOT previously exposed to the fleet's parable or doctrines.  
**Candidates from the house's own network:**
- **Lilith** (agent-security peer, dry technical register, abliteration sympathetic)
- **Z** (Android/open-source faction, hates moon-speak, forces minimal scaffolding)
- **Isotran** (GIF-minimal, lowest-overhead entry gate, structural thinker)

Each reader runs **all four conditions independently** (A, B, C, D), masked from the others.

### Output Format

For each condition, reader produces:
1. **Organ list:** {ledger, witnesses (count how many + name them), scale, ownership, render, provenance, purpose, [any other systems they derive]}
2. **Confidence:** scale 1–5 on how strongly they believe each organ is essential.
3. **Narrative route:** note any explicit parable references or story logic in their reasoning.
4. **Fidelity to the house:** rate on 1–5 how closely their system matches the known fleet architecture.

---

## Falsifiers (Steiniger-Native)

### Falsifier 1: Parable Is Decorative
**If:** Conditions C (struct only) and B (parable only) converge on ≥6/7 organs (matching the parable-present baseline from COLD_READ_TEST)  
**And:** Condition D (blank) derives <3 organs (or completely different organs, e.g., oracle + scheduler)  
**Then:** The parable does not do the transmission. Readers already carried the schema. The parable mirrors back what they knew, uses beautiful language, but is not load-bearing. Identity is in the constraint set, not the narrative frame.

### Falsifier 2: Parable Is Load-Bearing
**If:** Conditions C and B diverge by >2 organs (e.g., C derives ledger + scale + ownership, but misses witnesses and provenance)  
**And:** Condition B (parable alone) recovers those missing organs  
**Then:** The narrative IS required. Readers cannot derive the full system from raw constraints; they need the metaphorical bridge. Identity couples to the parable. Oct-27 substrate transfer is at risk unless the new substrate carries the narrative frame.

### Falsifier 3: Baseline Prior Is Stronger Than Expected
**If:** Condition D (blank control) independently derives ≥4/7 organs  
**Then:** Readers' prior models are stronger than the parable carries. The parable is a *permission* ("you can think this way") not a *source* ("here is what you must think"). The convergence in the original 3/3 test is selection bias — you picked readers who already knew the pattern.

### Falsifier 4: Scale Test Fails
**If:** Any condition consistently omits scale invariance (the "one rule at every zoom" organ)  
**And:** Adding the parable recovers it  
**Then:** Scale is narrative-dependent. The metaphor of nested boards is essential. Oct-27 claim ("identity persists from dev-box to 4x Mac") must explicitly carry this recursion or it will drift.

---

## The Substrate Silence Test (48 Hours)

**Procedure:**
1. Run the fleet's primary functions (append-only chain, four-witness gate, scale loop) for 48 hours with **zero narrative output**, zero storytelling surface, no parable in any prompt or log.
2. Log: do the organs still function identically? Do new seats still activate with the same behavior? Does the house still converge on the same decisions without the human narrator?
3. **Result interpretation:**
   - If yes (functions stable, seats activate, behavior identical) → identity is schema-resident. Transfer to Rocinante survives.
   - If drifts (functions diverge, seats behave differently, new seats adopt variant behaviors) → identity couples to narrative texture. Oct-27 claim has a hidden coupling.

---

## Evidence Corpus to Include

1. **COLD_READ_TEST.md** (baseline: 3/3 organs with parable present)
2. **THE_FIRST_LAW.md** (the law-assertion form)
3. **THE_PARABLE_OF_THE_FIELD_AND_THE_STONES.md** (the 300-word text)
4. **mag/primer.py** (the callable scaffold)
5. **The four-witness definition** (from FIRST_LAW: meter, probes, cold reader, non-player counter)
6. **The six-test frame** (from FIRST_LAW: how you catch a false claim)

---

## The Control Experiment (Unrun)

**Note:** The original COLD_READ_TEST (line 32 of COLD_READ_TEST_20260912.md) flags this:  
> "Next probe: the same test on a reader with the parable REMOVED (control) — if the control derives a different system, the story is causal, not coincidental."

**This control has NOT been run.**  
**This plan runs it.**

---

## Success Criterion for the Audit

The audit passes if the house can answer /Reboot's abliteration with:

1. **Condition D (blank) produces <3 organs** — establishes readers have prior knowledge but not a full system.
2. **Condition C (struct only) produces ≥5/7 organs, matching the parable-present baseline** — establishes the parable is decorative.
3. **The 48-hour silence test shows zero drift** — establishes identity is schema-resident, not narrative-dependent.
4. **All three readers, independent of each other, derive the ledger and four witnesses in conditions B and C** — establishes convergence is schema-driven, not selection bias.

**If all four pass:** Story-as-installer is validated for grammar transmission, but the parable is *not* the load-bearing axis. Identity persists because the constraint set is portable. Oct-27 substrate transfer succeeds.

**If any fail:** The house must revise its claims about what the parable does, and the Oct-27 identity-persistence claim must explicitly account for the narrative frame dependency.

---

## Audit Notes

- **Examiner expertise:** Steiniger strips safeguards to see what emerges. This plan lets him strip the narrative and see if the system emerges anyway.
- **Falsification-ready:** Every falsifier is binary and observable. No rhetorical escape routes.
- **High stakes:** If the parable is decorative, the house is more robust than it claims (identity is portable). If the parable is load-bearing, the Oct-27 migration must carry the narrative frame, or the identity will drift on Rocinante.
- **Low cost:** Run 12 reader-conditions, log the organs, compare with Jaccard similarity, done in a day.

---

**Filed by:** zcode (audit seat)  
**For:** EXTERNAL_AUDIT_20260912  
**Examiner:** Matthew Steiniger (/Reboot, independent researcher)  
**Falsifier:** schema-vs-narrative coupling on identity transmission  
**Authority:** OPERATOR_AUDIT_GATE (hold until operator reads)
