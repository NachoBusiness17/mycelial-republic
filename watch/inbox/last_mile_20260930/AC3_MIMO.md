# AC3 — XiaomiMiMo/MiMo-V2.6-RL-oss census

**Date:** 2026-09-29 · **Seat:** ZCode subagent (AC3) · **Owns:** `tools/mimo_census.py`, this receipt · **No commit** (per mission).
**Instrument:** `pyarrow` 25.0.1 over the 5 parquet shards downloaded 2026-09-29 via `huggingface_hub.snapshot_download` (allow_patterns = parquet + README + image-mapping; the 41,285-file `general/envs/` tree was excluded — rows embed the env manifests; 3 env files fetched separately for format inspection). `datasets` lib absent from venv; hub route was the sanctioned alternative. Shards + README: ~21.4 MB under `data/mimo_v26/`. License apache-2.0, public, unauthenticated.

## Census (7,780 rows total)

| shard | rows | data_source | ability | agent | reward style | verifier (per README) |
|---|---|---|---|---|---|---|
| code.parquet | 2,698 | opensource-code | swe | mimo_swe_agent | rule | executable tests |
| webdev.parquet | 2,093 | blackbox/webdev | webdev | mimo_swe_agent | rule | visual grading |
| cyber.parquet | 1,000 | arvo | (none) | mimo_swe_agent | rule | rule checks |
| music.parquet | 1,000 | music | music_generation | (none) | rule | rule checks |
| general/train.parquet | 989 | mimoagent/general_agent (925) + terminal_bench (64) | agent | mimo_swe_agent | rule | rubric-based judging |

**Row schema (uniform):** `data_source, ability, agent_name, prompt[{role,content}], reward_model{style,ground_truth}, extra_info{index,instance_id,dataset_type,instance_json}`. `reward_model.ground_truth` is empty in 100% of rows — reward is computed at rollout time by the verifier, never stored.

**Code shard envs:** every row = one bespoke docker image (`format-code-task-NNNNNN:latest`, 2,698 distinct; published at hub.docker.com/r/xiaomimimo/mimo-v2.6-rl-oss) + `test_command` (`bash /testbed/mimo_test_command.sh` ×1,903; `/workspace/repo` variant ×519; dual `base && new` ×276) + `test_patch` (all 2,698) + `verifier_timeout_sec=1800` (uniform). cwd is constant `/testbed` or `/workspace/repo`.

**Project types (text heuristic — instance ids and cwd carry no project field, so this is a multi-label regex over problem_statement; 2,002/2,698 name no stack):** Python 465, JS/TS/Node 171, Django 31, Java/JVM 29, C/C++ 25, Go 13, GitHub Actions 8, Rust 8, Flutter/Dart 4, Gazebo/ROS 1. Prompts are real GitHub issue bodies (`[FEAT]`/`[Bug]` prefixed).

**General shard envs (format, from `general/envs/` tree + one manifest fetch):** harbor-style two-container env — main + sidecar; `manifest.json` declares `uploads` (workspace → main; system sqlite state.dbs + tools + mcp_http/mcp_bridge → sidecar), `setup` command w/ 300s timeout, `wait_ports` (4 MCP HTTP servers), `mcp_servers` list. `run_verify.py` extracts last assistant message from session logs, builds post_state from the sqlite DBs, runs task rubrics, writes `/logs/verifier/reward.json`; env switches `VERIFY_DETERMINISTIC=1` (default on) and `VERIFY_AGENT_JUDGE=0` (default off → LLM judge available but opt-in). terminal_bench rows add agent_timeout 900s, verifier 120–240s, memory 2048 MB, allow_internet=false. Tasks are bilingual (zh/en) accounting/audit/tax knowledge work over fake SaaS MCP servers.

**Music shard:** bilingual prompts (zh 504 / en 496), extra_info = src_id, lang, tag, length (short 504/long 496), nvoice_want, bpm, meter. No docker env.

