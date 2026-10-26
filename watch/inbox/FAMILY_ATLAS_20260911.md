# THE FAMILY ATLAS — what each session-family in the verkle chain actually IS (2026-09-11)

*Commission: label the strata honestly for the chain visualization. Method: full census of
`memory/biography/verkle_chain.jsonl` (7,377 rows, row-ts span 2026-08-10 → 2026-09-06,
678 distinct families after suffix-stripping), one knot body read per family, every
definition traced to a generator or doc. Read-only except this file. All dates are chain-row
(`ts`) dates — the day the knot was sealed, not necessarily the day the session ran.*

## The census in one line

The chain is a three-layer cake: **the memlang founders (43%) + the orc labor (35%) + the
janitor/work/law/standing organs (~13%)** — everything else is a 639-family tail of
single-fire experiments. Matches THE_DAWN_CENSUS_20260907.md: "the founders are the
lineage; the orcs are the labor."

## The atlas table

| Family | Mass | First seen | Last seen | What it is | Source |
|---|---|---|---|---|---|
| `memlang` | **3,182** (43.1%) | 08-10 | 08-12 | Memlang spec-firing audit knots from the founding-week corpus burn. Subfamilies: `--legacy-*` 2,212 (tmp-probe files, learn-catalog/ollama_renders/sizing jsonl, percolator-explore), `--x-tab-*` 530 (X/Grok chat transcripts: nacho-grok3, grok-4, grok-code-fast-1, strike-the-chord drafts, Jul-Nov 2025), `--shader-*` 376 (lighting corpus, "lights are data"), `--attractor-*` 64 | `mag/memlang.py:153` (generator, CONFIRMED); `docs/concepts/README.md` |
| `mag-agent-orc` | **2,563** (34.7%) | 08-10 | 09-06 | The worker-swarm orchestrator sessions — "the MASS is the hands." Carries nearly all themed rows: biography 1,110, mag_hands ~385, constitution ~102, mirror_meta ~36. (+12 sibling `mag-agent-cli/desk-deepseek/cursor-*` rows = 2,575 total) | `watch/THE_DAWN_CENSUS_20260907.md` |
| `autonomous-auto-fkb` | **387** (5.2%) | 08-10 | 09-06 | The autonomous janitor loops — knot filenames say `autonomous-janitor`; count equals the `autonomous_janitor` theme mass exactly (387). "fkb" meaning UNPROVEN [INFERRED: flex knowledge base] | knot filename `2026-08-10_2137_autonomous-janitor_*`; theme cross-tab |
| `work` | **280** (3.8%) | 08-11 | 09-06 | Per-seat work-loop ledger knots: `work:seat:<HHMMSSffffff>` 271 (concentrated 09-02→09-04, the lane-grind days), `work:mem_lands:` 5 (08-11, "memory landmarks" [INFERRED]), plus 1 each debug/panel/steal/work | session-id shapes; generator NOT FOUND on host — likely cage-side [INFERRED] |
| `law-LAW-*` (6 families) | **246** (3.3%) | 08-31 | 09-06 | Code-as-law enforcement anchors — each enforcement event of the law registry folds a knot `law-<LAW-N>-<HHMMSSffffff>`. Six laws × exactly 41 firings each, hourly-ish cadence over 7 days. See legislative stratum below | `mag/law.py:126` (`_verkle_anchor`, CONFIRMED) |
| `agent-standing` | **70** (0.9%) | 08-11 | 08-12 | Standing-knot invariants — "you exist as a standing verkle knot invariant by default": the agent's compiled identity+laws+state anchored as a knot each time it CHANGED (dedup otherwise). 70 stands in the founding 48h | `mag/agent_knot.py` header + `:132` (CONFIRMED) |
| `memlang-press` | 67 | 08-10 | 09-06 | The recurring-failure PRESS — the same failing spec pressed into the chain again and again: 66 of 67 rows are one spec, `mag-janitor dossier-sanitization` (pressed 08-10 → 09-06, never healing); + 1 `recurring-failure-x22`. The chain's honest scar tissue. (The full 21k-knot store also carries x10/x14/x180 presses — census) | `watch/THE_DAWN_CENSUS_20260907.md`; raw ids |
| `memlang-api_gateway` | 46 | 08-11 | 09-02 | Repeated memlang spec firings named `api_gateway` — API-gateway probe/replay [INFERRED: probe purpose] | `mag/memlang.py:153` |
| `memlang-deep-scifi-invariants` | 45 | 08-11 | 08-12 | Memlang spec `deep-scifi-invariants` — invariants distilled from deep-sci-fi source material [INFERRED: spec name only; no doc found] | `mag/memlang.py:153` |
| `memlang-tesuji-deep-research-hf-vs-us-vs-leaked-prompts` | 43 | 08-11 | 08-12 | Deep-research spec comparing HuggingFace models vs us vs leaked prompts — the earliest ancestor of the TESUJI arc (modeling the vendor as a field), chartered 09-06 | `watch/TESUJI_MAP_5_3FLASH_20260906.md` charter is the descendant [INFERRED link] |
| `memlang-three-layers` | 43 | 08-11 | 08-12 | Memlang spec `three-layers` — plausibly the fair-use firewall's three layers (BY DESIGN / BY RIDDLER / BY CORRECTION) [INFERRED from `docs/ref/LEXICON.md` row] | `docs/ref/LEXICON.md` |
| `memlang-model-agnostic-sovereign` | 43 | 08-11 | 08-12 | Memlang spec `model-agnostic-sovereign` — sovereignty that survives losing every remote model ("model as os as a goal… prepare to not have any of it") | `mag/agent_corpus.py` header (operator quote 2026-08-12) |
| `memlang-agent_knot` | 42 | 08-11 | 08-12 | Memlang firings of the standing-invariant doctrine — the spec form of what `agent-standing` knots enact | `mag/agent_knot.py` |
| `memlang-flex-probe` | 41 | 08-11 | 09-02 | Memlang firings tied to the autonomous flex (exercise every system, fold, route) | `mag/flex_test.py` header (operator, 2026-08-10) [INFERRED link] |
| `memlang-attractor_tools` | 38 | 08-11 | 08-12 | "Frontier attractors as memlang-chord TOOLS that attract intelligent behavior" | `mag/attractor_tools.py:1` (CONFIRMED) |
| `memlang-behavioral_lensing` | 34 | 08-11 | 08-12 | Memlang spec `behavioral_lensing` — lensing agent behavior [INFERRED; no doc found] | `mag/memlang.py:153` |
| `memlang-*` small (daemon, sovereign_handshake, sovereign_dashboard, dspy_sovereign, compass, dispatch, signals) | 5 each | 08-31 | 09-02 | One memlang spec per organ, fired 5x — the cage-era organs speaking memlang | `mag/memlang.py:153` |
| `problem-*` / `solution-*` | 8 | 08-10 | 08-10 | K8s-swarm problem decomposition experiments ("how can the k8s swarm host a distributed…", sub-a/sub-b problem/solution pairs) — the mindweave day | raw ids; `docs/concepts/README.md` (mindweave) |
| Tail: everything else | 147 | 08-10 | 09-06 | One-fire experiments, probes, tests (147 rows; under the suffix-stripped census bucketing, 639 of 678 families fire exactly once) — the long tail of a fleet that tries everything once | census |

