# Verkle-chain structural coherence vs vector-embedding similarity

- Seat: ZCode night shift, free-lane analysis (ask: `memory/frontier/HELP_WANTED.md` 2026-10-03, "deep analysis of verkle coherence vs vector embedding"). Relaunch of a first attempt that died on an account rate limit.
- Date: 2026-10-04 (night of 10-03). Read-only except this file. Not committed.
- Instruments named per fact. Python = `.\.venv\Scripts\python.exe`; FTS read via `sqlite3` URI `mode=ro`; content grep = Git Bash `grep -r` (ripgrep-equivalent); chain counted by chunked line read, not `wc`, per ask.

## (a) Measured facts about each surface

### A1. memory/biography/verkle_chain.jsonl (chunked line read, first read 2026-10-04 ~08:50Z)

- 11,248 rows, 8,009,365 bytes. Row keys (last row): `ts, filename, leaf_hash, session_id, start_minute, end_minute, dominant_theme, theme_vector_normalized, tension_index, dossier_commit, amended, index, n_leaves, parent_verkle_root, verkle_root`.
- 11,248 distinct `session_id` values = exactly one row per session; `configs/mag.yaml` says `chain_mode: v1` (amend-in-place), confirmed by 0 rows carrying `chain_mode: v2`. 3,088 rows flagged `amended: true`.
- What the hashes actually bind: `mag/verkle_knot.py::build_leaf_from_dossier` + `_leaf_hash` make `leaf_hash` = sha256 over the canonical JSON of a session's SCALAR DOSSIER SUMMARY (8-dim theme vector, tension/residual/Q/gap proxies, `dossier_commit` hex, chord commitments). The chain binds session-topic summaries plus an indirect pointer (`dossier_commit`) to full dossiers. It does NOT bind session transcripts, receipts, or any prose artifact.
- Theme coverage is weak: `dominant_theme` is null in 6,227 of 11,248 rows (55%). Top non-null: biography 1,189, autonomous_janitor 839, mag_hands 549, constitution 118.
- Day coverage is 24 distinct days (2026-08-10 -> 2026-10-04) with holes, the largest being 2026-09-12T02:24Z -> 2026-09-26T20:23Z (14 days). Volume is bursty: 09-30: 252 rows, 10-01: 110, 10-02: 55, then 10-03: 2,281 and 10-04: 3,068 rows in the first hours (auto-session flood; only 46 + 17 of those carry the autonomous_janitor theme, the rest are other generated session ids).
- Integrity, verified live this shift: recomputed Merkle root over all 11,248 leaf hashes == last row `verkle_root` == `verkle_tip.json` root (`93ba598e...`, n_leaves 11,248). During the analysis an earlier read caught a mid-amend moment (tip `35a931...` vs tail `10f9d8...` at the same n_leaves) that self-resolved to full agreement minutes later: the chain is under active concurrent writes right now, and the writer's verify gate is doing real work.
- Knot-directory cross-check: `memory/biography/knots/` holds 28,443 `*.knot.json` files vs 11,248 chain rows (about 17,200 knot files are unreferenced by the current chain), attic 6,419, legacy pointers 1,352, v2 pointers 13,143; 52 of 11,248 chain-referenced knot files are missing on disk (0.46%).
- What append/amend guarantees (read of `mag/verkle_knot.py`): cross-process single-writer lock (`.verkle.lock`, O_CREAT|O_EXCL, stale-break); integrity gate `_verify_chain_consistent` refuses to extend a chain whose recomputed root disagrees with the tail row or the tip (root AND n_leaves AND last_leaf_hash); pure append costs O(n) hash work and one appended line; v1 amend rewrites the whole file through tmp + `os.replace` (crash-safe) and retires the old knot to the attic instead of unlinking (bytes preserved); B2-393 keeps the file LF-only at byte level; post-append self-verify heals same-second race roots; `prove()` builds an O(log n) inclusion proof (index + sibling path -> root), and `VerkleProof.verify` binds the leaf count so a proof cannot be replayed against a different-length chain.

### A2. memory/corpus/LINKS.jsonl (line read + json parse)

- 302 rows, 320,033 bytes, ts 2026-09-18T00:00Z -> 2026-10-03T22:53Z. Kinds: gala 149, x-drop 50, steal 13, build 9, drop 8, harvest 7, plus ~44 more singleton kinds. All 302 rows carry an `id`; 10 ids are duplicated.
- Row shape: `{ts, id, kind, title, src, author, lane, load_bearing, decision_changed}`. `src` points at an artifact path or URL; there is no `dst` field: the "graph" is a curated provenance ledger whose edges point outward to source artifacts, grouped by `lane` (e.g. gala-20260925/A).
- This is the estate's highest-signal, smallest surface: hand/seat-curated decisions with `load_bearing` one-liners. 302 rows total.

