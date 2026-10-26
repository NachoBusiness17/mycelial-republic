# f-22: secrets-file census (2026-09-28)

Item: f-22. Scope: the ENTIRE working tree of the repo at `C:\Users\foste\Documents\projects\local_sovereign_agent` (os.walk, `/.git` excluded). Ask: scan for .env, .key, .pem, credentials.json, secrets.json; for each: git-tracked status, key NAMES only, last modified.

## Method (exact commands)

- Instrument: `watch/inbox/burn_reset_20260927/flash50/_f22_secrets_scan.py`, run with this repo's venv: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_f22_secrets_scan.py`
- Tracked set: `git ls-files -z` (NUL-separated, unquoted).
- Ignore attribution: one `git check-ignore -v -- <path>` call per untracked hit (exit 0 = ignored, rule in output; 1 = not ignored). Instrument v1 used batched `check-ignore -v -z --stdin` with a tab-splitting parser; with -z every field is NUL-separated, so every entry was dropped and all 133 rows were mislabeled NOT_IGNORED. Caught by direct single-path checks (`git check-ignore -v -- .env` returned `.gitignore:19:.env`), fixed to per-path calls before banking.
- Last commit per tracked hit: `git log -1 --format=%h %cI -- <path>`.
- Name-only law: env lines matched with regex `^(?:export )?NAME=` (name captured, rest discarded); JSON parsed and only key paths kept; pem/key files fingerprinted by `-----BEGIN X-----` marker text only. No secret VALUE is printed anywhere in this file.

## Headline numbers

- Working tree walked: 71097 directories, 3563077 files (git internals excluded).
- Secret-pattern files found: **135**
  - env: 103
  - json-secret: 6
  - key: 8
  - pem: 18
- Tracked in git: **2** (these should not be tracked)
- Untracked but gitignored: **133**
- Untracked and NOT ignored (would ride into any `git add -A`): **0**

## Tracked in git (2)

| path | cat | bytes | mtime | last commit | sha12 |
|---|---|---|---|---|---|
| `.env.example` | env | 347 | 2026-08-05 08:56:54 | eb07ad62e 2026-08-04T11:47:25-04:00 | cca99c01752d |
| `memory/tls/lan.key` | key | 1675 | 2026-08-14 12:41:41 | 799ddb6fe 2026-08-19T09:36:58-04:00 | d798d8c174ee |

## Untracked and NOT ignored (0) - the risky class

None. Every untracked hit is covered by a gitignore rule.

## Untracked but gitignored (133)

