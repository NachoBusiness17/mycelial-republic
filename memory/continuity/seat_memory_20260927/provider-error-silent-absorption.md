---
name: provider-error-silent-absorption
description: B2-98 finding 9/26 — the main-session retry layer (maxAttempts 11)
  silently absorbs 429/1302s; "zero surfaced" ≠ "zero occurred"; durable tally
  tool built
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

The main-session retry layer (maxAttempts 11 per corpus/steal/TETHERED_LINK_STEAL_20260925.md:17) absorbs 429/1302 provider errors before they reach any lane-visible surface. B2-98's tally of the driver's daily log found 1,785 network failures on the burn session, 1,780 = 429 with [1302] markers, 1,741 absorbed by retries. Three waves B2-25 called "clean" (zero surfaced) carried 287 absorbed 1302s.

**Tool built**: `tools/provider_error_tally.py` counts model.network.failed/completed events from the CLI daily log, joins to agents via parentSessionId/childSessionId, counts statusCode 429, [1302] markers, absorbed retries, terminal failures. Writes provider_errors.json into the agent session dir.

**Why:** Envelope probes and width experiments cannot distinguish "none occurred" from "none surfaced" without this counter. The old claim "zero 1302s" was a measurement blind spot, not a fact.

**How to apply:** Any width experiment or envelope probe must use the tally tool or its successor, never grep lane outputs alone. B2-98's receipt has the exact join queries.
