"""One-shot builder for watch/inbox/task_shapes_20260109/task_shapes.jsonl.

TASK-SHAPE CENSUS lane, 2026-10-08. Sources: the two banked 2026-10-08
ecosystem receipts, the live Hermes user-stories gallery, the OpenClaw
showcase, and the awesome-openclaw-usecases list. Every row cites banked
bytes or a live URL. Run with the repo venv interpreter.
"""
import json
from collections import Counter

GALLERY = "https://hermes-agent.nousresearch.com/docs/user-stories"
MINE = "watch/inbox/HERMES_ECOSYSTEM_MINING_20261008.md"
DROP = "watch/inbox/LINK_DROP_HERMES_ECOSYSTEM_20261008.md"
SHOWCASE = "https://openclaw.ai/showcase"
AWESOME = "https://github.com/hesamsheikh/awesome-openclaw-usecases"

S = []


def add(sid, name, verb, inp, out, cadence, evidence, fits, fits_note=""):
    S.append({
        "shape_id": sid,
        "plain_name": name,
        "verb_object": verb,
        "input": inp,
        "output": out,
        "cadence": cadence,
        "evidence": evidence,
        "fits_our_17_animals": fits,
        "fits_note": fits_note,
    })


# ---- banked receipts (2026-10-08 class), cross-cited on the live gallery ----
add("ts001-memory-graph-compile", "Keep a memory that decays and promotes itself",
    "compile + demote memory into a temporal graph",
    "all agent activity, notes, conversations",
    "a queryable memory graph where stale facts demote, never dump into the prompt",
    "watch",
    [MINE + " (lauratom ~22k-line kernel, SQLite FTS5 typed nodes/edges, decay/promotion/supersession)",
     MINE + " (G4 typed-node layer row)",
     DROP + " (Synapse temporal knowledge graph with deliberate forgetting)",
     GALLERY + " (lauratom L1 Hindsight / L2 Graphiti / L3 MemPalace; Synapse)"],
    ["z-ai/glm-5.3-prime", "legality-propagator-v1", "anthropic/claude-haiku-4.5"],
    "graph legs ride the specialized graph animal (legality-water-graph-v1 p 0.9882 in ml3_route_table.json); signal extraction is haiku scut; promotion judgment glm-prime")

add("ts002-shared-memory-vault", "Share one memory vault across every agent I use",
    "share one vault across agents",
    "multiple agents (Claude Code, Codex, Grok, Hermes) writing one store",
    "one shared vault all agents read/write, fixing agent amnesia",
    "watch",
    [MINE + " (fxa3bah: ONE Obsidian vault + one local brain shared by four agents)",
     GALLERY + " (fxa3bah shared Obsidian memory across 4 agents)"],
    ["anthropic/claude-haiku-4.5", "z-ai/glm-5.3-prime"],
    "the shared-surface law already banks this shape; animals only do reconcile judgments, storage is estate machinery")

add("ts003-search-huge-document", "Ask questions against a 3,000 page manual",
    "index + query a huge local document",
    "one very large PDF/manual (3,799 pages)",
    "FTS5 index plus grounded answers without blowing context",
    "one-shot",
    [MINE + " (Barnet1123 parsed a 3,799-page AMD manual with SQLite FTS5 because vectors blew the context window)",
     GALLERY + " (u/Barnet1123 local parsing of AMD manual)"],
    ["z-ai/glm-5.3-prime", "x-ai/grok-4.7"],
    "retrieval is script-tier FTS5 (corpus_fts convergence); the answer leg is prime judgment")

add("ts004-overnight-dream-cycle", "Let the agent think while I sleep",
    "run an overnight dream cycle",
    "the day's accumulated state, notes, unresolved items",
    "a morning digest of overnight consolidation plus filed work",
    "cron",
    [MINE + " (German startup profile dreams at night)",
     GALLERY + " (u/HolmeBengt 28 cron jobs + 3am dreaming memory job)"],
    ["anthropic/claude-fable-5.1", "z-ai/glm-5.3-prime", "anthropic/claude-haiku-4.5"],
    "the estate's own night shape (route table: night 44 rows -> fable, night-judgment -> glm-prime)")

