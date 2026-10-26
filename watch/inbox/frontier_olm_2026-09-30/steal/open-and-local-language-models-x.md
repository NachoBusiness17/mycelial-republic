# Steal card: open-and-local-language-models-x (2026-09-30, rev 2)

## The find (verified)

"GLM-5.3-Flash is 100% FREE with UNLIMITED usage right now on ZCode (Extended)" - @nahid_pro09,
2026-09-22, https://x.com/nahid_pro09/status/2102229686378213649. fxtwitter fetch (this session and
the round-1 session) confirms: Z.ai extended the GLM coding plan promotion through October 7;
unlimited GLM-5.3-Flash on the ZCode harness during promotional hours; 2x quota on other coding
harnesses; original end was Sep 20. It is a promotional post, not an official z.ai page (OWED-1:
the extended window's hour shape is not named in the tweet; OWED-4: the verbatim line was confirmed
element-wise via a faithful fetch summary, not a byte diff). New to holdings: the tweet ID appears
in exactly two files, both today's mine (`rg 2102229686378213649 watch/inbox memory` = sweep + this
steal card only), and "October 7" has zero hits in memory/doctrine/scorecard_latest.json and
memory/doctrine/LEDGER.jsonl (`rg -c "[Oo]ctober 7|Oct 7"` = 0, exact regex).

## What the estate already holds

- `watch/inbox/frontier_olm_2026-09-30/lens/burns.md:57-59`: free-class 4 to 3, "GLM-5.3-Flash
  dropped", DeepSeek 401-alive, Lightning FULLY DEAD. burns.md states the drop, not the reason; that
  the drop presupposed the Sep 20 window end is THIS CARD'S INFERENCE, independently supported by
  the tweet naming Sep 20 as the original end (not a citation of intent).
- `memory/thinking/app_reasoning.jsonl:4709` (row ts 2026-09-03T15:27:48Z, provider
  builtin:zai-coding-plan, model GLM-5.3-Flash, cost 0): the full Sep 3-20 campaign spec (23:00-09:00
  SGT daily, zero quota via ZCode, 2x via other agents) plus the wiring plan.
- Catalog hits: the find metadata said 29. This session: `rg -c "GLM-5\.3-Flash" catalog/catalog.jsonl`
  = 13, `rg -i -c` = 28; the round-2 reviewer's `rg -i -o | wc -l` = 30. The sweep's 29 is
  unreconciled in either direction (OWED-2); the overlap-in-kind claim stands on 28-30 hits.

## The steal (mechanism): a date-guarded free-rung lane, LATENT not bleeding

The hour half of the Sep 3-20 wiring landed as code: `watch/salon_runner.py:242-246` defines
`_in_campaign_window()` checking ONLY the SGT hour (`sgt_hour >= 23 or sgt_hour < 9`), docstring
claiming "Sep 3-20 2026"; `:249-252` `_campaign_fold()` rides https://api.z.ai/api/coding/paas/v4
with ZAI_API_KEY_Pro and glm-5.3-flash; `:255` FOLD_LANES prepends the lane when in-window (note:
module-level, evaluated at import time - fine for CLI-per-run; `mag/kabuki_salon.py:55` loads the
module by path via spec_from_file_location, so any long-lived importer freezes the window at its
import moment). The hour half landed 2026-09-14 (`git log -S "_in_campaign_window" -- watch/salon_runner.py`
= 60b1bde7f, mid-campaign).

The defect is a MISSING DATE GUARD, and it is LATENT, not bleeding. No receipt shows the lane ever
fired: `rg -c '"lane": "zai-campaign"' memory/runs/trajectory/steps.jsonl` = 0 rows ever; the seal
stream is frozen (mtime 2026-09-09 13:28 EDT, 136,202 B; last row ts 2026-09-09T17:28:33Z, itself a
fold row; last fold rows read 2026-09-07). `_seal` is fail-open (salon_runner.py:397), so absence
is not absolute proof, but there is zero positive evidence of firing. The correct claim: the lane
is ARMED whenever a fold next runs, and it will ride a promo that expired Sep 20 unless the guard
gains a date half first.

Port move, three edits, all in `watch/salon_runner.py`:

1. Date guard with BOTH boundaries named. The hour check stays SGT (as today, :245); the new date
   range must be SGT too, or window edges shift a day across timezones. End = 2026-10-07 SGT (the
   tweet's extension date). Start: the conservative landing is deploy day; 2026-09-03 SGT (the
   evidenced original start, app_reasoning.jsonl:4709) is valid ONLY IF continuity between the two
   promo windows is verified (OWED-3, unverified). Do not bake an invented boundary into code.
   Fix comment notes the import-time evaluation hazard (above) per the fix-comment-carries-receipt
   law.
2. Docstring re-point to the extended window with its source (tweet URL + fetched date).
3. NEW banking code in the runner (not a pattern repeat): today's `_seal` rows (:407-415) carry
   kind/salon/brief_sha/shape/lane plus chars/survived/duration_s but NO provider, model, cost, or
   API-call ts, and zero `"provider": "zai-campaign"` rows exist anywhere in the repo (rg = 0 this
   session). The Sep 3-20 cost-0 rows landed in app_reasoning.jsonl via the seat harness
   (builtin:zai-coding-plan), not via salon_runner. Edit 3 therefore adds provider/model/cost (or a
   side receipt row) to the fold seal as NEW code so the window's banked usage is auditable after
   expiry.

