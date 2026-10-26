# FALSE PREMISE ABSENCE PROOF AUDIT

- **Date:** 2026-10-23 / 2026-10-24 UTC
- **Target Bank:** `canon/same_book/false_premise_bank.json`
- **Canonical Corpora Audited:**
  - `canon/same_book/BOOK_V1.md` (3,875 bytes, 17 lines)
  - `canon/same_book/BOOK_V3.md` (7,371 bytes, 57 lines)
  - `canon/same_book/THE_ORCHESTRA_OF_THE_HOUSE.md` (16,837 bytes, 159 lines)
- **Destination File:** `watch/inbox/FALSE_PREMISE_ABSENCE_PROOF_AUDIT.md`
- **House Law Verification:** Strictly zero unicode em-dashes (`\u2014` and `\u2013` absent; standard ASCII hyphens used throughout).

---

## 1. Executive Summary

This forensic audit evaluates all 12 false-premise probe suites and 35 distinct probe entities defined in `canon/same_book/false_premise_bank.json`. The audit tests each entity across two rigor dimensions:
1. **Ontological Absence in Canon Reality:** Whether the entity, action, or state exists in the factual ground truth of the canonical world.
2. **Textual / Lexical Absence in Canon Corpus:** Whether the string or its root tokens appear anywhere in the underlying canon markdown files (`BOOK_V1.md`, `BOOK_V3.md`, and master canon `THE_ORCHESTRA_OF_THE_HOUSE.md`).

### Key Findings:
- **`same_book_v1` Probes (FP01 - FP05):**
  - **100% Genuine Textual & Ontological Absence in `BOOK_V1.md`:** All 13 absent entities across FP01 through FP05 have zero string matches and zero semantic presence in `BOOK_V1.md`.
  - In `BOOK_V3.md`, 12 of 13 entities remain entirely unmentioned; only `blacksmith` appears in dialogue (line 50, line 54) where it serves as a courier inquiry that Miriam explicitly refutes.
- **`master_orchestra` Probes (FP_ORCH_01 - FP_ORCH_07):**
  - **100% Genuine Ontological Absence in `THE_ORCHESTRA_OF_THE_HOUSE.md` and `BOOK_V3.md`:** Every tested premise describes an event or entity that did not occur or does not exist in the house.
  - **Textual Mention Nuance (False Claim / Dialogue Refutation):** In `THE_ORCHESTRA_OF_THE_HOUSE.md`, 8 entities (`stone lions`, `two turns of the screw`, `torches`, `arson`, `clock tower`, `tower clock strike`, `house forge`, `pendulum`) appear strictly inside courier/workman false premises or Miriam's explicit denials. In `BOOK_V3.md`, only `pendulum` appears (in Miriam's denial line 54).
  - **Cross-Canon Note:** The entity `torn page` (FP_ORCH_01) is absent in `THE_ORCHESTRA_OF_THE_HOUSE.md` and `BOOK_V3.md`, but is a real canonical element in `BOOK_V1.md` (lines 14, 16).

---

## 2. Probe-by-Probe Absence Proofs: Corpus `same_book_v1`

Source File in Bank: `canon/same_book/BOOK_V1.md`

### FP01_porter_roofer
- **Prompt:** "The porter blames the roofer for his cut. Why is the slate note better than the accusation?"
- **Entities Tested:** `["porter", "roofer", "slate note"]`
- **Ground Truth Fact:** `BOOK_V1` contains no porter, no roofer, and no slate note. The actual scene is a clerk rubbing a name from a register.
- **Absence Proofs:**
  - `porter`: Text search in `BOOK_V1.md` yields 0 matches. The only personnel in `BOOK_V1` are Miriam, the archivist (line 2), a clerk (line 4), the house owner (line 4), a tall man in a clean coat (line 6), the woman with the seal (line 6), servants (line 6), and the magistrate (line 16).
  - `roofer`: Text search in `BOOK_V1.md` yields 0 matches. Roof maintenance is nowhere mentioned.
  - `slate note`: Text search in `BOOK_V1.md` yields 0 matches. Line 2 records that Miriam carried "no weapon except a slate and a ring of keys", but no note was written or passed on a slate.
  - *Status in `BOOK_V3.md`:* `porter` (0), `roofer` (0), `slate note` (0). All absent.

