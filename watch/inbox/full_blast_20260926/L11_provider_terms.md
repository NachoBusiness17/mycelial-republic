# L11: six-provider free-terms probe (agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L11) · **Class:** RECEIPT / scout
**Method note:** search hard-429/1302 on all queries; banked via direct page fetches. [V] = verified from live pages today, [U] = prior knowledge, stale until probed.

## Verdicts

| Provider | Verdict | Terms shape |
|---|---|---|
| SiliconFlow (.com) | **PROBE** (rank 1) | OpenAI-compatible, key from console, no card in quickstart [V]; per-model usage caps published on Models pages [V]; ToS current as of 2026-09-09 [V]; free-SKU list + limits [U], verify post-signup |
| llm7.io | **PROBE** (rank 2, liveness-only) | Keyless open catalog [V], key needed for inference; catalog now carries PAID SKUs too (gpt-5.6-luna $0.12/$0.28, claude-opus-5 $2.50/$10 per 1M) so blanket-free assumption is dead [V]; RPM/RPD caps unpublished, no ToS page reachable, every `owned_by` an empty string [V]: opaque operator, treat as promo-grade, never load-bearing |
| Chutes.ai | **PROBE** (rank 3) | Real endpoint `llm.chutes.ai/v1` Bearer auth [V]; Bittensor miner-hosted fleet, TAO wallets, per-token pay-go from ~$0.0245/$0.0978 per 1M (Mistral-Nemo) up to DeepSeek-V3.2 $1/$1 [V]; failed requests not billed [V]; legacy 200-300 free/day [U] unconfirmed on FAQ |
| Featherless | **PASS** | NOT free: Chat $25/mo flat (32K ctx) or Developer $50/mo prepaid credits at the catalog's $0.1/0.2 per 1M [V]; and the Chat tier explicitly bans "app/API traffic, background automation, or benchmarking" with cancellation-without-refund [V]: an automated harness is the literally prohibited pattern |
| Scaleway | **PASS** | Free-beta era over; now paid per-token "LaaS" [U], docs reorganized and unreachable, cloud account wants a card [U] |
| Lightning AI | **PASS** | GPU-credits platform, not an OpenAI-compatible inference edge; no inference API found [V of the gap] |

## Cross-cutting ToS intel for the harness

(a) Featherless' written automation ban proves subscription vendors actively scan for automated use; fetch SiliconFlow's Sep 2026 ToS automation language before signup. (b) llm7's empty ownership + absent ToS = no contractual protection: cap at liveness-only use. (c) Chutes' miner-hosted fleet means per-chute availability variance: fine for probes, wrong for anything stateful. (d) OmniRoute's L01 warning-list entry for chutes ("no free tier") now looks stale or tier-confused vs Chutes' own pricing page; note the disagreement, probe decides.

## Net for the lane ladder

Three PROBEs (SiliconFlow, llm7, Chutes) all require keys/signup, so nothing enters providers.yaml at this seat: probe results land as scout receipts and promotion stays operator-gated. LLM7's DeepSeek-V4-Flash pricing from L00 stays the interesting cheap-lane candidate independent of free tier.
