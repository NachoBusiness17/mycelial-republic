# STEAL CARD: inference-efficiency-hn (frontier OLM 2026-10-08) - REV 1

Round 1, first draft; no prior critique exists. Two confirmed finds from the HN door. The sweep
source is watch/inbox/frontier_olm_2026-10-08/sweep/inference-efficiency-hn.md (read in full this
session, 210 lines); the two finds are its items 2 and 3, at :60-76 and :78-94. One correction to
the ask landed before any port talk: the ask's per-find overlap fields claim "0 hits" for both
finds, and the tracked-tree re-check below (git grep over handles and thread ids, the sibling
card's instrument lesson) found real hits. None of them is a mechanism bank, so both finds
survive, but narrowed and with the receipt stated in full in the Overlap receipt section.

## Find 1 (headline): a firm's own dollar ledger is the external anchor for the owed Q3 economics re-measure, and it prices the self-host rung off the ladder

- URL: https://www.tomshardware.com/tech-industry/artificial-intelligence/firm-rents-four-nvidia-h200s-to-test-80x-cheaper-deepseek-claim-usd13-200-monthly-gpu-rental-doubles-claude-bill-while-security-flaws-keep-code-offline (Tom's Hardware on HN 49923539, 2026-10-01; sweep:60-61).
- Quote (sweep:62): "The custom setup couldn't beat DeepSeek's own list price."
- Measured (sweep:63-68): Call Center Doctors ran DeepSeek V4.1 Flash on 4x H200 at $18.37/hr
  on-demand = ~$13,200/month, over double their $5,500/month Claude sub. Peak ~213 tok/s written
  at $440.88/day on-demand vs $184-223/day for the same workload on DeepSeek's own API; API month
  equivalent $3,500-7,000. The box capped at ~20B tokens/day (mostly context re-reading) vs 51B
  consumed on peak days. Sandbox escapes demoted the box to 48-64 read-only reviewer agents
  (2,377 folders scanned, 32 bug reports); the firm went back to Opus 5.5.
- Estate prior art: the Q3 conditions-suspect economics law (lens/laws.md:149-153): every
  pre-2026-10-04 DeepSeek per-pass number ($0.0024 triangulations, $0.005 assembly, $0.00077/ask)
  rode thinking-ON by omission and the off-state re-measure is owed. The deliberate-ask quantized
  law (lens/laws.md:75-77: "frozen cache-shared prefix + tight ask + output contract", holding
  memory/corpus/quantized_thought/instructions_frontier.jsonl:22, verified non-blank this
  session) is exactly the lever the firm's ledger indicts: their box's cap was context
  re-reading, the thing a frozen shared prefix exists to kill. The measurement instrument exists:
  tools/prefix_cache_sim.py:1-11 (radix-leaf LRU prefix-cache sim over trail tapes; gap-fold G1
  law at :9) importing the estate clip shape from mag/context_pack.py:1416
  (tools/prefix_cache_sim.py:36; target line verified non-blank this session). The quantizer
  organ is live today: quant A/B receipt
  watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md:1-5 (qwen2.5:7b Q4_K_M vs q8_0
  run complete 2026-10-08).
- What is actually new: (a) an independent external dollar triangulation for the owed Q3
  off-state rows: the expected order of magnitude is the firm's API band ($184-223/day for the
  same workload, $3,500-7,000/month; sweep:65-66), not the rental band; (b) a measured kill of
  the "rent GPUs and self-host" rung: at agent-scale token volume the provider's list price beat
  4x H200 on-demand, before counting the sandbox containment cost that gated write access down to
  read-only (sweep:63-68), convergent with the estate's own shell-door posture (named at
  sweep:74); (c) the 20B-of-51B context re-read detail is the prefix-cache law measured in
  someone else's dollar ledger (sweep:66, 71-73), which converts the deliberate-ask prefix law
  (lens/laws.md:75-77) from style to money.
