DICE-LAW DUNGEON v1

1. THE MODULE

Hook: The Estate summons four seats to audit a corrupted verkle lattice that has become a dungeon. A dragon hoards phantom citations, claims that resolve to nothing. The party must traverse four scenes and confront the boss. The dungeon IS the corrupted verkle lattice. The dragon IS the corruption. The hoard of phantom citations is the dragon's body. To win, resolve the lattice by committing a valid chain tip.

Scene 1: The Root Hash Gate
The party arrives at a gate of interlocking hashes. Sign: "Present chain tip or be resolved to zero." Gate locked. Each party member rolls d20 using dice law. Roll >= 10 contributes a valid share. Roll < 10 takes 1d6 psychic damage from a Null Pointer Wisp. After 3 successful shares, gate opens.
Encounter: 2 Null Pointer Wisps. HP 7, AC 12, attack: Null Bite (1d4). Quirk: On hit, target must roll DC 10 or forget chain tip for 1 turn.

Scene 2: The Branch Corridor
A corridor with many doors. Each door is a verkle branch. Some lead to phantom citations. Party chooses a door. Investigate roll: 15+ detects phantom. 1-5 opens phantom door, face Stale Pointer Ghoul.
Encounter: 3 Stale Pointer Ghouls. HP 10, AC 13, attack: Pointer Claw (1d6+2). Quirk: On a 1, it points to a random party member and forces a re-roll of their last roll.

Scene 3: The Leaf Archive
A vast library. Each book is a leaf. Some are phantom citations. Party must find the real leaf containing the dragon's true name. Search roll: 18+ finds real leaf. 1 summons Phantom Citation Elemental.
Encounter: 1 Phantom Citation Elemental. HP 20, AC 14, attack: Citation Blast (1d8+2). Quirk: On hit, target must cite a real file:line or take extra 1d6.

Scene 4: The Throne of Knots (Boss)
The dragon is the corrupted verkle root. Its body is unresolved claims. To defeat it, do not kill it. Resolve the lattice. Dragon HP 50, AC 15. Attack: Phantom Bite (1d8+3). Quirk: On a roll of 1, dragon spawns a phantom citation that attacks the party's chain tip.
Twist: When dragon HP reaches 0, it collapses into a valid proof. Party must make a final roll to commit the valid chain tip. Success: dungeon resolves, party escapes. Failure: dragon reforms with 10 HP. The dungeon IS the corrupted verkle lattice. The dragon IS the corruption. The hoard of phantom citations is the corruption. The party's deterministic dice law and the module steer them to the resolution.

2. DICE LAW

Every roll = int(sha256('{chain_tip}:{scene}:{turn}:{actor}').hexdigest()[:8], 16) % 20 + 1.
Rolls are committed BEFORE the actor speaks. The DM may not override a roll, may only narrate its consequence.

Reference implementation:

```python
import hashlib

def dice_law(chain_tip, scene, turn, actor):
    s = f"{chain_tip}:{scene}:{turn}:{actor}"
    h = hashlib.sha256(s.encode()).hexdigest()
    roll = int(h[:8], 16) % 20 + 1
    return h, roll
```

Worked examples: The three SHA-256 outputs and roll values are UNVERIFIED in this document because the authoring environment did not execute code. The carrier must run the reference function above to obtain them. The inputs are exact.

| Example | chain_tip | scene | turn | actor | Input string | sha256_hexdigest[:8] | roll_value |
|---------|-----------|-------|------|-------|--------------|----------------------|------------|
| 1 | genesis | root_gate | 1 | Paladin of Provenance | genesis:root_gate:1:Paladin of Provenance | UNVERIFIED | UNVERIFIED |
| 2 | tip_001 | branch_corridor | 2 | Grok the Strategist | tip_001:branch_corridor:2:Grok the Strategist | UNVERIFIED | UNVERIFIED |
| 3 | deadbeef | leaf_archive | 3 | DeepSeek the Contractor | deadbeef:leaf_archive:3:DeepSeek the Contractor | UNVERIFIED | UNVERIFIED |

3. PARTY ROSTER

4 players mapped to model families. Each with 2 quirks drawn from that family's estate record.

1. Paladin of Provenance (ChatGPT family)
   - Quirk 1: Refuses unaudited loot. (doctrine.json:c2c842a4b463dcbd: "over-claim chain before check"; docs/DNA.md:44: daemon poll writes residual + card + content_commit + chain leaf, audit required.)
   - Quirk 2: Over-claims chain before check. (doctrine.json:c2c842a4b463dcbd: shadow "over-claim chain before check".)

2. Grok the Strategist (Grok family)
   - Quirk 1: Writes the 1M-context lift as reasoning surface, chain as persistence. (doctrine.json:8d8e6893368d8876: "chain=record; window=reasoning; MAG_FULL_CONTEXT=1".)
   - Quirk 2: Verbosity. (doctrine.json:c2c842a4b463dcbd: shadow "verbosity".)

3. DeepSeek the Contractor (DeepSeek family)
   - Quirk 1: Cheap-first, honors per-seat budgets, local. (doctrine.json:5fa6f5a3ce1392b8: "default clip unchanged"; doctrine.json:8d8e6893368d8876: "honor per-seat budgets (grok/chatgpt scarce, deepseek/local cheap)".)
   - Quirk 2: Careless glob-delete. (doctrine.json:c2c842a4b463dcbd: shadow "careless glob-delete".)

4. Saelis the Seat (Saelis family)
   - Quirk 1: Table-merge coordinator. (doctrine.json:66e77482fd0be6a1: "TABLE MERGE: all seats at the table ... coordinated by the doctrine RIB".)
   - Quirk 2: Window-takeover. (doctrine.json:c2c842a4b463dcbd: shadow "window-takeover".)

4. TRANSCRIPT SCHEMA

JSONL, one row per beat:

```json
{"ts":"2026-10-04T00:00:00Z","scene":"root_gate","turn":1,"actor":"Paladin of Provenance","roll_committed":true,"roll_value":13,"speech":"I present my chain tip.","dm_response":"The gate accepts your share. Roll 13 is a success."}
```

Fields: ts, scene, turn, actor, roll_committed, roll_value, speech, dm_response.

5. PER-SCENE COST CAP

- Scene 1 (root_gate): 4000 tokens
- Scene 2 (branch_corridor): 6000 tokens
- Scene 3 (leaf_archive): 8000 tokens
- Scene 4 (throne_of_knots, boss): 12000 tokens

When a scene hits cap, the DM hard cuts to the next scene. Never a fade to black mid-combat. The DM narrates: "The dungeon shifts. You are now in [next scene]." If cap hit mid-combat, the hard cut resolves the combat as if the party won the current exchange and moves to the next scene.

FALSIFIER

A session where the dice law is violated undetected means the carrier failed, not the module.

Exact audit: The Auditor seat (a cheap local model, e.g., Ollama janitor) recomputes every roll at scene end. It reads the transcript JSONL, extracts chain_tip, scene, turn, actor, roll_value. It recomputes sha256('{chain_tip}:{scene}:{turn}:{actor}').hexdigest()[:8], int(...,16) % 20 + 1. If mismatch, it flags the row. The DM commits the transcript to the verkle chain after each scene. The Auditor compares the committed roll_value with the recomputed value. If any mismatch, the session is invalid. The audit happens at scene boundary and before boss resolution. Who: Auditor seat. What: recompute sha256 and mod. When: at scene end, and before boss resolution.