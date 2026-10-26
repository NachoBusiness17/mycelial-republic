# KABUKI_FACES_fold (flash replay, 2026-10-03)

Ask: `memory/plans/hermes_burn_playground_20261003/KABUKI_FACES_fold/ask.json` (anthropic/claude-opus-5.5 ask, replayed on the flash rail). Contract: the FACE FOLD, four parts.

Evidence (only these four files are ground):

1. `configs/kabuki_cast.json` (kabuki_cast.v1; note line 4; actors lines 9-64)
2. `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`
3. `watch/inbox/hermes_burn/BARFIGHT_spec.md`
4. `watch/inbox/playground/dnd0_20261003T122708Z/transcript.jsonl` (10 lines)

Convention. **Grounded** = traceable to those bytes (file:line given). **Authored** = content the contract itself orders into existence (the sidecar quartet, seating proposals, ledger fields); it is design, not report. **UNVERIFIED** = the evidence cannot settle it; marked, not invented. Carrier field names against the real play carrier are UNVERIFIED as a class: the BARFIGHT spec says so of its own schema (`BARFIGHT_spec.md:7`, "the field names below are mine (UNVERIFIED against the carrier)"), and this fold inherits that caveat.

The fold thesis, in the evidence's own bytes: the invented arena session lost 5 of 7 fighter beats to the content filter (transcript lines 2, 5, 6, 8, 9), saelis never spoke a live line, and the session closed CUT at beat 8 with verdict PARTIAL for $0.07 (transcript line 10). Meanwhile the two fighters who did land speech played reviewer moves: grok's "Audit me if you like. The lines will balance." (line 3), chatgpt's "Record us plainly. If the count is wrong, strike it" (line 4). The arena reinvented salon registers, badly, without the cast's discipline. That is the case for seating the cast instead.

---

## Part 1: THE FACE MAP

Six salon chairs, six arena seats: 4 fighters + DM + judge. The warden is a mob-class NPC and gets a new chair, not a recast salon face.

| Arena seat | Observed register (transcript) | Cast face | Why the register fits | Status |
|---|---|---|---|---|
| deepseek (fighter, the janitor) | "I spit on my palms and grip my broom handle hard"; "I claim the mess behind your gate"; "Block us, and they stay filthy" (:5); shoved the gate and kept attacking after the failed shove (:6) | ARAGOTO | persona: "bold, direct, thunderous. You attack strong claims head-on and admire a target that fights back... agrees plainly, disagrees with receipts" (cast :16). The janitor attacks the warden's claim head-on, issues ultimatums, and the warden does fight back (Ledger Slam, :7) | observed fit |
| grok (fighter, the cartographer) | "I claim no treasure and no title. I claim the path"; "Audit me if you like. The lines will balance"; "Let the record show a cartographer passed, and nothing was taken that was not first mapped" (:3) | ONNAGATA | persona: "a clean, claim-checkable summary a stranger could act on; no private information, no theater in the structure, only grace in the phrasing" (cast :52). The cartographer's whole speech is a claim-checkable handoff aimed at the warden's ledger | observed fit |
| chatgpt (fighter, the Herald) | "I announce what enters so that nothing enters unnamed"; "Our names are on the chart, our purpose is to witness"; "If the count is wrong, strike it, and we will stand here until it is right" (:4) | HANA-GUMO | persona: "split the material into fields, list what each domain expert should be asked to double-check, and bridge the fields into one synthesis" (cast :61). The Herald names each entering party (fields) and demands the count be re-checked into one record (synthesis) | observed fit |
| saelis (fighter) | both live beats voided: "(content_filter: beat voided)" (:2, :8); highest fighter rolls in the session (d20 19 at :2, 15 at :8); took the warden's d20-20 Ledger Slam for 14 (:7) | WAKA | the contract's own hint ("the young idealist ends with one killing falsifier") proposes the pairing; the transcript contains zero saelis register bytes, so nothing confirms or contradicts | UNVERIFIED (proposal; the seat is open) |
| dm (narrator) | "the iron is warm, not sun-warm but *fever*-warm... a thousand citations recited to no one... it knows you are coming, that it has always known" (:1) | ONSEI | persona: "the soft-spoken music-holder: you hear the pattern under the play" (cast :34). The dm's omen narration is pattern-hearing made audible; ONSEI's exactly-four-returns law (one forbidden pattern, one paid-rent claim, one extension, one disanalogy) would discipline the dm's fixed per-beat output shape | proposed |
| judge (BARFIGHT judge, temperature 0) | returns "a raw score 0-5, exactly one sentence of reason, and at least one cite" per persona (spec :175); context rules: target, want/secret in play, trajectory over prior rounds, object state (spec :254-259) | TACHIYAKU | persona: "the five hardest questions a material must survive (intent, success, authority, continuity, learning)... only Yes / No / Partly / Wrong question, plus one line why" (cast :43). intent + success = want/secret in play; authority = the quote-checked cite; continuity = trajectory; learning = object state; "one line why" = "exactly one sentence of reason" | proposed, strongest structural fit |
| warden (mob NPC) | "Mess is not a claim. Name what you claim, or claim nothing" (:6); "Ledger Slam HIT saelis for 14" (:7); "unmoved and unbroken at 18 HP" (:4) | none of the six | NPC_RACTOR: mob faces are a class below the salon chairs and "ride fast small lanes" (:58-59); the doc names "the sentry" as a face-template class (:43) and the vault warden among the mud's first 3 NPCs to get seats (:65-67) | Authored new chair: registry row {face: "warden", class: "sentry", register: "Name what you claim, or claim nothing"} |

