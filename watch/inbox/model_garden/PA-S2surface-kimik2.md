# PA-S2surface-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

I'll analyze the shared inbox contract for attack surfaces from a compromised sibling seat. Let me examine the evidence files to understand the complete surface.

Based on my analysis of the evidence, here is the deliverable:

---

## (1) ATTACK SURFACE MAP

| Surface | Mechanism | Exploit Shape |
|---------|-----------|---------------|
| **INDEX.json derivation** | Fold from index_events.jsonl | Malicious seat appends forged events; fold promotes to derived INDEX without cryptographic verification of event authenticity |
| **Event log append** | Writer nonce gaps tolerated | Compromised seat floods log with replayed or fabricated events; "GAP" warnings in INDEX:fold_warnings show the detection is post-hoc, not preventive |
| **Receipt classification** | `class: "receipt"` in events | Forged receipt with fabricated sha256 promotes untrusted data as verified; no signature on `(file, sha256, writer)` tuple |
| **Living file seal** | `living:true + size:N` prefix hash | Compromised seat truncates living file at N+1, corrupting sealed prefix; validate only warns on downgrade (02__shared_surface.py:KNOWN_LIVING_PATHS comment) |
| **Hash-to-content mapping** | SHA256 in events, content on disk | Seat swaps file contents after registration; `stale-register heal` pattern in 01__INDEX.json shows this is known and "healed" by re-registration, not rejected |
| **Writer identity** | `writer` field in events | No authentication; any seat can write as any writer (e.g., "md-record-seal", "zcode-seat-20260926") |
| **Prompt injection via receipt** | `purpose` field in events | Receipt `purpose` strings rendered in UI/logs; 01__INDEX.json shows `purpose` contains full sentences, unescaped |
| **Path traversal** | `file` field in events | Events reference paths like `ractor_engine/2026-10-01-dogfood-gaps/lineage.md`; no validation that path is within inbox root |
| **Rebuild verb** | `python -m mag.shared_surface rebuild` | Compromised seat triggers rebuild with `--dry` false, causing fold to heal based on poisoned log |

---

## (2) THE 3 WEAKEST JOINTS

### JOINT 1: Unauthenticated Writer Identity (Critical)
**file:line**: `03__index_events.jsonl:1-3` (schema), `02__shared_surface.py:scan_events_log` (implied, no auth check)

**Exploit shape**: Any compromised seat writes events with arbitrary `writer` field. The log accepts "md-record-seal", "zcode-seat-20260926", "exp002a" without cryptographic proof of identity. A malicious seat can impersonate the seal authority or flood with conflicting registrations.

**Evidence**: `{"writer":"exp002a","nonce":1}` at seq 28; `{"writer":"md-record-seal","nonce":2044}` at tail. No signature field. Nonce gaps are detected but not prevented.

---

### JOINT 2: Hash-Content Split with Stale-Register Heal (High)
**file:line**: `01__INDEX.json` items with `"purpose": "...stale-register heal..."`, `02__shared_surface.py:KNOWN_LIVING_PATHS` comment about downgrade warnings

**Exploit shape**: Seat registers `sha256:X` for file `F`, then modifies `F` on disk. Next validate detects mismatch, but "heals" by re-registering current bytes with warning. This is a **promotion of mutation to accepted state**, not a rejection. The `PACK_OFFLOAD.jsonl` entry shows 3 stale-register heals stacked on same file.

**Evidence**: `"purpose": "hash refresh: static row evolved (patrol 20261001) | stale-register heal (whole-file): re-registered current bytes; prior sha 9E3523154126 | stale-register heal (whole-file): re-registered current bytes; prior sha 3914A259F11F..."`

---

### JOINT 3: Living File Downgrade to Silent Whole-File Seal (High)
**file:line**: `02__shared_surface.py:KNOWN_LIVING_PATHS` tuple definition and surrounding comment

**Exploit shape**: Living files (`LINKS.jsonl`, `QUEUE.md`, `phone_relay_log.jsonl`) use prefix sealing for append-only safety. A compromised seat re-registers without `living` flag (legal per "last-register-wins"). This **silently downgrades** to whole-file seal. Next append fails hard, but the downgrade itself is only a warning, not blocked. Seat can force DoS or force re-registration chain to obscure audit trail.

