# AH2 — real signatures for the "signed proof" (audit finding #8, refired 2026-09-30)

**Owner lane:** `mag/proof.py` + tests + this receipt. **Finding:** the proof module's
"signature" was an UNKEYED sha256 — anyone could forge a `claim_hash` — while
cryptography 49.0.0 sat installed in the venv (verified: `49.0.0`).

## What landed

**Already committed when this refire opened** (prior lane, verified in tree):
`mag/proof.py` ed25519 core — `load_signing_key()` (MAG_PROOF_KEY env hex-seed wins →
`configs/.proof_key`, auto-generated dev key, chmod 0600 attempt, gitignored at
`.gitignore:246`), `sign_payload(payload)` → `{sha, sig, pubkey, pubkey_fingerprint}`,
`verify_signature(signed)` (ED25519 path + LEGACY-UNKEYED fallback), CLI
`sign-payload`/`verify-sig`, `status()` signing block. Legacy `sign()`/`verify()`/
`anchor()` byte-unchanged — pre-AH2 proofs still verify.

**Landed by this refire:**

1. `mag/seal.py verify()` — AH2 rows (additive return keys; no external callers broke):
   - `chain_merkle`: Merkle-verify the SEALED chain copy — recompute the root over the
     sealed `verkle_chain.jsonl` rows with `verkle_knot._merkle_root` (single source of
     the hash law) and match sealed tip root + last row root. MATCHED entry that fails
     re-derivation → `broken` → verify FAILS. LIVE-flagged entry (chain grew mid-copy)
     that lags the sealed tip → WARNING only.
   - `tip_drift`: sealed tip vs LIVE tip. Drift is the norm on a living append-only
     chain → WARNING row (`warnings` list), NEVER flips `verified`.
   - unparseable sealed row → broken; missing chain copy / missing tip → `checked:false` skip.
2. `tests/test_ah2_proof.py` — 15 tests: ed25519 roundtrip + deterministic sig; tamper
   (payload / sig / transplanted pubkey) fails; LEGACY-UNKEYED verifies via BOTH
   `verify()` and `verify_signature()` fallback (+ legacy tamper fails); key law (env
   wins over file, tmp auto-generate persists + reuses same fingerprint, bad hex errors
   naming the source); real-newest-seal Merkle row; synthetic seal consistent; sealed-
   chain tamper FAILS even with the manifest sha mended (Merkle gate catches what the
   file-hash gate can't); live-tail lag warns; tip drift warns not fails. Tests key off
   a fixed env seed / tmp key file — they never mint `configs/.proof_key`.
3. Dev key minted via the real first-use path (`python -m mag.proof status`):
   fingerprint `2a3cab335bcf1d3c`, source `generated:.proof_key (0600)`.
   `git check-ignore configs/.proof_key` → IGNORED; `git status` sees nothing. The key
   is NEVER committed — a committed key makes every signature theater.

## Live evidence (real newest seal, read-only run)

`python -m mag.seal verify` on seal `2026-09-30T09-02-29`: sealed chain copy
(8,536 leaves) re-derives root `397ba6ab1109ceaf…` == its sealed tip root →
`chain_merkle.consistent: true`; live tip has drifted to 8,647 leaves / root
`cf28ec27177e5159…` → `tip_drift.drift: true` as a WARNING; `verified: true` held.
CLI roundtrip `sign-payload` → `verify-sig`: `verified: True, mode ED25519`.

## Test numbers (instrument + moment, per the census-denominator law)

- `pytest tests/test_ah2_proof.py -q` → **15 passed** in 0.97s (2026-09-30, this lane).
- `pytest tests/test_ah2_proof.py tests/test_ag5_tip_verify.py tests/test_kv_seal.py
  tests/test_md_record_seal.py -q` → **42 passed** (same moment).
- verkle/chain/seal/knot family (ah2 + ag5 + kv/md seals + knot patrol + compaction +
  every `tests/test_*verkle* *chain* *knot*`) → **111 passed** in 12.34s.
- Full `pytest -q` (2026-09-30, this lane's run, 37:48): **3,382 passed / 13 failed /
  5 skipped / 3 errors** (3,403 items executed — the tree has grown past the 2,303 /
  352 carrier census of 09-27; different moment, different denominator, per the census
  law). ZERO failures in this lane: none of the 13 failed + 3 errored touch proof /
  seal / ah2 (failed set: memory/working api_gateway + planner/multi-provider routing,
  clerk_route_fix x2, _diag_pid, debug_capsys, cursor_bridge, desk_dialogue x2 —
  other seats' files, pre-existing to this lane's changes).
- Ratchet: `tools/violation_ratchet.py check --changed` FAILs only on other lanes'
  pre-existing debt (ldt_train / concept_predictor / duel_harness / env_contract);
  zero violations on `mag/seal.py`, `mag/proof.py`, or this lane's files.

## Contract (post-AH2)

- `sign_payload(payload)` → real ed25519 sig over the canonical bytes + the legacy
  deterministic sha + pubkey + fingerprint. `verify_signature(signed)` → ED25519 mode,
  or LEGACY-UNKEYED fallback for pre-AH2 proofs (must keep verifying — it does).
- Key resolution: `MAG_PROOF_KEY` (64-hex seed) → else `configs/.proof_key` → else
  auto-generate 0600. Never commit, never log the seed.
- `seal.verify()`: manifest hashes + sealed-chain Merkle + sealed-vs-live tip diff;
  drift warns, tamper fails.
