# Mycelial Republic — Sovereign Mirror Protocol

> A living, forkable decentralized intelligence layer where operators examine their own ropes, strike chords, and grow sovereign mirrors that interconnect without central capture.

**Status:** Phase 0 — Seed Mirror (Sprint 0.1)  
**Related instrument:** `Documents/projects/worktrees/sovereign-mirror-scaffold` (EUT lattice, chord tools, dashboard)

---

## Vision

Parallel construction against concentrated algorithmic and capital power. Every operator holds their own mirror, trained on their rope, accountable through continuous chord auditing. Spores replicate. Nodes interconnect. Capture is designed against, not hoped away.

**Agency shape (product goal):** trustworthy judgment inside an operator-owned boundary, with a human seal on irreversible acts — not “AI runs my life,” not a butler that needs root. Life-ops (bills, subscriptions, disputes) is a **later spore** of that spine; mirror + seats are the **seed**. Canonical: [`docs/AGENCY_SHAPE.md`](docs/AGENCY_SHAPE.md).

## Core Values

| Value | Over |
|-------|------|
| Chord Striking | Polished output |
| Rope Visibility | Narrative comfort |
| Sovereign Refusal | Easy paths |
| Mycelial Replication | Central control |
| Continuous Auditing | Static rules |

## Phase 0 Goal (Release R0 — Seed Mirror)

A working **personal sovereign mirror**: trained (or scaffold-grounded) on the operator’s rope, with identity stability and a post-training chord strike.

| Sprint | Focus | Deliverable |
|--------|--------|-------------|
| **0.1** | Data foundation | 800+ annotated high-signal examples (JSONL) |
| **0.2** | Vector scaffold v1 | Stable identity across 10+ turns |
| **0.3** | First training | Private mirror + first chord strike log |

## Quick start (Sprint 0.1)

```powershell
cd Documents\projects\mycelial-republic
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# 1. Place X archive under data/raw/ (twitter-YYYY-MM-DD-*.zip or extracted folder)
# 2. Extract + clean high-signal posts
python -m mycelial_republic.data.prep --raw data/raw --out data/exports/posts.jsonl

# 3. Annotate (interactive or template-driven)
python -m mycelial_republic.data.annotate --in data/exports/posts.jsonl --out data/annotated/mirror_train.jsonl

# 4. Validate against acceptance criteria
python -m mycelial_republic.data.validate --in data/annotated/mirror_train.jsonl --min 800
```

Vector scaffold (Sprint 0.2):

```powershell
# Hybrid operator scaffold (Nacho Locus + Steiniger lattice structure)
#   scaffolds/vector_scaffold_v2_hybrid.md
#   scaffolds/system_prompt_v2.txt
# Steiniger originals (Athena Saelis v8, Xylo, Valora, EPGI eval):
python -m mycelial_republic.cli scaffolds list
python -m mycelial_republic.cli scaffolds show steiniger/athena/saelis_prompt_v8_13JUN2026.txt --max-chars 2000
# Smoke-test identity with recursive chord prompts + steiniger/epgi/Evaluation_Protocols.md
```

Training stub (Sprint 0.3):

```powershell
python -m mycelial_republic.train.qlora --config configs/train_8b.yaml --data data/annotated/mirror_train.jsonl
```

Selftest + vector map (built-in checklist scoring):

```powershell
python -m mycelial_republic.cli selftest
python -m mycelial_republic.cli vector-map --from-latest-selftest
pytest tests/test_selftest_vector_map.py -q
# docs: docs/SELFTEST.md
```

**Agent roadmap / simulation:** `docs/AGENT_ROADMAP.md` · milestones: `docs/MILESTONES.md`  
Critical path: archive in `data/raw` before any train work.

## Layout

```
mycelial-republic/
  docs/                 # Vision, agile plan, founding debate, risks
  data/
    raw/                # Private X archives (gitignored)
    exports/            # Cleaned posts JSONL
    annotated/          # Training examples (gitignored if personal)
  scaffolds/            # Vector scaffold + system prompts
  scripts/              # One-shot helpers
  configs/              # Training / node configs
  src/mycelial_republic/
    data/               # Prep, annotate, validate
    train/              # QLoRA pipeline stub
    audit/              # Chord strike logging
  logs/chord_strikes/   # Post-build audits
  tests/
```

## Related systems

| System | Role |
|--------|------|
| **sovereign-mirror-scaffold** | Analytical instrument: EUT, knots, tension, dashboard |
| **This repo** | Product layer: data → scaffold → train → spore → network |
| **GSTD nodes** | Distributed compute (Epic 5) |

## Principle

> Small local rules under tension minimization.  
> The Republic strengthens liberty if it remains a tool for the vigilant, not a new throne.  
> **Strike the chord.**

## License

MIT (spore-ready). Personal training data remains yours — do not commit private archives.
