# SALON SYNTHESIS — GLM-5.3-Flash LINEAGE DROP (2026-09-01 07:15Z)
> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: GLM-5.3-flash is a new base per vendor release with any distillation relationship undisclosed; custody and serving economics unchanged — UNPROVEN (vendor self-report, 3x/4.4x figures vendor-reported unaudited per lanes) · falsifier: probe battery (needle-sweep/behavioral signatures) showing Flash behaves as a distilled 5.3 checkpoint, or vendor disclosure of distillation lineage
input: operator drop 06:47Z (operator-authored) · lanes: 5/5 returned, DeepSeek, board-only, all ≤40 lines
lane files: /board/salon_glm53/lane_{a_harness,b_custody,c_probes,d_economist,e_redteam}.md

## VERDICT (one line)
The drop converts Flash from "one artifact" to "family recipe + Flash-disclosure gap": custody unaffected (grab continues), serving economics unchanged on evidence held, and the agentic-RL section independently validates our switchboard/steer_bus trajectory design — with three named invariants to adopt.

## CONSENSUS (≥3 lanes, quoted basis)
1. **"New base, not a public distilled GLM-5"** — B(P-class), A, E all land here. B corrects WEIGHTS_PLAN's 22:46Z "(distilled)" shorthand.
2. **3× attention / 4.4× KV are vendor-reported, unaudited** — C, D, E. D's economic ruling: provider-side serving lever, NOT a per-token-rate lever; our measured card ($0.075/$0.25) and route map do not re-rank on it.
3. **Probes before operator-facing facts** — C, D, E name probes for every must-NOT-reach-operator claim.
4. **Trajectory/receipt architecture validated** — A maps Z.AI's agentic-RL ops onto our switchboard target; the drop itself says both systems treat agents as workers producing auditable trajectories (§118).

## DIVERGENCES → RECONCILED
1. **Together "beats Sol + Fable 5" claim.** E: "zero fetched bytes, highest red flag." Counter: receipt `together_glm53_agentic` (08-31 22:38Z) pulled the post via x_search and classified provider-self-report PASS-with-flags. Ruling per convergence-dissection law: bytes exist via search-organ pull, but no raw post fetch and no linked benchmark table — classification stands at **provider-self-report, unverified**, E's probe demand adopted (web_fetch post + result tables + HF/leaderboard corroboration). E overcalled "zero bytes"; the stricter probe survives either way.
2. **"Not distilled" vs E's contradiction flag.** Release says new base (vendor assertion, P-class as *disclosure*); GLM-5 report has a cross-stage distillation stage and Flash's checkpoint relation is undisclosed (E). Precise wording for the weights plan: **"new base per vendor release; any distillation relationship undisclosed."** Both lanes right at different granularity.
3. **Lane C path miss.** `GLM53_FLASH_DEEPDIVE_20260831.md` lives at `/root/.openclaw/workspace/staging/` (main), not worker staging. C flagged it and substituted `glm_parts.txt` — discipline held. Lesson filed in ladder below.

## LOAD-BEARING FOR OPERATOR
- **Probe battery (C, ranked by info-per-credit, cap 400cr = 5% of weekly Flash slice):** 1) sparse/linear boundary needle-sweep at 32K (~0.7cr/call — cheapest discriminator for the hybrid-attention claim); 2) behavioral signatures (near-$0, feeds passport failure-signatures); 3) tool-use 2-iteration recovery vs 4.5/5 receipts; 4) long ladder 32K→1M (121.5cr, validation only, never discovery). Receipt schema specified. Needs your GO — it spends Lite credits.
- **Steer_bus invariants (A):** I1 trajectory-as-audit-unit · I2 version-pinned receipts + env-collapse→DROPPED (closes steering-synthesis gap #6) · I3 KV-locality routing + one unified row. Verdict: weak-yes PILOT demo (steer→claim→receipt + I2 abort, 30min/$0.001) as next build. These double as war-games referee mechanics (tamper-proof move logs, abort receipts).
- **Passport schema delta (B):** add `lineage_evidence[]` (P/L/U classes, nullable source) + `unknowns[]` to MODEL_ATLAS_PASSPORTS; backfill the zai/glm-5.3-flash row. Phase 5 bankable set = L-status PUBLIC only (TACO, Codeforces problems, DataComp-LM, open math/science with license check); the 10M issue-PR set and 10k agentic envs are vendor-internal — never bankable, never claimable as Flash data.
- **Ox Alpha precedent (E):** licenses our own anonymous-eval harness (de-identified model, synthetic traffic, board-side self-identification). Does not license claiming endorsement.
- **GLM-4.5 23T-vs-15T discrepancy:** preserved, not reconciled (E). No single-number token fact for 4.5 reaches the operator.

## ACTION QUEUE (awaiting operator word)
1. Probe battery GO/NO-GO (400cr Lite spend, off-peak Flash)
2. steer_bus: draft /patches JSON with I1–I3 baked in (the open question from 04:48Z, now with named invariants)
3. Passport backfill + weights-plan wording fix ($0, agent-fireable on your nod)
4. War-games v0: chess smoke test vs scenario game (open from 07:03Z)

## SALON LADDER (better-by-default, measured this run)
- 5/5 lanes returned, 18/35/37/38/36 lines (all ≤40), 0 messaging violations, 0 two-strike bails, 0 novel assertions caught, ~2min runtime each, DeepSeek $-trivial.
- Hit-rate 5/5 load-bearing output. Improvements next salon: (1) briefs carry exact artifact paths (C's miss); (2) any "no bytes held" ruling must grep the receipt trail first (E's overcall); (3) keep lane-cap + board-only — worked clean.
