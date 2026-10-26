# LBrain dig receipt (gala_20260925 localfirst-steal, lane lbrain, division B)

Banked 2026-10-01T09:11:52Z. Every claim below cites a file read or a command
run THIS session; raw output lives in
`watch/inbox/gala_20260925/localfirst-steal/lanes/lbrain.check.txt` (sections
S1-S9, corrections S3b/S5b/S6b/S9b appended where a first pass was wrong or
incomplete). No em-dash anywhere in this file.

## 0. Headline

LBrain (metavolve-labs/lbrain, BSD-3-Clause) is real and the closest published
cousin the estate's memory organs have: it already runs the estate's
tri-state/citation discipline (evidence grading with UNGRADED never silently
promoted, supersession with mutual confirmation, a write-gate that answers
"should this text be committed at all") on top of a CLI + MCP-server dual
shape. The brief's claims tri-state as: CLI+MCP dual shape CONFIRMED, BSD-3
CONFIRMED, no-account-by-default CONFIRMED, on-device embeddings CONFIRMED as
the unconfigured default but behind an optional extra with hosted Gemini/OpenAI
as first-class configured providers. The R2 question lands the other way from
the brief's framing: FTS5 stays the estate's retrieval organ (measured 0.4 to
6.5 ms over 691,788 rows, sha256-pinned to the catalog bytes); on-device
embeddings are declined for the catalog until a labeled recall bake-off beats
a grammar-fixed FTS, because the measured miss is a query-grammar problem, not
a semantic-recall problem.

## 1. Fetched bytes (first-hand)

- Shallow clones under
  `watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/`:
  - `lbrain` HEAD f9493d902d5f6f329324cc2d3ffd8ce8b5f43c26, 2026-09-16, 201
    tracked files (check S1).
  - `lbrain-coding-agents` HEAD 3ca1a1c193a04351e65b80e352db19f69581dc3b,
    2026-09-05, 32 tracked files (check S1).
- LICENSE sha256 identical in both repos:
  d0d3d085baa247e5d812dc02fbbda2fe3af8432aa9a881e6eac41b0644e779e4; text
  begins "BSD 3-Clause License / Copyright (c) 2026, Metavolve Labs, Inc."
  (check S2).
- GitHub API search saved: `fetched/lbrain/gh_search_lbrain.json`
  (total_count 14; both metavolve-labs repos carry license BSD-3-Clause).

## 2. Claim tri-state (the brief's four claims)

| claim | verdict | byte evidence |
|---|---|---|
| CLI and MCP-server dual shape | CONFIRMED | `pyproject.toml:46-47` `[project.scripts] lbrain = "lbrain.cli:main"`; `lbrain/mcp_server.py:32` `mcp = FastMCP("lbrain")` with 6 tools + 1 resource (census check S3b: decorators at 167/264/303/329/455/483 + resource 408; `serve(transport: str = "stdio", ...)` at 525); the distribution repo ships `server.json` (`"name": "ai.lbrain/lbrain"`, pypi/uvx, stdio) and a paste block "Otherwise add an MCP server named lbrain: command lbrain, args [\"mcp\"], stdio." (check S3) |
| on-device embeddings | CONFIRMED as unconfigured default, PARTIAL overall | `lbrain/embed.py:144` "On-device embeddings via fastembed (ONNX, no torch, no network, no API key)." default model BAAI/bge-small-en-v1.5, 384-dim, about 67 MB; BUT it needs the extra `local = ["fastembed>=0.3,<1"]` (`pyproject.toml:37`, check S4), the module docstring reads "Gemini (GCP-native, default) or OpenAI" (`embed.py:1`), the dataclass default is `embedding_provider: str = "gemini"  # fallback only` (`config.py:167`), and `Config.load()` at `config.py:277-301` makes NO-config fall toward local: "Unconfigured falls back to on-device." (check S4). Dim migration is a class, not a flip: "384 != the hosted default of 1536 ... a re-embed migration" (`embed.py:154-157`), guarded by `Store.embedding_config_status` drift states model_changed/dim_changed (`telemetry.py:16`) |
| BSD-3 | CONFIRMED | LICENSE bytes + GitHub license field (check S1/S2) |
| no account by default | CONFIRMED, one opt-in seam | outbound host census over the whole main repo (check S5b): arweave.net (7), generativelanguage.googleapis.com (5), turbo.ardrive.io (2), api.openai.com (2) and nothing else; `telemetry.py` is a READ-ONLY local Prometheus exporter ("A metric that cannot be measured is OMITTED, never reported as a false zero"); `identity.py:9-10` "an unregistered brain is a first-class state, not an error. Identity accretes onto an anonymous install; it never gates one." The seam is opt-in growth, not a gate: "The free name is generic. Make it permanent: https://lbrain.ai/claim.html" (coding-agents PASTE-TO-YOUR-AGENT.md:15, check S5) |

