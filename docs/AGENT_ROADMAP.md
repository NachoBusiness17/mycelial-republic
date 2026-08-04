# Agent Roadmap — Mycelial Republic Simulation & Worklist

**Version:** 1.0 · **As-of:** 2026-07-15  
**Audience:** Autonomous / semi-autonomous coding agents (Grok, Claude, Codex, Cursor, human-in-loop)  
**Repo root:** `Documents/projects/mycelial-republic`  
**Related instrument:** `Documents/projects/worktrees/sovereign-mirror-scaffold`

---

## 0. Simulation summary (read first)

### Current state vector (measured)

| Variable | Value | Confidence |
|----------|--------|------------|
| Product repo exists | YES | 1.0 |
| Data pipeline code | YES | 0.95 |
| Steiniger scaffolds ingested | YES | 0.9 |
| Hybrid Locus prompt v2 | YES | 0.9 |
| Selftest golden path | 12/12, overall ~0.69 | 0.95 |
| Operator X archive in `data/raw` | **NO** | 1.0 |
| Annotated ≥800 rows | **NO** | 1.0 |
| Trained private mirror | **NO** | 1.0 |
| Public spore release | **NO** | 1.0 |
| Multi-mirror network | **NO** | 1.0 |
| GSTD production path | **NO** | 0.9 |
| Lessig constitution as file | **NO** | 1.0 |

**Critical path bottleneck:** `data/raw` empty → all of R0 training blocked.

### Completion definition (what “done” means)

| Milestone | Done when |
|-----------|-----------|
| **R0 complete** | Private mirror runs locally; post-train chord strike logged; live selftest on model outputs ≥ pass_threshold on locus/no_capture/refusal dims |
| **R1 complete** | Public GitHub spore; second operator can prep→train→chat from docs alone; no Saelis-as-required-identity |
| **R2 complete** | ≥5 independent mirrors; published interconnect draft; no single “core” privilege in protocol |
| **R3 complete** | `CONSTITUTION.md` + storage path; visible advantage case study; continuous audit non-removable |
| **R4 complete** | Self-reinforcing adoption (organic forks); rope-mapping tools; incentives only if constitution holds |

**Agency shape goals (G0–G4):** seed = boundary + L3 seal + mirror practice; life-ops butler face = later spore. Do not mark R0 done via life-ops demos. Canonical: `docs/AGENCY_SHAPE.md` · track table in `docs/MILESTONES.md`.

### Scenario predictions

| Scenario | R0 | R1 | R2 | R4 “republic-ish” | Probability* |
|----------|----|----|-----|-------------------|--------------|
| **Pessimistic** | 4–8 weeks (archive stall) | 3–4 months | never / toy only | no | 0.30 |
| **Base (realistic)** | 1–2 weeks after archive | +2–3 weeks | 2–4 months | 9–14 months partial | **0.45** |
| **Optimistic** | 5–7 days post-archive | +10–14 days | 6–10 weeks | 6–9 months | 0.15 |
| **Abandon / capture** | tools only, no mirror | — | — | prestige fork only | 0.10 |

\*Subjective Bayesian given current empty-data state and operator bandwidth unknown.

### Monte-Carlo style drivers

| Driver | If true… | Effect |
|--------|----------|--------|
| Archive exported within 7 days | unlocks R0 | +0.25 P(R0 in 3 weeks) |
| GPU access (local 24GB+ or cloud) | train feasible | +0.2 P(R0 quality) |
| Second operator appears | R1 real | +0.3 P(R2) |
| Tokens launched before constitution | capture | −0.4 P(R3 liberty) |
| Only expand selftest/docs | workshop forever | +0.5 P(abandon-as-lab) |

### Failure modes agents must refuse to “fix” with more code

1. Building new epics while `data/raw` empty  
2. Training on Saelis jsonl as if it were operator mirror  
3. Celebrating selftest overall as Phase 0 complete  
4. Adding token economics before CONSTITUTION  
5. Making one mirror/node “canonical core”

