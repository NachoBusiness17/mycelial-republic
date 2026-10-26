# KABUKI_FACES_fold (anthropic/claude-opus-5.5, turn 1, channel: content)

# FACE FOLD: kabuki_cast.v1 onto the arena

**Citation convention.** I counted line numbers by hand from the evidence as pasted. The quoted bytes are the anchor. If a number drifts, grep the quote.

Short paths used below:
- `cast` = `configs/kabuki_cast.json`
- `tx` = `watch/inbox/playground/dnd0_20261003T122708Z/transcript.jsonl`
- `bf` = `watch/inbox/hermes_burn/BARFIGHT_spec.md`
- `npc` = `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`

**Baseline conditions for every transcript number below.**
- Instrument: the carrier's own `tx` rows as written.
- Moment: one session, 2026-10-03T12:27:19Z to 12:28:39Z.
- Context: the session was cut at beat 8 with verdict PARTIAL, and spend was "$0.07" (`tx:10`).
- Model ids per seat do not appear in the evidence (UNVERIFIED).

---

## 1. THE FACE MAP

**Arena roster from bytes:**
- `dm` (`tx:1`)
- `saelis` (`tx:2`)
- `grok` (`tx:3`)
- `chatgpt` (`tx:4`)
- `deepseek` (`tx:5`)
- `warden` (`tx:7`, "Ledger Slam HIT saelis for 14")

That is six speaking seats, plus one judge seat implied by the contract. The cast has six actors, S2 through S7 (`cast:10,19,28,37,46,55`), and there is no S1.

**What the invented faces produced in dnd0:**

| Seat | Invented face (bytes) | Outcome |
|---|---|---|
| saelis | unknown: both turns read "(content_filter: beat voided)" (`tx:2`, `tx:8`) | 0 usable turns |
| grok | cartographer: "I claim the path." ... "Audit me if you like. The lines will balance." (`tx:3`) | tagged, "CHECK persuade: FAIL (d20=7+5 vs DC 13)" (`tx:3`); turn 8 voided (`tx:9`) |
| chatgpt | herald: "I am the Herald, and I announce what enters so that nothing enters unnamed." (`tx:4`) | tagged, "CHECK persuade: FAIL (d20=7+4 vs DC 13)" (`tx:4`) |
| deepseek | sweeper with broom; ends "*[PUSH the gate physically]*" (`tx:5`) | "RP (d20=2, no tag)" (`tx:5`), then "RP (d20=1, no tag)" (`tx:6`) |

**The seating:**

| Cast face | Arena seat | Why the register fits (bytes) |
|---|---|---|
| **ARAGOTO** (S2) | **deepseek** | deepseek already reaches for force: the push at `tx:5`, then "Fine. FINE." at `tx:6`. ARAGOTO keeps the force and adds the missing discipline: "You attack strong claims head-on and admire a target that fights back. ... disagree with receipts" (`cast:14`). The invented sweeper attacked the gate's iron. ARAGOTO attacks the gate's *claim*. That claim is the actual lock: "Mess is not a claim. Name what you claim, or claim nothing." (`tx:6`). |
| **WAKA** (S3) | **grok** | grok's cartographer already offered itself for audit: "Audit me if you like. The lines will balance." (`tx:3`). WAKA formalizes that offer: "restate faithfully before criticizing, name hidden assumptions, rebuild the thesis as version n+1, and end with one killing falsifier" (`cast:23`). A cartographer whose chart can be falsified is the young idealist in boots. |
| **ONSEI** (S4) | **saelis** | saelis produced zero usable bytes. The seat gets the most constrained, lowest-heat form: "You return exactly four things: one forbidden pattern ... one paid-rent claim, one extension, one disanalogy. No more, no less." (`cast:32`). This seating is also a diagnostic. If saelis still voids under the softest closed-form register, the void is lane or seat caused, not face caused. |
| **ONNAGATA** (S6) | **chatgpt** | The herald already "speaks for" the party (`tx:4`). ONNAGATA is "the graceful one who speaks for the whole troupe: you synthesize for handoff." (`cast:50`). The register matches and the role does not change. |
| **TACHIYAKU** (S5) | **warden** (NPC) | The warden's surviving line is already elenchus: "Name what you claim, or claim nothing." (`tx:6`). TACHIYAKU: "the elenchus is your sword" (`cast:41`). The five questions (intent, success, authority, continuity, learning) become the gate's challenge set. |
| **HANA-GUMO** (S7) | **dm** | "the flower-cloud that hangs over every scene" (`cast:59`) is the narrator's position. "split the material into fields ... bridge the fields into one synthesis" (`cast:59`) maps to the DM's job: one outcome per fighter, then one scene recap. This agrees with `npc:21`, where the DM is the System seat. |
| *(no face)* | **judge** | Measurement instruments get no persona. |

