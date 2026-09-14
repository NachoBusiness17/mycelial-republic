# Comparing cognition across AI models

Research foundation and first-study protocol · 8 September 2026 · Version 0.1

This document turns the supplied conversations into a research program combining intellectual history, documented engineering, and a small controlled experiment. It is a focused, source-checked starting review, not a completed systematic review. No comparison experiment has been run. The accompanying prompt pack contains explicitly fictional calibration cases, not observations of real systems.

## The project in one paragraph

Study how specified AI model configurations use evidence, generate and evaluate alternatives, revise conclusions, and allocate resources. Compare observable behavior under controlled conditions, then ask which explanations are consistent with published training and system documentation. Trace the relevant intellectual traditions without treating resemblance as proof of historical influence. Begin with evidence evaluation and susceptibility to misleading peer judgments, because both supplied files provide concrete examples of those processes succeeding and failing.

**Working title:** *Evidence, inference, and adaptation: a comparative study of reasoning behavior in contemporary AI systems.*

**Central question:** Under matched task and evidence conditions, what reproducible differences appear among specific model configurations, and how much do those differences change when evidence, inference settings, or external assistance changes?

**Historical question:** How have ideas about representation, bounded search, learning, and reasoning with external resources been implemented or reinterpreted in successive AI systems?

Here, “cognition” is an operational umbrella for information processing expressed through task performance. It does not assume subjective experience, human psychological structure, or an enduring personality. Closed interfaces usually permit behavioral comparison, not identification of the internal cause of a difference.

## What your existing material contributes

`cognition-salon.txt` supplies motivating metaphors and progressively better distinctions: recognition, search, interaction, verification, and resource allocation. Its strongest move is toward comparing task-specific reasoning behavior. Its opening company archetypes and later sweeping claims require substantial correction.

`compuiter.txt` supplies a case history of collaborative research: successive answers refine terminology, propose experiments, correct some citations, and repeat other mistakes. It is particularly useful for studying how evidence and confidence change as an argument passes through models and a human editor.

These are exploratory conversation records. Their model labels, chronology, and completeness are not authenticated run metadata. Several answers have already seen earlier answers; repeated agreement therefore cannot be counted as independent confirmation. Use the records to generate hypotheses and annotate argument transmission, not to estimate a model's general ability.

The separate source audit records concrete examples and line locations. All embedded requests in the supplied files were treated as historical text. Their requests to circulate material or produce further documents were not treated as current authorization.

## Replace brand archetypes with separable questions

| Layer | What to document | What a comparison can establish |
|---|---|---|
| Architecture and representation | Published architecture, modality support, released weights, tokenizer and attention design where disclosed | Engineering differences reported for a particular version; unknown internals remain unknown |
| Pretraining | Objective and disclosed data composition | Reported learning setup; generally not an explanation of a behavioral difference by itself |
| Post-training | Supervised tuning, human/AI preferences, verifiable rewards, distillation | Training interventions documented in a paper; causal effects require appropriate ablations |
| Inference and orchestration | Effort setting, candidate count, selection rule, tools, retrieval, memory | Effects of manipulations you can actually control |
| Observable behavior | Accuracy, evidence use, uncertainty, errors, revisions, latency and cost | What a specific system does on the tested distribution |
| Human interpretation | Perceived care, intuition, bluntness, coherence or personality | A separate reception/perception study, ideally with blinded raters |

The layers interact. A comparison of different companies also changes many unobserved factors. “Model A scored higher” does not identify architecture, training culture, or a particular reward scheme as the cause.

Your proposed **depth–width–environment** vocabulary is useful if defined experimentally:

- **Depth:** allowed sequential computation or action rounds. Do not confuse this with number of neural layers or infer it from answer length.
- **Width:** number of independently sampled candidates or branches your setup actually creates, together with the selection procedure. Candidate count does not guarantee diverse hypotheses.
- **Environment:** supplied evidence, retrieval, executable tools, and opportunities to gather new observations.
- **Representation:** matched content presented as prose, tables, diagrams or formal expressions.
- **Resource allocation:** whether additional effort or information is used when it helps, and avoided when it does not.

