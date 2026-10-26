# OPERATOR MODEL V2 BASE — SELF-MODEL, SELECTION-BIAS-CORRECTED (2026-09-30)

**Label: SELF-MODEL selection-bias-corrected.** This doc answers N1's kill on the v2 operator
model (watch/inbox/last_mile_20260930/NIGHT_BURN_RECEIPT.md): *"the instrument is pointed at
its own commissioner... under 0.1% quote sampling with no base-rate contrast."* Every claim
below carries (count, denominator, method) or it is deleted / marked FRAME-NOT-FINDING.
Quote-ledger predecessors (OCEAN.md, OPERATOR_CARD_V2.md, INTERRUPTS.md, DECISIONS.md — all in
this directory) remain as evidence ledgers, but each is now covered by this caveat: **their
quotes were selected by the estate through operator-approved gates; they are not base rates.**

Reproducer: `watch/inbox/last_mile_20260930/imp10_operator_counts.py` (zero API spend, local
bytes only). Outputs byte-backing every number here:
`imp10_operator_pool.jsonl` (every counted message), `imp10_operator_counts.json`,
`imp10_audit_sample.json`.

## 1. Instruments and denominators (census-denominator law: name instrument, moment, delta)

| Instrument | Files | Counted | Messages kept | Dropped (rule) |
|---|---|---|---|---|
| grok pool `corpus/oral_history/seat_pools/grok_sessions/*/*/chat_history.jsonl` | 852 | 845 sessions yielded messages | 889 | 2,003 tagged boilerplate (`<user_info>`/`<system-reminder>`/…), 2 continuation blobs, 9 unparseable lines |
| codex pool `corpus/oral_history/seat_pools/codex_sessions/**/rollout-*.jsonl` | 193 | 170 files carried user messages | 1,015 | 358 tagged envelopes (incl. 51 auto-injected `<in-app-browser-context>`/`<turn_aborted>`/… found by audit), 64 md-context blobs, 15 tiny |
| **Total operator-side messages M** | | | **1,904** | |

- Extraction: grok = `<user_query>` inner text + bare turns (len>5); codex =
  `response_item/payload.message/role=user` bare text. Full rules in the script header.
