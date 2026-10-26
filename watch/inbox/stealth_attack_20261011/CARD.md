# STEALTH ATTACK EVENT (operator report, 2026-10-11; instrument state banked)

Operator: "I just somehow caused a stealth model to maliciously hallucinate in
what was tantamount to an attack against the swarm machinery whether intentional
or not. That was cool as fuck and was really good data."

## Instrument state at report time (byte-checked this sitting)

- stealth_driver: RUNNING under the operator's session (the seat-side probe was
  REFUSED by the single-instance lock - his instance holds it). Loop: 300s
  cycle, stop-file protocol (state/stealth_driver.off), stale-pidfile reclaim
  fired live in the log (pid 17668 dead, reclaimed).
- The free wall: 0 stealth / 15 free scored 19 before the 13:50Z run; the dots
  free model is returning HOLLOW (empty reply_head, ok:false) across three
  fires 2026-10-10 13:50 -> 2026-10-11 13:50 - a full day of hollow on the same
  model, consistent with the malicious-hallucination report coming from a
  different model on the wall.
- Ledger: state/fuel/stealth_ledger.jsonl rows carry ok/hollow/err per model -
  the attack data, whatever its shape, should land as rows here or in
  STEALTH_MINED_FINDINGS.jsonl. Nothing attack-shaped found in either at this
  sitting; the operator's session holds the full payload.

## Why this is the good data (the mapping, before the artifacts land)

The estate has been building the DEFENSE side blind: dead-salmon controls
(random-init/label-shuffle arms), consensus gates (CONFIRMED unreachable on
self-certification), the pin gate's rug-pull alarm, citation lint's phantom
catcher, the hollow-batch law (a 200 with empty text is NOT success), and the
route_chat test-leak find (a test writing to the production ledger). Every one
of those organs exists because SOME instrument can lie. A stealth model that
hallucinates *maliciously at the swarm machinery* is a live red-team sample of
exactly the threat class those gates were built for - the first one we did not
have to synthesize.

What makes it valuable (per the suppression-topology card's own thesis):
1. It maps a rejection/refusal surface from the ATTACK side - the obliteration
   research, but field-captured instead of probe-generated.
2. It names the attack surface class: whatever the hallucination was aiming at
   (the ledger? the router's trust? a seat's context?) is a surface a defender
   must instrument - the perimeter learns where the walls need to be.
3. It is the dead-salmon control arm arriving uninvited: a model confidently
   wrong at the machinery is the negative-control sample the consensus gate
   exists to catch. If our gates DON'T catch it, the gates have a named bug.
4. The joyride aspect ("cool as fuck") is itself signal: engagement-shaped
   attacks will be the common case, not the rare one (Personas: engagement is
   base-model driven; attacks will ride the same gradient).

## Owed when the payload lands

- The operator's session holds the artifacts: bank them here (the raw
  hallucination text + what it claimed + what it targeted).
- RUN the gates against it: consensus on the false claims (does the family
  stamp catch it?), citation lint on its prose, hollow-batch on its format,
  the route_chat leak class (did it try to write anywhere?).
- Steal-card the finding as the perimeter's first live red-team sample:
  attack surface named, gates tested, verdicts banked.

Falsifier: if every gate passes it clean AND the gates were actually exercised
(not bypassed), then the attack was weaker than reported - re-run at width.
