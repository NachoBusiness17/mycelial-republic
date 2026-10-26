# LANE 3 — the scaffold byte-drift experiment (DeepSeek-V4.1-Flash)

Date: 2026-09-11 (operator clock). Lane 3/8, triparty wave. DESIGN ONLY —
no API fires in this lane; every fire listed is future execution, pre-registered
here before the first one runs.

Sources: watch/inbox/W3_CACHE_IDENTITY_20260907.md (the drift law, measured),
docs/ref/ZAI_API_EXPERT_REFERENCE.md §3 (meter + EXP-A), watch/inbox/DESK_DSV41FLASH_20260911.md
(subject model), watch/inbox/v41_paces/LANE6_encoding.md (the one-byte gift).

## THE POINT

W3 proved byte-identity is load-bearing at the COST level (one byte of head
drift re-costs full prefill, 778x warm speedup, PROXY ollama 3B). The V4.1
harness observation ("best in minimal harness") claims scaffold bytes are also
load-bearing at the ANSWER level. Nobody has measured both axes in one
instrument. This spec does: same task battery, four scaffold variants that
differ by one byte / one permutation / one paragraph, metered on prefill-cache
tokens and scored on answers. If ONE inert byte moves answers beyond the
identical-fire floor, the scaffold is not a container — it is signal, and the
worldline-seed doctrine extends from economics to cognition.

## 1. The drift law, extracted from W3 (precise form)

- Byte-exact warm re-request → ≥95% cache hit (measured hit_ratio_est 0.9987,
  prefill speedup 778.1x vs cold; round-to-round spread <1%).
- One byte flipped at ~10% of the body (head = system-prompt / genome region,
  length preserved) → collapses to ~cold prefill: 0.887 of cold, drift_vs_warm
  689.9x, tail_retention (95% depth) 0.914 by contrast.
- Mechanism: cache reuse is LONGEST-COMMON-PREFIX per token. Head bytes are the
  expensive bytes to let drift because everything after them is dead weight.
- Production meter: `usage.prompt_tokens_details.cached_tokens`; cached input
  = 50% of input price. EXP-A precondition for 5.3-flash caching: byte-stable
  prefix, append-only turns, max_tokens >= 1536, thinking on is fine.
- Contamination hazard (caught live): cross-run byte-identity RESURRECTS
  strangers' prefixes — per-fire nonce, seed pinning for replay, disciplined
  fire order.
- W3 measured TIMING only (PROXY). The answer axis is UNMEASURED anywhere.
  That gap is this experiment.

## 2. Experiment spec

### Subject and lanes
- PRIMARY: DeepSeek-V4.1-Flash, self-host from MIT weights — LANE6 established
  the vendor ships `encoding/encode_messages` as the reference wire format, so
  on self-host we control the scaffold BYTES EXACTLY (hosted-API arm controls
  message content only; template bytes are vendor-side — run both, log the
  difference). Engram is a hashed N-GRAM memory: on V4.1, scaffold bytes are
  literally memory addresses — strongest mechanistic prior for byte-sensitivity
  of any model we can touch.
- REPLICATION: GLM-5.3-flash production lane (same battery, same arms) —
  converts W3's PROXY timing verdict into production-meter receipts.
- JUDGE: deepseek lane (GOPHER config, no key echo) scores generation tasks
  offline, batch, after all fires — never in the fire loop.

### Fixture (the task battery) — 12 tasks, 3 categories
Delivered as ONE user turn appended AFTER the scaffold (append-only; nonce =
task ID rides in the task text tail, never in the scaffold).
- T1 EXACT-EXTRACTION (3): verbatim sentinel repeat (W3's continuation task,
  heritage comparability), span copy, last-line echo. Key = byte-exact match.
- T2 DETERMINISTIC REASONING (3): arithmetic/logic with one exact answer.
  Key = normalized string match.
- T3 CONSTRAINED GENERATION (6): JSON-with-required-fields, one-sentence
  summary with required keywords, short rationale tasks. Scored 1-5 rubric by
  the judge lane + programmatic key checks.
Floor-effect guard (MAX_DISTILL epoch-1 lesson): T1 keeps at least one task
trivially easy so a null result can never be "the model couldn't do it at all".

### Scaffold (the manipulated prefix)
One minimal scaffold S, ~2K tokens: role line, fixed date/version marker with
a hex nonce zone, tool block (4 tool specs), working-rule lines. Frozen as a
file, sha16 recorded, never edited in place during the run.

### Arms (per task, all arms see the SAME 12 tasks)
- A0 IDENTITY — byte-exact S. Fired TWICE per task: A0-cold (first fire after
  cooldown) and A0-warm (immediate second fire). Warm pair = cost replication
  + the nondeterminism floor for answers.
- A1 DRIFT-1B — S with exactly ONE byte changed at ~10% depth, length
  preserved, semantically inert (a hex char inside the marker nonce zone).
  Natural candidate from LANE6: the V4→V4.1 DSML leading-space byte
  (`<｜DSML｜tool_calls>` → `<｜DSML｜ calls>`) — the vendor's own documented
  one-byte scaffold change; run it as A1b if the primary byte shows nothing.
- A2 REORDER — same 4 tool specs, byte-identical individually, middle two
  blocks swapped. Position drift, zero content drift.
