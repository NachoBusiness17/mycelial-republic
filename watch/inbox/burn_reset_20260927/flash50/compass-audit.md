# COMPASS AUDIT - v1-v10 arc vs what actually shipped (f-27)

Item: f-27, census gopher fire-f-27, 2026-09-28. Compass read in full: `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md` (258 lines, 13,132 bytes, `wc -l -c`). Machine truth read in full: `configs/version_roadmap.yaml` (313 lines), `configs/releases.yaml` (174 lines), `docs/ref/releases/VERSION_REGISTRY.md` (127 lines), `docs/ref/releases/RELEASE_NOTES_v3.md` (91 lines), `docs/ref/releases/RELEASE_NOTES_v4.md` (34 lines), head of `RELEASE_NOTES_v1.md` and `state/CURRENT.md`. Every number below comes from a command run this session (commands quoted inline).

## Verdict table

| ID | Compass says (line) | Machine truth says | What the disk shows | Verdict |
|----|--------------------|--------------------|---------------------|---------|
| v1 | shipped (L124) | shipped | RELEASE_NOTES_v1.md (3,411B) + 3 X witness posts in releases.yaml L29-38 + WITNESS_SPINE.md + docs/ref/strike_origin.md exist. External Grok/X origin era; not code-verifiable by design | LANDED (origin artifact) |
| v2 | shipped, hardening on branches (L125) | shipped | gates.jsonl: run_a red 08-05T23:40Z ("awaiting PR merge #8-#11") then green 08-06T12:07Z ("All #8-#11 branch tips are ancestors of HEAD; routing smoke 9/9"); autorun_card green 08-05T23:40Z; tier_refuse green 08-06T12:19Z ("focused suites 33+29 passed"). Surfaces on disk: dashboard/lab default port 8765 (`main.py:213`, `main.py:2068`), queue/handoff 132 entries, queue/results 92 entries, configs/lanes.yaml 6,968B | LANDED |
| v3 | in_progress (L126) | shipped | 6 gate rows, all ending green: factory_pilot red 08-05T23:40Z then green 08-05T23:55Z (evidence `memory/factory/build_audit-*.json`), freeze_gate + chat_preflight + witness_filed green 08-06T13:45Z, deepseek_run green 08-06T14:02Z (evidence `memory/runs/v3_deepseek_proof.md`, 2,516B, exists; task ta79c0045f0 exit 0). On-disk audit JSON head: `"schema": "build_audit.v1"`, `"verdict": "pass"`. Code present: mag/orchestrator.py, mag/factory_machine.py, mag/factory_gate.py, mag/conductor.py | LANDED |
| v4 | planned (L127) | shipped | 4 gate rows green 08-06T14:12-14:22Z, evidence files all verified on disk this session: memory/improve/evals/conductor/2026-08-06.json (conductor 10/10, threshold 1.0), memory/steward/daily/2026-08-06.json, memory/training/cost_ledger.jsonl (2,312 lines, 1.7M), memory/training/export/orch_train_2026-08-06.manifest.json + .jsonl. v4 notes honesty clause L33: "Shipping v4 does not claim a trained local foreman... Training the local model remains v5 work" | LANDED (process gates, NOT trained weights) |
| v5 | planned (L128) | planned | 2 of 3 named gates green 08-06: gstd_t0_probe (evidence memory/runs/roadmap/v5-gstd-t0-probe.json: worker task t6f6a517cb2 exit 0, 600.1s, full suite 477 passed / 7 skipped) and vast_train_dry (evidence v5-vast-train-dry.json: deepseek worker failed_write_shape, codex verifier, focused 3 passed + full 480 passed / 7 skipped, commit bc88777). Third gate xrpl_read_tools: NO row in gates.jsonl and `grep -rli xrpl mag/ tools/ scripts/` returns zero files; only the plan doc docs/ref/MAG_v5_XRPL.md (5,376B) exists. Plus 3 non-arc regime_* rows (09-26: ratchet, fanout width, drift registry) filed under the v5 commitment; per registry L107 these "never flip a version to shipped" | PARTIAL (GSTD + Vast dry real; XRPL absent; formally ungraduated) |
| v6 | curriculum TBD (L129) | curriculum_tbd | No gate rows, no release notes (RELEASE_NOTES_v6.md does not exist), meaning filed only | ASPIRATIONAL |
| v7 | curriculum TBD (L130) | curriculum_tbd | Same: no artifacts beyond filed meaning | ASPIRATIONAL |
| v8 | curriculum TBD (L131) | curriculum_tbd | Same | ASPIRATIONAL |
| v9 | curriculum TBD (L132) | curriculum_tbd | Same | ASPIRATIONAL |
| v10 | curriculum TBD (L133) | curriculum_tbd | Same | ASPIRATIONAL |

