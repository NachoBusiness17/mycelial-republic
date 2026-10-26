# swarm1-glm-flash-mag__probe_route (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: probe_one writes selftest rows (use_cache=False) into the shared cache anyway, poisoning fresh TTL verdicts with dogfood data | EVIDENCE: mag/probe_route.py:104-107 | FIX: skip the cache write when use_cache is False (wrap lines 101-107 in `if use_cache:`), cache reads already honor the flag.
DEFECT 2: empty API key is accepted and probed, stamping "dead" verdicts on healthy slugs and poisoning the gate for the TTL window | EVIDENCE: mag/probe_route.py:129-131 | FIX: raise or fail fast in _key when os.environ.get returns empty, mirroring the selftest check at line 137.
DEFECT 3: DNS is validated in _assert_public_https but the connection resolves DNS again, a TOCTOU rebinding window between check at line 47-50 and the open at line 71 | EVIDENCE: mag/probe_route.py:47-50 | FIX: pin the connection to a validated address (custom HTTPConnection using the getaddrinfo result) instead of re-resolving inside urllib.
DEAD-CODE: `if not use_cache: row["cached"] = False` at line 100 is a no-op, "cached": False is already set in the row literal | EVIDENCE: mag/probe_route.py:100
ONE-SITTING FIX: gate both cache pollution sources together, skip the write on use_cache=False and reject empty keys before probing | EVIDENCE: mag/probe_route.py:100-107
