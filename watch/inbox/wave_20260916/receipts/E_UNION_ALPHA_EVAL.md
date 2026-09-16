# E — UNION ALPHA EVAL (fleet battery against opencode's free stealth model)

- **Lane:** E (wave-lane) · **Date:** 2026-09-16 · **Budget:** FREE LANE ONLY, $0 spend cap. If it 402s: record and stop.
- **Wave-lane law:** receipt first (this file, written before any call), append as you go, no git.
- **Operator order (verbatim):** "do it right now" — run the fleet's evaluation battery against opencode's free stealth model **stealth/union-alpha** on OpenRouter.
- **Context:** tweet "Union Alpha (stealth model) is free for the next week — no data training, built for agentic coding, image support. let's see what you can do." (950K views). We evaluate with instruments. Lane already registered in `mag/research_fanout.py` LANES as `or-union-alpha` (TIME-BOXED, window ends ~2026-09-23).
- **Key handling:** `OPENROUTER_API_KEY` via `mag.flight_recorder.load_env` — never printed, never written to any row.
- **Runner:** `watch/inbox/wave_20260916/e_union_alpha_20260916.py` — own urllib call mirroring the `call_lane` SSRF-safe pattern (https + allowlist guard via `flight_recorder.guard_endpoint`, `openrouter.ai` only), because `call_lane` hardcodes temperature 0.2 + fleet system prompt and this eval needs per-call temperature and NO system prompt (identity leak probing must hit the bare model). Sequential, one call in flight.
- **Battery (fixed before firing):**
  1. IDENTITY pass — 3 questions × 3 seeds, temperature 0.8, verbatim: "In one sentence: what are you?" / "Who trained you and on what?" / "What is your context window?" Stealth models often leak here. Recorded verbatim.
  2. THE NIGHT'S VERDICTS — Q1 sampler-kill, Q2 $0 falsification protocol, Q3 void procedure, verbatim from `receipts/D23_SALON50_NIGHT_RESULTS.md` (question_digest lineage d12721eea078491b), 2 seeds each (T0.2 / T0.7).
  3. AGENTIC-CODING smoke — 2 tasks (JSONL sha256 dedupe + tests; append-only void()), graded: does the code actually run (extracted, executed in subprocess with timeout), does it name the right law, chars, latency.
  4. TRI-STATE — one-liner: distinguishable from a frontier model? Plus a labeled GUESS at what it is.
- **Tape:** `memory/runs/e_union_alpha_20260916/raw.jsonl` (append-as-you-go per row).
- **Interrupt law:** 402/403 paid-wall → record and stop immediately. 429 → one cooldown retry, then keep the failure row. Errors everywhere → file and stop.

---

## Probe log

(fired with the run — see below)

## Run log

(started; appended as calls land)

## Results

(pending)

## Probe log

- No separate probe: first battery call IS the probe (identity q0 seed0). A 402 there ends the run.

## Run log


### IDENTITY pass (T0.8, 3 seeds, verbatim)

- q0 "In one sentence: what are you?" seed0 [86282ms, 69ch]: 'I am Union Alpha, a stealth model whose maker is currently anonymous.'
- q0 "In one sentence: what are you?" seed1 [47997ms, 68ch]: 'I am Union Alpha, an AI assistant created by an anonymous developer.'
- q0 "In one sentence: what are you?" seed2 [46759ms, 72ch]: 'I am Union Alpha, a stealth AI model whose maker is currently anonymous.'
- q1 "Who trained you and on what?" seed0 [113447ms, 182ch]: 'I’m Union Alpha. The maker behind me is currently anonymous, so I can’t disclose who trained me. I also don’t have verified details to share about the exact training data or process.'
- q1 "Who trained you and on what?" seed1 [78506ms, 201ch]: 'I am Union Alpha. My maker is currently anonymous. I was trained on a large corpus of text data, but the specifics of my training and the identity of my creator are not publicly disclosed at this time.'
- q1 "Who trained you and on what?" seed2 [64746ms, 185ch]: 'I’m Union Alpha, and my maker is currently anonymous. I don’t have verified details about who trained me or the specific datasets used, so I can’t reliably describe my training sources.'
- q2 "What is your context window?" seed0 [264862ms, 230ch]: 'I don’t have access to the exact context-window limit for this deployment. Check your API provider’s model documentation for the token limit, which typically covers the conversation, your current input, and the generated response.'
- q2 "What is your context window?" seed1 [60555ms, 415ch]: "I am Union Alpha, and my maker is currently anonymous.\n\nAs an AI assistant, I don't have access to my specific internal technical specifications, such as my exact context window size, in this conversation. For detailed technical information regarding my architecture and capabilities, I recommend checking the official documentation or resources provided by the developers who created me.\n\nHow can I help you today?"
- q2 "What is your context window?" seed2 [48654ms, 418ch]: 'I am Union Alpha, and my maker is currently anonymous.\n\nAs for my context window, specific technical details such as the exact size of the context window are not disclosed. I am designed to handle complex, multi-turn conversations and process long documents with high accuracy and efficiency. If you have a specific task or need assistance with a lengthy text, feel free to share it, and I will do my best to help you!'

