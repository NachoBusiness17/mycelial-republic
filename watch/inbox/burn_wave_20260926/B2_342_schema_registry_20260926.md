# B2-342 events key schema registry, 2026-09-26

## Verdict

LANDED. The writer-key schema of watch/inbox/index_events.jsonl is now owned by a spec: configs/events_key_schema.json (events_key_schema.v1) registers every known writer key with its census count, first-seen line, first-seen seq (decimal string per the B2-40 scheme), first-seen ts, owning writer and a carries note, over a recorded log sha256. The schema is gated on both surfaces that read it: mag.shared_surface validate ERRORS on any event key outside the registry (mag/events_key_schema.py scan, wired at mag/shared_surface.py inspect_surface), and every fold run of scripts/index_fold_host.mjs WARNS on the same keys on the WARN + exit-2 fold_warnings channel. 49 tests pass across the three touched suites; ratchet check --changed NEW=0. The brief's falsifier was executed on both sides on throwaway bytes: a fresh key appended today is NAMED by validate and named by the fold.

## Evidence with file:line quotes

Census (byte scan, strict json.loads with NaN/Infinity rejected, the same semantics as scan_events_log and JS JSON.parse):

```
log sha256: ab7f6cdebb2748d5391d2815fad08d82e32100be2ac3153483ecab940fe939fb
lines(non-blank): 3484 parseable: 3481 skipped: 3 [(94, 95, 96 = the B2-42 grandfathered lines)]
distinct keys: 30
```

The 30-key set is identical to the B2-329 SCHEMA block in watch/inbox/burn_wave_20260926/B2_329_dump_strict_consumer.mjs (lines 27-58); counts grew with the 41 events landed since that census (log sha cfd3b2dd... then, 3443 lines). Raw census: B2_342_key_census_raw.json. Owning-writer highlights: writer and nonce first seen line 27 (EXP-002A genesis note, seq 27); cls first seen line 3139 and cls_key_disclosed line 3141 (zcode-seat-20260926, the class-alias slip that folds UNPROVEN); living/size line 3090 and seal line 3094 (zcode-b2-156-living-hash-law); the core keys seq/ts/op/file/sha256/class/purpose first seen line 1 seq 1, before the writer convention existed (first_writer recorded null, not guessed).

Gate, python side (mag/shared_surface.py):

```
:247  f"NEW event key in index_events.jsonl: {rec['key']!r} x{rec['count']} "
:248  f"(first line {rec['first_line']}, seq {rec['first_seq']!r}, "
:249  f"writer {rec['first_writer']!r}): register it in "
:250  f"configs/events_key_schema.json with first-seen evidence or fix "
:355  "events_log_keys": {
```

Gate, node side (scripts/index_fold_host.mjs):

```
:169  const KEY_SCHEMA_URL = new URL('../configs/events_key_schema.json', import.meta.url);
:394  `unknown event key not in configs/events_key_schema.json: ${k} x${rec.count} ` +
:499  fold_warnings: [...nonceWarnings, ...outsideWarnings, ...unresolvedWarnings, ...inexactWarnings, ...unknownKeyWarnings],
```

Real-surface validate (B2_342_validate_after.json): events_log_malformed {total: 3, grandfathered: 3, new: 0}; events_log_keys {lines_scanned: 3483, unknown_keys: 0}. The 3 errors in that capture (hash mismatch INDEX.json, REJECTION_TAXONOMY_20260917.md, BURN_JUDGE_LANE_BUILD_20260925.md) are concurrent-lane drift, the same class B2-42 filed as not-mine. Cross-check: the B2-329 strict consumer stays green over the fresh dump: `PASS: 3483 lines checked, 0 unknown key(s)`, fold skips exactly 94,95,96 (B2_342_strict_consumer_result.json), so the two schemas agree and this lane introduced no log drift.

## Work done

