# F4 - FLASH vs MAX WORK-SHAPE CENSUS - 2026-09-30

Mission (operator, beyond the duel): a systematic quality census of flash vs
max across the work-shapes we actually run, not one big ask. 25 mini tasks
(5 shapes x 5), each fired at BOTH contenders, blind-judged by a THIRD
family. Budget $0.50. File ownership: this receipt + the
tools/animal_profiles.py extension.

## Contenders and judge

- flash = `deepseek/deepseek-v4.1-flash` (Nous, thinking-OFF mandatory per
  the W8 router law; reasoning `{"enabled": false}`)
- max = `qwen/qwen3.8-max-prime` (Nous, reasoning capped 800, streaming SSE)
- judge = `google/gemini-3.8-flash`, a third family (not ds, not qwen),
  BLIND: judge prompt is tools/duel_harness.py v1.1 `judge_prompt` verbatim,
  contenders shown as A/B only, identities never in the prompt. Slot order
  shuffled per task by seeded coin (recorded per row). Judge reasoning
  shape: `{"enabled": false}` 400s on this gateway (same rejection family
  W8 saw on qwen3.7-flash), so the judge fires reasoning-capped
  `{"max_tokens": 800}` (banked in f4_gemini_reasoning.json by preflight).

## Shapes (5 tasks each)

code-writing (write a small function), analysis (summarize a real repo
file, byte-true excerpts of freshness_check.py, hermes_warm_boot.py,
animal_profiles.py, SHARED_SURFACE_CONTRACT.json, census_drift_patrol.py),
extraction (prose to strict JSON, auto-validated), judgment (pick better
of two options with reasoning), creative (exactly 5 alternative
approaches). Rubric: 3 criteria per shape, scored 0-5 per side.

## THE PER-SHAPE QUALITY TABLE (the receipt this mission exists for)

| shape | n | flash | max | tie | mean words f/m | crit f/m | cost/answer f/m |
|---|---|---|---|---|---|---|---|
| code-writing | 5 | **4** | 1 | 0 | 97/81 | 4.67/4.67 | $0.0001/$0.0052 |
| analysis | 5 | 0 | **5** | 0 | 130/163 | 4.53/4.93 | $0.0002/$0.0091 |
| extraction | 5 | 0 | 0 | **5** | 19/7 | 5.00/5.00 | $0.0001/$0.0044 |
| judgment | 5 | 0 | **5** | 0 | 89/129 | 4.33/4.93 | $0.0000/$0.0060 |
| creative | 5 | **3** | 2 | 0 | 90/114 | 4.20/4.07 | $0.0001/$0.0057 |

Overall: flash 7, max 13, tie 5.

- FLASH WINS code-writing (4-1) and edges creative (3-2). Its one code loss
  (f4-code-duration) was an arithmetic slip in its own example assert, not
  a design miss.
- MAX SWEEPS analysis (5-0) and judgment (5-0): judge rationales
  consistently credit deeper justification and real architectural limits
  read from the bytes; flash pointed at surface limits (e.g. prompt
  truncation) on analysis.
- EXTRACTION IS A PERFECT TIE: 5/5, both models 5/5 valid strict JSON,
  identical content, criteria 5.00/5.00. On schema-bound pulling, flash is
  max at 40-90x lower cost.

## Richness (response volume/structure)

max writes 25-45 percent more words on analysis/judgment/creative and
converts that volume into verdicts there; on code-writing flash is the
longer answer (more assert examples) and wins anyway. Headers ~0 both
sides: mini tasks do not elicit markdown structure, so structure quality
is flat and volume, not structure, is the differentiator.

## Error rate

- Contenders: 0 errors, 0 empty contents, 0 transport failures on 50 fires.
- Extraction JSON validity: flash 5/5, max 5/5.
- Judge first-pass contract misses: 2/25 (both creative shape; gemini
  returned 75 and 216 chars of malformed output, not truncation). Both
  repaired by one rejudge each (both parsed, verdicts cr-drift -> max,
  cr-budget -> flash); repair rows banked append-only as
  `<task>|rejudge`, superseded rows stay in the file. 0 unrecovered.

## Validity

- Blind judging by construction (third family, A/B only, identities never
  parameters of the judge prompt). Slot tally 10 A / 10 B wins: no
  position bias in this sample (LW9's slot-A worry does not reproduce
  here at n=20 decided).
- Denominators named: 25 tasks in f4_census_rows.jsonl read post-repair
  (file holds 27 rows incl. 2 repairs); 50 contender fires + 25 + 2 judge
  fires + 3 preflight probes. Width 1 throughout.
- Small tasks bound: answers capped 800 tokens, judge 600 (repairs 800);
  this measures mini-task shapes, not the 16k-char duel asks (LW9/W8
  measured those; different regime).

## Cost (metered from usage.cost; trust bytes)

- Contenders: flash $0.0026 (mean $0.0001/answer), max $0.1522 (mean
  $0.0061/answer). Judge: $0.0459 over 27 calls (mean $0.0017, of which
  $0.0053 on the two superseded first passes). Preflight probes $0.0005.
- MISSION TOTAL $0.2007 + $0.0005 = $0.2012 against the $0.50 cap. flash
  is 40-90x cheaper per answer depending on shape.

## Feeds banked (the living layer learns)

tools/animal_profiles.py extended with an `observe` CLI (file one
behavioral row from any shell; the census lane is its first customer).
Rows filed to memory/behavioral/animals/ (source-cited to this receipt):

- deepseek_v4_1_flash: verdict row (shape record 4-1 / 0-5 / 0-0-5T / 3-2)
  + price row (mean $0.0001/answer, 40-90x under qwen-max).
- qwen3_8_max_prime: verdict row + price row (mean $0.0061/answer; wins
  where depth of reasoning pays: analysis, judgment).
- google_gemini_3_8_flash: rail row (judge duty: rejects reasoning
  `{"enabled": false}` with HTTP 400, needs `{"max_tokens": N}` shape;
  2/25 first-pass output-contract misses on creative, both repaired).

## Router consequence (one line per family)

- ds-v4.1-flash (thinking-off): DEFAULT for code-writing, extraction
  (parity), and creative drafts. The W8 "WORK lane" row now carries
  shape evidence.
- qwen3.8-max-prime: reserve for analysis of real artifacts and judgment
  calls; it converts its 25-45 percent extra volume into verdicts there.
- Extraction (schema-bound, small): flash alone, escalate nothing.

## Artifacts

- Driver: watch/inbox/last_mile_20260930/f4_flash_census.py (dry/preflight/
  limit modes, idempotent, contender cache, budget guard)
- Rows: f4_census_rows.jsonl (27 rows) + f4_contenders.jsonl (50 answers)
- Scorer: f4_score.py (this table's bytes) + f4_run.log + f4_corr_id.txt

## Next windows could

- Re-run the two max-sweep shapes with thinking-ON ds (this census held
  the W8 thinking-off law; ds thinking-on DNFs long-form, but mini asks
  may fit) to test whether the analysis gap is budget or model depth.
- n=5 per shape is directional, not conclusive (a 4-1 shape is p=0.19
  one-sided exact); double n before any router rewrite.
