# GSTD official site delta - gstdtoken.com/docs dropped 2026-10-09

**Fetched:** 2026-10-09 (sitemap lastmod 2026-10-09T22:57Z - the site updated TODAY, mid-sitting). Raw HTML + extracted text banked in this folder. Docs hub carries 14 section cards (overview/architecture/node/compute/inference/payments/rewards/verification/treasury/token/security/api/developers/faq) but ALL section routes 404 - cards only, content not yet published. Live pages: /token /roadmap /advantages /about /buy /legal.

## New facts vs the estate's holdings (738-file analysis + dogfood + node-live)

| Fact | Value | Status vs our holdings |
|---|---|---|
| Canonical domain | gstdtoken.com (RU-first, /en 404s for docs) | NEW - we held github gstdcoin + telegram only |
| Token contract | EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO | NEW verbatim bank |
| Supply | 1,000,000,000 GSTD, fixed, admin key BURNED | NEW (fixed supply + burned admin) |
| Distribution | community 40% / liquidity 30% / team 20% / treasury 10% | NEW |
| Fee split | 85% node / 10% treasury / 5% buyback+burn, settled by SettlementMaster.tact ON TON MAINNET | CONFIRMS split shape; mainnet-working status NEW |
| Hardware tiers | Spark / Flame / Storm / Titan / Sovereign | NEW names; our node-live tier "gstd"/sovereignty=true now maps to Sovereign tier |
| Node client | 8 inference models baked in, one-line installer | matches our 16-capability census (15 ours) |
| Result signing | Ed25519 signature on submission = attribution only; correctness proof explicitly ABSENT, honest caveat repeated on 3 pages | CONFIRMS our audit finding, now network-official language |
| Fine-tuning | distributed LoRA pipeline live via nodes, real adapters trained end-to-end, base-model coverage limited | NEW status |
| GOLD RESERVE | treasury gold-reserve contract WRITTEN but not deployed, not audited; potential XAUt distribution; today's treasury holds only TON | NEW - the big one, see below |
| Bridge | Solana + XRPL cross-chain = open code, no working vault on either chain, never moved funds, audit mandatory - "consider it non-working" | CONFIRMS + strengthens our bridge risk row (B2-479 class); our forgeable-vote finding stands |
| Compliance posture | "no APY, no yield promises, utility not investment" repeated | NEW posture language |

## The convergence finding (this sitting's book + this drop)

The operator dropped the New Money Revolution reset book this morning; its core is the asset-dollar chartalist loop (Treasury issues against gold; taxes/fees retire tokens and create demand). GSTD's live design is the SAME LOOP at protocol scale: 85/10/5 fee split with 5% buyback-and-burn = retirement-by-usage creating demand, and a written-but-undeployed GOLD RESERVE contract (XAUt) for the treasury. The network's honest-verification posture (signed-not-proven) also mirrors the estate's two-tier-truth keystone: cheap local tier does the work, expensive settlement tier proves what matters when it matters.

Estate mapping: GSTD is building the book's asset-dollar thesis as permissionless software. Our incorporation draft's verification-gap chapter should cite the site's own words now (attribution-signed, correctness-unproven).

## Actions queued

1. Point GSTD_INCORPORATION_DRAFT.md + GSTD_DOGFOOD_PLAN.md citations at the official site language (contract address, 85/10/5, bridge non-working warning) - citation lint will verify
2. Our public PR lane (gstd-upstream-prs memory): the bridge warning language on-site strengthens the tasks/push-auth PR framing
3. Token contract address banked for the treasury/tier checks in the next dogfood round (read-only chain queries)
4. Watch /docs section pages going live (all 404 today) - the verification + payments sections are the two our audit most wants
