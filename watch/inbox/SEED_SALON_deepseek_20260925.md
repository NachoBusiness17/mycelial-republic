# Seed salon — deepseek seat (deepseek-chat)

*6ms, free/cheap lane*

**1. MAP — industry practice → seed**

1. **AGENTS.md / vendor-neutral auto-load** → **ADOPT.** Seed's "load order beats search" is the same idea done harder; ship an `AGENTS.md` at root that *is* the load order, so every vendor's tool reads the method for free. Teeth: if the file isn't auto-loaded by ≥2 harnesses, it's prose, not a standard.
2. **Agent Skills (frontmatter = discovery API)** → **ADAPT.** Seed has 13 engines + docs; give each a `SKILL.md` with `name`/`description` frontmatter so discovery is mechanical, not a README a human must read. Teeth: a skill with no frontmatter is invisible and therefore dead.
3. **Cookiecutter one-command scaffold** → **ADOPT.** `pipx run seed-init <dir>` that lays down laws, engines, map generator, and a failing audit. Teeth: if install takes >1 command or >60s, strangers bounce.
4. **12-Factor vocabulary** → **ADAPT.** Seed's 11 laws are better, but unnamed to outsiders. Publish a one-page crosswalk (Law 4 ↔ Factor "logs as event streams"). Teeth: shared vocabulary is the only thing that survives a handoff.
5. **Semver + changelog + tests-as-contract** → **ADOPT, narrowly.** Version the *method card* and *engines* separately; the audit engine is the test suite. Teeth: a law change without a version bump is an untracked mutation.
6. **Marketplace/registry distribution** → **REJECT as primary, ADAPT as channel.** Registry is a moat only if the artifact is a *skill*, not a 60KB philosophy. Ship one canonical skill (`seed-audit`) to a registry; keep the estate local. Teeth: distribution you don't control is a dependency you didn't price.
7. **Ralph loop folklore** → **ADAPT.** Seed's "morning loop" is Ralph with receipts. Name it, publish the pass condition as a single command. Teeth: a loop without a pre-stated pass condition is just a cron job.
8. **OpenClaw: self-hosted dies on security** → **ADOPT.** Seed's "one door, fails loud" is the correct answer; make the audit the *only* entry point and exit nonzero on its own logic. Teeth: if the audit can pass while broken, the door is decorative.

**2. Five highest-value enhancements**

1. **`AGENTS.md` at root = the load order, verbatim.** Machine-readable, vendor-neutral, zero new concepts. This is the single cheapest adoption unlock.
2. **`seed-init` scaffolder (pipx/uvx, one command).** Lays down laws, engines, empty map, and a *failing* audit so the first run teaches the method. Include `--dry-run` printing every file it will write.
3. **`SKILL.md` frontmatter on every engine + doc.** `name`, `description`, `inputs`, `outputs`, `fails-when`. Turns 13 engines from a directory into a discovery API any harness can index.
4. **`seed-audit` as the one door, published as a standalone skill.** Exits nonzero on any law violation *including its own checker*. This is the artifact strangers actually install.
5. **`CHANGELOG.md` + `METHOD_VERSION` file, semver'd.** Law changes are breaking; engine changes are minor. Gives strangers a contract to pin against.

**3. The one that matters most**

**`seed-init` + failing audit.** Every other enhancement assumes a stranger got far enough to care. The scaffolder is the only artifact that converts a 60KB philosophy into a 60-second first-run experience where the method *demonstrates itself* by failing loudly on an empty estate. Adoption is not persuasion; it's a first command that works and a first alarm that rings true. Everything else is downstream of that.

**CHAIR VERDICT:** Adopt AGENTS.md + scaffolder + frontmatter + one-door audit; reject registry-as-moat; the scaffolder-with-failing-audit is the whole game.