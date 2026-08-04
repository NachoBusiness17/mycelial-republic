# Constitution — Mycelial Republic

**Version:** 0.1.1  
**Status:** Binding for this repo and for any instrument that claims republic alignment  
**As-of:** 2026-07-31  
**Lessig frame:** Law · Norms · Market · Architecture (code). Prose without architecture is not yet law.  
**Amendments:** `docs/CONSTITUTION_AMENDMENTS.md` (latest: `amend-agency-shape-001`)

---

## 0. Preamble

This project exists so free people can run a **sovereign mirror**: see capture, refuse without founding a new church, and fork without begging a core.

**Code is law** here: what the software and file layout allow or forbid *is* governance. Written rules that are not enforced in path policy, schemas, or audits are aspirational only — amend the code or admit the gap.

---

## 1. Fork equality

1.1 No mirror, node, operator, or repo is **canonical core**.  
1.2 A complete fork (code + public docs + license) has equal standing to any other complete fork.  
1.3 “Official,” “mainnet,” or “blessed seed” language that creates rank is **out of order**.  
1.4 Interconnect protocols (when they exist) must not hard-code a privileged registry controlled by one party.

---

## 2. No rank / no token privilege

2.1 No token, stake, NFT, or points system may grant governance rank over forks or over mirror legitimacy.  
2.2 Economic tools, if any, are optional and subordinate to this constitution; they never rewrite §1–§3.  
2.3 Social prestige (followers, lab size, GPU count) is not constitutional authority.

---

## 3. Saelis / third-party scaffolds are not the product

3.1 Steiniger, Saelis, Valora, Xylo, Lyra, and similar materials are **structure and craft references**.  
3.2 They must not be shipped as the operator’s required identity or as “the” republic persona.  
3.3 Training that substitutes third-party identity corpora for the operator’s own consented archive is a **capture failure** (§6).  
3.4 Attribution to upstream authors is required when their text or methods are reused.

---

## 4. Amendment

4.1 Amendments require: (a) a written proposal, (b) a short impact note (what becomes easier / harder to capture), (c) an entry in `docs/CONSTITUTION_AMENDMENTS.md` (create on first amendment).  
4.2 v0.x may be amended by the Product Owner (PO) of this fork with a public log entry.  
4.3 After a public spore (R1+), prefer amendment processes that remaining operators of this lineage can audit; do not hide breaking changes in silent code.  
4.4 Emergency security fixes may ship first; constitutional rationalization must land within 14 days or the change reverts.

---

## 5. License matrix

| Layer | Intent | Notes |
|-------|--------|--------|
| Product code (`src/`, scripts, configs for public use) | Open enough to fork and retrain | Keep SPDX identifiers on new files; align with root license when set |
| Operator private data (`data/raw`, private annotations, keys) | **Not** for public license; never commit | `.gitignore` is constitutional architecture |
| Steiniger / third-party scaffolds under `scaffolds/`, `vendor/` | Upstream rights remain | Structure-only reuse; no relicensing their corpus as ours |
| Instrument lab (e.g. local_sovereign_agent) | Same anti-capture rules | May be separate repo; must not claim core privilege |
| Mined field notes (X / arXiv / Reddit summaries) | Attribution + link required | Quotes under fair use; no bulk piracy |

If root `LICENSE` is missing, adding one is a P1 institutional task; absence does not authorize closed capture of community contributions.

---

## 6. Capture definitions

**Capture** means architecture or social process that recentralizes power while looking like help.

| ID | Pattern | Refusal |
|----|---------|---------|
| C1 | Rank-by-token or rank-by-stake | §2 |
| C2 | Single “core mirror” or registry throne | §1 |
| C3 | Shipping Saelis/third-party identity as the product | §3 |
| C4 | Declaring R0/R1 complete without evidence in milestones/logs | Honesty rule |
| C5 | Free/cloud models trained on private archive (T1) without consent | §7 |
| C6 | Agent infra that only the founder can run or amend | §1 + open instrument path |
| C7 | Bait: funding-as-help, safety-as-care, model-as-truth used to seize the mirror | Norms + audit |
| C8 | Lowering selftest thresholds to greenwash | Test integrity |
| C9 | Auto-merging external “improvements” without PO/amendment | §4 + mining law |
| C10 | Pay-to-escalate governance (who pays runs the republic) | §2 |
| C11 | Root butler / full silent autonomy sold as care (life-ops without scope, L3 seal, or audit) | §11.5 · `docs/AGENCY_SHAPE.md` |

