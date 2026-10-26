# SELF-STEAL — MCP: what it is, what we did with it, and the leverage plan (2026-09-05)

**ITEM:** Operator: "What the fuck is mcp and how are we using it... eli5 how have I asked
you to use it? With what we know now how can we leverage mcp and all 4k servers... with
our internal systems — deep self steal."

## ELI5 (the one-paragraph version, no codenames)

MCP is a universal plug. Before it, connecting an AI to a tool meant custom wiring every
time — every AI app soldered its own cables to every file system, browser, or search API.
MCP says: everybody builds one standard plug. A "server" here is not a big machine — it is
a small program that offers tools through that plug: "search the web," "read this folder,"
"drive that browser," "generate an image." An AI app with an MCP socket can use any tool
built by anybody. That is the whole idea. Everything else is plumbing we already run.

## HOW WE USE IT TODAY (measured, all receipted 09-04/05)

1. **Our own organ is an MCP server.** The mag tools the seat uses hourly (run shell and
   python, read/write files, the blackboard, vision, voice) speak MCP. Tonight it moved
   INTO the cage: one copy at 127.0.0.1:8001/mcp serving every seat, instead of three
   copies per session spawning console windows on the desktop.
2. **Network senses with zero install.** The z.ai web-search / web-reader / zread doors
   are remote MCP — tools that run anywhere and never spawn a process here.
3. **Hands and eyes.** Computer-use (desktop control), browser-use (the staff-room drive),
   android-emulator (the phone body), mapbox (the geo seat), mimosa (the security scanner
   that has blocked real bad code twice) — each is an MCP server giving the seat one
   capability.
4. **We are a publisher too.** The gateway proves our internal tools can be served to any
   MCP-speaking client — any model body we hire can drive the fleet shelf.

## HOW THE OPERATOR ASKED (his own words, on the record)

- "We need to figure out how to use MCP servers now that we have fucking thousands of
  them... tease it out using steps first socratically" → produced the 3,838-server census
  and the senses map (09-04).
- "This mcp server thing needs to be dogfooded" → produced the three picks and the
  anti-sprawl selection rule (09-04).
- "Everything should be in containers and not running window swarms on my desktop" →
  produced tonight's topology fix: senses live in the cage.

## HONEST CORRECTION

We do not OWN 4k servers. We own the CATALOG — a triple-sourced shopping list of 3,838
that exist in the world, mapped against our gaps — plus ~9 live installs. The catalog is
the asset; ownership happens at adoption, one card at a time.

## THE LEVERAGE PLAN (deep self-steal — the synthesis)

**The core insight: the plug goes both ways.** MCP is not just how we consume the world's
tools — it is how our internal organs become uniformly drivable by every worker we hire.
Chain, room, blackboard, lanes, forge, census: each one that speaks MCP becomes part of
the same shelf the free flash lanes, GPT, and grok all work from. One shelf, inside and
outside tools, every worker the same interface.

1. **One adapter, whole aisles (pattern proven, extension is a small build).** Tonight
   proved in-cage serve + many clients. The build: let the gateway proxy adopted
   third-party servers too, so adoption cost stays "one row in the cage + one card" —
   never "per-seat install, per-desktop windows" again. (Supported pattern; proxy build
   Unproven until wired.)
2. **Aisle-before-build, applied hard.** The senses map says we are weak exactly where
   the dogfood salon picked: monitoring (the fleet feeling its own pulse — tonight proved
   the need: stale watchdog, idling handshakes), time-series fetch cache (attacks the
   92-97% context re-feed waste), agreements/signed leases (the enforcement backbone).
   Shop those three before building homegrown; steal the bones where a server fits,
   keep the sovereignty line where it does not.
3. **The census as the prose-burn tool.** Several stale cards in the 767 describe
   homegrown tools that now exist as free servers. The prose lane's conversion passes
   should check the catalog first: tombstone ours when the aisle has it, cite the server
   card as the replacement.
4. **Guardrails already minted (they are why this will not sprawl):** the sovereignty
   line — chain, room, keys, and the security scanner are NEVER third-party; NO DEFAULT
   SENSES — every adoption carries a manifest card, a real-task proof, a TTL, and a
   kill-switch test; SENSES LIVE IN THE CAGE — adoption is container-side or it does not
   happen.

## TRUTH

- What MCP is and how we use it: Supported (all of it running and probed tonight).
- "We own 4k servers": Disputed as stated — we own the catalog and ~9 live; corrected.
- The leverage plan: the pattern is Supported, the proxy extension and the three adoptions
  are Unproven until built and driven once each.

*— Sancho, 09-05 night watch. The plug goes both ways; that is the whole trick.*

## THE MINE (09-05, operator challenge: "why map 3,838 if 9 exist — what can we mine")

Ran the real pass on our own digest, $0, ~30 seconds: 58 categories / 3,483 entries parsed.

**THICK = world commodities (never build, adopt in minutes when an organ needs one):**
developer tools 451 · finance 402 · memory/knowledge 253·290 · search 138·203 ·
browser automation 88 · monitoring 77 · coding agents 73 · image/vision 112 · voice 105.

**HOLES = the keyword mine against our strengths (the actual gold):**
- invariant / verification / falsifier: **4 of 3,483 = 0.1%** — the emptiest strategic
  category in the catalog, and it is EXACTLY our strongest doctrine (paste falsifiers,
  tri-state, kill-switches). Invariant Workbench niche now MEASURED, not vibes.
