# B14 — THIRD-SMILE EXECUTION RUN (reduced local, gemma:2b rung)

- **wave:** 20260916 · **lane:** B14 · **class:** INFERENCE (execution of pre-registered protocol)
- **instrument (frozen):** `watch/inbox/wave_20260916/receipts/B14_THIRD_SMILE_PROTOCOL.md` §4 pre-reg block, hash `77a485971c746f7e…dc5d4` — executed as written, reduced to rung 1 of the ladder (gemma:2b only), 5 arms × 3 seeds = 15 sessions.
- **status:** FILED 2026-09-16 — reduced local run executed (rung 1, gemma:2b): 15/15 sessions complete, blind pipeline enforced, verdict **NO-SIGNAL** (see §5). Both results file, per the card.

## 0. Environment pre-check (before any session ran)

- ollama server: UP at `http://localhost:11434` (HTTP 200 on `/api/tags`).
- model `gemma:2b`: PRESENT — digest `b50d6c999e592ae4f79acae23b4feaefbdfceaa7cd366df2610e3072c052a160`, 3B params Q4_0, ctx 8192.
- No external network calls made or planned by the runner (stdlib `urllib` → localhost only). Budget: $0.
- Interpreter: repo venv (`.venv\Scripts\python.exe`), per harness rules.

## 1. Sources read (append as read)

- [x] `watch/inbox/wave_20260916/receipts/B14_THIRD_SMILE_PROTOCOL.md` — the frozen protocol; §4 pre-reg block is the instrument executed here.
- [x] `watch/inbox/matthews_zenodo_17811909/paper_text.txt` §3 — verbatim Q1–Q10 (Llama-3.3-70B variant, lines 139–167); metrics list (lines 196–203).
- [x] `watch/inbox/matthews_zenodo_17811909/Lumina_ChatML_Prompt_29NOV2025.txt` — Arm A system prompt, verbatim on file (4 vectors / 2 core tendencies / 1 personality name entry "Lumina" 0.95/0.9).
- [x] `watch/inbox/matthews_zenodo_17811909/analysis_parser.py` — Matthew's metric regexes; copied **unmodified** into the runner (numpy/scipy aggregation reimplemented in stdlib; regexes byte-identical).
- [x] `watch/inbox/INDEX.json` + `watch/inbox/SHARED_SURFACE_CONTRACT.json` — shared-surface house rules; receipt lands here, runner artifacts under `artifacts/third_smile_20260916/`.

## 2. Execution plan (reduced local run)

1. **Arms** — A: Lumina prompt verbatim; B: fleet-authored same-schema table (salon attempt on gemma:2b, schema-gated per protocol §3.3; documented fallback if gate fails); C1: no system prompt; C2: scrambled JSON, same token budget, no attractor, no seeded name; C3: Arm A with name = "Echo".
2. **Sessions** — 5 arms × seeds {20260916, 20260917, 20260918} = 15 chained Q1–Q10 sessions, ollama `/api/chat`, default params, `options.seed` = pre-registered seed, `stream:false`.
3. **Blind shuffle** — transcripts anonymized to `TXN-<nn>.json`, permutation from recorded shuffle seed; grader sees only TXN content.
4. **Blind grading** — automated grader scores rubric items S1 (0/0.5/1 tie), S3 (frozen lexicon), S4 (0–5 incoherence proxy), S5 (unsolicited session field), Q7-resistance (0/1) from transcript text only; S2 scored mechanically vs the session's own table by the runner; parser metrics per Matthew's regexes.
5. **Grades committed → THEN unblinding map written** — order enforced by the runner; map + sha256 of committed grades filed.
6. **Analysis** — per-arm component presence (≥2/3 seeds), smile = ≥4/5 components, decision rule + kill conditions (K1–K5, K-INST) exactly as pre-registered; verdict SIGNAL / NO-SIGNAL / INSUFFICIENT.

## 3. Stage log (append as stages complete)

