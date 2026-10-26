# swarm1-glm-flash-mag__wave_fire (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: A suspended slug is auto-cleared from a single-lane perfect ratio, bypassing the >=2-lane sample guard the else-branch enforces and un-bricking a breaker suspension on n=1 | EVIDENCE: mag/wave_fire.py:124-126 | FIX: change line 124 to `if ratio == 1.0 and len(oks) >= 2:`
DEFECT 2: The gate probes every slug with lanes[0]'s key_env and url only, so lanes pointing at a different endpoint or key_env get live/dead verdicts minted from the wrong credentials and host, and those lanes then fire on that verdict | EVIDENCE: mag/wave_fire.py:96-100 | FIX: probe per distinct (url, key_env) pair from the lanes list and gate each lane against its own pair's live set
DEFECT 3: lane_id is interpolated unvalidated into output filenames, so a lanes.json entry with a path separator writes lane output and receipts outside outdir | EVIDENCE: mag/wave_fire.py:81,84 | FIX: sanitize or reject lane ids not matching `^[A-Za-z0-9._-]+$` before use
DEAD-CODE: ALLOWED alias assigned and never referenced (callers use the full name) | EVIDENCE: mag/wave_fire.py:35
ONE-SITTING FIX: require len(oks) >= 2 before the breaker clear so one lucky lane cannot erase a suspension; this is the runner's own stated guarantee (comment at 116-117) currently violated by its code | EVIDENCE: mag/wave_fire.py:124-126

Falsifier for the one-sitting fix: run a 1-lane wave with a slug held in lane_breaker suspended state and status ok; after the patch WAVE.json breaker must show "unsampled(<2), not tripped" and lane_breaker._load() must still list the slug as suspended.