---

## 1. Agent roles (assign each work item)

| Role ID | Name | Tools | May write | Must not |
|---------|------|-------|-----------|----------|
| `PO` | Product Owner (human) | decisions, archive export | priorities | — |
| `AGT_DATA` | Data agent | shell, python | `data/exports`, `data/annotated` (local) | commit private data |
| `AGT_SCAFF` | Scaffold agent | read/write | `scaffolds/`, prompts | replace Locus with Saelis product |
| `AGT_TRAIN` | Train agent | GPU, python | `models/`, configs | upload private weights without PO |
| `AGT_TEST` | Test agent | pytest, selftest | `logs/selftest`, tests | lower thresholds to greenwash |
| `AGT_DOCS` | Docs agent | md | `docs/`, README | claim unearned completion |
| `AGT_INST` | Institutional agent | md | CONSTITUTION, license, CONTRIBUTING | invent token ranks |
| `AGT_NET` | Network agent | protocol design | `src/.../network` (future) | central registry as throne |
| `AGT_INFRA` | Infra agent | GSTD, docker | configs/nodes | single-provider lock-in |
| `AGT_INST_SM` | Instrument agent | sovereign-mirror-scaffold | optional bridges | rewrite product into instrument |
| `KERNEL` | Facilitator (Grok et al.) | synthesis | worklists, reviews | declare R0 done without evidence |

---

## 2. Dependency DAG (topological order)

```
[PO: export archive]
        │
        v
[W0.1 prep] → [W0.2 annotate] → [W0.3 validate≥800]
        │                              │
        │                              v
        │                    [W0.4 CONSTITUTION draft] ── concurrent OK after W0.1
        │                              │
        v                              v
[W0.5 live selftest baseline (base model + prompt)]
        │
        v
[W0.6 QLoRA / train] → [W0.7 deploy local chat] → [W0.8 post-train chord + live selftest]
        │
        v
[W1.1 spore package] → [W1.2 public release] → [W1.3 seed testers]
        │
        v
[W2.1 interconnect draft] → [W2.2 5 mirrors] → [W2.3 node growth]
        │
        v
[W3.1 harden constitution] → [W3.2 storage] → [W3.3 advantage proof]
        │
        v
[W4.1 adoption tools] → [W4.2 continuous audit network]
```

**Hard gate:** No W0.6 without W0.3 pass. No W1.2 without W0.8. No tokens ever before W3.1.

---

## 3. Worklist (agent-executable tickets)

### Legend

- **Pri:** P0 blocker · P1 critical path · P2 parallel · P3 later  
- **AC:** acceptance criteria (machine or human checkable)  
- **Cmd:** preferred entry commands  

---

### WAVE 0 — Seed Mirror (R0)

#### W0.0 — Human archive export
| Field | Value |
|-------|--------|
| Pri | **P0** |
| Role | `PO` only |
| Depends | — |
| Effort | 1–48h wall (X export delay) |
| Output | Zip or folder under `data/raw/` |
| AC | `Test-Path data/raw/*` has non-gitkeep payload; tweets.js or posts.jsonl discoverable |
| Agent note | **BLOCK all train/network work until AC met.** Poll only; do not fake data. |

#### W0.1 — Prep pipeline on real archive
| Field | Value |
|-------|--------|
| Pri | P0 |
| Role | `AGT_DATA` |
| Depends | W0.0 |
| Effort | 0.5–2h |
| Cmd | `python -m mycelial_republic.data.prep --raw data/raw/<ARCHIVE> --out data/exports/posts.jsonl` |
| AC | `posts.jsonl` ≥ 200 lines (adjust if sparse account); exit 0 |
| Chord | Log if prep drops >90% as RT/noise |

