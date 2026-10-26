# B2-386 higher-fidelity refetch for the 33881-group thumbs 2026-09-26

## Verdict

Probed, honest-limit STANDS. No reachable surface serves the 33881-byte original: the register's own signed cdn4.telesco.pe URL still returns the same 4727 bytes (sha 66268013e17b0727), the fresh t.me embed page's extracted URLs serve the same 4727-byte render, and telesco.pe ignores size query params (?size=l, ?size=x, ?download=1 all 200 at 4727). The Telegram Desktop public export arm is unavailable (none exists to pull). Since no exact-33881-byte hit landed, NO superseding row is owed and the falsifier's second arm holds: zero of the 314 existing register rows were edited (byte-unchanged, sha-spot-checked). The B2-88 identity honest-limit ("same message's publicly served image", never byte-identical original) remains the correct classification.

## Evidence file:line quotes

- watch/inbox/mrpool_export/media_recovered_register_20260926.jsonl row msg_id 176: `"bytes": 4727, "ledger_file_size": 33881, "sha256": "66268013e17b0727..."`; live refetch of its source_url 2026-09-26: HTTP 200, 4727 bytes, sha256 prefix 66268013e17b0727 (identical bytes, URL not yet expired).
- Fresh t.me/MrPool_Q/176?embed=1&mode=tme: HTTP 200, 16360 bytes, 2 distinct cdn*.telesco.pe/file/ URLs extracted; a fetched one lands 4727 bytes, sha 66268013e17b0727 (same render, same single image behind all 262 cites).
- Size-variant probes on the fresh URL: `?size=l` 200:4727, `?size=x` 200:4727, `?download=1` 200:4727, `&sz=33881` 404:161 (query params ignored; no size-selection surface exists).
- Register census (B2-88 receipt line 10): 33881x262 rows carry 1 distinct sha at 4727 bytes, 0 size matches; this probe adds the 2026-09-26T20:44Z re-measurement with the same outcome.
- Structured probe record: watch/inbox/burn_wave_20260926/B2_386_refetch_probe_results.json (all four arms with results).

## Work done

1. Re-read the B2-88 Verdict honest-limit paragraph and the register rows for the 262-group (single distinct sha 66268013e17b0727 at 4727 bytes).
2. Probed the brief's three surfaces plus variants: (a) original source_url refetch, (b) fresh t.me embed page with URL extraction and fetch, (c) telesco.pe size/query variants, (d) Telegram Desktop export availability (absent). Intermittent curl 000s in the local shell were diagnosed (single-shot fetches succeed; not a CDN verdict) and named rather than read as failures.
3. Confirmed every reachable arm returns byte-identical 4727-byte renders; no 33881-byte asset reachable; wrote the structured probe record.
4. Verified no register row was touched (the supersede rule binds only on an exact-size hit, which did not occur); filed this receipt + LEDGER row + queue flip.

## Falsifier

Dies if: (a) a fetched file at exactly 33881 bytes for any of the 262 cites exists without a NEW dated superseding register row (re-run this probe after any Telegram Desktop export lands; the supersede row must be a new dated row, never an in-place edit); (b) any byte of media_recovered_register_20260926.jsonl changes without a supersede receipt naming it; (c) the probe record's measurements stop reproducing (e.g. the CDN later serves full-size from the same URLs, which would flip the verdict).

## Bibliography closed

Read whole: watch/inbox/burn_wave_20260926/B2_88_metadata_fetch_20260926.md (Verdict honest-limit + census lines), register rows for msg_id 176 class. Bytes: live HTTP measurements recorded above with sizes and shas; probe JSON on file. Nothing synthesized; unavailable arm named unavailable, not failed.
