# TOOL GENOME PROJECT (deep-tool-genome) - 2026-09-28

Sequenced by a gopher lane, deep item `deep-tool-genome`. Genome definition per the ask:
ancestry = imports, descendants = callers, immune system = tests, fossil record = receipts.
Instruments banked beside this file: `tool_genome_extract.py` (sequencer),
`tool_genome_stats.py` (analysis), `tool_genome_data.json` (raw genomes, every tool).
All commands were run this session with `.venv/Scripts/python.exe` on repo
`C:/Users/foste/Documents/projects/local_sovereign_agent` at HEAD `d90bc8607` (branch
`mag/run-beta1-factory-build-audi-20260806T231709Z`, tree clean except 4 modified tools
and 1 untracked: `tools/prompt_compiler.py`).

## 0. Census law compliance (B2-216: name instrument, moment, delta)

The ask says "the 177 tools". The byte truth at 2026-09-28: `git ls-files tools/ |
grep '\.py$' | wc -l` = **189** tracked `.py` (190 on disk counting untracked
`tools/prompt_compiler.py`). `git ls-files tools/` = 262 files total (27 exe, 30 dll,
4 zip, 4 luau, 2 js, 2 json, 1 mjs, 1 md: the vendored luau/rojo toolchain are organelles,
not genes). I searched `watch/inbox/burn_reset_20260927/queue/` for a census artifact
naming 177 and found only numeric coincidences (`FW35_adventurelearn.md`,
`Q_031_retrieval_eval_results.json`, `RECIPROCITY_LEDGER.jsonl`); the 177 denominator is
stale or differently scoped and I cannot attribute the +12 delta. Everything below is at
189 (188 analyses after excluding the `tools/__init__.py` operon).

## 1. Genotype

188 genes, 42,691 LOC total. Largest: `pupeteer_gauntlet` 1281; smallest: `smoke_import` 4.
189/189 parse clean under `ast.parse` (0 failures). Git: 656 commits, first commit
2026-08-04 (`git log --reverse --format=%ad --date=short | head -1`), so the whole genome
is 55 days old.

## 2. Oldest ancestors (the primordial genome)

Born the repo's first day, 2026-08-04: `tools/__init__.py`, `code_execution.py`,
`filesystem.py`, `shell.py`. That is the original body plan: read, write, execute, and one
glue module. Second day-wave 2026-08-07: `autopilot`, `one_pipe`, `smoke_import`,
`spawn_gpipe`, `test_pipe_api`, the gpipes experiment, now all zero-strong-caller living
fossils.

`tools/__init__.py:1-2` is the **operon**: it imports exactly ten siblings
(`code_execution, corpus, drift, filesystem, research, sense_tools, shell, swarm_tools,
thrash_meter, verb_anchor`) plus `mag.vision`, and wires them into a `TOOL_MAP` of
lambdas (list_dir/read_file/write_file/apply_patch/run_shell/run_python/swarm_sense/
pheromone_drop/...). Those ten are the essential genome: the swarm body's organs. Deeper
mag ancestry: 39 tools import some `mag.*` (top: bare `mag` 23, `mag.lite_guard` 10,
`mag.improve` 10, `mag.verkle_knot` 9, `mag.orchestrator` 9, `mag.skill_ledger` 8), while
**149 of 188 import no mag module at all**: most tools are free-living plasmids, not
organelles of the mag cell.

## 3. Most prolific descendants

Because descent here is mostly invocation, not import, I tier callers: **strong** = a
`tools/X` path or `from tools import X` edge in live code (mag/, scripts/, dashboard/,
githooks/, .agents/), **bare** = a `name.py` string mention. Bare-only counts were
contaminated by homonyms (section 7) and by corpus/ oral-history transcripts, and were
demoted.

- **`pile_classify` is the most-connected gene: 6 strong callers, all verified**:
  `from tools.pile_classify import run_pile` at `mag/governor_autorun.py:1211` and
  `mag/improve_loop.py:194`, docstring pointer at `mag/state_snapshot.py:5`, plus
  `mag/decision_framework.py`, `mag/framework_map.py`, and `scripts/day_end_pile.ps1`
  (the FW-50 pile habit). Its 1 test is `tests/test_state_pile.py`. Six consumers, one
  antibody.
- `corpus`: 3 strong callers (`mag/catalog_freshness.py`, `scripts/build_knowledge_graph.py`,
  `dashboard/static/deck.html`) + 3 test files + 1 import child. The import hub.
- `corpus_fts_rebuild` 3 strong (the B2-465 daily FTS task), `drift` 3 strong,
  `census_drift_patrol` 2 strong + 2 tests (B2-215/B2-246), `pupeteer_gauntlet` 2 strong +
  2 tests + 1 child (imported by `pile_classify`: the pile classifier literally runs the
  gauntlet), `code_execution` 2 strong (`mag/framework_map.py`, `mag/guard_registry.py`),
  `filesystem` strong at `mag/openclaw_patches.py:42` (`from tools.filesystem import
  write_file`) + 2 tests.
