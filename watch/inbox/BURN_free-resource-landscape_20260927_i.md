# BURN free-resource-landscape 20260927 i - Lightning via SDK registry

## Verdict

steal

## Evidence

- .env name scan (cut -d= -f1, grep lightning/lit): only `ZAI_API_KEY_Lite` matched the "lit" fragment. No LIGHTNING/lightning-ai shaped key names. Authenticated probe skipped per rules.
- PyPI `https://pypi.org/pypi/lightning-ai/json`: HTTP 404. The name does not exist on PyPI; the board's SPA wall is not the only wall, the product name itself is not the package name.
- PyPI `https://pypi.org/pypi/lightning-sdk/json`: HTTP 200. info.summary: "SDK to develop using Lightning AI Studios". Version "2026.9.18.post1", requires_python ">=3.11", Apache-2.0, author_email "Lightning-AI <justus@lightning.ai>". Description head (4000 chars received): "Automate Lightning AI resources from Python scripts, notebooks, and CI." Documents the full API shape without the SPA: `Studio`, `Job.run(..., interruptible=True)`, `Deployment`, `Sandbox.create(name=..., instance_type="cpu-1")`, `Machine.CPU`, teamspace scoping ("owner/teamspace"), auth env names `LIGHTNING_API_KEY` and `LIGHTNING_SANDBOX_API_KEY`, warm-recipe sandboxes (recipe is the cache key, cold start "looks exactly like a warm one from the outside"), docs pointer `https://lightning.ai/docs/overview/sdk-reference`. No free-tier or credit quota statement anywhere in the received bytes.
- npm `https://registry.npmjs.org/-/v1/search?text=lightning%20ai%20serverless&size=5`: HTTP 200, all noise (lightningcss, serverless, unpdf, @neondatabase/serverless). No Lightning AI serverless package. npm angle is a miss.
- WebSearch "Lightning AI Studios free tier credits monthly 2026": thin and self-conflicting. lightning.ai docs snippet: "All users receive 5 free credits (1 credit equals $1 USD). Add a card for 25". Aggregator (usagepricing.com, not opened): 15 credits/month, ~80 spot GPU hours, one always-on Studio with 4-hour restart cycle, up to 2 concurrent GPUs, phone verification for GPU. Historical 22-30/month also cited. None opened directly.

## Steal or Vacuous

Steal, half-width. The SDK-registry angle is proven: lightning-sdk on PyPI is plain-text JSON that documents the Studios API surface (jobs, deployments, sandboxes, machine classes, auth) with zero SPA, and it is alive (release 2026.9.18.post1). That closes the "API shape" half of the owed Lightning row in fleet canon. Still owed: the exact free-tier credit numbers. Sources conflict (5+25-card vs 15/mo vs 22-30 historical) and none were read byte-direct; per no-fabrication law the number stays owed, structure (credit currency, card bonus, restart-cycled Studio, GPU concurrency cap, phone gate) is pinned as tier shape but not as receipts. Not a freelane candidate yet: no verified free endpoint, no keyless path, credits are metered dollars. Ledger row for the hot board: Lightning moves from "docs are SPA shells" to "API surface pinned via PyPI lightning-sdk; tier numbers still owed, conflicting snippets on file".

## Bibliography

- `watch/inbox/LINKS.jsonl` (tail -30, this repo)
- `memory/facts/behavioral.jsonl` (tail -30, this repo)
- `C:\Users\foste\Documents\projects\local_sovereign_agent\.env` (variable names only)
- https://pypi.org/pypi/lightning-ai/json (HTTP 404)
- https://pypi.org/pypi/lightning-sdk/json (HTTP 200, description head 4000 chars read)
- https://registry.npmjs.org/-/v1/search?text=lightning%20ai%20serverless&size=5 (HTTP 200)
- WebSearch result snippets: lightning.ai docs, usagepricing.com (pages not opened, marked owed)
