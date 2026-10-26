# VISION WATCH 20260906 — the first standing eye digest (BATCH5 v1)

Operator's order: "vision agents watching all of these things so we can steer them."
This is that watch. Law: code owns numbers (digest.txt, generated from db/room/chain),
eye owns patterns (qwen2.5vl:3b reads the board image). Re-run command at the bottom.

## ORGAN STATE (the 1210 autopsy + informed retry)
- R5's 1210 "[图片输入格式/解析错误]": NOT size, NOT malformed PNG. Board is a pure-stdlib
  PNG (960x640, 8-bit RGB, non-interlaced, IHDR/IDAT/IEND only, 9,248 bytes). Cause
  (SUPPORTED): the deepseek-v4-flash-vision-exp parser rejects the stdlib-rendered PNG as
  sent (data-URL base64); JPEG re-encode (640x427 q75) of the SAME board went through clean.
  Which property exactly (PNG-ness vs pixel dims) is UNPROVEN — single sanctioned retry.
- Second organ fact: mcp__mag__vision runs IN THE CAGE (/app). Host paths C:/... do not
  resolve (FileNotFoundError before any provider call). Images must be cage-visible
  (/app/... — the repo is a live bind mount, host writes appear instantly).
- Verdict: ORGAN WORKS with <JPEG re-encode + /app cage path>. Note: default max_tokens
  1024 truncated the read mid-sentence — pass a higher cap for full reads.
- The LOCAL eye (ollama qwen2.5vl:3b, loopback :11434) reads ANY image (board.png,
  burn_board.png both verified this pass), ~60s, $0. It is the standing eye; the DeepSeek
  organ is the bonus lens. Eye number-discipline is weak (it cited "error count 38" — no
  such value in ERRORS/DAY row) — always pair its patterns with digest.txt numbers.

## WHAT THE EYE SAW (fresh pass 20260906T014838Z, plus R3's 20260906T014208Z)
- Board shape: 4 panels. A = stacked burn bars rising across the window, tallest columns
  at the right (09-03..09-05). B = white seat bars with red error ticks above them,
  ticks cluster late-window and thicken toward 09-05. C = room events, tall early-mid
  window then settling. D = chain knots, one dominant spike (09-01), then steady ~180/day.
- Eye pattern verdicts: burn RISING (not falling), errors CONCENTRATED in the last 3 days
  of the window, one-day knot spike, no empty recent days (fleet active every day since 09-01).
- burn_board.png (eye, arbitrary-image read): spiky columns, NO red/danger markers, flat
  short bars in the middle region — matches a healthy-but-uneven burn.

## NUMBERS THE CODE OWNS (digest.txt, 20260906T014838Z)
- Census 14d: 3.8B tokens, 3 seats, 935 errors, 6,335 room events, 7,291 knots, 608 cards.
- ERRORS/DAY (08-24..09-06): 0 8 28 41 32 111 78 0 42 59 86 133 286 19 — 09-05 = 286 is the
  all-window peak; 09-06 partial = 19 at 01:48Z.
- GLM-5.3-Flash MTok/day: ...417.7 (09-04) 523.0 (09-05) 39.4 (09-06 partial, was 31.2
  six minutes earlier — live batch is burning now). GLM-5.3 today: 0.0 (lane idle).
- Sessions/day: 95 on 09-05, 24 so far today. Knots today: 0 (none sealed yet today).

## 3 STEERING SIGNALS for the live batch
1. ERROR RUNG-DOWN — eye saw: red ticks thickening over the last window days. Number:
   errors/day hit 286 on 09-05 (window peak) and +12 in 6 min during this watch (923->935).
   Action: if the next snapshot shows today's errors/day > 100, step the batch width DOWN
   one rung and check the failing lane before re-ramping.
2. BURN RUNG-UP / THROTTLE — eye saw: stacked bars rising, tallest at 09-05. Number:
   Flash burned 523.0 MTok on 09-05; today already 39.4 MTok by 01:48Z with the batch live.
   Action: bars flat (<100 MTok/day by mid-day) while workers report success -> widen one
   rung; any single day > 600 MTok -> throttle to protect the Sep-20 quota envelope.
3. BOARD FRESHNESS (ops hygiene) — eye reads the FRESH run-dir board, but the human-facing
   dashboard/static/swarm_board.png is stale since 09-05 12:37 (9,248 bytes). Action: when
   static board age > 6h, copy the latest run dir's board.png over it so the operator's
   dashboard shows what the eye actually read. (One-liner: cp memory/runs/swarm_snapshot/<ts>/board.png dashboard/static/swarm_board.png)

## THE ONE COMMAND (the standing vision agent)
    python -m mag.swarm_snapshot
Run from repo root, ~60s, $0: re-collects 14 days of state, re-renders the board,
eye-reads it against the numbers digest, banks memory/runs/swarm_snapshot/<ts>/
(board.png, digest.txt, vision_read.md). Point it at a schedule or a worker and the
operator's "vision agents watching" is real. For the DeepSeek organ: JPEG + /app path only.
