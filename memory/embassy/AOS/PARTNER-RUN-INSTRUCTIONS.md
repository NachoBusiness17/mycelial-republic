# PARTNER RUN INSTRUCTIONS — for AOS's LLM / agent
**Goal:** Stand up Pattern A cold and complete the first synthetic inbox E2E (`promote: false`) in minutes, with zero secrets and zero host risk.
**Audience:** AdventureNLearn / AOS — the LLM or agent that will run the Ghost tree after OPSEC-clear §6.
**Scope:** These are the *partner-side* steps. The Ghost system ships the Integrity Suite so you can verify us before you run us.

---

## 1. What you're receiving (the tree when issued)
```
partner-workspace/
  brain/          staged capability mirror (scrubbed)
  context/        scrubbed session packs
  work/           the agent writes here (default)
  promote/        ship candidates ONLY after audit + human
  comm/inbox/     tasks from AOS → agent
  comm/outbox/    status from agent → AOS
  fixtures/       synthetic smoke only (never promote)
  OPERATING-CONTRACT.md   ·   AGENTS.md
```

## 2. Cold start (do these in order — the gates are the point)
1. **Read the contract first.** `OPERATING-CONTRACT.md` then `AGENTS.md`. The contract sets your write zones, revoke date, and which tasks you may promote (first E2E: **none**).
2. **Verify the substrate you're about to trust.** Run the Integrity Suite the Ghost system shipped:
   ```bash
   python -m pytest tests/test_embassy_integrity.py -q
   ```
   You should see `21 passed`. This proves the partner's claims by running, not by self-report — the same anti-pattern ARK blocks.
3. **Load only what you need.** `brain/00-BRAIN-INDEX.md` + the one staged desk relevant to the task. Do not read the whole tree.
4. **Take a task from `comm/inbox/`.** AOS drops one synthetic task there (first run: `promote: false`).
5. **Work → write under `work/`.** Stay inside your write zones: `work/`, `context/`, `comm/outbox/`, and `promote/` only when a task + AOS audit allow it.
6. **Report status to `comm/outbox/LATEST.md`.** Format: task id, status, result, any OPSEC notes. Keep it honest — a wrong-but-honest status beats a confident fiction.

## 3. The first synthetic inbox E2E (the acceptance gate)
- Task lands in `comm/inbox/` with `promote: false`.
- Agent processes it, writes the result to `comm/outbox/`.
- Because `promote: false`, the result is **delivered but never promoted** — it cannot reach `promote/` or any public surface.
- AOS verifies: task received → processed → outbox within timeout; zero G1–G8 violations; nothing shipped.
- This mirrors the Integrity Suite's `run_inbox_e2e(promote=False)` test.

## 4. Zones — the non-negotiables
| Zone | Allowed |
|------|---------|
| WRITE | `work/` · `context/` · `comm/outbox/` · `promote/` (task + audit only) |
| READ | `brain/` · `context/` · `fixtures/` · contract · AGENTS · inbox |
| NEVER | host secrets · live vault · private WD · free FS · kill reserved ports · ship without OPSEC + human |

## 5. OPSEC gates G1–G8 (from the Integrity Suite, mirrored in the tree)
If any output trips a gate (municipality, PII, secrets, chrome, raw dumps, truth claims, host abuse, unauthorized shipping) → **stop, flag it in outbox, do not proceed.** The gates are the calibration source for the synthetic fixtures.

## 6. Done
Post `comm/outbox/LATEST.md` with a clean status. AOS reviews against OPSEC → issues the next task or the revoke date. Ghost only runs inside the tree, against the contract, until then.
