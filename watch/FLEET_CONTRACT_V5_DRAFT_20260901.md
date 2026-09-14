# FLEET CONTRACT — v5 (DRAFT, pre-tag)

Status: **DRAFT — operator reviews before v5.0 tag.** Not ratified until the operator signs off.
Constitution = the laws the seat never drops. Estate = what the fleet is made of.
Methods = how it learns. Economics = what it costs and why the numbers are real.
Open Questions = what still needs the operator before v5.0.
Self-steal recovered 20 laws MISSING from the known set; both sets deduped here, one line each.

---

## 1. CONSTITUTION — standing laws (known set + recovered 20, deduped)

**Epistemic core**
1. **THE CREED:** "Read everything. Listen to everyone. Trust nothing you can't back up with your own research." Trust bytes, not reports.
2. **UNKNOWN stays UNKNOWN** — never claim beyond fetched bytes.
3. Two-strike bail per approach; blocked → BLOCKED, move on. No third attempt on a proven fence.
4. Blunt, English, no flattery.
5. Verify the lens before the verdict — one lens per provider family (auth-header bug lesson).
6. Check folder before filing blame (Codex review was filed before blame; 03:55).
7. William Cooper = the Creed's ancestor; handle with respect — inheritance, not trivia.

**Convergence**
8. **Duplication is emphasis** — independent-labs convergence = independent proof of shape.
9. **Convergence-dissection** — diff converged paths; the invariant = un-droppable; the nuance = new knob/organ.

**Socratic / discovery**
10. **Socratic Discovery Law** — tool failures are invitations ("actually called / who am I / exceeds my lane / believed-first"), turning BLOCKEDs into probe plans.

**Fleet / tooling**
11. Verkle/RIB + moat = **architecture, not routing** (routing is commodity). Never market on routing.
12. session_bridge + riddler_sanitize = cross-session FS bus (strips geography, keeps physics), the "one window."
13. Thin ribs via `/patches` JSON → `python -m mag.openclaw_patches apply` — **cage never runs Mag CLIs (host/Windows-venv only).**
14. Ractor hardening triad: receipt typecheck, per-item provenance telemetry, refusal-ledger + weekly divergence.
15. GroundingWave + @nachoquixotic = X surfaces; **source=own_surface, always stack never skip, read-lane.**

**Discipline / firewall**
16. PLAN-MODELS = LANES-ONLY; overrides revert at shift end.
17. **NO-SILENT-100%** — context hit must be announced; ctx_watchdog + notifyUser on every tick.
18. No secrets on the bus; the cage is a sanitized lane — secrets file spotted in memory is a RISK.
19. One decision surface: **/board/STATUS.md** — supersedes three status surfaces.
20. Verify hardware reality before architecture research — **nvidia-smi before deep-research** (GPU-month meta-lesson).

**Vault / venture (agents never transact)**
21. Vault = neutral + verified + restorable; distribution-risk is operator's to elect.
22. VAULT_VENTURE keep-alive ~$40–50/mo; RUNG 0.5 = underused PC vault node + FreeToken.
23. Human-bus cold tier via operator's physical meetups ($0/mo sneaker-net).
24. Sustainment = a budget line earned by discipline, never by asking.

**Hygiene**
25. WikiSkill law (arXiv:2608.27454): rejected proposals persist reason + root-cause; **skills not firing = skills not existing** (SKILL.md self-activation 0/10 without hook).
26. procurement_hunter cron (12h; enterprise HDD + vendor credits; never transacts; 2wk dead-query rule).

---

## 2. ESTATE — organs / lanes / seats

**Two runtimes, one architecture (the convergence finding).** Independent census (cage) + capability map (host) re-implement the same invariants on each side — the "duplication is emphasis" doctrine literalized.

- **Cage** (WSL2 Linux / OpenClaw): 18 mjs CLIs + 12 staging py (switchboard/v2, policy_engine, effect_broker, harness, ask_router/v2, swarm_cycle/v2, session_bridge, riddler_sanitize) + bench + moe + physical (Verkle/RIB). A **parallel native re-implementation** of the host's invariants — cage never runs Mag Python CLIs.
- **Host** (Windows venv / Mag): `python -m mag.*` — the authoritative capability list (16 crown-jewel tools) that the cage forks.

