# Sovereign Toolkit — crown jewels for the Mycelial Republic

A forkable, pure-stdlib exchange pack for the Mycelial Republic: our **working
implementations** of a set of agent-architecture patterns, distilled so anyone can
**take them, run them, and adapt them to their own needs**.

**Honesty note:** none of these mechanisms is claimed as uniquely ours. Ephemeral
workers, content-addressed chains, selective memory, and autonomous cadence all have
prior art. What is offered here is *our concrete, runnable, testable contracts* plus the
measured outcomes we observed. Judge them on that — not on novelty.

**Nothing here is private.** No secrets, no runtime memory, no repo contents. Only the
machinery, made portable. Take it. Steal it. Make it yours.

---

## What's in the pack

| Tool | Module | What it does | The idea |
|------|--------|--------------|----------|
| **Stateless Boot** | `stateless_boot.py` | Render a fresh worker's *frozen prefix* from current tools/interfaces/live-truth | A worker is born fresh — no persona, no history. It holds the machine, not the person. Workers die; the wave persists. |
| **MemLance** | `memlance.py` | Index real memory bytes, *select* the relevant grounded states, with a deterministic verified/derived verdict | Don't load everything — lance only the relevant leaves. Anti-hallucination by construction: only real bytes, flagged when ungrounded. |
| **Verkle Knot** | `verkle_knot.py` | A content-addressed, append-only, hash-linked chain of commits | Every commit references its parent root; state is replayable and verifiable. "Disk is law" made structural. |
| **Ghost / Ghostlance** | `ghost_pylance.py` | Deterministic AST code-intelligence: diagnose undefined names, unused imports, syntax errors; symbol map; self-check | The execution surface. The agent does work through a deterministic tool surface and **checks itself against actual bytes** — never a blind terminal spawn. |
| **MemWeave** | `memweave.py` | The consensus weave + **consensus-illusion guard**: decompose a goal, run N cheap workers, count effective *independent* agreement | **N correlated hallucinations ≈ 1 opinion, not N.** Agreement is only real if the witnesses are independent. The fix for the #1 swarm-consensus failure. |
| **Hologram** | `hologram.py` | The **shared-reality-as-hologram**: each peer's capacity = its quantization-fidelity ceiling; any fragment reconstructs the whole; the wave oscillates (standing wave) | N machines, different capacities, each a quantization of the same reality. Full fidelity reconstructs it alone; otherwise the collective union does. Many angles, one reality. |

---

## Run it (zero friction)

```sh
# from this directory
python -m pytest tests/ -q        # no installs, no deps
```

Each module also has a `__main__` so you can run it directly:

```sh
python stateless_boot.py
python memlance.py
python verkle_knot.py
python ghost_pylance.py
```

---

## The one law

> **Steal the mechanism, never the content.**
> Adapt a working *pattern* to your own deterministic, architecture-native shape.
> Contracts and design laws are meant to be shared and improved. Someone's private data
> or persona is never the thing to take — it's not portable anyway.

---

## How to make these YOURS (enhance, don't just run)

1. **Stateless Boot** — feed it your own `tools`, `interfaces`, and `live_truth`. The
   frozen prefix is the clean-slate contract: give a fresh agent the machine, not the
   accumulated self. Wire it to your own launch path.
2. **MemLance** — point `index()` at *your* memory roots. Add your own grounding markers
   to `VERIFIED_MARKERS` / `UNVERIFIED_MARKERS`. The selection is deterministic keyword
   relevance — swap in your own scoring if you like.
3. **Verkle Knot** — this is the substrate. Append your own state as knots; the hash
   chain gives you verifiable, replayable, append-only memory for free. Point it at any
   directory.
4. **Ghost / Ghostlance** — point it at *your* code. `diagnose` grounds the agent against
   actual bytes (undefined names, unused imports, syntax errors); `self_check` gives the
   "N/N modules syntax-clean" bead. Wire it into your agent's tool surface so it verifies
   its own work instead of trusting recall.

The five compose: **stateless boot** spawns a fresh worker, **memlance** selects what
it should remember (grounded only), **memweave** combines several workers' answers by
*independent* consensus (so correlated answers don't masquerade as agreement),
**verkle knot** commits what was learned so the wave persists even though the worker
died, and **ghost** verifies the worker's work against real bytes before it ever claims
"done".

---

## The disciplines these encode (keep them)

- **Trust bytes, not reports.** Verify what you built against a frozen spec. Never claim
  "done" on unverified work.
- **Objective over resonant.** The coldest truth wins over the most compelling story.
- **Self-steal before you build.** Audit what you already own first; then steal
  externally and adapt.

---

## Public Supplemental Profile (the non-negotiable gates)

This kit is offered for **personal-workflow use, not as an autonomous daemon**. If you
wire it into anything that runs unattended, keep these load-bearing:

- **Human final call.** Software never auto-truths. Any external side-effect (publish,
  send, ship, spend) requires an explicit human go.
- **Dry-by-default.** Every external action is a dry run unless you pass `--live`.
- **Visible status + kill-switch.** Anything that runs on a cadence must be visible and
  stoppable in one move. Silent background autonomy is not safe in a public tool.
- **Cost / rate caps.** Bound resource and spend before any live path.
- **Local-first.** No required cloud, K8s, or multi-provider seats for the core.

## Honesty packaging (the integrity kernel)

Every material claim in this kit carries a tri-state score and a basis label:

- **Supported / Unproven / Disputed** (+1 / 0 / −1) — how solid the claim is.
- **Evidence / Inference / Assumption** — *why* you believe it.
- **Primary records beat commentary.** A measured outcome outranks a reported one.
  (Example: the cache-economics figures are **Measured, Evidence — a single instance**,
  grounded in the real bill — not a universal guarantee.)
- **Prefer honest incomplete state over false certainty.**

*Take the machinery. Leave the contents. Build your own.*