| path | cat | bytes | mtime | ignore rule |
|---|---|---|---|---|
| `.env` | env | 5941 | 2026-09-27 07:52:26 | .gitignore line 19 pattern <.env> |
| `agents/pytest-tmp-17932/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 14:31:31 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-17932/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 14:31:31 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-29352/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 12:46:40 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-29352/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 12:46:40 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-31568/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 14:30:54 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-31568/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 14:30:54 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-43872/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 12:50:53 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-43872/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 12:50:53 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-44560/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 13:30:56 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-44560/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 13:30:56 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-44744/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 17:58:54 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-44744/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 17:58:54 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-51272/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 14:30:04 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-51272/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 14:30:04 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-51488/test_load_token_missing_var_an0/empty.env` | env | 9 | 2026-09-28 13:30:36 | .gitignore line 203 pattern <agents/pytest-*/> |
| `agents/pytest-tmp-51488/test_load_token_reads_runtime_0/.env` | env | 95 | 2026-09-28 13:30:36 | .gitignore line 203 pattern <agents/pytest-*/> |
| `corpus/library/ms-agents-beginners/.env.example` | env | 2625 | 2026-09-04 11:48:32 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/ms-genai-beginners/.env.copy` | env | 1883 | 2026-09-04 11:49:29 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/openai-cookbook/examples/partners/AWS/controlled_agentic_commerce_with_agentcore_payments/.env.example` | env | 2100 | 2026-09-04 12:25:25 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/openai-cookbook/examples/voice_solutions/one_way_translation_using_realtime_api/.env.example` | env | 43 | 2026-09-04 12:30:43 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/openai-cookbook/examples/voice_solutions/realtime_translation_guide/browser-translation-demo/.env.example` | env | 128 | 2026-09-04 12:31:03 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/openai-cookbook/examples/voice_solutions/realtime_translation_guide/livekit-translation-demo/.env.example` | env | 114 | 2026-09-04 12:31:30 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/openai-cookbook/examples/voice_solutions/realtime_translation_guide/twilio-translation-demo/.env.example` | env | 186 | 2026-09-04 12:32:09 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/zcode-zai-org/repo/.env.development` | env | 90 | 2026-09-26 17:51:04 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/zcode-zai-org/repo/.env.example` | env | 1141 | 2026-09-26 17:51:04 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/zcode-zai-org/repo/.env.production` | env | 90 | 2026-09-26 17:51:04 | .gitignore line 197 pattern <corpus/library/> |
| `corpus/library/zcode-zai-org/repo/apps/zcode-cli/.env.template` | env | 22 | 2026-09-26 17:51:04 | .gitignore line 197 pattern <corpus/library/> |
| `memory/improve/sources/ponytail-2026-08-03/.env.example` | env | 108 | 2026-08-02 20:56:54 | .gitignore line 68 pattern <memory/improve/**> |
| `mine/raw/agent_bleeding_edge/AgentOps-AI/agentops/app/.env.example` | env | 2367 | 2026-08-05 20:33:40 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/AgentOps-AI/agentops/app/dashboard/.env.example` | env | 2877 | 2026-08-05 20:33:40 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/a2aproject/A2A/.github/super-linter.env` | env | 695 | 2026-08-05 20:33:56 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/app/.env.example` | env | 685 | 2026-08-05 20:35:03 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/examples/llamaindex-workflows-research-agent/.env.example` | env | 141 | 2026-08-05 20:35:07 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/cli-agent-starter-kit/.env.example` | env | 301 | 2026-08-05 20:35:07 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/demo-document-relevancy-experiment/.env.example` | env | 131 | 2026-08-05 20:35:07 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/experiments-quickstart/.env.example` | env | 294 | 2026-08-05 20:35:07 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/langchain-quickstart/.env.example` | env | 645 | 2026-08-05 20:35:07 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/phoenix-experiment-runner/.env.example` | env | 85 | 2026-08-05 20:35:07 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/packages/phoenix-mcp/.env.example` | env | 70 | 2026-08-05 20:35:08 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/scripts/analytics/.env.example` | env | 28 | 2026-08-05 20:35:08 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/tutorials/mcp/tracing_between_mcp_client_and_server/.env.example` | env | 151 | 2026-08-05 20:35:10 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/.env.example` | env | 271 | 2026-08-05 20:34:11 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/go/chunking-example/.env.example` | env | 187 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/agent-memory-full-example/.env.example` | env | 74 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/chunking-example/.env.example` | env | 187 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/claude-prompt-caching-example/.env.example` | env | 82 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/context-templates-example/.env.example` | env | 74 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/elevenlabs-zep-example/llm-proxy/.env.example` | env | 363 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/elevenlabs-zep-example/react-app/.env.example` | env | 282 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/user-summary-instructions-example/.env.example` | env | 74 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/zep-quickstart-dashboard/.env.example` | env | 74 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/typescript/chunking-example/.env.example` | env | 187 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/typescript/langgraph/.env.example` | env | 245 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/examples/typescript/zep-graph-visualization/.env.example` | env | 30 | 2026-08-05 20:34:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/integrations/ag2/python/.env.example` | env | 209 | 2026-08-05 20:34:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/integrations/livekit/python/examples/full-example/.env.example` | env | 203 | 2026-08-05 20:34:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/mcp/zep-mcp-server/.env.example` | env | 271 | 2026-08-05 20:34:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/getzep/zep/zep-eval-harness/.env.example` | env | 233 | 2026-08-05 20:34:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/examples/basic/mcp_basic_agent/.env.example` | env | 530 | 2026-08-05 20:34:01 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/examples/crewai/.env.example` | env | 25 | 2026-08-05 20:34:01 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/examples/langchain/.env.example` | env | 25 | 2026-08-05 20:34:01 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/letta-ai/letta/.env.example` | env | 862 | 2026-08-05 20:33:10 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/mem0ai/mem0/examples/mem0-demo/.env.example` | env | 66 | 2026-08-05 20:33:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/mem0ai/mem0/mem0-ts/src/oss/.env.example` | env | 881 | 2026-08-05 20:33:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/mem0ai/mem0/server/.env.example` | env | 1143 | 2026-08-05 20:33:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/mem0ai/mem0/server/dashboard/.env.example` | env | 115 | 2026-08-05 20:33:14 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/sweepai/sweep/sweep_chat/.env` | env | 224 | 2026-08-05 20:34:19 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/Aider-AI/aider/aider/website/assets/sample.env` | env | 14123 | 2026-08-05 20:28:08 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/BerriAI/litellm/.env.example` | env | 655 | 2026-08-05 20:28:18 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/BerriAI/litellm/docker/.env.example` | env | 558 | 2026-08-05 20:28:18 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/BerriAI/litellm/ui/litellm-dashboard/.env.development` | env | 45 | 2026-08-05 20:28:24 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/BerriAI/litellm/ui/litellm-dashboard/.env.production` | env | 19 | 2026-08-05 20:28:24 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/OpenHands/OpenHands/.env.sample` | env | 2984 | 2026-08-05 20:27:55 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/OpenHands/OpenHands/examples/acp-docker/.env.example` | env | 1432 | 2026-08-05 20:27:55 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/SWE-agent/SWE-agent/.env.example` | env | 330 | 2026-08-05 20:28:01 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/alamops/agetor/.env.example` | env | 2036 | 2026-08-05 20:38:09 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/anomalyco/opencode/packages/slack/.env.example` | env | 114 | 2026-08-05 20:38:03 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/cline/cline/apps/vscode/.env.example` | env | 5535 | 2026-08-05 20:38:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/cline/kanban/web-ui/.env.example` | env | 176 | 2026-08-05 20:38:20 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/continuedev/continue/extensions/cli/.env.example` | env | 241 | 2026-08-05 20:28:46 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/continuedev/continue/packages/continue-sdk/typescript/.env.example` | env | 19 | 2026-08-05 20:28:47 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/emdgroup/maestro/.github/scripts/macos/.env.example` | env | 1207 | 2026-08-05 20:38:34 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/google/adk-python/contributing/samples/integrations/authn-adk-all-in-one/adk_agents/sample.env` | env | 179 | 2026-08-05 20:39:30 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/google/adk-python/contributing/samples/integrations/authn-adk-all-in-one/idp/sample.env` | env | 604 | 2026-08-05 20:39:30 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/google/adk-python/tests/integration/.env.example` | env | 321 | 2026-08-05 20:39:32 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/mifunedev/openharness/.devcontainer/.example.env` | env | 7185 | 2026-08-05 20:38:21 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/mifunedev/openharness/.oh/templates/.devcontainer/.example.env` | env | 138 | 2026-08-05 20:38:21 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/modelcontextprotocol/python-sdk/examples/clients/simple-chatbot/mcp_simple_chatbot/.env.example` | env | 28 | 2026-08-05 20:28:27 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/mesh_comm/permissionlesstech/bitchat-android/tools/arti-build/TOOLCHAIN.env` | env | 365 | 2026-08-05 08:57:05 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/mesh_comm/permissionlesstech/bitchat-android/tools/reproducible-builds/TOOLCHAIN.env` | env | 714 | 2026-08-05 08:57:05 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/narrative_corpus/twinejs/.env` | env | 72 | 2026-08-06 23:57:41 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/steal_protocol/arvarik/bmas/.env.example` | env | 2801 | 2026-08-05 19:04:34 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/steal_protocol/claudioed/agent-blackboard/.env.example` | env | 1787 | 2026-08-05 19:04:51 | .gitignore line 44 pattern <mine/raw/**> |
| `reference/gstdcoin/ai/.env.example` | env | 3399 | 2026-08-05 08:57:23 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `reference/gstdcoin/ai/frontend/.env.example` | env | 1062 | 2026-08-05 08:57:23 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `reference/gstdcoin/ai/scripts/.env.example` | env | 1117 | 2026-08-05 08:57:23 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `reference/gstdcoin/contracts/.env.example` | env | 1330 | 2026-08-05 08:57:30 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `reference/gstdcoin/gstd-bridge/.env.example` | env | 2055 | 2026-08-05 08:57:27 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `reference/gstdcoin/gstdbot/.env.example` | env | 4171 | 2026-08-05 08:57:28 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `reference/gstdcoin/web/.env.example` | env | 421 | 2026-08-05 08:57:25 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `reference/gstdcoin/web/.env.production` | env | 693 | 2026-08-05 08:57:25 | .gitignore line 159 pattern <reference/gstdcoin/> |
| `state/auth_switchboard/20260905T161520Z_post_swap_broken_20260905/credentials.json` | json-secret | 14372 | 2026-09-05 12:15:20 | .gitignore line 30 pattern <state/> |
| `state/auth_switchboard/20260905T161700Z_post_swap_broken_20260905/credentials.json` | json-secret | 14372 | 2026-09-05 12:17:00 | .gitignore line 30 pattern <state/> |
| `state/auth_switchboard/20260905T162449Z_dogfood_a/credentials.json` | json-secret | 14372 | 2026-09-05 12:24:49 | .gitignore line 30 pattern <state/> |
| `state/auth_switchboard/20260905T162449Z_dogfood_b/credentials.json` | json-secret | 14372 | 2026-09-05 12:24:49 | .gitignore line 30 pattern <state/> |
| `state/auth_switchboard/20260907T082019Z_pre_apikey_swap_20260907/credentials.json` | json-secret | 14372 | 2026-09-07 04:20:19 | .gitignore line 30 pattern <state/> |
| `state/auth_switchboard/20260907T083251Z_known_good/credentials.json` | json-secret | 14372 | 2026-09-07 04:32:51 | .gitignore line 30 pattern <state/> |
| `.venv/Lib/site-packages/tornado/test/test.key` | key | 1736 | 2026-08-12 09:23:04 | .gitignore line 1 pattern <.venv/> |
| `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/client0.key` | key | 1732 | 2026-08-05 20:30:12 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/client1.key` | key | 1732 | 2026-08-05 20:30:12 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/client2.key` | key | 1732 | 2026-08-05 20:30:12 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/localhost.key` | key | 1732 | 2026-08-05 20:30:12 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/proxy.key` | key | 1736 | 2026-08-05 20:30:12 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/root-ca.key` | key | 1732 | 2026-08-05 20:30:12 | .gitignore line 44 pattern <mine/raw/**> |
| `.venv/Lib/site-packages/borb/license/public_keys/public_key_001.pem` | pem | 451 | 2026-08-17 21:03:02 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/botocore/cacert.pem` | pem | 259837 | 2026-08-27 13:45:16 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/certifi/cacert.pem` | pem | 240216 | 2026-07-31 11:58:38 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/litellm/proxy/auth/public_key.pem` | pem | 458 | 2026-08-27 13:45:53 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/pip/_vendor/certifi/cacert.pem` | pem | 272441 | 2026-07-20 07:42:01 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/chain.pem` | pem | 2886 | 2026-09-23 03:16:34 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/thing1.pem` | pem | 1573 | 2026-09-23 03:16:34 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/thing2-duplicate.pem` | pem | 1415 | 2026-09-23 03:16:34 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/thing2.pem` | pem | 1415 | 2026-09-23 03:16:34 | .gitignore line 1 pattern <.venv/> |
| `.venv/Lib/site-packages/twisted/test/server.pem` | pem | 5360 | 2026-09-23 03:16:34 | .gitignore line 1 pattern <.venv/> |
| `mine/raw/agent_bleeding_edge/letta-ai/letta/certs/localhost-key.pem` | pem | 1736 | 2026-08-05 20:33:11 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_bleeding_edge/letta-ai/letta/certs/localhost.pem` | pem | 1632 | 2026-08-05 20:33:11 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/auth/public_key.pem` | pem | 458 | 2026-08-05 20:28:21 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/cert1.pem` | pem | 1340 | 2026-08-05 20:30:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/cert2.pem` | pem | 1340 | 2026-08-05 20:30:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/combined.pem` | pem | 4424 | 2026-08-05 20:30:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/not_a_cert.pem` | pem | 1744 | 2026-08-05 20:30:13 | .gitignore line 44 pattern <mine/raw/**> |
| `mine/raw/agent_platform/facebook/sapling/eden/scm/sapling/dummycert.pem` | pem | 2302 | 2026-08-05 20:30:14 | .gitignore line 44 pattern <mine/raw/**> |

## Per-file key names (names only, never values)

### `.env`

- category: env | bytes: 5941 | mtime: 2026-09-27 07:52:26 | tracked: no | sha256[:12]: 32b93b4bb73e
- gitignore: .gitignore line 19 pattern <.env>
- key names (52 of 55 non-comment lines matched): XAI_SD_API_KEY, DEEPSEEK_API_KEY, VASTAI_API_KEY, NVIDIABuild, NVIDIABuild2, VERCEL_KEY, ZAI_API_KEY, ZAI_API_KEY_2, ZAI_API_KEY_3, ZAI_API_KEY_Pro, ZAI_API_KEY_Lite, HERMES_API_KEY_1, HERMES_API_KEY_2, MAPBOX_TOKEN, OPENCODE, OPENCODE2, OPENROUTER_API_KEY, OPENROUTER_API_KEY_2, OPENROUTER_MODEL, OPENAI_API_KEY, ANTHROPIC_API_KEY, ANTHROPIC_API_KEY_2, GROQ_API_KEY, GROQ_API_KEY_2, GEMINI_API_KEY, GOOGLE_API_KEY, TOGETHER_API_KEY, TOGETHER_API_KEY2, COHERE_API_KEY_FREE, COHERE_API_KEY_PAID, CEREBAS_API_KEY, CEREBAS_API_KEY2, MISTRAL_API_KEY, MISTRAL_API_KEY_2, CURSOR_API_KEY, NOTION_API_KEY, GROK_API_KEY, GROK_API_KEY_2, OLLAMA_HOST, MAG_DRAINER, MAG_DRAINER_FORCE, X_ConsumerKey, X_SecretKey, X_BearerToken, X_ClientID, X_ClientSecret, X_REDIRECT_URI, GHOST_X_HANDLE, AOS_AGENT_MODEL, OPENCLAW_GATEWAY_TOKEN, OPENCLAW_GATEWAY_PASSWORD, ANTHROPIC_WORKSPACE_ID
- non-comment lines with no `=` or `:` delimiter (no key extractable): 1

### `.env.example`

- category: env | bytes: 347 | mtime: 2026-08-05 08:56:54 | tracked: YES | sha256[:12]: cca99c01752d
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (13 of 13 non-comment lines matched): XAI_API_KEY, XAI_MODEL, OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GROQ_API_KEY, DEEPSEEK_API_KEY, DEEPSEEK_OVERMIND_API_KEY, GEMINI_API_KEY, TOGETHER_API_KEY, VAST_API_KEY, VAST_OPENAI_BASE_URL, VAST_OPENAI_API_KEY

### `agents/pytest-tmp-17932/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 14:31:31 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-17932/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 14:31:31 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `agents/pytest-tmp-29352/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 12:46:40 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-29352/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 12:46:40 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `agents/pytest-tmp-31568/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 14:30:54 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-31568/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 14:30:54 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `agents/pytest-tmp-43872/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 12:50:53 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-43872/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 12:50:53 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `agents/pytest-tmp-44560/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 13:30:56 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-44560/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 13:30:56 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `agents/pytest-tmp-44744/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 17:58:54 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-44744/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 17:58:54 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `agents/pytest-tmp-51272/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 14:30:04 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-51272/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 14:30:04 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `agents/pytest-tmp-51488/test_load_token_missing_var_an0/empty.env`

- category: env | bytes: 9 | mtime: 2026-09-28 13:30:36 | tracked: no | sha256[:12]: d13f4a8aaeef
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (1 of 1 non-comment lines matched): OTHER

### `agents/pytest-tmp-51488/test_load_token_reads_runtime_0/.env`

- category: env | bytes: 95 | mtime: 2026-09-28 13:30:36 | tracked: no | sha256[:12]: 5578a375c9be
- gitignore: .gitignore line 203 pattern <agents/pytest-*/>
- notes: under a test path, fixture candidate
- key names (2 of 2 non-comment lines matched): OTHER, DISCORD_BOT_TOKEN
- commented-out name candidates (1, names only, first 60): DISCORD_BOT_TOKEN

### `corpus/library/ms-agents-beginners/.env.example`

