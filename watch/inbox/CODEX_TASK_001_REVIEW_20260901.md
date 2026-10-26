# CODEX TASK 001 REVIEW — 2026-09-01

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: REVIEW_index_fold.mjs and REVIEW_invariant_root.mjs are not tamper-evident or concurrency-safe (3 blockers, 5 majors, 2 minors, line-cited) — SUPPORTED (read-only code review with exact line citations) · falsifier: re-reading the cited lines shows a hash chain, lock, or external-tip validation actually enforced

Scope: read-only review of `REVIEW_index_fold.mjs` and `REVIEW_invariant_root.mjs`.

## Findings

### BLOCKER

- [BLOCKER] `REVIEW_index_fold.mjs:52-64, 76-114, 219-230` has no authenticated hash chain or event identity. The event log is only parsed JSON sorted by `seq`/`ts`; a line can be reordered, edited, deleted, or replayed and the tool will accept the resulting history. Nonce gaps are warnings, not rejection, and a replay under another writer name is invisible. The claimed append-only source of truth is therefore not tamper-evident.

- [BLOCKER] `REVIEW_index_fold.mjs:67-74, 227-230, 250-288` has a read-then-append race for both `seq` and writer `nonce`. Two concurrent writers can choose the same sequence and nonce, then both append successfully. `fold()` applies both events and merely emits a warning for the nonce collision; duplicate registrations can remain active. `O_APPEND` protects the individual write position, not allocation or event ordering.

- [BLOCKER] `REVIEW_invariant_root.mjs:29-47, 64-75, 100-119` does not validate the chain it publishes. `prev_root` is never compared with the accumulator, records are not parsed or checked for unique/ordered `seq`, and the fold uses physical file order despite the comment saying “seq order.” `PUBLISHED-TIP MATCH` recomputes the tip from the same mutable log, so it is tautological without an external trusted tip. A reordered, edited, or replayed log can therefore produce a self-consistent but different “valid” history.

### MAJOR

- [MAJOR] `REVIEW_invariant_root.mjs:64-75` has the same concurrent append fork: two `propose` processes can read the same tail, assign the same `seq`, and record the same `prev_root`. Both lines are then folded; there is no lock or compare-and-swap to make one proposal fail.

- [MAJOR] Both tools are not crash-safe at the append boundary. `appendFileSync` does not fsync the file or directory. A crash can leave a partial final JSON line; `index_fold.mjs:52-64` then fails every read, while `invariant_root.mjs:29-33` silently hashes the malformed nonblank bytes instead of rejecting them. There is no quarantine, truncation-to-last-valid-record, or recovery path.

- [MAJOR] `REVIEW_index_fold.mjs:140-163, 240-300` has a materialization race. Concurrent writers can fold different snapshots and publish a stale `INDEX.json`; concurrent rebuilds share the fixed `INDEX.json.tmp`, so one can overwrite the other or rename can fail. The event log may retain the event, but the advertised derived index is then stale until a later rebuild.

- [MAJOR] `REVIEW_index_fold.mjs:90-114` accepts duplicate or missing/non-numeric sequence values and has no idempotency check for duplicate REGISTER events. The unused `seen` and `invalidated` sets do not enforce anything. Duplicate REGISTER lines create duplicate active items, and sorting ties by timestamps is not a protocol-level ordering rule.

- [MAJOR] `REVIEW_index_fold.mjs:185-211` does not actually verify the materialized index contents. It compares only item counts, then hashes the folded event-log items rather than comparing each `INDEX.json` item’s path, class, purpose, sequence, and hash. A stale or substituted index with the same count can pass the hash report.

### MINOR

- [MINOR] Empty-log behavior is incomplete. A missing events file is fatal at `REVIEW_index_fold.mjs:52-54`, so `rebuild` cannot bootstrap an empty inbox; a zero-byte existing file works, but `verify` still requires an existing `INDEX.json`. `invariant_root.mjs` handles an empty existing/missing log as genesis, but `prove` only reports a range error and `propose` assumes the parent directory already exists.

- [MINOR] Unicode and path identity are not canonicalized in `REVIEW_index_fold.mjs:92-106, 191-201`. NFC/NFD spellings, relative paths, case variants on case-insensitive hosts, and aliases can register the same file as different items. The file-byte hash itself is fine, but the identity and later invalidation/verification lookup are ambiguous.

## One improvement per tool

- `REVIEW_index_fold.mjs`: ship a locked transactional append primitive that assigns `seq` and nonce while holding the lock, validates a unique event ID plus `prev_hash`, fsyncs the committed event, and only then atomically publishes a uniquely named folded-index temp file. This turns allocation, integrity, and materialization into one serialized protocol boundary.

- `REVIEW_invariant_root.mjs`: make `propose` a locked, validated append that parses every existing record, requires `record.seq === arrayIndex` and `record.prev_root === currentRoot` before appending, and persists the resulting tip in a separately trusted publication record. `root` and `prove` should fail closed on any violation.
