# swarm1-kimi-tools__saturation_fourcond (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Blind label generation overflows after 26 cells producing non-letter labels | EVIDENCE: tools/saturation_fourcond.py:163 | FIX: Use base-26 or label format that handles >26 cells: `labels = {i: f"L{i:02d}" for i in range(len(cells))}`

DEFECT 2: HTTP 429 retry sleeps total 45s but loop only retries twice, losing third attempt on persistent rate limit | EVIDENCE: tools/saturation_fourcond.py:98-108 | FIX: Extend sleep sequence to cover third attempt or document hard-stop at 2 retries

DEFECT 3: judge_vector hardcodes 1200 prompt tokens for cost accounting but actual prompt varies with checklist length | EVIDENCE: tools/saturation_fourcond.py:183 | FIX: Compute actual prompt tokens from rendered prompt or pass through usage from ds_call response

DEAD-CODE: ipaddress import and DNS validation in _validated_api_url | EVIDENCE: tools/saturation_fourcond.py:57-68 | 

ONE-SITTING FIX: Blind label overflow breaks experimental reproducibility for >26 conditions | EVIDENCE: tools/saturation_fourcond.py:163 | FIX: `labels = {i: f"{i:03d}" for i in range(len(cells))}`
