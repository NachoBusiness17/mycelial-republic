# KG PDFs — Primary-Source Document Store GRAB RECEIPT

**Date:** 2026-09-02 00:25 UTC · **Lane:** KG primary PDF grab · **Verifier:** sha256sum + `%PDF` header check
**Status:** 13/13 arXiv PDFs OK · 1 DOI UNVERIFIED · 0 fabricated

---

## OK — verified PDFs (real downloads, real sha256, all `%PDF`)

| id | title (slug) | bytes | sha256-12 | status |
|---|---|---|---|---|
| 2607.28956 | MerchantBench (Qwen e-commerce agent benchmark) — `merchantbench` | 3,021,290 | `3e13c2b18347` | OK |
| 2209.13085 | Defining and Characterizing Reward Hacking — `reward_hacking` | 849,540 | `d9a8567f6d5b` | OK |
| 2307.03172 | Lost in the Middle: How LMs Use Long Contexts — `lost_in_the_middle` | 747,542 | `653b29619eae` | OK |
| 2309.06180 | Efficient Memory Mgmt for LLM Serving with PagedAttention — `pagedattention` | 1,459,631 | `55b3b324d779` | OK |
| 2310.05736 | LLMLingua: Compressing Prompts for Accelerated Inference — `llmlingua` | 645,326 | `0cd06ff6bf44` | OK |
| 2310.06839 | LongLLMLingua: Accelerating & Enhancing LLMs in Long Context — `longllmlingua` | 2,530,020 | `a81090e2589f` | OK |
| 2310.08560 | MemGPT: Towards LLMs as Operating Systems — `memgpt` | 663,708 | `9f674bcff69c` | OK |
| 2311.04934 | Prompt Cache: Modular Attention Reuse for Low-Latency Inference — `prompt_cache` | 905,557 | `15e198a54c37` | OK |
| 2403.02691 | InjecAgent: Benchmarking IPIs in Tool-Integrated LLM Agents — `injecagent` | 3,183,277 | `49e6e6a4a00c` | OK |
| 2406.13352 | AgentDojo: Dynamic Env to Eval Attacks/Defenses for LLM Agents — `agentdojo` | 1,042,076 | `349884fffbf4` | OK |
| 2407.00023 | Preble: Efficient Distributed Prompt Scheduling for LLM Serving — `preble` | 739,155 | `44114cf18e9e` | OK |
| 2507.01701 | Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture — `blackboard_architecture` | 3,896,075 | `b0fa397ba8d0` | OK |
| 2608.31036 | Normalized Low-Rank Adaptation (NoRA) — `nora_normalized_low_rank` | 817,490 | `4f6c4574dcc5` | OK |

**Total OK:** 13 PDFs · **20,500,687 bytes ≈ 19.55 MB**
**All hashes independently confirmed via `sha256sum` (match grab-time hashes). Every file starts with `%PDF`.**

---

## UNVERIFIED — DOI not downloadable (recorded, not pirated)

| id | title | status |
|---|---|---|
| 10.1080/00131857.2025.2494589 | AI based personalized learning in 'The Diamond Age': Artificial subversiveness and human feeling machines (*Educational Philosophy and Theory*, 2025) | **UNVERIFIED-PDF** |

**Evidence:** Unpaywall marks `is_oa: true` (publisher-hosted, `oa_date 2025-04-28`, but `license: null`, `journal_is_in_doaj: false`, `journal_is_oa: false`, PDF URL carries `?needAccess=true`). Direct fetch of the T&F PDF endpoint returned **HTTP 403** with Cloudflare "Just a moment..." challenge HTML (`<!DO...`, not `%PDF`). No freely-downloadable PDF reachable from this cage. No PDF stored; `sha256: null`. Do not pirate.

---

## FAILED

None. (All 13 arXiv targets fetched OK; the only non-OK is the DOI above, classed UNVERIFIED per policy.)

---

## Grep context — the 4 "unknown" IDs (were cited by name in source doc, not truly unknown)

Source: `/root/.openclaw/media/inbound/wow---6ee04bf2-cc54-41a1-8fdb-8cc3477ef411.txt` around line 1583.

**Line 1583 — KV/prefix-cache doctrine:**
> "KV-cache and prefix-cache research improves cost and latency, but caching does not increase semantic context capacity. [PagedAttention 2309.06180], [Prompt Cache 2311.04934], [Preble 2407.00023]"

- **2309.06180 PagedAttention** — cited as evidence that KV/prefix caching helps cost/latency but adds **no semantic context capacity**. (vLLM, SOSP'23.)
- **2311.04934 Prompt Cache** — same cluster: modular attention reuse / prefix caching for low-latency inference (MLSys'24).
- **2407.00023 Preble** — same cluster, now *distributed* prompt scheduling + KV reuse (1.5×–14.5× latency SOTA).

**Line 1584 + lines 479, 734, 1131 — blackboard architecture (2507.01701), cited 4×:**
> Line 1584: "Blackboard systems separate shared knowledge from the controller deciding which knowledge source acts. [Nii], [LLM Blackboard MAS 2507.01701]"
> Line 479: "Modern LLM blackboard work follows the same pattern: agents share information, agents are selected based on board state, and rounds repeat until a solution or stopping condition emerges. [Han and Zhang's LLM blackboard system]"
> Line 734: "Research on LLM blackboard systems uses board state to select which agents act next, repeating selection and execution rounds until the problem converges."
> Line 1131: "Blackboard | Classical blackboards separate shared state, knowledge sources, and a control component. ... The BBS should generate attention/proposals, not authority." + "Hypervisor claim" → current `switchboard.py` is a control plane/reference monitor, not a true hypervisor.

**Why load-bearing for the estate:** 2507.01701 (Han & Zhang) is the doctrinal source for the estate's blackboard-systems architecture — shared board state, control-component selection, round loop — and feeds directly into the switchboard/hypervisor control-plane doctrine in the source document. The three KV-cache papers anchor the estate's finding that caching ≠ semantic context capacity.

---

## Storage

- **PDFs:** `/board/KG_STORE/pdf/<slug>.pdf` (13 files)
- **Catalog:** `/board/KG_STORE/catalog.jsonl` (17 lines: 3 historical + 13 arXiv + 1 DOI UNVERIFIED) — schema `{"id","title","path","sha256","bytes","source","topics","fetched"}`
- **Note:** `/board/KG_STORE/pdf/1007.0455_kzg_polynomial_commitments_iacr.pdf` (294 KB) is a pre-existing file from a concurrent process, not part of this grab, not cataloged here.
