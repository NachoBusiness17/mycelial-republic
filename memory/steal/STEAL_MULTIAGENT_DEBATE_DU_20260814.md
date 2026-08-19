# STEAL — MULTIAGENT DEBATE (Du et al. 2023) as Mag contract, not a chair
**Date:** 2026-08-14
**Source:** Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, Igor Mordatch.
Improving Factuality and Reasoning in Language Models through Multiagent Debate.
arXiv:2305.14325. https://arxiv.org/abs/2305.14325
**Method:** steal the INVARIANT, not the DNA. No runtime dependency. No A2A/AutoGen/Du wire.

## What the paper actually did
Black-box copies of a model (sometimes mixed ChatGPT+Bard) propose independently, then each
reads the others and updates, repeated. Same prompt family across six tasks. Debate beat
single-agent, reflection, and majority vote. Gains rose with more agents and more rounds,
flattening after about four rounds. "Stubborn" prompts (trust own answer more) slowed
convergence and improved the final. Uncertain facts disagreed across instances and were
omitted. All agents could start wrong and still land right. They also found consensus is
not correctness: models will confidently affirm a shared wrong answer.

Main numbers they report (their eval, not ours): 3 agents, 2 rounds, chatGPT-0301.
Arithmetic 67.0 -> 81.8. GSM8K 77.0 -> 85.0. Biography factuality 66.0 -> 73.8. MMLU 63.9 -> 71.1.
Majority vote was weaker than debate (language model combining answers beat vote).

## Self-steal (what Mag already owns)
- `frontier_salon.roundtable`: attributed transcript, 1-3 rounds, down seats as ok=false.
- `quest_roshomon`: disagreement is evidence; consensus is not automatically truth.
- `party_subchain`: the relation persists; the model is interchangeable.
- `rib_bus`: instruction layer stays separate from candidate novelty.
- Ghost turn (subchain n=8): `_shared_invariant` is a quiet synthesizer; do not write
  novel_deltas onto rib_bus; scarce grok is not a default participant.

## External-steal (adapt the contract, refuse the DNA)
TAKE:
1. Round 1 is independent. Later rounds see attributed others. Mag currently round-robins
   inside round 1, so later same-round seats already see earlier moves. That is AutoGen
   broadcast, not Du first-round independence.
2. Disagreement is a confidence signal ("ease of persuasion"). Keep CHALLENGE as a first-class
   candidate list. Do not flatten it.
3. Heterogeneous adapters help. Mag already has mixed seats. Do not collapse them into one voice.
4. Cap rounds (paper flattens after ~4; Mag already caps at 3). Bound the transcript rather than
   summarizing speakers into one synthetic advisor.
5. Stubbornness: POSITION is own answer first; others are advice, not instructions. Mag's turn
   prompt already says this. Keep it.

REFUSE:
1. Success = "arrive at a common final answer." That is their metric and their own limitation.
   Mag's doctrine: the bus does not make a sovereign decision. Extract TEST, not a winner.
2. Majority vote as truth. They already showed it is weaker than debate; Roshomon forbids it
   as promotion.
3. A hidden synthesizer / LLM chair / summarizer that drops speaker identity. Their
   summarization trick is for context length; Mag's bound is "older attributed transcript omitted."
4. Distill debate traces back into Mag internals or a public model. Private machinery stays private.
5. Burning grok/supergrok as a default debate agent. Their cost note is our HABIT: scarce
   frontier is [priority] only.

## Adaptation (named, not a new throne)
- Rename `consensus_invariant` -> `overlap_tokens` (tokens shared across available answers;
  not truth).
- Round 1: each seat gets the question + mounted subchain only, not same-round peer moves.
  Round 2+: full attributed transcript including this table.
- `_extract_marked` must parse four fields as bounded blocks, not first lines.
- Extract CHALLENGE alongside NOVEL DELTA and TEST. None of them write to rib_bus.
- Default roundtable lane = janitor/local seats. Grok joins by [priority].

## Honesty
- We did not re-run their benchmarks. Numbers above are theirs.
- Their biography eval used a model to judge consistency with Wikipedia bullets; they note
  leftover false facts can still pass. Do not treat 73.8 as Mag's factuality.
- salon already cites this paper as "multi-round yes, unbounded no, no automatic truth."
  This steal is the sharper cut: independent first round, overlap is not consensus, and
  their confident-wrong-agreement is the reason Mag keeps the human gate.
