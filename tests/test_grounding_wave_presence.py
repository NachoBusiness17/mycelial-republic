import os
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def rel(p):
    return os.path.join(REPO_ROOT, p)


def test_files_exist():
    files = [
        'handoff/OX_MEGA_claim_grounding_gate.json',
        'handoff/OX_MEGA_recursion_grounding.json',
        'handoff/OX_MEGA2_own_ground_truth.json',
        'handoff/OX_MEGA2_shared_verifiable_ground.json',
        'window/surface.json',
        'tests/test_lattice_grounding.py',
    ]
    missing = [p for p in files if not os.path.exists(rel(p))]
    assert not missing, f"Missing required grounding artifacts: {missing}"


def test_surface_contains_tri_state_and_evidence_supremacy():
    p = rel('window/surface.json')
    assert os.path.exists(p), f"Missing {p}"
    with open(p, 'r', encoding='utf-8') as fh:
        txt = fh.read()
    assert 'tri-state' in txt or 'tri state' in txt, 'window/surface.json lacks "tri-state"'
    assert 'Evidence supremacy' in txt or 'evidence supremacy' in txt, 'window/surface.json lacks "evidence supremacy"'
