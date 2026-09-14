# PURPLE HARVEST B6 — TRANSFER-CONTRACT GATE (built + falsifiers PASS, 2026-09-06)

**Card:** watch/PURPLE_HARVEST_DIG_RHYME_20260906.md (LAUNCHED section, builder
fired same turn per LAUNCH LAW amendment 5) · **Built:** `mag/transfer_gate.py`
(stdlib only, zero LLM tokens — Zero-Mem law) · **The motivating complaint, a
stranger's, verbatim:** "some PhD in climate, Econ, finance writes a paper for x
reason from 1987. AI reads and incorporates that data into my model for no reason
because word search. **Rhyming is not mathematical.**"

## What was built

A deterministic, zero-token admission filter: a document enters a curriculum lane
only when its TRANSFER CONTRACT matches the lane's TARGET SPEC — on what the doc is
FOR (variable), where its claims were measured (regime), and how fresh they are
(as_of) — never on whether its words rhyme with the target.

- **CONTRACT schema** (per document): `claims_hold_under_assumptions` · `variable`
  (the operational concept the doc actually moves) · `regime` (where it was
  measured) · `as_of` · `source_question` (the question the doc was WRITTEN to
  answer). This is the TRIAGE card, made explicit — the dig card's "the card IS a
  transfer contract," now enforced as data.
- **TARGET SPEC as data** (attention-efficiency lane): variable synonyms
  `{attention_cost, kv_memory, inference_compute}` (hand-listed same-concept set) ·
  regimes `{long_context_inference, decode_serving, prefill_serving, kv_offload}` ·
  `as_of_floor 2024-01-01` · source_question "how to cut attention cost at
  inference time". A dict, not prose.
- **GATE**: admit iff variable ∈ synonyms AND regime ∈ regimes AND as_of ≥ floor.
  Three checks, deterministic. Vocabulary the doc shares with the target is
  REPORTED per decision but never decisive.
- **Baseline (the rhyme control)**: keyword-overlap scorer over the target's own
  16 nouns (attention, kv cache, cache, decode, inference, token, gpu, …), admit at
  threshold. Given its MOST GENEROUS operating point: threshold tuned at max F1 on
  the eval set, plus a second matrix at matched recall (tuned to the gate's
  true-recall, so the comparison isolates the rhyme damage).
- **CLI**: `python -m mag.transfer_gate eval` (matrices + every decision's
  reasoning, exit code = verdict) · `python -m mag.transfer_gate contract <path>
  [--section "Card 1"|"TRIAGE 03"|"row:pause token"]` (contract + gate verdict for
  any card; works on whole files and sub-cards of multi-card files).

Contracts are derived by hand-written ordered rules over card metadata (title +
text + date + file-level index topics): R_MECHANISM → R_PHYSICS_DOCTRINE →
R_RL_TRAINING → R_INFRA_SCHED → R_API_ECONOMICS → R_EVAL_HARNESS → R_PEDAGOGY →
R_NO_MATCH. Every field carries its derivation line; nothing appears from nowhere.

## EVAL SET — LOCKED BEFORE MEASUREMENT (build time, 2026-09-06)

The five TRUE transfers are exactly the documents the dig card named; the seven
RHYME-TRAPS are the four MEASURED false friends from TRIAGE_HAUL_BOT_01 (the ER=EPR
card + the lineage-diff / RL-paint / MuseSpark "EPR" index hits), the Kirk
infographic (named in the launch brief), and two index-defensible noun-rhymes.
Pre-lock inspection verified only that trap files carry target vocabulary — the
DEFINITION of a rhyme-trap. **No gate or baseline score was computed before this
lock.** A labeled failure would have been a valid outcome; numbers land as they land.

| Doc | Label | Why it's in the set |
|---|---|---|
| TRIAGE_HAUL_BOT_01 :: Card 1 (DA paper, arXiv:2609.02737) | TRUE | tag-driven KV masking, −52% attended tokens, cite-gate 5/5 |
| PURPLE_HARVEST_TRIAGE_02 :: TRIAGE 02 (SparDA) | TRUE | fourth projection forecasting KV blocks, long-context decode |
| PURPLE_HARVEST_B3_DECL_ATTENTION (receipt) | TRUE | the DA protocol as byte-proxy organ, falsifiers PASS |
| PURPLE_HARVEST_B4_FORECAST (receipt) | TRUE | forecast prefetch of KV blocks, 5/6 falsifiers PASS |
| PURPLE_HARVEST_01 :: pause-tokens row | TRUE | extra compute per next-token prediction, paid back by sequence |
| TRIAGE_HAUL_BOT_01 :: Card 2 (ER=EPR) | TRAP | MEASURED (dig card names it): physics doctrine, zero transfer |
| TRIAGE_02 :: TRIAGE 03 (Kirk infographic) | TRAP | says "attention" everywhere, is textbook pedagogy |
| LINEAGE_DIFF_DEEPRESEARCH | TRAP | MEASURED "EPR" hit; its "decode" is the riddler decode-gate, not LLM decode |
| INTAKE_RL_PAINT_CODE | TRAP | MEASURED "EPR" hit; its one "inference" is a VL judge |
| INTAKE_AV1DLIVE_MUSESPARK_REPROMO | TRAP | MEASURED "EPR" hit; price/model vocabulary, zero mechanism |
| CACHE_YIELD_MATH | TRAP | "cache" ×19 — API prompt-cache $/1M economics: the 1987-paper analog in our own house (same noun, different variable) |
| INTAKE_avrldotdev_gpu_scheduler | TRAP | "GPU inference" ×3 — fleet job scheduling, not attention cost |

