== ownmem.md ==
# OWNMEM DIG RECEIPT - gala ownmem lane (division B), 2026-10-01

Class: RECEIPT (digger lane, localfirst-steal wave) · Upstream: grpcer/ownmem @ main
(422 stars, JavaScript, Apache-2.0, created 2026-08-16, pushed 2026-10-01T03:59Z,
default branch main, npm: ownmem) · All bytes fetched first-hand this session via
curl from api.github.com + raw.githubusercontent.com, HTTP 200, saved under
`watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/` (19 files, byte
counts logged in `lanes/ownmem.check.txt`).

Repo meta: `fetched/ownmem/repo_meta.json`. Tree (193 blobs, not truncated):
`fetched/ownmem/tree.json`. Brief: `watch/inbox/LOCALFIRST_MEMORY_LANDSCAPE_20261001.md`.

## Tri-state table: the brief's claims

| # | Brief claim | Verdict | Byte evidence |
|---|---|---|---|
| C1 | Markdown memory in-repo | SUPPORTED | `.ownmem/MEMORY.md` fetched, 41 B, a one-link catalog; `.ownmem/MEMORY-general.md` fetched, 611 B, L2 index listing 4 topic files; `.ownmem/ci_latency_lock_needs_machine_scaling.md` fetched, 2176 B, a full frontmatter entry (triggers, authority, code_evidence, run-ID evidence lines). README.md:26 "Readable Markdown in `.ownmem/` travels through clone, review, and rollback with the code". docs_ARCHITECTURE.md:20 lists `.ownmem/` as "This repository's own reviewed project memory". Nuance: recall never reads the .md at query time; the Markdown is the source of truth, the JSON snapshot is the derived read cache (ARCHITECTURE.md:43-47). `.gitignore` (58 B) ignores only `node_modules/ *.tgz .local-test/ .DS_Store npm-debug.log*`, so the corpus commits. |
| C2 | Content-addressed snapshot compile | SUPPORTED | `lib/memory-index-store.mjs:74-76`: `snapshotId = sha256("ownmem-index/v1\0ownmem-compiler\0" + compilerVersion + "\0" + sourceSha256 + "\0" + contentSha256)` - the address binds source bytes + artifact bytes + compiler version. `:62-72` content_sha256 = sha256 over stable-sorted per-artifact metadata. Fetched manifest `.ownmem/index/snapshots/f03c1cb5.../manifest.json`: per-artifact sha256+bytes+records for 5 artifacts (documents/exact-map/graph/postings/ranking), per-source-file sha256, `content_sha256` 7205218b... distinct from snapshot id f03c1cb5... (id additionally binds compiler v0.10.0 + source_sha256). Reader re-verifies EVERY checksum on EVERY load (`:99-156`), and any mismatch falls to rebuild-from-Markdown, per the comment at `:24-27`. |
| C3 | Recall with no model call by default | SUPPORTED | Default path: `lib/features/recall.mjs:724-731` `embeddingChannelNeeded` returns false when no embedding config.json exists (default install has none), `:735-738` `loadEmbeddingChannel` then returns null, so `fetchImpl` (the only network seam, `:409-413`, `:744-753`) never arms. Ranker `lib/memory-ranker.mjs:527-536` adds the embedding branch only when `embedding_similarity > 0 && embeddingWeight > 0 && hasDeterministicEvidence && deterministicConfidence >= threshold`; the five default lanes (exact, BM25F, n-gram, fuzzy, graph) are pure local JSON lookups. docs_TECHNICAL.md:176-179 "Default recall uses no model and no query-time network call. The optional embedding channel begins in observation mode with weight zero." Only process call on the path is `git rev-parse HEAD` for trust context (recall.mjs:105-116), not a model. CAVEAT: the README's numbers (Recall@1 100% on 128 queries / 40 languages vs 3.9% grep -F; 0.46 ms P50 / 1.05 ms P95, README:34) are the project's own benchmark, NOT reproduced by this lane; I verified the code path is local and deterministic, not their numbers. |
| C4 | Trust receipts outside the text | SUPPORTED | `lib/memory-trust-store.mjs:39-41` `DEFAULT_MEMORY_TRUST_FILE = 'trust.lock.json'` - a separate schema-validated JSON lock (schemas/trust/lock.schema.json), receipts keyed by memory id (`:136-140`, lookup `:204-208`), each receipt's evidence normalized with sha256 (`:65-71`) and content-bound (`:359` binds path+sha256+content). docs_ARCHITECTURE.md:35-38 "Topic Markdown is untrusted content, including its own `authority` field. The separate `trust.lock.json` stores content-bound receipts for lifecycle, authority, action risk, version/environment applicability, evidence hashes, and rollback lineage." Note: the public dogfood corpus commits NO trust.lock.json yet (tree + manifest source list confirm), consistent with entries at `authority: observed` (nothing confirmed); the mechanism is in code+schema, live receipts are future state. |

