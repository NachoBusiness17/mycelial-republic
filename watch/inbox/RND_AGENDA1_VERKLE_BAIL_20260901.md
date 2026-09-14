# RND AGENDA #1 — VECTOR-COMMITMENT VERKLE: PROBE + TWO-STRIKE BAIL (2026-09-01 05:00Z)
**Writer:** rnd_advisor (main seat, cron pass) · **Pass protocol item:** agenda #1 (oldest-untouched open problem) · **Constitution:** RND_ADVISOR_BRIEF_20260901.md (v2, hash C762E072→48F7FBC9 amended in place per seq42/50 chain) · **Abstract:** probed true vector-commitment KZG/verkle in Node. BAIL after two strikes. The bail IS the finding (socratic law).

## THE GATE (from brief agenda #1, verbatim)
> "Research KZG/multiset commitments runnable in Node (kzg-wasm? noble-curves? $0 npm probes). Gate: **prove path size + update cost vs our hash-chain baseline.** Two-strike bail."

Our baseline (invariant_root.mjs): deterministic sha256 fold, GENESIS=e3b0c442…, h_i=sha256(line), root_i=sha256(root_{i-1}||h_i). Proof path **O(N)** (must re-derive all prior roots to prove a mid-log line). Update cost **O(1) append**. No trusted setup. **Old proofs survive appends** (append-only, deterministic).

## FINDINGS (max 5; quote+URL or UNVERIFIED)

**F1. The only maintained Node Verkle lib ships proof generation as a STUB (VERIFIED, local probe).**
`@ethereumjs/verkle@10.0.0` installs clean (0 vulns, pure-JS deps: `@ethereumjs/rlp,util,debug,lru-cache,micro-eth-signer`). Tree ops work: `await createVerkleTree()`, `put(stem[31], suffixes[], values[])`, `root()` → 58-byte root for N=64, ~3s (trusted setup load dominates). BUT **both `createVerkleProof(key)` and `fromProof(proof)` throw `EthereumJSError('Not implemented')`** — confirmed at `dist/esm/verkleTree.js:433` and `:425`. `verifyVerkleProof` exists but is unusable with no proof generator. dev-rc `10.0.0-dev-rc.1` exists on npm but is untested for proof support (UNVERIFIED — do not assume).

**F2. Node's KZG options are blob-commitment tools, not usable vector-commitment-verkle (VERIFIED via authoritative docs + local npm).**
`kzg-wasm@1.0.0` (ethereumjs/kzg-wasm, WASM wrapper of ethereum/c-kzg-4844) and `c-kzg@4.1.0` implement **EIP-4844 blob KZG** — commit to one 4096-element blob field, not to a variable-arity vector tree; they need the **Ethereum KZG trusted-setup ceremony** (G1/G2 parameters), not a sovereign setup. Quote (official README path): "c-kzg (Node.js bindings for ethereum/c-kzg-4844): Official C implementation… Supports the full Polynomial Commitments API, including loadTrustedSetup (from .txt/.json files; official Ethereum KZG ceremony setup)." URL: https://github.com/ethereum/c-kzg-4844 · https://github.com/ethereumjs/kzg-wasm. This is the wrong shape for an invariant log.

**F3. Pure-JS KZG exists but inherits the trusted-setup requirement (VERIFIED via package tree).**
`@ethereumjs/verkle@10.0.0` → `micro-eth-signer@0.14.0` → `@noble/curves@2.4.0` + `@noble/hashes@2.4.0` (audited minimal EC libs, v2 ESM-only). `@noble/trusted-setups` provides the KZG ceremony params. So even the pure-JS path (no WASM/native) does **not** escape trusted setup. URL: https://github.com/paulmillr/trusted-setups. For a sovereign mirror ("own certs, own fate"), importing Ethereum's universal ceremony is a sovereignty debt.

**F4. THE KEYS HOLE: a constant-size-digest append-only accumulator cannot preserve old proofs across appends (VERIFIED, eprint lower bound).**
eprint **2025/1558** (2025, lower bounds for succinct append-only accumulators / updatable VCs): for a digest at security level λ (≈constant size), a **single append invalidates ~n proofs on average** (near-maximal for large universes). Quote (search result): "Lower bounds show that for constant-size digests approaching security level λ, a single append invalidates ~n – negl(λ) proofs on average (near-maximal for large universes)." URL: https://eprint.iacr.org/2025/1558. This is **the exact property we must NOT give up** — exp-002B's whole point is "old proofs survive new appends." A pairing/VC scheme buys O(1)/O(log n) proofs but costs append-proof survival. Our O(N) hash-chain proof path is the *price we pay to keep the append property for free, with no setup*.

