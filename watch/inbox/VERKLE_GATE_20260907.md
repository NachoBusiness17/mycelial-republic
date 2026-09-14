# VERKLE GATE 20260907 — receipt

**Fold build order #3** (card `watch/WORLDLINE_SEED_20260907.md` §6 disputed territory).
**Decision: INTEGRATE-INFEASIBLE-$0 → path (b). Recommendation: OPTION 2 (drop the word "verkle" from the vision until earned), with the full re-earn SPEC on file and a named trigger for OPTION 1.**
Operator ratifies; nothing renamed by this seat. Card untouched.

---

## 1. Candidates surveyed

| Candidate | Where | Maintenance status | Runs on this box ($0)? | Verdict |
|---|---|---|---|---|
| **ethereum/go-verkle** | GitHub, Go | 237 stars, pushed 2026-01-02, not archived. README's own words: *"This implementation, while correct, is no longer used. It will still be maintained, but there will be delays in the responses."* — upstream-DEPRECATED (EF pivoted off verkle mid-2024) | **NO** — `go: command not found`; toolchain install is OPTION 1's gate | INFEASIBLE-$0; the re-earn path under OPTION 1 |
| crate `verkle-trie` | crates.io API | `{"errors":[{"detail":"crate `verkle-trie` does not exist"}]}` | n/a | DEAD (training-data ghost) |
| crate `verkle-cryptography` | crates.io API | does not exist | n/a | DEAD |
| PyPI: `verkle-trie`, `py-verkle`, `python-verkle`, `ipfs-verkle`, `verkle`, `pyverkle`, `verkle-py`, `python-verkle-cryptography`, `pyverkle-cryptography`, `verkle-cryptography` | pip index | "No matching distribution" for all 10 names | n/a | DEAD (nothing on PyPI at all) |
| `jsign/verkle-py` (pure-Python educational trie, from secondary-source leads) | GitHub | HTTP 404 — repo gone/renamed | n/a | DEAD (ghost) |
| `ethereum/verkle-trie-rs` | GitHub | HTTP 404 — does not exist under that name | n/a | DEAD (ghost) |
| GitHub search `verkle language:python` | GitHub API | 92 hits — all 0-star student repos / audit forks, none maintained | n/a | DEAD |
| **py_ecc 8.0.0** (EF, pure-Python BLS12-381 incl. KZG) | PyPI — EXISTS, maintained | alive | **YES** (pure Python) | **REJECTED**: a commitment *primitive*, not a verkle trie. Building trie+proof scheme on top = self-rolled crypto = house-law violation for load-bearing use |
| **ckzg 2.1.8** (EF c-kzg-4844 bindings) | PyPI — EXISTS, maintained | alive | YES (ships wheels) | **REJECTED**: same reason (blob-KZG primitive, wrong abstraction level) |

Toolchain inventory: `go` ABSENT, `cargo`/`rustc` ABSENT, Python 3.12.10 + pip 26.2 present. Survey method honesty: the web-search tool rate-limited mid-pass, so every live candidate above was checked directly against GitHub API / crates.io API / PyPI — primary sources, not summaries.

## 2. Decision (tri-state)

- **"A maintained verkle library installs and runs on this box for $0" — DISPUTED (findings say no):** no verkle implementation exists on PyPI under 10 probed names, no credible Python repo on GitHub, the Rust crates don't exist, and the one maintained reference (go-verkle) needs a Go toolchain this box doesn't have. → **path (b).**
- **"go-verkle is the viable re-earn path once a toolchain exists" — SUPPORTED (with caveats):** repo maintained-but-deprecated upstream, IPA-proof code present (`proof_ipa.go`, `proof_json.go` — JSON proof serialization exists, which makes a subprocess bridge trivial), Unlicense. Caveats: unaudited research code → **RESEARCH-GRADE label mandatory**; upstream has moved on, so expect no fixes.
- **"The word 'verkle' currently maps to a functional implementation" — DISPUTED (as the card already holds):** `memory/biography/verkle_chain.jsonl` (7,377 rows) is an append-only sha256 parent-chained ledger. Honest name: **hash-chained ledger**. It is a real and good organ — it is just not a verkle tree, and nothing today consumes verkle proofs.

## 3. Recommendation

**OPTION 2 — drop the word until earned.** Reasons, in order of weight:

1. **Nothing installable at $0.** The gate's integrate-arm had no candidate to integrate.
2. **The property has no consumer.** What verkle would add over the hash chain is compact stateless proofs (verify a leaf without the full chain, witness-size verification). Today chain verification is a local full scan over 7,377 rows — cheap; replication is operator-gated with egress none; no remote verifier exists. Integrating unaudited, upstream-deprecated research crypto to buy an unused property is the definition of premature.
3. **The honest name is stronger.** "Hash-chained ledger" describes exactly what the chain is and does (tamper-evidence, provenance) with zero borrowed prestige. The vision loses nothing true.