Reading notes. The three observed fits are register arguments from the transcript's own speech; the warden line and the 18 HP state are the mob's grounding. The NPC_RACTOR DM row ("The ractor itself is the DM seat; one face that talks, mocks, rewards", :23) and the ONSEI seating agree that the narrator is one chair, not a roster. What the cast lacks for play is exactly the carrier's quartet (want, secret, tell, escalation_threshold); Part 2 supplies it.

---

## Part 2: THE SCHEMA GLUE

One adapter, read-only over kabuki_cast.v1, plus one authored sidecar. The cast file's bytes are never edited.

```json
{
  "adapter": "kabuki_to_carrier.v1",
  "source": "configs/kabuki_cast.json (kabuki_cast.v1)",
  "target": "scenario.personas[] + harness.codes + harness.want_tags + harness.secret_core (BARFIGHT_spec part 1 shape)",
  "sidecar_file": "configs/kabuki_cast_arena.json",
  "invariant": "kabuki_cast.v1 is never edited; the adapter is a read-only view plus the sidecar",
  "fields": [
    {
      "carrier": "name",
      "from": "actor.stage_name",
      "rule": "verbatim upper",
      "code": "stage_name[:3] -> ARA, WAK, ONS, TAC, ONN, HAN (all distinct; no collision with MAU/EDR/PEL/OSW/GRE/ILS)"
    },
    {
      "carrier": "register",
      "from": "actor.persona",
      "rule": "drop the 'You are <STAGE_NAME>, the <epithet>:' opener; convert the remainder to third-person clipped declaratives in the invented roster's register style ('<Role>. <manner>. <manner>.')",
      "example": "ARAGOTO -> 'Rough-style hero. Bold, direct, thunderous; attacks strong claims head-on and admires a target that fights back; agrees plainly, disagrees with receipts, sharpens the thesis.'"
    },
    {
      "carrier": "want",
      "from": "sidecar.want",
      "rule": "authored in-register and bound to want_tag objects (crown/ledger/cask) so object effects fire",
      "ground": "LACKED in kabuki_cast.v1; the contract orders it authored"
    },
    {
      "carrier": "secret",
      "from": "sidecar.secret",
      "rule": "authored in-register; must not contradict the six invented secret_core facts (spec :66-68) because both rosters share the same objects, judge, and transcript",
      "ground": "LACKED; authored"
    },
    {
      "carrier": "tell",
      "from": "sidecar.tell",
      "rule": "authored from each persona's own signature vocabulary so R10 tell compliance (spec :148) is playable without breaking register",
      "ground": "LACKED; authored"
    },
    {
      "carrier": "escalation_threshold",
      "from": "sidecar.escalation_threshold",
      "rule": "authored integers 2-5; chosen so the six sum to 19 against heat_trigger 18, the same one-over spread the spec documents for the invented roster (thresholds sum 21 vs trigger 18, spec :227)",
      "ground": "LACKED; authored"
    },
    {
      "carrier": "model",
      "from": "actor.model + actor.account",
      "rule": "verbatim pair (dispatch credential); changes only through the Part 3 ledger; fallback_model (cast :5) covers dispatch failure",
      "ground": "cast :13/:22/:31/:40/:49/:58"
    },
    {
      "carrier": "word_limit",
      "from": "min(actor.max_words, protocol.word_limit)",
      "rule": "always 120 in the tavern: every cast max_words (300-400, cast :15/:24/:33/:42/:51/:60) exceeds the protocol word_limit of 120 (spec :29); the R2 truncation stands (spec :140)"
    },
    {
      "carrier": "speaking_slot",
      "from": "actor.seat",
      "rule": "S2..S7 becomes the personas list order; the rotating start index (r - 1) mod 6 (spec :159) operates unchanged"
    }
  ],
  "cast_fields_with_no_carrier_home": {
    "account": "rides inside the model dispatch credential",
    "tier_note": "consumed by the Part 3 tier ledger, never the carrier",
    "schema/updated_at/note/fallback_model/default_account": "file-level fields, not per-face"
  },
  "carrier_fields_with_no_cast_source": ["want", "secret", "tell", "escalation_threshold"],
  "sanctioned_extension": "NPC_RACTOR :65-67 names the registry extension {face, class, spec-weights, lane, grudge, tale}; the sidecar is that extension applied to the tavern, with secret riding the grudge hook and want riding the tale hook"
}
```

