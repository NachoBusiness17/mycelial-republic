# B2-169 research.py event-row pointers (SW-07, 2026-09-26)

## Verdict

LANDED. tools/research.py links search now skips LINKS rows with an empty canonical (the 54 event-derived rows of 338) and watch/inbox/EVENTS.jsonl is searchable as its own source (source=events, and inside source=all), emitting pointers of the form watch/inbox/EVENTS.jsonl#<id>. No search surface emits an empty pointer anymore.

## Evidence file:line quotes

- QUEUE.md row: "tools/research.py:48-62 matches event rows via title and emits an empty pointer (empty canonical) now that the 51 events are split out"
- Pre-fix disease reproduced on current bytes (old match logic): `PRE-FIX HIT pointer='' title=LANE-BREAKING: NVIDIA build API purged 82 models (yi-large,` -- the LINKS row matched via title and the emitted pointer was the empty string.
- Census on current bytes: LINKS.jsonl 338 rows, 54 with empty canonical; EVENTS.jsonl 51 rows, all event.v1 (ts, writer, id, kind, title, detail, schema).
- watch/inbox/EVENTS.jsonl:1 `{"ts": "2026-09-20T13:10:00Z", "writer": "free-resource-scout", "id": "ALERT-NVIDIA-PURGE", "kind": "ALERT", ... "schema": "event.v1", ...}`

## Work done

- tools/research.py: links branch now guards `if not canonical.strip(): continue` before matching, so event-derived rows cannot emit empty pointers.
- tools/research.py: new EVENTS constant (watch/inbox/EVENTS.jsonl) and an events branch: source in (all, events) matches title + detail + id and emits pointer `watch/inbox/EVENTS.jsonl#<id>` with a detail snippet and ts.
- Module docstring sources list names both the exclusion and the new events source.
- Post-fix probe: query "NVIDIA build API purged" over source=all returns 0 empty-pointer links hits and 1 events hit (`watch/inbox/EVENTS.jsonl#ALERT-NVIDIA-PURGE`); a links-only sweep of 100 hits shows every pointer non-empty.

## Falsifier

Stated in the brief as the failure mode: a match that emits an empty pointer. Falsified by the probes above (0 empty-pointer hits post-fix, events hit reachable). Residual falsifier for the next reader: any query over source=links or source=all returning a hit with pointer == "" reopens this brief; run tools/research.py research_search and check the pointer field.

## Bibliography closed

Read: tools/research.py (full, pre-edit), watch/inbox/EVENTS.jsonl (head + count), watch/inbox/LINKS.jsonl (census scan), QUEUE.md B2-169 row. No external sources needed; the brief pointed only at repo files.
