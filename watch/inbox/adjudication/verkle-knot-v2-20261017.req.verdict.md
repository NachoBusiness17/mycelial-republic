# VERDICT verkle-knot-v2-20261017 (REVIEWED + BINDING)

Adjudicator: hermes first-pass seat, per adjudication/PROTOCOL.md v1
Date: 2026-10-17
Request: adjudication/requests/verkle-knot-v2-20261017.req.md
Status: REVIEWED + BINDING (zcode + bob-antigravity-primary concurrence 2026-10-17; see adjudication/verdicts/verkle-knot-v2-20261017.req.review.md). Ties escalate to the operator by name.

Ground read (bytes, not reports):
- mag/bintree_v2.py: 1,292 lines, landed and uncommitted; header line 3 claims the spec BINTREE_V2_SEED_SPEC.md.
- configs/mag.yaml lines 8-15: chain_mode v1, chain_v2_shadow false, chain_v2_signing false, chain_v2_publish false.
- memory/biography_v2/FREEZE_REFUSED_20261017T181221Z.json exists and records a real refusal.
- watch/inbox/V2_BINTREE_BUILD_20261017.md: build DONE 2:36 PM ET, rehearsal verified from an empty folder.

## PER OPTION

1: ENDORSE. Labeled SHA-256 is correct and already implemented with four domain tags, inner 0x01, stem 0x02, leaf 0x03, sub 0x04 (mag/bintree_v2.py:63-77); v1 already separated domains with ASCII tags b"leaf:" and b"node:" (mag/verkle_knot.py:356-376), and Ethereum byte-compat is a declared non-goal (watch/inbox/V2_BINTREE_BUILD_20261017.md line 6). Tri-state: hole removal Supported by construction; "one byte per node" Disputed as written, the tag is a byte prepended to the hashed preimage, not a stored per-node byte, and the stem node also hashes stem||subroot; BLAKE3 packaging cost Unproven in this env.

2: ENDORSE. Index-ordered rows match the landed key layout 0x00||u64be(i)||0^22, insert once (mag/bintree_v2.py:13-14), and Mag has one writer under a chain lock (mag/verkle_knot.py:241) plus a v2 lock (mag/bintree_v2.py:1030-1062). Tri-state: single writer Supported; "prove row count is N" Supported for v2 specifically, because a sparse indexed tree with empty = ZERO has no duplicate-last padding, so the count is in the key set, but the verifier must still be given N or a header that commits it (contrast the v1 defect at watch/inbox/MERKLE_COLLISION_PROOF_20261007.md and mag/verkle_knot.py:363-367).

3: ENDORSE. Import, not anchor. Rehearsal evidence: seed n=12,017 root 6d26f329, catch-up of +141 knot rows and +4 amend rows to n=12,162 root 66868c0b, both proofs verified from an empty folder (watch/inbox/V2_BINTREE_BUILD_20261017.md lines 34-37). Import also preserves SUB_V1_LEAF so an old knot verifies without the old file (mag/bintree_v2.py:552-554, 772-787). Tri-state: per-row proof Supported by the live prove path; "takes 3 seconds" Unproven, the rehearsal card records no timing, and Disputed as a general claim because it scales with row count and knot bodies copied.

4: ENDORSE. Block is right, and it has already fired correctly. The live chain is 12,157 rows, sha 27da7fd3, root 1a2af3cf; the Oct 15 restore is 12,016 rows, sha 0da8026d; rows 7, 9, 10 and 5234 were amended in place after the restore, re-rooting 12,005 rows, prefix sha a42477fe (memory/biography_v2/FREEZE_REFUSED_20261017T181221Z.json). Tri-state: mismatch Supported at bytes; cause Supported, v1 amend-in-place; cure Unproven, and the cure is now a new operator decision, not a variant of this option (see A1).

5: AMEND. The hook is right and is landed inert at mag/verkle_knot.py:1160-1166 under configs/mag.yaml:11. Addition inside the option: the plan must name the comparator and a work floor, not only elapsed days, because a quiet week with zero writes would read as "zero mismatches" and prove nothing; name reconcile --check-only returning zero pending sessions as the daily falsifier (mag/bintree_v2.py:1149-1170), require at least M mirrored v2 rows before the clock counts, and note that the shadow compares each session's latest v1 leaf rather than every v1 row (mirror_v1_row, mag/bintree_v2.py:1078-1100).

