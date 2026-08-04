# Milestones — evidence-gated

Agents and humans update **only with evidence paths**. Do not mark complete on vibes.

## Dual progress (honest — 2026-07-28)

Two definitions of “moving.” Do not collapse them.

| Track | Meaning | Status now | Unblocks |
|-------|---------|------------|----------|
| **Practice R0-lite** | Craft + Locus + selftest + curated corpus + Mag residual/IJL — **mirror practice without weights** | **active** | Operator daily; not gated on full X zip |
| **Weight R0** | Train private adapter on ≥800 annotated operator rows + post-train chord | **blocked / optional** | W0.0 full archive *or* boot soil density → W0.3 → W0.6–W0.8 |

Standing: empty `data/raw` blocks **weight** R0 honesty. Empty soil does **not** block Mag or practice R0-lite (see AGENTS.md craft-first).

### Agency shape (goal interpretation — 2026-07-31)

**Canonical:** [`AGENCY_SHAPE.md`](AGENCY_SHAPE.md) · commitment `agency-shape-life-ops-20260731`

| Track | Meaning | Status now |
|-------|---------|------------|
| **G0 agency spine** | Boundary + scoped access + notice/draft + L3 nod + audit | **active** (Mag seats / residual) |
| **G1 practice R0-lite** | Mirror practice without weights | **partial** (same as dual progress above) |
| **G2 weight R0** | Private adapter + post-train chord | **blocked / optional** |
| **G3 life-ops spore** | First real tedious loop (notice → draft → L3 approve → audit) without root over whole life | **deferred** — unlocked by G0, not a substitute for G0 |
| **G4 forest** | Others run G0–G3 without a king | **later** (R1+) |

Do not mark G3 done on demos that skip L3 or dump root credentials.

| ID | Name | Status | Date | Evidence |
|----|------|--------|------|----------|
| W0.0 | Archive in `data/raw` | **pending** | | PO export; only `.gitkeep` present |
| W0.0b | Boot soil from exports (no full zip) | **open** | 2026-07-28 | `docs/BOOT_SOIL.md`; annotate from `data/exports/*` |
| W0.1 | Prep → posts.jsonl | **partial** | 2026-07-27 | Boot exports only: `data/exports/*.jsonl` (not full archive prep) |
| W0.2 | Annotated train set | **partial** | 2026-08-02 | `data/annotated/mirror_train.jsonl` **115** rows (22 high / 93 med; 0 errors); practice gate 100 **PASS**; weight gate 800 |
| W0.3 | validate --min 800 | pending | | blocked on density |
| W0.4 | CONSTITUTION.md | **done** | 2026-07-20 | `docs/CONSTITUTION.md` v0.1.0; `CONTRIBUTING.md` |
| W0.5 | Live selftest baseline | **done** | 2026-07-27 | `logs/selftest/latest.json` 12/12 overall≈0.694; `vector_map_latest.md`; pytest `tests/test_selftest_vector_map.py` 5 passed |
| W0.6 | First train adapter | pending | | weight track only |
| W0.7 | Local inference path | pending | | weight track only |
| W0.8 | Post-train chord + live selftest | pending | | weight track only |
| **R0-lite** | Practice seed (no weights) | **partial** | 2026-07-28 | selftest + Locus + Mag agent_state + exports; not spore |
| **R0** | Seed Mirror complete (weights) | pending | | requires W0.8 |
| W1.1 | Spore package | pending | | |
| W1.2 | Public release tag | pending | | |
| W1.3 | ≥3 external testers | pending | | |
| **R1** | First Spore complete | pending | | requires W1.3 |
| **R2** | Early Mycelium (5 mirrors) | pending | | |
| **R3** | Hardened Republic | pending | | |
| **R4** | Parallel Construction | pending | | |

Standing rule: if W0.0 pending, **no weight-train / network / token work**. Practice R0-lite and Mag may proceed.

See `docs/AGENT_ROADMAP.md` for full DAG, roles, and predictions.  
Agent recall (Mag): `../local_sovereign_agent/memory/agent_state/LATEST.md`