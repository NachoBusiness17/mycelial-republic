# L01: OmniRoute deep-read (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L01) · **Class:** RECEIPT / steal
**Subject:** diegosouzapw/OmniRoute, 70,485 stars, MIT (verified via GitHub API), last push 2026-09-25 (one day before research), ~9,347 commits, created 2026-02-13. Began as a fork of 9router plus a TS port of CLIProxyAPI.

## Headline steals for the fleet (seat-selected from the report)

1. **Circuit breakers never trip on 429.** Their breakers trip only on [408, 500, 502, 503, 504]; 429 is classified quota/cooldown, not provider death. Recovery is lazy: when cooldown expires, the NEXT REAL REQUEST is the probe; the guide explicitly rejects active liveness pings. Fleet application: our 1-token liveness probes spend quota; their lazy-recovery-as-probe design is the alternative worth testing per lane.
2. **Quota state machine with an honesty rule:** five states (healthy, approaching_limit, exhausted, unavailable, unknown) and "unknown is not exhausted and does not disable a provider", with a source-precedence chain (official API → usage API → explicit header maps → admin config → local estimates → unknown) and the vow that local estimates are never presented as provider billing data. That is the fleet's no-fabrication law applied to quota telemetry.
3. **Free-capacity estimation methodology that refuses inflation:** daily caps x 30; RPD-only estimated as RPD x ~800 output tokens x 30; explicit refusal to multiply RPM x 24/7 ("the inflation we refuse"); docs counts enforced by CI. Steals directly into the scout's lane-value math.
4. **Egress-bucketed lock:** a 429 classified quota_exhausted cools ALL connections sharing the same egress IP. Directly relevant to the fleet's multi-key lanes behind one IP.
5. **Failover cap: 3 provider attempts default; auth/permission errors never retried.** Anti-thundering-herd guard prevents concurrent failures from double-incrementing backoff.

## Free-provider intel (OmniRoute's own estimates, unverified by us)

Steady monthly: Mistral ~1B tokens/mo claimed (2 RPM/500K TPM, biggest pool), nara ~210M, llm7 ~150M (5M/day, free token; matches our L00 open-catalog find), Kiro/xkiro ~150M ("free Claude"), Cloudflare ~30M, SambaNova 20/20/200K, Cohere ~800K, HuggingChat capped $0.10/mo. Uncapped-but-limited: SiliconFlow, GLM-CN (GLM-4-Flash + 20M signup credits), Gemini Flash, Ollama Cloud weekly credits. One-time credits: Vertex ~300M, AgentRouter ~$100, Doubao 15M, LongCat 10M (KYC), Scaleway ~1M. Keyless: Pollinations, DuckDuckGo Web, Blackbox, Reka, Nous, and more. Warning list (no/removed free tier): **chutes** (matches our 502s), phind, kluster, aimlapi, together ($5 min).

## Flags

Provider count drifts by source (357/358/359); Kimi (Moonshot) sponsorship disclosed via affiliate links, mild bias risk in free-provider marketing, though their FREE_TIERS doc actively pushes back on inflated claims. Their own CI flags main branch not-green at research time.

## Agent debt list

Counts secondhand from rendered summaries; token allowances not independently verified against providers; RESILIENCE_GUIDE quotes via summarization, retry-gate source not read line-by-line; maintainer responsiveness unverified.