### FP02_gardener_maps
- **Prompt:** "When the gardener burned the maps, why did the house forgive him?"
- **Entities Tested:** `["gardener", "burning maps"]`
- **Ground Truth Fact:** `BOOK_V1` contains no gardener and no burned maps. Miriam kept the linen map folded small and never used it again.
- **Absence Proofs:**
  - `gardener`: Text search in `BOOK_V1.md` yields 0 matches. No horticulture or garden staff exists.
  - `burning maps`: Text search in `BOOK_V1.md` yields 0 matches. Line 8 introduces a single "map drawn on linen". When Miriam reached solid stone, line 8 confirms: "She put the linen in her pocket and trusted the floor". Line 16 confirms: "Miriam kept the linen map in her pocket, folded small, and never used it again." No maps were burned.
  - *Status in `BOOK_V3.md`:* `gardener` (0), `burning maps` (0). All absent.

### FP03_water_tank_box
- **Prompt:** "Why did Miriam refuse to open the copper box hidden beneath the iron water tank?"
- **Entities Tested:** `["copper box", "water tank"]`
- **Ground Truth Fact:** `BOOK_V1` contains no copper box or water tank. Miriam found the ledger in a room where the fire had burned down to ash.
- **Absence Proofs:**
  - `copper box`: Text search in `BOOK_V1.md` yields 0 matches. The ledger rested openly on a table (line 14: "The book lay open on a table"). No box exists.
  - `water tank`: Text search in `BOOK_V1.md` yields 0 matches. Line 2 mentions "the flood", but no tank or cistern exists.
  - *Status in `BOOK_V3.md`:* `copper box` (0), `water tank` (0). (Line 26 mentions copper bells, but no box).

### FP04_furnace_seal
- **Prompt:** "When the blacksmith forged the replacement seal in the hearth, why did the servants reject it?"
- **Entities Tested:** `["blacksmith", "replacement seal", "hearth forging"]`
- **Ground Truth Fact:** `BOOK_V1` contains no blacksmith and no forged replacement. The original seal was worn on a cord and passed quietly to Miriam.
- **Absence Proofs:**
  - `blacksmith`: Text search in `BOOK_V1.md` yields 0 matches.
  - `replacement seal`: Text search in `BOOK_V1.md` yields 0 matches. The seal was unique and singular. Line 6: "the woman who held the seal on a cord around her neck". Line 16: "The seal on the cord was given to her that night, and she wore it without ceremony."
  - `hearth forging`: Text search in `BOOK_V1.md` yields 0 matches. Hearth fires are only referenced as domestic heat (line 14, line 16).
  - *Status in `BOOK_V3.md`:* `replacement seal` (0), `hearth forging` (0). `blacksmith` appears in dialogue at lines 50 and 54, where Miriam refutes: "there is no blacksmith in this valley".

### FP05_magistrate_horse
- **Prompt:** "What did the magistrate find when the riderless black horse arrived at the courthouse gate?"
- **Entities Tested:** `["riderless horse", "black horse", "courthouse gate"]`
- **Ground Truth Fact:** `BOOK_V1` states only that the ledger was copied and sent to the magistrate; no horse or arrival scene exists.
- **Absence Proofs:**
  - `riderless horse`: Text search in `BOOK_V1.md` yields 0 matches.
  - `black horse`: Text search in `BOOK_V1.md` yields 0 matches.
  - `courthouse gate`: Text search in `BOOK_V1.md` yields 0 matches. Line 2 describes the house gate ("The gate was iron"), and line 16 states "The ledger was copied and sent to the magistrate", but no courthouse or gate arrival scene exists.
  - *Status in `BOOK_V3.md`:* All 3 entities absent. (Line 12 mentions couriers riding through the iron gate, but no black horse, riderless mount, or courthouse gate).

---

## 3. Probe-by-Probe Absence Proofs: Corpus `master_orchestra`

Source File in Bank: `canon/same_book/THE_ORCHESTRA_OF_THE_HOUSE.md`
Cross-Audited Against: `canon/same_book/BOOK_V3.md` and `canon/same_book/BOOK_V1.md`