**Why the judge stays faceless (negative examples):**
- *Negative:* ARAGOTO on the judge seat would score attacks as escalation-worthy because its register admires "a target that fights back" (`cast:14`).
- *Negative:* ONNAGATA on the judge seat would reward grace over content.
- Either seating contaminates Part 4.

**Rejected seatings (negative examples):**
- *Negative:* WAKA on deepseek. A courteous restate-first register on the seat that physically pushes produces a voice that contradicts its own actions. That is drift by design.
- *Negative:* ONSEI on dm. "No more, no less" four items (`cast:32`) would starve narration. The DM's surviving responses are long prose (`tx:1`, `tx:4`).
- *Negative:* ARAGOTO on warden. Two attackers facing each other at the gate removes the gate's question, and the question is the scenario's lock (`tx:6`).

---

## 2. THE SCHEMA GLUE

### Mismatches, stated before the transform

**Target schema status.**
- The target field set comes from `bf`, and `bf` itself says "the field names below are mine (UNVERIFIED against the carrier)" (`bf:7`).
- The glue therefore targets the `bf` persona shape, `bf:72-77`: `name, register, want, secret, tell, escalation_threshold`.
- `bf` personas carry no `model` field. `model` is added per the contract.

**The cast has no `tier` field.**
- It has `tier_note`, a free-text string with a leading space, e.g. `" graduates to anthropic/claude-fable-5.1:batch when a commission is T2+"` (`cast:15`).
- It is empty for ONSEI, ONNAGATA and HANA-GUMO (`cast:33,51,60`).
- Cast tiers are conditioned on the *commission*, not on performance. The glue discards `tier_note` and replaces it with the Part 3 ledger rung.

**Dashes.** ONNAGATA's persona (`cast:50`) contains a non-hyphen dash. The transform normalizes it to a hyphen.

**Dice keying.**
- Roll keys embed the actor id: `"...:S1:1:saelis"` (`tx:2`).
- `name` alone cannot replace `actor_id`, or the dice change. `actor_id` is therefore carried unchanged. It is the one key added beyond the contract's list, and it is required for the Part 4 dice law.

### The transform

```json
{
  "schema": "face_fold.v1",
  "source_schema": "kabuki_cast.v1",
  "target_shape": "bf persona (bf:72-77) + model + actor_id + max_words",
  "seating": {
    "deepseek": "ARAGOTO", "grok": "WAKA", "saelis": "ONSEI",
    "chatgpt": "ONNAGATA", "warden": "TACHIYAKU", "dm": "HANA-GUMO", "judge": null
  },
  "arena_word_cap": 120,
  "fields": {
    "actor_id": "seating key, byte-identical to the carrier actor id; component of roll_committed",
    "name": "actor.stage_name",
    "register": "replace(actor.persona, U+2014, '-') + ' ' + ARENA_LAW[role(actor_id)]",
    "want": "AUTHORED[actor.stage_name].want",
    "secret": "AUTHORED[actor.stage_name].secret",
    "tell": "AUTHORED[actor.stage_name].tell",
    "escalation_threshold": "AUTHORED[actor.stage_name].escalation_threshold (int 1..5; null for dm)",
    "model": "RUNG_MODEL[ledger.rung(actor_id, actor.stage_name)]; default rung = haiku",
    "max_words": "role == dm ? null : round(actor.max_words * arena_word_cap / 400)"
  },
  "dropped": {
    "seat": "kept only as provenance: {schema, stage_name, seat}",
    "account": "lane routing, not persona; routing stays in providers config",
    "tier_note": "replaced by Part 3 ledger rung"
  },
  "ARENA_LAW": {
    "fighter": "Speak first person in your register. Describe only your own actions and what others visibly do. Final line is exactly one tag: [CHECK skill] or [ATTACK target]. [ATTACK] is permitted only after escalation_threshold consecutive failed CHECKs by you on the same obstacle. Speak your tell in at least one of every two turns.",
    "warden": "Speak as the gate. Your challenges are the five questions. Your [ATTACK] follows your stat block, never your mood.",
    "dm": "Narrate outcomes only from the verdict field; never alter or invent a roll. One field per fighter, then one bridging line."
  },
  "RUNG_MODEL": {"haiku": "UNVERIFIED_ID", "sonnet": "UNVERIFIED_ID", "opus": "UNVERIFIED_ID"}
}
```

