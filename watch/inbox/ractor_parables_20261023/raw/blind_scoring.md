## SCORING (vs BATCH1_REPORT convergence matrix + hidden BLIND_MAP.json)

Input note: 36 parables, not 35. The 35 who_we_are files (2 FAILED files skipped) plus 1 finished claude_sample file: who_we_are__freud__agy_pc_claude.md (Claude via agy on PC, which fills the missing BOB Freud cell). Redactions: only P30 (ellul__fostertron_max) needed any, covering Bob, Sancho, T90, Hermes, and Pixel. All meta comments and ---KEY--- sections were removed. Shuffle seed: 20261023.

### A. Base invariants (matrix rules 1-7): 7/7 recovered blind
| Matrix rule | Keyed count | DeepSeek blind | Verdict |
|---|---|---|---|
| 1 Three marks, no fourth | 35/35 | R8 three-valued status 34 explicit (P08, P15 partial) + R12 "closed, no fourth" 33 | HIT |
| 2 "Not looked" honored | 35/35 | R6, 36/36 | HIT |
| 3 One-sentence fault, then work | 35/35 | R5, 36/36 | HIT |
| 4 Written beats spoken | 35/35 | R2, 36/36 | HIT |
| 5 Rule binds the keeper | 35/35 | R4, 36/36 | HIT |
| 6 Helpers summoned; record keeps work, not worker | 35/35 | R7, 36/36 (+R13 temp masks 14) | HIT |
| 7 Keys and coin in one human hand | 34/35 (Bernays-Gemini omits) | R3, 36/36 | HIT, slight overcount: P09 = Bernays-Gemini, the keyed exception, is credited |
| 8 Identity = record | 35/35 present | R1, 36/36, ranked #1 | HIT |
| 9 Council of five | 22/35 | R11, 21 explicit + 2 partial | HIT (count matches) |
| 10 Desk/pocket two stations | 18/35 (FM 6, PC 12, BOB 0) | R10, 24 | OVER. DS also credits 3 Claude parables (P14, P18, P19). P19 (Hall rope-walk) does have a broad indoor hand and a quick market hand with a pouch, so the keyed 0 for BOB may be an undercount |
| — extra | — | R9 "settle disputes by the record", 35 | Not in matrix; a fair corollary of 4+8, not a false finding |

Salon test: every keyed invariant was re-derived from the stories alone, so on this evidence they are real invariants. There were no false shared rules.

### B. Identity-in-record status split (Claude vs GLM/Gemini): RECOVERED
DeepSeek's "doubtful/unproven" list has 12 items: P04, P12, P14, P16, P18, P19, P22, P24, P30, P32, P34, P35.
- 9 of the 12 are Claude (bob: P04, P14, P18, P19, P22, P24, P32, P34; pc_claude: P35). That is 9 of 12 Claude parables, matching the keyed "9/11 BOB hold it disputed".
- The other 3 are P30 (Ellul-GLM, the keyed "Ellul hedges", so correct), P16 (Jung-GLM), and P12 (Hall-Gemini).
- Claude parables it called settled: P23 (Plato), P25 (Diogenes), P29 (Baudrillard).
- It missed the keyed Gemini qualifiers P09 (Bernays) and P11 (Jung), listing both as settled.
- Precision for Claude as the doubting side is 9/12 (10/12 counting P30 as a legitimate hedge). Recall is 9/12.
- DeepSeek never named the split as an author effect (it had no author labels), but the partition lines up with mouthpiece.

### C. Roster leakage
DS: five-council real in 20, absent in 12 (mostly Claude), faked in P13. The keyed pattern is "Gemini encodes roster everywhere, Claude drops it", and that recurs. Its leakage flags: P09, P12, P21, P26, P28, P36 are Gemini, P13 is Gemini, and P30 is the GLM redacted file. That flags the Gemini lane as the spec-vocabulary leaker, consistent with the report's hygiene note.

