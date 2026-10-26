# L02: CLIProxyAPI deep-read (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L02) · **Class:** RECEIPT / steal + warning
**Subject:** router-for-me/CLIProxyAPI. Go, MIT (verified), 53,266 stars, created 2025-07-01, pushed 2026-09-26 (today), v7.3.15-19 in the last 4 days.

## The core trick (read from source, not README)

Re-runs the official coding CLIs' own OAuth flows (PKCE, reusing each CLI's public client_id and localhost redirect), saves tokens as JSON, then serves OpenAI + Gemini + Claude wire formats translating to each provider. Wrapped: Codex/ChatGPT (client_id app_EMoamEEZ73f0CkXaXp7hrann), Claude Code (client_id 9d1c250a-..., redirect localhost:54545), Antigravity/Gemini via Google's cloudcode-pa v1internal, xai/Grok, Kimi, Devin, Meta, Vertex, Qwen/iFlow, any OpenAI-compatible upstream by key.

## The warning (this is the lane the fleet must NOT enter)

Maintainer in issue #3340: "Using these two products in other clients will inevitably violate the TOS, and a ban is certain." Real bans: #266 (OpenAI account banned ~8 hours after VPS + team key share), #2211 (Claude account disabled under consumer ToS), #3431, #1327 (Kimi For Coding). And the repo DELIBERATELY IMPERSONATES the native clients: internal/auth/claude/utls_transport.go uses refraction-networking/utls TLS-fingerprint mimicry plus byte-exact header ordering including the profile/roles companion GETs the real Claude Code client makes. That is circumvention engineering. The fleet's ToS-friendly key-based ladder does not need any of it; this lane is reference-only for what to avoid.

## What IS worth stealing (provider-neutral, clean)

1. **singleflight per token + invalid_grant exponential backoff (1min to 30min) + "ineffective refresh" 30s guard** around every token refresh; never stampede the refresh endpoint.
2. **Per-credential cooldown state machine driven by upstream quota headers** (Retry-After, model-scoped resetIn), backoff 1s to 30min with 10s floor; snapshots REPLACED not merged so stale watermarks never linger.
3. **Selector strategies:** RoundRobin keyed on last pick (shrinking pools don't starve), WeightedRoundRobin, FillFirst ("burns one account before moving to the next, staggers rolling-window subscription caps"), session-affinity sticky accounts.
4. **One-JSON-file-per-credential + filesystem watcher + manual re-login endpoint.**
5. Their ops mistakes to avoid: no per-client rate limiting (#3467), management IP-bans keyed on spoofable X-Forwarded-For (#4733).

## Health

Extremely active (448 commits/4 weeks), 628 open issues, v7 API churn real: pin a tag if borrowing code.

## Agent debts

Refresh-loop internals partially read; Qwen/iFlow/Gemini-CLI auth locations unverified; external ban-thread sentiment unchecked (search rate-limited); translator + management-API auth model not deep-read.
