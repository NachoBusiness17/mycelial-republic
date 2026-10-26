# B2-184 receipt: fix the corpus search/get path seam (2026-09-26, lane SW-03)

## Verdict

LANDED. The seam is fixed in _confine (tools/corpus.py): a leading "local_sovereign_agent/" prefix (the scanner's projects-dir-relative form, mag/catalog_scan.py:83) is stripped before resolve, so corpus_get and corpus_tail accept both search-hit paths and repo-relative paths. The brief's falsifier now holds live: corpus_get(corpus_search hit path) returns ok:true (verified live on local_sovereign_agent/mag/catalog_scan.py, served path mag/catalog_scan.py, bytes served). 4/4 new regression tests pass; neighboring corpus suites (fts, agent, seat) 20 passed. Search output and catalog ids are untouched (the id law derives from stored paths; normalizing search output would have broken re-verification).

## Evidence file:line quotes

- mag/catalog_scan.py:83-84: "ROOT = r\"C:\\Users\\foste\\Documents\\projects\"" / "LSA = os.path.join(ROOT, \"local_sovereign_agent\")" (the scanner walks the projects dir; its stored paths start with local_sovereign_agent/).
- tools/corpus.py:80-87 (pre-fix _confine): "if not rel or os.path.isabs(rel): return None; real = os.path.realpath(str(REPO / rel)) ..." (REPO = repo root; an LSA-prefixed hit resolved to the nonexistent REPO/local_sovereign_agent/... nested path and corpus_get refused it, reproduced live before the fix).
- tools/corpus.py docstring (the id law that chose the fix side): "echoes the sha256 of exactly the bytes served, plus the catalog id derived the same way the scanner derives it (sha256 of the relative path, first 12 hex), so any seat can re-verify the map against the disk."
- tools/corpus.py _zone_of (the seam's existing acknowledgment): "if p.startswith(\"local_sovereign_agent/\"): return \"lsa\"".
- QUEUE.md B2-184 row: "falsifier = corpus_get(corpus_search hit path) returns ok:true".

## Work done

- tools/corpus.py _confine: literal prefix strip of "local_sovereign_agent/" before resolve; refuses bare prefix and trailing-slash forms; confinement unchanged (absolute paths refused, realpath must stay under REPO, parent traversals after the strip still refused).
- tests/test_corpus_path_seam.py (new, 4 tests): both forms resolve to the same file; escape/absolute/bare-prefix refusals intact; corpus_get of a real search-hit-shaped path returns ok:true with the stripped served path; end-to-end corpus_search -> corpus_get roundtrip over a live hit.
- Live falsifier run: corpus_get('local_sovereign_agent/mag/catalog_scan.py') -> ok:true, path mag/catalog_scan.py.
- Observed, NOT fixed (outside this seam, disclosed): corpus_get's catalog_id derives from the served repo-relative path while scanner ids derive from the stored projects-relative path, so the two id spaces differ for the same file (pre-existing convention gap; pinning it here so the divergence is named, never silently inherited).

## Falsifier

The brief's falsifier, closed: corpus_get(corpus_search hit path) returns ok:true (test_corpus_get_of_search_hit_path_returns_ok_true + live run). Regression guards: any reintroduction of the refusal (prefix strip removed) or a confinement weakening (escape test red) fails the suite. The disclosed id-space divergence is falsified-open: if scanner ids and corpus_get ids are ever unified, this receipt's disclosure line must be retired by the lane that does it.

## Bibliography closed

- mag/catalog_scan.py (ROOT/LSA lines 83-84, walk surface)
- tools/corpus.py (module docstring, _confine, _catalog_id, _zone_of, corpus_get, corpus_search)
- tests/test_corpus_path_seam.py (new), tests/test_corpus_fts.py, tests/test_agent_corpus.py, tests/test_seat_corpus.py (regression runs)
- QUEUE.md B2-184 row (brief and falsifier)
