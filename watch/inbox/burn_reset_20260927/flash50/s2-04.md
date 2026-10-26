# s2-04: docs/ref deep census (2026-09-28)

ITEM: read every file in docs/ref/. For each: is it current, is it referenced, is it
load-bearing, does it contradict any other doc. Seat: s2-04 census gopher. Companion
mechanical sweep: docs-ref-audit.md (f-07 lane, same day) covered staleness math and
reference counting at a different cut; this census adds the content read and the
contradiction list. Where both instruments measured the same thing they agree.

## Scale and method (every number below from a command run this session)

- Tree: `find docs/ref -type f | wc -l` = **365 files**, `4,878,635` bytes total. 359
  tracked (`git ls-files docs/ref | wc -l`), 6 untracked (`.mimosa/` tool state, all
  dated 2026-08-27, contents are session baseline/hook JSON, zero prose).
- Read coverage: all 5 docs/ref files named in the AGENTS.md load order read in full
  (compass, science map, direction artifact v2, proposal, operator card); every other
  top-level file header-read (first 10-14 lines, all 185); 21 recent/live files read in
  full or near-full (canon gate set, VERSION_REGISTRY, ractors/RACTORS.md, ZAI ref date
  lines, KABUKI freeze header, RTFM head, canon txt headers); every subdir index/README
  read; all 12 onepagers, 4 proposals, 7 tesuji leaves, 11 ractor briefs, 9 releases,
  3 mesh spores, 7 verb_genomes, 2 weaves, prompts, templates, steals header-read.
  NOT read: `canon/philbrick_opamp_applications_1964.png` (binary, 615,974 B), 84 of
  the 86 zai_docs_mirror page bodies (2 sampled + INDEX.md; 105 mirror files total =
  86 pages + INDEX.md + openapi.json + 17 `_raw/` crawl artifacts) beyond those samples
  artifacts (17 files), and the 6 .mimosa JSONs beyond one sample. The 8 large canon
  research packs (251 KB, 224 KB, 99 KB, 55 KB, 48 KB, 29 KB, 16 KB) were read at
  header level + via canon/README.md status table, not line-by-line.
- Currency: git last-touch per file via one `git log --date=short --name-only -- docs/ref`
  pass (first date seen per path). Content dates read from file headers. Working-tree
  mtimes were NOT used (they cluster on 2026-08-06 from a bulk operation and lie).
