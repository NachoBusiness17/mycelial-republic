## Finding — what your cell yields
The fanout_organ's width ladder is a measured progression from 2 to 480 lanes, with each rung producing a falsifiable receipt. The ladder validates the claim that N-wide fan-out scales without bespoke runners per pack.

## Evidence — what in the repo supports it (file/shape, no invention)
- mag/fanout.py (107 lines): single-file stdin/stdout organ enforcing packs-as-data purity
- Pack files as width ladder rungs:
  - p3_mud_20260912.json (3 lanes)
  - p6_ractor_game_20260912.json (6 lanes)
  - p8_adam_onboard_20260912.json (8 lanes)
  - p20_clarkes_end_20260912.json (20 lanes)
  - p40_loom_iter_20260912.json (40 lanes)
  - p80_loom3_20260912.json (80 lanes)
  - p160_matthew_20260913.json (160 lanes)
  - p320_matthew_ds_20260913.json (320 lanes)
  - p160_loom3_ds_20260912.json (160 lanes, deepseek)
- HOST_ALLOW in fanout.py line 39: {"api.z.ai", "api.deepseek.com"}
- Guarded fetch in lines 41-54: https + allowlist + global IPs + no redirects
- Output contract line 102: ===FANOUTJSON=== marker

## Risk if wrong — what the audit breaks on if this is missed
- Without width ladder receipts, the 480-wide claim is unverified — the examiner cannot falsify the scaling law
- Missing rung documentation leaves gaps in the entropy-minimization narrative (EUT frame)
- Cache-correlation caveat (shared_head hits vs misses) is undocumented, risking the hard-reproducibility claim

## The act — the concrete prep step (file/spec/number)
Create audit_prep/fanout_organ_width_ladder_receipt.md documenting:
1. Each rung's date, width, pack file, and produced-what
2. Cost curve between rungs (shrinking gaps = efficiency gains)
3. Cache-correlation caveat: shared_head enables cache hits across lanes
4. HOST_ALLOW enforcement as iron egress proof

## Falsifier — what would prove this wrong
- Any pack file width does not match the claimed rung in the ladder
- Presence of file I/O inside mag/fanout.py (violates purity law)
- Successful egress to host not in HOST_ALLOW
- Output missing ===FANOUTJSON=== marker or deviating from schema
- Missing pack file for any claimed rung