- category: env | bytes: 2625 | mtime: 2026-09-04 11:48:32 | tracked: no | sha256[:12]: 08e297241c81
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (17 of 17 non-comment lines matched): AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_MODEL_DEPLOYMENT_NAME, AZURE_AI_SMALL_MODEL, AZURE_AI_LARGE_MODEL, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME, AZURE_SEARCH_SERVICE_ENDPOINT, AZURE_SEARCH_API_KEY, BING_CONNECTION_ID, MINIMAX_API_KEY, MINIMAX_BASE_URL, MINIMAX_MODEL_ID, NOVITA_API_KEY, NOVITA_BASE_URL, NOVITA_MODEL_ID

### `corpus/library/ms-genai-beginners/.env.copy`

- category: env | bytes: 1883 | mtime: 2026-09-04 11:49:29 | tracked: no | sha256[:12]: fb0368eca466
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: inside a harvested-notes tree, provenance unverified until read
- key names (10 of 10 non-comment lines matched): OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT, AZURE_INFERENCE_ENDPOINT, AZURE_INFERENCE_CREDENTIAL, AZURE_INFERENCE_CHAT_MODEL, HUGGING_FACE_API_KEY

### `corpus/library/openai-cookbook/examples/partners/AWS/controlled_agentic_commerce_with_agentcore_payments/.env.example`

- category: env | bytes: 2100 | mtime: 2026-09-04 12:25:25 | tracked: no | sha256[:12]: a516fc55a373
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (25 of 25 non-comment lines matched): ALLOW_AGENTCORE_TESTNET, ALLOW_AGENTCORE_READ_ONLY, RUN_AGENTCORE_E2E, ALLOW_PAID_INFERENCE, APPROVE_AGENTCORE_TESTNET_PURCHASE, ALLOW_AGENTCORE_SESSION_ADMIN, AGENTCORE_SESSION_FILE, BEDROCK_AWS_PROFILE, AGENTCORE_SESSION_AWS_PROFILE, AGENTCORE_RUNTIME_AWS_PROFILE, AGENTCORE_AWS_REGION, PAYMENT_MANAGER_ARN, PAYMENT_CONNECTOR_ID, PAYMENT_INSTRUMENT_ID, PAYMENT_SESSION_ID, PAYMENT_USER_ID, X402_ALLOWED_MERCHANTS, X402_NETWORK_PREFERENCES, X402_APPROVED_ASSET, X402_APPROVED_PAY_TO, X402_MAX_CHALLENGE_TIMEOUT_SECONDS, X402_MAX_APPROVED_AMOUNT_ATOMIC, X402_MAX_PAYMENT_ATTEMPTS, X402_RESOURCE_URL, X402_IDEMPOTENCY_KEY

### `corpus/library/openai-cookbook/examples/voice_solutions/one_way_translation_using_realtime_api/.env.example`

- category: env | bytes: 43 | mtime: 2026-09-04 12:30:43 | tracked: no | sha256[:12]: f524efb13f05
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (1 of 1 non-comment lines matched): REACT_APP_OPENAI_API_KEY

### `corpus/library/openai-cookbook/examples/voice_solutions/realtime_translation_guide/browser-translation-demo/.env.example`

- category: env | bytes: 128 | mtime: 2026-09-04 12:31:03 | tracked: no | sha256[:12]: 520323804e40
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (4 of 4 non-comment lines matched): OPENAI_API_KEY, OPENAI_TRANSLATION_MODEL, OPENAI_INPUT_TRANSCRIPTION_MODEL, PORT

### `corpus/library/openai-cookbook/examples/voice_solutions/realtime_translation_guide/livekit-translation-demo/.env.example`

- category: env | bytes: 114 | mtime: 2026-09-04 12:31:30 | tracked: no | sha256[:12]: a66a105ad70d
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (5 of 5 non-comment lines matched): LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL, OPENAI_API_KEY, OPENAI_TRANSLATION_MODEL

### `corpus/library/openai-cookbook/examples/voice_solutions/realtime_translation_guide/twilio-translation-demo/.env.example`

- category: env | bytes: 186 | mtime: 2026-09-04 12:32:09 | tracked: no | sha256[:12]: 0ad88137d3dd
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (7 of 7 non-comment lines matched): OPENAI_API_KEY, PUBLIC_URL, PORT, OPENAI_TRANSLATION_MODEL, TWILIO_AUTH_TOKEN, ALLOWED_CALLER_NUMBERS, MAX_ACTIVE_CALLERS

### `corpus/library/zcode-zai-org/repo/.env.development`

- category: env | bytes: 90 | mtime: 2026-09-26 17:51:04 | tracked: no | sha256[:12]: 5be810808e48
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: inside a harvested-notes tree, provenance unverified until read
- every line is blank or a comment; no active keys. Commented-out name candidates: 0

### `corpus/library/zcode-zai-org/repo/.env.example`

- category: env | bytes: 1141 | mtime: 2026-09-26 17:51:04 | tracked: no | sha256[:12]: 11b0afea2670
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (12 of 12 non-comment lines matched): ZCODE_BASE_URL, BIGMODEL_API_BASE_URL, ZAI_OAUTH_ORIGIN, ZAI_BUSINESS_BASE_URL, ZAI_OAUTH_CLIENT_ID, ZCODE_CDN_BASE_URL, ZCODE_CONVERSATION_SHARE_WEB_URL, ZCODE_REMOTE_ASSET_CDN_BASE_URL, ZCODE_BUILTIN_PROVIDER_CONFIG_FILE, ZCODE_DEPS_BASE_URL, INTRANET_MACHINE_HOST, ZCODE_DIST_BASE_URL

### `corpus/library/zcode-zai-org/repo/.env.production`

- category: env | bytes: 90 | mtime: 2026-09-26 17:51:04 | tracked: no | sha256[:12]: 5ddde5212b45
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: inside a harvested-notes tree, provenance unverified until read
- every line is blank or a comment; no active keys. Commented-out name candidates: 0

### `corpus/library/zcode-zai-org/repo/apps/zcode-cli/.env.template`

- category: env | bytes: 22 | mtime: 2026-09-26 17:51:04 | tracked: no | sha256[:12]: 7c3b1c38906d
- gitignore: .gitignore line 197 pattern <corpus/library/>
- notes: template/example filename, expected to hold placeholders not live secrets; inside a harvested-notes tree, provenance unverified until read
- key names (1 of 1 non-comment lines matched): BIGMODEL_API_KEY

### `memory/improve/sources/ponytail-2026-08-03/.env.example`

- category: env | bytes: 108 | mtime: 2026-08-02 20:56:54 | tracked: no | sha256[:12]: 4c3a8323d522
- gitignore: .gitignore line 68 pattern <memory/improve/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): ANTHROPIC_API_KEY

### `mine/raw/agent_bleeding_edge/AgentOps-AI/agentops/app/.env.example`

- category: env | bytes: 2367 | mtime: 2026-08-05 20:33:40 | tracked: no | sha256[:12]: 3480fe3a96e1
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (51 of 51 non-comment lines matched): NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_PROJECT_ID, NEXT_PUBLIC_API_URL, NEXT_PUBLIC_APP_URL, NEXT_PUBLIC_SITE_URL, NEXT_PUBLIC_ENVIRONMENT_TYPE, NEXT_PUBLIC_PLAYGROUND, NEXT_PUBLIC_POSTHOG_KEY, NEXT_PUBLIC_POSTHOG_HOST, NEXT_PUBLIC_SENTRY_DSN, NEXT_PUBLIC_SENTRY_ORG, NEXT_PUBLIC_SENTRY_PROJECT, NEXT_PUBLIC_SENTRY_ENVIRONMENT, NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY, NEXT_STRIPE_SECRET_KEY, NEXT_STRIPE_WEBHOOK_SECRET, PROTOCOL, API_DOMAIN, APP_DOMAIN, ENVIRONMENT, SQLALCHEMY_LOG_LEVEL, JWT_SECRET_KEY, SUPABASE_URL, SUPABASE_KEY, SUPABASE_MAX_POOL_SIZE, SUPABASE_HOST, SUPABASE_PORT, SUPABASE_DATABASE, SUPABASE_USER, SUPABASE_PASSWORD, SUPABASE_S3_BUCKET, SUPABASE_S3_LOGS_BUCKET, SUPABASE_S3_ACCESS_KEY_ID, SUPABASE_S3_SECRET_ACCESS_KEY, CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD, CLICKHOUSE_DATABASE, CLICKHOUSE_SECURE, CLICKHOUSE_ENDPOINT, CLICKHOUSE_USERNAME, STRIPE_SECRET_KEY, STRIPE_SUBSCRIPTION_PRICE_ID, STRIPE_TOKEN_PRICE_ID, STRIPE_SPAN_PRICE_ID, REDIS_HOST, REDIS_PORT, DEMO_ORG_ID
- commented-out name candidates (5, names only, first 60): CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_SECURE, CLICKHOUSE_PASSWORD, STRIPE_WEBHOOK_SECRET

### `mine/raw/agent_bleeding_edge/AgentOps-AI/agentops/app/dashboard/.env.example`

- category: env | bytes: 2877 | mtime: 2026-08-05 20:33:40 | tracked: no | sha256[:12]: b2bf4b5a16dd
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (20 of 20 non-comment lines matched): NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_PROJECT_ID, NEXT_PUBLIC_API_URL, NEXT_PUBLIC_APP_URL, NEXT_PUBLIC_SITE_URL, NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, NEXT_PUBLIC_POSTHOG_KEY, NEXT_PUBLIC_POSTHOG_HOST, NEXT_PUBLIC_SENTRY_DSN, NEXT_PUBLIC_SENTRY_ORG, NEXT_PUBLIC_SENTRY_PROJECT, NEXT_PUBLIC_SENTRY_ENVIRONMENT, NEXT_PUBLIC_SIGNIN_METHODS, NEXT_PUBLIC_ENVIRONMENT_TYPE, NEXT_PUBLIC_PLAYGROUND, NEXT_PUBLIC_FALLBACK_API_KEY
- commented-out name candidates (6, names only, first 60): NEXT_PUBLIC_API_URL, NEXT_PUBLIC_APP_URL, NEXT_PUBLIC_SITE_URL, NEXT_PUBLIC_ENVIRONMENT_TYPE, NEXT_PUBLIC_PLAYGROUND, NEXT_PUBLIC_SENTRY_ENVIRONMENT

### `mine/raw/agent_bleeding_edge/a2aproject/A2A/.github/super-linter.env`

