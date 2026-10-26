# X INTEL: the marfinxx fabrication catch + DeepGEMM refresh (2026-10-05)

Operator drop: "https://x.com/marfinxx/status/2106731158763360429" +
"github.com/deepseek-ai/DeepGEMM" (two drops in one line; each tri-stated).

## 1. The marfinxx tweet: FABRICATED ATTRIBUTION (primary-verified)

The tweet (89.9K views, 1.1K likes) claims a "Stanford paper" shows GPT-6
Astra (high-temperature exploration) paired with Claude Opus 5.5
(zero-temperature step auditing + "local surgery" of broken reasoning
steps) beating Best-of-N: "91.2% flaw recovery", MATH500 29.6 -> 58.0%,
+7.5% AMC-2023, no reward models. It funnels to the author's course
article and Telegram.

The arXiv ID it cites (2608.05643) is REAL but says NONE of that. Fetched
from the arXiv API this session:

- Real paper: "Refining Over Resampling: Test-Time Self-Correction for
  LLM Reasoning" - Bilal, Mohsin, Umer, Trigg, Subhan, Ali, Hougen;
  2026-08-06; EMNLP 2026 submission.
- Real finding: a verifier-free breadth-depth framework - sample multiple
  rollouts, refine each via iterative self-critique and self-correction,
  aggregate by majority vote - beats resampling more candidates and beats
  verifier-guided selection. Open-weight models: Qwen2.5-1.5B reaches
  58.0% on MATH500, 25.0 -> 32.5% on AMC.
- The graft: the tweet stole the real 58.0% MATH500 figure, bolted a fake
  29.6% baseline under it, invented the "GPT-6 Astra x Opus 5.5" pairing,
  the "Stanford" attribution, the "91.2% flaw recovery", and the "+7.5%
  AMC" - none of which appear in the paper.

THE REAL PAPER IS THE ESTATE-RELEVANT PART. "Refining over resampling" is
the estate's own workflow geometry empirically validated on open models:
sample -> critique -> correct -> majority-vote (the kit's workflow shapes
2 and 5, the confirm/revise legs) beats wider raw fan-out (Best-of-N).
It is also the falsifier doctrine in math form: a firing falsifier is
information - refine the trajectory instead of paying for more lottery
tickets. Steal door: cite this paper in the kit's workflow-shaper card as
the evidence that the five shapes beat naive width.

Standing lesson (the fabrication-frontier class): engagement accounts
graft hot model-pairing fantasies onto real papers, keeping the real
numbers as camouflage. The citation-resolution law (bytes or UNVERIFIED)
caught it in one fetch. The 29.6 baseline under a real 58.0 is the
tell - check the PRIMARY before believing any screenshot of a paper.

## 2. DeepGEMM refresh: estate verdict UNCHANGED + one vast-ladder fact

The estate's 10-01 verdict holds: DeepGEMM (8.3K stars, MIT) is
SM90/SM100-ONLY (Hopper H800 / Blackwell); nothing consumer, nothing AMD.
New since the estate's receipt: DeepGEMM-Ascend (2026-09-30) for Huawei
NPUs - a separate repo; plus the 09-10 Sparse Indexer / Mega Gate /
DeepJIT wave. Up to 1550 TFLOPS FP8 on H800.

THE VAST-LADDER FACT: the estate's armed ladder rungs cannot run it -
3090 (SM86), 4090 (SM89), 5090 (SM120-consumer? unverified), and even the
cheap A100s (SM80) are all outside the supported set. DeepGEMM-class FP8
serving requires the H100 tier (~2+ USD/hr on vast) - if the Mythos
build ever wants these kernels, that is a different ladder rung than the
one armed. No action; the fact is banked for the hardware table.

fetched: 2026-10-05
Writer: zcode-53-strategy-window