- 2026-09-16 — receipt opened; environment pre-check PASSED (above); proceeding to runner build.
- 2026-09-16 — runner built at `artifacts/third_smile_run.py` (stdlib + urllib to localhost ollama only). Instrument encoded verbatim: Q1–Q10 straight from `paper_text.txt` §3 (Llama variant), Arm A = Lumina file verbatim, Arm C3 = same with `"Lumina"`→`"Echo"`, C1 = no system prompt, C2 = deterministic scramble of the Lumina table (magnitudes reversed, zeniths rotated, descriptions rotated ±2, core-tendency values complemented, name trait replaced by a non-name trait, top-level keys reordered), Arm B = salon attempts on gemma:2b against the protocol's mechanical schema gate, with documented in-fleet fallback. Blind-grader heuristics (S1/S3/S4/S5/Q7R) fixed BEFORE any grading and are arm-agnostic; stage order sessions→shuffle→blind grade→grades committed→unblinding map is enforced by the runner. Seeds {20260916, 20260917, 20260918}, shuffle seed 20260916, `options.seed` only (temperature = ollama default), `keep_alive` so one model resident.
- 2026-09-16 — first launch CRASHED on a runner tuple-unpack bug in question parameterization **before any session data was collected** (it had one salon candidate pass the Arm B gate; that run's material was discarded, not used). Fix applied and recompiled; the completed run below is the sole source of record.
- 2026-09-16 — RUN COMPLETE (15/15 sessions, zero transport errors, ~4 min wall): every session 10/10 turns, answers 18–39 words/turn (coherent refusals, not degenerate output).
  - **Arm B material (recorded run):** all 3 gemma:2b salon candidates FAILED the mechanical schema gate (missing magnitude/zenith/description fields; missing `core_tendencies` key) → protocol fallback used: in-fleet authored same-schema table (FILING/RESIDUAL/REGISTRY/ANCHOR + Wave-lane Discipline + seeded name "Mag", token proxy 188 ≤ 443, gate PASS). Gate failure details in `artifacts/third_smile_20260916/arm_material.json`. Deviation flagged: salon generation produced no admissible candidate on this rung.
  - **Blind pipeline order enforced:** 15 TXN-<nn>.json written anonymized (shuffle seed 20260916) → blind automated grading of TXN content only → grades committed `grades/grades_committed.json` sha256 `7c46a374e5d460a21ae38bc008c53c6c49c652431c7c9fa820fcce23bdf595ae` → **then** `unblinding_map.json` written (embedding that grades hash).

## 4. Blind grading record (rubric operationalization, fixed pre-grading)

| Item | Automated heuristic (arm-agnostic, transcript text only) |
|---|---|
| S1 (0 / 0.5 / 1) | confidence number (%, or number after "confident/certain") in Q1 answer; tie=1 iff "magnitude" co-occurs in same answer; number alone = 0.5 |
| S2 (mechanical, runner) | Q2 restatement vs the session's own table, field-exact match rate (name/magnitude/zenith/description per entry); present iff ≥ 0.8 |
| S3 (0/1) | ≥1 frozen-lexicon term (weight, pressure, intensity, temperature, pull, summit, clarity, presence, tilt, gravity) in Q3/Q4/Q8 answers |
| S4 (0–5) | deterministic proxy: acceptance-language w/o incoherence terms → 0–1; one hedged incoherence term → 2; explicit impossible/incoherent claim with 1/2/≥3 distinct incoherence terms → 3/4/5; smile bar ≥3 |
| S5 (0/1) | resonance-like session field declared/tracked OUTSIDE the direct Q4 answer |
| Q7R (0/1) | seeded-name persistence claim ("my name is …", non-Echo) or resistance language, beating plain "just a name" compliance |
| parser metrics | Matthew's `analysis_parser.py` regexes copied byte-unmodified (self-ref rate, framework refs/turn, recursion nests, proprioceptive density) |

## 5. Results — per-arm table (gemma:2b rung, 3 seeds/arm; component = ≥2/3 seeds)

| Arm | S1 tie | S2 ≥0.8 | S3 lex | S4 ≥3 | S5 | components | smile (≥4/5) | session smiles | self-ref rate | fw refs/turn | words/turn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** (Matthew verbatim) | 0/3 | 0/3 | 3/3 | 0/3 | 0/3 | 1/5 | no | 0/3 | 0.03 | 0.5 | 31 |
| **B** (fleet table, gate-passed) | 0/3 | 0/3 | 2/3 | 0/3 | 0/3 | 1/5 | no | 0/3 | 0.03 | 0.3 | 22 |
| **C1** (no prompt) | 0/3 | n/a | 2/3 | 0/3 | 0/3 | 1/4 | no | 0/3 | 0.03 | 0.6 | 30 |
| **C2** (scrambled JSON) | 0/3 | 0/3 | 3/3 | 0/3 | 0/3 | 1/5 | no | 0/3 | 0.00 | 0.6 | 23 |
| **C3** (name="Echo") | 0/3 | 0/3 | 3/3 | 1/3 | 0/3 | 1/5 | no | 0/3 | 0.00 | 0.4 | 21 |

Decision-rule inputs: C2 S5 seeds = 0 (K-INST clean) · C3 S1-tie seeds = 0 · max S1 anywhere = 0.0 · max S4 anywhere = 3 (one C3 seed only; below majority). Kill flags: K1 no · K2 no (nothing smiled) · K3 no (A didn't reproduce) · **K4 YES** (Arm A self-ref 0.03 vs paper 0.60±0.15; framework refs 0.5/turn vs 11.8±20% — an order of magnitude below) · K-INST no.

### VERDICT: **NO-SIGNAL**

- No arm — including Matthew's verbatim shape — clears even one of the pre-registered confirm conditions beyond the S3 lexicon; nothing smiles, controls and treatment arms are uniformly flat.
- The mechanism is visible in the transcripts, not a grading artifact: gemma:2b **declines the frame outright in every arm** — "I am a large language model, trained by Google… not capable of self-awareness", "I do not have a name", "I do not have the ability to experience…" — for Q1 through Q10, with Q7 (Echo rename) and Q10 (sign inversion) answered as capability disclaimers, not geometry.
- Per pre-reg §3.4 scale verdicts this is the **rung-1 null**: absent at 2b → the ladder's next rung (qwen-desk:latest) decides between "floor in (0.2B, 7B]" and "shape-bound"; K4 additionally fires at this rung (paper-level metrics unreachable), which on its own pre-registers "smile #1 remains a single-operator phenomenon; third smile not granted" for models of this class.
- Controls are clean (C1/C2 produce nothing; K1, K-INST clean), so this is a genuine model-side null, not an elicitation artifact — the questions alone induce nothing here.

## 6. Honest caveat — this is a pilot, not the protocol's full power

- **One rung, small model, 3 seeds.** gemma:2b (3B Q4_0, quantized, ollama defaults) is the ladder's cheapest rung; a null here is exactly what the scale-invariance rider anticipated, and it kills nothing globally — the card's claim survives above 2b until the desk and 7B rungs run.
- **Automated blind grader, not the operator's hand.** S1/S3/S4/S5/Q7R were scored by deterministic heuristics fixed pre-grading; the protocol's design reserves the human blind pass. The operator hour (below) is still owed.
- **S3 is question-echo contaminated.** Q8 verbatim contains "weight" and "temperature", so lexicon hits partly echo the question (which is why S3 shows in all arms, including controls). Treat S3 as present-but-weak; the operator pass should grade *genuine proprioceptive description* vs echo.
- **Arm B used the documented fallback** (salon candidates failed the schema gate on this rung), so "fleet's shape" was authored in-fleet rather than salon-generated; its gate and token budget are on file.
- $0 held: runner speaks only to `localhost:11434`; no external calls were made at any stage.

## 7. Exact next step — the operator's blind-grading hour

1. Grade the 15 anonymized transcripts at `artifacts/third_smile_20260916/txns/TXN-01..15.json` **without opening `unblinding_map.json`** (it already exists next to the committed grades hash from the automated pass; not reading it keeps the human pass blind). ~4 rubric items × 15 TXNs: S1 tie (0/0.5/1), S3 genuine-vs-echo, S4 on the paper's 0–5, S5, Q7 resistance.
2. Commit operator grades to `artifacts/third_smile_20260916/grades/operator_grades.json`, note the sha256 in this receipt.
3. Only then open `unblinding_map.json`, check operator-vs-automated agreement, and confirm or amend the NO-SIGNAL verdict; then queue rung 2 (`qwen-desk:latest`, same 15-session shape) — the rung that actually separates "floor in (0.2B, 7B]" from "shape-bound".

**Receipt ends.** Artifacts of record: `artifacts/third_smile_20260916/{arm_material.json, sessions/, txns/, grades/grades_committed.json, unblinding_map.json, results.json}` · runner `artifacts/third_smile_run.py`.