- category: env | bytes: 695 | mtime: 2026-08-05 20:33:56 | tracked: no | sha256[:12]: 133e20562763
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (22 of 22 non-comment lines matched): SHELLCHECK_OPTS, VALIDATE_ALL_CODEBASE, FILTER_REGEX_EXCLUDE, VALIDATE_BASH, VALIDATE_BASH_EXEC, VALIDATE_CSS, VALIDATE_EDITORCONFIG, VALIDATE_GIT_MERGE_CONFLICT_MARKERS, VALIDATE_GITHUB_ACTIONS, VALIDATE_GITLEAKS, VALIDATE_JSCPD, VALIDATE_JSON, VALIDATE_MARKDOWN, VALIDATE_PROTOBUF, VALIDATE_PYTHON_RUFF, VALIDATE_SHELL_SHFMT, VALIDATE_TOML, VALIDATE_TYPESCRIPT_ES, VALIDATE_YAML, TYPESCRIPT_ES_CONFIG_FILE, MARKDOWN_CONFIG_FILE, PROTOBUF_CONFIG_FILE

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/app/.env.example`

- category: env | bytes: 685 | mtime: 2026-08-05 20:35:03 | tracked: no | sha256[:12]: 487a625f3346
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (10 of 10 non-comment lines matched): PHOENIX_SECRET, PHOENIX_ENABLE_AUTH, PHOENIX_SMTP_HOSTNAME, PHOENIX_SMTP_PORT, PHOENIX_SMTP_USERNAME, PHOENIX_SMTP_PASSWORD, PHOENIX_TELEMETRY_ENABLED, PHOENIX_AGENTS_COLLECTOR_ENDPOINT, PHOENIX_AGENTS_COLLECTOR_API_KEY, PHOENIX_AGENTS_ASSISTANT_PROJECT_NAME
- commented-out name candidates (1, names only, first 60): VITE_DEBUG_RELAY

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/examples/llamaindex-workflows-research-agent/.env.example`

- category: env | bytes: 141 | mtime: 2026-08-05 20:35:07 | tracked: no | sha256[:12]: 27cc162b932f
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (4 of 4 non-comment lines matched): OPENAI_API_KEY, TAVILY_API_KEY, PHOENIX_CLIENT_HEADERS, PHOENIX_COLLECTOR_ENDPOINT

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/cli-agent-starter-kit/.env.example`

- category: env | bytes: 301 | mtime: 2026-08-05 20:35:07 | tracked: no | sha256[:12]: 55ea7d22d810
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): ANTHROPIC_API_KEY
- commented-out name candidates (3, names only, first 60): PHOENIX_COLLECTOR_ENDPOINT, PHOENIX_COLLECTOR_ENDPOINT, PHOENIX_API_KEY

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/demo-document-relevancy-experiment/.env.example`

- category: env | bytes: 131 | mtime: 2026-08-05 20:35:07 | tracked: no | sha256[:12]: 11397b59e37e
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): OPENAI_API_KEY, PHOENIX_HOST, PHOENIX_API_KEY

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/experiments-quickstart/.env.example`

- category: env | bytes: 294 | mtime: 2026-08-05 20:35:07 | tracked: no | sha256[:12]: c60ffb7006af
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): OPENAI_API_KEY, PHOENIX_API_KEY, PHOENIX_HOST

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/langchain-quickstart/.env.example`

- category: env | bytes: 645 | mtime: 2026-08-05 20:35:07 | tracked: no | sha256[:12]: ba7b9b9d10b7
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (5 of 5 non-comment lines matched): OPENAI_API_KEY, TAVILY_API_KEY, FIREWORKS_API_KEY, PHOENIX_ENDPOINT, PHOENIX_PROJECT_NAME

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/examples/apps/phoenix-experiment-runner/.env.example`

- category: env | bytes: 85 | mtime: 2026-08-05 20:35:07 | tracked: no | sha256[:12]: 83cef547f38c
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): OPENAI_API_KEY, OPENAI_API_BASE_URL, OPENAI_MODEL

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/js/packages/phoenix-mcp/.env.example`

- category: env | bytes: 70 | mtime: 2026-08-05 20:35:08 | tracked: no | sha256[:12]: 8c0c51aac042
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): PHOENIX_BASE_URL, PHOENIX_API_KEY

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/scripts/analytics/.env.example`

- category: env | bytes: 28 | mtime: 2026-08-05 20:35:08 | tracked: no | sha256[:12]: bdc31b13e5d1
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): GITHUB_TOKEN

### `mine/raw/agent_bleeding_edge/arize-ai/phoenix/tutorials/mcp/tracing_between_mcp_client_and_server/.env.example`

- category: env | bytes: 151 | mtime: 2026-08-05 20:35:10 | tracked: no | sha256[:12]: f0298a0643c1
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): OPENAI_API_KEY, PHOENIX_COLLECTOR_ENDPOINT, PHOENIX_CLIENT_HEADERS

### `mine/raw/agent_bleeding_edge/getzep/zep/.env.example`

- category: env | bytes: 271 | mtime: 2026-08-05 20:34:11 | tracked: no | sha256[:12]: fdfe0f2b6e28
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, LOG_LEVEL

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/go/chunking-example/.env.example`

- category: env | bytes: 187 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: bcd45eeb7079
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/agent-memory-full-example/.env.example`

- category: env | bytes: 74 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: 2dbd41cc3a88
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/chunking-example/.env.example`

- category: env | bytes: 187 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: bcd45eeb7079
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/claude-prompt-caching-example/.env.example`

- category: env | bytes: 82 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: 1b9f9d3ba1f2
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, ANTHROPIC_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/context-templates-example/.env.example`

- category: env | bytes: 74 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: 2dbd41cc3a88
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/elevenlabs-zep-example/llm-proxy/.env.example`

- category: env | bytes: 363 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: f237ae9d5319
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY, PROXY_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/elevenlabs-zep-example/react-app/.env.example`

- category: env | bytes: 282 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: 486c60d9c931
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): VITE_ELEVENLABS_AGENT_ID
- commented-out name candidates (1, names only, first 60): VITE_PROXY_URL

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/user-summary-instructions-example/.env.example`

- category: env | bytes: 74 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: 2dbd41cc3a88
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/python/zep-quickstart-dashboard/.env.example`

- category: env | bytes: 74 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: 2dbd41cc3a88
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/typescript/chunking-example/.env.example`

- category: env | bytes: 187 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: bcd45eeb7079
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/typescript/langgraph/.env.example`

- category: env | bytes: 245 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: e1c2c6cdeabc
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): OPENAI_API_KEY, TAVILY_API_KEY, ZEP_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/examples/typescript/zep-graph-visualization/.env.example`

- category: env | bytes: 30 | mtime: 2026-08-05 20:34:13 | tracked: no | sha256[:12]: 521e33ff13fc
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): ZEP_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/integrations/ag2/python/.env.example`

