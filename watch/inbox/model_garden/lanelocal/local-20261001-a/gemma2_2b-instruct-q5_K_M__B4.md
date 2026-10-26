# garden-v1-B4 | gemma2:2b-instruct-q5_K_M | series local-20261001-a | instrument=lane-local-script
# finish=stop prompt_tokens=1608 completion_tokens=119 wall_s=8.18 tok_s=14.5 checks=1/5 {'SHAPE': 0, 'CITES-RESOLVE': 0, 'LINES-IN-RANGE': 0, 'NO-EM-DASH': 1, 'DISTINCT-EVIDENCE': 0}

IMPROVEMENT 1: the contract fails to declare which 'surface' acts as the canonical surface | EVIDENCE: watch/inbox/SHARED_SURFACE_CONTRACT.json:11 | FIX: add specification of the intended canonical surface 
IMPROVEMENT 2: the contract does not distinguish between 'surface' and 'inbox' | EVIDENCE: watch/inbox/SHARED_SURFACE_CONTRACT.json:10 | FIX: define a distinction between the surfaces for each intent
DIFFERENT-BUILD: build out a more comprehensive specification of the 'surface' | 

