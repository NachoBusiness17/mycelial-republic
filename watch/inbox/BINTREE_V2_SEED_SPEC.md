# BINTREE V2 SEED SPEC (2026-10-17, REVIEWED + BINDING)

- **Status:** REVIEWED + BINDING (`watch/inbox/adjudication/verkle-knot-v2-20261017.req.verdict.md` + `verkle-knot-v2-20261017.req.review.md`)
- **Code Counterpart:** `mag/bintree_v2.py`, `scripts/freeze_v1_seed.py`, `scripts/catchup_v2.py`, `scripts/checkpoint_v2.py`, `scripts/verify_knot_v2.py`, `public_seed/mag/verify_knot_v2.py`
- **Coordination Receipt:** `watch/inbox/V2_BINTREE_BUILD_20261017.md`

---

## 1. Hash Profile and Domain Separation (Decision 1 + Delta D1 + Addition A8)

- **Profile (`mag`):** Labeled SHA-256 over an EIP-7864-shaped binary hash tree (`32`-byte keys = `31`-byte stem + `1`-byte subindex; `256`-wide stem subtree; minimal internal nodes; empty subtree = `0^32`).
- **Domain Separation (RFC 6962 / Certificate Transparency lineage):** Just as RFC 6962 Section 2.1 prefixes leaf (`0x00`) and internal (`0x01`) preimages to prevent second-preimage/node-vs-leaf collisions, `mag/bintree_v2.py` prepends a 1-byte domain tag to the SHA-256 preimage for every non-empty hash computation (`mag/bintree_v2.py:63-77`):
  - `0x01` (`inner`): `SHA256(0x01 || left_32 || right_32)` (with `left == 0^32 and right == 0^32 -> 0^32`)
  - `0x02` (`stem`): `SHA256(0x02 || stem_31 || subroot_32)`
  - `0x03` (`leaf`): `SHA256(0x03 || value_bytes)`
  - `0x04` (`sub`): `SHA256(0x04 || left_32 || right_32)` inside the 8-level stem subtree
- **Measured Accounting (Addition A8):** The 1-byte tag is prepended in memory to the hashed preimage; it adds `0` stored bytes per node on disk. Ethereum byte-compatibility and BLAKE3 packaging are declared non-goals for this profile.

## 2. Key Layout and Single-Writer Row Ordering (Decision 2)

- **ROW Stem (`0x00 || u64be(i) || 0^22`):** Index-ordered rows `1..N`, inserted once under the `memory/biography_v2/.lock` writer lock (`mag/bintree_v2.py:13-14`, `1030-1062`).
- **SESSION Stem (`0x80 || sha256("mag.v2.session\0" + session_id)[:30]`):** Maps each session to its latest row index and mirrored `v1` leaf hash.
- **META Stem (`0xC0 || 0^30`):** Commits tree metadata (`N`, genesis binding, seed counts).
- **Row Count Commitment:** Because a sparse indexed binary tree with `empty = 0^32` uses no duplicate-last-leaf padding (contrasting the `v1` odd-leaf duplication documented in `watch/inbox/MERKLE_COLLISION_PROOF_20261007.md`), the key set commits `N` directly when paired with the signed checkpoint/tip header.

## 3. Seed Import vs Anchor (Decision 3 + Addition A8)

- **Full Row Import:** Frozen `v1` seed rows `0..(N_seed - 1)` are imported into `v2` as rows `1..N_seed` (`kind = "seed"`), preserving `SUB_V1_LEAF` (`mag/bintree_v2.py:552-554`, `772-787`) so any historical knot verifies against the `v2` root without requiring the legacy `v1` file.
- **Rehearsal Evidence (`watch/inbox/V2_BINTREE_BUILD_20261017.md`):** Seed `n = 12,017` (`root = 6d26f329...`), catch-up of `+141` knot rows and `+4` amend rows to `n = 12,162` (`root = 66868c0b...`), and live estate chain catch-up to `n = 12,182` (`root = 7a89fb705067cf620ef8b60cc9b7c15fcba715d721a4b686a44482158d262f86`), verified standalone on `bob` via `verify_knot_v2.py` (`results/proof_live_8009.json`, `results/proof_live_tip.json`). Wall-clock import time scales with row count and knot bodies copied.

