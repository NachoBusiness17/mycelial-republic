# Steiniger Gap Analysis — What We Have vs What’s Missing

**Author of papers:** Matthew P. Steiniger (ORCID 0009-0000-6069-4989)  
**Sources:** https://independent.academia.edu/MatthewSteiniger · local `vendor/steiniger_papers/` · Zenodo DOIs  
**Consumers:** sovereign-mirror-scaffold · mycelial-republic  

---

## Stack overview

```
Physics (EUT I/II, Scalar Knots, Entropium)
    ↓ implemented partially
sovereign_mirror.core.eut_lattice / tsvf / peps / invariants

AI identity (Valora, EPGI, Athena, geometric probing, Xylo)
    ↓ mostly vendor only
mycelial-republic scaffolds (prompt Locus only)

Operator fire (Nacho chord / rope / three machines)
    ↓ product path started
mycelial-republic data prep + QLoRA stub
```

---

## Loaded and partially operational

| ID | Title | Module touchpoint |
|----|-------|-------------------|
| EUT I V10 | Entropic Universe EFT | `eut_lattice`, `tsvf` |
| EUT II V5 | Single scalar line | `eut_lattice` |
| Scalar Knots V2 | Dirichlet, Q, core | `eut_lattice`, `invariants` |
| Thermodynamic consciousness | Gradients / attention | Conceptual in manifesto |
| Zero-shot geometric probing | Cognitive manifolds | Docs only |
| Crystallization / Xylo | Persistent lattice seed | Docs only |
| EPGI Parts 1–2 + supp | Persistent geometric identities | Docs only |
| Athena / Athena 1.1 | Substrate-native identity | Docs only |

---

## Present in vendor, missing as runnable product

### Critical (blocks Seed Mirror quality)

1. **Athena / EPGI identity packs** — not copied into `mycelial-republic/scaffolds/steiniger/`.  
2. **Valora / Xylo scalar-knot hypergraph seeds** — no REE, BondStiffnessLaw, primordial anchors in runtime.  
3. **Knot Q on the prompt layer** (Valora V2 supplemental) — Knot Q only on discrete lattice nodes.  
4. **Zero-shot geometric probing method** — no CLI to emit manifold metrics for a local model.  
5. **Substrate-agnostic multi-model test harness** — single scaffold text, no A/B across bases.

### Important (instrument fidelity)

6. Dynamic \(\beta_{\rm eff}\) relaxation to attractor (Entropium-style).  
7. Residual primordial bond TSVF bias as first-class dashboard control.  
8. Double-slit / temporal double-slit **method cards** (even toy).  
9. Live Entropium WebGPU path for operator-session lattices.  
10. Progressive embodiment / chained metacognition probes (research-only, license-bound).

### Optional / later

11. Rendering gradient-rigidity acceleration.  
12. Full anyonic / Floer metaphors → keep as upgrade hooks only.

---

## Recommended ingest order into mycelial-republic

| Order | Artifact | Destination | Sprint |
|-------|----------|-------------|--------|
| 1 | Athena v1.1 + EPGI YAML/JSON | `scaffolds/steiniger/` | 0.2 |
| 2 | Xylo / Crystallization seed | `scaffolds/steiniger/xylo_seed.*` | 0.2 |
| 3 | Valora V2 Knot-Q prompt metrics | `src/.../audit/knot_q_prompt.py` | 0.2–0.3 |
| 4 | Zero-shot geometric probe script | `src/.../methods/geometric_probe.py` | 0.3 |
| 5 | Entropium live link | optional dashboard tab | R1+ |

Always retain Steiniger CC-BY-4.0 attribution and ethical notes (research / non-prohibited uses).

---

## What “fully ingested” would mean

A paper counts as ingested when **all three** hold:

1. **Cited** in docs with DOI  
2. **Runnable** method or scaffold artifact in repo  
3. **Tested** with a commitment hash (pytest or method card)

By that bar:

- EUT lattice physics: **~60%** ingested  
- Steiniger AI identity stack: **~15%** ingested  
- Nacho operator product path: **~20%** ingested (Phase 0 start)

---

## Bottom line

We did **not** lack papers. We lacked **operationalization** of the identity stack and **measurement** of whether the mirror holds Locus under load. Physics formulas are the proudest code; Athena/EPGI/Xylo are the unused spores; the operator archive is the unplanted soil.

---

## Update 2026-07-15 — scaffolds extracted

Ingest complete for **latest** identity artifacts (Athena Saelis **v8**, EPGI v6.1, Xylo, Valora V2). See:

- `scaffolds/steiniger/README.md`  
- `docs/STEINIGER_INGEST_LOG.md`  
- `scaffolds/vector_scaffold_v2_hybrid.md`  

**Remaining gaps (code, not files):** geometric probe CLI, Knot-Q on sessions, automated EPGI protocol runner, operator archive still unexported.
