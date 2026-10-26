# WARMED_CONTEXT - the boot pack for every cross-model ractoring lane (2026-10-01)

Lane 0 (RIB WARM + CLARITAS) of the cross-model ractoring program. Sibling lanes
cite THIS file instead of re-reading the ribs. Every line below is distilled from
byte-read ribs and receipts this session; each section names its sources. If a
sibling needs the full evidence trail behind a law, the rib source is the pointer.

Moment: written 2026-10-01 (late UTC). Instruments: Read on the six source docs
+ grep sweeps + live face_for probes via .venv/Scripts/python.exe (output
transcribed below). No code under mag/ or tools/ was touched, so the
violation_ratchet step is not owed (watch/inbox only, same precedent as
watch/inbox/48h_synth/laws.md).

## PART 1: THE 10 LAWS THAT GOVERN CROSS-MODEL RACTORING

1. RIBS BEFORE MECHANISMS: load ribs + current state before building anything;
   the estate has already solved most of what a fresh seat is about to hand-roll.
   Source: RIB_DRIVING_LADDER_20260928.md (boot-order clause) + AGENTS.md load order.

2. PER-ANIMAL HARNESS: every family gets its own transport, rails, failure modes
   and proven shapes; never assume the last animal's harness fits the next one.
   Source: memory/rib/RIB_MODEL_GATES_20261001.md (the operator law, line 3-11).

3. THE GATE LAW (receipts-first routing + Amendment 10): model choice is a routing
   decision with receipts behind it (the duel table, the GPS momentum badges);
   a model whose fingerprint changed is a NEW animal, cold start, no inherited trust.
   Source: RIB_MODEL_GATES_20261001.md THE GATE LAW + Amendment 10 clause.

4. ONE BUG, ONE REACTION (the reasoning-channel burn): content empty + finish=length
   + burn evidence = EMPTY_REASONING, TERMINAL for that (ask, family); never refire
   the same params (re-fire theater cost $20.53 of $29.91 on descent day 1); the only
   recoveries are re-stage with the FAMILY_TABLE recipe or switch family. Big
   reasoning WITH content arrived never terminals (the kimi guard). Every fire path
   must ride mag/inference_budget.py plan_call + guard_terminal.
   Source: memory/rib/RIB_INFERENCE_BUDGET_20261001.md (the whole rib).

5. CONDITIONS ARE LOAD-BEARING (one-bug law, B2-216 generalized): a verdict without
   its conditions (instrument, moment, price, thinking mode, transport) is not a
   verdict; routing rows expire at 30 days or a family event; supersede, never overwrite.
   Source: RIB_MODEL_GARDEN_ROUTING.md laws 2-3 + watch/inbox/48h_synth/laws.md law 1.