## 4. Freeze Gate and Baseline Hashes (Decision 4 + Decision 7 + Additions A1/A4 + Delta D2)

- **Exact-Prefix Refusal Gate:** `scripts/freeze_v1_seed.py` refuses unless the certified Oct 15 restore is an exact prefix of the target chain (`memory/biography_v2/FREEZE_REFUSED_20261017T181221Z.json`), or `--source-restore` is explicitly passed with a verified Ed25519 seal.
- **Named Snapshot Counts and Hashes (Addition A4 / Decision 7):**
  - `watch/inbox/CHAIN_RESTORE_20261015.seal`: `key_id = de5fc05e962c43ab`, `chain_sha = 40869fb3...` (hashes `.chain.json` metadata wrapper)
  - Certified Oct 15 restore file (`verkle_chain.jsonl` at restore moment): `n_restored = 12,016` rows, `restored_sha256 = 0da8026d...`, `arc_root = 27848056...`
  - Live `v1` chain at `FREEZE_REFUSED_20261017T181221Z.json` moment: `12,157` rows, `sha256 = 27da7fd3...`, `root = 1a2af3cf...` (`4` post-restore in-place amends at rows `7, 9, 10, 5234`, prefix `sha256 = a42477fe...`)
- **Stranger Verification Recipe (Delta D2 - Pachomius Entry Condition):**
  ```bash
  python verify_knot_v2.py proof.json --expected-root <64-hex-root>
  ```
  Requires only Python 3.10+ stdlib (`public_seed/mag/verify_knot_v2.py`); verifies RFC 8032 Ed25519 signature (if signed) and recomputes all `SUB_META`, `SUB_KNOT_SHA256`, `SUB_CANON_SHA256`, `SUB_V1_LEAF`, and `SESSION` openings to the 32-byte root.

## 5. Shadow Hook, Work Floor, and Outer Failure Logging (Decision 5 + Addition A5 + Delta D4)

- **Hook Location:** `mag/verkle_knot.py` (after `v1` append + atomic tip write); gated by `configs/mag.yaml` `chain_v2_shadow` (or env `MAG_CHAIN_V2_SHADOW`).
- **Outer Failure Logging (Addition A5):** Neither inner `shadow_append` errors nor outer import/invocation exceptions may pass silently; any outer exception in `mag/verkle_knot.py` appends `{"kind": "outer_hook_exception", ...}` to `memory/biography_v2/shadow_mismatch.jsonl`.
- **Cutover Comparator and Work Floor (Delta D4):** The 7-day shadow window requires BOTH elapsed duration (`>= 7` days) AND a work floor of `M >= 100` mirrored `v2` rows, with daily comparator `python scripts/catchup_v2.py --check` returning `pending: 0` (`rc = 0`) and `shadow_mismatch.jsonl` holding `0` unresolved rows before the 30-day `v1` retirement clock starts.

## 6. Signing, Publication, and Proof Privacy (Decisions 6 & 8 + Additions A6/A7 + Delta D3)

- **Separate Operator Gates (Addition A7):** `chain_v2_shadow`, `chain_v2_signing`, and `chain_v2_publish` in `configs/mag.yaml` are independent gates; each requires its own operator flip and receipt.
- **Publication Surface (Addition A6):** Signed checkpoints (`PINNED_SEAL_KEY_ID = de5fc05e962c43ab`) publish to the `falsifier-index` repository only. Automated posting to X is prohibited (Law 17 filter register).
- **Proof Privacy and Secrets Tiering (Decision 8 + Delta D3):** Default proof export is hash-only (`--full` omitted) and carries locator `(index, session_hash, leaf_hash)`. Full-knot publication (`--full`) is additionally bound by the 3-tier secrets law (`warm_surface.redact_text` / public-eligible knots only).
