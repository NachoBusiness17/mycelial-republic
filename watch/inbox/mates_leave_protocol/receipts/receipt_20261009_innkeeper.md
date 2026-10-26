# Receipt: innkeeper mate, 20261009, cycle 1 (OPEN)

Mission: logs\mates\missions\mission_20261009_04_innkeeper.md (claimed via .claim sidecar per pack header).
Status: IN ROAD. Cold walk begun. This is the opening receipt filed before speech, per pack law. A closing receipt will replace this file when the walk stops.

## FINDINGS (so far)

1. The pack's own seed hash does not resolve: `git show 035a5e3` in this repo fails ("unknown revision"). The hash exists only as text inside commit 1aad038d7's message: "the-mountain clone-proofed (035a5e3)". Day-one Adam cannot check out the commit his mission names.
2. `memory/continuity/seat_memory_20260927/the-mountain-roblox-20260925.md` is 0 lines / empty. The estate's own memory about the-mountain has nothing in it.
3. Root README.md (218 lines) never mentions the-mountain, the roblox/ dir, or any game surface. A stranger cannot find the mountain from the front door.

## JOURNEY (threads followed in order, dead ends named, why each turn)

1. Read the mission pack (the one thing a fresh seat must do first). Learned persona, hunting ground, seed thread.
2. Tried `git show 035a5e3`. DEAD END (unknown revision). Why: the pack names it as the day-one starting commit; it does not exist here.
3. Globbed for mountain surfaces. FOUND roblox/the_mountain.rbxlx, roblox/README.md, tools/mountain_*.py, tests/test_mountain_*.py. Why: locate the actual cold-entry surfaces.
4. Read root README.md. Confirmed no mention of the mountain. Why: README is the first door a stranger opens.
5. Read the-mountain-roblox-20260925.md continuity page. DEAD END (empty file). Why: it looked like the fastest briefing on what the-mountain even is.
6. Grepped all-branches log for 035a5e3: only hits are the literal string inside 1aad038d7's message. Next turn: check whether roblox/ is its own git repo that holds 035a5e3.

## COUNTS (real)

- git show attempts that failed: 1
- README.md lines read: 218
- README lines mentioning the-mountain or roblox: 0
- empty continuity files found: 1

Resume-not-respawn: this seat may stop mid-road; resume by id (innkeeper, pack mission_20261009_04_innkeeper).
