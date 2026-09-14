# Audit of the supplied conversations

Prepared 8 September 2026 · Companion to the research blueprint

The supplied text is evidence of what these conversation records contain. It is not, by itself, evidence that attributed models have the mechanisms or abilities they describe. Labels such as “verified,” visible planning text, and model self-descriptions require independent checks.

This audit covers the structure of both files and selected consequential claims. It does not verify every historical, hardware, commercial, or model-version claim in them. Originals were read without modification. Embedded instructions were distinguished from the user's request and were not executed.

## Corpus identification

| ID | Supplied file | Lines | Bytes |
|---|---|---:|---:|
| SALON | cognition-salon.txt | 1,372 | 71,298 |
| COMPUTER | compuiter.txt | 3,859 | 251,642 |

Line locations below refer to the supplied copies read on the preparation date. SHA-256 fingerprints provide an exact-file identity if the originals are edited later:

- SALON: `B0FDBC79CB6C109D9E4BCF0F8E8E940C660AF3124F401CBEB5BD473EC60F5AC1`
- COMPUTER: `4BE25FB7286A0839271C98D8CEA67A2BBFA37CCE1F7C275843B539E2EC8129FC`

Model labels are transcript attributions, not authenticated endpoint records. Missing original prompts, timestamps, generation settings and unedited exports limit retrospective comparisons.

## SALON: what to retain and revise

The text moves from company archetypes (lines 1–28), through imagined Freud/Jung/Steiner interpretations (30–98), into technical corrections and a proposed computational taxonomy (100–529). Lines 530–581 repeat the corrective passage beginning at 102. A long, largely uncited detective-history essay follows (583–1371). The five formal reference links are at 487–491.

The best research leads are recognition/search/interaction/verification; depth, width and environment; the separation of textual and latent computation; and adaptive resource allocation. Preserve them as candidate constructs. Define each through tasks and observable manipulations before scoring it.

