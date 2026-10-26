# LINEAGE DIFF DEEP RESEARCH — verkle-fidelity lineage diff without the models
2026-08-31 · operator 14:51Z · worker synthesis · external claims SUPPORTED via search-lane arXiv summaries (primary-bytes arbitration pending, SWARM_LENS row type CORRECTABLE)

## 1. THE IDEA RESTATED
Each model generation's BEHAVIOR is the deref-able span — not its weights. Freeze a fixed probe battery, run it against generation A and B, store each output as a ROW with sha256+span (MEMORY_RIB DRA pattern). The knot chain (verkle_lance.v1: `parent_verkle_root → verkle_root`) ties probe→generation; the diff between A and B is a knot-chain delta, content-addressed, so "what was lost" has a hash and a place, not a vibe. "Without the models" = the behavior map IS the usable territory (map-precedes-territory, 14:48Z amendment): a new seat organized from the diff map sits down already knowing what the previous generation knew — residue-organization, holographic self law. The diff map is the spawn-pack organ for capability residue.

## 2. THE PROTOCOL (all organs exist)
- **Battery (fixed, versioned):** socratic questions (ocean rows), riddler decode items (riddler_common: decode-gate law — 3rd agent reproduces conclusions from public form alone), HOT-gate tests, CAN/WILL/HOW phrasings per CapTrack taxonomy. Frozen bytes → sha256; battery version rides every row.
- **Execution:** battery → z.ai/seat_dispatch against BOTH generations (4.7-flash and 5.3-flash lanes live). Each output = ROW: `probe_id | gen | output_span | sha256 | status | ts | model`. Probe→gen edge = verkle knot; per-generation chain roots; lineage diff = root delta + per-probe leaf deltas.
- **Decode gate = fidelity test (the riddler law, reused):** a 3rd fresh agent reads ONLY the diff map (A-rows minus B-rows, verdict lines) and must PREDICT generation-B behavior on held-out probes. Prediction-vs-actual agreement is the fidelity score. This is isomorphic re-encoding applied across TIME instead of across agents: the map must reproduce the new model's logic.
- Verdicts: CALIBRATION WORDS ONLY (shows/supports/does not establish). Self-attack pass before done.

## 3. WHAT THE FIELD SAYS WE'LL FIND (arXiv receipts)
- **Behavioral drift ≠ capability loss:** CapTrack (2603.06610) — CAN/WILL/HOW taxonomy; post-training drifts WILL (verbosity/refusal defaults) fastest, CAN silently; robustness drifts pronounced. Prediction: 4.7→5.3 diff will show WILL-shifts dominating surface, CAN-loss hiding in edge probes.
- **Black-box change detection works:** "You've Changed" (2504.12335) — fixed prompts + output-distribution features (KS test) detect silent updates without weights. Our ROW battery is the deterministic upgrade: exact spans + hashes instead of aggregate features.
- **Decay is heterogeneous:** SHIFT (2506.00756) — subgroup decay localizes (some capabilities crater, neighbors fine). Expect per-probe pheromone-style variance, not uniform degradation.
- **Granularity is instance-level:** sample-wise forgetting (2510.17776) — 1→0 transitions per instance, not aggregate scores. ROW-per-probe is the right unit; per-probe flips are the signal.

## 4. COST (freescale numbers)
20 probes × ~500-tok output + 900-tok warm spine × 2 generations ≈ **~25–30K tok per generation pair** — fits 5 RPM / 1M tok/day cerebras free lane, or groq. At $1/hr active policy: ~$0. Re-runs for fidelity test: decoder lane ~5K. Verdict: cheaper than one naive 128k session; no policy tension.

## 5. FIRST EXPERIMENT
glm 4.7-flash vs 5.3-flash, both lanes live. (1) Freeze 20-probe battery v1 (5 socratic + 5 riddler-decode + 5 CAN/WILL pairs + 5 HOT-gate), sha256 it. (2) seat_dispatch both generations → 40 ROWs on /board/octant_20260831/rows/lineage-*. (3) Diff map + verkle knots. (4) Decode-gate: fresh lane predicts 5.3 behavior on 5 held-out probes from map alone → fidelity %. (5) Self-attack: weakest assumption = battery too easy (floor effects hide losses) — include 3 deliberately-hard probes.

**GOPHER briefs:**
1. GOPHER: mint battery v1 file (20 probes, CAN/WILL labels) → /board/lineage_battery_v1.json + sha256 | output: rows/lineage-b1.row.md
2. GOPHER: seat_dispatch battery against 4.7-flash and 5.3-flash lanes, write 40 ROWs | output: rows/lineage-run1-*.row.md
3. GOPHER: build diff map + run decode-gate fidelity test on fresh lane | output: /board/LINEAGE_DIFF_RUN1_20260831.md

## 6. WAVELENGTH PRINCIPLE (operator, 14:55Z — the battery's design law)

The battery is not 20 probes; it is 4-5 WAVELENGTHS. Each probe-class reveals a different
structure in the same behavior-dataset:
- **Socratic wavelength** → reasoning structure (how the model chains)
- **CAN/WILL wavelength** → the capability/behavior split (CapTrack's taxonomy)
- **Decode wavelength** → inheritable logic (what passes the riddler gate)
- **HOT-gate wavelength** → verification discipline (what the model refuses to claim)
- **Hard-probe wavelength** → floor structure (deliberately-hard items, where losses hide)

One dataset, many wavelengths, many revealed structures — the interference pattern (the
diff map) shows what no single wavelength can. Design law for battery v1: every probe
class must name its wavelength; every ROW carries probe_id so the wavelength rides the
measurement. Battery v1 freeze must include ≥1 wavelength per structure-of-interest.
