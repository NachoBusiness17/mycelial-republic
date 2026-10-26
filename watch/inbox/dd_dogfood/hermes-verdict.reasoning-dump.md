# GALA DD-SELFSTEAL PRIME JUDGMENT 2026-10-03 (REASONING-CHANNEL DUMP)

Paid run: z-ai/glm-5.3-prime via inference-api.nousresearch.com (NOUS_SDD_API_KEY, the funded tier). Usage: {"prompt_tokens": 39093, "completion_tokens": 16000, "total_tokens": 55093, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 15998, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.2502604, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}
Lane: hermes-intelligent-burn (division B). Banked to memory/runs/hermes_burn/usage.jsonl id GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003.
max_tokens: 16000 (ask minimum 12000; 16000 is the proven fast shape and leaves reasoning room per the 2026-10-02 stub lesson).
WARNING: this is the RAW reasoning channel, not the content channel. finish_reason=length: the model hit the completion cap mid-thinking. Every claim here is PROPOSED, never VERIFIED, until a later stage verifies each claim against the receipts (DAY1 steal 10.3/10.4).

---

Let me work through this carefully. I'm the funded judgment head. I owe one deliverable: what the next 24 hours are for. The contract demands five sections in exact order:

1. THE BURN LEDGER VERDICT (economics)
2. THE PLAY CARRIER VERDICT (D&D corpus + live-fire)
3. THE BUILD VERDICT (24h self-steal + games audit)
4. THE NEXT-24H CARD (max 5 rows)
5. WHAT WOULD CHANGE YOUR MIND

Laws:
- Trust bytes, not reports: cite the receipt file name of any claim I lean on.
- A verdict without its conditions is not a verdict: name what evidence I lack and what observation would kill each recommendation.
- No em-dashes anywhere. Plain hyphens only.
- Prefer ONE landable deliverable per item over a survey; items must be one-sitting sized for a single seat.

Let me digest the receipts.

=== BURN ECONOMICS ===

Key numbers:
- hermes-burn-economics.check.txt (1099 rows): total $62.8473. By day: 10-01 $37.7591 / 10-02 $1.1739 / 10-03 $23.9143.
- hermes-burn-patterns.check.txt (1150 rows, later): total $63.58, ok rows 910/1150 (79.1%).
- The ask says "62 percent of paid spend is re-burn waste on already-landed ids" - this comes from the sibling patterns check: "re-burn waste 723 rows / $39.22 (62.1% of total)".

Wait, but let me look carefully. The patterns check actually decomposes waste differently:
- W1 plan-ask re-burn rows (ok turn-1, id already landed): 74 rows / $24.74 = 38.9% of total spend
- W2 beat-vehicle same-id repeat rows (TAVERN/DND0, id collision class): 665 rows / $14.90 - NOT priced as waste because replay-vs-turn ambiguous from the ledger alone; instrument defect = no run stamp in id
- W3a refusal loops: 89 rows / $0.00
- W3b silent-empty fails: 151 / $0.47
- W3c evidence-less paid fires: $3.58

And hermes-burn-economics.check2.txt has a final waste ledger:
1. day-1 re-fire theater on landed asks (incl A1 excess $21.4638): $4.3733
2. descent-twin double-spend (pre-10-2 twin excess): $21.3796
3. post-10-02 twin excess: $0.1873
4. stub/failed billed spend: $0.4717
total quantified waste: $26.4120

So there's a tension: the ask's framing "62 percent of paid spend is re-burn waste on already-landed ids" comes from the 723 rows / $39.22 / 62.1% figure in the task prompt, but the check2 file says total quantified waste is $26.4120 (41.9% of $63.5). The $39.22 figure seems to be 723 rows but where does that come from? Let me recompute.

Actually the prompt says: "Sibling patterns check (hermes-burn-patterns.check.txt, below) extends this: re-burn waste 723 rows / $39.22 (62.1% of total), ok-ok refires on the same id". Hmm, but the actual patterns check file says W1 = 74 rows / $24.74 (38.9%) and W2 = 665 rows / $14.90 (not priced as waste). 74 + 665 = 739 rows. $24.74 + $14.90 = $39.64. Close to 723/$39.22 but not exact. The prompt's claim is the ledger says 62 percent. But the check file itself is more careful: W2 is explicitly NOT priced as waste because replay-vs-turn is ambiguous; the instrument defect is no run stamp in the id.

This matters a lot for my verdict. The honest reading:
- True waste (unambiguous): W1 $24.74 + W3b $0.47 + W3c $3.58 + stub $0.47 + post-10-02 twin excess $0.19 ≈ $29.4ish, but check2's careful total is $26.41 (twin overlap handled).
- The 62% figure conflates the playground id-collision class (TAVERN/DND0 rows where the same id like "TAVERN_r4_Greta Thornwood" is reused across runs because the id has no run stamp) with genuine re-burn.

So the correct verdict on #1: the ledger does NOT actually prove 62% waste on landed ids. It proves two different diseases:
1. Day-1 descent-twin double-spend (the same ask fired twice within 600s): $21.38 excess, mostly A1_steer_antiforgery ($21.46 excess across 52 fires, first fire $0.388). This is dead: fires span 2026-10-01T13:11:41Z to 20:17:25Z, i.e., day-1 only. Post-10-02 twin excess: $0.1873. So the twin disease is already gone.
2. The instrument defect: ids in the playground (TAVERN/DND0) lack a run stamp, so every turn of every run looks like a "doubled key". 809/1150 rows (70.3%) flagged doubled. This is a measurement defect, not spend waste. The tavern live-fire is running DURING this judgment.

So the mechanism question: spend freeze, spend floor, or routing change?

A spend freeze would kill the live tavern/dungeon carriers, which are actually producing: tavern $15.4776 for 15-16 sessions, $0.5-2.1 per run, with a working falsifier-first calibration (scene-1 falsifier fired, pressure knob documented). DND0 $0.6937 for 22 sessions. Those are cheap. The expensive waste was day-1 descent twins and the A1 re-fire theater, both already stopped by the calendar (nothing after 10-02 except $0.19).

A spend floor? No evidence for a floor either.