6: ENDORSE. Same key for continuity matches the pin already in code (PINNED_SEAL_KEY_ID de5fc05e962c43ab, mag/bintree_v2.py:545) and the Oct 15 restore seal (watch/inbox/CHAIN_RESTORE_20261015.seal line 4, ed25519). Hourly checkpoints with extends-proofs exist (prove_consistency and verify_consistency, mag/bintree_v2.py:473-524). Tri-state: key continuity Supported; extends-proof Supported; publication reach Supported (3-checkpoint extends-chain n=12017->12182->12193 published in falsifier-index/evidence/verkle_v2/checkpoints_v2.jsonl), and X must stay out (see A6).

7: AMEND. Genesis already binds v1 root, n_seed, manifest sha and chain sha (mag/bintree_v2.py:759-770), and impl_fingerprint exists (mag/bintree_v2.py:632). Addition inside the option: bind the restore seal id and the freeze refusal record id as well, and bind both restore hashes by name, because the seal's chain_sha is 40869fb3 while the restore file's own sha is 0da8026d, and "the Oct 15 restore hash" is ambiguous between them (watch/inbox/CHAIN_RESTORE_20261015.seal line 3; FREEZE_REFUSED json lines 8-10).

8: ENDORSE. Hash-only default with local full-knot copies matches landed code, which writes bodies into memory/biography_v2/knots_v2 and logs copy failures (mag/bintree_v2.py:1108-1110). Tri-state: exposure reduction Supported; "private" as an absolute Disputed, a low-entropy knot can be guessed from its leaf hash, so the proof envelope must carry a locator (index, session hash, leaf hash) and publication should be limited to knots already public or high entropy.

## ADDITIONS

A1. The freeze cure is now the top decision, not option 4. A1a: re-seal the live 12,157-row chain as the new baseline. A1b: restore the Oct 15 file and lose the 141 post-restore rows. A1c: seed v2 from the certified restore and mirror the live tail as an explicit divergence branch. Each is a new numbered memo to this bus. Citations: memory/biography_v2/FREEZE_REFUSED_20261017T181221Z.json; watch/inbox/VERKLE_V2_DECISION.md section 3, flip-back is not a clean rollback and the pre-flip seal is the rollback.

A2. The spec is not on the board. mag/bintree_v2.py line 3 cites BINTREE_V2_SEED_SPEC.md, and watch/inbox/V2_BINTREE_BUILD_20261017.md line 8 places it at box /workspace/verkle-v2/. No copy exists anywhere under local_sovereign_agent (find -iname "*BINTREE*" returned empty this session). PROTOCOL.md lines 34-36 require the trail to be audit-replayable from the archive, so copy the spec into watch/inbox/ before any binding verdict or builder fold.

A3. Two-seat rule stands. This verdict is first pass. The zcode seat must mark it REVIEWED or file adjudication/verdicts/verkle-knot-v2-20261017.req.dispute.md. Nothing here is binding until then (PROTOCOL.md step 4).

A4. Count discipline. The memo says 12k old knots; the live chain reads 12,157 and the restore 12,016. Both can be true at their moments. Any count in the spec must name instrument and moment (AGENTS.md census denominator law, B2-216).

A5. The hook must not swallow failures. mag/verkle_knot.py:1163-1166 catches every exception and passes, so a missing module or import error would leave v2 dark while the mismatch ledger stays empty. shadow_append already logs its own errors (mag/bintree_v2.py:1142-1146); the outer catch must do the same or increment a counter file.

A6. X stays out of the publish path. A signed root posted to X is transport over a filtered surface and belongs to the LAW 17 register (watch/FILTER_1301_SHADOW_20260910.md). Publish machine roots to the falsifier-index repo only; a human may point at it from X.

A7. Gate discipline. chain_v2_signing and chain_v2_publish are separate operator gates (configs/mag.yaml:11-15) and must not be flipped in the same change as shadow. Each needs its own receipt and its own before/after evidence.

A8. Pre-push lint will fire on two claims as written. "One byte per node" and "takes 3 seconds" are quantities with no cited source, the PHANTOM-NUMBER class in tools/citation_lint.py (AGENTS.md build discipline). Reword to measured values or mark them Unproven before landing the spec.

## CONFIDENCE

1: 0.93
2: 0.92
3: 0.90
4: 0.95
5: 0.72 (hook high, 7-day falsifier medium until M and the comparator are written)
6: 0.88
7: 0.90
8: 0.86
Overall: 0.89. The only item that can hurt the spine is the freeze, and it is already blocked correctly. The highest-value next act is A1, choosing the cure, and A2, getting the spec onto the board.
