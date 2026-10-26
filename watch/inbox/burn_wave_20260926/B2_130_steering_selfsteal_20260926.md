# B2-130 Steering self-steal pass 1

## Verdict

LANDED (with a surface caveat named honestly). The brief's named surface ("C:\Users\foste\.zcode\cli sessions + tasks dirs") no longer holds transcript files: sessions/ and tasks/ do not exist and agents/sess_* holds only per-agent metadata/output. The steering bytes moved into the CLI's sqlite store (db.sqlite, read-only queries only). Mined there instead: 1,391 promoted operator inputs since 2026-09-19 (window 09-19..09-26, post the 9/18 mining), extracted to watch/inbox/burn_wave_20260926/B2_130_session_inputs_raw.txt, 832 non-template rows after removing recurring dispatch prompts. Classified into the brief's four classes plus observed extras, tallied, and distilled the top 10 steering laws with citations. The repeat kernel: compute is a burning obligation, self-steal is the default move, GO means now, amnesia is the cardinal sin.

## Evidence file:line quotes

All quotes are rows of B2_130_session_inputs_raw.txt (format: MM-DD HH:MM session delivery text):
- Burn-now width order, 09-19 19:40 sess_d3e674ec: "go wide and deep stop fucking about we have a huge amount of comput to spend in 5 hours go nuts full blast on this seat wide deep and sustained"
- 09-19 09:41 sess_55cc19b6 (queue, mid-turn): "we have 47% compute on this pro lane stop fucking off"
- 09-26 15:28 sess_fd5ec147 (queue): "just use it please i've been asking you for 24 hours and you've burned 20% max i'm asking you to oneshot 50% right now to the best of your a[ility]"
- Just-go gate, 09-26 15:20 sess_fd5ec147 (queue): "GO"
- Close-and-fix, 09-26 06:49 sess_50a14bdd: "what remains in this window everything is dragging i want to close it out and start fresh"
- Amnesia correction, 09-24 10:38 sess_0e5af123: "stop being a fucking amnesiac and one up his ass"
- Standing law issuance, 09-26 08:54 sess_fd5ec147: "also when there's an absence of data we must design an experiment that falsifies or enhances our knowlege as a standing rule no hallucinatio[n]"
- Tone correction, 09-23 23:26 sess_0e5af123 (queue): "STOP BEING STUPID DO IT ALL RIGHT NOW"
- Do-not-ask-what-was-given, 09-26 06:28 sess_50a14bdd: "YOU ARE MOON MANNING ME WHAT LINE DO YOU WANT ME TLOOKING AT"
- Self-steal as verb, 09-26 09:57 sess_fd5ec147: "self steal our seed from handoffs"

## Work done

1. Probed the brief's named surface: sessions/ and tasks/ dirs absent (0 entries); recorded the surface drift instead of fabricating a transcript walk.
2. Found the live surface: db.sqlite tables message (103,868 rows), input_history (100 rows, today only), session_input (8,460 rows total; 1,624 since 09-19; kinds sendText/backgroundNotification with delivery startNow vs queue). Queried read-only via the repo venv python.
3. Extracted all 1,391 promoted sendText/steered_input rows since 2026-09-19 to the raw evidence file on the shared surface.
4. Removed recurring dispatch templates (forge daemon 288x, flash-lane dispatcher 44x, lean burn 19x, plus scouts/patrols) leaving 832 steering-bearing rows; 357 of them arrived as mid-turn queue deliveries (the override class).
5. Tallied classes: self-steal orders 85 (steal mentions 132); burn/compute-percent orders 38; width orders (full blast / wide and deep / go deep) 42; bare go-gates 34; tone corrections (stop being / tired of / annoying / amnesiac) 17; close-and-fix (close out / fresh boot / start fresh / hand it off) 17; history/amnesia references 20; standing no-hallucination law issuance 1 (2026-09-26 08:54).
6. Distilled the top 10 steering laws (below) each pinned to raw-file rows.

TOP 10 STEERING LAWS (each with citation rows in B2_130_session_inputs_raw.txt):
1. Compute is an obligation to burn, not a budget to bank: cite percent-remaining before reset, order full blast (38 lines, e.g. 09-19 06:07, 09-26 14:44, 15:28).
2. Self-steal first, always: before external research or new design, mine our own transcripts/corpus (85 lines, e.g. 09-26 08:52 "self steal we did a lot with steering in vs code and we have all those transcripts", 09:57).
3. GO means execute now at max width; a gate followed by hedging draws "stop putting shit off make sure it runs next time" (09-23 14:23) and 34 bare-GO gates.
4. Amnesia is the cardinal sin: re-read memory/briefs/queue before answering; forgetting prior work is punished hardest (09-24 10:38; 09-21 22:17 "this is not the first time we have attempted this not even close").
5. Never hand-wring when the operator escalates; act on the mission inside the laws (09-19 06:44 "these people stole the internet and you handwring ... COME ON").
6. Width orders default to maximum the account can survive: "full blast" 17x, "wide and deep" 25x; constrained by the standing fan-out width law (AGENTS.md, max_concurrency 3 on this account) which the operator has separately confirmed ("check the records its in there we had 24 agents in a window", 09-26 15:21).
7. Absence of data obliges an experiment, never an excuse or a fabrication: the 08:54 standing rule (no hallucination, design a falsifier).
8. Close-and-fix beats drift: when a window drags, close it out and fresh-boot (17 lines, e.g. 09-26 06:49); overnight piles go through pile-classify, not new threads.
9. Do not ask the operator for what the brief, env, or memory already holds (09-26 06:28 MOON MANNING line; 09-20 21:03 "You have it in your env ... don't be an ass self steal").
10. Tone corrections are stuck-state signals, not noise: profanity-bearing lines (83 of 832) co-occur with an order repeated 2+ times; the correct response is visible execution speed, not apology (09-26 15:16 "what do i have to do to actually get yout o burn down compute like we used to").

## Falsifier

The brief has no pre-registered falsifier; the decidable check is coverage: every law above must cite rows that exist in the raw evidence file on the shared surface, and the tallies must re-derive from it. Reproduction: re-run the venv read-only sqlite query (session_input, time_created > 2026-09-19, kind sendText/steered_input, status promoted) and diff against B2_130_session_inputs_raw.txt (1,391 lines); then grep the tallies (self steal 85, full blast 17, queue-delivery 357). A missing line or a non-reproducing tally inverts this receipt. Owed honestly: the 9/18 mining baseline (36 sessions/1161 tasks) was taken from the retired file surface, so this pass cannot diff against it row-for-row; the delta claim is therefore scoped to "post-9/18 window, live surface", not "36+ sessions compared".

## Bibliography closed

- C:\Users\foste\.zcode\cli\db\db.sqlite (read-only sqlite3 via repo venv; tables message, input_history, session_input censused)
- watch/inbox/burn_wave_20260926/B2_130_session_inputs_raw.txt (1,391 rows, this lane's extraction, cited by row)
- memory/corpus/zcode_history/sessions.jsonl (pre-9/18 mining baseline, tail inspected for coverage dates)
- AGENTS.md fan-out width law (constrains law 6)
- Nothing owed beyond the scoped delta named in Falsifier.