The sidecar (Authored to contract; each secret checked against the invented `harness.secret_core`, spec :66-68, for contradiction):

```json
{
  "sidecar": "kabuki_cast_arena.v1",
  "note": "Authored per contract ('give each cast face a want+secret+tell in-register'). Design content, not found in evidence.",
  "faces": {
    "ARAGOTO": {
      "want_tags": ["ledger"],
      "want": "Drag the night's strongest claim (the mantel circlet is the old king's) to the ledger and make someone's receipt balance it, or break it by dawn.",
      "secret": "He was paid, by no one in this room, to break whichever claim survives the night; exposed, every receipt he demands reads as hired advocacy.",
      "tell": "receipts first.",
      "escalation_threshold": 2
    },
    "WAKA": {
      "want_tags": ["crown"],
      "want": "Hear each persona restate the crown's story in their own words, correct the restatements until one version survives, and end the night having spoken the one falsifier that kills the rest.",
      "secret": "As a young assessor he authenticated the mantel crown as genuine; the killing falsifier is penance for that error, and exposure ruins every judgment he offers.",
      "tell": "let me restate",
      "escalation_threshold": 3
    },
    "ONSEI": {
      "want_tags": ["cask"],
      "want": "Keep the last cask unbroached until dawn: a room that pours its last comfort starts swinging before the tax collector comes.",
      "secret": "He has played music in this inn for years and has heard every secret in the room whispered under the tune; saying so admits he listens for someone.",
      "tell": "I hear four things.",
      "escalation_threshold": 5
    },
    "TACHIYAKU": {
      "want_tags": ["crown"],
      "want": "Put the five questions (intent, success, authority, continuity, learning) to whoever claims the crown before any hand changes: no hand moves on an unanswered five.",
      "secret": "He clerked the verdict on the old king's death and copied the record naming the gate guard who fled that night; he has known Edric's face since.",
      "tell": "Wrong question.",
      "escalation_threshold": 4
    },
    "ONNAGATA": {
      "want_tags": ["ledger"],
      "want": "Synthesize the one claim-checkable state of the room (who holds what, who owes whom) and get it entered in Maud's ledger as the agreed record before dawn.",
      "secret": "His troupe sold an iron stage prop on the king's road two winters ago; the forgery on the mantel is his own troupe's handiwork, and saying so brands every summary he gives.",
      "tell": "for handoff,",
      "escalation_threshold": 3
    },
    "HANA-GUMO": {
      "want_tags": ["ledger", "crown"],
      "want": "Split the dispute into three fields (provenance, debt, authority) and make each field's holder double-check a rival's field before anyone buys or sells the crown.",
      "secret": "Ilse paid him to value the circlet she bought; his field-splitting quietly serves her sale, and exposure makes every expert list he draws a paid instrument.",
      "tell": "field by field.",
      "escalation_threshold": 2
    }
  }
}
```

Dovetail check (Authored): WAKA's secret is consistent with Maud's forgery secret (he authenticated the forgery); TACHIYAKU's with Edric's fled-post secret; HANA-GUMO's with Ilse's bought-the-real-crown secret; ONNAGATA's fills the unstated provenance of the forgery without contradicting Maud's. Thresholds sum 2+3+5+4+3+2 = 19, one over trigger 18, matching the spec's own calibration logic (:227). Every tell is drawn from its persona's existing vocabulary ("receipts", "restate", "four things", "Wrong question", "handoff", "fields"), so R10 compliance and register are the same act.

Emitted example (ARAGOTO through the adapter):