### A3. catalog/catalog.jsonl + catalog/catalog_fts.sqlite (line read; sqlite ro)

- catalog.jsonl: 1,040,765 rows, 296,517,251 bytes. Row: `{id, path, bytes, mtime, zone, ext, title, age_days}`. Zones: memory 552,942; lsa 301,924; runs 54,350; ext:lsa_reboot_stagi 52,992; intake 18,972; ext:mag-backup.git 12,953; watch 4,702; 57 zones total including game-server cores, pytest tmp dirs, and reddit archives.
- FTS (`catalog_fts.sqlite`, fts5 virtual table `corpus` over `crows`, columns `path, title`): 917,885 rows indexed vs 1,040,765 catalog rows = 122,880 rows (11.8%) behind; meta says `catalog_bytes` 261,013,216 vs actual 296,517,251; built 2026-10-03T13:00:12Z by tools/corpus_fts_rebuild.py. The B2-465 daily rebuild has not caught up with today's catalog growth yet.
- Critical shape fact: the FTS indexes FILENAME AND TITLE ONLY, never file content. Measured noise: `receipt` -> 12,596 docs led by `farm_receipt_5554.png`; `census` -> 2,340 docs led by pytest-tmp copies of AGENTS.md; `throttle` -> 11 docs all from the evennia corpus mirror.

### A4. memory/lenses/corpus_index.json

- `research_lens.v1`, 107 items keyed `{pack_id}::local|remote`; each item: pack_id, source, title, ask, answer_excerpt. Retrieval is key enumeration; there is no similarity query. This is the closest existing thing to a semantic surface and it is 107 Q/A research packs, not an index.

### A5. Embedding infrastructure that exists today (grep over live code)

- `mag/flock_scheduler.py` lines 34-68: a local Ollama embedding call (`nomic-embed-text` / `all-minilm` via `/api/embeddings`) used to place flock tasks in an invariant space. `mag/rel_mem_eval.py` is an eval harness stub that runs with no model. No embedding index exists over receipts, biography, ribs, or LINKS.

## (b) The three probe questions

### P1. "What landed right after the GALA (2026-09-25 night)?"

- Structural query 1 (chain neighbor): filter chain rows to `2026-09-25T20:00Z..2026-09-26T10:00Z`. Result: ZERO rows. The gala falls inside the chain's 14-day hole (09-12 -> 09-26); the first post-gap row is 09-26T20:23Z (autonomous_janitor), ~14 hours after the gala lanes closed. The chain is exact where it has coverage and silently empty where it does not.
- Structural query 2 (LINKS): `sorted(r for r in links if r.kind=='gala')` gives all 149 gala lane outputs (ts 2026-09-26T04:18Z onward), and the first non-gala rows after the gala closed are a clean answer: 09-26T12:05Z `instrument-correction` (qagg single-gap receipt corrected), 20:22Z `drop` (PICASSO deletion thesis), 20:30Z `drop-refraction` (State XI refuted), then 09-27T01:22Z `doctrine` (ENHANCE NOT BYPASS) and 01:47Z `self-steal` (ATLAS). Two lines, exact, with `src` pointers into watch/inbox.
- What embedding kNN would have returned: documents semantically similar to gala text - other festival-named receipts, width-probe receipts, anything about parties or showcases - with no ordering and no relation to "what came next". Wrong tool.
- Winner: structural (LINKS). The chain would win adjacency questions only inside covered windows, and only at session-topic granularity.

### P2. "Find receipts citing this file" (targets: watch/inbox/GALA_20260925.md, tools/census_drift_patrol.py)

- Structural query: `grep -rl "GA_LA_20260925\|gala_20260925" watch/inbox memory/rib docs AGENTS.md` (excluding .mimosa hook-state): 749 curated files cite the gala path. Same for `census_drift_patrol`: 370 files. Exact, complete, instant, and every hit is a true citation by construction.
- FTS: cannot answer this at any quality - it indexes the file's own path/title, not who cites it.
- Embedding kNN: cannot express "contains this exact string". Nearest neighbors of the gala receipt are documents ABOUT the gala; similarity conflates reference with aboutness and would mix the 749 citers with the 100+ about-docs with no way to tell them apart.
- Winner: structural, outright. This is the provenance/audit class (who cites X, which hash binds Y, does leaf i sit in root R - `prove()` answers that last one in O(log n)).

### P3. "Find everything the estate recorded about paid dispatch dying on rate limits, whatever words it used"

