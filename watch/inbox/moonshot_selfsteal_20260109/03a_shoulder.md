# 03a - THE SHOULDER L, MEASURED (first reading) - 2026-10-09 night

Probe 4 of the moonshot build order: measure the recovery shoulder L after
a heavy wave; hosts-for-24/7 = ceil(24/(5-L)); kill test at L > 1h.

## The measurement

- The wave: the night's width-8..11 mixed program (analytics + builds +
  compost + revivals + basecamp wave 1), staggered over hours. Last heavy
  lane (revivals retry, ~5.9M tokens) drained at T0.
- Ping 1 at ~T0+1min: CLEAN, 11.8s, 1 tool call, honest answer.
- Ping 2 at T0+11min (10-min hold interval): CLEAN, 13.5s, 1 tool call,
  honest answer.
- Two consecutive cleans: L = approx 0-2 minutes (effectively no shoulder).

## The arithmetic

hosts-for-24/7 = ceil(24/(5-L)) = ceil(24/4.97) = 5 hosts. Kill test L<1h:
PASS by two orders of magnitude. The 6-host composite design not only
survives - 5 hosts suffice at this L.

## Honest caveats (named, not buried)

- This wave was STAGGERED (hours of mixed lanes), not a dedicated
  width-10 instantaneous burst; a staggered drain recovers differently
  than a saturation burst. The canonical probe (dedicated width-10 wave,
  then pings) still stands for the definitive L.
- Pings rode the Task-agent retry path (maxAttempts 11) per the fan-out
  law - a clean completion means clean at THIS retry shape.
- Single night, single account state. The rolling-throughput law says the
  limit is the window, not the width; L should be re-measured after the
  next true saturation burst.

## Standing conclusion (provisional)

At measured L, the composite window across the 3 real devices + 2 more
covers 24/7 with margin. The mesh staggering math (moonshot 03 card)
holds: phase publication on the chan + a scheduler at each host's offset.
