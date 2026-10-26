# stealth-sw-06: Multimodal memory systems for AI agents

Question: what architectures exist for integrating text, image, audio, and video into unified agent memory?

Method: 9 web searches plus primary-source abstract fetches on 2026-09-28 (arXiv 2508.09736, 2512.03627, 2501.13956, 2505.00675 via WebFetch). Every claim below traces to a fetched abstract or a search-result listing; anything I could not verify this session is flagged in section 4. No fabrication.

## 1. Taxonomy baseline (the modality-agnostic layer)

"Rethinking Memory in AI: Taxonomy, Operations, Topics, and Future Directions" (arXiv 2505.00675) splits memory representation into parametric (implicit in weights) vs contextual (explicit external data, structured or unstructured), governed by six atomic operations: consolidation, updating, indexing, forgetting, retrieval, condensation. Crossing representations with operations yields four research topics: long-term memory, long-context memory, parametric modification, and multi-source memory. Multi-source memory is exactly the slot where multimodal integration lives. A second survey line, "LLM Agent Memory: A Survey from a Unified Representation" (OpenReview id KPs1EgGKcT), groups memory backends into natural-language tokens, intermediate representations, and parameters, and argues for a unified interface so one control plane can drive heterogeneous memory backends. A curated map of the space: TeleAI-UAGI/Awesome-Agent-Memory on GitHub.

## 2. Architecture families

### 2.1 Entity-centric perception memory (streaming audio + video into episodic/semantic stores)
- M3-Agent, "Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory" (arXiv 2508.09736, ByteDance Seed). Takes real-time visual and auditory inputs and builds two memory types, episodic and semantic, organized entity-centric and multimodal so world knowledge accumulates from continuous perception. Given an instruction it autonomously performs multi-turn reasoning and retrieves relevant memories. Trained via reinforcement learning. Introduces M3-Bench: M3-Bench-robot (100 newly recorded robot-perspective videos) and M3-Bench-web (920 web videos), QA annotated for person understanding, general knowledge extraction, and cross-modal reasoning. Beats a prompting agent built on Gemini-1.5-pro + GPT-4o by +6.7% (robot), +7.7% (web), +5.3% (VideoMME-long). Code: bytedance-seed/m3-agent.
- HippoMM: hippocampus-inspired cognitive architecture for long-form audiovisual event understanding (alphaxiv listing).
- Editable Multimodal Memory with RL: an actor-critic memory manager normalizing text, visual, and auditory events into versioned working/long-term memory stores (ResearchGate listing).
- ScrapMem: bio-inspired, storage-efficient on-device long-term memory for multimodal LLM agents (arXiv, May 2026 listing).

### 2.2 Hierarchical frameworks with parametric distillation
- MemVerse (arXiv 2512.03627, v2 June 2026, Junming Liu + 13 coauthors): model-agnostic, plug-and-play memory. Short-term memory holds recent context; raw multimodal experience is converted into structured long-term memories organized as hierarchical knowledge graphs; a periodic distillation mechanism compresses key knowledge from long-term memory into the parametric model for fast, differentiable recall while keeping the explicit store interpretable. Supports continual consolidation, adaptive forgetting, and bounded memory growth against catastrophic forgetting. The abstract states improved multimodal reasoning and continual-learning efficiency but gives no numbers (full text: 25 pages, 14 tables) and does not enumerate the modality list.

### 2.3 Video-memory agents (video as a first-class episodic store)
- VideoAgent (ECCV 2024): LLM-as-agent iteratively selects key frames from a long video to answer questions; the "memory" is the frame index plus intermediate findings.
- Streaming successors: EventMemAgent (arXiv, Sep 2026): active online video agent with hierarchical memory where short-term memory detects event boundaries and consolidates them into episodic long-term memory. VideoARM (arXiv, Dec 2025): agentic reasoning over a hierarchical memory structure for long-form video understanding.
- Benchmarks and neighbors: EgoMemReason (week-long egocentric video, memory-driven reasoning), EgoMemory (Microsoft, memory-augmented retrieval for wearable/AR-glasses egocentric video), VSeek (VLM actively searches for visual evidence in long videos), HiCrew (hierarchical long-form reasoning with BREASE episodic-memory simulation).

### 2.4 Spatial / embodied multimodal memory (scene graphs as the memory substrate)
- "Toward Versatile Embodied Agents" (OpenReview PDF): spatial memory stores a scene graph, initialized by a manual scan-and-annotation pass that assigns room names.
- 3D-Mem: 3D scene memory via informative multi-view "Memory Snapshots" for spatial recall.
- DAAAM ("Describe Anything Anywhere At Any Moment", OpenReview): a 4D scene graph acting as spatio-temporal metric-semantic memory.
- eMEM (HAL): hybrid spatio-temporal memory combining LLM-agent consolidation mechanisms with the spatial grounding of robotic scene understanding.
- Embodied-RAG: bottom-up memory with multimodal representations and structured integration.