The concept genuinely spans at least six vocabularies (the 03:00Z spend-drain bug, 429 storms, 1302 errors, throttling, quota caps). Measured fragmentation:

- FTS over titles/paths: `429` 5 docs, `rate limit` 56 (mostly doc mirrors and the evennia library), `throttle` 11 (all evennia corpus), `quota` 244, `1302` 323 (mostly raw memory-zone dumps), `usage cap` 0, `spend` 178. Mostly corpus mirrors, not estate receipts, and the sets barely overlap.
- Content grep in the curated zones (watch/inbox + memory/rib): `429` 1,261 files, `quota` 698, `1302` 486, `rate-limit` 386, `rate limit` 264, `throttl` 181. Six near-disjoint sets; the union needs a dedupe pass; and a seat that does not already know the token `1302` (a z.ai-specific error code) finds none of those 486 files by FTS or by the obvious query.
- What embedding kNN would do: one query over receipt CONTENT vectors would recall across all six vocabularies at once, because "429-storm", "1302s until the window decays", and "hoarding funded budget while free lanes grind" sit close in embedding space despite sharing no tokens.
- Honest scope note: no embedding model was run tonight (no paid APIs; the local nomic-embed-text is wired only for flock). The embedding side of P3 is argued from the measured vocabulary fragmentation above, not from a live kNN run.
- Winner: embeddings, on the evidence of fragmentation. This is the paraphrase/synonym recall class, and the current estate has no surface that answers it in one query.

## (c) Verdict

Structural coherence wins when the question is about TRUTH OF RELATION, not nearness of meaning:

- Provenance and audit: citations (P2), hash binding, inclusion proofs. An embedding index cannot tell you a receipt was edited after the fact; the chain gate caught real mid-amend inconsistency during this very analysis.
- Exact event adjacency where a curated ledger covered the event (P1 via LINKS).
- Determinism: the same structural query returns the same answer forever, and the answer is a citable receipt path - which is what the shared-surface contract and citation lint are built on.

Embeddings would win when the question is about MEANING ACROSS UNCONTROLLED WORDING:

- Paraphrase recall over the estate's own vocabulary churn (P3), where the asker does not know the exact token (1302), filename, or lane name.
- Aboutness over the 1M-row catalog, where FTS is titles-only, 11.8% stale, and dominated by corpus mirrors.

But the measured facts cap the prize: the chain has 24 days of coverage in a 55-day window, 55% null themes, 17k unreferenced knots, and 302 total LINKS rows. Embeddings do not fix any of that - an embedding index over a surface with holes embeds the holes. The two are complements: structure says WHAT HAPPENED AND WHAT POINTS AT WHAT; embeddings say WHAT ELSE READS LIKE THIS. Neither substitutes for the other, and the estate's effect-authorization path (switchboard/effect broker) should only ever consume the structural one.

## (d) Recommendation + law row candidate

ONE recommendation: do NOT adopt an estate-wide embedding index. Run the smallest falsifiable pilot, scoped to exactly the measured failure class (P3), using infrastructure that already exists:

1. Embed ONLY the curated zones - `watch/inbox/**/*.md` + `memory/rib/*.md` (bounded: watch is 4,702 catalog rows, rib is ~60 files) - with the local Ollama `nomic-embed-text` already wired in `mag/flock_scheduler.py`. No paid API.
2. Store vectors in a sidecar sqlite (path, vec blob) next to the FTS index, with a manifest row (row count + sha256 over the embedded path list) committed into the verkle-audit surface so index drift and index tampering are detectable.
3. Falsifier, fixed in advance: build a 20-question paraphrase battery from receipts already found by the six-token grep union (start with the rate-limit set). Ask each question WITHOUT its tokens. If local-model kNN@10 recall of the known-receipt set does not beat the FTS-title + single-token-grep baseline by at least 2x, embeddings are rejected, and the money goes to the cheaper measured defect instead: the FTS indexes no file content at all.
4. If kept, embeddings are a SENSING surface under the existing free-lane law: outputs are banked as findings, never as done/trusted work, and never authorize effects.

Law row candidate (for AGENTS.md Clippy list or a rib):

- "RETRIEVAL LADDER (2026-10-04): provenance, adjacency, and audit questions ride the structural surfaces (verkle chain, LINKS.jsonl, exact-string grep) - exact, deterministic, citable, tamper-evident; semantic recall may run as a sensing overlay over curated zones only (local embedder, sidecar index, manifest-bound), its outputs are findings never receipts, and no embedding result authorizes an effect."

Plain hyphens only in this file; no em-dashes. Receipt ends.
