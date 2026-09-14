# SALON_HARVEST_EVOLUTION_B_BLINDSPOTS_20260831.md — Lane B: what the harvest can never see by design

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: the three costliest harvest blind spots (leaderboards, pre-public signal, vendor changelogs) each have a sub-30-min weekly fix — UNPROVEN (cost-ranked reasoning; fixes not implemented) · falsifier: the named meters stay at 0 after the fixes land, or feeds catch the shifts equally fast without them

LAW: procedural only. Ranked by cost to Mag's goals (lane map, money map, FreeToken, steals). Cheapest fix each.

1. **Benchmark leaderboards / eval packs (SOTA claims).** Feeds report weights-drops but never leaderboard deltas or eval-pack updates — this is where "money map" and SOTA-steals shift first. Fix: weekly manual pass fetching Hugging Face Papers + lmarena.ai/artificialanalysis.ai key pages. Meter: # board updates sourced from leaderboards/week. Cost: ~15 min/week manual.

2. **Private repo / roadmap / unreleased-model signal (weights-drops before public).** X-only social lane misses private GH issues, Discord commits, closed arxiv preprints — the "lane map" moves here before feeds catch it. Cheap fix: add GH releases Atom fetch for Tier1+2 repos (public pre-release/PR activity). Meter: # pre-public steals caught >3h before feed. Cost: one URL class, ~5 min/week.

3. **Vendor changelogs without X presence (API-compat/price/rate/FreeToken terms).** FreeToken and money map depend on price/rate/free-tier changes that never hit X. Fix: add a weekly vendor-changelog fetch set (Anthropic, OpenAI, Gemma/Meta, deepseek, ollama) + special-clearance never in digest. Meter: # pricing changes receipted before partner asks. Cost: 4–6 URLs, ~15 min/week.

Blind spots that cost little are omitted; the three above are the costliest and each has a sub-30-min weekly fix.