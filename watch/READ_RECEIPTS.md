# READ RECEIPTS — the consumption meter (mag/read_receipts.py)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: the consumption meter catches cooked-but-never-read pages early (49k hits on / vs 4 zero-hit pages, 693 card back-refs measured) — SUPPORTED (measured hit table from the live dashboard log) · falsifier: hit counts fail to reproduce on re-scan, or a listed zero-hit page shows real traffic

Built 2026-09-06T22:13:22+00:00. Window: current dashboard log (no timestamps; restarts truncate). Question (operator 09-05): 'are they using them?' Verdict then: the machine eats what it just cooks, never goes back for leftovers. This page is how that gets caught early.

## Surfaces (hits, top 15 of 71 pages)

- 490905  /
-   687  /static/ractor.html
-    28  /static/room_lightmap.html
-    24  /static/intel.html
-    20  /static/agents.html
-    16  /static/decks.html
-    16  /static/daytool.html
-    15  /static/maze_arena.html
-    14  /static/salon_lightmap.html
-    13  /static/museum.html
-    12  /static/shadow_walk.html
-    12  /static/fable_room.html
-     9  /static/index.html
-     9  /static/fleet.html
-     9  /static/wave.html

## ZERO-hit pages (4)

- /static/bad_apple_field.html
- /static/chan.html
- /static/eraser_maze.html
- /static/live_feed.html

## Card back-refs (top 15 of 693)

-   70  STATUS
-   38  TOPIC_INDEX
-   36  SWARM_DOCTRINE_20260901
-   35  FLEET_STRUCTURE_20260901
-   34  LANE_SLOT_MAP_20260901
-   27  FLEET_AUDIT_20260901
-   26  DAY_WORK_DIGEST
-   26  INTAKE_BATCH_POPMATH_20260904b
-   25  TESUJI_MAP
-   23  AUDIT_B_ELDER_20260901
-   23  INTAKE_RUBRIC_20260903
-   23  INTAKE_XBATCH_20260905
-   23  STEERING_SYNTHESIS_20260901
-   23  ZAI_LITE_LAW
-   22  BATCH5_SALON_RECEIPT_20260906

## Cards with ZERO back-refs (1)

- TOPIC_INDEX_20260905

Zero back-refs is not shame — new cards start at zero. The signal is CARDS THAT STAY AT ZERO: written, never read, never disproven. Feed them to the topic index or disposition them.