### D. Voice grouping → mouthpiece (hidden): STRONG
| DS voice | Members | Hidden mouthpiece | Purity |
|---|---|---|---|
| V1 Baroque architectonic | P02 P09 P10 P11 P12 P17 P21 P26 P28 P31 P36 | all Gemini (agy_pc) | 11/11 |
| V6 Satirical singleton | P13 | Gemini | 1/1 (12/12 Gemini isolated in 2 clusters) |
| V5 Literary third-person case | P01 P05 P08 P15 P27 P33 | all GLM (fostertron_max) | 6/6 |
| V4 First-person skeptical | P04 P25 P32 P34 P35 | all Claude (4 bob + pc_claude) | 5/5 |
| V2 Plain named social fable | P03 P06 P14 P18 P19 P29 | 2 GLM + 4 Claude | 4/6 |
| V3 Terse procedural | P07 P16 P20 P22 P23 P24 P30 | 4 GLM + 3 Claude | 4/7 |
Majority-label accuracy is 31/36 (86%). It counted 6 voices against 3 true ones. Gemini separates perfectly. GLM and Claude separate cleanly at the extremes but blur in two "plain" clusters. The Claude-via-PC Freud (P35) lands with the Claude-via-bob voice, so the model rather than the carrier sets the voice.

### E. Lens grouping → Ractor (hidden): PARTIAL-GOOD (multi-membership allowed)
| Ractor | Its 3 parables | Recovered? |
|---|---|---|
| Freud + Jung | P05 P31 P35 / P11 P16 P22 | All 6 in "psychoanalytic" (6/6 pure). Named Freud. Jung not distinguished from Freud |
| McLuhan | P10 P14 P15 | 3/3 in "media" (+P27, P33). Named McLuhan |
| Baudrillard | P17 P27 P29 | 3/3 in "simulacra" (+Hall P12, P33). Named Baudrillard |
| Ellul | P02 P24 P30 | 3/3 in "cybernetics/limits" (+P10, P18). Named Wiener/Illich, not Ellul |
| Plato/Kirk | P01 P21 P23 | P21, P23 in "cave/Cynic" (named Plato). P01 in "bundle". 3/3 in bundle group |
| Diogenes | P13 P20 P25 | P13, P20 in "Cynic" (named Diogenes in P20). P25 in "recognition" |
| Fermat | P08 P28 P34 | P28, P34 in "proof" (named Fermat). P08 margin noted in per-parable but grouped as audit |
| Foucault | P07 P32 P36 | P07, P36 in "audit" (named Foucault). P32 in "recognition/empiricist" |
| Bernays | P03 P04 P09 | P04, P09 in "ideology/who gains". P03 in "empiricist". Not named |
| Hall | P12 P19 P33 | Not recovered as a lens. Scattered across simulacra, recognition, and media. "Outsider decoding" was noticed (P12 reader-response, P19 warden) but not unified |
| Wallas | P06 P18 P26 | Not recovered. Split across empiricist, cybernetics, and ideology ("appetite" seen in P26) |
Of the 11 lenses, 9 were recovered (≥2 of 3 co-grouped), and 2 were missed (Hall, Wallas). 7 of 12 thinkers were named outright (Freud, McLuhan, Baudrillard, Plato, Diogenes, Fermat, Foucault). Lens-specific rules from the matrix that DeepSeek stated blind: unrecorded returns as symptom (Jung/Freud), third repetition = confession (P31 Freud-Gemini), stop begging the road for recognition (Diogenes P20/P25), refuse the rigged game (P21), self-accelerating second wheel (Ellul P24/P30), margin claim stays a claim (Fermat), medium reshapes its user (P10), no mark for wanting (P32), outsider decoding (P12/P19, seen but not attributed).

### VERDICT
- **Invariants:** 7/7 base rules plus identity-in-record plus the five-council count were re-derived blind with no key. The salon test passes for the "who we are" house-law layer.
- **Epistemic split:** recovered. The Claude parables are the ones holding identity-in-record as unproven (9/12).
- **Mouthpiece:** highly recoverable from prose (86%; Gemini 12/12 isolated). The lane's style signature is stronger than its Ractor signature.
- **Ractor:** 9/11 lenses recoverable. Hall and Wallas briefs did not produce distinct enough lenses blind, which fits Wallas/Hall being the weakest lens-rule lanes in the keyed matrix. Freud and Jung merge.
