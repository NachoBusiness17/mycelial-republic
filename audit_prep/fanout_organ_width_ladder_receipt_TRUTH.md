## Finding — what your cell yields
The fanout_organ's width ladder claim is FALSIFIED. The audit_prep/fanout_organ_width_ladder_receipt.md documents a progression from 2 to 480 lanes with specific pack files, but ALL claimed pack files are missing. The organ itself (mag/fanout.py) is secure, but the scaling evidence is fabricated.

## Evidence — what in the repo supports it (file/shape, no invention)
- mag/fanout.py (107 lines): Single-file stdin/stdout organ with security intact
- audit_prep/fanout_organ_width_ladder_receipt.md: Claims 9 specific pack files as width ladder rungs
- ALL 9 claimed pack files MISSING: p3_mud_20260912.json, p6_ractor_game_20260912.json, p8_adam_onboard_20260912.json, p20_clarkes_end_20260912.json, p40_loom_iter_20260912.json, p80_loom3_20260912.json, p160_matthew_20260913.json, p320_matthew_ds_20260913.json, p160_loom3_ds_20260912.json
- HOST_ALLOW enforcement secure: Line 39, 45, 59 with guarded fetch (lines 41-54)
- Output contract intact: ===FANOUTJSON=== marker at line 102

## Risk if wrong — what the audit breaks on if this is missed
The entire 480-wide scaling claim is built on fabricated evidence. Matthew Steiniger will detect the missing pack files immediately and reject the entropy-minimization narrative (EUT frame). The hard-reproducibility claim collapses when receipts don't exist. The "CODE ONCE, PACKS ARE DATA" invariant appears hollow without the width ladder proof.

## The act — the concrete prep step (file/spec/number)
Create audit_prep/fanout_organ_width_ladder_receipt_TRUTH.md containing:
1. Admission: All 9 claimed pack files missing - width ladder claim falsified
2. Evidence: List existing fanout.py security features that ARE valid
3. Redefine claim: "fanout_organ works for N≤4, unverified for N>4" 
4. Document the fabrication pattern in audit_prep/ for transparency
5. Remove falsified width ladder claims from all audit documentation

## Falsifier — what would prove this wrong
- Any of the 9 missing pack files found in the repository
- Successful fanout_organ execution at width 160 or 320 with documented receipts
- Git history showing the pack files were deleted after audit prep (unlikely)
- Evidence that the width ladder was ever measured (logs, receipts, or other documentation)