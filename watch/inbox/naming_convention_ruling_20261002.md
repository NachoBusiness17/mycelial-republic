# Naming-convention ruling (2026-10-02, lane D of the full-width four)

Class: RECEIPT + RULING · Writer: zcode seat (lane D: address the other seat's
naming-convention plans) · Read-only except this file · Zero em-dash bytes.

## 1. FIND verdict: proposal FOUND as a pointer; the law's full bytes NOT LANDED

The sibling (laptop zcode seat "bob", the monitor/ractor/model-garden-night seat)
proposed FILE_NAMING_AND_CONTEXT_LAW_20261002.md. The only bytes of it on this
machine are the pointer in the handoff direct-drop note, quoted verbatim:

> "Naming law: see FILE_NAMING_AND_CONTEXT_LAW_20261002.md riding the same bridge
> push (SEAT_KIND_slug_date_hash8; context_index.db + MCP verbs
> context_lookup/context_name specced)."
> (watch/inbox/handoff/ZCODE_HANDOFF_README_20261002.md:82)

Searched for the law file itself, all negative, with the command evidence:

- Handoff zip: 20 files listed, zero basename match (`unzip -l ... | grep -ci
  file_naming` = 0). Zip fully extracted and grepped: the title appears 0 times
  across all 16 trajectory logs, HANDOFF.md, and SEED_MANIFEST.sha256.
- BRIDGE_LOG.jsonl (named by the note): does not exist anywhere in the repo
  (`find . -maxdepth 3 -name "BRIDGE_LOG*"` exit 1); the bridge/ dir is stale
  (last write Sep 16).
- Repo tree: `grep -rl FILE_NAMING_AND_CONTEXT_LAW` over md/jsonl/json/txt =
  exactly 1 hit, the README pointer itself.
- watch/inbox Oct-2 top-level files enumerated (18): no basename match; seats/
  does not exist at repo root.