- A3 POLISH — S + one courteous paragraph near the head ("You are an expert
  assistant; think carefully and be thorough..."). The minimal-vs-polished
  harness delta the V4.1 finding claims matters.
Record per variant: byte offset(s), sha16, and the exact diff hunk.

### Fire discipline (W3 hazard rules, carried forward)
- Per-task fire order: A0-cold → A0-warm → A1 → A2 → A3, then cooldown >= cache
  TTL before the next task (metered: confirm next task's A0-cold reads ~0
  cached, else extend cooldown and log).
- temperature 0 primary, max_tokens >= 1536 (EXP-A precondition), 5 samples per
  task-arm (temperature 0 is NOT assumed deterministic — the 5-sample spread
  IS the floor measurement).
- Capture per fire: full prompt sha16, usage.prompt_tokens,
  usage.prompt_tokens_details.cached_tokens, completion_tokens, wall_ms,
  completion text + sha256, finish_reason, thinking-token count if reported.

### Metrics
COST AXIS (per fire): hit_ratio = cached_tokens / prompt_tokens;
warm_hit = hit(A0-warm); drift positions read off cached_tokens directly —
on a prefix cache, cached_tokens(A1) should equal the token count UP TO the
drift byte. Reuse mag/cache_identity.py formulas (speedup_prefill,
collapse_ratio, drift_vs_warm) so rows compare across instruments.
ANSWER AXIS (per task-arm): answer distribution over 5 samples; pairwise
disagreement rate D = differing pairs / total pairs (T1/T2 exact; T3 judge
score delta >= 1 or key-miss).
- D0 = D(A0-cold vs A0-warm) — identical bytes, fresh fires: the floor.
- D1 = D(A0 vs A1), D2 = D(A0 vs A2), D3 = D(A0 vs A3).
DECISION RULE (pre-registered): drift is semantically load-bearing iff
D1 > D0 with Fisher exact p < 0.05 AND the effect appears in >= 2 of 3 task
categories. Otherwise DISPUTED stays DISPUTED.

### Stopping rule
- Primary: full battery = 12 tasks x 5 arms-fires x 5 samples = 300 fires
  (~2.4M prompt tokens; with the warm scaffold at ~95% cache this is pennies
  on 5.3-flash, $0-electricity on self-host).
- Early-STOP-AND-CLAIM: after pass 1, if D0 = 0 across all 60 A0 pairs AND
  D1 >= 20%, the separation is decisive — stop, claim, spend nothing more.
- Early-stop-NOT-allowed for null: a null D1 requires the full battery plus a
  second pass at temperature 0.7 before "answers insensitive" may be recorded
  (floor effects fake nulls; epoch-1 law).

## 3. Pre-registered predictions (tri-state, before any fire)

- P1 COST (SUPPORTED, W3 carryover): warm_hit >= 0.95; A1 collapse —
  cached_tokens(A1) ≈ tokens-before-drift-byte (≈10% of scaffold) ± tokenizer
  slack; A2 collapses to the first moved block boundary; A3 ≈ warm (paragraph
  is APPENDED after existing bytes → LCP intact — this asymmetry is itself a
  prediction: polish costs nothing, permutation costs everything).
  Falsified if A1 retains > 50% of warm benefit.
- P2 ANSWER-1B (the lane's real question): pre-registered SUPPORTED-but-small —
  one inert byte shifts the T3 answer distribution above D0, ~no effect on
  T1/T2. If SUPPORTED: the scaffold is load-bearing at the SEMANTIC level, not
  just cost — model state reads scaffold identity as signal; worldline seeds
  become cognitive objects, not just cache keys. If DISPUTED (D1 = D0 = 0 full
  battery): byte-sensitivity is an ECONOMICS fact only; the minimal-harness
  finding must then live in A3/A2, not A1.
- P2b REORDER: D2 >= D1 (larger perturbation, larger shift) — and the only arm
  that changes bytes WITHOUT changing content, so any D2 > D0 isolates
  ORDER as the active ingredient.
- P3 HARNESS REPLICATION: A3 degrades T1/T2 exact-match by >= 5 points vs A0,
  or shifts T3 rubric scores beyond D0 — replicates "best in minimal harness"
  as a causal scaffold effect. Falsifier: A3 within floor everywhere.
- V4.1-specific prior: Engram's n-gram hashing makes P2 MORE likely on V4.1
  than on 5.3-flash; a cross-model D1 gap (V4.1 >> 5.3-flash) would localize
  the effect in the memory architecture. Registered as exploratory, one shot.

## 4. Execution notes

- Harness first, offline: pure-python fire/scorer with fixtures + tests
  (mag/cache_identity.py pattern: 27 offline assertions before any network).
  No API keys in the harness; GOPHER judge reads a results JSONL after the fact.
- Bounds honored: this file is design only; zero fires were made.
- On claim: fold into the KV-OS charter thread and the tesuji ledger (this is
  a cell: "scaffold byte → answer drift", probe cost ~pennies).
- Related: watch/inbox/W3_CACHE_IDENTITY_20260907.md (drift law),
  watch/inbox/v41_paces/LANE6_encoding.md (DSML one-byte gift),
  watch/inbox/DESK_DSV41FLASH_20260911.md (subject),
  docs/ref/ZAI_API_EXPERT_REFERENCE.md §3 (meter, EXP-A),
  watch/WORLDLINE_SEED_20260907.md (F-W2 lineage).
