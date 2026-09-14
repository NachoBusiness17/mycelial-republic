# SALON SYNTHESIS — FULL RESEARCH SALON (2026-09-01 07:3xZ)
lanes: 5/5 returned · DeepSeek · board-only · fetch-log shared at /board/salon_research/fetch_log.md
inputs: operator directives 07:03Z (war games) + standing open questions ($600 lever, custody, launch watch)

## HEADLINE VERDICTS

**1. War-games (R1) — the venue is real and our infrastructure is the differentiator.**
Precedents VERIFIED: Grey Swan Arena (crowdsourced red-team, data feeds fine-tunes), AgentBench, tau-bench, OSWorld, TheAgentCompany (server-per-agent — closest to "server per participant"), AI Village/Smallville, CATArena (agents write strategies, compete, revise — closest to "write agent, test, iterate"). Winning format for us: **switchboard-arena** — our POSTED→CLASSIFIED→AUTHORIZED→EXECUTED→RECEIPT state machine IS the referee, verkle receipts ARE the anti-cheat. v0 (this week, $0, internal): chess-oracle arena — running NOW as match_001 (/board/WARGAMES_V0_SPEC_20260901.md). v1: server-per-participant intranet + adversarial objective, approved models = vault quants, distribution via X surfaces after receipts exist. Red lines honored: no second gateway, no new engine, no new authority path.

**2. The $600 question (R2) — the quote is UNDER street; real 128GB = $800–950.**
All prices QUOTED+URL'd 2026-09-01: 128GB non-ECC 4×32 kit $800–950 (A-Tech $904, Timetec $891, NEMIX $913+) — AM4 consumer takes non-ECC only, the $1,190+ ECC kits are irrelevant. 20TB CMR renewed **$328–630**; 4TB NVMe $470–490; used 3090 $1,100–1,300; 4090-48GB-mod and A5000 = skip. **Rank: 1) RAM (~$850) 2) 20TB drive ($328) 3) 3090 ($1,200).** Cheapest path to own-weights fleet this quarter: RAM + renewed drive ≈ **$1,180 that serves AND stores** — strictly more estate per dollar than a lone 3090. Flags: verify the $600 listing before spending (UNVERIFIED); 4-DIMM AM4 may downclock — board QVL/BIOS check first; GPU must live on the Windows host (Mag venv side), not the cage.

**3. Local serving reality (R3) — hybrid arch does NOT block CPU, but temper expectations.**
llama.cpp GLM5next support = OPEN PR #27773 (not merged; KDA layers via Kimi-K3 graph, mHC via DS-V4 graph, DSA via MLA). CPU-only AM4/128GB verdict: **~3–7 t/s on UD-IQ1_M (~70GB) or UD-IQ2_XXS (~92GB) only; IQ4_XS (167GB) doesn't fit.** Choose IQ2_XXS first (PPL 20.3 vs IQ1_M 73.9). ktransformers/vLLM/FreeToken = GPU-centric; AM4 has no AMX. Cross-check R2+R3: the RAM lever buys a **batch/sandbox local lane, not an interactive one** — interactive local serving needs the GPU lever. Sovereignty value stands; latency value doesn't.

**4. Quarantine lane (R4) — GLM-5.3-Flash-abliterated EXISTS, hours old.**
lovesenko/GLM-5.3-Flash-tr3-4bpw-Abliterated, created 2026-09-01 04:26Z, MIT, 0 downloads. Base MIT → self-host defensible. Full GLM-5.3 = license:other → contract-uncertain, abliteration.ai product = API-only (provider-mining lane, not custody). Fleet mirrors license-clean (Huihui DS-V4-Flash MIT; gemma-4-31B Apache + new huihui v2; Qwen3.6-35B-A3B Apache ×2). Eval harness = hobby-grade (<1K samples, Apache). Custody verdict: 4 model families + 4 datasets → Phase 6; new Tier-B grab candidate = the GLM-Flash-abliterated.

**5. Launch horizon (R5) — one HOT-gate correction, one verified drop.**
- **Together H100 cut VERIFIED**: primary post 2026-09-01 (@togethercompute/status/2094583517015376237), Dedicated Inference H100 $5.49→$3.99/hr for September, auto-applied. Economist may re-cost the $3.99 floor.
- **GLM 6.0 RSI claim: NO primary evidence.** docs.z.ai release notes show GLM-5.x only; the Emad-surfaced "GLM-6.0 RSI roadmap" fails deref. Downgraded from roadmap-watch to UNVERIFIED rumor. (Earlier 03:34Z verdict based on the Emad post gets this correction.)
- Anthropic next-gen = preparative signal, no date. **DS-V4 full weights ALREADY OPEN since April (MIT) — self-host now, not a wait.** Qwen3.8-Flash-Next = Qwen4-architecture preview, bankable. Llama frontier closed (Muse Spark), Muse Glimmer 30B Apache → vault candidate.

## CROSS-LANE SYNTHESIS
- R2+R3 fuse into one hardware decision tree: **$600→64GB (partial), $850→128GB (batch-local GLM), $328→20TB (archive), $1,200→3090 (interactive local + FreeToken real)**. The estate ladder wants RAM+drive first ($1,180), GPU when a serving need is proven.
- R4+R5 fuse: the quarantine lane just got its GLM family member the same day the base went MIT-custody — Tier B can mirror the FULL fleet.
- R1+A-invariant fusion: steer_bus I2 (version-pinned receipts, env-collapse→DROPPED) = the war-games anti-cheat core. One build serves both.

## ACTION QUEUE (new items from this salon)
1. Verify the operator's $600 128GB listing (or buy at street $850+ if it doesn't verify) — QVL/BIOS check first.
2. Tier-B grab: GLM-5.3-Flash-tr3-4bpw-Abliterated (MIT) — queue behind current chain.
3. Seat-dispatch route for probe battery execution if session-based probing underdelivers.
4. Muse Glimmer 30B + Qwen3.8-Flash-Next → vault candidates list.

## SALON LADDER (measured)
5/5 lanes ≤50 lines, shared fetch log kept, 0 messaging violations, 0 two-strikes, quotes-or-UNVERIFIED held by all lanes (R5's date discipline caught the GLM-6.0 fiction; R2's price discipline caught the $600 quote). Runtime 1–5.5min/lane. Next: batch probe spend behind operator receipt; keep 5-lane shape; add per-lane citation counts to future syntheses.