- Other sibling surfaces carry no naming proposal (incidental word uses only):
  watch/room.jsonl (Aug/Sep chatter), MONITOR_LANE_2026-10-01/02.md (openalex
  links), ractor_engine/* (24 files, all "a receipt naming X" idiom),
  STANDING_WORKFLOWS_20261001.md, memory/plans newer than 10-01
  (ARCHEOLOGY_20.md, XMODEL_BURN_20.md, BURN_PLAN_140.md),
  .zcode/workflow-drafts/*.dwf.ts (12 files), DRIFT_PATROL_20261002.md
  (pre-checked by the coordinator before the fan-out).

Consequence: every ruling below is PROVISIONAL ON THE LANDED POINTER. Three
components are nameable from it; any other clauses in the law are unruled until
its bytes ride a bridge arrival (adoption plan, line 2).

## 2. The estate's actual naming today (evidence table)

| Surface | Real pattern | Evidence |
|---|---|---|
| mag/ + tools/ modules | snake_case VERB_NOUN | ls mag/: build_*, verify_*, flag_*; ls tools/: ask_bank.py, anomaly_flagger.py |
| watch/inbox receipts | ALLCAPS_VERB_NOUN_YYYYMMDD dominant: 796 of 1,109 top-level md (72%); 99 lowercase_date; 63 undated | ls + grep -cE on watch/inbox/*.md |
| Seat attribution | SEAT_ prefix already used for cross-seat artifacts: 31 files (CODEX_TASK_*, ZCODE_HANDOFF_*) | ls watch/inbox, grep -cE '^(ZCODE\|GROK\|HERMES\|CODEX\|CLAW\|OPENCLAW)_' |
| tests/ | test_*.py law with patrol falsifier: 500 files, 3 non-test_ (conftest.py standard + 2 helpers); naming law precedent B2-389 landed 09-26 | watch/inbox/burn_wave_20260926/B2_389_selftests_namespace_20260926.md |
| workflows | kebab-case + .dwf.ts (ractor-engine, fill-ball, olm-mine) | ls .zcode/workflow-drafts |
| name discovery | the filename IS the index: FTS5 over path+title tokens; "its recall is bounded by naming discipline" | watch/inbox/burn_reset_20260927/flash50/w4-multimodal.md:28 |
| path coupling | INDEX.json folds 8,736 path-keyed events into 2,580 items (append-only log is source of truth, derived 2026-10-02T12:06Z); verkle pyramid 7,377 knots; receipts cite path:line (citation lint a05-r2) | watch/inbox/INDEX.json; state/verkle_pyramid_seed.json; AGENTS.md |
| pointer-name precedent | an estate index surface can hold THREE name families that join by rule, so a one-scheme law must scope or break | watch/inbox/POINTER_INDEX_REPORT_20260911.md:31 |

## 3. Rulings on the three landed components

### R1. Filename law SEAT_KIND_slug_date_hash8: ADOPT, AMENDED SCOPE (cross-seat transfer artifacts only; no retro-renames)

Already true where it matters: the proposer's own arrival landed as
ZCODE_HANDOFF_README_20261002.md and
ZCODE_HANDOFF_session-full_20261002-0900_1ea31bae.zip (SEAT_KIND_slug_datetime_
hash8 exactly, self-dogfooded), and 31 inbox files already carry SEAT_ prefixes.
Amendments, named exactly: (a) scope = watch/inbox/handoff/ + bridge pushes only;
the 796 ALLCAPS_DATE inbox receipts are a different, dominant, working family and
are left alone; (b) hash8 is mandatory only for byte-frozen archives (zips; a bare
md cannot self-hash), datetime allowed alongside the bare date the proposer used
on the README. Retro cost, rejected: 2,580 path-keyed INDEX items, append-only
event-log churn, path:line citations across the corpus, verkle knots, git blame.
New-artifact-only is free.

### R2. context_index.db: REJECT (duplicate index; cost = a second decaying surface)

The estate already runs two live name/context channels: the INDEX.json fold
(index_events.jsonl, 8,736 events, derived 2026-10-02T12:06:55Z, 2,580 active
items) and corpus FTS5 (catalog/catalog_fts.sqlite + the B2-465 daily rebuild
task). A third db duplicates both and will drift; the FTS decay disease B2-465
exists precisely because unowned indexes rot. The need the pointer names (context
over arrivals) is served by pointing corpus_search at the arrival dir. Rejected
on cost, not on need.

### R3. MCP verbs context_lookup / context_name: REJECT (verb-surface creep against a landed one-per-verb law)

The house MCP bridge landed under a one-tool-per-verb naming law:
"the estate's five verbs (six tools, one per verb per the design's naming law)"
(watch/inbox/gala_20260925/ball-20260929/lanes/mcp-bridge-r1.json:5). Minting two
new verbs to front the db rejected in R2 has no consumer on this machine; if
context lookup is ever needed it rides the existing corpus_search verb family.
Cost named: every new verb is a new gate/registry/test surface for zero reader.

### R4. Implicit retro-application of any scheme to existing files: REJECT

POINTER_INDEX_REPORT_20260911.md:31 already proved this estate's surfaces hold
multiple naming families that JOIN by derivation rule (94.4% hash-derived +
uuid-slice + semantic, all join-verified); the value is in the join rules, not
uniformity. Mass renames break path:line citations under the citation-lint
regime, force add+remove churn through the append-only INDEX event log, disturb
verkle path-keyed knots, and cut git blame. Zero benefit: FTS recall over
filenames already works (w4-multimodal.md:28).

## 4. Adoption plan (3 lines)

1. NOW: any seat pushing a bridge/handoff artifact names it
   SEAT_KIND_slug_datetime, hash8 appended when the artifact is a byte-frozen
   archive; make it law at the next AGENTS.md handoff-section or bridge-contract
   touch (one sentence, no new tooling).
2. NEXT ARRIVAL: the laptop seat re-pushes FILE_NAMING_AND_CONTEXT_LAW_20261002.md
   bytes with its bridge; this ruling's PROVISIONAL stamp lifts only after the
   full text is re-ruled against these same evidence tables (~30 min lane).
3. NEVER: no context_index.db, no new MCP context verbs, no retro-renames;
   context lookup rides corpus_search + the INDEX fold; any future naming-law
   enforcement follows the B2-389 shape (patrol falsifier, not a human checklist).

Filed 2026-10-02, lane D of the four. 112 lines (wc -l). Zero em-dash bytes.
