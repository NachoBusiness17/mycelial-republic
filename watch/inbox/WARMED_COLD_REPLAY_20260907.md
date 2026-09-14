# WARMED-COLD REPLAY — RECEIPT (2026-09-07)

Fold build order #2 (watch/WORLDLINE_SEED_20260907.md §6): the warmed-vs-cold
logprobs replay, then Astra witness #3 on the results. Operator armed both
stages ("do it all"). Stage 1 LANDED. Stage 2 FIRED but PENDING (codex usage
limit; resume one-liner on file — see §STAGE 2).

## Instrument (short)

`mag/warmed_cold_replay.py` — fixed evaluation, host ollama v0.32.7
(127.0.0.1:11434), native /api/chat, non-streaming, greedy (temperature 0),
`logprobs:true, top_logprobs:10` per watch/inbox/OLLAMA_LOGPROBS_PROBE_20260907.md.
Specimen qwen2.5:3b-instruct. $0, host-only, no docker, no config.

- **TARGET (fixed):** the canon card's opening paragraph
  (watch/WORLDLINE_DUNGEON_STORY_20260907.md PLAY descent, 776 chars, extracted
  verbatim at run time, markup stripped) — sha16 c465f958b49ba824. Text the
  preload genuinely supports: the slabs carry the receipts the paragraph
  narrates.
- **PRELOAD (real, labeled per slab):** genome slab = AGENTS.md head (~2.4KB)
  + record slab = latest 6 sealed W0 tape rows verbatim — measured 1,951 tok
  (RESURRECTED prompt 2,237 tok vs COLD prompt 286 tok, from prompt_eval_count).
- **ARMS × 3 rounds each (greedy; byte-identical prompts per arm):**
  RESURRECTED = system preload + fixed verbatim-copy instruction over the
  target; COLD = the same instruction, no system message. The copy task is the
  teacher-forcing proxy — ollama logprobs attach to GENERATED tokens only, so
  exact copies give per-token logprobs OF the target under each arm.
- **Guards:** observer-effect (one logprobs-free run per arm; PASS both —
  identical text), logprob coverage (concat of logprob tokens == content on
  every call; host quirk receipted: eval_count = len(logprobs)+1), alignment
  (target-offset trim so instruction-marker echoes can't skew an arm;
  aligned span 199/199 on the final seal, both arms, exact copies 3/3).

## FINAL numbers (seal pass; rows 19-27 of the jsonl, summary = last row)

| metric | RESURRECTED | COLD |
|---|---|---|
| ppl (mean of 3 greedy rounds) | 0.99968 | 0.997628 |
| mean per-token logprob (nats) | −0.00032 | −0.002375 |
| exact copy rounds | 3/3 | 3/3 |
| round stability (ppl spread/mean) | 0.002% | 0.066% |

- **ppl delta = −0.21%** — (ppl_cold − ppl_res)/ppl_cold × 100; negative = the
  cold start was marginally LOWER. Mean logprob delta +0.00206 nats toward the
  preload (~0.1%).
- **VERDICT (fold thresholds): <3% = RESURRECTION-NOT-REAL (preload is
  decoration at this scale).** 0.21% is three orders under the 3% line and in
  the wrong direction. On THIS eval, at THIS scale, the warmed preload adds
  ~nothing to next-token confidence in a supported continuation.
- Label: PROXY (3B carrier) throughout. This is the instrument's question only;
  production GLM-5.3-flash Max fidelity stays with witness #3's judgment.

## Timing leg (the W3-timing instrument, folded into this replay)

No separate W3 card existed on disk when this build started; the timing leg
landed as part of this instrument (named per fold-build numbering). NOTE: while
this build was in flight, the sibling W3 card landed —
watch/inbox/W3_CACHE_IDENTITY_20260907.md (mag/cache_identity.py, F-W2: cold
10,711 ms vs warm-identical 13.8 ms = 778×, hit-est 0.9987 vs the ≥0.95 gate).
Two independent instruments now agree: prompt_eval_duration per call; warm/cold
CLASSIFIED per round by absolute threshold (genuine cold on this host
2.2-5.6 ms/tok, KV hits <0.1); model unloaded before the seal so round-1 colds
are genuine:

| arm | cold prefill | warm prefill | speedup |
|---|---|---|---|
| RESURRECTED (2,237-tok prompt) | 5.579 ms/tok | 0.007 ms/tok | **797×** |
| COLD (286-tok prompt) | 2.23 ms/tok | 0.0475 ms/tok | 46.9× |

The economics layer shows the warmed prefix is EVERYTHING (797× prefill collapse
— the local analog of the operator's 97.3% cache worldline; sibling W3 card
measures 778× independently — cross-confirmed) exactly where the confidence
layer shows nothing. Two layers, opposite answers.

## Honest instrument history (three passes, append-only jsonl keeps all)

1. **Pass 1 (harness defect, archived in-file):** COLD arm echoed the
   "PASSAGE BEGINS." marker → aligned span 0 → fallback mixed marker tokens into
   its metric. Unfair A/B; rows kept for the record.