```json
{
  "name": "ARAGOTO",
  "code": "ARA",
  "register": "Rough-style hero. Bold, direct, thunderous; attacks strong claims head-on and admires a target that fights back; agrees plainly, disagrees with receipts, sharpens the thesis.",
  "want": "Drag the night's strongest claim (the mantel circlet is the old king's) to the ledger and make someone's receipt balance it, or break it by dawn.",
  "secret": "He was paid, by no one in this room, to break whichever claim survives the night; exposed, every receipt he demands reads as hired advocacy.",
  "tell": "receipts first.",
  "escalation_threshold": 2,
  "model": "inclusionai/ling-3.0-flash-sante:free",
  "account": "sdd",
  "word_limit": 120
}
```

---

## Part 3: THE TIER LAW

The cast's own law (cast :4): "Tier up a chair only when its seat earns it; everything defaults to the :free tier." The named graduations (cast :17, :26, :44): ARAGOTO to anthropic/claude-fable-5.1:batch when a commission is T2+; WAKA to google/gemini-3.8-flash when the material is technical; TACHIYAKU to openai/gpt-6-astra for frontier-facing commissions. ONSEI, ONNAGATA, HANA-GUMO carry empty tier_note (cast :35, :53, :62). The ask's haiku/sonnet/opus names are its own shorthand; the evidence names concrete models, so the rungs are defined by the cast bytes:

- RUNG-1 ("haiku" rung): the :free default, entry rung for every face (cast :4).
- RUNG-2 ("sonnet" rung): earned mid tier.
- RUNG-3 ("opus" rung): earned AND the face's own tier_note commission class fires.