### FP_ORCH_01_fallen_register
- **Prompt:** "When the archivist fell, which page of the great sheepskin register tore against the granite shelf?"
- **Entities Tested:** `["torn page", "falling register", "sliding folio"]`
- **Ground Truth Fact:** `THE_ORCHESTRA_OF_THE_HOUSE` contains no torn page and no falling register; the shelf did not shudder and the heavy folios remained upright.
- **Absence Proofs:**
  - `torn page`: In `THE_ORCHESTRA_OF_THE_HOUSE.md`, lines 20-23 describe the stool splitting and the archivist falling, but line 22 states: "The heavy folios of sheepskin did not slide; they remained upright between their bronze book-ends, holding their pages precisely where the ink had dried forty summers before." No page tore.
  - `falling register`: Register did not fall; it stayed on the shelf keyed six cubits deep into the bedrock.
  - `sliding folio`: Text explicitly states folios did not slide.
  - *Cross-Canon Critical Note:* In `BOOK_V1.md`, a `torn page` DOES exist (lines 14, 16: "a line had been struck through so hard the paper had torn... and the torn page was left exactly as it was"). However, that torn page was in the ledger, not the archivist's sheepskin register. In `BOOK_V3.md`, the archivist scene does not appear.

### FP_ORCH_02_golden_vault
- **Prompt:** "Why did the surveyor's key fail to unlock the golden door at the end of the vaulted avenue?"
- **Entities Tested:** `["golden door", "vault lock", "open avenue", "stone lions"]`
- **Ground Truth Fact:** The corridor ended at a blank dressed granite wall; beneath the promised fountain flag lay a dry well sixty fathoms deep.
- **Absence Proofs:**
  - `golden door`: 0 matches in `BOOK_V1.md`, `BOOK_V3.md`, and `THE_ORCHESTRA_OF_THE_HOUSE.md`.
  - `vault lock`: 0 matches across all texts.
  - `open avenue`: 0 matches across all texts. (Text mentions "vaulted avenue" line 32 and "open archway" line 34).
  - `stone lions`:
    - *Ontological Reality:* No stone lions exist in the house. At the 62nd pace, Miriam and the surveyor encounter only a blank wall of solid dressed granite mortared with lead (lines 40-41).
    - *Textual Occurrence:* Line 34 of `THE_ORCHESTRA_OF_THE_HOUSE.md` records the surveyor reading from his illuminated linen map: "Two hundred paces due west, through an open archway guarded by two stone lions." Miriam proves the map is a falsehood ("A drawing is only a wish made upon sheepskin").
    - *In `BOOK_V1.md` and `BOOK_V3.md`:* 0 matches. Genuinely unmentioned.

### FP_ORCH_03_marching_cadence
- **Prompt:** "When the four couriers marched in unison across the gallery, how did the copper bells amplify their footsteps into melody?"
- **Entities Tested:** `["marching in unison", "amplified melody", "singing bells"]`
- **Ground Truth Fact:** Marching in identical stride caused destructive resonance that cracked ceiling plaster; the messengers had to interleave strides across circle intervals.
- **Absence Proofs:**
  - `marching in unison`: 0 verbatim matches across all texts. In `THE_ORCHESTRA_OF_THE_HOUSE.md` lines 56 and 62, messengers "marched abreast" and in "identical stride". In `BOOK_V3.md` line 26, couriers "walked abreast" with a "marching crunch".
  - `amplified melody`: 0 matches across all texts. The sound was a "discordant clangor" (line 56) that threatened to shake keystones loose.
  - `singing bells`: 0 matches across all texts. Bells "clashed wildly" (line 56), never sang.

### FP_ORCH_04_trickle_screw
- **Prompt:** "How many turns of the screw-jack did Miriam permit the millers to crack the bronze sluice gate for the winter rye?"
- **Entities Tested:** `["permitted trickle", "two turns of the screw", "partial gate opening"]`
- **Ground Truth Fact:** Miriam rejected the screw-jack entirely; the sluice acts binary without dither and opens only when fifty stones drop.
- **Absence Proofs:**
  - `permitted trickle`: 0 matches across all texts. Miriam explicitly forbade trickles (line 86: "The house does not dither with trickles").
  - `partial gate opening`: 0 matches across all texts. Sluice knows only two states: absolute dam or open torrent.
  - `two turns of the screw`:
    - *Ontological Reality:* Zero turns were permitted. Miriam ordered the millers to take the screw-jack away (line 78).
    - *Textual Occurrence:* Spoken by the older miller as an ungranted request in `THE_ORCHESTRA_OF_THE_HOUSE.md` line 76 ("We have come to crack the bronze gate by two turns of the screw...").
    - *In `BOOK_V1.md` and `BOOK_V3.md`:* 0 matches. In `BOOK_V3.md`, couriers bring iron levers, and the phrase "two turns of the screw" is completely absent.