add("ts005-always-on-caged-fleet", "Run a fleet of always-on agents, one per person",
    "run an always-on isolated agent fleet",
    "N employees or roles, each with own data",
    "N isolated agents, own storage and network policy, no cross-bleed",
    "watch",
    [MINE + " (Razorpay 220+ employee agents each in own k8s namespace; Sionic Mac Mini farm)",
     DROP + " (Razorpay and Sionic rows)",
     GALLERY + " (Razorpay Engineering; 12 parallel instances building Hermes itself, Teknium)"],
    ["anthropic/claude-haiku-4.5", "deepseek/deepseek-v4.1-flash"],
    "fleet economics force cheap animals per seat; caging is harness law, not animal choice")

add("ts006-zero-token-cron", "Run a scheduled job that costs zero tokens",
    "run scheduled script without LLM",
    "a script-shaped leg: ledger minting, queue rotation, receipt filing",
    "the job runs, zero LLM calls, zero tokens",
    "cron",
    [MINE + " (kabira121 --script --no-agent mode, no agent loop no LLM call, G1 gap row)",
     GALLERY + " (u/kabira121 zero-token cron mode)"],
    ["NEW: script tier below all 17"],
    "no animal fits by design; the estate's G1 gap row assesses porting this into hermes_247")

add("ts007-two-tier-inbox-watch", "Watch my inbox and only call the model on new mail",
    "watch inbox + summarize new mail",
    "an email or message inbox stream",
    "summaries/drafts only when new items arrive, zero LLM calls when idle",
    "watch",
    [MINE + " (mayuronx two-tier event gate: Tier 1 pure Python, Tier 2 hermes chat only on new mail, G2 gap row)",
     GALLERY + " (mayuronx two-tier email pipeline)"],
    ["anthropic/claude-haiku-4.5", "deepseek/deepseek-v4.1-flash"],
    "gate is script tier; the on-event leg is cheap-animal scut")

add("ts008-install-agent-for-shop", "Have someone set the agent up for a small business",
    "install + configure agent for a nontechnical business",
    "a shop's real workflows (messenger leads, quotes, catalog)",
    "a running installed agent plus ~8,000 scheduled runs",
    "one-shot",
    [MINE + " (French consultant ~EUR 2,700/month installing Hermes for SMBs, ~8,000 scheduled runs; hermes-for-win one-click installer, G5)",
     GALLERY + " (u/pacmanpill installation service; EdwardWason hermes-for-win)"],
    ["z-ai/glm-5.3-prime"],
    "the value is workflow adaptation, one premium planning seat per install")

add("ts009-role-team-by-toolset", "Stand up a dev team of agents gated by permissions",
    "deploy a role team gated by toolset",
    "a role hierarchy (CTO down) plus per-role tool allowlists",
    "an installer that enforces hierarchy by toolset restrictions only",
    "one-shot",
    [MINE + " (9-role dev team installer, authority-by-toolset)",
     GALLERY + " (u/humanth-shashani 9-role dev team)"],
    ["z-ai/glm-5.3-prime", "anthropic/claude-opus-5.5"],
    "schema/planning shapes route glm-prime (schema-design p 0.6947); gating is the allowlist law")

add("ts010-trade-market-bot", "Run a trading bot on live markets",
    "trade a market automatically",
    "price/forecast feeds, a bankroll",
    "positions plus self-written strategy notes",
    "cron",
    [DROP + " (weather-market bot $100 to $216 in 48h; Polymarket across four parallel layers)",
     GALLERY + " (DeRonin_ weather bot hourly scans 3 forecast sources; Polymarket paper-trading autopilot)",
     AWESOME + " (Polymarket paper-trading autopilot with backtesting and daily reports)"],
    ["x-ai/grok-4.7", "z-ai/glm-5.3-prime"],
    "judgment fits animals but real money is operator-gated; GSTD is the estate money lane (NOT-BUILD column)")

