---
name: crash-census-chains-zero-20260927
description: 9/27 crash census on production bytes — all 52 real crashes count
  zero chains, only synthetic fixtures exercise the chains feature; plus the
  width-24 experiment verdict (dynamic ceiling confirmed by 8 surfaced deaths
  and 287 absorbed)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Two findings from the 9/26-27 flash-lane burn's final swarm waves, both byte-proven:

**Crash census chains=0 on real bytes** (B2-384): crash_log_census run against the production logs/seat_crashes.log (424 blocks, 372 test, 52 real) shows chains=0 across every real crash. The chains=N feature (counting wrap-and-reraise stanzas via "During handling of the above exception" markers) exists and is fixture-tested but has never fired on real fleet crashes. The only chains>0 bytes on disk are synthetic pytest-tmp copies of the test fixtures. A drift finding was also named: three receipts record contradictory line counts against a file whose mtime predates two of the reads.

**Chain quote pin proven necessary** (B2-383): the falsifier was real — a quoted chain-marker sentence inside a crash body DID increment chains before the fix. Hardened to column-anchored markers (re.escape + ^ MULTILINE) plus a structural rule (chains counted only in stanzas holding 2+ Traceback headers). Live census unchanged post-hardening.

**Width-24 experiment verdict** (B2-98 + B2-25 + SW-10): the "clean" waves carried 287 absorbed 1302s invisible to surfaced counts (wave 1: 129, wave 2: 35, wave 3: 123). Envelope ceiling is a function of window depth, not a constant. Ladder amends to 3-6-10-12 clean, 15-16 untested, width 24 surfaces limits when window runs deep. 1,785 driver-visible failures total; only 1 terminal death (B2-214 agent exhausting all 11 attempts). The burn hit ~816M witnessed tokens across 191 agents before the width-24 experiment phase.

**Why:** the fleet's instruments now measure their own blind spots — the tally catches absorbed retries, the census catches phantom chains on fixtures only, and the envelope law is parameterized by window depth instead of frozen. These are the three blindnesses the old instruments couldn't see.

**How to apply:** any future burn should run the provider-error tally alongside the envelope measurement; crash census chains= should be treated as unexercised on real bytes until a genuine chained crash appears; and the width ladder should be re-probed at the start of each window, not assumed from the last measurement.
