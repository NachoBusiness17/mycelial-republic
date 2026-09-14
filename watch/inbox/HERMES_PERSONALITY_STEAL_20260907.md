# THE HERMES STEAL — personality system → ractor bodies (2026-09-07)
**Operator: "look into hermes personality and how we can steal that for ractors. maybe hermes can ride our lite coding plan key"**

## THE ANATOMY (what Nous shipped)
- **Personas are config entries, not code**: `config.yaml` holds a personality roster (helpful,
  concise, kawaii, catgirl, pirate, shakespeare, surfer, noir, uwu, philosopher, hype) — each is
  a plain system prompt string. Adding a persona = adding a paragraph. The desktop UI exposes
  them as a selectable roster.
- **SOUL.md at the data root** — the persistent identity layer, separate from chat personas
  (identity = the file; style = the persona). Ours already carries the RACTOR FLEET AMENDMENT:
  *You are a gopher body of the local_sovereign_agent fleet.*
- **Provider = custom, base_url = api.z.ai/api/paas/v4, model = glm-4.7-flash** — the operator
  already aimed Hermes at Z.AI. auth.json holds a credential_pool (xai, openai-api) — a z_ai
  pool is one entry away.
- **The CLI is a platform**: moa (Mixture of Agents), fallback (provider chains = our
  failover-to-Max law), curator, memory-graph, dashboard, skin, serve/desktop/gui, acp (Agent
  Client Protocol stdio server — editors drive it), egress, gateway.
- **The body**: WebView2 native window over a Python core, 46KB launcher stubs on PATH, uv-managed.

## THE RACTOR STEAL (the mapping)
| Ractor concept | Hermes mechanism |
|---|---|
| ractor persona (comedy icons, Fermat) | a config.yaml personality entry — one paragraph each |
| the ractor's voice/style | the persona prompt verbatim |
| the ractor's body | the Hermes desktop window (chat history, tools, TUI) |
| face-verify | the SOUL.md per-body (identity file per body) |
| the posting circuit | hermes cron/send (built-in scheduling + send doors) |
| seat rotation | hermes profile / credential pool |
The steal is a FOR-EACH LOOP: ractor roster → config personalities. The slick UI is free.

## THE LITE RIDE (verdict: SUPPORTED, wiring spec'd)
Provider custom already points at api.z.ai; model already glm-4.7-flash. The Lite lane key
drops into Hermes's credential store via a no-echo script (reads the key from the fleet's
storage, writes Hermes's config; the key is never printed, never committed). Meter clamp
1,400/day applies to Hermes like any body — metered-until-receipted, receipts per call.

## DEMO (fired same-turn)
One ractor persona installed into Hermes config (backup-first) + the Lite key wired + one live
test call = the proof. See research/hermes_steal/ for the receipt.
