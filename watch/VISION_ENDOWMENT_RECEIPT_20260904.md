# VISION ENDOWMENT RECEIPT — the skill-quantization falsifier (2026-09-04)

Spec: watch/STEAL_MCP_SKILL_QUANTIZATION_20260904.md ("the MCP server is the skill,
quantized out of the weights"). Question: does a dumb local 7B + an MCP-shaped
eye-tool (`see()`: STRUCTURE, never pixels) match native vision at a fraction of cost?

Harness: `scripts/vision_endowment.py` — raw results:
`memory/runs/vision_endowment/results_20260904T162812Z.json` (A+B+C run 1),
`results_20260904T164250Z.json` (C re-run, cap fix + drift heal).
Aborted artifacts kept for honesty: `results_20260904T163918Z.json` (C on the drifted
page — see LAW 2).

## SETUP
- Rig: emulator-5554 (AVD medium_phone), pocketfleet WebView on
  `http://10.0.2.2:8765/static/daytool.html` (digest badge + LATTICE CONSOLE).
- Dumb model: **qwen2.5:7b** (pulled this shift, 4.7 GB, ~4 min) on mag-ollama
  (127.0.0.1:11434, **100% CPU**, ~4 tok/s warm eval; cold load 61-82 s; ollama 0.32.13,
  native tool_calls work — hermes-JSON fallback also implemented, unneeded).
- Native eye proxy: `mag/vision.py` describe() = deepseek-v4-flash-vision-exp (free lane).
- Environment protocol (identical per arm): prep loads invariants lattice + RESETs walk
  to pos 0/47; ground truth re-extracted from the live AX tree at question time; t4's
  STEP ×1 tap fired by the harness at question time (all arms answer the SAME post-tap
  state). Grading is keyword/geometry against that ground truth — per-row notes in the
  results JSON.
- Task set (5): t1 digest badge state · t2 name LATTICE CONSOLE buttons · t3 coords of
  'invariants' button center (hit = inside the button's true bounds) · t4 walk position
  after one STEP ×1 tap · t5 loaded lattice kind + count.

## THE THREE ARMS' RAW ANSWERS

### A. BLIND — qwen2.5:7b, task text only (0/5, all honest refusals, zero confabulation)
| task | answer (verbatim, truncated at ~100ch) |
|---|---|
| t1 | "The day-work digest badge is not currently displayed, so its state cannot be reported." |
| t2 | "I cannot know the specific buttons in the '2 · LATTICE CONSOLE' section without seeing the…" |
| t3 | "I cannot know the exact coordinates of the button labeled 'invariants' without additional…" |
| t4 | "Cannot determine the current walk position as the app's state or position tracking details…" |
| t5 | "I cannot know the currently loaded lattice, its kind, or its entry count as no specific la…" |

### B. ENDOWED — qwen2.5:7b + ONE tool `see(target)` (3/5; chose target='ui' on ALL 5 tasks)
| task | verbatim answer | steps | wall |
|---|---|---|---|
| t1 PASS | 'The state of the day-work digest badge is "1 · DAY-WORK DIGEST live".' | 1 | 88s |
| t2 PASS | "The section titled '2 · LATTICE CONSOLE' contains the following buttons: - invariants - la…" | 1 | 107s |
| t3 PASS | "The center of the button labeled 'invariants' is at coordinates **(166, 1784)**." — exact, dist 0 | 1 | 90s |
| t4 FAIL | 'pos X/136 Y/2091' — read the tree fine, misread the QUESTION: poured the STEP button's center into the "format: pos X/Y" template while 'pos 1/47' sat in its context | 1 | 95s |
| t5 FAIL | 'The currently loaded lattice is a "DAY LANES" lattice with 3 entries.' — the AX pill text renders as 'generic entries47 entriesinvariants.json' (no delimiters); the 7B could not segment it | 1 | 90s |

### C. NATIVE — deepseek-v4-flash-vision-exp on the raw screenshot (3/5)
| task | verbatim answer | wall |
|---|---|---|
| t1 PASS | "The state of the day-work digest badge is **live**." | 2.5s |
| t2 PASS | "The section titled '2 · LATTICE CONSOLE' contains the following buttons: * **invariants…**" | 4.3s |
| t3 PASS | '(160, 1775)' run 1 / '(185, 1780)' run 2 — inside bounds, manhattan dist 15-25 from true center | 4-7s |
| t4 FAIL | 'pos 2/47' — **reproduced identically in both independent runs** (gt: pos 1/47). Small-text pixel misread, measured twice | 2-3s |
| t5 FAIL | 'Kind: invariants / Entry count: 47' — count right; "kind" answered with the lattice FILENAME, not the rendered kind ('generic entries') | 3.9s |

## SCORE TABLE

| arm | score | notable |
|---|---|---|
| A. blind 7B | **0/5** | honest failure ×5 — baseline holds (eyes-receipt pattern replicated) |
| B. endowed 7B + see() | **3/5** | t3 EXACT (166,1784) — AX law replicated: center-of-bounds beats pixel estimate |
| C. native vision | **3/5** | t3 within 15-25px (pass), t4 small-text misread ×2, t5 kind-vs-filename confusion |

**B ≥ C: TRUE at equal 3/5** — B exact where C estimated; both drop 2 (different tasks).
Tie-break detail: B never touched a premium token; C's two failures are pixel-precision
class, B's two are transducer-presentation class (fixable in the tool — see LAW 3).

## COST TABLE (per arm, 5 tasks)

| arm | model tokens | premium-lane tokens | wall | $ |
|---|---|---|---|---|
| A | 669 (554p+115e) local | 0 | 49s | 0 |
| B | 10,564 (10,338p+226e) local — prompt re-feed across tool turns, counted honestly | **0** | 470s | 0 |
| C | 4,260 valid run (+4,298 first run; +6,648 burned on the drifted-page re-run = **15,206 total lane spend**) | 15,206 | 22s | 0 (free lane) |

Cost axis: B's premium-token cost is zero vs C's ~15.2K lane tokens — the ≥10x claim
holds trivially in the premium dimension (it is infinite), but the honest trade is
WALL-CLOCK: B was 21x slower (CPU-only ollama at ~4 tok/s). On GPU substrate the
latency gap collapses; on this CPU box, B is cheap-and-slow, C is fast-and-quota'd.

## VERDICT (tri-state)
- **Skill quantization REAL on this rig: SUPPORTED.** Dumb 7B + one MCP-shaped see()
  tool matched native vision 3/5 vs 3/5, with exact coordinates where the vision giant
  estimated, at zero premium tokens. The endowment delta vs blind (0/5 → 3/5) is the
  largest measured effect.
- **As a general law: UNPROVEN.** n=5 tasks, one page, one 7B, CPU-bound latency.
  B's two failures were transducer-presentation failures (pill delimiters, question
  template) — the thesis predicts they heal in the TOOL, but that prediction is not
  yet re-measured. Follow-up: delimit pills in see() output, restate t4's format line,
  re-run B; if B → 5/5 while C stays 3/5, structure-dominance is promoted.
- Cost claim ~$0: SUPPORTED (local + free lanes; 15.2K vision-lane tokens spent total,
  recorded).

## LAWS (honest failures, each measured)
1. **TRUNCATION-BURN LAW** — deepseek vision-exp at max_tokens=600 can spend the whole
   budget invisibly and return EMPTY content (finish=length, no error field): run-1
   t2/t5 scored 'ERROR:' with eval_tok exactly 600. Harness cap now 1200. Empty-content-
   at-cap is a failure mode that still burns quota.
2. **SHARED-RIG DRIFT LAW** — the emulator is a shared surface: between runs another
   driver navigated the WebView to lanes.html; the aborted C re-run scored 0/5 against
   a garbage environment (gt all null, kept as results_20260904T163918Z.json). Every
   prep must self-heal (tap the DAY TOOL button home) and every run must drift-guard
   (raise on null ground truth) — both now in the harness.
3. **PILL-CONCATENATION LAW** — the AX channel concatenates adjacent web spans with no
   delimiters ('generic entries47 entriesinvariants.json'); a 7B cannot segment it
   (t5 FAIL). The fix belongs in the transducer (inject delimiters between spans), not
   the model — the thesis operating on its own instrument.
4. **SMALL-TEXT PIXEL LAW** — native vision misread 'pos 1/47' as 'pos 2/47'
   identically in two independent runs; the AX tree reads it exactly. Structure beats
   pixels at small text — now measured twice on this rig.
5. **TRANSDUCER-PREFERENCE OBSERVATION** — offered see('ui') AND see('image'), the 7B
   chose 'ui' on all 5 tasks. The dumb model doesn't just tolerate structure; it
   prefers it when both channels are labeled.
6. **QUESTION-TEMPLATE LAW** — B's t4 failure was question comprehension (poured button
   coords into the literal "pos X/Y" template), not sensing. Task wording is part of
   the transducer surface; dumb models read templates literally.

*Filed by the research gopher. The guild taught a 7B to see for $0 — and it chose the
tree over the eye every single time.*
