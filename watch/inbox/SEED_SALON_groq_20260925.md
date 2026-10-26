# Seed salon — groq seat (openai/gpt-oss-120b)

*3ms, free/cheap lane*

**MAP – INDUSTRY PRACTICES vs. THE METHOD**

| # | Practice | Seed Alignment | Verdict (adopt / adapt / reject) + one‑line critique |
|---|----------|----------------|---------------------------------------------------|
|1| **AGENTS.md standard** – auto‑load vendor‑neutral filenames, nested precedence | The seed uses a *single* “method card” and hard‑coded load order (meaning → location → bytes). | **Adapt** – auto‑load is useful, but the seed’s rigid order ignores the proven benefit of hierarchical overrides; add configurable precedence layers. |
|2| **Anthropic Agent Skills** – YAML front‑matter as discovery API, progressive disclosure | The seed stores laws in markdown but no machine‑readable front‑matter; discovery is manual. | **Reject** – without declarative metadata the “load‑order beats search” rule becomes brittle; adopt YAML front‑matter for instant introspection. |
|3| **Cookiecutter Data Science** – CLI scaffolds a project in one command | The seed ships 13 Python engines and a VS Code path but requires manual copy‑paste of the playbook. | **Adapt** – keep the engines, but wrap them in a Cookiecutter‑style template that generates the full estate layout with a single `seed init`. |
|4| **12‑Factor Agents** – shared vocabulary, env‑based config, stateless processes | The method’s “one door per resource” aligns with single‑source‑of‑truth, but it hard‑codes manifests rather than using env vars. | **Adapt** – replace static manifests with 12‑factor style env‑driven config while preserving the seal‑and‑fail‑loud principle. |
|5| **Semantic versioning + changelog + tests‑as‑contract** | The seed’s “hash‑sealed record” is immutable, but there is no explicit version tag or contract tests. | **Reject** – immutable records alone don’t convey compatibility; add SemVer tags and a minimal test suite that validates each law’s receipt. |
|6| **GitHub Marketplace / skill registries** – distribution moat | The seed is a 60 KB zip with no registry entry; discoverability is zero. | **Reject** – without a marketplace listing the method cannot be “adopted by strangers”; publish it as a GitHub Action/Marketplace asset. |
|7| **Ralph loop** – self‑executing pass condition spread as folklore | The seed’s “morning loop” is a human ritual, not an automated pass/fail check. | **Adapt** – encode the loop as an automated health‑check script that emits a pass/fail metric, preserving the cultural intent while adding observability. |
|8| **OpenClaw critique** – one‑door + seal is the answer to self‑hosted runtime security | Directly mirrors law 7; the seed already enforces a single manifest and loud failure. | **Adopt** – the seed’s implementation is consistent with this best practice; keep it unchanged. |

---

**5 HIGHEST‑VALUE ENHANCEMENTS FOR STRANGER ADOPTION**

1. **Declarative YAML Manifest** – Add a top‑level `seed.yaml` containing: version, list of engines, entry‑point, required env vars, and a checksum of the immutable record. This makes the estate discoverable by tooling and satisfies practice 2.

2. **One‑Command Installer** – Publish a `pip install seed-method` (or a `brew` formula) that downloads the zip, validates the hash seal, expands the VS Code workspace, and registers the 13 engines as entry points. Mirrors practice 3.

3. **Marketplace Publication** – Release the seed as a GitHub Marketplace Action and as a VS Code Extension. This gives it a distribution moat (practice 6) and a standard install UI.

4. **Automated Health‑Check CLI** – Provide `seed health` that runs the “morning loop” automatically, emits JSON metrics, and exits non‑zero on any seal violation. Aligns with practice 7 and law 4/7.

5. **Semantic Versioning & Contract Tests** – Tag each release with SemVer, include a `CHANGELOG.md`, and ship a minimal `tests/` suite that asserts each law’s receipt (e.g., that every record has a `who/when/where` header). Satisfies practice 5.

---

**ONE ENHANCEMENT THAT MATTERS MOST**

**Declarative YAML Manifest** – it transforms the seed from a hidden, human‑only playbook into a machine‑introspectable artifact, unlocking auto‑loading, marketplace integration, health‑checks, and versioning in a single, standards‑compliant step.

---

**CHAIR VERDICT:** Adopt the seed only after adding a declarative YAML manifest; without it the method remains opaque and un‑adoptable.