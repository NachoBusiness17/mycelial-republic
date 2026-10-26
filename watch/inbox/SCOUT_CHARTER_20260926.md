# Free-resource scout charter v0 (2026-09-26, burn brief B2-123)

The free-resource scout is a LEAD watcher (DIRECTIVE_WATCHERS_20260926.md:14, 8 runs
logged, 09:00 cadence) that has been audited only by observed work (B2-27 evidence
section). This charter is the spec the next patrol audits against. One page, three laws.

## 1. Writers

- **Link rows** (schema `link.v1`, `watch/inbox/LINKS.jsonl`): written ONLY by
  writer id `free-resource-scout` through the `mag.link_library` module door. No
  other writer id may file scout links; no scout link is ever hand-appended to
  LINKS.jsonl by a script, editor, or session (append-only law, mag/link_library.py:21).
- **Event rows** (schema `event.v1`, `watch/inbox/EVENTS.jsonl`): findings that are
  NOT a URL library entry (provider policy changes, quota deaths, rate-limit
  sightings) are event rows per the B2-28 schema split, each self-describing with
  `"schema": "event.v1"` and an `"origin"` block naming file+line (mag/link_library.py:22-24,
  167-183). Kinds follow the existing ledger vocabulary (`finding`, `ALERT`, `verdict`).

## 2. Filing doors

- **Links:** `python -m mag.link_library add <url> [--note ...] --writer free-resource-scout`
  is the ONLY sanctioned door (B2_27_scout_checkgate_20260926.md: "add is the only
  sanctioned filing door, check the read-only pre-flight"). The door runs
  `check_url()` first and stamps `duplicate_of` at submission; `add_urls` is the
  programmatic form of the same door.
- **Findings:** append an `event.v1` row to `watch/inbox/EVENTS.jsonl` (never to
  LINKS.jsonl; the two ledgers are separate since B2-28). A finding that also
  yields a library URL uses BOTH doors: the link for the URL, the event for the
  observation, with the event `detail` naming the link row.
- **Real denominators only:** a scout filing cites what it measured (model id,
  limit header, docs URL). No stale numbers re-filed from memory (B2-03 law).

## 3. Dedupe law

Before any link filing the scout MUST pass `python -m mag.link_library check <url>`;
a known canonical answer (`known: true`) means the scout does not file a new row
unless the page content changed materially, and then files with `duplicate_of`
set to the canonical's identity, never `""` (the B2-06 disease: arxiv 2609.19107
re-filed with empty duplicate_of beside its own canonical). Re-confirmations of a
known URL are event rows, not new link rows. Falsifier (inherited from B2-27):
the next scout fire re-files a known canonical with empty `duplicate_of`, or any
scout link row appears in LINKS.jsonl that did not pass through `add`.

Audit basis on file: DIRECTIVE_WATCHERS_20260926.md:14 (8 runs, by observed work),
watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md (evidence section,
door + gate landing), watch/inbox/burn_wave_20260926/B2_28_schema_split_20260926.md
(event ledger split), B2_06_link_dupes_20260926.md (dupe triage precedent).

## 4. No-erase backfill amendment (2026-09-29, wave5 events-door)

A schema-less row in EVENTS.jsonl is never edited or erased (no-erase law). Its
owning lane repairs the door by appending a corrected carrier row in the
section-1 shape: schema event.v1, origin block, charter kind (finding, ALERT,
verdict), writer attribution, id = original id + "-BACKFILL". The carrier's
origin block names the row it supersedes: origin.file = watch/inbox/EVENTS.jsonl,
origin.line = its 1-based line number, origin.replaces = its original id, plus
the superseded row's own ts and line sha256 for provenance. load_events() does a
two-pass parse: it json-parses every line, collects the ids named by
origin.replaces on conforming rows, enforces the strict schema contract on every
row EXCEPT those named ids (accepted debt by name, ratchet pattern), and serves
only charter rows; any schema-less row NOT named by a carrier still fails
closed. Every carrier append re-registers per EVENTS_DRIFT_LAW_20260926 rule 2:
one op register row, class DATA, purpose naming the append and the new row
count. First use: 5 schema-less rows at lines 54-58 (f-05 census 2026-09-28),
carriers at lines 59-63, receipt watch/inbox/wave5_repair/events-door.md.
