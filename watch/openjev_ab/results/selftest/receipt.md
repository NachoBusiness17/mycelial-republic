# openjev A/B receipt

- run: SELFTEST (mock arms, zero inference)
- frozen set: frozen30_20260925.jsonl (sha256 8e0b6da1f283a301.., verified)
- arms scored: 30 pairable of 30 items
- agreement A vs B: 27/30 (kappa 0.7964)
- arm A vs prior tier-1: 23/30 (76.7%); arm B vs prior tier-1: 22/30 (73.3%)
- arm B infra fails: 0
- escalations: 9 items (disagreements, low confidence, low margin, infra)
- verdict: adopt_candidate=True meter_only=False (bars pre-registered in OPENJEV_AB_PROTOCOL_20260925.md section 6)

Escalation queue (operator adjudication at the fold gate):
- ojab-01390cde: arm-a-low-confidence, arm-b-low-margin (a=no b=no prior=no)
- ojab-0c3cdee4: arm-a-low-confidence, arm-b-low-margin (a=no b=no prior=no)
- ojab-0da96447: arm-disagreement, arm-a-low-confidence, arm-b-low-margin (a=yes b=no prior=yes)
- ojab-0fa281b5: arm-disagreement, arm-a-low-confidence, arm-b-low-margin (a=yes b=no prior=no)
- ojab-0ff538f6: arm-a-low-confidence, arm-b-low-margin (a=no b=no prior=no)
- ojab-16519dbd: arm-a-low-confidence, arm-b-low-margin (a=no b=no prior=no)
- ojab-16ab4ca2: arm-disagreement, arm-a-low-confidence, arm-b-low-margin (a=yes b=no prior=yes)
- ojab-1964bfcf: arm-a-low-confidence, arm-b-low-margin (a=no b=no prior=yes)
- ojab-1f4aebf5: arm-a-low-confidence, arm-b-low-margin (a=no b=no prior=no)
