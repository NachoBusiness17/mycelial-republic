# Receipt: Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving (2024)

- STATUS: SUPPORTED
- PULLED: 2026-09-10T20:57:09Z by Mickey G2-4 (tier-3 retrieval-plan backlog)
- AUTHORS: Qin, Ruoyu; Li, Zheming; He, Weiran; Zhang, Mingxing; Wu, Yongwei; Zheng, Weimin; Xu, Xinran
- YEAR: 2024
- CITE: arXiv:2407.00079
- SOURCE: https://arxiv.org/abs/2407.00079
- FETCHED: https://arxiv.org/abs/2407.00079
- SHA256: 9b1ef98e3f5601ccc2de5f660d1c932f235b20b6bbca7b4a3fe9114aba4e1c5b  (of fetched page; raw cached at C:\Users\foste\AppData\Local\Temp\g24raw_gj340nk2\mooncake-2024.raw)
- EXCERPT (verbatim, truncated):

> Mooncake is the serving platform for Kimi, a leading LLM service provided by Moonshot AI. It features a KVCache-centric disaggregated architecture that separates the prefill and decoding clusters. It also leverages the underutilized CPU, DRAM, and SSD resources of the GPU cluster to implement a disaggregated cache of KVCache. The core of Mooncake is its KVCache-centric scheduler, which balances maximizing overall effective throughput while meeting latency-related Service Level Objectives [...]

- WHY IT MATTERS: KV-cache as the first-class resource; prefix-cache reuse across requests.
- TRI-STATE: SUPPORTED - excerpt verbatim from fetched page, hash attached. Page may drift; the hash is the pin.
