# GATE DIGEST: operator gates at one glance

Generated 2026-10-04 04:43 by `tools/gate_digest.py` (byte scan of receipts, mtimes,
configs; never hand-edit this file, regenerate it).

**OPEN 5 / CLOSED 1. Oldest open: Adam invite to the-mountain (no GitHub username) (3d 23h)**

## Open gates (each row is ONE operator action)

| # | Gate | Open for | Why blocked | The ONE action | Birth receipt |
|---|------|----------|-------------|----------------|---------------|
| 1 | Adam invite to the-mountain (no GitHub username) | 3d 23h | No GitHub username for Adam exists in the estate; both handle guesses (AdamCrigler, ItsCommodore) 404. An invite to a guessed handle would grant a possible stranger push access. Onboarding lineage since 09-24. | Ask Adam on Discord (ItsCommodore) for his GitHub username, verify it (gh api users/NAME), then: gh api -X PUT repos/NachoBusiness17/the-mountain/collaborators/NAME -f permission=push | `watch/inbox/last_mile_20260930/LW2_ADAM_INVITE.md` |
| 2 | ZAI_Pro key rotation (rides with the other 6 leaked keys) | 3d 20h | Seven live keys, incl. ZAI_API_KEY_Pro, were exposed in the steps.jsonl leak (audit finding #1); the on-disk leak copy persists and the backup repo holds copies. AG1 containment (untrack, redaction, pre-commit gate) protects future rows only; provider-side rotation is the operator-only real fix. | Rotate ZAI_API_KEY_Pro at the provider console and replace the value in .env; same for ALIBABA x2, VERCEL_KEY, HERMES x1/2, GROQ (audit finding #1) | `watch/inbox/last_mile_20260930/AG1_SECRETS_CONTAINMENT.md` |
| 3 | Nous portal check (402s vs ~$171 rib arithmetic) | 3d 14h | Prime models 402 on reservation while ribs say ~$171 of the $180/$220 pool should remain; the API has no balance endpoint. Only the portal separates old-account-402 from a genuinely dry pool. | Log into portal.nousresearch.com, read credits + top-up history for BOTH key pairs (repo .env pair, old SDD/NACHO pair) against the COST_TRUTH section 4 table; top up if dry | `watch/inbox/last_mile_20260930/AJ9_NOUS_402.md` |
| 4 | Offsite backup medium pick | 3d 15h | Design + script complete (restic, scripts/backup_offsite.ps1), no medium chosen. One disk holds the estate, its only remote, and the gitignored truth core; audit row 18 FAIL stands until a restore passes. | Pick ONE medium (B USB SSD ~$70-110 / C laptop over Tailscale, $0, off-machine today / D Backblaze B2, cents per month; OFFSITE plan section 4) and run the 3 commands in section 7 | `watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md` |
| 5 | Verkle v2 flip (chain_mode v1 to v2) | 3d 14h | GO recommended (471x to 1,800x less write amplification); all three preconditions landed green (B8: compaction guard, reader dedupe, AH19 family). Waiting on the operator's quiet window; never mid-day. | At the next quiet window run VERKLE_V2_DECISION section 4 recipe: pre-flip seal, flip configs/mag.yaml chain_mode to v2, one real save, post-flip seal, addendum filled | `watch/inbox/VERKLE_V2_DECISION.md` |

## Closed (kept visible)

| Gate | How it closed |
|------|---------------|
| Phase-2 lensing GO | lensing returned; receipt watch/inbox/mountain_climb/THE_LENSING.md landed |

## Live byte checks run this pass

- adam-invite: OPEN (no close receipt found)
- key-rotation: OPEN (live ZAI_API_KEY_Pro value still byte-present in the on-disk leak copy memory/trajectory/steps.jsonl (unrotated, checked this run))
- nous-portal: OPEN (no close receipt found)
- offsite-medium: OPEN (no close receipt found)
- verkle-v2-flip: OPEN (configs/mag.yaml reads chain_mode: v1 (checked this run))
- phase2-lensing-go: CLOSED (lensing returned; receipt watch/inbox/mountain_climb/THE_LENSING.md landed)

## How a row closes (the law)

1. Byte probe flips it (config flag read, leaked-value match, landed
   return file). No human filing needed.
2. A receipt lands: any .md under watch/inbox, NEWER than the gate's
   birth receipt, containing the line `GATE-CLOSED: <slug>` with the
   slug from this table: adam-invite, nous-portal, key-rotation, phase2-lensing-go, verkle-v2-flip, offsite-medium.

Days-open is anchored to each birth receipt's file mtime (named per
row). Counts are snapshots of one scan moment (census denominator law).
