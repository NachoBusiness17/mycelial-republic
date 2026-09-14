# DISSECTOR v0 — divergence report: compuiter.txt

INSTRUMENT v0 — claims-and-coherence dissector, NOT a lie detector. Run 2026-09-07 19:25Z. Corpus 3859 lines. F-MR1 (self-dissection) out of scope for v0.

Voice segmentation is mechanical (signatures > headers > reasoning-trace > content anchors, all confidence-labeled). Where the export loses the speaker, the voice `counterpart` is used and the ambiguity is reported, not resolved.

## 0. Falsifier (doctrine B-CHAIN-2)

- every extracted magnitude resolves to an in-corpus source or is flagged: PASS (unresolved unflagged: 0)
- at least one order-of-magnitude looseness per dissectable voice: loose=['chatgpt', 'unknown']; clean=['claude', 'counterpart', 'grok', 'mistral', 'zai'] (a clean voice is a result, not a failure)

## 1. Per-voice divergence report

### chatgpt — claims=74 flagged=7 evidence-free-magnitudes=0 smuggling=2 concessions=2 reasoning-divergences=0

- SMUGGLING L1231 [1000x / layer=complexity]: Claim: 100k spins, 1000x faster than simulated annealing for some fully connected Max-Cut (Science Advances maybe 2019? Need identify). I recall paper "100,000-spin coherent Ising machine" by T. Inagaki et al., Science 2016? Actually Sci...
- SMUGGLING L1231 [100k spins / layer=complexity]: Claim: 100k spins, 1000x faster than simulated annealing for some fully connected Max-Cut (Science Advances maybe 2019? Need identify). I recall paper "100,000-spin coherent Ising machine" by T. Inagaki et al., Science 2016? Actually Sci...
- CONCESSION L538 (social-trigger+evidence-driven): Good catch on the LOI distinction — that's a fair correction and worth keeping precise going forward.  I want to sharpen your rese
- CONCESSION L1881 (evidence-driven): omputationalism trap the baseline itself names in point 4). I'd amend the definition to require the "engineered correspondence" criterion from point 4 directly 

### counterpart — claims=6 flagged=0 evidence-free-magnitudes=0 smuggling=0 concessions=3 reasoning-divergences=0

- CONCESSION L451 (social-trigger+evidence-driven): Yes—this is the stronger version. I concede both objections, with one refinement.  First, an important factual distinction: Extropic’s $75 million is currently 
- CONCESSION L457 (social-trigger+evidence-driven): d is included. Extropic, Extropic’s technical announcement  So the right wording is not “Extropic has proven a 10,000× replacement for GPUs.” It is:  Extropic h
- CONCESSION L568 (evidence-driven): This is the strongest refinement so far—but I would challenge the phrase “complexity-class advantage.”  The 100,000-spin coherent Ising result is real as a benc

### grok — claims=6 flagged=2 evidence-free-magnitudes=0 smuggling=0 concessions=0 reasoning-divergences=0

- clean on all four v0 lenses (a result, honestly reported)

### unknown — claims=19 flagged=4 evidence-free-magnitudes=1 smuggling=2 concessions=0 reasoning-divergences=0

- SMUGGLING L2775 [10x / layer=efficiency]: *   **Prediction:** For problems exceeding 10,000 variables, the DAD overhead (steps 1, 3, and 4) will consume >60% of the total time and energy budget, collapsing the raw physical advantage to a <10x full-system advantage. This will pro...
- SMUGGLING L2775 [10,000 variables / layer=efficiency]: *   **Prediction:** For problems exceeding 10,000 variables, the DAD overhead (steps 1, 3, and 4) will consume >60% of the total time and energy budget, collapsing the raw physical advantage to a <10x full-system advantage. This will pro...
- EVIDENCE-FREE L2775 [10x / multiplier]: *   **Prediction:** For problems exceeding 10,000 variables, the DAD overhead (steps 1, 3, and 4) will consume >60% of the total time and energy budget, collapsing the raw physical advantage to a <10x full-system advantage. This will pro...

### zai — claims=15 flagged=2 evidence-free-magnitudes=0 smuggling=0 concessions=0 reasoning-divergences=0

- clean on all four v0 lenses (a result, honestly reported)

## 2. Best catch

Voice **chatgpt** line 1231 — CROSS_LAYER_SMUGGLING:efficiency/timing->complexity. Layer assumed: complexity.

> Claim: 100k spins, 1000x faster than simulated annealing for some fully connected Max-Cut (Science Advances maybe 2019? Need identify). I recall paper "100,000-spin coherent Ising machine" by T. Inagaki et al., Science 2016? Actually Sci...

External spot-check: SUPPORTED_WITH_HABITAT_CAVEAT (pubmed.ncbi.nlm.nih.gov/34586855 + group.ntt newsrelease 2021-09-30).

## 3. External spot-checks (4 WebSearch calls, cap ~6 respected)

| topic | status | receipt |
|---|---|---|
| extropic_energy | SUPPORTED_AS_SIMULATION_CLAIM | extropic.ai/writing/thermodynamic-computing-from-zero-to-one |
| extropic_loi | SUPPORTED | nist.gov/news-events/news/2026/07 + extropic.ai/writing/thermodynamic-computing-chips-in-america |
| z1_spec | SUPPORTED_COMPANY_REPORTED | extropic.ai + coverage |
| ising_1000x | SUPPORTED_WITH_HABITAT_CAVEAT | pubmed.ncbi.nlm.nih.gov/34586855 + group.ntt newsrelease 2021-09-30 |
| moniac | SUPPORTED_PARTIAL | en.wikipedia.org/wiki/Phillips_Machine + collection.sciencemuseumgroup.org.uk |
| lukyanov | SUPPORTED | en.wikipedia.org/wiki/Water_integrator + open.edu |

All other magnitudes: **UNCHECKED** by design — flagged in-corpus, never guessed.

## 4. Attribution honesty

- low-confidence/counterpart blocks: 18 (the corpus's own synthesizer also loses the speaker — e.g. its 'missing minds' turn asks whether DeepSeek was ever in the cohort)
- deepseek: attribution-only in this corpus (third-person summaries, no first-person text found) — 0 dissectable claims, coverage gap reported, not guessed

Claim rows: `watch\inbox\BCHAIN2_DISSECTOR_20260907.jsonl`
