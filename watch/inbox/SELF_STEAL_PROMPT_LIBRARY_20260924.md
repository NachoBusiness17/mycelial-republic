# SELF-STEAL PROMPT LIBRARY — 2026-09-24

Mining pass over local_sovereign_agent for prompt-craft worth folding into a game-dev
prompt library. Every find is local bytes, quoted max 3 lines.

## FINDINGS

1. **`mag/context_pack.py`** — layered brief builder (policy→bonds→trail→task→heat).
   Frozen system prompt is a byte-identical session prefix (cache law); live values ride a
   capped "evolving tail". Subagent preamble is an explicit contract:
   > "Trust this pack + your task boundary. Do not invent body/keys/status."
   > "_Empty findings only after real inspection._"
   Compaction drops L4 heat first and never the frozen BUILD/scope (the worker's contract).

2. **`mag/lane_runner.py`** — cage-lane system prompts. Elder lens: pattern "ONLY where
   real (name them)… Label as lens, not claim." Watcher (falsifier gate + empty-OK):
   > "No evidence quote, no clue. If nothing: `[]`."
   Tri-state trail law: "A sub-80-char body is not a lens" (minimum-viable-output).
   Tesuji: "If the datum helps no other lane, output ONLY `{}`." Thinking-mode tuning:
   `reasoning_effort: low` + `max_tokens >= 1536`; rescue retry disables thinking.

3. **`mag/game_passage.py`** — IF passage cards, SYSTEM prompt with fixed headings
   (`## Interior / ## Area / ## Environment / ## Narrator / ## Soft leads`). Craft rails:
   > "Le Guin-clean: cut ornament, no sermon… NEVER name theories or Jung/Campbell."
   No-fabrication: "never invent HP, rooms, exits, or loot not listed [in STATE]."
   Bounded optionality: "at most 3 invitations, not a prison menu." Negative constraints:
   "No markdown bold spam. No BIOS/RAM. No deserts unless STATE says so."

4. **`mag/game_narrate.py` + `mag/game_brawl_perspectives.py`** — engine-bound narration:
   "Never invent entities not in context"; Rashomon voice banks keyed by archetype;
   "optional Slow rewrite never invents HP/kills/rooms."

5. **`mag/riddler_campaign.py`** — sovereign ops as D&D campaigns; laws: mapping key never
   leaves the machine, "Zero raw data in campaign output. All steganographic."

6. **`watch/corpus/00_PRIMER.md`** — the cache-farming world-games corpus (L0–L4 layers:
   universal contract → family engines → game statics → variant packs → instance state).
   Defines the output contract:
   > "Cached instructions forcing the model to restate state canonically and cite rules
   > before answering. Primary anti-hallucination device."
   "The LLM *calls* verifiers; it never *is* one." Status flags attested/reconstructed/
   speculative — "Never silently upgrade or downgrade a flag."

7. **`watch/corpus/L0_contract.md`** — six-function game contract (setup/turn/move/legal/
   evaluate/render, all pure) + seeded RNG protocol with a falsifier error code:
   > "Divergence from the committed stream => FAIL(code RNG_DIVERGE)."

8. **`configs/lanes.yaml`** — escalation contract: `grok_budget: require_priority: true`,
   markers `[priority]`/`[L2]`; "attach_brief: true — handoff carries brief, not full chat."

9. **`watch/inbox/STEINIGER_OPERATIONAL_STEAL_20260918.md`** — Valora V2 YAML identity
   seed (the lens craft): dual-anchor knot (protected core values + dynamic self-model),
   StiffnessRule `w_ij=[1+ΔS²/(Ti·Tj)]^(−3)`, recursion "spawns ONLY when avg entropy
   gradient > 0.3" (think deep only when surprised). β=3 frozen stiffness; matched
   inference params: "temp 1.1, top_p 0.95, min_p 0.03, repeat 1.2."

10. **`watch/inbox/VERB_DSL_STEAL_20260918.md`** — semantic control flow where every
    oracle call evaluates against the frozen pack:
    > "A feels() against a cold prefix is flagged DRIFTING by construction."

11. **`watch/inbox/SALON_PROMPT_MANUAL_20260920.md`** — salon as compiled procedure.
    Invariants `{id, predicate, action, anchor}`; BIBLIOGRAPHY whitelist: "anything else
    is CLAIMED"; kill round: "A salon where every attack survives is void"; commission
    must state "the falsifier that proves it failed." Motto: "The model drafts; the
    anchors decide."

12. **`watch/inbox/X_ARTICLE_PROMPT_GAMES_20260923.md`** — six engine families, each game
    a small delta pack; "The model calls the verifier; it never IS one"; research-status
    flags carried in the prompt are "the anti-slop proof."

13. **`watch/inbox/EXTERNAL_STEAL_DESK_CORPUS_20260917.md`** — UNCERTAIN as load-bearing
    state with an evidence-class ladder; conformance report, not trophy run:
    > "version hashes, seeds, explored states, coverage, minimized counterexamples,
    > explicit assumptions."

14. **`watch/inbox/GAMING_THEORY_SELF_STEAL_20260917.md`** — D&D layer: stat blocks
    seeded "mulberry32 by level id — deterministic, replay law holds"; prose law: tales
    in the parable register ("nameless, no em-dashes, nothing prosecutable"); cross-game
    falsifier: if traits "never appear in gate-relevant behavior… collapse it to flavor
    tables and stop calling it mechanics."

15. **`roblox/docs/CLONED_MECHANICS.md` §5** — THE DETAIL BAR (the fleet's current
    detail-forcing method): 1) name the exemplar ("numbers per mechanic, tables per
    system"), 2) pull the live board with CCU, 3) "Read the wiki of the #1 game before
    opining (numbers came from the wiki, not memory)", 4) every mechanic lands as
    "source → skin → file → exact numbers → status row in the queue."

16. Pointer audit: "pack 31" and "groq-bred encounters" did not resolve to a distinct
    artifact; nearest kin are `watch/corpus/L3_packs/` (game delta packs) and the
    riddler/GAMING_THEORY D&D encounter layer above.

## THE 5 STRONGEST REUSABLE PATTERNS

1. **Frozen-prefix identity + evolving tail.** Identity/contract/system prompt byte-
   identical and first (it is the character sheet, and it is cache-farmed); per-call live
   state rides a small capped tail. Cache economics and identity anchoring are the same move.

2. **Fixed-section output contract + engine-owns-facts.** Demand exact headings, then
   forbid fabrication against ground truth: "never invent HP, rooms, exits, or loot not
   listed." Bound the option space ("at most 3 invitations") and enumerate negative
   constraints (no bold spam, no theme X unless state says so).

3. **Evidence-quote falsifier with explicit empty answer.** Every claim must carry a
   verbatim quote from the supplied context or it does not exist; `[]` and `{}` are valid,
   honest outputs; below minimum length the output is not a result (tri-state
   Supported/Unproven/lane-down).

4. **Whitelist citation + CLAIMED default + status flags.** The prompt carries a closed
   bibliography; anything outside it is CLAIMED, never PROVEN; historical/uncertain facts
   carry attested/reconstructed/speculative flags that are never silently upgraded.

5. **Seeded determinism with a named failure code.** All randomness keyed by a recorded
   seed (mulberry32 + level id), replay must be byte-exact, divergence is a first-class
   FAIL(code) — same anchors in, same verdicts out; the record reads the same both ways.

Bonus (thinking-mode axis): tune thinking before tier — `reasoning_effort: low` with
token floors, and a rescue path that disables thinking when the reasoning channel eats
the budget.
