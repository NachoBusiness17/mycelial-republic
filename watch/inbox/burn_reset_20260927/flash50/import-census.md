# s2-16: repo-wide Python import census (2026-09-28)

Census lane f2, item s2-16. Question: which external (non-stdlib) packages does this repo
actually use, are they covered by requirements.txt or the venv, and which are unused.

Every number below comes from a command run during this ask against
C:/Users/foste/Documents/projects/local_sovereign_agent on branch
mag/run-beta1-factory-build-audi-20260806T231709Z. Census moment: 2026-09-28, roughly
19:55 to 21:10 local (the tree is live and grew during the census, see section 10).
Primary instrument: AST walk of every readable .py outside .venv
(`_s2-16_census.py` in this directory, final version v4, full data in `_s2-16_data.json`),
cross-checked with `find`, `grep`, `rg 15.2.0`, `pip list --format=freeze`, and targeted
`.venv/Scripts/python.exe -c "import X"` probes. Four instrument iterations (v1-v4) were
needed; section 10 records what each got wrong and why the v4 numbers are the census.

## 1. Universe

- .py files walked (v4, outside .venv): 24,315. Cross-check: `find . -name "*.py" -not -path "./.venv/*" -not -path "*/__pycache__/*" | wc -l` = 24,263 at session start; the +52 delta is files landed by concurrent lanes during the session (mag/ alone went 1,034 to 1,037; a sibling census lane s2-15 dropped `_s2_15_census.py` in root mid-walk, which is also the one "read: No such file" entry in the parse-error list).
- .venv excluded from the code census as environment, not source: 23,249 .py files inside it (find).
- Unreadable directories: 364 to the walker (`os.walk` onerror), 366 to find. All are dangling junctions: 20 root-level `.pytest-*` dirs plus 344 `agents/pytest-*` dirs; `cmd /c dir /a agents\pytest-tmp` returns "File Not Found" (targets gone). No .py content is provable inside them; they are excluded, not silently dropped.
- Parse errors: 54 files (list in `_s2-16_data.json`). Classes: 5 intentionally-broken pytest tmp fixtures (`test_broken.py`), ~13 `mine/raw` foreign clones (exo, litellm e2e) with py2/modern-syntax mismatches, 6 vscode colorize fixtures, 3 `corpus/library/mod-playerbots` py2 print statements, 2+2 unicode-broken `train_ghost.py` copies, 2 `memory/working` template breakage, 1 draft, 1 phase3 sample, 1 vanished mid-walk. Zero parse errors in the runtime scope (mag, tools, tests, scripts, dashboard, dashboard-deploy, root).

Per-top-dir py counts (v4): mine 15,800; corpus 3,402; dist_audit 1,076; mag 1,037; _archaeology_out 951; watch 465; memory 387; tests 373; tools 190; scripts 145; agents 128; attic 105; then 24 more dirs under 105. This repo is overwhelmingly archive: mine+corpus+dist_audit+_archaeology_out alone are 21,229 of 24,315 py files (87.3 percent), before counting watch/, memory/, attic/ and the other mirror surfaces.

## 2. Import totals and classification

- Static import statements: 206,496. Import occurrences (multi-name lines count per name): 207,951. Relative imports (`from . import x`): 10,312.
- Distinct top-level import names: 1,168, classified with root-first precedence (stdlib > repo-root-local > installed-third-party > archive-local > unresolved):

| class | count | meaning |
|---|---|---|
| stdlib | 150 | in `sys.stdlib_module_names` (Python 3.11.15) |
| local-root | 25 | a py-bearing top-level dir or root .py stem with this name (mag, config, tools, main, tests, ...) |
| third-party | 125 | name provided by an installed distribution, not local |
| local-archive | 467 | name matches a py-bearing dir/stem somewhere in the archive trees (mine/, corpus/, ...) |
| unresolved | 401 | no local module anywhere and no installed provider; imports inside copied foreign code |

