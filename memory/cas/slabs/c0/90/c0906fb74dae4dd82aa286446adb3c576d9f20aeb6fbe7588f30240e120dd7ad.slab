# WORK w-muse-spark-access

lane: hermes (headless one-shot)
ts: 2026-10-01T02:37:28.063341+00:00
ask: OpenRouter meta/muse-spark-1.3 and 1.2 return 403 on free keys. Research: what is the muse-spark access model? Is it a contributor program (like muse-glimmer-contributor), a paid tier, or region-locked? How do we get access? Check OpenRouter docs, Discord, model page.

---

Catalog confirmed live (12 muse variants, unchanged). Recon file is verified and complete. Here is the answer.

---

FINDING

The 403 is an age-attestation gate, not a paywall, not a contributor-membership gate, and not region-locked. All four `meta/muse-spark-*` slugs resolve to a single Meta-direct endpoint (`api.meta.ai/v1`) that enforces `age_18plus` via OpenRouter's provider-attestation layer. The 403 body names the fix exactly: "18+ age confirmation. Confirm at https://openrouter.ai/settings/preferences." After that fix a zero-credit key gets 402 (insufficient credits), not 403. Glimmer-30b returns HTTP 200 on the same key because it is open-weight served by non-Meta hosts (DeepInfra, Phala) with no Meta attestation. No free spark slug exists; all are paid. Contributor tier is a pricing-for-data tier, not a separate qualification program.

STEALABLE idea

The contributor tier is 12.5x cheaper input / 21.25x cheaper output / 75x cheaper cache read than standard slugs ($0.10/$0.20 per 1M tokens). For synthetic, riddler-encoded, non-corpus traffic it is a swarm-volume lane worth routing to — but only after the age attestation is confirmed and only with traffic that is already cleared for Meta training use (standing law: private corpus, memlang, verb genomes stay off that lane).

TESTABLE hypothesis

Completing the age attestation at settings/preferences and re-probing `meta/muse-spark-1.3-contributor` with a credited key returns HTTP 200 and a completion. Cost: ~$0.00002 per test message at contributor pricing.

EVIDENCE or OWED

EVIDENCE: live probe receipts in `watch/inbox/burn_reset_20260927/flash50/r-muse-gating.md` (403 body, endpoint topology, pricing, data-policy JSON from the contributor page), OpenRouter catalog `api/v1/models` (confirmed live, 12 ids), OpenRouter model page FAQ (contributor terms quoted). OWED: Meta's own full contributor-program terms (ai.developer.meta.com/legal/terms-of-service JS-rendered, not fetched clean), whether Meta requires any separate developer-side agreement beyond the OpenRouter data-policy choice, whether 18+ attestation stems from prior Llama license terms (search rate-limited during this ask), whether muse-spark-1.1 shares the gate (not probed live, inferred from catalog pricing).
