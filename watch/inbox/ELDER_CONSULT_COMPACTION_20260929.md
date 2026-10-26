# ELDER CONSULT (funded judgment): why are we compacting? 2026-09-29

Summoned by the operator: no sacred cows. Elder audit first: 41 organs declared, 40 verified, 0 ghost - and ZERO verkle/compact organs in the 25 gaps: the compaction program is not a witnessed live organ, so under the elder's law (contradictions resolve by evidence and hierarchy) there is no live evidence for it at all. This file carries the funded-tier verdict on the same question.

Run note: first attempt died on max_tokens=4000 (3,998 reasoning + 2 visible - the providers.yaml warning verbatim: reasoning models burn thinking out of max_tokens). Refired at 12000.

Paid run: z-ai/glm-5.3-prime, usage {"prompt_tokens": 271, "completion_tokens": 2383, "total_tokens": 2654, "prompt_tokens_details": {"cached_tokens": 256, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 1852, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.02115576, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}

---

**Verdict: (b) Park it.** The numbers convict option (a) outright: the compaction program targets a 5.8MB chain inside a 68GB tree - 0.0085% of the estate's mass - and the 68GB consists of archival JSONL ledgers and duplicate 1.86GB index files the program explicitly does not touch. Executing it means running a never-live mutation against the append-only provenance spine - the single irreplaceable integrity artifact - to recover megabytes on cheap disk. That is all downside, no upside: the hot-restore path has never fired in production, so the first live run is the riskiest possible moment, and the prize is a rounding error. The original justification - mem-lattice hot-swap, loading portions of state - is a vision, not an organ: undeclared in the organ map, unfunded, and demonstrably not the bottleneck. Tonight proved the bottleneck is delivery pipes and cadence. Compacting state that nobody is failing to load, while delivery is failing, is polishing the 0.01% and ignoring the rot. But (c) is also wrong: the program is fully spec'd and tested, and killing it destroys a working asset for ideological cleanliness. Parked and frozen, the code costs nothing. Park it, mark it non-organ, and spend the attention on the pipes.

**Named re-raise conditions (any one fires it):**

1. **Chain mass:** append-only chain exceeds ~1GB or ~1,000,000 leaves (~120x current) - the point where folding recovers real space and restore time becomes a recovery-cadence issue.
2. **Architecture:** mem-lattice hot-swap is declared as an organ in the organ map with a funded build - compaction is a prerequisite of that dream, not of current operations.
3. **Restore SLA:** full-chain hot-restore exceeds an operational threshold (minutes, not seconds) that would block recovery after an incident.
4. **Storage regime change:** disk stops being cheap - quota-billed or hosted environments where 68GB costs real money. Even then, the first target is the duplicate 1.86GB index files, which is a dedupe, not a compaction.

Until one fires: do not execute, keep the tests CI-green but unmaintained, and keep the program out of every organ map and capability claim. If no condition fires within 18 months of estate time, escalate to (c) - kill and retire the tests - at the next judgment seat.