- **Duplicates:** 673 rows are re-sends of earlier texts; one fleet template ("Use
  x_keyword_search ONCE…") appears 591 times. **Unique texts: 1,231.**
- **Tone pool (the base for all tone rates):** unique texts, length <= 1,000 chars → **M = 532**
  (grok 172, codex 360). Length cap evidence: keyword flags fire on pasted transcripts, not chat
  lines — the uncapped P∧A∧C cell held 90 rows with median length 80,905 chars (NACHO MASK
  drafting blobs quoting his X posts). Flag rate by length: <=100 chars A=1.8% vs >1,000 A=15.3%.
- Date coverage: 2026-08-04 → 2026-09-09 (1,897/1,904 rows dated). **Coverage gap:** the pools
  END 09-09; OCEAN.md quotes run to 09-29 (drawn from watch/inbox receipts — a different,
  uncounted instrument). Presence instrument `memory/mirror/operator_presence.json`
  (n_messages=4,968, crest Thu/Fri) is a third denominator and is NOT mergeable with these.

## 2. The classifier (stated, cheap, keyword — and its audited error bars)

Three independent flags, case-insensitive regex, first-match-anywhere:

- **P profanity:** `\b(fuck\w*|bullshit|shit\w*|damn\w*|bitch\w*|bastard\w*|crap\w*|piss\w*|asshole\w*|dickhead\w*)\b` ("hell" excluded — catches "hello"/"hell yes").
- **A approval:** `\b(hah+|lol|lmao|lmfao|baller|badass|spooky|beautiful|genius)\b|bad ass|i love it|love it|nice work|good work|great work|well done|good shit|fuck (yes|yeah)|hell (yes|yeah)|stamp it`
- **C correction:** `why are you|why is this|why do you|self steal|isn't gonna fly|handwavy|hand wavy|wasting|impatient|slop|stop asking|stop building|stop doing|stop running|stop\.|you're doing|you are doing|should have|shouldn't|didn't|wrong|again\?|no\.`
- **CAPS:** >=70% uppercase alpha and >=8 alpha chars.

**Manual audit** (author of this doc read and hand-classified; stratified seeded sample
random.Random(20260930), drawn from the pre-final pool — 51 system-envelope rows found this way
were then excluded and counts rerun):

| Audit | Sample | Verdict | Wilson 95% CI |
|---|---|---|---|
| A precision (genuine approval-of-fleet) | 9/9 A-flagged read | **3 strict** ("good work" dispatch; "it is beautiful… i love you rn"; "sounds good… love it"); 4 if profane banter counts; 2 of 9 are self-directed "lol", 1 is a paste, 1 external mockery | 3/9 = 33% [12%, 65%] |
| C precision (genuine behavior-correction vs task-word false hits: "Stop" in dispatch instructions, "wrong tag" in specs) | 15/50 read | 5/15 genuine corrections ("the tag is wrong again", 3× "self steal", "stop forgetting…") | 33% [15%, 58%] |
| P precision (operator genuinely using profanity, post-envelope-fix) | 15 read pre-fix; 3 were system envelopes, excluded since | 12/15 genuine; of the 12, **8 failure-directed** ("what the fuck are you doing", "STOP PAUSING JUST FIX THE REST"), 4 casual/positive ("holy fuck my man") | 80% [55%, 93%] |
| False negatives (probe, not full audit) | loose words `sounds good|perfect|great|cool|nice|nailed|…` over the 523 non-A unique tone rows | 6 additional candidate-approval rows ("you did great so far thanks") | approval upper bound +6 |

Known residual biases: keyword flags undercount approval phrased with plain words (bound above),
overcount on any missed template; the tone pool still contains operator-authored dispatch
prompts (neutral by nature), which pushes the neutral share UP.

## 3. Base rates (unique texts, <=1,000 chars, M = 532; 2026-08-04 → 2026-09-09)

| Tone | Count | Rate | Audited/genuine estimate (method: rate × audit precision) |
|---|---|---|---|
| Neutral / task dispatch | 441 | 82.9% [79.5%, 85.9%] | the MODAL operator message is a neutral ask/dispatch |
| C correction-flagged | 50 | 9.4% [7.2%, 12.2%] | genuine correction ≈ **3.1% [1.4%, 5.5%]** |
| P profanity-flagged | 42 | 7.9% [5.9%, 10.5%] | genuine profanity ≈ **6.3% [4.3%, 7.3%]**; ~2/3 of it failure-directed (8/12 audit) |
| A approval-flagged | 9 | 1.7% [0.9%, 3.2%] | strict approval ≈ **0.56% [0.19%, 1.6%]**; loose upper ≈ 1.7% |
| P∧C (profane correction) | 6 | 1.1% [0.5%, 2.4%] | |
| P∧A (profane + approval token) | 2 | 0.38% | **both rows audited as banter** ("lol stop being a bitch and publish them"; "LOL WHAT A FUCKING SCAM") — neither is affection-toward-fleet |
| CAPS | 7 | 1.3% [0.6%, 2.7%] | sampled rows are corrections ("STOP PAUSING…", "THE Z.AI THING IS STILL FUCKED") |

Per-surface split (unique tone rows): grok M=172 → P 3.5%, C 5.2%, A 2.9%; codex M=360 →
P 10.0%, C 11.4%, A 1.1%. The correction register concentrates ~3× on the build surface
(codex); both are the same operator on different surfaces.

## 4. Claim-by-claim verdicts (the re-base)

**SURVIVES (with numbers):**
1. *Profane correction register exists* — 6 P∧C per 532 (1.1%); ~8 audited failure-directed
   profane messages; concentrated in short messages (P rate 11.2% at <=300 chars vs 7.9% overall
   tone pool). Real, rare, short.
2. *ALL-CAPS = correction* — 7/532 (1.3%); all sampled rows are corrections. Survives as a
   rare-register rule, not a common event.
3. *Approval register exists* — strict 3/532 (0.56% [0.19%, 1.6%]); loose ceiling 1.7%. Real
   and LOUD ("it is beautiful… i love you rn") but a tail event, not a channel.
4. Countable facts kept: 20 numbered laws in .agents/skills/operator-corrections/SKILL.md
   (grep-verified 2026-09-30); presence instrument n_messages=4,968, crest Thu-Fri
   (memory/mirror/operator_presence.json); pool date range 08-04 → 09-09.

**DIES (quote-only, no base-rate support):**
5. *"Challenging is the affection"* (OCEAN.md headline) — **FRAME-NOT-FINDING.** The
   affection-in-challenge co-occurrence is 2 rows per 532 (0.38%), both audited as banter;
   corrections (≈3%) and approvals (≈0.6%) are separate tail events; the modal message is a
   neutral task dispatch (82.9%). The frame is the estate's reading of its commissioner, not a
   measured property.
6. *AGREEABLENESS "LOW-MED … with HIGH loyalty (confidence: HIGH)"* — **deleted as a rating.**
   Loyalty has no instrument (law 12 is 1 law of 20 on record — a count of one event class, not
   a loyalty rate). What the counts actually support: correction ≈ 3.1% [1.4%, 5.5%], approval
   ≈ 0.6-1.7% of interactive messages. A Big-Five grade cannot be computed from these.
7. *The v2 doc's own evidence base* — OCEAN.md's AGREEABLENESS section rests on 8 quotes =
   8/532 = 1.5% of the interactive pool, 8/1,231 = 0.65% of unique texts, 8/4,968 = 0.16% of
   the presence instrument (N1's "<0.1%-order" charge confirmed at the presence denominator).

**KEPT BUT DEMOTED:**
8. OCEAN axes Openness / Conscientiousness-split / Extraversion-asymmetric / Urgency —
   **QUALITATIVE-UNREBASED.** Each rests on <=5 selected quotes with no denominator; they are
   hypotheses a future count could test (e.g., "starter not finisher" is testable against repo
   prototype census; "urgency" against inter-message latency in the pool). Until then they
   carry no confidence grade.

## 5. Standing law for this doc

Any future edit that adds a claim without (count, denominator, method) is a defect. Re-run the
reproducer after pool growth (grok pool gains sessions continuously); a rate stated without a
date is a fabrication smell. Freshness: re-base monthly or freeze with reason.
