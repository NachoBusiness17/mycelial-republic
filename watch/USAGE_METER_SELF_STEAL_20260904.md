# USAGE METER SELF-STEAL — 2026-09-04 (the seat's own meter, never read, 2.84B tok)

**Operator trigger:** "why are we even using 5.3 when FLASH IS FREE?" → debug → "find out what it is doing and do a salon on it. Where else is this happening?"
**Tri-state:** every number below SUPPORTED by direct query of `~/.zcode/cli/db/db.sqlite` (tables `model_usage`, `turn_usage`, `session`) — the data behind the ZCode usage tab. This file is the first fleet document to read it.

## THE FINDING (one screen)

- **The seat burned 2.84B tokens in 10 days; the single biggest burner was a zombie heartbeat.**
- Automation `e2c00e27` ("Sancho tick v.2.1", */10 * * * *) fired **939 times** into session `sess_dddf6069` (born Aug 25, **pinned to paid GLM-5.3-full**).
- **1,296 of 2,609 premium turns output <200 tokens** ("nothing to do, exiting") and still re-fed ~95K context each: **740M tokens of no-op** on the paid meter. Real work: 108 turns / 35M tok. **82 compactions.**
- Useful output: **11 posts, all Aug 27–28.** Seven days of silent paid heartbeat after.
- Free 5.3-flash existed throughout (promo 11AM–9PM + night window 23:00–09:00). Config default was switched to Flash Sep 3 — **but the old session kept its birth model.**
- Useful-output ratio ≈ **7e-7** (deepseek chair's arithmetic). Any sane kill line is 1e-2.

## WHERE ELSE IT IS HAPPENING (measured, same db)

| Surface | Verdict | Evidence |
|---|---|---|
| Tick `e2c00e27` + session `dddf` | THE zombie (1.27B tok premium) | 939 runs, 11 posts ever, 82 compacts |
| Subagent model inheritance | REAL, small so far | Economist spawn rode 5.3-full (727K) while 60+ subagents from flash sessions rode flash — children inherit the parent session's model |
| Other interactive premium sessions | legit judgment seat, watch | caa41b99 53.7M, fc71a008 36.6M, 10fe54a8 10M lifetime (operator windows incl. this one) |
| Night-shift / night-wheel automations | CLEAN | fired in flash sessions, $0 class, room rows filed |
| Compaction churn | structural | 82 on the zombie; every long-lived premium session pays compounding re-feed interest |

Not in this db (separate ledgers, already audited or out of scope): bay API keys (Economist 12% report), claude-zai door (2.2MB, pennies).

## THE LAWS (salon verdict — groq + cerebras + deepseek-pro witnesses, $0)

1. **OUTPUT-RATIO LAW** — retire automation/session when useful-output ÷ billed-tokens < 0.01 over 24h rolling. (Would have killed the tick on day one.)
2. **MODEL-PIN ISOLATION** — subagents never inherit premium pins; cheapest capable default.
3. **CONTEXT-DEBT LAW** — compaction + re-feed ≤ 3× peak useful output; retire beyond.
4. **HEARTBEAT-THROTTLE LAW** — heartbeats are budgeted burns; "exit fast" is not free when context re-feed dominates.
5. **MODEL-PIN EXPIRY** (deepseek) — premium pin >72h without a completed task ⇒ auto-demote.

**The deep law: no surface ever compared BURN to OUTPUT.** The meter existed per-turn on disk the whole time; nothing queried it. Fix = nightly usage-db sweep as a fleet organ (one SELECT), retire-by-ratio.

## ACTIONS

- **PENDING OPERATOR GO:** disable `automation-e2c00e27` (spend-class). Rebuild, if wanted: hourly, fresh flash session, output-ratio-guarded.
- Adopted same-turn by this seat: no bulk subagent spawns from premium sessions; bulk → flash/free lanes; new sessions default Flash.
- Falsifier: in 7 days, premium no-op turns must be <1% of premium burn, else theater.

Fold + witnesses: memory/runs/salons/usage_meter_salon_20260904/SALON_ARTIFACT.md