# ---- primary gallery (live URL) ----
add("ts011-price-watch-alert", "Watch a price and tell me when it drops",
    "monitor a price feed and alert",
    "a product/market price feed or ETF list",
    "an alert only when a threshold or all-time-low hits",
    "watch",
    [GALLERY + " (u/knowoneknows CheapCharts all-time-low watcher for movies/TV)",
     GALLERY + " (u/SuperALfun morning dividend-ETF summary to Telegram)"],
    ["anthropic/claude-haiku-4.5", "deepseek/deepseek-v4.1-flash"],
    "threshold check is script tier; alert wording is cheap-animal scut")

add("ts012-listing-digest-email", "Email me the 3 best new listings every morning",
    "filter new listings into a daily email",
    "rental or real-estate listing sites",
    "a short daily email of 1-3 filtered listings",
    "cron",
    [GALLERY + " (u/kenmazaika rental listing curation, 8:30am daily email on a $175 Dell)",
     GALLERY + " (u/kenmazaika apartment scouting via dedicated Gmail + daily cron)",
     GALLERY + " (quifago Idealista CLI skill flat under 200.000 EUR)"],
    ["anthropic/claude-haiku-4.5", "z-ai/glm-5.3-prime"],
    "scrape and filter is script tier, the pick judgment is light prime work")

add("ts013-chat-group-digest", "Boil my group chats down to 3 lines",
    "digest busy chat groups",
    "WhatsApp/Telegram/Discord group traffic",
    "a short digest per group (82 messages to 3 lines)",
    "watch",
    [GALLERY + " (u/Godzillaton WhatsApp group digest, 82 messages to 3 lines across 11 construction groups)",
     GALLERY + " (u/Ysqander Reddit crawler delivering posts to Telegram)",
     AWESOME + " (Reddit/YouTube/tech-news digests as daily cron)"],
    ["anthropic/claude-haiku-4.5"],
    "high-volume low-stakes summarization: the tavern-turn lane (haiku p 0.9879) is the exact route-table analogue")

add("ts014-morning-brief", "Give me one brief every morning: mail, calendar, news",
    "digest mail + calendar + feeds into a morning brief",
    "inbox, calendar, feeds since yesterday evening",
    "one short brief delivered to phone/Slack/Telegram",
    "cron",
    [GALLERY + " (Anthony Maio natural-language cron: every weekday 9am summarize my inbox and post to Slack)",
     GALLERY + " (LLMJunky morning Gmail/Calendar rollup skill, multi-account)",
     GALLERY + " (DhruvalGolakiya morning email summary to WhatsApp then todos to Slack)",
     GALLERY + " (m05tr0 k8s daily cybersec + AI briefing)",
     AWESOME + " (custom morning brief via text; family calendar morning briefing)"],
    ["anthropic/claude-haiku-4.5", "z-ai/glm-5.3-prime"],
    "assemble is script tier; the write leg is cheap animal, premium only on request")

add("ts015-draft-replies-in-voice", "Draft replies in my voice and wait for my OK",
    "draft replies in the owner's voice",
    "inbound messages (messenger, WhatsApp, email)",
    "draft replies queued for human approval before send",
    "watch",
    [GALLERY + " (julientalbot974 reads FB Messenger leads every 15 min, drafts replies)",
     GALLERY + " (MarTech AI WhatsApp replies + approval-gated jobs)"],
    ["anthropic/claude-sonnet-5.5", "z-ai/glm-5.3-prime"],
    "style-bearing drafting: sonnet tier; send is effect-broker gated")

add("ts016-forward-to-file", "I forward an email, it lands filed in the wiki",
    "file forwarded mail into the knowledge base",
    "a dedicated update@ inbox staff forward into",
    "structured wiki/Notion pages",
    "watch",
    [GALLERY + " (u/theturtletalks email to wiki filing: staff forward to update@ inbox, agent files into wiki)",
     SHOWCASE + " (@localghost email receipts to a parts list via forwarded inbox)"],
    ["anthropic/claude-haiku-4.5", "deepseek/deepseek-v4.1-flash"],
    "classify-and-file is scut with a light structure judgment")

