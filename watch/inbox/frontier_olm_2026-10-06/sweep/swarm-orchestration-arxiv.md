# Frontier sweep: swarm-orchestration via arxiv (2026-10-06)

source-fetched: 2026-10-06. Doors used: `export.arxiv.org/api/query` Atom feeds (7 search queries) + `arxiv.org/abs/*` pages + one full-HTML read (`arxiv.org/html/2610.04779v1`). No door 403'd. Two `id_list` fetches came back with abridged quotes rather than full verbatim abstracts (the fetcher's quote cap), so banked quotes are the shorter spans it did show; all quotes below are from pages fetched this session.

## Pass 1 census

Seven queries, last-30-days window (submittedDate 202609060000-202610062359): multi-agent+LLM (26 entries), concurrency+agents+cs.MA (12), swarm+LLM (8), planning+LLM agent (30 of 44), serving+agents+cs.DC (25), coding agent (25), knowledge graph+agents+memory (4). About 130 candidate entries considered; strongest 24 shortlisted, every shortlist ID checked against `catalog/catalog.jsonl` by exact ID grep.

## Overlap census (what we already hold)

Already in the estate, therefore NOT re-banked:
- `2609.09153` Procedural Graphs: `catalog/catalog.jsonl:443484` (state/arxiv mirror 2026-09-09).
- `2609.26781` Agensh: `catalog/catalog.jsonl:445335`.
- `2610.05778` MedicalHarness + `2610.06069` Attention Tax/Handoff Tax: `catalog/catalog.jsonl:1071104,1071127` (today's 06:30Z mirror pull).
- `2609.33768` DEALS + `2609.38482` PANDA: full texts banked by the 2026-10-03 sweep (`catalog/catalog.jsonl:1073124,1073128`).
Grep command run: `rg -i -n "<titles+ids>" catalog/catalog.jsonl memory/` in one pass; only other hits were Project Gutenberg corpus noise for "waggle" (`memory/corpus/ractors/weird_prophetic/texts/pg78106.txt:2735`).

## The 8 banked items, mapped to the five research questions

1. **2610.04779 (Concurrent AI coding agents, RQ1 write seams).** The direct hit. On a 715-pair lineage set, 47.3 percent of conflicts (79) occur despite disjoint authored file sets, capping an overlap detector at 52.7 percent recall; a file-list-only LLM baseline recalls 2.5 percent. Root cause is a proxy mismatch: authored diffs are measured per-PR against PR-specific bases while the checker merges against the shared base; 48/79 reconstructed on the common base all became clean. Their contract splits observable scope (O), executable check (V), heuristic score (s), with scores never treated as proof. Scheduling gate: 91.7 percent median de-overlap at 65.0 percent makespan inflation (FIFO full serialization costs 167.3 percent). Their falsifier matches fold_gate exactly: median replay is 0.02 s, so when the checker is cheap you always verify and heuristics only prioritize. General lock/receipt contract candidate for our seams.
2. **2610.01160 Retire (RQ1 serializer + RQ4 resets).** Versioned execution: requests own resources, execution versions own "authority", the permission to publish output or install state. Revoke first, bound the old execution, certify the prefix the successor inherits. Zero obsolete output emitted in a replay of recorded coding-agent interruptions; revision TTFT median -17.1 percent. This is the missing concept for the LIVE_REPORT mtime inversion: regeneration cadence was never tied to a version that owns publish authority.
3. **2610.05241 StateWise (RQ1 seams).** Diagnoses and repairs corrupted persistent agent state BEFORE the next action: counterfactual replanning finds decision-critical records, read-only checks verify machine-observable facts, clarification handles developer-owned intent, typed evidence grounding carries repair lineage. 93.3 vs 38.7 percent correctness on 150 corrupted-state coding cases, zero unsafe actions. The estate's stash incident class, with a repair-lineage receipt.
4. **2609.34432 production trace (RQ4 envelope).** Two weeks, 11.7M requests, 10k+ GPUs: highly skewed request volumes per session, RARE execution overlap among logical sibling requests, context reuse across task boundaries. "Rare sibling overlap" is measured evidence against sizing dispatch shapes for heavy sibling concurrency; our 50-wide envelope runs a different regime worth naming against this trace.
5. **2609.34136 Waggle (RQ3 wiring).** One anonymous local law shared by interchangeable agents, learned by Swarm-Consistent Distillation; coordination emerges from repeated execution, no roles or global topology; retains over 96 percent of oracle quality and transfers across population changes without retraining. Test case for whether our law pack (ribs) can drive fresh seats without re-teaching topology.
6. **2609.32917 Planner-as-Router (RQ5 planning gate).** Folding tier selection into planning (small/mid/frontier assigned at decomposition) cuts cost 44 percent vs all-frontier for 2.9 accuracy points; unvalidated pilot hints cheap routing carries a hidden compounding penalty on compositional workflows. Direct design evidence for n_planning_mode as a built gate with tier assignment at plan time, plus a warning for the driving ladder.
7. **2610.04838 MemTrace (RQ1/RQ3).** Immutable traces stored as a graph, evidence validated against current repo state before use; DeepSWE pass@1 +21.2 points claimed. The receipt-contract shape for the knot/doctrine/steal layers: validity checks at read time instead of trust at write time.
8. **2610.04433 What Does a Harness Buy? (RQ2 boundary).** Harness swaps shift SWE-bench Verified scores about as much as reruns, while cost per task varies up to 3x. A measured null result for the harness axis: boundary claims need rerun-grade error bars, which bears on how we read the 36.3-percent class-variance receipt.

## Runners-up read but not banked

- `2610.00889` HakiCC: LLM multi-agent pipeline designs/evolves concurrency-control protocols, +50.6 percent TPC-C / +92.2 percent AuctionMark throughput; relevant if fold_gate grows beyond file-level serialization.
- `2610.06069` Attention Tax (already cataloged today): crossover at depth 10 on their task; decomposition wins when attention cost avoided exceeds handoff tax. Revisit if the mesh/boundary battery grows.

## Boundary of this sweep

Abstract-depth reads for 10 of 11 items, full-HTML read for 2610.04779 only. Nothing here is verified against our code beyond the catalog/memory greps named above; variance and gate numbers are the papers' own claims, not reproduced.
