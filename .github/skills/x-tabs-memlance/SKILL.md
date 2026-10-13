---
name: x-tabs-memlance
description: 'Read all open X (Twitter) tabs and research them through memlance. Use when the operator says "read my x tabs", "research my x tabs", "read the x tabs with memlance", or wants the captured X prompt tabs (memory/ghost/x_surface) grounded against our own verified memory states. Runs mag.ghost_memlance.select per tab, produces a grounded research synthesis, and optionally folds the win as a tesuji shell + STEAL pack. Deterministic + $0, module functions only, no terminal spawns.'
user-invocable: true
---

# X-Tabs Memlance Research

Read every open X (Twitter) tab and research it by grounding each tab's content against our
own verified memory via memlance (`mag.ghost_memlance.select`). The output is a deep-research
synthesis: for each tab, what it is + which of OUR grounded memory states it maps to + the
research takeaway. Honors the grounding rule: only real bytes from disk, never synthesized.

## Refined (2026-08-11): only useful data, noise to a noise file, percolator everywhere

Every tab now passes through the **percolator** (`mag/percolator.py`) BEFORE memlance, so only
USEFUL signal is brought in:
- **Noise/theater is stripped** to a per-domain noise file (`memory/ghost/noise/<domain>.jsonl`).
- **Repeatable signal is compiled into invariants** (dedupe by content hash, folded via fact_bus).
- **Novel signal is queued for exploration** (`memory/percolator/explore.jsonl`) → deep research /
  steal / synthesis / frontier assistance.
- **False positives are filtered** (a detected signal that is actually noise) — written to a
  `<domain>.fp.jsonl` noise file and counted, NEVER carried forward as truth.
- **Inaccessible tabs / blocked threads / replies** are logged to the **intake register**
  (`memory/ghost/intake/register.jsonl`, status `open`) to look into later — this assists
  inference/steering (e.g. when an AI is deep in training).
- `percolate_signal(text, pattern=...)` is the drop-in for **training-signal detection EVERYWHERE**:
  it strips noise, filters false positives, compiles repeats, queues novel, and emits a
  `mag.training_events.emit` training event.

## When to Use
- Operator: "read my open x tabs", "research my x tabs", "read the x tabs with memlance", "do the x tabs thing".
- Any time the captured X-surface prompts (`memory/ghost/x_surface/nachoquixotic_prompts/`) should
  be grounded against our memory and synthesized.
- Extends to live X tabs shared in the browser: read each shared tab, then run memlance per tab.

## Procedure

1. **Locate the X tab content.**
   - Captured tabs: `memory/ghost/x_surface/nachoquixotic_prompts/` (`.md`, `.txt`, `.mkd`).
   - Live tabs: use the shared browser pages; read each X page's content.

2. **Read all the tabs.** Read every file (or every shared page) — don't skip any.

3. **Run memlance per tab.** For each tab, call `mag.ghost_memlance.select(goal, k=5)` with a
   goal summarizing that tab's defining feature. This returns ONLY real bytes from disk, each with
   a deterministic `verified` verdict. Use the included script to do this for the whole folder:
   `python -m mag.x_tabs_memlance` or the skill script
   [scripts/research_x_tabs.py](./scripts/research_x_tabs.py) (module functions only — the script
   itself calls `ghost_memlance.select`, no terminal spawns, no LLM).

4. **Synthesize.** For each tab produce:
   - what the tab is (its defining capability / theme),
   - the top VERIFIED memory state(s) it grounds to (path + title + reason),
   - the research takeaway (how it maps to our architecture: swarm/consensus, agent-as-OS tool
     surface, grounding/sovereignty, leak-detection, stateless/invariant memory).

5. **Fold the win (optional, standing doctrine).** Log the emergent insight as a tesuji shell via
   `mag.tesuji_shell.log_tesuji_shell(...)` and/or write a `STEAL_*` research pack to
   `queue/handoff/`. Record any grounded PID/process facts via `mag.fact_bus.publish_fact`.

## Resources
- Script: [scripts/research_x_tabs.py](./scripts/research_x_tabs.py) — reads the x_surface folder,
  runs memlance per tab, prints the grounded readout. Deterministic + $0.
- Memlance module: `mag/ghost_memlance.py` (`index`, `select`, `trace_state`).

## Notes
- Grounding rule: never invent a connection — only report states memlance actually selected
  (real bytes). Unverified matches are flagged `[U]`; verified are `[V]`.
- If the operator wants it as a standing capability beyond one-off runs, wire it into a cadence job
  or keep it as this skill.
