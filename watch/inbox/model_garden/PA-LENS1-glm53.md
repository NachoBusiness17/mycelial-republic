# PA-LENS1-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# LENS VERDICT: MOONSHOT-DRIFT

**(1) The finish line is comfortable, not right.**
All three conditions are self-graded by the loop that produced them. "THE CREDITS BECOME LAW" (00__MOONSHOT_BRIEF.md, section 1: "every dollar leaves a rib, a test, a skill, or a spec that a future window consumes") is satisfiable by artifacts the loop itself defines and consumes. The sherpa named this exactly: "None implies the artifacts encode true claims about the target system... all three conditions are satisfiable by a self-consistent fiction" (01__lens1_sherpa.jsonl, id lens1-blind-spots). Day-1 precedent: the board read "LANDED 14/14" while all fourteen outputs were refusals (00, section 4) - the loop's own accounting already produced a well-formed lie once. The right finish line adds a fourth condition: an external consumer lands a workday task using only the loop's public outputs, within 1.5x loop time (sherpa falsifier (i), id lens1-falsifier-gaps). Without it, conditions 1-3 measure process hygiene, not sovereignty.

**(2) Three prescriptions, each with an owner and a one-sitting first step.**

- **P1 - Run the kill test before any more premium adjudication spend.** Owner: the driver lane. First step (one sitting): stage the sherpa's 20-item test verbatim (01, id lens1-fall-modes... specifically id lens1-kill-test): 20 held-out estate rules, free self-critique vs premium adjudication with evidence bytes, hand-written gold key, ~$0.20 total. The load-bearing assumption of the whole machine is "premium converts cheap bytes into law" (01, lens1-kill-test: "the loop's only premium-dependent node"). Day-1 evidence cuts both ways: premium "lost every time it asserted facts about bytes... it never saw" and the DG1 premium adjudication "stayed open at window close" (00, sections 4 and S4) - so the premium node has produced zero confirmed value on the ledger so far.
- **P2 - Freeze-ask test on the shoulders.** Owner: ASK FORGE lane (shoulder 1) plus ADVERSARY PASS (shoulder 2). First step (one sitting): pick the 6 duel-refire asks already staged with rendered payloads (02, REDEMPTION-STAGING: "20, not 6" staged, "24/24 PASS" preflight), snapshot each ask text to a frozen file, run shoulder 1+2 on a copy, then fire both versions and compare landed-clean rate on frozen vs shoulder-rewritten asks. This is sherpa launder-check (2): "if cleanliness gain vanishes on frozen asks, shoulders are theater" (01, lens1-falsifier-gaps).
- **P3 - Wire the redemption denominator to the drop path, then prove it with a forced drop.** Owner: free build lane. First step (one sitting): implement the T6 ticket instrument (02, item 6, ~$5) so that a deliberately poisoned ask (reuse the `*.md.poisoned-evidenceless` trick from 02) shows up as issued>0, run>0, dropped>0 in the same wave. Sherpa's earliest-signal test: "denominator instrument logs a wave with zero drops, which is statistically implausible and indicates the counter is not wired to the drop path" (01, lens1-fail-modes). Last-mile condition 1 is currently unmeasurable ("counted and above zero", 00 section 1, with $5 allocated but nothing built).

**(3) What to kill.**

- **Kill the descent protocol's artifact leg as a spending assumption, not the protocol.** Its own falsifier concedes it: "a descent week where the ledger grew but no rib/pack/receipt carries a frontier contribution forward = spend theater; fix the artifact leg first" (00, section 5). Until P1's kill test passes, treat "frontier contribution" as unproven and bank only free-lane artifacts.
- **Kill shoulder 6, BULK ASK MINING, for the moonshot's duration.** It is the widest path to ask-rewriting laundering (sherpa gap 2) and to the loose-law inflation failure ("laws being defined loosely enough to be trivially satisfiable", 01, lens1-falsifier-gaps gap 4). Ask generation is the cheapest human step; paying any model to multiply asks before the premium node is validated inverts the cut order.
- **Kill the $50 reserve as "unallocated."** Sherpa flagged "whether the $50 reserve is actually ring-fenced" as unknown (01, lens1-fail-modes). At the whole-span rate ($4.19/h, 1.13 days runway, 00 section 3) an unallocated reserve is a target, not a buffer. Ring-fence it in bytes: reserve spends only on the four never-cut items (T1, duel redemption, denominator, and now P1).
- Do **not** kill shoulders 1-5 or 3 as families yet; P2 is their trial, and the declared shoulders falsifier (00, section 5) is the correct executioner.

**(4) Verdict.** MOONSHOT-DRIFT. The aim is right-shaped but the load-bearing node (premium adjudication) is unvalidated, the finish line has no external consumer, and the reserve is unfenced.

**Flip condition:** MOONSHOT-SOUND when P1 lands with delta >= 0.25 absolute and condition-B pass rate >= 0.70 on the 20 held-out items, AND the denominator instrument shows one wave with issued, run, and dropped all above zero. If P1 fails (delta < 0.10 or B < 0.50), stop premium adjudication spend entirely and redeploy per the sherpa's reallocation (01, lens1-kill-test).

**DELIVERABLE (apply as-is): create `watch/inbox/model_garden/premium_autopsy/KILLTEST_SPEC.md`:**

```
KILLTEST v1 - adjudication value, 20 items, ~$0.20
1. Owner: driver lane. Budget cap: $0.30 hard.
2. Items: 20 held-out estate rules/tests, drawn from files NOT in any
   prior ask's EVIDENCE block. Freeze the draw list with sha256 in
   this file before any call fires.
3. Gold key: operator hand-writes 20 pass/fail keys, ~30 min, before
   firing. Keys committed first, calls second.
4. Condition A: free model answers + self-critiques + revises.
5. Condition B: same answers + evidence bytes -> one premium
   adjudication call, max_tokens 12000, evidence preflight exit 2 on
   empty blocks (carrier law).
6. Scoring: pass = artifact matches gold key. Report
   pass_rate(B) - pass_rate(A), and absolute pass_rate(B).
7. Pass: delta >= 0.25 AND B >= 0.70 -> premium node validated,
   moonshot continues on-plan.
8. Fail: delta < 0.10 OR B < 0.50 -> zero further premium
   adjudication spend this moonshot; redeploy per 01/lens1-kill-test.
9. Grey zone (0.10 <= delta < 0.25): rerun at n=100 (~$1.00) before
   any other premium ask fires.
10. Receipt: bank cost + both score cards to
   memory/runs/hermes_burn/usage.jsonl per descent leg 8.
```

**Falsifier of this deliverable:** the kill test runs as specified, returns delta >= 0.25 and B >= 0.70, and the moonshot still ends its week with no rib, test, skill, or spec consumed by a window other than the one that wrote it - in that case this lens's diagnosis was wrong and the drift was elsewhere.