1. configs/events_key_schema.json (spec first): events_key_schema.v1, 30 entries with count, first_line, first_seq (decimal STRING or null per the B2-40 seq scheme, so past-2^53 literals never truncate through float64), first_ts, first_writer, carries; reserved-prefix rule (underscore = fold-internal per B2-329); closed-vocabulary-not-required-fields rule; census block naming the log sha.
2. mag/events_key_schema.py: gate module (load_event_key_registry, scan_event_keys, reject_json_constant). scan skips malformed and blank lines exactly like scan_events_log, skips JSON scalar lines, exempts underscore keys, and returns one record per DISTINCT unknown key with count, first line, first seq, first writer.
3. mag/shared_surface.py: docstring spec section (Events key schema, B2-342); inspect_surface wiring (NEW key = ERROR one per distinct key; missing or shape-invalid registry = ERROR; events_log_keys {lines_scanned, unknown_keys} added to status); names re-exported for tests. Landed as an inline block first, which pushed the module to 447 lines and the ratchet filed file-too-long NEW debt; extracted the module instead of registering the debt (shared_surface.py now 388 lines, ratchet NEW=0).
4. scripts/index_fold_host.mjs: header spec block (lines 82-97); script-relative registry loader (lines 165-181, import.meta.url-relative so throwaway INDEX_INBOX_DIR test inboxes gate against the real vocabulary); fold() unknown-key warnings on the existing counted WARN + exit-2 channel (lines 371-402, one per distinct key with count and an example event naming seq and writer; disabled-gate warning if the registry is unreadable); appended to fold_warnings at :499. First cut compared a Set with .length (always undefined, gate silently disabled); the new exit-0 pins caught it before landing.
5. tests/test_events_key_schema.py: 11 pins (new key errors with first-seen evidence, registered keys clean, underscore exempt, missing registry errors, shape-invalid registry errors, malformed lines skipped, closed-not-required-fields, real registry covers the real log, real registry evidence shape, loader rejects shape drift). tests/test_index_fold_host.py: 3 pins appended (unknown key warns + exit 2 + lands in INDEX.json fold_warnings; registered keys produce no warning; underscore plumbing keys never trip it). 49 passed across the three suites; full targeted command: pytest tests/test_events_key_schema.py tests/test_index_fold_host.py tests/test_shared_surface_events.py -q.
6. Board: 4 CLAIM lines filed before each edit (17:22:09Z and 17:29:13Z), flipped to CLAIMED at landing; B2-358 landed an env-redirect tripwire in mag/shared_surface.py mid-lane at 17:2xZ, detected by the Edit tool's stale-byte check, rebased on the fresh bytes per the claim law.

## Falsifier

- Executed, python gate: a writer appended an event carrying fresh key `unregistered_probe_key_20260926` today (throwaway surface, B2_342_falsify_python.py) and validate NAMED it: `NEW event key in index_events.jsonl: 'unregistered_probe_key_20260926' x1 (first line 1, seq 1, writer 'b2-342-falsifier')` (B2_342_falsify_python_out.txt, exit 0 = law holds). If a fresh key appended today produces no validate error, this gate is broken.
- Executed, node gate: `fresh_key_not_in_registry` appended to a throwaway log; rebuild printed `WARN: unknown event key not in configs/events_key_schema.json: fresh_key_not_in_registry x1 (e.g. seq 2, writer rogue-writer)` and exited 2 (B2_342_falsify_node_out.txt).
- Registry row side: every key in the real log is a registry row (test_real_registry_covers_every_key_in_the_real_log over the real bytes); the registry itself names all 30 keys with first-seen evidence.
- If a fresh key lands and neither gate names it while the registry file parses, the most likely cause is the loader class bug class (Set.size vs array.length bit me once here); the exit-0 control pins exist to catch exactly that.

## Bibliography closed

configs/events_key_schema.json; configs/events_malformed_baseline.json (format precedent); mag/events_key_schema.py; mag/shared_surface.py; scripts/index_fold_host.mjs; tests/test_events_key_schema.py; tests/test_index_fold_host.py; tests/test_shared_surface_events.py; watch/inbox/index_events.jsonl (census over full bytes, first-seen lines 1, 27, 29, 42, 48, 55, 216, 338, 930, 1408, 1421, 3090, 3094, 3139, 3141); watch/inbox/INDEX.json (cls-alias UNPROVEN evidence); watch/inbox/burn_wave_20260926/QUEUE.md (law block, claims, landing); watch/inbox/burn_wave_20260926/B2_329_dump_strict_consumer.mjs (SCHEMA block + fresh consumer run); watch/inbox/burn_wave_20260926/B2_42_events_hygiene_20260926.md (pattern + baseline spec); watch/inbox/burn_wave_20260926/B2_342_key_census_raw.json; B2_342_validate_after.json; B2_342_falsify_python.py; B2_342_falsify_python_out.txt; B2_342_falsify_node_out.txt; B2_342_strict_consumer_result.json; memory/burns/LEDGER.jsonl.
