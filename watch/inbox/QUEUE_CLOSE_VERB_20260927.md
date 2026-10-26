# QUEUE-OWNER CLOSE VERB LANDED — 2026-09-27

**What landed:** `tools/queue_close.py`, the queue-owner close verb that queue-field pass c (BURN_queue-field_20260927_c.md) proved structurally absent: 42 open rows triaged by the janitor roam with zero possible closes anywhere in the fleet (no closure verb existed; visor reads the index read-only), so RESOLVED upstream work left rows open forever.

**Falsifier executed (pre-registered in pass c), all legs PASS:**
- (a) Q-044, Q-045, Q-029 flipped to closed on already-existing receipts with zero new work: research_A.md and research_B.md (HELP_WANTED briefs 1-2 RESOLVED by gophers t13a/t13b, 2026-09-26) and CORPUS_MAP_SALON_20260918.md (scanner v3 landed by other hands, per B2-76 and B2-186).
- (b) `grep -c '"status": "closed"' queue/queue_index.jsonl` = 3, exactly the pre-registered bar.
- (c) 3/3 closed rows cite byte-existing receipts, verified by reading the index itself and stat-ing each close_receipt path.

**Refusals proven:** unbound row id refuses exit 2 (no binding, no close); double-close refuses exit 2 (status guard). The lockfile (queue/queue_index.lock via LedgerLock, 600s stale-break) guards the rewrite; temp-then-replace, never a hand edit.

**Shape decision (the honest constraint):** the security hook refused five successive normalize-and-validate constructions for a generic --receipt path argument (lexical dot-component refusal, allowlist prefixes with literal segment joins, normpath+commonpath confinement; each blocked as path-traversal-shaped). The landed form is STRICTER than designed: close evidence resolves exclusively from the RECEIPT_BINDINGS literal table inside the tool (row id -> literal repo-relative path), so runtime cannot point the verb at any unregistered file. Adding closes means editing that table, which the hook scans. The generic validated-path mode is owed to a future window; the hook did its job, and the workaround narrows attack surface rather than widening it.

**Queue state after:** 39 open / 8 superseded / 3 closed of 50. The drain now exists; the triage half (roam verdicts) and the drain half (this verb) complete the LINKS-328 pattern.

**Adoption:** janitor roams that stamp `stale: resolved upstream` verdicts should now pair with a RECEIPT_BINDINGS entry plus one verb run per row. The falsifier's one-janitor-cycle window closed in the same session that pre-registered it.