add("ts017-qc-watch-flag", "Watch the field reports and flag the bad ones",
    "QC-watch incoming work and flag",
    "service tech reports, agent outputs, tickets",
    "flags plus notifications to Telegram/Slack",
    "watch",
    [GALLERY + " (u/andrewtcombs QC monitoring of service tech reports, flags bad reports live, notifies Telegram/Slack)"],
    ["x-ai/grok-4.7", "anthropic/claude-opus-5.5"],
    "adversarial-review class judgment (grok-4.7 p 0.9615 on that route-table shape)")

add("ts018-invoice-from-timesheets", "Turn my timesheets into a draft invoice",
    "draft invoices from time tracking",
    "Harvest/ClickUp time entries",
    "a draft invoice a human reviews and sends",
    "cron",
    [GALLERY + " (@corxntyn invoice drafting from Harvest/ClickUp, human reviews and sends)",
     GALLERY + " (u/xbxz client status reports among scheduled legs)"],
    ["anthropic/claude-sonnet-5.5", "anthropic/claude-haiku-4.5"],
    "structured extraction plus formatted drafting")

add("ts019-books-reconcile", "Keep my books reconciled all month",
    "reconcile books continuously",
    "QuickBooks/bank/Stripe transaction streams",
    "reconciled books, flagged mismatches (cut $18k/yr in accounting fees)",
    "watch",
    [GALLERY + " (jaredclucas accounting automation cut $18k/yr, QuickBooks + Google Workspace for a realtor)",
     GALLERY + " (u/hewi333 Telegram service business: leads to estimates to Stripe to QuickBooks)"],
    ["anthropic/claude-opus-5.5", "z-ai/glm-5.3-prime"],
    "money-adjacent reconciliation is premium judgment with effect gates")

add("ts020-lead-research-score", "Research my prospects and score them nightly",
    "research + score leads on a queue",
    "an account list, LinkedIn/inbox events",
    "researched, scored accounts waiting for one approval (stops on reply)",
    "cron",
    [GALLERY + " (VibeMarketer_ outbound sales queue, researched/scored accounts awaiting Telegram approval, stops on reply)",
     GALLERY + " (u/Forsaken_Coconut3717 daily prospect scraping 50/day)",
     GALLERY + " (leploutos LinkedIn prospecting agents, Lemlist to Slack event handling)",
     GALLERY + " (u/NKB82 IT consultancy CRM outreach and lead vetting)"],
    ["deepseek/deepseek-v4.1-flash", "x-ai/grok-4.7"],
    "the 50-a-day scrape-and-score grind is flash scut; final pick climbs to grok judgment")

add("ts021-competitor-scan", "Scan competitors every week and tell me what changed",
    "scan competitors on a schedule",
    "competitor sites, Search Console, ad libraries",
    "a diff report of what changed plus draft content",
    "cron",
    [GALLERY + " (u/Forsaken_Coconut3717 weekly SEO competitor scan)",
     GALLERY + " (AI Ranking daily SEO loop: Search Console analysis, drafts, publish after approval)",
     SHOWCASE + " (@xz3dev weekly automated SEO analysis)"],
    ["deepseek/deepseek-v4.1-flash", "x-ai/grok-4.7"],
    "diff is script tier; the what-changed-matters judgment climbs")

add("ts022-oncall-bug-tracer", "Trace bugs and open the PR while I sleep",
    "trace bugs + open pull requests on spikes",
    "feedback spikes, traces, logs",
    "opened PRs with root-cause notes",
    "watch",
    [GALLERY + " (u/avishic on-call engineer agent: traces bugs, opens PRs, wakes on feedback spikes)"],
    ["z-ai/glm-5.3-prime", "x-ai/grok-4.7"],
    "code shapes: glm-prime planning leg + grok review judgment (route-table code-analysis is thin/ungated, a gap this census feeds)")

