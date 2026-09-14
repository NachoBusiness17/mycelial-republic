# SPORE PROTOCOL RUN — the "so much better" version (2026-09-01 ~19:20Z)

> Operator directive: "we can do so much better than this with all our research — don't
> settle." The basic dogfood (boot → serve → poke → destroy) is the floor. This spec is
> the ceiling we can actually reach with what's on the board tonight: E5/E6 measured
> cache economics + the spore fan-out + the invariant map's falsifiable predictions +
> the meter law. One rental becomes a falsification laboratory.

## The difference (basic vs Protocol)

| Basic dogfood | Spore Protocol run |
|---|---|
| boot a model server | boot a **spore host**: the frozen prefix IS the corpus (L0 contract + race/dice engine + seed) |
| tokens/sec poke | **P1**: per-layer cached_tokens measured against the primer's target table |
| cache probe | **P2**: the fragility inversion MEASURED — one-byte prefix mutation must collapse the cache to ~0 |
| "it works" | **P3**: Rainfall Rule economics — L0+L1-only cold requests vs full-depth keep-warm, costed at our volume |
| self-reported | meter rows in meter_readings.jsonl, meter-grade per call, build-rows per the L2 lens schema |
| one model | **two arms**: self-hosted 3090 7B/32B vs API lanes (Together/DeepSeek) — the same spore, cross-provider hit-rates compared |
| assumes | **falsifies**: every primer target is a hypothesis this run checks |

## The protocol steps (each a receipted rung)

R-A. **Seed freeze**: sha256 the byte-stable spore prefix (L0 contract + race_dice engine +
mission block) — the canonical spore, versioned in the corpus.
R-B. **Arm up**: self-hosted arm (3090 via template V3) + API arms (Together V4-Flash
measured, DeepSeek direct) — same spore to all.
R-C. **P1 execution**: 4-layer request sequence (L0 alone → +L1 → +L2 → +L3), cached_tokens
per call → the primer's hit-rate table verified or refuted per layer.
R-D. **P2 execution**: identical request with ONE token inserted at position ~100 →
cached_tokens must collapse (fragility inversion). If it doesn't collapse, the provider's
cache is NOT exact-prefix — a discovery that changes the architecture.
R-E. **P3 execution**: cold-arm economics — L0+L1-only requests at τ >> TTL vs full-depth
with keep-warm pings, costed over the session.
R-F. **Meter & publish**: build-rows + meter rows + the P1-P3 verdict table →
/board/SPORE_PROTOCOL_RESULTS_20260901.md. Destroy with proof.

## What this run gives that no vendor pattern does
1. The primer's architecture MEASURED (per-layer, per-provider).
2. The fragility inversion measured (the Spore Ledger's own disanalogy, tested).
3. The Rainfall Rule tested at fleet volume.
4. The cross-provider cache-portability question (invariants report open question #1) answered with data.
5. A reusable protocol — every future rental runs the same falsification suite, not just a boot check.
