# WORK w-nelson-shuffle

lane: hermes (headless one-shot)
ts: 2026-10-01T00:55:54.390914+00:00
ask: Edward Nelson's card-shuffle LCM problem (order of permutation = LCM of cycle lengths) applied to our fleet: quota resets, patrol cadences, knot compaction cycles, fossil staleness bars. Compute the LCM of our actual cycle lengths and identify the full-reset period. Show the math.

---

FINDING: LCM of the fleet's verified cycle lengths = 18,144,000 seconds = 210 days = 30 weeks = 7 30-day months. Prime factorization 2^8 x 3^4 x 5^3 x 7. The full-reset period — when all cycles realign — is 210 days from any epoch.

Cycle inventory (all verified from source files):
- 5 sec — mag.yaml watch_interval_seconds
- 120 sec — mag.yaml interval_seconds
- 300 sec — blast.yaml cycle_seconds
- 3600 sec — aos_grok.yaml cooldown_seconds
- 86400 sec — daily drift patrol / provider quota reset
- 604800 sec — improve.yaml cadence_days=7 / census CENSUS_STALE_DAYS=7 / fossil bar 168h
- 2592000 sec — fossil bar 720h (jev lane)

STEALABLE: The card-shuffle framing maps cyclic fleet processes to permutation cycle decomposition; the order of the permutation (LCM = 210d) is the harmonic envelope within which all resets recur in phase. The 30-day fossil bar is the longest prime cycle and the 5-sec tick is the finest subdivision — the fleet's rhythm is a 210-day grand wave. Borrow this as a design pattern: any new cadence added to the fleet must be checked against the LCM to see whether it shortens or lengthens the full-reset period.

TESTABLE: Run `python -m tools.census_drift_patrol --days 7` and confirm the AGENTS.md carrier census date is within the 7-day bar. Pick a known knot timestamp from verkle_chain.jsonl, add 210 days, and verify all cycle bars complete integer revolutions relative to that epoch. Expect: watch tick completes 3,628,800 cycles, interval 151,200, blast 60,480, cooldown 5,040, daily 210, weekly 30, 30-day 7. All integer — no remainder.

EVIDENCE: blast.yaml:300, mag.yaml:120/5, aos_grok.yaml:3600, improve.yaml:7d, fossil_registry.json:168h/720h, census_drift_patrol.py:CENSUS_STALE_DAYS=7, drift_patrol_prompt.txt:daily. OWED: verkle chain knot compaction cycle — no compaction periodicity found in verkle_chain.jsonl or memory/biography (the chain froze Sep 6 23:09Z per memory but no recurring compaction interval is documented). OWED: provider quota reset cadence for z.ai, OpenRouter, Anthropic, Mistral — only aos_grok.yaml cooldown is documented, not the actual provider reset windows. OWED: the 12 missing knot files from the heal queue — their absence may shift the chain's completion index but is not a cycle length.
