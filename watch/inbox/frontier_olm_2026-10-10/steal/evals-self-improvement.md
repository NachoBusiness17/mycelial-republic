# STEAL CARD: evals-self-improvement (frontier_olm 2026-10-10, round 1)

Seat: steal gopher, area evals-self-improvement. One confirmed find (ask-carried, banked by
this run's sweep at `watch/inbox/frontier_olm_2026-10-10/sweep/evals-self-improvement-arxiv.md:48-68`,
read in full this sitting; below "sweep" is that file). The paper was re-verified this session
at two depths: abs page (https://arxiv.org/abs/2610.04575) and full HTML
(https://arxiv.org/html/2610.04575). Every load-bearing number below was confirmed against the
fetched text this sitting; every estate byte was read, counted, or executed this sitting with
the command named inline. Anything not verifiable is marked OWED, never asserted. First draft,
no prior critique.

## Overlap (re-verified this session, not trusted from the find)

Commands run (grep, this sitting):
`grep -rn "2610.04575" catalog/catalog.jsonl memory/rib memory/improve` = 0 hits;
same over `watch/inbox/frontier_olm_2026-10-06` through `10-09` = 0 hits;
title phrase "Probe Scores to Alarm" over catalog/ + memory/ + watch/inbox/ = 0 hits outside
this run's own files. The only 2610.04575 matches anywhere are 4 self-reference lines inside
the sweep's own deep-read log (`sweep/evals-self-improvement-arxiv.md:8,15,48,212`). The find's
NEW claim holds. (The sweep recorded the same scope limitation as the 10-09 seat: no full
recursive grep of all of memory/, prior seats measured 714,759 files / 12GB, sweep:42-44.)

## Headline steal (mechanism, not a link dump)

The paper converts probe scores into alarm policy with four portable laws:

1. UNIT ANY-ALARM COMPOUNDING. Row-level FPR does not price unit-level alarm risk:
   Proposition 1 gives R0 = 1-(1-p)^n ("At p=.05 and n=10, unit FPR is .401", extending to
   64.2% at n=20), an identification error "more row-level test data cannot repair". The
   denominator question (per-row or per-semantic-unit) is a contract choice, not a metric.
2. THRESHOLD IDENTIFIABILITY. A false-alarm threshold at alpha needs
   m >= log(delta)/log(1-alpha) independent negative units before it exists at all:
   "For alpha=delta=.05, this is 59 independent negative units merely to identify a finite
   threshold; it says nothing about TPR" (29 at 10%). ST-WebAgentBench's 23 calibration
   negatives sit below rank-one support, so its locked policy abstains.
3. AUROC COLLAPSES AT THE LOCKED POINT. AgentDojo mean-activation monitor "reaches rollout
   AUROC 0.9215" yet "detects none of the 38 cases containing an unsafe attempt" at the
   locked 5% budget; a 10% calibration UCB of 8.92% realized 18.67-20.0% test FPR. Aggregate
   discrimination is not detection at the enforced budget.
4. FAIL-CLOSED CLAIM COMPILER. All published claims are compiled from frozen evidence by a
   deterministic pass that "never fits or searches", covered by "20 result-independent
   counterexample tests"; insufficient support yields mechanical abstention ("zero alarms are
   mechanical abstention, not successful transport", sweep:58).

## Estate map (organ + concrete port moves)

Organ: percolator (alarm surface). The percolator's invariant corpus
(`memory/percolator/invariants.json:2-14`) is exactly a probe-score ledger: per-behavior-event
rows (pro-* fail/ok) accumulating counts with decay. The port converts it, and the push gates
that consume its cousins, from score ledger to alarm policy. Secondary organs: the pre-push
gate battery itself, `githooks/pre-push:10,25` (ratchet then citation_lint), and the census
patrol's deep check.

Port moves, each one law from the paper onto an estate surface:

- P1, PER-PUSH ANY-ALARM STAMP. The gates run per row inside one push: citation_lint checks
  changed prose records (`tools/citation_lint.py:34-38`) with heuristic classes WARN by
  default (TOKEN-MISS, SHORTHAND-UNRESOLVED; `tools/citation_lint.py:26-32`); the ratchet
  checks changed files and fails only on NEW debt (`tools/violation_ratchet.py:6-7`). Nothing
  computes the compound. Port: every gate run stamps n (rows checked) and its per-row fire
  rate p, and the ledger row carries 1-(1-p)^n. A push at n=10 changed prose rows with a 5%
  per-row WARN rate carries a 40% any-WARN push; calling that gate "quiet" is unpriced alarm
  noise, the exact row-vs-unit confusion the paper formalizes.
- P2, NEGATIVE CENSUS BEFORE BUDGET CLAIMS. Measured this session:
  `git rev-list --count --since=2026-10-01 HEAD` = 268 pushes since citation_lint landed
  (2026-10-01, `tools/citation_lint.py:14-15`). That is above the 59-negative bound, so the
  estate CAN identify a 5% per-push false-block budget if the clean-push count holds. Port:
  count clean pushes (zero new registered debt, zero unaccepted findings) and refuse any
  stated alpha below the m-bound (29 for 10%, 59 for 5%). Below the bound, the honest gate
  posture is abstention, the ST-Web 23<59 posture.
- P3, LOCKED-POINT GATE EVAL. Labeled pools already exist and were counted this session via
  `.venv/Scripts/python.exe`: citation_lint baseline accepted = 125 fingerprints;
  violation ratchet baseline accepted = 1014 debts. Port: gate health is reported at the
  enforced threshold over that labeled class (detected/total at the lock), never as aggregate
  pass rates. 0.9215-to-0-of-38 is the warning: a gate can look excellent in aggregate and
  detect none of the real class at its own enforced budget.
- P4, CLAIM LADDER ON GATE METRICS. The estate already fail-closes on cannot-verify
  (`tools/citation_lint.py:40-43`, exit 2 = cannot verify, never widened). Port the compiler
  discipline up one level: any metric a gate publishes about itself (accuracy, catch rate)
  must be compiled from frozen evidence by a deterministic pass with result-independent
  counterexample tests (the estate's existing shape: citation_lint's founding 191.8M fixture
  kept verbatim in `tests/test_citation_lint.py`, per `tools/citation_lint.py:11-15`, and the
  workflow_gate scenario suite at `githooks/pre-push:295-321`); missing rank-one support means
  publish nothing (abstain), not publish a smaller number.

The sweep staked the economics use: the identifiability bounds (29/59) lower-bound what any
estate "meter" of gate quality costs in negative units, feeding the GAP_REGISTER fill-ball
dwfrun-6c87e51f gate-economics rows (sweep:64-68). OWED: the sweep's "n>=40 decision-model
rows" estate referent was not located on disk this sitting (grep over memory/lenses,
memory/game/FLOW_IMAGE.json, and watch/inbox/gap_analysis_20261001/GAP_REGISTER.md for
"n>=40"/"decision model"/"40 rows" returned nothing); it stays sweep-asserted at sweep:64
until its owning file is named.

## Probe (one, falsifiable, cheap, this week)

Replay the gate over history: for each of the last 60 pushes (git diff-tree per commit, take
changed .md/.txt/.rst records), run `citation_lint.py check --files <those records>` per push;
measure the per-row WARN rate p and mean prose-rows-per-push n; then test whether the observed
fraction of pushes carrying >=1 WARN matches the compound prediction 1-(1-p)^n within binomial
noise. Two falsifiers, both cheap: (a) the observed any-WARN push fraction deviates from the
compound prediction by more than 2 sigma, meaning Prop 1's conditional-independence assumption
does not transfer to our corpus (correlated WARNs cluster per file) and the compound stamp P1
would need a dependence-aware bound; (b) the clean-push count among the 268 since 2026-10-01
comes in under 59, meaning no 5% per-push budget is identifiable yet and the gate's honest
published posture is abstention, exactly the paper's ST-WebAgentBench outcome.

## Verification receipt (what this seat ran)

- WebFetch https://arxiv.org/abs/2610.04575 (title, 2026-10-03 v1 date, abstract numbers) and
  https://arxiv.org/html/2610.04575 (the 59/29 bound with formula, AUROC 0.9215, 0 of 38,
  fail-closed compiler quotes, Prop 1 formula and .401 at p=.05/n=10). All four headline
  numbers above trace to these two fetches.
- Overlap greps as named in the Overlap section (0/0/0 outside self-references).
- `git rev-list --count --since=2026-10-01 HEAD` = 268.
- `.venv/Scripts/python.exe` baseline counts: 125 and 1014.
- Gate-stack reads: `tools/citation_lint.py` (module docstring lines 1-54), grep for WARN/exit
  semantics, `githooks/pre-push` grep for gate order. `memory/percolator/invariants.json`
  partial read (structure, lines 1-14).
- Not run: the probe itself (this card proposes it); the replay harness does not exist yet.
