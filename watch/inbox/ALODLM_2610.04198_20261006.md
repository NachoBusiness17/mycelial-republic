# LINK-DROP receipt: ALoDLM, adaptively looped diffusion LMs (Amazon AGI)

- Dropped: 2026-10-06, X https://x.com/arankomatsuzaki/status/2107473674211328010
- Fetched: arXiv abs page first-hand (43,460 bytes), same sitting. proj https://alo-dlm.github.io/ , repo github.com/amazon-science/ALoDLM , weights HF amazon/ALoDLM-8B (+1.7B scale in the paper).
- LINKS row: seq 1791315046466033, canonical sha256 9F28138B8A664E23...
- Verdict: STEAL (the integration probe is one sitting and local-runnable); every quality claim below is the abstract's own bytes, not yet re-measured here.

## What it IS (from its own bytes)

Verbatim, the diagnosis: "We attribute this gap to a computation-difficulty mismatch: within a partially observed sequence, some unknown tokens are easy to predict, while others require substantially more computation. Existing DLMs nevertheless apply uniform computational depth to all unknown positions at each denoising step."

Verbatim, the mechanism: "ALoDLM, which replaces uniform computation with token-adaptive latent recurrence. At each denoising step, ALoDLM iteratively refines latent representations and allocates computation according to token difficulty. Tokens ready to commit are fed back as discrete context, while unresolved tokens retain and further refine their latent states through additional recurrent passes."

Verbatim, the result: "Across eleven benchmarks, ALoDLM outperforms all evaluated DLMs and the corresponding AR baselines in average benchmark score at both scales. ALoDLM also retains fast parallel decoding."

## Estate mapping

1. The computation-difficulty mismatch is the estate's driving ladder as a decode-time law: cheap tokens get janitor compute, hard tokens get judgment compute - ALoDLM runs the tier ladder INSIDE one model, per token, learned via a conditional NELBO over token-wise compute schedules. The percolator's compute-where-demanded doctrine (Jev router) in latent space.
2. The light-maze thesis (banked 10-05): diffusion-LMs ARE the consensus-decode mechanism the swarm card demanded, probe held for the executor window. ALoDLM is an open-weights DLM beating its own AR baselines - the probe now has a runnable body at 1.7B/8B. The ReFlux watch note ("watch for 3090-rung finetunes") has fired: weights are up.
3. Consensus-within-one-model: committed tokens feeding back as discrete context is a model's own first-pass consensus; the consensus gate's agreement instruments (AUROC ladder, D6 monoculture proxy) get a new measurement subject - does a DLM's committed/underdetermined split behave like the fleet's agree/disagree split?
4. Delta-not-state (ReFlux, banked 10-05): unresolved tokens retain and refine latent state through extra passes instead of recomputing - the estate's delta-over-rewrite law as an architecture.

## Steal rows (one seat one sitting each)

- S1, high: garden integration probe - clone github.com/amazon-science/ALoDLM, read the serving path (HF transformers? vLLM? llama.cpp diffusion support?), land either a running 1.7B or a documented blocker on this box, bank the receipt. The 17-model garden has no DLM row yet; this is the first candidate.
- S2, high: mini-battery vs same-size AR animals - once S1 runs, ALoDLM-1.7B/8B vs the garden's nearest AR animals on one fixed math+code subset, pass@1 AND tokens/sec (parallel decode is the claimed lever; measured before believed, the flash-50wide envelope law).
- S3, medium: consensus-gate probe - feed the gate a DLM arm: measure whether committed-token confidence aligns with the janitor-agreement AUROC ladder's shape (0.58@1.5B / 0.71@7B class measurements).
- S4, watch: serving-engine dependency - the quality-efficiency claim is "under optimized inference engines"; if the optimized engine is not open, the garden probe measures the unoptimized path and the receipt says so honestly.

## Watch / owed

- OWED: PDF not read this sitting (abs page only); no weights pulled yet (S1 is the door). The eleven benchmarks were not re-run; the AR-baseline comparison rides the paper's own evaluation.
- No spend: weights are open (Apache/MIT unknown until the repo is read - license check lands with S1, the GSTD NOASSERTION lesson).
- Context: 5th independent drop this sitting (Teknium devices, MIRA, token cues, ALoDLM + the operator's own flow-state drops 10-05); the everyone-arriving-at-once pattern continues, all banked as receipts.
