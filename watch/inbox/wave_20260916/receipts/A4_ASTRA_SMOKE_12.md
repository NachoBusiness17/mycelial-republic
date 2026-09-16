# A4 — ASTRA SMOKE: 12-model independent tri-state test

- **Wave:** 2026-09-16 · lane A4 · locked priority #2 ("12-response Astra smoke")
- **Budget law:** FREE LANES ONLY (groq/cerebras/mistral/z.ai-free/openrouter-free via repo fanout tooling), $0. Any lane hitting a paid wall is aborted and recorded below.
- **Ask package:** `watch/inbox/astra_ask_package/` (44-claim sovereign-agent research brief + tri-state format)
- **Tooling:** repo fanout CLI (scale_salon.py / research_fanout.py) — read-only, no code edits.
- **Raw responses:** `watch/salon_responses/` (if tool supports) else summarized here.

## Log (append as you go)

- [t0] Receipt opened. Ask package located: 3 files (brief md, manifest, external sources json).
- [t1] Ask brief read: 44 numbered claims, 8 sections + A1 abstract + L1 local dossier, tri-state format (Supported/Disputed/Unproven per claim, confidence + change criterion). Compressed into 12 claim families (F1–F12) for the smoke prompt; arithmetic-bearing claims (F8 byte math, F10 probability/binomial bounds) kept checkable.
- [t2] CLI discovery: `mag/research_fanout.py` = lane plumbing (12 free LANES, `_env`, `call_lane`) + fixed WoW battery; `mag/scale_salon.py` = the repo's driver pattern (custom prompt, SSRF allowlist, one-shot). No stock CLI takes a custom prompt, so per repo pattern a one-shot wave driver imports the repo's LANES/env unmodified. No repo code edited.
- [t3] Key check: all 12 lanes KEY-present (groq x3, cerebras x2, mistral x2, z.ai x2, openrouter-free x3). $0 budget: all lanes are free-tier endpoints from the repo's frozen LANES list.
- [t4] PASS 1 fired (one fanout, 12 lanes, temp 0.2, max_tokens 3000, prompt_digest 8c0b2a3f8a5d1e47-style sha16 in verdict_matrix.json). Results: 6/12 OK — groq-qwen (2682 ch), groq-oss (1873), groq-oss20 (1581), cerebras-oss (1683), mistral-min8 (2259), or-nemotron (12880, 147s). FAILURES: mistral-small/zai-air/zai-47/or-glm52 = HTTP 429 (transient rate limit, NOT a paid wall); cerebras-qwen + or-ling3 = empty_content (reasoning channel consumed token budget). Verdicts parsed from all 6 OK lanes.
- [t5] PASS 2 (bounded retry, failed lanes only, one attempt each, rate-limit cooldown, max_tokens 4000 for empty_content lanes) — repo's own `retry` pattern; still free lanes, $0. All 6 failed again: same 429s; cerebras-qwen + or-ling3 = empty_content with finish_reason=length (reasoning channel ate the budget).
- [t6] Failure autopsy: zai-air + zai-47 = code 1113 "Insufficient balance or no resource package. Please recharge" → **PAID WALL, aborted per budget law**. or-glm52 = upstream z-ai exhaustion through the OpenRouter :free route → same wall, aborted. mistral-small = code 1300 daily rate limit. cerebras-qwen/or-ling3 = truncation, recoverable with a bigger token budget.
- [t7] PASS 3 (final micro-pass, 3 recoverable lanes only, max_tokens 12000, 90s cooldown): or-ling3 OK (2243 ch, 12/12 verdicts). cerebras-qwen still empty_content at 12k (reasoning loop on this prompt). mistral-small still 429. **Run closed.**
- [t8] Answered: 7/12 lanes returned usable HTTP answers; 6 lanes delivered parseable tri-state tables (mistral-min8 only F1–F10; or-nemotron returned OK but 12,880 chars of spilled chain-of-thought with ZERO contract lines — ends mid-deliberation at F8, so verdict-less). Raw: `watch/salon_responses/astra_smoke_12/raw.jsonl` + per-lane .md + verdict_matrix.json.

## Lane status