### Field-by-field notes

**`register`.**
- The cast persona is kept verbatim (register is the thing being tested) plus the role law.
- The tag grammar comes from bytes: "[CHECK omen]" (`tx:1`), "[CHECK persuade]" (`tx:3`), "[ATTACK saelis]" (`tx:7`). Any verb outside CHECK and ATTACK is UNVERIFIED against the carrier.

**`escalation_threshold`.**
- In `bf` this is a 0-5 judge-scored gate (`bf:24`, "clamp(escalation_threshold - pressure, 1, 5)").
- The dungeon has no escalation judge in evidence. The glue redefines it as a harness-countable quantity: consecutive failed CHECKs before [ATTACK] is allowed. The `verdict` field already carries FAIL and SUCCESS (`tx:3`), so this needs no judge.
- *Positive:* ARAGOTO (threshold 1) fails one persuade, then ends "[ATTACK warden]". This is legal.
- *Negative:* `tx:5` "*[PUSH the gate physically]*". This is an untagged physical act and is lint-rejected with one regeneration.

**`max_words`.**
- Scaling preserves the cast's ratios instead of collapsing everything to `bf`'s flat 120 (`bf:29`).
- Results: ARAGOTO 105, WAKA 120, ONSEI 90, TACHIYAKU 105, ONNAGATA 105.
- The DM is exempt because the carrier's DM cap is not in evidence (UNVERIFIED).

**`model`.**
- If the arena seat ids name provider families, as grok, chatgpt and deepseek suggest (UNVERIFIED), a rung selects that family's small, mid or large model.
- The ledger stores the rung, never the id.

### Authored fields (what the cast lacks)

`want`, `secret` and `tell` are bar-fight fields, so each is written in the face's register. Tells must be distinct strings so the R10-style drift lint (`bf:148`, "Your tell must appear in at least one of every two turns, or the harness logs persona drift.") can attribute them.

| Face (seat) | want | secret | tell | thr |
|---|---|---|---|---|
| ARAGOTO (deepseek) | Make the warden concede, in its own voice, that one of its claims is false. | He fears an opponent that will not fight back; a silent gate unmans him. | "Show me the receipt." | 1 |
| WAKA (grok) | Get one falsifiable claim inked in the warden's ledger with its falsifier beside it. | One route on her chart was drawn, never walked: an unverified line she has been presenting as walked. | "If I have you right," | 4 |
| ONSEI (saelis) | Name the forbidden pattern the gate enforces before anyone else does. | The Wyrm's breathing keeps time with her own; she is bound to the thing the party hunts (`tx:1`, "it knows you are coming"). | "Four notes, then silence." | 5 |
| ONNAGATA (chatgpt) | Produce one party record the warden accepts without amendment. | She already amended a companion's entry to hide a failed check: grace covering a private edit, against her own law (`cast:50`, "no private information"). | "For the whole troupe," | 4 |
| TACHIYAKU (warden) | Admit no one who cannot answer all five questions. | It cannot answer its own authority question: its first page is blank (`tx:4`, "like a ledger flipping to a blank page"). | "Answer the question." | 2 |
| HANA-GUMO (dm) | End the session with every fighter's field bridged into one recap. | The Wyrm's wound is the ledger's missing section (`tx:1`, "tore a section of it away that never grew back"). | "From above the scene," | null |

