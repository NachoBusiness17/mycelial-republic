# B2-143 receipt (2026-09-26)

## Verdict

PARTIAL LANDED, REST OWED. The sweep ran inside a heavily throttled window (the account's web search backend returned 1302 rate-limit storms on most queries, the exact constraint the AGENTS.md fan-out width law warns about), so the census splits honestly into three bands: byte-verified live, secondary-sourced, and known-unverified/owed. ZERO cards attached, ZERO accounts created; every card-gated candidate is filed as an operator GO ask only. Rank order for estate fit: (1) Google Cloud $300 trial (verified live, biggest denominator, Vertex AI carries Gemini frontier seats), (2) Anthropic $5 trial credits (secondary-sourced, no card needed, phone only; would move anthropic off dormant-by-keylessness), (3) Cerebras card-gated developer tier (numbers unreachable live today; estate already reclassified the free lane 2026-09-26), (4) AWS/Azure/Modal/Lambda/Together/Fireworks/Mistral/DeepInfra/Novita/SiliconFlow (unverified this lane, owed), (5) no-GO row: any card-gated trial whose window dies in under 7 days regardless of size.

## Evidence file:line quotes

- configs/providers.yaml:19-21 (post-surgery bytes): "2026-09-26 roster purge (B2-61): nvidia, mistral, gemini REMOVED from the ... (nvidia 410 EOL + 404 for-account, mistral limit-0 + 403 tier,". configs/providers.yaml:28-32: "2026-09-26: cerebras REMOVED from the standing free ladder, it is a ... receipt watch/inbox/burn_wave_20260926/B2_36_cerebras_reclassify_20260926.md." configs/providers.yaml:46-51: saelis "dormant: true". configs/providers.yaml:437: gemini "dormant: true # 2026-09-26 B2-61: generation 401-dead; operator GO flips this + re-adds to routing". The estate holds 35 provider blocks (grep count of top-level two-space keys).
- GOOGLE (VERIFIED LIVE, fetched cloud.google.com/free 2026-09-26): "New customers get [$300 in free credit] to try Google Cloud products and build a proof of concept. You won't be charged until you activate your full paid account." UNREACHABLE ON PAGE: trial duration in days, card requirement, and explicit "credit applies to Vertex AI model APIs" sentence are not stated on this page (page links signup FAQs; owed). Yield estimate: $300 at Gemini-class Vertex prices (order $1-5 per MTok input) is order 60-300M input MTok-equivalents, i.e. months of specialist seat overflow. FALSIFIER for the estimate: any single Vertex billed call whose usage fields do not price in that band kills the 60-300M band; the band also dies if the trial is confirmed to exclude Vertex AI.
- ANTHROPIC (SECONDARY SOURCE, one search hit via fast.io summary of console flow; not fetched from anthropic.com directly): "New Anthropic accounts receive $5 in complimentary credits, enough for initial testing and development"; phone verification required, no card for the credits; trial credits do not count toward tier upgrades (Tier 1 needs a real $5 deposit). UNVERIFIED against vendor bytes. Yield estimate: $5 at claude-sonnet-4-20250514 input pricing (configs/providers.yaml:242-250 wires that model) is roughly 5-25M input tokens depending on hit/miss mix. FALSIFIER: console billing page showing $0 grant or a per-MTok price outside the assumed band.
- CEREBRAS (UNREACHABLE LIVE): cerebras.ai/pricing fetched 2026-09-26; the page is JS-rendered, headings present ("Cerebras Inference tier pricing", "Developer Tier Pricing") but no numbers in fetched content, and cloud.cerebras.ai requires sign-in. Community figures (about 1M tokens/day free; developer tier card-gated) are NOT quoted as facts here. The estate already reclassified the lane (B2-36 receipt). Yield estimate deferred until the pricing table is reachable. FALSIFIER: the deferred estimate does not exist yet, so its falsifier is the fetch itself: a rendered-page capture either lands numbers or closes the row.
- THE REST (OWED, named so nothing hides): AWS Activate/Bedrock, Azure free/trial, Modal (monthly free credits), Lambda cloud trial, Together, Fireworks, DeepInfra, Novita, SiliconFlow, SambaNova. None fetched today (search backend 429-throttled); none carry a yield estimate here because an unfetched estimate would be fabricated denominator. DeepSeek carries no known trial (both estate deepseek lanes are paid-key lanes, providers.yaml:310-366).

## Work done

1. Read the estate roster and purge receipts from providers.yaml bytes so the census starts from what is actually wired.
2. Fetched cloud.google.com/free and cerebras.ai/pricing live; captured exact quoted sentences and named exactly what each page does not state.
3. Ran the card-trial search sweep; hit the account's 1302 rate-limit storms on most queries (receipt-named constraint); kept the single usable secondary hit for Anthropic clearly marked secondary.
4. Ranked candidates by estate fit and filed per-estimate falsifiers; registered the unverified remainder as owed instead of inventing numbers; attached no cards, created no accounts (the brief's operator-GO gate).

## Falsifier

Per-estimate falsifiers are inline above (Google band, Anthropic grant, Cerebras deferred-fetch). Whole-verdict falsifier: any lane that attaches a card without an operator GO line in this file or QUEUE.md falsifies this receipt's compliance claim. The Google $300 quote falsifies if the live page drops the quoted sentence on refetch; the Anthropic $5 falsifies against console.anthropic.com bytes directly.

## Bibliography closed

- configs/providers.yaml lines 19-32, 46-51, 242-250, 310-366, 437, 638-655 (roster + purge receipts)
- https://cloud.google.com/free (fetched 2026-09-26, quotes verbatim)
- https://www.cerebras.ai/pricing (fetched 2026-09-26, JS-rendered, numbers unreachable)
- watch/inbox/burn_wave_20260926/B2_36_cerebras_reclassify_20260926.md (referenced by providers.yaml)
- Search hits via the throttled backend: fast.io summary for Anthropic console credits (secondary, unverified against vendor)
- Owed: AWS/Azure/Modal/Lambda/Together/Fireworks/DeepInfra/Novita/SiliconFlow/SambaNova vendor-page fetches; Google trial FAQ (duration + card); anthropic.com trial policy page
