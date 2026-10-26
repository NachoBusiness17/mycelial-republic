# WORK w-selfplay-hardware

lane: openrouter model: meta/muse-glimmer-30b
ts: 2026-10-07T05:31:12.654614+00:00
finish: stop cached_tokens: 54
ask: Self-play reasoning (R-Zero, Absolute Zero, SCOPE): what is the MINIMUM hardware spec for a meaningful run? Could a single RX 5600 XT + free-tier API lanes produce measurable self-play gains? What scale reduction from the papers' setups is possible?

---

(1) FINDING
No verifiable public minimum hardware spec for a meaningful R-Zero / Absolute Zero / SCOPE self-play run could be verified. No authoritative source with concrete minimum GPU count, VRAM, or API throughput for measurable self-play gains was found. Specific claim about RX 5600 XT + free-tier API lanes producing measurable self-play gains is OWED. Scale reduction possible from paper setups is OWED.

(2) one STEALABLE idea worth keeping
Distill self-play to a minimal closed loop: tiny policy + tiny verifier + on-policy buffer replay with strict compute budget cap per iteration, to test if any learning signal emerges before scaling.

(3) one TESTABLE hypothesis
A single RX 5600 XT with 6 GB VRAM and free-tier API rate limits can complete at least one full self-play iteration of a toy reasoning domain with measurable delta in pass rate vs zero-shot baseline within 24 hours.

(4) EVIDENCE or OWED
EVIDENCE: none exist for the requested minimum spec and scale reduction claims. OWED for all specific hardware thresholds, paper setup baselines, and feasibility of RX 5600 XT + free-tier API lanes for measurable self-play gains.