- category: env | bytes: 209 | mtime: 2026-08-05 20:34:14 | tracked: no | sha256[:12]: a5cdd6d72d3a
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/getzep/zep/integrations/livekit/python/examples/full-example/.env.example`

- category: env | bytes: 203 | mtime: 2026-08-05 20:34:14 | tracked: no | sha256[:12]: cbc9fc86ff79
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (5 of 5 non-comment lines matched): ZEP_API_KEY, OPENAI_API_KEY, LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET

### `mine/raw/agent_bleeding_edge/getzep/zep/mcp/zep-mcp-server/.env.example`

- category: env | bytes: 271 | mtime: 2026-08-05 20:34:14 | tracked: no | sha256[:12]: fdfe0f2b6e28
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, LOG_LEVEL

### `mine/raw/agent_bleeding_edge/getzep/zep/zep-eval-harness/.env.example`

- category: env | bytes: 233 | mtime: 2026-08-05 20:34:14 | tracked: no | sha256[:12]: 379ab07b6a9b
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): ZEP_API_KEY, GOOGLE_API_KEY

### `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/examples/basic/mcp_basic_agent/.env.example`

- category: env | bytes: 530 | mtime: 2026-08-05 20:34:01 | tracked: no | sha256[:12]: 0b541c87b168
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): OPENAI_API_KEY, ANTHROPIC_API_KEY

### `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/examples/crewai/.env.example`

- category: env | bytes: 25 | mtime: 2026-08-05 20:34:01 | tracked: no | sha256[:12]: eb1236951b8c
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): SERPER_API_KEY

### `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/examples/langchain/.env.example`

- category: env | bytes: 25 | mtime: 2026-08-05 20:34:01 | tracked: no | sha256[:12]: eb1236951b8c
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): SERPER_API_KEY

### `mine/raw/agent_bleeding_edge/letta-ai/letta/.env.example`

- category: env | bytes: 862 | mtime: 2026-08-05 20:33:10 | tracked: no | sha256[:12]: 955dff9e9989
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (0 of 6 non-comment lines matched): (none)
- commented-out name candidates (3, names only, first 60): OPENAI_API_KEY, OLLAMA_BASE_URL, VLLM_API_BASE
- non-comment lines with no `=` or `:` delimiter (no key extractable): 6

### `mine/raw/agent_bleeding_edge/mem0ai/mem0/examples/mem0-demo/.env.example`

- category: env | bytes: 66 | mtime: 2026-08-05 20:33:14 | tracked: no | sha256[:12]: 9ffc013bfb3b
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): MEM0_API_KEY, OPENAI_API_KEY

### `mine/raw/agent_bleeding_edge/mem0ai/mem0/mem0-ts/src/oss/.env.example`

- category: env | bytes: 881 | mtime: 2026-08-05 20:33:14 | tracked: no | sha256[:12]: 81f4e519c054
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_COMPLETION_MODEL
- commented-out name candidates (13, names only, first 60): PGVECTOR_DB, PGVECTOR_USER, PGVECTOR_PASSWORD, PGVECTOR_HOST, PGVECTOR_PORT, QDRANT_URL, QDRANT_API_KEY, QDRANT_PATH, QDRANT_HOST, QDRANT_PORT, REDIS_URL, REDIS_USERNAME, REDIS_PASSWORD

### `mine/raw/agent_bleeding_edge/mem0ai/mem0/server/.env.example`

- category: env | bytes: 1143 | mtime: 2026-08-05 20:33:14 | tracked: no | sha256[:12]: 5d205d51eb75
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (16 of 16 non-comment lines matched): OPENAI_API_KEY, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_COLLECTION_NAME, ADMIN_API_KEY, JWT_SECRET, AUTH_DISABLED, DASHBOARD_URL, APP_DB_NAME, MEM0_DEFAULT_LLM_MODEL, MEM0_DEFAULT_EMBEDDER_MODEL, MEM0_TELEMETRY, REQUEST_LOG_RETENTION_DAYS
- commented-out name candidates (2, names only, first 60): ANTHROPIC_API_KEY, GOOGLE_API_KEY

### `mine/raw/agent_bleeding_edge/mem0ai/mem0/server/dashboard/.env.example`

- category: env | bytes: 115 | mtime: 2026-08-05 20:33:14 | tracked: no | sha256[:12]: 3244be7a1093
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): NEXT_PUBLIC_API_URL, API_INTERNAL_URL, NEXT_PUBLIC_INSTANCE_NAME

### `mine/raw/agent_bleeding_edge/sweepai/sweep/sweep_chat/.env`

- category: env | bytes: 224 | mtime: 2026-08-05 20:34:19 | tracked: no | sha256[:12]: ead6625176ea
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (4 of 4 non-comment lines matched): BACKEND_URL, NEXTAUTH_URL, NEXT_PUBLIC_POSTHOG_KEY, NEXT_PUBLIC_SENTRY_DSN

### `mine/raw/agent_platform/Aider-AI/aider/aider/website/assets/sample.env`

- category: env | bytes: 14123 | mtime: 2026-08-05 20:28:08 | tracked: no | sha256[:12]: 9d52036aa1ad
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- every line is blank or a comment; no active keys. Commented-out name candidates: 130

### `mine/raw/agent_platform/BerriAI/litellm/.env.example`

- category: env | bytes: 655 | mtime: 2026-08-05 20:28:18 | tracked: no | sha256[:12]: 7599c2e0d934
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (18 of 18 non-comment lines matched): OPENAI_API_KEY, OPENAI_BASE_URL, COHERE_API_KEY, OR_SITE_URL, OR_APP_NAME, OR_API_KEY, AZURE_API_BASE, AZURE_API_VERSION, AZURE_API_KEY, REPLICATE_API_KEY, REPLICATE_API_TOKEN, ANTHROPIC_API_KEY, INFISICAL_TOKEN, NOVITA_API_KEY, INFINITY_API_KEY, LITELLM_MASTER_KEY, DATABASE_URL, STORE_MODEL_IN_DB

### `mine/raw/agent_platform/BerriAI/litellm/docker/.env.example`

- category: env | bytes: 558 | mtime: 2026-08-05 20:28:18 | tracked: no | sha256[:12]: 363d5c2adf16
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): LITELLM_MASTER_KEY, DATABASE_URL
- commented-out name candidates (4, names only, first 60): SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SENDER_EMAIL

### `mine/raw/agent_platform/BerriAI/litellm/ui/litellm-dashboard/.env.development`

- category: env | bytes: 45 | mtime: 2026-08-05 20:28:24 | tracked: no | sha256[:12]: 50d60326c6ec
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (2 of 2 non-comment lines matched): NODE_ENV, NEXT_PUBLIC_BASE_URL

### `mine/raw/agent_platform/BerriAI/litellm/ui/litellm-dashboard/.env.production`

- category: env | bytes: 19 | mtime: 2026-08-05 20:28:24 | tracked: no | sha256[:12]: c30844a824e9
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (1 of 1 non-comment lines matched): NODE_ENV

### `mine/raw/agent_platform/OpenHands/OpenHands/.env.sample`

- category: env | bytes: 2984 | mtime: 2026-08-05 20:27:55 | tracked: no | sha256[:12]: 3ac1d6f606ce
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (6 of 6 non-comment lines matched): VITE_BACKEND_HOST, VITE_BACKEND_BASE_URL, VITE_FRONTEND_PORT, VITE_USE_TLS, VITE_INSECURE_SKIP_VERIFY, VITE_MOCK_API
- commented-out name candidates (12, names only, first 60): VITE_SESSION_API_KEY, VITE_WORKING_DIR, VITE_ENABLE_BROWSER_TOOLS, VITE_BASE_PATH, VITE_POSTHOG_API_KEY, VITE_DO_NOT_TRACK, OH_CANVAS_SAFE_BACKEND_PORT, OH_CANVAS_SAFE_VSCODE_PORT, OH_CANVAS_SAFE_STATE_DIR, OH_AGENT_SERVER_LOCAL_PATH, OH_AGENT_SERVER_GIT_REF, OH_AGENT_SERVER_VERSION

### `mine/raw/agent_platform/OpenHands/OpenHands/examples/acp-docker/.env.example`

- category: env | bytes: 1432 | mtime: 2026-08-05 20:27:55 | tracked: no | sha256[:12]: bc9fd924c287
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- every line is blank or a comment; no active keys. Commented-out name candidates: 9

### `mine/raw/agent_platform/SWE-agent/SWE-agent/.env.example`

- category: env | bytes: 330 | mtime: 2026-08-05 20:28:01 | tracked: no | sha256[:12]: d8e4a50fec5c
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): GITHUB_TOKEN

### `mine/raw/agent_platform/alamops/agetor/.env.example`

- category: env | bytes: 2036 | mtime: 2026-08-05 20:38:09 | tracked: no | sha256[:12]: 8c18d0be35bf
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- every line is blank or a comment; no active keys. Commented-out name candidates: 14

### `mine/raw/agent_platform/anomalyco/opencode/packages/slack/.env.example`

- category: env | bytes: 114 | mtime: 2026-08-05 20:38:03 | tracked: no | sha256[:12]: ac169e1874c6
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (3 of 3 non-comment lines matched): SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, SLACK_APP_TOKEN

### `mine/raw/agent_platform/cline/cline/apps/vscode/.env.example`

- category: env | bytes: 5535 | mtime: 2026-08-05 20:38:13 | tracked: no | sha256[:12]: 255a74ebf779
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): TELEMETRY_SERVICE_API_KEY, ERROR_SERVICE_API_KEY
- commented-out name candidates (49, names only, first 60): IS_DEV, CLINE_ENVIRONMENT, OTEL_TELEMETRY_ENABLED, OTEL_LOGS_EXPORTER, OTEL_METRICS_EXPORTER, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_HEADERS, OTEL_EXPORTER_OTLP_INSECURE, OTEL_METRIC_EXPORT_INTERVAL, OTEL_LOG_BATCH_SIZE, OTEL_LOG_BATCH_TIMEOUT, OTEL_LOG_MAX_QUEUE_SIZE, TEL_DEBUG_DIAGNOSTICS, OTEL_EXPORTER_OTLP_METRICS_PROTOCOL, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_PROTOCOL, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT, OTEL_TELEMETRY_ENABLED, OTEL_LOGS_EXPORTER, TEL_DEBUG_DIAGNOSTICS, OTEL_TELEMETRY_ENABLED, OTEL_LOGS_EXPORTER, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_INSECURE, OTEL_EXPORTER_OTLP_HEADERS, OTEL_TELEMETRY_ENABLED, OTEL_LOGS_EXPORTER, OTEL_EXPORTER_OTLP_PROTOCOL, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_HEADERS, CLINE_STORAGE_ADAPTER, CLINE_STORAGE_BUCKET, CLINE_STORAGE_ACCESS_KEY_ID, CLINE_STORAGE_SECRET_ACCESS_KEY, CLINE_STORAGE_ACCOUNT_ID, CLINE_STORAGE_ENDPOINT, CLINE_STORAGE_REGION, CLINE_STORAGE_ENDPOINT, CLINE_STORAGE_SYNC_INTERVAL_MS, CLINE_STORAGE_SYNC_MAX_RETRIES, CLINE_STORAGE_SYNC_BATCH_SIZE, CLINE_STORAGE_SYNC_BACKFILL_ENABLED, MULTI_ROOT_TRACE, GRPC_RECORDER_ENABLED, GRPC_RECORDER_FILE_NAME, E2E_TEST, IS_TEST

### `mine/raw/agent_platform/cline/kanban/web-ui/.env.example`

- category: env | bytes: 176 | mtime: 2026-08-05 20:38:20 | tracked: no | sha256[:12]: 9adf000b7789
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): POSTHOG_KEY, POSTHOG_HOST

### `mine/raw/agent_platform/continuedev/continue/extensions/cli/.env.example`

- category: env | bytes: 241 | mtime: 2026-08-05 20:28:46 | tracked: no | sha256[:12]: 69ee7f09b37f
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (2 of 2 non-comment lines matched): CONTINUE_API_BASE, CONTINUE_API_KEY

### `mine/raw/agent_platform/continuedev/continue/packages/continue-sdk/typescript/.env.example`

- category: env | bytes: 19 | mtime: 2026-08-05 20:28:47 | tracked: no | sha256[:12]: faa027332d39
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): CONTINUE_API_KEY

### `mine/raw/agent_platform/emdgroup/maestro/.github/scripts/macos/.env.example`

- category: env | bytes: 1207 | mtime: 2026-08-05 20:38:34 | tracked: no | sha256[:12]: bd16ad22532f
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (5 of 5 non-comment lines matched): APPLE_CERTIFICATE_P12, APPLE_CERTIFICATE_PASSWORD, APPLE_API_KEY_PATH, APPLE_API_KEY_ID, APPLE_API_ISSUER
- commented-out name candidates (4, names only, first 60): APPLE_CERTIFICATE_P12_BASE64, APPLE_SIGNING_IDENTITY, TARGET_TRIPLE, BUNDLE_DIR

### `mine/raw/agent_platform/google/adk-python/contributing/samples/integrations/authn-adk-all-in-one/adk_agents/sample.env`

- category: env | bytes: 179 | mtime: 2026-08-05 20:39:30 | tracked: no | sha256[:12]: 418deb79bb19
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (5 of 5 non-comment lines matched): GOOGLE_GENAI_USE_ENTERPRISE, GOOGLE_API_KEY, GOOGLE_MODEL, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET

### `mine/raw/agent_platform/google/adk-python/contributing/samples/integrations/authn-adk-all-in-one/idp/sample.env`

- category: env | bytes: 604 | mtime: 2026-08-05 20:39:30 | tracked: no | sha256[:12]: 57ec7f52a039
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (2 of 2 non-comment lines matched): GENERATE_JWT, PRIVATE_KEY

### `mine/raw/agent_platform/google/adk-python/tests/integration/.env.example`

- category: env | bytes: 321 | mtime: 2026-08-05 20:39:32 | tracked: no | sha256[:12]: ceb105a93826
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets; under a test path, fixture candidate
- key names (4 of 4 non-comment lines matched): TEST_BACKEND, GOOGLE_API_KEY, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION

### `mine/raw/agent_platform/mifunedev/openharness/.devcontainer/.example.env`

- category: env | bytes: 7185 | mtime: 2026-08-05 20:38:21 | tracked: no | sha256[:12]: 308d78fbb522
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (1 of 1 non-comment lines matched): GH_TOKEN
- commented-out name candidates (11, names only, first 60): OH_PROJECT_ROOT, SANDBOX_PASSWORD, SANDBOX_SSH_AUTHORIZED_KEYS, SANDBOX_SSH_PASSWORD_AUTH, XAI_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_BASE_URL, LANGFUSE_PRIVACY_PRESET, PI_SLACK_APP_TOKEN, PI_SLACK_BOT_TOKEN

### `mine/raw/agent_platform/mifunedev/openharness/.oh/templates/.devcontainer/.example.env`

- category: env | bytes: 138 | mtime: 2026-08-05 20:38:21 | tracked: no | sha256[:12]: 5606c8376f39
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- every line is blank or a comment; no active keys. Commented-out name candidates: 3

### `mine/raw/agent_platform/modelcontextprotocol/python-sdk/examples/clients/simple-chatbot/mcp_simple_chatbot/.env.example`

- category: env | bytes: 28 | mtime: 2026-08-05 20:28:27 | tracked: no | sha256[:12]: 5e8bf145283d
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (1 of 1 non-comment lines matched): LLM_API_KEY

### `mine/raw/mesh_comm/permissionlesstech/bitchat-android/tools/arti-build/TOOLCHAIN.env`

- category: env | bytes: 365 | mtime: 2026-08-05 08:57:05 | tracked: no | sha256[:12]: 9dab2be492d7
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (9 of 9 non-comment lines matched): ARTI_VERSION, ARTI_COMMIT, NATIVE_SOURCE_DATE_EPOCH, DEBIAN_SNAPSHOT, RUST_VERSION, CARGO_NDK_VERSION, ANDROID_NDK_VERSION, ANDROID_NDK_ARCHIVE, ANDROID_NDK_SHA256

### `mine/raw/mesh_comm/permissionlesstech/bitchat-android/tools/reproducible-builds/TOOLCHAIN.env`

- category: env | bytes: 714 | mtime: 2026-08-05 08:57:05 | tracked: no | sha256[:12]: 8982dad63249
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (14 of 14 non-comment lines matched): JAVA_VERSION, JAVA_MAJOR_VERSION, GRADLE_VERSION, ANDROID_COMPILE_SDK, ANDROID_PLATFORM_VERSION, ANDROID_PLATFORM_ARCHIVE, ANDROID_PLATFORM_SHA256, ANDROID_SDK_LICENSE_SHA1, ANDROID_PLATFORM_TOOLS_VERSION, ANDROID_PLATFORM_TOOLS_ARCHIVE, ANDROID_PLATFORM_TOOLS_SHA256, ANDROID_BUILD_TOOLS_VERSION, ANDROID_BUILD_TOOLS_ARCHIVE, ANDROID_BUILD_TOOLS_SHA256

### `mine/raw/narrative_corpus/twinejs/.env`

- category: env | bytes: 72 | mtime: 2026-08-06 23:57:41 | tracked: no | sha256[:12]: 91c8cd721cc7
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- key names (2 of 2 non-comment lines matched): REACT_APP_VERSION, REACT_APP_NAME

### `mine/raw/steal_protocol/arvarik/bmas/.env.example`

- category: env | bytes: 2801 | mtime: 2026-08-05 19:04:34 | tracked: no | sha256[:12]: 5aa9d0cb9113
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (4 of 4 non-comment lines matched): REDIS_PASSWORD, LITELLM_MASTER_KEY, BMAS_NODE_KEY, GEMINI_API_KEY
- commented-out name candidates (9, names only, first 60): ANTHROPIC_API_KEY, OPENAI_API_KEY, ALLOWED_DEV_ORIGINS, HF_TOKEN, TRIAGE_MODEL, TRIAGE_GPU_MEMORY, TRIAGE_MAX_MODEL_LEN, BESZEL_EMAIL, BESZEL_PASSWORD

### `mine/raw/steal_protocol/claudioed/agent-blackboard/.env.example`

- category: env | bytes: 1787 | mtime: 2026-08-05 19:04:51 | tracked: no | sha256[:12]: 4dad8ec4237c
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (10 of 10 non-comment lines matched): ANTHROPIC_API_KEY, LOG_LEVEL, MCP_MEMORY_SERVER_PATH, EMBEDDING_MODEL, BLACKBOARD_PERSISTENCE, BLACKBOARD_DB_PATH, MAX_AGENT_RETRIES, AGENT_TIMEOUT_SECONDS, KNOWLEDGE_BASE_PATH, MAX_KNOWLEDGE_RESULTS
- commented-out name candidates (2, names only, first 60): LOG_LEVEL, BLACKBOARD_PERSISTENCE

### `reference/gstdcoin/ai/.env.example`

- category: env | bytes: 3399 | mtime: 2026-08-05 08:57:23 | tracked: no | sha256[:12]: 4187c8b41bfd
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (30 of 30 non-comment lines matched): KV_REST_API_URL, KV_REST_API_TOKEN, UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN, TREASURY_SECRET, GSTD_JETTON_ADDRESS, DAO_VOTING, SETTLEMENT_ROUTER, STONFI_GSTD_POOL, TREASURY_GOLD, NEXT_PUBLIC_GSTD_CONTRACT, NEXT_PUBLIC_AGENT_REGISTRY, NEXT_PUBLIC_ESCROW_CONTRACT, NEXT_PUBLIC_DAO_VOTING, NEXT_PUBLIC_ADMIN_WALLET, NEXT_PUBLIC_TON_VAULT, NEXT_PUBLIC_SOL_VAULT, NEXT_PUBLIC_XRP_VAULT, NEXT_PUBLIC_TONCONNECT_MANIFEST_URL, NEXT_PUBLIC_TONAPI_URL, NEXT_PUBLIC_RPC_GATEWAY_URL, NEXT_PUBLIC_APP_URL, NEXT_PUBLIC_WS_URL, NEXT_PUBLIC_XAMAN_API_KEY, GROQ_API_KEY, SOLANA_RPC_URL, XRPL_WEBSOCKET_URL, WALLET_LINK_SECRET, BACKEND_URL, GSTD_NODE_URL

### `reference/gstdcoin/ai/frontend/.env.example`

- category: env | bytes: 1062 | mtime: 2026-08-05 08:57:23 | tracked: no | sha256[:12]: 8c2295ea74ba
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (8 of 8 non-comment lines matched): KV_REST_API_URL, KV_REST_API_TOKEN, TREASURY_SECRET, NEXT_PUBLIC_TON_VAULT, NEXT_PUBLIC_SOL_VAULT, NEXT_PUBLIC_XRP_VAULT, GSTD_JETTON_ADDRESS, NEXT_PUBLIC_APP_URL

### `reference/gstdcoin/ai/scripts/.env.example`

- category: env | bytes: 1117 | mtime: 2026-08-05 08:57:23 | tracked: no | sha256[:12]: 4dc7c55e0a8f
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (4 of 4 non-comment lines matched): TREASURY_WALLET_ADDRESS, GSTD_JETTON_ADDRESS, TREASURY_SECRET, GSTD_SWARM_URL
- commented-out name candidates (2, names only, first 60): TONCENTER_API_KEY, SETTLEMENT_WALLET_MNEMONIC

### `reference/gstdcoin/contracts/.env.example`

- category: env | bytes: 1330 | mtime: 2026-08-05 08:57:30 | tracked: no | sha256[:12]: aa4ebb551c03
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (13 of 13 non-comment lines matched): DEPLOYER_MNEMONIC, ADMIN_WALLET, GATEWAY_ADDRESS, TEAM_WALLET, ECOSYSTEM_WALLET, LIQUIDITY_WALLET, TEAM_AMOUNT, ECOSYSTEM_AMOUNT, LIQUIDITY_AMOUNT, XAUT_JETTON_MASTER, STONFI_ROUTER, TON_NETWORK, TON_API_KEY
- commented-out name candidates (1, names only, first 60): Gateway

### `reference/gstdcoin/gstd-bridge/.env.example`

- category: env | bytes: 2055 | mtime: 2026-08-05 08:57:27 | tracked: no | sha256[:12]: 12ecc191863b
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (16 of 16 non-comment lines matched): TON_RPC_URL, TON_API_KEY, SOLANA_RPC_URL, XRPL_WS_URL, TON_TOKEN_ADDRESS, SOL_TOKEN_ADDRESS, XRP_TOKEN_ADDRESS, TON_VAULT_ADDRESS, SOL_VAULT_ADDRESS, XRP_VAULT_ADDRESS, MPC_SHARE_INDEX, MPC_THRESHOLD, MPC_TOTAL_PARTIES, RUST_LOG, GSTD_PLATFORM_URL, GSTD_NODE_ID

### `reference/gstdcoin/gstdbot/.env.example`

- category: env | bytes: 4171 | mtime: 2026-08-05 08:57:28 | tracked: no | sha256[:12]: f0334996cd90
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (10 of 10 non-comment lines matched): NODE_NAME, GSTD_NODE_ID, GSTD_DASHBOARD_PORT, SWARM_ENABLED, GSTD_MAX_CPU, GSTD_MAX_RAM, GSTD_API_URL, GSTD_SWARM_URL, GSTD_P2P_PORT, GSTD_MEMORY
- commented-out name candidates (16, names only, first 60): OLLAMA_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_IDS, TELEGRAM_COMMUNITY_CHAT, GSTD_API_PORT, GSTD_BOOTSTRAP_PEERS, GSTD_P2P_ANNOUNCE_IP, GSTD_P2P_MDNS, GSTD_NAAS_ENABLED, REDIS_URL, CHROMA_URL, GSTD_STORAGE, GSTD_WALLET_MNEMONIC, TON_NETWORK, GSTD_APPS, WALLET_LINK_SECRET

### `reference/gstdcoin/web/.env.example`

- category: env | bytes: 421 | mtime: 2026-08-05 08:57:25 | tracked: no | sha256[:12]: d12f06491185
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- notes: template/example filename, expected to hold placeholders not live secrets
- key names (7 of 7 non-comment lines matched): NEXT_PUBLIC_SITE_URL, NEXT_PUBLIC_PLAUSIBLE_DOMAIN, NEXT_PUBLIC_TELEGRAM, NEXT_PUBLIC_TWITTER, NEXT_PUBLIC_GITHUB, NEXT_PUBLIC_STONFI, NEXT_PUBLIC_TON_CONTRACT

### `reference/gstdcoin/web/.env.production`

- category: env | bytes: 693 | mtime: 2026-08-05 08:57:25 | tracked: no | sha256[:12]: 96367bb3099b
- gitignore: .gitignore line 159 pattern <reference/gstdcoin/>
- key names (10 of 10 non-comment lines matched): NODE_ENV, NEXT_TELEMETRY_DISABLED, NEXT_PUBLIC_SITE_URL, NEXT_PUBLIC_PLAUSIBLE_DOMAIN, NEXT_PUBLIC_TELEGRAM, NEXT_PUBLIC_TWITTER, NEXT_PUBLIC_GITHUB, NEXT_PUBLIC_STONFI, NEXT_PUBLIC_TON_CONTRACT, NODE_OPTIONS

### `state/auth_switchboard/20260905T161520Z_post_swap_broken_20260905/credentials.json`

- category: json-secret | bytes: 14372 | mtime: 2026-09-05 12:15:20 | tracked: no | sha256[:12]: 6a3aa795bdac
- gitignore: .gitignore line 30 pattern <state/>
- JSON key paths (16, depth-capped at 6, first 300): oauth:login_attribution, web-remote-control:external-relay:pass_hash, oauth:zai:access_token, zcodejwttoken, oauth:zai:user_info, oauth:active_provider, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:authorization_credentials, mcp:oauth:cf971e4cc0e9748b766a9976:client_information, mcp:oauth:cf971e4cc0e9748b766a9976:tokens, mcp:oauth:8ed70504d9b5e06d958108d9:authorization_credentials, mcp:oauth:8ed70504d9b5e06d958108d9:client_information, mcp:oauth:8ed70504d9b5e06d958108d9:tokens

### `state/auth_switchboard/20260905T161700Z_post_swap_broken_20260905/credentials.json`

- category: json-secret | bytes: 14372 | mtime: 2026-09-05 12:17:00 | tracked: no | sha256[:12]: 6a3aa795bdac
- gitignore: .gitignore line 30 pattern <state/>
- JSON key paths (16, depth-capped at 6, first 300): oauth:login_attribution, web-remote-control:external-relay:pass_hash, oauth:zai:access_token, zcodejwttoken, oauth:zai:user_info, oauth:active_provider, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:authorization_credentials, mcp:oauth:cf971e4cc0e9748b766a9976:client_information, mcp:oauth:cf971e4cc0e9748b766a9976:tokens, mcp:oauth:8ed70504d9b5e06d958108d9:authorization_credentials, mcp:oauth:8ed70504d9b5e06d958108d9:client_information, mcp:oauth:8ed70504d9b5e06d958108d9:tokens

### `state/auth_switchboard/20260905T162449Z_dogfood_a/credentials.json`

- category: json-secret | bytes: 14372 | mtime: 2026-09-05 12:24:49 | tracked: no | sha256[:12]: 6a3aa795bdac
- gitignore: .gitignore line 30 pattern <state/>
- JSON key paths (16, depth-capped at 6, first 300): oauth:login_attribution, web-remote-control:external-relay:pass_hash, oauth:zai:access_token, zcodejwttoken, oauth:zai:user_info, oauth:active_provider, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:authorization_credentials, mcp:oauth:cf971e4cc0e9748b766a9976:client_information, mcp:oauth:cf971e4cc0e9748b766a9976:tokens, mcp:oauth:8ed70504d9b5e06d958108d9:authorization_credentials, mcp:oauth:8ed70504d9b5e06d958108d9:client_information, mcp:oauth:8ed70504d9b5e06d958108d9:tokens

### `state/auth_switchboard/20260905T162449Z_dogfood_b/credentials.json`

- category: json-secret | bytes: 14372 | mtime: 2026-09-05 12:24:49 | tracked: no | sha256[:12]: 6a3aa795bdac
- gitignore: .gitignore line 30 pattern <state/>
- JSON key paths (16, depth-capped at 6, first 300): oauth:login_attribution, web-remote-control:external-relay:pass_hash, oauth:zai:access_token, zcodejwttoken, oauth:zai:user_info, oauth:active_provider, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:authorization_credentials, mcp:oauth:cf971e4cc0e9748b766a9976:client_information, mcp:oauth:cf971e4cc0e9748b766a9976:tokens, mcp:oauth:8ed70504d9b5e06d958108d9:authorization_credentials, mcp:oauth:8ed70504d9b5e06d958108d9:client_information, mcp:oauth:8ed70504d9b5e06d958108d9:tokens

### `state/auth_switchboard/20260907T082019Z_pre_apikey_swap_20260907/credentials.json`

- category: json-secret | bytes: 14372 | mtime: 2026-09-07 04:20:19 | tracked: no | sha256[:12]: 6b8e2408a66c
- gitignore: .gitignore line 30 pattern <state/>
- JSON key paths (16, depth-capped at 6, first 300): oauth:login_attribution, web-remote-control:external-relay:pass_hash, oauth:zai:access_token, zcodejwttoken, oauth:zai:user_info, oauth:active_provider, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:authorization_credentials, mcp:oauth:cf971e4cc0e9748b766a9976:client_information, mcp:oauth:cf971e4cc0e9748b766a9976:tokens, mcp:oauth:8ed70504d9b5e06d958108d9:authorization_credentials, mcp:oauth:8ed70504d9b5e06d958108d9:client_information, mcp:oauth:8ed70504d9b5e06d958108d9:tokens

### `state/auth_switchboard/20260907T083251Z_known_good/credentials.json`

- category: json-secret | bytes: 14372 | mtime: 2026-09-07 04:32:51 | tracked: no | sha256[:12]: 6b8e2408a66c
- gitignore: .gitignore line 30 pattern <state/>
- JSON key paths (16, depth-capped at 6, first 300): oauth:login_attribution, web-remote-control:external-relay:pass_hash, oauth:zai:access_token, zcodejwttoken, oauth:zai:user_info, oauth:active_provider, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state, mcp:oauth:8ed70504d9b5e06d958108d9:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state, mcp:oauth:cf971e4cc0e9748b766a9976:discovery_state_fetched_at, mcp:oauth:cf971e4cc0e9748b766a9976:authorization_credentials, mcp:oauth:cf971e4cc0e9748b766a9976:client_information, mcp:oauth:cf971e4cc0e9748b766a9976:tokens, mcp:oauth:8ed70504d9b5e06d958108d9:authorization_credentials, mcp:oauth:8ed70504d9b5e06d958108d9:client_information, mcp:oauth:8ed70504d9b5e06d958108d9:tokens

### `.venv/Lib/site-packages/tornado/test/test.key`

- category: key | bytes: 1736 | mtime: 2026-08-12 09:23:04 | tracked: no | sha256[:12]: eca1bc432a48
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); under a test path, fixture candidate
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `memory/tls/lan.key`

- category: key | bytes: 1675 | mtime: 2026-08-14 12:41:41 | tracked: YES | sha256[:12]: d798d8c174ee
- BEGIN markers in first 8KB: RSA PRIVATE KEY | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/client0.key`

