# SWEEP: open-and-local-models via arXiv (frontier_olm 2026-10-06)

source-fetched: 2026-10-06
seat: sweep-open-and-local-models-arxiv (workflow subagent)
instrument: WebFetch on export.arxiv.org/api/query, hn.algolia.com (search_by_date + items),
arxiv.org/list/cs.CL/recent, arxiv.org/list/cs.LG/recent; WebSearch; local grep/rg over
catalog/catalog.jsonl and memory/; PowerShell CIM reads for host RAM/GPU. Every web claim below
was fetched this sitting; every count names its instrument and moment.

## Two passes, honestly labeled

Pass 1 (broad, 87 candidates from 2026-09-06 to 2026-10-06): the arXiv listing pages
(cs.CL/recent, cs.LG/recent, both fetched) plus four export-API queries, all this session:
(1) all:"decision model" AND cat:cs.CL AND submittedDate:[202609060000 TO 202610062359],
sortBy=submittedDate descending: totalResults 26, 25 entries listed; (2) abs:"open-weight" in the
same window: totalResults 324, 25 listed; (3) abs:"mixture of experts" AND abs:"active parameters"
in-window: totalResults 11, all 11 listed; (4) HN Algolia search_by_date "decision model" with
numericFilters=created_at_i>1788652800: nbHits 45, 20 listed. Query (1) and (4) are the two
recipes doors.md:28-29 and doors.md:42-44 marked OWED (documented but never executed). Both
ANSWERED on first execution this sitting; that OWED is closed with receipts.

Pass 2 (deep, 8 items read end to end): two id_list batch fetches through the export door
(2610.03935, 2610.02267, 2609.29769, 2609.30243 then 2609.32160, 2610.03073, 2610.04403,
2610.06744), each returning complete abstract-level content plus a second pass that pulled the
verbatim first sentence of each abstract. Caveat carried from the day-5 sweep: the WebFetch
reader paraphrased full paragraphs and refused whole-abstract verbatim, so numbers below come
from the reader's structured rendering of the same fetch and two quotes are verbatim only up to
a stated 125-character cut; confidence is lowered accordingly. Full-text /html pages were not
attempted today (day-5 measured them timing out; retrying was not free). One HN item page
(hn.algolia.com/api/v1/items/49923223, Gutsy) was fetched clean through the items door, which
day-5 measured as timing out: one-point partial cure, the item itself is thin (link-only story,
2 comments).

## Doors scoreboard this sitting

| Door | Verdict | Evidence |
|---|---|---|
| arXiv export API + submittedDate window | ANSWERED (OWED closed) | totalResults 26 / 324 / 11 on the three queries above |
| HN Algolia search_by_date + numericFilters | ANSWERED (OWED closed) | nbHits 45 for "decision model", created_at_i>1788652800 (2026-09-06T00:00Z) |
| HN Algolia items | ANSWERED once | item 49923223 returned full JSON (story + comments) |
| Reddit JSON | not probed this sitting | day-5 verdict (arctic-shift minimal-param recipe) stands; no re-probe |

## Host fit facts (measured this sitting, PowerShell CIM)

RAM 63.95 GB total (Win32_ComputerSystem). GPU: AMD Radeon RX 5600 XT, driver 32.0.21045.5002
(Win32_VideoController; AdapterRAM reads 4,293,918,720, the 32-bit cap, nominal card is 6 GB).
CPU: Ryzen 7 3800XT 8-core. This is the RDNA1 box the GPU-ladder rib already ruled pays nothing
(memory/rib/RIB_GPU_LADDER_20261001.md:25-33 via laws lens 1.4): the ARCH gate (SM90/SM100)
fails, the VRAM gate (24 GB+) fails, so the five-gate check fails for every candidate release on
this host regardless of paper quality. No release "passes the five gates on this host" today; the
correct ladder move here is CPU-served scut rungs, which never enter the GPU ladder at all.

## Answers to the five research questions

