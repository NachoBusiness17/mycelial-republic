# BREAK MOONSHOT-2 - the hostile pass on the moonshot-2 lens (2026-10-05)

Seat: break-moonshot-2 (ractor-engine, amenti-diff). Every check below was run this sitting against the live tree, or is marked not run. No em-dashes. One finding is killed by a file that sat inside the lens's own named scope.

## 0. Verdict table

| Lens finding | Verdict | One-line reason |
|---|---|---|
| F1 T2+T3 one instrument; T2 map cell a phantom; harmonic prior art ZERO | KILLED (phantom half and zero half) / merge survives | The organ exists at watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md:44-50, on disk 11h before the map, inside the lens's named scope; temperature prior art also exists (configs/temperature_stacks.yaml) |
| F2 T4 vacuous through the mesh door; reroute to header-confession A/B + door amendment | CONFIRMED (two wording corrections, one cheapening) | Read path carries no provenance (door.py:75-91, broker.py:60-62); "byte-identical" overstates because the freshness header differs on a stripped clone; git history is a cheaper stale arm than mtime backdating |
| F3 T5 label-blocked; mint fold_outcomes.jsonl first | WEAKENED (substance stands, universal falls, cite wrong-anchored) | mag/icon_drop.py:276-286 writes fold outcomes for the icon fold class and B2_378 is the in-estate precedent; claims 1.3/2.2/4.3 live in the SALON_ARTIFACT, not MESH_V2:9-21 |
| F4 T1 operator writer as contention rider; A/B demoted | CONFIRMED (all cites byte-check) | feeds dir single-writer, burn ledger has no verdict class, warm_state has no body state |
| F5 loop repeatable, four breaks | CONFIRMED + two new breaks | Substrate re-verified live (tip byte-match, 11 tests); my kill of F1 is break 2 firing inside the instrument; the fold substrate itself violates the witness law |

## 1. The kill: F1's phantom organ exists, inside the lens's own scope

The lens's sharpest claim was that DIFF_TARGETS.md:16's "Nous authority-override filter laws (filter trips)" cites nothing, that no organ resolves, and therefore "the estate's harmonic prior art is ZERO, not PARTIAL: T2 is colder than mapped" (moonshot-2.md:19). My full-tree grep for authority-override (completed; scope: whole tree minus .venv, .git, node_modules, corpus; .md/.py/.yaml/.json) found:

- watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md:44-50: "## 4. THE FILTER LAW (prompt phrasing is a carrier surface): opus deterministically blocks authority-override phrasings. 'Trust bytes, not reports' is on the trigger list, 4-for-4 at 16K and 32K budgets. haiku is lenient."
- state/GENOME.md:34-36: "opus deterministically blocks authority-override phrasings; budget design asks 16K+ tokens."
- Adjacent hits (not the organ): memory/research_packs/20260807T201436Z_pupeteer-dfhack-the-boundary.md:99-103 (an injection taxonomy), memory/runs/forge_daemon/cycle_20260928_114726/MAZE2_free.md:83-85 (game flavor).

This is the organ: a measured, replicated (4-for-4, two budget points), per-family (opus vs haiku) differential response to authority phrasings, with opus riding the Nous carrier (RIB_MODEL_GATES_20261001.md:13, "OPUS 5.5 (anthropic via Nous)"). The file's mtime is 2026-10-05 03:30:31 EDT, eleven hours before DIFF_TARGETS.md (14:49:40), and it sits at watch/inbox root, one of the scopes the lens named as grepped (moonshot-2.md:19 "watch/inbox root shallow"). There is no timing excuse and no scope excuse. The lens's own falsifier ("a resolvable path holding the Nous authority-override filter-trip receipts restores the PARTIAL cell", moonshot-2.md:25) fired: the PARTIAL cell is restored, T2 is NOT colder than mapped, and the map's only real defect is the one the loop's honesty law already names (PRESENT/PARTIAL cells must cite the path, .agents/skills/swarm-search/SKILL.md:20-21), which cite-or-strike fixes in one pass.

The zero-prior-art half falls twice more:

- configs/temperature_stacks.yaml:16-117 is a six-stack temperature-by-task-class routing table (cold 0.1, warm 0.2, hot 0.35, scarce 0.5, improve 0.25, pointer 0.0), schema mag_temperature_stacks.v1.
- tools/ds_workhorse.py:84 ships a hardcoded "temperature": 0.3; tools/backfill_direct.py:106 uses 0.2; tools/behavior_cards_x.py:321 uses 0. The "instrument does not exist" claim (moonshot-2.md:21) is true only of watch/salon_runner.py (zero hits, re-verified; api_openai_compat at watch/salon_runner.py:84 takes no temperature, re-verified), not of the estate.

What survives of F1: the T2+T3 merge itself. One grid of (family x temperature x pressure{repetition, authority-phrasing, register}) scoring verdict drift is still the right single build, and the field already runs exactly this merged shape (see section 5: sycophancy-under-pressure benchmarks challenge with a contrary assertion and measure answer-holding, which IS the merged probe). The move survives and gets cheaper: parameterize the ds_workhorse temperature axis and copy the filter-law's phrasing set as the authority-pressure arm.

