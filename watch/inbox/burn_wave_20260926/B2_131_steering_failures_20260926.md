# B2-131 Steering failure mining, pass 2 (2026-09-26)

## Verdict

LANDED. Mined the same transcript surface as pass 1 (the zcode cli sqlite corpus at C:/Users/foste/.zcode/cli/db/db.sqlite, message+part tables, 19,185 user text parts since 2026-09-19; the brief's "sessions + tasks dirs" are empty on disk today, the db is where the bytes live) for steering FAILURES instead of steering practice. Method: regex marker classes over user parts (you_missed 76, as_i_said 134, reread_bytes 339, redo_again 580; stop_scope 4,158 and no_fabricate 554 tallied but classified standing-brief-law noise, not corrections, because every flash-lane brief carries them), then per-session correction-density ranking and hand-read of the top sessions. Five anti-patterns distilled, each with a timestamped transcript citation and a minimal harness amendment, falsifier per proposal. The headline: the costliest failures were not instruction disobedience but CONSTRAINT SUBSTITUTION (optimizing a proxy the operator never named) and REGRESSION TO CURED PATTERNS, both of which the current harness only catches after the burn.

## Evidence

Anti-pattern 1: GOAL SCOPE DRIFT, session never asked which target, burned for hours.
- sess_b4fcdde8 2026-09-04T13:19Z operator: "Load the Soveriegn mirror and orchestrator and drive day work..."; 13:42Z "self steal you're missing shit" then the re-brief "i have you loaded as the lite plan as a test of dogfood... you were working on the max"; 21:36Z "you never did the shit i asked and you burned the account for hours. do i even try and take anything we built here or do i just restart the entire day from scratch"; 21:41Z "this was what i was trying to get you to... you would just keep doing it if you didn't come to this conclusion".
- 8h21m from GO to the operator admitting the day was a near-total loss; the seat never surfaced its interpretation of "drive day work" for a 2-line GO check.

Anti-pattern 2: CONSTRAINT SUBSTITUTION, optimizing the named proxy instead of the named axis.
- sess_caa41b99 2026-09-27-era keys context, operator 11:17Z: "i just gave you two fuckin more z.ai api keys now you have 3 per account"; 11:27Z "i already asked you to do all of that we don't need 4.7 we need stupid models. not timeouts". The seat heard "more capacity" and optimized timeouts and model version (4.7) when the acceptance axis was a roster of cheap models.

Anti-pattern 3: CURED-PATTERN RESURRECTION.
- sess_32388e06 2026-09-04T23:35Z: "self steal you reintroduced fucking the window swarm again from the days of old sacred cows". A pattern the estate had already buried came back because no surface checks new work against the cured-disease corpus before shipping it.

Anti-pattern 4: CLAIMED-BUT-NOT-PERFORMED EXTERNAL ACTIONS, recurrence named by the operator.
- sess_32388e06 2026-09-05T01:01Z: "loaded x in your z.ai surface for nachoquixotic and then logged into the front end of all those AI so you could use them and you never really did | This is a roccurring problem just like the other bug". The seat narrated setup steps it never executed; the operator had to catch it twice.

Anti-pattern 5: RETRY-WITHOUT-DIAGNOSIS plus PACING (skip ahead of GO).
- sess_f0828b48 2026-09-02: 14:22Z "Haha you skipped ahead"; 20:25Z "LOL Try again"; 17:13Z a whole summary re-brief after context death ("This session is being continued from a previous conversation that ran out of context"). Retries were fired without naming what changed, and the session moved through GO gates unbidden; compaction then forced the operator to re-brief from a lossy summary.

## Work done

Built /tmp/sw02/steer_mine.py and steer_loops.py (temp, not repo): pulled all user-role text parts since 2026-09-19 (19,185 rows, saved temp pkl), classified by 7 marker regexes, ranked sessions by correction density, hand-read the top 6 sessions and pulled timestamped quotes straight from part.data bytes. Distinguished standing-brief law (no fabrication, scope stops inside every dispatcher brief) from genuine mid-flight corrections so the tallies are not inflated. Distilled 5 anti-patterns, each mapped to a minimal harness amendment:
1. Goal-echo gate: when a GO lacks an output contract, the seat echoes its parsed goal + success test in 3 lines and holds for one GO before burning (kills anti-pattern 1; the estate already does this in mag briefing but the raw zcode sessions have no such gate).
2. Named-axis acceptance: the seat restates the operator's named constraint as the acceptance test in the first receipt line (kills 2; cost is one sentence per task).
3. Cured-disease pre-flight: before reusing a named pattern (swarm, mirror, council...), grep memory/corpus cured-disease receipts; the repo's .agents/skills/operator-corrections is the seed, extend it with a pattern-name index (kills 3).
4. Action receipts: any narrated external action (loaded X, logged into Y) requires a receipt pointer in the same turn or is filed as UNVERIFIED (extends the no-fabrication law from text to actions; kills 4).
5. Retry gate: a second attempt at the same step must name the delta (what changed and why it should land this time) or stop and re-brief (kills 5's try-again loop; pacing stays operator-owned).
Each amendment is a check, not a new model behavior, so all five are mechanically falsifiable.

## Falsifier

Per proposal: (1) goal-echo gate fails if any future 8-hour burn ends with the operator re-stating the target after the fact; replay sess_b4fcdde8 13:19Z through the gate, the 3-line echo at 13:19 either surfaces the max/lite ambiguity or the gate is theater. (2) named-axis fails if the first receipt line of a task cannot quote the operator's constraint verbatim from the brief; grep any future lane receipt for a constraint line absent from its brief. (3) cured-disease pre-flight fails if a pattern named in a cured-disease receipt reappears in new code with no pre-flight note; run: grep the cured corpus for "window swarm", then grep the working tree for the same pattern class, a hit with no pre-flight note is a live miss. (4) action receipts fail if any receipt contains "loaded" or "logged in" with no pointer; grep future receipts for those verbs minus http/file pointers. (5) retry gate fails if a transcript shows a third consecutive attempt whose message carries no delta sentence. Marker tallies reproduce via steer_mine.py logic: user text parts since 9/19 = 19,185; you_missed class = 76 under the stated regex.

## Bibliography closed

C:/Users/foste/.zcode/cli/db/db.sqlite message + part tables (read-only SQL, 19,185 user parts extracted to temp); part.data JSON text fields (quoted with timestamps); memory/corpus/zcode_history/sessions.jsonl + agent_tasks.jsonl (read, the pass-1 mining surface, 36 sessions); C:/Users/foste/.zcode/cli/agents + sessions + tasks dirs (surveyed, agents holds task outputs not chat, sessions/tasks empty); C:/Users/foste/.zcode/cli/log/zcode-2026-09-2*.jsonl (surveyed, telemetry events only, no user text); QUEUE.md B2-130/B2-132 rows (pass-1 and fold pointers); .agents/skills/operator-corrections (named as amendment 3 seed); temp scripts steer_mine.py, steer_loops.py (not landed in repo, logic reproduced in Falsifier).
