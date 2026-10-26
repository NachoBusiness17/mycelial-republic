# COST_TRUTH_20260930 — the $135.71 rollup reconciled (2026-09-30)

Fence owner: this seat. Files owned: this receipt only (read-only over `tools/cost_rollup.py`
surfaces, `training/cost_ledger.jsonl`, `memory/frontier/allowance.jsonl`, ribs, last-mile receipts).
Instruments named per the ONE-BUG LAW: rollup run `2026-09-30T18:53:50Z`; raw-byte sums beside it.

## 0) The headline question: is $135.7095 / 25,376 calls lifetime?

**Yes — lifetime, and already stale.** The IMP5 figure (17:41Z) covered all four surfaces from
2026-08-05 onward. Fresh run 18:53Z: **$135.8840 over 25,406 calls** (duels 73 rows, mates 2 files,
gopher 3 files, ledger 2439 rows / 1801 cost rows; unparseable: none). Composition: the ledger's
$128.06 (94%) is the Aug–Sep DeepSeek-account era (peaks 08-09 $34.31, 09-22 $23.89, 08-30 $21.22);
**all Nous-model spend is $9.05 lifetime, all of it since 2026-09-29.**

The rollup also undercounts: it scans only the four surfaces. Receipt-side burns with raw files
elsewhere add **$1.2208 today** (opus refires $1.0618, V2 grok $0.1463, V3 $0.0123, AJ9 probes
~$0.00003). **True lifetime ≈ $137.10; true today = $7.47** (below).

## 1) Today (2026-09-30), by bytes

In-rollup $6.2457 + receipt-side $1.2208 = **$7.4665 today**.

### By surface/series (duels all carry row ts; 73/73 rows are today, 00:25Z–18:21Z)

| series | wave home | rows | usd |
|---|---|---|---|
| v1mf-* | V1/V8 multifamily duel | 18 | 1.7953 |
| lw9-* | LW9 duel N30 | 9 | 1.1173 |
| z2-* | hydrology Z2 (gap-5, 09-29 start) | 10 | 1.0681 |
| x4-* | hydrology X4 (gap-5, 09-29/30) | 10 | 0.9623 |
| w8-* (incl AJ1 altjudge re-judges $0.1246) | W8 + AJ1 | 22 | 0.4693 |
| retro-g1-vs-g3-* | duel retro baseline | 2 | 0.2300 |
| ah10-* | **AH** (AH10 GLM-vs-DS) | 2 | 0.0972 |
| mates night_burn N1–N6 | **B** (burn) | 6 | 0.2725 |
| ledger deepseek (DeepSeek acct, orc graph jobs 02:43–12:49Z) | wave-untagged | 602 calls | 0.2337 |
| W4 opus whole-response (empty content) + AA1a3 opus stream | W4/AA1 refire | 2 | 1.0618 |
| V2 grok-4.7 (Nous host, pinned) | V2 | 3 | 0.1463 |
| V3 deepseek-v4.1-flash on Nous | V3 | — | 0.0123 |
| AJ9 probes (2 billable x 10 tok) | **AJ** | — | ~0.00003 |

### The mission's named waves specifically

| wave | metered spend today | where |
|---|---|---|
| AC / AD / AE / AF / AG / AI / IMP / LM | **$0.00** | seat lanes on THIS account (subscription tokens, no local meter); LM1's Nous escalation 402'd → landed $0 |
| AH | $0.0972 | AH10 duel pair; rest of AH was seat-side |
| AJ | $0.1246 + ~$0.00003 | AJ1 altjudge (inside w8 rows) + AJ9 probes |
| B (burn) | $0.2725 | night burn N1–N6; gopher burn $1.7910 is file-dated 09-29 (receipt says 09-29/30 — filename-dated, see unknowns) |
| **named-waves subtotal** | **≈ $0.4942 (6.6% of today)** | the other 93% rode lanes outside the named list (hydrology duels, V1MF, W8, opus refires, V2/V3) |

### By provider (Nous vs this account vs DeepSeek)

| provider | today | note |
|---|---|---|
| **Nous credits** | **$7.2325** | duels 5.7395 + night burn 0.2725 + opus 1.0618 + V2 0.1463 + V3 0.0123 + probes; every driver pins inference-api.nousresearch.com |
| **DeepSeek account** (not Nous) | $0.2337 | 602 calls, ledger orc sessions; per DRIVING_LADDER DeepSeek is off the funded rung but the account still meters |
| **THIS account** (ZCode subscription, the AC..IMP seat lanes + this reconciliation) | **$0 metered anywhere local** | subscription tokens have no local instrument at all |

## 2) Nous credits: ribs vs the 402 floor

