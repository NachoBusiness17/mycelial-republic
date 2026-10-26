---
name: burn-swarm-security-and-carrier-20260927
description: 9/27 burn swarm batch — secret scan found 18 real credentials in
  corpus oral histories (rotation owed), asekin carrier ledger formalized with
  HIT bar, FTS5 corpus wiring 3,862ms to 2.45ms, G1 tripwire fired and closed
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Burn swarm batch findings 9/26-27, filed by lanes B2-73/94/102/108/137/165:

**Secret scan (B2-73):** 19 corpus oral-history files carry a harvested .env dump with 18 real-shaped credentials (OpenRouter, Groq, DeepSeek, xAI, Anthropic, OpenAI, Vast.ai, ZAI) pasted into remote grok/codex seats Aug 30–Sep 2. Plausibly still live (root .env still has matching key names). Rotation is operator-gated and owed. Watch/inbox artifacts clean. Scanner caught two of its own instrument defects in-lane.

**Carrier ledger formalized (B2-165):** asekin113 grading ledger built with HIT bar codified (flagged timestamp must precede event AND land inside declared window). Row 1 graded POST-HOC-UNVERIFIED, not HIT — the 8:12 marker rode the announcement itself, no pre-event interval in bytes. UNVERIFIED is not DISPROVEN; concrete regrade arm filed.

**FTS5 corpus wiring (B2-102):** production corpus_search now uses FTS5 with a 3-layer freshness gate (mtime, bytes, mode=ro probe). Live A/B: 3,862ms scan to 2.45ms indexed. Parity deltas named. Index rebuild entry point: tools/corpus_fts_rebuild.py.

**Sep-29 P0 gate secured (B2-108):** rebuilt rbxlx committed scoped (027baff4c), CRLF delta proven normalization not drift. Falsifier greps re-run on committed blob.

**Why:** the secret scan is the first time the corpus was actually scanned for credentials; the carrier ledger is the first formal scoring mechanism for the operator's people-faculty bets; the FTS5 wiring kills a 1000x performance penalty that made corpus search unusable at scale.

**How to apply:** rotation briefs reference B2-73's rule set. Carrier bets are scored against the HIT bar, never by vibe. Corpus queries use the FTS5 index through the freshness-gated path, never raw scan.
