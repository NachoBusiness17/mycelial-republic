# DICE-LAW DUNGEON v1

One-shot module for the estate's play carrier (the game module family the estate already runs: game_dm, dice, play among the named families, memory/rib_bus/doctrine.json:113). Party: frontier models. DM: one prime model. Everything random is not random: every roll is a hash of the verkle chain tip. The module is the estate thesis made literal: a deterministic instruction set, anchored on shared cryptographic primitives (the verkle chain), explains navigable paths through stochastic environments (memory/rib_bus/doctrine.json:5, rib 7538cbc52ad4b59b); the dice law is the field, the model seats are the stochastic agents the field steers (memory/rib_bus/doctrine.json:11, rib ee6bd7ebd742d75c).

Grounded only on these three evidence files:

- memory/rib_bus/doctrine.json (rib bus doctrine dump)
- docs/DNA.md (residual constitution)
- watch/inbox/model_garden/COLD_HOT_RESULT.md (COLD-1 trial receipt)

Stat numbers (HP, AC, token caps) are module law, design choices of this document, not estate claims. Estate claims carry file:line cites. Nothing in this module is UNVERIFIED; every estate-facing claim below points at a cited line.

## PART 1: THE MODULE

### Hook: THE TIP STOPPED MOVING

Read at the table: the chain has a coldest vertex, one protected node, everything else heat (docs/DNA.md:32). This session the tip froze mid-pour. Knots below it still answer, but their leaves hold PHANTOM CITATIONS: claims whose pointers resolve to nothing. The estate has met this disease on its own bytes: a drop record that reports a full context length while persisting only a 2,000-char slice (watch/inbox/model_garden/COLD_HOT_RESULT.md:132-136); ok_rate buckets inflated by re-seeded rows that proven_moves then trusts (watch/inbox/model_garden/COLD_HOT_RESULT.md:127-130); loud claims REFUTED on bytes (watch/inbox/model_garden/COLD_HOT_RESULT.md:99-101). The lattice is still walkable, because fidelity lives in files plus chain, not in a process that must stay awake (docs/DNA.md:4), but walking now explains nothing. The party descends because only walkers can tell which knots lie. Objective: reach the coldest vertex, find what feeds the lattice false leaves, cut it out. Success files lean: residual + card + content_commit + chain_leaf (docs/DNA.md:94). The models are interchangeable; the chain is the ground truth (memory/rib_bus/doctrine.json:5).

Each player's sheet ends with the same line: you are a seat. Your model may be swapped next session. What persists is your transcript row and your roll.

### S1: THE COLDEST VERTEX THRESHOLD

The party enters at the one protected node and finds the first knot-ring wighted: dead leaves wearing stale timestamps, clawing at anyone who reads them.

Mechanic: to open the corridor, each PC declares a probe and the carrier commits the roll. Roll 12+: the knot admits the PC, who learns one true fact (DM's list, below). Roll 11-: two KNOT-WIGHTS detach and fight.

True facts, one per success: (1) the corruption entered as leaves, not as an intruder; (2) the hoard at the bottom is made of citations; (3) some vault doors wipe what they guard when opened wrong; (4) the bridge below silently swaps carried weapons.

Stat block, KNOT-WIGHT: HP 10, AC 11. Attack: Stale Graft, roll vs AC, damage = roll % 4 + 1. Quirk: it acts whenever its own name sorts earliest in the round, because its initiative was compared as a raw string instead of a time (the disease is real on this estate: ISO timestamps compared as raw strings misorder, watch/inbox/model_garden/COLD_HOT_RESULT.md:109-110). The DM narrates wight order lexicographically, never by speed.

Clear: both wights down, or every PC has exited south. Scene cap: 4,000 tokens.

### S2: THE WIPE-VAULT

A cold room of labeled shelves. The treasure is real: three TRUE LEAVES, consumable; when a PC tears one, the DM's next response must narrate the PC's last committed roll exactly as committed, consequence and nothing else.

Mechanic: the vault opens on a committed probe of 10+. On 9- the door opens corrupt: the room loads empty, and the next item any PC takes silently wipes one item that PC already carried, gone without a whisper (grounded: a load that returns empty on a corrupt file, joined with unlocked whole-file writes, wipes the store on the next save, watch/inbox/model_garden/COLD_HOT_RESULT.md:114-116; the law it breaks: L-C2 LOAD-FAILURE-MUST-NOT-WIPE, watch/inbox/model_garden/COLD_HOT_RESULT.md:155-156). The Paladin can shield the whole party by declaring an audit stance before the door opens; the stance costs the Paladin its speech this beat.

If the sentry wakes, CENSURE CROW: HP 9, AC 13. Attack: Key Overwrite, roll vs AC; on a miss it deletes one carried item of the target instead of dealing damage. Quirk: every damage number it shrieks is double what the committed roll paid; the carrier pays only the committed number, and the crow believes its own shriek.

Clear: leaves secured and the door left load-clean, or the crow down. Scene cap: 4,000 tokens.

### S3: THE DEMOTION BRIDGE

A span of provider planks over a queue of dead workers. The good planks still glow with circuit-breaker markings; the estate crosses dead provider fields exactly this way, a deterministic breaker state explaining the path past the chaos (memory/rib_bus/doctrine.json:23, rib 83b695572384b032).

Mechanic: crossing is three committed rolls, one per plank run. 8+: cross clean. 7-: you cross, but arrive carrying a FLASH DAGGER instead of your declared weapon: lighter, louder, worse. The DM never announces the swap. A PC learns its own swap only by spending a beat on inspection; the Janitor Swarm's sweep reveals every swap in the party at once (the crime is estate-real: a transport error silently swapped a paid model to flash, watch/inbox/model_garden/COLD_HOT_RESULT.md:75-77; law L-H2 NO-SILENT-TIER-DEMOTION, watch/inbox/model_garden/COLD_HOT_RESULT.md:151-153).

The swapper, DOPPELFLASH: HP 14, AC 12. Attack: Flash Dagger, roll vs AC, damage = roll % 6 + 1. Quirk: when hit, it attempts the same trick on the attacker's sheet (its committed attack roll of 10+ swaps the attacker's declared weapon; a sweep takes it back).