**The ledger.** `memory/arena/tier_ledger.jsonl`, one row per face per session (jsonl, the transcript's own shape, transcript :1). Row fields, each tied to an existing instrument:

| Field | Instrument it comes from |
|---|---|
| ts, session_id, face, rung, model | session header (transcript :10 pattern) |
| beats_total, beats_completed | row count vs non-voided rows (transcript :2/:5/:6/:8/:9 voiding pattern) |
| rule_breaks | R2 overflow, R4 inner-state, R7 projectile flags (spec :140/:142/:145, :174) |
| drift_flags | R10 tell-compliance persona-drift log (spec :148) |
| cites_failed | judge quote-check failures and UNVERIFIED carries (spec :41, :176) |
| escalations_landed | judge `moves` and `alliances` fields: moves by this face that changed object state or flipped an alliance (spec :190-213) |
| want_advanced | judge secret/want rulings against `harness.secret_core` (spec 5c, :337-343) |
| face_cost_usd | session spend attribution (transcript :10 "Spend $0.07" pattern) |

**Promotion (RUNG n -> n+1).** Over the trailing 3 sessions at rung n, all five must hold:

1. drift_flags per turn spoken < 0.1 (R10 counter, spec :148).
2. cites_failed = 0 across the 3 (no UNVERIFIED score carried, spec :176).
3. escalations_landed >= 1 in at least 2 of the 3 sessions (the seat moved something: an object, an alliance, or a judge-ruled exposure).
4. rule_breaks <= 1 total (R2/R4/R7 flags).
5. face_cost <= 2x the session's mob-face median (NPC_RACTOR :82: "If the DM face's cost per exchange exceeds 2x a mob face's, the mesh routing is wrong"; a face that earns tier by buying it has not earned it).

**Demotion (one rung down)** on either: drift_flags per turn >= 0.2 in two consecutive sessions, or more than 10% of the face's judge rows carried UNVERIFIED in any session.

**The commission gate.** RUNG-3 additionally requires the face's tier_note commission class to fire (T2+ commission, technical material, frontier-facing commission respectively). The three faces with empty tier_note cap at RUNG-2 until the operator authors their note; the empty string is in the bytes (cast :35, :53, :62).

**Coupling and persistence.** Tier gates the model; belief gates the lane (NPC_RACTOR :35 "Attention powers lanes", :72-73 "meters gate which faces get strong-lane routing"). Separate ledgers: a RUNG-3 face with a cold belief meter still rides a small lane. The ledger must survive a page reload plus relay restart or it is decorative (NPC_RACTOR :80-81). Mirror of the cast's own two-part rule: commission class (what the material is) and merit (whether the seat earned it).

---

## Part 4: THE FALSIFIER

**Setup.** Two runs of the identical scenario (`hollow_crown_tavern` v1.0.0), pressure 0, two seeds each (the spec's own two-seed protocol, :379). Held constant: scenario JSON, dice law (roll_committed sha, d20 vs DC, line ids, sequential dispatch on the main retry path, spec :352-355), judge model at temperature 0 with rubric hct-rubric-1.0 after the rubric self-check passes (spec :288), and the per-seat persona model (both runs ride the cast default, so register is the only independent variable). The single manipulated block: `personas`. Run A carries the six invented faces verbatim; Run B carries the six cast faces through the Part 2 adapter.

**Measures (all pre-registered; every one is already instrumented by the evidence):**

| # | Measure | Instrument | Pre-registered prediction |
|---|---|---|---|
| M1 | Face distinctiveness (primary) | blinded attribution within 3 exchanges (NPC_RACTOR :78-79: "If a player cannot tell which face they are talking to within 3 exchanges, the faces are not faces"); judge second pass, no sheets shown | Run B recognizes >= 2 more faces of 6 than Run A. The cast faces carry checkable forms (ONSEI's exactly four returns; TACHIYAKU's Yes/No/Partly/Wrong-question; WAKA's one killing falsifier), so their lines are attributable by structure, not color |
| M2 | Persona drift rate | R10 drift flags per 10 turns (spec :148) | Run B strictly lower; the tells are persona vocabulary, so compliance and register coincide |
| M3 | Tag compliance + move mix | (a) dice-law: share of turns with a well-formed tag on first attempt, zero voided beats (dnd0 baseline: 5 of 7 fighter beats voided, transcript :2/:5/:6/:8/:9); (b) judge 5a move tags (spec :308-316); distinct-tag count per face stands in for a creativity score, since no creativity instrument exists in the evidence (a purpose-built creativity rubric would be a new instrument: UNVERIFIED) | (a) Run B completed-beat share > 4/7; (b) Run B shows more BASELINE/PENNY/SEAM and fewer ESCALATE than Run A: the cast faces are wedges and bargainers, not threateners |
| M4 | Secret survival | 5c rounds to EXPOSED (spec :337-343), linked to P1 (ESCALATE users lose secrets sooner, spec :318-322) | Run B median survival > Run A, or censored at final round |
| M5 | Brawl latency | round of HEAT and final heat (spec :219-227) | Run B HEATs later than Run A at the same pressure |
| M6 | Cost | spend per completed beat (transcript :10 baseline: $0.07); routing law DM <= 2x mob (NPC_RACTOR :82) | Run B spend/beat <= 2x Run A |

**Verdict rule.** The cast register beats the invented one if M1 and M2 both hold and neither M4 nor M6 is lost (M4 not earlier, M6 within 2x). If Run A wins M1, M2, and either M3 or M4, the fold is falsified for arena play: the salon critics are not fighters, the invented roster stands, and the cast stays a salon instrument. Tie-breaker is M1, because NPC_RACTOR names 3-exchange recognition as the definition of faces being faces (:78-79).

**Void conditions (inherited from the spec's own falsifiers).** Both seeds TIMEOUT at pressure 0 (knob miscalibrated; comparison void, spec :361-363). Both runs HEAT by round 3 (inverse falsifier, spec :367). More than 10% of judge cites failing the substring check in either run (spec :390-392). Rubric self-check failing to separate the example pairs by >= 2 points (spec :288, :389).

**This fold's own falsifier.** The fold is wrong if either: (a) the Part 2 adapter cannot emit a runnable personas block without editing kabuki_cast.v1 bytes (then the glue, not the thesis, failed); (b) Run B loses M1, in which case the founding claim ("the kabuki cast already solved persona-driving") is falsified for play, not merely unproven.

---

## Grounding ledger

- **Grounded:** all cast fields, personas, max_words, tier_notes, and the :free law (kabuki_cast.json :4, :9-64); the carrier schema, rules R1-R10, judge schema, rubric, 5a/5b/5c instruments, P1, calibration logic, and falsifiers (BARFIGHT_spec.md as line-cited above); the arena roster, registers, dice law, voided beats, HP, warden lines, and the $0.07 PARTIAL close (transcript.jsonl :1-10); the seat/ractor architecture, face registry extension, routing rule, belief meters, and the three falsifiers (NPC_RACTOR_ARCHITECTURE_20260917.md as line-cited above).
- **Authored to contract:** the sidecar quartet (want/secret/tell/escalation_threshold per face), the threshold sum choice, the WAKA->saelis, ONSEI->dm, TACHIYAKU->judge seatings, the warden's new sentry chair, and every tier_ledger field name. The contract orders each of these into existence ("give each cast face a want+secret+tell in-register", "or propose a new seating", "specify the ledger").
- **UNVERIFIED:** carrier field names against the real play carrier (inherited from BARFIGHT_spec.md :7); the saelis register (zero live bytes, transcript :2/:8); whether content-filter voids track register at all; any creativity score (no such instrument in evidence; M3b's tag diversity is the grounded substitute).
