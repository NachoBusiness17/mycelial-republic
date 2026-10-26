# BURN middle-path-doctrine 20260927 h

## Verdict

steal

## Evidence

- Burn ledger census: the patrol "samples 3 LANDED rows per UTC day" and "mechanically checks every path-existence, sha256, and byte-size claim extractable from each one_line against disk"; "WARN-ONLY by law: the patrol never edits the ledger" (tools/ledger_spot_patrol.py docstring; SPOT_PATROL_LANDED_20260927.md).
- Registry census: "the visor owns nothing and remembers nothing. Every invocation recomputes the whole board from bytes on disk" covering "memory/workflows/REGISTRY.jsonl", "memory/burns/LEDGER.jsonl", "queue/queue_index.jsonl" (tools/visor.py docstring).
- Zombie arm: "refresh the doc (with today's truth) or re-register it as deliberately frozen by adding it to FROZEN_OK below with a reason and date"; FROZEN_OK is "Deliberately-frozen docs with the date + reason they are allowed to age" (tools/freshness_check.py lines 12-13, 43-44).
- Death arm: Q-044 sat as "leftover drop-candidate pointer awaiting queue-owner close"; the lane rule: "This pass stamps only, never closes" (BURN_queue-field_20260926_b.md). Byte truth: Q-044/Q-045 now carry "closed_ts": "2026-09-27T09:27:44Z", "closed_by": "queue-owner" (queue/queue_index.jsonl lines 44-45).
- X6, digest line 553: "if no auditable, dissolvable steward design can be stated for a modern application without collapsing into custody, C9's modern half is withdrawn."
- WebSearch 2026-09-27, "institutional decay detection ledgers 2026": thin. Financial-compliance analogy grade (OSFI Ledger bulletin, SBA fraud-ledger critique, a Miller Center decay event page); no 2026 twin-ledger decay instrument surfaced; snippets only, unread, owed.

## Steal or Vacuous

Statable. Pass g's decay gate survives its own falsifier's first test; its pre-registered falsifier carries unchanged.

(a) Census feasible: both counts read jsonl the fleet already writes and already scans. Mandate census (seats of record) and function census (gate acts on record) are greps over LEDGER.jsonl, REGISTRY.jsonl, queue_index.jsonl; the patrol proves claim-vs-artifact reads are mechanical; the visor proves a full recount is one stateless invocation. No standing observer is added; the meter is the ledger.

(b) Zombie arm has precedent: decay detection plus one-event dissolution already exists as a registration act. A stale live-claiming doc is refreshed or dissolved into FROZEN_OK with reason+date in one edit; superseded queue rows were "kept and tagged so the census stays honest rather than silently dropped" (BURN_queue-field_20260925_b.md). Registered freeze, never silent keeping.

(c) Death arm is live fleet behavior, completed today: Q-044/Q-045 sat open two days on "a 'queue-owner' with no lane or tooling" (BURN_queue-field_20260927_b.md); every lane suspended rather than self-appoint, then the queue-owner close verb seated the named steward and closed both rows on existing receipts; the suspension ended exactly when the steward was seated.

Ruling: steal stands. The gate reads acts on record, adds no observer, and both trip arms map to machinery already landed. X6's steward leg stays unfired.

## Pilot annotation

Annotation-only arm; nothing measured.

## Bibliography

- watch/inbox/BURN_middle-path-doctrine_20260927_g.md (read in full)
- watch/inbox/BURN_middle-path-doctrine_20260927_f.md (read in full)
- watch/inbox/TREE_DOCTRINE_V2_DIGEST_20260925.md (lines 1-290 and 520-599 read; X6 verified at line 553)
- tools/ledger_spot_patrol.py (docstring); watch/inbox/SPOT_PATROL_LANDED_20260927.md (full)
- tools/visor.py (docstring); tools/freshness_check.py (lines 12-13, 43-44 grep-verified)
- queue/queue_index.jsonl (lines 44-45); BURN_queue-field_20260925_b.md, _20260926_b.md, _20260927_b.md (quoted lines grep-verified)
- WebSearch 2026-09-27, "institutional decay detection ledgers 2026" (thin, snippets only, owed)
