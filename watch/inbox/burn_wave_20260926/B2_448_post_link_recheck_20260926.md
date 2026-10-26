# B2-448 Post-link download freshness proof (2026-09-26)

## Verdict

LANDED as the named-step arm; the standing-probe arm registered as optional and deliberately NOT scheduled. Measured premise correction first: NO posted Drive link exists tonight - the B2-100 flip card is a template (its flip_executed_at and drive_file_id fields still read <FILL>), B2-23's card says "No link exists yet; operator GO required" (line 8), and no real drive.google.com/file/d/<id> URL exists anywhere in watch/inbox or memory (grep; the only hits are the template placeholders). So the brief's hazard (a posted link whose served bytes silently diverge from the shipped seal) is REAL but FUTURE: the proof point to land is the re-check step inside the flip card itself, executed by the same operator hand that does the flip. Landed: watch/inbox/burn_wave_20260926/B2_100_flip_receipt_card_20260926.md gains step 5.5 "POST-POSTING RE-CHECK (B2-448)": E5.5a anonymous curl of the posted id after the share-state change, E5.5b sha256 must print the shipped seal e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e (filed next to E4's output), E5.5c a delta hash is an INCIDENT (delete/re-upload and amend the card, never silently refresh), plus the optional weekly schtask arm documented as unscheduled with the reason (no link existed yet, measured this lane). The local zip re-verified against the seal during this lane: sha256 e9f4603a... matches (nothing touched).

## Evidence

- watch/inbox/burn_wave_20260926/B2_100_flip_receipt_card_20260926.md step 5.5 (NEW, between E5 and the E6 ledger step): the three-part re-check with the seal constant, the incident rule, and the optional standing-probe arm
- watch/inbox/burn_wave_20260926/B2_23_seed_flip_card_20260926.md:8 "No link exists yet; operator GO required" and :31 the anonymous curl shape the re-check reuses
- watch/inbox/SEED_PUBLIC_PACK_20260925.md:34-35 the shipped seal sha256 e9f4603a... (re-verified against the local zip's bytes this lane: match)
- Link-absence probe (this lane): grep drive.google.com across watch/inbox/burn_wave_20260926/*.md returns only <FILL>/<drive_file_id> template placeholders; no real file/d/<id> URL in the estate's surfaces
- watch/inbox/seed-3.2.0.zip (read for hash only, unchanged)

## Work done

Verified the hazard's preconditions before building anything: the link does not exist, so a curl re-check tonight would prove nothing and could not be filed in a flip receipt that is still a template. Chose the brief's named-step arm at the card level: the re-check is now an inseparable step of the flip receipt (E5.5a-c) with the seal constant, the one-minute settle, the incident rule, and its output location named, so the operator cannot complete the flip receipt without either filing the fresh-hash proof or recording the incident. The standing-probe arm is documented as optional/unscheduled with the honest reason. Verified the local zip still matches the seal so the card's constant is live, not historical.

## Falsifier

The step works if: after the operator flip and posting, E5.5b prints the seal and the card carries it; if the printed hash differs, E5.5c's incident rule fires and the card must name the delta. The step is dead weight if a future flip lands WITHOUT E5.5 outputs in the card - grep the completed card for "E5.5b" alongside a real hash; its absence with a filled link means the re-check was skipped and the LANDED status is unproven. The unscheduled standing probe becomes mandatory if the estate ever claims continuous proof: no schtask named in the card plus a "continuously verified" claim is a fabrication pair.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_23_seed_flip_card_20260926.md (read, unchanged); watch/inbox/burn_wave_20260926/B2_100_flip_receipt_card_20260926.md (read, edited: step 5.5 inserted); watch/inbox/SEED_PUBLIC_PACK_20260925.md (read 34-41 + tail, unchanged); watch/inbox/seed-3.2.0.zip (hash-verified, unchanged); TWO_MACHINE_SYNC_20260919.md findings via B2-23 (no Drive bridge on host); QUEUE.md (row note); memory/burns/LEDGER.jsonl (appended); watch/inbox/burn_wave_20260926/B2_448_post_link_recheck_20260926.md (this receipt).