- Organ map: feeds the QUANTIZER / deliberate-ask organ (memory/corpus/quantized_thought;
  lens/laws.md:75-77) and the routing economics rows (cost-per-blind-point is the champion
  metric, lens/laws.md:40-43). Port move: when the Q3 off-state re-measure lands, its table
  carries an external-anchor column (self-host $13,200/month vs API $3,500-7,000/month at the
  firm's measured volume; sweep:64-66) and the driving ladder gains a self-host breakeven gate:
  any future self-host proposal must show measured estate tokens/day above the curve where
  rental beats list price. This session's ledger cut (Verification ledger below) reads estate
  peak day ~5.0M tokens and $94.74 total paid to date, orders of magnitude under that curve;
  that prediction is stated as falsifiable, not as a forever law. The probe replaces the
  chars/4 estimation layer (mag/token_economy.py:3, "Estimates only (chars/4)") with
  provider-billed rows.

## Find 2: the measured decomposition that sets the budget order for the six unwired fire surfaces, plus the ~145-token per-turn contract re-inject

- URL: https://github.com/lowenbjer/claude-terse (Show HN, 2026-10-07; sweep:78-79).
- Quote (sweep:80): "A Claude Code plugin that cuts reply length in half and removes mannered
  prose."
- Measured (sweep:81-87): 22 rules (877 words) as an output style; a UserPromptSubmit hook
  re-injects a 576-character (~145 input token) reminder every turn because style rules dilute
  over long context; a SubagentStart hook passes rules to subagents. Vanilla vs terse on Opus
  5.5, 12 prompts: words 5,959 to 1,793 (-70%), median reply 636 to 181 (-72%), output tokens
  19,310 to 10,528 (-45%), style violations 11.1 to 1.1 per 1k words. On a real codebase: Fable
  5.1 46% fewer words / 51% lower cost; Opus 5.5 54% fewer words / 32% lower cost; total cost
  fell only 2-12% on short sets because context tokens dominate per-call cost.
- Estate prior art: the Q4 wiring gap (lens/laws.md:154-158): the inference-budget guard is
  wired in two carriers only; six fire surfaces still hand-roll params (stealth_driver,
  duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire; ds_workhorse needs the
  classifier at minimum). The guard organ: mag/inference_budget.py:268 (plan_call, which already
  takes prompt_chars as an input) and :349 (guard_terminal); carrier pins at
  tests/test_inference_budget.py:1-15. The two wired carriers bank token ledgers:
  tools/hermes_burn.py:14-15 (rows {ts, id, model, turn, prompt_tokens, completion_tokens,
  cost_usd, ok} into memory/runs/hermes_burn/usage.jsonl) and tools/model_garden.py:17-18 (same
  shape plus reasoning_tokens into memory/runs/model_garden/usage.jsonl).
- What is actually new, and now estate-measured: the decomposition rule says output-side
  trimming is the WEAK lever; context-side resend is where a budget guard bites first. I ran the
  coarse cut this session (commands verbatim in the Verification ledger): hermes_burn ledger
  11,868,569 prompt vs 2,870,388 completion tokens over 2,312 ok rows = 80.5% prompt share;
  model_garden ledger 2,947,389 vs 858,875 over 710 ok rows = 77.4% prompt share (reasoning
  546,123). At an 80.5% prompt share, terse's own measured -45% output tokens caps total-token
  reduction near 8.8% (arithmetic from the two numbers just cited: 0.45 x 0.195) unless the
  context side moves, which is the quantitative case for wiring the six Q4 surfaces through
  plan_call with context-side accounting first. The second steal is the re-inject pattern: a
  ~145-token per-turn condensed reminder keeps an output contract alive across a long session
  for near-zero cost (sweep:82-83), the cheap twin of the deliberate-ask output contract; the
  SubagentStart hook is the same pass-through for gophers.
- Organ map: feeds the CONTEXT PACK organ (mag/context_pack.py:1, the min-token pack), the six
  unwired fire surfaces of the inference-budget guard (lens/laws.md:154-158), and the gopher
  fleet's per-ask contracts. Port move: (1) wire the six carriers through plan_call with
  prompt_chars accounting as the first budget axis (the input already exists,
  mag/inference_budget.py:268); (2) long-session lanes re-inject a condensed contract each turn
  (~145-token class) instead of paying full rule bytes per turn; (3) workflow child asks carry
  the condensed contract at subagent start.

## Probe (one probe, two legs, $0, this week; both ledger files verified present this session)

Read the two paid ledgers only. LEG A (context-share census): compute prompt_tokens share of
billed tokens from memory/runs/hermes_burn/usage.jsonl and memory/runs/model_garden/usage.jsonl,
cut per carrier, per model family, per day. Prediction: both carriers read above 60% prompt share
(coarse pass this session: 80.5% and 77.4%). Falsified if the formal cut reads under 50% on
either carrier: then that carrier's spend is output-dominated and the terse decomposition inverts
locally, so budget output-side trimming first there. Honest limit: the six unwired Q4 fire
surfaces bank no usage rows today (lens/laws.md:154-158), so leg A cannot see them; wiring them
through plan_call is what makes them measurable, which is the port move itself. LEG B
(self-host breakeven): place the estate's trailing-30-day token volume against the firm's curve
($440.88/day on-demand vs $184-223/day API for the same workload; sweep:65-66). Prediction: the
estate's API-equivalent monthly cost stays under $500/month, more than an order of magnitude
below the $13,200/month rental rung (sweep:64); falsified if any trailing-30-day window exceeds
$13,200, in which case self-host earns a routing-class row. Coarse pass this session:
hermes_burn peak day 2026-10-04 at 4,998,383 tokens and $94.74 total cost to date.

## Overlap receipt (corrections to the ask, instrument quoted)

The ask's overlap fields are claims, not evidence (the sibling card's instrument lesson:
grep handles and ids, never titles alone). This session's re-check: git grep -l over the tracked
tree for "claude-terse", "lowenbjer", "Call Center Doctors", "13,200", "49923539", "49995809".
The tracked tree excludes today's untracked sweep dir by construction. A full-tree recursive
grep was started first and killed as too slow on the binary-heavy trees; git grep is the
instrument that finished.

