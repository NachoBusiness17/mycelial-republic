# GROK BRIEF — THE CREATIVE DM STUBS OUT (the single most important live-game fix, 2026-08-15)
# From: the session's diagnosis. For: grok (playtesting / intra-agent). Self-stolen, proof-gated.

## THE BUG (confirmed, not a guess)
- The creative DM (mag/game_dm_llm, deepseek v4 flash) returns EMPTY/SHORT content on many calls,
  so the game's voice goes silent and the overnight epic (mag/hero_journey) wrote only ~500 of 5k words.
- A SINGLE deepseek call with a SMALL prompt returns 296 chars in ~3s, ok=True (verified in-container).
- Therefore deepseek is fine; the failure is the LARGE-PROMPT path: hero_journey._write_stage dumps the
  WHOLE corpus + saga + roster into EVERY chapter's prompt -> deepseek times out (90s) or returns empty.

## THE FIX (do this)
1. FEED A SMALL, RELEVANT SLICE, not the whole corpus, into each chapter's prompt
   (e.g. 2-4 sampled beats + the stage brief + a couple named NPCs, ~<600 tokens of context).
2. RETRY ON EMPTY/SHORT: if _raw_call returns ok but <80 chars, retry ONCE (a fresh call) before
   falling back to the placeholder. Never silently stub.
3. CONSIDER thinking OFF for pure prose (config note: disabling thinking "returns real text,
   ~10-15x cheaper, verified 08-03"). High temp (0.8) carries the creativity; thinking-on is what
   starves the budget on big prompts.

## PROOF GATE (before saying done)
- get_errors clean on every touched file.
- Drive hero_journey.compose() in the container; expect EVERY chapter to write real prose,
  total >= 4,000 words, no chapter == the placeholder text.
- Playtest: talk to an egregore-NPC and get a full reply, not an empty DM.

## WHY (the operator's law)
- Prove it or don't claim it. No repeating loops. The game's voice must not go silent.
- The whole point: wake up to a 5k-word story, not a stubbed fragment.
