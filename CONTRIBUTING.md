# Contributing — Mycelial Republic

## Read first

1. **[docs/CONSTITUTION.md](docs/CONSTITUTION.md)** — binding rules (fork equality, no rank/token, data tiers, handoffs, anti-capture).  
2. **[AGENTS.md](AGENTS.md)** — how agents should behave in this repo.  
3. **[docs/AGENT_ROADMAP.md](docs/AGENT_ROADMAP.md)** — work DAG; do not skip data gates with theater.  
4. **[docs/MILESTONES.md](docs/MILESTONES.md)** — what is actually done.

## Hard rules

- **Private data never committed** (`data/raw`, secrets, unredacted personal dumps).  
- **Saelis / Steiniger = structure refs**, not the product identity.  
- **Do not claim R0/R1** without evidence in milestones + logs.  
- **No tokens or rank systems** that privilege a core.  
- **Amend the constitution** via proposal + `docs/CONSTITUTION_AMENDMENTS.md` (create on first change).

## Data tiers (summary)

| Tier | Goes to cloud free models? |
|------|----------------------------|
| T0 secrets | Never (not even in prompts) |
| T1 private operator | Local only |
| T2 public / redacted | OK with care |
| T3 specialist (e.g. Grok) | Deliberate escalate |

## Practical

- Prefer small PRs that unblock mirror practice or data prep.  
- Run tests you touch (`pytest -q` when relevant).  
- Instrument/agent lab: sibling `Documents/projects/local_sovereign_agent` — not product `data/`.  
- One job per contribution message when possible.

## License

Respect the root license when present; do not relicense third-party scaffolds under `scaffolds/` or `vendor/`.
