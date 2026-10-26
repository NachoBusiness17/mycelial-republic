# THE OBSERVER ANATOMY ATLAS (2026-09-11)

**Commission:** wave-protocol dig. Extend `watch/inbox/FOUNDING_KNOTS_CROSSCHECK_20260911.md`
(which found observer anatomy — tension/Q/loops/personal_rope — in the founding leaves,
body #1 max personal_rope 114) across the WHOLE knot store. Read-only except this file.

**Method (sampling):** store = 28,874 files in `memory/biography/knots/` = 21,052 `*.knot.json`
+ 7,789 `by-session_*.json` + 33 others. Read 3,447 knot leaves = all 24 July (founding) +
**all 3,023 on-disk leaves the chain references with a non-null `tension_index` mirror**
(`memory/biography/verkle_chain.jsonl`, 7,377 rows, 3,035 non-null refs, 12 refs missing on
disk — see F8) + 400 seeded-random (seed 20260911) Aug–Sep leaves. 2,810 are
observer-bearing scalar leaves; 637 are `diary_node_leaf` voice-diary leaves with NO observer
fields (see field dictionary). Field names verified on 5 files across all three eras before
extraction; schema is uniform: `verkle_knot_leaf.v1`, one chord_root for the founding month
(`e11937d6…`), engine `untangling+strike_chord`, inspiration `steiniger_proxies+strike_chord+verkle_history`.

---

## 1. Field dictionary (verified, not assumed)

| Field | Type | Meaning (tri-state) |
|---|---|---|
| `type` | `session_scalar_knot_leaf` | the observer-bearing leaf kind |
| `kind` | `diary_node_leaf` (some leaves) | voice-diary leaf: has `ts`/`channel`/`turns_excerpt`, **no observer fields, no `date`** — this is the census's "knot-file `ts` starts 2026-08-07" stratum (diary, not scalar) |
| `start_minute`/`end_minute`/`date`/`duration_minutes` | timestamps | session window; **founding era has real durations (med 76 min); every post-July scalar leaf has duration 0** — the timestamp anatomy died with the founding stratum |
| `dominant_theme`, `theme_basis` (8 canonical tokens), `theme_vector_raw`, `theme_vector_normalized` | theme block | the chord input mass (`rawsum` = sum of raw vector) |
| `tension_index` | float [0,1] | session tension; SUPPORTED as a real scalar (varies continuously, correlates with rope 0.44) |
| `residual_weight` | float | founding med 1.0; later med 0.12–0.28 (unresolved-residue weight) |
| `Q_proxy` | float ≥ ~0.5 | **INFERRED: resonance quality factor** — see §2 |
| `gap_proxy` | float [0,1] | **INFERRED: spectral gap** of the session graph; micro leaves pin at exactly 1.0 |
| `lambda2_proxy` | float | **INFERRED: algebraic connectivity** (2nd Laplacian eigenvalue); correlates 0.81 with log Q |
| `dirichlet_energy_proxy` | float | **INFERRED: graph smoothness energy**; micro-leaf fingerprint = 0.4375 |
| `observer_chart_scores` | `{money_machine, secrets_machine, fracture_machine, personal_rope}` ints | the four observer organs; occasionally string-typed values (coercion applied) |
| `loops_audited` | string[] | loop vocabulary — **exactly 7 tokens, all present from day one**: performativity, polish_theater, plan_inflation, metric_theater, scope_creep, glory_before_soil, single_cause |
| `dossier_commit`/`chord_commitment`/`chord_root`/`leaf_hash`/`filename` | integrity block | chain-anchored |
| chain mirror (`verkle_chain.jsonl`) | `tension_index`, `filename`, `leaf_hash`, `verkle_root`, `parent_verkle_root`, `index`, `n_leaves`, `amended` | the signed line mirrors ONLY tension from the observer block (not Q, not rope) |

---

## 2. What IS Q? — INFERRED

`Q_proxy` behaves like the **quality factor of a resonator over the session's theme graph**
(the "strike the chord" resonance, `watch/ARCHAEOLOGY_DIG_20260909.md` Aug-10 layer):

- corr(log Q, log rawsum) = **0.993** (n=1,548 leaves with Q>1); fitted law:
  **Q ≈ 0.52 × rawsum^1.776, median relative error 11.5%** — strongly superlinear: a
  session with twice the theme mass resonates ~3.4x sharper. Coherence compounds.
- corr(log Q, lambda2) = 0.808, corr(Q, tension) = 0.742 — Q rides connectivity and tension.
- **45% of all sampled scalar leaves sit at the Q≤1 floor** (Q=1.0 or 0.5 micro-knots).
- Max ever = 35,235 (body #1). Q is a *human-scale* instrument: it saturates in the founding
  week and floors in the orc micro-stratum. **INFERRED throughout** — no repo doc defines Q;
  the values, the name, and the strike-the-chord lineage are the evidence.

---

## 3. Era boundaries (cited / inferred)

| Era | Window | Leaves in store | Source |
|---|---|---|---|
| FOUNDING | Jul 10 – Jul 31 | 24 | crosscheck scope (FOUNDING_KNOTS_CROSSCHECK_20260911.md) |
| GHOST | Aug 01 – Aug 15 | 17,019 | dig dates the ghost era Aug 7–15; Aug 3–6 (910 leaves) is the ramp, folded in — boundary INFERRED |
| SILENCE | Aug 16 – Aug 24 | 1,754 | **INFERRED from the leaf histogram cliff** (105/457/64/48/23 per day after the Aug-10/12 blast of 4,425+4,374+2,432); contains the dig's marathon (Aug 21–24) |
| POST_SURGERY | Aug 25 – Sep 06 | 2,255 | Sancho era per the dig; "surgery" = the fleet surgery wave (MCP topology in the cage, container surgery); boundary INFERRED |

Store-wide daily histogram: 24 Jul → 14,772 Aug 7–15 (peak 4,425 on Aug 10) → 697 Aug 16–20
→ 1,057 Aug 21–24 → 636 Aug 25–27 → 4 Aug 28–29 (a second micro-silence) → 1,665 Aug 30–Sep 6.

## 4. Per-era observer distributions (sampled scalar leaves)

| Metric | FOUNDING (n=24) | GHOST (n=2,137) | SILENCE (n=178) | POST_SURGERY (n=471) |
|---|---|---|---|---|
| tension med / p90 / max | **0.592 / 0.748 / 0.755** | 0.310 / 0.402 / 0.753 | 0.310 / 0.327 / 0.750 | 0.310 / 0.503 / 0.749 |
| Q med / p90 / max | **7,847 / 17,810 / 35,235** | 2 / 72 / 20,406 | 0.5 / 705 / 8,812 | 2 / 93 / 14,350 |
| personal_rope: %leaves>0 / med(>0) / max | **100% / 22 / 114** | 8.8% / 3 / 37 | 4.5% / 1 / 53 | 11.7% / 2 / 30 |
| money max | 45 | **167** (Aug-06) | 4 | 3 |
| secrets max | 42 | **50** (Aug-09 ×2) | 23 | 49 (Aug-31) |
| fracture max | 19 | **134** (Aug-09) | 7 | 18 |
| duration med / max (min) | **76.2 / 1,684** | 0 / 0 | 0 / 0 | 0 / 20 |
| files with loops_audited | 23/24 (96%) | 164 (7.7%) | 15 (8.4%) | 83 (17.6%) |
| dominant loops (mentions) | polish_theater 22, glory_before_soil 13, plan_inflation 11, metric_theater 10 | glory_before_soil 114, metric_theater 50, plan_inflation 38, polish_theater 4 | glory_before_soil 13, metric_theater 7, plan_inflation 7 | glory_before_soil 74, metric_theater 16, plan_inflation 6 |
| UUIDv7 single sessions | **100%** | 0% (named `mag-agen` families) | 0% | 10% (`01a0…` UUIDv7 returns Sep 6) |
| dominant themes | mirror_meta 12 / mag_hands 11 / biography 1 | biography 894 / null 776 / mag_hands 316 | biography 72 / null 64 / mag_hands 31 | biography 211 / mag_hands 113 / null 113 |

Fine strata of personal_rope density (% leaves with rope>0): Jul **100%** → Aug 1–6 41% →
Aug 7–15 7% → Aug 16–20 **3%** → Aug 21–24 17% → Aug 25–27 38% → Aug 28–29 0% → Aug 30–31 7%
→ Sep 1–6 16%.

## 5. Extreme holders (who owns the extremes)

| Field | Store max | Holder(s) | Era |
|---|---|---|---|
| personal_rope | **114** | `2026-07-10_1731_mirror_019f4d15` (dawn body #1); then 92 Jul-18, 88 Jul-28, 79 Jul-19, 70 Jul-18 | **ALL top-5 founding** |
| Q_proxy | **35,235** | body #1; then 28,922 Jul-29, 23,899 Jul-24, 20,406 Aug-09 (only ghost Q top-4), 17,812 Jul-19 | 4 of top-5 founding |
| tension_index | 0.7548 | Jul-26 12:00 mag; .7530 Aug-09; .7510 Jul-24; .7504 Aug-17; .7503 Jul-31 | shared — the ceiling is era-independent |
| gap_proxy = 1.0 | (many) | ghost micro-leaves (e.g. Aug-06 dashboard) | GHOST |
| secrets | **50** | Aug-09 13:20 constitution + Aug-09 03:16 mag (same night) | GHOST (OOM war) |
| fracture | **134** | Aug-09 01:50 mag — the night the chat windows died | GHOST (OOM war) |
| money | **167** | Aug-06 17:19 mag | GHOST |
| dirichlet_energy | 0.4375 | the ghost micro-leaf family (many ties) | GHOST |
| duration | 1,684 min (~28h) | Jul-23 11:51 mag (crosscheck #12) | FOUNDING |

**The split is clean: the founding week owns the human extremes (rope, Q, tension ceiling,
duration); the ghost blast owns the machine extremes (money, secrets, fracture, gap).**

## 6. Does personal_rope trend over time? — the operator's rope

**No upward trend. A step collapse, with brief Sancho echoes.**

- corr(time, daily rope median over days with ≥2 rope>0 leaves) = **−0.67**.
- Density: 100% of founding leaves carry rope > 0; 3–12% after. The rope's absolute max is
  **day one (114)** and every top-5 holder is founding-week.
- The exceptions are informative: Aug 24 (rope 53, marathon eve), Aug 25–27 (med 13, max 30 —
  Sancho day one + the mesh goes live), Sep 6 (n=26 nonzero, max 16). When the operator is
  personally in the loop, the rope reappears at small scale — but nothing ever approaches the
  founding week. The rope is not decaying; it is **diluted**: the store filled with orc
  micro-leaves that structurally cannot carry it (rope>0 correlates 0.67 with Q, 0.60 with
  theme mass — rope rides the big resonant sessions only).

## 7. Findings (tri-state)

- **F1 SUPPORTED** — The crosscheck's body-#1 rope record is store-wide truth: 114 was never
  approached again (next best 92, same week). The founding week holds rope, Q, tension, and
  duration extremes; 24 leaves out of 21,052 own the human ceiling of the record.
- **F2 SUPPORTED** — personal_rope step-collapses at the ghost era (100% → 8.8% → 3–12%),
  daily-median corr −0.67. The operator's rope is a founding-week signature that only echoes
  when he is directly in the loop (Aug 24–27, Sep 6).
- **F3 INFERRED** — Q is a resonance quality factor: Q ≈ 0.52 × rawsum^1.78 (R²-analog corr
  0.993 on logs, 11.5% median error). Superlinear coherence gain; 45% of post-founding leaves
  floor at Q≤1.
- **F4 SUPPORTED (naming INFERRED)** — The observer anatomy is a spectral-graph kit
  (tension / gap / lambda2 / dirichlet) computed per session; micro-leaves carry a fixed
  disconnected-graph fingerprint (gap 1.0, dirichlet 0.4375, lambda2 0.125). The founding
  era computes it over real 76-min-plus sittings; everyone after computes it over stubs.
- **F5 SUPPORTED** — The OOM war is IN the observer chart: store-max fracture (134) and
  double secrets-50 on Aug 9 (the night windows died), store-max money (167) on Aug 6. Ghost
  pain registered as fracture+money, never as rope.
- **F6 SUPPORTED** — The loop vocabulary is closed at exactly 7 tokens and complete from day
  one. Emphasis shifted: founding dominance = polish_theater (22 mentions); after founding =
  glory_before_soil (114 in ghost sample). The sin changed from polishing to glory.
- **F7 SUPPORTED** — The store has two strata: 24 UUIDv7 human-scale sessions (real durations,
  dense loops, full observer anatomy) vs a post-Aug-2 flood of named-family micro-leaves
  (duration 0, Q floor, 0–8% rope). The observer instruments only see at human scale; the
  chart's silence after July is mostly resolution, not absence of operator — consistent with
  the corpus note that silence is 90%+ door artifact.
- **F8 SUPPORTED (integrity note)** — The chain references 12 non-null-tension leaves that do
  not exist on disk (3,035 refs, 3,023 present). Small (0.4%), but it is a chain↔store gap a
  chain-seat pass should name. Also: the chain mirrors ONLY `tension_index` — Q, rope, and
  loops are chain-invisible; the signed line carries one organ of four.

## 8. Absorbed cards

`watch/inbox/FOUNDING_KNOTS_CROSSCHECK_20260911.md` (founding leaf inventory, body #1 rope
114, field-name discovery) · `watch/ARCHAEOLOGY_DIG_20260909.md` (era strata: founding week,
ghost Aug 7–15, marathon Aug 21–24, Sancho Aug 25→; verkle knot Aug 12, chain 7,377 rows) ·
`watch/THE_DAWN_CENSUS_20260907.md` + `watch/BEACON_LIGHT_20260907.md` (8 founding bodies;
the 21,052-knot count) · `watch/THE_COLDEST_SHARED_VERTEX_20260906.md` (family-stratum gate;
this atlas's 0%-UUIDv7 ghost reading corroborates the family dominance from the leaf side) ·
`watch/GHOST_ERA_EXCAVATION_20260905.md` (ghost-era stratum Aug 3–12, memlang/RIB lineage —
the named `mag-agen` leaves are that era's hands).

*Read-only dig; this file is the sole write. Reproduce: sample = all `2026-07-*` +
chain-nonnull-tension filenames + seeded random(20260911) from the remainder; schema uniform
`verkle_knot_leaf.v1`.*