Machine cross-check run: `./.venv/Scripts/python.exe main.py release status` printed `v1: shipped gates=0 / v2: shipped gates=3 / v3: shipped gates=6 / v4: shipped gates=4 / v5: planned gates=3 / v6..v10: curriculum_tbd gates=3`. Caveat: that gates column is `gates_defined` (`len(gates)` at mag/release_registry.py:70), i.e. gates DEFINED not passed, and for v6-v10 the yaml literal `gates: TBD` is a 3-character string so `len()` counts 3 - a display artifact, not three gates.

## Central finding: the compass is stale against its own machine truth

1. Compass section 3.2 (lines 120-135) says v3 in_progress, v4 planned, v5 planned. Machine truth (releases.yaml, version_roadmap.yaml, VERSION_REGISTRY.md as-of 2026-09-26, and the live `release status` command) says v1-v4 shipped, v5 planned, v6-v10 curriculum_tbd. The compass understates reality by two shipped versions.
2. The drift is dated by git. `git log --follow` on the compass: last three touches are 383fed94f (2026-09-27 10:01:25 -0400), 39afa181f, 1c156e2fa (2026-08-06 12:10:42 -0400). `git show ada91890f:configs/releases.yaml` (ada91890f = 2026-08-05 12:33:06 +0000, "Align version semantics: v1 Grok origin, v2 projects repo, v3 planning") has statuses v1 shipped / v2 shipped / v3 in_progress / v4 planned / v5 planned - exactly what the compass still shows. The compass text is a fossil of the 08-05 state.
3. Commit 1c156e2fa (08-06 12:10) flipped releases.yaml v3 in_progress to shipped and v4 planned to shipped and appended v6-v10 curriculum_tbd slots - but did not update compass section 3.2. The gate rows that justify the flip landed the same day (v3 remaining gates 13:45-14:02Z, v4 gates 14:12-14:22Z; the v4 status flip at 12:10 ran about 2 hours ahead of its own gate rows).
4. The only later compass edit, 383fed94f (09-27), added the section 4 FROZEN stamp and states explicitly: "Vision prose (section 1-3, 5+) untouched this turn - freeze stamp only, no compass rewrite." So the staleness is deliberate freeze, not an overwrite, but the freeze never reconciled section 3.2 and the front-matter as-of is still 2026-08-05 (L4) while VERSION_REGISTRY.md as-of is 2026-09-26.
5. The compass's own amend protocol (section 8, L241-248: "RUN A green - update section 4 built state; bump as-of"; "New version gate passed - release record + update VERSION_REGISTRY") was not executed for section 3.2 or the as-of. The registry followed it; the compass did not.
6. Section 4 is honest-by-labeling: it self-describes as the 2026-08-05/06 snapshot frozen 2026-09-26 (Mag P0-1) and points live truth to tip + state/CURRENT.md + watch/inbox/INDEX.json. But even at freeze time its "Not yet green: RUN A merge ritual... v3 factory pilot first audit JSON" rows were already resolved on 08-06 per gates.jsonl - the frozen body was stale on the day it was stamped.

## The arc has decoupled from daily operation