add("ts023-team-code-review", "Review the team's code and triage tickets",
    "review code + triage tickets for a team",
    "PRs, incident notes, tickets from ~50 devs",
    "review comments, incident notes, triaged ticket queue",
    "watch",
    [GALLERY + " (u/how_gauche code review, incident notes, ticket triage for a 50-dev team)"],
    ["x-ai/grok-4.7", "anthropic/claude-opus-5.5"],
    "adversarial-review/descent-leg classes: grok 0.9615, opus 0.9882 on those route-table shapes")

add("ts024-meeting-prep-brief", "Build me a brief before every meeting",
    "research + assemble a meeting prep brief",
    "CRM contacts, accounts, prior threads",
    "an 8-page research brief before the call",
    "one-shot",
    [GALLERY + " (u/jean-jcrx meeting prep brief, 8 pages from self-hosted CRM)"],
    ["anthropic/claude-opus-5.5", "x-ai/grok-4.7"],
    "descent-leg analogue: one premium turn, one landed deliverable")

add("ts025-organize-files-into-system", "Take this pile of files and put it in order",
    "organize a file pile into a system",
    "MP3 library, lab PDFs, receipts, downloads",
    "renamed/structured files filed into folders, Notion, or a parts list",
    "one-shot",
    [GALLERY + " (slowmotionrunner daily workout playlists plus MP3 library rebuild)",
     GALLERY + " (danpeguine bloodwork lab results organized into a Notion database)",
     SHOWCASE + " (@localghost email receipts into a parts list)"],
    ["anthropic/claude-haiku-4.5", "meta/llama-3.2-11b-vision-instruct"],
    "rule application is scut; scans and screenshots ride the vision animal")

add("ts026-voice-notes-to-docs", "Turn my rambling voice notes into real documents",
    "transcribe + structure voice notes",
    "Telegram voice notes or voice memos",
    "structured documents (reports, specs)",
    "one-shot",
    [GALLERY + " (u/kenmazaika voice notes to structured docs from a Telegram topic)",
     SHOWCASE + " (@LLMJunky mobile orchestration of dev machine via voice memos)"],
    ["NEW: no audio-in animal"],
    "the 17 animals are text plus one vision model; STT is tool-side (whisper class), no route-table animal exists")

add("ts027-sensor-watch-alert", "Watch the smoker all night and wake me if it slips",
    "watch a hardware sensor and alert",
    "a device API stream (FireBoard temps)",
    "an alert only when the temperature leaves the band",
    "watch",
    [GALLERY + " (u/Tasty-Property-434 pellet-smoker night watchman over the FireBoard API)"],
    ["anthropic/claude-haiku-4.5"],
    "threshold is script tier; only the wake-me wording touches an animal")

add("ts028-journal-into-vault", "Journal every day into my vault",
    "append daily journal into the vault",
    "the day's notes dictated or typed",
    "a dated Obsidian entry, filed",
    "cron",
    [GALLERY + " (jezza2463 daily journal to Obsidian via OSS models)"],
    ["open-mistral-nemo", "qwen2.5:7b", "anthropic/claude-haiku-4.5"],
    "the local free lane is exactly this volume class")

add("ts029-signals-into-ledger", "Run 20 small checks a day into one triage list",
    "collect cron signals into a triaged ledger",
    "many small scheduled probes (prices, feeds, statuses)",
    "one daily triaged ledger of what needs eyes",
    "cron",
    [GALLERY + " (u/SquishyData 20 cron signals writing to a daily triaged ledger)",
     GALLERY + " (u/HolmeBengt 28 cron jobs)"],
    ["anthropic/claude-haiku-4.5"],
    "the estate's own dawn-report/attention.md shape in a stranger's build")

