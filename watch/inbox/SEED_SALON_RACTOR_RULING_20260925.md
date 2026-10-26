# Ractor ruling — seed enhancement salon (gpt-oss-120b over deepseek+groq+together)

**CONVERGENCES – the canon**  
- **AGENTS.md** must exist at the repo root and be *auto‑loaded* by ≥2 tooling harnesses; otherwise it is mere prose.  
- **Skill front‑matter** (YAML/MD) is required on every engine; a skill without `name`/`description` is dead to discovery.  
- **One‑command scaffold** (`seed‑init`) is the only gateway that turns a 60 KB philosophy into a runnable estate; any extra steps kill stranger curiosity.  
- **12‑Factor cross‑walk** is mandatory: each of the 11 laws needs a named factor so CI, logs, and docs speak the same language.  
- **SemVer + CHANGELOG + tests‑as‑contract** are already present (v2.1.0, 6 passing unittest cases); they become the immutable contract for every future law change.  
- **One‑door audit** is the sole entry point and must exit non‑zero on *any* violation, including its own self‑check.  

**DIVERGENCES – each chair’s lone wolf**  

- **DeepSeek**: *Reject* registry distribution as primary, *adapt* it only for the canonical `seed‑audit` skill.  
- **Groq**: *Replace static manifests with env‑driven config*; insists on hierarchical overrides, contrary to DeepSeek’s “load order beats search”.  
- **Together**: *Reject* marketplace publication for now, arguing the method is not a plugin; Groq pushes a marketplace moat, DeepSeek pushes a single‑skill registry.  
- **Groq**: *Reject* semver claim, saying the seed lacks explicit version tags; DeepSeek (and the facts) prove semver already exists, making Groq’s stance contradictory.  
- **DeepSeek**: *Adapt* the Ralph loop into a single command pass condition; Groq calls it “folklore” and only *adopts* it when automated.  

**BUILD ORDER – numbered, each with a proving test**  

1. **Create `AGENTS.md` (root, machine‑readable list).**  
   *Test:* `python -m unittest discover -p test_agents.py` asserts the file is parsed by two reference harnesses.  

2. **Add `SKILL.md` front‑matter to all 13 engines.**  
   *Test:* `test_skill_schema.py` loads each `SKILL.md` and validates required keys (`name`, `description`, `inputs`, `outputs`).  

3. **Publish `seed‑init` CLI (pipx/uvx, one‑command, `--dry-run`).**  
   *Test:* `test_seed_init.py` runs the CLI in a temp dir, checks that the scaffold contains `AGENTS.md`, `CHANGELOG.md`, and a *failing* `seed‑audit` audit.  

4. **Expose `seed‑audit` as a standalone skill in a registry.**  
   *Test:* `test_registry_publish.py` publishes the wheel, installs it in an isolated venv, runs `seed‑audit` on a pristine estate and expects exit code 1.  

5. **Lock `VERSION` and `CHANGELOG.md` (SemVer bump on any law change).**  
   *Test:* `test_version_bump.py` diffs the current `VERSION` against the git tag of the last law‑change commit; mismatch fails CI.  

**VERDICT** – These enhancements *do* raise the seed’s G7 stranger bar: the method now *fails loudly* on first contact, making strangers *prove* compatibility before they can even read the law.