# ESTATE LAYOUT LAW - organization spec (Lane G, disk-audit wave 2026-10-09)

Spec only. Nothing moved, deleted, or created outside this file. Operator order:
"i think we can better organize our shit this is crazy", after the 30-burn
receipt-shape census and the c13997d8 founding incident (fleet-meta, 5.95 GiB
exhaust, no receipt dir - watch/inbox/disk_audit_20261009/internal/ATTRIBUTION.md).

## Current shape (census, 2026-10-09 reads)

- watch/inbox top level: 1654 entries = 140 dirs + 1515 files.
  - Machinery at top (stay put): INDEX.json, INDEX.md, index_events.jsonl,
    SHARED_SURFACE_CONTRACT.json. Loose work files: 1511.
  - Loose file classes: .md 1270, .json 112, .jsonl 29, .png 21, .py 18,
    .txt 14, .pdf 13, .jpg 9, .html 8, .log 3, .enc 2, .mp3 2.
  - Loose file dating: 1326 carry compact YYYYMMDD, 3 carry ISO dashes,
    186 undated. Two date grammars coexist plus a naked-slug tail.
  - Dirs: 57 dated (48 compact + 9 ISO) vs 83 undated themed.
- INDEX.json (fold catalog): schema shared_inbox.v1, DERIVED from the
  append-only event log index_events.jsonl (12614 events, derived_at
  2026-10-08T12:09Z) into 3638 active items (path/class/purpose/sha256);
  180 fold_warnings rows already police writer anomalies.
  - Registered names: 2359 compact-dated, 872 ISO-dashed, 407 undated.
  - Extensions: .md 2699, .py 389, .json 299, .jsonl 63.
- ractor_engine: 23 subdirs, all ISO grammar (2026-10-02-workflow-dogfood
  style) plus 1 default catch (ractor-topic). The estate's cleanest precedent.
- memory/ top level: 209 entries (mixed dirs, .md, .bak variants, stray
  working_*.py scripts). memory/rib/: 57 entries, 54 .md.
- Disk-audit facts this law answers (ATTRIBUTION.md): 30 burn identities,
  255.86 GiB mapped = 82.8 pct of the 309.12 GiB exec forest; one command
  class (unbounded stdout capture) explains 20.8 pct in 8 files; 1 of 30
  burns left exhaust with no receipt dir at all.

## The law: canonical layout

1. Every wave/burn lands in ONE dated workspace dir:
   `watch/inbox/<YYYY-MM-DD>-<slug>/` (new grammar, ISO dashes + prefix).
   Justification: all 23 ractor_engine subdirs and the 9 ISO inbox dirs
   (frontier_olm_2026-10-01..08) already follow it with zero exceptions;
   lexicographic sort = chronological; ATTRIBUTION's run-to-receipt matching
   already depends on it. Compact YYYYMMDD stays valid INSIDE file names
   (1326 of 1511 loose files carry it; the law does not force re-citing
   thousands of file:line refs) - only the DIR grammar unifies.
2. Mandatory per-burn receipt dir = the wave dir itself, minimum file set:
   RECEIPT.md (ractors: SYNTHESIS.md; mines: DIGEST.md) whose header carries
   run id (dwfrun-<id> or git sha), date window, purpose line, cost/GiB when
   a burn. Founding incident: c13997d8 - its conclusions rode sibling files,
   proving exhaust without a receipt dir is unverifiable spend.
3. Machinery files stay at top level; work product never lands loose at top
   level. New loose arrival = a bug in the writer, not a style choice.
4. Caches/exhaust live outside the durable root, by lifecycle class:
   - junk (unbounded dumps, full-disk walks, error loops): delete at wave
     close; keeper = the command line + a bounded head sample in the receipt.
   - re-derivable (indexes, compiled packs): TTL 30d or rebuild-on-change;
     keeper = the build script.
   - unique (receipts, syntheses, lens reports): no TTL; artifact is its
     own keeper. Keep the recipe, not the mass.

## Citation-safety protocol (index-first moves)

