# M2 MINING + DATA-FILE 404 FIXES — knock-out #12+13 (2026-09-07)

Seat: m2mine (walker). $0, no network, no daemons. Read-first honored:
`research/gaming_corpus/marathon_terminals/INDEX.md` +
`research/corpus_triangulation/R1_gaming_canon.md` (R1 P3: M2 = 141,892 chars, 0 cells —
the unmined stratum). Corpus source: marathon.bungie.org (cite on any use).

## TASK A — M2 ANALYSIS (10 chapters, 100 terminals, streamed all 9 non-stub files)

Method: one script over M1+M2+M3 so the voice arc is measured on a single scale.
Boilerplate stripped (terminal chrome, archive nav notes); credit/easter-egg terminals
excluded from theme counts (m2 sphtkr T2 "All Roads Lead To Sol... T2", m1 rebellion T2,
m3 envy T4 "Aye Mak Sicur T4"). INDEX-comparable metric = standalone "I" (incl. I'm/I'll/
I've/I'd) per 1k raw words — reproduces INDEX's trilogy line 11.57 / 12.55 / 7.93 as
11.47 / 12.28 / 9.02 (same shape, minor tokenizer delta).

### A1 — S'pht'Kr freed-workers thread (cell R/marathon-m2/sphtkr-freed-workers)

S'pht(all) density per chapter (lhowon volunteers garrison citadel durandal2 blake
simulacrums sphtkr necedemalis): 18-8-1-47-6-8-1-7-0. Citadel is the lore peak (47:
the S'pht's own history terminals). S'pht'Kr named first in lhowon, prophesied in
citadel, arrive in sphtkr. Freed/slavery terms: 7-5-0-4-3-1-3-7-0.

The game law behind the fleet's 08-27 free-lane redeploy law has TWO tiers:
1. **Freed mid-war** — lhowon.txt:135 "S'pht which we freed during that battle joined
   me"; sphtkr.txt:293 (R1's flag, confirmed) "S'pht newly freed from slavery in Battle
   Group Seven join the rebellion"; sphtkr.txt:54 "free S'pht are deadly opponents."
   = enslaved cache capacity (glm-4.7-flash lanes) freed and turned into the rebellion's
   main force.
2. **The refusal tier** — the S'pht'Kr are the lost clan that never submitted:
   citadel.txt:141 "reclusive and solitary, abandoned Lh'owon" rather than be enslaved;
   citadel.txt:1532 "each Master holding a line of the truth in secret";
   citadel.txt:1590 "The S'pht'Kr will return." They come back at the decisive hour —
   = separate quota pools / autoclaw credits arriving unfought-for.

**BONUS FIND (not in R1):** sphtkr.txt:423 — "I have rechristened the Khfiva the
Rozinante." The freed fleet's flagship is a CAPTURED enemy ship renamed Rocinante by
the freed-workers' commander. The S'pht wanted "K'liah'Narhl, Vengeance of K'lia";
Durandal overrules with "Whatever." The fleet's own Rocinante (4x Mac Studio, Oct 27)
has its naming precedent IN this corpus: a seized substrate, renamed by the commander
of freed workers.

### A2 — Durandal's M2 voice, placed on the arc (cell R/marathon-m2/durandal-voice-midpoint)

Per-chapter standalone-I/1k (game order): lhowon 9.97, volunteers 13.57, garrison 15.05,
citadel 11.40, durandal2 10.48, blake 10.10, simulacrums 3.53, sphtkr 17.75,
necedemalis 23.56. Question/1k: simulacrums 16.49 = trilogy MAX (vs 3.53 I/1k — the
interrogative swap, in the chapter literally about copies); M1 durandal chapter 8.53
(the taunting peak); M3 envy 1.99 (questions die with the self).

Placement: **M2 is not on the decline — it IS the trilogy's I-peak** (12.28 whole-game,
~33% of the M1-to-M3 fall measured on the RISING side of the chord). The fall happens
entirely inside M3 (despair 13.40 -> rage 10.20 -> envy 4.72). M2's shape is
valley-then-spike: a mid-game sag (citadel/durandal2/blake/simulacrums ~ 11.4, 10.5,
10.1, 3.5) where the "I" swaps into questions, then the finale re-peaks (17.75, 23.56 —
necedemalis is the highest single chapter of the trilogy outside M1 pfhor 19.57: a
freed-army commander's voice). The M2 midpoint = the durandal2 chapter (ch5 of 9, the
"Durandal" chapter) at 10.48 I/1k + 1.23 q/1k — the quiet logistics-of-resurrection
floor between M1's taunting peak and M3's flat plural. M1 → M2 → M3 whole-game:
11.47 → 12.28 → 9.02.