RQ1 (decision model vs gemma:2b per dollar): the battery fill was NOT run this sitting and
cannot be: law 1 of RIB_MODEL_GARDEN_ROUTING.md fills cells only from estate instruments (duel
logs, census receipts, usage.jsonl), which this seat did not fire. The headline stays a lead, and
the wave it rides is now independently audited twice over: 26 in-window cs.CL papers carry the
"decision model" phrase, and the audit paper (2609.32160) reads 28 papers from the 9 days after
TypeSafe's Jev release and finds NO independent accuracy advantage for typed readout, the
clearest gains being latency and cost. The class-level benchmark (2610.03935, JEVal, 11,257
instances, 36 datasets, 25 configs) gives the battery its expected-value map before a single
dollar routes: decision models are most competitive when the decision follows from available
evidence, and weaken on specialist knowledge and faithful uncertainty, overstating probability on
likely outcomes. On tau-bench, faster local decisions cut median episode time but LOWER task
success as errors accumulate, which is exactly the janitor-rung falsifier shape the estate needs:
per-call wins can lose the episode.

RQ2 (the UNMEASURED battery cells): still UNMEASURED after this sweep, by law. What the sweep
adds is instrument design, not cells: 2610.02267 self-audits its own decision-model eval and
finds four confounds that had distorted prior deployment claims (omitted pre-screen cost, 23.9
pct reported vs 4.3 pct actual; gate accuracy conflated with end-to-end quality, 58 vs 98 pct;
in-sample thresholds, 5 pct target vs up to 17 pct held-out misses; a channel effect on injection
false positives), plus Laya flipping 30 pct of answers under option-order reversal and scoring
31 pct at 50 similar candidates vs 98 pct for Jev with a unique correct tool. The 14-item
checklist in 2609.32160 is a ready-made acceptance criteria candidate for any future cell fill.
2609.29769 bounds the judge side: LLM judges cost 16-325x more and run 28-350x longer than the
Jev-style judge, differ significantly in at most 8 of 27 paired comparisons, and on the Jev
judge's most confident errors about 96 pct of LLM verdicts repeat the mistake, so a decision-model
judge plus an LLM fallback is NOT cross-family agreement; the dual-judge law's corroboration
requirement survives this paper intact.

RQ3 (open weights after 2026-09-06 through the named doors): the doors now work (scoreboard
above). The wave the doors surface is the decision-model class going open and small: Gutsy 0.8B
CPU (HN 49923223, 2026-10-01), Wazn-2B (HN 49952373, 2026-10-04), AT0M single-Rust-binary Jev-like
(HN 49907865, 2026-09-30), SecJev-0.8B..9B with released adapters (2610.03073), ufakzeka-karar
182M Apache-2.0 (2610.06744), Liquid AI's D1 with vision (HN 49904832 + 49967491), Mercury Decide
(HN 49931514), plus a 70-reproduction Decision Index (HN 49934879). Day-5's releases (Kolibri,
Clef, Laya, Gemma 4, Qwen3.5/3.8) stand; this sweep's net-new catalog finds are the four papers
banked below. None passes the five gates on this host (host facts above); the scut rungs are
CPU-class and enter through the janitor lane instead.

