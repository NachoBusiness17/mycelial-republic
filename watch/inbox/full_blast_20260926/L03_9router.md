# L03: 9router deep-read (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L03) · **Class:** RECEIPT / steal
**Subject:** decolua/9router, 29,855 stars, MIT (GitHub API verified), created 2026-01-05, pushed 2026-09-26 (today). The ORIGINAL of the gateway family: OmniRoute describes itself as a fork of 9router + port of CLIProxyAPI; same default port 20128 confirms lineage. (Search was storm-limited; agent banked fetch-only, per instructions.)

## Headline steals for the fleet

1. **Protocol translator at localhost:** one OpenAI-compatible shim translating OpenAI ↔ Claude ↔ Gemini ↔ Cursor ↔ Kiro ↔ Vertex ↔ Ollama ↔ Responses, so any CLI wires in with a two-line config edit (Claude Code via anthropic_api_base in ~/.claude/config.json, Codex via OPENAI_BASE_URL). The pattern to build ourselves in MIT isolation.
2. **3-tier fallback ladder: subscription → cheap (GLM/MiniMax) → free**, with quota tracking, multi-account round-robin, auto OAuth refresh. This is the fleet lane ladder restated.
3. **Token savers productized:** RTK tool-output compression (claims 20-40% input savings), "Caveman" mode (~65% output savings), Headroom, Ponytail (YAGNI prompts). Fleet-relevant for context-pack economics.

## Free-tier reality check (erosion documented by the repo itself)

Kiro moved to paid Sep 2025 (~50 credits/mo residual); OpenCode Zen serves a fluctuating no-auth model list; Vertex $300/90-day trial. Honestly documented as DEAD in 2026: iFlow (paid), Qwen Code free OAuth (ended 2026-04-15), Gemini CLI free tier (Google shut it 2026-06-18). The "unlimited free" headline is a treadmill; the durable free layer is key-based API free tiers or local models.

## Red flags (why we don't adopt the npm global)

Default dashboard password 123456 unless INITIAL_PASSWORD set; CLOUD_URL defaults to 9router.com (config leaves the machine if cloud sync on); ENABLE_REQUEST_LOGS writes full bodies to disk; all prompts and OAuth tokens transit it as middleman; OAuth multi-account round-robin against consumer subscriptions is a ban magnet the marketing glosses over; and the whole fork family (9router 30K, OmniRoute 70K, free-claude-code 56K, all created Jan 2026) shows hyper-growth star velocity, so discount the social proof.

## Verdict

Steal the pattern, never the dependency: build the localhost shim + tiered ladder + token savers ourselves; treat 9router as the design doc and free-claude-code as reference-only (AGPL).

## Agent debts

OmniRoute/FCC claims single-sourced from READMEs; star-history spike analysis not run; cloud-sync payload and npm contents unaudited; Kiro/OpenCode availability not re-checked live.
