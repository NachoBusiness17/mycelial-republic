## Finding — what your cell yields

The doctrine in configs (canon_configs) is **explicit, mechanical, and enforced by single-file organs**: the seat matrix (SEATS.md), operator habit (HABIT.md), and burst doctrine (BURST_DOCTRINE_20260903.md) together form a law lattice that is **read-only at runtime, versioned in git, and falsifiable by file shape**. No mythic nouns; every rule is a measured lane, a budgeted seat, or a concrete command. The canon is **not** a philosophy—it is a **routing table + budget ledger + seat registry** that the operator and seats must follow verbatim. The falsifier question is answered before it is asked: *Does the repo contain a single, authoritative, falsifiable doctrine file that defines seats, lanes, and budgets?* Yes—SEATS.md, HABIT.md, BURST_DOCTRINE_20260903.md, improve.yaml, features.yaml, and cost_rates.yaml together satisfy this. **Supported.**

---

## Evidence — what in the repo supports it (file/shape, no invention)

- **SEATS.md** (memory/improve/SEATS.md, 72 lines): defines the seat matrix with **exact provider/lane pairs** and invariants (lines 6–35, 58–72). Invariants include "No auto ollama pull unless max_auto_pull_gb raised" and "Grok TUI ≠ always-on"—mechanical, not aspirational. The file is the **seat registry** and is referenced by HABIT.md.
- **HABIT.md** (memory/improve/HABIT.md, 189 lines): operator habit that **wires the doctrine into daily commands** (lines 54–115). It mandates `python main.py lab`, `improve --once`, `context-pack`, and forbids Grok for janitor work—**enforcement-vs-ceremony divide is explicit**: commands are the enforcement; the chat is the ceremony. The file references SEATS.md and configs/lanes.yaml as the source of truth.
- **BURST_DOCTRINE_20260903.md** (docs/ref/BURST_DOCTRINE_20260903.md, 54 lines): **lane definitions with measured numbers** (lines 6–49). It defines lanes by model, concurrency, latency, cost, and USE FOR—**mechanical routing table**. Laws 1–9 are **measured assertions** (e.g., "50 simultaneous = 50/50 success, median latency +0.6s vs solo"). Law 13 is a **falsifiable claim**: "The 50-row is enforced PER KEY" with probe evidence. This file is the **burst lane registry** and is referenced by improve.yaml rotation.
- **improve.yaml** (configs/improve.yaml, 329 lines): rotation table (lines 18–30) and mesh/steal protocol repos (lines 43–74) are **data-driven organs**. The file defines budgets, sources, and rotation—**mechanical scheduling**. It references mesh_comm_repos.yaml and steal_protocol_repos.yaml as manifests.
- **features.yaml** (configs/features.yaml, 130 lines): **experiment registry** with status, hypothesis, metric, evidence—**falsifiable claims per experiment** (lines 8–130). Shipped experiments are **measured and receipted**; proposed experiments are **unproven but framed for falsification**.
- **cost_rates.yaml** (configs/cost_rates.yaml, 170 lines): **per-million-token USD rates and planning estimates** (lines 8–166). It is the **budget ledger** and is used by the dashboard/receipt pricing join. The file is **machine-readable** and referenced by improve.yaml swarm_defaults.
- **mesh_comm_repos.yaml** (configs/mesh_comm_repos.yaml, 162 lines): **law lattice organ** (lines 155–162). It defines Mag law for mesh comms: `never_default_seat`, `never_second_dna_store`, `steal_contracts_only`, `willing_participation`, `tier_max_research: T2`, `implement_gate: v4_steward_stable`—**mechanical constraints** that are **enforced by the organ’s design**.

No invention: every claim above is **directly supported by file shape and content**. The canon is **not** a document—it is a **set of single-file organs** that are **versioned, measured, and falsifiable**.

---

## Risk if wrong — what the audit breaks on if this is missed

- **Seat identity/substrate coupling**: If the seat matrix is not authoritative, the operator could route judgment work to a local janitor instead of Grok TUI, breaking the **scarce-judgment** constraint and wasting tokens. The audit would miss the **enforcement-vs-ceremony divide** and misclassify the system as a general chatbot rather than a **judgment-first sovereign agent**.
- **Burst lane misrouting**: If the burst doctrine is not authoritative, the operator might burst 50-wide on 4.7-flash (which is single-flight only) or use free lanes for long-context work (which dies at 8K), causing **provider throttling** and **failed runs**. The audit would miss the **measured lane definitions** and misreport the system’s scalability.
- **Budget ledger inaccuracy**: If cost_rates.yaml is not the canonical budget ledger, the dashboard’s receipt pricing join would be **wrong**, and the operator would **overspend** or **underutilize** credits. The audit would miss the **hard reproducibility** requirement for financial claims.
- **Experiment registry falsifiability**: If features.yaml is not the experiment registry, the system would lack **falsifiable claims** and **evidence links**, violating the examiner’s requirement for **hard reproducibility**. The audit would miss the **TSVF retrocausality** of past experiments informing future ones.