## Confusion matrices (rows = ground truth, cols = decision)

```
GATE (transfer contract):          BASELINE @ best-F1 t=0.188 (F1=0.889):
             ADMIT  BLOCK                        ADMIT  BLOCK
  TRUE          5      0             TRUE           4      1
  RHYME-TRAP    0      7             RHYME-TRAP     0      7

BASELINE @ matched recall t=0.062 (recall == gate 1.00):
             ADMIT  BLOCK
  TRUE          5      0
  RHYME-TRAP    6      1
```

Sweep (t, admit-class F1): (0.000,0.588) (0.062,0.625) (0.125,0.615)
(0.188,0.889) (0.312,0.750) (0.625,0.571) (0.750,0.333).

## Falsifier numbers (real, from `eval` run 2026-09-06, EXIT=0)

- **F6(a) gate admits TRUE ≥ 9/10: PASS — 5/5.**
- **F6(b) gate blocks RHYME-TRAP ≥ 9/10: PASS — 7/7.**
- **F6(c) baseline concedes rhyme where the gate does not: PASS** — trap-admit
  rate at matched recall **85.7% (6/7) vs gate 0.0%**. At its best-F1 point the
  baseline happens to block all traps but pays recall: it blocks the
  pause-tokens card (a TRUE transfer). The theorem underneath, measured: **no
  keyword threshold separates the classes — min TRUE score 0.062 (pause: one
  "token" hit) < max TRAP score 0.125** (Kirk, RL-paint, cache-yield, GPU-sched).
  Every operating point concedes either a rhyme admit or a lost true transfer.
  Rhyming is not mathematical — shown, not asserted.
- **F6(d) zero LLM tokens: PASS** — AST self-audit of the module's imports:
  stdlib only (`argparse, ast, dataclasses, json, pathlib, re, sys`), no network
  modules, no model calls. Grep-able by construction.
- **F6(e) every decision printed its reasoning line: PASS — 12/12**, each with
  rule name, matched markers, all three gate checks, claims, and source question.

**Specimen worth keeping:** the baseline matched "token" on the MuseSpark promo —
from the sentence "never reads or copies those clients' OAuth tokens." That is the
1987-climate-paper disease in one line: the word is present, the concept is absent.

## Verified vs not

- **VERIFIED (this build):** gate 12/12 on the locked set; both CLI modes exercised
  on curated (Card 1, TRIAGE 03) and non-curated (INTAKE_KIRKDBORNE_SMLBOOK)
  cards; F6(a)-(e) all PASS with the numbers above; exit code 0.
- **NOT CLAIMED:** an automatic claim/assumption/question EXTRACTOR. Contracts here
  are RULE-DERIVED from card metadata via hand-written rules, with hand-curated
  claims for the six hand-read cards and honest REGEX-HARVEST tri-state fallback
  (marked "PLACEHOLDER — extractor not built" in every derivation line) for the
  rest. That extractor is the NEXT door (SciCite/Claimify lineage, per the dig
  card's third generation) — this build proves the GATE math works and builds the
  doorframe it will plug into.
- The 12-doc set is our own corpus, not the world; adversarial set scaling
  (hundreds of cards, rule coverage audit) is open work, not claimed.

## Doors

WIRE — make TRANSFER CONTRACT a required section on future TRIAGE cards (dig card,
seat-side, no builder) · NEXT-DOOR — the automatic extractor (SciCite/Claimify) ·
B6 verify on landing.

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran `python -m mag.transfer_gate eval` twice fresh: EXIT=0 both runs,
output byte-identical (determinism held), every number reproduces — gate 5/5 TRUE
admits, 7/7 trap blocks; baseline at matched recall admits 6/7 traps (85.7%) vs
gate 0%; at best-F1 it loses the pause-tokens true transfer; the theorem row
reproduces exactly: min TRUE score 0.062 < max TRAP score 0.125 — **no separating
keyword threshold exists**. Zero-token claim verified in the run's own AST audit
output. B3 regression (`decl_attention demo`) EXIT=0 — untouched as promised.
The MuseSpark specimen (keyword matched "OAuth tokens" from a credential-safety
sentence) is the whole disease in one line. VERDICT: PASS. The LeftyHikes reply
draft now carries a measured theorem: rhyming is not mathematical — shown on our
own corpus, twelve cards, no threshold survives.
