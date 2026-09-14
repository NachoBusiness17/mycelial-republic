# TASK — Guild Daylight Queue, Batch 1 (assigned 2026-08-27, operator GO)

You are a grok seat doing authored work for the Villains Guild module. Read everything
listed below BEFORE writing anything. Work ONLY inside `campaigns/villains_guild/daylight/`.
Never modify `module.json`, the canon trio file, or the quest files — those are canon.

## Read first (the shelf — bind, don't invent)

1. `docs/concepts/RIDDLER_PROTOCOL.md` — the four moves, two channels, the ANSWER: line fix.
2. `mag/riddler.py` — the EXISTING codec (`compile_surrogate`, `PrivateGraph`). Your output
   must be consumable by this code, not a new format you invent.
3. `mag/surrogate.py` — decode + aggregate; note the raw-answer extraction contract.
4. `docs/ref/GAME_VILLAIN_GUILD_DESIGN.md` — the binding design law for all guild writers.
5. `campaigns/villains_guild/module.json` — rooms, the five verification skills
   (parse_contracts / cross_reference_documents / check_sources / verify_arithmetic /
   build_consensus), and the `rooms_detail_note` that promises this map.

## Deliverable 1 — `daylight/riddler_map.json`

Bind each room to its verification skill via the existing codec:
- One surrogate face per room, seeded and deterministic — record the seed in the file.
- Every room binding must carry BOTH channels: the surrogate-action verb AND the
  raw-answer `ANSWER:` line convention (the consensus-illusion trap is law).
- If the existing codec cannot express a binding you need, DO NOT hack around it —
  write the gap in the receipt instead.
- Schema note at top of file: which module/version produced it, and the seed.

## Deliverable 2 — `daylight/kid_test_gate.md`

The gate any guild quest must pass before canonization:
- 8-10 test tasks a 9-12 year old completes in one sitting, covering all five skills.
- Pass/fail rubric per task (plain language, a parent can administer it).
- Fun-bar check per the design law's trap ratio, and a "would a kid ask to play again" prompt.
- ZERO internal fleet references: no repo paths, no agent jargon, no model names — kid-facing only.

## Deliverable 3 — `daylight/RECEIPT.md`

What you read (file paths), what you wrote, honest unknowns. Tri-state any claim you
cannot verify from the bytes you read: Supported / Disputed / Unproven.

Laws: English only. No secrets, keys, or internal endpoints in any output. Cite file
paths, not folklore. If a shelf file contradicts this task, the shelf wins — say so in
the receipt.
