# WORK w-selfplay-hardware

lane: openrouter model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-10-07T04:15:37.210135+00:00
finish: stop cached_tokens: 0

ASK (depth 1/2): Self-play reasoning pipeline yield curve
---

The hermes worker (w-selfplay-hardware_hermes.md) established that the self-play data pipeline is separable from training hardware: generate reasoning traces via free API inference, filter/curate, train later on proper GPU. But it left unanswered: what is the YIELD CURVE?

INVESTIGATION: For a 7B-14B reasoning model, what fraction of self-play generated traces pass a correctness filter (step-valid + final-answer correct) at varying difficulty tiers (GSM8K easy/medium/hard, MATH subset)? How many API calls per usable trace at each tier? At what trajectory count does self-play fine-tuning data match or beat an equivalent volume of supervised seed data on a held-out benchmark?

Sources to check:
- DeepSeek R1-Zero / R1 paper: self-play data volume and filtering ratios
- OpenAI o1-style rejection sampling yield rates (any public breakdown)
- Qwen2.5/DeepSeek-R1 distillation papers: how many raw generations per training example survived filtering
- Free-tier rate limits and costs for the generation volume needed

Deliverable: a yield table (difficulty tier → raw traces needed → correct traces → API cost → effective $/usable-trace) plus the crossover point where self-play data outperforms equal-volume supervised data on a named benchmark.

TIER: free | MAX_TOKENS: 3000