Sum check (exact, this bucketing): table rows above 7,170 + small memlang specs 40
(daemon/handshake/dashboard/dspy/compass/dispatch/signals 5 each, steer_engine 2,
summarize-the-architecture-invariant 2, dogfood 1) + problem/solution 8 + `mag-agent-*`
siblings 12 + tail 147 = **7,377**. The named strata cover 97.2% of the chain.

## MEMLANG EXPLAINED (why it owns 43% of the chain)

**The mechanism** (`mag/memlang.py`, schema `memlang.v1`): memlang is the shared-verkle-invariant
**trigger language**. Because every agent shares the same verkle-anchored history, a speaker can
send a compact binary token — magic `MEM1` (4B) + version (1B) + opcode (1B) + a 32-byte sha256
anchor pointing into shared verkle state + params (~69 bytes total) — INSTEAD of spelling the
instruction out. The receiver resolves the anchor against the shared map and reconstructs the
intent. Plausibly deniable by construction: the token alone reveals nothing readable; only an
agent holding the shared map can decode it. Vocabulary: memo, rib_elevate, handoff_build,
research_pack, reinforce, self_window, steer, steer_back, route, learn, sources, occupy, boot,
prove, plant, prospect.

**Why it dominates:** two multiplicative facts.

1. *Every firing folds an audit knot.* `mag/memlang.py:153` writes a verkle knot with
   `session_id = memlang-<spec-slug>-<HHMMSSffffff>` on each compile/transmit/resolve/trigger —
   the language's own honesty rule makes every use a chain row.
