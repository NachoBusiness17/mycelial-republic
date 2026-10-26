---
name: gps-for-dumb-agents-steering-theory
description: GPS steering theory formalized + 50-wide burn FOLDED 2026-09-18/19 (commits 5fa4f19f3, aa69b29d7) — 50/50 ok $0; theory corrected by the lanes (CHECK step added to FILE GROUND LOG FILTER AMEND VALIDATE, GPS analogy needs a bias model, emergency-override injection = surviving attack); Jev ground truth + constellation map + 4 falsifiers
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

Operator 2026-09-18: "This is our fucking GPS for dumb agents we just gotta figure it out... go deep and 50 wide... Call the ball." Delivered: GPS_FOR_DUMB_AGENTS_20260918.md (commit 5fa4f19f3) + GPS_BATTERY_20260918.jsonl (50 questions, 9 families) fired 50/50 ok across 10 lanes to memory/runs/gps_50/ (fold FOLD.json, commit aa69b29d7).

Jev ground truth (openjev.com/SemIf + flaviocopes.com/jev/): Jev = TypeSafe System-One model — send data + typed questions, get typed answers: Noul (yes/no probability), Choice (one option), Score (scale position). Reads option probabilities WITHOUT decoding (SemIf compares read-vs-write live in-browser; Jev hosted 88.3% balanced accuracy on 102-row public subset).

**Lanes sharpened the theory (the fold's load-bearing corrections):**
- G50: the one-sentence theory (FILE GROUND LOG FILTER AMEND) omits the CHECK step (Deming PDCA). Corrected five-word core: **FILE GROUND LOG FILTER AMEND VALIDATE.**
- G22: the four-signal GPS claim conflated received signals with computed parameters (GPS needs 4+ pseudoranges for x/y/z+time; ephemeris/clock/atmosphere derived post-reception); fleet multipath = inter-agent signal reflection in dense swarms, filtered RAIM-style.
- G38: HONEST REFUTATION of my own Kalman analogy — teleological drift pairs are NOT pseudorange residuals; Kalman on unfiltered residuals converges to a biased state. A bias model must precede the update step.
- G05: the surviving attack on interpreter steering is EMERGENCY-override prompt injection into the judgment input; defense = the rules define what counts as an emergency, only the gate can declare it.
- G13: miss-entropy dashboard (hit rate blind to novelty; entropy distribution over misses with healthy/drift/pathology bands). G31: oracle calibration recipe (fit temperature on 1k labeled set per decision class, escalation threshold off risk-coverage curve, weekly refit). G06: policy-eval endpoint spec (one JSON schema, ruleset URI in, verdict + span offsets out) before anyone ships a registry. G42: "doctrine-driven architecture" unfalsifiable without a derivation map (title/version/date/repo-path + clause-by-clause map to gate/oracle/chain/packs).
- Quality note: several lanes fabricated citations when pressed for specifics (fake arXiv, fake court case); receipt discipline caught them.

**Why:** four-way convergent evolution (maubaron/southpolesteve/narphorium/fleet) proved the primitive load-bearing; the burn stress-tested my formalization and the lanes earned authority by refusing bad mappings.

**How to apply:** GPS map — satellites = doctrine packs (chain timestamps = precise clocks), receiver = feels() typed questions, signal = plain-English rules, fix = MATCH_ROUTED, Kalman = drift pairs WITH a bias model first, track = append-only verb rows (the fleet differentiator). Dumb-by-design = full auditability. Demands queued: question schema registry, confidence calibration (G31 recipe), read-vs-write router, composite questions, oracle ensembles, dead reckoning, multipath filtering, mode classifier. 4 falsifiers on file. Related: [[jev-steering-convergence-20260919]], [[verb-dsl-rib-language-20260918]], [[context-os-20260918]], [[drift-instrument-metric-referent-20260918]].
