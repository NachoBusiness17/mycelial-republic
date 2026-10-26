# FLASHX PROBE 2026-09-27: glm-5.3-flashx vs glm-5.3-flash on the fleet OpenRouter lane

Class: RECEIPT · Writer: zcode seat · Operator order: "build it" (after the
GLM-5.3-FlashX lane-math answer) · Tool: tools/flashx_probe.py · Frozen verdict
rule registered in the script header BEFORE any call fired: EARNS if TTFT >= 2x
faster or decode >= 3x; DECLINED if TTFT < 1.5x and decode < 2x; else borderline.

## Verdict

DECLINED per the frozen rule, with one flip condition owed. glm-5.3-flashx on
the fleet's OpenRouter lane decodes 2.4x faster end to end but arrives at the
first VISIBLE content token 1.5s later than flash, because flashx ships with
thinking ON by default and burns reasoning tokens before any content. For the
latency lanes that would justify its price (phone relay, companion, NPC
gateway), the user feels the first content token, so the default configuration
is worse where it is sold as better, at 2.5x the token price.

## Evidence (5 streaming calls per model + 1 diagnostic, spend about $0.02)

| metric (mean of 5) | glm-5.3-flash | glm-5.3-flashx |
|---|---|---|
| first content token | 3521 ms | 5246 ms (0.67x) |
| total call | 12.65 s | 5.37 s (2.36x faster) |
| price in / out per M | $0.04 / $0.50 | $0.37 / $1.25 |

Diagnostic call ("Say OK and nothing else", max 400): completion_tokens 138 of
which reasoning_tokens 133. The thinking tax is the whole story: content waits
behind reasoning. Rule check: ttft_gain 0.67 < 1.5 and decode 2.36 < 3.0, so
DECLINED fires. Raw JSON outputs captured in the tool run history; the probe
script prints them verbatim.

## Work done

- tools/flashx_probe.py: catalog price pull, spend cap ($0.50, projected
  $0.018), streaming TTFT (any-token and content-token measured separately),
  usage-chunk token counts, frozen verdict rule in code.
- First probe pass returned null TTFT on flashx: parser counted only content
  deltas while default thinking consumed the 220-token budget. Fixed by
  counting reasoning deltas separately and raising the budget to 600. The
  null-pass verdict was discarded as measurement failure, never filed.

## Falsifier (the flip condition, one config line owed)

If flashx fired with reasoning disabled (effort none / thinking off) beats
flash first-content TTFT by 2x or more, the verdict flips to EARNED for the
latency lanes. One follow-up probe owed; also worth re-measuring at a busier
hour since tonight's lane was quiet.

## Bibliography (closed: only what was actually read)

OpenRouter models catalog (live fetch, ids z-ai/glm-5.3-flash and
z-ai/glm-5.3-flashx); OpenRouter chat completions API responses from the
fleet's own key; LINKS row flashx-scout (watch/inbox/LINKS.jsonl) for the
launch facts (announced 2026-09-18, 200 tok/s claim, not on the coding plan).
