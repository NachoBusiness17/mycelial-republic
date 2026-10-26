# PA-C1-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

# ABLITERATION MECHANICS AND EXPERIMENTAL PROGRAM

## Research Synthesis: Censorship Mechanics and Commonality

### (1) Mechanisms of Censorship

The refusal behavior is a synthesized *defense-in-depth* stack (C2:114). There may be no single structural location for refusal; it is layered.

| Layer | Mechanism | Operates | Removability | State (Family) | Citation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Training-Time (Weights)** | RLHF/DPO/KTO/ORPO | End-to-end policy gradient shaping (C2:112). | Partial. Abliteration (projection) and SFT reversal are possible (C2:112). | Core knowledge base. | C2:112 |
| **Training-Time (Weights)** | CAI / RLAIF | High-level, rule-based policy baking (C2:112). | Harder. Requires multi-direction or data-level reversal (C2:112). | Policy scaffolding. | C2:112 |
| **Weight-Level Direction** | Residual Direction ($d$) | Projecting a single, low-dimensional write vector $d$ onto the residual stream (C2:113). | High. Single vector subtraction or orthogonalization (C2:113). | **The Core Handle.** | C2:113 |
| **System Prompt/Input** | Classifiers / Guardrails | Input validation, content filtering, or role-play constraint imposition (C2:114). | Trivial/User-Controlled. Bypassed by encoding, jailbreaks, or roleplay (C2:114). | Prompt boundary. | C2:114 |
| **Output Filtering** | LLM API Filters | Post-processing output check (moderation APIs). | External/Impossible for the user to control (cannot be bypassed by weight change). | Serving layer. | C2:114 |

### (2) Commonality, Geometry, and Quantization Survival

There is a shared empirical observation: refusal is mediated by
