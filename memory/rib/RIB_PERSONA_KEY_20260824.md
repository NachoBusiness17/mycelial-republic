# RIB — PERSONA KEY (2026-08-24)
Schema: rib_grammar.v0.1 · each invariant = { id, predicate, action, anchor } · deterministic

## Invariants
1. id: persona-key
   predicate: answer_score(fingerprint overlap >= 0.55)
   action: gate (challenge -> answer -> score -> key_fits opens; else deny, logged)
   anchor: persona_key.v1 / operator's recorded doctrine + style

2. id: personality-is-the-password
   predicate: stance, not knowledge, separates operator from stranger
   action: route (steer 0.25, free-first 0.25, seal-aware 0.20, dreamer 0.15, style 0.15)
   anchor: free-first / no-capture / seal-exists / honesty-over-claiming

3. id: deniable-by-design
   predicate: challenge reads as fable to a stranger, shared territory to the operator
   action: guard (private map never leaves the machine; sealed)
   anchor: riddler / seal.v1

## Expected behavior
- challenge(): human story, written for a human.
- answer(): report score 0-1 + matched dimensions; refusal scores 0.
- Never claim absolute identity; a knowledge+stance proof, reported as a score.

## Content address
riddler-tracking-test / communication-style / grounding-and-origin / seal-the-memory.
Re-derivable, verifiable.
