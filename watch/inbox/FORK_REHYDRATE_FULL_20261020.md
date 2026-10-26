# FORK_REHYDRATE_FULL_20261020

Run 2026-10-20 16:37-16:45 ET (America/New_York). No commit, no push, no daemon, no schedule.
Live chain read-only. Nothing woven into the live chain. Tool unmodified.

## Task 1: full fork rehydrate

Command: .venv\Scripts\python.exe tools/chain_fork_rehydrate.py --out %TEMP%\magfork20261020 (no --limit = all rows)
Wall time: 21.3 s. Tool exit 0, no fix needed at full scale.

| Metric | Value |
|---|---|
| Live rows compared | 13138 |
| leaf_ok (live leaf == knot leaf, recipe 'session' recompute matched) | 13128 |
| Dangling (no knot in knots/, knots_attic/, diary_nodes/) | 10 |
| Leaf divergences | 0 |
| First divergence index | none |
| Fork merkle roots == live verkle_root, per row | 13138/13138 (first mismatch: none) |
| parent_verkle_root breaks on live | 0 |
| fork_root vs live tip root | a7a9b441120942ac == a7a9b441120942ac |

### Divergence classes

| Class | Count | New/Known | Notes |
|---|---|---|---|
| Leaf mismatch | 0 | n/a | none |
| v1 in-place amends dated 2026-10-17 (amended=true, ts 2026-10-17) | 25 rows | KNOWN (sealed history, 10/17 '24 rewrites') | Count reads 25, not 24: row 12132 (2026-10-17_1206_mag_01a149c1_37e6100a) is a same-day 10/17 knot, likely its own amend rather than one of the 24 back-dated rewrites. Rows: 7,9,10,13,14,15,17,18,20,21,22,23,24,718,972,4934,4951,4958,4961,4965,5234,6826,7264,7907,12132. Leaves agree with knots because knot and row were amended together, so the fork tool cannot see them as divergence. |
| Other amended=true rows (2026-08-11..2026-10-10, mostly 10/01-10/03 and 09/26-09/27 waves) | 2935 | KNOWN class (v1 amend path, pre-gate) | Total amended=true is 2960. Not re-audited here. |
| Dangling, no source session/knot file | 10 | KNOWN-ish (pre-10/15 lost window era); first time listed by this tool at full scale | 2513 (2026-08-11 mem-invariant-map, filename contains a serialized dict "{'ok': F" = malformed filename), 5547 (ts 09-11, knot named 08-15), 7371, 7372, 7373, 7374, 7376 (09-06 23:00-23:08 burst), 7424 (09-10), 7479 (09-10), 7587 (09-11). Live leaf kept, not invented. |

Writer/source attribution: live rows carry NO source / seat / writer field (keys: amended, chain_mode, dominant_theme, dossier_commit, end_minute, filename, index, leaf_hash, n_leaves, parent_verkle_root, session_id, session_seq, start_minute, tension_index, theme_vector_normalized, ts, verkle_root). The only writer hint is the filename kind (session, mag, biography, constitution, mirror, harness, rib-doctrine, dashboard). Seat attribution per row is therefore NOT possible from chain bytes; it is a gap, not a finding.

Tool limit (hostile): divergence = live leaf vs knot-stored leaf_hash; an amend that rewrote knot and row together is invisible. divergence_sample caps at 50 rows (unused today, 0 divergences).

Artifacts: %TEMP%\magfork20261020\verkle_chain.fork.jsonl, verkle_tip.fork.json, divergence.json, analyze.py (read-only analysis).

### Before/after live chain proof

| Moment (ET) | Rows | sha256 |
|---|---|---|
| Before 16:37:55 | 13138 | 33311208952768dab48d2ff3cea397e02b3494cf17c741915b0d296de2b74d92 |
| After run | 13138 | 33311208952768dab48d2ff3cea397e02b3494cf17c741915b0d296de2b74d92 |
| Matches CHAIN_HARDEN_ITER2 baseline | yes | same n and sha |

## Task 2: commit-lane claim

commit-lane status: claimed/design

Appended ONE line to watch/claims.jsonl (schema mag_claims.v1, matching the 5 existing rows' keys):

```
{"schema":"mag_claims.v1","id":"claim-commit-lane-single-001","claim_text":"A single seat-independent commit lane (a cron-style committer that commits files independently of whichever seat wrote them) is CLAIMED so the other seats do not each build their own. Status: claimed/design, NOT built. Codex is the de facto single committer today (author and committer of all of the last 25 commits at 2026-10-20 16:40 ET).","carrier_path":"watch/inbox/FORK_REHYDRATE_FULL_20261020.md","pins":[{"pin_id":"commit_lane_status","claim_regex":"^commit-lane status: (claimed/design)$","flags":"MULTILINE","capture_fields":["status"],"expected":{"status":"claimed/design"}}],"moment":"2026-10-20T20:40:00Z","owner":"operator (Nacho), pending a choice of builder","verifier":{"type":"design_requirements","args":{"requirements":["path allowlist: only allowlisted paths are ever staged","secret scan before each commit; any hit aborts that commit","skip files modified in the last ~2 minutes (in-flight writes)","never --no-verify, never force (no force push, no amend of pushed commits)"],"de_facto_committer":"Codex (git log -25: 25/25 author+committer Codex)"},"bar":{"built_without_requirements":"CONTRADICTED: a lane that lacks any requirement is not this claim","second_lane_built":"CONTRADICTED: another seat built a parallel committer"}},"consumer":"every seat about to build its own committer: read this claim and defer to the operator's builder choice","on_fail":"WARN","registration_verdict":"CLAIMED-DESIGN","evidence":{"date_et":"2026-10-20","git_log_last25":"25 Codex|Codex"},"receipt":"watch/inbox/FORK_REHYDRATE_FULL_20261020.md","anchor":null}
```

## Reuse / staleness

| Item | Source date | Verified at HEAD | Outcome |
|---|---|---|---|
| tools/chain_fork_rehydrate.py | 2026-10-20 | yes, ran unmodified | full run 13138 rows, 0 div, 10 dangling |
| 50-row smoke (ITER2) | 2026-10-20 | superseded | full run agrees (rows 0-49 ok) |
| mag.verkle_knot _leaf_hash/_merkle_prefix_roots | 2026-10-19 gate edits | yes (imported) | roots reproduce live tip |
| 10/15 restore pattern (TEMP-only candidate) | 2026-10-15 | pattern reused | output in TEMP only |
| 24 v1 amends 10/17 | 2026-10-17/19 | yes | 25 amended rows dated 10/17 (see note) |
| ITER2 baseline n=13138 sha 33311208... | 2026-10-20 | yes | unchanged |
| watch/claims.jsonl mag_claims.v1 | 2026-10-18 | yes, 5 rows | 6th row appended |
| git log -25 committer | 2026-10-20 | yes | 25/25 Codex |

## Rollback

- Task 1: nothing to roll back on live; delete %TEMP%\magfork20261020 if wanted.
- Task 2: remove the last line of watch/claims.jsonl (id claim-commit-lane-single-001).
- This receipt: delete the file.