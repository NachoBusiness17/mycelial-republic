# Fine-tuned MedGemma 4B (LoRA) and 27B (QLoRA) for oncology on one DGX Spark. Also: a possible LoRA scale discrepancy under Unsloth, looking for independent reproduction

- url: https://reddit.com/r/LocalLLaMA/comments/1wywscq/finetuned_medgemma_4b_lora_and_27b_qlora_for/
- id 1wywscq | score 5 | comments 0 | created 1791273304
- url_in_post: https://www.reddit.com/r/LocalLLaMA/comments/1wywscq/finetuned_medgemma_4b_lora_and_27b_qlora_for/

## SELFTEXT

Public data only (5 datasets, 9 tasks, frozen quiz of 2,199 eval items, paired McNemar tests).

Overall accuracy: 4B 56.0% -> 71.6% (2h39 of training), 27B 68.8% -> 77.9%. The tuned 4B beats the base 27B (209 items gained, 149 lost, p = 0.002). Biggest gains on report extraction/classification (biomarker status 97.5% on test for the 4B). Weak spots: exact ICD-10 code (37.6% for the 27B), and MCQ accuracy collapses from val to test for all models, base included (cause unknown). 

What I would like a second pair of eyes on: merging. Merging the 4B adapter (r=64, alpha=16) at the nominal scale lost most of the tuning (83.8% agreement with the adapter on the quiz). Merging with alpha=32 gave 93.2%. Identity probes are consistent with an effective scale of \~2x alpha/r under Unsloth (7/7 under Unsloth at nominal; 0/4 under Transformers+PEFT at nominal, 4/4 at 2x), but this is NOT a demonstration: 

\- the two probes do not build their inputs the same way (Unsloth: gemma-3 template rendered as text, tokenized without special tokens; PEFT: tokenizer chat template straight to ids) and I did not check the sequences are identical; 

\- I did not measure the scale actually applied by a trained layer, nor find a mechanism; - the 27B probe is inconclusive (4/4 at nominal); 

\- my environment may be at fault: Unsloth installed with --no-deps, Transformers 5.18.0 and TRL 0.26.1 are outside the ranges declared on PyPI. I no longer have the GPU, so the direct check is not done. A script is in the Zenodo code: 74\_probe\_scale\_logits.py compares last-token logits under Unsloth and PEFT on identical token ids at several scale multipliers (0 = base model as control). It was only tested on a mock model, not on the adapter. If someone with a clean environment can run it, or knows whether this is expected behavior, I would love to hear it. 

Separately: bf16 rounding erases 17-37% of the delta elements on merge, so the quiz tasks survive but verbatim memorization (an oath text I trained on) does not. 

Models (merged + adapters): [https://huggingface.co/Grujowmi](https://huggingface.co/Grujowmi) 

Quiz: [https://huggingface.co/datasets/Grujowmi/OncoLLM-Quiz-Onco-v1](https://huggingface.co/datasets/Grujowmi/OncoLLM-Quiz-Onco-v1) 

Report (revised Oct 5, same DOI), code, results: [https://doi.org/10.5281/zenodo.23134374](https://doi.org/10.5281/zenodo.23134374) Research models, not medical devices. Other limits (one seed, no CV, no ablation) are in section 8.

## COMMENTS (0)