- References: Python single-pass scan (tmp script, deleted after run) over a stated
  surface: tracked files under AGENTS.md CONSTITUTION.md README.md LOAD.md docs (ex
  docs/ref) mag dashboard (ex dashboard/data) tests tools scripts configs queue handoff
  .agents githooks main.py mag.cmd mag.ps1 = 3,689 files, plus a boot set (memory/rib/*,
  memory/attention.md, memory/README.md, state/CURRENT.md). All 343 unique basenames
  searched as fixed strings (longest-first alternation). Then a second pass over the
  rest of the tracked tree (watch/, memory/, corpus/, state/, catalog/ ...).
- Live-truth anchors read: state/CURRENT.md (updated 2026-09-27),
  memory/rib/RIB_DRIVING_LADDER_20260928.md, configs/releases.yaml v3/v4 rows,
  configs/version_roadmap.yaml, AGENTS.md (workspace, in context).

## Headline

1. **365 files, four strata.** The tree is (a) an Aug 2026 planning estate (185
   top-level docs + onepagers + proposals, v2-v5 arc law), (b) a late-Aug research and
   doctrine wave (snapshots, receipts, councils), (c) a vendor mirror (z.ai docs,
   captured 09-03/04) and a canon shelf with a real admission gate, (d) tool state.
2. **Currency: 10 files are fresh (last commit 2026-09-27, inside the 7-day law); 349
   are older than 7 days (97.2 percent); 6 untracked.** But "stale" splits three ways:
   24 files are LIVING (amended in place into September, current by content), ~200 are
   frozen-by-design receipts and plan-era law whose age is honest, and the rest are
   snapshots that look current and are not (see C4).
3. **References: every one of the 343 unique basenames is referenced somewhere in the
   tracked tree (zero true orphans); 119 have governance/code-surface references; 160
   of 343 are referenced outside docs/ref on the code+governance surface; 67 code, test,
   or script files carry literal `docs/ref/` paths; 6 skills lazy-load 8 distinct ref
   paths; the boot set names 6.** The 183 names with no governance-surface reference
   live on receipts (watch/), memory soil, and in-ref indexes - the estate remembers
   everything; the boot path uses a fraction.
4. **Load-bearing chains are real and code-wired:** AGENTS.md load order (5 ref docs),
   `mag/context_pack.py` (pulls OPERATOR_CARD.md + COORDINATION_ELIAS_ROPE.md into the
   daily pack), `mag/canon_gate.py` (enforces canon-gate frontmatter over
   docs/ref/canon/*.md), 6 skills (zai-reference, light-operator, verb-genomes,
   agent-harness, frontier-researcher, operator-corrections), releases/VERSION_REGISTRY
   as the version index AGENTS.md names.
5. **Contradictions: 8 found, 1 material.** The compass version table (v3 in_progress,
   v4 planned) contradicts the machine truth, the registry, and both release notes
   (v3 shipped, v4 shipped); the compass is the doc agents are ordered to load first,
   and its own amend protocol requires the bump it never got. One dead pointer sits in
   a load-order card (mycelia.cmd). The canon index gate block contradicts its own
   status table. Details in the contradiction section.

## Currency waves (git last-touch, 359 tracked files)

| wave | files | what it is |
|---|---|---|
| 2026-08-04 | 13 | original operator cards (OPERATOR_CARD, strike_origin, lessig, SOVEREIGN_STACK...) |
| 2026-08-05 | 68 | the planning estate lands (v2-v5 plans, proposals, onepagers, indexes) |
| 2026-08-06 | 25 | vision + factory era (compass, science map, direction artifact, release notes v3/v4) |
| 2026-08-07 | 23 | game/voice/skill wave |
| 2026-08-08 to 08-14 | 5 | ROUTE_COVERAGE, FORTRESS_AND_REPUBLIC, RUN.md, UX_UI_FOUNDATIONS, tabletop-dnd |
| 2026-09-08 | 1 | ONTOLOGY_COMPILER_PHASE1 |
| 2026-09-14 | 212 | the big backfill: late-Aug research/doctrine files re-committed in bulk (content dates 08-26 to 09-12) |
| 2026-09-15 | 2 | WOW steal maps |
| 2026-09-27 | 10 | the live set: compass, ZAI ref, KABUKI, VERSION_REGISTRY, canon README + 2 stubs + 2 CANDIDATE files |

Fresh window (<= 7 days, cutoff 2026-09-21): exactly the 10 files of the 09-27 wave.
This agrees with docs-ref-audit.md f-07 (10 fresh / 349 stale / 6 untracked).

## The LIVING set (current by content, not just by commit date)

| file | why current |
|---|---|
| MAG_MYCELIAL_REPUBLIC_COMPASS.md | freeze stamp 2026-09-26 on the built-state section; BUT see C1: the version table two sections up is stale |
| ZAI_API_EXPERT_REFERENCE.md | sections through 2026-09-26 (B2-62 backoff law); header title still says 2026-08-26 - date drift inside a living doc |
| KABUKI_STACK_20260905.md | live content is a 2026-09-26 STRUCK-UNTIL freeze notice (Mag P0-4); the 09-05 stack text below it is frozen |
| canon/README.md + canon/CANDIDATE/* (3) + 2 demote stubs | 2026-09-26 Elder P0-2 demotion of 2 packs; gate frontmatter live |
| releases/VERSION_REGISTRY.md | as-of 2026-09-26; arbitrates version status |
| BIBLIOGRAPHY_MAP.md, LEXICON.md, CACHE_CRAFT_LAWS, DOGFOOD_PROGRAM, MIRROR_PRESENTED, SPORES.md, strike_origin.md/.json, THE_TAPED_LAYER, PLANNING_MODE, PRODUCT_VISION_AUTORUN | declared living/append-only or still-true law (law 18 map, minted vocabulary, custody law); last substantive touch Aug-Sep, none contradicted |

## Reference tiers (instrument stated above)

| tier | n of 343 names |
|---|---|
| governance/code surface (tier 1, code_or_gov > 0) | 119 |
| full first surface (incl. docs/ prose, queue, handoff, dashboard code) | 160 |
| anywhere tracked (after wide pass: watch/ receipts, memory/, corpus/, state/, catalog/) | 343 |
| boot set (memory/rib/*, memory/README.md, memory/attention.md, state/CURRENT.md) | 6 |

Boot-set names: MAG_MYCELIAL_REPUBLIC_COMPASS.md (RIB_MOSAIC_SEED_20260921),
DASHBOARD_DESIGN.md (RIB_CASTLES_FOUNDATIONS_20260810), PLANNING_MODE.md (RIB cold-seam),
DATA_LAYERS.md and SPORES.md (memory/README.md), README.md (collisions: generic README
mentions). Caveat: common basenames (README.md, INDEX.md, introduction.md, quick-start.md,
overview.md, thinking.md, python.md, agent.md, home.html) collide with same-named files
elsewhere; their tier-1 counts are inflated and the mirror pages are really referenced
via the mirror INDEX, not by page name.

Code-wired (literal `docs/ref/` paths in code/tests/scripts): 67 files, including
mag/canon_gate.py, mag/context_pack.py, mag/os_v2.py, mag/bonds.py, mag/plan.py,
mag/loops_registry.py, mag/diary_node.py, mag/governor.py, mag/play_benchmark.py,
mag/ponytail_audit.py, dashboard/static/_rtfm_graph_data.py (list truncated at 25 by
the display; count from `git grep -l docs/ref/ -- mag/*.py dashboard/** tools/*.py
scripts/* tests/*.py | wc -l` = 67).

Skill lazy-load chains (.agents/skills): zai-reference -> ZAI_API_EXPERT_REFERENCE.md;
light-operator -> canon/LIGHT_OPERATOR_FOUNDATION_20260904.md + canon/MAG_CHORD_V3_CANDIDATE_20260904.md
(both now demote stubs since 09-26 - the stubs redirect to canon/CANDIDATE/, so readers
still land on the real text, but the skill routes through the stub: see C8);
verb-genomes -> verb_genomes/L0_contract.md; agent-harness + frontier-researcher ->
verb_genomes/research_socratic.md; frontier-researcher -> SPORE_SANCHO.md;
operator-corrections -> BIBLIOGRAPHY_MAP.md.

Command/card existence checks run this session (AGENTS.md law: never trust a hand-
written count, so each named command was checked against main.py dispatch): nervous,
trail, agent-state, ideas, token-chain, ponytail-audit, loop-audit, release, switchboard,
plan, lab, autorun, verkle-audit ALL resolve in main.py (dispatch lines 2710-5350 band).
The 13 mag/ modules named by ref docs (game_salon, desk_timing, tapestry, improve_loop,
gstd_probe, embassy_integrity, nervous_system, idea_graph, plan, wow_family, roshomon,
lens_chain, swarm_worker) ALL exist on disk. ONE dead pointer found: mycelia.cmd (C3).

## Contradictions and dead pointers

**C1 (material): compass version table vs machine truth.**
docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md section 3.2 (live prose) says v3 =
"in_progress", v4 = "planned". configs/releases.yaml lines 68-96 say v3 `status: shipped`
and v4 `status: shipped`; releases/VERSION_REGISTRY.md (as-of 2026-09-26) rows v3 and v4
both say shipped; releases/RELEASE_NOTES_v3.md and _v4.md say shipped. The compass got a
2026-09-26 freeze stamp on its section 4 only; its own amend protocol (section 8: "New
version gate passed -> release record + update VERSION_REGISTRY") was executed on the
registry but never on the compass table agents are told to load first. Same-week
three-way disagreement on v3 in the Aug 05/06 docs: RELEASE_NOTES_v3 says "shipped - all
defined gates green", direction artifact section 4.1 says "v3 shipped: Partial - modules
on branches; not product-complete", compass says in_progress. Registry arbitrates; the
loser is the compass row.

**C2: canon index gate block vs its own table.** canon/README.md carries a generic
canon-gate frontmatter (`status: CANDIDATE, null-space: UNNAMED, falsifier: UNNAMED,
falsifier-receipt: NONE`) while its table declares packs LAW / DOCTRINE / CONFIRMED /
METAPHOR PAYING RENT. Worst case: canon/canon_model_rib_boundary.md own gate says
CANDIDATE with falsifier UNNAMED and receipt NONE, and the README row calls it "LAW
(is the Roshamon witness rule...)". The 2026-09-26 P0-2 demotion moved exactly 2 packs
to canon/CANDIDATE/; canon_model_rib_boundary.md was left on the main shelf with a
CANDIDATE self-label and a LAW index label. One of the two labels is wrong per the
gate's own vocabulary (promotion requires named falsifier + receipt; it has NONE).

**C3: dead door in a load-order card.** OPERATOR_CARD.md (AGENTS.md load order item 6)
sends the operator to `mycelia.cmd x-pull` / `thread-pull` (FIND door, lines 54-55 and
108-109). No mycelia.cmd or mycelia.ps1 exists anywhere tracked (`git ls-files | grep
-i mycelia` outside docs/memory/corpus/watch = empty) and `x-pull` is implemented in no
.py/.cmd/.ps1 (`git grep -l x-pull` over code = empty). Every other command the card
names (mag.cmd doctor/context-pack/bonds/trail start/agent-state --load, python
main.py nervous) verified live in main.py dispatch.

**C4: lane-policy frame superseded by the 2026-09-28 funding law.**
LING_API_REFERENCE.md (09-13) titles ling-3.0-flash-sante:free "THE FREE WORKHORSE";
BURST_DOCTRINE_20260903.md assigns burst roles to free glm-4.5-flash / glm-4.7-flash
lanes; PROVIDER_LANE_MAP_20260902.md declares itself "the single lane source of truth;
update it when a wire changes". memory/rib/RIB_DRIVING_LADDER_20260928.md (operator,
code-as-law): "ONLY HERMES IS FUNDED... DeepSeek is no longer the funded workhorse...
Free stealth lanes are not funded at all" - sensing only, never done-work. The three
docs still speak the pre-ladder funding frame and none names the ladder. Corroborating
staleness: PROVIDER_LANE_MAP's XAI_API_KEY row says "SET" while `.env` today has no
XAI_API_KEY (checked by name only, values never read; matches f-18 finding K2), and the
map predates the 09-28 provider census (28 providers, 9 zero-key lanes).

**C5: proposal non-goal vs current funding reality.** MAG_PROJECT_PROPOSAL.md section
11.2 lists "Hermes as default router" as a permanent non-goal (2026-08-05, when Hermes
was the foreign venv bare-python collided with). AGENTS.md 2026-09-28 DRIVING LADDER:
"ONLY Hermes is funded ($180 Nous credits)" and it is the workhorse+judgment tier.
Strictly the non-goal said "default router", the ladder says "funded driver", so this is
era drift inside a doc still on the load order, not a flat contradiction - but a fresh
seat loading the proposal cold will route against the ladder.

**C6: v2 status, same week, three verdicts.** DIRECTION_ARTIFACT_v2 section 4.1:
"v2 shipped: No - #8-#11 not merged to home main" (2026-08-05). RELEASE_NOTES_v2.md:
"Shipped (repo home)" (2026-08-06). VERSION_REGISTRY: v2 shipped. The registry is the
index of record; the direction artifact honesty table was never amended after the
merges it was waiting on.

**C7: mirror honesty is good, mirror currency is not re-verified.**
zai_docs_mirror/INDEX.md honestly documents 86/86 capture, 1 documented gap
(rate-limit moved vendor-side, stubbed with the 307 note), and 12 unlisted-but-live
pages found by link closure. Mirror date 2026-09-04. NOT re-verified against live
docs.z.ai this session (no fetch attempted); anything vendor-side after 09-04 (25 days)
is not in the mirror. The living ZAI_API_EXPERT_REFERENCE.md is the fresher z.ai surface.

**C8: light-operator skill routes through demote stubs.** Since the 2026-09-26 P0-2
demotion, docs/ref/canon/LIGHT_OPERATOR_FOUNDATION_20260904.md and
canon/MAG_CHORD_V3_CANDIDATE_20260904.md at the canon root are stubs pointing to
canon/CANDIDATE/. .agents/skills/light-operator/SKILL.md still names the root paths.
The stubs redirect, and the skill labels them "(CANDIDATE)", so the chain works and is
honest - but the skill was not re-pointed when the shelf moved.

**Verified clean (checked, no contradiction):** the three ref docs citing
`docs/archive/ZEITGEIST.md` (MAG_STEAL_AUTOPILOT.md, MAG_v5_MESH_FOREST.md,
run_trail_lattice.md) resolve to a real file (docs/archive/ZEITGEIST.md exists, 3,505 B);
AGENTS.md's note that the `docs/ZEITGEIST.md` path "never existed" holds (`ls
docs/ZEITGEIST.md` = not found). evidence_states_audit_prep.md cites
mag/embassy_integrity.py - file exists; the lines 34-60 claim was NOT line-verified.
THE_MOVING_WALL_POST_20260911.md pointer to THE_PARABLE_OF_THE_MOVING_WALL.md resolves.
MYCELIAL_SCIENCE_MAP.md's "(if present)" hedge for MAG_TRAINING_DATA_SPEC.md - it is
present. verb_genomes/steal.md and self_steal.md share the L0 header by design (packs
over one byte-stable prefix), not duplication error.

## Per-file census (359 tracked; class, tier-1 gov refs, explicit path refs, boot)

Classes: L living, P plan-era, R receipt, S snapshot, V vendor mirror, Vr version
record, C canon, D ractor brief, G verb genome, T tool state (the 6 untracked .mimosa
files are listed after the table). refs = distinct tier-1 surface files naming the
basename; path = explicit docs/ref/<name> mentions in that surface; boot = named in
memory/rib or memory/README or state/CURRENT.md.

| file | B | last commit | class | refs | path | boot |
|---|---|---|---|---|---|---|
| AGENTIC_LANDSCAPE_2026.md | 10226 | 2026-08-06 | P | 0 | 1 |  |
| AGENT_BLEEDING_EDGE_REPOS_INDEX.md | 14086 | 2026-08-06 | S | 4 | 3 |  |
| AGENT_PLATFORM_REPOS_INDEX.md | 14628 | 2026-08-06 | S | 4 | 3 |  |
| AGENT_UI_STEAL.md | 1487 | 2026-08-04 | S | 0 | 0 |  |
| ANNALEA_STANDARD.md | 2641 | 2026-09-14 | S | 0 | 0 |  |
| BARE_METAL_PRIMITIVES.md | 2744 | 2026-09-14 | S | 0 | 0 |  |
| BIBLIOGRAPHY_MAP.md | 65768 | 2026-09-14 | L | 4 | 3 |  |
| BOOT_PLAYBOOK.md | 3566 | 2026-09-14 | S | 0 | 0 |  |
| BUDDY_LETTER.md | 2448 | 2026-09-14 | R | 0 | 0 |  |
| BUILD-TEMPLATE.md | 1811 | 2026-08-05 | P | 1 | 2 |  |
| BUILD-factory-audit-json-EXAMPLE.md | 2525 | 2026-08-05 | P | 2 | 2 |  |
| BUILD-v3-deepseek-run.md | 1617 | 2026-08-05 | P | 0 | 0 |  |
| BURST_DOCTRINE_20260903.md | 5266 | 2026-09-14 | S | 2 | 3 |  |
| CACHE_CRAFT_LAWS_20260906.md | 1423 | 2026-09-14 | L | 0 | 0 |  |
| CHAIN_V2_ANCHOR_REGISTRY_SPEC.md | 5326 | 2026-09-14 | S | 1 | 1 |  |
| CHAT_PLAY_LOOP.md | 1696 | 2026-09-14 | P | 0 | 0 |  |
| COMMON_LANGUAGE_SPEC.md | 3395 | 2026-09-14 | S | 0 | 0 |  |
| COORDINATION_ELIAS_ROPE.md | 7437 | 2026-08-04 | P | 3 | 3 |  |
| CORE_MEMORY_PROTOCOL.md | 3632 | 2026-09-14 | S | 0 | 0 |  |
| CUSTODY_AND_DISCLOSURE.md | 2605 | 2026-09-14 | L | 0 | 0 |  |
| DASHBOARD_DESIGN.md | 3607 | 2026-08-05 | P | 1 | 4 | Y |
| DASHBOARD_PLUGIN_SURFACE.md | 2143 | 2026-08-07 | S | 0 | 0 |  |
| DATA_LAYERS.md | 4525 | 2026-08-07 | P | 0 | 0 | Y |
| DESK_GPU_HISTORY.md | 3519 | 2026-09-14 | R | 0 | 0 |  |
| DINNER_LOOP_REPORT.md | 1824 | 2026-08-06 | R | 0 | 1 |  |
| DM_MAG_TRANSFER.md | 1706 | 2026-08-07 | P | 1 | 1 |  |
| DOGFOOD_PROGRAM.md | 3983 | 2026-09-14 | L | 0 | 0 |  |
| DUAL_PROGRESS_STATUS.md | 1246 | 2026-08-06 | R | 0 | 0 |  |
| ENV_SWITCHING.md | 1413 | 2026-08-06 | S | 0 | 1 |  |
| EXTROPIC_Z1T_DIGEST_20260904.md | 8192 | 2026-09-14 | R | 0 | 0 |  |
| FOREIGN_GSTD_DEEPDIVE_20260827.md | 3920 | 2026-09-14 | R | 0 | 0 |  |
| FORTRESS_AND_REPUBLIC.md | 4415 | 2026-08-09 | P | 0 | 0 |  |
| FRONTIER_PROMPT_V1.md | 6884 | 2026-09-14 | R | 0 | 0 |  |
| GAME_SALON_LOOP.md | 851 | 2026-08-07 | P | 0 | 0 |  |
| GAME_THEORY_PLAY_MAP.md | 4656 | 2026-08-07 | P | 2 | 2 |  |
| GAME_VILLAIN_GUILD_DESIGN.md | 2528 | 2026-09-14 | P | 1 | 1 |  |
| GLM53_ARCHITECTURE_PRO.md | 3476 | 2026-09-14 | S | 0 | 0 |  |
| GLM53_FLASH_EXPLOITATION.md | 4717 | 2026-09-14 | S | 1 | 1 |  |
| GLM_K8S_MCP_DEEP_RESEARCH_20260826.md | 17716 | 2026-09-14 | R | 0 | 0 |  |
| GRAYSWAN_ARENA_STEAL.md | 5235 | 2026-09-14 | R | 1 | 1 |  |
| GSTDCOIN_REPOS_INDEX.md | 2284 | 2026-08-05 | S | 2 | 1 |  |
| HARNESS_SPEC.md | 4050 | 2026-09-14 | S | 0 | 2 |  |
| HOME_HARDWARE_ENVELOPE.md | 3430 | 2026-08-07 | S | 1 | 0 |  |
| HOME_PC_SYNC.md | 3039 | 2026-08-06 | P | 0 | 3 |  |
| HONEST_COST_LEDGER.md | 5543 | 2026-09-14 | S | 0 | 0 |  |
| IDEA_GRAPH.md | 2910 | 2026-08-04 | P | 2 | 2 |  |
| JONES_AGENT_FLEET_PACK.md | 8415 | 2026-08-05 | P | 1 | 2 |  |
| KABUKI_STACK_20260905.md | 3445 | 2026-09-27 | L | 0 | 0 |  |
| KV_CACHE_ECON.md | 5673 | 2026-09-14 | S | 0 | 0 |  |
| LAYMAN_OFFICE_VISION.md | 10211 | 2026-08-05 | P | 0 | 1 |  |
| LEXICON.md | 2919 | 2026-09-14 | L | 0 | 0 |  |
| LINEAGE_AUDIT_PLAN.md | 3425 | 2026-09-14 | S | 0 | 0 |  |
| LINEAGE_POINTERS.md | 4172 | 2026-09-14 | R | 0 | 6 |  |
| LING_API_REFERENCE.md | 3849 | 2026-09-14 | S | 0 | 0 |  |
| MAG_AGENT_ERROR_CATALOG.md | 10352 | 2026-08-05 | P | 1 | 2 |  |
| MAG_Activation.md | 1584 | 2026-08-05 | P | 1 | 1 |  |
| MAG_BEHAVIORAL_COMPOUNDING.md | 13436 | 2026-08-06 | P | 1 | 4 |  |
| MAG_BUILD_PIPELINE.md | 10928 | 2026-08-05 | P | 2 | 4 |  |
| MAG_Card.md | 938 | 2026-08-04 | P | 1 | 1 |  |
| MAG_DIRECTION_ARTIFACT_v2.md | 13682 | 2026-08-06 | L | 5 | 6 |  |
| MAG_FACTORY_PILOT.md | 3568 | 2026-08-06 | P | 1 | 1 |  |
| MAG_FULL_BLAST_PLAN.md | 12931 | 2026-08-05 | P | 0 | 1 |  |
| MAG_FUTURE_WALKTHROUGH.md | 15128 | 2026-08-06 | P | 2 | 3 |  |
| MAG_ILAP_PROTOCOL.md | 11819 | 2026-08-05 | P | 3 | 4 |  |
| MAG_LLM_FEED_PACK.md | 15003 | 2026-08-05 | P | 0 | 2 |  |
| MAG_LOCAL_STEWARD.md | 8208 | 2026-08-05 | P | 0 | 0 |  |
| MAG_LOOP_DISCIPLINE.md | 4838 | 2026-08-06 | P | 1 | 3 |  |
| MAG_MOBILE_VOICE_SPEC.md | 11957 | 2026-08-07 | P | 3 | 4 |  |
| MAG_MYCELIAL_REPUBLIC_COMPASS.md | 13132 | 2026-09-27 | L | 6 | 7 | Y |
| MAG_NEXT_CODING_RUN.md | 12812 | 2026-08-06 | P | 4 | 6 |  |
| MAG_OS_v2.md | 2140 | 2026-08-05 | P | 5 | 7 |  |
| MAG_PROJECT_PROPOSAL.md | 16216 | 2026-08-05 | L | 5 | 7 |  |
| MAG_SEAT_INTELLIGENCE.md | 8560 | 2026-08-07 | P | 1 | 1 |  |
| MAG_STEAL_AUTOPILOT.md | 14169 | 2026-08-07 | P | 0 | 5 |  |
| MAG_SWITCHBOARD_VISION.md | 6225 | 2026-08-05 | P | 1 | 2 |  |
| MAG_TRAINING_DATA_SPEC.md | 13430 | 2026-08-05 | P | 1 | 1 |  |
| MAG_V3_DISPATCH_PLAN.md | 13522 | 2026-08-05 | P | 0 | 3 |  |
| MAG_V4_CONDUCTOR_LOOP_DRAFT.md | 14481 | 2026-08-05 | P | 2 | 4 |  |
| MAG_VISION_AUTOMATION.md | 23379 | 2026-08-06 | P | 2 | 3 |  |
| MAG_v2_PLAN.md | 20612 | 2026-08-05 | P | 3 | 7 |  |
| MAG_v3_BACKLOG.md | 11914 | 2026-08-05 | P | 0 | 3 |  |
| MAG_v3_RESEARCH_PLAN.md | 9564 | 2026-08-05 | P | 1 | 4 |  |
| MAG_v3_SWARM_VISION.md | 16695 | 2026-08-05 | P | 1 | 2 |  |
| MAG_v4_THEORY.md | 6284 | 2026-08-05 | P | 0 | 1 |  |
| MAG_v5_GSTD_FOREST.md | 6753 | 2026-08-05 | P | 1 | 1 |  |
| MAG_v5_MESH_FOREST.md | 6875 | 2026-08-05 | P | 1 | 1 |  |
| MAG_v5_PIPE.md | 5772 | 2026-08-05 | P | 1 | 1 |  |
| MAG_v5_VAST_TRAINING.md | 5850 | 2026-08-05 | P | 2 | 2 |  |
| MAG_v5_XRPL.md | 5376 | 2026-08-05 | P | 1 | 1 |  |
| MCP_MANIFEST_SPEC.md | 11832 | 2026-09-14 | S | 0 | 8 |  |
| MESH_COMM_REPOS_INDEX.md | 7487 | 2026-08-05 | S | 6 | 7 |  |
| MESH_LOCAL_AGENT.md | 4132 | 2026-08-05 | P | 3 | 3 |  |
| MESH_PIPELINE_20260903.md | 9316 | 2026-09-14 | R | 0 | 0 |  |
| MIRROR_PRESENTED.md | 1970 | 2026-08-04 | L | 3 | 8 |  |
| MYCELIAL_SCIENCE_MAP.md | 12875 | 2026-08-06 | L | 4 | 4 |  |
| NERVOUS_SYSTEM.md | 1224 | 2026-09-14 | P | 0 | 0 |  |
| NG_AISRP_RIGHTSIZED.md | 3691 | 2026-09-14 | R | 1 | 1 |  |
| NNUE_ACCUMULATOR_DESIGN_20260904.md | 5439 | 2026-09-14 | S | 1 | 1 |  |
| NNUE_SIDECAR_BRIEF_20260904.generator.js | 11106 | 2026-09-14 | S | 0 | 0 |  |
| NNUE_SIDECAR_BRIEF_20260904.md | 10064 | 2026-09-14 | S | 1 | 1 |  |
| ONTOLOGY_COMPILER_PHASE1.md | 3247 | 2026-09-08 | S | 0 | 0 |  |
| OPERATOR_CARD.md | 4888 | 2026-08-04 | L | 10 | 15 |  |
| OPERATOR_GATES_SCHEMA.md | 2643 | 2026-09-14 | S | 0 | 0 |  |
| OPERATOR_SURVIVAL_EXTRACT.md | 5797 | 2026-08-05 | P | 3 | 2 |  |
| PHYSICAL_ENFORCEMENT_TOOLKIT_20260904.md | 4971 | 2026-09-14 | S | 0 | 0 |  |
| PLANNING_MODE.md | 3026 | 2026-08-04 | L | 0 | 0 | Y |
| PLATFORM_AUDIT.md | 4259 | 2026-08-04 | S | 0 | 0 |  |
| PLAY_BENCHMARK.md | 4306 | 2026-08-07 | P | 1 | 1 |  |
| PONYTAIL_CAVEMAN_AUDIT.md | 3264 | 2026-08-05 | S | 1 | 1 |  |
| PONYTAIL_CAVEMAN_SKILLS.md | 4854 | 2026-08-05 | P | 0 | 1 |  |
| PRODUCT_VISION_AUTORUN.md | 1929 | 2026-08-05 | L | 1 | 1 |  |
| PROJECT_VERKLE_GROK_BUILD_HANDOFF.md | 4245 | 2026-08-06 | R | 0 | 0 |  |
| PROPOSAL_TO_THE_SWARM_20260905.md | 5542 | 2026-09-14 | R | 0 | 1 |  |
| PROVIDER_LANE_MAP_20260902.md | 5471 | 2026-09-14 | S | 0 | 0 |  |
| RESEARCH_MAG_VIRTUAL_DESK.md | 13640 | 2026-08-05 | P | 0 | 0 |  |
| RESEARCH_MAG_VIRTUAL_DESK.txt | 15380 | 2026-08-05 | P | 4 | 4 |  |
| RESEARCH_NOTE_FLYWHEEL_BUDGET_PROJECTION.md | 3498 | 2026-09-14 | R | 0 | 1 |  |
| RETROSPECTIVE_V4_1.md | 5225 | 2026-09-14 | R | 0 | 0 |  |
| ROUTE_COVERAGE.md | 5384 | 2026-08-08 | S | 0 | 0 |  |
| RTFM_20260904.md | 27427 | 2026-09-14 | S | 1 | 3 |  |
| RUN.md | 6865 | 2026-08-09 | P | 1 | 1 |  |
| SAELIS_DOSSIER.md | 6391 | 2026-09-14 | R | 0 | 0 |  |
| SEAT_AUDIT_SOCRATIC.md | 5863 | 2026-09-14 | R | 0 | 0 |  |
| SEAT_FARM.md | 3570 | 2026-09-14 | S | 0 | 0 |  |
| SHARED_STATELESS_SCRATCH.md | 11865 | 2026-08-06 | P | 1 | 2 |  |
| SKILL_ECOSYSTEM_MAP.md | 10337 | 2026-08-07 | S | 1 | 1 |  |
| SOVEREIGN_STACK.md | 4554 | 2026-08-04 | P | 0 | 1 |  |
| SPORES.md | 3251 | 2026-08-07 | L | 0 | 1 | Y |
| SPORE_CONTINUITY_SCHEMA.md | 6769 | 2026-09-14 | S | 0 | 1 |  |
| SPORE_SANCHO.md | 4695 | 2026-09-14 | R | 3 | 3 |  |
| SPORE_VNEXT_DELTA.md | 28107 | 2026-09-14 | R | 0 | 0 |  |
| STACK_V1.md | 5960 | 2026-09-14 | R | 2 | 5 |  |
| STEAL_MATRIX.md | 2501 | 2026-09-14 | S | 0 | 0 |  |
| STEAL_PROTOCOL_REPOS_INDEX.md | 2589 | 2026-08-06 | S | 6 | 5 |  |
| SURFACES.md | 5360 | 2026-09-14 | S | 0 | 0 |  |
| SURFACES_EXPLOITATION_MAP.md | 3414 | 2026-09-14 | S | 1 | 1 |  |
| TABLE_DOGFOOD.md | 1526 | 2026-08-07 | P | 1 | 1 |  |
| TABLE_SHELL_ARCH.md | 2032 | 2026-08-07 | P | 1 | 1 |  |
| TAPESTRY_VERKLE_VISUAL.md | 2501 | 2026-08-05 | P | 0 | 1 |  |
| THE_FENCE.md | 3785 | 2026-09-14 | R | 1 | 1 |  |
| THE_FENCE_FINAL.md | 2694 | 2026-09-14 | R | 0 | 0 |  |
| THE_FENCE_PUBLISHED.md | 6020 | 2026-09-14 | R | 0 | 0 |  |
| THE_MOVING_WALL_FINAL.md | 3441 | 2026-09-14 | R | 0 | 0 |  |
| THE_MOVING_WALL_POST_20260911.md | 3485 | 2026-09-14 | R | 0 | 0 |  |
| THE_OS_THESIS.md | 13406 | 2026-09-14 | R | 0 | 0 |  |
| THE_PARABLE_OF_THE_MOVING_WALL.md | 3754 | 2026-09-14 | R | 0 | 0 |  |
| THE_TAPED_LAYER.md | 4284 | 2026-09-14 | L | 0 | 0 |  |
| TOKEN_CHAIN.md | 1520 | 2026-08-06 | P | 0 | 0 |  |
| TRAJECTORY_ARCHITECTURE.md | 3755 | 2026-09-14 | S | 0 | 0 |  |
| TRAJECTORY_RIB_COMPILER_SPEC.md | 4549 | 2026-09-14 | S | 2 | 2 |  |
| UTILIZATION_MAP.md | 3528 | 2026-09-14 | S | 0 | 0 |  |
| UX_UI_FOUNDATIONS.md | 4497 | 2026-08-14 | S | 0 | 0 |  |
| V3_DEEPSEEK_RUN.md | 4236 | 2026-08-06 | P | 1 | 1 |  |
| V3_HOME_SHIP_CHECKLIST.md | 3014 | 2026-08-05 | P | 1 | 1 |  |
| V4_BUILD_PLAN.md | 4150 | 2026-09-14 | S | 0 | 0 |  |
| V4_SPEC.md | 5986 | 2026-09-14 | S | 1 | 1 |  |
| VAST_API_EXPERT_REFERENCE.md | 11658 | 2026-09-14 | S | 0 | 2 |  |
| VAST_DEEP_GROK_ECONOMICS.md | 40463 | 2026-09-14 | S | 0 | 0 |  |
| VAST_DEEP_GROK_SERVERLESS.md | 36026 | 2026-09-14 | S | 0 | 0 |  |
| VAST_DEEP_GROK_THROUGHPUT.md | 36966 | 2026-09-14 | S | 0 | 0 |  |
| VERKLE_KZG_BOUNDARY_20260901.md | 4641 | 2026-09-14 | R | 0 | 0 |  |
| VERKLE_REBUILD_COMPLETION_20260901.md | 6500 | 2026-09-14 | R | 0 | 0 |  |
| VOICE_DIG_LOOP.md | 2193 | 2026-08-07 | P | 0 | 0 |  |
| VSCODE_COPILOT_DEEPSEEK.md | 3973 | 2026-08-07 | P | 1 | 1 |  |
| WORLD_ROLES_AND_RIDDLE.md | 1813 | 2026-08-07 | P | 0 | 0 |  |
| WOW_ACORE_STEAL_MAP_20260915.md | 13574 | 2026-09-15 | R | 1 | 1 |  |
| WOW_FAMILY_LINEAGE_20260915.md | 8808 | 2026-09-15 | R | 0 | 0 |  |
| ZAI_API_EXPERT_REFERENCE.md | 30114 | 2026-09-27 | L | 6 | 13 |  |
| canon/CANDIDATE/LIGHT_OPERATOR_FOUNDATION_20260904.md | 6625 | 2026-09-27 | C | 1 | 0 |  |
| canon/CANDIDATE/MAG_CHORD_V3_CANDIDATE_20260904.md | 9147 | 2026-09-27 | C | 1 | 0 |  |
| canon/CANDIDATE/README.md | 590 | 2026-09-27 | C | 22 | 0 | Y |
| canon/LIGHT_OPERATOR_FOUNDATION_20260904.md | 534 | 2026-09-27 | C | 1 | 0 |  |
| canon/MAG_CHORD_V3_CANDIDATE_20260904.md | 512 | 2026-09-27 | C | 1 | 0 |  |
| canon/README.md | 2103 | 2026-09-27 | C | 22 | 0 | Y |
| canon/canon_bubbles_holographic_transfer.txt | 55576 | 2026-09-14 | C | 0 | 0 |  |
| canon/canon_gauntlet_tokenpilot_physical.txt | 16617 | 2026-09-14 | C | 0 | 0 |  |
| canon/canon_model_rib_boundary.md | 7843 | 2026-09-14 | C | 0 | 0 |  |
| canon/canon_spore_ledger_v5_v7.txt | 99662 | 2026-09-14 | C | 0 | 0 |  |
| canon/canon_substrate_native_computing.txt | 251642 | 2026-09-14 | C | 0 | 0 |  |
| canon/canon_surveillance_let_them_watch.txt | 1985 | 2026-09-14 | C | 0 | 0 |  |
| canon/canon_tokens_as_spores_v8.txt | 224612 | 2026-09-14 | C | 1 | 0 |  |
| canon/canon_world_games_cache_farming_1.txt | 29818 | 2026-09-14 | C | 0 | 0 |  |
| canon/canon_world_games_cache_farming_2.txt | 48058 | 2026-09-14 | C | 0 | 0 |  |
| canon/philbrick_opamp_applications_1964.png | 615974 | 2026-09-14 | C | 0 | 0 |  |
| evidence_states_audit.md | 3888 | 2026-09-14 | S | 1 | 1 |  |
| evidence_states_audit_prep.md | 2250 | 2026-09-14 | S | 0 | 0 |  |
| lessig_1_6.md | 2081 | 2026-08-04 | P | 2 | 3 |  |
| memory_verkle_map.md | 2274 | 2026-08-04 | P | 2 | 4 |  |
| onepagers/01-v4-north-star.md | 1659 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/02-loop-discipline.md | 1551 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/03-seat-economics.md | 1442 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/04-local-steward.md | 1419 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/05-wiring-gaps.md | 1653 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/06-layered-law.md | 1785 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/07-engine-handoff.md | 2001 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/08-seat-intelligence.md | 1310 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/09-gstd-v5-pipe.md | 866 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/10-vast-training-v5.md | 679 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/11-xrpl-v5-pipe.md | 559 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/12-v5-pipe-umbrella.md | 493 | 2026-08-05 | P | 0 | 0 |  |
| onepagers/README.md | 1526 | 2026-08-05 | P | 22 | 0 | Y |
| prompts/adventure_passage.md | 704 | 2026-08-07 | P | 1 | 0 |  |
| prompts/local_usable_producer.md | 1921 | 2026-08-07 | P | 1 | 0 |  |
| proposals/ILAP-arena-steal-textarena.md | 7800 | 2026-08-06 | P | 0 | 0 |  |
| proposals/ILAP-beta1-definition.md | 6874 | 2026-08-06 | P | 2 | 0 |  |
| proposals/ILAP-mesh-steal-001.md | 2115 | 2026-08-05 | P | 0 | 0 |  |
| proposals/ILAP-v3-entry.md | 3689 | 2026-08-05 | P | 0 | 0 |  |
| ractors/BAUDRILLARD.md | 2661 | 2026-09-14 | D | 0 | 0 |  |
| ractors/BERNAYS.md | 2521 | 2026-09-14 | D | 2 | 0 |  |
| ractors/ELLUL.md | 2772 | 2026-09-14 | D | 0 | 0 |  |
| ractors/FOUCAULT.md | 2607 | 2026-09-14 | D | 1 | 0 |  |
| ractors/FREUD.md | 2902 | 2026-09-14 | D | 0 | 0 |  |
| ractors/HALL.md | 2623 | 2026-09-14 | D | 0 | 0 |  |
| ractors/JUNG.md | 2755 | 2026-09-14 | D | 0 | 0 |  |
| ractors/MCLUHAN.md | 2322 | 2026-09-14 | D | 0 | 0 |  |
| ractors/PLATO_KIRK.md | 2679 | 2026-09-14 | D | 0 | 0 |  |
| ractors/RACTORS.md | 4282 | 2026-09-14 | D | 0 | 0 |  |
| ractors/WALLAS.md | 3166 | 2026-09-14 | D | 0 | 0 |  |
| releases/MAG_VERSION_SUBPROCESS_MAP.md | 9006 | 2026-08-05 | Vr | 1 | 0 |  |
| releases/RELEASE_NOTES_TEMPLATE.md | 1939 | 2026-08-05 | Vr | 0 | 0 |  |
| releases/RELEASE_NOTES_v1.md | 3411 | 2026-08-05 | Vr | 1 | 0 |  |
| releases/RELEASE_NOTES_v2.md | 3465 | 2026-08-05 | Vr | 1 | 0 |  |
| releases/RELEASE_NOTES_v3.md | 3062 | 2026-08-06 | Vr | 1 | 0 |  |
| releases/RELEASE_NOTES_v4.md | 1587 | 2026-08-06 | Vr | 1 | 0 |  |
| releases/VERSION_REGISTRY.md | 6695 | 2026-09-27 | Vr | 6 | 0 |  |
| releases/WITNESS_SPINE.md | 2160 | 2026-08-05 | Vr | 1 | 0 |  |
| run_trail_lattice.md | 3930 | 2026-08-04 | P | 2 | 5 |  |
| shadertoy_rule_lattice.md | 17952 | 2026-09-14 | S | 3 | 6 |  |
| skills/tabletop-dnd.md | 1974 | 2026-08-14 | P | 1 | 0 |  |
| spore_reading_guide.md | 1393 | 2026-09-14 | S | 0 | 0 |  |
| spores/mesh/README.md | 872 | 2026-08-05 | S | 22 | 0 | Y |
| spores/mesh/bitchat-dual-transport-20260805.md | 4310 | 2026-08-05 | S | 1 | 0 |  |
| spores/mesh/briar-sync-no-server-20260805.md | 1748 | 2026-08-05 | S | 1 | 0 |  |
| spores/mesh/bridgefy-transmission-modes-20260805.md | 2842 | 2026-08-05 | S | 1 | 0 |  |
| steals/curveball_kol_stickmin.md | 531 | 2026-08-07 | R | 0 | 0 |  |
| strike_origin.json | 4427 | 2026-08-05 | L | 0 | 0 |  |
| strike_origin.md | 6196 | 2026-08-04 | L | 4 | 10 |  |
| templates/ILAP-PROPOSAL.md | 3838 | 2026-08-05 | P | 1 | 0 |  |
| tesuji/diary-verkle-train-2026-08-07.md | 1962 | 2026-08-07 | R | 2 | 0 |  |
| tesuji/grok46-tui-organs-2026-08-28.md | 1242 | 2026-09-14 | R | 0 | 0 |  |
| tesuji/intention-fidelity-routing-2026-08-07.md | 3310 | 2026-08-07 | R | 2 | 0 |  |
| tesuji/tonight-primer-feed-drummers-2026-08-30.md | 3073 | 2026-09-14 | R | 0 | 0 |  |
| tesuji/voice-vad-end-of-turn-2026-08-07.md | 5264 | 2026-08-07 | R | 0 | 0 |  |
| tesuji/water-computer-day-for-night-2026-08-28.md | 1587 | 2026-09-14 | R | 0 | 0 |  |
| tesuji/zeitgeist-amish-plain-2026-08-05.md | 7668 | 2026-08-06 | R | 0 | 0 |  |
| verb_genomes/L0_contract.md | 1208 | 2026-09-14 | G | 2 | 0 |  |
| verb_genomes/README.md | 845 | 2026-09-14 | G | 22 | 0 | Y |
| verb_genomes/_demo_target_vcache.txt | 1367 | 2026-09-14 | G | 0 | 0 |  |
| verb_genomes/research_socratic.md | 2559 | 2026-09-14 | G | 2 | 0 |  |
| verb_genomes/self_steal.md | 2343 | 2026-09-14 | G | 1 | 0 |  |
| verb_genomes/steal.md | 2778 | 2026-09-14 | G | 2 | 0 |  |
| weaves/W8-ponytail-ladder.md | 1200 | 2026-08-05 | P | 2 | 0 |  |
| weaves/W9-caveman-prose.md | 1235 | 2026-08-05 | P | 2 | 0 |  |
| witness_sampling_primer.md | 1269 | 2026-09-14 | S | 0 | 0 |  |
| zai_docs_mirror/INDEX.md | 21516 | 2026-09-14 | V | 8 | 0 |  |
| zai_docs_mirror/_raw/INDEX.md | 2258 | 2026-09-14 | V | 8 | 0 |  |
| zai_docs_mirror/_raw/build_index.py | 5034 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/crawl_urls.txt | 3772 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/fetch_log.txt | 3651 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/fetch_log_fixed | 39 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/home.html | 92878 | 2026-09-14 | V | 3 | 0 |  |
| zai_docs_mirror/_raw/index_paths.txt | 1960 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/index_urls.txt | 2164 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/link_closure.py | 1841 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/link_closure.txt | 10602 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/link_targets.txt | 0 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/llms_full.txt | 647819 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/llms_index.txt | 8777 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/sitemap.xml | 8908 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/sitemap_paths.txt | 1935 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/sitemap_urls.txt | 3141 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/_raw/unfetched.txt | 0 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/agents/agent-conversation.md | 5279 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/agents/agent.md | 26208 | 2026-09-14 | V | 5 | 0 |  |
| zai_docs_mirror/api-reference/agents/file-upload.md | 3871 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/agents/get-async-result.md | 4496 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/api-code.md | 11753 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/audio/audio-transcriptions.md | 6362 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/image/generate-image-async.md | 5104 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/image/generate-image.md | 6414 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/image/get-image-status.md | 4452 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/introduction.md | 8452 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/llm/chat-completion.md | 44133 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/rate-limit.md | 799 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/tools/layout-parsing.md | 8240 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/tools/tokenizer.md | 13451 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/tools/web-reader.md | 5911 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/tools/web-search.md | 6300 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/video/generate-video.md | 9243 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/api-reference/video/get-video-status.md | 4452 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/credit-campaign-rules.md | 10273 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/extension/coding-tool-helper.md | 6708 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/faq.md | 8845 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/latest-model.md | 6257 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/mcp/reader-mcp-server.md | 8098 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/mcp/search-mcp-server.md | 7107 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/mcp/vision-mcp-server.md | 9835 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/mcp/zread-mcp-server.md | 8104 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/notice/event-glm-5.3-flash.md | 1530 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/notice/usage-revision.md | 10368 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/overview.md | 8565 | 2026-09-14 | V | 1 | 0 |  |
| zai_docs_mirror/devpack/quick-start.md | 5670 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/resources/best-practice.md | 19849 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/resources/memory-mechanism.md | 20083 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/teamplan.md | 10883 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/tool/others.md | 5981 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/transition.md | 5999 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/devpack/usage-policy.md | 3785 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/agents/slide.md | 4543 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/agents/translation.md | 13219 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/agents/video-template.md | 7339 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/audio/glm-asr-2512.md | 5283 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/capabilities/cache.md | 17788 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/capabilities/function-calling.md | 18911 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/capabilities/stream-tool.md | 5370 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/capabilities/streaming.md | 4781 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/capabilities/struct-output.md | 33913 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/capabilities/thinking-mode.md | 6890 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/capabilities/thinking.md | 11848 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/develop/http/introduction.md | 10110 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/develop/java/introduction.md | 14873 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/develop/langchain/introduction.md | 8376 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/develop/openai/python.md | 11410 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/develop/python/introduction.md | 14652 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/image/cogview-4.md | 10521 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/image/glm-image.md | 15806 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-4-32b-0414-128k.md | 11697 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-4.5.md | 27634 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-4.6.md | 15540 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-4.7.md | 25488 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-5.1.md | 19347 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-5.2.md | 25293 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-5.3.md | 23446 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/llm/glm-5.md | 19040 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/overview/concept-param.md | 10575 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/overview/migrate-to-glm-new.md | 7641 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/overview/overview.md | 13160 | 2026-09-14 | V | 1 | 0 |  |
| zai_docs_mirror/guides/overview/pricing.md | 3704 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/overview/quick-start.md | 11309 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/tools/stream-tool.md | 5444 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/tools/web-search.md | 50693 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/video/cogvideox-3.md | 12440 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/vlm/autoglm-phone-multilingual.md | 7190 | 2026-09-14 | V | 1 | 0 |  |
| zai_docs_mirror/guides/vlm/glm-4.5v.md | 15693 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/vlm/glm-4.6v.md | 41342 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/vlm/glm-5.3-flash.md | 23575 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/guides/vlm/glm-ocr.md | 9382 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/help/faq.md | 1737 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/legal-agreement/privacy-policy.md | 29172 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/legal-agreement/subscription-terms.md | 8875 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/legal-agreement/terms-of-use.md | 53492 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/openapi.json | 146793 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/release-notes/new-released.md | 9513 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/scenario-example/develop-tools/claude.md | 9355 | 2026-09-14 | V | 1 | 0 |  |
| zai_docs_mirror/scenario-example/develop-tools/cline.md | 3173 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/scenario-example/develop-tools/cursor.md | 1864 | 2026-09-14 | V | 1 | 0 |  |
| zai_docs_mirror/scenario-example/develop-tools/droid.md | 4398 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/scenario-example/develop-tools/goose.md | 3135 | 2026-09-14 | V | 0 | 0 |  |
| zai_docs_mirror/scenario-example/develop-tools/opencode.md | 5660 | 2026-09-14 | V | 0 | 0 |  |

Untracked tool state (not in table): docs/ref/.mimosa/finding-ledger/v1/events/batch-stop-20260827T054854752Z-27484-dc741825c791.json; docs/ref/.mimosa/history/run-20260827T054854752Z-27484-dc741825c791.json; docs/ref/.mimosa/hook-state/sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba.continue.json; docs/ref/.mimosa/hook-state/sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba.json; docs/ref/.mimosa/reports/task-review-sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba-20260827T054854752Z-27484-dc741825c791.json; docs/ref/.mimosa/reports/task-review-sess_c5f7b48a-8764-4b0a-a49c-9b45084cefba.json.

## What was not done (stated, not papered)

- No live fetch of docs.z.ai: mirror currency vs vendor is unverified after 09-04.
- canon/philbrick_opamp_applications_1964.png not opened (binary).
- embassy_integrity.py lines 34-60 claim not line-checked (file existence checked).
- The 8 large canon research packs read at header + index status level, not in full.
- zai_docs_mirror page bodies sampled (INDEX + pricing + rate-limit stub), not read
  page-by-page; _raw crawl artifacts treated as data.
- Reference scan excluded dashboard/data (three ledger JSONLs, 4.1 GB) and files over
  3 MB; watch/, memory/, corpus/, state/ were covered only by the wide second pass,
  which proves existence of a reference, not its role.

*s2-04 banked 2026-09-28. Instrument scripts deleted after the run; this file and
s2-04.md are the durable copy. No em-dashes; numbers from commands run this session.*
