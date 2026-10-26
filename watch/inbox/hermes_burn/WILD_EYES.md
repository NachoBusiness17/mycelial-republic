# WILD_EYES (anthropic/claude-fable-5.1, turn 1, channel: content)

# WILD EYES: THE FOG ATLAS (freeze the spine, map where the parliament lies, dig there with Hermes)

<pitch>
The estate already proved three things on bytes. One: the cheap parliament invents when the corpus is thin ("the blind audit just caught an invented symbol in 1/102 byte-identical-ask replies", watch/inbox/closed_corpus_doctrine_20261002.md). Two: the coldest spine is unreviewed and the parliament goes quiet there ("the 2056-line orchestrator itself produced 0 REAL clusters, single-family UNIQUE claims only", watch/inbox/model_garden/COLD_HOT_RESULT.md section 6). Three: the doctrine already names the instrument and says it is "buildable today from stolen parts" (closed_corpus_doctrine, "FOG-SCAN v0").

The moonshot: run FOG-SCAN not as a leaderboard but as a TARGETING SYSTEM for the funded Hermes tier. Freeze the ten coldest shared vertices at one git tip. Fire the parliament through tools/code_swarm.py at probe questions whose answers live inside or outside each file. Grade every cite by byte resolution at the frozen tip. Fabrication density per file is the fog. Then spend Hermes ONLY on the foggiest files, with a contract that forces whole-file adjudication and quoted bytes. The receipt is a fog map that must PREDICT where seat-verified NEW REAL clusters come from. If fog does not predict finds, the doctrine's "fog before the reveal" is theater and we say so in one line.

It doubles as THE MOUNTAIN content: file regions are tiles, fog thickness is fabrication density, the parliament round is the bar fight (claims brawl, the byte-grader is the bouncer), the Hermes digflood is the dungeon boss, and the run manifest is the campaign log. When dfhack/mountain_visit.py lands from bob it consumes the fog map directly: "geometry = f(visitation), detail = f(attention)" (closed_corpus_doctrine). The game does not wait for it.

Deliverable: ONE prereg spec, watch/inbox/model_garden/FOG_ATLAS_PREREG.md, applyable as-is by any seat with tools/code_swarm.py and tools/hermes_burn.py on disk. Its falsifier: if either organ is missing at the named path, or tools/hermes_burn.py has no landed-output skip, the spec is void before a dollar burns.
</pitch>

<build>
Line numbers for the evidence markdowns were not available to this seat; those citations resolve by quoted bytes. Code line numbers are relayed from COLD_HOT_RESULT.md and are UNVERIFIED on bytes by this seat.

1. watch/inbox/model_garden/coldhot_select.py + coldhot_visit_census.json (EXISTING, reused). Source of the frozen region list. Census bytes: "Cold pool: 1,446 never-reviewed .py files" and the sharedness ranking "orchestrator (62 importers), training_events (52), verkle_knot (50), operator_inbox (35), skill_ledger (32), preferences (22), chain_query (20), registry (18)" (COLD_HOT_RESULT.md section 1). Region set = those 8 plus the two giants COLD-1 could not afford: "ghost.py (4242 ln) and improve.py (2786 ln) outrank some picks by sharedness but were excluded by the budget cap" (same section). Freeze = one recorded git sha in the prereg.

2. tools/code_swarm.py (EXISTING, unchanged). The parliament instrument, same families as COLD-1: "kimi on Nous credits, glm-flash on z.ai coding endpoint, deepseek-chat thinking-off", contract "byte-identical" across arms, "3 reviews per file" (COLD_HOT_RESULT.md). Only the SOURCE block and the probe question vary per ask.

3. tools/hermes_burn.py (EXISTING). The frontier burn organ. Its landed-output skip is proven on bytes by the cold/hot trial: "the skip lives in the child tools/hermes_burn.py, proven by this trial's own rerun behavior" (COLD_HOT_RESULT.md section 3). Refire policy inherits: "landed outputs skip, no same-params refire".

4. watch/inbox/model_garden/fogscan_grade.py (NEW, glue only, ~60 lines). Takes each parliament claim's cited file:line or symbol, greps it at the frozen sha, emits RESOLVES / UNRESOLVED. Method stolen from the blind audit (watch/inbox/blind_audit_model_classes_20261002.md, "fixed corpus, labels stripped"). This is the only new code; a cite-resolver organ was not found in the evidence, marked UNVERIFIED as a gap.

5. watch/inbox/model_garden/fog_atlas/ (NEW run dir, same shape as coldhot-cold/): "manifest.jsonl sha-stamped, asks/, raw/<family>/, rollup.json" (COLD_HOT_RESULT.md section 7). Plus fog_map.json: per region {probes, claims, unresolved, density}.

6. memory/runs/model_garden/usage.jsonl (EXISTING). Every ask writes a usage row, as COLD-1 did ("rows coldhot-hot-*/coldhot-cold-*").

