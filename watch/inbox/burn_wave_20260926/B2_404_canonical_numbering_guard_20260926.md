# B2-404 receipt: qdrop local-row to canonical-numbering guard (2026-09-26, lane SW-03)

## Verdict

LANDED. watch/inbox/qdrop_export/qdrop_canonical.py resolves drop numbers from id plus ts only, refuses position/ordinal lookups by construction, and refuses to mint canonical numbers without a receipt-anchored pair: id-keyed anchors carry only the two byte-verified pairs (580331 -> canonical #874, 967331 -> #1104); every other row resolves to its LOCAL drop_no with canonical=None, canonical_anchored False, and an explicit warning. The line-6423 counter shape rerun through q_authored_ordinal_guard(874) no longer yields a bare "Q drop #874": it names the row (local drop_no 1406, id 967331, canonical #1104) and carries the mandatory guard warning naming the line-6423/B2-93 trap; the CLI demo exits 2 on conflation. 7/7 tests pass. A significant discovery is filed with the guard: qdrops.jsonl's drop_no FIELD is itself a local renumbering (local 1088 carries the Snowden HK post = canonical #874; B2-67 proved the field divergence), so any script printing the field as "drop #N" has been printing local numbers all along.

## Evidence file:line quotes

- memory/runs/compaction_eval/steps_frozen_20260920.jsonl:6423 (the counter shape, read this lane): "if r.get(\"trip\") == \"!!Hs1Jq13jV6\" or (r.get(\"name\") or \"\").strip() == \"Q\": n += 1; if n == 874: print(\"Q drop #874\" ..." with output "Q drop #874 date: 2018-04-09 ... Think 'Bridge'".
- watch/inbox/burn_wave_20260926/B2_93_stego_erratum_20260926.md:12 (root cause): "The command counted the 874th Q-authored row, not canonical drop #874; that conflation is where the wrong number was minted"; :13: "canonical drop #874 is the Snowden HK post (8ch post 580331, 2018-03-07) ... the central-algorithm post is drop #1104 (post 967331)".
- Live bytes (this lane): qdrops.jsonl row with id 580331 (Snowden HK, ts 2018-03-07T20:56:26) carries drop_no 1088; row with id 967331 (Think 'Bridge', ts 2018-04-09T17:09:25) carries drop_no 1406; 6,242 rows total.
- watch/inbox/qdrop_export/media_register.jsonl:119-120 (post-B2-367 shift): "{\"drop_no\": 874, \"id\": \"299177\", \"url\": \"https://media.8ch.net/...\"}" (the media register's own parallel id space; urls are media.8ch.net, the brief's "lines 118-119" cite shifted +1 by the B2-367 scope header).
- QUEUE.md B2-404 row (the falsifier): "rerun the line-6423 counter shape and it still prints 'Q drop #874' for the Think Bridge post with no guard warning".

## Work done

- watch/inbox/qdrop_export/qdrop_canonical.py (new): canonical_drop_no(id, ts) resolver (both fields required; ts must prefix-match; unknown/ambiguous ids raise), CANONICAL_ANCHORS table limited to the two receipt-anchored id pairs, q_authored_ordinal_guard(nth) replicating the line-6423 shape with the mandatory warning, drop_label() as the only sanctioned "drop #N" printer (fields, never positions; unanchored rows labeled "canonical number unanchored"), and a --guard CLI (exit 2 on conflation).
- Correction of my own first draft, filed: v1 of the anchor table included two ids I had inferred from B2-67's local-to-q_num pairs without byte verification; removed before landing (an unverified id in the anchor table would mint exactly the class of wrong number this guard exists to stop). B2-67's remaining pairs are recorded in the module comment as unanchored-by-id, awaiting content-match verification.
- tests/test_qdrop_canonical.py (new, 7 tests): Snowden anchors to #874 with local 1088 named; Think Bridge anchors to #1104 with local 1406; unanchored rows refuse a canonical number (None + warning + label); resolver refusals (missing ts, ts mismatch, unknown id, position); the line-6423 shape rerun with guard warning and canonical #1104; label signature takes fields only; CLI conflation exit code.

## Falsifier

The brief's falsifier, closed: rerunning the line-6423 counter shape through the guard now warns and resolves instead of printing a bare "Q drop #874" (test_line_6423_counter_shape_now_carries_the_guard_warning; CLI exit 2). Kills going forward: (a) an unanchored id appearing in CANONICAL_ANCHORS (the table's comment names the bar: content-match verified or it does not enter), (b) any consumer printing "drop #N" from enumerate/ordinal positions instead of the resolver (the guard warning instructs the fix; a new index-walking script is caught only if routed through the helper, so the pin test plus this receipt are the review hook), (c) the anchor table contradicting a RECEIPT.json/B2-14 correction byte (re-verify on any qdrop_export re-export).

## Bibliography closed

- memory/runs/compaction_eval/steps_frozen_20260920.jsonl:6423 (the counter shape, read)
- watch/inbox/burn_wave_20260926/B2_93_stego_erratum_20260926.md (erratum wave, root cause, correcting authorities)
- watch/inbox/qdrop_export/qdrops.jsonl (6,242 rows; id/ts/drop_no fields verified for the anchored pairs)
- watch/inbox/qdrop_export/media_register.jsonl:119-120 (parallel id space, post-shift lines read)
- memory/corpus/LINKS.jsonl STEGO-PASS1-QDROP874-CORRECTION (via B2-93's citation; the correcting authority for the anchor pairs)
- watch/inbox/burn_wave_20260926/B2_367_media_register_scope_20260926.md (the +1 line shift this receipt inherits)
- tests/test_qdrop_canonical.py (new)
