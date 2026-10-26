# THE FLEET INDEPENDENT-BUILDS DOCTRINE (operator order, 2026-10-10)

Operator words: "i want us to build all those things independantly" + "and run them on
the phone pc laptop docker. etc"

## The law

Every fleet-bound thing (the ones we have been building tonight and the queue behind
them) becomes an INDEPENDENT UNIT: one file or one small directory, stdlib-only (or
vendored deps), zero estate imports, config via env/args, receipts to local disk.
Independence is the portability test: if the unit needs the repo to run, it cannot run
on the phone, and it is not done. Build queue ordered by fleet value:

1. consensus_harness - INDEPENDENT as of tonight (fixture fallback landed: a bare box
   with no estate LINKS runs 8 built-in tasks, 8 distinct truths, all three shapes;
   9/9 tests green after the change).
2. pheromone bus - ALREADY independent (verified: pure stdlib, zero estate imports).
3. nightcrew + ds_workhorse pair - needs extraction (ds_workhorse imports
   tools.instance_guard) or vendoring into one dir.
4. budget smith (the projection organ over the burn ledger) - build independent from
   the start (projection() logic is already standalone in disk_smith).
5. seed_mcp cold boot - already a separate server; phone target = the join_protocol
   client only.
6. GWAP observer client - future unit, phone-first by design.

## The target matrix (run everywhere)

| surface | runtime | first units |
|---|---|---|
| PC (desktop) | repo venv, full stack | all |
| laptop (W10) | python 3.10+, single files | consensus_harness (dispatcher/judge), nightcrew |
| docker | python:slim, one unit per container | consensus_harness node, pheromone bus |
| phone (Android/Termux) | termux python, single files | consensus_harness vs LAN host, pheromone client, observer |

Phone note: the coldest vertex stays the law - if the phone cannot run the unit, the
unit is not independent. Termux python runs stdlib fine; no docker on phone; GPU never.

## Dogfood leg (the cron builds the fleet)

The decoupling map is a nightcrew job: DS extraction pass listing, per queued unit,
its estate imports and blockers - the build order for making each independent. Queue
row fires with the swarm self-steal batch tonight.

## Falsifier

An independent unit must PASS on a bare directory (no repo) before it carries the
"independent" label - the bare-phone simulation is the instrument (tonight's harness
check: 8 tasks, 8 truths, zero estate). A unit that only runs inside the repo is a
tool, not a fleet member.
