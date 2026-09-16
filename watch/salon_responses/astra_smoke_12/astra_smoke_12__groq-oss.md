# lane groq-oss (openai/gpt-oss-120b) — OK — 5767ms

F1 | Unproven | No peer‑reviewed study demonstrates fully unattended local agent stacks operating reliably over extended periods.  
F2 | Disputed | Huang et al. 2024 show limited self‑correction while Liu et al. 2024 report error amplification from stored feedback.  
F3 | Unproven | RouteLLM and similar models have no published large‑scale fleet cost‑quality evaluation across heterogeneous hardware.  
F4 | Supported | Capsicum and AgentDojo papers show that scoped API tokens alone can be bypassed without kernel‑enforced capability attenuation.  
F5 | Supported | Google SRE book notes HTTP 200 does not guarantee correct payload and metrics without request IDs cannot infer distinct executions.  
F6 | Supported | Temporal’s separation of workflow decisions from side‑effects and RIFL’s exactly‑once definition require receiver acknowledgments, not just append‑only logs.  
F7 | Supported | RAGCache, TeleRAG and Venti demonstrate that content‑addressed storage lacks semantic freshness and authorization guarantees.  
F8 | Supported | 19 M × 256 × 2 B = 9.728 GB; adding 608 MB keys and 152 MB IDs yields 10.488 GB (≈9.77 GiB), and a second vector copy adds ≈9.06 GiB, matching the claim.  
F9 | Supported | Carlini et al. 2023 show membership inference dose‑response varies with duplication and model scale, with no universal memorization threshold.  
F10 | Supported | 512 × 16 = 8 192 plus 256 = 8 448 comparisons; false‑match ≤10 000/2¹²⁸≈2.9e‑35, and Clopper‑Pearson 95 % upper bound for 0/10 is ≈0.37, confirming the claim’s arithmetic.  
F11 | Supported | Wynn et al. 2025 and Yao et al. 2025 demonstrate that agreement between two agents can stem from shared bias, not independent correctness.  
F12 | Supported | ACM SIGOPS reproducibility guidelines require open failure evidence and independent replication for systems claims, matching the stated posture.
