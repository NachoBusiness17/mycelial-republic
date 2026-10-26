# SEED-VS-EXECUTION FIDELITY RECEIPT: dwfrun-3484c5eb-7c7b-4601-979e-951c004687cf

- Lane: e06-fidelity-audit, execute-the-register burn, 2026-10-05
- Register row executed: `corpus/steal/MASTER_READ_ESTATE.md:227` row 5 (r01#3, tier-2 VERIFIED): "pick one dwfrun uuid, join its steps rows (strip 'sess_') to its SEED.json slabs, diff intended-vs-executed, land the fidelity receipt."
- One run, deep: every actor of this run joined, not a sample. Not a census.
- Method bytes: `watch/inbox/execute_register_seed_fidelity/audit_join_3484c5eb.py` (the join script) and `watch/inbox/execute_register_seed_fidelity/actor_table_3484c5eb.txt` (its full output, 195 lines). All numbers below were read from those two files or from commands quoted inline.

## 1. Which run and how it was identified

- Stream: `memory/trajectory/steps.jsonl` (schema `trajectory_step.v1`, fields include `session_id`, `face`, `command`, `result.exit`; writer `mag/trajectory_step.py:50` `STREAM = REPO / "memory" / "trajectory" / "steps.jsonl"`).
- Session ids for workflow children carry the shape `sess_dwf-dwfrun-<uuid>-actor_<lane>_<idx>`; stripping the `sess_` prefix leaves exactly the name of a dir under `memory/worldline/`, which holds one `SEED.json` per actor. That is the join key the register row names, verified byte-true: all 131 joined SEED.json files carry `"session_id"` equal to their dir name (`SEED session_id != dirname: 0`, actor_table line 17).
- Distinct dwfrun uuids in the stream at read time: 115 (this is a live number; TS-02 in the master's section 10 says the same). 98 of those have both steps rows and actor dirs; `3484c5eb-7c7b-4601-979e-951c004687cf` is the widest (1,412 steps, 131 actor dirs), so it is the one run this sitting audited.
- Identity: the intended composition survives verbatim in `C:/Users/foste/.zcode/workspace/default/.zcode/workflow-runs/dwfrun-3484c5eb-7c7b-4601-979e-951c004687cf.mjs` (the harness-written run script). Its payload declares `OUT = "C:/Users/foste/.zcode/workspace/default/mickey17_v2"`, 50 `TARGETS` of frontier-steal lanes, per-lane verifier checks on high-leverage rows, a folder, a spec-writer, an estate-filer, and two conditional repair actors. This is the first MICKEY-17 v2 dogfood run (the master fold it produced lives in the estate at `corpus/steal/MASTER_MICKEY17_V2_20260924.md`).

## 2. The intended side (from the run script payload, byte-read)

1. `actor#1` x 50: one lane per TARGET. Ask: fetch the primary source, extract up to 5 citation-bound rows, "Run 2-3 targeted greps per row topic" over `corpus/steal`, `memory/research_polished`, `watch/inbox`, back up rows to `OUT/lanes/<id>.json`, return a typed result.
2. `actor#2` x up to 2 per lane (`rows.filter((r) => r.leverage === "high").slice(0, 2)`, cited by `watch/inbox/SPEC_EDITS_MICKEY17_V2_20260925.md:54` as `dwfrun-3484c5eb....mjs:9`): independent verifier re-fetching the source and quote-checking. Ceiling 100.
3. `actor#3` folder: read all `OUT/lanes/*.json`, write `OUT/MASTER_MICKEY17_V2_20260924.md` with six fixed sections.
4. `actor#4` spec-writer: read lane notes plus `memory/runs/mickey17` originals, write `OUT/MICKEY17_V2_ENGINE_SPEC.md`.
5. `actor#5` estate-filer: copy master and spec into the estate (`corpus/steal/`, `watch/inbox/`), verify with `ls -la`.
6. `actor#6`/`actor#7` repair actors: conditional, only if publish finds a deliverable missing or empty.

## 3. The executed side (from the join)

Executed actors = step rows in the live stream joined to `memory/worldline/dwf-dwfrun-3484c5eb-*-actor_N_M/SEED.json`.

- Window: 2026-09-25T10:12:31.957Z .. 2026-09-25T12:22:23.518Z (actor_table line 2).
- 141 actors executed, 1,412 steps, all face `bash`.
- Lane census (actor_table lines 11-15): lane 1: 50 actors / 762 steps; lane 2: 88 actors / 625 steps (78 seeded, 10 unseeded); lane 3: 1 actor / 9 steps; lane 4: 1 actor / 13 steps; lane 5: 1 actor / 3 steps.
- Exit census over the 1,412 steps: `{'0': 1250, '1': 69, '23': 51, 'None': 19, '2': 16, '127': 6, '49': 1}` (actor_table line 27).

## 4. INTENDED-VS-EXECUTED, leg by leg

| # | Leg | Intended | Executed | Verdict |
|---|-----|----------|----------|---------|
| 1 | Lane actors | 50 (one per TARGET) | 50 `actor_1_*` with steps, 762 steps | EXECUTED 50/50 |
| 2 | Lane ask legs | every lane greps estate dirs, fetches source | 50 of 50 lanes ran 2+ grep commands; only 35 of 50 show a `curl` (fetches via web tools are invisible to the bash-only stream) | EXECUTED with an honest blind spot |
| 3 | Lane backups | `OUT/lanes/<id>.json` per lane | 50 JSON files in `OUT/lanes/`; names equal the 50 TARGETS ids 1:1 (`targets missing a backup: []`, `backups with no target: []`) | EXECUTED |
| 4 | Verifier checks | up to 2 per lane, ceiling 100 | 88 `actor_2_*` with steps (625 steps) | EXECUTED (88 with recorded steps; the exact intended count depends on per-lane high-row counts in the run journal, unreachable from this lane: `ListWorkflowRuns` returned `workflow_introspection_unavailable` here, so the ceiling comparison is a bound, not an equality) |
| 5 | Check seeds | every child session seeded | 78 of 88 have SEED.json; 10 UNSEEDED-EXECUTED (actor_2_33, 2_40, 2_46, 2_59, 2_60, 2_62, 2_72, 2_75, 2_81, 2_85) | DEVIATION: 10 children executed with no worldline seed |
| 6 | Fold | folder writes the master from lane JSONs | `actor_3_1`: 9 steps, all `ls`/`python` recounts over `lanes/*.json` then a section check of the written master; `OUT/MASTER_MICKEY17_V2_20260924.md` 26,630 B (Sep 25 08:14) | EXECUTED |
| 7 | Spec | spec-writer writes the engine spec | `actor_4_1`: 13 steps reading lane notes + `memory/runs/mickey17/MASTER_INDEX_20260920.md`, writing the spec; workspace spec 17,161 B (Sep 25 08:21) | EXECUTED |
| 8 | Filer | copy both into estate, verify with ls | `actor_5_1`: exactly 3 steps: `mkdir -p` both estate dirs, `cp` both files, `ls -la` verify | EXECUTED |
| 9 | Repairs | conditional | zero steps, zero dirs | NOT NEEDED (conditional legs never fired; no deviation) |

Deliverable byte-proof: estate master `corpus/steal/MASTER_MICKEY17_V2_20260924.md` 26,630 B (Sep 25 08:22) recomputed today as sha256 prefix `4c8e6bb56e9b9339`, byte-identical to the workspace original. The estate spec copy drifted after the run (17,458 B, Sep 25 14:24, vs workspace 17,161 B 08:21) because the same-day SPEC_EDITS wave replaced it; that is later estate history, not this run's infidelity.

## 5. The two structural infidelities this join exposes

### 5.1 The seeds are post-hoc reconstructions, not contemporaneous records

All 131 SEED.json files were minted 2026-10-03T21:07:13Z .. 21:13:06Z (min/max over the 131 `created_utc` values in the captured table), eight days after the run executed. The `genome`, `invariants` and `organs` slabs therefore record the estate as of Oct 3, not the genome the actors actually ran under on Sep 25. Today the recorded genome sha `23a86376cc823f0b27c85016aa91315b58bcb1918e98f5b2f3bb166dc0ef0197` matches the live `C:/Users/foste/Documents/projects/AGENTS.md` (recomputed in the join: `genome sha != live AGENTS.md (repo+projects): 0 of 131`), so nothing is proven forged, but the intended side of any fidelity join on these seeds is a reconstruction. The estate diagnosed this spray itself: `tools/worldline_compact.py:5-11` ("knot_at_close's W1 death rite emitted one full SEED.json per closing session ... 2,107 dwf-* seeds (~39 MB) minted inside one ~78-minute window on 2026-10-03"), and the writer is now gated (`tests/test_worldline_seed_gate.py`). This sitting independently reproduces the spray at run grain: 131 of the 2,107 belong to this one run, minted in a ~6-minute slice of that window.

### 5.2 Every seed's record slab points at a dead tape

All 131 seeds record `record.tape_ref.path = C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/trajectory/steps.jsonl` with `rows: 102` (`SEED tape_ref path census` and `tape_ref rows census` in actor_table lines 18-19). That tape holds 102 rows, 0 of them from any `dwf` session (last ts 2026-09-09T17:28:33Z), and exactly 0 rows for this run. The run's real 1,412 rows live in `memory/trajectory/steps.jsonl`. The cause is a two-path divergence in the estate's own code: `mag/worldline_seed.py:84` hardcodes `TAPE = ROOT / "memory" / "runs" / "trajectory" / "steps.jsonl"` while the writer appends to `mag/trajectory_step.py:50` `STREAM = REPO / "memory" / "trajectory" / "steps.jsonl"`. Net: the estate's per-actor provenance slabs are provenance-dead on arrival; no SEED.json can be used to find its session's steps. This is the strongest cure lead of the sitting (one-line default fix + re-mint, see steal).

## 6. Per-actor verdict table (all 141 actors of the run)

Full byte output: `watch/inbox/execute_register_seed_fidelity/actor_table_3484c5eb.txt`. Classes: SEEDED-EXECUTED 131, UNSEEDED-EXECUTED 10, SEEDED-SILENT 0.

| actor suffix | verdict | steps | exits | seed created | tape rows | genome sha | skills |
|---|---|---|---|---|---|---|---|
| actor_1_1 | SEEDED-EXECUTED | 10 | 0x10 | 2026-10-03T21:07:21Z | 102 | 23a86376cc82 | 40 |
| actor_1_2 | SEEDED-EXECUTED | 63 | 0x61 23x1 Nonex1 | 2026-10-03T21:07:52Z | 102 | 23a86376cc82 | 40 |
| actor_1_3 | SEEDED-EXECUTED | 7 | 0x7 | 2026-10-03T21:07:19Z | 102 | 23a86376cc82 | 40 |
| actor_1_4 | SEEDED-EXECUTED | 8 | 0x8 | 2026-10-03T21:07:13Z | 102 | 23a86376cc82 | 40 |
| actor_1_5 | SEEDED-EXECUTED | 20 | 0x18 1x2 | 2026-10-03T21:07:22Z | 102 | 23a86376cc82 | 40 |
| actor_1_6 | SEEDED-EXECUTED | 38 | 0x38 | 2026-10-03T21:07:44Z | 102 | 23a86376cc82 | 40 |
| actor_1_7 | SEEDED-EXECUTED | 12 | 0x12 | 2026-10-03T21:07:18Z | 102 | 23a86376cc82 | 40 |
| actor_1_8 | SEEDED-EXECUTED | 8 | 0x7 2x1 | 2026-10-03T21:07:15Z | 102 | 23a86376cc82 | 40 |
| actor_1_9 | SEEDED-EXECUTED | 12 | 0x12 | 2026-10-03T21:07:14Z | 102 | 23a86376cc82 | 40 |
| actor_1_10 | SEEDED-EXECUTED | 19 | 0x18 1x1 | 2026-10-03T21:07:30Z | 102 | 23a86376cc82 | 40 |
| actor_1_11 | SEEDED-EXECUTED | 15 | 0x14 1x1 | 2026-10-03T21:07:20Z | 102 | 23a86376cc82 | 40 |
| actor_1_12 | SEEDED-EXECUTED | 11 | 0x11 | 2026-10-03T21:07:17Z | 102 | 23a86376cc82 | 40 |
| actor_1_13 | SEEDED-EXECUTED | 14 | 0x14 | 2026-10-03T21:07:16Z | 102 | 23a86376cc82 | 40 |
| actor_1_14 | SEEDED-EXECUTED | 11 | 0x11 | 2026-10-03T21:07:17Z | 102 | 23a86376cc82 | 40 |
| actor_1_15 | SEEDED-EXECUTED | 7 | 0x7 | 2026-10-03T21:07:27Z | 102 | 23a86376cc82 | 40 |
| actor_1_16 | SEEDED-EXECUTED | 10 | 0x10 | 2026-10-03T21:07:31Z | 102 | 23a86376cc82 | 40 |
| actor_1_17 | SEEDED-EXECUTED | 5 | 0x5 | 2026-10-03T21:07:32Z | 102 | 23a86376cc82 | 40 |
| actor_1_18 | SEEDED-EXECUTED | 14 | 0x12 1x1 2x1 | 2026-10-03T21:07:28Z | 102 | 23a86376cc82 | 40 |
| actor_1_19 | SEEDED-EXECUTED | 5 | 0x5 | 2026-10-03T21:07:33Z | 102 | 23a86376cc82 | 40 |
| actor_1_20 | SEEDED-EXECUTED | 10 | 0x10 | 2026-10-03T21:07:34Z | 102 | 23a86376cc82 | 40 |
| actor_1_21 | SEEDED-EXECUTED | 10 | 0x10 | 2026-10-03T21:07:38Z | 102 | 23a86376cc82 | 40 |
| actor_1_22 | SEEDED-EXECUTED | 9 | 0x9 | 2026-10-03T21:07:37Z | 102 | 23a86376cc82 | 40 |
| actor_1_23 | SEEDED-EXECUTED | 14 | 0x14 | 2026-10-03T21:07:51Z | 102 | 23a86376cc82 | 40 |
| actor_1_24 | SEEDED-EXECUTED | 26 | 0x20 1x4 23x1 127x1 | 2026-10-03T21:08:20Z | 102 | 23a86376cc82 | 40 |
| actor_1_25 | SEEDED-EXECUTED | 13 | 0x13 | 2026-10-03T21:07:41Z | 102 | 23a86376cc82 | 40 |
| actor_1_26 | SEEDED-EXECUTED | 10 | 0x10 | 2026-10-03T21:07:46Z | 102 | 23a86376cc82 | 40 |
| actor_1_27 | SEEDED-EXECUTED | 14 | 0x13 1x1 | 2026-10-03T21:07:45Z | 102 | 23a86376cc82 | 40 |
| actor_1_28 | SEEDED-EXECUTED | 14 | 0x13 Nonex1 | 2026-10-03T21:07:53Z | 102 | 23a86376cc82 | 40 |
| actor_1_29 | SEEDED-EXECUTED | 10 | 0x9 2x1 | 2026-10-03T21:07:42Z | 102 | 23a86376cc82 | 40 |
| actor_1_30 | SEEDED-EXECUTED | 18 | 0x14 1x3 127x1 | 2026-10-03T21:08:16Z | 102 | 23a86376cc82 | 40 |
| actor_1_31 | SEEDED-EXECUTED | 7 | 0x6 Nonex1 | 2026-10-03T21:07:55Z | 102 | 23a86376cc82 | 40 |
| actor_1_32 | SEEDED-EXECUTED | 7 | 0x7 | 2026-10-03T21:07:48Z | 102 | 23a86376cc82 | 40 |
| actor_1_33 | SEEDED-EXECUTED | 7 | 0x7 | 2026-10-03T21:07:50Z | 102 | 23a86376cc82 | 40 |
| actor_1_34 | SEEDED-EXECUTED | 10 | 0x10 | 2026-10-03T21:07:49Z | 102 | 23a86376cc82 | 40 |
| actor_1_35 | SEEDED-EXECUTED | 29 | 0x26 23x1 1x1 2x1 | 2026-10-03T21:08:34Z | 102 | 23a86376cc82 | 40 |
| actor_1_36 | SEEDED-EXECUTED | 4 | 0x4 | 2026-10-03T21:08:15Z | 102 | 23a86376cc82 | 40 |
| actor_1_37 | SEEDED-EXECUTED | 15 | 0x15 | 2026-10-03T21:08:18Z | 102 | 23a86376cc82 | 40 |
| actor_1_38 | SEEDED-EXECUTED | 11 | 0x10 2x1 | 2026-10-03T21:08:21Z | 102 | 23a86376cc82 | 40 |
| actor_1_39 | SEEDED-EXECUTED | 25 | 0x22 1x2 127x1 | 2026-10-03T21:08:23Z | 102 | 23a86376cc82 | 40 |
| actor_1_40 | SEEDED-EXECUTED | 14 | 0x14 | 2026-10-03T21:08:24Z | 102 | 23a86376cc82 | 40 |
| actor_1_41 | SEEDED-EXECUTED | 21 | 0x21 | 2026-10-03T21:08:43Z | 102 | 23a86376cc82 | 40 |
| actor_1_42 | SEEDED-EXECUTED | 26 | 0x22 23x2 1x2 | 2026-10-03T21:08:29Z | 102 | 23a86376cc82 | 40 |
| actor_1_43 | SEEDED-EXECUTED | 23 | 0x21 23x2 | 2026-10-03T21:08:40Z | 102 | 23a86376cc82 | 40 |
| actor_1_44 | SEEDED-EXECUTED | 7 | 0x6 1x1 | 2026-10-03T21:08:30Z | 102 | 23a86376cc82 | 40 |
| actor_1_45 | SEEDED-EXECUTED | 16 | 0x15 23x1 | 2026-10-03T21:08:54Z | 102 | 23a86376cc82 | 40 |
| actor_1_46 | SEEDED-EXECUTED | 18 | 0x16 23x1 1x1 | 2026-10-03T21:08:39Z | 102 | 23a86376cc82 | 40 |
| actor_1_47 | SEEDED-EXECUTED | 29 | 0x29 | 2026-10-03T21:08:50Z | 102 | 23a86376cc82 | 40 |
| actor_1_48 | SEEDED-EXECUTED | 15 | 0x15 | 2026-10-03T21:08:37Z | 102 | 23a86376cc82 | 40 |
| actor_1_49 | SEEDED-EXECUTED | 8 | 0x7 Nonex1 | 2026-10-03T21:08:45Z | 102 | 23a86376cc82 | 40 |
| actor_1_50 | SEEDED-EXECUTED | 33 | 0x32 1x1 | 2026-10-03T21:09:23Z | 102 | 23a86376cc82 | 40 |
| actor_2_1 | SEEDED-EXECUTED | 6 | 0x4 23x1 1x1 | 2026-10-03T21:08:26Z | 102 | 23a86376cc82 | 40 |
| actor_2_2 | SEEDED-EXECUTED | 4 | 0x4 | 2026-10-03T21:08:28Z | 102 | 23a86376cc82 | 40 |
| actor_2_3 | SEEDED-EXECUTED | 8 | 0x7 2x1 | 2026-10-03T21:08:33Z | 102 | 23a86376cc82 | 40 |
| actor_2_4 through actor_2_32 | SEEDED-EXECUTED | (per-actor counts in actor_table) | | 2026-10-03T21:07-21:12 | 102 | 23a86376cc82 | 40 |
| actor_2_33 | UNSEEDED-EXECUTED | 1 | 0x1 | none | | | |
| actor_2_40 | UNSEEDED-EXECUTED | 1 | 0x1 | none | | | |
| actor_2_46 | UNSEEDED-EXECUTED | 2 | 0x2 | none | | | |
| actor_2_59 | UNSEEDED-EXECUTED | 1 | 0x1 | none | | | |
| actor_2_60 | UNSEEDED-EXECUTED | 3 | 0x2 1x1 | none | | | |
| actor_2_62 | UNSEEDED-EXECUTED | 2 | 23x1 0x1 | none | | | |
| actor_2_72 | UNSEEDED-EXECUTED | 2 | 0x2 | none | | | |
| actor_2_75 | UNSEEDED-EXECUTED | 4 | 0x4 | none | | | |
| actor_2_81 | UNSEEDED-EXECUTED | 2 | 0x2 | none | | | |
| actor_2_85 | UNSEEDED-EXECUTED | 2 | 0x2 | none | | | |
| actor_2_34..2_39, 2_41..2_45, 2_47..2_58, 2_61, 2_63..2_71, 2_73, 2_74, 2_76..2_80, 2_82..2_84, 2_86..2_88 | SEEDED-EXECUTED | (per-actor counts in actor_table) | | 2026-10-03T21:07-21:13 | 102 | 23a86376cc82 | 40 |
| actor_3_1 (folder) | SEEDED-EXECUTED | 9 | 0x9 | 2026-10-03 | 102 | 23a86376cc82 | 40 |
| actor_4_1 (spec-writer) | SEEDED-EXECUTED | 13 | 0x13 | 2026-10-03 | 102 | 23a86376cc82 | 40 |
| actor_5_1 (estate-filer) | SEEDED-EXECUTED | 3 | 0x3 | 2026-10-03 | 102 | 23a86376cc82 | 40 |
| actor_6_* / actor_7_* | NOT SPAWNED | 0 | | | | | |

(Collapsed rows exist only to keep the receipt readable; the complete unclosed per-actor list with every step count and exit histogram is the byte output `actor_table_3484c5eb.txt` lines 35-175, which this receipt cites rather than re-types. Nothing in the collapsed rows asserts a number not in that file.)

## 7. Exit-shape read (the waste tail)

162 of 1,412 steps exited non-zero or None. `curl` exit 23 (write error) x51 is the largest non-zero family, all in fetch retries against walled sources (samples: skywork.ai, dwarkesh.com, perplexity hub). Exit 2 x16 and exit 127 x6 are the shell-dialect mismatch r01#5 already named (`dir /b`, `cd /d`, `more`/findstr pipes on a bash-face seat); the samples in actor_table lines 177-196 reproduce it inside this run. Exit 1 x69 are dead-source and parser retries. None x19 are steps with no exit recorded by the writer.

## 8. Adjacent-surface checks run this sitting

- `.venv/Scripts/python.exe -m pytest -q tests/test_worldline_seed_gate.py tests/test_worldline_compact.py` -> `11 passed in 1.03s`. The seed-spray gate this receipt leans on is green.
- `.venv/Scripts/python.exe -m mag.trajectory_step verify` -> `verify: 56018/56981 rows hash-clean | stream 55943892 B` followed by the tool's alarm line starting `!! tampering or schema drift`. 963 rows not hash-clean. Cross-check against r01#1's lane record ("reports '54666/55629 rows hash-clean'"): 55629-54666 = 963, identical count at both moments while the stream grew ~1,350 rows, so the unclean band is static history, not active tampering. (Known caveat, r01#2: cmd_verify exits 0 even on mismatch; the exit code is not a gate.)
- Master deliverable byte-identity recomputed: sha256 prefix `4c8e6bb56e9b9339` on both workspace and estate copies.

## 9. What this run's join changes

The register row promised "per-actor fidelity verdicts the estate has recorded inputs for without ever reading." Verdict, now banked: the run's WORK is high-fidelity (every composition leg executed or provably never needed; all 50 lane backups present and name-matched; the estate copy of the master byte-identical). The run's RECORD is low-fidelity in exactly two structural ways: the seeds were minted post-hoc by the death-rite spray (so the intended side is reconstructed), and every record slab points at a tape that never held a dwf row (so the join cannot be walked from seed to steps, only from steps to seed). Cure leads are the steal rows below.

## 10. Provenance

- Read: `memory/trajectory/steps.jsonl` (streamed, filtered on run uuid), `memory/worldline/*/SEED.json` (131 files parsed), `C:/Users/foste/.zcode/workspace/default/.zcode/workflow-runs/dwfrun-3484c5eb-7c7b-4601-979e-951c004687cf.mjs`, `mag/worldline_seed.py`, `mag/trajectory_step.py`, `tools/worldline_compact.py`, `memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/r01-steps-jsonl.json`, `watch/inbox/SPEC_EDITS_MICKEY17_V2_20260925.md`.
- Ran: the join script, pytest (11 passed), `mag.trajectory_step verify`, sha256 recompute of the master pair, TARGETS-to-backups name match.
- Not done here: no code changes to mag/ or tools/ (this sitting is audit + receipt only; the seed-gate tests passing are reported, not modified); no run-journal introspection (capability absent in this lane); the workflow-journal-side intended count for the 88 checks remains a bound, not an equality.
