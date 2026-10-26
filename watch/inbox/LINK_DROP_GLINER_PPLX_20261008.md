# LINK DROP pair + wire question: GLiNER2.5 and Perplexity embeddings (2026-10-08)

Operator pasted two X links and asked: "hermes gives us perplexity right?"

## The wire question, answered from bytes (this sitting)

NO standing Perplexity wire exists in the estate:

- .env carries no PERPLEXITY / PPLX / SONAR key (grep clean).
- configs/providers.yaml has no perplexity provider row.
- What DOES exist: configs/browser_env.yaml allows perplexity.ai as a
  browsable surface (the browser lane can drive the site UI), and the grok
  CLI door (live-proven this morning) carries web search by default, which
  covers the search-the-web need at $0 marginal.
- Hermes (the Nous-funded dispatch agent) is unrelated to Perplexity Inc;
  no Perplexity tool wire is configured on the estate side, and per the
  10-07 402-wall receipt the Nous keys are nearly dry (key 2 bounded
  [0.16, 0.17) USD, key 1 below 0.16; haiku-shaped asks only). Any
  Hermes-mediated search spends those dregs.
- Per the operator's standing order (2026-10-08): no key requests, ever.
  Fact stated once: a Perplexity API door would need a key he creates on
  his side. Until then: grok -p, browser lane, free fleet.

## Drop 1: Perplexity pplx-embed-v2-late (fetched this sitting)

Late-interaction embedding pair, public on Hugging Face:

- Token-level 128-dim vectors scored by MaxSim, NOT one vector per document.
- Text, images, and rendered pages in ONE shared embedding space; PDFs,
  slides, scans searchable without OCR.
- 0.6B and 9B sizes distilled token-by-token from an 18B teacher; cross-size
  query: a 9B-indexed corpus is searchable with 0.6B queries.
- Benchmarks: ViDoRe v3 63.5, Q2D-Web Recall@1000 74.8 (9B), BrowseComp+
  64.0 via GPT-OSS-120B agent, MADQA 92.4.

Estate placement: the EmbeddingGemma 2 GPS substrate was KILLED by its own
falsifier on 10-07 (strings 100.0 vs embedding-kNN 99.05, McNemar p=0.5, at
60x the ms budget; model banked for the shape-diversity future). This is a
DIFFERENT shape, not a revival: token-level late interaction wins on
long-document and vision-doc retrieval, which single-vector models do not.
The 0.6B-queries-9B-index asymmetry is the mesh-expansion roster shape
(smashed-phone queries the desktop-built index). Any adoption rides the same
pre-registered strings-vs-embeddings A/B at matched tasks; the falsifier law
is the door, not a veto.

## Drop 2: GLiNER2.5 unlimited-length spans (fetched this sitting)

George Maloney (Fastino, the GLiNER makers) promoting GLiNER2.5: predicts
where entities BEGIN and END rather than scoring spans up to a fixed max
width, so it extracts full addresses, long quotes, legal clauses, product
descriptions. Framing: deterministic extraction from a small local model,
previously only decoder-LLM territory (which hallucinates). API + HF Space +
weights linked; not fetched this sitting.

Estate placement: the stupid-model lane thesis in another receipt (small
local model, structured output, no hallucination; dice-never-lie). Candidate
deterministic extractor for catalog tagging (configs/catalog_tags.py is
rule-based today) and for claim-and-citation span extraction over the prose
record estate. Any adoption rides the matched-task A/B against the current
rule-based taggers before it replaces anything.

## Disposition

CARD ONLY, $0. Wire answer banked above. No runs fired, nothing pulled.