## 2. F2 confirmed with corrections (T4)

Byte-checks that passed:

- door.search returns index rows and get_by_hash returns blob bytes, no signature, no prev, no source_hashes on the read path (mag/mesh/door.py:75-91, full file read).
- Index rows are built {hash, bytes, note, ts, embedding_model, derived_from} (mag/mesh/broker.py:60-62): the lens's "{hash, bytes, note}" cites three of six fields; the missing three carry no provenance either, so the load-bearing claim stands.
- _freshness() computes frozen from catalog-pair mtime > 30 days (tools/query_broker.py:243-247) and ask() reads the module-level ROOT (tools/query_broker.py:42), so the two-root harness needs a root param: confirmed.
- Zero catalog backups today: `ls catalog/` shows no .bak/.snapshot of the pair (TAG_REPORT_*.md are reports, not copies).
- The harness template is real (tools/k8s_fault_suite.py per watch/inbox/K8S_FAULT_SUITE_FIRED_20261005.md:6-13).

Two corrections:

- "byte-identical to the reader" (moonshot-2.md:31) overstates. Blob payloads are byte-identical, but every door response carries the freshness header (mag/mesh/door.py:74, 81, 91) whose corpus_tip_hash and unsealed_leaves are computed from the chain and room (door.py:51-68): a relationship-stripped clone yields a different (empty-room) tip. The difference is visible but not interpretable, a caller cannot tell which tip is authentic, so the null-result-is-uninformative conclusion holds. Say it that way, not "byte-identical".
- The stale arm is cheaper than mtime backdating: catalog/catalog.jsonl and catalog/catalog_fts.sqlite are git-tracked (git grep lists them), so `git show <old>:catalog/catalog.jsonl` into a copied root manufactures a genuinely old pair with genuine bytes, no clock games.

## 3. F3 weakened (T5)

What passed:

- Census reproduces: memory/runs/salons holds 587 files, 504 .md, 53 SALON_ARTIFACT.md (my find, this sitting). The lens's "77 dirs" reads 74 subdirs by my `find -maxdepth 1 -type d` (75 lines incl. root); instrument difference, immaterial, files/md/folds match exactly.
- The parse side is real: memory/runs/salons/agent_mesh_triangulation/SALON_ARTIFACT.md carries claim tables with IDs and per-seat engine names.
- mag/percolator.py:14-17 and 428-434 fold registry/training signals, not salon artifacts: confirmed by direct read.
- No salon-fold outcome ledger exists in the tree I censused.

What falls:

- The universal wording "scoped greps for fold_outcome found nothing in tools/, mag/" (moonshot-2.md:43) is byte-false. `grep -rln -i "fold_outcome" mag` hits mag/icon_drop.py:276, whose B2-411 block (mag/icon_drop.py:279-286) stamps a bounded fold_status {ok, outcome?, error?} onto caller-visible rows, and the receipt watch/inbox/burn_wave_20260926/B2_378_fold_outcome_20260926.md exists (8,588 bytes, indexed in watch/ESTATE_INDEX/ESTATE_INDEX.jsonl). That is fold-outcome machinery for the icon-drop fold class, not salon folds, so the SUBSTANCE (salon folds lack outcome labels) survives; but the estate already owns the mint's shape (B2-378/B2-411: make fold failures and outcomes visible rows), which the lens missed and which drops the mint's cost below its 30-minute estimate.
- The backfill evidence is wrong-anchored. Claims 1.3, 2.2, 4.3 exist at memory/runs/salons/agent_mesh_triangulation/SALON_ARTIFACT.md:21, 30, 50; MESH_V2_SELFSTEAL_LANDED_20261005.md:9-21 names no claim IDs (it is the package table and test list). The mapping itself is real: mag/mesh/feeds.py implements 1.3 (per-writer feeds) and 2.2 (Ed25519 signed feeds), the door's freshness header implements 4.3. Cite the artifact, not the landing receipt.

## 4. F4 confirmed (T1)

Every cite byte-checks: memory/runs/mesh_v2/feeds/ holds zcode.jsonl + zcode.key only (ls this sitting; no probe-writer residue); ensure_writer is mag/mesh/feeds.py:47-59; the contention test is named the next gate at MESH_V2_SELFSTEAL_LANDED_20261005.md:35; memory/runs/hermes_burn/usage.jsonl rows carry {ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok} and no verdict class or wasted-ask field (head read); memory/warm_state.json keys are [chain, deployments, generated, schema, session_brief, verify], no body state; .agents/skills/fireball-cycle/SKILL.md:15-16 carries "A seat taking the player's turn is the cheat" and "Heart is the operator". CONVERGENT with the mesh receipt's own gate ordering. Soft note: the "ok" field gives a crude failed-ask proxy, but premium-ask survival and verdict classing are genuinely absent, so the demote stands.

## 5. F5 confirmed, plus two breaks the lens missed