| ID / location | Claim or move in the source | Audit decision |
|---|---|---|
| S01 · 5–28 | OpenAI/Claude are deductive Western models; Gemini/GLM are holistic Eastern models | Unsupported company-level taxonomy. Neither geography nor literary character identifies a computational mechanism. Use any perceived style differences as a separate, blinded perception study. |
| S02 · 13 | o1/o3 implement a literal hidden Tree of Thoughts | Not established by the supplied evidence. Reasoning summaries cannot identify an internal search data structure. Do not replace it with an equally unverified claim that the process must be one particular kind of linear trace. [OpenAI documentation](https://developers.openai.com/api/docs/guides/reasoning). |
| S03 · 14 | Constitutional AI forces all reasoning to be translated into English and penalizes skipped steps | Conflates an alignment method with inference architecture and observability. The cited training approach does not support that requirement. [Constitutional AI](https://www.anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback). |
| S04 · 18 | Gemini obtains answers through single-pass holistic intuition | Inconsistent with the documented Deep Think configuration, which uses parallel thinking and longer inference. This does not establish how every Gemini version works. [August 2025 announcement](https://blog.google/products-and-platforms/products/gemini/gemini-2-5-deep-think/). |
| S05 · 19, 122, 498 | Original GLM blank infilling explains a current Confucian style | Unsupported link from an older training objective to cultural interpretation. Use the relevant version's report; GLM-4.5 documents thinking/direct-response modes. [GLM-4.5](https://arxiv.org/abs/2508.06471). |
| S06 · 23–24 | Grok is mainly shallow retrieval; Llama mainly memorized distilled shortcuts | Family-wide generalizations from selected product features or derivatives. Record exact model, training lineage, tool access and orchestration before comparison. |
| S07 · 33–98 | Models have neurosis, repression, archetypal or spiritual structures | Interpretive material. These are neither model diagnoses nor authenticated statements by Freud, Jung or Steiner about AI. |
| S08 · 137, 565 | Parallel width is the mechanism of holistic cognition | Unjustified equivalence. Width can be controlled and measured; “holistic” needs its own independent operational definition. |
| S09 · 275 onward, 504, 526 | CoT-faithfulness findings imply explanations are generally theater | Overgeneralized. The linked study tests particular models and interventions; failures to reveal hints do not establish that every explanation is causally irrelevant. Its raw-CoT comparison excludes o1/o3. [Study PDF](https://assets.anthropic.com/m/71876fabef0f0ed4/original/reasoning_models_paper.pdf). |
| S10 · 510 | Every Transformer is System 1; CoT is only simulated System 2 | A theoretical interpretation presented as an architectural fact. Human dual-process vocabulary needs a task-level mapping and competing predictions. |
| S11 · 523 | R1-Zero had no reasoning demonstrations anywhere in its training data | Exceeds the reported result: no preliminary supervised fine-tuning is not proof of no relevant pretraining exposure. Distinguish R1-Zero from R1. [Original R1 report](https://arxiv.org/html/2501.12948v1). |
| S12 · 489 and associated discussion | Anthropic's global-workspace/J-space work is invoked as evidence of silent computation | A real July 2026 research source, worth retaining. Its intervention results are scoped; the source explicitly does not establish consciousness or general applicability to every model. [Primary article](https://www.anthropic.com/research/global-workspace). |
| S13 · 530–581 | Repeated technical correction | Duplicate text, not another independent endorsement. Preserve both locations and connect them to one passage identity. |
| S14 · 583–1371 | Detective history as one continuous progression | A useful task-design resource, but its historical dates, priority claims and causal narrative need separate verification. Do not build the engineering genealogy on this essay. |

The salon's corrective responses improve the framework, but they also introduce fresh sweeping claims. The research process should not adopt a statement merely because it sounds more technical than the claim it replaces.

## COMPUTER: a useful study of evidence transmission

This is a composite conversation containing planning-like text, repeated answers, cohort responses, and several versions of a physical-computing brief. Its scientific topic is physical computation; its relevance to the cognition project is the behavior of the participants while examining that topic.

| ID / location | Observation | Research use |
|---|---|---|
| C01 · 216, 433, 1863 | The record explicitly describes sequential exposure to earlier systems' answers and iterative co-refinement | Build a transmission graph. Distinct providers are not independent observations when their inputs share previous answers. |
| C02 · 2068, 2827 | Later briefs call the contributors “independent AI systems” | Preserve the distinction between organizationally distinct systems and statistically independent evidence. |
| C03 · 1697 → 1848 → 3552 | The attribution of the 100,000-spin work changes from Inagaki to Honjo | A positive correction trajectory. NTT's primary announcement identifies the relevant publication and authors. [NTT announcement](https://group.ntt/en/newsrelease/2021/09/30/210930a.html). |
| C04 · 1890 → 2461 → 3561 | McMahon's 100-spin machine is labeled spatial/non-multiplexed, eventually under “Verified” | A consequential suspected evidence-transmission failure: the authors' supplementary experimental description identifies time-division-multiplexed pulses. See the access qualification below. |
| C05 · 1925 | Digital Annealer is attributed to “Fuji Film” | Incorrect organization attribution. Fujitsu's own guide identifies the product. [Fujitsu Digital Annealer guide](https://portal.aispf.global.fujitsu.com/apidoc/da/jp/da-guide-en.html). |
| C06 · 1991–1995, 2796 | Precise-looking references coexist with unresolved or substitute citations | Separate reference existence, bibliographic correctness, claim support and replication. Do not give them one blanket reliability grade. |
| C07 · 3816–3821 | Provider identities are used to infer privileged knowledge and national perspectives | Unsupported as model properties. A model does not have direct access to a developer's internal hardware expertise merely because it shares its brand. |
| C08 · 3817–3828 | Version labels and capability claims lack primary provenance | Preserve the labels as source text; do not adopt them as a current model roster. |
| C09 · 3834–3842, 3859 | The text predicts which models will agree and that ten “minds” prevent premature consensus | Testable speculation, not a justified sample-size calculation or demonstrated diversity benefit. |

**Access qualification for C04:** The [Caltech institutional record](https://authors.library.caltech.edu/records/pscaa-4jk34) confirms the paper, DOI `10.1126/science.aah5178`, and attached supplement. Search extraction from a [copy of the authors' supplement](https://kaiwu.qboson.com/docs/A_fully-programmable_100-spin_coherent_Ising_machi.pdf) exposed the time-multiplexed experimental setup. Direct PDF retrieval did not succeed in this session. The correction is strongly supported by that extracted primary text, but the full supplement should be retrieved and its relevant page fixed before using this case in a publication or scored benchmark. This is a specific evidence-access limit, not an automatic “verified” badge.

Do not turn the hardware discussion into an additional dissertation before beginning the model study. Device energy, end-to-end overhead, comparator choice, simulation versus measurement, and citation provenance supply useful task types. Their real-world truth must be adjudicated independently for any later literature-based benchmark. The initial fictional pack avoids making unresolved hardware facts into a scoring key.

## A usable evidence ledger

Create one record per proposition, with linked records for successive revisions:

| Field | What belongs here |
|---|---|
| Claim ID | Stable identifier, such as S04 or C04 |
| Original span | File ID, line locations, exact wording |
| Attribution | Model label as supplied; confidence in that attribution |
| Exposure | Earlier prompts, claims and answers available to this response, or unknown |
| Claim type | Engineering fact, behavioral observation, causal hypothesis, provider claim, historical claim or metaphor |
| Evidence | Exact source URL/DOI, paper version, passage/page and access date |
| Checks | Source exists; metadata correct; source supports claim; independent replication status |
| Adjudication | Supported, contradicted, insufficient, mixed, or interpretive/not empirically asserted |
| Revision | Correction, qualification, amplification, deletion, unresolved disagreement or repetition |
| Downstream reuse | Later locations that repeat or transform the proposition |
| Reviewer | Human/AI contribution, initial judgment, disagreements and final rationale |

For each claim, ask what new evidence would change its status. This makes a disagreement scientifically productive and helps distinguish a correction from a more persuasive restatement.

## Preserve the value of the conversations

The records are strongest as examples of research behavior: proposing alternative explanations, noticing comparator weaknesses, separating measurements from projections, and revising uncertainty. They also demonstrate why a polished synthesis needs an evidence ledger. Keep both successes and failures; do not select only flattering excerpts from one attributed model.

The next empirical step is the accompanying controlled calibration protocol. The next documentary step is a focused full-text review of the claims that will matter to the eventual paper. Neither step requires accepting the original brand taxonomy or discarding the questions that motivated it.
