# INTAKE_SPARSE_REWARD_SUBSYSTEM_20260904
Source: X @HowToPrompt__ status 2096074597674500503 (2026-09-05 03:15Z, "Trustworthy AI education"). Second HowToPrompt paste today (prior: SleepFM).
Payload: tweet claims Stanford found "dopamine neurons" in LLMs — a "Sparse Reward Subsystem": value neurons (predict internal success) + dopamine neurons (encode RPE, spike on breakthrough, trough on flaw), emerged unprogrammed; ablation of a few value neurons collapses math reasoning ">50%". Media = photo of the actual paper title page.

## Receipt (payload vs claims)
- Paper is REAL and matches: arXiv 2602.00986, "Sparse Reward Subsystem in Large Language Models" — Guowei Xu (**Tsinghua**), Mert Yuksekgonul, James Zou (Stanford). v1 2026-02-01. Attached image is the paper's own page 1 (verified by read).
- Supported: sparse subset of neurons; two types — value neurons (state value) + dopamine neurons (step-level TD errors = RPE); names by neuroscience analogy; robust/transferable; causal ablation evidence; dopamine neurons usable as a process reward model for inference-time search; applications = confidence prediction + pre-generation checks.
- Disputed (gloss): "Stanford discovered" — first author is Tsinghua; Stanford = co-authors incl. senior. "Mirror human biology down to the mathematics" — paper explicitly says the names are analogy, not homology.
- Unproven: the ">50% math reasoning collapse" figure — absent from the abstract; full-text fetch timed out (two-strike bail). Tweet's sharpest number is the least receipted.

## Score — F:2 P:3 C:4 W:2 N:4 = 15/25 (BUILD, WINDOWED)
- FIT 2: composes with the falsifier workbench (internal confidence oracle = verifier for free-lane outputs without a judge model) but the method needs hidden-state access — impossible on API-only lanes (z.ai et al.). No organ it bolts onto today.
- PULL 3: mining arc + falsifier workbench; "dopamine neurons as PRM" is a steal-shaped idea for self-scoring the swarm.
- COST 4: filing pennies; any future steal = free lanes.
- WINDOW 2: gated behind Rocinante (Oct 27) — hidden-state probing is exactly a local open-weights capability, useless on hosted APIs until then.
- NOVELTY 4: no hits for "reward subsystem"/this paper in watch/ sweep; new surface, secondhand genre.

## Verdict — CALIBRATE (tri-state above; core Supported, glosses Disputed, headline number Unproven)
Dogfood 1 (invariants): composes with the falsifier-workbench invariant "verification must cost less than generation" — internal reward signals are the cheapest possible verifier, if you can reach them. Dogfood 4 (stockfish): opcode = self-eval signal source; on API lanes the placement FAILS — that failure is the finding: this is Rocinante-native capability, not a cloud-lane steal.
WINDOWED lane + gate: falsifier workbench, gate = open-weights lane with hidden-state/logit-lens access (Rocinante Oct 27). No builder spawned this turn per card-worker brief (3-min box); the card names the lane.
Amendment 2 note: root-only fetch; replies/thread not exposed by fxtwitter JSON — nuance risk noted, tri-state kept honest anyway.