6. INSTRUMENTS ONLY: cells fill only from estate instruments (duels.jsonl, census
   receipts, usage.jsonl, animals/*.jsonl); vendor pages are planning inputs only;
   UNMEASURED is the legal default and hand-copying a vendor number is fabrication.
   Source: RIB_MODEL_GARDEN_ROUTING.md law 1.

7. THE MASK / G2 CROSS-FAMILY LAW: a mask on one mind is decoration; the same mask
   across families is an instrument, disagreement becomes evidence about the question,
   not the renderer; cross-family agreement is the only corroboration that counts
   (G2 supersedes G1); wire divergences into animal_profiles as behavioral rows.
   Source: watch/inbox/RIB_BOOT_DECISION.md (the mask epiphany, GO on G2) +
   RIB_DEEPSEEK_SHOULDERS_20261001.md shoulder 3.

8. HIDDEN OVER VISIBLE (contamination law): estate-facing asks use surfaces the
   families cannot have seen results about, with identical contract text across
   families so diffs attribute to family, not prompt; plain-sight verdicts are
   quarantined (the D6 inversion); a family never sole-judges its own authored text
   (glm-on-glm confound G7) and ember is never the only judge on dollar-routing verdicts.
   Source: watch/inbox/model_garden/GARDEN_RACTOR.md law 3 + PRIORS.md rows 3, 4, 7 +
   RIB_MODEL_GATES_20261001.md (GLM + EMBER rows).

9. DEEPSEEK OWNS THE SHOULDERS: the cheap seat multiplies the premium dollar across
   six shoulders (ask forge, adversary pass, judge number two, assembly, revision
   drafting, bulk ask mining), never the judgment seat; cheap triangulates, premium
   adjudicates, bytes verify.
   Source: memory/rib/RIB_DEEPSEEK_SHOULDERS_20261001.md (THE LAW + six shoulders).

10. SENSING/JUDGMENT SPLIT + SPREAD THE CASH: free and flash lanes are a SENSING
    surface only, their outputs are banked as findings never done-work, verification
    climbs to funded tiers; cash spreads by measured price-per-quality, not evenly
    (anthropic premium gets the slim variant, kimi/glm/qwen/deepseek carry the wide
    grid); grok-4.3 and grok-4.7 are DIFFERENT animals, never confuse them.
    Source: GARDEN_RACTOR.md laws 5-6 + RIB_FREE_USAGE_POLICY_20260823 (via
    RIB_MODEL_GARDEN_ROUTING prior-art block) + RIB_MODEL_GATES_20261001.md (GROK rows).

## PART 2: CLARITAS COVERAGE (mag/claritas.py, probed live this session)

How it resolves: face_for(model_id) -> vendor_for(model_id) via the _MATCHERS
substring list (first match wins) -> FACES dict, falling back to FACE_NEUTRAL
(the house contract). Probes run with .venv/Scripts/python.exe on the garden's
canonical ids (from GRID_*.json + CENSUS.md) and on bare family names.

| family | garden id probed | vendor_for | face | verdict |
|---|---|---|---|---|
| grok-4.7 | x-ai/grok-4.7 and bare grok-4.7 | grok | grok face (distinct) | COVERED |
| haiku | anthropic/claude-haiku-4.5 and bare claude-haiku-4.5 | anthropic | anthropic face | COVERED |
| sonnet | anthropic/claude-sonnet-5.5 and bare claude-sonnet-5.5 | anthropic | anthropic face | COVERED |
| fable | anthropic/claude-fable-5.1 | anthropic | anthropic face | COVERED via the claude substring; BARE "fable-5.1" falls to neutral (no fable matcher) |
| glm-flash | glm-5.3-flash and z-ai/glm-5.3-flash | zai | FACE_NEUTRAL | MATCHED, faceless BY DESIGN (zai maps to the neutral house contract) |
| deepseek-flash | deepseek/deepseek-v4-flash and deepseek-v4.1-flash | deepseek | FACE_NEUTRAL | MATCHED, faceless BY DESIGN |
| kimi | moonshotai/kimi-k2 and bare kimi | neutral (no matcher) | neutral fallback | MISSING: no matcher at all, no vendor attribution |
| qwen-prime | qwen/qwen3.8-max-prime and bare qwen3.8-max-prime | neutral (no matcher) | neutral fallback | MISSING: no matcher at all, no vendor attribution |

Edge findings from the same probes:

- FACES carries 9 keys but only 8 vendors are reachable from _MATCHERS: the
  "ollama" face is dead code (no matcher routes to vendor "ollama").
- Local janitors mis-route: "gemma:2b" matches ("gemma" -> "gemini") and receives
  the GEMINI claritas face, not the intended local/ollama face.
- Distinct faces exist only for grok, anthropic (claude), gemini, openai; the
  ollama face is unreachable; deepseek/zai/cohere/hermes are neutral by design.
- Consequence for this program: garden runs that single-source the system prompt
  from face_for are giving kimi and qwen the undifferentiated house contract, and
  giving local gemma a Google-family face. If lanes want a true same-mask G2
  comparison, either fix the matchers (a code change, out of this lane's scope)
  or pin the system block explicitly per family and disclose it.

## PART 3: THE 5 UNIQUE-INPUT FACTS WE HOLD (per family, PRIORS + today's GRID)

What only that family sees/contributes. Averages are mean score_norm over the
8-item garden battery (B1-B8), all staged 2026-10-01.

1. KIMI (moonshotai/kimi-k2, GRID_kimi1.json, graded 22:17:46Z): avg 0.894 at
   $0.0 metered, and it graded FIRST, so all 10 of its convergence clusters are
   marked "unique" - kimi is the de facto baseline instrument for every later
   cross-family convergence call. Unique misses: B3 LINES-IN-RANGE (cited a line
   beyond file length) and single-bucket evidence. Kimi also minted the
   false-positive guard in the burn law: 234s cold call, 17,617 reasoning tokens
   billed against 354 visible, content ARRIVED = NOT EMPTY_REASONING
   (RIB_INFERENCE_BUDGET_20261001.md + KIMI1_RUN.md). Before today: zero duel
   verdicts ever (PRIORS row 25).

2. SONNET + HAIKU (GRID_ANTHROPIC1.json, the anthropic pair): sonnet tops the
   whole grid at 0.95 ($0.4235, 34/36 checks) and is the only family whose finds
   are byte-verified operator-gate bypasses: self-declared authority_label +
   require_confirmation:false skips the operator gate (lines 246, 301-303), empty
   triple-channel rows never banked with unlimited re-fire (raise before _bank at
   334-335), no spend breaker against the $145 stop, mv handoff loses pending
   items, 7 of 9 aliases lack validators, mode sentinel fails open. Sonnet also
   holds the standing judge2 upset 6-0 over both incumbents (PRIORS row 18).
   Haiku at 0.9188 (unpriced, sonnet-rate upper bound $0.1111) uniquely found the
   preflight 400-char probe blind spot (lines 175-182) and byte-refuted an IMP3
   budget-string claim (line 614 already int-cast). These are the first haiku
   rows the estate holds (PRIORS hole 3).

3. FABLE (anthropic/claude-fable-5.1, GRID_fable1.json): the recipe-boundary
   animal, avg 0.45. It burned BOTH 18KB review asks whole (B1/B5: 12000/12000
   reasoning tokens, empty content, $2.03 of series cost, ramble carrying em-dashes)
   while hitting 0.8 on B3/B4 with convergent cites and 1.0 on B6/B8 byte-exact at
   ZERO reasoning tokens. Fable's unique contribution IS the failure mode: its B1/B5
   burns minted the EMPTY_REASONING terminal amendment (RIB_INFERENCE_BUDGET +
   FABLE1.md; cells re-marked MEASURABLE-WITH-RECIPE in RIB_MODEL_GARDEN_ROUTING).
   Re-fire fable only through plan_call at review-shape floor 24000.

4. GROK-4.7 (GRID_cheapgrid1.json): all 8 cells 0.0 "NO OUTPUT (fire failed)" -
   the cheap-grid runner's transport could not fire it, while the same animal
   holds the V1 adversarial-review championship 9-0 at avg 4.92 ($0.23/answer,
   PRIORS rows 11-12). Grok's unique input today is the transport requirement
   itself: streaming SSE only, whole-response hangs 900s+; a battery lane that
   does not carry the streaming rail measures its own harness, not the animal.
   (Conditions law applied: these zeros are transport zeros, not capability zeros.)

5. THE CHEAP TRIO + LOCAL (GRID_cheapgrid1.json + GRID_local-20261001-a*.json):
   glm53flash 0.831 at ~$0.0015/ask carries the MAX author-confound in the grid
   (the glm-family seat authored and maintains the probed surfaces; its rows are
   the most contaminated and must never stand alone - pair a second family);
   qwen38max 0.719 owns the grid's only B1 zero and a 0.4 B5; ds41flash 0.806
   shows the planning weakness (B7 0.25) that matches its W8 profile (value
   monster, thinking-off mandatory, long-form elsewhere); local gemma2/gemma4/
   gemma:2b measured 0.16/0.53/0.17 mean at 4-49 tok/s with identical ask bytes
   (sha256-proven), the free floor the paid grid sits on.

## CHECKS RUN THIS LANE

- Read: RIB_MODEL_GATES_20261001.md, RIB_DEEPSEEK_SHOULDERS_20261001.md,
  RIB_INFERENCE_BUDGET_20261001.md, RIB_MODEL_GARDEN_ROUTING.md,
  watch/inbox/RIB_BOOT_DECISION.md (the mask/G2 law home, found by widening the
  grep past the two named dirs), watch/inbox/48h_synth/laws.md,
  GARDEN_RACTOR.md, PRIORS.md, CENSUS.md, mag/claritas.py.
- Probes: face_for/vendor_for on 17 model-id strings (table above), plus the
  FACES/matcher set arithmetic, via .venv/Scripts/python.exe, exit 0.
- GRID facts pulled from GRID_kimi1.json, GRID_ANTHROPIC1.json, GRID_fable1.json,
  GRID_cheapgrid1.json, GRID_local-20261001-a_RECEIPT.md with a json parse pass.
- violation_ratchet: NOT RUN, not owed (no mag/ or tools/ edits; watch/inbox only).
- No commits, no paid fires, dash-free by construction (seat law gate rule 2).
