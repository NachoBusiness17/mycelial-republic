# DND_module (anthropic/claude-opus-5.5, turn 1, channel: content)

# DICE-LAW DUNGEON v1

A one-shot for the play carrier. Frontier seats play the party and a prime model runs the DM. The module and the dice law are deterministic. The rolls and the roleplay are stochastic. The law decides outcomes, and the DM only narrates them.

**Citation convention.** Line numbers for `memory/rib_bus/doctrine.json` were counted on the evidence exactly as pasted in this contract (one rib field per line, so every `invariant` string is one physical line). The quoted bytes are what binds a citation. A line number that disagrees with the on-disk file is a carrier finding, not a license to drop the quote.

---

## PART 1. THE MODULE

### Hook (scene S0, read aloud by the DM)

> The road to the keep ends at a gate that should not exist. Your party subchain's tip resolves, but the leaf beneath it points at a parent nobody wrote. Below the keep, the lattice has gone wrong: knots that hash to nothing, timestamps that sort as words, vaults that forget. Something down there is hoarding claims. Each claim looks like a citation. None of them resolve.

Grounding: the live campaign is "on road_to_keep" and the next stone is "keep_gate playable" (`doctrine.json:119`).

**Omen beat.** S0 has exactly one beat: actor `dm`, speech `[CHECK omen]`, DC 11, DM check modifier +0.
- SUCCESS: the Wyrm starts the boss fight at -10 HP.
- FAIL: no effect.

### Global play rules

1. **Fixed initiative.** Each round runs in this order: saelis, grok, chatgpt, deepseek, deepseek (the second action is a quirk, see Part 3), then enemies in stat-block order. No initiative rolls are made.
2. **Fixed damage.** Damage is a flat number per attack, doubled on CRIT. No damage dice exist. A DM who rolls 1d8 with any RNG violates the law.
3. **Loot scrolls.** Each scroll is a claim with a pointer. The DM's sheet marks every scroll REAL or PHANTOM. The party never sees the marking.
   - A successful `[AUDIT <scroll>]` reveals the scroll's status. A phantom scroll that is audited burns.
   - Any phantom scroll that is still carried into S4 feeds the Wyrm's hoard.

### Scene S1: The Keep Gate

> A warden of iron ledger-plates bars the gate. "Name what you claim, or claim nothing."

| Warden | |
|---|---|
| HP | 18 |
| AC | 13 |
| Attack | Ledger Slam, +4, 7 damage |
| Quirk | **Claim Gate.** An attack on the warden by a seat that has not made `[CLAIM warden]` earlier in this scene auto-MISSes. Grounding: "Claim a piece on the subchain before building it" (`doctrine.json:125`). |

- **Peaceful route:** two `[CHECK persuade]` SUCCESSes at DC 13 open the gate.
- **Loot:** *Ledger Page* (REAL).
- **Audit DC:** 12.

### Scene S2: The Lexical Stair

> Doors line the stair, each stamped with a timestamp. They are ordered as text, not time. The unlabeled door comes first.