- Import-descendant counts: only `corpus`, `drift`, `estate_env`, `secret_gate_rules` have
  2 children each. Deepest lineage chain in the whole genome:
  `corpus_diff -> corpus_lens -> corpus_self_lens`, depth 3.
- Fossil-record leaders (distinct receipt files mentioning the tool, strong-or-bare,
  outside tools/): `shell` 259, `violation_ratchet` 220, `code_execution` 181,
  `autopilot` 149 (homonym-inflated, see section 7), `pupeteer_gauntlet` 125,
  `filesystem` 110, `swarm_tools` 109, `secret_gate` 116 with ZERO code callers: a pure
  law-gene, endlessly cited, never wired.

The caller distribution (6, 3, 3, 3, 3, 2, 2, ...) is a steep designed drop, not a
scale-free hub. That matches a wired organism (the estate literally keeps a wiring
diagram, `mag/organ_map.py`), not preferential attachment (Barabasi-Albert 1999, general
literature). Nobody "grew into" hub status; `pile_classify` was *wired* into five mag
modules on purpose.

## 4. The immune system

36/189 tools (19%) have at least one test file; 153 have none. By Feathers' definition
("to me, legacy code is simply code without tests", *Working Effectively with Legacy
Code*, 2004, general literature), **81% of this genome is legacy code**, and it does not
die of it. The 2x2 (callers x tests):

- **VITAL 16** (wired AND tested): audio_channel, auto_promote, census_drift_patrol,
  config_seal, corpus, corpus_fts_rebuild, drift_dashboard, filesystem, md_record_seal,
  meter_patrol, pile_classify, pupeteer_gauntlet, shell, tier_probe, violation_ratchet,
  workflow_gate.
- **RISKY 24** (wired, untested): autopilot, classify_corpus, code_execution,
  compare_versions, corpus_lens, drift, estate_smith_chart, fold_mickey17, fossil_check,
  freshness_check, lattice_build, local_bench, oracle_calibration,
  policy_eval_schema_check, research, roblox_npc_gateway, spec_execute, stealth_sweep,
  steer_compare, swarm_tools, task_wall, thought_quantizer, thrash_meter, topic_research.
  `drift`, `code_execution`, `research`, `thrash_meter` are body-plan organs with zero
  antibodies.
- **GLASS 20** (unwired, tested): museum specimens under tests/ with no live consumer
  (secret_gate, seed_mcp pair, stealth_driver, freshness_gate, quote_gate, ...).

The acquired immune system is not pytest, it is the pre-push ratchet:
`tools/violation_ratchet.py` + `tools/workflow_gate.py` (AGENTS.md build discipline),
1 strong caller each (the hook), 220 and 103 fossils respectively. The estate spends its
immunity budget on law-enforcement genes, not on the body-plan.

## 5. Fossil record

**188/188 tools have at least one fossil mention** in watch/memory/docs/queue/state/corpus.
Zero unmarked graves: the receipt discipline functions as a complete sedimentary record,
which is extraordinary by software-archaeology standards. But fossils decouple from
metabolism: 148 tools have fossils yet zero live-code callers, i.e. **remembered but not
expressed**. The extreme is `violation_ratchet`: 220 fossils, 1 execution site per push.
`TOOLS.md` itself is a fossil of the expressed genome: 3,788 lines registering 472 tools
from `memory/tool_manifest.json`, auto-generated 2026-08-10T23:16Z, 49 days stale
(FW-11 assigns the fence to the operator).

## 6. Extinct lineages

Git truth: `git log --no-renames --diff-filter=D --name-status -- tools/` finds **zero
removals in 55 days and 656 commits** (262 paths ever added, 0 removed). Extinction by
deletion does not exist in this genome, and the estate's own laws forbid it: fireball-cycle
SKILL.md Law: "Fireball does not delete. It changes phase and **creates a tool**"
(`.agents/skills/fireball-cycle/SKILL.md:29`), and death is instead *declared*:
`watch/inbox/GENE_POOL_TOMBSTONE_20260927.md` root-causes `mag/gene_pool_feeder.py` as
"Dead-at-birth" (no regenerator, zero consumers) and records the disposition in
`configs/fossil_registry.json` ("revive condition = named consumer first"). One gene has
a tombstone; 148 are silent with no disposition.

So extinction here is functional silence, and it has a signature: **date-stamped names
are self-archiving fossils** (`eastwest_thorn_20260920`, `letter_salon_20260920`,
`verify_lyapunov_decode_20260921`, `librarian_backfill_20260927`: the estate dates its
dead ends into the gene name). The Aug-7 gpipes wave (`one_pipe`, `smoke_import`,
`spawn_gpipe`, `test_pipe_api`) is the coelacanth clade: alive on disk, unparsed by any
caller since August, immortal because nothing deletes.

## 7. Horizontal gene transfer and homonyms

Six byte-identical clone groups (sha256, tracked `.py` estate-wide): `tools/build_seed.py`
== `seed/engines/build_seed.py`, and likewise `estate_atlas`, `estate_smith_chart`,
`model_bakeoff`, `stealth_sweep`; plus `tools/seed_rib.py` ==
`watch/inbox/seed_rib_20260926/seed-rib/rib/seed_rib.py`. That is whole-organism budding
across repos, transfer without divergence (zero byte drift so far), not recombination.

