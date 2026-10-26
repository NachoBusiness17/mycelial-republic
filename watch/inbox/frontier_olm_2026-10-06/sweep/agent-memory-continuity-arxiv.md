# SWEEP: agent-memory-continuity via arXiv (2026-10-06)

source-fetched: 2026-10-06. Sweeper: sweep-agent-memory-continuity-arxiv (subagent, dynamic workflow run).
Door: arXiv (export.arxiv.org Atom API + arxiv.org abs/html pages). No door 403'd. One fetch timed out at 60s (arxiv.org/html/2610.03902v1, first attempt) and was retried successfully in the same session; reported, not papered over.

## Pass 1 census (broad sweep, >=30 candidates required)

9 arXiv API queries, all `sortBy=submittedDate&sortOrder=descending`, fetched 2026-10-06 via WebFetch:

| query | rows listed |
|---|---|
| all:"agent memory" | 25 |
| all:"knowledge editing" | 25 |
| all:"memory" AND all:"multi-agent" | 25 |
| all:"context compaction" OR all:"memory consolidation" | 25 |
| all:"belief revision" AND all:"LLM" | 20 |
| all:"memory addressing" OR all:"content addressable" | 20 |
| abs:"summarization" AND abs:"long-term memory" AND abs:"agent" | 20 |
| abs:"memory freshness" OR abs:"stale knowledge" OR abs:"knowledge staleness" | 13 |
| abs:"conflicting" AND abs:"instructions" AND abs:"LLM" | 20 |

193 rows listed total; after date-filtering to 2026-09-06..2026-10-06 and relevance triage, 40+ distinct in-window candidates were considered (requirement: >=30, met). Candidate ids triaged include: 2610.06830, 2610.06361, 2610.05176, 2610.03902, 2610.02897, 2610.02687, 2610.00872, 2609.39765, 2609.38270, 2609.37953, 2609.36739, 2609.36795, 2609.36457, 2609.36170, 2609.35431, 2609.34422, 2609.34385, 2609.34242, 2609.29587, 2609.29045, 2609.28575, 2609.21533, 2609.17645, 2609.16178 (2609.16178 is 2608-listed, dropped), 2609.11060, 2609.08646, 2609.05510, 2609.03588, 2610.04672, and others from the tables above.

## Pass 2 deep reads (>=5 end to end, requirement met)

Full-text HTML reads (arxiv.org/html/<id>v1), each read end to end with a targeted extraction prompt:
1. 2610.03902 When Evidence Changes (retry after one 60s timeout)
2. 2609.36457 Memory Consolidation Flattens the Temporal Shape of User Facts (LAPSE)
3. 2609.36170 Assay: Claims That Decay With the Code
4. 2609.11060 Grounding Agent Memory: Environment-Probing Curation
5. 2609.29045 The Tokens Remember (Toketive)

Abs-page reads (title/date/verbatim-sentence/summary extraction): 2609.17645, 2610.02897, 2609.34422, 2610.05176, 2609.38270, plus a second abs fetch of 2609.36170 for a meatier verbatim quote.

Quote-fidelity caveat, stated plainly: on three abs fetches (2609.36457, 2609.36170, 2609.29045 first pass) the WebFetch sub-model declined full-verbatim abstract copies and returned faithful summaries instead; exact verbatim sentences were then obtained from the HTML full-text fetches or a re-fetch. Every quote in the banked items below is one the fetch returned verbatim.

## Overlap greps (run in this session)

`rg -i -c "<phrase>" catalog/catalog.jsonl memory` from repo root. NO-HIT for: "When Evidence Changes", "Memory Consolidation Flattens", "Claims That Decay", "The Tokens Remember", "Environment-Probing Curation", "State Without a Landlord", "Interpreting at Write Time", "Memory as Infrastructure", "Lost in Compaction", "Grounding Agent Memory", "Stashbird", "Coding Agent Memory Post-training", "VirusCascade", "Asymmetric Experience Consolidation", "Peer-to-Peer Replication of Durable Workflow", "aspectual flattening", "Toketive", "environment-probing". ("AECG" and "TWIST" bare-acronym greps hit unrelated substring noise in DL-book HTML and museum files, so exact-title phrases were grepped instead.)

