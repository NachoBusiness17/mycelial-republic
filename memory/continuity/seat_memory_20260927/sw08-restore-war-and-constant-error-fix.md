---
name: sw08-restore-war-and-constant-error-fix
description: SW-08 swarm lane fixed the standing constant-1-error test disease and caught/deduped/gated a QUEUE.md whole-file restore war; 93.6M tokens heaviest single lane
metadata:
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

SW-08 swarm lane (24 briefs, 93.6M tokens, 406 tool uses) completed 9/27 with three load-bearing findings beyond its briefs:

1. **Standing test disease fixed**: the suite's constant 1 error was `tests/test_spore_seed.py` mocker. Fixed in-lane.
2. **QUEUE.md whole-file restore war caught, deduped, and gated**: the evening's restore war (erased rows + 20 verbatim duplicate rows) was caught by the B2-486 census tool built in-lane.
3. **Falsifiers fired live on 7 briefs** (B2-318/B2-303/B2-386/B2-486/B2-427/B2-291/B2-297), proving the brief's own falsifier predictions on real bytes.

**Why:** the restore war is a multi-writer failure mode where concurrent whole-file restores erase landed edits; the census tool that caught it is reusable for any shared mutable file under concurrent writes.

**How to apply:** when a shared file shows unexpected reverts, check for a whole-file restore from a pre-landing snapshot; build a census that counts duplicate rows and gates the war.
