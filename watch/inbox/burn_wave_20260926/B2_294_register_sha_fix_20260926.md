# B2-294 Autoseal over-256KB registers can never verify (SW-07, 2026-09-26)

## Verdict

LANDED (preventive: the disease had not fired yet -- zero '"size-only"' matches in index_events.jsonl at fix time). tools/md_record_seal.py register events now carry a value verify can check: real bytes hashed with one streaming read for everything up to the gate's own 8 MB cap, and the B2-156 living-style prefix seal (sha256 of exactly the first 262144 bytes, size-named) beyond it. The bare "size-only(>256KB)" token can no longer reach a register row. Probes: 300KB file hashes equal to the whole-file sha; 9 MiB live probe produces the exact living-style string; passthrough of an existing hash untouched. Suite: tests/test_md_record_seal.py 6 passed.

## Evidence file:line quotes

- QUEUE.md row: "tools/md_record_seal.py seal_line writes sha size-only(>256KB) for big files (:50) and the register event reuses it (:142), so the first hook-registered inbox file over 256KB mints an item whose registered sha is not a hash and fails verify forever".
- Pre-fix bytes: `"sha256": "size-only(>256KB)"` in seal_line, and the register built `"sha256": rec.get("sha256", "")` verbatim.
- New register_sha256() docstring (fix-comment law): "CAUSE: seal_line() writes the cheap token 'size-only(>256KB)' for big files and the register event reused it ... 0 such events exist today -- the fix is preventive. FIX: hash real bytes for the register (one streaming read, same 8 MB cap the gate enforces); only a file beyond that cap falls back to the B2-156 living-style prefix seal".
- Live probe (9 MiB, real bytes): `sha256(first 262144):31389c5ddf0f...@9437184B(living-style, B2-156)` verified equal to hashlib.sha256(blob[:262144]) with the exact size suffix.
- Tests: test_register_sha256_big_file_gets_real_hash (300KB -> whole-file sha), test_register_sha256_passthrough_and_living_fallback (hash passthrough; beyond-cap branch via a monkeypatched-down MAX_BYTES after the estate's watcher deletion quirk, named in the test docstring); pytest -q -> 6 passed.

## Work done

- tools/md_record_seal.py: register_sha256(path, rec_sha) helper (passthrough for real hashes; streaming whole-file hash <= 8 MB; exact-256KB living-style seal beyond) wired into the register row; seal_line's cheap autoseal token unchanged (the autoseal journal line is not a verified item; the register is).
- tests/test_md_record_seal.py: two new tests pinning all three branches.
- Process receipt per the no-fabrication law: the first monkeypatch test run failed with FileNotFoundError because my first appended test omitted the write_bytes line (an editing defect, found by the red run, fixed and re-run green); the earlier watcher-deletion hypothesis was wrong and is retracted here.

## Falsifier

Reopen if a register event with sha256 "size-only(>256KB)" or "unreadable" ever appears in watch/inbox/index_events.jsonl again (grep law: `grep -c "size-only" watch/inbox/index_events.jsonl` must stay 0 for register rows), or if test_register_sha256_big_file_gets_real_hash fails while the hook claims the law.

## Bibliography closed

Read: tools/md_record_seal.py (seal_line, gate guard, register block), tests/test_md_record_seal.py (fixtures + new tests), watch/inbox/LIVING_HASH_LAW_20260926.md (prefix-seal shape, cited from the B2-385 read this session), watch/inbox/index_events.jsonl (size-only census = 0). No external sources.
