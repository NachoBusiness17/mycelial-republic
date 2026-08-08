# Steer agent — operator/assistant guidance drop

> Write steering notes here. `main.py steer-agent --sync` pushes new lines into
> the agent's `operator_inbox`, which it drains at its next checkpoint.
> Every non-empty, non-heading line = one guidance note (idempotent; re-run
> never duplicates). Source tag: copilot-assistant (default).

- Example: Prefer verifying existing work over rewriting; file residual notes under memory/.
- Example: If a tool result looks wrong, stop and say exactly what, do not invent a fix.
