# AC8 — MiMo RL environments vs the estate (2026-09-30)

Seat: Explore (read-only), banked by orchestrator. Sources: HF XiaomiMiMo/MiMo-V2.6-RL-oss + estate tools (legality_dataset, legality_propagator, gps_mcp, duel_harness).

| Dimension | Xiaomi MiMo | Estate | Ahead |
|---|---|---|---|
| Environment format | Real SWE tasks, Docker-packaged | Seeded water-graph boards (`tools/legality_dataset.py`), flat token render | MiMo |
| Verifier | Hidden test patches, 30-min timeout | Exact constraint propagator (`tools/legality_propagator.py`), engine-free, agreement law: any disagreement = propagator bug | Estate |
| Reward signal | Rule-based, binary pass/fail | 5-way label (3 illegal reasons + gain/no-gain), measured on real engine; lattice abstain (soundness 0.883→0.986) | Estate |
| Scale | Industrial RL fleet | 20k states, one box, $0 | MiMo |
| Diversity | Thousands of real repos | One physics family (Mountain), 5 verbs | MiMo |
| Training target | Agentic SWE model | Tiny model internalizing law + measured model routing (`tools/gps_mcp`) | Split — each fits its budget |
| Openness | Public on HF | Private but byte-reproducible (sha-pinned MANIFEST) | MiMo |

**Steal from MiMo (3):**
1. Docker-packaged disposable execution sandboxes per ask
2. Hidden holdout verifier cases the tested lane never sees
3. Declared wall-clock verifier budget so a hung lane can't stall the meter

**Our moat (3):**
1. Provably exact, instant, $0 oracle vs their flaky-timed tests
2. Determinism law — seeded, hash-pinned, regenerable
3. Calibrated cross-family honesty (`tools/duel_harness.py`: blind judge, position swap, CIs, admits p=0.23)
