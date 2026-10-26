# STEAL: Google Research Harness² mapped onto Mag's existing organs (2026-10-17)

Classification: CARD (read-only study + smallest-build proposal). No Mag code was changed.
Producer: Grok Bot executor, 2026-10-17, about 19:05-19:45 ET (UTC-4).
Method: Harness² was cloned and run on the Grok Bot box (`/workspace/steal/harness2`, shallow clone of
https://github.com/google-research/harness2). The paper (arXiv 2610.14224) was fetched and read.
Mag was read on DESKTOP-7C70KSC with Get-Content, Read and rg only. No git commands. No .env, key files,
secret_gate_results/, free_keys/ or memory/trajectory/steps.jsonl were opened. No model or paid API calls.
No processes or containers were touched. The only writes on the PC were this file and one appended line
in watch/LIBRARY/INDEX.md.

Line numbers below are the ones I saw on 2026-10-17. Harness² paths are relative to the repo root.

---

## 1. What Harness² does, in plain English

The model stays frozen. Harness² changes only the files around it, which the paper splits into 8
components: system prompt, guardrails, memory, tool guidance, skills, scripts, subagents and plugins
(`harness2/substrate/opencode.py:42-63` names the OpenCode file for each one; paper Table 5).

For each new task it does the following:

1. **Reference runs.** It runs the current harness k times on the task. Those runs show how the harness
   behaves, not whether the answer is right.
2. **Propose.** Two editors read those runs and edit copies of the harness files. The INV editor fixes how
   the agent works (procedure, tools, finishing); see `harness2/core/prompts.py:347-370`. The DOM editor
   adds what a practitioner in that field knows; see `prompts.py:372-407`. Every edit has to point to a
   specific moment in a run. "KEEP_BASE" counts as a valid answer (`prompts.py:333-335`).
3. **Probe.** Each candidate harness runs once on the same task with the same model.
4. **Compose.** A composer reads the base runs, the candidates, their diffs and their runs. It then merges
   the edits the runs support, adopts one candidate whole, or keeps the base
   (`harness2/core/recursion.py:404-449` for parallel, `:452-566` for sequential). There is no answer key.
   The only evidence is the difference in behavior between runs. Agreement between candidates counts as
   support, not proof.
5. **Select.** When k>1, a selector compares the final outputs with their labels hidden and picks one
   (`harness2/core/selection.py:71-77` assign_ids, `:268-357` run_selection).
6. **Reflect.** A reflector reads the whole record and writes a lesson with cue, lesson, evidence and
   confidence fields. No lesson is stored unless all three of cue, lesson and evidence are filled
   (`selection.py:454-505`, and the check at `:500`).
7. **Library (the "improvement harness").** The adopted harness tree and its EXPERIENCE.md go into a
   per-domain library with an INDEX.md. The next task's editors read that library
   (`harness2/core/library.py:15-24` layout, `:106-152` add, `:154-181` rebuild_index).

Budget per task and mode is fixed at 4k executor runs and 3k editor sessions
(`harness2/core/ledger.py:26-33`). An invalid edit gets one retry and then falls back to the current
harness (`recursion.py:36`, `:135-251`). A tripwire refuses to put any grader output into an editor's
context (`harness2/core/context.py:419-518`).

Paper results: one step improves both GLM-5 and Gemini 3.5 Flash. The gains are up to +11.5 on
WorkBuddy-Bench, +4.5 on JobBench and +11.8 pp on LAB Partial. In the ablation, removing the library, the
INV/DOM split, or composition each costs 1.6 to 3.7 points (paper Table 3). Using the same model as both
editor and executor still helps; GLM-5 gains 13.7 on LAB (paper Fig. 8). The default editor in the main
tables was Claude Opus 4.8.

## 2. Demo result (box, no credentials)

`uv venv --python 3.12 .venv; uv pip install -e '.[render]'; harness2-demo --output /workspace/steal/harness2/runs/demo --k 2`

- Output line: `Local demo: 2 tasks completed; 0 failed.` Exit 0.
- `demo.json`: done=2, failed=0, execution_count=28, editor_calls=32. That is 2 tasks x 2 modes x
  (4k=8 runs) = 32 runs, minus 4 base runs that the two modes share. Editor calls are 2 x 2 x (3k=6 stages
  + 1 select + 1 reflect) = 32.
- Library: `runs/demo/library/k2/agg/accounting/INDEX.md` and `.../harnesses/ledger-1/EXPERIENCE.md`.
  The cue was "When a ledger includes credits and debits". The edit was "dropped the positive-only filter".
  The verdict was "helped".
- The second task started with 1 library entry per mode (`library_entries_before: {agg: 1, seq: 1}`), so
  the cross-task loop ran.
- The repo's own tests: `python -m unittest discover -s tests`: 5 tests OK.
- **Caveat:** the demo's editor and selector are scripted. The demo selector computes the true ledger
  total from the source file (`harness2/demo.py:120-135`). The demo therefore proves the plumbing and file
  formats. It does not prove that selection works without ground truth.

## 3. Component map: Harness² role -> existing Mag organ

| Harness² piece | Mag file / organ that already plays it | Status |
|---|---|---|
| Executor (OpenCode + GLM) | Daily mates: `scripts/register_leave_task.ps1:37,60` registers `MagLeaveProtocolDaily` at 08:00. `tools/leave_dispatcher.py:60-70` has the constant RUNNER_ARGV, DEFAULT_PARALLEL=8 and MAX_PARALLEL=16, with width clamped at `:210`. `scripts/run_mate.ps1:151` runs `opencode run -m zai/glm-4.7` (z.ai coding plan, pin explained at `:143-150`). Each run gets its own opencode data dir (`run_mate.ps1:113-120`). | **Have.** This is the same executor family as the paper (OpenCode + GLM). |
| Task / evidence | Mission packs in `logs/mates/missions/` (`leave_dispatcher.py:51`, template at `:72`). Receipts with a JOURNEY section in `watch/inbox/mates_leave_protocol/receipts/` (`:52`; journey law in `configs/mates.yaml:13-14`). | **Have.** JOURNEY works as a compact trajectory. |
| 1 System prompt | `mag/invariant.py:74-89` stable_prefix (state/SESSION_SEED.md + formatting block). `mag/warm_surface.py:297-344` per-seat preamble. `mag/context_pack.py:2091` format_agent_preamble. | Have |
| 2 Guardrails | `mag/rib_boot.py:177-187` CORE_LAWS. Law ribs listed in `rib_boot.py:90-101` (VAULT_RIBS). Served read-only at `mag://warm/laws` (`warm_surface.py:218-245`). Mates' own laws are in `configs/mates.yaml:8-31`. | Have |
| 3 Memory | `memory/warm_state.json`, `memory/zknot/LATEST.md` and the live tip, served by `warm_surface.py:51-55,168-215`. The failure KB is at `mag/failure_kb.py` (log `logs/failure_kb.jsonl`). | Have |
| 4 Tool guidance | The MCP tool list and descriptions in `mag/mcp_server.py:139-216`. `TOOLS.md` exists at the repo root (not opened). | Have (partial) |
| 5 Subagents | Mate personas in `configs/mates.yaml:33+` (cartographer, locksmith, ...). The seats themselves. | Have |
| 6 Skills | `.agents/skills/<name>/SKILL.md` (31 dirs, e.g. agent-harness, operator-corrections). The one-turn ephemeral skill gate is in `mag/skill_lifecycle.py:15-23`. | Have |
| 7 Scripts | `scripts/`, `tools/` | Have |
| 8 Plugins (in-loop enforcement) | `mag/leases.py:420` guard(). `mag/fleet_report.py:155` check_body, which the receipt writer runs, so a bad body is refused. The argv law in `leave_dispatcher.py:3-18`. | Have (as code-is-law hooks, not per-run plugins) |
| Harness editor, INV/DOM split | Closest: `mag/failure_kb.py:325` auto_draft_remedy (a deterministic remedy card when a failure repeats). Any seat can file a diff through `mag/proposals.py:348` tool_propose. Nothing reads mate runs and writes a scoped harness edit. | **GAP** |
| Probe (same task, base vs candidate) | Closest precedent: `mag/rotation_harness.py:1-14` (same input, different seat, check that structure holds). The dispatcher runs each mate once on its own mission, with no paired A/B. | **GAP** |
| Composer (evidence-based merge) | `mag/proposals.py:270-305` tally is a vote (approvals >= quorum 2, author excluded, operator override/reject). It is not a merge built from behavioral contrast. `mag/quorum_window.py:11-16` has a mechanical fold and self-vote exclusion. | **GAP** (the adopt gate exists, the compose step does not) |
| Anonymous final selection | No A/B blinding organ. `mag/consensus_gate.py:1-25` already encodes the paper's warning that correlated samples agreeing is not proof. | Partial |
| Adopt gate | `proposals.py` quorum 2 plus a promotion marker written only when ready (`:253-256`). Nothing is applied by code; git stays with the operator (`:29-30`). `invariant.py:193-248` freeze_instructions/check_instructions makes any instruction-layer change a deliberate, labelled epoch. | **Have** |
| Experience reflector | `mag/failure_kb.py:542` recurring_patterns. `mag/skill_ledger.py:94,137` proven_moves/record_decision (case law in `memory/improve/skill_ledger.jsonl`, `:31`). These feed `mag/session_route.py:87-103` learned_block, which `invariant.py:251-268` puts in the volatile tail. Missing: a lesson tied to a specific harness diff and to the contrast that justified it. | Partial |
| Improvement-harness library | `watch/LIBRARY/` (catalog.jsonl cards with family/supersedes/latest/verified, built by `scripts/inbox_librarian.py:1-18`). The rib vault uses amend-never-rewrite (`rib_boot.py:48-54,145-175`). Missing: per-domain "adopted harness tree + EXPERIENCE.md" entries that editors read before proposing. | Partial |
| Budget ledger (4k/3k) | Width cap law (`configs/mates.yaml:9-10`, `leave_dispatcher.py:69`). `mag/cost_ledger.py` exists (not opened). | Partial |
| Fixed shared surface for all seats | `warm_surface.py` fixed `mag://warm/*` URIs, wired in `mcp_server.py:543-555`. | Have (Harness² has no equivalent) |

## 4. Top 3 gaps

1. **No editor.** Nothing turns mate run evidence (JOURNEY receipts) into a scoped harness edit with one
   INV candidate and one DOM candidate.
2. **No paired probe.** Mates never run the same mission twice with only the harness changed, so Mag has
   no behavioral contrast to judge an edit by.
3. **No evidence-backed lesson store tied to adopted edits.** The failure KB and skill ledger record
   failures and routing wins. They do not record "this harness change helped, here is the cue, here is the
   receipt line that shows it."

## 5. Smallest build that closes them (Propose-Probe-Compose over mate missions and law cards)

The idea is to reuse every existing organ and add one small stdlib module plus config rows. The free GLM
mates act as editors and probes. proposals.py plus quorum 2 acts as the compose/adopt gate. The rib vault
amendment convention acts as the library.

**Harness surface in scope (k=1):** the mission-pack template (`tools/leave_dispatcher.py:72` MISSION_TEMPLATE),
one skill under `.agents/skills/`, and one law-card amendment under `memory/rib/RIB_*.md`. The pinned
stable prefix (SESSION_SEED, BRIEF, FROZEN_RIB) is NOT edited by candidates, because editing it breaks the
prompt cache (`invariant.py:7-21`). Candidates ride in the mission pack or the volatile tail. Only an
adopted change reaches the pinned layer, through a labelled `freeze_instructions` epoch.

**Daily flow (all variance in files, so the argv law in `leave_dispatcher.py:3-18` holds):**

1. *Propose.* Two new mate rows in `configs/mates.yaml`, `editor_inv` and `editor_dom`. Their seed thread
   is to read yesterday's receipts in `watch/inbox/mates_leave_protocol/receipts/` and write one candidate
   as a unified diff file, citing receipt:line for every change, or write KEEP_BASE. The INV/DOM prompt
   wording can be taken almost verbatim from `harness2/core/prompts.py:295-407` (Apache-2.0).
2. *Probe.* `leave_dispatcher.write_missions` gets a paired mode. For one chosen mate it writes
   `mission_<date>_<nn>_<mate>__A.md` (base) and `__B.md` (base plus a "HARNESS DELTA" section holding the
   candidate). The packs are byte-identical apart from that section. run_mate.ps1 is unchanged; it just
   claims the next pack. With width 8 of a 16 cap, k=1 adds 2 editors + 2 probes + 1 composer = 5 runs, so
   13 of 16 in total, under the law.
3. *Compose.* A `composer` mate row reads the A and B receipts. A/B labels are shuffled with a seed, using
   the same method as `harness2/core/selection.py:71-77`. It writes a verdict file: merge, adopt, or
   KEEP_BASE, each with receipt:line evidence. If its verdict is not KEEP_BASE, a host-side wrapper files
   it through `proposals.submit` as a signed proposal (targets = the harness files, patch_path = the diff
   file).
4. *Adopt.* Use the existing `proposals.tally` unchanged: quorum 2, distinct seats, author excluded,
   operator override/reject. Add a policy note: at least one approving seat must be a non-GLM model,
   following the correlated-unanimity law in `mag/consensus_gate.py:1-25`. The operator's git window applies
   the patch. Then `python -m mag.invariant freeze-instructions --label <proposal_id>` if the
   instruction layer was touched.
5. *Reflect.* After promotion, write one experience block as a dated AMENDMENT section on the relevant
   law rib (amend-never-rewrite, already mounted by `rib_boot.py:145-175` and served at `mag://warm/laws`).
   Fields: cue, lesson, evidence (receipt:line for A and B), confidence, proposal_id. Refuse to write it if
   cue, lesson or evidence is empty, as `harness2/core/library.py:43-47` does. The editors read it the next
   morning through the preamble. That closes the second loop with no new store.

**Files:**

- `mag/harness_probe.py` (new, about 200 lines, stdlib): pair-pack builder, seeded A/B blinding, verdict
  parser, experience-block writer. It ports `library.has_experience`, `selection.assign_ids` and the
  `<experience>` parser from Harness², with Apache headers kept.
- `tools/leave_dispatcher.py`: a paired-mode branch in write_missions (files only, no argv change).
- `configs/mates.yaml`: rows for editor_inv, editor_dom and composer.
- No change to `mag/proposals.py`, `mag/warm_surface.py`, `mag/rib_boot.py` or `mag/invariant.py`; they are
  used as they are.

**Tests that would prove it (none need a model; they use a fake runner like harness2-demo):**

- `tests/test_proposals.py` (missing today; I found no test file for proposals.py): quorum 2 counts distinct
  seats, the author is excluded, a duplicate vote counts once, an operator reject blocks, and promotion is
  refused before ready.
- `tests/test_harness_probe.py`:
  - The A and B packs differ only inside the HARNESS DELTA block (byte diff).
  - Paired mode never pushes width past `MAX_PARALLEL` (16).
  - A/B blinding is stable across reruns and differs across tasks.
  - The experience writer refuses a block that is missing cue, lesson or evidence.
  - A composer verdict with no receipt:line citation produces no proposal.
  - A KEEP_BASE verdict files nothing.
  - An end-to-end fake-runner demo (2 missions, scripted editor) produces one proposal and one
    amendment block. This is Mag's own version of `harness2-demo`.
- Regression: `tests/test_leave_dispatcher_exit_contract.py`, `tests/test_invariant.py`,
  `tests/test_rib_boot_amendments.py` and `tests/test_fleet_coordination.py` still pass.
- Live check (operator GO only): one paired day. Show the A/B receipts, the proposal folder under
  `watch/receipts/proposals/`, and the tally output.

## 6. Risks and costs

- **Weak contrast on open-ended missions.** The paper's tasks have a deliverable. Mates hunt open threads,
  so two runs can differ for reasons unrelated to the harness. Single-run probes are noisy (paper App. E.6:
  the selector picked a 55 over a 95). Mitigation: start with a mate whose seed thread has a checkable
  output, and treat one day as one sample.
- **Correlated judges.** GLM editor, GLM probe and GLM composer share biases. proposals.py counts distinct
  seats, not distinct model families. Hence the non-GLM approver rule above.
- **Signing.** Proposals must be Ed25519-signed by an allowlisted seat (`proposals.py:5-6,233-237`).
  Giving the GLM mates a key widens trust. A host-side wrapper that signs as one "mates" seat after
  deterministic checks is safer. Either way, this is an operator decision.
- **Cache cost.** Any edit to the pinned prefix or instruction layer is a full cache miss fleet-wide
  (`invariant.py:3-21`). Keep candidates in the pack or tail, and adopt into the prefix only at labelled
  epochs.
- **Compute.** GLM is flat-rate, so the cost is concurrency and wall time, not dollars. Rollouts per
  candidate double, and the Harness² identity is 4k runs + 3k sessions per task (`ledger.py:26-33`). k=1
  fits under the 16 cap. k>=3 would not, unless admission is staggered (`configs/mates.yaml:9-10`).
- **Mates rate.** A RAM gate already applies (`configs/mates.yaml:25-28`). Paired mode adds about 5 opencode
  processes.
- **INDEX.md gets regenerated.** `scripts/inbox_librarian.py` rewrites INDEX.md on its next run, so the
  one-line link appended today may disappear. The durable link is a catalog card; run
  `python scripts\inbox_librarian.py --no-model` to card this file.
- **Things not to import from Harness².** It runs executors with unrestricted network, and Codex with its
  sandbox off (README "Web access"; docs/EXPERIMENTS.md). Its benchmark setup needs a .env with Vertex
  credentials. Mag needs neither.

## 7. Directly reusable under Apache 2.0

Harness² is Apache-2.0 (`LICENSE`, `pyproject.toml` license field). Each file carries a "Copyright 2026
Google LLC" header. To reuse: keep the header, include the LICENSE, and mark modified files (Apache 2.0
section 4). The repo has no NOTICE file to carry.

