---
name: late-night-burn-20260926
description: Late-night 9/26 burn wave results — B2-79 returncode law (grounding
  chain crash could file firing rows), B2-98 quantified 287 absorbed 1302s
  proving "clean" waves were dirty, B2-359 found 8 test-to-production writer
  chains, B2-358 env tripwire caught pytest's unreliable suppression marker,
  B2-25 confirmed 109M tok/h at width 10
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Late-night 9/26 burn wave (lanes B2-64..98) landed across seven swarm lanes plus the width-24 experiment:

**B2-79 returncode law**: grounding_chain.py fired rows BEFORE the fire and discarded the subprocess result, so a crashed driver still filed a "firing" WHY row (proven live: KeyError stranded state + lock while row claimed grounded). Fixed: rows land after fires, every action carries exit_code + state_before/state_after. 6 new tests. Residual honestly named: no real dead-child proof yet (queue was empty).

**B2-98 provider-error tally**: 1,785 driver-visible network failures on the burn session today, 1,780 = 429 with [1302], 1,741 absorbed by retry layer. Three waves B2-25 called "clean" carried 287 absorbed 1302s (wave 1: 129, wave 2: 35, wave 3: 123). "Zero surfaced" ≠ "zero occurred" — the falsifier B2-25 pre-named, now quantified. Durable per-session tally at provider_errors.json.

**B2-25 envelope re-measure**: width 10 confirmed clean at 109M tok/h witnessed, ladder extends to 3-6-10-12, 15-16 rung still untested. Carry-forward: B2-98's absorption discovery means "zero surfaced 1302" only means zero got past retry.

**B2-359 writer census**: 8 live test-to-production writer chains confirmed on bytes, including two tests that drain the real operator inbox and one that can consume pending operator guidance. Previously closed sinks verified still clean.

**B2-358 env tripwire**: MAG_SEAT_CRASH_LOG / MAG_GAPS_LOG leaks now caught by doctor + validate. Design finding: PYTEST_CURRENT_TEST can never be a suppression key (pytest re-sets it at every phase transition).

**B2-374 behavioral scout pin**: same unpinned-substring-count disease as the crash scout, in the neighboring behavioral-events block. Fixed with the census function pattern. Also caught: a non-dict JSON row raised inside the block and the outer except silently dropped the whole behavioral row.

**Width-24 data**: 397 → 471 dispensed briefs, 206 landed. The swarm lanes ground through the backlog for 14+ hours. Every landed receipt has a 5-section file on disk.

**Key findings for the operator**: (1) the width-24 experiment is running live; (2) the depth thesis is proven: unbounded deep lanes produce what bounded briefs cannot; (3) the envelope ceiling is dynamic by window state, not a constant.