Homonyms are the dangerous lookalikes: `tools/autopilot.py` (83 LOC, gpipes swarm runner,
`python tools/autopilot.py goals.txt` usage line) vs `mag/autopilot.py` (113 LOC,
three-track improve/governor/seed-mirror governor), and `tools/swarm_tools.py` (77 LOC)
vs `mag/swarm_tools.py` (455 LOC). Same name, different gene: convergent naming, verified
by `diff` and `wc -l` this pass. My first-pass caller table had `autopilot` at 69 callers;
that was almost entirely the mag homonym and transcript noise, which is exactly how a
naive text router fires the wrong gene.

Paralog families (gene duplication with suffix drift, Ohno 1970 style, general
literature): seed_* 6, build_adam_* 5 (setup -> setup_final -> soul -> soul_full: an
explicitly iterated allele chain), build_*pdf 5 (`build_plain_pdf` -> `build_plain12_pdf`
is a numbered allele), cathedral_* 4, corpus_* 4, census_*/probe20_*/queue_*/stealth_*/
x_churn_* 3 each, drift_*/eigenmap_*/steer_grok_* 2 each. Foreign gene cassettes:
reportlab markers (A4/HexColor/Paragraph/Table, 9 tools: the PDF-builder cassette),
python-dotenv 8, plus repo-root packages `config` (25) and `models` (19).

## 8. Speciation dynamics

Births per week (git first-add dates): week of Aug 3: 26, Aug 10: 1, Aug 17: 6,
Aug 24 - Sep 13: 0, Sep 14: 15, **Sep 21: 135**, Sep 28: 5 so far. That is punctuated
equilibrium (Eldredge and Gould 1972, general literature), not gradualism: 72% of the
genome is one week old, the product of the burn-wave adaptive radiation that this very
flash50/queue batch belongs to. Lehman's law of continuing change (Lehman 1980, general
literature) is hyper-obeyed; his law of increasing complexity is obeyed with no opposing
force, because the genome has no apoptosis: LOC only ratchets up, exactly like the
violation ratchet it reveres.

## 9. Diagnosis

This is a **bacterial genome, not a eukaryotic tree**: 18 sibling-import edges among 188
genes (28 counting the operon), max depth 3, descent by cloning, budding, and subprocess
invocation, with the true phylogeny recorded not in imports but in prose receipts.
`mag/organ_map.py:7-16` already invented the estate's gene ontology (DECLARED,
INSTRUMENTED, WIRED, STATEFUL, VERIFIED, LIVE, GHOST); this project is the
population-genetics sequel to that anatomy lesson. Three actionable findings:

1. The 24 RISKY genes are the fragility surface: wired into live paths with zero
   antibodies. `pile_classify` (6 callers, 1 test) is the single point of highest
   load-times-lowest-redundancy.
2. Homonym shadowing (`autopilot`, `swarm_tools`) means any bare-name router can fire the
   wrong gene; organ_map wiring should be strong-path-only.
3. The missing organ is not more tests, it is a **controlled apoptotic pathway**: the
   GENE_POOL_TOMBSTONE protocol (root-cause, disposition row in
   `configs/fossil_registry.json`, revive condition named) generalized from one gene to
   the 148 silent ones, converting them from unbounded context tax into declared sediment
   (the fireball law keeps the bytes: phase-change to receipt, never deletion).

## 10. Falsifiable predictions (dated 2026-10-28, re-run protocol included)

Re-run: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/tool_genome_extract.py`
then `tool_genome_stats.py` (deterministic, $0, no network). Predictions: (a) tools/
deletion count will still be exactly 0; (b) tools/*.py will exceed 230; (c) of the
Sep-21 cohort of 135, fewer than 15% will have gained a strong caller. If (c) fails the
other way (>= 30%), the radiation was real speciation; if under 5%, it was a Cambrian
bloom followed by mass functional extinction without burial, and the tombstone pathway
becomes urgent rather than advisable.

## Provenance

Commands run this session: `git ls-files tools/` (+ wc/grep counts), `git log
--no-renames --diff-filter=A/D ... -- tools/`, `git rev-list --count HEAD` (656),
`git log --reverse --format=%ad | head -1` (2026-08-04), the three banked scripts above,
`diff`/`wc -l` on the autopilot and swarm_tools homonym pairs, `grep -n` verification of
every cited edge (`mag/governor_autorun.py:1211`, `mag/improve_loop.py:194`,
`mag/state_snapshot.py:5`, `mag/openclaw_patches.py:42`, `mag/organ_map.py:209`,
`tools/__init__.py:1-2`). Not run: pytest (no test surface touched; the banked
instruments are new untracked files under watch/inbox, outside the ratchet's mag/+tools
scope). Literature anchors (Lehman 1980, Feathers 2004, Barabasi-Albert 1999, Eldredge
and Gould 1972, Ohno 1970) are cited from general knowledge, marked as such; every estate
number above is reproducible from the banked JSON.
