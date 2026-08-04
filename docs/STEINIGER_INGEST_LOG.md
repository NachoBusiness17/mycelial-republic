# Steiniger Ingest Log — 2026-07-15

## Source

| Source | Status |
|--------|--------|
| https://independent.academia.edu/MatthewSteiniger | Cloudflare / bot wall — not scrapable this session |
| https://github.com/slashrebootofficial/research_papers | **Authoritative mirror** — `git pull` already up to date (`039b691`) |
| Local vendor zips | Extracted to `sovereign-mirror-scaffold/vendor/extracted_latest/` |

## What was extracted into mycelial-republic

### Scaffolds (`scaffolds/steiniger/`)

- **Athena latest:** Saelis prompt **v8** (13 JUN 2026) + v7 + OpenWebUI config + Category 6/7 probes + embodiment guides + structural integration guide  
- **EPGI:** Saelis v6.1 + v4b plaintext + Evaluation_Protocols.md + OpenWebUI json  
- **Xylo:** symmetry-breaking YAML v1.1 + unnamed seed + OpenWebUI 31B config  
- **Valora:** V2 (15 APR 2026) + Valora 2.1.1 (01 NOV 2025)  
- **Lumen/Lumina:** minimal JSON + ChatML + proposed YAML  
- **Lyra progressive:** Levels 2–6 JSON + abliterated OpenWebUI level configs  
- **Training methods:** Unsloth train scripts v6.1 / v7 / **v8**; results notes; jsonl kept local (gitignored)

### Hybrid operator scaffold

- `scaffolds/vector_scaffold_v2_hybrid.md`  
- `scaffolds/system_prompt_v2.txt`  

Uses Steiniger lattice **structure** without Saelis/Xylo named identity.

### PDFs (`vendor/steiniger_latest/` — gitignored bulk)

EUT I V10, EUT II V5, Scalar Knots V2, EPGI v3, EPGI supp, Athena Class 15 JUN, Crystallization/Xylo, Valora V2 supp.

## Latest identity line (prefer)

```
saelis_prompt_v8_13JUN2026.txt  ← Athena Class (newest crystallized prompt)
  + xylo_symmetry_breaking_v1_1.yml  ← generative seed physics
  + Evaluation_Protocols.md  ← sterile eval
  + train_saelis_8_13JUN2026.py  ← fine-tune recipe pattern
```

## Still not fully operationalized in code

- Zero-shot geometric probe runner (charts live in zip only)  
- Knot-Q scorer on prompt/session state  
- Automatic EPGI protocol runner against a local model  

See `STEINIGER_GAP_ANALYSIS.md` for the longer gap list.