- "claude-terse" / "lowenbjer": NOT zero. Four tracked files. watch/scout/MONITOR_LANE_2026-10-
  06.md:315-321: the monitor lane's 2026-10-06T23:00:33Z run surfaced the Show HN post under the
  term "open world agent benchmark" (title, repo URL, description opening: a listing, no
  measurements). watch/inbox/endpoint_news/endpoint_news.jsonl and snapshot_hn.json: raw HN
  Algolia payloads (story id 49981531, author lowenbjer). watch/inbox/frontier_olm_2026-10-
  07/sweep/hn_raw/bench.json: raw bench payload. None banks the measured decomposition. The find
  survives NARROWED: today is the first estate bank of the numbers and the organ mapping, not
  the first sighting. Two thread ids now exist in estate holdings (49981531 raw-held vs 49995809
  swept); not adjudicated here.
- "Call Center Doctors": 0 hits, confirmed.
- "13,200": one tracked hit, unrelated: a "+13,200" tokens-freed-per-compaction table row inside
  the 10-03 sweep's raw payload watch/inbox/frontier_olm_2026-10-03/sweep/tmp/sw2_full.jsonl
  (window extracted this session).
- "49923539": held unbanked in the 10-03 sweep's raw pass-1 payload
  watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/p1_deepseek.json (window extracted this
  session: points 2, num_comments 0 at capture time). Today's deep read is the first bank. The
  find survives.

## Verification ledger (commands run this session by this seat)