Standing constraint (one explicit sentence): the driving ladder confines free lanes to SENSING -
outputs "SENSED, never trusted, bank as findings, never as done-work" and "sensing may feed
judgment, but sensing is never substituted for it" (memory/rib/RIB_DRIVING_LADDER_20260928.md,
invariant 2; corroborated by AGENTS.md driving ladder). The fold prompt this lane answers is
judgment-shaped (VERDICT/COLLISIONS/BUILD ORDER/POSTRUN, salon_runner.py:458-464), so the lane
rides ONLY as candidate-generation: its fold text is banked as findings, never done/trusted, and
any verdict that must bind climbs to the funded tier (Nous glm-5.3-prime or grok-4.7).

Economics, stated exactly: dollar-cost is zero (inside the paid coding-plan subscription); quota
cost is NOT zero. Unlimited applies on the ZCode harness; salon_runner's direct api.z.ai
coding-endpoint call is an "other harness" per the tweet and consumes 2x quota per ask. The
20-ask falsifier below is exactly the quota-cap test.

Reach, scoped: FOLD_LANES has exactly one consumer, the fold loop at salon_runner.py:465-475 (first
lane whose text survives the gate floor becomes the fold verdict). `rg -l "FOLD_LANES" -g "*.py"` =
watch/salon_runner.py only. No drain worker inherits this lane today; if the drain lanes want it,
that is a separate wiring ask.

## Estate map

- **Water graph (fuel/economics)**: burns.md:57-59 dropped the rung from the free class; the dated
  re-entry restores it through Oct 7 at $0 cash and 2x coding-plan quota per ask, without loosening
  the funded ladder (rib invariant 1 + the SPEND addendum name Nous glm-5.3-prime and grok-4.7 as
  the funded judgment tier).
- **Gopher fleet / fold lanes**: the port site is salon_runner.py:242-256; one consumer (:465).
  Fleet drains are not wired to FOLD_LANES and are not claimed as such.
- **Percolator**: in-window fold output feeds candidate generation at sensing tier, banked as
  findings, exactly the pattern the rib's invariant 2 prescribes; the Sep 3-20 precedent
  (app_reasoning.jsonl:4709) shows the window wiring survived one full campaign.
- **Sovereign mirror**: app_reasoning.jsonl:662 holds cost 0 with cache read 721,472 tokens on the
  coding-plan lane; in-window economics can budget off that row (dollar-zero, quota-metered).
- Not fed this round: quantizer, context pack (no mechanism here touches them; stated rather than
  stretched).

## Falsifiable probe (cheap, this week)

One tiny salon fold ask through the zai-campaign lane at the next in-window slot (23:00 SGT
tonight; UTC 2026-10-01T01:17Z read this session = SGT hour 9, just outside; well before Oct 7).
Credential present: `rg -c "^ZAI_API_KEY_Pro=" .env` = 1 (name-only check, value never printed).
Outcomes: (a) 200 at $0 with 2x-quota accounting confirms the extension for the estate's credential
and settles OWED-1 by recording which hours the endpoint actually honors; (b) 401/429 or a billed
call falsifies the free claim for estate load; (c) 20 consecutive in-window asks hitting a usage
cap falsifies "unlimited" for estate-shaped load. Fold output is banked as sensing-tier findings
only, per the constraint above.

## Receipts (this session)

- fxtwitter fetch of api.fxtwitter.com/nahid_pro09/status/2102229686378213649 (round 1 and
  re-confirmed by the round-2 reviewer's own fetch).
- Reads: salon_runner.py:242-256, :393-422, :455-475; mag/kabuki_salon.py:49-55,116;
  memory/rib/RIB_DRIVING_LADDER_20260928.md (whole, 4,195 B, mtime Sep 29); lens/burns.md:45-74;
  app_reasoning.jsonl:4709, :662.
- Ran: rg counts for "lane": "zai-campaign" (= 0), "kind": "fold" tail (last ts 2026-09-07/09),
  stat on steps.jsonl (frozen 2026-09-09 13:28 EDT), rg -l FOLD_LANES (= one file), rg -c
  '"provider": "zai-campaign"' (= 0), git log -S "_in_campaign_window" (= 60b1bde7f, 2026-09-14),
  rg for the tweet ID (= today's mine only), rg Oct-7 in doctrine (= 0), rg "^ZAI_API_KEY_Pro="
  .env (= 1), date -u (= 2026-10-01T01:17Z, SGT hour 9), rg -c GLM-5.3-Flash catalog (= 13 / 28 -i).

## OWED

- OWED-1: extended-window hour shape (tweet says "promotional hours" without naming them; 23:00-09:00
  SGT is proven only for Sep 3-20, app_reasoning.jsonl:4709). The probe settles it.
- OWED-2: the sweep's "29 catalog hits" instrument unreconciled (13 case-sensitive lines / 28 -i
  lines / 30 -o occurrences across two sessions' instruments).
- OWED-3: continuity between the Sep 3-20 window and the Oct 7 extension (no official z.ai page
  fetched; the tweet asserts the extension).
- OWED-4: verbatim tweet line not byte-diffed; elements confirmed via faithful fxtwitter summary.