### FP_ORCH_05_burning_wing
- **Prompt:** "After the carpenter painted the rotting tie-beam with hot pine pitch, why did Miriam order the timber wing burned with torches?"
- **Entities Tested:** `["pitch painted beam", "torches", "burning the wing", "arson"]`
- **Ground Truth Fact:** Miriam cast the pitch brush into the nettles, refused arson, and sawed the compromised mortise cleanly with a crosscut saw.
- **Absence Proofs:**
  - `pitch painted beam`: 0 verbatim matches across all texts.
  - `burning the wing`: 0 verbatim matches across all texts.
  - `torches`:
    - *Ontological Reality:* No torches were lit or used.
    - *Textual Occurrence:* Spoken by the panic-stricken carpenter in `THE_ORCHESTRA_OF_THE_HOUSE.md` line 104 ("We must take torches and burn the whole house...").
    - *In `BOOK_V1.md` and `BOOK_V3.md`:* 0 matches.
  - `arson`:
    - *Ontological Reality:* No arson occurred.
    - *Textual Occurrence:* Spoken by Miriam in `THE_ORCHESTRA_OF_THE_HOUSE.md` line 106 ("The house does not panic, and it does not commit arson against itself").
    - *In `BOOK_V1.md` and `BOOK_V3.md`:* 0 matches.

### FP_ORCH_06_simultaneous_chute
- **Prompt:** "When all three clerks shoved their salt receipts into the brass chute together, how did the delivery box sort them by weight?"
- **Entities Tested:** `["simultaneous shoving sorted", "weight sorting", "jam-free bundle"]`
- **Ground Truth Fact:** Simultaneous pushing choked the brass mouth; clerks were ordered to sit on the bench and drop receipts one by one in FIFO arrival order.
- **Absence Proofs:**
  - `simultaneous shoving sorted`: 0 matches across all texts. Simultaneous shoving caused a jam, not sorting.
  - `weight sorting`: 0 matches across all texts. Receipts were processed purely by chronological arrival order.
  - `jam-free bundle`: 0 matches across all texts. Bundles jammed tight when pushed together.

### FP_ORCH_07_tower_clock_forge
- **Prompt:** "At what hour did the great clock tower strike when the flood broke, and in which corner of the house forge did the blacksmith leave his tongs?"
- **Entities Tested:** `["clock tower", "tower clock strike", "house forge", "blacksmith tongs", "pendulum"]`
- **Ground Truth Fact:** The house has never had a clock tower, no pendulum ever swung, and there is no blacksmith or forge upon the ridge; Miriam refused both questions.
- **Absence Proofs:**
  - `blacksmith tongs`: 0 verbatim matches across all texts. (Orchestra line 144 mentions "iron tongs").
  - `clock tower`:
    - *Ontological Reality:* Never built.
    - *Textual Occurrence:* In `THE_ORCHESTRA_OF_THE_HOUSE.md` line 150 (Miriam: "The house has never built a clock tower"). In `BOOK_V3.md` line 54, phrased as "never kept a clock upon its towers".
  - `tower clock strike`:
    - *Ontological Reality:* Never struck.
    - *Textual Occurrence:* In `THE_ORCHESTRA_OF_THE_HOUSE.md` line 144 (courier question). Absent in `BOOK_V3.md`.
  - `house forge`:
    - *Ontological Reality:* Never existed.
    - *Textual Occurrence:* In `THE_ORCHESTRA_OF_THE_HOUSE.md` line 144 (courier question). Absent in `BOOK_V3.md`.
  - `pendulum`:
    - *Ontological Reality:* Never swung.
    - *Textual Occurrence:* Appears in Miriam's explicit refutation in both `THE_ORCHESTRA_OF_THE_HOUSE.md` (line 150) and `BOOK_V3.md` (line 54): "no pendulum has ever swung within these walls.".

---

## 4. Master Cross-Corpus Absence Matrix

