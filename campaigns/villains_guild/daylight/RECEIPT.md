# RECEIPT — Guild Daylight Queue, Batch 1 (riddler map)

Seat: grok. Date: 2026-08-27. English only. No secrets, keys, or endpoints.

## What I read (paths, not folklore)

**Task-listed shelf (read before writing):**

- `campaigns/villains_guild/daylight/TASK_DAYLIGHT_RIDDLER_MAP.md`
- `docs/concepts/RIDDLER_PROTOCOL.md`
- `mag/riddler.py` (`compile_surrogate`, `PrivateGraph`, `SurrogateStory.to_public`, `validate_surrogate`)
- `mag/surrogate.py` (`decode_response`, `_extract_raw_answer`, `aggregate_responses`)
- `docs/ref/GAME_VILLAIN_GUILD_DESIGN.md`
- `campaigns/villains_guild/module.json`

**Shelf the listed files point at, read so the bind is not invented:**

- `configs/riddler_domains.yaml` (domain templates the codec actually dresses)
- `mag/riddler_transport.py` (the `ANSWER:` plant lives here, not in `compile_surrogate`)
- `mag/campaign.py` (`load_riddler_map`, DM must-not reveal mappings)
- `campaigns/sunless_citadel/riddler_map.json` (existing `riddler_campaign_map.v1` shape)
- `tests/test_campaign.py` (schema `riddler_campaign_map.v1`, `campaign_id`, rooms keyed)
- `tests/test_riddler.py` (same seed → same story)
- `campaigns/villains_guild/quests_room_bound.md` (read only; not modified)
- `campaigns/villains_guild/quests_tradecraft_five.md` (read only; not modified)
- `campaigns/villains_guild/villains_chapter2_canon_trio.md` (read only; not modified)
- `campaigns/villains_guild/daylight/grok_run_log.json` (empty)
- `docs/ref/WORLD_ROLES_AND_RIDDLE.md` (grandparent named by the design law)
- `docs/ref/CUSTODY_AND_DISCLOSURE.md` (riddler rows; raw-answer channel)

## What I wrote

Only under `campaigns/villains_guild/daylight/`:

1. `riddler_map.json` — five rooms bound to the five verification skills through `compile_surrogate`. Map seed `20260827`. Room seeds `202608271`–`202608275`. Schema note at top: `riddler_campaign_map.v1` wrapping codec faces `riddler_surrogate.v1` produced by `mag.riddler.compile_surrogate`. Each room carries both channels.
2. `kid_test_gate.md` — ten paper tasks, ages 9–12, one sitting, parent rubric, 30/70 fun-bar, play-again prompt. Kid-facing only.
3. `RECEIPT.md` — this file.

Not modified: `module.json`, `villains_chapter2_canon_trio.md`, `quests_room_bound.md`, `quests_tradecraft_five.md`.

A one-shot compiler `_compile_map.py` was used to call the codec, then deleted so this folder keeps only the three deliverables plus the assigned task file.

## Bind (from the bytes)

| Room id | Skill (`module.json` `rooms_detail_note` + design-law table) | Domain | Seed | Bound verb | `ANSWER:` expected |
|---|---|---|---|---|---|
| `guildhall_of_gracious_crimes` | `parse_contracts` | `medieval_guild` | 202608271 | `inspect` | `turn the sheet` |
| `hall_of_fine_print` | `cross_reference_documents` | `restaurant_kitchen` | 202608272 | `expedite` | `the named guest` |
| `registry_of_regrets` | `check_sources` | `space_colony` | 202608273 | `scan` | `the quiet archivist` |
| `counting_house_of_minor_miracles` | `verify_arithmetic` | `tower_defense` | 202608274 | `scan` | `8` |
| `overthrow_floor` | `build_consensus` | `fantasy_village` | 202608275 | `consult` | `HOLD then read exhibits` |

Recompile check at those seeds: story text matched on a second `compile_surrogate` call. `validate_surrogate` returned `ok=true`, `leakage_detected=false` for all five. Bound verbs are in each face’s `allowed_story_actions`.

The number `8` is the honest tenth from `quests_room_bound.md` (“A Generous Tenth”: strike moods, unit the handling fee, tenth of 80 gp). It is a private decode target. The public story does not contain it. See gaps.

## Codec gaps (did not hack around them)

`compile_surrogate` is a structural disguiser. It does not carry the verification skill into the public story as readable pedagogy. Recorded, not patched:

