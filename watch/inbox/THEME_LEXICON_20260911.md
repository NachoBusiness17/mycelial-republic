# THE THEME LEXICON — every dominant_theme the knot FILES ever spoke (2026-09-11)

*Commission: fleet research worker, 2026-09-11 wave. The verkle chain knows 9 recurring
`dominant_theme` values + NULL. The 28.9k files in `memory/biography/knots/` know more.
Method: FULL census (no sample needed — it finished) of all 21,052 knot leaves, 0 parse
failures, every `dominant_theme`, `theme_vector_raw` length, and `theme_basis` captured;
chain vocabulary verified against `memory/biography/verkle_chain.jsonl` (7,377 rows).
Read-only except this file. Dates are filename leaf dates (the day the leaf was written);
chain column dates are chain-row `ts`.*

**Headline: the files speak 62 distinct non-null themes + NULL (63 values) — the chain's
recurring vocabulary is 9 + NULL. 31 themes exist ONLY in the leaves; 1 theme exists ONLY
in the chain. The theme-vector length is not global: it equals the length of that leaf's
`theme_basis`, and there were TEN different bases.**

## 0. What the directory actually holds (28.9k entries)

| Kind | n | Note |
|---|---|---|
| `*.knot.json` leaves | **21,052** | the census population; matches THE_DAWN_CENSUS_20260907's 21,052 exactly |
| `by-session_*.json` | 7,789 | NOT leaves — a filename+leaf_hash index only, no theme fields; excluded |
| dict-repr filename corrupt | 26 | zero-byte, filename embeds `{'ok' …` payload repr — 11 on **Aug 11**, 15 on Aug 23-25 |
| truncated, no extension | 11 | `2026-08-11_*_untagged_work/probe…` — all Aug 11 |
| `.mimosa` | 1 | marker |

The commission's "28,838 knot files" ≈ leaves + by-session index (21,052 + 7,789 = 28,841).
**New finding: the `mem-invariant-map` serializer broke TWICE — Aug 11 (11 corrupt + 11
truncated) and again Aug 23-25 (15 corrupt, per SILENCE_DOSSIER §2). The dossier's window
batch was the second failure, not the first.**

## 1. The lexicon (63 values, in first-appearance order)

NULL = 12,147 leaves (57.7% of the store), span 2026-08-03 → 2026-09-06. The single largest
"theme" — the husks (marathon mass, per SILENCE_DOSSIER §2) plus every leaf where the miner
committed without interpreting.

