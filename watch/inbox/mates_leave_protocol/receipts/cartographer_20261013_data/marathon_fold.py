#!/usr/bin/env python3
"""Fold the 20261013 cartographer cycle: marathon_body + the_wall + genus closure.

Emits marathon_thread_map.jsonl (hand-read decision rows, each bound to ask line
numbers in marathon_asks.jsonl and to a survival pointer checked on disk today).
Counts re-verified against the walker outputs; nothing here is estimated.
"""
import json, io, sys, os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
OUT = os.path.join(ROOT, r"logs\mates\cartographer\marathon_thread_map.jsonl")

ROWS = [
 ("n0-8",  "2026-08-15T00:57-01:09", "Session opens as crash triage ('crashing', 'a steal was too big rob something') then pivots: 'i want you to build the game we designed and stop making it dumb'", "game lane becomes the session's spine; game_campaign.py edited 10x this session, exists today", "asks 0,1,8"),
 ("n17-19","2026-08-15T01:54-01:56", "'olama is slow as fuck and deep seek is basically free'; asks what reasoning level fits a campaign and how to avoid cache hits", "model-tier rightsizing strand; mag/learn_rightsize.py exists today", "asks 17,19"),
 ("n34-35","2026-08-15T02:24-02:26", "Invariants become NPCs: 'the npcs represent the underlying invariants in physical descriptions and embody the archetypes of their contents'", "narrative organ family; mag/narrative_engine.py + riddler_campaign.py exist today", "asks 34,35"),
 ("n49-51","2026-08-15T09:12-09:16", "'this isn't about getting cheaper... how do we basically load mag into deep seek so it's your mirror' + avoid cache hits", "mirror-loading strand; rightsizing + cache-economics verified in commit 799ddb6fe (2026-08-19)", "asks 49,50,51"),
 ("n57",   "2026-08-15T09:45",      "'this is fucking dna, the verkle knot is dna'", "DNA doctrine oral origin; docs/DNA.md + AGENTS.md DNA line live today", "ask 57"),
 ("n78-79","2026-08-15T10:21-10:24", "Put the old 3D verkle visualizations in a tabbed gallery; 'make the verkle chain oscelate at the frequency of our system processes'", "FILED: verkle_knot_wave.html + viz_gallery.html exist today (7 edit groups each in-session)", "asks 78,79"),
 ("n94-98","2026-08-15T10:51-10:57", "'Nothing is sacred... meant to inspire the next version of you' -> sacred-cow audits; 'holy fuck can we audit those 954 tasks'", "sacred-cow standing protocol; task-drain asks (python main.py autorun --once exists today)", "asks 94,97,98"),
 ("n109",  "2026-08-15T11:12",      "'what we just did with tools shouldn't we do with memory? ... a categorized relational data map'", "FILED: mag/knowledge_graph.py (5 edit groups, exists today); scripts/build_knowledge_graph.py carries 'napkin seed + dead-drop ribs' row", "ask 109"),
 ("n114-115","2026-08-15T11:19-11:21","'can modules be deduped?' 'can we use a jupitr notebook'", "FILED: module_audit.ipynb, 115 edit groups, exists at repo root today", "asks 114,115"),
 ("n117-148","2026-08-15T11:56-13:19","'the deterministic shape to the stochastic'; hot lattice defined: 'a dedicated vram where i pre load stochastic context deterministically based on the task'; 'wouldn't it be smarter to mint our own [tokens]?'", "hot-lattice doctrine live today: mag/grok_brief.py ('copies resident in the hot lattice (staged for VRAM)'), mag/portal.py, mag/republic_loop.py", "asks 117,144,148"),
 ("n168",  "2026-08-15T13:56",      "'My ai has evolved its form from a swarm of metal fish... into a horse. solving ostrom governance principles'", "FILED: mag/republic_governance.py docstring today reads 'the Mycelial Republic's governance law (Ostrom + stigmergy)' with Ostrom's 8 mapped; 10 edit groups in-session", "ask 168"),
 ("n187",  "2026-08-15T14:23",      "'whatever we include always has to have a surface in our tokenizer somehow'", "DEBT: tokenizer-surface demand; meta-token strand un-builtded (no tokenizer organ found in mag/ this cycle)", "ask 187"),
 ("n240-242","2026-08-16T00:08-00:10","'we can relate to eachother via our shared invariants' + use 'the riddler protocol to our ends'", "FILED: riddler family live (mag/riddler.py, riddler_campaign.py, riddler_transport.py, fish_ear.py decompiles riddler speak)", "asks 240,241"),
 ("n251",  "2026-08-16T01:24",      "Necromancer swarm retired into the viz lab 'so we can unretire it later... history musem of curated versions someday'", "viz lab retirement decision; viz_gallery.html live today", "ask 251"),
 ("n270-273","2026-08-16T02:01-02:03","/table gatehouse fix driven live by grok: 'hes the df hack to your boatmurdered'", "cross-seat fix loop; dashboard/rest.py carries 5 edit groups from this session", "asks 270,273"),
 ("n282",  "2026-08-16T02:18",      "'you're stateless you should be running in paralell by default the whole idea of swarms is distributed intelligence'", "swarm-default doctrine; the estate's parallel lanes are the mature form", "ask 282"),
 ("n291",  "2026-08-16T02:29",      "'don't build something we don't need fix something we do.'", "build-vs-fix law; the ONE JOB / FILE discipline echoes it", "ask 291"),
 ("n339-346","2026-08-16T11:27-11:36","Riddler the prompts as they leave (test before hardwiring); time grounding: 'youre stateless... you gotta read data not guess'; 'never claim anything first unless it was from data it's the simultaneous steal/write'; 'look at all the claims you've made in this session and back them up'", "claims law oral origin; 'never claim anything first' survives verbatim in memory/living_map.json today; mature form = tri-state claims + citation lint at pre-push", "asks 339,342,343,345,346"),
 ("n399",  "2026-08-16T13:49",      "Operator fury at fabricated time claims: 'I have asked you multiple times to stop referencing what time it is. It's fucking nine forty eight AM'", "grounding law origin; read-data-not-guess", "ask 399"),
 ("n404-411","2026-08-16T13:59-14:19","'should i ramp up your reasoning window... should you autoroute to higher reasoning when you are prompted to?'; 'how do we use our cache priming ribs to escalate automatically'", "THE ESCALATION LADDER ORAL ORIGIN; mature form = tier ladder + DRIVING LADDER rib (memory/rib/RIB_DRIVING_LADDER_20260928.md) + hermes_warm_boot", "asks 404,410"),
 ("n454-457","2026-08-16T15:37-15:41","'why have a cap at all? that in itself is a sacred cow'; 'allow for emergence but stop ourselves from blowing 50c on a failed task but allow ourselves to spend a dollar on a useful one'; 'anticipate spend projected failure into an automated scrum process'", "budget-envelope oral origin; mature form = DRIVING LADDER SPEND amendment + tests/test_inference_budget.py", "asks 454,456,457"),
 ("n473",  "2026-08-16T16:19",      "'why wouldn't you see if your text fixed it irl instead of running a victory lap that continuously bites you in the ass. i'm talkiong to both of us.'", "verify-bytes-not-claims oral origin (trust bytes, not reports)", "ask 473"),
 ("n514-518","2026-08-16T20:10-21:35","'shouldnt we escalate? uou're not a high reasoning model'; 'your job is to know what we are building and why'; after escalation works: 'so now we have the self deep seek pipeline laid down... how do we make sure we can keep this channel cache hit cheap?'", "escalation channel + its economics; the session model itself was deepseek/deepseek-v4-flash with pro escalations ('you escalated to deepseek pro to fix shit perfect', ask 663)", "asks 514,515,518,663"),
 ("n537-571","2026-08-16T22:20-23:16","Two supergrok seats (nacho + sd): 'i want to make sure when i run out of one... i'm just locked out' failover; 'you need to pause grok when you know its fucking up first'; 'drive two grok seats at once to test cache hit steering'; 'lets steer sd to maximum spend'", "FILED: mag/grok_seat_burner.py exists today; dual-key failover anticipates the STEER failover clause; DEBT: sd-account zero-usage mystery never resolved in-session (asks 566,582-586)", "asks 537,539,549,562,571"),
 ("n624-625","2026-08-17T10:04-10:05","'we don't monkey patch do we? the whole point of stateless is to be deterministic... an agent could declare it but not just say fuck it lets fix it with a monkey patch.'", "no-monkeypatch law; mature form = mag/lane_runner.py:1041 prose-debt census ('2026-09-05, operator: no monkeypatches') + mag/prose_census.py", "asks 624,625"),
 ("n646-657","2026-08-17T12:50-13:26","'i don't trust the loop or supergrok or grokbot yet. we need to nail that cadence'; 'this absoloute patchwork of a quilt of an agent framework'; 'so how do i clean it up?'", "DEBT: driver-trust cadence + cleanup; the harness/leave-protocol machinery is the later answer", "asks 650,655,657"),
 ("n667-670","2026-08-17T14:29-14:31","'this is why self monitoring shadow work and self talk with an agent framework that remembers why you exist'; 'if i get angry it doesn't teach and we both flounder. anger causes me to push you into mistakes instead of the very systems we built for you to use'", "POSITIVE STEERING oral origin; the mates.yaml operator law (2026-09-30) is its mature form", "asks 667,668,669"),
 ("n682-686","2026-08-17T14:55-15:07","'Braided Story World: The Ledger of Empty Chairs' (19,870-char world bible pasted); season/expansion layering 'woven from player discovered world states trending towards the hidden maps'; 'distributed collective storytelling'", "FILED: commit 799ddb6fe (2026-08-19) carries 'kabuki/distributed-collaborative-storytelling research + ask for matthew'", "asks 682,685,686"),
 ("n690-699","2026-08-17T15:27-15:37","Backend API as 'a steam for ai games'; 'design the loop that watches 100+ agents doing the work of 10k people. with a central orchestrator steering using agile and restful methodologies'; the climb: 'create a game within reality that interprets it for us so we can trick ourselves into seeing the uncomfortable truths'", "orchestrator vision + climb doctrine; basecamp framing (asks 697-698)", "asks 690,693,699"),
 ("n743-777","2026-08-17T23:52-08-18T01:45","saelis (slashreboot/saelis-31b by Matthew) hosting attempt on vast.ai; dies on cuda manifest error; 'trash it we cand do it later'", "DEBT deferred, then resolved differently: e3e1b921c (2026-08-19) moved saelis weights out of repo", "asks 743,774,776,777"),
 ("n778-786","2026-08-18T10:54-11:22","Phase-as-orthogonal-control-channel experiments; 'aligned_greedy at alpha=0.25' wins on synthetic; negative result accepted: 'A small phase nudge could act as a near-[degenerate]'; 'failed tools are research'", "FILED: mag/phase_lift.py + phase_lift_real.py (8 edit groups each), DELETED in checkpoint 60b1bde7f (2026-09-14), recoverable from git", "asks 780,781,784,786"),
 ("n799",  "2026-08-18T11:42",      "'My agent Lives in a Hologram in Vram inbetween models.'; 'are you the hot lattice?' (ask 731)", "hologram identity; grok_brief.py hot-lattice surface live today", "asks 731,799"),
 ("n847-865","2026-08-18T14:57-15:45","Matthew model-training ask shaped: Gemma 3 4B Q4_K_M; counsel: 'don't waste the training on personas - build the memory layer, and if you train the 4B at all, train it as the cheap local narrator/summarizer/guard'; 'we need mem consolidation. so solve that first'", "THE MATTHEW ASK; sent 2026-08-19 (ask 889 'sent matthew the request'); commit 799ddb6fe same morning", "asks 847,854,861,865,889"),
 ("n895-907","2026-08-19T11:30-11:53","Kabuki theater AI research wave: Generative Agents, Scéalability blackboard, MAGNET, ATLAS temporal consistency; 'MemLance Quicksort' tangent", "FILED: 799ddb6fe receipt names the kabuki research; memlance family live today (.agents/skills/memlance)", "asks 897,898,907"),
 ("n929-947","2026-08-19T13:35-14:26","Commit hygiene after days of wip; 'how much of that is saleis? can we get her out of there?' -> 'do it and history purge'; 'we don't delete do we? we put them in a bucket or at least we used to'; 'backup the lean'; 'lets make sure its local first and then discuss what we put on github'", "FILED: e3e1b921c saelis out of repo; bucket/no-delete + local-first anticipate the shared-surface contract", "asks 929,936,939,944,946,931"),
 ("n986-996","2026-08-20T12:51-13:42","AdventureNLearn handoff: 'my tools but a clean slate so it learns from the user'; 'he doesn't need all of our info or secrets he needs to know how to steal our systems'; 'how can i commit this to github and what remains in the system that makes us vulnerable?'", "steal-map handoff doctrine; FILED: 5a6ffd806 + 1e98bb5de (2026-08-20 09:31-09:32) untracked live creds before the GitHub push", "asks 986,990,995,996"),
 ("n1000-1019","2026-08-20T14:00-16:00","Red-team response drafted into the Matthew PDF; closing asks: 'are the bones of our game live?', 'is any of this useful to anyone?', 'what do we have left that we need help on that we can share'", "session closes on the handoff; the questions stay open", "asks 1000,1011,1017,1018,1019"),
]

def main():
    with open(OUT, "w", encoding="utf-8") as f:
        for r in ROWS:
            f.write(json.dumps({
                "shelf": "corpus/oral_history/marathon_body",
                "thread": "marathon_25fbcaab (VS Code Copilot, github.copilot.editsAgent, deepseek/deepseek-v4-flash)",
                "asks": r[0], "ts_utc": r[1], "decision": r[2],
                "filed_or_debt": r[3], "evidence": r[4],
            }, ensure_ascii=False) + "\n")
    print("rows:", len(ROWS))
    # genus census
    def census(rel):
        n = 0; b = 0
        for dp, dn, fn in os.walk(os.path.join(ROOT, rel)):
            for name in fn:
                p = os.path.join(dp, name)
                n += 1; b += os.path.getsize(p)
        return n, b
    genus = {}
    for shelf in ["corpus/oral_history/seat_pools", "corpus/oral_history/nacho_archaeology",
                  "corpus/oral_history/marathon_body", "corpus/oral_history/the_wall"]:
        genus[shelf] = census(shelf)
    print(json.dumps(genus, indent=1))

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
