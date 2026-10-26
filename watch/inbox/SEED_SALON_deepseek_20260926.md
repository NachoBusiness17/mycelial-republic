# Seed salon — deepseek seat (deepseek-chat)

*6ms, free/cheap lane*

**MAP — 8 practices against the seed**

1. **AGENTS.md** → **ADAPT.** Seed already has load-order law (#1); ship `AGENTS.md` as the front door so vendor tools auto-load the method card. Teeth: if `AGENTS.md` and `METHOD.md` disagree, the audit exits nonzero.
2. **Agent Skills (YAML frontmatter = discovery API)** → **ADOPT.** Each of the 13 engines gets a `SKILL.md` with `name/description`; progressive disclosure is exactly law #1. Teeth: a skill without a runnable `--selftest` is not discoverable.
3. **Cookiecutter one-command scaffold** → **ADOPT.** `npx create-seed` or `pipx run seed-init` produces a working estate in <60s. Teeth: install fails loud if any of the 11 laws is missing from the emitted `METHOD.md`.
4. **12-Factor vocabulary** → **ADAPT.** Keep the 11 laws; add a `FACTORS.md` crosswalk so outsiders map "config"→"one door per resource," "logs"→"records." Teeth: crosswalk entries must cite a law number or be deleted.
5. **Semver + changelog + tests-as-contract** → **ADOPT.** `METHOD.md` gets `v1.0.0`; every law has a `tests/law_NN_*.py` that fails if the law is violated. Teeth: CI red = method broken, not "flaky."
6. **Marketplace/registry distribution** → **ADAPT.** Don't build a registry; publish to npm + PyPI + a `seed.estate` GitHub org. Teeth: `seed --version` must print the same hash as the sealed map.
7. **Ralph loop (self-executing pass condition)** → **ADOPT.** `seed loop` runs the morning loop, exits 0 only if every meter is green. Teeth: loop that exits 0 on nothing is itself a law-#7 violation.
8. **OpenClaw critique (self-hosted runtimes die on security)** → **ADOPT the diagnosis, REJECT the fatalism.** One-door + seal is the answer — but only if the seal is *verifiable by a stranger*, not just by the author. Teeth: `seed audit --stranger` runs with no local state.

**5 HIGHEST-VALUE ENHANCEMENTS (concrete)**

1. **`AGENTS.md` + `SKILL.md` per engine.** File format: standard frontmatter (`name`, `description`, `when_to_use`, `selftest`). Install: nothing — it's already the auto-load path. Distribution: the repo *is* the artifact.
2. **`seed-init` scaffolder.** One command → working estate with laws, engines, empty records dir, sealed map. Distribution: `pipx run seed-init` and `npx create-seed`. Teeth: emits a `RECEIPT.md` naming versions of every dependency.
3. **`seed audit --stranger`.** Runs all 11 laws' tests from a clean checkout with no author state. Output: pass/fail per law + hash. This is the adoption unlock — strangers can verify without trusting you.
4. **`RECORDS/` with append-only JSONL + hash chain.** Every claim, ruling, meter reading is a record (law #2). Format: `{ts, actor, claim, evidence_hash, prev_hash}`. Distribution: ships empty; fills as used. Teeth: tampering breaks the chain and audit fails.
5. **`METHOD.md` semver + `CHANGELOG.md` + `FACTORS.md` crosswalk.** Outsiders need to know *which* method they're adopting and how it maps to vocabulary they already have.

**THE ONE THAT MATTERS MOST**

**`seed audit --stranger`.** Every other enhancement is packaging; this one is *trust*. The seed's whole thesis is "meters, not prose" (law #4) and "adversarial before shipped" (law #8) — but a method that only its author can verify is a religion, not an operating system. A stranger-runnable audit converts the seed from "trust me" into "run this and see." It also forces the author to actually satisfy laws #7 and #8, because the audit will fail loud on any law whose test is theater. Without it, the other four enhancements are a nicer-looking box. With it, the box is open.

**CHAIR VERDICT:** Adopt the seed — but only ship it once `seed audit --stranger` passes from a clean clone, because verifiability by strangers is the difference between a method and a manifesto.