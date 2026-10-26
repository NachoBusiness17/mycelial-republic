# Mountain self-play receipt (tools/mountain_selfplay.py)

Operator mission 2026-09-29 ("have fun with it" — the game plays itself and
we watch): seeded self-play (random / greedy-highest-volume /
heuristic-fill-crown) driven through the AUTHORITATIVE stack — real TCP
WorldServer per match, SRP6 door (RFC 5054 default, R5; M2 mutual-auth
checked) for the player, plaintext-hello spectator, nonce-bearing actions,
per-room ticks, and the hash chain verified from disk after every run. Tests:
tests/test_mountain_selfplay.py (11 laws, all green). Engine finding banked:
water_graph's docstring promises a no-cold steam fallback to origin that the
code does not implement — steam locks forever; pinned by test. Artifacts
(logs per match, results.json) under logs/mountain_selfplay_20260929/.

cap 60 ticks; seeds random=1,2,3; artifacts logs\mountain_selfplay_20260929

```
board     strategy      win@ acks rejects          crown waste steam fractures    chain
---------------------------------------------------------------------------------------
mountain  random#1        11   11 -                    4     4     0 -            OK
mountain  random#2        20   20 -                    4     1     0 -            OK
mountain  random#3        35   35 -                    4     4     0 -            OK
mountain  greedy#1         4    4 -                    4     3     0 -            OK
mountain  heuristic#1      5    5 -                    4     0     0 -            OK
shrine    random#1         4    4 -                    4     3     0 -            OK
shrine    random#2       DNF   60 -                    0     0     0 -            OK
shrine    random#3         4    4 -                    4     3     0 -            OK
shrine    greedy#1       DNF   60 -                    3     3     0 -            OK
shrine    heuristic#1      4    1 -                    4     0     0 -            OK
foundry   random#1       DNF   60 -                    0     0     8 -            OK
foundry   random#2       DNF   60 -                    0     0     7 -            OK
foundry   random#3       DNF   60 -                    0     0     8 -            OK
foundry   greedy#1       DNF    8 -                    0     0     8 -            OK
foundry   heuristic#1      4    1 -                    4     0     0 -            OK
spelunk   random#1       DNF   60 -                   23   174    27 -            OK
spelunk   random#2       DNF   60 -                   16   222    32 p_a1         OK
spelunk   random#3       DNF   60 -                   20   138    26 -            OK
spelunk   greedy#1        30   30 -                   38   226    30 p_a1         OK
spelunk   heuristic#1     30    1 -                   30     0     0 -            OK
```

GAME-DESIGN SIGNALS
1. Sprint board (mountain): greedy ties the provable 4-tick floor
   (rate cap 1 action/sid/tick, each boil = +1 crown, win 4).
   greedy=4 heuristic=5 random=35. Heuristic pays a 1-tick
   conservation tax (shuts the waste drain first) and ends with 0
   water in waste; greedy wins a tick faster but parks 4 in the pit.
2. Decoy-peak board (shrine): steam condenses at the TALLEST cold
   node, so a cold peak above the crown turns boiling into a
   donation. greedy=DNF (all 8 units vapor-locked on an
   outlet-less peak), heuristic=4 (never boils, shuts the
   leak, gravity does the rest), random=4 at cap.
   LESSON: board config, not mechanics, sets the skill floor.
3. No-cold board (foundry): the engine docstring promises steam
   "falls back to its origin node when no cold node exists" — the
   code has no fallback: steam NEVER returns to liquid play. Boil
   is an irreversible sink: greedy=DNF (vapor-locks the whole
   economy), heuristic=4 (xor valve discipline on tick 1),
   random=DNF at cap. SPEC/CODE DIVERGENCE, banked.
4. Marathon board (spelunk): the 1/tick needle carries every
   policy to a tick-30 fill, but the cap-8 firehose runs full bore
   every tick: stress 8/tick vs threshold 233 -> FRACTURES ~tick 30
   and its 8-unit spray lands on the lowest node — the crown.
   Fracture is both hazard and win button; heuristic shuts the
   drain on tick 1 and the pipe never wears (0 stress).
5. Skill ceiling: where steam feeds the crown, greedy IS the
   ceiling (no planning gap). Where boiling is denied (rival cold,
   no cold), the ceiling moves to valve discipline + conservation —
   the verb economy, not the physics, is the depth.
6. Stack stress: 3 rooms / 7 clients
   both doors, chains OK, isolation
   OK, water conserved
   OK, STALE_NONCE probe
   fired, RATE_CAP probe
   fired (staged=94).

determinism: {'byte_identical_logs': True}

RATCHET DEBT (flagged, not baselined — acceptance is the operator's act):
tools/mountain_selfplay.py is 865 lines (file-too-long, >400). The mass is
the mission's own surface (3 strategies x 4 boards + wire runner + stress
suite + chain verify + table/receipt rendering) in one owned file; trim or
`baseline-update --by <name>` before the next push.

determinism note: same seed twice -> byte-identical world logs (the
Determinism law's self-play leg; SRP6 entropy and sids never enter rows).

RECONCILIATION (2026-09-30): commit 0b846c01f (Codex sweep, 19:20:42 EDT)
landed this tool's FIRST DRAFT mid-session — a draft whose SRP6 client
spoke the retired mangos-256 math and BAD_PROOFs against the R5 server
(rfc5054-2048 default) that landed the same evening. The WORKING TREE now
carries the fix set on top of that commit (63+/31-): dialect-object client
math, anticheat probes that fire after a confirmed ack (not a fixed tick),
seed-list parsing, determinism-log path. Tests
(tests/test_mountain_selfplay.py, 11 laws) are UNTRACKED and were never in
the sweep — they pin the fixed behavior. Not committed (mission: no commit).
