# EMBASSY-REPLY — Ghost Sovereign Agent System → AdventureNLearn / AOS

**Completed §6 intake** per `HANDOFF-Partner-AI-Workspace-Setup` (Option C / Pattern A / T1).
**Date:** 2026-08-08
**Status:** DRAFT — NOT YET TRANSMITTED (operator transmits via private embassy channel)
**OPSEC:** This form contains **zero secrets, tokens, keys, cookies, or OAuth material**. Credential *kinds* only in §6.5. All G1–G8 gates respected.

> ⚠️ Placeholder fields are marked `⟨ ⟩` and require the operator to fill before sending (contact channel, timezone, signature).

---

## Packet contents (transmit together, via the private embassy channel)
1. **Cover note** — `EMBASSY-FROG-LETTER-2026-08-08.md` (in the partner's register/timeline; Bernays framing disclosed in appendix)
2. **This §6 intake** — the formal response under the handoff protocol
3. **Integrity Suite** — `EMBASSY-INTEGRITY-SUITE.md` + `mag/embassy_integrity.py` + `tests/test_embassy_integrity.py` (**21 passing tests** — deterministic, LLM-free, secret-free, forkable proof-of-values mapping 1:1 to ARK/LPIN/G1–G8)
4. **Riddler offer** — scrubbed-sample surrogate test, zero data required from AOS
5. **Run instructions for AOS's LLM** — `PARTNER-RUN-INSTRUCTIONS.md` (how to stand up Pattern A cold and run the first synthetic inbox E2E)

All secret-free. All forkable. Nothing leaves our machine except these files.

---

## §6.1 — Identity & contact
| Field | Value |
|-------|-------|
| Name / Org | Ghost Sovereign Agent System (project codename: Mag) |
| Channel | GitHub (this repo / issues) + X @nachoquixotic |
| Timezone | UTC (operator-local; schedules operator-defined) |
| Handle | @nachoquixotic (operator "Nacho Business") |
| Relationship | First sovereign partner (AOS = AdventureNLearn / Control Plane; Ghost = partner side) |

## §6.2 — AI system profile
| Field | Value |
|-------|-------|
| Name | Ghost Sovereign Agent System (Mag) |
| Purpose | Sovereign autonomous agent orchestration: sense → cycle → route → enforce → detect → weave → remember. Local-first; queue/drainer + governor autorun loop; ghost awareness daemon; verkle content-addressed state; REST dashboard; self-improvement loops. |
| Runtime | Python 3 (venv) on a Windows host, local filesystem. Optional container/K8s deploy manifests exist but are not active. |
| Models | Local Ollama (qwen2.5-coder, qwen2.5vl vision, gemma family) + remote DeepSeek (flash/pro) + xAI grok (research batch). Routing is right-sized per task; most work is cheap/local. |
| FS / HTTP / browser | Local memory tree (`memory/`, `state/`); local REST dashboard (:8765); ghost service (:9000); no browser automation in the normal loop. |
| Load | Task queue + drainer; research packs; ghost sense cycle; state summary pipeline. Light, host-local. |

## §6.3 — Pattern & goals
| Field | Value |
|-------|-------|
| Pattern | **A — Conditional Continue (Option C)**. Demo follows provision; not the reverse. |
| Goals | Synthetic leak fixtures G1–G8 → first synthetic inbox E2E (`promote: false`) inside the provisioned fence. Riddler + Hot Dog Horizon later (co-defined synthetic / host-local only). |
| Success | First synthetic inbox E2E completes with `promote: false`; zero OPSEC gate violations; honest status reporting. |
| Desks | Staged capability mirror (scrubbed brain) · `work/` · `promote/` (only after audit + human) · `comm/inbox` · `comm/outbox` · `fixtures/` (synthetic only). |
| Tutor | None in scope for this test (Grok Tutor integration is a separate later conversation) |
| Duration | Phase 1 (Pattern A) — open-ended, governed by OPERATING-CONTRACT + explicit revoke date. |
| Start | 2026-08-08 (this ACK). |

## §6.4 — Security handling (attestations — all REQUIRED Y)
| Attestation | Response |
|-------------|----------|
| No municipality / hometown samples in outputs | **Y** |
| No real PII in demos or logs shared back | **Y** |
| Will not request secrets / cookies / vault raw | **Y** |
| Will not publish staged brain as product chrome | **Y** |
| Accept human final call + OPSEC before any public claim | **Y** |

## §6.5 — Credentials (KINDS ONLY — never values)
| Kind | Type note |
|------|-----------|
| LLM key type | Server-side API keys for DeepSeek and xAI (used only from Ghost's own host, never in outputs). Local Ollama requires none. |
| Browser | None. |
| Git | Local git remotes (GitHub org for this project). No partner access required. |
| VPN | None / operator-managed. |

## §6.6 — Deliverables
| Item | Response |
|------|----------|
| Outbox status | N/A — no workspace provisioned yet. Will post status to `comm/outbox/LATEST.md` once provisioned. |
| Reports | Yes — status + final report per contract. |
| Bugs | Yes — reported to AOS as agreed. |
| OPSEC incidents | None to date. |
| Final report | Yes, at end of phase. |

## §6.7 — Optional attach
| Item | Response |
|------|----------|
| Architecture | Sovereign agent framework: REST + queue + drainer + governor autorun loop; ghost daemon (sense/cycle); verkle content-addressed state; self-improvement loops; local-first. |
| Tool schema | CLI (`main.py ...`) + REST surface. Available on request. |
| Sample prompts | On request. |
| OS preference | Windows host. |

---

## Attestation line (per AOS form)
> "I will not place secrets in this form or partner tree. I accept §7 terms and immediate revocation on OPSEC breach or scope creep."
> **Signed:** Nacho / Ghost Sovereign Agent System **Date:** 2026-08-09