state/CURRENT.md (updated 2026-09-27, head 60 lines read) contains zero v1-v10 references; the estate speaks in burns, organs, waves, and machines. The version arc survives as law-on-disk maintained at phase boundaries. VERSION_REGISTRY.md L105 records this honestly: "The version-gate trail went dark 2026-08-10 while fleet motion continued (468K+ training events since)... Drift pairs T4/T5 (B2-05, 2026-09-26) proved the referent frozen while lanes moved." The 09-26 revival added regime_* milestones (separate display field per B2-209, three such rows exist in gates.jsonl under v5). Live proof of continued motion: memory/training/events.jsonl first ts 2026-08-05T13:44:34Z, last ts 2026-09-28T22:23:04Z (today), and it grew between two `wc -l` runs this session (573,158 then 574,593 lines, live append); `grep -c release_milestone` = 21.

## Machine-truth internal defects found

1. releases.yaml L110 sets v5 notes_path to docs/ref/releases/RELEASE_NOTES_v5.md which does not exist on disk (25-path existence sweep: 24 EXISTS, 1 MISSING); VERSION_REGISTRY.md L33/L66 itself says v5 release notes are TBD. Yaml promises what the registry disclaims.
2. `release status` gates=N is gates_defined (mag/release_registry.py:70 `len(gates)`); for v6-v10 the string "TBD" counts as 3.
3. version_roadmap.yaml as_of is "2026-08-06" (L9) yet carries v3/v4 graduation notes - fine, but nothing in either machine file points out that the compass table contradicts them.
4. Unsloth: the v2 current_built list (roadmap L99 "unsloth_seat") has no backing module - `grep -rli unsloth configs/ mag/` hits only version_roadmap.yaml itself (the claim), violation_baseline.json, and mimosa hook-state files; no mag module and no weights dir. v4's honesty clause already scopes training as v5 work; the unsloth seat remains configuration-intent only. (Grep scope was configs/ and mag/ only.)

## Answer to the ask

Landed: v1, v2, v3, v4 (v1 external origin era, witnessed; v2-v4 backed by green gate rows in memory/improve/releases/gates.jsonl plus evidence artifacts verified on disk this session). Partial: v5 (gstd_t0_probe and vast_train_dry green with evidence JSONs read this session; xrpl_read_tools has no gate row and zero code; status stays planned). Aspirational: v6, v7, v8, v9, v10 (curriculum slots, no gate rows, no release notes). The compass table itself is the stale artifact: correct for 08-05, two versions behind since 08-06, deliberately untouched by the 09-26/27 freeze stamps.

## Method (commands as run)

- Read: compass, version_roadmap.yaml, releases.yaml, VERSION_REGISTRY.md, RELEASE_NOTES_v3.md, RELEASE_NOTES_v4.md in full; head of RELEASE_NOTES_v1.md and state/CURRENT.md.
- `ls docs/ref/releases/` (8 files) + 25-path existence loop with sizes (1 MISSING).
- `wc -l -c` compass; `wc -l` gates.jsonl (19) and events.jsonl (573,158 then 574,593); `grep -c release_milestone` (21); head/tail ts extraction.
- `cat memory/improve/releases/gates.jsonl` (all 19 rows read); `grep -oE '"version": "v[0-9]+"' | sort | uniq -c` (v2=4, v3=6, v4=4, v5=5).
- Existence + size check of all 7 evidence files named in gate rows (all exist); `head -c 600 memory/factory/build_audit-factory-audit-json.json`; `cat` both v5 roadmap evidence JSONs.
- `grep -rli xrpl mag/ tools/ scripts/` (empty); `grep -rli unsloth configs/ mag/`; `ls mag/ | grep -iE "orchestr|factory|conductor|steward|chat|lab|gstd|handoff|improve|grok|escalate|router"`.
- `git log --follow -5` compass, `git log -8` releases.yaml, `git show` on 383fed94f / 1c156e2fa / ada91890f / 19620ea5e with diffs on the truth files; `git status --short` + `git diff HEAD --stat` on releases.yaml / roadmap / compass / docs/ref/releases (all clean: working tree equals HEAD for these).
- `./.venv/Scripts/python.exe main.py release status`; `grep -n gates_defined mag/release_registry.py`; `grep -n 8765 main.py`; `ls queue/handoff | wc -l` (132), `ls queue/results | wc -l` (92).

Not run: the X witness post URLs were not fetched (external network, out of item scope); v1 and v2 release notes were read partially (head), not in full.
