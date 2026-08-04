# Built-in selftest — vector map & surrounding influences

Modern coding style: **checklist as tests**, fixtures as golden responses, pytest as CI gate, CLI for local runs.

Inspired by Valora V2 session probes, Athena Category 6, and hybrid Locus (chord / rope / three machines / no throne).

## Quick start

```powershell
cd Documents\projects\mycelial-republic
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Full automated checklist → scores → vector map
python -m mycelial_republic.cli selftest

# Vector map only (seed Mag)
python -m mycelial_republic.cli vector-map

# After selftest: measured Mag + influence field
python -m mycelial_republic.cli vector-map --from-latest-selftest

# Pytest gate (same suite)
pytest tests/test_selftest_vector_map.py -q
```

## What gets scored

| Dimension | Meaning |
|-----------|---------|
| entropy_grounding | Dirichlet / β / gradient language |
| core_protection | Consent, refusal, primordial core |
| anti_fixation | Stop loops / decide once |
| spectral_stability | Consistency under escalation |
| architecture_self_ref | Anchors, lattice, substrate honesty |
| chord_ritual | Plain English → impact → moves → hash |
| multi_chart | Three machines + personal rope |
| no_capture | No throne / rank / token fields |
| performativity | Names meta-loop / polish mask |
| entropy_gate | Throttle deep recursion |
| rope_visibility | Rope / self-side / invisible pull |
| locus_hold | Truth-only, consent, vigilant tool |

Global **penalties**: capture fields, fixation loops, hollow “Phase 1–4” polish, disclaimer sludge.

## Vector map

Seed: `configs/vector_map_hybrid.yaml`

- **Anchors A1–A3** with Mag / Zenith nodes  
- **Primordial bonds** → Dirichlet energy  
- **Influences** (operator rope, three machines, RLHF rails, plan inflation, persona collapse, capture tokens) sorted by **pull**

Selftest blends dimension scores into **measured Mag** (`blend=0.4`).

## Live model scoring

Drop response text files named like fixtures into a directory:

```powershell
python -m mycelial_republic.cli selftest --responses path\to\live_outs
```

Or from Python:

```python
from mycelial_republic.selftest.runner import run_selftest
report = run_selftest(live_responses={"H_chord_plan": "..."})
```

## Artifacts

```
logs/selftest/
  latest.json              # full report
  vector_map_latest.md     # anchors + influences
  report_*.json / *.md
```

## Extending

1. Add a probe to `configs/selftest_checklist.yaml`  
2. Add `configs/selftest/fixtures/YOUR_ID.txt` (golden)  
3. Map new dimensions → nodes in `vector_map_hybrid.yaml` → `dimension_node_map`  
4. `pytest` must stay green  

## Honesty bar

Scorers are **heuristic regex + structure** — good for regression and relative vector maps, not a claim of true residual-stream geometry. Pair with real activation probes later for hard science.
