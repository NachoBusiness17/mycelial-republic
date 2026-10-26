# tests/ mock + fixture census (s2-19, 2026-09-28)

Item: census every test fixture and mock in tests/ - what does it mock, is the mock accurate,
has the real interface changed since the mock was written. Banked to
`watch/inbox/burn_reset_20260927/flash50/mock-drift.md`; receipt `s2-19.md`.

Snapshot: repo HEAD `993099f65` (2026-09-28 19:21:17 -0400), branch `mag/run-beta1-factory-build-audi-20260806T231709Z`.
Every number below is from a command run during this ask (instruments banked alongside; see §9).
Per the B2-216 census-denominator law: these are counts of this tree at this moment with the named instrument.

## 1. Headline

| Measure | Number | Instrument |
|---|---|---|
| tests/ .py files (excl __pycache__/.pytest_cache) | 373 | os.walk |
| tests/ .py lines | 40,930 | read+splitlines |
| test_* function defs | 2,312 | AST name census (defs, not pytest collected items - different denominators, never difference vs the 2,303 collected 09-27 carrier) |
| unittest.mock object instantiations (MagicMock/Mock/AsyncMock/PropertyMock) | 0 | AST + byte-grep cross-check (0 hits each) |
| mock_open / create_autospec / autospec=True usage | 0 / 0 / 0 | AST + byte-grep |
| `unittest.mock` imports | 7 files | byte-grep |
| unittest.mock patch() calls | 26 calls, 7 unique string targets, 5 files | AST |
| monkeypatch.setattr calls | 1,127 calls in 182 files | AST (method count) |
| monkeypatch.setattr unique module-level targets | 86 string-form + 458 object-form (alias-resolved) = 527 unique | AST + import-alias rewrite |
| monkeypatch.setenv / delenv / setitem | 82 / 48 / 7 calls | AST |
| fake/stub/double class definitions | 15 in 12 files | AST name+bases heuristic, hand-read all 15 |
| pytest fixtures (@pytest.fixture) | 87 defs in 76 files (77 function-scope, 10 module-scope, 23 autouse, 20 yield-based, 0 create mock objects) | AST |
| conftest.py fixtures | exactly 1 (`_isolate_gap_log`, autouse, function scope) + one module-level subprocess.Popen patch | read tests/conftest.py:36-83 |
| non-py fixture data files under tests/ | 0 (two independent walks) - fixture data is code-inline | os.walk |
| test files with no monkeypatch, no patch(), no fake class | 180 (pure functional tests) | AST per-file flags |

**Stale-mock verdict: 526 of 527 unique mocked/patched module-level targets resolve against the live tree at HEAD.
The 1 exception (`mag.orchestrator.ollama_tags`, tests/test_orchestrator_queue.py:173) is patched with
`raising=False` as a deliberate defensive clear; the live interface moved to `models.registry.ollama_tags`,
which the same test patches for real at :178; the file passes live (12 passed, §7).**

**Interface-locking verdict: near zero. 0 autospec, 0 create_autospec, 1 spec= in the whole tree. Nothing uses
unittest.mock objects at all - the suite fakes by direct monkeypatch.setattr replacement and hand-rolled
double classes. Drift protection is structural (isolation fixtures + suite runs), not spec-locked doubles.**

## 2. The 7 patch() targets (all resolve; real signatures captured live)

