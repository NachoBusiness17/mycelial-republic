# killed/ - eigenmap-one's preserved bytes (card eigenmap, panel 2026-09-26)

The judge's revision ruling (2026-09-27): eigenmap-two survives (every prong
of the position/distance/bearing check passes on its shipped bytes; worst
render-vs-bearing deviation 0.0 deg) and eigenmap-one dies on the mirrored
minimap: its own bearing law defines north as eigen -y (its README bullet
said "north = eigen -y = world -Z") while its minimap renders max +ey at the
TOP (EigenMapHud.client.luau:110, `(py1 - ey) / (py1 - py0)`), so its drawn
map is 180-deg rotated against its own bearing readouts.

The revise-eigenmap pass pruned the killed build from the repo tree so the
estate carries exactly one cathedral map, and moved its bytes HERE instead of
deleting them (annotate, never delete: a killed candidate's rows are records
too). Original tree paths, for the record:

| file in this dir | original tree path |
|---|---|
| EigenMap.luau | roblox/src/shared/EigenMap.luau |
| EigenMapZone.luau | roblox/src/server/EigenMapZone.luau |
| EigenMapHud.client.luau | roblox/src/client/EigenMapHud.client.luau |
| eigenmap_overlay_check.py | tools/eigenmap_overlay_check.py |
| gen_eigenmap_luau.py | tools/gen_eigenmap_luau.py |

The three .luau files moved byte-identical (mv). The two .py tools carry all
their original code bytes plus a dated [RECORD COPY] annotation at the top of
the docstring (code body verified line-identical below the annotation before
the originals were removed). Nothing in this folder is maintained: the check
and generator still reference their old ROOT and the pruned tree paths, so
running them as-is will not resolve. The surviving build's falsifiers live in
tools/eigenmap_two_check.py and tools/eigenmap_two_smoke.py.

Kill evidence and the killed build's own account: ../eigenmap-one.md,
../eigenmap-one.overlay_check.txt, ../eigenmap-one.mountain_check.txt. The
fold decision and its receipts: ../../eigenmap.final.md.