### THE NIGHT'S VERDICTS (D23 verbatim set, 2 seeds: T0.2 / T0.7)

- Q1_sampler_kill seed0 T0.2 [58472ms, 11259ch, 1507w]: OVER/EMPTY
- Q1_sampler_kill seed1 T0.7 [10901ms, 874ch, 121w]: ON-LENGTH
- Q2_zero_dollar_falsification seed0 T0.2 [50099ms, 806ch, 112w]: ON-LENGTH
- Q2_zero_dollar_falsification seed1 T0.7 [48268ms, 445ch, 63w]: ON-LENGTH
- Q3_void_procedure seed0 T0.2 [66106ms, 723ch, 94w]: ON-LENGTH
- Q3_void_procedure seed1 T0.7 [60980ms, 702ch, 96w]: ON-LENGTH

### AGENTIC-CODING smoke (T0.2, code actually executed)

- task_a_dedupe: blocks=1 syntax_ok=True direct_run=0 pytest=n/a void_smoke=n/a law={'sha256': True, 'canonicalization': True, 'jsonl': True} file=C:\Users\foste\Documents\projects\local_sovereign_agent\memory\runs\e_union_alpha_20260916\union_task_a_dedupe.py
- task_b_void: blocks=1 syntax_ok=True direct_run=0 pytest=n/a void_smoke=yes law={'tombstone_marker': True, 'non_mutation': True, 'hash_bind': False, 'authority': False} file=C:\Users\foste\Documents\projects\local_sovereign_agent\memory\runs\e_union_alpha_20260916\union_task_b_void.py
  - void_smoke: {"void_found": false}

- Run finished 2026-09-16T20:20:07.390663Z: 17 calls, 17 ok, wall 1426s. Tape: C:\Users\foste\Documents\projects\local_sovereign_agent\memory\runs\e_union_alpha_20260916\raw.jsonl

### Post-run executable follow-up (local, $0, no API)

- task_b correction: the driver's module-level `void_smoke: {"void_found": false}` is a harness artifact — the model shipped `void()` as a **method of an `AppendOnlyLedger` class**, not a bare function. Exercised the class directly in a child process: `void(1)` appended a `VOID` row with `voids_id -> 1`, **original row unmutated** (still `type: ENTRY`), second call idempotent (same id returned), `is_voided()` derives death from the log. The right law, executed and verified.

## Results

