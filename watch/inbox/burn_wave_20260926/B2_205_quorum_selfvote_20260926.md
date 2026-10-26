# B2-205 quorum p4 self-vote exclusion (2026-09-26)

## Verdict

LANDED. An addition's author chair now ABSTAINs on its own addition in the p4
quorum tally: excluded from its addition's YES/NO tally AND from its
denominator (eligible set = P1 returners minus the author; need recomputed
per addition as ceil(2 x eligible / 3)). The pre-registered falsifier recount
ran over the fleet's quorum runs: 1 run qualified (memory/runs/salons/
quorum_20260907), 10 additions recounted, 4 pivotal self-votes witnessed
(authors voting YES on their own additions), ZERO outcome flips (closest
call: A2 PASSED 8/10 need 7 stays PASSED at 7/9 need 6; A1's author YES did
not save it under either rule). Past verdicts stand; the exclusion is
prospective.

## Evidence file:line quotes

- The disease, mag/quorum_window.py (pre-edit): "for chair in p1s:" reads
  every returner's ballot (the author among them), then "denom = len(p1s) /
  need = math.ceil(2 * denom / 3)" and "yes = [c for c, v in votes.items()
  if v.get(aid) == 'YES']" counts the author's vote toward its own addition.
- The author is parseable from the fold the brief pointed at:
  memory/runs/salons/quorum_20260907/FOLD.md:8 "- **A1** [NOTE]
  (BAUDRILLARD): ...", and every addition header carries its author.
- Post-edit mag/quorum_window.py: author map built from the fold headers;
  tally loop uses eligible = [c for c in p1s if c != author], per-addition
  denominator/need, records "author_abstain" in the result row, and the
  verdict line names the rule ("B2-205 rule: an addition's author chair
  ABSTAINs on it"); module docstring rulings list carries the spec line.
- Pre-registered recount (watch/inbox/burn_wave_20260926/
  B2_205_quorum_recount.py, results in B2_205_recount_results.json):
  "runs_recounted: 1, additions_recounted: 10, pivotal_self_votes_found: 4,
  outcome_flips: 0"; quorum_20260907 A2: old 8/10 need 7 PASSED, new 7/9
  need 6 PASSED; A1: old 6/10 need 7 NOT PASSED, new 5/9 need 6 NOT PASSED.
- Pin tests tests/test_quorum_p4_selfvote.py: 2 passed. The pivotal fixture:
  A1 (author CHAIR_A) raw 2/3 would PASS the old rule, excluded tally 1/2
  need 2 FAILS; A2 (3/3 raw, 2/2 eligible) still PASSES, pinning that the
  exclusion never sinks a genuinely popular addition.

## Work done

1. Read the p4 tally bytes and the quorum_20260907 fold/VERDICT; confirmed
   the author header is machine-parseable and the self-vote was live.
2. Edited mag/quorum_window.py: author map, per-addition eligible set, ABSTAIN
   bookkeeping, verdict rule lines, docstring spec line (spec before behavior
   change).
3. Wrote and ran the pre-registered recount over memory/runs/salons/quorum_*
   (read-only), archived results JSON beside the receipt.
4. Wrote fixture-first pin tests (2, green); scratch-ran the tally against a
   staged run to debug test arithmetic (two mid-lane corrections, both named:
   the fold grammar needs A\\d+ ids, and the first fixture's votes were not
   pivotal); ratchet check --changed: NEW=0.
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This landing is inverted if any of the following holds: (a) a future p4 run
records a vote from a chair equal to the addition's author in its yes/no
lists (the exclusion regressed; the pin tests catch the shape);
(b) the recount script, rerun after new quorum runs land, reports outcome
flips that no receipt adjudicates (a past verdict's margin rested on
self-votes; the B2-60 D1 lens demands those verdicts be re-graded, not left
standing silently);
(c) an addition whose author header is missing from a future fold (author
map empty) silently tallies under the old rule; the result row's
author_abstain field is the witness: absent for every row means the header
format drifted.

## Bibliography closed

mag/quorum_window.py (read: docstring, p4 body, _parse_p1/_P1_SEC, _dir);
memory/runs/salons/quorum_20260907/ FOLD.md + VERDICT.md + p4/*.md (read;
the recount's byte source); watch/inbox/burn_wave_20260926/B2_60_judge_independence_20260926.md
D1 lens (accepted from the brief as the ruling context). No network calls;
no model calls (all fixtures file-backed).
