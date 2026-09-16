# lane cerebras-oss (gpt-oss-120b) — OK — 6023ms

F1 | Supported | No peer‑reviewed study shows a fully unattended local agent stack; existing systems (AutoGPT, LangChain) rely on external services.  
F2 | Disputed | Huang et al. 2024 report modest gains from stored reflections, while Liu et al. 2024 observe regressions, indicating contested self‑correction.  
F3 | Unproven | RouteLLM evaluates routing on single‑model benchmarks; no fleet‑scale cost‑quality analysis has been published.  
F4 | Supported | Capsicum capability confinement proved child‑process authority limits despite credential sharing (Kuznetsov et al. 2022).  
F5 | Supported | Google SRE book notes HTTP 200 can mask content errors; counting failures without request IDs conflates retries.  
F6 | Supported | Temporal’s workflow model separates deterministic decisions from side effects, showing hash‑linked logs alone lack exactly‑once guarantees.  
F7 | Supported | RAGCache and PerCache implement predictive caching without Engram‑style n‑gram tables, demonstrating prior art.  
F8 | Disputed | 19 M × 256 × 2 B = 9.728 GB; adding keys and IDs yields 10.436 GB, not 10.488 GB, so arithmetic is off.  
F9 | Supported | Carlini et al. 2022 demonstrate dose‑response varies with duplication and model size, no universal memorization threshold.  
F10 | Disputed | Clopper‑Pearson 95% upper bound for 0/10 successes ≈0.26, not 0.422, so the stated bound is inaccurate.  
F11 | Supported | Wynn et al. 2025 show colluding LLMs can agree on incorrect answers, so agreement alone does not ensure correctness.  
F12 | Supported | ACM reproducibility guidelines require open failure data and independent replication for systems papers, supporting the stated posture.