All four claims SUPPORTED at byte level. Nothing DISPUTED. One UNVERIFIED residual:
the project's benchmark numbers (their `npm run benchmark`, locked CC0 corpus) and
the npm-download/star social proof are their claims, not this lane's measurements.

## What the bytes show beyond the brief (the steal surface)

1. Reader-side total verification: every snapshot load re-checks manifest schema,
   source checksum, every artifact's byte length + sha256 + record count, then
   recomputes content_sha256 and the id (`memory-index-store.mjs:99-156`). A
   failed read is never patched; it degrades to a rebuild from the Markdown
   source. The comment at `:24-27` is a law: "the index is derived from the
   Markdown corpus, so recompiling it is cheap and always correct, whereas a
   second reader for an older encoding is a parser that has no producer and
   never goes away."
2. Two-slot immutable snapshot pointers: `v1` and `previous-v1` are symlinks
   (74-byte targets like `snapshots/f03c1cb5...`), publication moves
   previous-v1 to the old current then v1 to the new (`:279-280`), Windows
   gets an unlink-then-rename with restore-on-failure (`:210-238`), and
   `rollbackMemorySnapshot` swaps the two (`:185-199`).
3. Pointer-ordered GC: unreferenced snapshots are collected only AFTER the
   pointers moved, the reference set is read FROM the pointers, and an empty
   reference set deletes nothing: "Deleting on an incomplete set is how a
   garbage collector eats the live snapshot, so do nothing instead"
   (`:290-309`). Their incident: 76 orphan dirs, 1.56 GB, invisible from the
   recall path.
4. Nonce-owned lockfile with mechanical stale recovery: `recoverStaleLock`
   (`:342-363`) removes a lock only when age > staleMs AND the owner pid is
   dead; release removes it only if the recorded nonce matches: "Never remove
   a lock that no longer proves ownership by this process" (`:399-409`).
5. Three ledgers, never merged (docs_TECHNICAL.md:181-202): retrieval feedback
   / outcome receipts / agent self-attribution. Self-attribution is "reported
   as counts, never as an adoption rate". "Missing data is shown as
   unavailable, never as zero or inferred accuracy." Headline metric is the
   known false-delivery residual, and "how often its answers were actually
   used is reported as permanently unmeasured instead of approximated".
6. Evaluation before ranking (docs_TECHNICAL.md:107-140): a leakage gate
   rejects eval cases whose wording overlaps the target entry; ablation is the
   primary metric (remove the correct memory, rerun, anything still delivered
   is a false delivery); tuning and holdout split with the seed recorded in a
   lock file; "every number is reported with its denominator".
7. Quota ratchet: a hard entry count that only ratchets downward (README:30,
   ARCHITECTURE.md:85-89); the audit "refuses the write, it does not pick a
   victim".
8. Read-only governance surface: the MCP server exposes exactly recall + read;
   "a governance command one token away from an autonomous agent is not
   governance" (ARCHITECTURE.md:76-89). Memory writes stay human commits.
9. Honest no-match: recall distinguishes "nothing matched" from "a gate
   withheld everything" and the abstention names the refusing gate
   (ARCHITECTURE.md:70-74; recall.mjs comment at the tier split).
10. Checksum-implies-verdict performance law: the reader skips re-running JSON
    Schema validation on artifacts whose bytes just matched a declared sha256,
    measured at 86 ms Ajv per cold recall, 20% of it (`:130-137`).