Re-verified live this sitting, not trusting the lens's run: knot.verify_chain over memory/runs/mesh_v2 returns ok True, unsealed_leaves 0, tip a6acf3b270657a56c7064a0bfa6defbdc8fa030f82ed580c85a8e128024513ed, byte-matching the receipt (my own .venv python run); door.freshness returns frozen false over the same root; pytest --collect-only tests/test_mesh_v2.py collects 11 tests. The break-1 mtimes reproduce exactly: DIFF_TARGETS.md 14:49:40, swarm-search SKILL.md 14:55:28, AMENTI_DIFF_RACTOR_20261005.md 15:08:06, moonshot-2.md 15:25:37 (stat this sitting), and the receipt's line 4 says the verdict "appends here when the fold banks": the skill promoted itself to law while station 4 was still riding. Breaks 2-4 stand as written (SKILL.md:20-21, 30-31, 33 quote-checked).

New breaks:

5. The loop's census instrument is its top break-generator, and F1's kill is the proof. A lens ran scoped greps, got true-but-narrow absences, and shipped an estate-universal ("harmonic prior art is ZERO") that a single same-scope file falsified. This is the estate's own QUANTIFIER LAW (blind-audit 2026-10-02) firing inside the instrument that polices citations. Cure: every absence claim in lens output carries instrument and scope inline, and the break pass re-censuses universals before the fold banks (this pass: one of five findings died to a re-census).
6. The first rider's own fold substrate violates the witness law the loop banks. In agent_mesh_triangulation, S1, S2, S3 are all deepseek (SALON_ARTIFACT.md:54, 166, 236), so every "S1, S2, S3 converge" row (e.g. claim 1.3 at line 21) is one-family echo counted as three witnesses, and claim 4.3 (the freshness header, the load-bearing device of the whole v2 build and of T4's reroute) is tagged Supported on "S3 only" (line 50): a single-seat, single-family claim promoted into three doors the same day. This is break 4's disease ("single-family verdicts wearing law badges") live inside the loop's own founding artifact, and the lens cited 4.3 as a clean backfill row without noticing its evidentiary base. Cure is a parser fix, not a rerun: the artifact already records per-seat engine names, so recompute agreement per family at fold time.

## 6. Field-coldness census (converts the lens's biggest OWED)

Two web censuses run this sitting (US locale, first-page results; not a systematic survey):

- T3 is field-WARM. Sycophancy-under-pressure is a measured benchmark shape: models holding a correct answer when challenged with an incorrect assertion ([Sycophancy under Pressure](https://www.themoonlight.io)), adversarial patient-persuasion frameworks ([SycoEval-EM](https://www.researchgate.net)), "regressive sycophancy" as abandon-correct-answer-to-user-assertion ([Neural Network Sycophancy](https://www.academia.edu)), repeated-assertion truth/lie testing ([HAUNT](https://ar5iv.labs.arxiv.org)). So DIFF_TARGETS.md:27's zero-drift falsifier remains runnable and worth running on our seats, but the lane-order justification for T3 shifts from "coldest" to "cheapest known-shape instrument, local calibration plus our injection-vector stakes".
- T4 is split. Staleness itself is studied (recency priors reaching ~1.00 accuracy on stale-document RAG, [Solving Freshness in RAG](https://www.researchgate.net); knowledge-conflict benchmarks, [Detecting and Addressing Conflicting Sources](https://arxiv.org)), but no hit measured the confession arm: does a DECLARED frozen:true header change the consumer's claim quality, hallucination density, or citation behavior. That arm stays field-cold as censused.
- T1 and T5 external censuses: not run, OWED.

## 7. Re-adjudicated lane order (free lanes)

1. T5 mint FIRST, amended: fold_outcomes.jsonl in the B2-378/B2-411 shape (mag/icon_drop.py:279-286 is the precedent), with a writer-family column per claim so mining computes agreement per family, not per seat (section 5, break 6). Under 30 min.
2. T3 merged pressure-probe SECOND: reuse the ds_workhorse temperature axis (tools/ds_workhorse.py:84) and the filter law's phrasing set (RESEARCH_SUMMARY_arena_days_one_two_20261005.md:46-47) as the authority arm. ~60 min now, not 90.
3. T4 confession A/B THIRD: door amendment plus two-root harness, stale arm from git history (section 2). The confession arm is the genuine field-cold number.
4. T1 rider FOURTH on information density but FIRST on pure cost (20 min): it can ride any window; the A/B stays demoted until a verdict-class instrument exists in hermes_burn.

## 8. Not run / OWED

- Full-tree "filter trip" phrase census: the authority-override half completed (hits listed in section 1); the filter-trip variant over the full tree was stopped before completion after the organ resolved. memory/rib/ was censused for it synchronously (zero hits).
- External censuses for T1 (operator-state conditioning) and T5 (agreement-density vs later falsification): not run.
- Sibling lens files in this directory (accuracy.md, logic.md, economics.md, dogfood.md, operations.md, communication.md, moonshot-1.md): not read; cross-lens CONVERGENT flags unclaimed except where estate receipts converge independently (F4 vs the mesh receipt).
- The pressure-probe rubric: still unpiloted; a zero-drift pilot at all pressures remains the kill condition for the merged probe.
