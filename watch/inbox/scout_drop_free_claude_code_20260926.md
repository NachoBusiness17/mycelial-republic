# SCOUT DROP: free-claude-code + the free-provider-gateway genre

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 · **Class:** RECEIPT / scout finding
**Origin:** operator drop https://x.com/RoundtableSpace/status/2103767783141949937 (@RoundtableSpace: "run Claude Code for $0 using free model providers", 55.9K stars claimed)

## Verified live this seat

- **Alishahryar1/free-claude-code** (GitHub API): 55,986 stars, pushed 2026-09-26, AGPL-3.0. Mechanism: local proxy "fcc-server" + Admin UI; agents point at it, it routes to configured providers with an ordered fallback chain (failed request auto-tries next model without restarting the turn). Launchers for 10 harnesses: Claude Code, Codex, Pi, OpenCode, Cline, Hermes, DeepSeek Harness, Grok Build, Muse Code, Aider. Provider keys pasted into the UI; some OAuth (ChatGPT, GitHub Copilot, Vertex). Repo claims 1.3B+ free tokens/month (repo-claimed, unverified by us).
- Providers named: NVIDIA NIM (its default), OpenRouter, Groq, Google AI Studio, DeepSeek, Mistral, Cerebras, SambaNova, Cloudflare Workers AI, Z.ai, Kimi, MiniMax, Featherless, Chutes, SiliconFlow, LLM7, Scaleway, Lightning AI, plus local LM Studio / llama.cpp / Ollama.
- Same-genre siblings surfaced by GitHub search, all bigger or comparable, all pushed 2026-09-25/26: **diegosouzapw/OmniRoute** (70,420 stars, "one endpoint, 359 providers, 150+ free", MIT), **router-for-me/CLIProxyAPI** (53,252 stars, wraps Antigravity/Codex/Claude Code/Grok as OpenAI-compatible), **decolua/9router** (29,847 stars).

## Fleet relevance

1. **New free-lane names for the scout to probe:** Featherless, Chutes, SiliconFlow, LLM7, Scaleway, Lightning AI (plus SambaNova recheck). Feeds the provider-liveness pass and the lane ladder.
2. **The fallback-chain design is our lane ladder, productized.** Their own caveat, "a failed request may consume quota on multiple providers before succeeding," is the fleet's 1302-storm lesson restated by a 56K-star repo: naive fallback chains burn quota in storms. Their scale (56-70K stars in months) says demand for harness-agnostic free routing is huge; the fleet built this pattern internally and never shipped it.
3. **Cerebras parked gate:** genre evidence for the B2-142/143 revisit trigger, though FCC treats Cerebras as just another keyed provider, nothing card-specific. Gate stays parked.
4. **ToS posture:** FCC claims ToS-friendliness as a design goal (personal interactive coding use). The fleet's lanes are consistent with that posture; adopting the tool would not change it. AGPL-3.0 = steal-the-pattern freely, copyleft only bites if we ship derived code.

## Owed / gates

- Probe the 6 new provider names (1-token liveness, per provider-liveness protocol) before any lane decision. Owner: next scout pass or operator word.
- No install/adopt decision taken at this seat; file sits at the scout-drop tier.

Sources: tweet via syndication API (web_reader 1302'd, WebFetch timed out; syndication path clean), GitHub search API + repo README fetch. Evidence inline in this receipt; nothing else staged.