| # | Theme | n | First | Last | In chain (ts) | What/where |
|---|---|---|---|---|---|---|
| 1 | `mirror_meta` | 360 | 07-10 | 09-06 | yes, mass 44 | July founder; the mirror watching itself |
| 2 | `mag_hands` | 2,159 | 07-10 | 09-06 | yes, mass 422 | the swarm's labor theme, day one |
| 3 | `biography` | 4,303 | 07-21 | 09-06 | yes, mass 1,110 | the miner's work on itself; largest non-null |
| 4 | `data_r0` | 64 | 08-02 | 08-31 | yes, mass 11 | round-zero data era; dies with the founding week |
| 5 | `constitution` | 436 | 08-03 | 09-06 | yes, mass 104 | law/identity weighting |
| 6 | `harness` | 52 | 08-06 | 08-10 | yes, mass 7 | short-lived harness era, pre-chain-lit |
| 7 | `dashboard` | 26 | 08-06 | 08-09 | yes, x3 (backfilled, ts 08-31) | pre-chain observability burst |
| 8 | `autonomous_janitor` | 1,158 | 08-08 | 09-06 | yes, mass 387 | the heartbeat; matches autonomous-auto-fkb exactly |
| 9 | `holographic_q` | 7 | 08-08 | 08-14 | **never** | basis `q,steer,verkle,holographic`; `2026-08-08_1838_holographic-q_q-knot-q_2f0b4b9e` |
| 10 | `context_freeze` | 1 | 08-08 | 08-08 | **never** | `2026-08-08_1850_context-freeze_freeze-a_32713252` |
| 11 | `?` (literal) | 1 | 08-08 | 08-08 | **never** | `2026-08-08_1855_untagged_quantum-_1274c06c`, basis `quantum,state,compressed,summary` — a compression summary that could not name itself |
| 12 | `runaway_python` | 1 | 08-10 | 08-10 | **never** | `2026-08-10_0938_runaway-python_runaway-_src_trac` — the record engine watching a runaway process |
| 13 | `scrum_plan` | 39 | 08-10 | 09-04 | yes, mass 16 | planning stratum |
| 14 | `window-bus-knot` | 1 | 08-10 | 08-10 | **never** | `2026-08-10_1827_window-bus-knot_winbus-d_7724d580` |
| 15 | `agent_os_cycle` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | basis `loop,fold,sovereign,compound` |
| 16 | `fact_infra` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | fact-bus channel; basis `fact,who,when,where,why` |
| 17 | `fact_providers` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 18 | `fact_ops` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 19 | `fact_x-tabs` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 20 | `fact_general` | 4 | 08-11 | 08-12 | yes, x1 (08-12) | " |
| 21 | `fact_behavioral` | 10 | 08-11 | 08-16 | yes, x1 (08-16) | the chain's last pre-silence word (SILENCE_DOSSIER §4.1) |
| 22 | `rib_testdomain` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | rib-bus channel; basis `rib,instruction,frontier,sovereign` |
| 23 | `rib_ghost-debug` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 24 | `rib_machinedemo` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 25 | `rib_howto-steal-linux-dev` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 26 | `rib_babelfish-turtles` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 27 | `rib_compiler-flywheel` | 1 | 08-11 | 08-11 | yes, x1 (08-11) | " |
| 28 | `rib_copilot-session-base` | 1 | 08-11 | 08-11 | **never** | one of the Aug-11 rib probes the chain never folded |
| 29 | `rib_gpu-rightsizer-surface` | 1 | 08-11 | 08-11 | **never** | " |
| 30 | `rib_mem-invariant-map` | 1 | 08-11 | 08-11 | **never** | NOTE: the chain folds the SAME event as `mem_invariant_map` (see §3) |
| 31 | `rib_rib-os-self-advancing` | 1 | 08-11 | 08-11 | **never** | " |
| 32 | `rib_k8s-resource-governor` | 1 | 08-11 | 08-11 | **never** | " |
| 33 | `rib_eut-coherence-lens` | 1 | 08-11 | 08-11 | **never** | " |
| 34 | `rib_hil-setpoint-flock-control` | 1 | 08-11 | 08-11 | **never** | " |
| 35 | `rib_bare-metal-zeitgeist` | 1 | 08-11 | 08-11 | **never** | " |
| 36 | `rib_structured-extraction` | 1 | 08-11 | 08-11 | **never** | " |
| 37 | `rib_frontier-internals-capture` | 1 | 08-11 | 08-11 | **never** | " |
| 38 | `rib_castle-in-the-sky` | 1 | 08-11 | 08-11 | **never** | " |
| 39 | `rib_standing-novelty-wave-trickster` | 1 | 08-11 | 08-11 | **never** | " |
| 40 | `rib_archetypes-esoteric` | 1 | 08-11 | 08-11 | **never** | " |
| 41 | `rib_titor-worldline` | 1 | 08-11 | 08-11 | **never** | " |
| 42 | `rib_kobayashi-maru-tesla-q` | 1 | 08-11 | 08-11 | **never** | " |
| 43 | `rib_titor-rib-attractor` | 1 | 08-11 | 08-11 | **never** | " |
| 44 | `rib_reframe-not-brute-force` | 1 | 08-11 | 08-11 | **never** | " |
| 45 | `rib_grok-bot` | 1 | 08-12 | 08-12 | **never** | hyphenated twin of `rib_grokbot` — the string was never canonicalized |
| 46 | `rib_grokbot` | 33 | 08-12 | 09-02 | yes, x1 (09-02) | the surviving spelling |
| 47 | `rib_territory` | 2 | 08-12 | 08-12 | **never** | |
| 48 | `rib_k3s-toolset` | 135 | 08-12 | 09-02 | yes, x1 (09-02) | the marathon's one coherent channel (SILENCE_DOSSIER §2) |
| 49 | `wow_manifest` | 6 | 08-12 | 08-12 | yes, mass 5 | basis `wow,verkle,rib` |
| 50 | `rib_wow` | 1 | 08-12 | 08-12 | yes, x1 (08-12) | |
| 51 | `rib_arrival` | 15 | 08-12 | 09-06 | yes, x1 (09-06) | the restart signal's theme (SILENCE_DOSSIER §4.5) |
| 52 | `rib_reconstruct` | 1 | 08-12 | 08-12 | **never** | |
| 53 | `rib_saelis` | 1 | 08-13 | 08-13 | **never** | `2026-08-13_2308_rib-saelis_rib_bus__d5c69a6d` |
| 54 | `rib_party_subchain` | 1 | 08-14 | 08-14 | **never** | |
| 55 | `rib_doctrine` | 5 | 08-14 | 09-06 | yes, x1 (09-06) | |
| 56 | `fact_game` | 1 | 08-14 | 08-14 | **never** | |
| 57 | `rib_swarm` | 1 | 08-15 | 08-15 | **never** | |
| 58 | `rib_standing-wave` | 7 | 08-16 | 09-02 | yes, x1 (09-02) | |
| 59 | `fact_probe` | 1 | 08-16 | 08-16 | **never** | |
| 60 | `rib_shader` | 42 | 08-23 | 08-27 | **never** | SILENCE-ONLY — see §4 |
| 61 | `backfill-explore-the-python-codebase-at-c-users` | 1 | 08-25 | 08-25 | yes, x1 (09-06) | SILENCE-ONLY — a backfill knot whose theme is a whole sentence |
| 62 | `backfill-integrating-model-into-glm-4-6` | 1 | 08-25 | 08-25 | yes, x1 (09-06) | SILENCE-ONLY; Sancho day one's second knot (SILENCE_DOSSIER §1, Aug 25) |

