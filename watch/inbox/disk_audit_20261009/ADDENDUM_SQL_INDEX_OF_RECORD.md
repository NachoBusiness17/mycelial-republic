# ADDENDUM - SQL INDEX OF RECORD + SCHEMA-BEARING FILENAMES - 2026-10-09

Operator order (this window): "optimize too. didn't we have the idea of having
a solid filestructure that had the actuals schema embedded in the file names
for fast crawling so the contents would relate to a sql database we run"

## The remembered idea is real and landed in PIECES - the unification is owed

What exists today, all verified this window:
- watch/inbox/INDEX.json - the fold catalog: 3,638 items derived from a
  12,614-event append-only log (Lane G census). JSON, not SQL; the sole
  sanctioned writer is the fold host (index_fold_host.mjs mints seq/ts/sha256/
  nonce per row).
- catalog/catalog.jsonl + catalog/catalog_fts.sqlite - the corpus FTS5 SQL
  database, rebuilt daily 09:00 (MagFtsIndexDaily), sha256 deep-verified -
  PROOF the sqlite-over-catalog shape already runs in production here.
- Knot filenames already embed schema: 2026-10-08_1111_autonomous-janitor_
  autonomo_t9337189.knot.json = date_time_author_type_hashfragment. The
  grammar exists; it just never generalized past the chain.
- ReFold sha-addressed stubs + mesh_delta sha256 snapshots - content-addressing
  already proved estate-side.

## The unification (the optimize addendum to ORGANIZATION_SPEC.md)

1. FILENAME GRAMMAR becomes law for new work product:
   <YYYY-MM-DD>_<kind>_<slug>_<8-char-digest>.<ext> - the name alone tells the
   crawler kind, date, and content identity without opening the file; the
   crawl is metadata-only (the harvester pattern, never a content walk).
2. INDEX OF RECORD GOES SQLITE: the fold gains a sqlite sink beside INDEX.json
   (schema: seq, ts, sha256, path, kind, wave, lifecycle_class) - INDEX.json
   stays as the derived view for tools that read JSON; sqlite becomes the
   queryable database the operator remembered. One writer (the fold) still;
   the FTS5 organ is the precedent, not a second writer.
3. FAST CRAWL LAW: any crawler over the estate reads the sqlite/INDEX first,
   walks only what it must (one process, metadata-only) - the find-dump
   disease (64GiB of accidental C:\ root walks) is the founding incident
   making this a gate, not advice.

Priority: AFTER cleanup + retention land (the standing-wave budget first);
this addendum is banked so the Lane D law pack carries it forward whole.