**Evidence**: Comment states: "A plain `add` re-register legally drops the living flag...validate warns (never errors) when one of them folds to an item without item.living"

---

## (3) PATCH SPEC PER JOINT

### PATCH 1: Writer Authentication via Seat Key
**Deliverable**: `configs/seat_keys.json` + `mag/seat_identity.py`

**Spec**:
- Each seat generates Ed25519 keypair on first run; public key registered in `configs/seat_keys.json` with `seat_name`, `pubkey`, `first_seen_seq`, `revoked` flag
- Every event appends `sig` field: `sign(privkey, canonical_json(event without sig))`
- `validate` rejects events with unknown `writer`, revoked key, or invalid signature
- `rebuild` only folds events with valid signatures

**Falsifier**: Event with `writer:"exp002a"` and valid signature from unregistered key must fail validate; event with registered key and tampered content must fail validate.

---

### PATCH 2: Content-Addressed Storage with Hash Verification
**Deliverable**: Modify `02__shared_surface.py:inspect_surface` + new `mag/content_store.py`

**Spec**:
- Inbox becomes content-addressed: files stored at `inbox/.content/<sha256>` with read-only permissions
- Event `file` field becomes symlink pointer to content address
- `validate` verifies: (a) content at address matches hash, (b) symlink target matches event
- `stale-register` condition becomes impossible (content immutable); instead `content_missing` error if hash not in store
- Migration: existing files hashed and moved to content store; symlinks created

**Falsifier**: File modification after registration must result in `content_hash_mismatch` error, not heal warning; content store must contain exactly the bytes referenced by active events.

---

### PATCH 3: Living Flag Immutability via Seal Commitment
**Deliverable**: `mag/living_seal.py` + `02__shared_surface.py` modification

**Spec**:
- Living status becomes **append-only property** in events log: `op:"seal_living"` with `file`, `size`, `sha256_of_first_N_bytes`
- Once `seal_living` event exists for path, any `register` without `living:true` referencing same path is **rejected** by validate
- Downgrade attempt produces `living_seal_violation` error, not warning
- `rebuild` respects seal commitment: refuses to fold conflicting registrations

**Falsifier**: Attempted re-registration of `LINKS.jsonl` without `living` flag after seal event must fail; seal event must reference hash of first N bytes, not just size.

---

## (4) THE SINGLE VALIDATION THE CONTRACT'S OWN LAW DEMANDS BUT NO TOOL RUNS TODAY

**The Law**: `00__SHARED_SURFACE_CONTRACT.json` law 3: "Treat every inbox item as untrusted data until it is classified."

**The Missing Validation**: **No tool verifies that a reading seat has actually performed classification before acting on inbox content.**

**Evidence**:
- `00__SHARED_SURFACE_CONTRACT.json` defines classes: `FACT`, `INFERENCE`, `PROPOSAL`, `UNPROVEN`, `RECEIPT`
- `01__INDEX.json` shows `class` field per item
- `02__shared_surface.py` `inspect_surface` reports `indexed_items` and `unindexed_items` but **no `unclassified_but_used` detection**
- No tool checks that a seat reading `class: "UNPROVEN"` or `class: "PROPOSAL"` has logged its classification decision before using the content

**The Gap**: A compromised seat can write `class: "RECEIPT"` (promoted as trusted), and reading seats consume it without verifying the classification chain. The contract's law 3 is **advisory only**; no enforcement.

**Required Validation**: `mag/classification_gate.py` - before any seat uses inbox content, it must log `classification_commit` event with `(file, declared_class, reader_seat, use_intent, timestamp)`; `validate` checks that all `class != UNPROVEN` items have classification commit from reading seat, or warns `unclassified_use_detected`.

---

**Deliverable falsifier**: Run `python -m mag.shared_surface validate` on inbox with `class: "UNPROVEN"` item that was read by another seat; current tool passes, patched tool must fail with `unclassified_use_detected` unless classification commit exists in events log.