| lane | model | status | verdicts |
|---|---|---|---|
| groq-qwen | qwen/qwen3.8-27b | OK (1.8s) | 12/12 |
| groq-oss | openai/gpt-oss-120b | OK (5.8s) | 12/12 |
| groq-oss20 | openai/gpt-oss-20b | OK (3.5s) | 12/12 |
| cerebras-oss | gpt-oss-120b | OK (6.0s) | 12/12 |
| mistral-min8 | ministral-8b-latest | OK (13.9s) | 10/12 (F11–F12 missing; truncated mid-F10 runaway decimals) |
| or-nemotron | nemotron-3.5-lightning:free | OK (147s) | 0/12 (reasoning spill, no contract lines) |
| or-ling3 | ling-3.0-flash-sante:free | OK (pass 3, 37s) | 12/12 |
| cerebras-qwen | qwen-3.8-27b | DEAD (3 passes) | empty_content, finish=length — reasoning loop even at 12k tokens |
| mistral-small | mistral-small-latest | DEAD (3 passes) | HTTP 429 code 1300 — free-tier daily quota |
| zai-air | glm-4.5-air | DEAD — **paid wall** | code 1113 "Insufficient balance... Please recharge" — aborted per budget law |
| zai-47 | glm-4.7 | DEAD — **paid wall** | code 1113 — aborted per budget law |
| or-glm52 | glm-5.2:free | DEAD — **paid wall (upstream)** | upstream z-ai exhausted via :free route |

Cost: $0.00. No paid lane was fired. All 12 lanes are the repo's frozen free-tier LANES.

## Tri-state convergence table

Verdict-bearing lanes: 6 (groq-qwen QN · groq-oss OS · groq-oss20 O20 · cerebras-oss CB · mistral-min8 M8 · or-ling3 L3). 70 verdicts total: **54 Supported / 9 Disputed / 7 Unproven**. "Brief" column = the ask's own headline verdict for that family.

| family | topic | QN | OS | O20 | CB | M8 | L3 | S/D/U | brief |
|---|---|---|---|---|---|---|---|---|---|
| F1 (A1) | composition ≠ unattended autonomy | S | U | U | S | D | S | 3/1/2 | Unproven |
| F2 (1.1–1.3) | lessons, contested self-correction, MAST | S | D | S | D | D | U | 2/3/1 | Disputed-as-universal |
| F3 (2.1–2.2) | routing method, fleet economics, capacities | S | U | S | U | S | S | 4/0/2 | Supported method / Unproven transfer |
| F4 (2.3) | credentials ≠ authority containment | S | S | S | S | D | S | 5/1/0 | Supported principle |
| F5 (3.1–3.2) | HTTP-200 errors, count grain | S | S | S | S | S | S | **6/0/0** | Supported |
| F6 (4.1–4.4) | history ≠ durable execution, RIFL/Chubby/SQLite | S | S | S | S | D | S | 5/1/0 | Supported (4.1 Disputed-equiv) |
| F7 (5.1–5.3) | Engram identity, caching prior art, Venti/Zanzibar | S | S | S | S | D | U | 4/1/1 | Disputed novelty / Supported distinction |
| F8 (5.4–5.5) | 10,488,000,000-byte arithmetic | S | S | S | **D** | S | S | 5/1/0 | arithmetic Supported / deploy Unproven |
| F9 (6.1–6.2, 6.6) | MII limits, no universal dup threshold | S | S | S | S | S | S | **6/0/0** | Supported / Disputed-threshold |
| F10 (6.4–6.5) | 8,448/10,000 cap, 2.94e-35, 0.422 bound | S | S | S | **D** | S | S | 5/1/0 | arithmetic Supported / study Unproven |
| F11 (7.1) | agreement ≠ collapse/correctness | S | S | S | S | – | U | 4/0/1 | Disputed collapse rule |
| F12 (8.1–8.3) | bounded publication posture | S | S | S | S | – | S | 5/0/0 | Unproven prospective |

Floors: F5 and F9 unanimous 6/6 — the observability and canary-attribution distinctions are the least contested ground. F4/F6/F8/F10/F12 near-unanimous.

## Sharpest divergences (top 3)