Plus 3 leaves with NO theme machinery at all: two `.diary.knot.json` leaves (08-07,
`talk-about-bernays…`, `freeze-fidelity`) and the `usage_digest_knot_leaf` (08-26, the
cache-economy receipt, SILENCE_DOSSIER §1). They carry neither `dominant_theme` nor vectors.

### July, answered precisely
ALL July leaves = **24 files** (07-10 → 07-31), 3 themes: `mirror_meta` + `mag_hands`
(both from 07-10, the store's first day), `biography` (from 07-21). The chain (starting
08-10) never saw July's raw leaves — July is files-only territory for its founding triple.

## 2. Theme-vector lengths — there is no global length

`theme_vector_raw` length == `len(theme_basis)` of the same leaf. Two lengths, TEN bases:

| len | n | first | last | Basis (ordered vocabulary) | notes |
|---|---|---|---|---|---|
| 8 | 19,586 | 07-10 | 09-06 | `mirror_meta,mag_hands,scrum_plan,constitution,dashboard,harness,biography,data_r0` | the canonical 8 — note it contains `dashboard` and NOT `autonomous_janitor`/`wow_manifest` |
| 4 | 1,158 | 08-08 | 09-06 | `mag_hands,harness,biography,constitution` | the janitor's own reduced basis, every tick since 08-08 |
| 4 | 268 | 08-11 | 09-06 | `rib,instruction,frontier,sovereign` | the rib bus |
| 4 | 20 | 08-11 | 08-16 | `fact,who,when,where,why` | the fact bus (dies with the founding week) |
| 4 | 7 | 08-08 | 08-14 | `q,steer,verkle,holographic` | holographic_q |
| 4 | 6 | 08-12 | 08-12 | `wow,verkle,rib` | wow_manifest day |
| 4 | 1+1+1+1+1 | 08-08..08-11 | — | `freeze,grok,context,verkle` / `quantum,state,compressed,summary` / `biography,holographic_q,autonomous_janitor,mirror_meta` / `loop,fold,sovereign,compound` (+ the canonical-8 leaf at `?`) | five one-shot bases, each a single leaf |

Sum check: 19,586 + 1,463 = 21,049 vector-bearing leaves + 3 bare leaves = 21,052.

**Consequence:** comparing theme vectors across eras compares different axes. The
canonical 8 and the janitor's 4 share only slot names by position — any downstream
consumer (the miner, a future visualization) must key on `theme_basis`, not index. The
"theme_vector length" question resolves to: **8 (canonical) and 4 (nine channel-specific
bases), nothing else, ever.**

## 3. Chain vs files — the vocabulary delta

