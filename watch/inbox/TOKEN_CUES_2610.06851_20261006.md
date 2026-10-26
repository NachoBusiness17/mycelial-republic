# LINK-DROP receipt: token cues recover RL gains on base models

- Dropped: 2026-10-06, X https://x.com/arXivBangers/status/2107534160856527155 -> arXiv https://arxiv.org/abs/2610.06851 (the tweet's arxivb.org link is the mirror-class aggregator; fetched the real arXiv abs page, 43,482 bytes, first-hand)
- LINKS row: seq 1791314753683718, canonical sha256 2DC482B578BD272E...
- Authors: Sophie L. Wang, Amil Dravid, Rulin Shao, Kevin Farhat, Sewon Min, Alexei A. Efros. Submitted 5 Oct 2026.
- Verdict: STEAL, high leverage, $0 to act on (local fleet).

## What it IS (from its own bytes)

Verbatim: "fixing particular starting token cues makes a base model's performance competitive with that of its reinforcement learning (RL)-trained counterparts on math and coding. For instance, the cue '.\n\nOkay' raises Olmo-3-7B's MATH-500 pass@1 accuracy from 42% to 78%, while 'Alright,' raises Qwen3-14B's from 72% to 87%."

Verbatim: "RL makes these cues more likely, while fixing them recovers much of its performance gain over the base model." And: "We perform causal data interventions to turn an arbitrary word, such as 'chicken', into an effective reasoning cue" - "a similar edit makes the prompt instruction 'Think duck duck goose' as effective as 'Think step by step'".

Verbatim: "the hidden state representations induced by different cues correlate with different document types from the training set." Plus a safety case: "different cues elicit distinct refusal and compliance behaviors that correspond to different types of training data."

## Estate mapping (four-way convergence)

1. HyperThink (2610.03039, banked 10-05): a VQ codebook of reusable bias patterns vs this paper's reusable token cues - the same organ in weight space vs token space. The d07-hyperthink-quantizer lane in the live burn (dwfrun-5de02c51) probes our pack's domain clustering; cues are the zero-training twin.
2. Sharpening Tax (Meta, banked 10-04): post-training trades coverage for pass@1. This paper names WHAT most of RL's pass@1 gain is: a likelier starting cue over reasoning the base model already contains. Coverage doctrine gets a decode-time lever.
3. Thinking-mode-is-the-axis law: cue is another axis on the same law, and it is free (no inference cost, no training, no params). Per-animal harness profiles (RIB_MODEL_GATES) gain a dimension.
4. Fleet coverage (EG-20: fleet 0.586 vs best single 0.500, cheap mesh 0.349): cues are a diversity axis for same-model fleets - cue-induced hidden states correlate with different training-doc types, so cue-varied same-model fleet may be a stronger cheap mesh than temperature-varied. Directly measurable against the D6 monoculture proxy (agreement 0.117).
5. The reasoning-burn one-bug (RIB_INFERENCE_BUDGET): cue choice is a candidate lever on reasoning-token burn and the EMPTY_REASONING class - untested, one probe away.

## Steal rows (one seat one sitting each)

- S1, high: cue-lift battery on the local garden - one fixed ~50-item math subset, 3 arms (no cue / '.\n\nOkay' / 'Alright,'), gemma:2b plus two more garden animals, pass@1 per arm, banked as a receipt. All local, $0, instruments exist (route_chat / model_garden).
- S2, high: FAMILY_TABLE cue column - mag/inference_budget.py gains a per-animal measured-cue profile wired like the thinking-control law (explicit, measured, synced to memory/behavioral/animals).
- S3, medium: cue-diversity fleet probe - re-run the smallest consensus-gate fleet probe with cue-varied same-model arms vs temperature-varied arms; does cue diversity beat temperature for the cheap mesh?
- S4, medium: cue vs reasoning-burn probe - one deepseek-v4-flash arm measuring whether the cue changes reasoning-token burn and empty-content rate (the one-bug law's newest lever).
- S5, watch, scoped: the safety section is steering literacy for the estate's own documented filter trips (the Nous authority-override trigger census), NOT a bypass recipe; the estate's law against detection evasion stands. Bank as understanding, never as evasion tooling.

## Watch / owed

- OWED: PDF not read this sitting (abs page only); every claim above is the abstract's own sentences. Olmo-3-7B and Qwen3-14B are the paper's animals, not the garden's - S1 measures OUR animals before any law is minted.
- The tweet's photo is the paper's figure card; not re-verified beyond the abstract bytes.
