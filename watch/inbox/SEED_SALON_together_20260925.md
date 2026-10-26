# Seed salon — together seat (DeepSeek-V4-Flash-0731)

*65ms, free/cheap lane*

**MAPPING INDUSTRY PRACTICES**

1. **AGENTS.md standard** — *Adopt.* Ship a root `AGENTS.md` that points to the method card and the generated map, so any agent auto-loads the load order; without it, strangers' agents will grep first, violating Law 1.
2. **Anthropic Agent Skills** — *Adapt.* Wrap each of the 13 python engines as a skill with YAML frontmatter (name, description, input/output schema) for discovery and progressive disclosure; currently they're opaque, forcing full-context loads.
3. **Cookiecutter Data Science** — *Adapt.* Provide a `seed init` CLI that scaffolds the estate (map, records, meters, method card) in one command; reading a method is not adopting it.
4. **12-Factor Agents** — *Adapt.* Name the 11 laws as factors (e.g., Factor 1: Load Order, Factor 4: Meters) to create shared vocabulary; prose laws aren't referenceable in code, reviews, or error messages.
5. **Semver + changelog + tests-as-contract** — *Adopt.* Version the method card and engines, add a CHANGELOG, and write tests that assert the laws (e.g., a claim without a receipt fails CI); the seed is a living artifact, not a static doc.
6. **GitHub Marketplace / registries** — *Reject for now.* Distribution is a moat, but the seed is a method, not a plugin; a single canonical URL for the method card suffices until the CLI exists.
7. **Ralph loop** — *Adopt.* Encode the morning loop as a cron/CI job that runs the meters and exits nonzero on violation; folklore must be executable, not just documented.
8. **OpenClaw critique** — *Adopt.* Make the seal a cryptographic hash of map+records, and run the one-door audit on every boot; this is the seed's strongest defense — make it the default entry point.

**FIVE HIGHEST-VALUE ENHANCEMENTS**

1. **`seed init` CLI** — Scaffolds map, records, meters, `AGENTS.md`, and `method.md` in a new directory, with a sample record and meter read.
2. **YAML frontmatter on each engine** — Name, description, input/output schema, and a one-line "bar" for its meter, so any agent can discover and call them via progressive disclosure.
3. **`seed check` command** — Runs all 13 engine audits, prints each meter against its pre-stated bar, and exits nonzero on any violation (Law 7 made executable).
4. **Public CHANGELOG + semver** — Version the method card and engines, with a `VERSION` file and a `CHANGELOG.md`; adopters need to know what changed and when.
5. **"Stranger's tour" doc** — A 5-minute walkthrough mapping each of the 11 laws to concrete files, with a worked example of a claim → receipt → meter → ruling.

**THE ONE ENHANCEMENT THAT MATTERS MOST**

`seed init` CLI. The seed is a method, not a product. Strangers need to instantiate it in their own estate. Without a scaffold, they must manually create the map, records, and meters — a high barrier that kills adoption. The CLI turns the 60KB seed into a working system in one command, forcing the laws to become concrete file templates, which is the seed's core value. Everything else (frontmatter, check, changelog) is polish on top of that instantiation.

**CHAIR VERDICT:** The method is sound but inert; `seed init` is the single bridge that turns a philosophy into a practice strangers can run.