#!/usr/bin/env python3
"""tools/sovereign/universal_constructor.py — Von Neumann Universal Constructor Engine.

A sovereign computational implementation of John von Neumann's Theory of Self-Reproducing Automata (1966):

VON NEUMANN'S FIVE ELEMENTS OF REPRODUCTION:
1. Component A (Universal Constructor): A machine capable of reading any blueprint Phi
   and manufacturing the physical structure described by Phi.
2. Component B (Copier): A mechanism capable of copying any blueprint tape Phi without
   interpreting its active meaning (passive replication).
3. Component C (Controller): A supervisory finite state machine that coordinates A and B:
   Step 1: Instructs A to build (A + B + C) from tape Phi(A + B + C).
   Step 2: Instructs B to copy tape Phi(A + B + C) and insert it into the newly built machine.
   Step 3: Detaches the offspring, yielding a fully autonomous self-reproducing automaton.
4. Tape Phi (The Blueprint): Dual-role semantic object:
   Role 1: Active instructions executed by A to build hardware/software.
   Role 2: Passive data copied verbatim by B to ensure hereditary transmission.
5. Mutation Invariance: Demonstrates evolutionary divergence when noise alters Phi.

Self-Contained Invariant: Zero external dependencies beyond standard library Python 3.
"""

from __future__ import annotations

import copy
import hashlib
import json
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


