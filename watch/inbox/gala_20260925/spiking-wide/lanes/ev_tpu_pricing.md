# RAW EVIDENCE: WebFetch https://cloud.google.com/tpu/pricing
# Fetched 2026-10-01 by lane nonnvidia-stacks (division B, spiking-wide). Verbatim fetch result below.

PROMPT: What is the on-demand price per chip-hour for TPU v5e (also called CT5LP or v5-lite-pod) in us-central1 or any listed region? Also list any v5e pricing and v7 Ironwood pricing if shown. Quote the exact dollar figures and region names shown.

RESULT:
# TPU v5e (CT5LP) On-Demand Pricing - per chip-hour

## On Demand (USD):
- **us-central1 (Iowa):** $1.20
- **us-east5 (Columbus):** $1.20
- **us-south1 (Dallas):** $1.416
- **us-west1 (Oregon):** $1.20
- **us-west4 (Las Vegas):** $1.20
- **europe-west1 (Belgium):** $1.32132
- **europe-west4 (Netherlands):** $1.56
- **asia-southeast1 (Singapore):** $1.56

## Other v5e pricing columns (for reference):
- DWS Flex-start: $0.60/hr (all regions)
- DWS Calendar Mode: $0.84/hr (all regions)
- 1-year Commitment: $0.84 (most), $0.9912 (Dallas), $0.924924 (Belgium), $1.092 (Netherlands/Singapore)
- 3-year Commitment: $0.54 (most), $0.6372 (Dallas), $0.594594 (Belgium), $0.702 (Netherlands/Singapore)

# TPU v7 Ironwood On-Demand Pricing - per chip-hour

- **us-central1 (Iowa):** $12.00
- **europe-west2 (London):** $13.20

Ironwood also shows: DWS Flex-start $6.00/hr, DWS Calendar Mode $8.40/hr, 1-year CUD $8.40 (Iowa) / $9.24 (London), 3-year CUD $5.40 (Iowa) / $5.94 (London).

**Note:** All prices are per chip-hour; console billing is displayed in VM-hours (e.g. a TPU v4 host with 4 chips shows as $12.88/hr on demand).
