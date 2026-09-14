# PRELOAD SELECTOR FW5 — RECEIPT (2026-09-07)

Fold build order #1 (watch/WORLDLINE_SEED_20260907.md §6): the trajectory-conditioned
preload selector A/B probe. Falsifier F-W5: conditioned preload vs shuffled-order
preload, same dead session — relative delta <3% = the selector is decorative, kill it.

## Instrument (short)

`mag/preload_selector.py` — three organs:

1. **ORDERER** — loads trajectory evidence (watch/TESUJI_MAP.jsonl 319 rows +
   memory/runs/trajectory/steps.jsonl W0 tape = 324 candidate blocks), scores each:
   `score = 0.5*recency + 0.2*heat + 0.3*success` (recency = ts position in [0,1];
   heat = within-source normalized probe tokens, or duration for tape rows; success =
   tesuji SUPPORTED / exit 0). Deterministic, total order via (-score, ts, id) tiebreak.
2. **SHUFFLER** — `random.Random(seed=20260907)` over the SAME block set: the control
   differs in ORDER ONLY. Determinism PASS (selftest: orderer stable, shuffle stable,
   shuffle differs, same multiset, probe-subset invariant).
3. **PROBE** — fixed continuation prompt (system = 10 top-scored real blocks, ~1K
   tokens, well under the 2K budget; user = fixed "single most important next action"
   ask), run TWICE through HOST ollama 127.0.0.1:11434 v0.32.7, native /api/chat,
   non-streaming, greedy (temperature 0, num_predict 48), `logprobs:true,
   top_logprobs:10` — wire shapes exactly per watch/inbox/OLLAMA_LOGPROBS_PROBE_20260907.md.
   Specimen: qwen2.5:3b-instruct (byte-identical target; gemma:2b fallback coded).

Metrics on shared continuation tokens (positions where both runs' selected tokens
match; position-wise alignment, conservative): mean |Δ logprob|, its relative delta
vs mean |logprob| (the F-W5 metric), top-1 churn rate, perplexity delta. Verdict
thresholds: <3% DECORATIVE / 3–10% MEASURED_EFFECT / >10% LARGE_EFFECT.

## Probe results (2 runs, $0, host ollama, no docker touched)

| run | mean\|Δlp\| | rel_delta | churn | ppl cond/shuf | ppl Δ | verdict |
|---|---|---|---|---|---|---|
| 1 | 0.1484 | **112.74%** | 0.750 | 2.193 / 2.033 | 7.31% | **LARGE_EFFECT** |
| 2 | 0.1431 | **222.10%** | 0.833 | (row 2) | 10.29% | **LARGE_EFFECT** |

The generations diverge qualitatively, not just numerically: conditioned order
(leading with the freshest sealed steps + A4-needle heat cells) yields "validate and
integrate the steering organ's output from Hermes"; shuffled order yields "verify and
document the successful completion of the A4-needle tasks." Same blocks, different
order → different continuation.

## F-W5 VERDICT (tri-state, on the instrument's question)

- **"Preload order moves the field at all" — SUPPORTED (PROXY).** Both runs land
  >10% relative delta; the <3% kill condition is NOT met. On this specimen the
  selector is NOT decorative — it is a large lever. "The selector is decorative"
  stands **DISPUTED** by this instrument.
- **"This predicts production 5.3-flash resurrection fidelity" — UNPROVEN.** This is
  a **PROXY instrument**: a 2–3B local model measuring ordering sensitivity, not the
  GLM-5.3-flash Max session. The F-W5 falsifier here answers the instrument's
  question only (does order move the field AT ALL); production warmed-vs-cold
  fidelity is build #2 (Astra witness #3 replay), explicitly not claimed here.

## Honest instrument limits (all named, none hidden)

1. **Observer effect unstable** (ollama #18163): run 1's logprobs-free guard run
   produced DIFFERENT text than its logprobs run; run 2's matched. Requesting
   logprobs perturbs greedy generation on this specimen, unreliably. The A/B is
   symmetric (both arms request logprobs identically), so this adds noise, not bias,
   to the delta — but absolute logprob values carry the caveat.
2. **Live-tape self-reference (emergent finding):** run 2 did not reproduce run 1's
   absolute numbers because the probe is dogfooded — run 1's own sealed tape row
   entered run 2's trajectory inputs and re-ranked the top-10 (9/10 blocks shared,
   one swap: tesuji:05d33950ec0e out, tape:9551cd1e021b in). **The selector is
   live**: fresh sealed steps re-order the preload by construction. Verdict held
   across the drift. Replication pin for future runs: pass a frozen tape copy.
3. Position-wise token alignment underestimates alignment when churn realigns later
   tokens (conservative direction for the kill-condition).
4. g1-style single-seed single-specimen: one seed, one model, one prompt. Width and
   seed sweeps are open falsifier extensions, not blockers for build order #2.

## Dogfood (self-sealed)

Session fw5-preload-selector-20260907 on memory/runs/trajectory/steps.jsonl:
both probe invocations ran through `python -m mag.bash_local` — steps
9551cd1e021b7373 → 393fca2f7d940697 (chained). The build sealed its own steps, and
its sealing visibly fed back into the selector (finding 2).

## Files

- Instrument: `mag/preload_selector.py` (scoring formula in module docstring)
- Probe rows: `memory/runs/preload_selector/probe_20260907.jsonl` (2 rows, label PROXY)
- Sources read: `watch/TESUJI_MAP.jsonl`, `memory/runs/trajectory/steps.jsonl`
- Wire shapes: `watch/inbox/OLLAMA_LOGPROBS_PROBE_20260907.md` (untouched)
- Program card: `watch/WORLDLINE_SEED_20260907.md` (untouched)

Constraints held: $0 (host ollama only, no cloud), no docker changes, no config
edits, no secrets echoed, card/W0 files untouched.

---
Receipt by the zcode seat, 2026-09-07. PROXY-labeled throughout, per fleet honesty law.