The strongest single byte in the repo is the red-team history at
`config.py:277-283`: the old default (gemini + env-harvested key) meant the
README's own step 3, "runnable without `init`," "shipped the corpus to Google
on a key the user never pointed at LBrain. Verified 2026-07-28 (red-team
finding 12)." (`config.py:281-282`.) The fix is the law shape the estate
already holds: provider
selection comes from an explicit init and nowhere else, and an unconfigured
install fails toward local, never toward a hosted provider.

## 3. On-device embeddings vs FTS5 for the catalog (the ask's R2 question)

Measured on this tree this session (check S6, S6b):

- The ask said 581K rows. Measured truth: catalog.jsonl holds 691,788 lines;
  the FTS5 `corpus` table holds 691,788 rows; the meta table pins
  `rows_indexed 691788`, `catalog_sha256
  50cc5c4609475d6638adc5b66acb098517616f0e6dcd5936e8918927f0c1c65c`,
  `built_utc 2026-09-30T13:00:21Z`, builder
  `tools/corpus_fts_rebuild.py (B2-102, shape of B2-22 spike)`. The index is
  byte-pinned to the catalog it was built on. Never difference two counts at
  different moments: 581K was a stale moment, not a smaller catalog.
- bm25 query latency at k=10 over 691,788 rows: 0.4 to 1.5 ms (five natural
  queries), 4.0 to 6.5 ms with quoted-phrase/AND/prefix grammars. Sub-10 ms is
  the ceiling of what a retrieval organ needs; embeddings add a local model
  call (order 10-30 ms on CPU) and cannot beat that on speed.
- The real measured gap is grammar, not recall: 3 of 5 natural multi-word
  queries returned zero hits under FTS5's implicit AND (S6), and an unquoted
  hyphen query is an FTS5 syntax error, byte-caught live: "sqlite3.
  OperationalError: fts5: syntax error near "-"" (S6 traceback, corrected in
  S6b). That is a `mode` field in the tool schema (exact | any + prefix
  fallback), not an embedding purchase.
- Cost of the embeddings alternative (arithmetic, not a measurement): 691,788
  rows x 384 dims x 4 B/f32 = 1,062,586,368 bytes, 1.06 GB raw before
  sqlite-vec/ANN overhead, one vector per row, before chunking multiplies the
  row count, plus the re-embed migration class any provider switch carries.

Verdict: FTS5 stays the served retrieval organ; it is $0 marginal,
deterministic, sha256-pinned, and already 1 ms. On-device embeddings are the
right INSTRUMENT if a labeled recall bake-off later shows the grammar-fixed
FTS missing semantically (paraphrase, synonymy). Declined for the catalog
until then. LBrain's own architecture agrees: it keeps `lair_search` (exact
FTS5, "no embedding call") as a separate MCP verb from `lair_query` (hybrid
BM25 + sqlite-vec cosine fused by Reciprocal Rank Fusion, `search.py:1`).

## 4. Memory organs on the house MCP surface (spec against the bridge admission test)

Admission test: the seven clauses at `watch/inbox/ractor50/mcp.md:107-124`
(one verb one wrapper; stateless or caller-held state; effect class in _meta;
bounded output bounded time; $0 marginal or registry-metered; pin-stable;
never-crosses clean). The R2 memory pair:

1. **estate_corpus_search (R2, the named gap).** ractor50 mcp.md section 8 row
   4 already names it: "exists in the archivist/full surface (and docker),
   absent from the bridge: an external agent gets estate compute but not
   estate memory." Proposed shape, copied from the house pattern
   (`mag/estate_bridge.py:59` BRIDGE_INPUT_SCHEMAS hand-written JSON Schema,
   enum for scope, bounds for numbers):
   - input: `{query: string 1..512, k: integer 1..25 default 10, mode:
     "exact"|"any" default "exact", with_snippet: boolean default true}`;
     additionalProperties false.
   - exact mode = FTS5 MATCH on the caller's tokens as given (implicit AND);
     any mode = OR expansion + unquoted-prefix fallback for the last token.
     Never a hosted embedder call on either mode.
   - output: bounded k hits, each `{rowid, snippet <= 280 chars, catalog_
     sha256, built_utc}` so every hit is citation-resolvable to catalog bytes
     (the citation-resolution law: fetched bytes or UNVERIFIED).
   - _meta: effect_class read, cost_kind deterministic_local, exhaustion
     retry_or_defer; passes all seven clauses; pin row in the same landing
     commit (law MCP-1).
   - falsifier: if any served path can trigger a model or network call on the
     $0 verb, or a hit's rowid does not resolve against the pinned catalog
     sha256, the spec is wrong.