add("ts030-kanban-agent-team", "Run my team of agents off one kanban board",
    "coordinate agents on a shared kanban",
    "a board of tasks plus worker agents",
    "graded work (pass/rework/failed) flowing across the board",
    "watch",
    [GALLERY + " (u/Ok_Run_5401 Kanban board coordinating 7+ agents)",
     GALLERY + " (HoLiPrompt Chief-of-Staff orchestrator grading workers pass/rework/failed, auto-creating skills)",
     DROP + " (seven agents on a shared Kanban; Chief of Staff grading worker output)"],
    ["anthropic/claude-opus-5.5", "z-ai/glm-5.3-prime"],
    "the gopher-director/grading shapes; route table grading is thin (8 rows), evidence this census feeds")

add("ts031-lessons-into-policy", "When it messes up, write the rule so it never repeats",
    "codify mistakes into policy rules",
    "support mistakes, bad outputs, user corrections",
    "new standing policy rules applied to future runs",
    "watch",
    [GALLERY + " (scotty529 Gumroad agent on a dedicated Mac: support tickets, X mentions, finance docs, mistake to policy rules)"],
    ["z-ai/glm-5.3-prime", "anthropic/claude-opus-5.5"],
    "the estate's ratchet/self-improve law as a user-facing shape")

add("ts032-build-app-approval-gates", "Build the whole app, but I approve each step from my phone",
    "build an app with human approval gates",
    "a product idea, a repo, a phone",
    "shipped app/PR reviewed over Telegram at each gate",
    "one-shot",
    [GALLERY + " (u/riceinmybelly solo app build: agent files tasks, codes, QA, deploys, reviewed over Telegram)",
     GALLERY + " (u/Elegant_Emergency859 Greek PDF to reviewed PR over Telegram)",
     SHOWCASE + " (@chrisbanes feature implementation agents driven from phone via Telegram)"],
    ["z-ai/glm-5.3-prime", "anthropic/claude-opus-5.5"],
    "descent-leg loop: one landed deliverable per turn, operator-proxy steering")

add("ts033-tell-a-story", "Tell my kid a bedtime story tonight",
    "generate a personal story on request",
    "the child's current obsessions, the evening",
    "a fresh bedtime story",
    "one-shot",
    [GALLERY + " (kovern bedtime stories for daughter)",
     GALLERY + " (u/Exciting_Charity7304 JARVIS kid-mode tablet for a 7-year-old)"],
    ["anthropic/claude-haiku-4.5", "anthropic/claude-sonnet-5.5"],
    "light creative generation; tavern-turn class volume")

add("ts034-research-report", "Go research this and bring me a real report",
    "research a topic into a cited report",
    "a topic, a deadline",
    "a structured report (80-project ecosystem map, market map)",
    "one-shot",
    [GALLERY + " (KSimback ecosystem map of 80+ projects from a research task)",
     GALLERY + " (Halfbit Studio lead research and competitor analysis with YouTrack tickets)",
     GALLERY + " (dre108 Gigaxity free research stack replacing Perplexity)"],
    ["x-ai/grok-4.7", "anthropic/claude-opus-5.5", "deepseek/deepseek-v4.1-flash"],
    "the descent protocol's own shape: cheap-first sensing, premium synthesis")

# ---- openclaw sweep ----
add("ts035-smart-home-control", "Control my house by chat",
    "control smart home devices on command",
    "chat/voice commands, device APIs",
    "device actions plus confirmations",
    "watch",
    [SHOWCASE + " (@iannuttall smart home control)",
     SHOWCASE + " (@buddyhadry Alexa CLI for smart home control)",
     SHOWCASE + " (@acevail_ email + Home Assistant + homelab SSH via Telegram)"],
    ["anthropic/claude-haiku-4.5", "qwen2.5:7b"],
    "intent parse is scut; the effect goes through the effect broker (model text proposes, only the broker authorizes)")

add("ts036-family-meal-plan", "Plan our meals and the shopping list every week",
    "plan meals + build a shopping list",
    "family preferences, calendar, pantry",
    "a weekly meal plan plus shopping list plus reminders",
    "cron",
    [SHOWCASE + " (@stevecaldwell family meal planning with shopping lists and reminders)",
     AWESOME + " (family calendar morning briefing + household inventory)"],
    ["anthropic/claude-haiku-4.5", "z-ai/glm-5.3-prime"],
    "constraint planning, light")

