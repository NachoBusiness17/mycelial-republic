# lane or-ling3 (inclusionai/ling-3.0-flash-sante:free) — pass 2 — OK — 37218ms

F1 | Supported | Constituent mechanisms (feedback, routing, dedup, storage) have individual published support, but no evidence establishes reliable unattended operation of the composed stack.
F2 | Unproven | Cannot verify Huang et al. 2024 vs Liu et al. 2024 citations; self-correction contestation is plausible but specific references unknown to me.
F3 | Supported | RouteLLM establishes learned routing; fleet cost-quality economics and distinct memory costs for loaded vs parallel models remain empirical.
F4 | Supported | Scoped API credentials are not kernel enforcement; Capsicum capability attenuation and AgentDojo adversarial evaluation are the relevant bars.
F5 | Supported | Internal instrumentation differs from external behavior; HTTP 200 with wrong content occurs; aggregate counts without attempt IDs cannot prove distinct executions.
F6 | Supported | Hash-linked history lacks durable-execution semantics (Temporal separates decisions/activities); exactly-once requires receiver-side dedup (RIFL); dead-worker writes unfenced (Chubby); SQLite transactions don't cover file effects.
F7 | Unproven | Cannot verify Engram architectural identity claim; RAGCache/TeleRAG/PerCache are prior art for caching; content-addressed storage lacks semantic retrieval/freshness/auth (Venti/Zanzibar).
F8 | Supported | Arithmetic verified: 19M×256×2=9.73GB, +608MB keys +152MB IDs =9.77GiB; second copy=9.06GiB; unmeasured estimate-only budgets cannot support feasibility claims.
F9 | Supported | Membership inference cannot prove inclusion; retrieval extraction doesn't imply weight memorization; Carlini et al. show dose-response depends on duplication/prefix/scale.
F10 | Supported | 512×16+256=8,448 comparisons verified; false-match ≤10,000/2^128≈2.94e-35; 10 trials 0 hits gives upper bound ~0.422 (99.6% CI), insufficient to prove low contamination.
F11 | Unproven | Cannot verify Wynn et al. 2025 / Yao et al. 2025 citations; agreement-not-implies-correctness is valid principle but specific references unknown.
F12 | Supported | Bounded systems contribution with open failure evidence is defensible; correctness claims need different standards than performance (one counterexample refutes universal, null performance is inconclusive).
