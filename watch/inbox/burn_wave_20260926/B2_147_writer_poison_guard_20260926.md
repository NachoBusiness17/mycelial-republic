# B2-147 Writer-side poison guard, 2026-09-26

## Verdict

LANDED. scripts/index_fold_host.mjs add/invalidate no longer MINT outside events: a new writerGuard(file, op) runs the argv path through the fold's OWN normalizer (normInboxFile, hoisted to module scope so writer and reader share one source of truth) and DIES before appendOp when the normalized path matches OUTSIDE_RE or has no inbox-relative form (drive letter, dot-dot, empty). No new watch/ or repo-root poison can be appended; the read side is unchanged, so legacy poison in the log stays counted on the B2-40 fold-warning channel exactly as before. Proven in a throwaway INDEX_INBOX_DIR sandbox this lane: add of mag/verkle_knot.py dies exit 1 with "refusing to append an outside event: normalized path mag/verkle_knot.py matches OUTSIDE_RE" and the events file is never even created (guard fires before any write); invalidate of watch/poison.md dies the same way; the happy paths still work (sandbox add of an inbox file appends seq and folds, invalidate of an inbox-relative name appends and deactivates). node --check clean; production read side byte-behaves as HEAD (verify MISSING-set diff against HEAD's script shows only concurrent-lane registrations landing between runs, base set identical).

## Evidence file:line quotes

- scripts/index_fold_host.mjs header (post-edit): "Writer-side poison guard (2026-09-26 B2-147): add/invalidate DIE before appendOp when the argv path, normalized by the fold's own normInboxFile, matches OUTSIDE_RE or has no inbox-relative form ... the read side still folds and counts legacy poison on the B2-40 warning channel, unchanged."
- Hoist block (post-edit): "B2-147 2026-09-26: hoisted to module scope (were readEvents-local) so the WRITER side (add/invalidate) shares one source of truth with the fold's read side: the writer guard must normalize and classify with the exact bytes the fold will use, never a drifting copy." followed by the verbatim-moved normInboxFile, OUTSIDE_RE, isUnresolved definitions.
- writerGuard: `if (OUTSIDE_RE.test(p)) { die(op + ": refusing to append an outside event: normalized path " + p + " matches OUTSIDE_RE (B2-147 writer guard); inbox files only"); }` plus the isUnresolved arm; wired as `writerGuard(file, 'add');  // B2-147: die before appendOp on outside/unresolved` after the existsSync check in add, and the same call in invalidate after the file check.
- Sandbox runs (this lane, throwaway INDEX_INBOX_DIR): "ERROR: add: refusing to append an outside event: normalized path mag/verkle_knot.py matches OUTSIDE_RE (B2-147 writer guard); inbox files only" exit 1, events file absent (never written); "ERROR: invalidate: refusing to append an outside event: normalized path watch/poison.md matches OUTSIDE_RE" exit 1; happy paths: "add: appended seq 1 for ...note.md -> 1 active items" exit 0 and "invalidate: appended seq 2 for note.md -> 0 active items" exit 0.
- Read-side parity: `node /tmp/fold_head.mjs verify` (HEAD bytes) vs working-tree verify MISSING sets diffed: base identical (CAPTION_LEDGER missing entry present in BOTH, a pre-existing concurrent-seal condition also visible in B2-90's receipt notes), delta only new registrations landed by concurrent lanes between runs (INDEX.json self-class, SHARED_SURFACE_CONTRACT.json, B2_467, fullsend_s2 wave files from a live lane).
- Pointer: watch/inbox/burn_wave_20260926/B2_40_fold_poison_guard_20260926.md (the read-side warning law this lane extends to the writer side).

## Work done

- Claim law: fresh CLAIM SW-00 line for scripts/index_fold_host.mjs (still working-tree-modified; first two append attempts hit a concurrent QUEUE.md write and were retried until landed), retired at landing; bytes re-read after claim.
- Read the read-side normalizer/OUTSIDE_RE/isUnresolved and both CLI mint paths (add, invalidate) in current bytes.
- Refactor: hoisted normInboxFile + OUTSIDE_RE + isUnresolved from the readEvents closure to module scope verbatim (single source of truth for both sides); added writerGuard with a dated law comment; wired into add and invalidate before appendOp; documented the law in the module header.
- Tested in a sandbox (never the production log): two die arms, two happy arms, events-file-untouched proof on the die path; node --check; read-side parity check against HEAD's own bytes over the production log (read-only verify).
- Em-dash: added lines carry one em-dash only as a verbatim MOVE of the pre-existing "// place they all get canonicalized -" comment line from the closure (no new em-dash prose introduced); receipt em-dash 0.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Any new event in watch/inbox/index_events.jsonl appended AFTER this landing whose normalized path matches OUTSIDE_RE kills the guard claim (check the log tail for new watch//mag//scripts/-prefixed registers; seq and ts make new rows identifiable).
- A writer bypassing this script (Python appenders, raw shell appends) is out of the guard's reach by design; the read-side B2-40 warnings remain the counter, and any such append is visible there.
- If the hoisted normalizer's behavior ever diverges from the fold's usage (e.g. someone re-copies a local variant into readEvents), the single-source law is broken and the guard can be bypassed by a normalization gap.
- Re-running the sandbox matrix above must reproduce die/die/pass/pass; a pass on an outside path or a die on an inbox path inverts the verdict.

## Bibliography closed

scripts/index_fold_host.mjs (pre-edit readEvents closure, add, invalidate; post-edit whole-file syntax and behavior); watch/inbox/burn_wave_20260926/B2_40_fold_poison_guard_20260926.md; QUEUE.md B2-147 row and claim lines; sandbox probe transcripts quoted above; verify parity diff (HEAD bytes vs working tree over the production log). No web sources. Em-dash count 0 in this receipt.