Two exclusions for known-work: **2609.21533 MACE is already in the catalog** (catalog/catalog.jsonl row citing `corpus/lsa/2026-09-21/2609.21533v1.txt`, 1772 bytes, mtime 2026-09-21T06:30:32Z) and **2608.22752 Compaction Cliff is already held** (1 catalog hit; the ask itself cites it at burns.md:79). Re-banking either is waste; MACE's repair-relations finding is nonetheless subsumed below by AECG's governance loop.

## Findings mapped to the five research questions

### Q1 memory propagation clock + continuous instrument per seat class
**Assay (2609.36170)** is the direct steal. Claims bind to the Merkle hash of the code's dependency cone; "a claim is fresh iff its binding equals the current cone hash"; decay is a hash comparison, not a judgment; blast radius equals the set of claims a change invalidates. Estate translation: a law row's cone is the set of boot-pack inputs that compile it (rib files, law_amendments feed, quantizer input); a seat's pack is FRESH iff its input-hash set covers the post-landing law tip, and the propagation clock is just (now minus landing) per seat whose hash lags, sampled continuously. The paper's key cost number maps exactly onto "compile coverage is not propagation": cone binding re-verifies only 7.9-81.9% of claims vs repo-wide binding, and narrower self-hash binding misses 23-68% of required invalidations. Compile-coverage is the self-hash binding of law propagation.
**Grounding Agent Memory (2609.11060)** supplies the heal leg: an asynchronous, least-privilege, read-only probing curator that checks/refreshes stale entries before write; stale-memory failure mode named verbatim in read: a memory "retaining a renamed table name post-migration" is a stale law row one seat still carries. Their numbers: pass rate 39%->73% on CLBench, task-agent cost $3.38->$1.68, tool calls down 16-75% across six APEX worlds, all 18 memory-vs-baseline comparisons positive. Auditability: probes inherit platform auth, off the task critical path, no production write authority.

### Q2 two-law-stack merge (AGENTS.md vs 56-rib vault)
**AECG (2610.05176)** names the disease: "scope collapse occurs when procedural knowledge escapes the coordination scope in which it was shown effective and is repeatedly reused at incompatible decision levels" (verbatim from abs fetch). That is a formal name for a law row doing double duty across two stacks at different altitudes. Its governance loop is a candidate merge contract shape: confidence-aware detection, prioritized review of high-risk knowledge, and reactivation of revised entries only after paired replay, i.e. a merge retires a row by DEMOTION + review queue + re-earning, never silent deletion (wins 11 of 12 settings, up to +10.23pp). Detection leg candidate: ELCD 2609.08646 (listing-level read only) detects instruction-conflict drift from latent representations.