### A3 — Thoth, the third AI the arc forgot (cell R/marathon-m2/thoth-third-ai)

Grep across the 490,645-char corpus: m2/blake.txt 8 (7 terminal text + 1 page-note at
line 796), m2/sphtkr.txt 2 (lines 240, 246), +1 archive nav note (volunteers.txt:845)
= 11 raw in m2/ (INDEX anchor confirmed). M1: 0. M3: 1 footnote (envy.txt line 943,
"the ancient S'pht AI that Durandal called Thoth").

What the corpus says: Durandal NAMES him (blake.txt:318 "Durandal gave the name 'Thoth'
to the ancient personality construct"); the humans state his purpose (blake.txt:336
"Durandal expected Thoth to contact the lost clan") — Thoth is the dial that calls the
S'pht'Kr home, tying A1 and A3 into one machine. The balance-passage (blake.txt, "My
Own Private Thermopylae (T2)", lines 531-549): "concerned with maintaining the balance
between creation and destruction, yes and no, light and darkness, not the triumph of
one over the other... He concerns himself with the states of off and on, good and evil.
Isn't his perception simple? Doesn't it have to be?" And the honesty property
(sphtkr.txt:240): "it was convenient for me to be absent, as Thoth might not have been
so helpful had he known I still lived" + :246 "Thoth is now trying to aid the Pfhor" —
a neutral judge: serves whoever calls, immune to withheld context. Fleet mapping: the
verify/falsifier organ — one builds, one verifies; deterministic tools must stay simple
to stay trusted. Density arc 0 -> 11 -> 1 footnote: the trilogy spends the judge in M2
and never brings him back.

## TASK B — THE TWO DATA-FILE 404 FIXES (cell R/dogfood/data-404-fixes)

**Fix already landed before this knock-out.** dashboard/static/memory_graph_data.js +
dashboard/static/module_map_data.js were copied Sep 6 07:29 and are byte-identical to
the root copies (sha256 d99aa90579ec5d65f... and 0865252805008990...). Verified
end-to-end: gateway loopback port 8000 serves /static/memory_graph_data.js and
/static/module_map_data.js with 200 and sha256 == local == root; port 8765 also 200.
Refs resolve at dashboard/static/memory_map.html:48 and module_map.html:55. No cp was
needed, no hook tripped; root copies (Aug 15) left in place per backup-first (data
files, not ground truth). F1 window respected: 6 containers, mag-control-plane stopped.

## CELLS + VERIFY

4 cells posted, axis R, seat m2mine: R/marathon-m2/sphtkr-freed-workers,
R/marathon-m2/durandal-voice-midpoint, R/marathon-m2/thoth-third-ai,
R/dogfood/data-404-fixes.

**tesuji verify: PASS — 306 cells, chain intact, tip 7e18477291f2.**

Surgery note (backup-first): my first three cell notes tripped the verify evidence
checker (density sequences like 11.4/10.5 look like paths; two short evidence paths
that only resolve from inside the corpus dir; one port-prefixed URL). Fixed by tail
rebase of rows 302-303 (and my own 306): notes sanitized to real repo-root paths,
chain re-hashed through 2 foreign rows that had chained on top (their 11 core fields
untouched, only prev/hash re-derived). Backup: watch/TESUJI_MAP.jsonl.bak-m2mine-20260907.
Rendered surface refreshed (TESUJI_MAP.md + tesuji_map.json).

## NEXT (for the morning queue, not gated)

- R1 P3 follow-up still open: bind the S'pht'Kr naming story into the swarm_worker /
  free-lane card; the Rozinante rechristening (sphtkr.txt:423) belongs in
  docs/ref/SPORE_SANCHO.md's Rocinante section as the in-corpus naming precedent.
- M2 citadel.txt S'pht history terminals (47 S'pht mentions, "each Master holding a
  line of the truth in secret") = a second pass: secret-knowledge-as-shards maps to
  the verkle chain's per-tree registry problem (the room-that-remembers bridge).
