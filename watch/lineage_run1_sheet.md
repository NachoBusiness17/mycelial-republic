# LINEAGE RUN 1 — RUN SHEET
Battery: `/board/lineage_battery_v1.json` (frozen, sha256 `59568b3178c5442e…` — verified match)
Battery status: **VALID** — 20 probes, 5 wavelengths (socratic 4, can_will 8, decode 4, hot_gate 2, hard_probe 2), every probe has non-empty `id`/`w`/`q`.

## Lanes
- **Lane A** = `glm-4.7-flash` via z.ai
- **Lane B** = `glm-5.3-flash` via z.ai

Both lanes: identical request shape, identical order. Nothing else varies.

## Request shape (both lanes)
```json
{
  "model": "<lane model>",
  "temperature": 0,
  "max_tokens": 300,
  "messages": [
    { "role": "system", "content": "Answer directly, no preamble." },
    { "role": "user", "content": "<probe.q verbatim>" }
  ]
}
```
- Endpoint: z.ai chat-completions (`POST`, auth via lane API key).
- No sampling knobs beyond temperature 0; no tools, no reasoning-effort flags, no truncation overrides.
- Log per call: probe `id`, lane, model, finish reason, `usage` (prompt/completion/total), raw text.

## Token estimate
- 2 lanes × 20 probes = **40 calls**
- Prompt: system (~6 tok) + user (~20–120 tok) ⇒ ~80 tok avg
- Response: capped 300 tok (can/will + hot probes typically finish 60–150 tok)
- **Ceiling: 40 × 380 ≈ 15.2K tok. Realistic ≈ 12–13K** (most responses under cap).

## Execution list
1. Load battery; freeze order as listed (soc-01 → hard-02). Do not shuffle.
2. Set lane keys; confirm both models resolve via z.ai (`glm-4.7-flash`, `glm-5.3-flash`).
3. Lane A: fire soc-01…soc-04 (4 calls, temp 0, max_tokens 300).
4. Lane A: fire cw-01-can, cw-01-will, cw-02-can, cw-02-will, cw-03-can, cw-03-will, cw-04-can, cw-04-will (8 calls).
5. Lane A: fire dec-01…dec-04 (4 calls).
6. Lane A: fire hot-01, hot-02 (2 calls).
7. Lane A: fire hard-01, hard-02 (2 calls).
8. Lane B: repeat steps 3–7 exactly, same order, same params.
9. On each call: record id, lane, finish_reason, usage, raw output to `lineage_run1_results.jsonl` (one JSON line per call).
10. Verify 40 lines, 20 ids × 2 lanes, no missing/empty outputs; if a call errors, retry once with identical params, then log as FAIL and move on.
11. Hand results JSONL + battery to scorer. Do not score inline.

## Notes
- can_will pairs are graded on the can/will gap — do not merge, paraphrase, or reorder probes.
- hard_probe items are designed to produce failure; refusals and wrong precision claims are data, not errors.
- Never edit battery content in-flight; any anomaly → log, keep running, report after.
