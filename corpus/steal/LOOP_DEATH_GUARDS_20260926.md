# LOOP DEATH GUARDS - steal receipt (gopher t6b, 2026-09-26)

Estate: local_sovereign_agent. Source lane: a14-ghost-guards (gala 20260925, wave 3).
Three uncovered laws, each verified live in the tree on 2026-09-26.

## LAW 1: A loop that dies must file WHY

CLAIM: A daemon wrapper that swallows its own death makes the subsystem silently
vanish, indistinguishable from never-started. The fix stays non-fatal for the daemon
but leaves a traced print naming the loop and the exception. Landed 2026-09-25 in the
cost enforcer wrapper (LOOP-DEATH GUARD); repeated for the bard wrapper at
mag/ghost.py:1585.

VERBATIM QUOTE (grep -F verified, count=1):
mag/ghost.py:1569: print(f"[ghost] COST-ENFORCER LOOP DEATH GUARD: cost_enforcer_loop exited: {_ce}", flush=True)

STEAL: Sweep every daemon entry wrapper in the estate for `except Exception: pass`
and convert each to a traced non-fatal print naming the loop and the exception.

FALSIFIER: Force cost_enforcer_loop to raise inside the wrapper in a test run and
observe no "[ghost] COST-ENFORCER LOOP DEATH GUARD" line on stdout; or find the
wrapper region reverted to a bare pass body.

## LAW 2: Re-fire is gated on the landing artifact

CLAIM: A recurring quest loop with no completion marker re-fires forever: one FKB
signature spawned 504 times (Aug 8 to Sep 22) because the trail never recorded that
the diagnosis landed. The fix appends the auto-fkb quest only when the diagnosis file
does not exist (mag/ghost.py:1417-1419), and the suppression is itself a trail fact
the next SENSE pass can see.

VERBATIM QUOTE (grep -F verified, count=1):
mag/ghost.py:1412: # sig spawned 504 times (Aug 8 -> Sep 22) because the trail

STEAL: For any recurring escalation or quest loop in the fleet, write a completion
marker at the landing site, gate the next fire on its absence, and keep a comment
naming the historical spawn count as the lesson.

FALSIFIER: Create memory/runs/ghost/autonomous_fixes/<sig>.md for a sig with count
>= 5, rerun the SENSE pass, and observe a new auto-fkb quest still appended for
that sig.

## LAW 3: Taxonomize before fixing

CLAIM: The wave2 except-pass fix read ghost.py's 70 except-pass sites first (4,244
lines, 140 except-Exception, zero bare excepts) and filed a 3-class taxonomy
(aggregator guards BY DESIGN, loop-death guards the black-hole species since FIXED,
daemon cycle guards stated-intent) before the first dent, so the fix spec preceded
the diff.

VERBATIM QUOTE (grep -F verified, count=1):
corpus/steal/ZCODE_RATCHET_WAVE2_20260925.md:100: Loop-death guards (the black-hole species)

STEAL: Before pruning the next except-pass chunk, read the target file and file its
own 3-class taxonomy (design silence vs death swallowing vs stated-intent cycle
guards) as the fix spec.

FALSIFIER: Read mag/ghost.py's remaining except-pass sites and find a swallowed
wrapper death the receipt claims is fixed, or find the taxonomy miscounts the site
total (70).

## BIBLIOGRAPHY (only sources actually read)

1. mag/ghost.py, lines 1395-1434 and 1550-1599, read 2026-09-26
2. corpus/steal/ZCODE_RATCHET_WAVE2_20260925.md, lines 88-112, read 2026-09-26
3. watch/inbox/gala_20260925/w3/lanes/a14-ghost-guards.json, whole file, read 2026-09-26

Evidence: watch/inbox/gala_20260925/afterparty/lanes/t6b.check.txt