- Root-local usage leader: `mag` 14,022 occurrences (4,238 from runtime scope), `config` 2,898, `agents` 2,210, `models` 742, `tests` 591.
- Shadow collisions where BOTH a root-local module and an installed dist provide the name: exactly 2, `docs` and `tests` (repo wins at runtime from root; dist copies like python-barcode's own `tests` package are shadowed only inside their own trees).
- Stdlib-named local files/dirs: 29 names (json, os, queue, site, ...). Only two exist at repo root: `queue/` (no `__init__.py`, 0 top-level py) and `site/` (no `__init__.py`, 1 py). Both are namespace dirs, which do not preempt stdlib regular modules; the other 27 are archive-tree copies. No runtime shadowing found.

## 3. The 125 third-party import names

Runtime scope for this census = {repo root, mag/, tools/, tests/, scripts/, dashboard/, dashboard-deploy/} = 1,847 py files (detailed second pass `_s2_16_runtime_detail.py`). These are the surfaces the .venv actually executes.

30 of 125 names are imported from runtime scope:

| import name | occ runtime | files runtime | occ all scopes | dist(s) |
|---|---|---|---|---|
| pytest | 126 | 125 | 4,913 | pytest |
| reportlab | 64 | 11 | 105 | reportlab |
| yaml | 46 | 46 | 341 | PyYAML |
| numpy | 32 | 20 | 364 | numpy |
| PIL | 23 | 12 | 114 | pillow |
| psutil | 21 | 17 | 112 | psutil |
| requests | 9 | 9 | 322 | requests |
| fastapi | 8 | 4 | 2,059 | fastapi |
| matplotlib | 8 | 4 | 75 | matplotlib |
| httpx | 6 | 6 | 1,376 | httpx |
| torch | 6 | 4 | 652 | torch |
| pywinauto | 6 | 2 | 24 | pywinauto |
| langgraph | 3 | 2 | 37 | langgraph, langgraph-checkpoint, langgraph-prebuilt |
| pyperclip | 3 | 2 | 16 | pyperclip |
| faster_whisper | 3 | 2 | 10 | faster-whisper |
| langchain_ollama | 3 | 3 | 6 | langchain-ollama |
| discord | 3 | 2 | 3 | discord.py (and dead `discord` 2.3.2 also installed) |
| dotenv | 2 | 2 | 447 | python-dotenv |
| uvicorn | 2 | 2 | 108 | uvicorn |
| pypdf | 2 | 2 | 6 | pypdf |
| transformers | 1 | 1 | 149 | transformers |
| huggingface_hub | 1 | 1 | 32 | huggingface_hub |
| playwright | 1 | 1 | 21 | playwright |
| jsonschema | 1 | 1 | 16 | jsonschema |
| sounddevice | 1 | 1 | 10 | sounddevice |
| soundfile | 1 | 1 | 9 | soundfile |
| pytest_timeout | 1 | 1 | 4 | pytest-timeout |
| pyttsx3 | 1 | 1 | 4 | pyttsx3 |
| qrcode | 1 | 1 | 4 | qrcode |
| xdist | 1 | 1 | 1 | pytest-xdist |

The other 95 third-party names are imported ONLY from archive/mirror copies (occ_rt = 0). Heaviest: litellm 29,705 occurrences (all inside the mine/raw litellm clone importing itself), google 5,934, pydantic 2,257, openai 1,301, evennia 1,229, opentelemetry 1,197, typing_extensions 692, django 614, starlette 579, rich 538. Full 125-row table with dists is in section 3 of the raw data; notable dist mappings confirmed: yaml to PyYAML, PIL to pillow, dotenv to python-dotenv, winrt family to 16 winrt-* dists, zmq to pyzmq, dateutil to python-dateutil, bs4 to beautifulsoup4.

## 4. Guard status of runtime third-party imports

The detail pass classifies each import site as lexically guarded (inside a try with an ImportError/ModuleNotFoundError/Exception/bare handler) or not:

- Unguarded (works because the dist is installed): pytest (all 126, tests), reportlab (mag/pdf_layout.py:8), yaml (mag/arena_adapter.py:18, mag/arena_strategies.py:7, main.py:4441, dashboard/server.py:1083), numpy (mag/archetype_image.py:193), PIL (mag/archetype_image.py:274), requests (mag/x_oauth.py:44), fastapi (mag/api_server.py:29), httpx (mag/agent_cli.py:746), torch (mag/emergence_test.py:7), discord (mag/bones_adapter.py:50), langgraph (root graph.py:6), pywinauto (mag/grok_desktop.py:58), jsonschema (tools/policy_eval_schema_check.py:150), plus smaller sites.
- Guarded try/except: psutil 20 of 21, PIL 13 of 23, pywinauto 5 of 6, dotenv 2 of 2, pypdf 2 of 2, faster_whisper 1 of 3, langchain_ollama 2 of 3, matplotlib 4 of 8, uvicorn 1 of 2, and all single-occurrence audio/vision names (sounddevice mag/gab_seat.py:76, soundfile :77, pyttsx3 mag/tts.py:68, qrcode mag/ecosystem_surface.py:298, transformers mag/vast_launcher.py:387, playwright mag/browser_driver.py:115, pytest_timeout mag/test_runner.py:53, xdist tests/conftest.py:70, huggingface_hub mag/hf_space.py:398).
- Path-guarded (verified by reading the file, invisible to the try/except heuristic): sovereign_mirror at scripts/run_mirror_dashboard.py:35 sits in main() after the `_mirror_home()` scaffold probe (lines ~15-23) that returns early exit 0 "scaffold not found" when the external sovereign_mirror repo is absent.

### The 5 unresolved names imported from runtime scope

None is installed; none is local; none is an unguarded crash:

| name | runtime sites | guard | consequence |
|---|---|---|---|
| chess | 10 occ / 10 files: mag/agent_arena.py:23 plus scripts/_bfs_qxd1.py:4, _find_exd5.py:4, _find_from_qxd1.py:4, _find_full_line.py:4, _find_qxd1_prefix.py:4, _pick_line.py:4, _replay_chess_line.py:4, _search_opening.py:4, _test_suffix.py:4 | 1 of 10 guarded | mag/agent_arena.py:23 is UNGUARDED: any mag path importing agent_arena without chess installed raises ModuleNotFoundError. Matches the 7 "python-chess missing" skips f-15 recorded in the 09-28 full-suite run |
| textarena | 1 occ: mag/arena_adapter.py:27 | guarded (try/except ImportError, lines 25-31, degrades to _HAS_TEXTARENA=False) | arena probes silently disabled on this venv |
| PyPDF2 | 1 occ: scripts/pdf_triage.py:92 | guarded try/except in the extractor ladder | skipped when absent |
| pdfminer | 1 occ: scripts/pdf_triage.py:102 | guarded try/except | skipped when absent |
| sovereign_mirror | 1 occ: scripts/run_mirror_dashboard.py:35 | path-guarded, early exit 0 | script no-ops without the external scaffold |

## 5. requirements.txt verdicts (all 14 lines)

`requirements.txt` read this session: 14 requirement lines. Venv inventory: `.venv/Scripts/python.exe -m pip list --format=freeze` = 249 distributions, cross-checked against importlib.metadata.distributions() = 249. Venv python: 3.11.15.

| line | declared | installed | runtime AST evidence | verdict |
|---|---|---|---|---|
| 1 | langgraph>=0.2.0 | langgraph 1.2.10 | 3 occ / 2 files (root graph.py:6-7, state.py:6) | USED, declared, installed |
| 2 | langchain-core>=0.3.0 | langchain-core 1.5.3 | 0 runtime occ; 64 occ all inside mine/ archive copies | DECLARED+INSTALLED, no direct runtime import (pulled transitively by langchain-ollama at runtime) |
| 3 | langchain-ollama>=0.2.0 | langchain-ollama 1.1.0 | 3 occ / 3 files (root llm.py:96, mag/lattice_loop.py:269, tools/pupeteer_gauntlet.py:117) | USED |
| 4 | httpx>=0.27.0 | httpx 0.28.1 | 6 occ / 6 files (mag/agent_cli.py:746, mag/research_pack.py:64, tests/test_tool_dispatch_shape.py:159, tools/corpus_lens_run.py:21) | USED |
| 5 | reportlab>=4.0 | reportlab 5.0.0 | 64 occ / 11 files (mag/pdf_layout.py:8) | USED |
| 6 | matplotlib>=3.8 | matplotlib 3.11.1 | 8 occ / 4 files (mag/session_dossier.py:386, tools/curvature_scan.py:327) | USED |
| 7 | Pillow>=10.0 | pillow 12.2.0 | 23 occ / 12 files (dashboard/rest.py:4008, mag/archetype_image.py:249) | USED |
| 8 | fastapi>=0.110 | fastapi 0.141.1 | 8 occ / 4 files (mag/api_server.py:29, mag/ghost.py:1695) | USED |
| 9 | uvicorn>=0.27 | uvicorn 0.52.1 | 2 AST occ (mag/api_server.py:117, mag/ghost.py:1697) + project-owned `python -m uvicorn` at mag/api_server.py:19 and backend/provider_gateway.py:26 | USED |
| 10 | PyYAML>=6.0 | PyYAML 6.0.3 | 46 occ / 46 files | USED |
| 11 | pytest>=8.0 | pytest 9.1.1 | 126 occ / 125 files + `python -m pytest` in mag/system_map.py:124, mag/roadmap_runner.py:173, scripts/bootstrap_test_env.ps1:45, tools/pupeteer_gauntlet.py | USED |
| 12 | chess>=1.10 | NOT INSTALLED (`import chess` raises ModuleNotFoundError, probed) | 10 occ / 10 files, 9 unguarded | DECLARED BUT NOT INSTALLED; mag/agent_arena.py:23 unguarded import is live debt |
| 13 | textarena>=0.7.0 | NOT INSTALLED (probed) | 1 occ, guarded | DECLARED BUT NOT INSTALLED; harmless (guarded) |
| 14 | faster-whisper>=1.0.0 | faster-whisper 1.2.1 | 3 occ / 2 files (mag/space_ear.py:62, mag/voice_stt.py:35) | USED |

Score: 14 declared / 12 installed / 2 missing (chess, textarena) / 11 of 12 installed lines directly used at runtime / langchain-core the only installed-but-runtime-unimported declared line.

## 6. The venv: 249 installed, three-way usage split

Evidence per dist: any of its import names imported at runtime scope (AST), or invoked via project-owned `python -m` (shell line or Python list form), or present in runtime dynamic literals. After correction (litellm, debugpy, jupyter_core `-m` evidence lives only in archive files and was removed):

| bucket | count |
|---|---|
| runtime-used | 35 |
| archive-only (imported somewhere in the repo, zero runtime usage) | 108 |
| never imported anywhere in the repo (no AST, no dynamic, no -m) | 106 |

Runtime-used 35: pytest 9.1.1, reportlab 5.0.0, PyYAML 6.0.3, numpy 2.4.6, pillow 12.2.0, psutil 7.2.2, requests 2.34.2, fastapi 0.141.1, matplotlib 3.11.1, httpx 0.28.1, torch 2.13.0, pywinauto 0.6.9, discord.py 2.7.1 (+ dead `discord` 2.3.2 shares the import name), faster-whisper 1.2.1, langchain-ollama 1.1.0, langgraph 1.2.10, langgraph-checkpoint 4.1.1, langgraph-prebuilt 1.1.0, pyperclip 1.11.0, python-dotenv 1.2.2, pypdf 6.15.0, uvicorn 0.52.1, huggingface_hub 1.26.1, jsonschema 4.26.0, playwright 1.62.0, pytest-timeout 2.4.0, pytest-xdist 3.8.0, pyttsx3 2.99, qrcode 8.2, sounddevice 0.5.6, soundfile 0.14.0, transformers 5.15.0, twspace-dl 2024.7.2.1 (invoked, not imported: mag/space_ear.py:53 runs `[sys.executable, "-m", "twspace_dl", ...]`), pip 26.1.2 (env management). That is 14.1 percent of the venv doing 100 percent of the harness work.

Unused, leaf tier (nothing installed requires them, no import, no invocation, word-scan over the project-owned code surface found no use): a2a-cli 0.2, git-filter-repo 2.47.0 (one-time migration tool, kept installed), ractor-salon 0.1.0 (the fleet's own plugin; referenced as a standalone sibling repo at scripts/build_deck.py:344,430 and 100+ receipt mentions, never imported; f-15 recorded 5 test skips "ractor engine unbuilt"), vizdoom 1.3.0.

Unused, transitive tier (104 dists minus twspace-dl = 103; nothing imports them directly but another installed dist declares them): full list in `_s2-16_verdicts` data banked with the receipt. Notable names people might wrongly prune: black, isort, ipykernel, jupyter_client, onnxruntime, sentencepiece, ctranslate2, pygame-ce, six, tornado, attrs, pluggy (pluggy is pytest's own dependency; my criterion counts it unused-directly because nothing imports it in repo code, which is normal for it).

Archive-only 108: imported only by archive copies. Heaviest meaning: litellm, openai, google-api-core, google-auth, googleapis-common-protos, protobuf, pydantic, pydantic_core, pydantic-settings, evennia, opentelemetry-api, Django, starlette, anyio, aiohttp, websockets, langchain-core, ollama (the mag harness talks to Ollama over HTTP, not via the python client). Also the entire winrt-* OCR stack (16 dists), Twisted/autobahn (evennia's stack), boto3/botocore.

## 7. Used but NOT declared in requirements.txt (the real gap)

22 of the 35 runtime-used dists are absent from requirements.txt: numpy, psutil, requests, torch, pywinauto, discord.py, pyperclip, pypdf, python-dotenv, transformers, huggingface_hub, playwright, jsonschema, pytest-timeout, pytest-xdist, pyttsx3, qrcode, sounddevice, soundfile, twspace-dl, pip (tooling), plus the dead duplicate `discord` 2.3.2 which is installed and shadowing-paired with discord.py. requirements.txt covers 12 of the 14 real runtime dependencies; everything else the harness imports survived only because it happens to sit in the venv.

## 8. Invocation and dynamic-import surfaces (AST-invisible usage)

- Shell-form `python -m X` across 1,236 code-ext files (.py/.ps1/.psm1/.bat/.cmd/.sh): 33 distinct modules, top: pip 18, venv 16, mag 9, json 7, pytest 6, dynamo 5, fastchat 4, vllm 3, then 2-count and 1-count tail. Project-owned verification pass (excluding mine/corpus/dist_audit/_archaeology_out/attic/reference) confirmed real invocations only for: uvicorn (mag/api_server.py:19, backend/provider_gateway.py:26), pytest (mag/system_map.py:124, mag/roadmap_runner.py:173, scripts/bootstrap_test_env.ps1:45, scripts/census_patrol_daily.ps1:19, tools/pupeteer_gauntlet.py:517-527), pip (tools/pupeteer_gauntlet.py:519,527, watch/hermes_wings/src/mcp_serve.py:629). The rest of the 33 (dynamo, fastchat, vllm, sglang, aider, openhands, mcp_agent_cli...) are references inside archive copies or probe fixtures to tools that are NOT installed.
- Python list-form `[..., "-m", "X", ...]` (missed by the shell regex): mag 99, pytest 15, pip 15, blackboard 13, uvicorn 4, twspace_dl 2, plus noise words. This is how mag launches its own modules and how space_ear launches twspace_dl.
- Runtime dynamic literals (importlib.import_module / __import__ with constant string, runtime scope only): 15 distinct names, all stdlib or local except numpy (1 site): mag 36, os 17, datetime 12, json 10, pathlib 5, math 4, uuid 3, hashlib 3, dead_hand 2, dashboard 2, config 1, contextlib 1, io 1, sys 1, numpy 1.

## 9. Findings

1. chess is declared, not installed, and imported unguarded at mag/agent_arena.py:23 (plus 9 one-off scripts): the only live breakage in the runtime import graph. textarena is the same shape but guarded.
2. requirements.txt under-declares: 22 runtime-used dists missing, including torch, transformers, numpy, requests, python-dotenv, playwright, pytest-xdist/timeout. A fresh venv built from requirements.txt alone would fail on first `import requests`.
3. The venv is 14 percent exercised: 106 of 249 dists are never imported anywhere in the repo, 108 more only by archive clones. Disk-weight suspects for cleanup review: torch 2.13.0 IS runtime-used (mag/depin.py:324, mag/emergence_test.py:7), but ctranslate2 4.8.1, onnxruntime 1.28.0, sentencepiece 0.2.2, vizdoom 1.3.0, av 18.0.0, pygame-ce, gymnasium are never-imported.
4. langchain-core is the one declared-but-runtime-unimported line; langgraph itself is used from two ROOT-level files (graph.py:6, state.py:6), not from mag/.
5. Double-install hazard: both `discord` 2.3.2 (abandoned nameholding package) and `discord.py` 2.7.1 are installed and both claim the `discord` import name.
6. The census instrument itself needed 4 iterations; naive external-package scans on this repo are wrong twice over: root-only internal rules leak archive-sibling names into third-party (v1: 993 externals), and any-directory rules let mine/raw clone dirs named pytest/yaml swallow real packages (v2-v3 hid pytest/fastapi/langgraph/requests). An interim claim I made in-session that langgraph and fastapi were "imported nowhere" was WRONG and is corrected by v4 (langgraph: 3 runtime occ; fastapi: 8). Banked so the next census does not repeat it.

## 10. Method, instrument history, limits

Commands run this ask: `find` inventory (3 passes), `pip list --format=freeze`, AST scanner v1/v2/v3/v4 (banked as `_s2-16_census.py`, data `_s2-16_data.json`), runtime guard-detail pass (`_s2_16_runtime_detail.py`, data in temp), requirements parse, `python -c "import chess/textarena/reportlab"` probes, `rg` word-evidence passes (2 corrected attempts, final pattern regex-safe words only), `rg -m` invocation scans (shell-form and list-form), targeted `sed -n` reads of the 4 unresolved import sites, junction probe `cmd /c dir /a agents\pytest-tmp`, root shadow-dir probes (`__init__.py` checks for queue/ and site/).

Instrument history: v1 internal rule = root-only (external bucket polluted with 993 names including local scratch modules like api/app/auth). v2 = any-dir-basename rule (internal bucket 535) let py-less clone dirs named pytest/yaml (mine/raw phoenix, sapling, vscode-extension clones) shadow real packages: pytest, yaml, fastapi, langgraph, requests all misfiled internal and only 29 runtime externals surfaced. v3 = py-bearing-dir rule (internal 512, external 506) fixed most of it but pytest stayed shadowed via a py-bearing clone dir. v4 = root-first precedence, final: 150/25/125/467/401.

Limits, stated plainly:
- The tree grew during the census (24,263 at find time to 24,315 at v4); all counts are the v4 walk moment. Same-tree-same-moment law applies to any future comparison.
- Dynamic imports with computed strings, plugin entry-point loads, and sys.path tricks (conftest inserting dirs, which is how bare-name imports like m12_pairing or kvos_block resolve inside pytest) are invisible to the AST pass; the runtime-detail pass records literal-string dynamic sites only.
- "Unused" is evidence-scoped: no import, no literal dynamic import, no project-owned -m invocation, and no installed requirer. It cannot see usage from outside the repo (operator shells, scheduled tasks that were deleted, other machines).
- 364 dangling junction dirs could not be descended; nothing in them is counted.
- `python -m` counts inside archive trees were excluded from verdicts after verification; the raw counts remain in `_s2-16_data.json` (module_invocations).

Banked in this directory: `_s2-16_census.py` (scanner, rerunnable from repo root), `_s2-16_data.json` (full per-name data, 940,969 B), receipt `s2-16.md`, this report `import-census.md`.