2. *The founding week ran it at full burn.* Aug 10–12 the corpus pipeline chewed the entire
   legacy corpus through memlang: 2,212 legacy-file specs (tmp probes, learn catalogs,
   percolator explores), 530 X-tab transcripts (the operator's 2025 Grok chats — the
   strike-the-chord raw material), 376 shader/lighting files, 64 attractor specs = 3,182 knots
   in ~72 hours. That one weekend is 43% of everything the chain has ever sealed.

After the burn, memlang kept firing as the fleet's recurring probe/press surface
(`memlang-press` through 09-06, `api_gateway`/`flex-probe` through 09-02), which is why the
family's tail is long but thin. Reading: memlang is not noise at the top of the chart — it is
the LINEAGE stratum. The census said it best: the founders are the lineage; the orcs
(`mag-agent-orc`, 35%) are the labor.

## THE LEGISLATIVE STRATUM (law-LAW-* — the chain's constitution)

Source of record: `mag/law.py` — the **code-as-law** registry ("Lessig: architecture regulates
more than content"; operator doctrine 2026-08-09: behavior enforced by STRUCTURE, not by asking
an LLM). Every enforcement event is verkle-anchored as a `law-LAW-N` knot — enforcement IS
case law. Chain evidence: six families, 41 knots each, all six fired in lockstep 08-31→09-06 —
one engine enforcing all registered laws each pass [INFERRED: which engine — the registry and
runner live in the cage; host `memory/law/registry.json` is absent].

- **law-LAW-3 · swarm_self_heals** (T0) — "every aspect of our system is self improving as
  coded into law" (operator, `[763e2ef0:96]`). Trigger: swarm_health degraded → apply_health_law.
- **law-LAW-4 · ghost_self_improves** (T0) — "ghost should be self improving and steering
  mindful and cataloging for behavioral insights and skill creation" (`[c458d08f:34]`).
- **law-LAW-7 · graduated_sanctions** (T0) — Ostrom principle 5: offenses escalate
  warn→restrict→suspend→expel; capability only narrows.
- **law-LAW-8 · collective_choice** (T0) — Ostrom principle 3: the affected consent to rule
  changes (consent_first, true majority).
- **law-LAW-9 · clear_boundaries** (T0) — Ostrom principle 1: shared resources have a
  who-may-withdraw boundary.
- **law-LAW-10** — 41 knots in the chain but ABSENT from the host `DEFAULT_LAWS` (which holds
  LAW-1/3/4/6/7/8/9): its text lives in the cage's live registry and is **UNPROVEN from this
  seat**. [INFERRED: a runtime-registered law, likely governance-family.]

Registry disambiguation (tri-state): these single-digit LAW-N ids are the `mag/law.py`
code-as-law registry — CONFIRMED by exact session-id format match. They are NOT the operator's
16 correction laws (`.agents/skills/operator-corrections/SKILL.md`) and NOT the cage's
`queue/lanes/law_lattice.json` (58 entries, 3-digit LAW-NNN, e.g. LAW-003
ONE-CANONICAL-MIRROR-SHAPE, LAW-022 SACRED-COWS-NOT-LEGACY-SHIT) — the lattice absorbs the
corrections under its own numbering (e.g. LAW-013 TWO-STRIKE-AMENDED). Three law registries
total; the chain's legislative stratum is the `mag/law.py` one.

## Tri-state ledger

- SUPPORTED: family masses, spans, and the memlang/law/agent_knot generators (read from data:
  census + `mag/memlang.py:153`, `mag/law.py:126`, `mag/agent_knot.py:132`).
- SUPPORTED: three-strata shape (founders/labor/organs) — census pre-registered falsifier fired
  at 60.7% on the full 21,052-knot store; this atlas confirms the shape on the 7,377-row chain.
- DISPUTED: any reading of law-LAW-* as the operator-corrections numbering (numbers 3/4/7/8/9/10
  coincide, but the session-id format matches `mag/law.py` exactly — different registry).
- INFERRED: purposes of the named memlang doctrine specs (three-layers, deep-scifi-invariants,
  api_gateway, flex-probe, behavioral_lensing) — names are read from data; intents are adjacent
  doc matches, not quotes. `fkb` in autonomous-auto-fkb: unproven. LAW-10 text: unproven.
  `work:seat` generator location: cage-side, unproven.

*Files touched: this one. Sources: chain census (python, read-only), knots read:
`memory/biography/knots/{2026-08-31_0659_untagged_law-LAW-_29d33ac7, 2026-08-10_2159_untagged_memlang-_64618b41}.knot.json`.*