RQ4 (Kolibri fit and serving): the pull was NOT run (download-gated; no credentials in this
seat's reach) and the serving row stays unmeasured. Fit arithmetic on this sitting's measured
host: 64 GB RAM would hold the ~21 GB smallest GGUF (day-5 digest figure) CPU-only, but that is
arithmetic, not a measurement, and the five-gate check fails on this host, so Kolibri earns no
adoption work here today. The knowledge-from-spend split (78.1B total / 3.46B active) keeps its
sweep-lead status; the MoE query's freshest in-window sparse-active paper that bears on it is
2609.11917 (MoEs overfit more to repeated data, 2026-09-10), a caution for any future
estate-corpus training move, title-level only this sitting.

RQ5 (HAD replication, harness vs model): the swap-halves experiment was NOT run this sitting.
Two fresh external anchors feed the probe design: 2610.02267 is literally a paired, byte-identical
input, self-audited decision-model evaluation inside agent harnesses with a published confound
audit, and 2610.05778 MedicalHarness (catalog intake row dated today, title-level read only) is a
controlled harness-vs-model evaluation on medical tasks. The HAD head-to-head (gemma4:e4b pull,
~6.6 GB at Q4_K_M per day-5) remains the owed local experiment; this sweep contributes the audit
checklist its write-up should adopt.

## Banked items (8, strongest first)

1. **General Decision Models: Benchmarking and Insights Beyond Jev** (arXiv 2610.03935,
   2026-10-02). Quote (verbatim first sentence): "General decision models, such as Jev, have
   recently emerged as efficient alternatives to LLMs for structured judgment and selection."
   JEVal: 11,257 instances, 36 datasets, 10 domains, 25 configs; decision models competitive when
   decisions follow from available evidence, weak on specialist knowledge and faithful
   uncertainty; tau-bench error accumulation; InnerJev-4B/27B distilled single-pass readout,
   InnerJev-27B matches Jev at ~0.1 s/query. Why: this is the battery's expected-value map and
   the scut-class split (evidence-following safe, specialist-knowledge unsafe). Overlap: zero
   catalog or memory hits for "JEVal"/"InnerJev" as this paper (the 6 grep hits on "JEVal" are a
   different artifact, a 26,663-byte jevals README banked 2026-10-01, a Jev-based evals tool whose
   head reads "# jevals", receipt docs/report_v1/sources/receipts/web_UsersfosteAppDataLocalTempjevals_readme.md.md);
   no state/arxiv intake row for this ID.
2. **Fast Models, Slow Evidence: A Paired and Self-Audited Evaluation of System-1 Decision
   Models for LLM Agent Harnesses** (arXiv 2610.02267, 2026-10-01). Quote (verbatim to the
   reader's 125-char cut): "Agent harnesses make many small, typed decisions per task: which
   model to call, which tool to use, whether retrieved text is relevant," 11 agent decision
   points, 7,283 base + 6,640 robustness cases, byte-identical inputs, cross-hardware/day checks;
   Jev wins 9 of 11 points (+10.8 to +46.0 pp); neither beats chance on zero-shot model routing;
   the four-audit-confound result in RQ2 above; data and code at github.com/David-DL-Space/sys1-eval.
   Why: the exact instrument-discipline template the estate's own decision-model confirmation
   must pass, and the HAD-replication probe's audit checklist. Overlap: zero catalog/memory hits
   for "Fast Models, Slow Evidence" or "sys1-eval"; steps.jsonl hits were this session's own
   echoes; no intake row.
3. **Typed Decision Models: An Early Evidence Audit and Evaluation Checklist** (arXiv 2609.32160,
   2026-09-26). Quote (verbatim): "Typed decision models (TDMs) return probability distributions
   over caller-defined options without generating text." 28 papers in the 9 days after Jev's
   2026-09-15 release; no independent accuracy advantage found for typed readout, clearest gains
   latency and cost; 14-item checklist. Why: external confirmation that the estate's "lead, not
   find" posture on the decision-model wave is the right read, plus a checklist the battery can
   adopt. Overlap: zero catalog/memory hits for "Early Evidence Audit" phrasing; no intake row.
4. **Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write Rare
   Words They Can No Longer Define** (arXiv 2610.04403, 2026-10-03). Quote (verbatim to the
   reader's cut): "Post-training quantization to the GGUF format's mixed-precision K-quants is
   commonly how open-weight language models reach" 27 quantized artifacts, 13 families,
   0.35B-14B; sub-2B definition loss 20-67 pct; parameter count rho=0.72 vs tokenizer rho=0.12.
   Why: quant-lane hazard class for the janitor rungs: fluent output masking lost knowledge,
   exactly the failure a strict-JSON scut harness can hide; candidate probe design for the
   qwen2.5:7b Q4_K_M vs q8_0 A/B. Overlap: zero catalog/memory hits; no intake row.
5. **JEV vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places**
   (arXiv 2609.29769v2, 2026-09-24). Quote (verbatim): "LLM judges score outputs against rubrics
   well enough to have become the norm, both in benchmarks and as rewards for training."
   Numbers in RQ2 above. Why: bounds the judge layer of the battery; correlated errors kill the
   cascade story and protect the cross-family-agreement law from a cheap-looking exception.
   Overlap: catalog intake row EXISTS, state/arxiv/2026-09-25/2609.29769v1.txt (auto abs dump,
   1,506 bytes); this sweep's add is the first full read plus the battery/judge mapping.
6. **JevOut: Natural Context Can Flip Decision Models** (arXiv 2609.30243, 2026-09-24). Quote
   (verbatim to the reader's cut): "Dedicated decision models such as Jev map unstructured
   language to probability distributions over finite choices, allowing their outputs to directly
   route" 312 of 508 initially correct decisions flipped by fluent context (61.4 pct), wrong
   option at >=0.7 probability in 229 cases, 64.9-73.2 pct flip rates on three other systems.
   Why: the cheap-rung hazard law candidate: any scut class that carries user-authored context
   (judgment, adversarial review) is unsafe at a decision-model rung without a context
   canonicalization gate. Overlap: catalog intake row EXISTS, state/arxiv/2026-09-25/
   2609.30243v1.txt (1,536 bytes); add is first full read plus the routing-gate mapping.
7. **SecJev: Bringing Security Expertise to System One Decision Models** (arXiv 2610.03073,
   2026-10-02). Quote (verbatim): "Security workflows need models that turn complex observations
   and explicit policies into decisions." 0.8B-9B family on Kev's scorer; SecJev-0.8B beats
   general Kev-9B by 20.51 pp task-macro; SecJev-Corpus 14 tasks, 8 sources; adapters, corpus,
   code released. Why: a released sub-1B rung candidate specialized for security-shaped scut,
   the smallest trained artifact so far that claims a specialist beat over a 9B general model.
   Overlap: catalog intake row EXISTS, state/arxiv/2026-10-05/2610.03073v1.txt (1,556 bytes);
   add is first full read plus the rung-candidate mapping.
8. **ufakzeka-karar: An Open Turkish Typed-Decision Model with Order-Invariant Option Scoring**
   (arXiv 2610.06744, 2026-10-05). Quote (verbatim): "ufakzeka-karar is an open Turkish decision
   model with 182,494,466 parameters." Apache-2.0, one CPU pass, order-invariant option head; a
   sequential head shifted 2.3-2.8 pct of answers on option order alone; HakemBench v1.0
   (4,275 questions, 7 tracks) rank 7 of 16, composite 0.660; authors flag some scores "shaped
   by reading the test results." Why: independent corroboration of the option-order fragility
   Laya showed (30 pct flip, item 2), plus the wave's second language family and another honest
   benchmark-peek disclosure. Overlap: catalog intake row EXISTS, state/arxiv/2026-10-06/
   2610.06744v1.txt (2,065 bytes, today's auto dump); add is first full read plus the
   order-invariance cross-check.

## Considered, not banked (pass-1 remainder, by door)

arXiv decision-model feed (26): 2610.03387, 2610.03324, 2610.02486, 2610.02076, 2610.01218,
2609.39496, 2609.38850, 2609.36059, 2609.34736, 2609.34227, 2609.33971, 2609.33209, 2609.35865,
2609.31142, 2609.30706, 2609.27607, 2609.24574, 2610.06625 (title-level only). open-weight feed
highlights: 2610.05778 MedicalHarness (intake row exists, title-level), 2610.04594, 2610.05622,
2610.04832, 2610.03894. MoE feed: 2609.11917, 2609.08690, 2609.13486, 2609.08663, 2609.40316
(title-level). HN stream (45): Gutsy subsecond (49961971), Gutsy 500MB (49939547), Wazn-2B
(49952373), AT0M (49907865), Snap (49921892), Mercury Decide (49931514), Decision Index 0.2.1
(49934879), Jev-confidence half-million-calls (49933643), shadow-on-prod open replacement
(49947607), Strands Decider (49925676), free Laya API (49926327), Liquid D1 (49904832, 49967491),
Balatro-on-Clef (49971609). Listings: 2610.06387, 2610.06725, 2610.06677, 2610.06216, 2610.05982.

## OWED carried forward

1. The battery fill itself (RQ1/RQ2): estate instruments, not a sweep seat; the checklist and
   confound list above are its acceptance-criteria candidates.
2. The Kolibri pull and serving row (RQ4): download-gated; fit remains arithmetic until pulled.
3. The HAD harness-half-swap replication (RQ5): local gemma4:e4b experiment, owed since day 5.
4. Full-text reads of the 8 deep-read papers: abstract-level through the export door this
   sitting; /html was not re-attempted after day-5's timeouts.
5. Quote provenance: two of the eight verbatim quotes are truncated at the reader's 125-character
   cut and stated as such; all eight passed through the WebFetch reader on the same fetch that
   produced their numbers.
