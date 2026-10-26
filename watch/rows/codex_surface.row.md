ROW
pointer: /mag/mag/codex_seat.py + /mag/jobs
claim: Codex is invoked today as a BOUNDED one-shot wrapper over `codex exec` (gpt-5.6-sol / xhigh, six-day priority window, workspace-write approval=never). Entry points: (a) direct CLI `python -m mag.codex_seat run "<prompt>"`, (b) job dirs under /mag/jobs/<job_id>/ carrying seat_contract.json + PASTE.md that other seats (e.g. reset-burn-codex) run; there is NO persistent mailbox — jobs ride one-shot exec, and seat_dispatch.py can queue/route a goal to any seat by name. No seat_corpus/latest.json lane file exists (path absent). Max trail depth in runs tree (codex_seat/fold) shows the seat already folded long-horizon projects (project-zcode-seat-protocol, project-chain-v2, project-swarm-directive), so it has run multi-project work before.
type: probe
confidence: M
status: VERIFIED
evidence: codex_seat.py:5 bounds it as a "BOUNDED one-shot wrapper over `codex exec`" with workspace-write sandbox; codex_seat.py:101 run() is one-shot exec bounded by timeout
evidence: /mag/jobs/reset-burn-codex/{seat_contract.json(goal: burn Codex quota), PASTE.md}; corresponding reset-burn-grok2 seat_contract.json proves the job-dir mechanism is seat-agnostic
evidence: seat_dispatch.py:126 "Queue + dispatch a goal to the chosen seat", seat_dispatch.py:157-158 holds gate_model then subprocess-runs the seat, writes a dispatch record
evidence: /mag/memory/runs/codex_seat/fold/ lists 30 projects (project-zcode-seat-protocol, project-swarm-directive, feedback-cost-session-economics) — the seat's long-horizon history
evidence (negative): no /mag/seat_corpus/latest.json (checked /mag/seat_corpus absent; -d seat_corpus = none); /mag/memory/runs/codex_seat/ has fold/ + *.json but no trail_core.md/trail files

INTEGRATION OPTIONS:
1. Job dir via /patches — drop a seat_contract.json+PASTE.md into /mag/jobs/<new-id>/ following reset-burn-codex shape; seat_dispatch route already honors contract goals, near-zero code.
2. Bridge/inbox post — plug a mailbox/new-inbox onto codex_seat.run() (mirror deepseek-room-adapter bridge pattern) so long-horizon tasks arrive as queued messages instead of one-shot prompts.
3. seat_dispatch task — call `python -m mag.seat_dispatch task "<goal>" --seat codex` (seat_dispatch.py:216 CLI) to queue+run codex as a dispatched seat with gate-hold + dispatch record; cheapest, uses existing routing.