---

## The act — the concrete prep step (file/spec/number)

Create a **single-file spec** that pins the canon_configs doctrine for the audit:

1. **Pin the seat matrix**: Ensure `memory/improve/SEATS.md` is the **canonical seat registry** and that all seats reference it in their briefs.
2. **Pin the operator habit**: Ensure `memory/improve/HABIT.md` is the **canonical operator habit** and that it references SEATS.md and configs/lanes.yaml.
3. **Pin the burst doctrine**: Ensure `docs/ref/BURST_DOCTRINE_20260903.md` is the **canonical burst lane registry** and that it is referenced by improve.yaml rotation.
4. **Pin the budget ledger**: Ensure `configs/cost_rates.yaml` is the **canonical budget ledger** and that it is used by the dashboard/receipt pricing join.
5. **Pin the experiment registry**: Ensure `configs/features.yaml` is the **canonical experiment registry** and that every experiment has a **metric + evidence link**.
6. **Pin the law lattice organ**: Ensure `configs/mesh_comm_repos.yaml` law block (lines 155–162) is **enforced by the organ’s design** and that no .bak fossils remain.

**File**: `audit_prep/canon_configs_spec.md`
**Spec**: A 100-line markdown file that lists each organ, its **file path**, **measured/falsifiable claim**, and **enforcement mechanism**. Example structure:

```markdown
# Canon Configs Spec — Matthew Steiniger Audit Pin

## Seat Matrix (SEATS.md)
- Path: memory/improve/SEATS.md
- Claim: "Seat matrix defines provider/lane pairs and invariants"
- Evidence: lines 6–35, 58–72
- Enforcement: commands in HABIT.md

## Operator Habit (HABIT.md)
- Path: memory/improve/HABIT.md
- Claim: "Operator habit wires doctrine into daily commands"
- Evidence: lines 54–115
- Enforcement: `python main.py lab`, `improve --once`, `context-pack`

## Burst Doctrine (BURST_DOCTRINE_20260903.md)
- Path: docs/ref/BURST_DOCTRINE_20260903.md
- Claim: "Burst lanes are measured and falsifiable"
- Evidence: lines 6–49, laws 1–9, law 13 probe
- Enforcement: improve.yaml rotation table

## Budget Ledger (cost_rates.yaml)
- Path: configs/cost_rates.yaml
- Claim: "Per-million-token USD rates are canonical"
- Evidence: lines 8–166, dashboard/receipt pricing join
- Enforcement: improve.yaml swarm_defaults

## Experiment Registry (features.yaml)
- Path: configs/features.yaml
- Claim: "Every experiment has metric + evidence"
- Evidence: lines 8–130, shipped experiments receipted
- Enforcement: improve.yaml evaluation pipeline

## Law Lattice Organ (mesh_comm_repos.yaml)
- Path: configs/mesh_comm_repos.yaml
- Claim: "Mag law for mesh comms is enforced by organ design"
- Evidence: lines 155–162
- Enforcement: organ’s tags and mag_slot fields
```

**Number**: 6 organs pinned; 0 .bak fossils in configs/; 0 mythic nouns in canon files.

---

## Falsifier — what would prove this wrong

- **Seat matrix falsifier**: A seat referenced in a brief does not exist in SEATS.md, or a provider/lane pair in SEATS.md is not used by any command in HABIT.md. **Prove by grep**: `grep -r "seat" memory/improve/*.md | grep -v SEATS.md` should return 0 unexpected seats.
- **Burst doctrine falsifier**: A lane in BURST_DOCTRINE_20260903.md is contradicted by a measured probe (e.g., 50-wide on 4.7-flash returns 1302s, not 50/50 success). **Prove by rerunning the probe**: `scripts/conc_probe_past50.mjs` should return 50 successes + 1302s for the next 10 calls.
- **Budget ledger falsifier**: A rate in cost_rates.yaml does not match the provider’s public pricing page. **Prove by web_search**: `web_search("deepseek pricing api")` should return the same rate as the file.
- **Experiment registry falsifier**: An experiment in features.yaml lacks a metric or evidence link. **Prove by grep**: `grep -A5 "id: exp-" configs/features.yaml | grep -E "metric:|evidence:"` should return non-empty for every experiment.
- **Law lattice organ falsifier**: A tag in mesh_comm_repos.yaml law block is violated by a repo’s license or platform. **Prove by grep**: `grep -r "license: GPL" configs/mesh_comm_repos.yaml` should not appear under tags that forbid it.

If any falsifier returns a contradiction, the canon_configs doctrine is **Disputed** and must be corrected before the audit.