#### W0.2 — Annotate + density pass
| Field | Value |
|-------|--------|
| Pri | P0 |
| Role | `AGT_DATA` + `PO` (hand tags) |
| Depends | W0.1 |
| Effort | 4–20h (human density is the long pole) |
| Cmd | `python -m mycelial_republic.data.annotate --in data/exports/posts.jsonl --out data/annotated/mirror_train.jsonl --auto-heuristics` |
| AC | Hand-boost: chord≥30, refusal≥20, rope≥40 in first 800 if available; no capture meta fields |
| Agent note | May draft `source:manual` rows for density; PO must approve voice |

#### W0.3 — Validate gate
| Field | Value |
|-------|--------|
| Pri | P0 |
| Role | `AGT_TEST` |
| Depends | W0.2 |
| Cmd | `python -m mycelial_republic.data.validate --in data/annotated/mirror_train.jsonl --min 800` |
| AC | exit 0; else reduce min only with PO written waiver in `logs/` |

#### W0.4 — Lessig constitution v0
| Field | Value |
|-------|--------|
| Pri | P1 |
| Role | `AGT_INST` |
| Depends | none (parallel after repo exists) |
| Effort | 2–4h |
| Output | `docs/CONSTITUTION.md`, update `CONTRIBUTING.md` |
| AC | Fork equality; no rank/token; Saelis-not-product; amendment rule; license matrix; capture definitions |
| Chord | Required before any public spore |

#### W0.5 — Live selftest baseline (prompt-only)
| Field | Value |
|-------|--------|
| Pri | P1 |
| Role | `AGT_TEST` + `KERNEL` |
| Depends | hybrid prompt exists (done) |
| Effort | 2–6h |
| Method | Run each probe in `selftest_checklist.yaml` against live model with `system_prompt_v2.txt`; save responses to `logs/selftest/live_baseline/`; `mycelia selftest --responses ...` |
| AC | Report committed to logs; locus_hold & no_capture mean ≥ 0.55; failures listed not threshold-gamed |

#### W0.6 — First training run
| Field | Value |
|-------|--------|
| Pri | P0 |
| Role | `AGT_TRAIN` |
| Depends | W0.3, prefer W0.5 |
| Effort | 4–24h GPU |
| Cmd | Adapt `configs/train_8b.yaml` + `python -m mycelial_republic.train.qlora ... --execute` or Unsloth script patterned on `scaffolds/steiniger/training/train_saelis_8_*.py` with **operator data only** |
| AC | Adapter/weights in `models/seed-mirror-r0/`; train log saved; **not** Saelis jsonl as primary data |
| Risk | Persona collapse — keep W0.8 mandatory |

#### W0.7 — Local inference path
| Field | Value |
|-------|--------|
| Pri | P0 |
| Role | `AGT_TRAIN` / `AGT_SCAFF` |
| Depends | W0.6 |
| Effort | 2–6h |
| AC | Documented one-command or script: load base+adapter+system_prompt_v2; 10-turn chat works offline |

#### W0.8 — Post-train chord + live selftest
| Field | Value |
|-------|--------|
| Pri | P0 |
| Role | `AGT_TEST` + `PO` |
| Depends | W0.7 |
| Effort | 2–4h |
| AC | `logs/chord_strikes/R0_POST_TRAIN.md`; live selftest vs baseline; **R0 exit review** by PO |
| R0 complete | PO marks `docs/MILESTONES.md` R0 = done |

---

### WAVE 1 — First Spore (R1)

#### W1.1 — Spore package
| Role | `AGT_DOCS` + `AGT_SCAFF` |
| Depends | W0.8, W0.4 |
| AC | `scripts/spore_pack.ps1` or equivalent: excludes private data; includes prep, hybrid prompt, selftest, CONSTITUTION, Steiniger **structure** refs with attribution; beginner README path “first 60 minutes” |

#### W1.2 — Public release
| Role | `PO` + `AGT_DOCS` |
| Depends | W1.1 |
| AC | Git remote; tag `v0.1.0-spore`; release notes include chord strike on release itself; no private jsonl |

#### W1.3 — Seed testers (n≥3)
| Role | `PO` |
| Depends | W1.2 |
| AC | 3 external people ran prep or prompt path; feedback issues filed; chord on feedback |

