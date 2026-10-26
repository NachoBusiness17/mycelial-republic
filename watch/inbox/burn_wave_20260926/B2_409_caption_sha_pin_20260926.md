# B2-409 receipt (2026-09-26)

## Verdict

LANDED. The have-row sha invariant of CAPTION_LEDGER_20260926.jsonl is now enforced by a named drift detector: tools/caption_ledger_sha_check.py recomputes every have-row sha256 from disk bytes and fails naming path + ledger sha + disk sha, and it is wired into the B2-12 builder as a post-write gate (next to the B2-421 caption_via gate), so no rebuild can land with a drifted hash again. Full live run: 2689 have-rows hashed, 37 metadata-only, 0 mismatches, 0 missing, PASS.

## Evidence file:line quotes

- The invariant's bytes at land time: watch/inbox/CAPTION_LEDGER_20260926.jsonl holds 2726 rows, 2689 have-rows (path present), ALL 2689 carrying sha256 (the B2-89 backfill state; the brief's 2375 was the count at B2-89 time, the ledger has since grown - named, not silently mixed), 37 metadata-only rows.
- tools/caption_ledger_sha_check.py (new): recompute-and-name check; relative paths resolve under watch/inbox/mrpool_export (proven: 497/497 of the first 500 rows resolve there); mismatch/missing/bad-row each produce named lines (line number, path, ledger sha prefix, disk sha prefix) and exit 1; a DRIFT LAW note names the re-audit steps (B2-89 provenance + named byte audit).
- Falsifier replay (scratch copy, real bytes): copied media_recovered_20260926/msg_176.jpg to a temp root, flipped exactly one byte (data[0] ^= 0xFF), built a 2-row scratch ledger, ran the check: "mismatches 1 ... line 1: media_recovered_20260926/msg_176.jpg DRIFT ledger=66268013e17b0727... disk=922520b42f696183...", exit 1. Before this gate, running "every current check" against such a flip named nothing (the builder verified register-supplied shas only at build time; the verifier family over q_caption_ledger is a different ledger).
- Wiring: watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py after the B2-421 gate: subprocess call to tools/caption_ledger_sha_check.py --ledger OUT, nonzero exit fails the rebuild with "have-row sha check FAILED"; builder py_compile clean. The B2-12 script was last touched by the B2-421 lane (its gate block sits directly above; rebased on those bytes).

## Work done

1. Censused the live ledger (2726/2689/2689/37) and proved the path base root by sampling.
2. Landed the check script with named-failure output, metadata-only handling, and a --limit scratch arm.
3. Proved the falsifier replay on a one-byte-flipped scratch copy (exit 1 naming the DRIFT).
4. Wired the gate into the builder after the existing post-write gate, per "wired wherever the ledger is rebuilt".
5. Full live run over all 2689 have-rows: PASS (0 drift on disk right now).

## Falsifier

The brief's falsifier ("flip one byte in a scratch copy of a hashed media_full file, run every current check, and none names the drift") is dead for this class: the replay above shows the named DRIFT line and exit 1, and the same gate runs on every rebuild. The gate falsifies itself if the export root moves (relative resolution misses; the missing-file arm names the path so the move is loud) or if rows are added without sha256 (the bad-row arm names them). Named limit: the check hashes disk bytes against ledger sha; it cannot detect a coordinated drift where both the file and the ledger row are rewritten together - that requires an external anchor and is filed as the standing residual, not hidden.

## Bibliography closed

- watch/inbox/CAPTION_LEDGER_20260926.jsonl (2726 rows read; UNMODIFIED)
- tools/caption_ledger_sha_check.py (new); watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py (gate wired after B2-421's)
- watch/inbox/burn_wave_20260926/B2_89_caption_ledger_sha_fill.py + B2_89_hash_backfill_20260926.md (the backfill whose invariant is pinned)
- watch/inbox/burn_wave_20260926/B2_12_caption_ledger_20260926.md; B2_259_pin_law_20260926.md (maintenance law shape)