- **2026-09-09:** $220 armed (LAW-11 `memory/continuity/seat_memory_20260927/law-11-credits-over-failure.md`; 2026-09-14 audit confirms "dispatch log active through 2026-09-09, $220 armed budget").
- **2026-09-28:** RIB_DRIVING_LADDER_20260928 names **$180** as the funded tier.
- **Visible Nous burn in every local surface, ever:** 09-29 $1.8101 + 09-30 $7.2325 = **$9.0426**. Zero Nous rows exist before 09-29.
- **Per the ribs, what SHOULD remain:** $180 − $9.04 = **~$170.96** (or ~$210.96 if $220 still held).
- **The 402 finding says otherwise:** LM1 (09-30, after 17:37Z) got HTTP 402 "Insufficient available credits" on BOTH prime models, even a 64-token reservation — implausible against a ~$171 pool. Yet the SAME DAY, after that: AJ1 probe 200 ($0.000016), V3 200, W4/AA1 opus 200 ($1.06 burned). Two live hypotheses the bytes cannot separate: (a) LM1's failover chain rode the pre-rotation hermes-env pair (AJ9 proved hermes `.env` carries the OLD keys; NACHO 401-dead, old SDD alive) so the 402 describes the OLD account's pool; (b) the repo-pair pool is genuinely near-empty and only tiny/cheap reservations squeak under a floor. **The portal is the only instrument that decides.**

## 3) Honest unknowns, each with the instrument that closes it

| # | unknown | closing instrument |
|---|---|---|
| 1 | Actual Nous credit balance, per account (repo pair vs old SDD/NACHO pair) | **Operator at https://portal.nousresearch.com** — API has no balance endpoint (AJ9: /v1/credits,/v1/usage,/v1/key all 404) |
| 2 | The $220→$180 delta ($40): no surface records ANY Nous burn 09-09..09-28; un-logged hermes dispatches, a re-arm, or a wrong figure | portal transaction/top-up history |
| 3 | Server-side cost of the 3 AA1 client-timeout opus attempts (1800s/1800s/3600s) metered $0 locally | portal usage ledger vs local receipts |
| 4 | THIS account's subscription token burn (the seat waves) — no local meter exists | ZCode account usage UI (operator side); locally unclosable |
| 5 | Wave split of today's $0.2337 DeepSeek-account ledger burn: cost_ledger.v1 has no wave/corr tag (duels got corr_id via AH14; the ledger never did) | add corr_id to cost_ledger.v1 |
| 6 | mates/gopher day attribution is filename-based (a renamed file re-dates rows); gopher receipt says 09-29/30 but all 18 rows file-date 09-29 | row-level ts in burn drivers |
| 7 | Hand-written totals vs bytes: NIGHT_BURN header says "$0.41 total", row bytes sum **$0.2725** | cost_rollup.py (now landed) is the single source; never trust a hand-sum |
| 8 | allowance.jsonl — the "quota organ" — is NOT a quota organ: 531 rows of `frontier_council.v1` (surface, goal, ts; chatgpt 291 / grok_web 232 / deepseek 8, 2026-08-14→09-30). It logs free-lane STEER goals, carries **zero numeric quotas, zero Nous rows** | a real credit-balance log fed from the portal (manual operator entry), or accept the portal IS the organ |

## 4) Operator portal check table (both Nous accounts)

Check at https://portal.nousresearch.com — once for the repo-key account (`.env` HERMES_API_KEY_1/2), once for the old-key account (hermes `.env` NOUS_SDD/NOUS_NACHO):

| portal field | local bytes say | rib arithmetic says | verdict you are checking |
|---|---|---|---|
| credits remaining (new-key acct) | 402s on prime reservations today, yet $1.06 opus + probes passed after | should be ~$171 if the 09-28 $180 was real | near-empty ⇒ ribs' $180 was never the balance; ~$171 ⇒ 402 was the old account |
| credits remaining (old-key acct) | NACHO key 401-dead; old SDD 200-alive | unknown | is LM1's 402 this account? |
| spend 2026-09-29 | $1.8101 | — | matches ⇒ local Nous metering is complete for that day |
| spend 2026-09-30 | $7.2325 | — | matches ⇒ metering complete; higher ⇒ un-logged burn exists (timeout server-side, hermes dispatches) |
| top-up history | — | $220 armed 09-09; $180 cited 09-28 | was either figure ever portal-true? |

## 5) One-line truth

**Today cost $7.47 all-in ($7.23 Nous + $0.24 DeepSeek acct + $0 this-account-seat); the named AC..B waves metered only ~$0.49 of it; lifetime is $135.88 in-rollup / ~$137.10 true; the ribs say ~$171 Nous should remain, the 402s say near-empty, and only the portal can say which — the local estate has never once measured the balance it budgets against.**