2. **estate_bonds_read (R2.5, the residual store's first crossing).** The
   residual store (residual beads + bonds edges + registry card, `docs/DNA.
   md:14,35`) currently crosses no surface. Read verb only: input
   `{seed: residual id, hops: 1|2 default 1, k: <= 25}`; output bounded bond
   rows `{from, to, kind, weight, leaf_hash}`, hash-carried to
   residual/{id}.json; caller-held state; no seedless enumeration (bounded
   blast radius). Seat scope binds to transport identity (R3 bridge tokens),
   never to a schema argument, on the LBrain persona lesson below.
   Never-crosses (unchanged rulings, confirmed against LBrain's own shape):
   residual WRITE, prune, coarse-grain stay seat-internal; dirac BANK stays
   broker-gated R4 (`mcp-bridge.md:136-137` precedent); write gates answer
   advice only. LBrain's `lair_protocol_check` ("Should I commit this text to
   a lair?" decision tool) is the pattern: grading as a READ verb on the
   write path, the commit itself stays local and gated.

## 5. Steal rows (mapped to estate organs, each with a falsifier)

1. memory-read/memory-write split: exact keyword FTS5 as its own no-embedding
   MCP verb (`mcp_server.py:5` "- lair_search    : exact-keyword FTS5 search (no
   embedding call)"). Steal: estate_corpus_search exact mode as above.
   Falsifier: any network or model call reachable from the $0 verb.
2. unconfigured-fails-toward-local (`config.py:285` "Unconfigured falls back
   to on-device", bought with red-team finding 12). Steal: corpus_search with
   unset embedder config serves keyword-only and SAYS SO in the response;
   never a silent hosted fallback. Falsifier: a build where unset config
   silently selects a hosted provider.
3. two-axis evidence grade, never one score (`grading.py:15-16` "Multiplying
   them back into a single score reintroduces the correlation the scheme
   exists to prevent"; UNGRADED is a declared state, "never silently
   promoted"). Steal: corpus_search hits carry two named axes: source class
   and citation-resolution state (RESOLVED-to-bytes / UNVERIFIED). Falsifier:
   any hit rendering a synthesized claim with observed weight, or an
   UNVERIFIED citation rendered as confident.
4. supersession must not govern (`search.py:35` "where a self-retired
   record NAMES its correction. Three states, never two", plus ruling s3
   mutual confirmation: "True only when the successor THIS record names is
   also the source of an incoming Supersedes edge"); served posture "SUPERSEDED
   must not govern" (coding-agents PASTE-TO-YOUR-AGENT.md:12). Steal: estate_bonds_read
   renders a superseded bond only with its named successor, confirmed only
   when both sides agree; mirrors the estate's receipt-only supersession
   habit (selfsteal.md). Falsifier: an incoming-edge-only pair served as
   confirmed, or a superseded record served without its successor link.
5. persona binds to transport, not to a tool argument (`mcp_server.py:30-42`,
   assignment at 42:
   PERSONA is env-only "on purpose: a model that could pass persona='cfo'
   could read the CFO's private working memory by asking nicely, and draft
   isolation that a prompt can talk its way past is not isolation"). Steal:
   estate_bonds_read and any future per-seat memory verb bind scope to the R3
   bridge token, not to a schema string. Falsifier: a bridge client
   enumerating another seat's scope by passing a scope argument. Note the
   boundary: today's estate_dirac_scan/_rank already guard this the other
   way, `_scope` is a bounded enum (`mag/estate_bridge.py:338-342`), so the
   law applies to new per-seat verbs, not as a defect in existing ones.
6. FTS5 stays; embeddings are an instrument, not a purchase (section 3
   numbers). Falsifier: a labeled recall bake-off where a hybrid lane beats
   grammar-fixed pure FTS on estate questions reopens the purchase.

## 6. Honest gaps

- Not run: LBrain itself. No install, no live MCP session against it, no
  embedding latency measurement of bge-small-en-v1.5 on this host, no hybrid
  recall bake-off (that is the falsifier experiment, deliberately deferred).
  The verdicts above are from fetched source bytes, not from running the
  product.
- The S6 first pass died mid-loop on the hyphen query (FTS5 syntax error,
  traceback kept in the transcript); S6b is the corrected completion. The
  first-pass numbers for the five completed queries stand.
- S9 first claimed a clean mag//tools/ census; false. Real census: 4 untracked
  rows, all sibling-lane files (mag/rib_boot.py, tools/flock_parity.py,
  tools/flock_parity_out/, tools/reverse_map.py). The ratchet was then run
  for proof only: FAIL exit 1, NEW=1 tools/flock_parity.py:1034 file-too-long
  (check S9b). This lane wrote zero files under mag/ or tools/; that NEW row
  is sibling debt, named, not accepted here.
- The catalog census is one moment (2026-10-01 09:11Z window); it will drift.

## 7. Decision ledger

Closes the R2 memory-organ selection question this lane was fired with: the
R2 memory pair on the house MCP bridge is estate_corpus_search (exact mode,
grammar law included) plus estate_bonds_read (bounded, hash-carried read);
dirac's existing read-only crossing is confirmed as correctly scoped; the
residual WRITE path stays never-cross until broker envelopes (R4); on-device
embeddings are declined for the catalog until a labeled bake-off beats
grammar-fixed FTS; the ask's 581K-row premise is corrected to the measured
691,788 at the pinned index sha256. Register row appended to
`watch/inbox/localfirst_memory_landscape_signals.jsonl`; lane JSON at
`watch/inbox/gala_20260925/localfirst-steal/lanes/lbrain.json`.
