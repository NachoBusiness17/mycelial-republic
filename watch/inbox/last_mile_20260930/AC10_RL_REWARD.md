# AC10 — RL reward design for the estate (2026-09-30)

Seat: Explore (read-only), banked by orchestrator. Sources read: tools/gps_mcp/ledger.py, logs/duel/duels.jsonl, mag/gwap_payload.py, mag/gwap_to_gps.py, tools/legality_propagator.py.

**(1) Signals already emitted.** gps ledger: binary verdicts with `evidence_hash` into a running `pass_rate` per (model, task_shape) plus `cost_usd_per_call`. Duel rows: winner + per-criterion 0-5 scores (root-cause accuracy, evidence citations, falsifying predicates, actionability), blind judge with position swap. gwap_payload: `agreement_score` -> ladder (VERIFIED_AGREE >=0.6, CHALLENGE >=0.3, DISPUTE, BLOCKED; suspected collusion demotes AGREE->CHALLENGE); gwap_to_gps feeds only AGREE(=1)/DISPUTE(=0); CHALLENGE/BLOCKED are skips. legality_propagator: exact, $0 correctness oracle.

**(2) What a policy would optimize.** Max agreement -> sycophancy (collusion demotion already fights this). Max pass_rate -> Goodhart into easy-shape farming and ledger poisoning. Honest optima: propagator-verified law extraction, soundness-at-coverage (V7 lattice, 0.883->0.986), receipt-hashed verdicts.

**(3) Lesson (MiMo thread cross-ref AC4).** MiMo's rule rewards are cheap, dense, gameable at the seam (test-pass != correct). Receipt rewards cost ~$0.03/judgment but every credit is auditable — reward hacking leaves a trail. Spend receipts where the gradient flows; rules for dense shaping. "Every reward term is a place to cheat" — audit each metered term as an exploit surface.

**(4) v0 lane-chooser.** r = delta-H(Beta posterior over pass_rate) / cost_usd - redundancy penalty on well-measured shapes; only receipt-backed verdicts pay; skips pay 0.
