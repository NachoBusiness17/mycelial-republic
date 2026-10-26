# FAN headless-agent-cli

lane model: inclusionai/ling-3.0-flash-sante:free
ts: 2026-10-03T22:33:26.902924+00:00
dt: 10.1s

---

Session persistence
Keep a structured journal of tool calls and outputs (SQLite or JSONL) and use git to track diffs so sessions can resume. Aider stores patches and supports restore; see its repo. Claude Code retains conversation state locally. OWED: a writeup specifically on persistence patterns for headless research agents. I searched my training data and found none to cite.

Banking
Wrap the agent with a token counter and a per-session spend cap. Rotate API keys and log usage. OWED: a canonical source on agent banking. I checked for papers or repos on cost guardrails for CLI agents and found none to cite.

Safety rails
Sandbox execution (bubblewrap, docker, or a VM), enforce timeouts, and require approval for shell commands. Anthropic describes permission modes for Claude Code. OWED: a formal safety framework for autonomous research workers. I looked for one and found none to cite.

Sources
- Aider repo: github.com/Aider-AI/aider
- Anthropic Claude Code docs: docs.anthropic.com (search Claude Code permissions)
- None for opencode or Hermes-style specifics.