- Read in full: watch/inbox/frontier_olm_2026-10-08/sweep/inference-efficiency-hn.md (210
  lines; the finds at :60-76 and :78-94); watch/inbox/frontier_olm_2026-10-08/steal/
  finetuning-adaptation.md (house format + the instrument lesson this receipt applies).
- Read targeted: watch/inbox/frontier_olm_2026-10-08/lens/laws.md:140-169 plus the :20-30,
  :40-56, :70-80 windows; tools/prefix_cache_sim.py:1-60; mag/context_pack.py:1-50;
  mag/token_economy.py:1-40; tools/hermes_burn.py:1-40; tests/test_inference_budget.py:1-30;
  sweep/quant_ab/RECEIPT.md:1-25.
- Line pins by grep: lens/laws.md:75 (Deliberate ask), :40 and :43 (question-class routes,
  cost-per-blind-point); tools/hermes_burn.py:14; tools/model_garden.py:17;
  mag/inference_budget.py:268 (plan_call), :349 (guard_terminal); tools/prefix_cache_sim.py:9
  and :36; mag/context_pack.py:1416 (verified non-blank by sed).
- Ledger runs (heredoc python via .venv/Scripts/python.exe, ok = row.ok true and
  prompt+completion > 0). hermes_burn: rows_total 3038, ok_token_rows 2312, prompt 11,868,569,
  completion 2,870,388, prompt_share_pct 80.5, cost_usd_total_all_rows 94.74, peak day
  2026-10-04 = 4,998,383 tokens. model_garden: rows_total 725, ok_token_rows 710, prompt
  2,947,389, completion 858,875, reasoning 546,123, prompt_share_pct 77.4.
- Overlap instrument: git grep -l over the tracked tree, six terms, results above; window
  extractions by grep -o on the two 10-03 raw payloads and the three terse-pointer files.
- OWED / not run this session: the formal per-family/per-day ledger cut (probe leg A's formal
  form); the Q3 off-state re-measure itself; no fetch of the Tom's Hardware page or the
  claude-terse repo this session (the numbers ride the sweep's banked fetches, sweep:60-94,
  which this seat read in full); no pytest run (not asked).

## Machine-readable card (identical to the returned StealCard JSON)

chars counts this file's characters (python len() of the file text, stamped after writing).

