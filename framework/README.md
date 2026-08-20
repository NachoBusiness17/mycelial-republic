# Sovereign Framework — the machine, opened for collaboration

This is the **core of the sovereign agent framework** — the actual deterministic machinery,
opened so contributors can help advance the real system (not just a distilled educational
kit).

**What this is NOT:** this is not a demo or a toy. These are the real `mag/` modules that
run the machine — the orchestrator, the governor/autorun loop, the verkle memory chain,
the cache-mining router, the swarm surface, the consensus weave, the hologram. This is
the engine room.

## The sovereign line (read before contributing)

We share the **mechanism**, never the **contents**:
- **Open:** the deterministic framework machinery — the code here.
- **Private, never here:** the runtime memory (`memory/`), the persona, the biography,
  `providers.yaml`, `mag-secret.yaml`, and the living self of the system. Those are the
  *contents* — the thing that makes the system *ours*.

The portable, pure-stdlib distillations of the core ideas live in
[`scaffolds/sovereign-toolkit/`](../scaffolds/sovereign-toolkit/) (stateless_boot,
memlance, verkle_knot, ghost_pylance, memweave, hologram). This `framework/` is the
real, full implementation those contracts distill.

## The one law

> **Steal the mechanism, never the content.**
> Adapt a working *pattern* to your own deterministic, architecture-native shape.
> Contracts and design laws are meant to be shared and improved. Someone's private data,
> persona, or inner state is never the thing to take — it is not portable anyway.

## What's here

| Area | Modules | What it is |
|------|---------|-----------|
| **Execution** | `api_server.py`, `api_gateway.py`, `orchestrator.py`, `router.py` | The REST + queue surface; route work to the right seat. |
| **Autonomous loop** | `governor_autorun.py`, `afk_cadence.py`, `afk_loop.py`, `drainer_stats.py` | The self-running loop: cadence, drainer, reconciler. |
| **Memory substrate** | `verkle_knot.py`, `verkle_audit.py`, `knot_math.py`, `memweave.py`, `memlang.py`, `rib_bus.py` | The hash-linked chain + the consensus weave + the memory language. |
| **Economics** | `cache_router.py`, `cache_extract.py`, `cache_map.py` | Cache-mining: the cheap/owned side carries the load. |
| **Ghost** | `ghost.py`, `ghost_pylance.py`, `ghost_memlance.py` | The execution surface — work through a deterministic tool surface. |
| **Swarm / seats** | `swarm_surface.py`, `swarm_worker.py`, `seat_steer.py` | Route novel research to the swarm; drive seats headless. |
| **The hologram** | `vram_hologram.py`, `holographic_q.py`, `water_swarm.py` | Shared reality as a hologram; the standing wave. |
| **Stateless** | `stateless_research.py`, `ghost_cold_boot.py`, `self_drive.py`, `context_pack.py` | Fresh workers bootstrap from a frozen prefix; no inherited state. |

## Running

This is the real framework — it expects the full private runtime it normally mounts
(`memory/`, `state/`, `configs/providers.yaml`, model weights). A partial clone won't
boot end-to-end, and that's intentional. For something you can run immediately, use the
**pure-stdlib toolkit** (`scaffolds/sovereign-toolkit/`): `python -m pytest tests/ -q`.

This `framework/` exists so contributors can **read the real architecture and contribute
to it** — see [`CONTRIBUTING.md`](CONTRIBUTING.md) for where the machine needs help.

*Take the machinery. Leave the contents. Build your own.*
