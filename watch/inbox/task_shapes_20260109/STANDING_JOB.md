# TASK-SHAPE CENSUS standing job - SPEC ONLY (2026-10-08, not registered)

This is the refresh spec the operator ordered ("make that a standing job").
Nothing is registered, no scheduled task created, no whitelist row added.
Registration is a post-review step (named at the bottom).

## Cadence (proposed)

Weekly, Sunday 09:00 local, same slot family as MagImproveDaily (08:00) and
MagCensusPatrolDaily (08:30) so the three never collide inside one hour.
Weekly, not daily: the sources move on human timescales (gallery stories,
showcase threads), and the zombie law below forces the run to prove fresh
work anyway.

## Source rotation (one source class per week, round-robin)

Week A - GALLERY DIFF: refetch
https://hermes-agent.nousresearch.com/docs/user-stories, diff story count
and named stories against the last fetch (store the fetch hash + count in
this directory's `fetch_log.jsonl`). New stories become candidate evidence
rows; a count drop is a finding, not an error.

Week B - SKILLS REPOS: refetch https://openclaw.ai/showcase and
https://github.com/hesamsheikh/awesome-openclaw-usecases (plus one rotating
awesome-list sibling, e.g. awesome-claude-skills class lists). Only
use-case-level tasks are harvestable; a skill with no user story is not a
shape.

Week C - OUR OWN QUEUE: mine `queue/results/` and the gps ledger for ask
shapes the estate actually served that no census row covers (today this
source yields internal machinery only; it starts contributing the day a
real user ask lands).

Every week regardless of rotation: re-run the dedupe (verb+object) over the
union of banked + new rows, and refresh the CENSUS.md counts.

## Zombie-law compliance block (every run, no exceptions)

1. DATED RECEIPT EVERY RUN: append a dated block to
   `watch/inbox/task_shapes_20260109/CENSUS.md` (or its successor directory
   named for the run month) with: run moment (UTC), sources fetched, rows
   added/merged, counts by cadence. A run with no receipt never happened.
2. DOES-REAL-WORK TEST: a run must land at least ONE of: a new evidence row
   on an existing shape, a new shape, a confirmed-dead source flagged with
   the HTTP status, or a correction to an existing row. A run that changes
   nothing in the database for three consecutive weeks is a zombie: the
   fourth such run must file an alert (next point) proposing cadence decay
   to biweekly, not silently continue.
3. ALERT-NOT-SILENT ON ZERO FINDINGS: zero new shapes in a run writes a
   dated line to `memory/attention.md` ("task-shape census: 0 new, sources
   X/Y/Z fetched at <moment>") so a dark or failing fetch is visible, never
   swallowed. A fetch that errors entirely (no sources reached) exits
   nonzero the way the census drift patrol does.

## The AUTO-WIRE (census row -> route table row)

The gate that already exists: `tools/gps_router_v0.py` trains on
`memory/corpus/ml/training/` (row contract ts / model_id / task_shape /
verdict, written by `tools/gps_mcp/ledger.py` into gps_ledger.db3 verdict_log)
and emits `ml3_route_table.json`; its evidence gate refuses to route any
shape whose best animal holds fewer than 5 training rows ("do not route"
fallback note in the existing table).

The wire, in order:

1. CENSUS SIDE: a shape with >= 3 distinct evidence rows in
   `task_shapes.jsonl` graduates from candidate to vocab: it takes a stable
   shape_id and is listed in CENSUS.md's vocab section.
2. LEDGER SIDE: the estate dogfoods the shape: dispatches executed under
   that task_shape name log verdicts through `tools/gps_mcp/ledger.py`
   (verdict_log rows keyed model_id x task_shape x evidence_hash, the
   UNIQUE dedupe already in the schema).
3. ROUTER SIDE: once a shape holds >= 5 verdict rows in the refreshed
   corpus, a rerun of `tools/gps_router_v0.py` emits a gated
   best_animal for it in the route table. Below 5 rows it stays
   unpickable - the census never bypasses the evidence gate, it only feeds
   it named shapes to measure.
4. NEW-class rows (audio/video-in, media generation, voice-out) do NOT
   wire to animals; they accumulate evidence until an operator decision
   adds an animal class. The census's job for them is the evidence count,
   visible in CENSUS.md.

Wire law: the census proposes shape names and evidence; only verdict rows
measured in the gps ledger make a route. No row is ever hand-assigned a
best_animal.

## Registration (POST-REVIEW, not done this pass)

When the operator approves: follow the established pattern -
`scripts/register_<name>_task.ps1` (sibling:
`scripts/register_census_patrol_task.ps1`) creating a MagTaskShapeCensus
weekly task, log under `logs/`, and add the task name to
`configs/sanctioned_scheduled_tasks.yaml` (the whitelist the gap map
measured at 13 rows). The runner itself would be a small
`tools/task_shape_census.py` wrapping the fetch + dedupe + receipt steps
above, reusing `_build_task_shapes.py` as the row validator. Until then
the census is refreshed by hand, by any seat, using the three steps in
this spec.