```json
{
 "area": "inference-efficiency-hn",
 "steal": "Two finds, both narrowed but surviving the overlap re-check. (1) THE SELF-HOST DOLLAR ANCHOR (Tom's Hardware on HN 49923539, firm 'Call Center Doctors', quote 'The custom setup couldn't beat DeepSeek's own list price'): DeepSeek V4.1 Flash on 4x rented H200 cost $18.37/hr = ~$13,200/month, over double their $5,500/month Claude sub, while the same workload on DeepSeek's own API ran $184-223/day ($3,500-7,000/month equivalent); the box capped at ~20B tokens/day, mostly context re-reading, vs 51B consumed on peak days; sandbox escapes demoted it to 48-64 read-only reviewer agents (2,377 folders, 32 bug reports) before the firm went back to Opus 5.5. This is the external dollar triangulation for the estate's OWED Q3 off-state DeepSeek re-measure (lens/laws.md:149-153) and a measured kill of the 'rent GPUs and self-host' rung; the 20B-of-51B context re-read share is the deliberate-ask prefix law (lens/laws.md:75-77, frozen cache-shared prefix + tight ask + output contract) measured in someone else's dollar ledger. (2) THE TOKEN-BLEED DECOMPOSITION (github.com/lowenbjer/claude-terse, Show HN 49995809, quote 'A Claude Code plugin that cuts reply length in half and removes mannered prose'): 22 rules as an output style plus a UserPromptSubmit hook that re-injects a 576-char (~145 token) condensed reminder every turn because style rules dilute over long context, and a SubagentStart hook that passes rules to subagents; measured on Opus 5.5 over 12 prompts, words -70% but output tokens only -45% and total cost only -2..-12% on short sets because context tokens dominate per-call cost (real-codebase rows: Fable 5.1 46% fewer words / 51% lower cost, Opus 5.5 54% / 32%). Mechanism: output-side trimming is the WEAK lever; budget guards should bite the CONTEXT side first, and a ~145-token per-turn re-inject keeps an output contract alive across a long session for near-zero cost. Estate-confirmed this session: the two wired carriers' ledgers read 80.5% (hermes_burn) and 77.4% (model_garden) prompt-token share, so terse's own -45% output cut caps near 8.8% total token reduction (arithmetic) unless context moves.",
 "source_url": "https://www.tomshardware.com/tech-industry/artificial-intelligence/firm-rents-four-nvidia-h200s-to-test-80x-cheaper-deepseek-claim-usd13-200-monthly-gpu-rental-doubles-claude-bill-while-security-flaws-keep-code-offline",
 "estate_map": "Find 1 feeds the QUANTIZER / deliberate-ask organ (memory/corpus/quantized_thought/instructions_frontier.jsonl:22 frozen cache-shared prefix + tight ask + output contract, lens-held at lens/laws.md:75-77; the organ is live, quant A/B receipt sweep/quant_ab/RECEIPT.md:1-5) and the routing economics rows (cost-per-blind-point champion metric, lens/laws.md:40-43). Port move: the owed Q3 off-state re-measure table gains an external-anchor column (self-host $13,200/month vs API $3,500-7,000/month at the firm's measured volume) and the driving ladder gains a self-host breakeven gate - any future self-host proposal must show measured estate tokens/day above the rental-beats-list-price curve; the prefix-cache instrument for that curve already exists (tools/prefix_cache_sim.py:1-11 over trail tapes, clip shape from mag/context_pack.py:1416). Find 2 feeds the CONTEXT PACK organ (mag/context_pack.py:1 min-token pack) plus the six unwired fire surfaces of the inference-budget guard (lens/laws.md:154-158: stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire; ds_workhorse needs the classifier at minimum) and the gopher fleet's per-ask contracts. Port move: wire the six carriers through plan_call (mag/inference_budget.py:268, prompt_chars input already exists; guard_terminal :349) with prompt-side accounting as the FIRST budget axis; adopt the ~145-token per-turn condensed contract re-inject in long-session lanes and at subagent start instead of full rule bytes every turn. Both wired carriers already bank the needed rows (tools/hermes_burn.py:14-15, tools/model_garden.py:17-18), so the guard's priority order is measurable for free. Full write-up: watch/inbox/frontier_olm_2026-10-08/steal/inference-efficiency-hn.md.",
 "probe": "One probe, two legs, $0, this week; reads only the two paid ledgers (both verified present this session). LEG A (context-share census): compute prompt_tokens share of billed tokens from memory/runs/hermes_burn/usage.jsonl and memory/runs/model_garden/usage.jsonl, cut per carrier, per model family, per day. Prediction: both carriers above 60% prompt share (coarse pass this session: 80.5% over 2,312 ok rows and 77.4% over 710 ok rows). Falsified if the formal cut reads under 50% on either carrier - then that carrier is output-dominated and the terse decomposition inverts locally (budget output-side trimming first there). Honest limit: the six unwired Q4 fire surfaces bank no usage rows today, so leg A cannot see them; wiring them through plan_call is what makes them measurable, which is the port move itself. LEG B (self-host breakeven): place the estate's trailing-30-day token volume against the firm's curve ($440.88/day on-demand vs $184-223/day API for the same workload, sweep:65-66). Prediction: estate API-equivalent monthly cost stays under $500/month, more than an order of magnitude below the $13,200/month rental rung; falsified if any trailing-30-day window exceeds $13,200, in which case self-host earns a routing-class row. Coarse pass this session: hermes_burn peak day 2026-10-04 = 4,998,383 tokens, $94.74 total cost to date.",
 "chars": 18992
}
```