## Steal mechanisms (organ + falsifiable probe)

### S1. $0 deterministic recall lane beside the context pack
- Organ: `mag/context_pack.py` `build_context_pack` (mag/context_pack.py:638).
  Verified this session: it clips FIXED files every turn regardless of task
  (brief, live_from_grok, attention at 600 chars, operator_directives 2800,
  todo 500; mag/context_pack.py:687-691). There is no query-conditioned
  selection: every seat gets the same clips. The brief's framing ("context
  pack builds server-side") is the ask's material; what I verified locally is
  the fixed-clip, task-blind shape.
- Steal: compile the estate's law corpus (memory/rib/*.md + AGENTS.md clippy
  bullets + watch/inbox law rows) into a checksummed JSON snapshot; add a
  recall step that picks which 1-3 law files reach THIS task's context, using
  OwnMem's exact+BM25F lanes, zero model calls. Pairs with the quota ratchet
  (S1b): a cap that only ratchets down, forcing retire-before-add on the rib
  corpus the way RACTER50 retired skills.
- Probe (falsifiable): take 20 past sessions whose close receipts name the law
  that actually mattered; run a local BM25F snapshot over memory/rib/ + the
  clippy bullets per session task and measure Recall@3 against that ground
  truth, plus per-query wall time with a socket guard proving zero network.
  Kill condition: if local recall Recall@3 < the fixed-pack's coverage of the
  same 20, or per-query cost > 50 ms, the lane is dead and the fixed pack
  stands. If it wins, land it as a `mag.cmd recall` beside `context-pack`.

### S2. Refuse-and-rebuild encoding contract for estate derived caches
- Organ: the estate's derived caches with writer/reader coupling, today the
  corpus FTS5 index (B2-465 daily rebuild, `tools/corpus_fts_rebuild.py`) and
  the verkle chain read path (`mag/verkle_knot.py`, launch-verified via
  `_verify_tip_chain` mag/context_pack.py:608-637, which degrades to
  UNVERIFIED instead of blocking boot).
- Steal: OwnMem's "exactly one readable encoding per artifact" + reader
  validates every checksum on load + mismatch means rebuild-from-source,
  never a second reader for an old encoding. For the FTS index: a schema
  version row in the index that the reader checks and a rebuild-on-mismatch
  path (it already exists as the rebuild writer; the missing half is the
  reader refusing rather than degrading to scan fallback silently).
- Probe: grep `tools/corpus_fts_rebuild.py` + the corpus_search read path for
  version/fallback branches on index encodings. If any old-encoding reader
  branch exists, the steal lands (delete it, refuse+rebuild instead); if zero
  exist, the law already holds and the confirmation gets banked. Second
  probe: verify one estate snapshot-style cache actually re-verifies content
  hashes on read (the verkle chain does; the FTS index does not - it has a
  freshness gate, B2-102, which detects staleness but does not checksum the
  index body).

### S3. Nonce-owned lock release for fleet lockfiles
- Organ: fleet lockfile incidents handled by hand. Receipt in the estate's own
  git log: commit bdbb1714e "Stale 11h index.lock from a quota-killed lane
  removed after verifying no git process" - a human executed exactly
  OwnMem's `recoverStaleLock` three-condition test (age > stale AND owner pid
  dead AND, on release, nonce match) as judgment.
- Steal: port `recoverStaleLock` + nonce-ownership release semantics into a
  `scripts/` helper (or `mag/` lock util) so any lane hitting a stale lock
  runs the mechanical test instead of operator judgment; refuse removal when
  the pid is alive regardless of age.
- Probe: unit-test the helper on a planted lock: (a) fresh lock, live pid ->
  refuses; (b) old lock, dead pid -> removes; (c) old lock, alive pid ->
  refuses; (d) nonce mismatch at release -> leaves the lock. Falsified if any
  estate lock consumer already implements pid-liveness+nonce release (then
  this collapses to a pointer to it).

### S4. Three-ledger s

== pam.md ==
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
   (`cli.py:450-453`) is the only signa