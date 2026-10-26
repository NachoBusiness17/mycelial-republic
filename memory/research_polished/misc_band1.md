# misc band 1 — polished (first third of cluster "misc", 19/58 packs)

Wave: 2026-09-20 burn. Slice = first 19 of 58 misc packs, alphabetical by path string.
Source packs: `memory/research_packs/`. Register: `memory/runs/mickey17/digest_rp_*.jsonl`.
Sub-threads: **L1 lattice-dig chain** (12) · **L2 SSI process-contracts + blast-focus** (5) · **L3 local-agent landscape & puppeteering** (3 incl. ollama footnote).

## Header table — slice inventory

| Pack (memory/research_packs/) | Register status | Sub-thread |
|---|---|---|
| 20260807T201436Z_pupeteer-dfhack-the-boundary.md | LIVE | L3 |
| 20260807T_hermes-agent-frameworks-comparative-research.md | OWED | L3 |
| 20260720T155500Z_what-is-the-ollama-project-homepage-prom.answer.local.md | DONE | L3 (footnote) |
| 20260729T134821Z_lattice-layer-five-step.answer.local.md | DONE | L1 |
| 20260729T134938Z_lattice-url-3.answer.local.md | DONE | L1 |
| 20260729T135051Z_lattice-url-4.answer.local.md | DONE | L1 |
| 20260729T135201Z_lattice-url-6.answer.local.md | OWED | L1 |
| 20260729T135209Z_lattice-url-7.answer.local.md | DONE | L1 |
| 20260729T135226Z_lattice-url-8.answer.local.md | DONE | L1 |
| 20260729T135257Z_lattice-url-9.answer.local.md | STALE | L1 |
| 20260729T135324Z_lattice-url-10.answer.local.md | DONE | L1 |
| 20260729T135359Z_lattice-url-13.answer.local.md | DONE | L1 |
| 20260729T135427Z_lattice-url-14.answer.local.md | DONE | L1 |
| 20260729T135504Z_lattice-url-15.answer.local.md | OWED | L1 |
| 20260731T161032Z_deep-c-2fcab987a80f.answer.local.md | STALE (dup) | L2 |
| 20260731T161530Z_blast-focus.answer.local.md | STALE (no sources) | L2 |
| 20260731T162755Z_deep-c-2fcab987a80f.answer.local.md | DONE (steal landed) | L2 |
| 20260731T163254Z_blast-focus.answer.local.md | STALE (dup, no sources) | L2 |
| 20260731T164729Z_deep-c-2fcab987a80f.answer.local.md | STALE (dup) | L2 |

---

## L1 · The lattice dig chain — a self-indicting conspiracy-test instrument (12 packs)

**Essence.** The "Sovereign Mirror conspiracy test lattice" ran cycles 2–15 (2026-07-29) on the question *how capture hides in plain sight*, holding official/dissent/material frames over McMartin, Finders, Franklin, Dutroux, Epstein. Its substantive output is one unverified narrative template — the **five-step containment loop** (retail exposure → absurdity amplification → shield phrase → seal the leverage files → public self-applies the kill-phrase) — while its *durable* output is a catalogue of its own pipeline failures: fabricated citations, a never-passed LAW gate, off-question drift, and a broken Verkle chain. The chain is worth more as a validator test corpus than as research.

**Merged findings, with receipts.**
- Recurrence ≠ conspiracy, stated in-pack: cycle 2 concedes each case's own documented failures can explain the pattern without unified conspiracy; its fidelity card failed the LAW check 1/4 (`20260729T134821Z`, ratio 0.25).
- Fabricated/wrong citations, confirmed in code: `parlament.com` is flagged in `mag/lattice_loop.py:319` — "not Belgian parliament; invent host in bag"; `franklinreport.com` disproved at cycle 5. The Dutroux *official* frame was never grounded — url-6's fetch failed ("Source URL: N/A") and the offered replacement was the invented host (`20260729T135201Z`). Cycle 8's six "primary sources" are sequentially-numbered DocumentCloud IDs 3729416–3729421 that pattern-match templated links (`20260729T135226Z`).
- The frame-neutral core (url-7, Epstein): flight logs, properties, Maxwell conviction, Acosta-era NPA, redacted DOJ releases are material record on which official and dissent frames *diverge in interpretation*; the dissent-confirming primary docs were never obtained (`20260729T135209Z`).
- Gate never passed, then the chain drifted: cycles 2–10 all scored ≤0.5 with recommend `elevate_or_retry`; the retry never happened (url-9 wrote filler on a mythology article that "does not address the question"). Cycles 13–15 scored 4/5 "hold" — but on generic CIA/Nixon/secrecy history, not the capture question (`20260729T135359Z`, `…135427Z`, `…135504Z`).
- Verkle chain defects, all reproducible from pack headers: url-13 has `parent_root=None` yet the chain-extension check passed ok:true; url-14's bead has `leaf_hash == parent_root == verkle_root` (all `d6e06…`, seq 2) so the bead commits no new content; url-15's header `parent_root=f47cf1…` contradicts its bead `parent_root=d6e06…`.
- Chain holes: url-11 raw dig exists with no answer .md, url-12 absent, url-16 dig exists unanswered (register rows for url-10/15).

