# B2-36 Cerebras lane reclassify (2026-09-26)

## Verdict

LANDED. Cerebras is off the standing free-lane ladder and reclassified as a
card-gated 30-day trial, dormant pending operator GO: removed from
prefer_order and all 6 routing lists, provider block carries dormant: true,
the live-verified 2-model catalog, and the trial denominators (5 RPM / 90K
total TPM / 1M TPD, no RPD). The operator card decision is surfaced in
queue/todo.md as P0 with a real deadline, 2026-10-03.

## Evidence with file:line quotes

- Pointer row, watch/inbox/LINKS.jsonl:314 (ALERT-CEREBRAS-TRIAL-GATE,
  endpoint-news 2026-09-26T11:37:05Z): "payment method mandatory at sign-up,
  5 dollars in credits expire after 30 days, table shows 5 RPM / 90K total
  TPM / 1M TPD and NO RPD, on exactly two models (gpt-oss-120b,
  qwen-3.8-27b)"; detail: "live probe 2026-09-26 with existing key: GET
  /v1/models HTTP 200 returning exactly those 2 models".
- B2-04 receipt, B2_04_provider_health_20260926.md:8-9: "cerebras 402 (no
  credit)" measured from the live chat call, the lane was already dead.
- Prior operator ask, watch/inbox/LINKS.jsonl:297 (ALERT-CEREBRAS-CARD,
  2026-09-21): "operator decision required (card on file vs skip the lane)",
  severity "operator-decision", 5 days unanswered.
- Post-edit configs/providers.yaml:25: "# 2026-09-26: cerebras REMOVED from
  the standing free ladder"; :535 "name: Cerebras (card-gated 30-day trial,
  dormant pending operator GO)"; :550 "dormant: true   # card-gated trial;
  operator GO flips this + re-adds to prefer_order"; :560-561 models
  gpt-oss-120b + qwen-3.8-27b (gemma-4-31b dropped, gone from live catalog);
  :667-676 routing comment plus public_summarize/default lists without
  cerebras. yaml.safe_load passes; no routing list retains cerebras.
- Mechanism is real: mag/doctor.py:441 "dormant: true  DORMANT, declared
  state, never probed, never alarms"; the saelis block (providers.yaml:42)
  is the precedent dormant lane sitting outside every list.
- Deadline grounding: the repo 7-day staleness law (AGENTS.md build
  discipline, freshness_check) makes the 09-26 trial-gate intel stale
  2026-10-03; the 30-day credit expiry is Cerebras docs verbatim via row 314.
- Tests: tests/test_doctor_provider_endpoints.py + tests/test_seat_corpus.py,
  17 passed post-edit.

## Work done

1. Read the cerebras block, ladder lines, LINKS rows 297/314, B2-03/B2-04/
   B2-35 receipts, and the doctor dormant law before touching bytes.
2. Swept consumers: doctor.py already classifies the 402 cerebras class
   (B2-21 wiring); mag/ code hardcodes (fuel_feed, rotation_harness,
   lane_salon, quorum_window, research_fanout, cost_truth, free_tier) are
   behavior-owned elsewhere, not reclassified here, filed as B2-78.
3. Applied the three providers.yaml edits (ladder, block, routing), kept the
   block as the knowledge carrier, em-dash law checked and one violation in
   my own new text fixed.
4. Validated YAML shape with .venv python asserts; ran the 2 pinning test
   files (17 passed).
5. Surfaced the operator decision in queue/todo.md:3 as P0, GO/NO-GO by
   2026-10-03, with the 30-day credit window named for any GO.
6. Filed this receipt, ledger row, and 2 self-feed briefs (B2-133, B2-134;
   first appended as B2-78/79 before seeing a concurrent lane had taken those
   numbers, corrected in place same hour per the B2-35 precedent).

## Falsifier

This lane is inverted if: (a) a re-probe shows Cerebras restored a no-card
free tier (docs row 314 no longer matches the cited URL, reclassify back);
(b) the live catalog grows beyond the 2 listed ids while dormant (block
roster stale, re-probe before any GO); (c) a chat call with the fleet key
returns 200 with content before any card attach (the 402 claim dies, dormant
is overcautious and the lane re-enters the ladder); (d) queue/todo.md loses
the P0 row before the operator answers (decision surface rotted, my
surfacing failed).

## Bibliography closed

watch/inbox/LINKS.jsonl:297 and :314, read in full; configs/providers.yaml
(edited, gitignored per B2-35 note so the landing is the live file);
mag/doctor.py dormant law; watch/inbox/burn_wave_20260926/
B2_04_provider_health_20260926.md and B2_35_groq_surgery_20260926.md
(pattern); queue/todo.md:3 (decision surface); inference-docs.cerebras.ai
rate-limits page accepted via row 314 same-day quotes, not independently
fetched (no browser in this lane).