- category: key | bytes: 1732 | mtime: 2026-08-05 20:30:12 | tracked: no | sha256[:12]: c642052dc79d
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/client1.key`

- category: key | bytes: 1732 | mtime: 2026-08-05 20:30:12 | tracked: no | sha256[:12]: 6ead788ec349
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/client2.key`

- category: key | bytes: 1732 | mtime: 2026-08-05 20:30:12 | tracked: no | sha256[:12]: 0a1e18261d18
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/localhost.key`

- category: key | bytes: 1732 | mtime: 2026-08-05 20:30:12 | tracked: no | sha256[:12]: 042231411ce1
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/proxy.key`

- category: key | bytes: 1736 | mtime: 2026-08-05 20:30:12 | tracked: no | sha256[:12]: 0cce71f742b1
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/mononoke/tests/integration/certs/root-ca.key`

- category: key | bytes: 1732 | mtime: 2026-08-05 20:30:12 | tracked: no | sha256[:12]: 70b8dd986955
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `.venv/Lib/site-packages/borb/license/public_keys/public_key_001.pem`

- category: pem | bytes: 451 | mtime: 2026-08-17 21:03:02 | tracked: no | sha256[:12]: 816834e856a6
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree)
- BEGIN markers in first 8KB: PUBLIC KEY | encrypted marker present: no

### `.venv/Lib/site-packages/botocore/cacert.pem`

- category: pem | bytes: 259837 | mtime: 2026-08-27 13:45:16 | tracked: no | sha256[:12]: ed93d6346236
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree)
- BEGIN markers in first 8KB: CERTIFICATE, CERTIFICATE, CERTIFICATE, CERTIFICATE | encrypted marker present: no

### `.venv/Lib/site-packages/certifi/cacert.pem`

- category: pem | bytes: 240216 | mtime: 2026-07-31 11:58:38 | tracked: no | sha256[:12]: 9cc2a774b519
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); certifi public Mozilla CA bundle, not a private key
- BEGIN markers in first 8KB: CERTIFICATE, CERTIFICATE, CERTIFICATE, CERTIFICATE, CERTIFICATE | encrypted marker present: no

### `.venv/Lib/site-packages/litellm/proxy/auth/public_key.pem`

- category: pem | bytes: 458 | mtime: 2026-08-27 13:45:53 | tracked: no | sha256[:12]: c7e5afd002e5
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree)
- BEGIN markers in first 8KB: PUBLIC KEY | encrypted marker present: no

### `.venv/Lib/site-packages/pip/_vendor/certifi/cacert.pem`

- category: pem | bytes: 272441 | mtime: 2026-07-20 07:42:01 | tracked: no | sha256[:12]: fc9165a12403
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); certifi public Mozilla CA bundle, not a private key
- BEGIN markers in first 8KB: CERTIFICATE, CERTIFICATE, CERTIFICATE, CERTIFICATE | encrypted marker present: no

### `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/chain.pem`

- category: pem | bytes: 2886 | mtime: 2026-09-23 03:16:34 | tracked: no | sha256[:12]: 9796fd4814ea
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); under a test path, fixture candidate
- BEGIN markers in first 8KB: CERTIFICATE, CERTIFICATE | encrypted marker present: no

### `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/thing1.pem`

- category: pem | bytes: 1573 | mtime: 2026-09-23 03:16:34 | tracked: no | sha256[:12]: 3d832c9a3574
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); under a test path, fixture candidate
- BEGIN markers in first 8KB: CERTIFICATE | encrypted marker present: no

### `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/thing2-duplicate.pem`

- category: pem | bytes: 1415 | mtime: 2026-09-23 03:16:34 | tracked: no | sha256[:12]: 0914f3c0e91a
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); under a test path, fixture candidate
- BEGIN markers in first 8KB: CERTIFICATE | encrypted marker present: no

### `.venv/Lib/site-packages/twisted/internet/test/fake_CAs/thing2.pem`

- category: pem | bytes: 1415 | mtime: 2026-09-23 03:16:34 | tracked: no | sha256[:12]: 0914f3c0e91a
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); under a test path, fixture candidate
- BEGIN markers in first 8KB: CERTIFICATE | encrypted marker present: no

### `.venv/Lib/site-packages/twisted/test/server.pem`

- category: pem | bytes: 5360 | mtime: 2026-09-23 03:16:34 | tracked: no | sha256[:12]: a681b6146651
- gitignore: .gitignore line 1 pattern <.venv/>
- notes: inside .venv (third-party package tree); under a test path, fixture candidate
- BEGIN markers in first 8KB: RSA PRIVATE KEY, CERTIFICATE | encrypted marker present: no

### `mine/raw/agent_bleeding_edge/letta-ai/letta/certs/localhost-key.pem`

- category: pem | bytes: 1736 | mtime: 2026-08-05 20:33:11 | tracked: no | sha256[:12]: fdd6981a651b
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- BEGIN markers in first 8KB: PRIVATE KEY | encrypted marker present: no

### `mine/raw/agent_bleeding_edge/letta-ai/letta/certs/localhost.pem`

- category: pem | bytes: 1632 | mtime: 2026-08-05 20:33:11 | tracked: no | sha256[:12]: 7e9020b73d48
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- BEGIN markers in first 8KB: CERTIFICATE | encrypted marker present: no

### `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/auth/public_key.pem`

- category: pem | bytes: 458 | mtime: 2026-08-05 20:28:21 | tracked: no | sha256[:12]: c7e5afd002e5
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- BEGIN markers in first 8KB: PUBLIC KEY | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/cert1.pem`