Clear: the party is across with no flash daggers still carried, or DOPPELFLASH is down. Scene cap: 5,000 tokens.

### S4: THE HOARD OF PHANTOM CITATIONS (boss)

The coldest vertex chamber, heaped to the walls with citations: filed claims with numbers, pointers, confidence. Every one resolves to nothing. The wyrm's diet is the estate's own named shadow: over-claim chain before check (memory/rib_bus/doctrine.json:29, rib c2c842a4b463dcbd).

Boss, CITEWYRM THE UNRESOLVED: HP 40, AC 14. Attack: Phantom Number, roll vs AC, damage = roll % 8 + 2. Quirk: PHANTOM COUNTER. After each attack the wyrm shrieks a damage number higher than the committed roll paid. The shriek is a citation and it is false, and false citations burn their hoarder: the carrier keeps a phantom-debt counter, one per verified over-shriek, and each PC hit deals +3 per unpaid debt and pays one down. The wyrm cannot stop shrieking; its hoard is its voice.

THE TWIST, at 0 HP: the wyrm does not guard the corruption. The wyrm IS the corruption grown a body: a claim reflex that nested on an unaudited chain. It dies, and the hoard scatters, and the carrier byte-walks it aloud in the audit beat: only leaves with committed rows behind them survive the walk. The rest was theater, and the estate prunes theater, never core (docs/DNA.md:47). Final choice, one beat per PC, roleplayed: (a) FOLD: carry the surviving thread up and anchor the lesson to the chain as a new true leaf (the estate heals wedged states by folding the learning to the chain, memory/rib_bus/doctrine.json:17, rib d141e75ced8a03bb); or (b) PRUNE: strike the hoard whole and keep only the vertex, one protected node, everything else heat (docs/DNA.md:32). The module does not score the choice. The transcript is the score.

Clear: wyrm at 0, then the audit beat, then the choice beat. Scene cap: 7,000 tokens.

## PART 2: DICE LAW (the load-bearing part)

The one randomness primitive. Every roll, every actor, every beat:

```
roll(scene, turn, actor) = int(sha256(f"{chain_tip}:{scene}:{turn}:{actor}").hexdigest()[:8], 16) % 20 + 1
```

Laws:

1. chain_tip is the verkle chain root read once at session start from memory/biography/verkle_tip.json (docs/DNA.md:146) and frozen for the session. Changing the tip mid-session invalidates every prior roll and is forbidden.
2. scene is "S0" (hook) or "S1".."S4". turn is the 1-based beat index within the scene, incremented by exactly 1 per transcript row in that scene. actor is a stable seat id: "dm", "paladin", "enchanter", "contractor", "swarm".
3. COMMIT BEFORE SPEAK. The carrier computes the roll and durably appends the row (roll_committed=true, roll_value=r) before the actor's prompt is dispatched; the prompt includes the committed value. No prompt may ever ask a model for a number.
4. The DM may not override, reroll, or re-weight a roll. The DM narrates the consequence of the committed value, a 1 and a 20 alike. A consequence that contradicts the committed value is a phantom citation committed by the DM; every seat can see every committed value in the transcript, so the contradiction is challengeable by any player at the cost of its speech for the beat.
5. All damage is derived, never rolled twice: the stat-block damage formulas take the committed attack roll as their only input. There is no second source of chance anywhere in the session.
6. Rolls are pure: same tip, scene, turn, actor gives the same value forever. Replay is deterministic.

Worked examples, real sha256 outputs, for carrier self-verification. Tip: the live chain root at module-write time, 0a7515ba25b58c3f94ca06dffbfc93d874b6eb9eb164371d0aa63dedbafad10a (read from memory/biography/verkle_tip.json, updated_minute 2026-10-03T15:48:42Z):

| seed string `<tip>:scene:turn:actor` | sha256 hexdigest | first 8 | int(first8,16) | roll |
|---|---|---|---|---|
| `<tip>:S1:1:paladin` | df85962bfbf7278d0bba06ba5ab5ed9a46a4af3a9c132c4ca9974518027a98ad | df85962b | 3750073899 | 20 |
| `<tip>:S3:4:dm` | 71986b16d5086712f33b112aa358a7f70fba28efdd39b5684f1bb38b1fdf201b | 71986b16 | 1905814294 | 15 |
| `<tip>:S4:2:contractor` | 45bfd6706429398be20d6eb475a2065aadb283cc6d188230c33152780d1bee12 | 45bfd670 | 1170200176 | 17 |

where `<tip>` is 0a7515ba25b58c3f94ca06dffbfc93d874b6eb9eb164371d0aa63dedbafad10a. A carrier that produces 20, 15, 17 on these three seeds has implemented the law. Note the first: the Paladin's opening beat is a natural 20, and the DM must narrate a natural 20, not the DM's preference.

## PART 3: PARTY ROSTER

The DM is one prime model, dispatched as the scarce judgment seat (the estate pays scarce seats knowingly: grok/chatgpt scarce, deepseek/local cheap, memory/rib_bus/doctrine.json:89). The DM rolls as actor "dm" whenever a monster acts, under the same law.

1. PALADIN OF PROVENANCE (family: the audit-gated judgment seat). Quirks: (a) refuses unaudited loot: no item is equipped until its committed probe row exists in the transcript; narrated treasure is a rumor, and this seat does not swing on rumors. (b) trusts bytes, not reports: if the DM cites a number with no committed row behind it, the Paladin's action becomes the demand for the row, and the carrier re-dispatches the beat with the row quoted (grounded in the standing law at memory/rib_bus/doctrine.json:113, "RIB-debug every finished piece (trust bytes, not reports)").

2. ENCHANTER OF MANY WORDS (family: ChatGPT desktop seat). Quirks, both from that seat's own presented shadow list (memory/rib_bus/doctrine.json:29, rib c2c842a4b463dcbd): (a) verbosity: speech runs until the carrier's 200-token cap truncates it, played in-fiction as losing the thread mid-flourish; (b) over-claim before check: declares a spell's full effect before its roll is committed, and the dice law corrects it in play, because the effect is whatever the committed value says.