| Target | Sites | Real interface today (inspect.signature at HEAD) | Verdict |
|---|---|---|
| `backend.provider_gateway.chat_messages` | test_provider_gateway.py:62; test_provider_gateway.py:81; test_provider_gateway.py:104; test_provider_gateway.py:155; test_provider_gateway.py:178 | (provider_id: 'str', messages: 'list[dict[str, Any]]', *, tools: 'list[dict[str, Any]] \| None' = None, model: 'str \| None' = None, temperature: 'flo | EXISTS; module backend/provider_gateway.py |
| `backend.provider_gateway.provider_keys` | test_provider_gateway.py:33 | (pcfg: 'dict[str, Any]') -> 'list[str]' | EXISTS; module backend/provider_gateway.py |
| `mag.route._run_local` | test_clerk_route_fix.py:21; test_clerk_route_fix.py:48 | (goal: 'str', kind: 'str') -> 'dict[str, Any]' | EXISTS; module mag/route.py |
| `mag.route.chat` | test_clerk_route_fix.py:20; test_clerk_route_fix.py:30; test_clerk_route_fix.py:39; test_clerk_route_fix.py:47; test_clerk_route_fix.py:57 | (role: 'str', system: 'str', user: 'str', temperature: 'float' = 0.2, *, strict: 'bool' = True, timeout_seconds: 'float' = 300.0) -> 'str' | EXISTS; module mag/route.py |
| `mag.voice_turn._voice_context` | test_voice_turn.py:28; test_voice_turn.py:57; test_voice_turn.py:75; test_voice_turn.py:95; test_voice_turn.py:132 | () -> 'str' | EXISTS; module mag/voice_turn.py |
| `mag.voice_turn.handle_voice_turn` | test_voice_scratch.py:26; test_voice_scratch.py:42 | (body: 'dict[str, Any] \| None') -> 'dict[str, Any]' | EXISTS; module mag/voice_turn.py |
| `models.providers.chat_provider` | test_voice_shadow.py:39; test_voice_turn.py:27; test_voice_turn.py:56; test_voice_turn.py:74; test_voice_turn.py:94; test_voice_turn.py:131 | (provider_id: 'str', system: 'str', user: 'str', *, model: 'str \| None' = None, temperature: 'float' = 0.2, max_tokens: 'int' = 65536, tier: 'str' =  | EXISTS; module models/providers.py |

Accuracy note: every patch() call passes only `return_value=`/`side_effect=` (18/4 of 26 calls), 0 autospec,
so these mocks assert nothing about the real signatures - they are blind replacements that pass because the
SUT calls them with the old shapes. Verified accurate today by reading + live runs, but unlocked against drift.

## 3. The 86 monkeypatch.setattr string targets (all sites verified)

All 86 resolve at HEAD except `mag.orchestrator.ollama_tags` (section 6). Real kind captured at runtime.

| Target | Sites | Real kind | Module | Status |
|---|---|---|---|---|
| `config.LAB_BIND_PATH` | 1 | WindowsPath | config.py | OK |
| `config.ROOT` | 2 | WindowsPath | config.py | OK |
| `llm._chat_http` | 1 | function | llm.py | OK |
| `llm.chat` | 1 | function | llm.py | OK |
| `mag.agent_corpus.log_chat` | 2 | function | mag/agent_corpus.py | OK |
| `mag.agent_desk.DESK_PATH` | 9 | WindowsPath | mag/agent_desk.py | OK |
| `mag.agent_desk.ROOT` | 8 | WindowsPath | mag/agent_desk.py | OK |
| `mag.autorun_common.refresh_context_for_goal` | 1 | function | mag/autorun_common.py | OK |
| `mag.cleanup.ROOT` | 4 | WindowsPath | mag/cleanup.py | OK |
| `mag.cleanup.TRASH` | 1 | WindowsPath | mag/cleanup.py | OK |
| `mag.coding_session_loop.SESSION_STATE_PATH` | 5 | WindowsPath | mag/coding_session_loop.py | OK |
| `mag.coding_session_loop._check_path_gate` | 2 | function | mag/coding_session_loop.py | OK |
| `mag.coding_session_loop._run_cmd` | 3 | function | mag/coding_session_loop.py | OK |
| `mag.coding_session_loop.load_config` | 1 | function | mag/coding_session_loop.py | OK |
| `mag.coding_session_orchestrator.ORCH_STATE_PATH` | 4 | WindowsPath | mag/coding_session_orchestrator.py | OK |
| `mag.coding_session_orchestrator._sprint_gate_check` | 4 | function | mag/coding_session_orchestrator.py | OK |
| `mag.coding_session_orchestrator.assess_sprint_status` | 1 | function | mag/coding_session_orchestrator.py | OK |
| `mag.coding_session_orchestrator.orchestrator_tick` | 4 | function | mag/coding_session_orchestrator.py | OK |
| `mag.coding_session_orchestrator.plan_session` | 4 | function | mag/coding_session_orchestrator.py | OK |
| `mag.coding_session_runner.ROOT` | 1 | WindowsPath | mag/coding_session_runner.py | OK |
| `mag.coding_session_runner.RUN_REPORT_DIR` | 5 | WindowsPath | mag/coding_session_runner.py | OK |
| `mag.coding_session_runner._git_out` | 1 | function | mag/coding_session_runner.py | OK |
| `mag.coding_session_runner.close_session_if_ready` | 3 | function | mag/coding_session_runner.py | OK |
| `mag.coding_session_runner.run_preflight` | 5 | function | mag/coding_session_runner.py | OK |
| `mag.coding_session_runner.seed_desk` | 4 | function | mag/coding_session_runner.py | OK |
| `mag.coding_session_runner.session_status` | 5 | function | mag/coding_session_runner.py | OK |
| `mag.compass.record_decision` | 1 | function | mag/compass.py | OK |
| `mag.context_pack.build_context_pack` | 1 | function | mag/context_pack.py | OK |
| `mag.context_pack.format_context_pack_text` | 1 | function | mag/context_pack.py | OK |
| `mag.desk_dialogue.CURSOR_PATH` | 2 | WindowsPath | mag/desk_dialogue.py | OK |
| `mag.desk_dialogue.DIALOGUE_LOG` | 4 | WindowsPath | mag/desk_dialogue.py | OK |
| `mag.desk_dialogue.read_cursor` | 1 | function | mag/desk_dialogue.py | OK |
| `mag.desk_dialogue.read_trust_status` | 1 | function | mag/desk_dialogue.py | OK |
| `mag.desk_observer.collect_observer_context` | 1 | function | mag/desk_observer.py | OK |
| `mag.desk_overseer.measure_context_pressure` | 2 | function | mag/desk_overseer.py | OK |
| `mag.doctor.check_scheduled_tasks` | 7 | function | mag/doctor.py | OK |
| `mag.env_registry.activate_track` | 1 | function | mag/env_registry.py | OK |
| `mag.env_registry.get_active_env` | 1 | function | mag/env_registry.py | OK |
| `mag.factory_machine.checkout_run_branch` | 1 | function | mag/factory_machine.py | OK |
| `mag.ghost.ROOT` | 2 | WindowsPath | mag/ghost.py | OK |
| `mag.governor_autorun.enqueue_routed` | 1 | function | mag/governor_autorun.py | OK |
| `mag.improve.scout` | 2 | function | mag/improve.py | OK |
| `mag.improve_loop.run_improve_cycle` | 2 | function | mag/improve_loop.py | OK |
| `mag.lane_cadence.cooldown` | 2 | function | mag/lane_cadence.py | OK |
| `mag.loop_audit.AUTORUN_TRAIL` | 1 | WindowsPath | mag/loop_audit.py | OK |
| `mag.nervous_system.build_glance` | 1 | function | mag/nervous_system.py | OK |
| `mag.operating_protocol.build_envelope` | 2 | function | mag/operating_protocol.py | OK |
| `mag.operator_inbox.log_behavioral_event` | 1 | function | mag/operator_inbox.py | OK |
| `mag.operator_inbox.status` | 1 | function | mag/operator_inbox.py | OK |
| `mag.operator_mode.pause_reason` | 6 | function | mag/operator_mode.py | OK |
| `mag.orchestrator.enqueue` | 1 | function | mag/orchestrator.py | OK |
| `mag.orchestrator.list_queue` | 2 | function | mag/orchestrator.py | OK |
| `mag.orchestrator.spawn_task` | 1 | function | mag/orchestrator.py | OK |
| `mag.orchestrator.task_status` | 4 | function | mag/orchestrator.py | OK |
| `mag.peer_handoff.file_peer_handoff` | 1 | function | mag/peer_handoff.py | OK |
| `mag.pro_library.add_move` | 1 | function | mag/pro_library.py | OK |
| `mag.release_registry.GATES_LOG` | 2 | WindowsPath | mag/release_registry.py | OK |
| `mag.release_registry.record_gate` | 1 | function | mag/release_registry.py | OK |
| `mag.remedy.REMEDY_DIR` | 1 | WindowsPath | mag/remedy.py | OK |
| `mag.repo_readiness.repo_readiness` | 1 | function | mag/repo_readiness.py | OK |
| `mag.route.model_for` | 1 | function | mag/route.py | OK |
| `mag.router.route` | 2 | function | mag/router.py | OK |
| `mag.run_trail.close_run` | 1 | function | mag/run_trail.py | OK |
| `mag.session_state_brief.ROOT` | 2 | WindowsPath | mag/session_state_brief.py | OK |
| `mag.steward.execute_steward_goal` | 1 | function | mag/steward.py | OK |
| `mag.swarm_worker.provider_spawn_allowed` | 1 | function | mag/swarm_worker.py | OK |
| `mag.swarm_worker.run_rightsized_once` | 1 | function | mag/swarm_worker.py | OK |
| `mag.switchboard.route_intent` | 1 | function | mag/switchboard.py | OK |
| `mag.training_events.EVENTS_PATH` | 1 | WindowsPath | mag/training_events.py | OK |
| `mag.training_events.emit` | 3 | function | mag/training_events.py | OK |
| `mag.verkle_audit.DAILY` | 2 | WindowsPath | mag/verkle_audit.py | OK |
| `mag.verkle_knot.append_verkle_knot` | 1 | function | mag/verkle_knot.py | OK |
| `mag.virtual_desk_loop.PACK_ROOT` | 3 | WindowsPath | mag/virtual_desk_loop.py | OK |
| `mag.virtual_desk_loop.ROOT` | 2 | WindowsPath | mag/virtual_desk_loop.py | OK |
| `mag.virtual_desk_loop.load_config` | 1 | function | mag/virtual_desk_loop.py | OK |
| `models.probe.probe_all` | 1 | function | models/probe.py | OK |
| `models.providers.get_provider` | 5 | function | models/providers.py | OK |
| `models.providers.list_provider_ids` | 4 | function | models/providers.py | OK |
| `models.providers.load_providers` | 4 | function | models/providers.py | OK |
| `models.quota.pick_provider` | 2 | function | models/quota.py | OK |
| `models.quota.provider_budget` | 10 | function | models/quota.py | OK |
| `models.quota.record_usage` | 2 | function | models/quota.py | OK |
| `models.registry.model_for` | 1 | function | models/registry.py | OK |
| `os.name` | 1 | str | C:\Users\foste\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\Lib\os.py | OK |
| `subprocess.run` | 1 | function | C:\Users\foste\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\Lib\subprocess.py | OK |
| `sys.argv` | 3 | list | - | OK |

## 4. The 458 object-form setattr kind-slots (434 unique targets, 905 qualified call sites) + 23 local-object stubs

(458 kind-slots; 24 of them also appear as string-form/patch targets, so 434 unique object-form targets.
Cross-foot: 199 string-form sites + 928 object-form sites (incl. the 23 local-object stubs) = 1127 = the AST setattr call count.
Object-form targets like `monkeypatch.setattr(wc, "tick", ...)` were rewritten through each file's import
table (`import mag.water_computer as wc` -> `mag.water_computer.tick`) and resolved at runtime. Rollup by
resolved module (top 30 of 160 distinct modules):

| Resolved module | Targets | OK | Not-OK |
|---|---|---|---|
| mag/shared_surface.py | 11 | 11 | 0 |
| mag/unsloth_seat.py | 11 | 11 | 0 |
| mag/orchestrator.py | 10 | 9 | 1 |
| mag/capability_steal.py | 9 | 9 | 0 |
| mag/desk_dialogue.py | 9 | 9 | 0 |
| mag/factory_machine.py | 9 | 9 | 0 |
| mag/roadmap_runner.py | 9 | 9 | 0 |
| mag/process_supervisor.py | 8 | 8 | 0 |
| mag/steward.py | 8 | 8 | 0 |
| mag/verkle_knot.py | 8 | 8 | 0 |
| (IMPORT_FAIL) | 7 | 0 | 7 |
| mag/agent_state.py | 7 | 7 | 0 |
| mag/gstd_probe.py | 7 | 7 | 0 |
| mag/feature_lab.py | 6 | 6 | 0 |
| mag/ghost.py | 6 | 6 | 0 |
| mag/tripartite_boot.py | 6 | 6 | 0 |
| mag/attention_ranker.py | 5 | 5 | 0 |
| mag/doctor.py | 5 | 5 | 0 |
| mag/growth_cycle.py | 5 | 5 | 0 |
| mag/lane_runner.py | 5 | 5 | 0 |
| mag/lifecycle.py | 5 | 5 | 0 |
| mag/link_library.py | 5 | 5 | 0 |
| mag/run_trail.py | 5 | 5 | 0 |
| mag/swarm_worker.py | 5 | 5 | 0 |
| models/providers.py | 5 | 5 | 0 |
| models/quota.py | 5 | 5 | 0 |
| mag/afk_loop.py | 4 | 4 | 0 |
| mag/arena_adapter.py | 4 | 4 | 0 |
| mag/behavioral_synth.py | 4 | 4 | 0 |
| mag/chain_guard.py | 4 | 4 | 0 |

External/stdlib targets patched by object form (all exist): `os.readlink`, `socket.create_connection`, `socket.getaddrinfo`, `sys.argv`, `sys.platform`, `sys.stdin`, `sys.stdout`, `urllib.request.urlopen`.

23 sites stub attributes on LOCAL objects (instances/loaded modules, not module interfaces - not resolvable
statically, all live and exercised by the suite):

- `tests/test_context_checkpoint_pack.py:17` `setattr(engine.checkpoint_dir, ...)`
- `tests/test_corpus_fts.py:65` `setattr(corpus.CATALOG, ...)`
- `tests/test_corpus_fts.py:66` `setattr(corpus.FTS_DB, ...)`
- `tests/test_corpus_fts.py:67` `setattr(corpus.TAGS, ...)`
- `tests/test_corpus_fts.py:68` `setattr(corpus.REBUILD_CLI, ...)`
- `tests/test_corpus_fts.py:197` `setattr(rebuild._load_corpus, ...)`
- `tests/test_corpus_fts.py:216` `setattr(rebuild._load_corpus, ...)`
- `tests/test_dead_hand.py:28` `setattr(dead_hand.STATE, ...)`
- `tests/test_dead_hand.py:29` `setattr(dead_hand.STATE_PATH, ...)`
- `tests/test_dead_hand.py:30` `setattr(dead_hand.WITNESSES_PATH, ...)`
- `tests/test_dead_hand.py:31` `setattr(dead_hand.HOLD_DIR, ...)`
- `tests/test_dead_hand.py:33` `setattr(dead_hand.VOICE_SURFACES, ...)`
- `tests/test_dead_hand.py:35` `setattr(dead_hand._loud, ...)`
- `tests/test_dead_hand.py:145` `setattr(dh.VOICE_SURFACES, ...)`
- `tests/test_gate_blocking_paths.py:59` `setattr(cs.CONFIG_DIR, ...)`
- `tests/test_gate_blocking_paths.py:60` `setattr(cs.SEAL_PATH, ...)`
- `tests/test_gate_blocking_paths.py:147` `setattr(cg.ROOT, ...)`
- `tests/test_party_subchain.py:18` `setattr(module.DIR, ...)`
- `tests/test_party_subchain.py:19` `setattr(module.CHAIN, ...)`
- `tests/test_party_subchain.py:20` `setattr(module.HEAD, ...)`
- `tests/test_party_subchain.py:21` `setattr(module.LOCK, ...)`
- `tests/test_party_subchain.py:22` `setattr(module.TIP, ...)`
- `tests/test_stealth_driver_effort_dial.py:35` `setattr(mod._sdd_key, ...)`

Note on the 7 `grounding_chain.*` targets (tests/test_grounding_chain.py): first resolution attempt reported
IMPORT_FAIL because the worker's sys.path lacked `scripts/`; the test itself inserts `sys.path` at
tests/test_grounding_chain.py:20 before `import grounding_chain`. Re-verified with scripts/ on path: module
is `scripts/grounding_chain.py`; all 6 patched attrs exist (`CHAIN_LOG` WindowsPath, `evaluate()` -> list[dict],
`queue_remaining()` -> int, `build_remaining()` -> int, `lock_age(p: Path)`, `subprocess` module). Accurate.

## 5. The 15 hand-rolled fake classes (all read; accuracy vs real call site)

| Fake (file:line) | What it mocks | Real call site evidence | Accuracy verdict |
|---|---|---|---|
| `_FakeEnv` tests/test_arena_adapter.py:93 | TextArena env (reset/get_observation/step/close) injected via `monkeypatch.setattr(aa, "ta", fake_ta)` + `_HAS_TEXTARENA` | mag/arena_adapter.py:180,182,193,195,202,208,237 call exactly those five methods | ACCURATE; `wrappers.LLMObservationWrapper` provided at test:117 is never called (mag/arena_adapter.py:186: ta.make already includes it) - vestigial provision |
| `FakeResponse` tests/test_bones_adapter.py:31 | discord.py Interaction response (`send_message`) | mag/bones_adapter.py:157-160 `send_message(text, ephemeral=True)`, :162 `send_message(build(ch))` | ACCURATE; `**_` absorber so future discord kwargs cannot break it |
| `FakeInteraction` tests/test_bones_adapter.py:40 | discord.py Interaction shell (channel_id + .response) | bones_adapter reads `interaction.channel_id` (:156) and `.response.send_message` | ACCURATE |
| `FakeLst` tests/test_catalog_scan_junctions.py:135 | os.lstat result (st_reparse_tag/st_mode) | mag/catalog_scan.py:163 reads only `getattr(lst, "st_reparse_tag", 0)`; :165 `os.readlink` (also monkeypatched at test:139) | ACCURATE; `st_mode` attribute is provided but never read - vestigial |
| `FakeJunc` tests/test_catalog_scan_junctions.py:148 | same, junction reparse tag 0xA0000003 | same SUT lines | ACCURATE (the tag flips the law split at :163) |
| `_FakeLLM` tests/test_desk_dialogue.py:71 | langchain_ollama.ChatOllama via `monkeypatch.setitem(sys.modules, "langchain_ollama", ...)` | mag/desk_dialogue.py contains ZERO langchain references (grep); llm.py:96 imports ChatOllama only inside a function with raw-HTTP fallback (:121) | VESTIGIAL - injected module is never imported on the tested path; harmless dead double kept from the pre-fallback era |
| `FakeWorld` tests/test_game_dm.py:47 | `mag.game_world` module surface (`set_state`) | mag/game_dm.py:178 `_world().set_state(f"...", record, source="game_dm")`; test replaces `gd._world` at :54 | ACCURATE (`*_args, **_kwargs` absorbs) |
| `FakeConn` tests/test_lifecycle.py:175 | socket connection context manager | mag/lifecycle.py:396 `with socket.create_connection(("127.0.0.1",11434), timeout=1.0)`; fake_create matches (address, timeout=None) | ACCURATE |
| `FakeOpener` tests/test_perplexity_research.py:41 | urllib opener at module seam `pr._OPENER` | mag/perplexity_research.py:179,227 `with _OPENER.open(req, timeout=timeout) as resp` | ACCURATE; records method/headers/body/timeout for assertions |
| `_FakeResp` tests/test_perplexity_research.py:62 | urlopen response (context manager + read) | same SUT lines (json.loads of read()) | ACCURATE |
| `_FakeTime` tests/test_process_supervisor.py:76 | `time` module attr on mag.process_supervisor (`ps.time` -> instance) | mag/process_supervisor.py:255,355 call `time.time()` only (the `time.sleep` at :62 is inside a child-code string literal) | ACCURATE |
| `_FakeProc` tests/test_spawn_smoke.py:29 | subprocess.Popen result for `orc._spawn_cmd` (pid, poll) | mag/orchestrator.py:535-561 uses only `proc.pid` and `proc.poll()`; kill path goes through `_kill_tree(proc.pid)` (:569) so no proc.kill needed | ACCURATE for the spawn path |
| `FakeModel` tests/test_t1_steering.py:35 | `chat_messages` model seam via bare rebind `ac.chat_messages = fake` (:75,:102,:121) | mag/agent_cli.py:42 imports `chat_messages` from models.providers; call at :1421; consumption :1485-1487 reads `tool_calls`/`text`/`message` keys - exactly the fake's response shape | ACCURATE; note the rebind is a raw assignment, never restored (each test reassigns; monkeypatch not used) |
| `FakeProc` tests/test_unsloth_seat.py:77 | Popen result (pid only) for mag/unsloth_seat | mag/unsloth_seat.py:314 Popen; :332,:344,:360 read `proc.pid` only | ACCURATE |
| `FakeUrlopen` tests/test_zai_backoff_floor.py:50 | global `urllib.request.urlopen` | models/providers.py:494,797,800,917,989 `with urllib.request.urlopen(req, timeout=...) as r` | ACCURATE; scripted exceptions + bodies drive the backoff law |

## 6. The one non-existent target + dead/vestigial patches (drift found by reading + the 07 full-suite run)

1. **`mag.orchestrator.ollama_tags` does not exist at HEAD** - the only ATTR_MISSING of 527. Patched at
   tests/test_orchestrator_queue.py:173 with `monkeypatch.setattr(orc, "ollama_tags", None, raising=False)`.
   The real probe lives in `models.registry.ollama_tags` (the 09-14 checkpoint d575bc168 moved the import
   inside a function per the diff hunks); the same test patches that live location at :178 with a scripted
   `lambda timeout=2.0: ["qwen2.5-coder:7b"]`. So the mock was written TOGETHER with the interface change
   (both sides last touched by the same commit), not overtaken by it. Live run: file passes (§7).
2. **Dead patch: `llm._chat_http`** (tests/test_desk_dialogue.py:79). The target still exists (llm.py:27),
   but the tested path no longer calls it: mag/desk_dialogue.py:212-215 imports and calls `llm._chat_http_ex`
   (llm.py:44; `_chat_http` is now a thin wrapper at llm.py:38). The patch intercepts nothing on the path the
   test exercises (the test also replaces `dd._invoke_local_llm` wholesale at :80-88, which is what actually
   bypasses llm). Harmless, but it no longer guards anything: if `_invoke_local_llm` were un-mocked, the
   `_chat_http` patch would not stop the real HTTP call.
3. **Vestigial double: `_FakeLLM` + langchain_ollama sys.modules injection** (tests/test_desk_dialogue.py:71-78).
   Zero langchain references remain in mag/desk_dialogue.py; vestigial from before llm.py's raw-HTTP fallback.
4. **Vestigial attributes**: `wrappers.LLMObservationWrapper` on the fake TextArena (test_arena_adapter.py:117,
   never called per mag/arena_adapter.py:186) and `FakeLst.st_mode` (test_catalog_scan_junctions.py:137, never
   read per mag/catalog_scan.py:163).
5. **Narrow-lambda risk class** (accurate today, unlocked tomorrow): fakes whose signature is a strict subset
   of the real one, e.g. `fake_chat(role, system, user, temperature=0.2)` (tests/test_desk_orchestrator.py:28)
   vs real `llm.chat(role, system, user, temperature=0.2, *, strict=True, timeout_seconds=300.0)` - holds only
   because mag/desk_orchestrator.py:77 passes `temperature` alone. The `**_`-absorber style used by
   FakeResponse/FakeWorld is the drift-proof variant; the fixed-signature style is not.
6. **Silently-bypassed fake, proven by the 07 run**: tests/test_loop_death_guards.py afk_routing parametrization
   injects `sys.modules["mag.skill_pipeline"]` only, but mag/afk_loop.py:260 does `from mag import skill_pipeline`
   inside the function - which reads the parent package attribute, not sys.modules - so once any earlier test
   imported the real module the fake stops intercepting and the real match() runs (assert produced==0 got 1).
   The same file fixed this exact disease for fuel_feed (B2-288 comment, tests/test_loop_death_guards.py:180-186:
   patch BOTH surfaces) but left skill_pipeline single-surface. Order-dependent drift: passes solo, fails in
   the full run.
7. **Mock-vs-mock collision, proven by the 07 run**: tests/conftest.py:36-44 (landed 2026-09-28) wraps
   subprocess.Popen in a plain FUNCTION; mag/headless.py:24 then captures that function as `_REAL_Popen` at
   first import under pytest (its :21-23 comment assumes capture happens before any wrapper exists - false
   in a pytest process since 09-28), and mag/headless.py:72 `class _Popen(_REAL_Popen)` raises TypeError.
   Three suite failures share this root (2x test_swarm_quota_gate via mag/swarm_worker.py:380,553;
   test_write_strip via main.py:39). Two real mocks, each correct alone, incompatible in one process.

## 7. Runtime accuracy check (the check that matters)

- Targeted live run of the two files owning the interesting drift: `pytest tests/test_orchestrator_queue.py
  tests/test_grounding_chain.py -q` -> **12 passed in 6.29s** (includes the ollama_tags test and the whole
  grounding returncode-law battery).
- Full suite, isolated run (private `--basetemp`, `-p no:cacheprovider`): **%s**. First background attempt was
  INVALID and is not counted: every setup errored with PermissionError while pytest's tmp factory rmtree'd the
  shared `agents/pytest-tmp-21944` (2,403 errors in 444.58s) - environmental tmp contention, not mock failures.

Failure taxonomy of the 8 (from the full traceback log):

| Class | Count | Tests |
|---|---|---|
| Mock-architecture collision (conftest Popen function vs headless.py Popen subclass) | 3 | test_swarm_quota_gate x2, test_write_strip x1 |
| Silently-bypassed module fake (skill_pipeline sys.modules-only injection vs afk_loop.py:260 package-attr import) | 1 | test_loop_death_guards[afk_routing] |
| Live-state assertions, not mocks | 4 | test_organ_map x3, test_shared_surface_events links baseline x1 |

- 3 MOCK-ARCHITECTURE COLLISION, one root cause: tests/conftest.py:36-44 (landed 2026-09-28) replaces subprocess.Popen with a plain FUNCTION wrapper; mag/headless.py:24 then captures that function as _REAL_Popen at first import under pytest, and mag/headless.py:72 class _Popen(_REAL_Popen) raises TypeError (function() argument 'code' must be code, not str). Casualties: tests/test_swarm_quota_gate.py::test_run_once_skips_and_leaves_queued_when_spent (via mag/swarm_worker.py:380), tests/test_swarm_quota_gate.py::test_rightsized_local_still_drains_when_remote_spent (via mag/swarm_worker.py:553), tests/test_write_strip.py::test_flag_wired_through_cli_parsers (via main.py:39 import). headless.py:21-23 comment explicitly assumes capture happens 'before any wrapper can be installed' - the conftest mock invalidates that premise in every pytest process.
- 1 SILENTLY-BYPASSED MODULE FAKE: tests/test_loop_death_guards.py::test_loop_death_guard_fires_on_raise[afk_routing] setitem's sys.modules['mag.skill_pipeline'] with a match() that raises, but mag/afk_loop.py:260 does 'from mag import skill_pipeline' INSIDE squeeze_free_test_data, which reads the PARENT PACKAGE ATTRIBUTE (mag.skill_pipeline), not sys.modules - once any earlier test has imported the real module the fake never intercepts. Result: produced=1 instead of 0. The same test file documents and fixes this exact disease for fuel_feed (B2-288 comment, tests/test_loop_death_guards.py:180-186, patch BOTH sys.modules and the mag package attribute) but skill_pipeline was left single-surface. Order-dependent: passes solo, fails in the full run.
- 4 LIVE-STATE ASSERTIONS unrelated to mocks: tests/test_organ_map.py x3 (atlas LIVE promotion missing, dirac scan open_gaps==0, elder audit still lists ask_router) and tests/test_shared_surface_events.py::test_real_links_jsonl_matches_the_registered_baseline (new unregistered LINKS.jsonl row line 377 SCOUT-QUIET-3 by free-resource-scout, sha256 355612f8e4a50694338a58ad56e706883346f8035a5a203db9a852db9dd158ff - needs a baseline-update, not a mock fix).

So the runtime answer to `is the mock accurate`: 2,390 passing tests exercise the monkeypatch surface daily;
the 4 mock-caused failures are exactly the two drift classes this census names (bypassed fakes and
mock-vs-mock incompatibility), and both are pinned to file:line above.

## 8. Has the real interface changed since the mock was written?

Instrument: last-touch commit date of each mock site's file vs last-touch of the resolved real module file
(one `git log --pretty=format:%cI --name-only` pass over full history, per-path max).

| Signal | Count (of 509 in-repo resolvable targets) |
|---|---|
| Real module last touched AFTER the mock site's file | 165 (32%) |
| Real module not touched since | 343 |
| Date-unknown | 1 |

This is a drift WINDOW, not proof of breakage: the repo is 55 days old (first commit 2026-08-04), most mocks
were written in the early-August land-rush, and modules keep evolving. Proof of non-breakage is §7 + the
existence checks. Proven interface changes since mocks were written: the two target moves in §6 items 1-2
(ollama_tags move, co-adapted same-commit; _chat_http -> _chat_http_ex, patch left dead) plus the two
mock-behavior drifts of §6 items 6-7 proven by the §7 run (bypassed fake; mock-vs-mock collision).

Largest windows (real-newer deltas, top 15):

| Target | Mock written | Real module last touched | Window |
|---|---|---|---|
| `mag.context_pack.build_context_pack` | 2026-08-04 | 2026-09-27 | +54d |
| `mag.context_pack.format_context_pack_text` | 2026-08-04 | 2026-09-27 | +54d |
| `mag.compass.record_decision` | 2026-08-05 | 2026-09-27 | +53d |
| `mag.governor_autorun.route_task` | 2026-08-05 | 2026-09-27 | +53d |
| `mag.improve.scout` | 2026-08-06 | 2026-09-28 | +53d |
| `mag.orchestrator.enqueue` | 2026-08-05 | 2026-09-27 | +53d |
| `mag.router.route` | 2026-08-06 | 2026-09-28 | +53d |
| `dashboard.rest.ROOT` | 2026-08-07 | 2026-09-28 | +51d |
| `mag.governor_autorun.enqueue_routed` | 2026-08-06 | 2026-09-27 | +51d |
| `mag.orchestrator._running_tasks` | 2026-08-06 | 2026-09-27 | +51d |
| `mag.orchestrator._spawn_cmd` | 2026-08-06 | 2026-09-27 | +51d |
| `mag.orchestrator.spawn_task` | 2026-08-06 | 2026-09-27 | +51d |
| `mag.power.stack_status` | 2026-08-06 | 2026-09-27 | +51d |
| `mag.release_registry.GATES_LOG` | 2026-08-06 | 2026-09-27 | +51d |
| `mag.release_registry.record_gate` | 2026-08-06 | 2026-09-27 | +51d |

Modules with the most post-mock churn: `mag/orchestrator.py` (11 targets), `mag/unsloth_seat.py` (11 targets), `mag/roadmap_runner.py` (9 targets), `mag/verkle_knot.py` (8 targets), `mag/steward.py` (7 targets), `mag/ghost.py` (6 targets), `mag/coding_session_orchestrator.py` (5 targets), `mag/lane_runner.py` (5 targets), `mag/swarm_worker.py` (5 targets), `mag/afk_loop.py` (4 targets).

## 9. Environment-variable fakes + fixtures

monkeypatch.setenv/delenv: 130 calls, 58 distinct literal var:method pairs (12 further calls build var names
dynamically). Top: setenv ZAI_API_KEY_Pro x11, delenv MAG_REMOTE_PROVIDER_LOCK x9, delenv
MAG_DISABLE_REMOTE_PROVIDER_LOCK x9, setenv MAG_GAPS_LOG x5 (conftest autouse), setenv MAG_ARENA_RANDOM x5,
delenv MAG_CONTAINER x5, setenv OLLAMA_HOST x4. Full map in `_s219_verify.json` (`env_vars`).

All 87 fixtures (file, fixture, line, scope, what it yields/returns - truncated):

| File | Fixture | Line | Scope | Produces (first return/yield expr) |
|---|---|---|---|---|
| conftest.py | `_isolate_gap_log` | 80 | | log |
| test_ack_reaper.py | `battery` | 25 | | checks |
| test_agent_arena.py | `_clean_arena_state` | 10 | | ? |
| test_arena_adapter.py | `_isolated` | 19 | | ? |
| test_arena_learning.py | `_isolated_arena_learning` | 13 | | ? |
| test_autorun_v1.py | `_isolate_prefs` | 18 | | ? |
| test_base_drift.py | `isolated_runs` | 17 | | runs |
| test_behavioral_awareness.py | `behavioral_fixture` | 13 | | tmp_path |
| test_bind_policy.py | `_clean_bind` | 18 | | ? |
| test_bones_adapter.py | `kernel_store` | 61 | | tmp_path |
| test_campaign.py | `module` | 25 | | load_module(MODULE_PATH) |
| test_campaign.py | `riddler_map` | 30 | | load_riddler_map(MODULE_PATH.parent) |
| test_campaign.py | `state` | 35 | | CampaignState(session_id='test-session', module_id=module.get('module_id', ''), current_ro |
| test_canvas_bridge.py | `canvas_env` | 31 | | {'src': src, 'viewports': viewports, 'lattice': lattice} |
| test_coordination.py | `coord_env` | 10 | | act |
| test_corpus_fts.py | `fts_env` | 55 | | {'corpus': corpus, 'rebuild': rebuild, 'catalog': cat, 'db': db, 'tags': tags} |
| test_dead_hand.py | `sandbox` | 24 | | (dead_hand, state) |
| test_decision_framework.py | `iso_env` | 11 | | tmp_path |
| test_doctor_provider_endpoints.py | `tags_server` | 55 | | 'http://127.0.0.1:%d/v1' % srv.server_address[1] |
| test_doctor_provider_endpoints.py | `dead_port` | 66 | | port |
| test_doctor_provider_endpoints.py | `deep_server` | 254 | | 'http://127.0.0.1:%d' % srv.server_address[1] |
| test_doctor_provider_endpoints.py | `no_dns` | 477 | | monkeypatch |
| test_drift_pairs_stamp.py | `isolated` | 109 | | tmp_path |
| test_env_load_mistral_keys.py | `clean_env` | 44 | | ? |
| test_env_redirect_tripwire.py | `plain_shell` | 25 | | monkeypatch |
| test_events_key_schema.py | `surface` | 30 | | {'inbox': inbox, 'configs': configs, 'log': inbox / 'index_events.jsonl', 'schema': config |
| test_failure_kb.py | `_isolate_fkb` | 17 | | ? |
| test_gemini_native.py | `_quota_off` | 48 | | ? |
| test_ghost.py | `isolate_ghost_dir` | 26 | | ? |
| test_ghost.py | `mock_session_state` | 278 | | tmp_path |
| test_ghost_summon.py | `tree` | 17 | | tmp_path |
| test_grounding_wave_v4.py | `wave` | 31 | | gw |
| test_growth_cycle.py | `growth_fixture` | 17 | | tmp_path |
| test_healthz_status.py | `client` | 23 | | TestClient(server.app) |
| test_icon_drop_fold.py | `sandbox` | 27 | | tmp_path |
| test_idea_graph.py | `idea_tmp` | 16 | | tmp_path |
| test_improve_loop.py | `_isolated_write_roots` | 26 | | ? |
| test_intervention_gate.py | `_isolate_register` | 17 | | reg_path |
| test_lattice_query.py | `lattice_store` | 11 | | store |
| test_law.py | `_isolate` | 18 | | ? |
| test_lesson_gate.py | `battery` | 25 | | checks |
| test_line_range_and_verify.py | `tmpfile` | 25 | | f |
| test_link_library.py | `ledger` | 18 | | fake |
| test_md_record_seal.py | `seal_estate` | 23 | | (estate, inbox, events) |
| test_memory_events.py | `memory_env` | 10 | | {'events': events, 'checkpoints': checkpoints} |
| test_meter_patrol.py | `estate` | 26 | | tmp_path |
| test_mirror_lens_gate.py | `lens_on` | 11 | | ? |
| test_mirror_voice_pack.py | `mirror_jsonl` | 14 | | republic |
| test_operator_inbox.py | `_isolate_inbox` | 13 | | ? |
| test_orchestrator_queue.py | `_isolate_orchestrator_trail` | 25 | | ? |
| test_overseer_steering_api.py | `steer_env` | 9 | | {'mail_root': mail_root, 'steering_log': steering_log} |
| test_pro_library.py | `isolated` | 16 | | tmp_path |
| test_pro_library_eval.py | `pro` | 24 | | isolated_pl |
| test_pro_library_eval.py | `isolated_pl` | 30 | | tmp_path |
| test_process_supervisor.py | `_isolate_state` | 11 | | tmp_path |
| test_provider_error_tally.py | `env` | 104 | | (log, sess_dir) |
| test_provider_gateway.py | `_keys` | 27 | | ? |
| test_pupeteering.py | `silent_steer` | 117 | | _probe_g5(MODEL, timeout=300) |
| test_qdrop_canonical.py | `qdrops` | 33 | | _mod().load_qdrops() |
| test_repack_integration.py | `_b2_403_isolate_production_sinks` | 28 | | [] |
| test_resume_contract.py | `_isolate_current` | 20 | | cur |
| test_riddler.py | `sample_graph` | 20 | | PrivateGraph(actors=['Alice', 'Beth', 'worker_A', 'worker_B'], resources=[{'name': 'GPU_la |
| test_riddler.py | `compiled_story` | 44 | | compile_surrogate(sample_graph, seed=42) |
| test_run_worth.py | `worth_fixture` | 18 | | (tmp_path, cfg) |
| test_seat_registry.py | `_isolate_seat_trail` | 14 | | ? |
| test_seed_mcp.py | `estate` | 25 | | est |
| test_seed_mcp.py | `seeded` | 40 | | seed_path |
| test_session_freeze.py | `mock_state_files` | 17 | | tmp_path |
| test_shared_surface_events.py | `surface` | 35 | | {'inbox': inbox, 'configs': configs, 'log': inbox / 'index_events.jsonl', 'baseline': conf |
| test_skill_ledger.py | `isolated` | 12 | | tmp_path |
| test_skill_lifecycle.py | `_clean_registry_and_gate` | 38 | | ? |
| test_spec_gate_job_floor.py | `isolated` | 14 | | tmp_path |
| test_stealth_driver_prompt_lance.py | `_isolate_pack` | 33 | | (pack, real) |
| test_steer.py | `_isolate` | 18 | | ? |
| test_steer_bridge.py | `isolated` | 13 | | {'inbox': inbox, 'seen': seen, 'drop': drop} |
| test_supervision_soak.py | `_isolate_pipes` | 27 | | ? |
| test_t1_steering.py | `_b2_403_isolate_production_sinks` | 22 | | [] |
| test_tesuji_shell.py | `shell_fixture` | 13 | | tmp_path |
| test_verb_stones.py | `trace` | 12 | | t |
| test_verkle_compaction.py | `folded_env` | 47 | | {'chain': chain, 'tip': tip, 'knots': knots, 'evo': evo, 'rows': rows, 'root': root, 'tmp_ |
| test_wow_bones.py | `bones` | 23 | | d |
| test_wow_bones_session.py | `fx` | 21 | | load_fixture() |
| test_wow_bones_session.py | `auth_verb` | 34 | | first_verb(fx, AUTHED) |
| test_wow_bones_session.py | `game_verb` | 39 | | first_verb(fx, LOGGEDIN) |
| test_wow_family.py | `lin` | 23 | | wf.lineage() |
| test_wow_player.py | `store` | 25 | | tmp_path |
| test_wow_world.py | `fx` | 24 | | load_fixture() |

(Scope per fixture is in `_s219_scan.json` records; 77 function / 10 module, 23 autouse, 20 yield-based.
0 fixtures construct unittest.mock objects - the estate's fixtures isolate paths/env, they do not mock.)

conftest.py (read in full, 84 lines) carries exactly one fixture and one module-level mock:
- `_isolate_gap_log` (autouse, function scope, tests/conftest.py:79-83): points MAG_GAPS_LOG at a tmp_path
  file so track_loop_gap pollution is structurally impossible (B2-336).
- tests/conftest.py:36-44 patches `subprocess.Popen` session-wide on win32 to OR in CREATE_NO_WINDOW by
  default (2026-09-28 headless law) - itself a mock of the stdlib at the choke point, call sites that pass
  their own creationflags still work. CAVEAT from the 07 run: this function wrapper is incompatible with
  mag/headless.py:72's Popen subclassing (§6 item 7) - three suite failures hang on it today.

## 10. Method, commands, caveats

Instruments (all banked in flash50/): `_s219_scan.py` (AST census: fixtures, mock classes, patch targets,
monkey methods, fake classes, data files), `_s219_xcheck.py` (byte-level marker grep cross-check),
`_s219_verify.py` + `_s219_worker.py` (import-alias rewrite of object targets; runtime resolution of all 527
unique targets in 18 subprocess batches of 30, CREATE_NO_WINDOW, 420s cap each; git last-touch map),
`_s219_lists.py`, `_s219_summary.py`, `_s219_sut.py/_s219_sut2.py/_s219_sut3.py` (SUT call-site greps),
`_s219_build.py` (this document). Raw evidence: `_s219_scan.json`, `_s219_verify.json`.

Key commands actually run: the scan; the byte-grep cross-check (MagicMock 0 lines/0 files, monkeypatch 2,082
lines/203 files, patch( 62 lines/15 files); 18/18 resolution batches ok (527 targets: 519 OK unique, 1
ATTR_MISSING, 7 grounding IMPORT_FAIL re-verified OK with scripts/ on path); `git log -S ollama_tags` on
mag/orchestrator.py and the test file (single commit d575bc168 2026-09-14 both sides); per-file pytest runs;
the full suite (§7).

Caveats, stated plainly:

- The Windows findstr/dir flag mangling in this harness forced python byte-greps instead of shell greps for
  the cross-check; the `patch(` substring count (62) includes 36 non-mock lines (`.dispatch(`, `apply_patch(`,
  test names) - the AST count 26 is the real one and the two reconcile exactly (62-36=26).
- 551 kind-slots dedupe to 527 unique targets (a target can be both string-form and object-form).
- Per-callsite signature equivalence for all 1,127 setattr lambdas was NOT statically proven; that is what
  the suite run is for. Existence was proven for 526/527; the 527th is deliberate (raising=False).
- tests/test_* defs (2,312) are a different denominator from pytest collected items (2,303 on 09-27 per
  AGENTS.md); parametrize and the land-rush since then make them incomparable by law B2-216. Not differenced.
- mag/agent_arena.py was grepped by mistake once (the module is mag/arena_adapter.py); corrected in round 2.