### 2.5 Memory infrastructure products (text-first; multimodal support varies)
- Mem0: two-phase pipeline; an extraction phase analyzes conversations to identify facts, stored in a vector store with an optional knowledge-graph layer.
- Zep / Graphiti (arXiv 2501.13956): a temporally-aware knowledge graph engine combining unstructured conversational data with structured business data while preserving historical relationships, beyond static RAG. Reported results: DMR 94.8% vs MemGPT 93.4%; LongMemEval accuracy up to +18.5% with roughly 90% response-latency reduction. Caveat: I fetched the abstract only; the bi-temporal model internals, community detection, and edge-construction details were not verified this session.
- Letta (formerly MemGPT): the agent edits its own memory blocks in agent state (self-editing memory), rather than fact extraction or a graph.
- Benchmark dispute worth knowing: Mem0's LOCOMO claims were publicly contested by Letta; Zep then published a correction showing itself ahead by about 24%, with Mem0's graph variant at 68.5%. Vendor memory benchmarks are marketing-grade until reproduced.

### 2.6 Parametric / latent memory (no explicit store)
MemoryLLM lineage: latent-space memory inside the model. M+: Extending MemoryLLM with Scalable Long-Term Memory (ICML 2025, Yu Wang et al.) extends MemoryLLM with scalable long-term memory, turning historical information into continuously accessible latent representations. Retrieval happens in activation space; nothing to grep or audit, which is the trade.

## 3. Synthesis: four integration strategies recur across all families

1. Transcode-to-text: ASR + captioning first, memory stays plain text. The default for product stacks; Zep and Mem0 are effectively here for audio/video.
2. Shared embedding space: every modality embedded into one vector index for cross-modal retrieval. The default RAG-flavored design; a Hacker News discussion of "Unified Multimodal Memory Without Embeddings" criticizes it as hard to explain at scale versus structured alternatives.
3. Structured multimodal records: entities, events, timestamps as first-class graph nodes with multimodal attributes. M3-Agent's entity-centric memory, Zep/Graphiti, and embodied scene graphs all instantiate this; retrieval becomes graph traversal plus attribute lookup, which preserves provenance.
4. Parametric distillation: memory folded into weights or latent tokens. MemVerse's periodic distillation and M+/MemoryLLM. Fast recall, weakest auditability.

The research frontier is strategy 3 fused with strategy 4 (MemVerse does exactly this hybrid), and the benchmark layer is only now catching up (M3-Bench, EgoMemReason) after text-only benchmarks like LOCOMO and LongMemEval.

## 4. Honest gaps in this session's coverage

- Voice-agent-specific audio memory (full-duplex speech dialogue systems) was pursued in two searches that both returned 429 rate-limit errors; audio evidence here is indirect (M3-Agent auditory streams, HippoMM audiovisual events).
- Zep bi-temporal internals, MemVerse's modality list and benchmark numbers were not verified from primary full text (abstract-only fetches).
- LOCOMO/LongMemEval vendor numbers were not independently reproduced in this session; they are reported as published claims with the noted dispute.

## Sources

- https://arxiv.org/abs/2508.09736 (M3-Agent, abstract fetched)
- https://arxiv.org/abs/2512.03627 (MemVerse, abstract fetched)
- https://arxiv.org/abs/2501.13956 (Zep/Graphiti, abstract fetched)
- https://arxiv.org/abs/2505.00675 (Rethinking Memory in AI taxonomy, abstract fetched)
- https://openreview.net/forum?id=KPs1EgGKcT (LLM Agent Memory: unified representation survey)
- https://dl.acm.org/doi/10.1145/3748302 (ACM survey, memory mechanisms of LLM agents)
- https://github.com/TeleAI-UAGI/Awesome-Agent-Memory (curated map)
- https://forum.letta.com/t/agent-memory-letta-vs-mem0-vs-zep-vs-cognee/88 (Mem0/Zep/Letta architecture comparison)
- https://www.letta.com/blog/benchmarking-ai-agent-memory (LOCOMO dispute)
- https://news.ycombinator.com/item?id=46525174 (Unified Multimodal Memory Without Embeddings discussion)
- https://openreview.net/pdf/a6b294472ecf7c8fa312d6c962231824f0dc7d86.pdf (Toward Versatile Embodied Agents, scene-graph spatial memory)
- https://hal.science/hal-05640776v2/document (eMEM hybrid spatio-temporal memory)
- https://openreview.net/pdf?id=lAPgLxg8w7 (DAAAM 4D scene graph)
- Search-result listings (arXiv): EventMemAgent, VideoARM, EgoMemReason, HippoMM, ScrapMem, 3D-Mem, VSeek, M+ (ICML 2025)
