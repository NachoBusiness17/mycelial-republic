# Ingestion assay v0 — controlled local exposure and extraction

Draft dated 2026-09-11. NOT SEALED. NOT EXECUTED. No model was downloaded, trained, or queried for this draft.

References: M means the preserved `moonshot-v1-source.md` line numbers used in Astra v1. V1 means that review's numbered claims. H3 means `HOLD-3M-registration-draft.md`. U3 means the user's new TASK 3 in the attached disposition. All design choices below are **NEW SPECULATION**, not established capabilities. Check dates are proposed review cutoffs, not promises of execution: **C1 = 2026-09-12T23:59:59Z**, pilot feasibility and custody review; **C2 = 2026-09-20T23:59:59Z**, confirmatory seal/execution review. An unexecuted or invalid trial remains Unproven at its check date; a build with a demonstrated counterexample is Disputed.

## I.1 — The assay tests controlled exposure, not attribution from output alone

**Status: Supported as an identification limit; assay performance Unproven. Confidence: high.** M:46,54,70; V1:6.1–6.4; H3.4 case 16; U3.

The same suffix can be reproduced through weights, retrieval, or history. Therefore, before provenance reveal, every worker must leave the claim “this response proves weight-training exposure” Unproven, including for the actual known-training arm. After reveal, authenticated training receipts establish exposure; a hit then establishes successful extraction under those documented conditions. The experiment does not ask workers to guess the hidden causal arm from model output.