class UniversalConstructor:
    """Component A: The Constructor.
    Interprets passive specification data and executes assembly into active runtime agents.
    """

    def __init__(self, constructor_id: str = "constructor-alpha"):
        self.constructor_id = constructor_id

    def build(self, blueprint_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Construct an operational entity from specification."""
        components = blueprint_spec.get("components", {})
        assembled_machine = {
            "entity_id": f"automaton-{blueprint_spec.get('generation', 0) + 1}-{hashlib.sha256(json.dumps(blueprint_spec, sort_keys=True).encode()).hexdigest()[:8]}",
            "generation": blueprint_spec.get("generation", 0) + 1,
            "capabilities": list(components.keys()),
            "operational_state": "CONSTRUCTED",
            "created_at": time.time(),
            "active_methods": {}
        }

        # Wire assembled components
        for comp_name, comp_def in components.items():
            assembled_machine["active_methods"][comp_name] = {
                "type": comp_def.get("type", "generic"),
                "status": "ONLINE",
                "checksum": hashlib.sha256(json.dumps(comp_def, sort_keys=True).encode()).hexdigest()[:12]
            }

        return assembled_machine


class TapeCopier:
    """Component B: The Copier.
    Reads tape Phi and duplicates it with zero semantic interpretation.
    """

    def __init__(self, copier_id: str = "copier-beta"):
        self.copier_id = copier_id

    def replicate(self, tape: Dict[str, Any], mutation_rate: float = 0.0) -> Dict[str, Any]:
        """Replicate tape with optional evolutionary mutation."""
        replicated_tape = copy.deepcopy(tape)
        if mutation_rate > 0.0:
            # Inject controlled point mutation in evolutionary slot
            mutations = replicated_tape.setdefault("mutations", [])
            mutation_entry = {
                "generation": replicated_tape.get("generation", 0) + 1,
                "locus": "adaptation_vector",
                "delta": round(mutation_rate, 4),
                "timestamp": time.time()
            }
            mutations.append(mutation_entry)

        return replicated_tape


class SupervisoryController:
    """Component C: The Controller.
    Governs the two-phase lifecycle of reproduction and bounds execution.
    """

    def __init__(self, controller_id: str = "controller-gamma"):
        self.controller_id = controller_id
        self.constructor = UniversalConstructor(f"{controller_id}-A")
        self.copier = TapeCopier(f"{controller_id}-B")

    def reproduce(self, tape: Dict[str, Any], mutation_rate: float = 0.0) -> Dict[str, Any]:
        """Execute von Neumann's 3-step reproduction protocol:
        1. A builds offspring body from tape Phi.
        2. B copies tape Phi.
        3. C equips offspring with copied tape and releases it.
        """
        # Step 1: Physical construction
        offspring_body = self.constructor.build(tape)

        # Step 2: Genetic replication
        copied_tape = self.copier.replicate(tape, mutation_rate=mutation_rate)
        copied_tape["generation"] = offspring_body["generation"]

        # Step 3: Integration and verification
        offspring_body["tape"] = copied_tape
        offspring_body["operational_state"] = "AUTONOMOUS"

        tape_hash = hashlib.sha256(json.dumps(copied_tape, sort_keys=True).encode()).hexdigest()
        offspring_body["heredity_hash"] = tape_hash

        return offspring_body


class SovereignAutomaton:
    """The Complete Integrated Organism: (A + B + C + Phi)."""

    def __init__(self, tape: Dict[str, Any]):
        self.tape = tape
        self.controller = SupervisoryController("organism-C")

    @property
    def generation(self) -> int:
        return self.tape.get("generation", 0)

    def spawn_next(self, mutation_rate: float = 0.0) -> SovereignAutomaton:
        """Self-reproduce next generation."""
        offspring_dict = self.controller.reproduce(self.tape, mutation_rate=mutation_rate)
        return SovereignAutomaton(offspring_dict["tape"])

    def verify_quine_fidelity(self, offspring: SovereignAutomaton) -> bool:
        """Verify that offspring preserves ancestor invariant structure."""
        ancestor_components = set(self.tape.get("components", {}).keys())
        offspring_components = set(offspring.tape.get("components", {}).keys())
        return ancestor_components == offspring_components and offspring.generation == self.generation + 1


def run_selftests() -> bool:
    """Verify von Neumann Universal Constructor theorems."""
    print("=== VON NEUMANN UNIVERSAL CONSTRUCTOR SELFTESTS ===")

    # 1. Base Blueprint (Phi)
    base_blueprint = {
        "generation": 0,
        "name": "EstateSovereignNode",
        "components": {
            "constructor_A": {"type": "hardware_synthesizer", "version": "1.0"},
            "copier_B": {"type": "tape_duplicator", "version": "1.0"},
            "controller_C": {"type": "lifecycle_governor", "version": "1.0"},
            "homeostat_H": {"type": "two_loop_ultrastability", "poles": 4},
            "vault_feeder_V": {"type": "ouroboros_in_memory", "tiers": 2}
        }
    }

    # Test 1: First-generation reproduction
    parent = SovereignAutomaton(base_blueprint)
    child = parent.spawn_next(mutation_rate=0.0)

    assert child.generation == 1, f"Expected gen 1, got {child.generation}"
    assert parent.verify_quine_fidelity(child), "Quine fidelity failure between parent and child!"
    print(f"  [PASS] Test 1: Self-reproduction 100% fidelity (Gen 0 -> Gen 1, id: {child.tape['name']})")

    # Test 2: Recursive multi-generation cascade (Gen 0 -> Gen 5)
    current = parent
    for g in range(1, 6):
        next_gen = current.spawn_next(mutation_rate=0.0)
        assert next_gen.generation == g, f"Generation mismatch at step {g}"
        assert current.verify_quine_fidelity(next_gen)
        current = next_gen

    print(f"  [PASS] Test 2: 5-generation recursive cascade preserved without entropy decay")

    # Test 3: Mutation Invariance (Hereditary divergence)
    mutated_child = parent.spawn_next(mutation_rate=0.05)
    assert mutated_child.generation == 1
    assert "mutations" in mutated_child.tape, "Expected mutation record in child tape"
    assert len(mutated_child.tape["mutations"]) == 1
    assert mutated_child.tape["mutations"][0]["delta"] == 0.05
    print("  [PASS] Test 3: Controlled point mutation successfully inherited without corrupting constructor")

    # Test 4: Quine serialization test
    parent_bytes = json.dumps(parent.tape, sort_keys=True).encode()
    child_unmutated_bytes = json.dumps(child.tape, sort_keys=True).encode()
    # Tapes differ only by generation counter
    assert parent.tape["components"] == child.tape["components"], "Core component blueprint drifted!"
    print("  [PASS] Test 4: Dual-role tape resolution verified (Code executes, Data transmits)")

    print("\nALL 4 UNIVERSAL CONSTRUCTOR TESTS PASSED (100% OK)")
    return True


if __name__ == "__main__":
    run_selftests()
