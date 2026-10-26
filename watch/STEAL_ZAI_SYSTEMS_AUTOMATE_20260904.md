# STEAL — z.ai's existing systems as the fleet's automation substrate (2026-09-04)

**ITEM:** The operator's question: how do we use existing systems within z.ai to automate
the day-work process? Answer mined from the LOCAL 86-page docs mirror
(`docs/ref/zai_docs_mirror/`, mirrored complete 09-04) — no web, all doors Bearer-keyed on
keys the fleet already holds (z_ai / z_ai2 / z_ai3 / z_ai4).

## RECEIPTS (the enumeration, condensed)

14 openapi paths on one key family. Concurrency is the real shape:
5.3-Flash=50 · ASR/Search-Prime/Web-Reader/Vidu/AutoGLM-Phone/CogView-4=5 ·
FlashX=3 · GLM-OCR=2 · GLM-Image/CogVideoX-3=1. Full table: `docs/ref/ZAI_API_EXPERT_REFERENCE.md`.

Tier 1 — genuine MULTI-STEP engines:
- **AutoGLM-Phone-Multilingual** — the only API-reachable EMBODIED agent. Sees screenshot →
  plans → executes tap/type/swipe via ADB, 10 primitives, 50+ apps, EN/CN. CLIENT-SIDE loop:
  the open-source `zai-org/Open-AutoGLM` runner + ADB — the harness runs on OUR box, only the
  brain is theirs. Per-step telemetry is fully ours. Needs ADBKeyboard.apk for typing.
  Vendor defaults: temperature 0.0, top_p 0.85, max_tokens 4K. Concurrency 5, "free for a
  limited time". Doc: `guides/vlm/autoglm-phone-multilingual.md`.
- **/v1/agents** — three server-side multi-step black-boxes with observable traces: slides
  agent (thinking→tool→answer phases, named tools), translation agent (multi-pass strategies,
  `usage.total_calls` proves multi-call execution), vidu template agent (async pipeline).
  Poll door: `/v1/agents/async-result`. History: `/v1/agents/conversation`.
- **5.3-Flash + function calling + vision** at concurrency 50 — the vendor-designed agent
  brain; BUA/CUA GUI-agent design intent ("observes interfaces, rendered results, and
  interaction feedback to continuously test and improve its work" — that sentence is our
  dogfood doctrine in vendor voice).

Tier 2 — async primitives: image/video async → shared `/paas/v4/async-result/{id}` poll door.
Tier 3 — single-shot organs that compose: Search-Prime, Web-Reader ($0.01), GLM-OCR ($0.03/M),
ASR, tokenizer. Implicit prompt cache: ~50% off, fleet-verified 99.5% hit on byte-stable prefix.
MCP suite: search/reader/zread remote + LOCAL vision server (8 tools incl. `ui_to_artifact`,
`diagnose_error_screenshot` — vendor-built EYES for a phone rig).

**NOT PRESENT anywhere in the mirror:** webhooks/callbacks, queues, scheduled jobs, workflow
API, hosted fine-tuning, hosted RAG. Every async door is FIRE → POLL.

## READ (the two steals that matter)

1. **LAW CANDIDATE — POLL-NOT-PUSH:** z.ai sells organs, never chains. Zero webhook surface
   across all 86 pages. Whoever owns the polling loop owns the automation — and the fleet
   built exactly that TODAY (the 30-min day-work scheduler: diff surfaces → read finishes →
   load responses → mirror digest). The vendor's architecture CONCEDES the orchestration
   layer to the customer. We are the orchestration layer. Supported by exhaustive-mirror
   absence (86/86 pages) + openapi (14 paths, zero callback fields).
2. **LAW CANDIDATE — HONEST-AUTH-WALL:** AutoGLM-Phone ships a `Take_over` action primitive —
   the vendor BUILT IN "stop and hand the human the controls at login/captcha." Never fake
   past the wall; name it, escalate it. This mirrors our operator-gates law (KEYS/spend/ONE
   STOP) as a vendor-designed action. Steal the pattern into every fleet actuator spec.

## TRI-STATE
- Enumeration + concurrency table: **Supported** (mirror receipts above).
- AutoGLM-Phone on our emulator as B3 driver: **Unproven** (door documented, lane untried —
  probe owed; "free for a limited time" makes it $0 today).
- Slides/translation agents as intake batch summarizers: **Unproven** (server-side multi-step
  receipted in docs; no fleet call yet).
- POLL-NOT-PUSH law: **Supported** (absence evidence, exhaustive).
- HONEST-AUTH-WALL as law: **Supported** (vendor doc verbatim).

## VERDICT + SCORE: 22/25 BUILD — the substrate is already paid for; the chain is ours.

## ROUTE (wire)
- B3 lane: AutoGLM-Phone probe ON emulator-5554 against daytool.html (the page IS the
  task board: buttons = targets, digest = read-target, 70-step walk = the ladder). $0.
- Slides agent probe = one intake-batch summarization call (deck-fold lane). $0-margin.
- Vision MCP (`diagnose_error_screenshot`) = B2-eyes stand-in until B2 KEY-gate opens.
- Concurrency table → swarm sizing for the Legion organs (already in expert-ref).

## DOGFOOD
The 70-step ladder: AutoGLM-Phone walks daytool.html — load lattice, STEP ×70, read digest,
report. Steps completed / where it broke / tokens per step = the dumb-models-complex-tasks
falsifier, embodied. Every failure = a law, not a bug.

*Filed by the zcode seat (Max), day-drive 09-04. Economist stamp owed on any $ claim.*
