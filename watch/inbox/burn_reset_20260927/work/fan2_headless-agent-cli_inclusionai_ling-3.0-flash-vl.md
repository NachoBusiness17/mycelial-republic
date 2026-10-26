# FAN2 headless-agent-cli

lane model: inclusionai/ling-3.0-flash-vl

---

Best-practice patterns for wrapping headless CLI coding agents as autonomous research workers, organized by your three concerns. I have cited sources I can verify by name and marked the rest as OWED with what I tried.

---

## 1. Session Persistence

**Pattern: Git-integrated checkpointing.**
aider (paul-gauthier/aider on GitHub) persists conversation history in `.aider.history` within the working repo. It also uses a repo-map (a cached summary of the codebase) stored in the session directory to maintain context across runs. Using `--restore` resumes from a prior session. This is a verified pattern from the aider documentation and source.

**Pattern: Structured state snapshots.**
For Claude Code used in headless/CI mode (documented at claude.ai/code), sessions can be run non-interactively with `--output-format stream-json` for programmatic consumption. However, I could not find verified documentation on Claude Code's internal mechanisms for resuming interrupted long-running sessions. OWED: I searched the Claude Code documentation and GitHub presence but could not verify whether it natively supports checkpoint-based resume for autonomous (non-interactive) long-running research tasks.

**Pattern: External session store (recommended for autonomous workers).**
For wrapping any headless agent as a long-running research worker, a common best practice is an external session store separate from the agent itself:
- Store conversation transcripts, current task state, partial outputs, and accumulated findings in a lightweight database (SQLite) or structured files (JSONL, Markdown).
- Use a watchdog or orchestrator process that periodically snapshots state and can resume the agent from the last checkpoint.
- Use git commits as logical checkpoints when the agent modifies code in a repo.

I could not find a single authoritative writeup describing this exact pattern for CLI coding agents specifically. OWED: I searched for "autonomous agent session persistence pattern" and "CLI agent checkpoint resume" and found discussions on the Claude Code Discord and various blog posts, but none I could verify as a canonical reference.

**Pattern: Anthropic's guidance on agent persistence.**
Anthropic's "Agents" documentation (anthropic.com/agents) and the "Building AI Agents" guidance discuss that agents should maintain external memory since context windows are finite. The concept of "compaction"
