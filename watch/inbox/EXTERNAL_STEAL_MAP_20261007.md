# EXTERNAL STEAL MAP 2026-10-07 - who does this better, mapped onto our gaps

Written 2026-10-07 by the Hermes seat (contractor lane). First issued with the four external arms IN FLIGHT; the arms
landed the same session and this file is AMENDED IN PLACE, not rewritten (the estate's own rule, GAP_REGISTER: "if
a09-a14 land later, they amend this register, they do not rewrite it"). Sections 1 and 2 are carried verbatim from the
first issue; corrections to them are recorded in section 4 rather than silently spliced. No em-dashes in this record.

## 0. Dogfood provenance: our instruments produced this, not my memory

Every number in section 1 is tool output captured this session, verbatim from the estate's own organs:

- `main.py self-steal` (2026-10-07T14:22:06Z), schema `self_steal.v1`
- `main.py gap-map` (2026-10-07T14:22:10Z), schema `gap_map.v1`
- `main.py gap-map --stack-status`
- The recon counts in section 2 are `grep -rliE` word-boundary file counts over `mag tools configs docs
  corpus/steal memory watch`.

## 1. What our own instruments say (the dogfood)

### 1.1 self-steal: the estate's answer to "who already has this" is itself, 14 times

`self_steal.v1` tracked 22 capabilities and raised **14 findings**. The six shown in the head (the remaining eight are
in the full JSON, not carried here):

| capability | utilization | age | module | wired | recommendation |
|---|---|---|---|---|---|
| cache_map | stale | 3,239,646 s (37.5 d) | `mag/cache_map.py` | true | report-only |
| session_maze | stale | 592,863 s (6.9 d) | `mag/session_maze.py` | true | report-only |
| dogfood_audit | stale | 3,230,835 s (37.4 d) | `mag/dogfood_audit.py` | true | report-only |
| surface_steal | stale | 2,482,656 s (28.7 d) | `mag/surface_steal.py` | true | report-only |
| whisper_image | stale | 3,230,835 s (37.4 d) | `mag/whisper_image.py` | true | report-only |
| shader_bus | stale | 3,230,835 s (37.4 d) | `mag/shader_bus.py` | true | report-only |

Read that as written: **built, wired, and unused.** `surface_steal` is 28.7 days stale, which means the module whose
name literally means "steal from the surface" has not run in a month. `dogfood_audit` is 37.4 days stale. This is the
register's meta-gap 1 (MINED-NEVER-SCHEDULED) reappearing as an instrument reading rather than a prose claim, and it
is the first answer to the operator's question: before we shop outside, we own 14 stale capabilities that were each
someone's answer to a gap.

### 1.2 gap-map: the cheap-vs-frontier split, measured

`gap_map.v1`, `success_bar` 0.6, 3 cheap-capable shapes:

| task_shape | cheap_calls | cheap_success_rate | cheap_avg_usd | frontier_gap |
|---|---|---|---|---|
| janitor | 57 | 0.842 | 0.020723 | false |
| **route** | **2,307** | **0.244** | 0.054982 | **true** |
| audit | 3 | 0.000 | 0.000000 | true |

Its recommendation, verbatim: `stack+batch-elevate frontier-gap shapes to grok; keep cheap for the rest`.

The load-bearing number is **route: 2,307 cheap calls at a 24.4 percent success rate.** Three quarters of the
estate's cheapest and most frequent act fails by the estate's own measure. `--stack-status` adds: complexity 5.0
against a 6.0 threshold, items 2, `ready_to_batch_elevate: false`.

### 1.3 The contradiction this exposes

My behavioural audit measured `usage.jsonl` at 159,537 `ok: true` against 4,953 `ok: false`, which is a 97 percent
success rate. `gap-map` measures the `route` shape at 24.4 percent. Both are the estate's own numbers over the same
estate. So either the two surfaces define success differently, or the `route` failures are being recorded as
successes somewhere upstream. This is the `fake_success` class (139 recorded in `behavioral_events`) showing up as an
instrument disagreement, and it is worth resolving before any cost-per-outcome work lands. IN FLIGHT: the first
external arm is explicitly tasked with how the observability field handles outcome attribution, which is the same
question.

## 2. Our gaps, and what we already know about the outside

Recon before shopping, so the arms do not re-buy the shelf. Word-boundary file counts (the earlier substring counts
were inflated: `arize` matches "summarize", `weave` matches "memweave", so those two are discarded as grep artifacts):

| outside player | files naming it | verdict |
|---|---|---|
| mem0 | 124 | known deeply |
| sentry | 101 | known (error grouping is the GN-3 cure, but not obviously used for that) |
| letta | 94 | known deeply |
| zep | 69 | known deeply |
| memgpt | 65 | known deeply |
| graphiti | 55 | known deeply |
| langfuse | 14 | **thin, and it is the cost-per-outcome answer (EG-07)** |
| in-toto | 6 | **near-zero** |
| sigstore | 4 | **near-zero (the chain's nearest outside analogue)** |
| rekor | 3 | **near-zero** |

So the memory-stack family is already on the shelf and the transparency-log family is not. The counts for
`cognee`, `langmem`, `immudb`, `trillian`, `transparency log`, `fingerprint`, `semconv`, `openinference`, `langsmith`
and `phoenix` did not complete: the grep loop hit its 240 s timeout after the tenth term. That is a stated gap in this
card, not a zero.

Existing estate steal infrastructure the arms were told to respect: `configs/steal_protocol_repos.yaml` (11 orchestrator
and blackboard repos, schema `steal_protocol_repos.v1`, as_of 2026-08-05), `mag/corpus_selfsteal.py`,
`mag/surface_steal.py`, `main.py self-steal`, plus today's fresh folds `corpus/steal/MASTER_MORNING_BLOCK_20261007.md`
(8 lanes, 36 rows) and `MASTER_GSTD_MYCHELIAL_KICKOFF_20261007.md`.

## 3. The four external arms: LANDED

Dispatched 2026-10-07 as `deleg_25f1d9bd`, four parallel read-only researchers, 645 s total. Each was told: read-only,
no `.env`, byte cites or URL on every claim, no em-dashes, name the mechanism and not the product, and say what a
Python estate can copy in one sitting. All four completed and returned structured mechanisms with URLs.

| arm | question | our gap it serves | status |
|---|---|---|---|
| A | Cost-per-outcome attribution, and error-signature clustering and dedup at scale | EG-07, GN-2, GN-3, and the 1.3 contradiction | LANDED, 10 mechanisms |
| B | Verifiable provenance for append-only records, and compaction without losing verifiability | GN-4, the chain, EG-10, receipts-before-claims | LANDED, 9 mechanisms |
| C | Cross-surface session memory consolidation, and the write cadence that stops summaries going stale | EG-01, EG-16, EG-24, zknot | LANDED, 7 mechanisms |
| D | Open-loop and commitment tracking, Stop hooks, and promises that age visibly | EG-02, EG-16 open loops, meta-gap 1 | LANDED, 9 mechanisms |

Transcripts: `AppData/Local/hermes/cache/delegation/live/deleg_25f1d9bd/task-0..3.log`.

## 4. THE FALSIFIER PASS: what the arms corrected, and what I corrected back

This section is the point of the exercise. Three of my own figures failed reproduction and I concede them; one arm
headline did not survive my read of the code.

| item | my first figure | measured now | verdict |
|---|---|---|---|
| `verkle_chain.jsonl.bak-*` copies | "about 16" | **28** (`ls` piped to `wc -l`) | MY FIGURE WAS WRONG, corrected to 28 |
| knots.bak tarballs | 66.9 MB and 83.7 MB | **66,918,400 B** and **83,742,720 B** | BOTH RIGHT: 66.9 decimal MB = 63.8 MiB, 83.7 MB = 79.9 MiB. The arm's "64 MB and 80 MB" is the same bytes in binary units. Unit mismatch, not a dispute |
| `INDEX.json` carries `event_count` 12,055, `active_items` 3,480, `derived_at` | stated as INDEX.json fields | those keys are **absent** from `INDEX.json` (all read as None); only `fold_warnings` is present, and it is a **list of 179**, verified | MY ATTRIBUTION WAS WRONG. The 179 stands; the other three figures live on a surface I have not identified |
| `index_events.jsonl` length | "past 12,055 events" | **12,138 lines** (`wc -l`) | the figure was stale and the log is growing |
| chain is unsigned | not previously stated | `ed25519` 0, `signature` 0, `sigstore` 0, `cosign` 0, `witness` 0, `checkpoint` 0 hits in `mag/verkle_knot.py` | CONFIRMED by my own grep: nothing in the chain module signs anything |
| duplicate-last Merkle padding | not previously stated | `mag/verkle_knot.py:216` `right = layer[i + 1] if i + 1 < len(layer) else left`, and the docstring at `:222-228` calls it "the legacy duplicate-last Merkle root" | CONFIRMED at the line |
| arm claim: "an inclusion proof is replayable against a different-length chain because callers can skip the leaf-count check" | the arm's headline | `mag/verkle_knot.py:588-597` documents exactly this under **T1W1 ticket 12 (2026-10-01, RACTOR law L3)** and the mitigation is **already shipped**: `verify()` takes an optional `n_leaves`, refuses indices outside `0..n_leaves-1` and any path whose depth is not exactly `(n_leaves - 1).bit_length()`; `prove()` passes it; pinned by `tests/test_t1w1_ractor_fixes.py` | ARM CLAIM WAS INCOMPLETE, not wrong. The residual is narrow: a caller who cannot know n may omit it and get the legacy root-only check |

**The consequence, stated plainly: the estate's single biggest external steal was already half-built on its own shelf
six days ago.** The RACTOR pass of 2026-10-01 reached the RFC 9162 insight unaided and shipped the leaf-count binding.
What is genuinely still missing is three named things, in ascending cost: the padding itself is still duplicate-last
(the binding mitigates it and does not remove it, because `[a,b,c]` and `[a,b,c,c]` still share a root), the tip is
unsigned, and there is no second party.

Two more honest notes on the arms' own output: the "8 consecutive block cap" for Claude Code Stop hooks is that arm's
own CLAIM from a third-party blog, not vendor docs; and one arm cited `watch/inbox/ESTATE_GAP_DIG_20260404.md`, a date
that does not exist (the file is `ESTATE_GAP_DIG_20261004.md`). Both recorded, neither load-bearing.

## 5. THE MECHANISMS, mapped to our gaps

### Arm A: behavioural telemetry and cost-per-outcome

| mechanism | cures | what to copy | effort |
|---|---|---|---|
| **LangSmith feedback record + `run_id` join** | EG-07, open since 2026-08-08 | a second ledger `outcomes.jsonl` keyed by `run_id`; put `run_id` in each `usage.jsonl` row's meta and join cost rows to score rows | S: one ledger, one key, one join |
| **Drain3 template mining** | GN-3, the 7,332 `tool:sha16` signatures | `TemplateMiner` over the error field with numeric/IP/UUID masking, `sim_th` 0.4, depth 4; replaces the opaque sha16 with a template id that actually groups variable error text | **S: pure Python, one sitting** |
| **Sentry multi-hash GroupHash** | GN-3 | `sig` becomes a LIST of fingerprints (app hash from in-app frames plus system hash from all frames); an event joins a group if ANY hash matches; the message fallback normalizes numbers, timestamps and UUIDs to placeholders | S: one field changes type |
| **OTel GenAI semconv field names** | portability of every ledger | rename meta keys to `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.request.model`, `gen_ai.conversation.id`, `error.type`; the standard has tokens and cost but **no outcome**, so pair it with the LangSmith row | S: a rename, no SDK |
| **OpenInference USD cost attributes** | EG-07 | `llm.cost.total` / `prompt` / `completion` as **float** USD; a string cost silently breaks aggregation | S: one float per row |
| **cost per successful task** | EG-07 | `sum(cost of every call in every run) / runs that succeeded`; retries stay in the numerator | S: two ids, one wrapper |
| **ClickHouse `SummingMergeTree` rollup** | GN-2, `reaper-enumerate-error` 97,565 rows with no rollup | `LowCardinality` keys, a token index on message, a materialized view of `count()` by (service, level, minute); the SQL ports to SQLite or DuckDB | M |

### Arm B: verifiable provenance for append-only records

| mechanism | cures | what to copy | effort |
|---|---|---|---|
| **Signed Tree Head / C2SP checkpoint** | the chain is unsigned, verified above | one Ed25519-signed checkpoint per committed head: origin line, tree size, base64 root, signature line (RFC 6962 section 3.5 struct); verify against a pinned key before trusting any root | **about 1 hour: keypair, one sign, one verify** |
| **RFC 9162 domain-separated hashing without duplicate padding** | the legacy padding at `:216` | `SHA-256(0x00 || leaf)` and `SHA-256(0x01 || left || right)`, never duplicate. NOTE: the estate already has tag-based domain separation (`b"leaf:"`, `b"node:"`); the missing half is dropping the duplication | about 1 hour of code, **but the re-hash of 11,621 rows is operator-gated (chain read-only by standing ruling)** |
| **Raft snapshot boundary (`lastIncludedIndex`, `lastIncludedTerm`)** | any future compaction of a log with no boundary metadata | compaction writes a snapshot carrying the index and root of the last folded leaf, kept outside the truncated log | about 1 hour |
| **Merkle consistency proof (RFC 9162 section 2.1.4)** | the estate can only assert `root[i-1]` is a prefix of `root[i]`; it cannot prove it in O(log n), which is what blocks ever dropping the prefix | the SUBPROOF generator and verifier, about `log2(n)` hashes | about 2 hours |
| **immudb prefix truncation retaining proof nodes** | 28 `.bak` copies plus two tarballs with no compaction story | when truncating to offset k, keep the interior hash nodes needed for future proofs and delete only leaf payloads | 2 to 3 hours |
| **in-toto statement in a DSSE envelope** | chain rows are opaque estate JSON | wrap each committed artifact as `{_type, subject:[{name, digest:{sha256}}], predicateType, predicate}` inside `{payloadType, payload, signatures}` | about 2 hours, new rows only |
| **Rekor v2 sharding with a final checkpoint** | one unbounded chain with no rotation | freeze a bounded shard at a signed checkpoint, publish it, start a fresh shard | about 1 day |
| **Tile-based storage (C2SP tlog-tiles)** | the whole file is rewritten on every amend, so writes are O(n) and there is no immutable unit to drop | fixed-size tiles addressed by level, index and width; immutable, so no write ever rewrites history | about 1 day |
| **Witness cosigning (C2SP tlog-witness)** | a solo operator signing its own log detects nothing | a witness stores the last checkpoint it verified, checks a consistency proof, returns a timestamped cosignature; for a solo estate the second machine is the witness | about 2 hours, needs a second party |

### Arm C: cross-surface session memory

| mechanism | cures | what to copy | effort |
|---|---|---|---|
| **Hash-anchored staleness warning (arXiv 2607.20972)** | EG-16 root cause: a frozen summary cannot self-invalidate | hash the anchored file when the note is written; at delivery, if the hash differs, the injected memory carries an explicit staleness warning. That paper measured voluntary memory use at about **zero** (0 memory operations in 114 turns) while deterministic harness-side injection fired in every equipped run | **S: the hash plus the warning line** |
| **Stop-hook per-turn detached extraction** | EG-16: refresh is per-logon, so today's work is missing by construction | one hook per turn writes the delta to a tmpfile, forks a detached worker and returns in about 10 ms; the worker emits a roughly 300-char resumable summary that **keeps failures and dead ends**. ARM NOTE: zknot is already idempotent on session growth (`tools/zknot.py:325`), so only the trigger and the detach are new | S |
| **Zep / Graphiti bi-temporal edge invalidation** | the demotion register is a flat markdown list with no as-of query | four timestamps per edge: `t_valid`, `t_invalid` (event time) and `t'_created`, `t'_expired` (transaction time); on contradiction set the old edge's `t_invalid` and `t'_expired` and **keep the edge, never delete**; retrieval filters both timelines | S/M: a schema field, no new store |
| **Idle-gated two-phase consolidation (Codex CLI Memories)** | EG-16 | a session becomes eligible only after about 6 h idle; phase 1 extracts strict-schema memories and redacts secrets before disk; phase 2 takes a lock and merges into the summary under a git baseline; unrecalled memories age out at 30 days; read switch and write switch independent | M |
| **Provider-plugin transcript multiplexer** | EG-01 | one Provider per store with `discover_files()`, `parse_file(path, content, offset)` (incremental byte-offset parse), `watch_roots()`; wrap the estate's **existing** `mag/chat_source.py` (Grok) and `mag/team_knot.py` (chatSessions) behind one interface plus an offset ledger | M: the readers exist, the interface is new |
| **VS Code chatSessions operation-log decoder** | EG-01's VS Code half, 4,860 prompts | `<uuid>.jsonl` is an append-only operation log: line 0 is a full snapshot (`kind:0`), later lines are Set/Push/Delete patches; sessions are discovered only through `state.vscdb` key `chat.ChatSessionStore.index`; replay snapshot then patches, back up the db, refuse to run while VS Code is open | M |
| **Letta sleep-time consolidation subagent** | EG-24: 47 interactive Grok design sessions nothing points to | split the read path from the write path; the seat is deliberately not given memory-edit tools, and a background consolidator holds them and rewrites the blocks the seat reads | M/L |

### Arm D: open loops and commitments

| mechanism | cures | what to copy | effort |
|---|---|---|---|
| **Dated register with an age bar and a fabrication fail-close** | EG-02 owed board; meta-gap 1 | ARM FINDING: **the estate already owns this shape** in `tools/gate_age_patrol.py` plus `configs/gate_register.json`: rows with an ISO opened date, age = today minus opened, STALLED past the bar (default 14 days), a future-dated opened fail-closes exit 2, and decided rows stay as the closure record. The only work is extending the rows from operator gates to promise rows | **1 to 2 hours, zero new tooling** |
| **Fingerprint ratchet, no silent reap** | unkept promises | ARM FINDING: already landed in `tools/violation_ratchet.py`; debt leaves the register only by a named baseline-update or an explicit prune, never a silent reap. Reuse the same contract for promises | 0, already on the shelf |
| **Stop-hook block contract** | EG-02 change 2 `nextball` never landed | print top-level `{"decision":"block","reason":"..."}` (or exit 2 with the reason on stderr) to force one more turn when a condition is unmet; check `stop_hook_active` first so the gate asks once; judge the CURRENT turn only, anchored to a `UserPromptSubmit` timestamp; exit 1 does NOT block | 2 to 3 hours |
| **Brief-marker plus outcome-file Stop gate** | a promise never reaches a carrier | every brief carries one fixed sentence naming its id and its `outcome.md` path; on Stop the hook compares the outcome file mtime against the brief's arrival timestamp and blocks once if it is missing or older; absent or bad JSON prints nothing and exits 0; no LLM in the hook | 2 to 4 hours |
| **Deterministic action-item extractor** | the 4,860 VS Code plus 47 Grok prompts, unextracted | four regex classes (checkboxes, `ACTION:`/`TODO:`, `@name will`, `Name will ... by <date>`); capture OWNER and DUE; flag **ORPHAN** (no owner: unowned actions die) and **NO-DUE** (undated actions drift); group by owner, orphans last and loud | 2 to 3 hours |
| **Commitment rows with aging status and a dated block id** | no first-seen dating, so an unkept promise cannot age visibly | row shape `text, owner, recipient, deadline, source_file, block_id, extracted_date, status`; overdue past deadline, aging past 7 days with no completion evidence; the boot digest prints only overdue and aging | 2 to 4 hours |
| **Weekly review gate that refuses to close** | no refusal-to-close cadence | evidence first, then a gate that exits 0 COMPLETE or 2 INCOMPLETE and names every missing step; an unskipped mandatory step always forces INCOMPLETE; relay the exit code, do not soften it | 2 to 3 hours |
| **Pre-fire deterministic lint (`dwflint`)** | the 40 percent dwf failure share, 54 of 134 runs failed or cancelled | split the pipeline: deterministic extraction and rule checks, AI only for judgment; extraction at temperature 0 with a strict verbatim-quote requirement, and a deterministic engine rejects any item whose cited text is not in the source; for workflows, lint actor-name uniqueness, report tags against declared artifacts, the report cap, and path plus args shape before the run fires | 2 to 3 hours |

## 6. The ranked steal list (register law: severity x fill-ease, cheapest first inside a band)

| rank | steal | cures | effort | band |
|---|---|---|---|---|
| 1 | Drain3 over the error field | GN-3, the 7,332 signatures consumed at last | one sitting, pure Python | S2 |
| 2 | Signed checkpoint on the tip (C2SP / RFC 6962 section 3.5) | the verified-unsigned chain | about 1 hour | S1, cheapest real cure |
| 3 | `sig` becomes a list (Sentry GroupHash shape) | GN-3, grouping survives refactors | one sitting | S2 |
| 4 | `run_id` in usage rows plus `outcomes.jsonl` | EG-07, open since 08-08 | one sitting | S2 |
| 5 | Extend `gate_register.json` rows to promises | EG-02 owed board | 1 to 2 hours, **zero new tooling** | S2 |
| 6 | `t_invalid` on knots | demotion register gains an as-of query | one sitting | S3 |
| 7 | Hash-anchored staleness warning | EG-16 root cause | one sitting | S3 |
| 8 | Per-turn detached extraction on zknot's existing idempotence guard | EG-16 | one sitting | S3 |
| 9 | OTel `gen_ai.*` rename plus float USD cost | every ledger becomes portable | one sitting | S4 |
| 10 | Deterministic action-item extractor over the August corpora | EG-01, EG-24 | 2 to 3 hours | S3 |

## 7. What this exercise proved about our own systems

Three of the four arms performed the self-steal-first discipline and came back with an estate asset rather than a
proposal: `gate_age_patrol.py` plus `gate_register.json` for the owed board, `violation_ratchet.py` for the
no-silent-reap contract, `tools/zknot.py:325` for the idempotence guard, `mag/chat_source.py` and `mag/team_knot.py`
for the transcript readers. One arm's headline finding turned out to be a ticket this estate closed on 2026-10-01
(T1W1 ticket 12, RACTOR law L3). The shelf is fuller than the gap register implies, which is the same thing
`self-steal` said in section 1.1 with 14 stale capabilities, and the same thing the register said about itself in
meta-gap 1.

## 8. Fold

This card folds to `corpus/steal/MASTER_EXTERNAL_STEAL_20261007.md` so it stops living only inside a `watch/inbox`
window. That fold is the EG-11 cure (corpus fold never run), executed by hand once, on this card's own output.

RECEIPT: read-only for everything except this card and its corpus fold. VERIFIED by my own byte reads this window: 28
`.bak` copies; tarball bytes 66,918,400 and 83,742,720; `INDEX.json` carries `fold_warnings` as a list of 179 and does
NOT carry `event_count`, `active_items` or `derived_at`; `index_events.jsonl` at 12,138 lines; zero hits for `ed25519`,
`signature`, `sigstore`, `cosign`, `witness` and `checkpoint` in `mag/verkle_knot.py`; the duplicate-last padding at
`mag/verkle_knot.py:216` with its "legacy" docstring at `:222-228`; the T1W1 ticket 12 mitigation at
`mag/verkle_knot.py:588-597`; and by tool output `self_steal.v1` 22 capabilities and 14 findings with the six ages
tabulated above, `gap_map.v1` success_bar 0.6 with route 2,307 at 0.244, and `--stack-status` complexity 5.0 threshold
6.0 items 2 ready false. UNVERIFIED: every external URL in section 5 (cited by the arms, not fetched by me); the arms'
own CLAIM lists, in particular the Claude Code 8-block cap and the Codex 6 h idle default; the surface that carries
the `event_count` and `active_items` figures now that `INDEX.json` is ruled out; the six recon terms that timed out;
and the cause of the 97 percent versus 24.4 percent disagreement, which is named in section 1.3 as an open
contradiction and not resolved here.