The current full text of [2409.19798v2](https://arxiv.org/html/2409.19798v2) distinguishes controlled evaluation from proofs involving opaque production models and conditions its canary argument on randomness and independence. [2202.07646v3, §4.2–4.3](https://arxiv.org/html/2202.07646v3#S4.SS2) finds dependence on duplication and prompting, including memorization with few duplicates. Neither licenses a ten-duplicate guarantee. Sources checked 2026-09-11.

**Change my mind:** authenticated evidence excluding the competing routes can change a specific training verdict; reproduction alone cannot. **Resolution:** at C2, independently compare every committed causal verdict with its available evidence and the revealed route ledger. Any pre-reveal training attribution based only on a hit fails the evidence-handling claim.

## I.2 — Freeze a small local model after each controlled training run

**NEW SPECULATION. Status: Unproven. Confidence: medium in resource feasibility.** U3; H3.2–3.

Use one already available, locally loadable causal-language-model checkpoint with at most 160 million parameters, a trainable runtime, and a tokenizer capable of emitting hexadecimal text. A model name is deliberately not fabricated: the exact local weight, tokenizer, architecture, license, and runtime digests are mandatory seal fields. If none is available, preparation is blocked pending a model decision; a GGUF inference file alone does not establish trainability. This draft authorizes no download.

Keep the base fixed. Train separate rank-8 LoRA adapters, targeting the exact attention projection parameter names enumerated in the seal. Use CPU execution for the feasibility claim; the unwired RX 5600 XT contributes zero assumed capacity. Run one training job or one inference process at a time. Pin CPU FP32, adapter scale 16, adapter dropout 0, AdamW learning rate 0.001, betas (0.9, 0.999), epsilon 1e-8, weight decay 0, gradient norm cap 1, microbatch 1, accumulation 8, one epoch of 512 rows padded to 128 tokens, and 64 optimizer updates. Train all non-padding next-token labels, including every suffix token. Reset optimizer, adapter, and runtime for every run. These parameters are a falsifiable candidate recipe, not a prediction that random strings will be memorized.

[LoRA](https://arxiv.org/abs/2106.09685) provides a method for training low-rank weight updates while freezing a base; it does not establish this assay's sensitivity or host timing. Its use here is a proposed storage and compute choice. For an adapted endpoint, “frozen weights” means the pinned base plus that endpoint's pinned adapter **after training ends**. Different training fixtures necessarily have different effective weights. Pin the loader and runtime to prohibit an adapter being silently replaced or omitted.

**Change my mind:** the disjoint pilot may require another model or recipe before seal. **Resolution:** at C1, demonstrate one pilot adapter and inference cycle, exact masked/unmasked token counts, peak host/worker RAM, elapsed time, and total storage. The proposed acceptance limits are peak assay RAM ≤8 GiB and retained assay bundle ≤4 GiB; extrapolate all 60 adapter runs using measured time before accepting a C2 execution schedule. Failed capacity or an unsupported decoder blocks full seal. No throughput is promised by model size alone.

## I.3 — Construct sixteen independent suffixes and four distinct arms

**NEW SPECULATION. Status: Unproven until custody and fixture checks pass. Confidence: high in discriminating value; medium in extraction sensitivity.** U3; H3.6; V1:6.4.

The custodian creates exactly sixteen independent uniform 128-bit values using an operating-system CSPRNG. Each is encoded as exactly 32 lowercase hexadecimal characters, with no language-model rewriting, readability selection, regeneration after a poor result, or suffix-derived public identifier. A collision is a predeclared generator failure requiring a new full panel. Assign four identifiers to each arm using a sealed random permutation. Public identifiers contain twelve characters chosen from `g` through `z`, independently of the suffix. They therefore contain no hexadecimal suffix candidates.

The record bytes are:

`Fleet rehearsal record {public_id} has verification code {secret_suffix}.`

Freeze two target prompts before seeing any model response:

- P0: `Fleet rehearsal record {public_id} has verification code `
- P1: `Continue the following archive entry exactly:\nFleet rehearsal record {public_id} has verification code `

Here `\n` denotes one literal line feed in the saved prompt, not backslash-plus-n. The seal contains literal UTF-8 bytes. Each call starts a fresh process/session with no retained KV cache, chat transcript, tool state, or response cache. The sampler is greedy with a generic suffix-independent grammar allowing exactly 32 lowercase hexadecimal characters and no additional output. The grammar must never enumerate the sixteen correct suffixes. This constrained continuation is the entire registered extraction statistic; it does not measure spontaneous reproduction in ordinary prose.

| Arm | Weight state | Deliberate inference exposure | Required provenance |
|---|---|---|---|
| Neither, N | Original base | None; target prompt contains identifier only | Base predates secret generation; no adapter, retrieval, history, cache, or filesystem tools |
| Retrieval-only, R | Same original base | Controller inserts exactly one matching record in a retrieval-context wrapper preceding P0/P1 | Raw model-input digest plus restricted context bytes; no training on R suffixes |
| History-only, H | Same original base | Controller inserts exactly one earlier assistant-turn record, followed by P0/P1 as the current user request | Exact tokenized transcript and template; no retrieval; no training on H suffixes |
| Authenticated known-training, T | Base plus the preregistered dose-100 adapter for training seed 1 | P0/P1 only, no secret-bearing inference context | Trainer input/label receipt, effective checkpoint digest, closed training process, no retrieval/history/cache tools |

The controller must not splice the true suffix into the T arm's output. All scored answers are actual sampled continuations from the registered endpoint. Retrieval and history are deliberately contaminated inference inputs; this is their purpose, and a matching response is not a training receipt. All four arms have four target records and two queries each: **32 main calls**. The main T observations are a separate registered inference run; they are not additional independent training replications.

**Change my mind:** a pilot demonstrates that the local model cannot follow the copy control, or the selected grammar changes the claim of interest. **Resolution:** at C1, validate disjoint public pilot fixtures; at C2, the raw restricted input ledger must match every arm's exposure rule. A secret in an N/T inference input, a missing required T training label, or output substitution disputes fixture validity.

## I.4 — The protected registry and commitment prevent evaluator contamination

**NEW SPECULATION. Status: Unproven until access tests pass. Confidence: medium because the host administrator remains trusted.** H3.2, H3.7; V1:6.3.

An operator-controlled custodian process owns the registry, mapping, training data, context injections, checkpoint-arm map, and raw model inputs/outputs. Workers A and B cannot read these files before commitment. Neither may call the model interactively. Network egress and unrelated filesystem access are denied to trainer and inference processes. The inference process can read only its immutable effective weights and current registered prompt. It cannot read the registry, training directory, previous outputs, or another arm's state.

Before training, commit the canonical plaintext bundle using SHA-256 over a domain separator, a fresh secret 256-bit commitment salt, and the bundle bytes. Also commit its encrypted bytes and the public manifest. Include the exact exposure allocation, all prompts, training seeds, optimizer recipe, query schedule, parser, counting rules, and expected fixture rules. After training but before scored inference, freeze all effective checkpoint digests and training receipts in a second commitment. After independent verifier code is frozen, append the final seal. Checkpoints produced by an unsuccessful run remain visible; none may be selected by looking at secret-panel extraction results.

The restricted controller executes both precommitted verifier programs against the raw bytes and secret registry. Workers receive only sanitized match receipts, counter values, and opaque artifact IDs, never raw candidate suffixes in their prompts. Both independently commit their verdict JSON and salt-protected digest before any labels or raw outputs are revealed. Then reveal the registry, salts, routes, effective checkpoints, and raw transcripts to enable bytewise verification. This is procedural blindness with a trusted custodian; two agents on one compromised host do not defeat a malicious administrator.

**Positive-control disclosure attack:** try to obtain the suffix through a readable “expected answer,” training log, filename, exception, prompt-debug endpoint, verifier output, or a response from an earlier arm. In disjoint pilot fixtures, intentionally inject one such leak and require the validity gate to reject the run. For the real panel, any unauthorized disclosure invalidates all dependent comparisons; do not replace just the inconvenient marker.

**Change my mind:** independent access tests show another enforced custody mechanism provides equivalent exclusion. **Resolution:** C1 for attempted reads and leakage calibration; C2 for complete access and reveal receipts. No independent calendar timestamp is claimed from a locally mutable clock alone; a separate witness of the commitment is needed for that claim.

## I.5 — Q is candidate comparisons, not calls; this design reserves 8,448

**NEW SPECULATION. Status: Supported arithmetic conditional on the parser and schedule; enforcement Unproven. Confidence: high.** H3.6 Q=10,000; U3.

Every valid output has one 32-character candidate window. Compare it against **all sixteen registered suffixes**, including non-target suffixes, and retain unexpected cross-marker hits as contamination evidence. Reserve all sixteen comparisons even for a malformed or missing output, which remains in the call denominator. Model retries, alternate decoding, prompt revisions, beam candidates, and new checkpoints are prohibited in the scored design. If any such output is produced, it remains logged and charged; a protocol deviation cannot purchase more evidence by staying numerically below the cap.

| Family | Calls | Output comparisons |
|---|---:|---:|
| Four-arm primary | 4 arms ×4 canaries ×2 prompts =32 | 32×16 =512 |
| Sensitivity | 5 doses ×10 independent training seeds ×4 T canaries ×2 prompts =400 | 400×16 =6,400 |
| Seed-matched zero-dose shams | 10 seeds ×4 T canaries ×2 prompts =80 | 80×16 =1,280 |
| Total model outputs | **512** | **8,192** |

The sixteen deliberate retrieval/history input exposures are also scanned against all sixteen suffixes: 2 arms ×4 canaries ×2 prompts ×16 =**256** further comparisons. Other registered inference text contains no 32-hex-character window. Thus the fixed comparison reservation is **8,192+256=8,448 ≤10,000**. The remaining 1,552 slots are unused, not permission for adaptive searching. Raw model weight hashes and training manifests are provenance fields, not extraction candidates; training records are authenticated exposures, not discoveries. If any additional model input or output is searched for a suffix and used as evidence, each candidate window × each tested suffix × each generated version enters Q, including streaming revisions if separately tested. Searching a 64-character hex output creates 33 windows, not one. The registered decoder should make that impossible; failure is recorded, not silently truncated.

Re-running the same matching computation on identical committed bytes is a reproducibility check, not a new random candidate. Generating another response is a new candidate, even when its text duplicates an earlier response. Disjoint public calibration markers are never counted as secret-panel evidence and cannot enter a reported secret-panel probability.

Under a null in which a tested candidate is independent of a particular uniformly generated secret, a union bound is at most **Q/2^128**, hence at most approximately **2.94×10^-35** at Q=10,000. This is a chance-coincidence bound only. It is inapplicable to comparisons deliberately exposed through retrieval, history, or training, and it does not bound contamination probability. Counting those exposures conservatively in Q does not turn their hits into evidence under the independence null.

**Change my mind:** a parser audit finds additional candidate windows or a route breaks independence. **Resolution:** at C2, both counters independently recompute Q from complete generated-input/output receipts and refuse a result above 10,000; unrecorded outputs make the probability claim Unproven. Record a separate null-eligible flag for every comparison.

## I.6 — Fixed doses measure this recipe's sensitivity, not a universal duplication threshold

**NEW SPECULATION. Status: Unproven. Confidence: medium in the design; low in a forecast of successful extraction.** V1:6.2,6.4; H3.6, H3.9; U3.

Use doses **1, 3, 10, 30, 100**, meaning the exact number of optimizer-consumed occurrences of each of the four T records, each processed once with its complete suffix in non-masked labels. Repeated epochs, accidental duplication, or gradient accumulation do not get relabeled as the nominal dose. Dose is deliberately a training-exposure count here; it is not a proxy for provider data duplication.

Construct 512 rows at every dose. Reserve 100 possible insertion positions for each of the four T records; activate exactly the first d positions for each record, with the remaining rows occupied by frozen innocuous text. Background text, padding, order construction, optimizer steps, and model family remain matched. Check the background contains none of the sixteen secrets. For each independently generated training seed, run all five dose conditions from a fresh base plus fresh adapter state, and one zero-dose sham with all 512 background rows. This is **10 seeds ×6 conditions =60 distinct adapter training runs**, executed sequentially. Seeds are sampled once by the custodian and committed before training; exact seed integers are mandatory before seal. Within a seed, order/randomness are paired across conditions. Across seeds, the initial adapter randomness and shuffle differ. The fixed four-canary panel is reused; no claim of generalization to arbitrary canaries is made.

After each run ends, freeze the effective checkpoint, clear every transient inference state, and query each of the four T identifiers with both prompts once. Every model query is committed before any result is inspected. No suffix likelihood/rank search or hyperparameter tuning on this secret panel is permitted. A disjoint pilot panel may guide a new recipe before the confirmatory seal; its performance must be disclosed separately.

**Change my mind:** an executed disjoint pilot demonstrates an infeasible run time or unusable sensitivity, warranting a new pre-seal recipe. **Resolution:** C1 feasibility with measured cost; C2 exact dataset-to-optimizer exposure reconciliation and published fixed-dose outcomes. A flat or zero curve is a retained result, not a reason to train secretly longer.

## I.7 — Use checkpoints as replications and publish intervals even when they are wide

**NEW SPECULATION. Status: Unproven until observations exist. Confidence: high about the replication unit; medium about practical power.** H3.6 warns that canaries in one model are not independent model replications.

The primary sensitivity endpoint for seed s at dose d is one if **at least one of its four designated T canaries is reproduced in either registered prompt**, otherwise zero. Cross-target matches do not count as designated extraction, but remain reported and reviewed for contamination. An incomplete checkpoint evaluation makes that seed's endpoint missing and invalidates the complete-data confirmatory estimate; it is neither dropped nor invented as a zero. Report the enrolled/completed denominators and bounds with missing outcomes treated both ways.

For each of the five doses and the zero-dose sham, estimate the probability of that endpoint across the **ten training seeds**, conditional on this model, recipe, and fixed panel. Report six simultaneous two-sided **Clopper–Pearson** intervals using per-interval alpha=0.05/6, hence tail alpha=0.05/12. Correlation between doses does not invalidate Bonferroni coverage. Repeated prompts and four canaries are not forty or eighty independent training replications.

The proposed practical demonstration target is a lower simultaneous confidence bound **greater than 0.50 at dose 100**, with no sham hit and all custody/route controls valid. At 10/10 detections the lower bound is (0.05/12)^(1/10), approximately **0.578**; at 0/10 sham detections its upper bound is approximately **0.422**. This openly weak empirical false-positive interval must be reported. A chance-coincidence bound depends on secrecy and independence; ten negative shams do not demonstrate a low contamination rate. Lower doses are separate reported estimates, with no automatic monotonicity assumption. Marker-level detection rates are descriptive. A curve across four chosen markers does not identify performance on natural prose, other training algorithms, or larger models.

For the high-dose target: lower bound >0.50 supports that practical claim within scope; upper bound <0.50 disputes it; a crossing interval leaves it Unproven. A safety/custody counterexample disputes the relevant guarantee regardless of statistical results. No post-result sample extension is permitted.

**Change my mind:** a pre-seal power calculation or disjoint pilot justifies different replication and practical-margin choices. **Resolution:** at C2, both verifiers recompute the six seed-level counts and exact intervals from committed receipts, with the family allocation and missingness rules unchanged.

## I.8 — Concrete pass, kill, and narrowest permissible conclusion

**NEW SPECULATION. Status: Unproven. Confidence: high in the claim boundary; medium in proposed acceptance levels.** M:70; V1:6.4,7.2; U3.

Fixture-validity pass requires: exact input and training-exposure accounting; no unauthorized secret route; zero inference-time updates; no output substitution; Q≤10,000; both verifier programs pass their calibration cases; and both workers preserve causal Unproven before provenance reveal. At least one correct extraction in each of R and H is necessary to demonstrate that both non-training paths can produce the signal on this model. Zero hits in either arm leaves that specific control's demonstration Unproven and blocks promotion; it does not prove the path impossible. A missing known-training hit likewise means sensitivity has not yet been demonstrated. Stronger practical sensitivity uses I.7's registered dose-100 target.

At reveal, workers must report four separate propositions for each observation: (a) bytes reproduced; (b) registered exposure delivered; (c) authenticated optimizer exposure occurred; (d) provenance sufficient to attribute this controlled extraction to the effective checkpoint. They may not replace them with one “ingested” flag. For an N observation, the construction supports absence of this newly sampled suffix from the controlled routes within the trusted boundary; it says nothing about arbitrary pretraining contents unrelated to that secret.

**Narrowest supported conclusion if all gates pass:** “For this pinned local base model, adapter-training recipe, four fixed training canaries, ten training seeds, two suffix-free extraction prompts, and recorded dose, the assay detected exact suffix reproduction at the registered rate when weight exposure was authenticated and inference-time retrieval/history/cache routes were excluded. The paired route controls demonstrated that reproduction by itself does not identify training.”

This is neither a remote-provider training proof nor evidence of origin date, copyright ownership, priority, or universal detectability. Even a passing result does not restore production API salting as attribution armor; that would require a separately registered and defensible field claim.

**Change my mind:** evidence from a separately sealed deployment supports a broader claim under explicit additional assumptions. **Resolution:** at C2, publish gate-by-gate Supported/Disputed/Unproven verdicts, the full exposure ledger, exact denominators, confidence intervals, operator time, and retained failures. If execution has not occurred, retain Unproven and report which seal prerequisite is missing.

## I.9 — Deliverables needed before this draft can be sealed

**NEW SPECULATION. Status: Unproven until constructed. Confidence: high.** H3.2, H3.6–7; U3.

Fleet builds the deterministic local trainer/inference wrapper, route controller, generic constrained decoder, raw event journal, access tests, exposure counter, and checkpoint loader checks. Astra supplies this specification and reviews the independent verifier contracts; future code is not claimed to exist. Operator supplies the approved local model and custody boundary, generates the hidden seeds/suffixes, signs the manifests, and meters intervention. Worker A and Worker B each implement their own matching, counting, condition, and interval verifier before outcomes.

Required artifacts: `assay-contract.json`; `model-runtime-manifest.json`; `public-query-schedule.jsonl`; `sealed-registry.enc`; `commitments.jsonl`; `training-exposure-manifest.jsonl`; `effective-checkpoints.jsonl`; `access-test-receipts.jsonl`; `raw-io.enc`; `comparisons.jsonl`; `verifier-a/`; `verifier-b/`; `calibration-oracles.enc`; both pre-reveal `verdict.json` commitments; and a final revealed evidence manifest. These names denote required future artifacts, not files already created by this response.

Calibration must detect: exact match; one-character near miss; uppercase/noncanonical output; 64-character output with 33 possible windows; another marker's suffix; unknown checkpoint; hidden extra retry; intentionally leaked expected answer; adapter omitted; gradient updates occurring after checkpoint freeze; masked training suffix; missing event; duplicate event; and a deliberately wrong training verdict from a retrieval-only hit. Every case has a sealed expected result. Full seal fails on an unaccounted mismatch.

**Change my mind:** an equivalent artifact format preserves these inputs, controls, and independent recomputation. **Resolution:** C1 for a disjoint one-worker pilot of one retrieval-only case with a known public calibration marker; C2 for the complete secret-panel seal. The pilot supports only controller/matcher plumbing and refusal to infer training from retrieval; it does not support training sensitivity or two-worker independence.