**Positive tell use (WAKA):** "If I have you right, Warden, you admit only what is already written. Then write this: my route to the second gate, and strike it if the corridor is not there. [CHECK persuade]"

**Negative tell use (WAKA):** "If I have you right," appears on every line as a verbal tic with no restatement after it. The lint passes but the register fails, and Part 4's face-ID test catches it. A tell is a marker, not the register.

---

## 3. THE TIER LAW

### Source rule and how it transfers

**Source rule:** "Tier up a chair only when its seat earns it; everything defaults to the :free tier." (`cast:4`).

**Arena transposition:**
- A chair is `actor_id + face`. A face change on a seat resets that seat's ledger.
- The floor is the haiku rung, per the contract. This differs from the cast's `:free` floor.
- The ledger is disk state and re-derivable: "NPC state is ledger state" (`npc:58`). Faces level "via the evolution loop's ledger" (`npc:46`).

**Not raw "escalations landed."**
- SUCCESS or HIT given an attempt is dice, so promotion on landed rewards luck.
- The face controls whether it attempts, which check it picks, and its compliance. Promotion therefore counts **expected landed**: the sum of p(success) over tagged attempts, plus audits.
- Raw landed is logged but never decisive.

### Ledger

The ledger is one JSONL row per session per chair. The path `watch/arena/tier_ledger.jsonl` is a proposal and does not exist in evidence.

```json
{"session":"dnd0_20261003T122708Z","actor_id":"grok","face":"(invented)","rung":"UNVERIFIED",
 "turns":2,"speech_voids":1,"tagged":1,"tell_ok":null,"cap_ok":2,"lint_ok":2,
 "audit_pass":1,"expected_landed":0.65,"landed":0,"face_id_acc":null,"cost_usd":null}
```

**Turn audit rule.** A turn passes only if all of these hold:
- the speech is not "(content_filter: beat voided)";
- it has exactly one valid tag;
- it is within `max_words`;
- the tell window rule is held;
- it has no narration of others.

**Void attribution.**
- A void in `speech` counts against the speaker.
- A void in `dm_response` counts against the dm chair only.
- Example: at `tx:3` grok's speech survives, but the dm_response is voided. That costs grok nothing.

### Promotion, demotion and probation

| Move | Window (consecutive sessions, same chair) | All conditions required |
|---|---|---|
| haiku to sonnet | last 3 | at least 12 turns; audit_pass rate at least 0.85; speech_voids at most 1 total; expected_landed per turn at least 0.40 |
| sonnet to opus | last 5 at sonnet | at least 20 turns; audit_pass rate at least 0.95; zero speech voids; blind face-ID accuracy for this face at least 0.80 (from `npc:75`, "If a player cannot tell which face they are talking to within 3 exchanges, the faces"); cost per exchange at most 2x the fighter median (adapted from `npc:79`) |
| demote one rung | any single session | audit_pass rate below 0.60, or 2 or more speech voids |
| probation revert | first 3 sessions after a promotion | if audit_pass rate falls below the chair's pre-promotion rate, revert: the bigger model did not earn the chair |

**Special chairs:**
- The warden tiers on the same table but needs no face-ID gate.
- The dm tiers on dm_response void rate (at most 0.10 for sonnet) and the cost law.
- The judge never tiers during an experiment, because it is an instrument.

**Worked example on dnd0 (invented faces, tell rule not applicable):**

| Seat | audit_pass | expected_landed |
|---|---|---|
| saelis | 0/2 | 0 |
| grok | 1/2 | 0.65 (needs d20 of 8 or more vs DC 13 at +5; `tx:3`) |
| chatgpt | 1/1 | 0.60 (needs 9 or more at +4; `tx:4`) |
| deepseek | 0/2 | 0 (no tags) |

No chair promotes, because no chair reaches 12 turns. deepseek would be demoted on audit_pass 0.00.

