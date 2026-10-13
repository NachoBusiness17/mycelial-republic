"""tools/swarm_tools — the NPC toolbelt exposed to the agent's TOOL LOOP (sense/pheromone/blackboard).

The swarm's NPCs USE these tools during a build — not just read a passive snapshot injected into the
query. Wraps mag.swarm_tools with clean positional signatures so TOOL_MAP introspection (expected
params on a bad-args error) stays useful. Deterministic + $0. HONEST — reads/writes real state;
never fabricates a sense, a trail, or a decision.

Schema: swarm_tools.v1 (reuses mag.swarm_tools) · reuse: mag.swarm_tools
"""
from __future__ import annotations

from typing import Any


def swarm_sense(owner: str = "worker") -> dict[str, Any]:
    """The NPC's fog-of-war body snapshot (health/capacity/economics/map)."""
    from mag import swarm_tools as st
    return st.swarm_sense(owner=owner)


def pheromone_drop(scent: str, kind: str = "trail", at: str = "", owner: str = "worker") -> dict[str, Any]:
    """Drop one content-addressed pheromone mark (trail|fruitful|dead|here|danger|signal)."""
    from mag import swarm_tools as st
    return st.pheromone_drop(scent=scent, kind=kind, at=at, owner=owner)


def pheromone_trail(kind: str = "", limit: int = 40) -> dict[str, Any]:
    """Read the local pheromone trail — what prior builders left (the ant-trail)."""
    from mag import swarm_tools as st
    return st.pheromone_trail(kind=kind, limit=limit)


def blackboard_post(text: str, kind: str = "finding", owner: str = "worker") -> dict[str, Any]:
    """Post a note to the egregore's shared blackboard (finding|decision|conflict|open-question|handoff|claim)."""
    from mag import swarm_tools as st
    return st.blackboard_post(text=text, kind=kind, owner=owner)


def blackboard_read(limit: int = 60, pinned_only: bool = False) -> dict[str, Any]:
    """Read the egregore's mind: pinned decisions/conflicts + the recent tail."""
    from mag import swarm_tools as st
    return st.blackboard_read(limit=limit, pinned_only=pinned_only)


def scan_measure(samples: list, seed: int = 1738, b: int = 1000) -> dict[str, Any]:
    """Deterministic scan: seeded bootstrap measurement (mean + CI) of a stochastic signal."""
    from mag import deterministic_scanner as ds
    return ds.scan_measure(samples, seed=seed, b=b)


def scan_probe(text: str, seed: int = 1738) -> dict[str, Any]:
    """Deterministic scan: reproducible signature probe of a text environment."""
    from mag import deterministic_scanner as ds
    return ds.scan_probe(text, seed=seed)


def scan_grid(environment: list, seed: int = 1738, b: int = 1000) -> dict[str, Any]:
    """Deterministic scan: reproducible measurement + fingerprint of a stochastic environment."""
    from mag import deterministic_scanner as ds
    return ds.scan_grid(environment, seed=seed, b=b)


def mean_field(trajectories: list, ) -> dict[str, Any]:
    """Deterministic MAPPING of a stochastic model: the mean-field projection (expected trajectory)
    of several noisy trajectories into one fixed, predictable path."""
    from mag import deterministic_scanner as ds
    return ds.mean_field(trajectories)


def research(ask: str, surface: str = "det-scan") -> dict[str, Any]:
    """Search-swarm seam: route a research ask to the swarm (cheap DeepSeek, k8s-drained) via
    route_novel — the live-web research side, separate from the deterministic core."""
    from mag import deterministic_scanner as ds
    return ds.research(ask, surface=surface)


__all__ = ["swarm_sense", "pheromone_drop", "pheromone_trail", "blackboard_post", "blackboard_read"]