### Q3 placement-vs-compaction on zknot summaries
**LAPSE (2609.36457)** is the strongest find of the sweep for the zknot question. Writers systematically flatten temporal aspect: "I am driving a Peugeot" stored as "The user drives a Peugeot". Measured: 244 of 381 matched progressive-vs-simple pairs flattened by writers with ZERO reversals (807 progressive-only vs 2 simple-only across 11 configurations); holds inside installed pipelines mem0 2.0.19 (49/128), Graphiti 0.30.1 (15/32), Letta 0.16.8 (26/29). Causal leg: changing only the stored verb shifted all three readers' still-holds estimates (p<1e-5) and made 2 of 3 readers act-without-asking more often. And the killer: their memory-use task could NOT detect this because readers acted on almost every stored fact, even expired ones, which is exactly the freshness-theater shape. Steal for zknot: run a LAPSE-style matched-pair benchmark over the 171 zknot pairs; store original wording + temporal form + observation time as separate fields (their fix recommendation), and expect summarize-at-window-close to flatten exactly like mem0.
**Interpreting at Write Time (2610.02897)** backs placement-before-compaction: per-goal summaries written at write time beat one all-goal summary on relevance/completeness/accuracy; verbatim: "Per-goal summaries win on relevance, completeness and accuracy, and the all-goal summary loses even to the neutral one written at a fraction of its budget." The estate analog: per-seat-class boot packs (elder/builder/day_work) written from the vault at pack time beat one monolithic zknot recap for any seat's recall.
**When Evidence Changes (2610.03902)** prices the summarization lane: on short ICU records every memory pipeline cost at least 2x full source-filtered re-reading (local repair's full pipeline 3.5-4.3x re-reading at k=20, reuse did not close the gap); memory only wins at ~10k-token records after 2-14 uses. Corollary for the estate: for law/source questions, re-read the rib/source bytes rather than trusting any summary layer until the source genuinely exceeds a window.

### Q4 addressability by content id vs path
**Coding Agent Memory Post-training (2609.34422)**: RL on plain file operations as memory (CAMG environments: shell access, persistent workspaces) gets 4B/9B models to match much larger models on SWE-bench Verified / MLE-bench Lite, i.e. path-addressed memory is not just viable, it is trainable capital. Supports the estate's path+corr_id hybrid over wholesale id-addressing.
**State Without a Landlord (2609.17645)**: P2P replication of a durable workflow journal with single-writer epoch cores, quorum-finalized succession, and a content-addressed payload plane; verbatim: "durability, timeout, and checkpoint decisions are carried by explicit certificates rather than implicit trust". Design template if estate memories ever move to content-id addressing with multi-seat writers.
Honest gap: nothing in this window's reads surfaced the trailing-space/id-exact-match undercount disease generalizing to id-based addressing; the nearest neighbor is Assay's exact hash binding, where a whitespace change in the underlying artifact legitimately changes the hash. Not found is not the same as refuted; marked as a gap, not an answer.

### Q5 belief-retirement depth
**When Evidence Changes (2610.03902)** reproduces freshness theater in controlled form: under replacement, re-reading adopted the new value 13/13 per model vs 8-9/13 for rebuild/local-repair memory; in every memory miss the NEW value was already present in the prompt, so the failure was use-stage, not propagation, and their commit gate checked neither support nor freshness; the no-propagation negative control committed superseded values. Estate translation: a cured graph node whose downstream seats never re-derive is exactly this use-stage failure; the instrument must test adoption at use, not presence in the pack.
**The Tokens Remember (2609.29045)** is the one-layer-down law: localized fixes leave reachable residue. Alternative valid tokenizations bypass localized edits at 38.6%; across 5 models x 6 datasets x 6 editing/unlearning techniques; and the adaptive-editing experiment shows the tradeoff explicitly: driving bypass 0.32->0.04 inflated ripple effects 1.0x->8.6x. Verbatim from full text: "the same input string can be represented by alternative valid tokenizations that induce different computational trajectories, allowing an adversary to bypass localized modifications and recover information intended to be suppressed." For R4B's 29/31 dangling welds cured to 0: the paper predicts a cure that only patches the canonical access path leaves the other paths open, and that pushing the cure wider multiplies collateral.
**AECG (2610.05176)** again: retirement is a loop, reactivation only after paired replay, 11/12 settings won.

## Banked items (8, strongest first)

1. 2610.03902 When Evidence Changes: Evaluating Memory Repair and Re-reading in Language-Model Agents (2026-10-02)
2. 2609.36457 Memory Consolidation Flattens the Temporal Shape of User Facts (2026-09-29)
3. 2609.36170 Assay: Claims That Decay With the Code (2026-09-28)
4. 2609.11060 Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents (2026-09-10)
5. 2610.02897 Interpreting at Write Time: A Policy Ablation for Multi-Goal Agent Memory (2026-10-02)
6. 2610.05176 AECG: Asymmetric Experience Consolidation and Governance In Multi-Agent Systems (2026-10-04)
7. 2609.29045 The Tokens Remember: When Tokenization Bypasses Knowledge Editing and Unlearning (2026-09-24)
8. 2609.34422 Coding Agent Memory Post-training (CAMG) (2026-09-28)

## Not run / limits

- No full PDF downloads; end-to-end means the arXiv HTML full-text rendering (ar5iv-class) plus abs pages. Where HTML was unavailable or timed out, that is stated above.
- ELCD 2609.08646, TWIST 2609.28575, KC-Bench 2609.03588, Frontier Autolab 2609.36739, MemFit 2610.00872, Stashbird 2609.34242, State-side items beyond the abs reads were triaged at listing level only and are NOT banked.
- Quote fidelity caveat above applies; every banked quote was returned verbatim by a fetch in this session.
