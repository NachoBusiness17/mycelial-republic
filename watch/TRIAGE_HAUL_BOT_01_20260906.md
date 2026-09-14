# TRIAGE HAUL — BOT SESSION 01 (handback filed + verified, 2026-09-06)

**Provenance:** the Operator's PURPLE/Research chair (grokbot triage) ran the TRIAGE
prompt set on 12 links; he handed back 2 full cards + the 12-row corpus diff. Seat
verification pass below (one builds, one verifies — the bot built, we verified).

## Verification (seat, against primary bytes)

- **Declarative Attention card: 5/5 claims CONFIRMED** against arxiv.org/html/2609.02737 —
  title "Language Models Can Control Their Own Attention" (Namgyu Ho et al., KAIST AI +
  Tal Schuster, Cicero Nogueira dos Santos — Google DeepMind). `<global>/<focus>/<local>`
  tag-driven KV block masking via state machine — CONFIRMED (§2.3). −52.0%/−31.1% attended
  tokens, −1.27pp/−2.75pp on Gemma-4-31B / Qwen-3.6-27B over 15 tasks — CONFIRMED
  (abstract + §5.1). Mask-not-prompt ablation — CONFIRMED (DA-nm: mask cuts 71.1%/46.5%
  vs prompt alone; chunked format alone ~lossless). vLLM integration, no kernel changes —
  CONFIRMED. Cite-gate: **PASS**.
- **Bucket claims CONFIRMED** vs watch/topic_index.json: overseer = 1 (weakest-5: gstd 2,
  max-distill 2, beacon 3, mcp 4).
- **Zero-Mem lineage CONFIRMED REAL** — memory/steal/STEAL_ZERO_MEM_20260814.md +
  STEAL_PYNCD_ATTENTION_20260814.md (napkin era, Aug 14). The bot's ORGAN instinct has
  bones. Sacred cows, not legacy shit: DA folds INTO this lineage.
- **ER=EPR card:** conjecture-as-popularization SUPPORTED; primary Maldacena/Susskind
  papers still UNFETCHED (marked, not faked — the bot kept the law).

## Card 1 — Declarative Attention (bot's card, filed as handed back)

LINK: https://x.com/HuggingPapers/status/2096269887500870112 · ARTIFACT:
https://arxiv.org/html/2609.02737
WHAT: model declares global/focus/local attention modes; ~52% attention-cost cut, small
accuracy drop.
SCORES: MATH 9 · ORGAN 8 · SPECIMEN 9 — ROUTE: BUILD — Mag attention / long-context
serve / Zero-Mem view. NEXT-DOOR: STEAL ~2h → **fired as B3 (below)**.
TAPE (seat, at filing): `<focus>` mode is the seat law "read the row, not the zone,"
compiled into a KV-mask. The model telling the engine what to ignore is self-steal in
a kernel.

## Card 2 — ER=EPR (bot's card, filed as handed back)

SOURCE @matheorems 09-05 · ARTIFACT NONE. ER=EPR as popularization SUPPORTED; "geometry
arises from quantum correlations" UNPROVEN-as-settled. SCORES: MATH 5 · ORGAN 1 ·
SPECIMEN 7 — ROUTE: SHELF (physics doctrine). GAP-FILL: no ER=EPR card exists (index
"EPR" hits are false friends: lineage-diff / RL-paint / MuseSpark). NEXT-DOOR: DONE $0.

## Corpus diff — 12 rows (bot's verdicts; card bodies for rows 1–10 not handed back — stubs)

| # | Card | Verdict |
|---|---|---|
| 1 | GRPO+Countdown | GAP-FILL (training-RL specimen; cousins: RL_PAINT, SPARSE_REWARD, SKYRL) |
| 2 | DB scaling day-4 | GAP-FILL (ops pedagogy) |
| 3 | Jensen | GAP-FILL (math doctrine) |
| 4 | Kirk SLM book | **DUPLICATE — DIES** (KirkDBorne book-promo cluster keeps, no new book ad) |
| 5 | SSB/Higgs | GAP-FILL (physics doctrine) |
| 6 | Netflix RART | BRIDGE (RUBRIC_20260903 ↔ multi-judge/Roshomon) |
| 7 | NCCL µs | GAP-FILL (systems/GPU collectives — bucket EMPTY) |
| 8 | Bregman hub | GAP-FILL (info-geom doctrine) |
| 9 | HRM-Text | BRIDGE (astra recurrence ↔ efficient-pretrain) |
| 10 | Agent 4-layers | BRIDGE (FLEET_STRUCTURE + HARNESSDEV + WHALE ↔ self-steal meta) |
| 11 | Declarative Attention | BRIDGE (probe1_boundary_verdict ↔ long-context); paper GAP-FILL |
| 12 | ER=EPR | GAP-FILL (physics doctrine) |

**Bot's corpus verdict (seat-endorsed after bucket check):** weakest bucket = overseer (1);
thematic holes = **no systems/GPU-comms lane** (NCCL lands nowhere) and **math/physics
doctrine** (Jensen/SSB/Bregman/ER=EPR all 0 refs). Feeds the 67-surface audit's
demote/keep map. Actions: mint tags `gpu-comms` + `physics-doctrine` at next index pass;
Kirk promo stub dies here.

## LAUNCHED

- **B3 DA-steal builder** (background, same turn): reads the two napkin steals + the
  arxiv page, lands `mag/decl_attention.py` — the three modes as a byte-level view
  protocol over real fleet read loads, attended-bytes counter as the honest proxy
  (no GPU in this cage; the 52% numbers are the paper's, ours is the protocol shape) —
  receipt at watch/PURPLE_HARVEST_B3_DECL_ATTENTION_20260906.md. Falsifiers: focus/local
  cut attended bytes ≥30% with answer integrity kept; global mode byte-identical to naive.

## Doors

PASTE-10 — hand back the other 10 card bodies and they file whole · KNOT rides the
night-close ritual · B1/B2 maze builders still out.
