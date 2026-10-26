# Y5 — server/ published to the-mountain (2026-09-29)

**Lane:** batch 2, lane 5/12 · **Target:** `C:\Users\foste\Documents\projects\the-mountain` (separate repo; committed, NEVER pushed)

## What landed

- `the-mountain/server/` — the estate's `server/` package copied verbatim:
  `__init__.py auth.py protocol.py protocol_table.py room.py server.py
  verdict_feed.py world.py ws_door.py README.md` (source:
  `local_sovereign_agent/server/`, tree state 2026-09-29 23:20).
- `the-mountain/server/_vendor/water_graph.py` — byte-verbatim copy of
  `mag/water_graph.py` (pure stdlib, no transitive mag deps — verified by
  read: dataclasses + typing only). `server/_vendor/__init__.py` carries the
  provenance note.

## The one rewrite (documented judgment)

`world.py` line 44: `from mag.water_graph import WaterGraph` →
`from server._vendor.water_graph import WaterGraph`, with a fix-comment
naming the estate original. Judgment: vendored the whole file rather than
inlining classes — WaterGraph + Node + Pipe ARE the physics engine (~275
self-contained lines); inlining would be a re-copy with worse provenance.
`server/README.md` header documents this plus two estate-only caveats:
the pytest line refers to the estate suite, and `verdict_feed.py` (gwap →
gps return-leg) imports estate modules not vendored — carried for
reference, importable nowhere in the-mountain, and nothing in the package
imports it (verified by grep: `__init__.py` imports only world + protocol).

## Quickstart

`docs/ADAM_QUICKSTART.md` §3 rewritten: the "server half is NOT here"
promise is now real — run instructions for
`python -m server.server --demo` (works standalone, pure stdlib, Py 3.9+),
the `--tick-ms 80` fast variant, and serve mode (`server.auth` add user →
`server.server` on 127.0.0.1:8800). Example WIN line corrected to the
measured output after the test run (receipts, not vibes).

## Test (the proof)

```
cd the-mountain && <estate>\.venv\Scripts\python.exe -m server.server --demo
```

Exit 0, 30 ticks, stats `{'clients': 2, 'ticks': 30, 'actions_staged': 34}`,
closing line:

```
THE CROWN FILLS. WIN at tick 4; boiler boiled 4, tagger tagged 30.
```

(the-mountain has no venv; the estate's interpreter ran it with the-mountain
as cwd — the `python -m` cwd path + server.py's own ROOT sys.path insert
resolve the package from the-mountain, zero estate imports on the demo path).

## Commit

`bac2b89` on `main` — "land the estate's world server as server/ with
vendored physics (Y5)" (13 files, +2801/−8). Not pushed.
