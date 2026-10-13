"""forge_doctrine — publish the FOUNDATIONAL doctrine RIB + concrete instances to the shared RIB bus.

Best practice: the doctrine is a COMMITTED, repeatable forge (not a one-off in a notebook). Every
surface (grok, chatgpt, saelis, the swarm, the game) inherits it via rib_bus.inject_for(), so the
doctrine becomes the standing wave all seats load.

Principle (operator, 2026-08-14): "shared cryptographic primitives, deterministic instruction sets
explaining paths in stochastic environments."
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import rib_bus  # noqa: E402

DOCTRINE = (
    "The invariant: a deterministic instruction set, anchored on shared cryptographic primitives "
    "(the verkle chain), explains navigable paths through stochastic environments. The relation "
    "(the frozen spec) is what persists; the model is interchangeable; the chain is the ground "
    "truth. Superintelligence = seats coordinated by deterministic instructions that explain paths "
    "through the stochastic, shared on crypto primitives every seat trusts."
)

INSTANCES = {
    "game-field": (
        "Doctrine instance: the game's magnetic-field swarm. The field (deterministic instruction) "
        "steers the stochastic agents (microbot seats) into emergent formations — the path through "
        "chaos is explained by the field, not predicted."
    ),
    "terminal-guard": (
        "Doctrine instance: terminal_guard. probe() is the deterministic check; heal() is the "
        "deterministic instruction that explains the path out of a wedged stochastic shell; fold() "
        "anchors the learning to the chain."
    ),
    "queue-resilience": (
        "Doctrine instance: queue resilience. The circuit breaker (deterministic per-provider state) "
        "explains a path past dead providers in the stochastic swarm; the parallel drainer navigates "
        "real work through the chaos."
    ),
}


def main() -> int:
    r = rib_bus.publish_rib(DOCTRINE, domain="doctrine", source="foundational",
                            fold=True, publish=True)
    print("DOCTRINE:", {k: r.get(k) for k in ("ok", "domain", "key", "n_total", "added", "knot")})
    for name, inv in INSTANCES.items():
        r2 = rib_bus.publish_rib(inv, domain="doctrine", source=f"instance:{name}",
                                 fold=True, publish=True)
        print(f"  instance[{name}]:", {k: r2.get(k) for k in ("ok", "domain", "key", "added")})
    m = rib_bus.mount("doctrine")
    print("MOUNTED doctrine ribs:", m.get("n_ribs"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