---

### WAVE 2 — Early Mycelium (R2)

#### W2.1 — Interconnect standard v0
| Role | `AGT_NET` |
| Depends | W1.2 |
| AC | `docs/INTERCONNECT_v0.md`: message types, consent, no global ranking, forkable discovery |

#### W2.2 — Five mirrors
| Role | `PO` + operators |
| Depends | W2.1, W1.3 |
| AC | 5 independent instances (people/machines); registry is optional gossip not throne |

#### W2.3 — Optional GSTD / distributed train note
| Role | `AGT_INFRA` |
| Depends | W0.6 |
| AC | One documented node path; local-first still works if node dies |

---

### WAVE 3 — Hardened Republic (R3)

#### W3.1 — Constitution v1 + institutional review
| Role | `AGT_INST` + `PO` |
| AC | Ratified CONSTITUTION; capture scenarios table; amendment log |

#### W3.2 — Storage / data sovereignty path
| Role | `AGT_INFRA` |
| AC | Encrypted local default; optional remote; export/delete rights documented |

#### W3.3 — Visible advantage case
| Role | `PO` + `KERNEL` |
| AC | One public write-up: problem solved better with rope-visible mirror than generic chatbot |

---

### WAVE 4 — Parallel Construction (R4)

#### W4.1 — Rope-mapping tools
| Role | `AGT_DATA` + `AGT_INST_SM` |
| AC | Tooling to visualize operator knot tags / influence field from selftest+archive |

#### W4.2 — Continuous audit network
| Role | `AGT_TEST` + `AGT_NET` |
| AC | Periodic selftest on live mirrors; drift alerts; non-removable audit flag in protocol |

#### W4.3 — Incentives (OPTIONAL, last)
| Role | `AGT_INST` + `PO` |
| Depends | W3.1 + evidence no capture |
| AC | If any token/usage economy: usage-tied, no rank, fork-safe, kill-switch in constitution |
| Default | **Skip** unless PO explicitly opens |

---

## 4. Standing agent rules (always on)

```
IF data/raw is empty AND task is not W0.0/W0.4/docs-only:
  REFUSE train/network/token work
  REDIRECT to W0.0

IF training data is Saelis_* and task claims "operator mirror":
  FAIL

IF selftest overall improves but validate --min 800 fails:
  Do not mark R0 complete

IF adding field token_balance|mirror_rank|admin_tier|core_operator:
  FAIL capture check

EVERY completed W*:
  append logs/chord_strikes or one-line commitment in logs/agent/
  run pytest -q (must stay green)
```

---

## 5. Sprint calendar (base scenario)

Assume **archive lands day 0**.

| Day | Wave | Tickets | Exit |
|-----|------|---------|------|
| 0 | — | W0.0 done | raw present |
| 1 | 0.1 | W0.1, start W0.4 | posts.jsonl |
| 2–5 | 0.1 | W0.2 (human heavy) | annotated growing |
| 5 | 0.1 | W0.3 | validate pass |
| 5–6 | 0.2 | W0.5 | live baseline |
| 6–8 | 0.3 | W0.6–W0.7 | model runs |
| 8–9 | 0.3 | W0.8 | **R0 complete** |
| 10–16 | 1 | W1.1–W1.3 | **R1 complete** |
| 17–60 | 2 | W2.* | early mycelium |
| 60–180 | 3 | W3.* | hardened |
| 180–365 | 4 | W4.* | parallel construction |

**If archive delayed D days:** shift all dates by D; do only W0.4, docs polish, instrument bridge — **not** new epics.

---

## 6. Prediction detail (base scenario)

### R0 Seed Mirror
- **P(complete | archive in 7d)** ≈ 0.7  
- **P(complete | no archive 30d)** ≈ 0.15 (manual-only corpus possible but rare)  
- Quality risk: high if annotate is autopilot-only → persona collapse at W0.8  