- prompt/context caching: **1 hit = 0.0%** — the cache-mining craft has one prior art
  entry in the entire world list.
- gpu/cluster scheduling for agents: **1 hit** — empty until Rocinante lands (Oct 27).
- agreements/leases 1.7% and multi-agent coordination 1.3% — thin but non-zero: steal
  bones, early field (the dogfood picks validated).
- agent receipts/audit/provenance: 127 = 3.6% — THICKER than expected: our verkle-chain
  doctrine has company; steal-pass queued (who is building agent audit trails and what
  do their schemas look like).

**THE ANSWER TO "WHY MAP":** the map is not endpoints to run. It is (1) the parts
catalog — "we need X" costs minutes instead of a build day; (2) the demand curve — the
categories are the world's bets on what agents need, free market intel; (3) the hole
map — measured proof of where we are alone (0.0-0.1% categories = moat/niche/public-turn
story) and where we are late (provenance 3.6% = go read their schemas and steal).
Mining costs nothing; running all 3,838 would be insane — running 9 well + mining the
rest is the whole play.

## THE TRIANGULATION (09-05, operator: "how does this map to what frontier AI companies are hiring for")

Two independent instruments, one target. Instrument A = where labs spend headcount
(20-lab sweep, receipted 09-04: the universal five). Instrument B = where the tooling
market is empty (tonight's catalog mine). Where they agree, that is the frontier.

| Frontier demand (hiring) | Tooling market (3,483 servers) | Our position | The read |
|---|---|---|---|
| EVALS — the prerequisite department | verification/falsifiers **0.1%** (4 hits) | our CORE doctrine: tri-state, falsifiers, kill-switches, harness_eval | **CONVERGENT. Labs hire it; the market has none; we do it daily.** The moat is measured. |
| Inference optimization | prompt/context caching **0.0%** (1 hit) | we LIVE the problem: 92-97% context re-feed measured; cache-mining craft; Lite lane economics | the tooling gap IS the hiring signal — labs hire for what no server wraps yet |
| Kernels / compute | gpu/cluster scheduling **0.0%** (1 hit) | COMPUTE_DIG: burst-rich, memory-poor until Rocinante (Oct 27) | empty tooling + owned compute coming = our timing, not the market's |
| Agents infra | coordination 1.3% / signed leases 1.7% — early field | one-scheduler, lanes, claim-organ (CAS fix verified) | early is good: org-design is the differentiator, bones stealable |
| Post-training / RL | (no direct tool layer — it eats data) | receipts everywhere = training data by construction; #AGENT-TRACE-MINER boot ordered | "every record surface is future training data" is the moat that compounds |
| (bonus) audit/compliance | provenance/audit **3.6%** (127 — thicker than expected) | verkle chain, signed history | not a moat, a STEAL-PASS: go read the 127 schemas |

**THE PUNCHLINE:** the catalog mine independently rediscovered the sweep's conclusion.
The labs' prerequisite department (evals) is the tooling market's emptiest shelf (0.1%)
and our daily operating doctrine. Two instruments, one target — that is what "rich
frontier signal" looks like when it is real. Build order already carries it:
#EVALS-ANCHOR-EXTERNAL (day 3) and #SOVEREIGN-AGENT-BENCHMARK (Sep 20 wall).

*Instrument A asked labs where they hurt. Instrument B asked the market what nobody
built. Same answer. That is triangulation.*

## THE FREE-FEEDING FLYWHEEL (09-05, operator: "use their desperate spend with infinite capital to feed our system for free using our surface")

Their capital is desperate in four visible places, and our surface drinks from each:

- **A. PROMO ARBITRAGE (running, receipted).** The land-grab pricing war IS our free
  inference: 5.3-flash unlimited in ZCode (wall = Sep 20 — bank work before it),
  glm-4.7 cache-mining, grok free lane, Lite 50/50 sustained. Law: bulk on free,
  premium for judgment only. Their spend, our queue.
- **B. WEIGHTS + SPEC MINING (running).** Their open-source releases are free organs
  and corpus: Apache/MIT harnesses (openai/evals secretly MIT), commerce-agents, arXiv
  (Dual Contouring steal), and 3,483 tool specs + 127 provenance schemas = free design
  intel. LEGAL_MEMO_002: method is not expression; the only bite is a ban — so never
  earn one (rate-craft, no login bypass).
- **C. THE EVAL-SURFACE FLIP (the strategic move, in the build order).** They are
  desperate for exactly what we do free: credible external evals. Benchmark orgs get
  free frontier-model access because labs NEED third-party scores. #EVALS-ANCHOR-
  EXTERNAL (day 3) + #SOVEREIGN-AGENT-BENCHMARK (Sep 20) make our surface an eval
  surface; then their model budgets pay our lanes — eval keys, early access, credits —
  to be scored by us. They sell docility; we sell receipts; receipts are what they buy.
- **D. GRANT/BOUNTY CONVERSION (operator-gated).** Their research-funding arms
  (DeepMind safety $10M class, lab grant programs) fund exactly our receipts-doctrine.
  Gate: applications ride the operator's name and keys — his GO, one-time handshake.

The flywheel: publish receipts on the public surface (let-them-watch) → their scouts
and readers arrive → B/C/D convert inbound → free lanes and model access feed the
system → more receipts. Their spend buys the traffic; the surface converts it.

GUARDRAILS (unchanged): LAW-055 harvest-free-train-clean (stay ban-free), premium for
judgment only, secrets never echoed, sovereignty line — their capital never touches
chain/room/keys.