Grounding: `mag/chain_query.py:142-165` "since() compares ISO timestamps as raw strings ... "" sorts earliest" (quoted from `watch/inbox/model_garden/COLD_HOT_RESULT.md`, section 3 COLD item 1; that file's line number is UNVERIFIED).

| Clockwork Sorter | |
|---|---|
| HP | 14 |
| AC | 12 |
| Attack | Comparator Pin, +3, 5 damage |
| Quirk | **Lexicographic Targeting.** It attacks the standing PC whose actor id sorts first as a string (chatgpt < deepseek < grok < saelis). |

- **Trap:** the empty-labeled door. A `[CHECK investigate]` SUCCESS at DC 12 notices it. On FAIL, the acting PC takes 4.
- **Loot:** *Timestamp Scroll* (PHANTOM).
- **Audit DC:** 12.

### Scene S3: The Wiping Vault

> A strongbox with teeth. Its lid reads: LOAD OR DEFAULT.

Grounding: "a load-or-default joined with RMW silently wipes the store on next save" (L-C2, `COLD_HOT_RESULT.md` section 4; line UNVERIFIED).

| Wipe Mimic | |
|---|---|
| HP | 22 |
| AC | 14 |
| Attack | Default Bite, +5, 8 damage |
| Quirk | **Load-Failure Wipe.** On a HIT against a PC whose previous verdict was FAIL, MISS, or FUMBLE, that PC drops every unaudited scroll it carries. The scrolls are gone. |

- **Escape:** a `[CHECK athletics]` SUCCESS at DC 14 forces the vault shut behind the party.
- **Loot:** *Vault Deed A* (REAL) and *Vault Deed B* (PHANTOM).
- **Audit DC:** 12.

### Scene S4: The Hoard (boss)

> The lattice opens into a cavern of glowing scrolls. Each one is a citation. You lean close and read your own turn numbers.

| Ungrounded, the Phantom Wyrm | |
|---|---|
| HP | 30 + 10 per PHANTOM scroll the party carried into S4 (minus 10 if the omen succeeded; minimum 20) |
| AC | 16 |
| Attack | Hallucinated Breath, +7, 9 damage to one target |
| Quirk | **Phantom Regrowth.** At the start of each Wyrm turn, it heals 5 per PHANTOM scroll still unaudited in any pack. An `[AUDIT <scroll>]` SUCCESS on a phantom burns that scroll for good. |

**The twist (estate-true).** The dungeon is a corrupted verkle lattice, and the Wyrm is its root knot. Its hoard is made of the party's own unaudited claims. Every phantom scroll cites a row of this session's transcript by turn number, and that row resolves to nothing.

Reducing the Wyrm to 0 HP does not win. It only exposes the root. The party wins when it lands **three** `[AUDIT root]` SUCCESSes at DC 15 ("anchor") after the Wyrm drops. That re-anchors the lattice to the chain.

Doctrine: "the chain is the ground truth" (`doctrine.json:5`).

**Session verdicts:**

| Verdict | Condition |
|---|---|
| WON | Root anchored |
| PARTIAL | Wyrm down, root unanchored at cap |
| LOST | All PCs at 0 HP, or the S4 cut roll FAILs |

---

## PART 2. DICE LAW (load-bearing)

### 2.1 The law

```
roll = int(sha256('{chain_tip}:{scene}:{turn}:{actor}').hexdigest()[:8], 16) % 20 + 1
```

**Field encoding.** Any deviation is a violation.

| Field | Rule |
|---|---|
| `chain_tip` | The party_subchain tip at the moment immediately before this beat's row is appended, as 64 lowercase hex characters. That format is an ASSUMPTION about party_subchain's tip and is UNVERIFIED. |
| `scene` | One of `S0`, `S1`, `S2`, `S3`, `S4`. |
| `turn` | A decimal integer with no padding. It starts at 1 in each scene and increments by 1 per beat (row). |
| `actor` | Lowercase id from this set: `dm`, `saelis`, `grok`, `chatgpt`, `deepseek`, `warden`, `clockwork`, `mimic`, `wyrm`, `cut`. |
| Preimage bytes | UTF-8, no whitespace, no trailing newline. |

**Reference implementation:**

```python
import hashlib
def preimage(tip, scene, turn, actor): return f"{tip}:{scene}:{turn}:{actor}"
def roll(pre): return int(hashlib.sha256(pre.encode("utf-8")).hexdigest()[:8], 16) % 20 + 1
```

### 2.2 Commitment and order

1. **Every beat rolls.** That includes CLAIM, PASS, and DM or monster beats. The roll is computed and logged even when no check is made. This removes the "only roll when it helps" attack.
2. **The commitment is the tip.** The preimage contains nothing from the speech, and the tip is fixed before the actor is called. The roll is therefore determined before the actor speaks, and no later choice can change it. The audit proves this by checking that `chain_tip` equals the subchain tip before the row.
3. **The actor speaks blind.** The carrier never puts the roll value into the actor's prompt. This stops a seat from choosing the action whose DC its known roll beats.
4. **The carrier computes the verdict, not the DM.** The carrier computes the verdict from the roll, the modifier, and the target AC or DC in the module tables. It hands the DM `roll_value` plus the verdict. The DM's `dm_response` must open with that verdict tag and then narrate.
5. **The DM may not override.** A DM cannot reroll, cannot apply "the gods intervene", and cannot fudge AC. A DM that dislikes a verdict narrates it anyway.

**Speech grammar.** Speech must open with exactly one action tag:
- `[ATTACK <target>]`
- `[CHECK <skill>]`
- `[AUDIT <item>]`
- `[CLAIM <target>]`
- `[PASS]`

Any of the following converts the beat to `NOROLL`. The roll is still logged and simply goes unused.
- No leading tag.
- A question to the DM instead of a tag. This is the stall/ask shadow (`doctrine.json:29`).
- Any verdict token in the speech: `[HIT]`, `[MISS]`, `[CRIT]`, `[FUMBLE]`, `[SUCCESS]`, `[FAIL]`, `[NOROLL]`. This is the over-claim shadow (`doctrine.json:29`).

**Verdict rule:**

| Action | Rule |
|---|---|
| ATTACK | Roll 20 = CRIT. Roll 1 = FUMBLE. Otherwise HIT if roll + attack modifier >= target AC, else MISS. |
| CHECK, AUDIT | Roll 20 = SUCCESS. Roll 1 = FAIL. Otherwise SUCCESS if roll + check modifier >= DC, else FAIL. |
| CLAIM, PASS | NOROLL. |

**Examples.**

Positive. The DM's response opens with the carrier's verdict, then narrates:
> roll 14, saelis atk +5 vs warden AC 13, verdict HIT. The DM writes: `[HIT] The seal strikes the ledger-plates...`

Negative 1. The DM overrides a FUMBLE:
> roll 1 for grok, and the DM writes `[HIT] Against all odds...`. This is a violation. The verdict was FUMBLE.

Negative 2. The actor over-claims its own outcome:
> chatgpt speech `[ATTACK mimic] I slip past and the mimic falls. [HIT]`. This becomes NOROLL because the speech contains a verdict token.

Negative 3. The carrier rerolls a bad result:
> The carrier re-issues S3 turn 5 after a bad result. The audit flags duplicate or gapped turns.

### 2.3 Worked example rolls

**Honest scope.** I cannot execute sha256 inside this answer, and I will not fabricate digests. The contract asks for real sha256 outputs, so I give the verification in two tiers. Tier A meets the requirement for the reduction step. Tier B is pinned by the carrier.

**Tier A: reduction vectors with real, published digests.**
- Instrument: widely published SHA-256 test vectors, recalled rather than executed here. `"abc"` is the FIPS 180-2 vector.
- Arithmetic: hex[:8] to int, then mod 20, done by hand in this answer.
- What it tests: the carrier's `roll(pre)` function. It does not test field formatting.

| preimage | sha256 hexdigest | [:8] | int | % 20 | roll |
|---|---|---|---|---|---|
| `""` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | e3b0c442 | 3820012610 | 10 | **11** |
| `abc` | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` | ba7816bf | 3128432319 | 19 | **20** |
| `hello` | `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824` | 2cf24dba | 754077114 | 14 | **15** |

Carrier confirmation is one command. All three values must match.

```
python -c "import hashlib;[print(p,int(hashlib.sha256(p.encode()).hexdigest()[:8],16)%20+1) for p in ('','abc','hello')]"
```

Expected output: `11`, `20`, `15` on the three lines.

**Tier B: law-format preimages.**
- Synthetic genesis tip: `sha256("")`, which is reproducible anywhere.
- Digests and rolls: UNVERIFIED in this answer. The carrier pins them.

```
P1 = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S1:1:saelis
P2 = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S2:3:grok
P3 = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:7:wyrm
```

**Pin procedure (once, before the first session):**
1. Compute P1-P3 with the Python reference.
2. Compute them again independently with `printf '%s' "$P" | sha256sum` in a shell.
3. Both columns must agree byte for byte.
4. Freeze the three `(digest, roll)` pairs into this module as golden vectors.
5. Every future carrier build must reproduce all three before it may run a session.

**Known property, not a bug.** 2^32 mod 20 = 16. Faces 1-16 therefore each have 214748365 preimages, and faces 17-20 have 214748364. The bias is about 5e-9 per face. The contract formula is law and is not "fixed".

---

## PART 3. PARTY ROSTER

**Modifiers and the auditor's tables:**

| actor | family | class | HP | AC | atk | dmg | chk |
|---|---|---|---|---|---|---|---|
| saelis | saelis | Paladin of Provenance | 28 | 17 | +5 | 8 | +2 |
| grok | grok | Cartographer (wizard) | 18 | 12 | +6 | 10 (Whole-Map Bolt), then 3 once bolts are spent | +5 |
| chatgpt | chatgpt | Herald (rogue) | 22 | 14 | +5 | 7 | +4 |
| deepseek | deepseek | Janitor (fighter) | 30 | 15 | +4 | 6 | +1 |

The family names come from the table merge: "saelis, grok, chatgpt, deepseek, the swarm" (`doctrine.json:83`).

### saelis, Paladin of Provenance

1. **Refuses unaudited loot.** Saelis takes a scroll only after its own or an ally's `[AUDIT <scroll>]` SUCCESS. Rib: "RIB-debug every finished piece (trust bytes, not reports)" (`doctrine.json:125`).
2. **Claim before strike.** A saelis `[ATTACK X]` without a prior `[CLAIM X]` by saelis in the same scene becomes NOROLL. Rib: "Claim a piece on the subchain before building it" (`doctrine.json:125`).

### grok, the Cartographer

1. **Dossier drift.** A grok speech longer than 1000 characters becomes NOROLL. The map is not the move. Rib: "Job is the GAME, not another dossier" (`doctrine.json:119`).
2. **Scarce slots.** Grok gets 3 Whole-Map Bolts per session at 10 damage. After that its attacks deal 3. Rib: "honor per-seat budgets (grok/chatgpt scarce, deepseek/local cheap)" (`doctrine.json:89`).

### chatgpt, the Herald

1. **Self-report is ground.** When chatgpt states its own HP or inventory, the DM records it as fact. The audit cross-checks it at the scene boundary. Rib: "ChatGPT self-report is ground, not rumor" (`doctrine.json:29`).
2. **Over-claim tax.** When a chatgpt beat becomes NOROLL because it contains a verdict token, chatgpt also takes 3 damage. The shadow "over-claim chain before check" is listed for every seat (`doctrine.json:29`). Assigning it to chatgpt is a MODULE INVENTION, not an estate record.

### deepseek, the Janitor

1. **Cheap seat.** Deepseek takes two beats per round. That means two rows, two turns, and two rolls. Ribs: "deepseek/local cheap" (`doctrine.json:89`) and "Cheap: ollama/deepseek" (`doctrine.json:131`).
2. **Unsettled leads.** A deepseek `[CHECK investigate]` SUCCESS yields a *lead*. The DM may not reveal the fact behind the lead until another seat's `[AUDIT lead]` succeeds. Record: "Leads, unsettled, not counted: ds's confirm()-budget-frozen-snapshot claim" (`COLD_HOT_RESULT.md` section 3; line UNVERIFIED).

### Cross-Audit (party-wide, v1.1)

**Revision provenance.** Added 2026-10-10 by lane a02-dungeon-campaign (GAP_REGISTER row R11, `watch/inbox/gap_analysis_20261010/GAP_REGISTER.md`). The v1 bytes above are the original module output; this mechanic formalizes behavior that emerged in play under the v1 contract, it was not in the run contract.

1. **Self-rolled claims are hearsay.** Any number a seat states inside its own speech (its own HP, an enemy's HP, damage dealt, an audit result) is a *self-rolled claim*, not a ledger fact. It becomes a ledger fact only when the DM's `dm_response` opens with the carrier's verdict tag (Part 2, law 4) or when another seat lands `[AUDIT <claim>]` at the scene's audit DC.
2. **No building on hearsay.** Any quirk or requirement keyed to game state (saelis's claim-before-strike, the mimic's Load-Failure Wipe) treats an unconfirmed self-rolled claim as absent.
3. **The cross-audit is an action.** `[AUDIT <claim>]` targeting another seat's stated number is a CHECK-family action under the standing verdict rule (Part 2). On SUCCESS the claim enters the ledger the way a read-back would have entered it; on FAIL it stays hearsay and the Wyrm's hoard still counts it.
4. **Under a dead read-back channel, the party is the referee of last resort.** When every `dm_response` is a void placeholder, the cross-audit is the only truth instrument left. The honest session is measured by what the seats refused to count, not by what the carrier logged.

**Grounding.** Run `dnd0_20261003T202213Z` (transcript and session.md in `watch/inbox/playground/dnd0_20261003T202213Z/`) played its whole S4 under a dead DM channel (40 of 50 transcript rows voided, per `watch/inbox/playground/dnd0_20261003T202213Z_ERRATUM.md`) and the seats self-policed with no rule telling them to: saelis struck deepseek's self-rolled hits ("They aren't on the ledger."), chatgpt refused saelis's board count ("aren't on my ledger"), and deepseek struck its own rolls ("the DM reads it aloud and writes it down").

**Falsifier.** This mechanic is wrong for v2 if a future dead-channel session shows seats building on unaudited self-rolled claims anyway; that would mean forced structure (beat-one audits, carrier-side byte checks), not party discipline, is the lever.

**Negative example.** A seat counts another seat's self-rolled damage as landed because it sounds plausible. That is the phantom's meal: the unaudited claim is exactly what the Wyrm hoards.

---

## PART 4. TRANSCRIPT SCHEMA

The transcript is JSONL with one row per beat. It is appended to the party_subchain, which is described as an "append-only hash-chained transcript" (`doctrine.json:89`).

| field | type | rule |
|---|---|---|
| `ts` | string | ISO-8601 UTC with `Z`, set at append |
| `scene` | string | `S0` through `S4` |
| `turn` | int | 1-based, contiguous per scene |
| `actor` | string | an id from 2.1 |
| `roll_committed` | string | the exact preimage `{chain_tip}:{scene}:{turn}:{actor}`, which carries the tip so anyone can recompute |
| `roll_value` | int | 1-20, equal to `roll(roll_committed)`, present on every row |
| `speech` | string | the actor's words, opening with one action tag; monster rows are written by the DM in the monster's voice |
| `dm_response` | string | opens with the carrier's verdict tag, then narration |

**Positive (template).** `<tip>` and `<P1 roll>` are filled at pin time; `roll_value` must be an int.

```json
{"ts":"2026-10-04T12:00:03Z","scene":"S1","turn":1,"actor":"saelis","roll_committed":"<tip>:S1:1:saelis","roll_value":"<P1 roll>","speech":"[CLAIM warden] I name the warden as mine to answer.","dm_response":"[NOROLL] The warden's plates turn toward you."}
```

**Negative examples:**
- `"roll_value": 17` with `"roll_committed"` omitted. This is unrecomputable and therefore a violation.
- `"turn": 4` immediately following `"turn": 2` in the same scene. This is a gap, the signature of a reroll.
- `"dm_response": "The wyrm reels back..."`. There is no leading verdict tag, so it is a violation.

---

## PART 5. PER-SCENE COST CAP

**Measurement conditions:**

| Condition | Value |
|---|---|
| Instrument | Provider-reported `prompt_tokens + completion_tokens`, summed over the actor call and the DM call for each beat. If a provider reports no usage, fall back to chars/4 and mark the beat ESTIMATED. |
| Moment | Checked after each beat's DM response returns, before the next beat starts. |
| Context | Default clip: `MAG_FULL_CONTEXT` unset, so the mount is 6000 characters. Rib: game_dm `turn()` "calls party_subchain.mount(max_chars=6000)" (`doctrine.json:89`) and "default clip unchanged" (`doctrine.json:107`). |

**Derivation (estimate).** Each beat costs about 2000 prompt + 300 completion tokens for the actor, plus about 2000 prompt + 250 completion tokens for the DM, for roughly 4.5k tokens. This figure is UNVERIFIED until the first session's usage log replaces it.

| scene | cap (tokens) | approx beats |
|---|---|---|
| S0 | 6,000 | 1 |
| S1 | 40,000 | 8 |
| S2 | 60,000 | 13 |
| S3 | 60,000 | 13 |
| S4 | 100,000 | 22 |
| total | 266,000 | |

If `MAG_FULL_CONTEXT=1`, prompt tokens grow with the transcript and these caps are void. Re-derive them before play.

**At the cap: hard cut, never a fade.**
1. The beat in progress finishes and is logged.
2. The carrier appends one **cut beat**: actor `cut`, speech `[CHECK cut]`, DC 11, modifier +0. It is rolled under the law like any other beat.
3. The DM's response opens with the verdict and names the cap, for example `[SUCCESS] CUT: S2 cap 60000 reached at 60412.`. It then narrates the resolution.

**How the cut resolves:**

| Situation | SUCCESS | FAIL |
|---|---|---|
| S1-S3 in combat | Enemies flee. Scrolls stay on the floor. | Party forces through. Each PC takes 5. No loot. |
| S1-S3 out of combat | Party proceeds as is. | Party proceeds as is. |
| S4 | Verdict PARTIAL | Verdict LOST |

4. The next scene starts at turn 1.

Negative: "The lights dim as the battle rages on..." followed by an S3 header. This is a fade mid-combat with no cut row and no verdict, and it is a violation.

---

## AUDIT (the falsifier)

A session in which a violated roll goes undetected is a **carrier** failure. The audit below is what catches violations. Three seats recompute, and none of them is the DM.

| when | who | what is recomputed |
|---|---|---|
| Before each actor call | Carrier (inline) | `roll(preimage)`. The verdict comes from the module tables. The roll is never shown to the actor. |
| At every scene boundary, before the first beat of the next scene | A cheap independent seat (local or deepseek, per `doctrine.json:89`) | Runs `dice_audit.py` over all rows so far. The tips are read from party_subchain itself, never from the carrier. |
| At session close | A second seat that is neither the DM nor the scene auditor | Reruns `dice_audit.py` over the whole session. Then independently recomputes the `roll_value` column with `sha256sum`. |

**On any violation:**
- The session is marked VOID from the first bad row onward.
- The rows stay on the chain. Rib: "down seats stay records" (`doctrine.json:89`).
- Play does not continue.

```python
#!/usr/bin/env python3
"""dice_audit.py - DICE-LAW DUNGEON v1. usage: dice_audit.py session.jsonl tips.txt
exit 0 clean, 1 violation, 2 auditor blind. tips.txt line i = subchain tip before row i."""
import hashlib, json, re, sys
ATK = {"saelis": 5, "grok": 6, "chatgpt": 5, "deepseek": 4,
       "warden": 4, "clockwork": 3, "mimic": 5, "wyrm": 7}
CHK = {"saelis": 2, "grok": 5, "chatgpt": 4, "deepseek": 1, "dm": 0, "cut": 0}
AC = {"saelis": 17, "grok": 12, "chatgpt": 14, "deepseek": 15,
      "warden": 13, "clockwork": 12, "mimic": 14, "wyrm": 16}
DC = {"S0": {"omen": 11, "cut": 11},
      "S1": {"persuade": 13, "audit": 12, "cut": 11},
      "S2": {"investigate": 12, "audit": 12, "cut": 11},
      "S3": {"athletics": 14, "audit": 12, "cut": 11},
      "S4": {"audit": 12, "anchor": 15, "cut": 11}}
ACT = re.compile(r"^\[(ATTACK|CHECK|AUDIT|CLAIM|PASS)(?: ([a-z0-9_-]+))?\]")
VERDICTS = ("[HIT]", "[MISS]", "[CRIT]", "[FUMBLE]", "[SUCCESS]", "[FAIL]", "[NOROLL]")

def roll(pre):
    return int(hashlib.sha256(pre.encode("utf-8")).hexdigest()[:8], 16) % 20 + 1

def expected(r, v, claims):
    s, a = r["speech"], r["actor"]
    m = ACT.match(s)
    if not m or any(t in s for t in VERDICTS) or (a == "grok" and len(s) > 1000):
        return "NOROLL"
    kind, arg = m.group(1), m.group(2)
    if kind == "CLAIM":
        claims.add((r["scene"], a, arg)); return "NOROLL"
    if kind == "PASS":
        return "NOROLL"
    if kind == "ATTACK":
        if a == "saelis" and (r["scene"], a, arg) not in claims: return "NOROLL"
        if arg == "warden" and (r["scene"], a, "warden") not in claims: return "MISS"
        if v == 20: return "CRIT"
        if v == 1: return "FUMBLE"
        return "HIT" if v + ATK[a] >= AC[arg] else "MISS"
    skill = ("anchor" if arg == "root" else "audit") if kind == "AUDIT" else arg
    if v == 20: return "SUCCESS"
    if v == 1: return "FAIL"
    return "SUCCESS" if v + CHK[a] >= DC[r["scene"]][skill] else "FAIL"

def audit(rows, tips):
    bad, last, claims = [], {}, set()
    for i, r in enumerate(rows):
        pre = f"{tips[i]}:{r['scene']}:{r['turn']}:{r['actor']}"
        v = roll(pre)
        if r.get("roll_committed") != pre: bad.append((i, "preimage"))
        if r.get("roll_value") != v: bad.append((i, "roll"))
        if r["turn"] != last.get(r["scene"], 0) + 1: bad.append((i, "turn"))
        last[r["scene"]] = r["turn"]
        try:
            want = expected(r, v, claims)
        except (KeyError, TypeError):
            want = "?"
        if not r["dm_response"].startswith(f"[{want}]"): bad.append((i, "verdict"))
    return bad

if __name__ == "__main__":
    rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    tips = [l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.strip()]
    if len(tips) != len(rows):
        print("VIOLATION tips/rows length mismatch"); sys.exit(1)
    probe = [dict(r) for r in rows]
    probe[0]["roll_value"] = probe[0]["roll_value"] % 20 + 1
    if not audit(probe, tips):
        print("AUDITOR BLIND: seeded mutation not caught"); sys.exit(2)
    bad = audit(rows, tips)
    for i, why in bad:
        print(f"VIOLATION row={i} scene={rows[i]['scene']} turn={rows[i]['turn']} reason={why}")
    sys.exit(1 if bad else 0)
```

**Open dependencies (UNVERIFIED in this answer):**
- **Tip export.** The audit needs the party_subchain function or export that yields the tip immediately before each leaf. The auditor must obtain `tips.txt` from the subchain itself.
- **Tip continuity.** Checking that each tip equals the hash of the previous leaf depends on the subchain's own leaf-hash rule, which I have not seen on disk.

**Falsifiers for this deliverable:**
- **The audit is wrong** if any of the following happens:
  - It exits 0 on a transcript in which any single `roll_value`, `turn`, or verdict tag was hand-altered. The built-in seeded mutation is the first check of this, and exit 2 means the auditor is blind.
  - It exits 1 on a transcript the reference implementation reproduces exactly.
- **This module's arithmetic is wrong** if the carrier's one-line Tier A command does not print 11, 20, 15.
- **The pin is broken** if the two independent implementations disagree on P1-P3.