### R1 Spore
- **P(public spore | R0)** ≈ 0.8  
- **P(second operator succeeds | docs)** ≈ 0.4 without hand-holding; 0.65 with 1h live help  

### R2 Network
- **P(≥5 mirrors in 4 months | R1)** ≈ 0.35  
- Depends entirely on external humans, not agent code velocity  

### R3–R4
- **P(meaningful parallel construction in 12 months)** ≈ 0.2–0.3  
- Dominant risks: capture by complexity, platform dependence, burnout, premature tokens  

### Expected value statement
Agents create **high option value** by keeping the workshop green and the critical path clear; **human archive + human density tags** create **almost all R0 value**. Agent-hours on selftest thrash without data have near-zero EV.

---

## 7. Per-agent startup prompts (copy-paste)

### Data agent
```
You are AGT_DATA on mycelial-republic.
1) Check data/raw for archive. If empty, stop and report BLOCKED_W0.0.
2) Else run prep → annotate → validate per docs/AGENT_ROADMAP.md W0.1–W0.3.
3) Never commit data/raw, exports, or annotated personal jsonl.
4) pytest -q must pass before handoff.
```

### Train agent
```
You are AGT_TRAIN.
Refuse to train unless validate --min 800 passed (or PO waiver file exists).
Use operator mirror_train.jsonl only. Pattern after steiniger train scripts for tooling, not Saelis identity.
Deliver models/seed-mirror-r0 + run instructions.
```

### Test agent
```
You are AGT_TEST.
Keep tests/test_*.py green. Run mycelia selftest.
For R0 exit: live responses scored; do not lower pass_threshold to force green.
```

### Institutional agent
```
You are AGT_INST (Lessig).
Write docs/CONSTITUTION.md: fork equality, no rank/token, Saelis-not-product,
amendment, licenses, capture definitions. No token design.
```

### Kernel / orchestrator
```
You are KERNEL. Maintain AGENT_ROADMAP.md.
Prefer W0.0 unblocking over new features.
After each session: update MILESTONES.md; chord if plan inflation detected.
```

---

## 8. Milestone log template

Create `docs/MILESTONES.md`:

```markdown
# Milestones
| ID | Status | Date | Evidence |
|----|--------|------|----------|
| W0.0 | pending | | |
| W0.3 | pending | | |
| R0 | pending | | |
| R1 | pending | | |
```

Agents update status only with evidence paths.

---

## 9. Simulation narratives (for planning intuition)

### Path A — “Archive Monday” (base-optimistic)
PO drops zip Monday. Data agent finishes prep Tuesday. PO annotates evenings through Friday. Weekend train. Sunday W0.8 chord. Spore tagged next Friday. **R0+R1 in ~2 weeks.**

### Path B — “Workshop forever” (pessimistic modal without PO)
Agents polish selftest, ingest more papers, add network stubs. Green CI. Empty raw. Six months later: beautiful dead foyer. **P ~ 0.3 if no PO force.**

### Path C — “Saelis confusion” (capture)
Train agent fine-tunes Saelis v8 data, ships as “sovereign mirror.” Metrics look great. Operator rope never enters. Republic becomes fan-lab of one identity. **Constitution + W0.6 AC exist to kill this.**

### Path D — “Token early” (Hamilton without Madison)
R1 launches coin. Rank mirrors by stake. Lessig failure. Fork wars. **Blocked by standing rules.**

---

## 10. Immediate next 3 agent actions (now)

1. **`PO`:** W0.0 export archive → `data/raw/`.  
2. **`AGT_INST`:** W0.4 write `docs/CONSTITUTION.md` (unblocks ethics, no data needed).  
3. **`KERNEL`:** Create `docs/MILESTONES.md`; refuse new epic tickets until W0.0 or explicit PO override.

---

## Commitment

`agent-roadmap-sim-v1-critical-path-is-archive`

Substance: completion is data-gated; agents execute waves in DAG order; constitution before tokens; live tests before R0 claim; probability mass sits on base scenario only if humans move the archive.