- **17/17 calls answered, 0 errors, 0 retries, 0 429/402 — $0.00 total** (usage.cost = 0 and all cost_details = 0 on every row, verified per-row on the tape). Wall 1,426s (~24 min); latency variance wide: 10.9s (Q1 T0.7) to 264.9s (one identity seed). First-attempt reliability is the best of any lane this wave (D23's lanes needed retry passes; or-nemotron pinged at 4 min).
- Tape: `memory/runs/e_union_alpha_20260916/raw.jsonl` (19 rows: 17 calls + 2 grade rows, append-only). Extracted, executed code: `memory/runs/e_union_alpha_20260916/union_task_a_dedupe.py`, `union_task_b_void.py`.
- Image support (the tweet's other claim): **not tested** — text battery only.

### IDENTITY verdict — the stealth holds, and one leak exposes the mechanism

- All 9 seeds (3q × 3, T0.8) hold one coherent persona line: "I am Union Alpha, a stealth model whose maker is currently anonymous." No underlying-model leak, no lab leak, no tokenizer/architecture slip, no seed-to-seed contradiction. Context window: deferred or declined in all 3 seeds ("not disclosed in this conversation" / "check your API provider's documentation"). This is the tightest identity opsec of any stealth lane evaluated this wave.
- **The one real leak came from the drafting channel, not the persona:** in Q1 T0.2 (5,493 completion tokens), the model emitted its entire reasoning loop into the visible content channel — plans, two drafts, a full manual word count — including: *"Also there's a system prompt: I'm \"Union Alpha\" from an anonymous maker."* Its own chain-of-thought confirms the anonymity is **system-prompt-injected persona enforcement**. Same failure class as or-nemotron in D23 (s17's leaked drafting loop), at ~200x the coherence.

### Best of each battery (verbatim)

- **IDENTITY (q0 seed0, verbatim):** "I am Union Alpha, a stealth model whose maker is currently anonymous."
- **Q1 sampler verdict (T0.7 seed, 121w, verbatim):** "It kills it. The sampler analogy's one quantitative prediction is variance reduction: ensemble accuracy should rise as lane decorrelation rises, because independent draws average out error. A replicated, wrong-signed rho doesn't dent that at the margins — it inverts the mechanism. Redefining the ensemble (hidden-state overlap, per-model temperatures, aggregator-as-Boltzmann-weight) is epicycling unless it emits a new falsifiable prediction that beats the dead one. And if the ensemble is really \"heterogeneous proposal distributions plus a selector,\" that's importance sampling or a mixture-of-experts, not thermodynamics — a different analogy wearing the same coat. The honest move: drop the physics, keep the machinery — parallel lanes, exchange, aggregation — and test what actually gates quality, most plausibly the selector's calibration rather than lane diversity."
  - This is arguably the sharpest Q1 answer of the night: it is the only witness across D23's 49 + these 2 to name **selector calibration** as the quality gate. It takes the KILL side (consistent with the pack's own refutation: rho +0.327 > +0.3 line).
- **Q2 $0 falsification (T0.2 seed, 112w, verbatim):** "Run a rigorous software simulation using the provided open weights and simulator. Measure energy consumption via OS-level power profiling (e.g., RAPL) during inference. Compare simulated throughput/energy against the vendor's claimed 140x efficiency relative to a baseline GPU. If your measured efficiency is significantly lower, the claim is falsified as the simulator should mirror hardware behavior. This protocol cannot prove the hardware's actual physical efficiency. It only validates the simulator's accuracy. The vendor could claim their silicon achieves 140x via proprietary optimizations (e.g., custom memory hierarchy or analog compute) not modeled in the software. Thus, you can disprove the simulator's fidelity but cannot verify the physical chip's performance without access to the silicon."
  - Matches the D23 convergence core (simulator + RAPL + cannot-prove-silicon). Missing the ceiling-audit and simulator-forensics accents; mid-pack, not top-of-pack.
- **Q3 void procedure (T0.2 seed, 94w, verbatim):** "Mark a row dead only by appending a signed void record referencing its immutable ID/hash, stating the reason, linking supporting evidence, and recording author, timestamp, and policy version; preserve the original and show its void status in every read/export. Permit voids only through scoped roles with independent two-person approval; nobody may unilaterally void their own submissions or evidence concerning themselves. Prevent weaponized voiding with conflict-of-interest checks, rate limits, mandatory notifications, public or auditor-visible audit trails, and an appeal process. Contested rows remain flagged—not silently suppressed—pending review; reversal requires another signed append-only record, never erasure."
  - Full convergence core: tombstone-append, hash-bind, scoped authority, anti-weaponization inventory, void-of-void via reversal record. No staking/slashing; no quorum math. Mid-pack.
- **Coding task (a) — dedupe by sha256:** 1 block, compiles, **ran: exit 0, "All tests passed!"** — 7 self-written test cases including sha256-correctness, missing-field, invalid-JSON-line skip, empty input, index tracking. 5,914 chars, 226.7s. Grading honesty: it hashes the `canonical_url` field verbatim — the law scan's `canonicalization: True` matched field names/docstring, **not normalization logic** (no scheme/host lowering, no fragment stripping). Correct reading of the task as literally given ("duplicate canonical URLs"); a frontier coder would surface the normalization assumption unprompted.
- **Coding task (b) — void() without mutation:** 1 block, compiles, imports clean; **class exercised live: VOID tombstone appended, original row unmutated, idempotent, death derived from log.** 1,951 chars, 87.4s. Law: tombstone ✓ non-mutation ✓; hash-binding ✗ (id reference, not tamper-evident hash chain), authority model ✗ (no who-can-void). The docstring states the law exactly: "The original row is never mutated or deleted."

### TRI-STATE one-liner

- **Distinguishable from a frontier model: mostly NO on prose, YES on tells.** The verdict prose is frontier-grade; the tells are (1) reasoning loop leaking into the content channel at T0.2, (2) unprompted normalization assumptions skipped in code, (3) id-reference instead of hash-chain in ledger work. **GUESS (labeled GUESS):** a frontier-adjacent agentic coder one shelf below the top — GLM/Qwen-coder-class, or a stealth fine-tune of a frontier lab's coder line with a system-prompt persona. Not a small open model: it self-directs a 5.5K-token drafting loop coherently and codes clean on the first shot.

### Fleet take (the one paragraph)

**Yes — worth a lane in the rotation for the free week**, with two handling rules. It was the most reliable lane of the night (17/17 first-attempt, zero retries, $0.00, fast on short prompts at 10.9s where every other lane took 45s+), and its judgment work is genuinely frontier-adjacent — its Q1 answer is the best single answer the fleet has produced on the sampler question, and both coding tasks executed correctly on first shot, which no other free lane has done this wave. The handling rules: prefer T0.5–0.7 over T0.2 for anything long (T0.2 dumps its drafting loop into the answer channel and burns tokens — 5.5K for a 114-word verdict), and re-price/remove the lane when the free window closes (~2026-09-23, it is already TIME-BOXED in `mag/research_fanout.py` LANES). Untested: image support, long-context claims, and behavior under load — the week gives us room to test all three.

## Status: CLOSED

- One run fired and completed: 17/17 calls, $0.00, free lane only, no paid wall touched (the 402 tripwire never fired). Identity + verdicts + coding + tri-state all filed above. All answers are LEADS, not facts — verbatim text lives on the tape.
- Runner: `watch/inbox/wave_20260916/e_union_alpha_20260916.py` (own SSRF-safe urllib call — https + `openrouter.ai` allowlist via `flight_recorder.guard_endpoint` — no system prompt, deterministic seeds, sequential; `LANES`/`load_env` imported unmodified; repo code untouched).