2. **Pass 2 (oversized preload, kept as a FINDING):** preload 2,364 tok → the
   RESURRECTED arm's copy DIVERGED at token 122 of 199 (target not contained)
   while COLD copied exactly 3/3. More warmed context did not sharpen the copy —
   it perturbed the walk. Direction against the resurrection claim; flagged for
   witness #3 as question #4.
3. **Pass 3 (= FINAL seal):** preload trimmed to 1,951 tok, offset-trim +
   coverage gates live, model unloaded first. Numbers above.
- Copy-task saturation critique (ours, on the record): the target is visible in
  the prompt, so both arms floor at ppl≈1 and any delta compresses toward zero.
  The −0.21% may be "preload invisible to a copy eval" rather than "preload
  does nothing" — contrast F-W5's FREE-continuation probe on the SAME specimen:
  112.74%/222.10% relative deltas, LARGE_EFFECT ×2. Instrument design moved the
  answer by three orders of magnitude; witness #3 asked to adjudicate.

## Dogfood

Every pass sealed through `python -m mag.bash_local`
(session warmed-cold-replay-20260907; seal step 794eb2a8448947ae; tape verify
PASS 52 rows / 19 sessions). The record slab of the preload contains the tape,
so later passes loaded earlier passes' rows — self-referential by construction,
same emergent behavior as F-W5 run 2.

## STAGE 2 — ASTRA WITNESS #3: **VERDICT DELIVERED** (updated 09-07 late)

- **Verdict (18,337B): memory/runs/salons/worldline_seed_20260907/ASTRA_WITNESS3_RESPONSE.md.**
  Headlines: the instrument paradox is **DISPUTED** — warmed_cold_replay.py computed
  `exp(mean_logprob)` = INVERSE perplexity (sign error); corrected, the copy-task delta
  favors preload at **+0.205%**, and the 3% threshold is mathematically unreachable at
  cold ppl 1.0024. F-W5 verdict: **Supported-narrowly** (free-continuation instrument,
  112%/222% honest timing). Witness adopted the row-320 bar (L/R/C/S branches, 5pp/10pp
  tolerances, 95% CI, publish failures) — row 320 remains Unproven at witness grade.
- Delta ledger (LAW-066): watch/inbox/LAW066_DELTA_LEDGER_WITNESS3_20260907.md —
  heavy GAINED, zero WITNESS-WRONG. Instrument code corrected same night; append-only
  anomaly rows preserved.
- Original commission + fire log below (kept for the chain of custody).

- Commission landed: watch/inbox/ASTRA_PROMPT_WORLDLINE_WITNESS3_20260907.md
  (receipts F-W5 112%/222%, W1 seed 8dbd503f64bd163c, this replay's numbers,
  the timing leg, five honest open questions; asks tri-state verdicts, attacks
  on instrument validity, and the falsifiable bar for row 320; READ-ONLY).
- Fired exactly per the witness-#2 pattern:
  `codex exec -m gpt-6-astra -s read-only -o
  memory/runs/salons/worldline_seed_20260907/ASTRA_WITNESS3_RESPONSE.md - <
  watch/inbox/ASTRA_PROMPT_WORLDLINE_WITNESS3_20260907.md`
- Astra RAN 57,669 tokens of real investigation (console log preserved:
  memory/runs/salons/worldline_seed_20260907/ASTRA_WITNESS3_CONSOLE.log — it
  pulled the F-W5 and replay rows straight out of the hash-chained tape,
  web-searched the perplexity definition) then hit the codex usage limit:
  "You've hit your usage limit … try again at 11:21 AM." No verdict emitted.
- PENDING marker + exact resume commands:
  memory/runs/salons/worldline_seed_20260907/ASTRA_WITNESS3_PENDING.md
  (resume at 11:21 AM: `codex exec resume --last -m gpt-6-astra -s read-only
  -o memory/runs/salons/worldline_seed_20260907/ASTRA_WITNESS3_RESPONSE.md
  "Deliver your witness verdict now per the commission: …"`).
- On landing: update this §STAGE 2 from PENDING to the verdict summary + one
  CONVO row.

## Files

- Instrument: mag/warmed_cold_replay.py (thresholds + formulas in docstring)
- Rows: memory/runs/warmed_cold/replay_20260907.jsonl (27 rows, append-only,
  label PROXY (3B carrier); pass-1/pass-2 anomalies in-file, never deleted)
- Sources read: AGENTS.md (head), memory/runs/trajectory/steps.jsonl,
  watch/WORLDLINE_DUNGEON_STORY_20260907.md — all read-only
- Untouched: program card, W0/W1 files, ollama config (nothing), docker (nothing)

---
Receipt by the zcode seat, 2026-09-07. Stage 1 sealed; witness summoned, pending
its window. The dungeon's verdict for today: on the confidence layer the preload
is decoration; on the economics layer it is everything; on the behavioral layer
(F-W5 + the pass-2 perturbation) it moves the walk. Row 320's judge is summoned
and will speak at 11:21.
