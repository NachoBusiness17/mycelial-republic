---
name: compute-wealth-inventory-20260918
description: 12 alive API endpoints confirmed 2026-09-18 — browser UA fixes
  Cloudflare 403 on groq/together; nvidia 102 models; ~50-100 model-lanes at $0;
  drivers use ~35
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

2026-09-18 operator: "we really need to steal all our api env endpoints — this is a
wealth of knowledge sitting here unmined and unexploited." Full probe of every key in
.env against its provider endpoint.

## Confirmed alive (12 endpoints, ~50-100 model-lanes at $0)

| Provider | Key env | Status | Notes |
|---|---|---|---|
| groq | GROQ_API_KEY | ALIVE (browser UA required) | gpt-oss-120b answers in 1-3s |
| groq2 | GROQ_API_KEY_2 | ALIVE (second account — doubles rate ceiling) | 0 calls since Sep 7 until tonight |
| deepseek | DEEPSEEK_API_KEY | ALIVE (526ms) | deepseek-chat, deepseek-reasoner |
| gemini | GEMINI_API_KEY | ALIVE (277ms) | gemini-2.0-flash |
| cohere | COHERE_API_KEY_FREE | ALIVE (259ms) | command models |
| xai | XAI_API_KEY | ALIVE (293ms) | grok seats |
| mistral | Mistral_API_KEY | ALIVE (395ms) | + Mistral_API_KEY_2 second account |
| openai | OPENAI_API_KEY | ALIVE (1128ms) | gpt-4o-mini |
| openrouter k1 | OPENROUTER_API_KEY | ALIVE (341ms) | stealth + free models |
| openrouter k2 | OPENROUTER_API_KEY_2 | ALIVE (second key doubles stealth rate) | pareto + glm |
| nvidia | NVIDIABuild | ALIVE — 102 models confirmed | deepseek-v4-flash 3.4s, llama, nemotron, kimi |
| together | TOGETHER_API_KEY | ALIVE (browser UA required) | llama-3.3-70b-turbo |

## Key findings

- **Browser UA fixes Cloudflare 403** on groq and together — bare urllib gets blocked,
  browser-like User-Agent header passes. chat_provider already does this; bare urllib
  probes need it too.
- **NVIDIA NIM: 102 models behind one key** — deepseek-v4-flash-0731 verified at 3.4s,
  Kimi K2.6, nemotron-super-49b, gpt-oss-120b/20b. In configs/providers.yaml since Aug.
- **Cerebras key name mismatch**: .env has CEREBRAS_API_KEY but providers.yaml expects
  CEREBRAS_API_KEY — need to find the actual env var name.
- **The wealth is the DIVERSITY of the pool, not any single model.** Every lane is a
  different reasoning pattern; the evolution loop gets stronger with more genetic
  diversity.

## Steal from the sibling corpus (same night)

The Desk/DEP/AOS sibling lineage (4 PDFs + S-001 audit of our own code) dropped the
same night — their typed control surface (ActionRequest→Capability→ActionReceipt),
UNCERTAIN evidence classes, tool-lifecycle tombstones, and registry A10 defect
(confirmed OURS: mag/registry.py read-modify-write, no locking) are adopted. Receipt:
watch/inbox/EXTERNAL_STEAL_DESK_CORPUS_20260917.md. Build order: CONTROL_SURFACE_AUDIT
Phase 0-1 = the Elder pass-2 meter.
