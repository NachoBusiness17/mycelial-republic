---
name: ox-alpha-was-glm53-flash
description: receipt 2026-09-17 — OpenRouter stealth/ox-alpha's 404 body revealed it
  WAS z-ai glm-5.3-flash; SUPERSEDED same day by operator "we're using union" —
  build lane = stealth/union-alpha first, both OpenRouter keys rotated; env
  OPENROUTER_MODEL is an old config, ignored
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

The operator's second OpenRouter key (OPENROUTER_API_KEY_2) with env OPENROUTER_MODEL=
stealth/ox-alpha hit HTTP 404 on 2026-09-17 whose body said: "Thank you for participating
in the Stealth Ox Alpha testing period. This model was ZAI's GLM-5.3 Flash. Use it now:
https://openrouter.ai/z-ai/glm-5.3-flash."

Facts:
- stealth/ox-alpha window ENDED; the model identity was glm-5.3-flash all along — the
  operator's "we have a parallel line to 5.3 flash" was literal.
- **SUPERSEDED hours later by the operator: "i know what ox is thats an old config.
  we're using union. gogo"** — the build lane model chain is now state-sticky →
  `stealth/union-alpha` → `z-ai/glm-5.3-flash` (direct id, fallback); env
  OPENROUTER_MODEL is stale and deliberately ignored by the lane.
- **Both OpenRouter keys are one pool**: build_lane_game.py rotates
  OPENROUTER_API_KEY_2 → OPENROUTER_API_KEY on 429/401/402; each receipt row records
  key_index.
- glm-5.3-flash via OpenRouter has an unbounded reasoning channel on complex prompts:
  with ANY max_tokens cap (2600/4200/9000/16000 all tried) it returns empty_content with
  finish=length — the cap is the bug. Fix = REMOVE max_tokens entirely; short prompts
  return content fine. See [[no-token-caps-100k-windows]].
- build_lane_game.py prunes transport-failure deaths (empty_content/HTTP/SSRF) from the
  dead list so briefs keep their real 2 merit attempts.

- **UPDATE (2026-09-17 night): the stealth family RE-OPENED.** OpenRouter's Stealth page
  confirms BOTH Union Alpha and Ox Alpha live (new window opened Sep 14 — the Aug 20-25
  window peaked ~6T tokens/day industry-wide). ox-alpha is back in the research driver's
  lane set on both keys; union-alpha remains the build lane primary.

- **UPDATE (2026-09-17 ~21:00Z): the union-alpha window ENDED — the 404-body migration
  law confirmed twice now.** The 404 body named the successor: unbiased/pareto (filed to
  LINKS). Drivers updated to strike pareto first, union kept until the models endpoint
  stops 404ing. The MODEL LAW held through the event: the fallback (glm) served one run
  only and never persisted; the sticky model stayed union/primary per the no-silent-
  downgrade rule.

Related: [[lite-key-seat-glm53flash]], [[union-alpha-free-window-20260916]],
[[union-fullsend-day-20260917]], [[operator-usage-as-probe]], [[elder-audit-3-passes]].