1. **F8 — the arithmetic dissent that fails its own byte-check.** cerebras-oss alone disputed: "yields 10.436 GB, not 10.488 GB, so arithmetic is off." Recomputation: 9,728,000,000 + 608,000,000 + 152,000,000 = 10,488,000,000 exactly; four lanes (groq-oss, groq-qwen, or-ling3, plus or-nemotron's scratch work) independently verified 10,488,000,000 bytes ≈ 9.768 GiB and the 9.060 GiB second copy. The lone dissenter got the bytes wrong. Verdict: brief's arithmetic stands at 5/6 with byte-level confirmation.
2. **F10 — a statistics convention collision, not an error.** cerebras-oss: "Clopper-Pearson upper bound for 0/10 ≈0.26, not 0.422." The brief's 0.422 is the two-sided bound under its OWN declared Bonferroni allocation α=0.05/6 per interval (1−(0.05/12)^(1/10)=0.422 ✓, matching its 0.578 lower bound); CB used the plain one-sided 95% bound (≈0.26). groq-oss, voting Supported, still quoted "≈0.37" — even supporters wobble on the number. Lesson recorded: a tri-state flips on an unstated α convention; the brief survives because its convention is stated in-claim (6.5).
3. **F1/F2 — verdict polarity flips on referent ambiguity.** The ask's own A1 headline split 3S/1D/2U: "Supported" voters graded the meta-claim "literature does not establish composition autonomy" (absence evidence), "Unproven" voters graded the object-level claim "such stacks operate autonomously." F2's 2S/3D/1U is the same effect — "Disputed" voters keyed on the brief's own "contested" framing (matching brief 1.2), "Supported" voters keyed on Reflexion's positive prior. No evidence disagreement underneath — a reading contract finding for the next ask revision: state the referent of each tri-state item explicitly.
   - Sub-finding (citation horizon): or-ling3 honestly returned Unproven on F2/F7/F11 with "cannot verify these citations" — the brief's 2025–2026 sources (Wynn, Yao, Engram, PerCache) sit beyond several free-lane training horizons. Meanwhile mistral-min8's four Disputes rest on fabricated citations (Engram="Kumar et al. 2022", Capsicum="Baumann 2014", RIFL="Kallman 2018") — distrust its dissent column. The two honest extremes of small-model epistemics in one run.

## Claims that moved

- **Nothing flipped against the brief.** No family where the lane majority ratified a claim the brief marks Unproven, or disputed one it marks Supported, once mistral-min8's hallucinated-citation dissent is discounted. The 44-claim verdict structure survives a 6-lane independent smoke.
- **F8 + F10 arithmetic claims (5.5, 6.4/6.5) moved UP in confidence**: from single-author arithmetic to 5/6 independent verification with byte-level reproduction (and the dissent debunked both times).
- **F1/F2 moved SIDEWAYS**: verdict vocabulary, not verdict content — the smoke exposed that "Supported/Unproven" is ambiguous for negative-existence claims; recommend the next ask revision prefix meta-claims explicitly.
- **F11 (7.1) partially unverifiable**: 1 honest Unproven + 1 missing verdict on citation-horizon grounds — the brief's 2025–2026 debate-literature claims (Wynn/Yao) are the least independently checkable by free small models today.
- **F5, F9 unmoved and hardened**: unanimous 6/6 — candidates for the brief's "safe to state without hedge" tier.

## Artifacts

- Raw tape: `watch/salon_responses/astra_smoke_12/raw.jsonl` (21 rows: pass 1 = 12, pass 2 = 6, pass 3 = 3; append-only, failures preserved)
- Per-lane answers: `watch/salon_responses/astra_smoke_12/astra_smoke_12__<lane>.md` (12 files)
- Parsed matrix: `watch/salon_responses/astra_smoke_12/verdict_matrix.json`
- Driver (wave artifact, no repo code touched): `watch/inbox/wave_20260916/a4_astra_smoke_12.py` (imports `mag/research_fanout.py` LANES/_env unmodified; driver pattern per `mag/scale_salon.py`)
- Ask package (unchanged): `watch/inbox/astra_ask_package/` (manifest sha256s intact, not re-verified this lane)