Precondition: INDEX.json is derived from the append-only event log, so
registration = an event append through the sanctioned writer, not a hand edit.

1. BEFORE moving: append a MOVE event to index_events.jsonl (old_path,
   new_path, sha256, actor, timestamp) via the shared-surface writer; regen
   INDEX (python -m mag.shared_surface validate green).
2. Execute: git mv (tracked) or plain move, then leave a redirect stub AT THE
   OLD PATH, exactly one line:
   `moved-to: watch/inbox/<new-path> (2026-10-09, lane-g)`
3. Post-move: validate again; run citation lint with explicit --files over
   prose known to cite the old path.
4. Mass moves forbidden while any audit/wave is live (this wave included).
5. citation_lint.py gains a MOVED-PATH class, exact shape: when a cited
   path is missing, read that path as text; if line 1 matches
   `^moved-to: (\S+)`, resolve the target, verify it exists and the cited
   line range is within its EOF; emit STUB-RESOLVED (pass) - range past EOF
   on the target downgrades to the existing blank/EOF defect. No stub, or
   dead stub target, keeps today's hard FAIL. Stubs are permanent until a
   citation-refresh wave retires them by count.

## Enforcement map (which gates grow a tooth)

- Workflow gate (tools/workflow_gate.py), new check RECEIPT_DIR: a run does
  not fold unless its deliverable sits in a dated wave dir holding
  RECEIPT.md/SYNTHESIS.md/DIGEST.md with the run id in the header; registry
  row gains the dir path.
- Drift patrol (tools/census_drift_patrol.py): orphan-receipt census row -
  wave dirs without a receipt file, and loose top-level files absent from
  INDEX; WARN-only at pre-push, flip-to-enforce is an operator call
  (mirrors B2-215 precedent).
- Shared-surface validate (mag.shared_surface): LOOSE-AT-TOP WARN for any
  non-machinery file at watch/inbox top level.
- Daily smith (MagImproveDaily 08:00): lifecycle-class rows - junk past
  TTL, re-derivable past TTL without a keeper script, unique-class count.

## Migration plan (incremental, law-gated)

- Ceiling: 1511 loose work files are candidates (ESTIMATE for full retrofit;
  per-file mapping to waves is required before any honest sub-count).
- Phase 0: enforce the law for ALL NEW work only (zero moves, immediate).
- Phase 1: the 186 undated loose files - date them from git log or INDEX
  purpose fields, move into their wave dir or a dated misc dir. Small,
  auditable, stubbed per protocol.
- Phase 2: dated loose files whose sibling wave dirs exist (burn_wave,
  gala, ractor_engine kin). Oldest-first; waves before loose files; one
  wave dir per commit.
- Never mid-audit: this disk-audit wave finishes and files its receipt
  before phase 1 starts.
- Two-registry warning (flash-zombie kin): a moved path lives in THREE
  places - the git tree, index_events.jsonl/INDEX.json, and citation prose
  (ribs, receipts, LINKS.jsonl, baselines). Update one and you breed ghosts:
  INDEX says new, git says old, lint reads a stub. All three change in ONE
  commit or the move does not happen.

## What NOT to reorganize

- memory/rib/ (57 entries): boot-mounted, rib_boot.json pins law-head
  digests; renames break the regen chain and AGENTS.md load-order citations.
- memory/zknot/ session files: tools/zknot.py reads them for the recap.
- Gate baselines (configs/violation_baseline.json,
  configs/citation_lint_baseline.json, configs/workflow_gate_scenarios):
  debt is accepted BY NAME/PATH; moving them orphans the acceptances.
- Top-level machinery (INDEX.json, INDEX.md, index_events.jsonl,
  SHARED_SURFACE_CONTRACT.json) - the contract names its home.
- state/*.md canon: newest-mtime crowns the boot order (row 0a); any touch
  is a crown event, not housekeeping.
- watch/inbox/inbound + outbound: standing queues named by the contract.
- The .zcode exec forest: outside the repo; handled by lifecycle TTL, not
  by reorganization.
