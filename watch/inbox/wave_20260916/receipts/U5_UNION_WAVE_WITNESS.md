# U5 — UNION WAVE WITNESS (fresh outside reader reads the WAVE via stealth/union-alpha)

- **Lane:** U5 (wave-lane) · **Date:** 2026-09-16 · **Budget:** $0 (free stealth model; no git, no paid calls)
- **Wave-lane law:** receipt first (this file, written before any call), append as you go, no git.
- **Operator order:** fresh witness reads the WAVE itself. Assemble ≤1500-token digest from receipt FILENAMES + PHYSICAL_COMPUTING_PACK_20260916.md §6 + 3-4 load-bearing receipts; feed to `stealth/union-alpha` on OpenRouter as outside reviewer; rank next 5 actions, biggest unmanaged risk, self-congratulation-vs-evidence audit, blunt. Record verbatim. Fleet responds.
- **Key handling:** `OPENROUTER_API_KEY` via `mag.flight_recorder.load_env` — never printed, never written to any row.
- **Model:** `stealth/union-alpha` (free window, ends ~2026-09-23). 402/403 → record and stop. 429 → one retry, then keep the failure row.
- **Inputs read (filenames):** A1_BLIND_CHALLENGE_SET, A2_EPISTEMOLOGY_ENGINE, A3_THE_TOY_CORE_VERB, A4_ASTRA_SMOKE_12, B6-B14 (links backfill, canonical-check writers, arXiv six leads, Zenodo DOIs gen2, MLP KV cache prior-art, sliding-window RIB, Rashomon dedupe, Codetaur KAN, third-smile protocol), D20_BONES_ADAPTER, D21_ESTATE_LOD_SPECTATOR, D22_PROVIDER_PROBE (+pass2), D23_SALON50_NIGHT_RESULTS, D24_MEMORY_DOCTRINE_BUNDLE, E_UNION_ALPHA_EVAL, S5_JOURNAL_VENUES. Pack §6 + §6.2-§6.8 read in full.
- **Receipts skimmed (load-bearing picks):** E_UNION_ALPHA_EVAL.md (the seat itself), D23_SALON50_NIGHT_RESULTS.md (the night's verdicts), D22_PROVIDER_PROBE_20260916.md (which lanes are alive), A2_EPISTEMOLOGY_ENGINE.md (what the epistemology engine needs). Digest built from these + §6.

---

## Digest (assembled before the call)

(~1,100 tokens; assembled from receipt filenames above, pack §6–§6.8, and skims of E/D23/D22/A2)

---

DIGEST FOR OUTSIDE REVIEWER — "local_sovereign_agent" fleet, night of 2026-09-16

WHAT THIS PROJECT IS: a local-first "Mag" agent harness (Windows, Ollama janitors + scarce remote specialists) that runs wave-lanes of parallel AI seats to do research, build falsification protocols, and file append-only receipts in a shared inbox. Epistemic law: receipts before work, bytes over reports, $0 free-tier budget, no git tonight, human gates on effects.

BUILT TONIGHT (all receipts in wave_20260916/receipts/): 23 receipt files across A/B/D/E/S lanes. Physical-computing pack round-2 folds: a red-team of our own claims (3 attacks accepted, $0), a 25-call free-lane salon, canon mining (5 finds: the water computer already exists in our MUD as "The Clear Pipes"), discovery that a vendor's replication seat is unclaimed (Extropic 140x efficiency claim: simulator + open weights public, nobody has measured). A 50-seed salon fanout (D23: 49/50 answered, $0) over three pre-registered verdict questions. A provider probe (D22: 8 of 12 free lanes alive, 4 distinct failure classes, two paid walls hit and logged do-not-retry). Epistemology-engine stone 1 designed (A2: "Row Law" — every claim needs a machine-checkable warrant; found our own live evidence chain FAILS verification at row 122, a hand-written bypass). A blind external challenge set (A1). A 12-model identity smoke (A4). Research verified: sliding-window RIB (B11), arXiv leads (B8), Zenodo DOIs (B9 gen2), journal venue ladder (S5). Built-but-unrelated-to-theory: /bones Discord adapter (D20) and estate LOD spectator (D21), both Sep-20 demo critical path, tests green.

REFUTED TONIGHT: (1) Our own "fleet-as-thermodynamic-sampler" analogy — inter-lane decorrelation does NOT predict answer quality (rho +0.33 wrong-signed, replicated; kill threshold rho<0.3 now binding). Yet in the 50-seed salon, 11 of 17 witnesses still tried to SAVE the analogy with 11 different rescue mechanisms; 6 said kill. We filed the refutation anyway. (2) Verifying our sims against themselves is circular — a physical artifact must confirm a sim prediction first (new falsifier). (3) A gen-1 run design that confounded temperature with question was caught and replaced. (4) Our own append-only chain contains a broken/forged row (122) that the schema cannot even express as dead — the exact problem our new engine is designed to fix.

PENDING: Extropic replication stone ($0, this week). Row-Law implementation + two-eyes review. Row 122 void procedure (append-only cannot delete). The union-alpha free-seat eval battery (parallel seat, not yet fired). Sep-20 demo burn-down (bones + estate). Step-3 journal submission needs an APC decision.

OPERATOR GATES: $0 hard budget (free tiers only; a paid wall = abort that lane, never retry); no git tonight; receipt-first append-as-you-go; "model text proposes, only the switchboard/effect broker authorizes effects"; consensus raises confidence but never grants permission; no key ships without an execution receipt by another hand; human promote-gate on candidates. Known self-admitted weaknesses: 34 of 1,341 tests failing; evidence rows damaged by our own driver bug mid-run (an abort gate overwrote real error rows — since fixed); one lane answers with visible chain-of-thought and contradicts itself across temperature.

---

## Witness prompt sent

(verbatim wrapper; digest spliced at {digest}):

> {digest}
>
> ---
>
> You are an outside reviewer. Given this state, rank the next 5 highest-value actions for this project, name the single biggest unmanaged risk, and identify anything that looks like self-congratulation instead of evidence. Be blunt.

Call params: `stealth/union-alpha`, T=0.4, seed=2026091615, max_tokens=2500, NO system prompt (bare model), one call in flight. Runner: `../u5_union_witness_20260916.py` (mirrors E seat's SSRF-safe pattern). Tape: `memory/runs/u5_union_witness_20260916/raw.jsonl`.

## Call log (5 rows on tape, all $0.00, free model)

1. **CALL 1** (seed 2026091615, T0.4) — digest verified in-prompt (3,311 chars, est ~827 tokens; model's answer cites row 122, 11/17, 34/1341 — it had the real digest). Long free-form review; **TRUNCATED at cap** (`completion_tokens` 5000, finish=length, 10,739 chars, cuts mid-sentence in self-congratulation item on "49/50"). Full verbatim on tape.
2. **CALL 2 continuation** (seed 2026091616) — API is stateless; model **refused to fabricate context** ("a verdict of 'real' or 'theater' would itself be epistemic theater"). Honest refusal, recorded as evidence of the witness's own epistemics. Deliverables still missing.
3. **CALL 3 contracted** (seed 2026091617) — **FLEET DRIVER BUG:** heredoc digest extraction (`split("---")[1]`) grabbed the digest *preamble*, not the body — model correctly answered "the message contains review instructions, not project evidence" and refused to invent. Same bug class D23 gen-1 caught; probe cheap, that is why we probe.
4. **CALL 4 v2** (seed 2026091618, attempt 1) — KeyError `choices`, response body not captured (transient provider error class; row preserved as-is).
5. **CALL 5 v2 retry** (seed 2026091618, attempt 2, 20s cooldown, raw-body capture added) — **SUCCESS**, finish=stop, 1,724 total tokens. The recorded answer below.

## Verbatim answer (CALL 5 — the seat's complete review)

## 1. RANKED ACTIONS
1. **Quarantine the damaged evidence chain:** preserve raw files, record hashes, identify everything downstream of row 122 and the overwrite bug, and append explicit invalidation/supersession records; compromised provenance cannot support promotion.
2. **Implement Row Law with independent adversarial review:** require resolvable evidence, explicit validity states, and fail-closed promotion checks; machine-checkable structure must not turn an unsupported claim into a certified one.
3. **Triage all 34 failing tests before adding seats:** prioritize authorization, budget enforcement, receipt integrity, and demo-critical paths; green component tests do not establish that the harness is safe to operate.
4. **Close the sampler hypothesis formally:** publish the exact hypothesis, metric definitions, uncertainty, threshold history, and termination decision; rescue mechanisms become separately registered hypotheses, not retroactive exceptions.
5. **Freeze scope through Sep-20 and execute one bounded replication:** finish the demo-critical path, defer more salons and identity batteries, and attempt the Extropic study only after fixing its baseline, measurement boundary, artifact requirements, and $0 stop rule; prioritize discriminating evidence over activity.

2. BIGGEST UNMANAGED RISK

**Your evidence authority is not independent of the machinery producing the evidence.** The harness can generate claims, damage their records, and potentially present the surviving chain as trustworthy. Append-only storage does not establish truth, completeness, or authorization; hashes added now cannot reconstruct overwritten history. A second AI seat is not necessarily an independent reviewer if it shares the same driver, summaries, or defective evidence source. Until invalidity propagates to downstream claims and promotions fail closed, "receipts before work" risks becoming permission laundering: well-formatted records standing in for verified observations. Require an independently implemented verifier, preserved raw execution artifacts, and human review of exceptions—not merely another approving receipt.

3. SELF-CONGRATULATION AUDIT
- **"23 receipts," "25-call," "50-seed," and "49/50 answered"** measure production and availability, not correctness, independence, or research value.
- **Repeated "$0"** establishes compliance with a spending constraint, not efficiency. Operator time, local compute, and opportunity cost still count.
- **"11 of 17 witnesses" and "11 rescue mechanisms"** are not independent scientific testimony. Shared training and prompting can multiply the same bias.
- **"Nobody has measured"** outruns the reported evidence. Say that your documented search found no qualifying independent measurement.
- **"The water computer already exists in our MUD"** may be a useful creative connection; it supplies no physical validation.
- **"Tests green" for two components** needs scope and dates beside the 34 suite failures. Otherwise it invites an unjustified whole-system inference.
- **"Broken/forged row"** conflates corruption with fabrication. Establish mechanism and attribution before calling it forged.
- **The sampler refutation's numerical shorthand is insufficient:** "wrong-signed" and the stated kill threshold need their variable definitions to be interpretable. Also, "now binding" leaves unclear whether the threshold preceded the result.
- **Calling the chain failure "the exact problem our new engine is designed to fix"** turns an incident into product validation prematurely. Successful detection, containment, and independently tested prevention would be evidence.
- **"We filed the refutation anyway"** is genuinely creditable—but only if it changes scheduling, claims, and promotion decisions. Filing without consequences is ceremony.

4. VERDICT
**Real but not yet dependable: you expose disconfirming evidence; whether that evidence actually blocks work is the test separating discipline from theater.**

*(Note: CALL 1's truncated long-form contained 10 additional observations in the same direction — incl. "no-git during the session where provenance broke is self-sabotage," "APC vs $0 budget collide," "49/50 is coverage not validity" — full text 10,739 chars on tape `memory/runs/u5_union_witness_20260916/raw.jsonl` row 1. Recorded, superseded as the deliverable by CALL 5.)*

## Fleet response

**ACCEPT, with three catches we genuinely missed.** (1) The threshold bookkeeping: our own texts disagree — pack §6.1 pre-registered "ρ < 0.3 kills," the replicate read +0.327 (p=0.052, n=36), yet D23 and the mission text call the analogy "refuted/wrong-signed." Whether +0.327 is a marginal SURVIVAL of the pre-registered line or a kill depends on variable definitions we never filed in one place. The witness is right that "now binding" without the threshold's history is exactly the retrospective-fitting move we prosecute in others; a formal closure receipt (hypothesis, metric, threshold provenance, termination decision) is owed before the word "refuted" travels anywhere. (2) "Forged" vs "corrupt" on row 122: the mechanism (crash mid-write, missing hash field) points to corruption by a bypassed writer, not fabrication — we conflated them, and attribution is unestablished. (3) "Nobody has measured" is an overclaim; the honest form is "our documented search found no qualifying measurement." Also accepted operationally: its biggest-risk paragraph indicts THIS seat too (a reviewer reading our digest of ourselves shares our driver — so this witness must be fed receipt bytes/hashes, not just our prose, and paired with A1's blind challenge set to count as independent). REJECTED: none of substance; its call-3 refusal was our extraction bug, not its failure, and its call-2 refusal to continue blind was correct behavior. The "filing without consequences is ceremony" test stands as a standing gate: the refutation must visibly change scheduling and promotion checks by the next wave or it was theater.

## Seat verdict

**KEEP** — this seat produced, in one $0 call-series, a sharper external audit than our internal red-team (threshold-provenance catch, forged/corrupt split, verifier-independence requirement), refused two separate temptations to fabricate, and its failure modes (truncation, statelessness) are contract-fixable: standing outside-reader for the epistemology engine, on the amended protocol — feed receipt bytes + hashes, contracted output format, one call, no continuation dependence.