**Verified vs owed.**
- Verified now: `mag/lattice_loop.py:319` parlament.com fabrication flag; all fidelity scorecards read in-pack; hash equalities in url-14/15 read in-pack; chain holes per register.
- Owed: fate of the chain undecided (retire vs re-run with gates); fabricated URLs still in the citation set; Dutroux official frame ungrounded (real primary: Belgian House of Representatives Onderzoekscommissie Dutroux report); DocumentCloud IDs 3729416–3729421 never resolved; no chain-consistency validator exists.

**Three next actions.**
1. Decide the chain's fate: formally retire the lattice dig (0/13 answered cycles ever passed LAW) or re-run with the gate enforced — carry the five-step loop only as a labeled narrative template, never as fact.
2. Before any reuse: purge `parlament.com` and `franklinreport.com` from the citation set, and either ground the Dutroux official frame from the real parliamentary report or mark the node ungrounded.
3. Turn the three hash defects into a chain-consistency validator (reject `parent_root=None`; reject `leaf_hash == parent_root`; header-vs-bead root match) — url-15 is a ready-made regression test — plus a fail-fast rule aborting any bead whose source admits non-address (url-9's lesson).

---

## L2 · SSI/Ilya process contracts, twice-duplicated, plus a sourceless blast-focus pair (5 packs)

**Essence.** Three `deep-c-2fcab987a80f` worker runs (2026-07-31, same session) digest the local `20260728_ssi_ilya_dig/REPORT.md` into portable process contracts; two are near-duplicates of the one that landed. Two `blast-focus` runs do structural analysis of the "Lattice Loop" metadata stack with **zero sources supplied** — method only, no grounded content — and the second adds nothing over the first.

**Merged findings, with receipts.**
- Core claim set (all sourced "Dig 1, Claim N" → `memory/research_packs/20260728_ssi_ilya_dig/REPORT.md`): bottleneck is unreliable generalization / sample efficiency, not data or cluster size (Claim 4); scaling-only progress is ending (Claim 3); target is a "superintelligent 15-year-old" learner, not a finished encyclopedia (Claim 7).
- Steals: mid-trajectory critic — "emotions ≈ value function," short-circuit bad paths without finishing 10k-step rollouts (Claim 6); skill beads / `FIND→FILE→LOAD` as the merge surface instead of weight merges (Claim 8); jagged-failure-mode self-tests, not just the mean (Claim 1). Refusals: any "SSI reverse-engineer" naming a specific network/loss is story, not shipped; the undisclosed "missing ML principle" stays external (Claim 5).
- Landed steal (verified now): `ijl_core.py:17` `SCHEMA = "mag_skill_bead.v1"`, `ijl_core.py:183` `write_skill_bead`; `memory/improve/pins/skills/` populated (register row for `20260731T162755Z`).
- Duplicate tax: `20260731T161032Z` (first digest, no URLs, cites only "Dig 1") and `20260731T164729Z` (18 min after 162755, near-duplicate + jagged-testing delta) both STALE per register; blast-focus `20260731T163254Z` repeats `20260731T161530Z`'s identical zero-source condition ("SYSTEM ALERT: Source Material Empty" / "SOURCES is empty" in-pack) and is marked duplicate.
- Blast-focus salvage: one reusable method note — metadata triangulation across disparate stack layers to expose the linkage template ("Rhyme is not identity"), treating absence-of-evidence as a pattern — and one honest exit: ground a single stack claim (e.g. one date/name from `layer_ms13_claim`) against outside public records before any further lattice digging.

**Verified vs owed.**
- Verified now: `ijl_core.py` skill-bead implementation; source REPORT exists (register); both blast-focus packs self-admit empty sources (read in-pack).
- Owed: doc-level deltas never executed — `memory/improve/evals/features/p0-sector-plansearch-gcrm-2026-07-28.md` exists (register's "no evals/ tree" refers to top-level `evals/`, absent) but grep shows no "Jagged" section, no "Residual Skill Integration Protocol", zero `[CONTRACT]` sections; no mid-trajectory critic wired into any live loop beyond the aimbot's post-hoc `learn()`; blast-focus grounding move never done.

**Three next actions.**
1. Execute the owed doc delta once, on the real path: add a "Jagged Failure Mode Testing" section (three concrete multi-step tasks that induce known failure modes + success-check criteria) to `memory/improve/evals/features/p0-sector-plansearch-gcrm-2026-07-28.md`.
2. Do not re-run blast-focus on the lattice stack without sources; first perform its own prescribed move — cross-reference one verifiable stack datum against outside public records.
3. Add a pre-fire dedup guard for dig workers (content-hash of source bundle / delta-vs-prior-answer check): 3 of 5 packs in this sub-thread were duplicates burning a local model for zero new grounding.

---

## L3 · Local-agent landscape and puppeteering the small model (3 packs: hermes survey, pupeteer direction, ollama footnote)

**Essence.** Two 2026-08-07 packs stake MAG's external position and its internal exploit discipline. The Hermes-frameworks survey maps the whole agent-framework landscape onto one universal SENSE-DECIDE-ACT-OBSERVE-LEARN loop and locates MAG's moat in verkle-chain memory + ghost experiments; the pupeteer pack inverts the problem — a 2B–3B Ollama model is a bounded dwarf, and DFHack-style world-editing (not prompting) converts its dumb defaults into correct behavior. The tiny ollama pack is the substrate footnote: local = easy open-model building, optional cloud, offline privacy — vendor self-description only.

**Merged findings, with receipts.**
- Survey's deep structure: Hermes trades sovereignty for convenience, CrewAI depth for breadth, MAF simplicity for enterprise guarantees, LangGraph opinionation for flexibility, MAG ecosystem for sovereignty; "the files don't go into maintenance mode" (AutoGen's maintenance-mode → MAF succession is the cautionary tale). Enduring moat claim: verkle chain + ghost = the only framework that asks "did our intervention work?" and proves it cryptographically (`20260807T_hermes…` §9–11).
- Top steals named: H1 skills auto-creation (5+ consumed deploys across 3+ contexts → promote), H2 proactive memory/synthesis nudge, C4 `or_`/`and_` multi-condition ghost MATCH triggers, M1 middleware pipeline (dedup → rate_limit → constitution_check) around deploy.
- Pupeteer's six exploitable boundaries: B1 single-shot horizon → job_floor one-step designation; B2 bounded context → inbox breadcrumbs; B3 reward blindness → pro-library `learn()`; B4 no stuck-self-model → spec_gate + false-success guard; B5 instruction authority → operator-guidance outranks drift; B6 meta-awareness gap → silent compliance. DFHack law: *trust bytes, not reports* (`20260807T201436Z` §1–2).
- Proven in gauntlet (qwen2.5:3b, `memory/runs/pupeteer/20260807T202058Z/REPORT.md`): +1.00 flips on G1/G2/G3/G5, 0 meta-tokens; two honest limits in-pack — silence is unconditional but flipping is not (strong-prior targets flaky → "silent but not omnipotent") and G4 aimbot's value is variance-elimination, not new capability.
- Verified now (beyond register): `tools/pupeteer_gauntlet.py`, `tests/test_pupeteering.py`, five run dirs under `memory/runs/pupeteer/`; P1 auto-aim LANDED — `mag/agent_cli.py:2200` `_auto_aim` → `pro_library.aim_once(fire_moves=True)` at :2219. Ghost side: `mag/ghost.py:2812` `catalog()` keeps PIPE-2 auto-promote (3+ deploys, all consumed) but grep finds no synthesis nudge and no `or_`/`and_` triggers anywhere in `mag/ghost.py`.
- Ollama footnote (`20260720T155500Z`): homepage promise = "easiest way to build with open models," optional cloud scaling, offline privacy; single source (ollama.com), no independent falsifier — context for the local-first bet, not evidence of anything.

**Verified vs owed.**
- Verified now: pupeteer gauntlet artifacts + auto-aim wiring; hermes P0 steals absent from `mag/ghost.py` (H1 cross-context promotion, H2 nudge, C4 multi-condition all NOT landed); blast of the survey's moat columns is assertion, not measurement.
- Owed: H1/H2/C4/M1 steals; survey star counts (Hermes 227k, MetaGPT 69.7k) unverified and flagged by the register as inflated — must be re-verified before any external citation; pupeteer P1 leftovers (dashboard table rig — the `dashboard/rest.py` "puppet" surface is the partner rig, not this; `main.py pupeteer` subcommand — grep absent) and all P2 strange experiments (persona stitching, adversarial self-critique, hive steering, boundary stress battery).

**Three next actions.**
1. Land C4 first: `or_`/`and_` multi-condition MATCH triggers in `mag/ghost.py` (lowest effort of the survey steals, register-rated Low) — e.g. deploy when (FKB high AND spider blind) OR (verkle stale AND training ready).
2. Re-verify the survey's star/fork counts against live GitHub before the pack is cited anywhere outside the repo; treat the framework matrices as hypotheses until then.
3. Close the pupeteer P1 gap (`main.py pupeteer` subcommand mirroring the gauntlet; wire the gauntlet into the dashboard as a probe-per-row rig) and queue one P2 experiment — the boundary stress battery (how many injected directives before the model notices) is the natural continuation of the proven B6 finding.

---

*Polished 2026-09-20 from 19 misc-cluster packs (first alphabetical third). No content beyond packs + register rows + repo spot-checks cited inline.*
