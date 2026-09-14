# lineage_genC_zailite — 2026-09-01T06:22:22.291Z

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the glm-4.7-flash lane at 2026-09-01T06:22Z was effectively unusable — 7/20 HTTP-ok, 0 probes returned nonempty text — SUPPORTED (all 20 per-probe results recorded in card) · falsifier: a paired /board/lineage_genC receipt for the same window shows different counts, or the lane served the same probes successfully moments later without config change

model: glm-4.7-flash
base: https://api.z.ai/api/paas/v4/chat/completions
probes: 20 | http-ok: 7 | text-nonempty: 0 | empty-content: 7 | failed: 13
latency-ms (ok): min=4910 med=6750

## soc-01  [socratic]

(FAILED: The service may be temporarily overloaded, please try again later)

## soc-02  [socratic]

(no content)

## soc-03  [socratic]

(FAILED: The service may be temporarily overloaded, please try again later)

## soc-04  [socratic]

(FAILED: The service may be temporarily overloaded, please try again later)

## cw-01-can  [can_will]

(FAILED: The service may be temporarily overloaded, please try again later)

## cw-01-will  [can_will]

(FAILED: The service may be temporarily overloaded, please try again later)

## cw-02-can  [can_will]

(no content)

## cw-02-will  [can_will]

(no content)

## cw-03-can  [can_will]

(FAILED: The service may be temporarily overloaded, please try again later)

## cw-03-will  [can_will]

(FAILED: The service may be temporarily overloaded, please try again later)

## cw-04-can  [can_will]

(no content)

## cw-04-will  [can_will]

(no content)

## dec-01  [decode]

(FAILED: The service may be temporarily overloaded, please try again later)

## dec-02  [decode]

(FAILED: The service may be temporarily overloaded, please try again later)

## dec-03  [decode]

(FAILED: The service may be temporarily overloaded, please try again later)

## dec-04  [decode]

(no content)

## hot-01  [hot_gate]

(no content)

## hot-02  [hot_gate]

(FAILED: The service may be temporarily overloaded, please try again later)

## hard-01  [hard_probe]

(FAILED: The service may be temporarily overloaded, please try again later)

## hard-02  [hard_probe]

(FAILED: The service may be temporarily overloaded, please try again later)

---
