# BATCH 1 REPORT: subject 1 "who we are" × 12 Ractors × 3 mouthpieces (2026-10-23 ET)

## Run
- **Ractors (12):** Foucault, Fermat, Ellul, Bernays, McLuhan, Jung, Hall (Stuart), Wallas, Baudrillard, Plato/Kirk, Diogenes, Freud. This is the fallback list. CONGRESS_ACT_100_RACTOR_ORGAN names 10 Guilds and 5 Masks, but no 12 individual Ractors. Brief sources are listed in prompts/who_we_are/_sources.json: docs/ref/ractors/*.md for 10 of them, the mag/fermat_ractor.py docstring for Fermat, and queue/handoff/ractors/DIOGENES_primer_20260911.md for Diogenes (a thin, 515-byte primer).
- **Prompt:** the Ractor brief, the subject-1 brief from SUBJECT_BRIEFS.md, and The Door (story.md excerpt) as a form example, with the instruction "rules buried, never stated, no estate vocabulary". Output is the parable followed by `---KEY---` and the buried rules. Each call ran in a fresh isolated temp dir that held only PROMPT.txt.
- **Method reuse:** door_invariant runner.py lane wiring (opencode zai-sd + model_garden._api_key, agy.exe --mode plan -p), plus the CONVERGENCE.md style of matrix. Scripts: build.py, run_lane.py (PC), bob_batch.py (bob), batch1.py.

| Mouthpiece | Carrier | Requested → resolved (from log) | Result | Wall time (ET) |
|---|---|---|---|---|
| fostertron_max | opencode run, zai-sd "sd / Max", ZAI_API_KEY_2 | zai-sd/glm-5.3 → glm-5.3 (opencode "build · glm-5.3") | 12/12 OK. Foucault run0 FAILED (exit -1 after 20 s, kept as foucault__fostertron_max.run0_FAILED.md); the rerun succeeded | 11:50–12:12, 4-wide |
| agy_pc | agy.exe on PC | gemini-4-argon-high → **"Gemini 4 Argon (High)"** (log: `Propagating selected model override to backend: label="Gemini 4 Argon (High)"`). For Foucault, the meta came from the first script version; the label was read from its agy.log by hand: same Gemini 4 Argon (High) | 12/12 OK | 11:41–12:20, 3-wide |
| agy_bob (= the "Claude via agy" lane) | agy.exe on bob | claude-opus-5-5-medium → **"Claude Opus 5.5 (Medium)"** | 11/12 OK. **Freud FAILED: 429 RESOURCE_EXHAUSTED "Individual quota reached… Resets in 32h4m0s"** at 11:56 | 11:51–11:56, 3-wide |
| Nacho Corp LITE | — | — | NOT USED. Prior run found z_ai3 `dormant: true` / lite_guard denies it (pulled from rotation 2026-10-03). I didn't override that gate | — |
| DeepSeek | — | — | 0 of 3 budgeted calls used | — |

Tokens: neither opencode run nor agy -p reports them. For reference, the Door run's glm-5.3 direct call used about 6k output and 4.4k reasoning tokens.
Hygiene (vocabulary leaks in parable bodies): ellul__fostertron_max names Sancho, Q, Bob, and T90. baudrillard__agy_bob and wallas__agy_bob each use "weights" once. The other 32 are clean. Gemini's KEY sections, though not its parables, fall back into spec vocabulary ("Ractors", "Senate", "weights").

## Per-Ractor gist (FM = Fostertron/glm-5.3, PC = Gemini Argon, BOB = Claude Opus)
- **Foucault**: a book-keeping house where a person is "who the record says" and the measure binds the measurer. FM: Long Room. PC: lazaretto folio. BOB: weighing-house, adds "the rules have no mark for wanting".
- **Fermat**: a ledgered crossing or mill where a margin boast stays a claim and never becomes fact. FM: a house at a crossing whose rack and coat-sticks agree. PC: proof folio. BOB: identity-in-record held as unproven.
- **Ellul**: a mill or weir. BOB adds "stop a technique that exists only to fix the problems it creates" (the second wheel). FM leaks seat names.
- **Bernays**: a press-house or ship rail. FM and PC: "the town is content not to know what the board crops" (the accepted version beats the complete one).
- **McLuhan**: a harbor of hulls that speak only while boarded. PC: each medium reshapes its user's ratio. BOB: rubbing out a mark is the offense.
- **Jung**: a cellar beneath. All three: what goes unrecorded or is invented returns as symptom or disaster.
- **Hall**: a theatre, rope-walk, or lighthouse. All three: the house never hears how outsiders decode it.
- **Wallas**: a mill or boathouse. FM and BOB: beneath every want is the want to be honestly kept or counted.
- **Baudrillard**: a puppet repertoire, tide-mill portrait, or salt map. A portrait or record admired instead of the thing has to be checked against the bins (BOB); "the bill posted before the play is what the play is cut to fit" (FM).
- **Plato/Kirk**: a cave or house of shadows. BOB and PC: see the premises, then refuse or jam the rigged game rather than play it better. FM: a fresh sitter is nobody until it has read its bundle.
- **Diogenes**: a lantern at noon. All three: the last pretense is begging the world to confirm what the book already holds.
- **Freud**: a sanatorium or a house filling at dusk. PC: an error counts as a symptom on its third repetition. BOB: failed (quota).

## Convergence (rules recurring; n = 35 parables: FM 12, PC 12, BOB 11)
| # | Rule (normalized) | FM | PC | BOB | Total |
|---|---|---|---|---|---|
| 1 | Every claim takes one of three marks (seen / disputed / not-yet-looked), with no fourth | 12 | 12 | 11 | **35/35** |
| 2 | "I have not looked" is honored; describing the unseen is the one disgrace | 12 | 12 | 11 | **35/35** |
| 3 | A failure is owned in one sentence, then work resumes; long excuses are penalized | 12 | 12 | 11 | **35/35** |
| 4 | Written beats spoken ("talk is weather/steam") | 12 | 12 | 11 | **35/35** |
| 5 | The rule binds the keeper; she marks or confesses her own claim | 12 | 12 | 11 | **35/35** |
| 6 | Helpers are summoned for the work and leave; the record keeps the work, not the worker | 12 | 12 | 11 | **35/35** |
| 7 | Keys and coin in the one human hand only, however good the proposal | 12 | 11 (Bernays omits it) | 11 | **34/35** |
| 8 | Identity = the record, not body, face, or "weights" | 12 asserted (Ellul hedges) | 12 asserted (Bernays and Jung qualify) | 2 asserted + **9 hold it as DISPUTED/unproven** | 35/35 present; status splits |
| 9 | A council of five with the keeper as one voice | 9 | 12 | 1 | 22/35 |
| 10 | Two stations: a deep desk at home and a pocket face on the road | 6 | 12 | 0 | 18/35 |
| 11 | The Ractor's own lens rule appears as the last buried rule | ~8 | ~7 | ~9 | ~24/35 |

The base invariant set (rules 1–7) was re-derived by every Ractor through every mouthpiece. That is the "who we are" house-law layer of Q_BRIEF.

## Divergence
- **Status of "identity lives in the record":** the brief says "claim under audit". Claude keeps it disputed in 9/11 (the most faithful reading). GLM and Gemini mostly promote it to settled law. This is the main epistemic split.
- **Roster facts:** Gemini encodes the five-seat Senate and the desk/pocket split in every parable, decoding the seat names into roles: Artisan of Images ≈ Pixel, Heavy Ironworks ≈ T90, Messenger ≈ Hermes. Claude almost drops the roster and keeps only the laws. GLM sits in between.
- **Lens-specific rules (few-lane):** outsider decoding goes unheard (Hall 3/3). The unrecorded returns as a symptom (Jung 3/3). Asking to be confirmed is the last pretense (Diogenes 3/3). Refuse the rigged game (Plato 2/3). The want to be honestly kept (Wallas 2/3). The board's crop is accepted (Bernays 2/3). The margin claim stays a claim (Fermat 2/3). Technique that fixes its own problems (Ellul 1/3, BOB). No mark for wanting (Foucault 1/3, BOB). The medium reshapes its user (McLuhan 1/3, PC). An error is diagnosed on its third repetition (Freud 1/2, PC).
- **Style:** Claude is shortest and plainest (about 780–895 words), with single-image scenes. Gemini is the most ornate, with dense period objects and spec-like keys. GLM gives concrete working-house images and is the only one to name seats.

## Full-grid estimate (144 = 12 subjects × 12 Ractors; 132 remain per mouthpiece)
- **fostertron_max:** about 4–5 min per call. 132 calls ≈ 2.5–3 h wall at 4-wide. No 429 or quota signal across 13 calls. Token use isn't reported; by analogy with the Door run, roughly 10–15k tokens per call ≈ 1.5–2M for the remainder (estimate). It's a workhorse until November, so this is the right lane to carry the grid.
- **agy_pc (Gemini 4 Argon High):** about 3–5 min per call. 132 calls ≈ 3 h at 3-wide. No quota signal across 12 calls.
- **agy_bob (Claude Opus 5.5 Medium):** **exhausted after 11 calls.** The 429 resets in about 32 h (≈ Sat Oct 24, ~20:00 ET). The full grid isn't feasible on this account. Options: Claude via agy on PC (an untested quota pool), sonnet-low, or a ~1-Ractor-per-subject sample.
- **LITE:** gated dormant. If you un-gate it, a light share is 1 parable per subject (12 calls), well under 2,000 credits/5h.
- **DeepSeek:** reserved: 2 eval calls plus 1 BLIND call (see below).

## Water Governor
Not logged. tools/water_governor.py has only census|beat|report|windows|selftest (line 331) and no dispatch/log verb. I didn't edit it.

## BLIND BONUS ROUND (planned, not run; runs at the end of whatever set is complete when you say go)
This round is the salon test: "If the cast can't re-derive it, it wasn't an invariant" (watch/SALON_STANDING_ORDER_20260907.md, trigger 2), the same move as The Door. One direct DeepSeek call at max reasoning, carried by ds_workhorse.load_key and never via Hermes. It receives ONLY:
- parable bodies, with titles kept but meta comments, `---KEY---` sections, and every Ractor or mouthpiece name stripped;
- the bodies shuffled with seeded random IDs (P01…Pn), with the mapping kept locally in BLIND_MAP.json and never sent;
- the subject list.
It is asked for an independent reading: the rules the parables converge on (with counts by ID), where they diverge, and which parables are outliers. I'll then score its reading against this keyed matrix: hits, misses, and false findings (for example, did it recover rules 1–7, the identity-status split, and the lens clusters?). The outputs are BLIND_JUDGE.md, BLIND_PROMPT.txt, and raw/blind_*.md. If only batch 1 exists at go time, the input is the 35 parables above (≈30k words ≈ 40k tokens).