- **Chain full vocabulary: 32 non-null + NULL = 33 values.** The commission's "9 + NULL"
  is the RECURRING vocabulary. The other 23 chain values are one-offs: 17 folded live
  during the founding week (ts 08-11/08-12: fact_*, agent_os_cycle, rib_testdomain,
  rib_ghost-debug, rib_machinedemo, rib_howto-steal-linux-dev, rib_babelfish-turtles,
  rib_compiler-flywheel, mem_invariant_map, rib_wow; ts 08-16: fact_behavioral — the
  chain's last pre-silence word), 3 backfilled with the Aug-31 re-arm (dashboard x3,
  ts 08-31), 3 folded post-restart (ts 09-02: rib_k3s-toolset, rib_grokbot,
  rib_standing-wave; ts 09-06: rib_arrival, rib_doctrine, backfill x2).
- **Files-only: 31 themes the chain NEVER saw** — #9-11, 12, 14, 28-45, 47, 52-54, 56-57,
  59-60 in the table. Mostly the Aug-11 rib-probe burst (17 of the 31) that fired the day
  the rib bus was born; plus holographic_q; plus the silence-window trio (§4); plus the
  oddballs (`runaway_python`, `window-bus-knot`, `context_freeze`, `?`).
- **Chain-only: 1 — `mem_invariant_map`** (ts 08-11). In the leaves the same writer signs
  `rib_mem-invariant-map`. Same event family, two different theme strings.
- **Never canonicalized:** `rib_grokbot` (33 leaves + 1 chain row) vs `rib_grok-bot`
  (1 leaf, never chained). Theme strings are free text, not an enum. Any theme-driven
  chain visualization dedupes on normalized slugs or it will double-count.

## 4. Themes that appear ONLY in the silence window (2026-08-17 → 08-30)

Exactly three — the silence minted almost no new vocabulary; its real output was NULL:

1. **`rib_shader`** — 42 leaves, 08-23 → 08-27, all inside the window. The rib bus's
   shader channel; the marathon's second voice (SILENCE_DOSSIER §2 counted 42 across the
   window — exact match).
2. **`backfill-explore-the-python-codebase-at-c-users`** — 1 leaf, 08-25 17:14. Theme
   string = an entire instruction sentence; the miner echoing the task as theme.
3. **`backfill-integrating-model-into-glm-4-6`** — 1 leaf, 08-25 22:00, the Sancho-day-one
   backfill knot (SILENCE_DOSSIER §1). Both backfill themes ARE in the chain (folded ts
   09-06) — the chain caught the silence's vocabulary only 12 days after the restart.

Everything else the window spoke was existing vocabulary (`autonomous_janitor`,
`biography`, `mag_hands`, `rib_k3s-toolset`…) or the husk-NULL.

## 5. Tri-state ledger

- SUPPORTED: all 63 values, counts, first/last dates, both vector lengths, ten bases,
  chain cross-tab (full census, 0 parse failures; reproducible by streaming
  `memory/biography/knots/*.knot.json` and `verkle_chain.jsonl`).
- SUPPORTED: 21,052-leaf store size (independent confirmation of THE_DAWN_CENSUS figure).
- DISPUTED (refined): "the chain knows 9 + NULL" — true only of the recurring engine
  vocabulary; the chain's full distinct set is 32 + NULL. The Aug-10-16 chain already
  spoke rib/fact one-offs live; they are not all backfill artifacts.
- DISPUTED (extends SILENCE_DOSSIER §2): the serializer corruption began Aug 11, not
  Aug 23 — 26 dict-repr + 11 truncated files total.
- INFERRED: semantic glosses in the table's "What/where" column (names are data; intents
  are adjacent readings). The `?`-theme leaf as "a summary that could not name itself" is
  interpretation of basis `quantum,state,compressed,summary`.
- UNPROVEN: why the miner accepted a bare `?` as a dominant_theme and why theme strings
  were never slug-normalized (no generator for the miner is host-reachable).

## Absorbed cards

- `watch/inbox/FAMILY_ATLAS_20260911.md` — family masses, chain row spans, memlang/law
  generators; the 21,052 store figure cross-checked.
- `watch/inbox/SILENCE_DOSSIER_20260911.md` — window day-by-day, husk anatomy, the five
  key knots; rib_shader x42 and backfill themes verified exactly.
- `watch/THE_DAWN_CENSUS_20260907.md` (via both cards) — store-size and strata context.

*Files touched: this one. Census: python, read-only, full-population (no sampling).*