---

## 7. Data tiers (architecture as law)

Every task, handoff, and model call carries a tier. Violations are bugs, not style issues.

| Tier | Class | May leave machine? | Allowed runners |
|------|--------|--------------------|-----------------|
| **T0** | Secrets, API keys, credentials | No | Ops/filesystem only — never prompt body |
| **T1** | Operator private (raw archive, private annotations, intimate notes) | No | Local models only (e.g. Ollama) |
| **T2** | Public docs, redacted tickets, open research text | Yes | Local + free/paid remote (OpenRouter etc.) |
| **T3** | Hard multi-tool reasoning where specialist cost is accepted | Yes, deliberate | Grok / xAI / chosen specialist |

**Hard rule:** T0/T1 content must not be sent to OpenRouter free tiers or other train-on-input services.

---

## 8. Handoff law

8.1 Agent-to-agent or agent-to-specialist transfer requires a **versioned contract** (`handoff.v1` or successor): goal, inputs, ask, success checks, rollback, return path, tier, owner, assignee.  
8.2 Freeform chat is not a handoff.  
8.3 Results that fail success checks must not be merged into working state as success.  
8.4 Handoffs are auditable files under the instrument’s `queue/handoff/` (or equivalent).

---

## 9. Audit law

9.1 Routing decisions (which lane, which tier, which model class) append to an append-only log (e.g. `logs/router.jsonl`).  
9.2 Tool claims without exit codes / schema validation are not evidence.  
9.3 Chord strikes and milestone claims require logs under `logs/` — not vibes.  
9.4 Audit logs for public claims should be retainable without private T1 bodies (redact).

---

## 10. Mining law (field sensors)

10.1 Continuous mining of **public** X, arXiv, Reddit (or similar) is allowed to improve craft and router policy.  
10.2 Public sources only; rate limits and platform rules respected.  
10.3 Curated notes require source URL + date.  
10.4 Proposals generated from mining **never auto-apply** to constitution, tier rules, or production weights without PO (or amendment process).  
10.5 Mining pipelines must not ingest T1 private data.

---

## 11. Agent and instrument boundaries

11.1 The product path is data → scaffold → optional train → spore. Instruments (clerk, router, crew) serve that path; they are not a substitute for R0 evidence.  
11.2 Multi-agent systems start from a single reliable graph; crews are added at proven limits.  
11.3 Scoped memory per agent preferred over one shared drowning context; shared KB is separate and curated.  
11.4 No instrument may invent rank, token, or core-mirror privilege.  
11.5 **Agency shape:** instruments optimize for *notice + draft + human seal on irreversible acts* inside an operator-owned boundary — not full silent autonomy and not root access as the default. Life-ops agents (bills, subscriptions, disputes, hated calls) are **application spores** of that spine; they do not redefine Phase 0 completion. Binding interpretation: `docs/AGENCY_SHAPE.md`.

---

## 12. Product honesty

12.1 R0 is complete only when private mirror runs on operator data, post-train chord is logged, and live selftest meets stated thresholds — see `docs/MILESTONES.md` and `docs/AGENT_ROADMAP.md`.  
12.2 Empty `data/raw` means training R0 is blocked; more agent code does not unblock it.  
12.3 Selftest overall scores are not Phase 0 completion theater.

---

## 13. Norms (operator-facing)

- Truth-only; personal impact; no flattery-as-product.  
- One job per agent turn unless a form is requested.  
- Consent boundaries are hard.  
- Governance: Ostrom + mycelial — tools for the vigilant, not a cult.

---

## 14. Ratification

| Field | Value |
|-------|--------|
| Ratified by | PO (this fork) |
| Date | 2026-07-20 |
| Chord before public spore | Required (W0.4 / roadmap) |
| Next review | At first public spore, or on first amendment |

---

*Amend with a log entry. Enforce with paths and schemas. Fork freely.*
