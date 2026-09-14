# TRAJECTORY ENVELOPE — ZCode UI export of this window (2026-09-05, operator hand-carried)

Continues: watch/TRAJECTORY_LENS_20260905.md (vendor envelope upgrade path; rib salon T1/T2).

## SPECIMEN
4 segments (01-04), session "Elder" main. Segment 01 header: **20 calls · 4,291,673 tok · GLM-5.3-Flash**.
Segments 02-04 carry per-call vendor numbers: IN 259,158/OUT 797 (64.3s) → IN 260,238/OUT 302 → IN 260,549/OUT 154.

## THE SMOKING GUN (answers the operator's pin question with vendor bytes)
Line 1264: **`TerminalStreamChunkError: model concurrency limit exceeded`** with full stack
(handleStreamErrorEvent → AiSdkModelAdapter.streamTextWithResolved → AgentRuntime.runModelBackedTurnStepImpl
→ runRegularTurnLoop). The window did not "choose" 5.3 — **the Flash lane hit the user concurrency
limit mid-stream, the stream died terminal, and the runtime's retry/failover machinery stepped in.**
Same class as the A2 builder death + LAW-16 (ONE STEERER: parallel warm sessions starve each other's slots).
The pin DB says Flash (verified earlier); the "switch" was failover-under-concurrency, now receipted.

## THE REFEEF TAX, VENDOR-VISIBLE
Segments 02-04: each turn carries ~260K input tokens to produce 154-797 output tokens. Ratio ~500:1
against, on retries. (Lite incident measured 122M in → 0.5M out — same shape.) The envelope makes the
tax a first-class number: context-refeed dominates burn cost in long-lived windows. Trajectory-lens
implication: COMPILE-over-RECORD rows should carry IN/OUT per turn so the tax is steerable.

## EXPORT QUIRKS (for the rejoiner T1)
- Every turn stamped with ONE of two snapshot timestamps (11:00:40 ×34, 11:02:20 ×35) + uniform
  elapsed "15.1s"/"17.0s" — the exporter renders snapshot-time, not historical wall clock. Wall-clock
  history is NOT in this envelope; the DB (session/message/part tables) remains the time authority.
- Reasoning exported inline as first-class channel (thought-bank thesis confirmed at UI level).
- Tool results carried with content + hashes; 2 tool_use_errors visible (Read-before-Edit) —
  failures ship in the envelope too. Good for training; watch for secrets in future exports.

## DISPOSITION
CONTINUES trajectory card. Findings: concurrency-failover receipted; refeed tax quantified per-turn;
envelope lacks wall-clock (DB is time authority). No spend. Wire: morning brief adds pin+concurrency check.
