# PRIORS - what the estate already knows about model families (2026-10-01)

Lane 4 (SELF-STEAL) of the model-garden project. Law applied: prior-art sweep
(never relearn a known lesson expensively) + conditions law (every verdict
carries its instrument and moment). One row per (family, capability-verdict,
evidence file, instrument+moment, condition). Status closes each row.

Instruments named once here: DUEL = tools/duel_harness.py v1.1 blind judge
(A/B slots, parity swap, per-criterion 0-5 scores) writing logs/duel/duels.jsonl
via the Nous gateway; ASKBANK = configs/ask_bank v1 hidden-half first draws;
JUDGE2 = deepseek-chat blind second judge (ds_workhorse.py); ALTJUDGE = AJ1
ember-to-glm replay; USAGE-PROBE = operator usage history as pre-verification.

## A. The prior-verdict table

| # | Family | Capability-verdict | Evidence file | Instrument + moment | Condition | Status |
|---|---|---|---|---|---|---|
| 1 | glm-5.3-prime vs qwen3.8-max-prime | PARITY. n=30 blind era: glm 17, qwen 12, tie 1; exact two-sided p=0.4583; Clopper-Pearson 95% CI [0.389, 0.765] straddles 0.5. "Either workhorse, judgment tier", NOT glm dominance | watch/inbox/last_mile_20260930/V8_DUEL_FINAL.md + LW9_DUEL_N30.md | DUEL (ember judge, parity swap), 2026-09-29..30, ledger 31 rows | estate-real ask mix (adv/plan/schema/grade/code), primes via Nous, slot-A bias canceled by swap | STILL-VALID (question closed by two receipts) |
| 2 | glm-5.3-prime vs gemini-3.8-flash (plain-sight arm) | gemini swept 3-0 (v1mf-r1/r2/r3) on W8 material in plain sight | watch/inbox/last_mile_20260930/V1_MULTIFAMILY_DUEL.md | DUEL, 2026-09-30 | glm side was a REUSED G3 answer to a sibling ask (disclosed ask-mismatch handicap); visible ask = contamination-suspect | SUPERSEDED (by row 3; plain-sight verdicts quarantined) |
| 3 | glm-5.3-prime vs gemini-3.8-flash (hidden arm, THE INVERSION) | FULL FLIP: glm-prime 3-0 on first provably-unseen ask (ab1-coremem-safeguard); criteria 9-12 to glm; won under both slot layouts; $0.0146-0.0174 vs $0.0287-0.0400 per answer | watch/inbox/last_mile_20260930/D6_ASKBANK_DUEL.md | ASKBANK draw v1h-0002 + DUEL (ember), 2026-09-30, corr c76e6d0e | n=3 on ONE hidden draw; Fisher 3-0 vs 0-3 p=0.10 (not significant, D6's own caveat); hidden half derivable from tracked code (A2 G9) | STALE-CONDITIONS (direction banked, magnitude unproven at n=3) |
| 4 | D6 contamination flip (the meta-verdict) | The 3-0/0-3 inversion is consistent with contamination, equally with material effect or handicap; nothing in the bytes can clear visible-ask verdicts; quarantine plain-sight verdicts stands | watch/inbox/hermes_burn/A2_duel_provenance.md sec 0 | byte-audit of duel_harness.py + duels.jsonl, 2026-10-01 (claude-opus-5.5 provenance spec) | legacy rows carry no schema/provenance (G3, G11) | STILL-VALID (policy, not a model claim) |
| 5 | glm-5.3-prime vs deepseek-v4.1-flash | glm 2-0 in scored rounds (criteria 40/40 vs 10/40); round 2 was a ds DNF | watch/inbox/last_mile_20260930/AH10_GLM_VS_DS.md | DUEL (ember), 2026-09-30 | ds thinking-OFF (W8 law), glm reasoning cap 6000; adv-review shape on BASELINE_SPEC sections 4-5 | STILL-VALID (with W8 caveat: glm-vs-ds order also has a cycle blind spot there) |
| 6 | glm-5.3-prime (W8 tier) | 6-0 sweep (2-0 each in adv/schema/plan) vs grok-4.3 and qwen3.7-flash | watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md | DUEL (ember), 2026-09-30, 12 rows | glm side session-authored at $0 (catalog equivalent $0.02-0.04/answer); plain-sight estate asks | STILL-VALID (tier split survived altjudge, row 7) |
| 7 | ember-1 as sole judge | AJ1 altjudge: 10/10 agreement, zero flips, tier split intact under glm-prime rejudge; BUT slot-A favoritism 19/28 decided, one-sided p=0.0436 = real first-position bias | watch/inbox/last_mile_20260930/AJ1_ALT_JUDGE.md + V8_DUEL_FINAL.md | ALTJUDGE replay without regeneration, 2026-09-30, $0.1246 | judge sees A/B only; parity swap mandatory, single-slot judging inflates first-sitter ~10 win-rate points | STILL-VALID (law: ember never the only judge on dollar-routing verdicts; always swap slots) |
| 8 | deepseek-v4.1-flash RAIL | THINKING OFF MANDATORY. Thinking-on burned the ENTIRE completion budget on hidden reasoning, zero content at 4500/8000/16000-token caps, socket hangs, DNFs; thinking-off = 38s, 10704 chars, $0.0021 | watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md (contender config section) | byte-confirmed live diags + w8_run_20260930.log + _ds_diag_schema_nothink.txt, 2026-09-30 | Nous gateway serving ds-v4.1-flash; long-form asks; reconfirmed in AH10 DNF round | STILL-VALID (byte-confirmed mechanism, never refire thinking-on) + POST-DATUM 2026-10-04 amendment banked below the table (parked-decision D3, carrier-enforced) |
| 9 | deepseek-v4.1-flash (value) | W8 6-0 sweep at $0.0130 total (avg $0.0043/ask, $0.0006 on plan); "the value monster" with thinking-off attached; V1: cheapest 4-23x, sharpest single find (Wilson lb95 on raw n), "correct but shallower" coverage | watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md + V1_MULTIFAMILY_DUEL.md | DUEL (ember), 2026-09-30 | thinking-off; long-form degradation caveat = route long-form elsewhere | STILL-VALID |
| 10 | deepseek as judge2 | 3/3 agreement with ember on the D6 glm-vs-gemini rows (conf 78-88, slot-alternated picks 5/4); family-level agreement is the only corroboration that counts | watch/inbox/hermes_burn/DUEL_JUDGE2.md | JUDGE2 (deepseek-chat, thinking off, temp 0.3, blind ANSWER 1/2), 2026-10-01, $0.0102 | n=1 judge opinion per item at temp 0.3; cannot see material bytes, identity, or price | STILL-VALID (judge2 is now standing shoulder 3 of RIB_DEEPSEEK_SHOULDERS) |
| 11 | grok-4.7 | ADVERSARIAL-REVIEW CHAMPION: 9-0 V1 multifamily sweep, avg criterion 4.92/5, deepest spec-internal contradiction hunting (decay-clock kill verified); duel rows 3-0 each vs glm-prime, ds-flash, gemini-flash | watch/inbox/last_mile_20260930/V1_MULTIFAMILY_DUEL.md + logs/duel/duels.jsonl v1mf rows | DUEL (ember), 2026-09-30, 18 rows | adv-review shape, plain-sight material, streaming SSE transport; SLOW (646s/498s per answer) and MOST expensive at $0.231/answer because reasoning tokens bill as output (V9 law) | STILL-VALID (reserve for judgment asks) |
| 12 | grok-4.7 transport | Streaming SSE only; whole-response hangs 900s+ (2x zero-spend clean aborts in the first V1 attempt); strong refusal-honesty (GROK47 luncheon: would not fabricate intel) | watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md (V1 history) + watch/inbox/GROK47_LUNCHEON_INTEL_20260929.md | harness socket logs 2026-09-30 + paid run via api.x.ai XAI_SD_API_KEY 2026-09-29 | Nous gateway duels + direct xAI key intel runs | STILL-VALID |
| 13 | grok-4.3 | 0-6 W8 (0-2 x 3 shapes), 0-6 vs ds-flash, 0-5 vs glm-prime, 0-5 vs qwen3.7-flash; judges: "invents defects", "fabricates statistics, files" | watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md + logs/duel/duels.jsonl | DUEL (ember), 2026-09-30 | reasoning cap 6000/16000, workhorse-tier asks | STILL-VALID (SENSING ONLY; grok-4.3 is a DIFFERENT animal from grok-4.7, never confuse them) |
| 14 | gemini-3.8-flash | FORMAT-FIDELITY CHAMPION: V1 6-3, 4.47 avg; qualification-impossibility find; compact, cheap, fast, "the value pick for this shape" at $0.043/answer; beats ds-flash 3-0; loses to grok-4.7 0-3 | watch/inbox/last_mile_20260930/V1_MULTIFAMILY_DUEL.md + duels.jsonl | DUEL (ember), 2026-09-30 | adv-review shape; $0.0287-0.0400/answer in D6 series | STILL-VALID |
| 15 | qwen3.7-flash | 0-6 W8 at near-free ($0.0028 total); "fabricates under load" (judges flagged invented content); rejects the reasoning param outright (HTTP 400, fires without) | watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md + RIB_MODEL_GATES_20261001.md | DUEL (ember), 2026-09-30 + live param probe | workhorse/judgment asks | STILL-VALID (SENSING ONLY) |
| 16 | glm-5.3-flash (F1 flash-swept-prime) | FLASH SWEPT PRIME 4-0: 3 hidden-ask duels (gates/cml/chainreg) + 1 code duel, all winner=A=flash; $0.0006-0.0009 vs $0.0116-0.0181 per answer (~20x cheaper, sometimes slower: 33-45s vs 13-20s) | logs/duel/f1_run_20260930.log + f1_code_run_20260930.log | DUEL (ember), 2026-09-30, cap $0.30, spent $0.0969+$0.018 | z.ai glm-5.3-flash vs glm-5.3-prime via Nous; hidden askbank draws + one code shape; n=4 | STILL-VALID direction (n=4; the estate's strongest price-quality inversion) |
| 17 | glm-5.3-flash reasoning-channel disease | UNBOUNDED REASONING CHANNEL: with ANY max_tokens cap (2600/4200/9000/16000 all tried) returns empty_content finish=length; fix = REMOVE max_tokens entirely; short prompts fine | memory/continuity/seat_memory_20260927/ox-alpha-was-glm53-flash.md | OpenRouter build-lane receipts, 2026-09-17 | glm-5.3-flash via OpenRouter (stealth/ox-alpha identity revealed in a 404 body) | STILL-VALID (channel law; carrier now known direct z.ai too) |
| 18 | claude-sonnet-5.5 (judge2 upset) | 6-0 over BOTH incumbents (glm-prime and gemini-3.8-flash) on the one shared ask ab1-coremem-safeguard, deepseek blind judge conf 82-88, 3 wins from each slot; decisive in 5/6: only answer naming the false-pass mechanism (original commit row satisfies the Section 1 hash test) | watch/inbox/hermes_burn/DUEL_JUDGE2.md | JUDGE2 (deepseek blind), 2026-10-01 | n=1 ask x 3 rounds; $0.0616/answer vs glm $0.0146-0.0174 (quality upset, NOT a router verdict); blind judge cannot verify citations against the file; content-channel answer | STALE-CONDITIONS (promising, needs a real duel series before routing) |
| 19 | claude-opus-5.5 transport/rails | STREAMING SSE ONLY: whole-response dies at 1800s/3600s ($0 metered, zero bytes, 3 documented deaths); streaming lands 192-362s finish=stop; max_tokens 64000 rail (32k burns 29.5k on reasoning and length-caps; 16k returns all-reasoning empty); ask-shape = sections with word budgets | memory/rib/RIB_MODEL_GATES_20261001.md (OPUS 5.5 row) | Nous transport receipts, 2026-09-30 (W4 + AA1) | anthropic via Nous; $0.42 for 26K-char verdict vs $0.37 for empty; paid asks only on operator GO (AA1 law) | STILL-VALID |
| 20 | claude-opus-5.5 reasoning-channel disease | Deliverable arrives in the REASONING channel with content empty; cheap seat assembles it after (A1/C1 ASSEMBLED files, descent law leg 6); 61 reasoning-channel rows in one burn; every em-dash carrier was a reasoning-channel dump, assemblies are the compliance surface | watch/inbox/hermes_burn/A1_steer_antiforgery_ASSEMBLED.md + DAY1_SKILLS_DOGFOOD.md + LENS1_moonshot.md (raw reasoning dump) | hermes descent burn, 2026-10-01 | premium opus turns via Nous; assembly by deepseek at ~$0.005 is standing rule now | STILL-VALID |
| 21 | Nous primes lane (rails) | LESSIG RAILS MANDATORY: reasoning {max_tokens} + retry-on-empty + reasoning-tail labeled unverified. Without: gopher disease 11/12 zero-content, $1.43 for one answer. With: night burn 6/6 full at $0.41. 402 = credit floor on primes, not dead pool | memory/rib/RIB_MODEL_GATES_20261001.md (NOUS PRIMES row) | mates night_burn N1-N6, 2026-09-30 ($0.2725) | glm/qwen primes via inference-api.nousresearch.com | STILL-VALID |
| 22 | tethered-link width (workflow children) | 50-wide workflow dig = 1302/429 STORM (1,838 log lines, fake "subscription" crashes); dwf children 9/20-26: 896 network failures, 817 of them 1302-shaped, 11 terminal actors, zero tally visibility; workflow children get maxAttempts 0 = zero absorption, NO measured clean rung | corpus/steal/TETHERED_LINK_STEAL_20260925.md + watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md | harness adapter audit + log census, 2026-09-25/26 | account:zai-individual-coding-plan (GLM-5.3-Flash), phone-tethered link, carrier NAT kills idle streams 71-80s | STILL-VALID (cap lives on dispatch shape, not width alone) |
| 23 | tethered-link width (Task agents) | Task agents ride main-session retry (maxAttempts 11 + backoff): clean at widths 3, 6, 10, 12; width 10 banking 109.4M tok/h with zero surfaced 1302s; 10x3 waves in 37 min clean; ~15 width = 2 rate-limit deaths refired; 12 after a burst takes 1302s until window decays (rolling throughput is the binding constraint, not width); 15-16 rung untested | watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md (B2-476 proven-width table) + B2_25_envelope_remeasure_20260926.md | envelope re-measure, 2026-09-26 | same account, Task-agent transport; after a burst even 12 degrades until decay | STILL-VALID (supersedes the flat 3-cap; unanchored 50-wide-clean claims flagged, do not cite) |
| 24 | stealth/ox-alpha identity | ox-alpha WAS z-ai glm-5.3-flash all along (404 body named it); union-alpha window then also ended, successor unbiased/pareto; free stealth lanes are SENSING surface only, outputs banked as findings never trusted work | memory/continuity/seat_memory_20260927/ox-alpha-was-glm53-flash.md | OpenRouter 404 bodies, 2026-09-17 | stealth windows open/close; both OpenRouter keys one rotating pool | SUPERSEDED (window closed; the identity-law and sensing-law live on) |
| 25 | kimi / moonshot | NEAR-ZERO verdicts. Held: (a) kimi-k3 tesuji dossier (2.8T MoE, cluster-only, MXFP4, $0.30/$3 in $15 out per 1M, always-thinking default, must preserve reasoning_content or it breaks); (b) moonshotai/kimi-k2.6 on the operator-proven id list 2026-09-17; (c) kimi-k2 flew two hermes_out lanes (flygomoku F11 gomoku rules ok 108s; matthew480 maps) with NO duel verdicts; (d) cache-portability project: Moonshot prompt-cache early-stage | memory/improve/evals/models/kimi-k3-2026-07-27.md + memory/continuity/seat_memory_20260927/operator-usage-as-probe.md + memory/runs/flygomoku_20260912/hermes_out/F11_gomoku_rules_moonshotai__kimi-k2.md | tesuji desk research 2026-07-27; usage-probe 2026-09-17; hermes lanes 2026-09-12/13 | no duel rows in logs/duel/duels.jsonl mention kimi; zero blind-judged comparisons | STALE-CONDITIONS (dossier only; the family is UNMEASURED by the estate's own instruments) |
| 26 | local Qwen3-8B (Zen2 box) | bf16 emulation pathology 159-183s/forward; fp32 is 6x faster and higher precision; RAM gate: never launch needing > free-2GB; gemma:2b was Q4_0 (quant correction ordered 2026-10-01) | memory/rib/RIB_MODEL_GATES_20261001.md (LOCAL row) + RIB_GPU_LADDER_20261001.md | local llama-path timings, distilled 2026-09-30 | AMD RX 5600 XT (RDNA1, gfx1010): no MFMA, no FP8; DeepGEMM pays only on NVIDIA tensor cores | STILL-VALID (gate the memory-radar, ignore DeepGEMM on this box) |
| 27 | flash routing table (the distillation) | Per-animal harness profiles: opus-5.5 streaming+64k rail; glm-5.3-prime workhorse+judgment (pair a second family on judgment, glm-judging-glm confound G7); ds-flash thinking-off bulk workhorse, long-form elsewhere; grok-4.7 judgment reserve; grok-4.3 + qwen-flash sensing only; gemini-3.8-flash balanced-value middle; ember never sole judge; model whose fingerprint changed = NEW animal, cold start (Amendment 10) | memory/rib/RIB_MODEL_GATES_20261001.md + configs/router_policy.yaml | F12 first bulk feed distillation 2026-09-30T23:47:51Z over memory/behavioral/animals/*.jsonl (+37 obs / 13 animals) | routing decision = receipts-first (duel table + gps momentum badges) | STILL-VALID (this IS the current router law) |
| 28 | ling-3.0-flash-sante, meta-muse-glimmer-30b, stealth-space-bunny-alpha | Envelope/rail observations only (3 obs each or fewer: envelope x2, rail, failure x2, verdict x1); no duel series, no tier placement | memory/behavioral/animals/*.jsonl via RIB_MODEL_GATES evidence section | F12 distillation, 2026-09-30 | observed opportunistically during burn windows | STALE-CONDITIONS (animals exist in the ledger but are UNMEASURED for capability) |

### Row 8 POST-DATUM amendment (2026-10-04, parked-decision D3; landed verbatim from watch/inbox/ractor_engine/2026-10-04-parked-decisions/SYNTHESIS.md, append-never-rewrite)

POST-DATUM 2026-10-04 (parked-decision D3; d4_thinking_probe.md;
hermes_burn usage.jsonl:1151-1152): row 8's mechanism is confirmed
cross-family (deepseek-v4-flash 3-arm probe: omitted key = 18 reasoning
tokens on a one-word ask; glm-5.3-prime: 15998 of 16000 completion tokens
reasoning, content_chars 1). Scoped ruling: THINKING OFF is the SENT
default for depth=mechanical/short-output asks, enforced BY THE CARRIER:
route_chat sends thinking:{type:disabled} unconditionally on mechanical
(mag/route_chat.py:204, lane-config condition removed); omission is NOT
the off state (d4 3-arm probe 2026-10-04, three independent runs). Lane
config (providers.yaml disable_thinking) is demoted from enforcement to
design-depth capability attestation. "Never refire thinking-on" holds as:
thinking-on rides ONLY depth=design on attested lanes at max_tokens >=
32000, substance-gated (mag/route_chat.py:238-249). The off state is verified
from response-side reasoning_tokens banked per row, not assumed from the
request (openrouter/auto measured ignoring the key, providers.yaml
:219-223). Falsifier: a judged equal-budget mechanical A/B where
thinking-ON wins material_chars per dollar with zero hollow rows flips the
default back; a measured 400 on the disabled key from a funded lane forces
capability-scoped off.

Land-note (law-amendments lane, 2026-10-04): the route_chat cites inside
the amendment text are SYNTHESIS-moment lines, kept verbatim; the wire
sitting landed the carrier fix in the same window and the module moved
under the edit. Line truth at landing (sed-verified 2026-10-04, module
under active wire-sitting edit): depth enum ValueError at
mag/route_chat.py:193-196, wire_thinking (unconditional mechanical
disabled, design gated on capability attestation and DESIGN_MIN_TOKENS
32000) at :134ff wired at :266, closed-loop bank (depth + thinking_sent +
reasoning_tokens) at :308-310.

## B. The reasoning-channel disease, per SKU (the descent learning)

The disease: premium output lands split across channels; naive harnesses read
empty content and pay for re-burns. Per animal (RIB_MODEL_GATES + receipts):

- opus-5.5: work in reasoning channel, content empty. Standing fix: cheap-seat
  ASSEMBLY first (deepseek ~$0.005), re-burn only if assembly fails.
- glm-5.3-flash: unbounded reasoning channel; any max_tokens cap yields
  empty_content finish=length. Standing fix: remove the cap entirely.
- deepseek-v4.1-flash: thinking-on burns the whole budget on hidden reasoning
  and DNFs. Standing fix: thinking off, always, on this gateway.
- qwen3.7-flash: rejects the reasoning param (HTTP 400); fires without it.
- glm-5.3-prime / grok-4.3: tolerate a reasoning max_tokens rail (6000); the
  LESSIG rails (retry-on-empty + unverified reasoning-tail label) are the
  general prime-lane defense.

## C. Costs already metered (per answer, for price-aware routing)

- ds-v4.1-flash: $0.0006-0.0103 (thinking-off)
- glm-5.3-flash: $0.0003-0.0009
- qwen3.7-flash: ~$0.001
- gemini-3.8-flash: $0.029-0.043
- glm-5.3-prime: $0.015-0.036 (catalog equivalent)
- claude-sonnet-5.5: $0.0616
- grok-4.7: $0.231 (reasoning bills as output)
- opus-5.5: $0.37 empty / $0.42 for 26K chars
- ember-1 judge: ~$0.012-0.040 per duel
Source: V1/V8/W8/D6/F1/AH10 receipts + COST_TRUTH_20260930.md (lifetime
$135.88 over 25,406 calls at 2026-09-30T18:53Z; all Nous spend $9.05 lifetime,
all since 2026-09-29).

## D. What this means for the new battery (the 3 + the 3)

Do NOT re-measure (already settled):
1. glm-5.3-prime vs qwen3.8-max-prime head-to-head (row 1): closed at n=30 with
   CIs, two receipts; route either as workhorse and spend the battery elsewhere.
2. deepseek-v4.1-flash thinking-on vs thinking-off (row 8) and the glm-5.3-flash
   max_tokens cap (row 17): both are byte-confirmed failure mechanisms, not
   capability questions; refiring them only re-buys DNFs.
3. grok-4.3 and qwen3.7-flash in workhorse/judgment lanes (rows 13, 15): 0-6
   and 0-6 with fabrication flags, survived a 10/10 altjudge replay; they are
   sensing-tier by settled evidence.

Biggest holes (families with ZERO estate verdicts):
1. kimi / moonshot (row 25): dossier and two unjudged lanes only; never entered
   a duel. The operator-proven kimi-k2.6 id is the cheapest entry point.
2. fable: zero mentions anywhere except as a benchmark fallback footnote inside
   the Kimi-K3 tesuji. Completely unmeasured, no lane, no id on file.
3. haiku (and the claude-sonnet family beyond one ask): haiku has zero rows;
   sonnet-5.5 holds a single 6-0 judge2 upset (row 18) that was never converted
   into a real duel series - and ling-3.0-flash-sante / meta-muse-glimmer-30b
   sit in the behavioral ledger with envelope observations but no capability
   verdicts (row 28).

Lane 4 seat, 2026-10-01. Evidence files all named above; no new measurements
were fired for this sweep (desk mining only, $0).
