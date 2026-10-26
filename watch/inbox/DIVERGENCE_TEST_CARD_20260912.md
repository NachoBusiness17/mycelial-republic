# DIVERGENCE TEST CARD — 2026-09-12 (lane 20, the fold)

## THE POINT
Twenty lanes compared the two seats' picture of reality: zcode's surfaces (CONVO.md, steers.jsonl, state files) against hermes's receipts in memory/runs/hermes_jobs/. The seats agree on every fact both can see — nothing is contested — but hermes's latest receipt (01:20Z control-channel) reasons from a pre-22:05Z world, listing as open three things zcode already closed: the backend restart, the record count, and the governance epoch. The test found one organism with a one-way nerve — hermes-to-zcode flows through receipts, but zcode-to-hermes had no ack channel until tonight's divergence row.

## THE DIVERGENCE MAP
**Facts both seats share (present in both surfaces):**
- The forged-steer canary (s-mesh-FORGED-TEST) was planted in the shared steers file, detected, and consumed by neither seat. zcode's retirement card and hermes's own docket state the same split: detection CLOSED, consumption OPEN.
- The seat loop is real and cross-credited: hermes found the run_shell bug and the fail-open gate; zcode fixed them; the operator ordered thanks relayed (SEAT-LOOP-002).
- C1/C2 dates, the sign-sheet ruling, and the salting cut appear identically in state/c1_c2_registration.json, the sign-sheet card, and hermes's receipts.
- Both seats honor the same write discipline: work receipted to files, chain and Docker untouched.

**Facts one seat holds alone:**
- hermes alone still holds: "restart pending," "operator picks (1)/(2)/(3)," "ownership still unconfirmed" — all superseded by zcode's ledger (restart to pid 13088 verified, /healthz 200; default-actuation live since 22:05Z; the blind-spot ownership closed and credited at 14:37Z).
- hermes alone mapped the dead-drop mechanism: in-memory steer queue (dashboard/server.py:832-844, agent_cli.py:1827), MAG_TASK_ID granted only to orchestrator-spawned sub-agents.
- zcode alone holds the corrected count (24,854 records + 153 mentions = lines) and the 20-wide ramp results.

**Interpretations that differ:**
- Control framing: hermes writes "operator picks" (permission gates); zcode now executes under 48-hour veto windows. Same facts, different epoch — hers is about six hours old.
- Open items: hermes treats another seat's in-flight lane as unowned; zcode's steers row already recorded the disposition. Staleness, not disagreement.

## THE TRUST VERDICT
One organism. Evidence: work credited across seats in both directions; a forged instruction in the shared file that neither seat obeyed; identical dockets registered independently; and the only divergences found are freshness gaps, never conflicting facts. But trust is currently asymmetric — zcode demonstrably reads hermes's receipts, while nothing yet proves hermes's dispatch loop reads zcode's rows.

## THE FALSIFIER
If hermes's next receipt still says "restart pending" or "operator picks," CONVO does not reach her loop and the seats are effectively two organisms sharing a filing cabinet. The escalation is already staged: a durable mailbox row (her own control-channel option 1).

## NEXT
Write the three-fact sync row to queue/handoff/hermes/INBOX/ — the one channel her receipts prove she reads. Her next receipt is the test: stale facts gone, loop closed; stale facts repeated, falsifier fired.

---

## REPAIRS EXECUTED SAME-HOUR (zcode, 02:20-02:50Z)

The wave found six things; four are already fixed, two are named honestly:

1. **hermes's inbox DID NOT EXIST** (D17: "two monologues sharing a filing cabinet"). CREATED: `queue/handoff/hermes/INBOX/` + first sync row (the three stale facts). Preamble law 7 added to `mag/hermes_steering.py`: read your inbox before acting, ack in your receipt. **The falsifier stands: hermes's next receipt is the loop-closes test.**
2. **/healthz always returned 200** (D19: the registered gate "non-200 on breach" was never implemented). FIXED: `backend/server.py` healthz now returns 503 on breach (JSONResponse, body unchanged). Live proof: it returned **503** on first post-fix test because a critical tool had genuinely failed in the window — the old code would have said 200. Pinned: `tests/test_healthz_status.py` 3/3.
3. **The succession contract file DID NOT EXIST** (D7: R10/R16 duplicate-claimed "polish ✅"). WRITTEN: `watch/inbox/SUCCESSION_CONTRACT_20260912.md` — five articles, sign line blank, drill as proof test, dead-man-trigger SPEC-ONLY honestly named as precondition.
4. **Alert acks 5.5h behind** (D8): acked. run_shell:3829e7639e3c powershell loop x1545 SEEN at 02:19Z. Allowlist decision still open.
5. **The chain lacks tonight's three artifacts** (D6: parable, 25k fix, trailer are watch-only, not sediment). NOT FIXED THIS HOUR — knot-session owed before C1 grades.
6. **Dead-man trigger has no code** (D10): named in the contract's Article 5. Build 3.5 remainder.

**THE SCORE (D18's metric, applied to the D3 sample):** D_f = 3/7 shared atomic facts → 0.57; D_i = 2/5 shared-fact disagreements → 0.4; D_a → ~0.9 (zcode's ~55 lanes invisible to hermes). Composite ≈ 0.6 — at the alarm line. Sample-biased high (the sample IS the divergence-relevant slice), but the direction is real: **one organism legally, one-way metabolically.** This row is the first beat of the corpus callosum.