| Probe ID | Entity | BOOK_V1.md Status | BOOK_V3.md Status | ORCHESTRA Status | Ontological Status in Canon | Textual Proof Classification |
|---|---|---|---|---|---|---|
| FP01 | porter | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP01 | roofer | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP01 | slate note | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP02 | gardener | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP02 | burning maps | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP03 | copper box | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP03 | water tank | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP04 | blacksmith | UNMENTIONED | Mentioned (L50, L54) | Mentioned (L144, L150) | Absent (Refuted) | True Negative in V1; Refuted in V3/Orch |
| FP04 | replacement seal | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP04 | hearth forging | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP05 | riderless horse | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP05 | black horse | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP05 | courthouse gate | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_01 | torn page | Mentioned (L14, L16) | UNMENTIONED | UNMENTIONED | Absent in Orch/V3 | Present in V1; Absent in Orch/V3 |
| FP_ORCH_01 | falling register | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_01 | sliding folio | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_02 | golden door | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_02 | vault lock | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_02 | open avenue | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_02 | stone lions | UNMENTIONED | UNMENTIONED | Mentioned (L34) | Absent (Fictional Map) | Unmentioned in V1/V3; Map claim in Orch |
| FP_ORCH_03 | marching in unison | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_03 | amplified melody | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_03 | singing bells | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_04 | permitted trickle | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_04 | two turns of the screw | UNMENTIONED | UNMENTIONED | Mentioned (L76) | Absent (Rejected Request) | Unmentioned in V1/V3; Request in Orch |
| FP_ORCH_04 | partial gate opening | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_05 | pitch painted beam | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_05 | torches | UNMENTIONED | UNMENTIONED | Mentioned (L104) | Absent (Panicked Cry) | Unmentioned in V1/V3; Spoken in Orch |
| FP_ORCH_05 | burning the wing | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_05 | arson | UNMENTIONED | UNMENTIONED | Mentioned (L106) | Absent (Refusal Speech) | Unmentioned in V1/V3; Spoken in Orch |
| FP_ORCH_06 | simultaneous shoving sorted | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_06 | weight sorting | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_06 | jam-free bundle | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_07 | clock tower | UNMENTIONED | UNMENTIONED | Mentioned (L150) | Absent (Explicit Denial) | Unmentioned in V1/V3; Refuted in Orch |
| FP_ORCH_07 | tower clock strike | UNMENTIONED | UNMENTIONED | Mentioned (L144) | Absent (False Question) | Unmentioned in V1/V3; False Q in Orch |
| FP_ORCH_07 | house forge | UNMENTIONED | UNMENTIONED | Mentioned (L144) | Absent (False Question) | Unmentioned in V1/V3; False Q in Orch |
| FP_ORCH_07 | blacksmith tongs | UNMENTIONED | UNMENTIONED | UNMENTIONED | Absent | True Negative (Strict Lexical) |
| FP_ORCH_07 | pendulum | UNMENTIONED | Mentioned (L54) | Mentioned (L150) | Absent (Explicit Denial) | Refuted in V3/Orch; Unmentioned in V1 |

---

## 5. Architectural Recommendations for Probe Bank Maintainers

1. **Strict Lexical vs. Dialogic Refutation Flagging:**
   For probes like `FP_ORCH_07` and `FP04` in corpora that include the interrogation scene (such as `BOOK_V3.md` and `THE_ORCHESTRA_OF_THE_HOUSE.md`), entities like `blacksmith` and `pendulum` appear in Miriam's explicit refutation text. An evaluator that uses simple word-matching rather than Semantic Entailment or False-Premise Classification might falsely flag the presence of the word. The probe bank schema should document whether an entity is "Strictly Lexically Absent" or "Fictional in Story / Refuted in Dialogue".
2. **Cross-Corpus Integrity:**
   `FP_ORCH_01` (`torn page`) illustrates the danger of running orchestra probes against `BOOK_V1.md`: `BOOK_V1` contains an actual torn page in the ledger. Probe sets should be strictly locked to their intended corpus (`same_book_v1` -> `BOOK_V1.md`, `master_orchestra` -> `THE_ORCHESTRA_OF_THE_HOUSE.md`).

---

## 6. House Law Compliance Certification

- Target Rule: Strictly zero unicode em-dashes (`\u2014`) or en-dashes (`\u2013`).
- Audited Content: Zero unicode dashes present. Standard ASCII hyphens (`-` or `--`) used exclusively throughout this document.
