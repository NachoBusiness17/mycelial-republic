# Seed salon — groq seat (openai/gpt-oss-120b)

*3ms, free/cheap lane*

**MAP OF INDUSTRY PRACTICES ONTO THE SEED**

| # | Industry practice | Seed stance | One‑line justification |
|---|-------------------|-------------|------------------------|
| 1 | **AGENTS.md standard** – auto‑load vendor‑neutral filenames, nested precedence | **Adapt** | The seed already enforces a single‑door manifest (Law 8); adding deterministic auto‑load rules will reduce manual loader churn without breaking the “one door” principle. |
| 2 | **Anthropic Agent Skills** – YAML front‑matter as discovery API, progressive disclosure | **Adopt** | The seed’s “record‑first” approach (Law 2) aligns with declarative front‑matter; using YAML gives a machine‑readable contract that satisfies Law 3 (decode, never invent). |
| 3 | **Cookiecutter Data Science** – one‑command project scaffolding | **Reject** | The seed’s “no hand‑maintained map” (Law 2) makes a static scaffold a liability; a generated map must be derived from the live estate, not from a template. |
| 4 | **12‑Factor Agents** – shared vocabulary of named factors | **Adapt** | The seed’s “laws” already form a vocabulary; formalizing them as 12‑factor style env vars would aid onboarding but must not become another mutable config source (violates Law 2). |
| 5 | **SemVer + changelog + tests‑as‑contract** | **Adopt** | Immutable, hash‑sealed records (Law 2) are a perfect substrate for signed SemVer tags and contract tests that become part of the execution receipt (Law 5). |
| 6 | **GitHub Marketplace / skill registries** – distribution moat | **Adapt** | The seed’s “salon” (Law 8) already provides a peer‑review gate; exposing the package via a registry adds discoverability while preserving the adversarial audit. |
| 7 | **Ralph loop** – self‑executing pass condition folklore | **Reject** | The loop’s “folklore” nature conflicts with Law 4 (meters, not prose); without explicit numeric pass‑criteria the loop is a hidden metric, violating the method. |
| 8 | **OpenClaw critique** – one‑door + seal as security answer | **Adopt** | Directly mirrors Law 7; the seed should formalize the seal as a signed manifest and enforce non‑zero exit on any manifest drift. |

---

**5 HIGHEST‑VALUE ENHANCEMENTS FOR STRANGER‑ADOPTION**

1. **Standardized, self‑describing package format (ZIP‑with‑manifest.yaml).**  
   - Includes a signed `manifest.yaml` (Law 7 seal), a `laws.md` copy, and a `record-index.json` (hash‑sealed map).  
   - Allows any toolchain to verify integrity before loading.

2. **One‑step bootstrap script (`install.sh`) that:**  
   - Verifies the manifest signature,  
   - Generates the estate map (`record-index.json`) via the built‑in scanner,  
   - Installs the 13 Python engines into an isolated virtualenv,  
   - Registers the single‑door loader in the user’s PATH.  
   - Guarantees “execution receipt before fix” by halting on any verification failure.

3. **Distribution via a public, immutable artifact repository (e.g., GitHub Releases + IPFS hash).**  
   - Provides content‑addressable distribution, satisfying Law 2’s “hash‑sealed record” and enabling reproducible installs.

4. **Machine‑readable “law‑contract” schema (JSON‑Schema) for each of the 11 laws.**  
   - Enables automated compliance checks (Law 8 adversarial audit) by CI pipelines before a user can run the seed.

5. **Interactive “salon‑cli” that runs a pre‑flight adversarial simulation:**  
   - Generates synthetic hostile queries, measures bar‑vs‑claim compliance, and logs votes.  
   - Makes the “adversarial before shipped” requirement explicit and repeatable for newcomers.

---

**ONE ENHANCEMENT THAT MATTERS MOST**

**Standardized, self‑describing package format (ZIP‑with‑manifest.yaml).**  
*Why:* It is the single point where every other enhancement (bootstrap verification, immutable distribution, law‑contract schema, salon‑cli) can be anchored. Without a universally recognizable, signed container, strangers cannot trust the seed’s integrity, cannot automate verification, and cannot reliably reproduce the estate map—nullifying Laws 2, 4, 7, and 8. The format becomes the “one door per resource” that fails loudly if tampered.

---

**CHAIR VERDICT:** Adopt the seed only after packaging it as a signed, self‑describing ZIP with a manifest; otherwise the method’s guarantees collapse.