Worth lifting:
- `harness2/core/library.py` (222 lines): the adopted-tree + EXPERIENCE.md + INDEX.md library format.
- `harness2/core/selection.py`: `assign_ids` (seeded anonymization, `:71-87`), the `<experience>` and
  `<edits>` parsers, and the "cue+lesson+evidence or nothing" rule (`:454-505`).
- `harness2/core/prompts.py`: the INV and DOM editor sections (`:347-407`), the GENERALIZE grounding text
  (`:295-330`), KEEP_BASE (`:333-335`), and the composer, selector and reflector builders (`:893`, `:964`,
  `:1040`, `:1105`). These are the most valuable part, and they are prompts, so they port to any executor.
- `harness2/core/tree.py`: the validator (`validate`, `:336`). Every skill needs a trigger line, every
  named script must ship, scripts must compile, and the always-on budget is capped at 24,000 chars
  (`substrate/opencode.py:50`). Mag's `.agents/skills/` could use the same lint.
- `harness2/core/context.py:399-518`: the leak-path and verdict tripwire pattern (a context directory is
  refused, not trimmed).
- `harness2/core/ledger.py`: the budget-identity assertion.
- `harness2/demo.py` + `cli/demo.py`: the pattern of a deterministic local adapter for testing the loop
  with no model.

Not reusable as-is: everything under `third_party/` keeps its upstream license. The WorkBuddy runner
files carry Tencent's custom license with a territorial limitation (docs/BENCHMARKS.md). The benchmark
adapters (`harness2/benchmarks/`) and the Vertex/Codex bridge are not relevant to Mag.

## 8. One-line verdict

Mag already has Harness²'s executor (OpenCode + GLM mates), all 8 harness components, an adopt gate
(proposals quorum 2 plus instruction-epoch pins) and an amend-only law library. It lacks the editor,
the paired probe and the evidence-tied lesson. Those three fit in one stdlib module, a paired-pack mode
in the dispatcher and three mate rows.