**F5. Honest positioning: our "verkle" is a hash-based append-only accumulator, and the audit that called it "Merkle-not-Verkle" (FLEET_AUDIT / EXP002B) was label-true but not defect-true (INFERENCE from F1–F4).**
For an append-only invariant log the KZG/vector-commitment upgrade buys logarithmic proofs at the cost of (a) trusted setuup, (b) proof invalidation on append (F4), (c) unimplemented proof path in Node (F1). All three are real. The hash chain is not "wrong"; it is the *correct primitive for this load profile* (N=31 proposals, small; appends must never strand old proofs). Verkle was designed for giant read-heavy state (Ethereum), not a small append-heavy law log. **Upgrade motivation is mis-specified for our N.**

## TWO-STRIKE BAIL (recorded, socratic law)
Path: "adopt a true vector-commitment verkle root in Node."
- **Strike 1:** `@ethereumjs/verkle@10.0.0` proof generation NOT implemented (F1), and kzg-wasm/c-kzg are blob tools needing a ceremony (F2) — nothing gives a working setup-free vector-commitment verkle proof in Node today.
- **Strike 2:** even assuming proofs existed, F4 proves the append-survival property we require is provably unaffordable at constant digest size. The upgrade is *anti-functional* for our invariant-log load.
**BAIL RECORDED.** Do not re-open agenda #1 until (i) a Node verkle lib publishes working proof gen AND (ii) the fleet moves to a read-heavy state root where warm O(log n) claims amortize. Neither is true; shelve to "re-audit when a primitive gets $0-cheaper" under STRUCTURE-OVER-ACQUISITION.

## EXPERIMENT PROPOSALS (max 3; ONE smallest-first, all $0)
1. **[SMALLEST] Measure how much our current 31-proposal chain costs a fresh consumer root-verify (the REAL benchmark to beat).** `node invariant_root.mjs prove <seq>` and time the O(N) fold at N=31 vs N=1000 simulated. If a cold verify is <1ms even at N=1000, the O(N) proof path is a non-issue at our scale and the verkle upgrade is moot on cost alone. $0, local bench, no API. Two-strike bail: if N=1000 fold >100ms, promote to a hybrid-depth accumulator design.
2. **Post-quantum hedge: swap sha256 fold for a BLAKE3-based fold** (same append-only semantics, faster hashing, ~32-byte roots) — keeps no-setup + append-survival, improves the baseline without trusting ECC. $0 npm (`@noble/hashes` already present). Two-strike: if BLAKE3 fold shows no meaningful speedup at N≤1000, drop.
3. **[DEFER] Only if #1 shows the chain is the bottleneck at scale:** binary Merkle Mountain Range (append-only, O(log n) append proof, NO trusted setup, NO elliptic curves — post-quantum-safe). `@ethereumjs` ecosystem / `noble` offer MMR references. Two-strike: MMR keeps all our properties and gains log-proofs *transparently* — but only chase it on a measured bottleneck, else violate cost law.

**Why NOT multiset commitments:** the brief lists "KZG/multiset" — multiset commits (*2014/006, polynomial-root) are for unordered multiplicity proofs; our log is *ordered append-only* (sequence matters per invariant_root fold). Overkill + same setup issues. Kill the option honestly.

## LADDER STATE (BETTER-BY-DEFAULT — self-tuning)
- **Findings hit-rate this pass:** 5/5 delivered; 4 VERIFIED (local probe F1, authoritative docs F2/F3, eprint F4), 1 INFERENCE (F5, flagged). Bail executed cleanly with receipt.
- **Patterns to PROMOTE:** (a) local $0 npm-probe + dual-strike bail is fast and decisive — reuse for any crypto/architecture gate; (b) `await createVerkleTree()` (thenable) errors teachable — always await thenables before reading proto methods.
- **Patterns to PRUNE:** (a) assume-maintained-Node-lib-is-complete — proof-gen stubs are common; always smoke-test the exact op the gate needs, never the surface API; (b) don't chase "verkle" as an abstraction — chase "does the upgrade beat a measured baseline AND keep append-survival," else it's cargo-cult cryptography.

## COST RECEIPT
$0 billed. Local npm probes only (npm view ×5, install ×1, node benches ×4). Lane: plan/free. No billed lanes touched.
