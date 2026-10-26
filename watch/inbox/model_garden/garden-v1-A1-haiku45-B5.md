# garden-v1-A1-haiku45-B5 (anthropic/claude-haiku-4.5 @ nous, turn 1, channel: content)

IMPROVEMENT 1: Nonce eviction uses real wall time instead of injectable `now` parameter, permitting replay attacks when verify() is called with a frozen clock for testing | EVIDENCE: mag/steer_seal.py:281-283 | FIX: Change `cutoff = time.time() - 2 * FRESHNESS_SECONDS` to `cutoff = now - 2 * FRESHNESS_SECONDS` and pass `now` to `check_and_record()`.

IMPROVEMENT 2: admit() enforces strict envelope parse but permit words in plaintext directives are rejected without a fallback, breaking the documented "plaintext classify" path | EVIDENCE: mag/steer_seal.py:390-391 | FIX: Change `parse_envelope(text)` to `_try_parse_envelope(text)` to allow plaintext restrictive words in directive files.

IMPROVEMENT 3: FileNonceStore.check_and_record() does not validate `now` is an integer, permitting non-int timestamp values to be written to marker files | EVIDENCE: mag/steer_seal.py:272 | FIX: Add `if not isinstance(now, int): raise VerifyError("now must be int")` before the mkdir call.

DIFFERENT-BUILD: Decouple nonce state from filesystem markers into a transactional log with atomic compare-and-swap semantics (e.g. SQLite WAL mode or a single append-only file with CAS offset). The current glob-based eviction is racy under concurrent verify() calls and loses nonce claims on I/O errors even though exclusive-create already claims them; a single writer pattern would close that race and simplify testing.