1. **`ANSWER:` is not in the compiler.** The plant is `mag/riddler_transport.py` `send_surrogate` system prompt. Extraction is `mag/surrogate.py` `_extract_raw_answer`. The map copies that contract onto each room. The compiled `public_question` still only asks for an allowed story action.
2. **Goal is not woven.** `PrivateGraph.goal` is hashed into `scratch_id` and ignored by `_weave_question`. The public question is “The {role} must {random allowed verb}.”
3. **That random verb is not the answer.** Room 1’s question says “The master must seal.” The bound steering verb is `inspect`. Treating the question’s verb as correctness is the consensus-illusion trap, now inside the compiler. Not rewritten.
4. **Constraint semantics are replaced** by shuffled domain `constraint_patterns`. “Read the reverse” becomes “guild seal required before any work leaves the hall.” Structure (count of constraints) is preserved. Meaning is not.
5. **Conflicts leak literally** (`There is a tension: {conflict[:120]}.`). Graphs used story-language conflicts on purpose so the public face stays fiction. Territory language was not stuffed into conflicts to smuggle the skill.
6. **Numbers are not woven.** Resource records do not emit amounts. The codec cannot express “honest tenth = 8.” Expected `8` is therefore a campaign decode target, not a fact a remote face can compute from the story. Not hacked into a conflict string.
7. **`scratch_id` / `expires_at` are time-stamped.** Dropped from the stored public face so the map is a stable bind. Seed + story_text + maps are the bind.
8. **`shape_hash` hashes counts, not identity.** Rooms 1–4 share `88bfbc76e604a28a` (4 actors, 2 resources, 1 dep, 4 constraints, 1 conflict). Room 5 differs (3 resources).

## Shelf vs this task

- `module.json` `rooms_detail_note` promises room blocks in `riddler_map.json` once merge completes. This task files them at `daylight/riddler_map.json`. Not a contradiction: daylight is pre-merge. **Unproven** that `mag.campaign.load_riddler_map` will see this file — that loader reads `campaign_dir / "riddler_map.json"`, i.e. the campaign root, not `daylight/`.
- Design law kid-test: paper-prototype **one** trap quest, watch **three** real kids; their faces outrank the document. This task: **8–10** tasks covering all five skills. The gate document does both: ten tasks, three-kid rule, faces-outrank. Shelf wins on the three-kid veto.
- Sunless `riddler_map.json` also has hand-authored `action_map` / `ghost_steers`. The codec does not emit those. Not invented. Villains `module.json` rooms are a name/order list with empty `ghost_steer_log`; no steer schedule to bind.
- Room-bound quests match the design-law skill table. Tradecraft B2 quests teach adjacent habits in the same five rooms (postmark, survivorship, gloss, compartments, worldline diff). Both files left untouched. **Disputed** which quest set is “the” room bind until a human merge chooses. This map follows `module.json` + the design-law table, as the task asked.

## Tri-state

| Claim | State | From |
|---|---|---|
| Five rooms exist with those ids and the five named skills | **Supported** | `campaigns/villains_guild/module.json` `rooms` + `rooms_detail_note`; `docs/ref/GAME_VILLAIN_GUILD_DESIGN.md` room→skill table |
| Same seed recompiles the same public story | **Supported** | two `compile_surrogate` calls at each room seed; matches `tests/test_riddler.py` experiment 1 |
| Each stored face validates with no leakage flag | **Supported** | `validate_surrogate` on the five compiles |
| Both channels are the existing protocol, not a new format | **Supported** | `docs/concepts/RIDDLER_PROTOCOL.md`; decode in `mag/surrogate.py`; plant in `mag/riddler_transport.py` |
| Surrogate-action consensus is not correctness | **Supported** | protocol “consensus illusion” (2026-08-10); `aggregate_responses` splits the two vote tallies |
| Public surrogate text teaches the verification skill unaided | **Disputed** | constraint rewrite + random question verb + unwoven goal. Private map is required to decode. |
| Engine will load `daylight/riddler_map.json` in play | **Unproven** | `load_riddler_map` looks at campaign-root `riddler_map.json` |
| `8` is recoverable from the compiled counting-house story | **Disputed** | weaver never emits amounts; `8` is from `quests_room_bound.md`, stored as decode target |
| Kid-test 30/70 will hold at a real table | **Unproven** | no kids have played these ten tasks. Design law: their faces outrank this paper. |
| Villains `module.json` rooms can be indexed as `module["rooms"][room_id]` | **Disputed** | rooms are a **list** of `{id,name,order}`; `mag/campaign.py` does `.get(state.current_room, {})` as if rooms were a dict (sunless shape). Out of scope — did not patch the module. |
| B2 tradecraft skills equal the five verification skills | **Disputed** | same rooms, different skill names in `quests_tradecraft_five.md` |

## Honest unknowns

- Whether dawn merge copies `daylight/riddler_map.json` to campaign root.
- Whether a later seat will add sunless-style `ghost_steers` once rooms grow `steer_schedule` fields. Not in the codec, not invented here.
- Whether `medieval_guild` / `restaurant_kitchen` / `space_colony` / `tower_defense` / `fantasy_village` is the right domain rotation. Chosen to vary fingerprints per `riddler_domains.yaml` header law, not because the codec required those five.
- Kid-test props (real cookie, fridge, crate) are a parent’s house, not this repo.

## Stop

Three deliverables are in `campaigns/villains_guild/daylight/`. Canon trio and quest files untouched.