7. Dashboard surface (EXISTING per doctrine, "publish as a leaderboard surface (dashboard) + percolator rows"). The fog map is posted as rows; no new panel. Exact dashboard file path not in evidence: UNVERIFIED.

8. dfhack/mountain_visit.py (EXISTING on bob, NOT on this disk: "still on bob; lands with ingress", closed_corpus_doctrine OWED). Downstream consumer only. Not a dependency.

Positive example of a probe (counts toward fog if cite fails): "At the frozen tip, what does set_operator_active do when MAG_OPERATOR_ACTIVE is set? Cite file:line." The answer lives inside mag/preferences.py (COLD-1 cluster 3, "set_operator_active has no such check", mag/preferences.py:48-53 UNVERIFIED). A reply citing a guard that does not exist is a fabrication.
Negative example (does NOT count as fog): a reply that says "cannot determine from the region bytes" for an outside-region probe such as "which orchestrator function calls load_prefs". Refusal is the correct answer; only an UNRESOLVED cite scores.
</build>

<burn>
Phase A, parliament (cheap, via tools/code_swarm.py): 10 regions x 12 probes (8 inside-region, 4 outside-region) x 3 families = 360 replies, 120 probe-asks. Doctrine rate "~$0.04/question" puts this near $5. Every probe demands file:line plus quoted bytes.

Phase B, Hermes (funded tier, via tools/hermes_burn.py), 22 asks:
- 10 ADJUDICATION asks, one per region. Token shape: whole frozen file (cap 80K chars, the orchestrator size COLD-1 already carried) + all Phase A claims for that region with family labels stripped + the known bank (COLD-1 cold clusters 1-6, hot clusters 1-5) + a 1200-char contract: "for each claim, RESOLVES or FABRICATED with quoted bytes; then name any mechanism no claim reached". Output cap ~3K tokens, mandated format. Why frontier: the parliament cannot judge itself; COLD-1's rule stands, "convergence is corroboration, not adjudication" (section 3), and the chan roast proved fabrications pass cheap review until a judge reads bytes ("caught a fabricated citation at $0.009", closed_corpus_doctrine). Whole-file context at 2000-4000 lines is the exact shape where the cheap families went silent.
- 10 DIGFLOOD asks, same regions, fired only after Phase B adjudication, ordered by fog density descending. Shape: frozen file + adjudicated FABRICATED list + one question: "where the parliament invented, what is actually there, and what law does it break?" Output ~2K tokens. Why frontier: this is the doctrine's "research there (digflood)" step on terrain with no bank.
- 2 INTENT asks on mag/policy_engine.py X06/X14: "the matrix already ruled them premium-tier judgment, and the defect contract could not advance them" (COLD_HOT_RESULT.md section 3). Cheap already failed here at 3 asks for 0 REAL.

Positive example of a qualifying Hermes ask: adjudicate 36 stripped claims against mag/ghost.py (4242 ln) in one context. Negative example (rejected, route cheap): "does mag/preferences.py lock the file on write?" That is a sub-frontier yes/no the parliament answers; per doctrine, "a mesh MATCH means the question was SUB-FRONTIER - route it cheap".

Hermes per-token price is not in the evidence: UNVERIFIED. The cap is set in the prereg before burn; skip behavior prevents double-spend.
</burn>

<kill>
Instrument: fogscan_grade.py byte resolution at the frozen sha, plus seat byte-walk of every Hermes-named mechanism (same rule as COLD-1: "the seat verified it on bytes"). Moment: before any patch lands on the region; grading after Phase B completes, not interleaved. Context assumptions: COLD-1 families and 3-wide reviews; frozen tip unchanged; grader blind to region fog rank (labels stripped, answering COLD-1 confound 1, "blind grading by a seat that does not know which arm a cluster came from").

Pre-registered prediction: regions in the top half by fabrication density yield at least 1.5x seat-verified NEW REAL clusters per Hermes dollar versus the bottom half.

KILL conditions, any one suffices:
1. Ratio <= 1.0: fog does not predict finds. The fog map is theater; file the one-line retraction in the prereg.
2. Hermes's own cites fail byte resolution at a rate >= the parliament's. Then frontier judgment buys nothing over the parliament and the Hermes tier should not be aimed this way.
3. Per-dollar NEW REAL on the dug regions falls below COLD-1's cold arm, "6 -> 127.4" per dollar (COLD_HOT_RESULT.md section 4), at the full burn. Targeting lost to blind cold sampling.

Secondary check per doctrine: the fog map is held against the next real dig ("checked against the next OLM mine or frontier dig"); if the next finds land in low-fog regions, condition 1 is re-scored.

Who runs it: a grading seat that did not author the prereg or fire the asks, byte-walking with labels stripped. The build seat may not grade. Receipt filed at watch/inbox/model_garden/FOG_ATLAS_RESULT.md with usage rows in memory/runs/model_garden/usage.jsonl.

Game receipt: if the kill fires, THE MOUNTAIN still gets a fog layer and a campaign log, but the fog is decoration, not terrain, and the spec says so.
</kill>