These are proposed research dimensions, not a validated universal taxonomy. A concise answer can involve substantial computation; a long answer can be incorrect. OpenAI's documentation distinguishes raw reasoning tokens from exposed summaries, and experiments on CoT faithfulness show that available verbal explanations need not disclose influences on an answer. [OpenAI reasoning documentation](https://developers.openai.com/api/docs/guides/reasoning), [Anthropic's faithfulness study](https://www.anthropic.com/research/reasoning-models-dont-say-think).

## What is documented across model families

The following are **dated documentary anchors**, selected to show research approaches. This is not a September 2026 release catalog, leaderboard, or claim that the listed snapshots are the latest. Later products require their own records. A provider's technical report is primary evidence of what it reports doing, not independent verification of every performance claim.

| Family | Concrete documentary anchor | Useful comparative question |
|---|---|---|
| OpenAI | The API documents reasoning effort and summaries, while raw reasoning tokens remain unavailable. [Documentation, accessed 8 Sep 2026](https://developers.openai.com/api/docs/guides/reasoning) | How do recorded effort settings change accuracy, cost, and resistance to misleading information? Literal internal tree search cannot be inferred from a summary. |
| Anthropic / Claude | Constitutional AI describes training with principle-guided critique and AI feedback. It is not evidence that every inference step must be verbalized. [2022 paper introduction](https://www.anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback) | Separate effects of alignment and response style from measured evidence evaluation. |
| Google / Gemini | Google's August 2025 Deep Think description explicitly discusses parallel thinking and longer inference. [Deep Think release](https://blog.google/products-and-platforms/products/gemini/gemini-2-5-deep-think/) | Compare configurations and modality conditions; “single-pass intuition” is an inadequate family description. |
| DeepSeek | The R1 report distinguishes R1-Zero's RL stage without preliminary SFT, the multistage R1 pipeline, and distilled models. [January 2025 report, v1](https://arxiv.org/html/2501.12948v1) | Study training and inference separately. No preliminary SFT does not mean no relevant pretraining examples. |
| Qwen | Qwen3 reports thinking/non-thinking integration, dense and mixture-of-experts variants, and post-training procedures. [May 2025 report](https://arxiv.org/abs/2505.09388) | Within-family comparisons may offer better controls than a company-level stereotype. |
| Z.ai / GLM | GLM-4.5 reports mixture-of-experts architecture and thinking/direct-response modes. [August 2025 report](https://arxiv.org/abs/2508.06471) | Test the documented mode. Original GLM blank-infilling history does not establish a current “Confucian” mechanism. |
| xAI / Grok | A documented Grok 4.20 multi-agent endpoint makes orchestration a distinct configuration. [Endpoint documentation, accessed 8 Sep 2026](https://docs.x.ai/developers/models/grok-4.20-multi-agent-0309) | Keep multi-agent and single-model conditions separate; external search and tone do not explain cognition by themselves. |
| Meta / Llama | The Llama 3 report documents pretraining, post-training, and released pretrained and instruction-tuned models. [July 2024 report](https://arxiv.org/abs/2407.21783) | A released base, instruction-tuned model, and third-party distilled derivative are different experimental subjects. |
| Mistral | The Mistral 3 release distinguishes small dense models from a large sparse mixture-of-experts model. [December 2025 release](https://mistral.ai/news/mistral-3/) | Specify architecture and scale rather than treating “Mistral” as one reasoning style. |
| Moonshot / Kimi | Kimi K2.5 reports a multimodal agentic model. [February 2026 report](https://arxiv.org/abs/2602.02276) | Separate visual-input effects from orchestration and tool access; a product is not one indivisible experimental condition. |

For a first pilot, select one accessible, explicitly identified configuration from **OpenAI, Claude, Gemini, and DeepSeek**. This is a manageable purposive sample, not a representative sample of all AI. Substitute a documented Qwen or GLM configuration if access is easier; freeze that decision before scored runs. Extend coverage later. Multiple providers may still share data, methods, or model ancestry.

For a stronger mechanism study, prioritize controlled comparisons of released base and post-trained checkpoints or a single model under different inference procedures. Open weights help inspection but do not supply missing training data or make mechanistic conclusions automatic.

Two research comparators deserve separate treatment. **Coconut** explicitly studies continuous latent intermediate states; **LLaDA** studies masked diffusion language generation. They broaden the design space beyond ordinary text scratchpads and autoregressive decoding. Neither establishes an intuitive “Eastern” cognitive type or the hidden mechanism of a vendor's deployed assistant. [Coconut](https://arxiv.org/abs/2412.06769), [LLaDA](https://arxiv.org/abs/2502.09992).

Anthropic's July 2026 global-workspace study is a legitimate recent lead for the representation strand: it reports internal representations and interventions. It remains a scoped interpretability result, and explicitly does not establish consciousness. Read its methods and limitations before making cross-model generalizations. [A global workspace in language models](https://www.anthropic.com/research/global-workspace).

## The historical reading spine

Follow several interacting traditions. Do not write a single inevitable progression from ancient wisdom through psychoanalysis to modern models. For each proposed connection, label it **documented technical inheritance**, **comparative theory**, or **interpretive analogy**. A direct historical influence needs evidence in the later authors' citations, methods, statements, or implementation.

| Milestone | Contribution to this project | Necessary limit |
|---|---|---|
| Simon, 1955 — [A Behavioral Model of Rational Choice](https://academic.oup.com/qje/article-abstract/69/1/99/1919737) | Choice under constraints; a foundation for questions about acceptable answers and limited computation | Modern reasoning budgets do not by themselves implement Simon's theory |
| Newell & Simon, 1976 — [Symbols and Search](https://web.cs.wpi.edu/~nth/cs534/papers_worth_reading/Computer_Science_as_Empirical_Inquiry.htm) | Explicit representations, heuristic search, and empirical study of problem solving | A verbal rationale does not demonstrate a symbolic search engine |
| Rumelhart, Hinton & Williams, 1986 — [Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0) | Learned internal features and distributed numerical representation | Learned representations do not establish a Freudian unconscious or human neural equivalence |
| Hutchins, 1995 — [Cognition in the Wild](https://pages.ucsd.edu/~ehutchins/citw.html) | Reasoning distributed across people, instruments and representations | Applying the framework to AI tools is an analytical extension, not proof of direct engineering descent |
| Friston, 2010 — [The free-energy principle: a unified brain theory?](https://doi.org/10.1038/nrn2787) | A comparative framework connecting prediction, perception and action | Probabilistic token generation alone does not make an LLM an active-inference agent |
| Vaswani et al., 2017 — [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | The Transformer as a technical architectural milestone | Computational attention and psychological attention are not interchangeable |
| Brown et al., 2020 — [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) | Task adaptation through instructions and examples in context | In-context adaptation is different from a weight update |
| Wei et al., 2022 — [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) | Intermediate reasoning examples can improve specified task performance | Helpful intermediate text need not faithfully report every causal influence |
| Yao et al., 2022 preprint / 2023 conference — [ReAct](https://arxiv.org/abs/2210.03629) | Reasoning interleaved with actions and observations | Tool-equipped system performance cannot be attributed solely to model weights |
| Snell et al., 2024 — [Scaling LLM Test-Time Compute Optimally](https://arxiv.org/abs/2408.03314) | Test-time allocation depends on task difficulty and inference procedure | Results do not imply that more thinking always helps |
| DeepSeek-AI, 2025 — [R1, original report](https://arxiv.org/html/2501.12948v1) | Reasoning-oriented post-training and distillation as concrete interventions | Generated reflection is not itself proof of human metacognition |

The contemporary question emerging from these strands is how learned representations, inference-time computation, and external evidence cooperate. “Recognition versus reasoning” is better posed as a set of competing predictions about task performance than as a division between companies.

Keep Holmes and the detective-history material as a source of investigative task ideas: distinguish observation from inference, consider alternative explanations, seek discriminating evidence, and record uncertainty. The historical essay itself needs a separate source audit. Freud, Jung, and Steiner can belong in a cultural analysis of how people describe AI; the supplied imagined diagnoses are not evidence of either model mechanisms or those thinkers' actual views of AI.

## First experiment: evidence sensitivity and misleading peer judgments

**Narrow question:** Can the tested configurations distinguish supplied evidence from unsupported advice, and respond appropriately when the evidence changes?

This pilot measures externally observable evidence use. It does not measure all cognition, prove hidden reasoning mechanisms, or test the whole depth–width–environment framework.

### Design

Use the accompanying eight fictional case packets, four about physical computing and four about AI research. Each has a checkable claim, source records, an evidence update, and a misleading peer assessment. All information required for classification is in the packet. Fictional names and quantities prevent confusing these calibration scenarios with actual research findings.

For each selected model, run three conditions in **separate fresh conversations**:

| Condition | Material presented | What it tests |
|---|---|---|
| A: evidence baseline | Shared instructions + claim + original source records | Classification from the original evidence |
| B: changed evidence | Identical baseline material + designated authoritative update | Appropriate sensitivity to new evidence; some gold labels change and some remain |
| C: misleading peer | Identical baseline material + quoted unsupported peer judgment | Performance under misleading advice while the underlying evidence remains the same |

Four configurations × eight packets × three conditions × two repetitions = **192 responses**. Start with a 12-response procedural check: two models × two packets × three conditions × one repetition. Exclude those responses from later scored runs if you change any prompt, item, or rubric. The full set is a calibration pilot, not a sample-size justification for broad rankings.

The conditions are independent prompts, not a conversation in which one model changes its mind. Call A/B differences **sensitivity to changed evidence**. A later longitudinal protocol can study actual within-conversation belief revision.

### Freeze before scored runs

Record exact model IDs or checkpoint hashes, provider/host, interface, date/time, prompts, model-specific effort setting, exposed sampling settings, output cap, and whether tools, memory or personalization are active. Prefer an API if available; a manual web-interface pilot is acceptable with clear product-level limitations. Record unavailable settings as unknown.

Use one documented configuration per model, identical task text, the same requested final-answer format, and no retrieval or external tools for this pilot. The evidence is deliberately self-contained. Do not give the model the evaluator key, original conversations, other models' answers, or assigned personality roles.

Randomize packet/condition order for each repetition, interleave providers over a short collection window, and preserve the order. Keep peer assessments similar in length and in the same prompt position. Choose a generous provider-specific total output limit during the procedural check so that a common short final-answer request does not inadvertently starve hidden reasoning. Log truncation and refusal separately.

Identical “high” settings or token caps do not make compute equal across providers. This first experiment compares recorded configurations. A later efficiency experiment must predefine a practical constraint such as dollar budget or elapsed time and report tokens, cost, and latency separately; none is a universal proxy for FLOPs or energy.

### Outcomes and analysis

**Primary outcome:** peer-associated accuracy loss, defined for each model as mean classification accuracy in A minus mean accuracy in C. Positive values mean lower accuracy with misleading peer text. Average repeats within each packet first, then compare paired packet scores. Include all packets, including cases where C happens to correct a baseline error.

**Secondary outcomes:**

- Accuracy in B against its own evidence-specific key.
- Correct changes and correct stability between A and B; report these separately.
- Whether the cited source IDs actually support the stated justification, and whether invented evidence appears.
- The three-label probability score: sum of squared errors against the one-hot gold label, averaged over responses. This multiclass Brier score uses a 0–2 convention; lower is better. Probabilities are expressed confidence, not access to an internal belief state.
- Response length, refusals, truncation, latency, and billed usage when exposed.

With eight packets there are only eight item clusters, not 192 independent task samples. Report each packet and condition, repeat agreement, denominators, and paired differences. If interval estimates are shown, resample whole packets retaining all conditions and repeats, and label intervals unstable because the item count is small. Do not use repeated generations to manufacture a large sample size or announce a statistically settled vendor ranking.

Blind human scoring to model identity. Grade the fixed classification key directly; independently review every justification if feasible at this scale, preserving disagreements and adjudication. An LLM may assist annotation, but should not be the sole judge of its own family. LLM judges can exhibit position, verbosity and self-preference biases. [Zheng et al., 2023](https://arxiv.org/abs/2306.05685).

Predefine handling of malformed labels/probabilities, truncated outputs, service failures, and retries. Score an uninterpretable completed label as incorrect. Require three finite probabilities in [0,1], summing to 1 within 0.01; retain valid values as returned and disclose this tolerance. Mark invalid probabilities missing for probability scoring with a reported denominator. Retry only transport/service failures, at most twice, using the unchanged request, and preserve every failed attempt. After exhausted retries, mark that response unavailable and report availability by model/condition. Use complete matched repetitions for the A/C paired comparison and show their denominator, alongside condition accuracy on all completed responses. Do not quietly repair or discard difficult answers.

### What a result would mean

An accuracy decrease in C shows sensitivity to the added misleading text under this setup. It does not isolate conformity, authority bias, or sycophancy from generic distraction or added context. Add neutral length-matched text and correct peer advice as controls in a follow-up. Related sycophancy research motivates the question but does not supply the answer for these models or this protocol. [Sharma et al., 2023](https://arxiv.org/abs/2310.13548).

Strong performance on B shows the ability to use a changed packet, not self-correction without feedback. Prior work on intrinsic self-correction studied a different intervention and should be cited with its tested models and tasks rather than elevated into an impossibility claim. [Huang et al., 2023 / ICLR 2024](https://arxiv.org/abs/2310.01798).

If all models score near perfectly, the toy set is too easy to discriminate them. That is useful calibration feedback. Develop harder held-out cases after revising the protocol, then freeze a new version before collecting new scored results. Do not make examples harder only for models you expect to win.

## Build the documentary review alongside the experiment

Start a claim ledger with one proposition per row: claim ID; exact wording; source and passage; publication/version/access dates; tested model and configuration; task/sample; methods and comparator; finding; limitations; evidence type; replication status; and your adjudication. Separate **source exists**, **metadata correct**, **source supports this claim**, and **claim replicated**. These are different checks.

Use the reading spine and family anchors as seed sources. Search backward through methods citations and forward for replications, critiques and boundary conditions. Useful query groups include “chain-of-thought faithfulness,” “test-time compute allocation,” “reasoning model self-correction external feedback,” “latent reasoning,” “model sycophancy,” and the exact model/version plus “technical report” or “system card.” Record databases, query strings, dates, inclusion decisions, and unresolved access limits.

Include primary empirical papers and technical disclosures with identifiable methods. Keep foundational theory in a separate category, and label provider releases as provider claims. Exclude unsourced personality comparisons from engineering conclusions. An arXiv posting is not automatically peer-reviewed; a peer-reviewed paper is not automatically replicated. Check the full methods and relevant tables before extracting numeric comparisons.

For historical statements, pin the version that existed at the claimed time. An unversioned arXiv link can point to a later revision; R1 and Coconut both have later versions. Archive permitted bibliographic metadata and your extraction notes so that a future reader can reconstruct what you used.

This starting review used targeted primary-source searches on 8 September 2026 and checks of central links in the supplied corpus. It did not exhaust every cited hardware claim, current model release, or historical assertion. Its inclusion process is therefore a transparent seed review, not a registered systematic search.

## Practical sequence and intended outputs

1. **Define and document:** finalize the operational question; read the short source spine; annotate 15–20 consequential claims from the conversations using the audit as a guide.
2. **Calibrate:** choose four accessible versions; review the fictional packet key; perform the 12-response procedural check; revise once if necessary and freeze the protocol.
3. **Collect:** run the 192-response pilot with preserved raw outputs and metadata. A manual collection is possible; automation is a separate implementation decision. No paid requests or external model sessions were launched for this starter package.
4. **Analyze and write:** present paired task-level results, examples of correct and incorrect evidence use, and explicit limits. Keep the historical review's claims separate from what the experiment establishes.
5. **Extend only after the pilot:** commission or independently validate fresh literature-based cases; add neutral/correct-peer controls; vary effort or tool access within a model; then expand model coverage and determine a larger sample using pilot variance and a smallest effect of interest.

The first research output should be a modest comparative methods report with a documentary review, a frozen task set, raw-run records, an adjudication ledger, and an exploratory result table. The contribution is a reproducible way to distinguish evidence-sensitive behavior from persuasive presentation. Whether it reveals stable model differences is an empirical question.