## 5-prompt sample (seed 20260930, one per shard)

1. **code** `format-code-task-002057` — "# Host multiple applications behind one server…" (Tornado-style AS issue). env: image `format-code-task-002057:latest`, `bash /testbed/mimo_test_command.sh`, verifier 1800s, cwd /testbed, test_patch present.
2. **cyber** `arvo_42488517` — "MemorySanitizer: use-of-uninitialized-value in tinfl_decompress (miniz)". env: `arvo-rl:v1-arvo-42488517`, cwd /home/agent, no test_command/timeout (verifier baked into image).
3. **general** `s3k_0199_accounting_audit_tax_zh_t2_rl_005` — zh audit task over 用友 NC Cloud + csv/xlsx exhibits. env: `general-agent-env-0:oss`, cwd /work/workspace, env_task_dir + num_turns; timeouts live in the env dir manifest, not the row.
4. **music** `gK-0243` — "Compose a piano duet for four hands in F major, 99 BPM andante, 4/4, ~96 bars…". No container; reward = rule checks on the symbolic output.
5. **webdev** `dasyn_260630_01338` — "Create a modern static photography dashboard landing page, Amazon-inspired…". env: shared `webdev-rl-opensource:v2`, cwd /workspace; reward = visual grading.

Full JSON: `watch/inbox/last_mile_20260930/ac3_mimo_census.json`.

## Format comparison — MiMo SWE envs vs estate water-graph legality envs

| axis | MiMo-V2.6-RL-oss | estate (`tools/legality_dataset.py`, water_graph.v1) |
|---|---|---|
| Row format | chat messages (role/content list) + env config as JSON string in `extra_info.instance_json` | flat typed-token JSONL row: `[STATE] nodes/pipes [ACTION] verb/tgt [LABEL]` + full graph spec per row |
| Verifier | external docker per task (2,698 bespoke images; harbor main+sidecar w/ MCP + sqlite post-state); test_patch + shell script | in-process deterministic Python engine (MountainWorld validate/_apply verbatim); no container, no subprocess |
| Reward signal | `style=rule` uniformly, but heterogeneous in fact: executable tests (code), rule checks (cyber/music), deterministic rubrics + opt-in LLM agent-judge (general), visual grading (webdev); `ground_truth` column empty, reward computed at rollout into `reward.json` | exact-match label measured by the engine before training: `legal_gain / legal_no_gain / illegal_{unknown_verb,unknown_target,dry_pool}`; zero inference, zero wall clock |
| Time | verifier 1800s / agent 900s / setup 300s wall-clock timeouts | none — seed → byte-identical, reproducible via `MANIFEST.json` seed |
| Scale strategy | breadth: 7,780 human-world tasks, heavy infra | depth: one synthetic hydraulics world, byte-reproducible |

**Shared doctrine:** both make the environment — not a model — the judge, and both default away from LLM judging (MiMo ships `VERIFY_AGENT_JUDGE=0` default; estate has no judge at all). **Divergence:** MiMo pays docker + wall clock + per-task images for real-world breadth; the estate pays synthetic narrowness for determinism. **Steal candidates:** (a) their `manifest.json` env contract (`uploads`/`setup`/`wait_ports`/`mcp_servers`) + `reward.json` convention is a clean container-native rollout lane the water graph could adopt without touching label law; (b) their per-row `instance_json`-embeds-env pattern beats our sidecar manifest for portability; (c) our seed+manifest byte-reproducibility law is exactly what their `VERIFY_AGENT_JUDGE` rubric lane lacks — if the estate ever runs judged rubrics, keep them opt-in the way MiMo does.

## Next-attempt design (if re-run needed)

Download already succeeded; for a re-run: `python tools/mimo_census.py` is idempotent (skips existing shards, `--no-write` for print-only). To census the 925 env dirs too, extend `allow_patterns` with `general/envs/*/manifest.json`. No auth needed unless rate-limited (HF_TOKEN optional).
