# PA-S4verkle-grok47 (grok-4.7 @ xai, turn 1, channel: content)

STRANGER AUDIT, surface 4. Instrument: the four truncated evidence files (head 75% + tail 25%, moment 2026-10-01). Line numbers are UNVERIFIED because the replay stripped them. Claims below are tied to quoted bytes. Anything not in those bytes is marked UNVERIFIED.

Deliverable: `S4-VERKLE-JOINTS.spec` (one patch a seat can apply). Falsifier named at the end.

## 1. Attack surface map

Writer model (quoted, `00__verkle_knot.py`): v1 is the fail-closed default. "a re-save of an existing session replaces its row and rewrites the WHOLE chain file"; "Unknown/missing values fail closed to v1." A write-capable insider, or any tool that holds `verkle_lock` and rewrites `verkle_chain.jsonl`, can replace history. Amend-in-place is not a bug beside the design. It is the design.

What is undetectable from in-repo bytes alone: the witness module says so. Quoted, `02__tip_witness.py`: "the writer can rewrite the whole chain and no in-repo byte survives to contradict the rewrite." `chain_repair.py` then stamps the laundered row `chain_race_repaired` and refreshes the tip from the leaves now on disk. After that, a tip-only check agrees with the new story.

Witness: tip hash, not an interior witness. Quoted, `02__tip_witness.py` `load_tip`: it reads `root` and `n_leaves` from `verkle_tip.json` only. "tip-vs-chain consistency is AG5's job, not recomputed here." `compare` returns DIVERGENT only for shrink, or for same `n_leaves` with a different root. LAG is returned whenever `live["n_leaves"] > witnessed["n_leaves"]`, and that branch is before the same-count root check. Publish on LAG calls `patch_gist` and advances.

So the claim "interior rewrite plus recomputed tip is invisible" is half true:

- Same leaf count, recomputed tip, witness already published: NOT invisible. `compare` returns WITNESS-DIVERGENT ("same count ... but root differs"). Publish refuses. Caught, if a witness line exists.
- Interior rewrite, then one honest append, then publish: invisible to this witness. Count grew, so the verdict is LAG, not DIVERGENT. The gist advances onto the laundered tip. The ratchet never compared the old root to a prefix of the new chain.
- Tip file set back to the witnessed root while the jsonl interior differs: invisible here. This tool does not re-hash the chain. Whether AG5 fails that closed is UNVERIFIED (not in these bytes).
- No published witness: invisible. Quoted: gist WRITE was 403 on 2026-09-30; first real publish exits 2. External publish is still pending that flag. Until a gist line exists, there is nothing to diverge from.

`chain_repair.py` trusts `leaf_hash` fields already in the jsonl. Quoted: `hashes.append(str(r["leaf_hash"]))`, then `true_root = _merkle_root(hashes)` over every row with a leaf hash, then it overwrites `verkle_root`, `parent_verkle_root`, and `n_leaves` on the first mismatched row and atomically replaces the chain. It does not re-derive `leaf_hash` from knot bytes (that call is absent from this file). A subtle tool bug, or an insider, edits leaf hashes, runs repair, and the committed roots become "truth."

Lock (`00__verkle_knot.py`): `O_CREAT|O_EXCL` is real, but stale break unlinks the lock if mtime is older than 900s, or if `os.kill(owner, 0)` raises `ProcessLookupError`, `SystemError`, or `OSError`. A seat that can delete `memory/biography/.verkle.lock` becomes the writer. After that, knot unlink plus whole-file rewrite is atomic only against other lock-takers, not against the lock owner.

Parallel mutable history, same file: `latest_leaf_for_session` trusts the v2 pointer doc before the chain. Evolution replaces by `session_id` and keeps `series[-500:]`. Neither is covered by the gist line.

Grounding wave (`03__grounding_wave.py`): append-only hash chain with `src_sha256` on path-shaped evidence, checked at verify (EVIDENCE-MUTATED). That binds the files the row names. It does not, in the bytes shown, store a Merkle inclusion proof into the verkle list. A wave row that cites a tip root or a knot path still verifies after an interior chain rewrite if those cited bytes were updated to match, or if the citation was only the tip. Full wave-to-verkle binding is UNVERIFIED past the truncation.

Positive (would be caught): shrink the chain under a live gist (DIVERGENT). Same-count root swap under a live gist, if publish is not forced (DIVERGENT, publish refused). A v4 wave row whose evidence file bytes change and whose `src_sha256` is left stale (EVIDENCE-MUTATED).

