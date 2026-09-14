# PRE-REGISTRATION — CORPUS GAUNTLET W1–W4 (filed 13:3xZ, before any run)
> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: arms, metrics, and fail thresholds were fixed before any provider call, making W1–W4 (incl. W4 steering-tail cache obedience) falsifiable — SUPPORTED (protocol timestamped pre-run, addendum pre-registers frontier row before first fire) · falsifier: any threshold moved after data exists (logged as protocol violation per card)

Falsifiable protocol per builder doc §7 (verbatim thresholds) + W4 (our instrument). Arms, metrics, and fail conditions are FIXED before first provider call. Post-hoc changes = protocol violation, logged as such.

## Workloads
- **W1 Riichi Mahjong tutor** — static ~3.5K tok (L0–L2+riichi), high churn (hand states), 1K requests. Lever: H.
- **W2 Nikoli generator + verifier loop** — static ~2K tok, 100 puzzles × 5 loops. Lever: H under loop re-entry.
- **W3 Solo-RPG campaign** — 20–70K tok static, 500 turns. Lever: c × H interaction (TokenPilot-class tail policy).
- **W4 (OURS) Steering-tail obedience** — fixed frozen prefix (4.8K), steering instructions varied post-prefix; measure obedience + cachedTok retention at warm vs cold. Lever: static/dynamic boundary integrity (builder's §6, untested by his W1–W3).

## Arms
A0 naive single-prompt · A1 structured prompt, no corpus layering · A2 full L0–L4 corpus, provider-native caching · A3 A2 + cache-aware compaction + linting.

## Metrics
Weighted hit rate H; cost/request (USD + token-equiv); p50/p95 latency; verifier pass rate (W2); blind review vs reference (W1/W3); drift incidents /100 turns; W4: obedience rate + cachedTok floor retention.

## Pre-registered predictions (fail thresholds in parens)
1. A2 achieves H ≥ 0.85 within-genre (FAIL < 0.75).
2. A2 price savings ≥ 75% on 0.1×-read providers; ≥ 40% on OpenAI-class (FAIL below H(1−r) floor).
3. A3 beats A2 on W3 by ≥10 additional % cost without quality loss (FAIL if quality non-inferiority violated).
4. Gauntlet critic loops (W2) show no H degradation across iterations when critic block is L0-resident (FAIL > 5% drift).
5. Cross-provider portability: same corpus within 15 points H across providers (FAIL if per-provider re-authoring needed).
6. **W4 (ours): steering obedience at warm cache ≥ obedience at cold, and cachedTok stays ≥ 95% of prefix size across ≥50 varied tails (FAIL: obedience degrades >5pp warm-vs-cold or cache rebuilds).**

## Lanes + budget
Provider-native caching arms on DeepSeek (r=0.214 measured; off-peak window 16:30–00:30Z); cross-provider portability arm on groq + key2 OpenRouter paid (r measured per lane first). **Burn cap: $5 total + $2 reserve. Cost per arm computed BEFORE the arm runs; ledger row per arm in water_ledger.**

## Known fences (from lane map — the term the builder's law lacks)
z.ai 1305 quota walls + burst gates + content-security filter; OpenRouter :free dead; cerebras 429s; plan-lane quota metering. Mitigation: DeepSeek primary, fences logged per arm as first-class data rows (fence name, code, tokens lost) — feeding the v6 `+ fences()` term.

## Status
R2 (corpus extraction) pending operator fuel — W1–W3 cannot run on ghost specs. W4 CAN run on our own prefix without the corpus; scheduled first tonight if corpus isn't ready by 16:30Z.

## ADDENDUM (19:xxZ, pre-registered BEFORE first Anthropic call): THE FRONTIER ROW
New experiment, registered before any Anthropic traffic: the 20-probe battery runs on **claude-sonnet-4-5** (frontier family, first non-open-weights row). Purpose: anchor the wavelength matrix against the frontier — the matrix's honest gap (open-weights-only) closes here.
- Predictions: (F1) frontier H will match or exceed open-weights warm-cache behavior IF cache_control is wired (deferred — first run is uncached baseline); (F2) answer depth on hard-01/hard-02 will exceed together-v3's 100-score depth (falsifiable by same-rubric scoring); (F3) cost per probe ≤ $0.025 sonnet-class (FAIL above $0.05/probe).
- Auth-map shape 4: x-api-key + anthropic-version + anthropic-workspace-id (the wrkspc_ paste is the gate).
- Cap $0.50. This addendum pre-registers BEFORE first fire — no threshold moves after data exists.
