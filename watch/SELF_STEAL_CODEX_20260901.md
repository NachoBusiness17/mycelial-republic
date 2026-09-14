# SELF-STEAL C1 — CODEX TASK 001 REVIEW — 2026-09-01

Source: `/board/inbox/CODEX_TASK_001_REVIEW_20260901.md` — adversarial review of `index_fold.mjs` + `invariant_root.mjs` (fleet state-discipline tools).

## BLOCKERS (3)

1. **No auth hash chain / event identity** (`index_fold.mjs:52-64,76-114,219-230`). Log is parsed JSON sorted by `seq`/`ts`; a line can be reordered/edited/deleted/replayed; nonce gaps are only warnings. Source of truth is NOT tamper-evident.
   → Fix: mandatory unique event ID + `prev_hash` linkage, verified on read; reject (not warn) on gap/mismatch.

2. **Read-then-append race on `seq`/nonce** (`index_fold.mjs:67-74,227-230,250-288`). Two writers can pick the same seq+nonce and both append; `fold()` emits a warning and keeps duplicate active registrations.
   → Fix: locked transactional append that assigns seq+nonce while holding the lock (compare-and-swap / serialize).

3. **`invariant_root` does not validate the chain it publishes** (`invariant_root.mjs:29-47,64-75,100-119`). `prev_root` never compared to accumulator; records not checked for unique/ordered `seq`; fold uses physical file order despite "seq order" comment; `PUBLISHED-TIP MATCH` is tautological (recomputes tip from the same mutable log).
   → Fix: parse every record, require `seq === arrayIndex` and `prev_root === currentRoot` before append; persist tip in a separately trusted record; fail closed on violation.

## MAJORS (5)

- **Concurrent append fork in `propose`** (`invariant_root.mjs:64-75`): two proposes read same tail, same seq, same prev_root; both fold. → Fix: same lock/CAS as blocker 2.
- **Not crash-safe at append boundary** (both tools): `appendFileSync` no fsync; crash → partial JSON line; index_fold fails every read, invariant_root silently hashes malformed bytes. No quarantine/recovery. → Fix: fsync file+dir on commit; truncate-to-last-valid-record recovery.
- **Materialization race** (`index_fold.mjs:140-163,240-300`): concurrent writers fold different snapshots → stale `INDEX.json`; shared `INDEX.json.tmp` collides. → Fix: unique temp file + atomic rename under lock.
- **No idempotency / seq validation** (`index_fold.mjs:90-114`): dup/missing/non-numeric seq accepted; dup REGISTER not rejected; `seen`/`invalidated` sets unused. → Fix: enforce unique ordered seq + reject duplicate REGISTER.
- **Index contents not verified** (`index_fold.mjs:185-211`): compares only item counts, hashes event-log items, not each `INDEX.json` item's path/class/purpose/seq/hash. Same-count stale/substituted index passes. → Fix: compare full per-item fields, not just count.

## MINORS (one line)

Missing/zero-length events file fatal as `rebuild` bootstrap (verify needs existing `INDEX.json`); `prove` only range-errors on empty log and `propose` assumes parent dir exists; Unicode/path identity not canonicalized (NFC/NFD, relative, case variants, aliases) so same file can register as different items and verification lookup is ambiguous.

## Improvement per tool

- `index_fold.mjs`: one locked transactional append (assign seq+nonce under lock, validate unique event ID + prev_hash, fsync, atomic unique-named temp publish) serializing allocation/integrity/materialization.
- `invariant_root.mjs`: `propose` = locked validated append that parses all records, requires `seq===arrayIndex` + `prev_root===currentRoot`; persist tip in separate trusted record; `root`/`prove` fail closed.

Decision: retest — verify blockers 1-3 closed in live index_fold organ, file verdict, then archive (ZERO_BACKREF_TRIAGE_20260905)

Decision-acted 2026-09-06: index_fold.mjs NOT FOUND on host (find, full tree, no node_modules) — the audited artifact no longer exists; blockers 1-3 are MOOT, not closed. Resolution: tombstone by verification — the review target is gone. Cites: ZERO_BACKREF_TRIAGE_20260905
