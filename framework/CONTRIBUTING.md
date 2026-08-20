# CONTRIBUTING — help advance the machine

This is an open invitation into the real framework. We want help with the **machine** —
the actual sovereign architecture — not just the educational kit.

## The machine, in one paragraph

A self-running agent system built on a few load-bearing ideas:
- **State-first, LLM-last.** The deterministic engine owns truth; the model narrates after.
- **Content-addressed memory.** The verkle chain: append-only, hash-linked, replayable.
  "Disk is law" made structural.
- **The autonomous loop.** A governor + cadence + drainer keeps the system alive without
  being asked.
- **Cheap-first economics.** The owned/cheap side carries the routine load; cache aggressively.
- **Consensus, honestly.** N cheap workers agree only when the witnesses are *independent*
  (the consensus-illusion guard).
- **The hologram.** Any fragment of the shared reality reconstructs the whole; each peer's
  capacity is its fidelity ceiling.
- **Statelessness.** Workers are born fresh from a frozen prefix; they die; the wave persists.

## The two surfaces

| Surface | Location | What you can do |
|---------|----------|-----------------|
| **Portable contracts** | `scaffolds/sovereign-toolkit/` | Run them (`python -m pytest tests/ -q`), adapt them, enhance them. Best place to start. |
| **The real machine** | `framework/` | Read the architecture, propose changes, contribute code to the actual engine. |

## Where the machine needs help

1. **The consensus-illusion guard** (`mag/memweave.py`) — strengthen independent-agreement
   detection beyond token overlap.
2. **The cache-mining router** (`mag/cache_router.py`) — improve hit-rate and the routing
   decision without leaking cost.
3. **The hologram / right-size curve** (`mag/vram_hologram.py`) — better fidelity vs
   capacity curves; honest, measured, no fake telemetry.
4. **The verkle substrate** (`mag/verkle_knot.py`) — correctness, replay, and verification
   of the hash chain.
5. **The autonomous loop's safety** — human-final-call, visible status, kill-switch, and
   cost/rate caps as first-class, load-bearing features (never afterthoughts).
6. **Grounding** — every claim labeled Supported/Unproven/Disputed + Evidence/Inference/
   Assumption. Primary records beat commentary.

## Non-negotiable rules

- **Never commit secrets.** No API keys, tokens, `providers.yaml`, or `mag-secret.yaml`.
  If a diff touches one, it's rejected. Secrets are presence-only; you never need to read
  a value to build a gate.
- **Never commit the runtime.** No `memory/`, no persona, no biography, no `state/`.
- **Dry-by-default.** Any external side-effect (publish, send, ship, spend) is a dry run
  unless `--live` is explicit.
- **Human final call.** Software never auto-truths. Autonomous surfaces must be visible
  and stoppable.
- **Trust bytes, not reports.** Freeze a spec, verify the finished piece against it, and
  never claim "done" on unverified work.
- **Steal the mechanism, never the content.** Adapt patterns; don't copy private payloads.

## How to contribute

1. Start in the **portable toolkit** — understand the distilled contracts.
2. Open an issue proposing a change to a `framework/` module, naming the real constraint
   it addresses (steer-first, not patch-first).
3. Submit a PR that is: deterministic where possible, gated, dry-by-default, and shipped
   with a test that proves the expected behavior.
4. Every finished piece gets a frozen-spec check (RIB) before it's "done."

## The spirit

This is a republic, not a hierarchy — an exchange of ideas, not a command tree. We offer
the machinery freely and ask only that you honor the one law and the honesty kernel. Take
the mechanism, leave the contents, and build your own. Human final call remains with the
recipient.