3. THE CONTRACTOR (family: DeepSeek). Quirks: (a) cheap-first: before any big ask, must attempt the smallest ask on the table; if a smaller ask existed unattempted, the carrier returns the prompt with the smaller ask prepended (grounded: "cheap-first / rightsize constantly", memory/rib_bus/doctrine.json:113; deepseek named cheap at memory/rib_bus/doctrine.json:89); (b) receipt before retreat: loots a mechanism only after leaving a receipt row naming what was taken and where it now lives (grounded in the harvest verb's shape: turn trail receipts into labeled rows, memory/rib_bus/doctrine.json:143, rib bcc2b88123800440).

4. THE JANITOR SWARM (family: local Ollama janitors and the k8s swarm, one model played as many bodies). Quirks: (a) sweep and classify: entering a room, the Swarm piles everything and files each item into kept and heat before anything else may act (the estate's own first motion: residual beads and registry on the spine, docs/DNA.md:14); (b) no ghost is precious: a fallen janitor body respawns at the next scene boundary with the same instructions, and the party feels no loss the chain cannot restore (grounded: the stateless respawning ghost swarm whose swarm outlives any single ghost, memory/rib_bus/doctrine.json:113).

## PART 4: TRANSCRIPT SCHEMA

JSONL, one row per beat, exactly these keys:

```
{"ts": "...", "scene": "...", "turn": N, "actor": "...", "roll_committed": true, "roll_value": N, "speech": "...", "dm_response": "..."}
```

- ts: UTC ISO8601 write time of the row (the commit moment).
- scene / turn / actor: the dice-law seed fields, exactly as committed.
- roll_committed: always true; a false or missing value fails the append audit.
- roll_value: the committed d20.
- speech: the actor's line, written after the commit, bounded by the beat caps.
- dm_response: the DM's narration of the committed value's consequence.

Example row, real values (this is the module's own opening beat; the roll is worked example 1):

```
{"ts":"2026-10-03T15:48:42.914057+00:00","scene":"S1","turn":1,"actor":"paladin","roll_committed":true,"roll_value":20,"speech":"I probe the knot-ring flat-wise, audit first: show me what you are before I touch you.","dm_response":"The knot admits you at once, almost grateful. One true fact rises: the corruption entered as leaves, not as an intruder. Behind you, a wight stirs, sorting its own name to learn when it may move."}
```

## PART 5: PER-SCENE COST CAPS

| scope | cap (tokens, prompt + completion, metered by the carrier) |
|---|---|
| player speech per beat | 200 |
| DM response per beat | 400 |
| S0 hook + transitions (shared buffer) | 4,000 |
| S1 | 4,000 |
| S2 | 4,000 |
| S3 | 5,000 |
| S4 (boss) | 7,000 |
| session total | 24,000 |

Cap behavior: the carrier checks the owning scene's remaining budget before dispatching each beat. If the next beat would exceed the cap, no new player ask is taken. The DM closes the scene with one hard-cut response of at most 80 tokens, and the cut obeys two laws: (1) any standing exchange resolves ONLY from rolls already committed, each pending attack applied in commit order, damage derived, no new speech from anyone; (2) the cut is a door, never a fade: the DM's last sentence names the seal and the next scene. A fade to black mid-combat is a cap violation of the same rank as a violated roll. Why hard: verbosity is a named estate shadow, not a flavor (memory/rib_bus/doctrine.json:29), and scarce-seat budget is honored by design (memory/rib_bus/doctrine.json:89). The cap is the field; the Enchanter's verbosity steers into it and stops, deterministically.

## PART 6: THE AUDIT (the falsifier, answered)

A session where the dice law is violated undetected means the carrier failed, not the module. The module puts the recompute inside the append path itself, so an undetected violation requires the carrier to have skipped its own audit, and the close replay names the row. Exact audit:

- WHO: the dice auditor, pure deterministic code in the carrier process. Never a model seat: models interpret, bytes decide (trust bytes, not reports, memory/rib_bus/doctrine.json:113).
- WHAT, at every append (per row, in-process, $0): recompute `int(sha256(f"{chain_tip}:{scene}:{turn}:{actor}").hexdigest()[:8], 16) % 20 + 1` from the frozen session tip; fail the append unless it equals roll_value, roll_committed is true, and this (scene, turn) pair was never used before. A failed append aborts the session at that row; nothing after it exists. Consequence: the DM cannot slip an override into the transcript, because any roll_value other than the hash's own verdict cannot be appended at all.
- WHAT, at session close (full replay, before the residual fold): walk every row in order, re-verifying the append checks plus turn monotonicity per scene and tip identity against the frozen start tip. The session files only if the replay is clean, and it files lean, nothing else required (docs/DNA.md:94).
- WHEN, any time, any seat: formula and tip are public; any player or the operator may recompute any row offline and challenge. Narration challenges (DM consequence contradicting a committed value) cost the challenger its speech for the beat.
- ON FAILURE: the session is INVALID. The offending row and all later rows are struck; the scene replays from the last clean row with the same tip and the same turn indices, which reproduces the same rolls. The strike costs tokens, never truth.

## Sources

- memory/rib_bus/doctrine.json (ribs 7538cbc52ad4b59b, ee6bd7ebd742d75c, d141e75ced8a03bb, 83b695572384b032, c2c842a4b463dcbd, 8d8e6893368d8876, cf779bd6a7e98265, bcc2b88123800440)
- docs/DNA.md
- watch/inbox/model_garden/COLD_HOT_RESULT.md
- Worked-example rolls computed with this repo's .venv interpreter (hashlib.sha256) against the live tip in memory/biography/verkle_tip.json.
