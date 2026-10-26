# WORK w-selfplay-hardware

lane: openrouter model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-10-07T04:15:37.210135+00:00
finish: stop cached_tokens: 0
ask: Self-play reasoning (R-Zero, Absolute Zero, SCOPE): what is the MINIMUM hardware spec for a meaningful run? Could a single RX 5600 XT + free-tier API lanes produce measurable self-play gains? What scale reduction from the papers' setups is possible?

---

FINDING: Published specs for R-Zero, Absolute Zero, and SCOPE are unverified, so exact minimum hardware and scale reduction are OWED. General architecture suggests an RX 5600 XT with 8 GB VRAM and free-tier API rate limits lacks the memory and throughput for the rollout batches and model sizes in those papers; meaningful self-play gains on this setup are unlikely.

STEALABLE idea: Cache opponent checkpoints during self-play and freeze all but the final policy layer; this cuts per-step compute and lets a single consumer GPU iterate faster.

TESTABLE hypothesis: A 770M-parameter model trained for 100k self-play episodes on an RX 5600 XT using a frozen 1.3B opponent pool will show less than 3% accuracy gain over supervised fine-tuning on GSM8K.

EVIDENCE or OWED: OWED. No verified source states exact hardware requirements for R-Zero, Absolute Zero, or SCOPE.
