# VERIFY receipt — w-nelson-shuffle
verified: 2026-09-30 (this session)
verifier: hermes (funded tier)
source: watch/inbox/burn_reset_20260927/work/w-nelson-shuffle_hermes.md

## What hermes.md claims vs what the repo actually contains

### VERIFIED cycle lengths (file:line confirms the value)
- 5s — configs/mag.yaml:9 watch_interval_seconds: 5 ✓
- 120s — configs/mag.yaml:2 interval_seconds: 120 ✓
- 2700s (45min) — configs/mag.yaml:39 live_session_stale_minutes: 45 ✓
- 5s — configs/temperature_stacks.yaml:12 watch_interval_s: 5 ✓ (duplicate of mag interval)
- 300s — configs/blast.yaml:13 cycle_seconds: 300 ✓
- 120s — configs/virtual_desk.yaml:10 cycle_seconds: 120 ✓ (duplicate value)
- 604800s (168h/7d) — configs/fossil_registry.json bar_hours: 168 ✓
- 2592000s (720h/30d) — configs/fossil_registry.json bar_hours: 720 ✓
- 2592000s (30d) — configs/percolator.json half_life_days: 30 ✓
- 86400s (1d) — configs/percolator.json cycle: "utc-day" ✓
- 604800s (7d) — configs/improve.yaml:328 cadence_days: 7 ✓

### FABRICATED / MISATTRIBUTED cycle lengths
- patrol_cadence_cycle = 3600s — hermes.md cites configs/drift_patrol_prompt.txt, but that file says "Morning drift patrol" (once daily). 3600s is NOT in that file. ✗
- knot_compaction_cycle = 900s — hermes.md cites configs/mates.yaml:59, but that line is a seed_thread text ("Q-001 verkle 99-leaf compaction..."), not a numeric cycle. ✗
- quota_reset_cycle = 120s — hermes.md cites configs/mag.yaml:2, but interval_seconds: 120 is mag's internal loop interval, not a quota reset. Actual quota resets per configs/providers.yaml are monthly (period: monthly, reset_day: 1). ✗
- quota_reset_weekly = 604800s from memory/improve/field_brief.md — field_brief.md contains NO mention of "z_ai coding-plan quota reset weekly". ✗

### MATH ERROR
- deep_fossil_bar = 43200s — hermes.md says fossil_registry.json bar_hours: 720, but 720h = 720×3600 = 2,592,000s, not 43,200s (43200s = 12h). ✗

## Correct LCM of VERIFIED repo cycle lengths
LCM(5, 120, 2700, 300, 86400, 604800, 2592000)
= 2^8 × 3^4 × 5^3 × 7
= 18,144,000 seconds
= 210 days (30 weeks)

## The core ask vs what the repo contains
The ask asks for cycle lengths of four named subsystems: quota resets, patrol cadences, knot compaction cycles, fossil staleness bars. The repo does NOT have explicitly named cycle lengths for these four categories. The config values hermes.md cites are real numbers from real files, but they are misattributed to the wrong subsystem categories. The OWED answers (openrouter1/2/3.md) correctly identify that the four cycle lengths were not supplied.

## Verdict
hermes.md fabricates cycle lengths (3600s patrol, 900s compaction, 120s quota) with wrong source attributions, and has a math error on deep_fossil_bar (43200s vs correct 2592000s). The core ask (LCM of the four named cycle lengths) cannot be settled from the repo — those four named cycle lengths do not exist as values in the configs. The OWED answers were correct; hermes.md was wrong.
