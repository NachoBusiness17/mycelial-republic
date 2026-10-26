# Master Build Notes — v6.0 Consolidated

**Built:** 2026-09-26 (America/New_York)  
**Deliverable:** `/workspace/research-brief/ENDOGENOUS_CAPABILITY_ACCUMULATION_MASTER.md`  
**Method:** Synthesize v5 + pre-reg + SCS design + open questions + citation audit + changelog; WebSearch/WebFetch + HTTP checks for links; lessons (not dump) from socratic gap analysis.

## Sources synthesized

| Source | Use |
|--------|-----|
| `v5-endogenous-capability-accumulation.md` | Primary scientific content |
| `v5-extended-abstract.md` | Abstract compression |
| `fle-pilot-preregistration.md` | §11 design condensation |
| `scs-design.md` | §12 architecture condensation |
| `scs-mvp/` | §12.5 toy MVP pointer (C blocks Comp; D_aff Comp→Challenge retain/forget; stub Y; not FLE) |
| `sim/README.md` | §12.6 toy metric sim mention |
| `open-questions.md` | §14.3 P0-first tracker |
| `socratic-gap-analysis.md` | Lessons §3.3 only |
| `audit-citations-literature.md` | Venue-honest citation status |
| `v5-changelog-from-v4.md` | Traceability |

## Link verification (HTTP 200 unless noted)

### Papers / DOI / arXiv — VERIFIED

| Item | URL checked |
|------|-------------|
| Darwiche & Marquis JAIR | https://doi.org/10.1613/jair.989 · https://www.jair.org/index.php/jair/article/view/10311 · https://arxiv.org/abs/1106.1819 |
| Option-Critic | https://arxiv.org/abs/1609.05140 · https://doi.org/10.1609/aaai.v31i1.10916 |
| DIAYN | https://arxiv.org/abs/1802.06070 |
| POET | https://arxiv.org/abs/1901.01753 |
| Enhanced POET | https://arxiv.org/abs/2003.08536 |
| OMNI | https://arxiv.org/abs/2306.01711 |
| EWC arXiv + PNAS | https://arxiv.org/abs/1612.00796 · https://www.pnas.org/doi/10.1073/pnas.1611835114 |
| Toolformer | https://arxiv.org/abs/2302.04761 |
| FLE | https://arxiv.org/abs/2503.09617 |
| CSRO | https://arxiv.org/abs/2603.10098 |
| Opponent shaping | https://arxiv.org/abs/2510.08255 |
| Bowman oversight | https://arxiv.org/abs/2211.03540 |
| Foldit Nature | https://doi.org/10.1038/nature09304 |
| LegoNE Nat Comm | https://www.nature.com/articles/s41467-026-74003-1 |
| Jain & Parkes TEAC | https://doi.org/10.1145/2399187.2399190 |
| Acemoglu & Restrepo AER | https://doi.org/10.1257/aer.20160696 |
| Sutton options DOI | https://doi.org/10.1016/S0004-3702(99)00052-1 (DOI form; ScienceDirect may paywall) |

### Code / platforms — VERIFIED

| Item | URL |
|------|-----|
| FLE GitHub | https://github.com/JackHopkins/factorio-learning-environment |
| factorioctl | https://github.com/MarkMcCaskey/factorioctl |
| Gymnasium | https://github.com/Farama-Foundation/Gymnasium |
| PettingZoo | https://github.com/Farama-Foundation/PettingZoo |
| HELM | https://github.com/stanford-crfm/helm |
| OpenAI Evals | https://github.com/openai/evals |
| Inspect AI | https://inspect.aisi.org.uk/ |
| MLflow + Registry docs | https://github.com/mlflow/mlflow · https://mlflow.org/docs/latest/ml/model-registry/ |
| Garak | https://github.com/NVIDIA/garak |
| PyRIT docs | https://microsoft.github.io/PyRIT/latest/ |
| Avalanche | https://github.com/ContinualAI/avalanche |
| LangChain | https://github.com/langchain-ai/langchain |
| LlamaIndex | https://github.com/run-llama/llama_index |
| Gray Swan | https://grayswan.ai/ |
| OSF | https://osf.io/ |
| AsPredicted | https://aspredicted.org/ |
| COS Prereg | https://www.cos.io/initiatives/prereg |

### Partial / alternate

| Item | Notes |
|------|-------|
| Deci, Koestner & Ryan 1999 DOI `10.1037/0033-2909.125.6.627` | APA DOI / PsycNet returned HTTPError from this host; **verified alternate:** https://selfdeterminationtheory.org/wp-content/uploads/2014/04/1999_DeciKoestnerRyan_Meta.pdf (used in master) |
| Arrow 1962 / Romer 1990 | Classic print journals; no single canonical open DOI required; cited venue-honest without fabricated links |
| MACROPS / Korf / Soar chunking | Cited from v5/audit as FOUND literature; Springer Soar chunking DOI 10.1007/BF00116249 known from audit; not re-HEAD-checked in this pass |
| Ryan & Deci 2000 *American Psychologist* | Standard SDT citation; not separately HEAD-checked |
| Model cards arXiv:1810.03993 | Referenced as industry pattern; not separately HEAD-checked in this pass |

### Failed

| Item | Result |
|------|--------|
| Deci 1999 APA DOI resolver | HTTPError from build host — mitigated via SDT.org PDF |

### Intentionally demoted (not “failed”)

- **Gray Swan Arena** — live product site verified; demoted from four-arm substrate to Challenge analogy only (per v5/audit).

## Word count

Final master ≈ **~8.0k words** (stdlib `str.split()`), substantive consolidation in target band (~8k–14k). No Nature rhetoric; MAG composition residual stated honestly.

## Deliverable check

- [x] File exists at specified path  
- [x] Self-contained (reader need not open other files)  
- [x] Many https links actually looked up  
- [x] SCS MVP subsection points to `/workspace/research-brief/scs-mvp/`, demo behaviors, toy-not-FLE  
- [x] This build notes file lists verified vs failed  