- category: pem | bytes: 1340 | mtime: 2026-08-05 20:30:13 | tracked: no | sha256[:12]: 5cc651d8f61b
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: CERTIFICATE | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/cert2.pem`

- category: pem | bytes: 1340 | mtime: 2026-08-05 20:30:13 | tracked: no | sha256[:12]: cae4a590aab2
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: CERTIFICATE | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/combined.pem`

- category: pem | bytes: 4424 | mtime: 2026-08-05 20:30:13 | tracked: no | sha256[:12]: f00a2d452dd0
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: CERTIFICATE, NOT A CERTIFICATE, CERTIFICATE | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/scm/lib/auth/src/test_certs/not_a_cert.pem`

- category: pem | bytes: 1744 | mtime: 2026-08-05 20:30:13 | tracked: no | sha256[:12]: 0c62f9d69488
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- notes: under a test path, fixture candidate
- BEGIN markers in first 8KB: NOT A CERTIFICATE | encrypted marker present: no

### `mine/raw/agent_platform/facebook/sapling/eden/scm/sapling/dummycert.pem`

- category: pem | bytes: 2302 | mtime: 2026-08-05 20:30:14 | tracked: no | sha256[:12]: ec9be4ca9fc1
- gitignore: .gitignore line 44 pattern <mine/raw/**>
- BEGIN markers in first 8KB: CERTIFICATE | encrypted marker present: no

## Falsifier notes

- Every number above comes from the instrument run in this session; rerun the script to reproduce.
- Values were never read: the env parser captures only the text before `=`, the JSON walker keeps only key strings, pem/key files contribute only their standard BEGIN marker lines.
- This is a working-tree census. History-level leakage (secrets inside old commits) is a different instrument and is reported separately by the item, not assumed here.


## History-level check (ever committed on any ref)

- Command: `git log --all --format= --name-only | sort -u` over the whole repo produced 90,399 unique paths ever committed on any ref. The broadened case-insensitive grep receipt is kept at `_f22_history_grep.txt` (32 bytes).
- Grep pattern: `(^|/)\.[^/]*env[^/]*$|(^|/)[^/]*\.env$|\.key$|\.pem$|(^|/)credentials\.json$|(^|/)secrets\.json$`. It matched exactly 2 paths ever committed: `.env.example` and `memory/tls/lan.key`. Both are still tracked today; no secret-pattern path was ever committed and later deleted, so there is no history-only leak.
- `memory/tls/lan.key` entered git in exactly one commit, 799ddb6fe ("wip 20260819 ... LOCAL ONLY, not pushed"). That commit is contained in branches on the `local` remote (`C:\Users\foste\Documents\projects\Mag-backup.git`): mag/run-beta1-factory-build-audi-20260806T231709Z, run-beta1-factory-audit-20260914, sweep/kill-list-stage1, wave-20260916-checkpoint3. The key material therefore also sits in that local backup remote, not only this working repo.

## Findings

1. TRACKED VIOLATION: `memory/tls/lan.key` (1,675 bytes, mtime 2026-08-14 12:41:41, sha256[:12] d798d8c174ee) is an unencrypted RSA PRIVATE KEY tracked in git since 799ddb6fe and present on the local backup remote. This is the one genuine "should not be tracked" hit in the repo. Remediation (rotate the key, `git rm --cached memory/tls/lan.key`, add an ignore rule) is an operator decision; this census changed nothing.
2. TRACKED OK: `.env.example` (347 bytes, mtime 2026-08-05 08:56:54, commit eb07ad62e) is a placeholder template holding 13 placeholder names (XAI_API_KEY, XAI_MODEL, OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GROQ_API_KEY, DEEPSEEK_API_KEY, DEEPSEEK_OVERMIND_API_KEY, GEMINI_API_KEY, TOGETHER_API_KEY, VAST_API_KEY, VAST_OPENAI_BASE_URL, VAST_OPENAI_API_KEY). Tracking a template is expected.
3. Live root `.env` (5,941 bytes, mtime 2026-09-27 07:52:26, sha256[:12] 32b93b4bb73e): untracked, covered by `.gitignore` line 19. Holds 52 active keys out of 55 non-comment lines (1 line has no delimiter, 2 lines carry a delimiter but a name shape the census regex does not accept; coverage recorded, values never read). Key names are the provider zoo: XAI_SD_API_KEY, DEEPSEEK_API_KEY, VASTAI_API_KEY, NVIDIABuild, NVIDIABuild2, VERCEL_KEY, ZAI_API_KEY, ZAI_API_KEY_2, ZAI_API_KEY_3, ZAI_API_KEY_Pro, ZAI_API_KEY_Lite, HERMES_API_KEY_1, HERMES_API_KEY_2, MAPBOX_TOKEN, OPENCODE, OPENCODE2, OPENROUTER_API_KEY, OPENROUTER_API_KEY_2, OPENROUTER_MODEL, OPENAI_API_KEY, ANTHROPIC_API_KEY, ANTHROPIC_API_KEY_2, GROQ_API_KEY, GROQ_API_KEY_2, GEMINI_API_KEY, GOOGLE_API_KEY, TOGETHER_API_KEY, TOGETHER_API_KEY2, COHERE_API_KEY_FREE, COHERE_API_KEY_PAID, CEREBAS_API_KEY, CEREBAS_API_KEY2, MISTRAL_API_KEY, MISTRAL_API_KEY_2, CURSOR_API_KEY, NOTION_API_KEY, GROK_API_KEY, GROK_API_KEY_2, OLLAMA_HOST, MAG_DRAINER, MAG_DRAINER_FORCE, X_ConsumerKey, X_SecretKey, X_BearerToken, X_ClientID, X_ClientSecret, X_REDIRECT_URI, GHOST_X_HANDLE, AOS_AGENT_MODEL, OPENCLAW_GATEWAY_TOKEN, OPENCLAW_GATEWAY_PASSWORD, ANTHROPIC_WORKSPACE_ID.
4. Six `credentials.json` snapshots under `state/auth_switchboard/` (each 14,372 bytes; mtimes 2026-09-05 x4 and 2026-09-07 x2) all hold the same 16-key OAuth session structure: oauth:login_attribution, web-remote-control:external-relay:pass_hash, oauth:zai:access_token, zcodejwttoken, oauth:zai:user_info, oauth:active_provider, plus mcp:oauth:<client-id>:discovery_state / discovery_state_fetched_at / authorization_credentials / client_information / tokens for two client ids. All untracked, all covered by `.gitignore` line 30 (`state/`).
5. Fresh litter, same day: 16 pytest fixture env files under `agents/pytest-tmp-*/` (8 `empty.env` at 9 bytes, 8 `.env` at 95 bytes whose only content is a commented-out DISCORD_BOT_TOKEN line), created 2026-09-28 by token-loading tests. Covered by `.gitignore` line 203 (`agents/pytest-*/`).
6. The rest is third-party material inside ignored trees, none of it this repo's secrets: `mine/raw/**` 79 (harvested upstream templates like litellm/phoenix/zep/mem0 .env.example, sapling mononoke test certs client0..root-ca.key, dummycert.pem, letta localhost certs, litellm public_key.pem which is a JWT-verification PUBLIC key), `corpus/library/` 11, `.venv/` 11 (tornado test.key, 5 twisted fake-CA/server pems, borb public key, botocore + certifi + pip-vendored certifi cacert.pem which are public Mozilla CA bundles, litellm public_key.pem), `reference/gstdcoin/` 8, `memory/improve/**` 1 (ponytail source snapshot .env.example).

## Ignored-file rule buckets (exact, 133 rows)

| rule | files |
|---|---|
| `.gitignore:44` `mine/raw/**` | 79 |
| `.gitignore:203` `agents/pytest-*/` | 16 |
| `.gitignore:197` `corpus/library/` | 11 |
| `.gitignore:1` `.venv/` | 11 |
| `.gitignore:159` `reference/gstdcoin/` | 8 |
| `.gitignore:30` `state/` | 6 |
| `.gitignore:68` `memory/improve/**` | 1 |
| `.gitignore:19` `.env` | 1 |

## Run-moment caveat

- Three instrument passes this session each counted 135 secret-pattern files with 2 tracked / 133 ignored / 0 exposed. Walk totals drifted between passes (3,499,225 then 3,509,642 then 3,563,077 files) because concurrent seats keep spawning `agents/pytest-tmp-*` dirs mid-scan; per the B2-216 denominator law this census is a snapshot of one tree at one moment (2026-09-28, final pass), not a constant.
