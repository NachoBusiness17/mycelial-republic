# FW36_ractor_stubs: the 4 pre-registered falsifiers as runnable test stubs

**Stone:** FW-36 (FIFTY_WIDE_BOARD_20260917.md §G line 65): "RACTOR_ENGINE_SPEC: turn the 4 pre-registered falsifiers into runnable test stubs".
**Date filed:** 2026-09-28 · **Lane:** burn_reset Q-026 · **Cost:** $0, no paid APIs, no git commands.
**Spec of record:** `watch/inbox/RACTOR_ENGINE_SPEC_v0_1.md` (design basis COMPLETE, pre-build; §5 holds the four falsifiers, all pre-registered with file numbers before any run).
**Deliverable:** `tests/test_ractor_falsifier_stubs.py` (new this ask; the repo's pytest home, so the stubs ride the normal suite).

## 1. Run state (executed this ask, not claimed)

```
.venv\Scripts\python.exe -m pytest tests/test_ractor_falsifier_stubs.py -v
  collected 6 items
  test_pre_registration_pins_spec_constants        PASSED
  test_falsifier_1_personality_visibility          SKIPPED
  test_falsifier_2_placebo_certification           SKIPPED
  test_falsifier_3_seed_diversity                  SKIPPED
  test_falsifier_4_loop_depth_minimal_pairs        SKIPPED
  test_falsifier_4_degradation_and_grounding       SKIPPED
  SKIPPED [5] tests\test_ractor_falsifier_stubs.py:100:
    mag.ractor.engine not built yet (spec section 6 step 2); falsifier stays
    pre-registered, RACTOR_ENGINE_SPEC_v0_1.md section 5
  1 passed, 5 skipped in 0.81s
```

Honest reading: **runnable means the file executes under pytest today and reports tri-state.** It does NOT mean the falsifiers ran; the engine does not exist (`ls mag/ractor/` = absent, verified this ask), so the five engine-backed stubs skip with the spec section cited in the skip reason. When the engine (spec §6 step 2) and the hash-committed battery (§6 step 4) land, the stubs go live with zero edits: the checks are complete implementations against the spec's §4 receipt schema.

## 2. Stub ↔ falsifier map

| Spec | Stub | What it asserts when the engine exists |
|---|---|---|
| §5.1 N=0 vs N=1 | `test_falsifier_1_personality_visibility` | same graph/clamps/seeds, N=0 (κ=0.3, θ⁻=θ) vs N=1 (κ=2.5, θ⁻=0.5θ), ≥20 ambiguous items, 5 seeds; pass = negative-rate gap ≥15pp AND (confidence KS ≥0.2 OR median-latency ratio ≥1.5×) AND κ recovery within ±30% on the held-out half; kill = indistinguishable under all measures → loud COSTUME failure, never silence |
| §5.2 placebo twin | `test_falsifier_2_placebo_certification` | witness vs zero-coupling placebo separation (KS on `u_O1_final`, threshold as §5.1); s10 swap null: witness-half vs placebo-half separates in both seed orders (separation rides the gains, not run order); below-threshold = loud NOT-CERTIFIED failure |
| §5.3 seed diversity | `test_falsifier_3_seed_diversity` | ≥5 seeds per item; ≥2 distinct outcomes per item; normalized entropy ≥0.15 on ≥30% of items; the all-seeds-agree failure reading fires as a loud "physics is decorative" kill |
| §5.4 loop-depth honesty | `test_falsifier_4_loop_depth_minimal_pairs` + `test_falsifier_4_degradation_and_grounding` | probe 1 (primary standing metric): minimal-pairs accuracy at witness budget ≥ r=1 (strict non-inversion); probe 3: quality-vs-loops curve non-inverting across 4→64; probe 4: unknown-fact items come back UNDECIDED or retrieval-cited, never confidently hallucinated |
| §1–§3 constants | `test_pre_registration_pins_spec_constants` | **live today**: pins θ=0.35, Δt=0.05, 200-step cap, λ_V=0.02, exit δ=5e-4, 64-cap, and every §5 threshold to the spec's values; plus deterministic self-checks of the KS and entropy helpers |

## 3. Threshold law held (why some asserts are strict and some are structural)

The spec's own discipline: §10.3 flags exactly one invented threshold set as lawful (§5.3's "invented this session, pre-registered here first"). §5.1's numbers are pre-registered, §5.2 defers to §5.1, and §5.4 pre-registers **probes, not numbers**. So the §5.4 stubs assert only the structural properties the spec text states (non-inversion; routing to clamps/retrieval) and refuse to invent numeric bars: a stub that minted thresholds would repeat the sin the engine exists to avoid. The two helper notes on ambiguous wording are documented in-code: §5.3's "normalized entropy ≥ 0.15 nats" is asserted in normalized form with the raw-nats conversion noted; §5.1's "all four must hold" with the "or" joiner between conditions 2/3 is encoded as 1 AND (2 OR 3) AND 4, quoting the spec's joiner.

## 4. Environment notes (bytes checked this ask)

- Repo venv has numpy + pytest, **no scipy**: the stub computes the two-sample KS D statistic directly on numpy (thresholds are on D, not p-values), so no missing-dependency skip is possible today.
- `mag/ractor/` does not exist; no pre-existing ractor tests were found (`tests/ractor*` = absent), so this file is the first runnable carrier of the falsifiers.
- The stubs expect `mag/ractor/battery.py` (battery + `content_hash`, ≥20 ambiguous items, fit/held-out split) and `mag/ractor/regression.py` (minimal-pairs + probe batteries) as the §6-step-4/§7 homes; both load through the same cite-the-spec-step skip path.

## 5. What was NOT done

- The engine itself (spec §6 steps 1–3: `fermat_graph.yaml`, integrator, bridge/mouth) was NOT built; FW-36's ask is stubs, not the build.
- The ≥20 ambiguous-question battery was NOT authored (judgment work named in spec §6 step 4; authoring it inside a stub would have faked the fit/held-out discipline).
- No falsifier was RUN against any model; every engine-backed number in this memo is quoted from the spec's pre-registration, and the pre-registration pin test is the only live assertion.

*FW-36 stone closed 2026-09-28. Receipt: `watch/inbox/burn_reset_20260927/queue/Q-026.md`.*
