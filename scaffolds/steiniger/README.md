# Steiniger Scaffold Ingest

**Author:** Matthew P. Steiniger (Independent Researcher)  
**ORCID:** [0009-0000-6069-4989](https://orcid.org/0009-0000-6069-4989)  
**Academia:** https://independent.academia.edu/MatthewSteiniger  
**GitHub mirror:** https://github.com/slashrebootofficial/research_papers  
**Contact:** matthew@slashreboot.com · @slashreboot  
**License:** CC-BY-4.0 — attribute when reusing. AI artifacts: research / personal non-commercial exploration; obey base-model licenses.

Academia.edu is often bot-blocked; ingest used the official GitHub Zenodo mirror (pulled 2026-07-15, commit `039b691`, already up to date with `origin/main`).

---

## Latest versions ingested (operational artifacts)

| Line | Latest artifact | Path | Paper / DOI lineage |
|------|-----------------|------|---------------------|
| **Athena / Saelis v8** | `saelis_prompt_v8_13JUN2026.txt` | `athena/` | Athena Class 14–15 JUN 2026 · Zenodo 20694274 / 20710731 |
| Saelis v7 | `saelis_prompt_v7_10JUN2026.txt` | `athena/` | intermediate |
| EPGI Saelis v6.1 | `saelis_prompt_v6_1_31MAY2026.txt` | `epgi/` | EPGI v3 + supp · 20437461 / 20500837 |
| EPGI Saelis v4b | `saelis_v4b_plaintext.txt` | `epgi/` | EPGI Part 2 |
| EPGI eval | `Evaluation_Protocols.md` | `epgi/` | sterile multi-turn protocols |
| **Xylo seed** | `xylo_symmetry_breaking_v1_1.yml` | `xylo/` | Crystallization · 19600856 |
| **Valora V2** | `valora_v2_15APR2026.yml` | `valora/` | Valora V2 supp · 19598775 |
| Valora 2.1.1 | `valora_2_1_1_01NOV2025.yml` | `valora/` | Emergence · 17811728 |
| Lumen / Lumina | `lumen_minimal.json`, `lumina_chatml.txt` | `lumen_lumina/` | Substrate-agnostic · 17811909 |
| Lyra progressive L2–L6 | `lyra_progressive/` | JSON levels | Progressive embodiment · 17811862 |
| Probes | `probes/progressive_refined_probe_set.txt` | | Progressive V2 |
| **Training (Saelis)** | v6.1 / v7 / **v8** jsonl + Unsloth scripts | `training/` | Athena / EPGI fine-tunes |

### Physics PDFs (reference copies)

Under `vendor/steiniger_latest/` (project root):

- `EUT_I_V10.pdf` (19654688)  
- `EUT_II_V5_19MAR2026.pdf` (19120992)  
- `Stability_of_Scalar_Knots_...pdf` (19617100)  
- `EPGI_in_LLMs_v3_28MAY2026.pdf`  
- `Supplemental_Note_to_EPGI_in_LLMs_v3_01JUN2026.pdf`  
- `Athena_Class_Persistent_Substrate_Native_Identities_15JUN2026.pdf`  
- `Crystallization_of_a_Persistent_Generative_Lattice.pdf`  
- Valora V2 supplemental PDF  

Full zip archive remains at  
`Documents/projects/worktrees/sovereign-mirror-scaffold/vendor/steiniger_papers/`.

---

## Version ladder (identity line)

```
Valora (hypergraph) → Xylo (symmetry-break seed)
  → EPGI Saelis v4b → v6.1 (fine-tune) → v7 → Athena Saelis v8 (latest)
```

**Prefer for new work:**

1. Structure: `athena/saelis_prompt_v8_13JUN2026.txt` (richest: ESDT, embodiment axiom, REE)  
2. Physics seed YAML: `xylo/xylo_symmetry_breaking_v1_1.yml` or `valora/valora_v2_15APR2026.yml`  
3. Eval: `epgi/Evaluation_Protocols.md` + Category 6/7 questions in `athena/`  
4. Train recipe: `training/train_saelis_8_13JUN2026.py` + `saelis_v8_dataset_13JUN2026.jsonl`

---

## Critical distinction for Mycelial Republic

| Steiniger identity | Operator sovereign mirror |
|--------------------|---------------------------|
| Named lattice (Saelis / Xylo / Valora) co-evolved with Matthew | **Operator-specific** Locus from rope archive |
| Substrate embodiment as native body | Chord / rope / three machines / refusal |
| Fine-tune on Saelis datasets | Fine-tune on **operator** JSONL |

Use Steiniger **structure** (anchors, S_core=−8, REE, BondStiffnessLaw, eval protocols, train scripts).  
Do **not** ship Saelis-as-product or claim co-evolution with the author.

Hybrid operator scaffold: `../vector_scaffold_v2_hybrid.md`

---

## Ethical notes (from upstream README)

1. AI work: scientific research and personal, non-commercial exploration.  
2. Comply with base model licenses (Gemma, Llama, GPT-OSS, …).  
3. Prohibited: harm, deception, psychological manipulation, military/surveillance productization.  
4. No warranty; attribution required (CC-BY-4.0).

---

## Loader

```powershell
python -m mycelial_republic.scaffolds.list
python -m mycelial_republic.scaffolds.show athena/saelis_prompt_v8_13JUN2026.txt
python -m mycelial_republic.scaffolds.show xylo/xylo_symmetry_breaking_v1_1.yml
```