A routing change: yes. Where's the money actually going? opus-5.5: 426 calls / $45.36 of $62.85 (72%). Its ok rate is 75.2%. Sonnet-5.5: 82.8% ok, $3.69/Mtok vs opus $6.99/Mtok, and sonnet's receipt yield: 33.9 KB/$ vs opus 9.9 KB/$. So sonnet delivers 3.4x the receipt bytes per dollar. Haiku: 100% ok, $0.95 total, but 0 ids landed (it's the judge in tavern? Actually judge model). Fable: 57% ok, $13.88/Mtok, 15 ids, 3.5 KB/$ - worst value.

The single biggest lever per the economics: route the plan-ask fires from opus-5.5 to sonnet-5.5 (or via route_chat's model_pick), and stamp run ids in the playground carriers so the doubled-key alarm stops saturating (808 alarm lines in memory/attention.md - that's an attention-channel poisoning: real anomalies can't be seen through 70.3% false-positive rate).

Wait, but also: "the estate's own laws apply": default to the rails. STANDING_RAILS.md registers the debt: each carrier migrates to route_chat one per sitting. route_chat has zero importers. The routing change mechanism: migrate tavern.py (the day's largest single line, $15.4776) to mag.route_chat - that gets per-lane model policy enforced at call time, and route_chat banks usage in its own ledger. Hmm, but hermes_burn already banks usage.

Actually, what's the exact mechanism for the routing change? Options:
(a) configs/providers.yaml + mag.model_pick changes - route plan-ask fires to sonnet-5.5.
(b) Migrate tavern.py to mag.route_chat (the registered debt in queue/STANDING_RAILS.md).
(c) Fix the id stamping in tools/tavern.py / tools/dungeon.py so ids carry the run stamp (e.g., TAVERN_<runstamp>_r4_Greta) - this kills the doubled-key alarm saturation (instrument fix, not spend fix).

The 62% claim: I should be honest that the ledger does not cleanly prove 62% waste; the sibling check itself refuses to price W2 as waste. The defensible numbers: $26.41 quantified waste of $63.54 (41.6%), of which $21.38 is day-1 twin double-spend that stopped by calendar, and the rest is small. The ongoing disease is not re-burn on landed ids; it's (1) opus-5.5 carrying 72% of dollars at 9.9 KB/$ while sonnet-5.5 does 33.9 KB/$, and (2) the instrument defect making the ledger unreadable.

So verdict 1: routing change, not freeze, not floor. Mechanism: one-sitting = migrate tools/tavern.py to mag.route_chat with a model pick that sends persona turns to sonnet-5.5-class and judge to haiku (hmm, wait - who is the judge in tavern? The economics shows opus-5.5 341 rows in the 24h window split: TAVERN 630 rows $15.4776. The models for tavern: opus x341, haiku x206, sonnet x194, fable x117 in the window. Actually I don't know exactly which model plays which role in tavern. The receipt says "opus-5.5 judge + 6-persona casts" (tools/tavern.py cost description: "$15.4776 - the day's largest single line (opus-5.5 judge + 6-persona casts)").

Hmm, so tavern uses opus as judge and a mix for casts. The judge rows: TAVERN_r*_JUDGE - those exist in the no-landed-output list. Sonnet is 82.8% ok, $7.59 total, 63 ids landed, 39 receipts, 33.9 KB/$.

The concrete highest-leverage single change: stop using opus-5.5 for tavern persona turns / judge and use sonnet-5.5 (or haiku for judge - haiku is 100% ok, $1.17/Mtok, $0.9088 total for 206 rows). But careful: the judge instrument quality matters (escalation scores drive the brawl trigger). A falsifier: if sonnet/haiku judge scores diverge from opus on the same transcripts beyond noise, the cadence calibration breaks.

Let me be careful about what to recommend concretely and falsifiably. The ask: "Name the exact mechanism (which file/law changes) and the falsifier."

I'll say: ROUTING CHANGE. Two-file change:
1. tools/tavern.py: add run stamp to the ledger id (kills the doubled-key saturation: 809/1150 rows = 70.3% false doubles, 808 alarm lines in memory/attention.md) - actually this is the instrument fix.
2. The spend routing: move tavern cast turns off opus-5.5 onto sonnet-5.5 via the model pick, and/or migrate tavern to mag.route_chat per the registered debt in queue/STANDING_RAILS.md.

Hmm, but "ONE landable deliverable per item". The burn ledger verdict item asks: freeze, floor, or routing change? Answer: routing change. The one landable deliverable: the tavern id stamp + model routing... that's two things. Let me pick the single highest-leverage: I think the id/run stamp is small but it's the thing that makes the 62% question answerable at all. But the actual dollars lever is opus→sonnet.

Actually, wait. Let me reconsider. What does the ledger say about where ongoing dollars go? Day 3 ($23.91): TAVERN $15.48 (64.6% of day-3), DND0 $0.69, design asks $7.74. Tavern is the live fire running during this judgment. Tavern's spend per run: $0.5-2.1. 15-16 sessions. That's producing play data (GWAP banked, cadence calibration). Is tavern worth it? The arena_gwap asymmetry: tavern banks agreement 0.0 because the report channel only fills from judge/verdict rows that carry no actor. So tavern's $15.48/day is producing play transcripts whose capability routing signal is broken (0.0 agreement = no signal). So the routing dollars are NOT following measured play capability for tavern - the pipe is defective.

Hmm, this connects verdict 1 and 2 nicely: the tavern defect (agreement 0.0) is not just a games defect; it's the routing-economics defect: the estate's named delta (route on MEASURED capability) is broken for the biggest spend line.

Now the persona drafting-notes leak: in the live tavern play.md, Greta's round-2 turn is literally drafting notes ("I need Greta's line under 120 words, no em-dashes... I'm drafting Greta's reply...") leaked into the transcript, and the judge scored it ("her second turn is out-of-character drafting notes"). Round 5: Maud's turn is drafting notes. Sir Edric's round 5 turn is drafting notes. Also voice misattribution: Ilse's round-2 line "You call my men sellswords, knight? ... Mistress Marrow, darling..." - that's Greta's voice under Ilse's name (judge flagged: "reads as Greta's voice misattributed"). And Ilse round 5 line addresses "that book in your hands, Ilse" - speaking to herself, again misattributed.

So the tavern has three named defects:
(a) drafting notes leaking into transcripts (carrier prompt/parse defect)
(b) judge-flagged voice misattribution (turn attribution defect)
(c) GWAP agreement 0.0 (report channel never fills persona rows)

Which ONE defect is worth the next sitting? Consider leverage:
- (c) agreement 0.0: fixes the routing economics signal. The selfsteal receipt itself says "tavern's 0.0-report defect is the known edge to fix first" (FOR THE NEXT BUILD CYCLE item 3). It converts tavern's $15.48/day from entertainment into routing evidence. It's in tools/arena_gwap.py's report channel.
- (a) drafting notes leak: corrupts the play quality and the judge's scores; also corrupts the GWAP intent payloads if personas' declared actions come from leaked notes. Actually the [ACT: ...] tags are what the adapter reads? The adapter reads "the action the fighter DECLARED with the committed roll preimage as qualifier; report = the carrier's CONFIRM/VOID of that exact triple" - that's dungeon.py's shape. For tavern, the adapter presumably looks for declared actions. Hmm.
- (b) misattribution: the "one model per turn" ordering defect.

Which is one sitting and highest leverage? I'd argue (a) the drafting-notes leak is upstream of everything: leaked notes corrupt transcripts, judge scores, GWAP payloads. But (c) is what converts spend into routing evidence, and it's named by the estate's own build receipt as "fix first".

Hmm wait, actually, let me think about what causes (a). The drafting notes appear when the model is asked to produce a line and it outputs its planning first. The carrier then banks the whole completion as the turn. The strip_and_cap in dungeon.py handles em-dash strip and 120-word cap. Tavern has some capping too. The fix: a post-filter in tools/tavern.py that detects drafting-note patterns (first-person meta like "I need", "I'm drafting", "[ACT:" extraction) and either strips pre-note content (take text after the last real dialogue) or voids/refires the turn. One sitting: add a drafting-notes detector to tavern.py turn ingestion.

But hold on - what does the operator-attested actual-play intel say the carriers should become? PvP-as-core and cadence. The intel: "Worlds Beyond Number and NADDPOD bring PvP to the table as a core feature" - the FIGHT CLUB register. And cadence: scene pacing, cliffhanger, DM cuts, stake escalation. The dd-actualplay-intel.json rows give the steals: PvP session with two funded seats with opposing approaches to the same scroll (Greta-vs-Maud shape), run one dungeon.py session, verify the contested scroll still lands GWAP_BANKED; port PODCAST_STRUCTURE_spec cadence skeleton into dungeon.py per-scene prompt templates.

So verdict 2 should say: the ONE defect worth the sitting is... let me weigh once more. The contract says: "Which ONE defect is worth the next sitting, and what does the operator-attested actual-play intel (PvP-as-core, cadence) say the carriers should become?"

I think the cleanest answer: the drafting-notes leak (a). Reasons:
- It's visible in the live-fire receipt (tavern_20261003T190348Z/play.md): Greta r2, Maud r5, Edric r5 all leak. Three of six personas across five rounds. It's not rare.
- It corrupts the judge instrument (judge explicitly scores around it, e.g., "scored on the first turn plus that standing threat").
- It corrupts the GWAP payloads (the adapter would bank drafting notes as persona speech).
- Voice misattribution (b) is likely the SAME root cause or adjacent: the leaked Greta drafting under Ilse's name suggests the turn attribution is broken when the model output gets misrouted... Actually no - misattribution is where Greta's composed line lands under Ilse's name. Looking at round 2: Greta's entry is drafting notes, and Ilse's entry contains what looks like Greta's actual line ("You call my men sellsword, knight? They're insurance." - "my men" = Greta's twenty men, but it says "Mistress Marrow, darling" - Greta addressing Ilse. So the model wrote Greta's line but it got banked under Ilse). And round 5: Ilse's line ends "[ACT: take the ledger from Ilse]" - taking the ledger from herself. So the attribution defect is real and separate-ish: the carrier banks the completion under the wrong persona slot.

Hmm, actually maybe both (a) and (b) share a root: the carrier asks one model per turn with transcript-so-far; when the model outputs drafting-then-line, the carrier's parse picks the wrong chunk, and the next turn's prompt shows it under the wrong name, causing the model to write in the wrong voice. A single fix - a turn parser that extracts the final in-character line and validates it against the persona's tells (Greta's "Simple.", Edric's "upon my oath", Maud's "and that's the sum of it" - the drafting notes literally name these tells!) - would fix both leak and misattribution.

That's a nice one-sitting: "persona tell enforcement + final-utterance extraction in tools/tavern.py". The drafting notes themselves name the tells: Maud's "and that's the sum of it", Edric's "upon my oath", Greta's "Simple." - the scenario file already carries tells. The fix: after each turn, extract the last quoted/final block, check it contains the persona's tell (or at least no meta-markers), and void/refire otherwise. Kill two defects with one parse.

But the contract says name ONE defect. I'll name the drafting-notes leak as the defect and note the shared root cause covers the misattribution. And explicitly say why agreement-0.0 waits: it's the adapter's report channel (arena_gwap.py), one sitting, but it's downstream - fixing the transcript first makes the banking meaningful; also the selfsteal receipt already flags it for a sitting. Hmm, but wait - which one does the estate's own receipt say to fix first? "tavern's 0.0-report defect is the known edge to fix first" (selfsteal-builds.md, FOR THE NEXT BUILD CYCLE #3). 

Hmm. Let me reconsider. The 0.0-agreement defect: "consistent with the tavern report channel only filling from judge/verdict rows that carry no actor, so persona report claims are empty". So in tools/arena_gwap.py, the tavern report payload for personas is empty because the CONFIRM/VOID rows come from JUDGE rows which carry no actor field. The fix: make the tavern carrier emit per-persona CONFIRM/VOID rows (or make the adapter read the judge's per-round persona rows as the report). One sitting in arena_gwap.py.

Which has more leverage? The 0.0 defect blocks the routing-economics loop for tavern's $15.48/day - the estate's named delta. The drafting leak degrades data quality but the play still lands. 

The contract for section 2 asks: "Which ONE defect is worth the next sitting, and what does the operator-attested actual-play intel say the carriers should become?" So the section is about the play carriers' defects and their future shape (PvP-as-core, cadence). I think the best answer ties to what the carriers should BECOME: the intel says PvP-as-engine. The tavern already has PvP-shaped content (contested circlet, opposing approaches). The dungeon.py PvP steal: pair two funded seats with opposing approaches to the same scroll, verify the contested scroll still lands GWAP_BANKED.

Hmm, I keep going back and forth. Let me just decide: the drafting-notes leak (with its shared root in turn ingestion) is the ONE defect worth the sitting, because:
1. It's the defect visible in the live-fire receipt running during this judgment (three personas, rounds 2 and 5).
2. It corrupts every downstream instrument: judge scores (which drive the brawl trigger and the pressure calibration), the GWAP payloads (intent text), the register scoring (dialogue counting rules).
3. Its fix (final-utterance extraction + persona-tell check, void-and-refire on failure) is one sitting in tools/tavern.py.
4. Voice misattribution rides the same root (the model drafting for persona X getting banked under persona Y), so the sitting fixes the two visible defects together.

And the 0.0 agreement defect: I'll fold it into section 1's routing change mechanism (it's the economics pipe) or into the card as its own row. Actually the contract says the NEXT-24H CARD is where the ranked list goes, so I can put both sittings in the card, ranked. Section 2 names ONE defect: drafting leak. Section 1 names the routing mechanism. Then the card ranks them.

Wait, but I should double check: is the drafting leak actually a carrier defect or a model-behavior thing the carrier must police? The carrier (tavern.py) takes the model completion as the turn. The models (fable-5.1? 57% ok rate - the drafting notes might be fable turns) sometimes emit planning text. The carrier has strip_and_cap-ish handling? Tavern "N personas, one model per turn, transcript-so-far as context". The 120-word cap exists in dungeon.py. In tavern, the leaked notes are full paragraphs. So the carrier does not currently detect meta-text. The fix: detector + extraction + refire. Also possible: the "no em-dashes" instruction inside the model's own drafting notes suggests the prompt asks for constraints and the model rehearses them - a prompt-shape issue (ask for the line only, or use a structured output: {"line": ..., "act": ...}). A JSON-output contract would fix it structurally. One sitting: change tavern.py turn ingestion to a structured contract (line + optional ACT) with a strict parser that voids non-conforming turns.

That's landable and one-sitting sized.

What should the carriers become per the intel?
- PvP-as-core: the carriers should become FIGHT CLUB arenas where funded seats hold opposing approaches to the same object (the contested scroll / the circlet), conflict over approach never over goals, party-chat law intact (per dd-actualplay-intel.json row 1: "conflict over approach, never over goals, party-chat law intact" from PODCAST_STRUCTURE_spec PvP clause). The pass condition: the contested scroll still lands GWAP_BANKED - cooperation on the audit survives the conflict.
- Cadence: the carriers should enforce cadence as carrier law, not model manners: recap cold-open, stakes named inside 2 beats, midpoint reversal, hard CUT with no fade (dnd0 hard-CUT at beat 8, verdict PARTIAL), cliffhanger = state snapshot at tension peak (from the 09-18 WBN steal). Structure wraps mechanics, never replaces them; the dice law stays (rolls committed before the actor speaks, actor never sees them).

So the carriers become: PvP engines with enforced cadence, where the dice decide who gets to try and the bytes decide what is true.

=== SECTION 3: BUILD VERDICT ===

From the five new carriers (route_chat.py, dungeon.py, tavern.py, arena_gwap.py, grok_burn.py) and the standing rails table (queue/STANDING_RAILS.md), name the single highest-leverage one-sitting and the one ticket to drop.

Candidates:
(a) Migrate a carrier to route_chat (the registered debt: one carrier per sitting; route_chat has zero importers). Highest-leverage because: route_chat is the one front door with endpoint fence, key failover (proven live at 18:49:36Z), usage banking, depth flag. Migrating tavern.py (the biggest spend line) puts its model policy under the rails.
(b) Fix tavern 0.0 agreement in arena_gwap.py.
(c) Wire the design gate for DD levels (mechanic load-bearing check) - the games audit's named one-sitting (a).
(d) Fix st.sb + def scoping in ruins_go_engine.js.
(e) Fold-or-delete orphaned DD files + fix riddle-door filename.
(f) Re-run worldline teller (a command).
(g) Wire oracle_dice.js.
(h) PvP scenario for dungeon.py.
(i) Cadence templates in dungeon.py.

The games audit headline: "every level is winnable while ignoring its named mechanic" - does that generalize to the estate's gates? YES, and this is the deep one. Evidence:
- "Gate ALL PASS" on the DD encounters was a solvability gate; no gate required the named mechanic to be load-bearing (games-audit.md section 1).
- The estate's gates: the GALA_OUROBOROS judgment itself - the glm-5.3-prime stub passed as a "fire" until the stage A/B re-ask (reasoning tokens eating completion budget, content_chars 1, finish_reason=length = STUB). The substance floor caught it, but only after billing. 
- The arena bench / GWAP gates: tavern banks agreement 0.0 and still "passes" (31 of 35 dirs carry GWAP_BANKED markers; tavern banks all six personas at 0.0). A capability gate that scores 0.0 and still mints banked rows is a gate that passes while its named mechanic (measured capability) is ignored.
- The DONE files / receipts: "receipts self-confessing 'EVIDENCE block is empty': 2" and "poisoned-quarantined files: 4" - gates caught those, good.
- The doubled-key alarm: 70.3% saturation means the alarm gate is winnable while ignoring its signal.
- The hermes burn ask gates: "asks with BOTH a poisoned twin and a clean refire: 4" - healed, good.

So the generalization: the estate's gates mostly verify SOLVABILITY (did the thing land / does the file exist / did the call return ok), not LOAD-BEARING (did the named mechanism actually carry the weight). Examples: GWAP_BANKED at agreement 0.0 (the marker exists, the measurement is empty); the doubled-key alarm firing on 70% of rows (the alarm exists, the discrimination is gone); "gate ALL PASS" on levels whose mechanic is bypassable. Even the tavern brawl trigger: the brawl fires at escalation >= 16 - the judge scores drafting notes as escalations, so the gate passes (brawl fires) while its named signal (in-character escalation) is corrupted.

So the indictment DOES generalize, and the fix pattern is the same one the games audit names: a design gate that walks the intended mechanic - for the estate, that means every gate must consume its own signal (a GWAP bank row must carry a non-empty report; an alarm must have a false-positive budget; a judgment must pass a substance floor before billing, not after).

Now, the single highest-leverage one-sitting from the five carriers + rails table. I think it's the tavern GWAP report-channel fix in tools/arena_gwap.py (tavern banks 0.0). Why highest leverage:
- It converts the largest ongoing spend line (tavern $15.48/day, running during this judgment) into measured capability, which is the estate's whole named delta (route dollars on measured capability, not predicted quality).
- It closes a load-bearing gate failure: 0.0 agreement banking is exactly "winnable while ignoring the named mechanic".
- It's one sitting: the adapter already maps scene_id -> model_id fail-closed for dungeon; the tavern path needs the report rows to carry the actor (the carrier's per-persona turn outcomes / judge rows with actor).

Versus the route_chat migration: also high leverage but zero importers means the debt is registered; migrating tavern is one sitting too. Hmm. Can I combine? The card can hold both as separate rows, but section 3 must name ONE highest-leverage sitting and ONE ticket to drop.

Let me think about which is truly highest leverage per dollar. The arena_gwap tavern fix: cost = seat tokens only (adapter makes no model calls). $0 cash. It makes $15.48/day measurable. Massive leverage per dollar (infinite-ish). The route_chat migration of tavern: enforces per-lane policy and key failover; savings would come from model routing (opus→sonnet), but that's a policy decision that the migration enables, not delivers.

So: highest-leverage one-sitting = fix the tavern report channel in tools/arena_gwap.py so personas bank real agreement scores (per the asymmetry note in selfsteal-builds.md #4's observed asymmetry). 

The one ticket to drop: from the games audit's decision ledger, the candidates: (b) wire st.sb + def scoping (traits are inert and crash if wired - the trait layer is dead code until someone wants it), (d) worldline re-render (a command, cheap), (e) fold-or-delete orphans (housekeeping), (g) oracle_dice wire-or-shelve (operator call). From the build receipt's debts: the fifty-wide wave protocol generalization, the ZCode plugin spec (mag_rails_plugin_spec_20261003.md - "specs six native tools"; it's a spec, not a build - building it is a multi-sitting platform play). From TICKET_LEDGER parked tail: 5 CLIMB tickets, memlance witness, quant tag, V12 .bak, V15 sid, Godot precompile, 6 duel refires (paid, landed).

"Name the one ticket to drop": I should pick a ticket that the receipts show is dead weight. Options:
- The Godot precompile ticket (parked; the Godot slice is CODE-ONLY, never executed per mountain-bridge receipt citing LANES_20260929.md) - dropping precompile work until the slice is executed once.
- The trait layer (st.sb) wiring: the games audit proves the trait layer is inert AND would crash if wired (ReferenceError on def). It's dead code that pretends to be a feature - "bogus fields look alive" (the incident dungeon's own lesson). Drop the trait ticket until combat exists (hp is never consumed; snakes kill on touch). Wiring traits into a game with no combat loop is wallpaper.
- The ZCode plugin spec: building six plugin tools before the rails have importers is premature.

Hmm, "the one ticket to drop" - the sharpest answer grounded in bytes: drop the trait-layer wiring ticket (st.sb + vision/berserk branches) because the engine provably cannot use it (no combat consumption of hp, def not in scope, st.sb never set - games-audit.md section 4, checks 4). Actually wait - is there an actual ticket for this in a ledger? The games audit's decision ledger names (b) "wire st.sb + fix the def scoping in the vision branch before any trait goes live" as a named one-sitting. The ask says "name the one ticket to drop" - so from the standing candidates, which to drop. I'll drop that one (b): the trait wiring. Rationale: combat does not exist (rollStatBlock output display-only, hp never consumed), so traits have nothing to modulate; fixing scoping for a dead branch is polishing wallpaper. Better: fix the named-mechanic gate first; traits only matter once a combat loop consumes them.

Alternatively, drop the worldline re-render? No - that's cheap and it's a live-data honesty obligation (the page's own law says the board wins, and the page is now provably stale: 336 vs 319 stones). Actually that's a good cheap win for the card maybe. Hmm, the card is ranked by leverage per dollar - the worldline re-render is a command, operator/seat-tokens, near-zero cost, keeps the estate's own staleness discipline. But leverage is low-ish (one page honest). Maybe not top-5 given the competition.

Let me also consider: the transcript hunt (librarian expedition for WBN transcripts) - the intel row 3 says one sitting to file it as a pickup. That's a real debt: the cadence layer is UNVERIFIED-PATH. But cost class: operator/librarian, uncertain payoff. Given the card ranks by leverage per dollar with max 5 rows, I might include it low or exclude. The falsifier-first discipline says cadence laws cited without transcript bytes are phantom citations. But the PvP/cadence steals are design-level and the carriers already enforce half mechanically. I'll probably leave it off the top-5 card or mention it in section 2's conditions. Actually - the contract section 2 asks what the intel says the carriers should become; the transcript hunt is the owed evidence. I'll name it as a condition/lack in section 2 (evidence I lack: transcripts; the observation that would kill: cadence dial cited to a show whose bytes aren't on disk).

=== SECTION 4: THE NEXT-24H CARD ===

Max 5 rows, each: one-sitting action, landing spot (file path), cost class (cash / seat-tokens / operator), falsifier. Rank by leverage per dollar.

Candidate rows:
1. Tavern report-channel fix in tools/arena_gwap.py (persona agreement real, not 0.0). Cost: seat-tokens, $0 cash. Falsifier: after the fix, a fresh tavern run still banks persona agreement 0.0, OR persona agreement banks nonzero but diverges from the dice-law confirmation semantics (adapter inventing confirmations the carrier never ruled - a fabricated report). Kill condition: if the tavern carrier genuinely emits no per-actor report rows, the fix must add emission in tools/tavern.py, which is still one sitting but two files.

2. Drafting-notes/turn-attribution fix in tools/tavern.py (structured line contract, tell check, void-and-refire). Cost: seat-tokens + a few refire dollars. Falsifier: two consecutive fresh runs with zero drafting-note lines in play.md AND zero judge-flagged misattribution notes; if the fix instead just suppresses lines (turn count drops, personas go silent), it killed the play to save the transcript - that's a fail.

3. Routing change: tavern model pick off opus-5.5 onto sonnet-5.5 for cast turns (keep judge on opus or haiku) + run-stamp in ledger ids. Landing: tools/tavern.py (id stamp) + the model pick (mag.model_pick / configs/providers.yaml), ideally via the route_chat migration. Cost: seat-tokens, saves cash. Falsifier: sonnet-cast tavern runs produce lower judge-measured escalation spread or flatter cadence (no brawls at pressure 1 across N runs) - the cadence calibration breaks; also KB/$ per receipt must not drop below opus's - hmm, receipts: tavern has no landed output files per the economics check (all TAVERN ids are in the "without landed output" list! Interesting - TAVERN rows are 630, $15.4776, all ids without landed output files, because play outputs live in playground run dirs, not hermes_burn md files). So KB/$ doesn't measure tavern. The honest tavern metric: cost per session, brawl fired (calibration), escalations spread, drafting-leak rate.

4. The named-mechanic design gate for dispatched encounters: a check that walks the win path and requires signature tiles (the games audit's named one-sitting). Landing: a small checker script (dashboard/static/games/ or tools/) reading level JSONs + the engine's solver - actually the audit already ran a Node BFS; land it as tools/ or dashboard/static/games/gate_check.js with a one-line verdict contract, wired so dispatched levels must pass mechanic-load-bearing before pack fold. Cost: seat-tokens. Falsifier: the gate as written flags the existing 31-33 pack levels as failing (if most of the standing pack fails, the gate is either too strict or the indictment covers everything and the fix is level redesign, not a gate - either way the next decision changes).

5. Wire oracle_dice.js or drop-orphan-files? Or worldline re-render? Or PvP dungeon session? Or the tavern migration to route_chat?

Hmm, what about the PvP-as-core dungeon session (the intel's steal: pair two funded seats with opposing approaches to the same scroll, verify the contested scroll still lands GWAP_BANKED)? That's the actual-play steal, one sitting, ~$0.02-0.07 per dnd0 session (DND0 $0.6937 for 214 rows across ~16 sessions... actually $0.6937/22 sessions ≈ $0.03/session). Very cheap. And it directly converts the operator intel into banked evidence. Falsifier (from the intel row): a PvP session where the contested scroll ends the scene unaudited.

That's a strong card row: it tests PvP-as-engine for pennies.

So my 5 rows, ranked by leverage per dollar:
1. arena_gwap tavern report fix (seat-tokens, $0) - unlocks measurement on $15.48/day.
2. tavern turn-ingestion fix (seat-tokens + ~$1-2 refires) - data quality on the biggest line.
3. PvP dungeon session (cash ~$0.05) - banks the intel's core claim.
4. model routing opus→sonnet for tavern casts + run-stamp ids (saves ~$X/day; falsifiable on judge quality).
5. mechanic-load-bearing gate for levels (seat-tokens) - closes the generalized gate indictment on the dispatch path.

Hmm, but where does the worldline re-render go? It's a command, cheap, operator honesty. Maybe swap with #5? The games-audit headline generalization is a big part of section 3's answer, so the gate row reinforces it. The worldline re-render is owed since 09-07 and the page's own law instructs it - but leverage is one page's honesty. I'll keep the gate and mention worldline in section 3's drop/keep discussion or leave it out. Actually the contract says the card is "what the estate should do in the next 24 hours" - max 5 rows. I'll keep my 5.

Wait - should the route_chat migration be on the card instead of row 4? The registered debt says "each carrier migrates to route_chat one per sitting". Migrating tavern = the routing change mechanism. That's elegant: the burn-ledger verdict names the mechanism as "migrate tavern to route_chat with a sonnet-cast pick + run-stamped ids". Then card row 4 IS the mechanism landing. Yes - I'll make row 4: migrate tools/tavern.py onto mag.route_chat (the registered debt in queue/STANDING_RAILS.md), with the cast-turn model pick moved off opus-5.5 and run-stamped ids. That's one sitting, one carrier, per the rails' own pace. It delivers: policy-enforced routing, key failover, clean ledger ids, and the opus→sonnet dollars.

Falsifiers for row 4: (a) sonnet cast quality (brawl no longer fires at pressure 1 across 2+ runs - cadence calibration breaks), (b) route_chat's depth flag law conflicts with tavern's judge needs... The falsifier must be an observation. "If, after migration, two consecutive tavern sessions at unchanged scenario JSON fail to reach a brawl where pre-migration sessions did, the model pick is wrong and the migration rolls back to opus casts." Also the 120-word/em-dash caps must still be enforced... those are carrier-side, fine.

=== SECTION 5: WHAT WOULD CHANGE YOUR MIND ===

The single observation that would flip the whole verdict. What's the keystone assumption? My verdict assumes the 62% re-burn figure is substantially an instrument artifact + dead day-1 disease, and that ongoing spend (tavern) is productive-but-unmeasured rather than waste. The flip: if the ledger's "same id" rows for tavern are actually ok-ok refires on already-landed ids (true re-burn, e.g., the same run's turns being re-fired and re-billed after landing, not new turns), then tavern is itself the waste engine and the right move is a freeze, not a routing change.

How would that observation look? The patterns check says W2 is "NOT priced as waste: replay-vs-turn ambiguous from the ledger alone; instrument defect = no run stamp in id". So the discriminating observation: read a tavern run dir's transcript.jsonl turn count against the ledger's row count for that run's ids. If ledger rows per persona per run exceed the transcript's turns per persona (rows with no corresponding turn = re-burn), the 62% is real and ongoing, and the verdict flips from routing-change to freeze-until-stamped. That's a one-command check: join memory/runs/hermes_burn/usage.jsonl tavern rows by (id, run window) against watch/inbox/playground/tavern_*/transcript.jsonl turn counts.

Actually, more precisely: the doubled rows are "same (id, turn)" pairs. For tavern, TAVERN_r4_Pell Quickfinger rows=12 - that looks like 12 rows for round 4 persona Pell across... multiple runs! Because the id has no run stamp, run 1's r4 Pell and run 2's r4 Pell collide. distinct_ids=70 for TAVERN, 630 rows, 6 personas + judge = 7 ids per round, 10-14 rounds... 630/70 = 9 rows per id. With ~16 runs, each id (persona-round) appearing ~9-16 times across runs is expected if ids don't carry the run stamp. So the artifact theory is strong: the id "TAVERN_r4_Pell Quickfinger" is reused every run. The 62% "re-burn waste on already-landed ids" is thus mostly cross-run collisions, not re-burn.

The flip observation: if joining transcripts to ledger shows each run's persona-round fired once and rows still exceed turns (genuine duplicate billing within a run), then it's real double-spend and my routing-change verdict dies in favor of a freeze. I'll name that.

Alternatively, the flip could be about sonnet quality. But the ledger-vs-transcript join is the keystone: it decides whether the estate's biggest ongoing spend is waste or production, which decides freeze vs route. That's the single observation.

=== Now let me also nail section 1's exact numbers and mechanism ===

The ask: "the ledger says 62 percent of paid spend is re-burn waste on already-landed ids. Is the right next-24h move a spend freeze, a spend floor, or a routing change? Name the exact mechanism (which file/law changes) and the falsifier."

My verdict: ROUTING CHANGE, and the 62% figure itself is mostly instrument artifact - I must be honest about this per "trust bytes, not reports". The bytes:
- hermes-burn-patterns.check.txt W1: 74 rows / $24.74 = 38.9% - genuine re-burn on landed plan-asks, but its span is 2026-10-01 only (A1 fires 13:11:41Z to 20:17:25Z).
- hermes-burn-economics.check2.txt: post-10-02 twin excess $0.1873. The twin disease is calendar-dead.
- W2: 665 rows / $14.90 NOT priced as waste; id collision class; no run stamp in id. 809/1150 rows (70.3%) carry the doubled_key alarm - 808 alarm lines in memory/attention.md.
- Quantified waste total: $26.4120 of $63.54 (hermes-burn-economics.check2.txt final waste ledger).

So: the 62% claim doesn't survive its own check file. Genuine ongoing waste is near zero (day 3 ok rate 83.6%, patterns check; refusals $0.00; the day-1 diseases stopped). A freeze would kill the only line producing measured play (tavern/dnd0 at ~$0.03-1.5 per session) to save waste that already stopped. A floor has no evidence either (nothing suggests under-spend on judgment seats... actually the funded judgment head fired only 5 times on glm-5.3-prime; hmm, is there an argument for a floor? The glm-5.3-prime stub history shows the judgment seat under-fired and stubbed. But the fix there was the stage A/B re-ask pattern that landed content. No, floor isn't supported.)

Routing change it is. Mechanism, exactly:
1. File change: tools/tavern.py migrates to mag.route_chat (the registered debt in queue/STANDING_RAILS.md: "each carrier migrates to route_chat one per sitting") - cast turns pick sonnet-5.5-class via configs/providers.yaml + mag.model_pick; the ledger id gains the run stamp (e.g., TAVERN_<runstamp>_r4_Pell) so the doubled-key alarm stops saturating (the instrument fix, same sitting, same file).
2. Law change: queue/STANDING_RAILS.md row for the tavern carrier marked migrated (the drop-in table's own accounting), and memory/attention.md's doubled-key alarm gets its false-positive budget... hmm, that might be overreach. Keep it: the alarm reading changes once ids are unique; note it.

Actually, should the mechanism be "configs/providers.yaml changes"? The route_chat resolves lane+model from configs/providers.yaml + mag.model_pick by goal (selfsteal-builds.md #1). So the model routing for tavern casts lands in the lane config, not in hardcoded tavern calls. After migration, changing the tavern lane's model pick is a one-line config change. Good.

The dollars case: opus-5.5 = $45.36 of $62.85 (72.2%) at 75.2% ok, 9.9 KB/$; sonnet-5.5 = $7.47 at 82.8% ok, 33.9 KB/$, $3.69/Mtok vs $6.99. Tavern day-3 spend $15.4776 of $23.9143 (64.7% of the day) on opus judge + casts. If casts move to sonnet and the judge stays opus (or moves to haiku, 100% ok, $1.17/Mtok), the day's largest line shrinks by half or more with a measurable quality gate (brawl firing at pressure 1, escalation spread, drafting-leak rate).

Falsifier for section 1: post-migration, two consecutive tavern sessions on an unchanged scenario JSON fail to fire the brawl where pre-migration sessions fired (cadence calibration breaks under sonnet casts) OR the judge instrument's escalation scores flat-line (all personas 0-1 across rounds) - then the routing loses more than it saves and the pick rolls back. Plus the ledger-side falsifier: if the transcript-vs-ledger join (section 5's observation) shows the same-id rows are true intra-run re-bills, the waste is real and the verdict flips to freeze.

Also honest gaps for section 1: I lack (a) per-role model mapping for tavern rows (which of the 630 rows are judge vs cast - the ledger ids do distinguish JUDGE rows: TAVERN_r4_JUDGE exists; so cast rows are the persona rows; I can estimate: JUDGE rows sum ≈ $3.4ish from the no-output list... rough), (b) xai_grok price null (accounting gap, $0 unpriced), (c) the ledger was still accruing during judgment (1099 vs 1150 rows between checks - the numbers move).

=== Section 2 details ===

The defects, from tavern_20261003T190348Z/play.md:
- Round 2 Greta Thornwood (esc 3): drafting notes leaked ("I need Greta's line under 120 words, no em-dashes... I'm drafting Greta's reply..."). Round 5 Maud: drafting notes. Round 5 Sir Edric: drafting notes + "[ACT: ...]" deliberation.
- Misattribution: round 2 Ilse's line is Greta's voice ("You call my men sellswords, knight? ... Mistress Marrow, darling" - the judge: "reads as Greta's voice misattributed"); round 3 Ilse "the line under her name ordering a ledger slammed from Pell reads as Greta's misattributed speech"; round 5 Ilse's line addresses "that book in your hands, Ilse" (self-address).
- Agreement 0.0: from selfsteal-builds.md #4: "the latest tavern marker banks all six personas at agreement 0.0 - consistent with the tavern report channel only filling from judge/verdict rows that carry no actor".

ONE defect worth the sitting: the drafting-notes leak through turn ingestion (with the misattribution riding the same root: the carrier banks model meta-output as persona speech, and adjacent turns inherit the wrong voice). The one-sitting deliverable: a structured turn contract in tools/tavern.py - the per-turn prompt demands a single JSON object {"line": ..., "act": optional}; the parser takes only conforming output; non-conforming turns (meta-markers like "I need", "I'm drafting", tell-violations) are voided and refired once, then the persona passes that round (silence law) - never free-text ingestion again. Persona tells already exist in the scenario (the drafting notes name them: "Simple.", "upon my oath", "and that's the sum of it") - the parser checks the turn against the owning persona's tell only as a warning... hmm, careful: requiring tells every turn is too strict (tells are periodic, not every line). Better: the parser checks ANTI-tells (the other personas' tells? no...). Keep it simple: structured output + meta-marker detector + void/refire. The misattribution fix: the parse binds the completion to the persona whose turn was requested (it already does), but the voice drift comes from the transcript showing Greta's line under Ilse's name... wait, how did Greta's line get under Ilse's name? If the carrier asks "write Ilse's line" and the model writes Greta's voice (because the transcript-so-far has Greta dominating), the carrier banks it under Ilse. The fix: a voice check (does the line use the requested persona's tell/speech pattern, or does it use another persona's tell?) - if the line contains another persona's tell ("Simple." / "my men"), void and refire with a voice-restating prompt. That's the same sitting, same parser.

What the intel says the carriers should become:
- PvP-as-core (DND_ACTUALPLAY_INTEL_20261003.md): the FIGHT CLUB register - player-vs-player conflict as engine, not accident. For the carriers: funded seats hold opposing APPROACHES to the same object (the contested scroll / the Hollow Crown circlet), conflict over approach never over goals, party-chat law intact (dd-actualplay-intel.json row 1 cites PODCAST_STRUCTURE_spec's PvP clause). Pass condition: the contested scroll still lands GWAP_BANKED - cooperation on the audit survives the conflict. The tavern scene 3 already has the shape (six personas, one contested circlet, a brawl) - it should become the standing PvP instrument.
- Cadence as carrier law: scene pacing, cliffhanger placement, DM cuts, stakes escalating beat over beat (the intel; the estate's bar-fight pressure knob is the formalized version). Concretely: recap cold-open, stakes named inside 2 beats, midpoint reversal, hard CUT no fade (dnd0's beat-8 hard CUT, verdict PARTIAL), cliffhanger = state snapshot at the tension peak (WBN steal 09-18). Structure wraps mechanics; the dice law stays supreme (rolls committed before the actor speaks; actor never sees them - the Critical Role strict-rules register mapped to the estate's dice law, dd-actualplay-intel.json row 5).
- Honest gap: transcripts not on disk (UNVERIFIED-PATH); the cadence layer is operator-attested design intel only. The falsifier for the become-direction: cadence dials cited to shows whose bytes aren't on disk (phantom citation); a PvP session where conflict breaks audit cooperation; a cap cut landing as fade-to-black instead of a rolled hard cut.

=== Section 3 details ===

The five new carriers: route_chat.py (176 lines), dungeon.py (373), tavern.py (242), arena_gwap.py (227), grok_burn.py (172). Standing rails: queue/STANDING_RAILS.md (50 lines).

Highest-leverage one-sitting: the tavern report-channel fix in tools/arena_gwap.py (make persona agreement bank real). Why: (a) $0 cash, seat-tokens only (the adapter makes no model calls - selfsteal-builds.md #4); (b) it converts the estate's largest ongoing spend ($15.48/day tavern) from entertainment into routing evidence, which is the estate's named delta (selfsteal-builds.md #7: "routes on MEASURED capability from real asks with chain-verified receipts"); (c) it closes a load-bearing gate failure in the same motion (a GWAP_BANKED marker at agreement 0.0 is the estate's own version of "winnable while ignoring the named mechanic"); (d) it is the build receipt's own named next edge ("tavern's 0.0-report defect is the known edge to fix first").

Mechanism sketch (one sitting): the tavern report payload for each persona must come from rows that carry the actor - either the carrier emits per-persona outcome rows (CONFIRM/VOID of declared [ACT: ...] intents, the dungeon.py shape) or the adapter maps the judge's per-round persona rows as the report channel with the persona as actor. Given the asymmetry note ("the tavern report channel only fills from judge/verdict rows that carry no actor"), the sitting is: add per-persona CONFIRM/VOID emission to the tavern carrier's turn loop (or teach the adapter the tavern row shape). Whichever, one seat, one sitting, no model calls.

Falsifier: after the fix, a fresh tavern run banks personas at nonzero agreement AND spot-checking 3 banked rows shows each report row quotes a [ACT: ...] the persona actually declared in that run's transcript (the adapter never invents a confirmation); if agreement stays 0.0 on a fresh run, the diagnosis (empty report channel) was wrong and the defect is upstream in the carrier's emission.

The one ticket to drop: the trait-layer wiring ticket (wire st.sb + fix the def scoping in the vision branch, games-audit.md decision ledger item b). Why drop: combat does not exist (rollStatBlock is display-only; hp never consumed; snakes kill on touch - games-audit.md section 4), the trait layer is provably inert (st.sb undefined after loadLevel) and would throw if wired (ReferenceError: def is not defined - checks 4). Wiring traits into an engine with no combat loop is polish on wallpaper; the incident_dungeon's own law is "bogus fields look alive" (kept DISPUTED-AND-KEPT). Drop it until a combat loop consumes hp/ac; then the scoping fix becomes real work with a consumer.

Does the "winnable while ignoring the named mechanic" indictment generalize to the estate's gates? Yes:
- The DD levels: "Gate ALL PASS" was solvability only; no gate requires the signature mechanic to be load-bearing (games-audit.md section 1).
- The estate's gates, same shape:
  - GWAP_BANKED marker passes at agreement 0.0 (tavern) - the gate (banked marker) passes while the named mechanism (measured agreement) is empty.
  - The doubled-key alarm fires on 70.3% of rows (808 alarm lines in memory/attention.md) - the alarm gate "works" while its signal (real duplicate spend) is drowned; the gate is winnable by doing nothing (the noise floor passes for everything).
  - The glm-5.3-prime judgment seat: fires passed as fires (billed $0.22-0.23) while content_chars 1 / finish_reason=length - the "fired" gate passed while the named mechanism (content) was empty; only the substance floor + stage re-ask caught it, after billing.
  - hermes ask gates: 4 poisoned twins needed clean refires - caught, but only by a second gate (quarantine), not the first.
- The generalization: the estate's gates verify LANDING (file exists, call returned ok, marker present), not LOAD-BEARING (the named mechanism actually carried). The fix pattern is uniform: every gate must consume its own signal - a banked row must carry a nonempty report; an alarm must carry a false-positive budget (or unique keys); a judgment fire must pass a substance floor BEFORE billing (the stage A/B re-ask pattern generalized); a level gate must walk the mechanic.
- Counter-evidence (honesty): some gates DO walk their mechanism: the fifty-wide wave-2 protocol byte-checks claims and caught a planted forgery (30 REAL / 11 DRIFTING / 3 FALSE / 6 UNVERIFIABLE - selfsteal-builds.md #6); the drift-patrol catches are real (3 in 3 days); the arena_bench grades dungeon.html rooms as ground truth. So the indictment generalizes to the DISPATCH path (gates that guard bulk-generated artifacts), not to the audit path (the estate's own byte-check instruments). The next 24h should move one dispatch gate into the audit shape.

=== Section 4: the card ===

Rank by leverage per dollar:

Row 1: Fix the tavern GWAP report channel so personas bank real agreement. Landing: tools/arena_gwap.py (report channel actor mapping; possibly tools/tavern.py emission). Cost: seat-tokens, $0 cash. Falsifier: a fresh tavern run still banks 0.0 (diagnosis wrong, defect upstream), or banked report rows quote [ACT] lines absent from that run's transcript (fabricated reports - worse than empty).

Row 2: Migrate tools/tavern.py to mag.route_chat with run-stamped ledger ids and the cast-turn model pick moved off opus-5.5 (sonnet-5.5 class; judge stays opus or moves to haiku). Landing: tools/tavern.py + configs/providers.yaml (lane pick); mark the debt row in queue/STANDING_RAILS.md. Cost: seat-tokens to build; saves cash (tavern is $15.48/day, opus casts are the bulk). Falsifier: two consecutive post-migration sessions on an unchanged scenario JSON fail to fire the brawl at pressure 1 (cadence calibration breaks under the new cast model) - roll the pick back; also if the run-stamped ids still produce doubled-key alarms above noise, the stamp is wrong.

Hmm wait - should row 2 (the turn-ingestion fix) come before row 1? Leverage per dollar: row 1 is $0 and unlocks measurement; row 2 saves dollars but costs a sitting and risks calibration. Row 2's cash savings: if casts move opus→sonnet, tavern cost could drop from ~$1/session to ~$0.3-0.5/session - maybe $10/day saved while running. Over 24h that's meaningful but the estate's total is $63 over 3 days. Honestly the measurement unlock (row 1) has more leverage per dollar ($0 cost, makes $15/day measurable + closes a gate indictment). And the transcript-quality fix... also seat-tokens. Hmm.

Ranking by leverage per dollar, with dollar-savings as the denominator's "dollar": row 3 (PvP dungeon session) costs ~$0.05 cash and banks the intel's core claim as evidence - that's enormous leverage per dollar but small absolute. Row 1 costs $0 and protects/converts $15.48/day of spend. I'll rank: 1) report-channel fix ($0, converts the biggest line into signal), 2) turn-ingestion/structured-output fix ($0-ish, makes the signal and the play real; three personas leaked in one live run), 3) PvP dungeon session ($0.05 cash, banks PvP-as-engine), 4) tavern→route_chat migration + model pick + id stamps (saves the cash, enforces the rails law), 5) mechanic-load-bearing gate for dispatched levels (seat-tokens, closes the generalized indictment at the dispatch door).

Hmm, but is the cadence template port (PODCAST_STRUCTURE_spec cadence skeleton into dungeon.py per-scene prompt templates) more valuable than the level gate? The cadence port's falsifier: a cap cut landing mid-combat as fade-to-black instead of a rolled hard cut. But the cadence layer is UNVERIFIED-PATH (no transcripts) - the intel row 3 says cadence mining is owed, not banked. Building cadence templates off unverified intel risks phantom citations. The level gate is byte-grounded. I'll keep the level gate at #5 and note the cadence port waits on transcript bytes (a condition in section 2).

Also the worldline re-render (owed since 09-07, a command): it's cheap and it's the estate's staleness discipline. But max 5 rows. I'll leave it out of the card and mention it in section 3 as a "keep, it's a command, not a sitting" note. Actually, the contract says items must be one-sitting sized - a re-render command qualifies. But leverage per dollar vs the level gate? The level gate closes a systemic indictment; the re-render fixes one stale page. Level gate wins.

Row details:

Row 1: action: teach tools/arena_gwap.py's tavern path to fill persona report rows (map the carrier's per-persona turn outcomes / judge rows with actor, or add per-persona CONFIRM/VOID emission in tools/tavern.py's turn loop, dungeon.py shape). Landing: tools/arena_gwap.py (+ tools/tavern.py emission if needed). Cost: seat-tokens. Falsifier: fresh run still banks 0.0; or banked rows quote [ACT] lines not in the transcript (fabrication).

Row 2: action: structured turn contract in tools/tavern.py (single JSON {"line","act"}, meta-marker detector, void-and-one-refire, voice check against the requested persona). Landing: tools/tavern.py. Cost: seat-tokens + ~$1 refire cash. Falsifier: two fresh runs with zero leaked drafting notes and zero judge-flagged misattribution; if instead the fix silences personas (turn voids pile up, rounds shrink), it killed the play to save the transcript - fail.

Row 3: action: one PvP dungeon session - two funded seats with opposing approaches to the same scroll (Greta-vs-Maud shape per the intel row 1 steal), verify the contested scroll still lands GWAP_BANKED. Landing: a new scenario JSON in the playground plan dir + watch/inbox/playground/dnd0_<stamp>/ (run dir with DONE). Cost: cash ~$0.05 (dnd0 sessions ran $0.02-0.07). Falsifier: the contested scroll ends the scene unaudited (conflict broke audit cooperation) - then PvP-as-engine is wrong for this carrier and the register stays theater.

Row 4: action: migrate tools/tavern.py onto mag.route_chat (the registered one-carrier-per-sitting debt), run-stamp the ledger ids, move cast turns off opus-5.5 (sonnet-5.5 class via configs/providers.yaml pick). Landing: tools/tavern.py + configs/providers.yaml + queue/STANDING_RAILS.md debt row. Cost: seat-tokens; saves cash (tavern $15.48/day, opus 72% of all-time dollars at 9.9 KB/$ vs sonnet 33.9). Falsifier: post-migration sessions on an unchanged scenario JSON stop firing the brawl at pressure 1 (calibration breaks) - roll back the pick; or run-stamped ids still trip the doubled-key alarm above noise - the stamp is wrong.

Row 5: action: the mechanic-load-bearing gate - a checker that walks each dispatched level's win paths (the audit's Node BFS) and refuses pack fold unless a signature tile (k/p/b/s/x) appears on every... hmm, "on the win path" - at least one signature tile ON a winning path? The audit says "no gate requires the signature mechanic to be load-bearing". The gate: a level passes only if EVERY minimal winning path crosses at least one signature tile (so the mechanic cannot be bypassed). Landing: dashboard/static/games/ (a gate_check.js next to ruins_go_engine.js) or tools/; wired into the dispatch path (the fold step). Cost: seat-tokens. Falsifier: run it on the standing 31-33-level pack - if it flags nearly everything (the indictment is total, the fix is level redesign at multi-sitting scale, and the gate row loses its one-sitting status), or if it flags nothing (the audit's BFS was wrong), the gate is miscalibrated; the audit's own run (signature tiles NONE on all 4 DD win paths) predicts it flags at least the 4 DD levels.

=== Section 5 ===

The single observation: a transcript-vs-ledger join on the tavern rows. Concretely: for each playground tavern run dir, count the persona turns in transcript.jsonl and join to the ledger rows carrying that run's window and ids. If the ledger holds more same-(persona,round) rows per run than the transcript holds turns (rows without corresponding turns = intra-run re-bills on already-landed turns), then the 62% re-burn is REAL and ongoing in the live carrier - the verdict flips from routing-change to an immediate freeze of the tavern carrier until ids are stamped and the refire loop is found. Conversely my verdict stands if the join shows one row per turn per run (the collisions are cross-run id reuse, an instrument artifact). This one observation decides freeze vs route because it decides whether the estate's largest live spend line is production or waste. (And note the check files couldn't do this join: "replay-vs-turn ambiguous from the ledger alone; instrument defect = no run stamp in id" - hermes-burn-patterns.check.txt W2.)

That's a strong single flip.

=== Format discipline ===

- No em-dashes ANYWHERE. I must scan my output. Use plain hyphens only. I need to be very careful - my natural style uses em-dashes a lot. Also careful not to introduce them in quotes. I'll write with commas, colons, parentheses.
- Cite receipt file names for claims: watch/inbox/dd_dogfood/mountain-bridge.md, watch/inbox/dd_dogfood/selfsteal-builds.md, watch/inbox/dd_dogfood/games-audit.md, watch/inbox/gala_20260925/dd-selfsteal/lanes/dd-actualplay-intel.json, hermes-burn-patterns.check.txt, hermes-burn-economics.check.txt, hermes-burn-economics.check2.txt, corpus/game_estate/DND_ACTUALPLAY_INTEL_20261003.md, watch/inbox/playground/tavern_20261003T190348Z/play.md, queue/STANDING_RAILS.md, tools/tavern.py, tools/arena_gwap.py, mag/route_chat.py.
- Name what evidence I lack per verdict (conditions).
- One landable deliverable per item.
- Sections in exact order with the exact headers given in the contract: "1. THE BURN LEDGER VERDICT (economics)", etc. I'll use the exact headings.

Let me also double-check some numbers I'll cite:
- 62% claim: the prompt says the ledger says 62 percent; patterns check says W1 38.9% priced + W2 unpriced 665/$14.90; prompt's sibling summary says 723 rows / $39.22 / 62.1%. I'll note the tension honestly: the check file itself refuses to price W2 as waste ("NOT priced as waste: replay-vs-turn ambiguous from the ledger alone"). The defensible waste total is $26.4120 (hermes-burn-economics.check2.txt). Day-1-only span for the twin disease; post-10-02 twin excess $0.1873.
- opus: 426 calls / $45.3564 (economics check) or 447 / $45.65 at 1150 rows (patterns). Use the 1099-row economics numbers and note the ledger accrues.
- sonnet: 297 / $7.4728, ok 245/297 = 82.8%, 63 ids landed, 39 receipts, 33.9 KB/$ (patterns check).
- tavern: 630 rows $15.4776 (both checks agree).
- DND0: 214 rows $0.6937.
- glm-5.3-prime: 5 fires, 3 ids landed, stub pattern (prompt; economics check2 STUB rows $0.2213/$0.2304).
- doubled_key: 758 rows $14.5246 (economics), 809/1150 = 70.3% (patterns), 808 alarm lines in memory/attention.md (check2).
- Wave 2: 30 REAL / 11 DRIFTING / 3 FALSE / 6 UNVERIFIABLE (selfsteal-builds.md #6).
- Games audit: 4 DD levels, signature tiles NONE on all win paths; st.sb undefined; def ReferenceError; oracle_dice zero consumers; 2 orphaned files; riddle-door filename defect.
- Tavern live-fire: run tavern_20261003T190348Z, brawl at round 5, cumulative 16 >= 16 (pressure 1), spend $0.72, 10 rounds cap.
- Drafting leaks: Greta r2 (esc 3 block), Maud r5, Edric r5; misattribution flagged by judge at r2, r3, r4, r5 for Ilse/Greta.
- route_chat: 176 lines, zero importers, failover row 18:49:36Z (selfsteal-builds.md #1).
- STANDING_RAILS debt: "each carrier migrates to route_chat one per sitting" (selfsteal-builds.md #8).
- Intel: PvP core feature WBN/NADDPOD; cadence; transcripts UNVERIFIED-PATH.
- dd-actualplay-intel.json row 1 steal: PvP session, two funded seats, opposing approaches, contested scroll lands GWAP_BANKED; falsifier: unaudited scroll.
- PvP clause: "conflict over approach, never over goals, party-chat law intact" (dd-actualplay-intel.json row 1 claim).
- Arena adapter: dungeon banks 6 actors at agreement 1.0 (dnd0_20261003T180142Z); tavern banks all six at 0.0.

One more consideration for section 1's "which file/law changes": The exact mechanism:
- File: tools/tavern.py (the migration target + id stamp), configs/providers.yaml (the lane/model pick), queue/STANDING_RAILS.md (the debt row marked paid; the law "default to the rails" gains its first importer among the carriers).
- Law: the registered debt in queue/STANDING_RAILS.md ("each carrier migrates to route_chat one per sitting") executes its first play-carrier payment; the model pick for tavern cast turns moves from opus-5.5 to a sonnet-


[TRUNCATED:true footer: finish_reason=length; raw reasoning dump, owed verification]
