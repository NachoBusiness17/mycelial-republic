# CAPTURE: Small Model, Big Leverage (Nemotron 3.5 Lightning fine-tune article)

Captured 2026-09-29 via the mcp web_reader door on
https://x.com/i/article/2088303137182679378 (canonical per page:
https://x.com/fastinoAI/article/2088303137182679378), verbatim below from the
reader output. Recovery provenance: the 09-28 sweep read this article end to
end through the same door but saved nothing (sweep/
open-and-local-language-models-x.md:21-22); this file closes that hole so
every number the steal card banks is rerunnable from the repo.

- title: Small Model, Big Leverage: What We Learned Fine-Tuning NVIDIA Nemotron 3.5 Lightning with an Agent
- author: Fastino Labs (@fastinoAI)
- published: 2026-08-14T16:34:01Z (find carried date 2026-08-14, matches)
- wordCount: 4978 (sweep's "4,978 words" matches)
- likes at capture: 1294

---

2026 NVIDIA. All rights reserved.

NVIDIA, the NVIDIA logo, and Jetson are trademarks or registered trademarks of NVIDIA Corporation in the U.S. and other countries. Other company and product names may be trademarks of the respective companies with which they are associated.

© 2026 Fastino Labs

____
Small Model, Big Leverage: What We Learned Fine-Tuning NVIDIA Nemotron 3.5 Lightning with an Agent
____

We used our autonomous Fastino Fine-tuning agent to adapt early access checkpoints of Nemotron 3.5 Lightning into two specialized models, one for medical tasks and one for finance. We ran the full loop, generating synthetic data, training, evaluating, and iterating, and we are sharing the recipe and the adapters.

The result is a pair of small open models that punch far above their weight on domain-specific benchmarks while remaining fully deployable on a single GPU.

This post walks through the full recipe, the trade-offs we made, the mistakes worth learning from, and the decision points that made the biggest difference. We also include the final benchmark numbers and links to the released model weights.

____
What we released
____

Two production models:

- Fastino-Nemotron-3.5-Lightning-Finance
- Fastino-Nemotron-3.5-Lightning-Healthcare

Both are available now under the Apache 2.0 license:

- https://huggingface.co/fastino/Fastino-Nemotron-3.5-Lightning-Finance
- https://huggingface.co/fastino/Fastino-Nemotron-3.5-Lightning-Healthcare

____
Why Nemotron 3.5 Lightning?
____

NVIDIA's Nemotron 3.5 Lightning is a 30B-A3B model, meaning 30 billion total parameters with roughly 3 billion active per token. That balance matters for a few reasons:

- It trains fast. With only ~3B active parameters, each training step is cheap, so iteration cycles stay short.
- It fits consumer and prosumer GPUs. Quantized, the full model sits comfortably in 24 GB, which means a wide audience can run it.
- It has strong general reasoning for its size, which gives fine-tuning a solid floor to build on.

The thesis was simple: rather than train a model to know medicine or finance, train it to behave like a competent professional inside those domains. The knowledge was already there. What was missing was the interface.

____
The agent in the loop
____

The Fine-tuning agent is an autonomous system that owns the whole adaptation loop. Given a target domain, it:

1. Scopes the domain and drafts a curriculum
2. Generates and filters synthetic training data
3. Runs QLoRA fine-tuning jobs
4. Evaluates against held-out benchmarks
5. Diagnoses failure modes and revises the curriculum

The agent's value was not any single clever trick. It was iteration speed. A human team doing this work runs maybe two or three full cycles per week. The agent ran dozens, and the compounding effect of that iteration showed up directly in the final numbers.

____
Lesson 1: Synthetic data quality dominates quantity
____

Early runs used large synthetic corpora in the millions of tokens, with minimal filtering. Results plateaued quickly. The winning configuration used far less data, aggressively filtered for:

- Factual consistency with verified sources
- Realistic professional task shapes (queries a practitioner would actually issue)
- Diversity of difficulty and phrasing

The filter mattered more than the generator. Passing raw model output straight to training produced a model that mimicked the generator's tics, including its hallucinations.

____
Lesson 2: Curriculum order changes what the model learns
____

Training on hard cases first produced brittle models that pattern-matched to surface forms. The best runs started with foundational task formats, then layered in complexity: straightforward factual queries, then multi-hop reasoning, then adversarial or ambiguous cases.

____
Lesson 3: Evaluation must be domain-honest
____

Generic benchmarks were nearly useless for tracking progress. The models improved on MMLU-style tests while getting worse at the actual professional tasks. The fix was building held-out eval sets from real practitioner workflows, then gating all promotion decisions on those sets.

____
Lesson 4: Hyperparameters were less important than expected
____

QLoRA defaults (rank around 16-32, learning rate around 1e-4) got within a few points of the tuned configuration. The levers that actually moved results were data quality and curriculum design, not optimizer settings.

____
Lesson 5: Quantization is nearly free
____

The fine-tuned models lost almost nothing in the Q4 quantization needed for single-GPU deployment. Domain adaptation survived quantization far better than general capability does, which makes the small-model-plus-fine-tune stack even more attractive at the edge.

____
Lesson 6: The base model held the domain knowledge all along
____

The clearest surprise: on knowledge-probing tasks, the un-tuned base model often matched the specialized versions. The base model held the medical knowledge but lacked the interface, the function selection, argument construction, and multi-step state the harness scores, and a specialist adapter supplied exactly that. What fine-tuning bought was not knowledge but behavior.

____
Recipe J: Finance with strict tool-calling discipline
____

The Finance model was trained with a large share of tool-use traces, teaching the model when to call a calculator, a data API, or neither. It learned to refuse to hallucinate numbers and to show its work. On our internal finance benchmark, it beat the base model by 19 points while refusing 3x more unanswerable questions.

Framework: we trained with a mid-size open QLoRA stack, rank 32, learning rate 2e-4 for Recipe I (default near 1e-4 elsewhere), two epochs on the winning configuration, batch size tuned to the 24 GB envelope.

____
Recipe I: BFCL by separating tool syntax from conversation state
____

The reported BFCL winner used 27,542 real-harness trajectories with rank 32, a 2e-4 learning rate, and two epochs. Corrected internal evaluation moved overall performance from 48.00% to 71.18%. Single-turn performance rose from 51.42% to 81.88%, while multi-turn changed by less than half a point.

That asymmetry is the most important finding in this post. The adapter taught the model the interface, not the state discipline. Multi-turn competence needs real multi-turn trajectories, and synthetic pairs did not move it.

____
Benchmarks at a glance
____

| Model | BFCL overall | Single-turn | Multi-turn | Finance internal |
|---|---|---|---|---|
| Nemotron 3.5 Lightning (base) | 48.00% | 51.42% | - | 41.2 |
| Fastino Finance adapter | 71.18% | 81.88% | <0.5pt delta | 60.4 |

Numbers are corrected internal evaluations on held-out sets, not vendor-reported figures.

____
What we would do differently
____

- Start with real trajectories, not synthetic ones, for anything multi-turn
- Build the eval harness before the first training run
- Spend budget on filtering, not generation

____
Try it
____

Both adapters are on Hugging Face under Apache 2.0, and the Nemotron 3.5 Lightning checkpoints are available from NVIDIA. A single 24 GB GPU runs the quantized stack end to end.

Co-authors: @m_newhaus @DhruvAtreja1

---

CAPTURE NOTE (this session): the numbers the steal card banks all appear
verbatim above: 27,542 real-harness trajectories; rank 32; 2e-4; two epochs;
48.00% to 71.18% overall; 51.42% to 81.88% single-turn; multi-turn under half
a point; Apache 2.0 adapters; 30B-A3B Lightning; the interface-not-knowledge
reading (Lesson 6). One correction to the round-1 card's framing: the article
is by Fastino Labs (their Fine-tuning agent did the work) about NVIDIA's
Nemotron 3.5 Lightning, and Recipe I's 2e-4 is a deliberate override of the
1e-4 default the article names elsewhere.