add("ts037-video-instead-of-watching", "Summarize the video so I do not have to watch it",
    "summarize videos on a schedule",
    "a YouTube/watch-later queue",
    "short text summaries replacing watch time",
    "cron",
    [SHOWCASE + " (@chrisrodz35 YouTube summary cron replacing video watching)",
     AWESOME + " (Reddit/YouTube/tech-news digests)"],
    ["NEW: no video/audio-in animal"],
    "llama-vision sees frames, none of the 17 ingests video or audio tracks; a transcript-first path would fit haiku")

add("ts038-self-heal-server", "Fix the home server before I notice it broke",
    "watch + self-heal a server",
    "SSH, service health, cron probes",
    "repairs plus an incident note",
    "watch",
    [AWESOME + " (self-healing home server with SSH + automated cron jobs)",
     GALLERY + " (u/Bichev profiling pass is the measure-first cousin)"],
    ["anthropic/claude-haiku-4.5", "z-ai/glm-5.3-prime"],
    "detection is script tier; the fix-decision leg is cheap judgment with effect gates")

add("ts039-generate-media-assets", "Make the thumbnails and ad creatives for me",
    "generate images/video assets",
    "a product URL, a campaign brief",
    "thumbnails, UGC-style ad videos, briefs",
    "one-shot",
    [SHOWCASE + " (@xMikeMickelson UGC influencer video generation)",
     AWESOME + " (multi-agent Discord content factory: research, writing, thumbnails)",
     GALLERY + " (codewithimanshu UGC ad briefs in ~4 min from a product URL)"],
    ["NEW: no generation animal"],
    "the 17 are judgment/text animals (one vision reader, zero generators); media generation needs a NEW animal class")

add("ts040-voice-call-agent", "Have it actually call people for me",
    "place voice calls with two-way conversation",
    "a guest list or confirmation task",
    "completed calls with outcomes logged",
    "one-shot",
    [AWESOME + " (event guest confirmation by AI voice calls)",
     AWESOME + " (phone-call notifications with two-way conversation)"],
    ["NEW: no voice-out animal"],
    "TTS plus live telephony has no animal and no route-table shape; operator-gated effect class")

# ---- validate + write ----
assert len(S) == len(set(r["shape_id"] for r in S)), "dupe shape_id"
vo = {}
for r in S:
    assert r["verb_object"] not in vo, "dupe verb_object: " + r["verb_object"]
    vo[r["verb_object"]] = r["shape_id"]
for r in S:
    assert r["cadence"] in ("one-shot", "cron", "watch")
    assert r["evidence"], "empty evidence " + r["shape_id"]

bad = []


def scan(x, path):
    if isinstance(x, str):
        if "\u2014" in x or "\u2013" in x:
            bad.append(path)
    elif isinstance(x, dict):
        for k, v in x.items():
            scan(v, path + "." + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            scan(v, path + "[%d]" % i)


for r in S:
    scan(r, r["shape_id"])
assert not bad, "em/en dash found: " + repr(bad)

out = "watch/inbox/task_shapes_20260109/task_shapes.jsonl"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    for r in S:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

cad = Counter(r["cadence"] for r in S)
evcount = [(r["shape_id"], r["plain_name"], len(r["evidence"])) for r in S]
new_ids = [r["shape_id"] for r in S
           if any(str(x).startswith("NEW") for x in r["fits_our_17_animals"])]
animals_used = set()
for r in S:
    for a in r["fits_our_17_animals"]:
        if not str(a).startswith("NEW"):
            animals_used.add(a)
print("rows:", len(S))
print("cadence:", dict(cad))
print("NEW shapes:", new_ids)
print("animals covered:", len(animals_used), sorted(animals_used))
print("top evidence:", sorted(evcount, key=lambda t: -t[2])[:10])
