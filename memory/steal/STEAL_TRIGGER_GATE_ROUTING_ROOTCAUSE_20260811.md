# STEAL — ROOT CAUSE OF ROUTING CONFUSION: skill_pipeline TRIGGER-GATE (2026-08-11)

Operator: "it seems that the launch in vs code are gated to skills somehow or when i ask for my deep
dives or steals or our user patterns" + "which is causing the issues of confusion the source therein" + "steal".

## Root cause (the source of the confusion)
mag/skill_pipeline.py routes every VS Code/ghost ask by EXACT trigger-keyword match (match/route).
- Plain asks were silently GATED: "steal" (capability_steal triggers were "steal search"/"capability steal"),
  "deep dive" (deep-research skill lacked it), "user patterns" (word_skill_map lacked it).
- Fragile: one prompt hits multiple skills -> ambiguous chain; missing keyword -> swallowed. THIS has
  been a major source of the confusion all session.

## Fix (done, verified get_errors clean)
Added missing trigger keywords:
- deep-research/frontier skill: + "deep dive", "deep-dive", "dive into".
- capability_steal: + "steal", "steal it", "do a steal".
- word_skill_map: + "user pattern", "user patterns", "our patterns", "patterns".

## Deeper lesson (the real steal)
Routing on fragile exact-keyword triggers silently swallows/mis-routes intents. HARDEN:
1. Add a FALLBACK so no ask is silently gated (route unmatched -> a general dispatch/intent skill).
2. Add the missing intent keywords for the operator's common asks (done for steal/deep-dive/patterns).
3. Prefer INTENT over keyword where ambiguous (or a cheap classifier) so routing isn't keyword-fragile.
