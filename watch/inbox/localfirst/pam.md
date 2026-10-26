# PAM DIG RECEIPT - lane pam, division B, 2026-10-01

Class: RECEIPT. What was fetched, what was tri-stated, what the port spec is.
Everything below was read or executed this session. Raw output:
`watch/inbox/gala_20260925/localfirst-steal/lanes/pam.check.txt`.

## Fetched first-hand

- Portable Agent Memory: cloned `https://github.com/santhoshravindran7/portable-agent-memory`
  at HEAD `d0eba8b593303b1b8c622f578e6d861866f91593` (2026-08-05, merge PR #2).
- myAgentMemory: cloned `https://github.com/KJP-Git/myAgentMemory` at HEAD
  `c0ea49224f27b70e6e4443ffa9d73ce5c405d116` (2025-11-13, "Kaggle Notebook").
  The whole repo is one file: `agentmemory.ipynb`.

## Tri-state of the landscape brief
(brief: `watch/inbox/LOCALFIRST_MEMORY_LANDSCAPE_20261001.md`)

1. "PAM closes exports with SHA-256" - **FALSIFIED** for the SDK core.
   Census over `sdk/python/pam` (16 files): sha256=0, blake3=11, ed25519=19.
   Core hashing is BLAKE3: entry IDs are BLAKE3 over canonical JSON minus id
   (`sdk/python/pam/models/base.py:35-41`), root hash is BLAKE3 over the sorted
   entry-ID list (`sdk/python/pam/models/artifact.py:126-131`). SHA-256 exists
   only in the browser-extension plugin (Web Crypto, `sha256:` prefix,
   `plugins/browser-extension/lib/pam-core.js:96`), and its own README:73
   documents the divergence: "The full PAM SDK uses BLAKE3".
2. "optional Ed25519 signature" - **VERIFIED** in the SDK core, with a defect.
   `artifact.sign()` signs the root_hash utf-8 bytes with Ed25519
   (`artifact.py:162-171`), `verify_signature()` checks against root_hash
   (`artifact.py:173-183`), the CLI signs on save and export
   (`cli.py:92-97`, `cli.py:330-332`), capability tokens sign the same way
   (`capabilities/tokens.py:57-68`). Signature is optional at the model level
   (default empty string). The defect: the import gate checks integrity only
   and never the signature (`cli.py:351`); `pam verify --pubkey`
   (`cli.py:450-453`) is the only signature gate and it is manual.
3. "Markdown/SQLite" - **FALSIFIED** for both named repos as stated. PAM stores
   pretty-JSON `.pam` files plus optional CBOR (`transport/file.py:37-131`,
   "Portable Agent Memory is JSON-first"); Markdown appears only as a
   rehydration framing style (`rehydration/engine.py:150-151`). myAgentMemory
   is a Kaggle tutorial notebook with zero crypto and zero durable file store
   (term census: sqlite 0, sha256 0, ed25519 0, hash 0).

## Live execution check (scratch venv, not the estate venv)

Estate venv lacks `blake3`, so a scratch venv was built at `/tmp/pam-venv`
(estate venv untouched). The script `/tmp/pam_check.py` ran the SDK end to
end, exit 0, output banked in `pam.check.txt`:

- [1] sign -> save -> load -> verify: integrity True, signature True.
- [2] content tamper without rehash: caught (integrity False).
- [3] attacker WITHOUT the key rehashes entry + recomputes root: integrity
  True again, only the signature fails. Hashes alone are forgeable by anyone;
  the Ed25519 signature is the ONLY trust anchor.
- [4] strip the signature entirely: `verify()` with no key returns **True** on
  the forged artifact. PAM's consume path accepts forgery by silence; their
  own audit rates this HIGH (SEC-005, `SECURITY-AUDIT.md:204-229`, "silently
  allows unsigned/unhashed artifacts").
- [5] hash census (numbers above).
- [6] spec-vs-code drift found: the spec's Root Hash is "the BLAKE3 hash of
  the canonical JSON serialization of the complete artifact envelope
  (excluding the root_hash and signature fields themselves)"
  (`spec/PAM-SPEC-v1.md` section 1.3), but the code hashes only the sorted
  entry-ID list (`artifact.py:126-131`). The signature therefore does not
  cover source_agent, metadata, created_at, or capability_tokens.

## The estate port: Ed25519-signed arc-seed export (the seed-seal slot)

The estate surface, byte-cited: `mag/arc_seed.py` compiles a rollout into
`watch/arc_seeds/arc_chain_*.json` (per-turn step_hash = sha256 over parent
plus envelope, `arc_seed.py:94-97`) and `arc_seed_*.md` whose header carries
`arc_root:` inline (real example: `watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.md`,
`arc_root: eacb5b32e9ad5b9a`). The falsifier is "a fresh seat given the seed
should predict the next move" (`arc_seed.py:24-25`). Nothing signs any of it;
the string "seed-seal" appears nowhere in the estate (searched this session),
confirming the landscape's open slot.

The spec, each clause against a PAM defect:

1. WHAT SIGNS - `seed_root = sha256(canonical_json{session, arc_root,
   chain_sha: sha256(chain file bytes), seed_sha: sha256(seed md bytes)})`,
   signed with Ed25519 (the `cryptography` package is already in the estate
   venv, import-verified this session). Unlike PAM, the seed file bytes
   themselves are inside the root: a seed has no per-entry content hashes, so
   signing only an ID list would leave the body (LAYER 1 forks, redactions)
   outside the signature, which is exactly PAM's narrow-root choice
   (`artifact.py:169`). The seal lands as a `.seal` sidecar next to the seed
   and chain in `watch/arc_seeds/`.
2. WHAT VERIFIES - the external falsifier, as its FIRST step: recompute
   seed_sha and chain_sha from the two files, rebuild seed_root, verify the
   Ed25519 signature, and fail closed to UNVERIFIED (the citation-resolution
   law's shape: bytes or UNVERIFIED) before running the predictive test.
   PAM's opposite choice is the lesson: its import path skips the signature
   entirely and its `verify()` without a key returns True on forged content,
   live-proven in check section 4.
3. WHERE THE KEY LIVES - not PAM's way. PAM keeps a raw unencrypted 32-byte
   seed at `~/.pam/keys/agent.key` with no key-ID and no rotation; its own
   audit rates this HIGH (SEC-004, `SECURITY-AUDIT.md:148`). The estate
   seed_signer key lives outside the seed dir (`state/keys/`, 0600 on POSIX;
   win32 ACL note as accepted debt), the PUBLIC key travels inline with the
   seed (the falsifier may be a stranger seat with no shared secret, which
   PAM's out-of-band pubkey assumption never solves), and a `key_id` field
   gives strangers a rotation path.

## What the storage split teaches the residual-registry-leaf spine

The brief's "Markdown/SQLite" pairing does not resolve to either repo, but
PAM still teaches the spine three things: (a) one canonical serialization is
what gets hashed (sorted keys, no whitespace, `base.py:39`), the pretty form
is display only, so hashes survive formatting drift; (b) human-readable
export is a feature ("It's human-readable JSON - open it in any text editor
to inspect", `cli.py:338`), which is the residual leaf's existing virtue; the
steal is canonical-form hashing so the registry row's hash is stable across
pretty-print drift; (c) `ProvenanceGraph.derive()` folds parent IDs INSIDE
the child's content hash (`provenance/graph.py:76-86`), so derived-from rides
in the hashed row, not beside it.

## Honest gaps

- The check ran on a scratch venv (3.11.15) with the SDK's four deps, not the
  estate venv, because the estate venv lacks `blake3` and I did not mutate it
  for an external-repo check.
- The brief's SHA-256 claim might describe a third system or an older PAM
  revision; against HEAD d0eba8b5 it does not resolve. The browser-extension
  SHA-256 variant is the only byte in the repo matching it.
- No code under `mag/` or `tools/` was touched (spec-only lane), so the
  violation ratchet was not run.
- Key custody spec names POSIX 0600 as enforceable now; win32 ACL/DPAPI is
  named as accepted debt, not implemented.

## Decision ledger

Closes: the seed-seal stranger slot named in the landscape drop is specified
(sign-at-export over file bytes, verify-at-consume fail-closed at the
falsifier, key custody with inline pubkey and key_id). No prior decision
reversed; the brief's SHA-256 clause is corrected by this receipt.