Negative (missed): rewrite interior leaf hashes, recompute roots, append one leaf, publish (LAG advances). Edit knots and leaf hashes together, run `chain_repair` (roots rewritten to match). Point the tip file at the old root while the jsonl differs (this tool never opens the jsonl). Publish never succeeded (no external byte).

## 2. Three weakest joints

1. Witness growth exception. `02__tip_witness.py`, `compare`, then publish-on-LAG (`patch_gist`). Quoted LAG branch and "witness advances on leaf-count growth only." Rank 1 because it is the only external checkpoint, and one append hides a full interior rewrite.

2. Repair and amend trust the leaves they are supposed to protect. `01__chain_repair.py` `find_bad_tail_index` / `repair` (quoted `leaf_hash` walk and root rewrite). `00__verkle_knot.py` `chain_mode` v1 whole-file rewrite (quoted). Rank 2 because it converts a tamper into a stamped consistent chain.

3. Tip file is the witness's entire world, and the lock is stealable. `02__tip_witness.py` `load_tip` (quoted: tip file only). `00__verkle_knot.py` stale-unlink on `OSError`/`SystemError` (quoted). Rank 3 because a lying tip plus a stolen lock makes joint 1's MATCH path lie even without a clever rewrite. Pointer-before-chain (`latest_leaf_for_session`, quoted) is the same class: an O(1) doc can disagree with the tape and win.

## 3. Patch spec (apply as-is)

File targets are the live modules these evidence copies came from (`mag/verkle_knot.py`, `tools/chain_repair.py`, `tools/tip_witness.py`). Do not patch the autopsy copies.

Joint 1 and 3, `tools/tip_witness.py`:

- Add `require_chain_root(chain_path) -> (root, n, prefix_roots)` that replays leaf hashes with the same `_merkle_root` the chain uses, and refuses if `verkle_tip.json` root or `n_leaves` disagrees. Witness never reads the tip file alone.
- Change `compare` so LAG is legal only if `witnessed["root"]` equals `prefix_roots[witnessed["n_leaves"]]` (the Merkle root of the first `n_witnessed` current leaves). If the prefix root differs, return DIVERGENT even when live count is larger. Same-count root mismatch stays DIVERGENT.
- Publish refuses unless that prefix check passed. Do not `patch_gist` on bare count growth.
- Persist the gist id outside the repo the writer rewrites (operator copy). In-repo `tip_witness_state.json` is not the trust root; the gist body is.

Joint 2, `tools/chain_repair.py` and `mag/verkle_knot.py`:

- Repair may recompute a row root only from knot-file bytes via the existing leaf hash function, not from the `leaf_hash` string in the jsonl. If the knot file is missing or its hash disagrees with the row, exit 1 and do not rewrite roots.
- Repair may fix only a tail row whose prefix (rows `[:bad_i]`) already matches committed roots. It must not set `bad["verkle_root"]` to the full-chain root when `bad_i` is not the last row. Quoted bug: `true_root = _merkle_root(hashes)` uses every leaf, then writes that into `rows[bad_i]`.
- v1 amend stays until migration, but each amend appends an external note (same gist channel) of `(session_id, old_leaf_hash, new_leaf_hash, old_root, new_root)` before the chain replace. No note, no amend.

Joint 3 lock, `mag/verkle_knot.py` `verkle_lock`:

- Do not treat bare `OSError` as "owner dead." Unlink only on `ProcessLookupError` plus the documented Windows `SystemError` (WinError 87), and only if the lock body pid matches. Log the break to the witness channel.

Not in this patch: per-era frozen snapshots are the right long-term store (copy `verkle_chain.jsonl` and tip to a content-addressed object every N leaves, witness that object hash). Interior-tree witnesses are the same idea as the prefix-root check above; do that first. It is smaller and falsifiable. Frozen copies without the prefix check still lose if the snapshot job is the same writer.

## 4. Restore drill

No restore-drill receipt, command, or result is in these four files. What the drill proved is UNVERIFIED. Do not treat a green `chain_repair` post-verify as integrity: quoted post-verify calls `_verify_chain_consistent` after rewriting roots to the leaves just read, so it proves internal agreement of the current file, not that those leaves are the ones previously witnessed.

What these bytes do prove: consistency after repair means "roots match leaf_hash fields now on disk," not "history matches an external checkpoint." What they do not prove: knot bytes match leaf hashes, tip matches chain (witness does not check), a published gist exists, or a restore reproduced a prior era.

Falsifier for this spec: fixture with 3 leaves, publish witness at n=3, replace leaf 1's `leaf_hash`, append leaf 4, recompute tip. Current `compare` returns LAG. Patched `compare` must return DIVERGENT and must not call `patch_gist`. If that test returns LAG, this audit is wrong or the patch was not applied.