**OPTION 1 stays open, spec complete (§4), one sitting (~30 min):** install Go → build a ~100-line Go CLI bridge over go-verkle → `mag/verkle_pointers.py` shells out to it. **Named trigger for firing OPTION 1:** the day a *remote/compact* verifier becomes real — cross-seat worldline replication (consent: replication operator-gated) is that day. Until the trigger fires, the word stays dropped.

## 4. SPEC — `mag/verkle_pointers.py` (for the one-sitting re-earn)

**Backend:** go-verkle via a tiny Go subprocess CLI (`tools/verkle_ptr/main.go`, ~100 lines: read JSON op from stdin, write JSON result to stdout; uses go-verkle `Insert`/`Prove`/`VerifyProof` + `proof_json.go` serde). The Python organ NEVER reimplements any crypto — it shells out. House crypto law satisfied by construction; RESEARCH-GRADE banner on the module (go-verkle: correct per authors, unaudited, upstream-deprecated).

**Store (files-only, append-only, read-only on chain+seeds):**
```
memory/verkle_pointers/
  root.json          # {root_commitment_hex, leaves_count, updated_ts, backend:"go-verkle/IPA"}
  leaves.jsonl       # one leaf per line, append-only
  proofs/<key>.json  # one membership proof per leaf
```

**Leaf schema (exactly one leaf per sealed worldline seed):**
```json
{"seed_hash": "<16 hex — from SEED.json seed_hash>",
 "chain_tip": "<64 hex — verkle_chain.jsonl tip leaf_hash at seed time>",
 "ts":        "<ISO-8601 UTC>"}
```
**Key derivation:** `key = sha256(canonical_leaf_json)` where canonical = `json.dumps(leaf, sort_keys=True, ensure_ascii=False)` — mirrors `mag/worldline_seed.py::_canonical` so keying is reproducible from the seed file alone. Value = canonical leaf JSON bytes (32-byte key path, go-verkle-native).

**CLI contract:**
```
python -m mag.verkle_pointers insert  --seed PATH/SEED.json   # appends leaf {seed_hash, chain_tip, ts}
python -m mag.verkle_pointers prove   --seed-hash <16hex>     # writes proofs/<key>.json
python -m mag.verkle_pointers verify  --seed-hash <16hex>    # exit 0 iff proof verifies against root
python -m mag.verkle_pointers root                            # prints root commitment
```

**Verify contract:** `verify(leaf, proof, root_commitment) -> bool` — recomputes key from the leaf, checks the IPA membership proof against the root commitment. No trust in the store files: a tampered `leaves.jsonl` row MUST fail verify against the pinned root.

**Falsifier battery (the gate's own, plus two):**
- F-G1: intact leaf verifies (exit 0) — `seed_hash 8dbd503f64bd163c` + 2 real chain tips inserted.
- F-G2: one-byte tamper in a leaf value → verify FAILS (exit 2).
- F-G3: proof from root A does not verify against root B (cross-store confusion rejected).
- Integration: `worldline_seed.py emit()` gains one fail-open line appending the leaf; `knot_at_close.py` untouched; chain and seeds stay read-only.

## 5. What was built this pass (path-b honest artifacts)

- **`mag/_verify_verkle_gate_spec.py`** — read-only spec-validation harness. Result (all PASS, exit 0):
  - seed_hash recompute (exact `worldline_seed.py` canonicalization) = `8dbd503f64bd163c` = on-disk field → the SPEC's leaf-1 payload is real, not transcribed.
  - leaves 2-3 bound to live chain tips `d0a798c2972208c4…` (tip, 09-06T23:08:56Z) and `87a40614d05b72f4…` (7,377 rows).
  - contract-level tamper teeth: one-byte flip in a leaf → digest flips (`7ed9791f…` → `7ea546af…`). sha256 used here as the stand-in commitment for the CONTRACT demo only — the cryptographic IPA version runs under OPTION 1's F-G1/F-G2.
  - **Dogfooded through `python -m mag.bash_local`** — session `verkle-gate-20260907`, step `d319b8b54184d44e`, exit 0 sealed on the tape.
- This receipt. No chain writes, no seed writes, no config/docker touches.

## 6. Sources

- github.com/ethereum/go-verkle (repo README quote, API surface via file tree)
- api.github.com repos + search endpoints; crates.io API v1; PyPI via `pip index` (direct probes)
- Card: `watch/WORLDLINE_SEED_20260907.md` §6 · organ: `mag/worldline_seed.py` · store: `memory/biography/verkle_chain.jsonl` · seed: `memory/worldline/w1-dogfood-20260907/SEED.json`
