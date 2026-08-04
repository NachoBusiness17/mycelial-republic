# Sprint board

- **knot:** Stand up agent scrum so work is planned not improvised
- **goal:** SCRUM process runnable; W0.0 still PO critical path
- **end:** 2026-07-27
- **updated:** 2026-08-04T00:25:47.452581+00:00
- **data/raw empty:** True

See `docs/SCRUM.md`. Evidence → `docs/MILESTONES.md` on major Done.

## BACKLOG

- **W0.1** [P0] `AGT_DATA` — Prep posts.jsonl from archive (dep: W0.0; assignee: —)
- **W0.2** [P0] `PO` — Annotate train set (dep: W0.1; assignee: —)
- **W0.6** [P0] `AGT_TRAIN` — First train adapter (operator data only) (dep: W0.3; assignee: —)
- **W0.7** [P0] `AGT_TRAIN` — Local inference path (dep: W0.6; assignee: —)
- **W0.8** [P0] `KERNEL` — Post-train chord + live selftest (dep: W0.7; assignee: —)
- **R1.W1.1** [P2] `AGT_DOCS` — Spore package script (dep: W0.8; assignee: —)

## READY

_none_

## DOING

_none_

## REVIEW

_none_

## DONE

- **SCRUM-001** [P1] `KERNEL` — Scrum process + CLI for agents (dep: —; assignee: KERNEL) · evidence: `docs/SCRUM.md;src/mycelial_republic/scrum/;scrum/`
- **W0.0b** [P1] `PO` — Boot soil from exports (annotate without full zip) (dep: —; assignee: MAG) · evidence: `data/annotated/mirror_train.jsonl 115 rows; validate PASS at --min 100; annotate drift-check NONE 2026-08-02; density 22 high/93 med`
- **W0.4** [P1] `AGT_INST` — CONSTITUTION.md v0 (dep: —; assignee: —)
- **W0.5** [P1] `AGT_TEST` — Live selftest baseline (prompt-only) (dep: —; assignee: —) · evidence: `logs/selftest/latest.json 12/12 overall≈0.694; docs/MILESTONES.md`
- **INST-001** [P2] `AGT_DOCS` — Instrument bridge note (dashboard vs republic) (dep: —; assignee: —) · evidence: `docs/INST_001_MAG_BRIDGE.md`
- **SCRUM-002** [P2] `MAG` — Wire Mag optional [scrum] status chore (dep: SCRUM-001; assignee: MAG) · evidence: `chore exercised 2026-08-02: scrum status via republic CLI from queue/todo.md [x]`

## BLOCKED

- **W0.0** [P0] `PO` — Operator archive in data/raw (dep: —; assignee: —) · **blocked:** data/raw empty; needs operator archive zip drop (PO)
- **W0.3** [P0] `AGT_DATA` — validate --min 800 (dep: W0.2; assignee: —) · **blocked:** dep W0.0 archive; current 115 < 800 weight gate

## WIP check

_no doing tickets_ (limit 2/role)
