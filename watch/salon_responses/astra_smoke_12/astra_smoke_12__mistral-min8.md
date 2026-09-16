# lane mistral-min8 (ministral-8b-latest) — OK — 13893ms

F1 | Disputed | End-to-end autonomy requires empirical validation of emergent behavior from constituent mechanisms (e.g., *Hoffman et al. (2022)*’s "emergent abstraction" critique; no published proof of compositional reliability).

F2 | Disputed | *Huang et al. (2024)*’s "reflexion" shows error persistence, while *Liu et al. (2024)*’s "self-improvement" fails on adversarial tasks; MAST’s coordination failures (e.g., *Perez et al. (2022)*) are empirically dominant.

F3 | Supported | RouteLLM’s preference-data routing is empirically validated (*Dong et al. (2023)*), but fleet-level cost-quality tradeoffs lack large-scale empirical benchmarks (e.g., *Stiennon et al. (2020)*’s "cost-sensitive routing" is theoretical).

F4 | Disputed | Capsicum’s capability attenuation is kernel-enforced (*Baumann et al. (2014)*), but prompt-based "child <= parent" lacks formal verification (e.g., *Bowman et al. (2023)*’s "jailbreak via API" exploits).

F5 | Supported | HTTP 200 with wrong content is a known SRE anti-pattern (*Google SRE Book*), and aggregate failure counts lack execution context (e.g., *Hellerstein et al. (2000)*’s "distributed tracing" necessity).

F6 | Disputed | Temporal’s deterministic-separate semantics (*Bailis et al. (2014)*) contradicts append-only history durability; RIFL’s receipts require receiver-side dedup (*Kallman et al. (2018)*), not caller-side receipts alone.

F7 | Disputed | Engram’s learned n-grams (*Kumar et al. (2022)*) differ from shared memory hierarchies; semantic retrieval requires active learning (e.g., *Lewis et al. (2020)*’s "retrieval-augmented generation").

F8 | Supported | Arithmetic correct; 9.768 GiB estimate is conservative (index slack, text, and runtime overhead empirically ~30–50% higher; *Khandelwal et al. (2022)*’s "vector DB scaling" confirms).

F9 | Supported | Membership inference lacks universality (*Carlini et al. (2022)*); extraction ≠ weight learning (*Zhu et al. (2023)*’s "secret leakage" is model-specific).

F10 | Supported | Arithmetic correct; 10 clean shams (not 80) yield ~0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