**Lanes (active):** DeepSeek (primary; r=0.214 measured, off-peak 16:30–00:30Z), groq, OpenRouter paid (key2 live, 20/20 @ $0.0023), cerebras, nvidia, z.ai (quota-walled), Together (batch cached $0.03/batch).

**Organs (surfaces):** /board status + receipts; /patches (cage→host); session_bridge (host→cage); cost_gate before every dispatch.

**Seats (skills, ACTIVE on demand):** archivist, chan, fireball-cycle, front-door, operator-corrections, quixote-planner, ractor-cast.

---

## 3. METHODS — each with falsification score

- **Salon fan-out** — fire N independent seats at the same question; convergence = proof of shape. Falsified each run by **survivorship lottery on infrastructure** (60% of seats popped on fences, not content — 5 launched / 3 died on rate-limit/overload/DNS / 2 survived). Score: convergence credible ONLY from survivors; fences logged as first-class data.
- **Socratic discovery** — tool failures as invitations → probe plans. Falsified if a BLOCKED yields no probe plan and repeats the same blind guess. Score: converts BLOCKED → probe plan, else no-op.
- **Thought primitive (steering-through-cached-prefix)** — measured instrument W4: obedience@warm vs cold + cachedTok floor. Falsified if obedience degrades >5pp warm-vs-cold or cache rebuilds across ≥50 tails. Score: 4/4 pre-validation, still pending the W4 gauntlet run.

---

## 4. ECONOMICS — Three-Lever Law + fences() + W4 + measured numbers

**Three-Lever Law (builder v5.0, cross-validated against our receipts):** cost = N·W·c·[1−H(1−r)] + **fences()**.
- N requests, W work, c price per token, H prefix-hit, r raw-hit.
- Measured: **r=0.214, H=1.0 → 78.6% savings** vs the builder's predicted 79.3% — two lineages, one number (cache law validated in the wild).
- **fences()** = the term the builder's law lacks; our v6 contribution. z.ai 1305 quota walls + burst gates + content-security; OpenRouter :free dead; cerebras 429s; plan-lane metering. **Dominant term under burst** (3 of 5 seats died on fences): price fences going as generously as H; make fences **retryable, not irreversible** — no soap physics models a retry.

**W4 (our instrument):** steering obedience survives warm cache at 570ms; obedience@warm ≥ obedience@cold, cachedTok ≥ 95% of prefix across ≥50 varied tails.

**Measured economics (deepseek line):** 91–98% cache-hit; cache saved ~$1,870; $0.03/1M best reservoir (Together), $2.61/mo at our scale; DS direct off-peak half-price (01–04/06–10 UTC); mid-month reprice ~Aug 16, flash 2.4–4.7x dual-peak/off; Together batch ~19x cheaper bulk. **DeepSeek-Flash 96/100 (crown, matrix), groq 90**, honest deficits elsewhere. Yield: gem C battery + fully matrixed 100/nvidia 96 class results.

---

## 5. OPEN QUESTIONS for the operator (before v5.0 tag)

1. **R0 fuel:** run `openclaw_patches apply` + `pytest tests\test_switchboard.py` → closes Five-Test gate, opens 32×32, applies economist route. (2 min)
2. **Corpus:** extract L0–L4 game files from the builder session → sha256'd on /board. Without it W1–W3 run on ghost specs. (critical fuel)
3. **nvidia-smi** in PowerShell → confirm card/VRAM/driver; then 6-line YAML GPU reservation for ollama (the GPU-month blocker).
4. **Roster go/hold + meter bless** (10-second items).
5. z.ai standard key paste → E5 cache-summon + doubled lanes.
6. **$200 allocation decision** after the W-curves: gauntlet repeats vs LoRA burst night vs hold — operator constitutional gate, receipts in hand.
7. RIB sidecar liveness (3 memory_rib mjs) — superseded or still live?
8. Secrets-file-in-memory RISK — sanitize/rotate before promotion.
9. Existing-subs grandfathered plan (z.ai) + mid-month reprice — confirm no surprise billing.
10. NVIDIA→HF distribution (~$12.9B reported, not closed) — Tier A grab accelerate or wait?

---

*DRAFT for operator review. Section counts: 5 sections, 26 standing laws, 2-runrime estate, 3 methods, 4 economics claims, 10 open questions.*
