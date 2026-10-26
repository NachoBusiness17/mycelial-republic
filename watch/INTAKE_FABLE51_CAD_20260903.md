# INTAKE — Fable 5.1 agentic-CAD vendor demo (@adamdotnew)

**ONE-LINE VERDICT: CALIBRATE — 12/25. Real model, real demo, but it's an ad: vendor claims "most capable we've tested" with no bench, no artifacts, no receipts. File one calibration row (Fable 5.1 = agentic-tool-use frontrunner on our claude lane), wire nothing.**

Date: 2026-09-03 | Evaluator: intake sub-agent (background spawn per Amendment 1)

## ITEM
https://x.com/adamdotnew/status/2095193896687177873 — "Claude Fable 5.1 is a beast at agentic CAD! At Max effort it's the most capable model we've tested so far. Here, inside Adam's harness in Fusion, it rebuilt the SO-101 gripper around the stock servo and mounted a real Pi Camera Module 3 from the official STEP."
Context that changes the read: the author IS the vendor — "Adam | AI CAD Copilot for Hardware Teams" (adam.new). His follow-up tweet is "Try it today at:" with the product card. This is a launch-week product demo, not an independent eval.

## RECEIPTS
Fetched: root post + thread via webReader (root text, follow-up CTA, top reply visible); WebSearch pass 1 (post text + replies + amplification); WebSearch pass 2 (model verification against vendor announcement).

- Root post metrics: 493.3K views, 75 replies, 215 reposts, 3.1K likes, 2K bookmarks. Posted Sep 2, ~16:55 — one day after Anthropic announced Fable 5.1 (Sep 1, 2026, alongside Mythos 5.1, per anthropic.com/claude-fable-and-mythos-5-1; Fable 5.1 GA, Mythos trusted-access only; platform docs note same I/O prices as Fable 5 with cache reads at 1/4 cost).
- Model is REAL and already on our books: our claude lane roster (verified PONG 09-03) lists Fable 5.1 among 11 frontier models. The post is not news to the fleet on model existence — only on claimed capability domain (CAD).
- TOP REPLY — the load-bearing one (@zeropassio, 78 likes): "Please, make this into a bench! ... we want to see how they can build around existing parts (not just making 3d models that don't need to fit into anything)." The community is demanding exactly our receipts-over-claims law: a falsifiable fit-check against real parts, not a demo reel. Vendor has not published one.
- Amplification, not verification: reposted by Y Combinator's account; Max For AI amplified in Chinese ("not just a 3D image that looks like a robot arm"). No community note found. Zero independent reproductions surfaced in two passes.
- Name-collision hazard, flagged: @adamdotnew (CAD vendor) is NOT Adam Crigler (childhood friend, game director, first external human on the game harness, Exhibit Zero). Do not let the corpus conflate the two Adams.

## SCORE
F:2 P:2 C:4 W:2 N:2 = 12/25 — CALIBRATE band

## READ
This is a vendor riding a two-day-old frontier model through a demo-shaped ad funnel — the capability claim ("most capable model we've tested") is their own marketing measured on their own harness with no published bench, so it's Unproven by default, and the top reply says the quiet part: show us parts that must FIT. What survives for us is narrow but real: (1) a third-party, market-facing datum that Fable 5.1 is being picked as the agentic-tool-use frontrunner within 24h of launch, which supports pointing the claude-zai plan door's judgment engine at Fable 5.1 — a lane we already fund and verified; (2) the Anthropic docs line that cache reads cost 1/4 with unchanged I/O prices, which lands directly on our 91%-cache-hit economics when we next route the claude lane; (3) the demo's shape — agent harness driving a professional desktop app against official STEP files as ground truth — rhymes with the phone-driver/CUA surfaces arc but sits in a domain (mechanical CAD, robotics) the fleet does not run, so there is no bay for it. Placement failure is the finding: strongest-at-a-domain-we-don't-run = a routing note, not a build.

## TRI-STATE
- Fable 5.1 exists, GA since Sep 1, 2026 — SUPPORTED (Anthropic announcement + platform docs + our own claude-lane roster PONG).
- "Most capable model we've tested at agentic CAD" — UNPROVEN (vendor self-assessment, own harness, no published eval, no bench; the top reply demands exactly this receipt).
- Demo happened as shown (gripper rebuilt around stock servo, Pi Cam 3 mounted from official STEP) — UNPROVEN (demo video is a record but not a falsifiable one; no STEP diffs, no reproducible artifact).
- Market signal (YC repost, 493K views, 2K bookmarks) — SUPPORTED as attention; DISPUTED as verification (amplification is not replication; no community note either way).
- Adam Crigler connection — DISPUTED/none; different person, corpus hazard flagged.

## VERDICT
CALIBRATE — no wire. File one calibration row: Fable 5.1 = the agentic-frontrunner claim circulating in vendor demos; keep it judgment-only on the claude lane (cheapest-lane law holds — "at Max effort" is max premium burn, never bulk). Do not touch CAD, do not sign up for adam.new, do not spend operator time on it.

## ROUTE (no wire)
1. claude-lane note only: when the plan door next picks a judgment engine, Fable 5.1 carries third-party agentic-tool-use hype + the 1/4-price cache-reads docs line — a one-line probe on the already-funded lane (key 1, PONG-verified) settles it. Free, operator-optional.
2. The zeropassio reply is quotable in our own receipts-over-claims doctrine ("even CAD Twitter is asking for the bench") — fold as a citation row, not a task.
3. Guard row: corpus must not conflate @adamdotnew with Adam Crigler (user-adam-crigler memory). Distinct Adams.
4. Per intake Amendment 1, driver may pull this card on cadence; suggested typed room row — `intake.card{slug:"fable51_cad",verdict:"CALIBRATE",score:12,route:"claude-lane.calibration-row+adam-name-collision-guard"}`.
5. No engine, no queue, no salon, no spend.
