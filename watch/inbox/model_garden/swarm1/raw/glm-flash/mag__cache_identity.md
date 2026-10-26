# swarm1-glm-flash-mag__cache_identity (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: probe crashes with TypeError when run without --seed: nonce `seed` is computed but the marker is built from `args.seed`, which is None by default | EVIDENCE: mag/cache_identity.py:330 vs 343 | FIX: change `marker_for(args.seed, r)` to `marker_for(seed, r)`
DEFECT 2: with --seed pinned, cross-run byte-identity serves stale KV as hits and inverts the drift arms (the failure the code comment itself documents), and nothing warns or blocks it | EVIDENCE: mag/cache_identity.py:326-331, 343 | FIX: when args.seed is not None, print a loud WARNING and stamp `seed_pinned: true` into the row before measuring
DEFECT 3: docstring verdict rule "Warm slower than 1.5x / hit < 0.5 -> DISPUTED" reads as OR but the code gates DISPUTED on AND, silently reclassifying fast-no-hit and slow-hit runs as UNPROVEN | EVIDENCE: mag/cache_identity.py:36-38 vs 264-268 | FIX: fix the docstring to "speedup < 1.5 AND hit < 0.5" or split the gate in code to match the doc
DEAD-CODE: tautological assertion comparing prompt_sha to itself, always true, checks nothing | EVIDENCE: mag/cache_identity.py:356
ONE-SITTING FIX: apply the DEFECT 1 one-token patch (`marker_for(seed, r)`) plus the seed_pinned stamp from DEFECT 2, then run `python -m mag.cache_identity check` and a 1-round `probe` with no --seed to prove the default path lands a MEASURED row | EVIDENCE: mag/cache_identity.py:330,343,510

Falsifier for the fix: after the patch, `probe` with no --seed must complete with `seed_nonce: true` and a nonzero integer `seed` in the appended row; a TypeError traceback at the marker line means the fix is wrong.
