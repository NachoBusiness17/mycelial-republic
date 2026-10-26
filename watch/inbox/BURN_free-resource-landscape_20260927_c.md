# BURN free-resource-landscape 2026-09-27 c

## Verdict

steal

## Evidence

Pointer read: `watch/inbox/LINKS.jsonl` confirms the six unprobed lanes (Featherless/Chutes/SiliconFlow/LLM7/Scaleway/Lightning AI) came from the 2026-09-26 scout drop (entry: "6 new free-lane names for scout probe (Featherless/Chutes/SiliconFlow/LLM7/Scaleway/Lightning AI)"). `memory/facts/behavioral.jsonl` tail held only percolator invariants, no lane intel. `.env` variable names listed: no FEATHERLESS or SILICONFLOW key exists, so both lanes probed unauthenticated.

Featherless probe: `curl https://api.featherless.ai/v1/models` returned HTTP 200 unauthenticated. Body 7,065,556 bytes; grep counted 22,032 model id entries. First entries: "recursal/EagleX_1-7T" (model_class rwkv5-7b, context_length 16384), "recursal/EagleX_1-7T_Chat", "RWKV/EagleX-7B-Chat-V0.5-pth". Each entry carries pricing metadata (EagleX example: prompt 0.0000001, completion 0.0000002) and class breakdown: qwen2-0b5 3,087; llama2-7b 2,571; llama32-1b 2,480; qwen3-4b 1,438.

SiliconFlow probe: `curl https://api.siliconflow.com/v1/models` returned HTTP 401, body: {"code":30014,"message":"Token is invalid."}. Filed as-is per lane rules. Second attempt unspent: no env key to try, docs-page probe adds no lane value.

Web search "Featherless API free tier 2026": thin but directional. StartupMKT 2026 profile: "No, Featherless operates as a commercial paid service without an unrestricted permanent free tier." Devpost Pixel Forge hackathon offered code "PIXELFORGE26" for one month free API access, event-bound. Flat-rate subscription pricing model. No active permanent tier found; searcher noted results varied on trial status.

## Steal or Vacuous

Steal, one lane hot one lane gated. Featherless goes hot as a RECON freelane: its models catalog is keyless, returns the full 22k roster with per-model pricing and class tags, which is exactly the roster-diff food our endpoint_news sensor eats (roster rotates, the scout canon says free endpoints are perishable). It is NOT an inference freelane: no permanent free tier, so no hammer window without a funded key or promo code; any signup is an owed operator move. SiliconFlow stays dead until a key lands in `.env`; 401 is filed, lane remains on the owed list with the other four (Chutes/LLM7/Scaleway/Lightning AI). Adopted: nightly keyless catalog pull of api.featherless.ai/v1/models feeds roster-diff, zero key budget spent.

## Falsifier

Build proposed: a featherless catalog-diff sensor (one keyless curl nightly, diff against prior snapshot, receipt on roster delta). Pre-registered falsifier: if within 7 days of landing the endpoint returns 401/403 or drops pricing metadata from the payload, the sensor is vacuous, gets pruned, and the lane reverts to dead-until-key.

## Bibliography

- `watch/inbox/LINKS.jsonl` (repo, grepped for lane names)
- `memory/facts/behavioral.jsonl` (repo, tail 40)
- `.env` (repo, variable names only, values never read)
- curl https://api.featherless.ai/v1/models (HTTP 200 observed 2026-09-27)
- curl https://api.siliconflow.com/v1/models (HTTP 401 observed 2026-09-27)
- WebSearch "Featherless API free tier 2026" (StartupMKT 2026 profile; Devpost Pixel Forge hackathon listing)