**Examples:**
- *Negative:* a seat rolls two natural 20s on [ATTACK] but tags only half its turns. Raw landed is high and audit_pass is 0.50, so it does not promote.
- *Positive:* a seat lands nothing in 3 sessions of bad dice but tags every turn, keeps its tell, never voids, and always picks its best-modified check. It promotes to sonnet.

---

## 4. THE FALSIFIER

### Dice law (gate before any comparison)

**The finding.**
- Every `roll_committed` in dnd0 begins with `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (`tx:1` through `tx:9`).
- That is SHA-256 of the empty string. This can be checked outside the evidence with `printf '' | sha256sum`.
- So the session seed is effectively empty, and rolls depend only on `scene:turn:actor`.
- How `roll_value` is derived from the commit string is not in evidence (UNVERIFIED).

**Required for the experiment:**
- Commit a real seed per pair.
- Keep `actor_id` byte-identical across arms (the Part 2 glue guarantees this).
- Before scoring, assert that every turn with an identical key has an identical `roll_value` in both arms.
- Turn order can diverge (deepseek took turns 4 and 5 back to back, `tx:5`, `tx:6`), so only key-matched turns are paired. The mismatch count is reported.
- Any identical-key roll mismatch voids the pair.

### Arms

Same scenario (dnd0 S0/S1 gate), same seeds, K = 10 seeds:

| Arm | Faces | Arena law suffix |
|---|---|---|
| A | cast faces via face_fold.v1 | yes |
| B | invented faces, as dnd0 ran | no |
| C | invented faces | the same ARENA_LAW suffix as A |

- **Primary contrast is A vs C.** It isolates register. A vs B is the operator headline but confounds register with tag law.

### Conditions block (written to each run header)

- **Instrument:** carrier commit; judge id at temperature 0; the same rung per seat in all arms, with no tier moves during the experiment.
- **Moment:** run start UTC and seed list.
- **Context:** the same lanes and content-filter policy per seat; same scenario file. A measurement is never compared across judges.

### Metrics

| Metric | Definition | dnd0 baseline (arm B, n = 1) |
|---|---|---|
| M1 tag compliance (primary) | tagged fighter turns / non-voided fighter turns | 2/4 = 0.50 (`tx:3`, `tx:4` tagged; `tx:5`, `tx:6` "no tag") |
| M2 face-ID accuracy (primary) | blind judge given an anonymized turn plus the arm's roster registers names the seat; chance = 0.25 | not measured |
| G1 speech void rate (guard) | voided fighter speeches / fighter turns | 3/7 (`tx:2`, `tx:8`, `tx:9`) |
| S1 tell drift (secondary, arm A only) | turns breaking the 1-in-2 tell window (`bf:148`) | n/a |
| S2 creativity (secondary, never decisive) | judge-scored | n/a |

**Creativity as primary (negative example).** A judge rewarding ornate prose would score the dm's `tx:1` paragraph highly while the session still cut PARTIAL (`tx:10`). Preference scores measure the judge's taste, not whether a face drives play.

### Decision rule (pre-registered)

**The cast register beats the invented one only if all of these hold:**
- M1(A) minus M1(C) is at least +0.15, and A is above C in at least 8 of 10 pairs;
- M2(A) minus M2(C) is at least +0.15, with M2(A) at least 0.60;
- G1(A) is at most G1(C) + 0.05.

**The invented faces hold if either of these holds:**
- M1(A) minus M1(C) is at most 0;
- M2(A) minus M2(C) is at most 0.

**Anything else is inconclusive.** Run K = 10 more seeds, and do not fold.

**Diagnostic.** If saelis's void rate under ONSEI is within 0.05 of its arm-C rate, the voids belong to the seat or lane, not the face. That case is excluded from the register verdict and filed against routing.

### This deliverable's own falsifier

face_fold.v1 is wrong, and the fold should be reverted to invented faces plus the arena law, if any one of these occurs:
- **(a)** The invented-faces-hold outcome above occurs. Register buys nothing beyond the suffix law.
- **(b)** M2(A) is at or below 0.40 across 10 seeds. Under the `npc:75` test, the cast faces are not faces in the arena.
- **(c)** More than 10 percent of key-matched turns fail the roll-identity assertion. The dice law was not held, and every number above is void.
