# THE 50 · W1 T04 - NPC DIALOGUE BANK (mud-boon traits -> lines via free lanes)

Filed 2026-09-19 · W1 GAME BUILD (WBN x RUINS GO) · finish line per
`watch/inbox/THE_50_PROGRAM_20260918.md` item 4.

Artifact: `memory/runs/the50/w1_t04_npc_dialogue_bank.jsonl` - 30 rows, one row
per NPC line, every row carrying trait provenance.

## What landed

- 30 NPC dialogue lines (>= 20 required), 6 lines per mud-boon trait across
  thorns / berserk / arc / vision / chain.
- 6 faces speak: the mud's first 3 NPCs from the NPC=SEAT build order
  (innkeeper, vault warden, bones guide), the sentry and merchant face
  classes, and the DM face (the room itself speaking).
- Each row binds: trait -> TRAIT_TEXT ->
  `dashboard/static/games/ruins_go_engine.js:184-190` (MONSTER_TABLE :174-183,
  "traits ported from mud.html's boon system" per :163-165) -> donor boon in
  `dashboard/static/mud.html` (12 gods, draft 1-of-3) -> engine mechanic where
  one exists (vision pathfind at :339-357, berserk double-move at :378-394).
- Every line passes the parable register law
  (`watch/inbox/GAMING_THEORY_SELF_STEAL_20260917.md:39-40`): nameless, no
  dashes of any kind, nothing prosecutable, voice matched to the TALES
  register ("the charcoal is free. Nothing else is.").

## Via free lanes (method, honest)

- 30 trait x face prompts were fired at the free local lanes (ollama):
  `gemma:2b` (AGENTS.md scut tier) first, `gemma4` (short worker) on retry.
  Raw drafts and register-check verdicts are preserved in
  `memory/runs/the50/_w1_t04_lane_drafts.json`; the drafter is
  `memory/runs/the50/_w1_t04_lane_drafts.py`.
- Result: 26/30 register-clean drafts from gemma:2b; gemma4 returned empty
  output on all 4 fallback attempts (known empty-reply behavior).
- Curation: 1 draft accepted verbatim (W1T04-014, the merchant arc warning);
  29 lines are seat rewrites of their lane drafts, each row storing the raw
  lane draft, its register problems, and the rewrite reason under
  `lane_generation` / `curation` / `curation_note`. The scut tier produced
  voice and texture; the seat pass enforced trait linkage and the register
  law. Both layers are on disk per row.
- Builder: `memory/runs/the50/_w1_t04_build_bank.py` (json.dumps, one row per
  line, self-verifying on write: parse-back, row count >= 20, provenance keys,
  no dash of any kind, trait vocabulary).

## Falsifier

- If a line's trait cannot be felt by a player who has read only that row's
  TRAIT_TEXT, the row is decoration: delete it and the bank still stands at
  29.
- If NPC_RACTOR_ARCHITECTURE's falsifier "a player cannot tell which face
  they are talking to within 3 exchanges" fires for two rows of the same
  trait, those two faces are not faces yet.

## Sources (every claim's file)

- `watch/inbox/THE_50_PROGRAM_20260918.md` item 4 - the task and finish line.
- `dashboard/static/games/ruins_go_engine.js:163-218, 339-394` - D&D layer v1,
  MONSTER_TABLE, TRAIT_TEXT, TALES, vision and berserk mechanics.
- `dashboard/static/mud.html` BOONS array - donor boon system, 12 gods.
- `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md` - NPC=SEAT architecture,
  first 3 mud NPCs, face classes, lane routing rule, falsifiers.
- `watch/inbox/WBN_STEAL_20260918.md:54-56` - "RUINS GO mud-boon traits,
  classes, tiny tales" as the D&D layer this bank serves.
- `watch/inbox/GAMING_THEORY_SELF_STEAL_20260917.md:39-40` - register law
  (seeded randomness, gate tests, nameless/no-dash/nothing-prosecutable
  register).
- `watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md` - sibling receipt whose
  prophecy-seat notes this bank's DM face inherits.

## Repair 2026-09-25 (re-verified this window)

The 2026-09-22 dedupe moved the canonical mud copy to
`dashboard/static/games/mud.html`; `dashboard/static/mud.html` became a
447-byte redirect stub, so the donor_source path the rows cited went stale.
The donor boons themselves verify verbatim at the canonical path (BOONS
array, `dashboard/static/games/mud.html:461-472`, 12 gods, "draft 1 of 3"
comment at :460). This window: all 30 rows' donor_source fields were
rewritten to the canonical path with line numbers (line content, ids, and
all other fields untouched) by
`memory/runs/the50/_w1_t04_repair_paths.py`; the builder constants were
updated so regeneration reproduces the canonical path; and the full bank
was re-verified with

- `.venv/Scripts/python.exe memory/runs/the50/_w1_t04_verify_bank.py`
  -> RESULT: PASS all checks, 30 rows, traits thorns 6 / berserk 6 / arc 6 /
  vision 6 / chain 6, 6 faces, lanes ollama:gemma:2b. 25 checks: JSONL
  parse, count >= 20, unique ids, spoken line per row, provenance keys,
  trait vocabulary, row trait_text == engine TRAIT_TEXT
  (ruins_go_engine.js:184-190, read fresh), donor god + desc found in
  games/mud.html for all five traits, free-lane models, raw draft preserved
  per row, no dash of any kind in spoken lines, coverage and faces.

New executable this window: `memory/runs/the50/_w1_t04_verify_bank.py`
(re-runnable verifier) and `memory/runs/the50/_w1_t04_repair_paths.py`.
Not re-run this window: the lane firings themselves (2026-09-19 drafts and
register verdicts remain the record in `_w1_t04_lane_drafts.json`, 30
prompts, 34 attempts); ollama was not re-invoked.

## Correction 2026-09-25 late (gala lane b3-the50-quality)

The R3-era content review (watch/inbox/THE50_REVIEW_R1.json) flagged the
thorns rows' carrier_monsters: Barbed Sentry is trait berserk in the engine
MONSTER_TABLE (ruins_go_engine.js:176), not thorns; thorns has only Crypt
Snake (:175). This window the carrier was dropped from all SIX affected rows
(W1T04-001..005, the reviewer's five, plus W1T04-026, which the review
sample missed), and the builder constant d_carriers() was corrected so
regeneration reproduces the fix. Cause and evidence named in
`memory/runs/the50/_w1_t04_carrier_fix.py`; the verifier was re-run after the
fix: RESULT PASS all checks, 30 rows (raw output:
watch/inbox/gala_20260925/w1/lanes/b3_w1_t04_verify_after_fix.txt).
Berserk rows were already correct and are untouched.
