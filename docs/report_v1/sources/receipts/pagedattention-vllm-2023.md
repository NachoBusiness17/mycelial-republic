# Receipt: Efficient Memory Management for Large Language Model Serving with PagedAttention (2023)

- STATUS: SUPPORTED
- PULLED: 2026-09-10T20:57:09Z by Mickey G2-4 (tier-3 retrieval-plan backlog)
- AUTHORS: Kwon, Woosuk; Li, Zhuohan; Zhuang, Siyuan; Sheng, Ying; Zheng, Lianmin; Yu, Cody Hao; Gonzalez, Joseph E.; Zhang, Hao; Stoica, Ion
- YEAR: 2023
- CITE: arXiv:2309.06180; SOSP 2023
- SOURCE: https://arxiv.org/abs/2309.06180
- FETCHED: https://arxiv.org/abs/2309.06180
- SHA256: de9353854db4e16af0c63f73502f7e463f03bdc4f3c98f3fcd377fe1c625ed08  (of fetched page; raw cached at C:\Users\foste\AppData\Local\Temp\g24raw_gj340nk2\pagedattention-vllm-2023.raw)
- EXCERPT (verbatim, truncated):

> High throughput serving of large language models (LLMs) requires batching sufficiently many requests at a time. However, existing systems struggle because the key-value cache (KV cache) memory for each request is huge and grows and shrinks dynamically. When managed inefficiently, this memory can be significantly wasted by fragmentation and redundant duplication, limiting the batch size. To address this problem, we propose PagedAttention, an attention algorithm inspired by the classical virtual [...]

- WHY IT MATTERS: OS-style paged KV-cache - the memory-management door the corpus walks through for LLM serving.
- TRI-STATE: SUPPORTED - excerpt verbatim from fetched page, hash attached. Page may drift; the hash is the pin.
