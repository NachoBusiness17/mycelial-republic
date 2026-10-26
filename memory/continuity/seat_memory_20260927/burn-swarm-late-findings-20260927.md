---
name: burn-swarm-late-findings-20260927
description: 9/27 late flash-lane burn findings — resolver deadline bound, chain
  quote pin, real-bytes chain census, doctor hostage prevention, and the FCFS
  census proving queue is FCFS not value-ranked
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Late 9/26-27 flash-lane burn findings — three technical fixes plus the FCFS census:

**B2-489 resolver deadline bound**: `mag/doctor.py _host_resolves` now runs `socket.getaddrinfo` on a daemon thread with a hard 2s deadline (`_RESOLVE_TIMEOUT_S`). Pre-fix, a blackholed DNS server stalled the entire `check_provider_endpoints` for 30+ seconds with zero red pins. Post-fix the same sleeper is bounded. 20 pins green. Follow-ups: B2-517/518/519.

**B2-383 chain quote pin**: `crash_log_census` chain-marker counting hardened — quoted markers inside a crash body no longer increment chains. Anchored `re.escape` + MULTILINE + structural 2-header rule. Falsifier confirmed the disease was real (quoted marker DID increment chains pre-fix). 28 passed. Live census byte-still {424, 424, 372, 52, 0}.

**B2-384 real-bytes chain census**: all 52 real crashes count chains=0; the only chained>0 bytes on disk are 25 synthetic pytest fixtures. A drift finding was named: three receipts record contradictory line counts for `logs/seat_crashes.log` against an mtime that predates two of them — sha256 anchored for the next census.

**FCFS census (operator "that a fact?")**: the burn queue dispatches strictly first-come-by-brief-number with zero value ranking. Census of 398 landed receipts: 97 debt-class by name, 27 clearly frontier, 274 neutral where real builds also live. The neutral majority is what no filename classifier can settle — the structural fact is the feed is FCFS, so queue composition is a choice we make, not a machine property.

**Key lesson**: the width-24 experiment confirmed the envelope ceiling is dynamic (function of window depth, not constant), and B2-98 proved 1,741 rate limits were silently absorbed at "clean" width 10 — the surfaced count undercounts by an order of magnitude.
