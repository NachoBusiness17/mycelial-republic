# RAW EVIDENCE: WebFetch https://arxiv.org/abs/2509.05276 (SpikingBrain technical report abstract)
# Fetched 2026-10-01 by lane nonnvidia-stacks (division B, spiking-wide). Verbatim fetch result below.

PROMPT: What does the abstract say about hardware: which domestic/non-NVIDIA chips or clusters were used for adaptation and training (MetaX, Cambricon), what scale (number of GPUs), and what claims about training stability, efficiency vs Transformer baselines, and the 100x TTFT / energy claims? Quote exact sentences.

RESULT:
Per the abstract, the work used MetaX (no mention of Cambricon):

## Hardware/cluster:
- "SpikingBrain leverages the MetaX GPU cluster" - training was adapted to non-NVIDIA chips.
- Scale: "training remains stable for weeks on hundreds of MetaX GPUs" with "Model FLOPs Utilization at expected levels."

## Efficiency vs Transformer baselines:
- Models match baselines with modest data: "comparable to open-source Transformer baselines while using only about 150B tokens for continual pre-training."
- Long-context gains: "inference with (partially) constant memory and event-driven spiking behavior."

## 100x TTFT claim:
- "SpikingBrain-7B attains over 100x speedup in Time to First Token for 4M-token sequences."

## Energy/sparsity claim:
- "the proposed spiking scheme achieves 69.15 percent sparsity, enabling low-power operation."

No specific chip model names (e.g. Cambricon) appear - only the MetaX GPU cluster is cited.
