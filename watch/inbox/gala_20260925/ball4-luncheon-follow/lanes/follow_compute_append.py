# gala-follow-compute lane: append 5 compute rows to the luncheon signals register.
# Schema mirrors rows already written by gala-ball4-follow-defense-enterprise (rows 1-8)
# and gala-ball4-follow-models (rows 9-17) in the same file.
import json
from datetime import datetime, timezone
from pathlib import Path

REG = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\luncheon_watchlist_20260929_signals.jsonl")
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
W = "gala-follow-compute"
WIN = "2026-09-15/2026-09-29"

rows = [
 {
  "ts": ts, "writer": W, "watch_id": "lunch-jensen-huang", "name": "Jensen Huang",
  "org": "Nvidia CEO", "lane": "compute", "window": WIN,
  "in_window": [
   {"signal": "Nvidia announced a $150B stock buyback (GuruFocus headline 'NVIDIA (NVDA) Announces $150 Billion Stock Buyback', '8 hours ago' at 2026-09-29 search; syndicated headlines call it 'the largest single authorization in history'); stock climbed on the news",
    "date": "2026-09-29 (recency marker '8 hours ago' under oneWeek filter; exact article timestamp unpinned)",
    "source": "gurufocus.com headline via web_search_prime; corroborating finance.yahoo.com and finviz.com syndications", "grade": "search"},
   {"signal": "Nvidia unveiled an AI security platform said to stop AI agents 'going rogue'", "date": "2026-09-28 +/-1d (recency marker '1 day ago')",
    "source": "dailyunion.com via web_search_prime", "grade": "search"},
   {"signal": "OpenAI and Nvidia jointly announced measures to safeguard against AI threats", "date": "2026-09-28 +/-1d",
    "source": "ABC / modernghana.com syndication via web_search_prime", "grade": "search"}
  ],
  "out_of_window_nearest": [
   {"signal": "CES 2026 (Jan 5): Vera Rubin superchip launched, Rubin in full production, systems shipping H2 2026 (CoreWeave integrating)", "date": "2026-01-05", "source": "nvidianews.nvidia.com via web_search_prime"},
   {"signal": "GTC 2026 (Mar 16): Huang cites $1T in orders for Blackwell+Rubin through 2027; Rubin Ultra demoed with 1TB HBM4e on the Kyber rack", "date": "2026-03-16", "source": "web_search_prime search summary"}
  ],
  "date_honesty_note": "The in-window legs are recency-marker-dated search results (domain-level URLs, no article slugs byte-verified). A Jan 22 2026 headline referencing a '$150 Billion Buyback Bombshell' also surfaced in an unfiltered search, so whether Sept 29 is a fresh incremental authorization on top of a Jan one is UNCONFIRMED; registered as the in-window buyback story by its own '8 hours ago' recency marker.",
  "estate_angle": "VRAM ladder + local-inference economics: cash-return mode at the top of the stack plus a sold-out-through-2027 datacenter roadmap means zero consumer-VRAM price relief is coming; the frontier memory rung (Rubin Ultra 1TB HBM4e per package) recedes from our 24GB RTX 3090 sweet-spot rungs (~$1,100-1,300 used, attic HARDWARE_RADAR_20260901.md:27), so local stays the sovereignty hedge and frontier rental (estate cost model: frontier ask $0.29 naive / $0.15 batched, AGENTS.md clippy block) stays supply-constrained and priced high through Rubin's H2-2026 shipping window.",
  "handle_check": "org @nvidia live-confirmed on fxtwitter (code 200: 'NVIDIA', id 61559439, 2,673,377 followers, bio 'The official handle for NVIDIA'); register's org grade stands, no watchlist row change needed",
  "sources": ["web_search_prime: 'Jensen Huang Nvidia September 2026 announcement roadmap Rubin' (2026-09-29)", "web_search_prime: 'Nvidia news this week late September 2026' recency oneWeek (2026-09-29)", "web_search_prime: 'Nvidia $150 billion buyback announcement September 2026' (2026-09-29)", "web_search_prime: 'gurufocus Nvidia NVDA announces $150 billion stock buyback Jensen Huang' (2026-09-29)", "api.fxtwitter.com/nvidia (fetched this session)"]
 },
 {
  "ts": ts, "writer": W, "watch_id": "lunch-lisa-su", "name": "Lisa Su",
  "org": "AMD CEO", "lane": "compute", "window": WIN,
  "in_window": [
   {"signal": "AMD Helios racks shipping ~50,000 MI450 GPUs to Oracle in Q3 2026, positioned against Nvidia Rubin NVL72 on memory capacity", "date": "2026-09-28 +/-1d (recency marker '11 hours ago')",
    "source": "shattered.io headline 'AMD Helios Ships 50000 MI450 GPUs to Oracle [2026]' via web_search_prime", "grade": "search"},
   {"signal": "ROCm AMD Infinity Context (AIC), a purpose-built KV-cache/context system supporting MI455X/Helios deployments, in tech preview", "date": "2026-09 (month-pinned, exact day unpinned)",
    "source": "web_search_prime search summary", "grade": "search"},
   {"signal": "AMD stock broke $524 mid-September on Helios demand, analysts eyeing $548", "date": "2026-09-15 +/-3d (mid-September, unpinned exact)",
    "source": "web_search_prime search summary", "grade": "search"}
  ],
  "out_of_window_nearest": [
   {"signal": "Advancing AI 2026 (Jul 23): Helios rack launched, up to 2.9 exaflops FP4, 72 MI455X GPUs per liquid-cooled rack, MI455X carrying 432GB HBM4 per accelerator; second-gen AI servers in full production", "date": "2026-07-23", "source": "money.usnews.com + newsroom.amd.com via web_search_prime"},
   {"signal": "Citi Global TMT (Sep 8): MI450 production shipments began Q3 2026, larger ramp Q4 2026, further increase Q1 2027", "date": "2026-09-08", "source": "web_search_prime search summary"},
   {"signal": "OpenAI deal: 6 GW of Instinct GPUs, starting with 1 GW MI450 in H2 2026; Feb 2026 ~$100B Meta MI450/Helios deal", "date": "2026-02 (Meta) / earlier (OpenAI)", "source": "newsroom.amd.com via web_search_prime"}
  ],
  "date_honesty_note": "The Oracle 50k-GPU item is in-window by its own '11 hours ago' recency marker on a site not independently verified; AIC tech preview is month-pinned September 2026 without a day; the $524 break is 'mid-September' and may straddle the window edge. Roadmap specs (432GB HBM4, 72-GPU rack) are dated Jul 23, outside the window, folded as standing context.",
  "estate_angle": "VRAM ladder + local-inference economics: AIC is KV-cache/context management at rack scale - the exact problem class our corpus/library/lmcache-src tree studies - so AMD's software rail is converging on our own stack's design point. A second GPU source at 432GB HBM4 per card structurally pressures frontier rental prices down at the margin (good for our batched asks) while MI455X-scale HBM4 demand tightens memory markets further (bad for used 24GB street prices on our VRAM ladder rungs).",
  "handle_check": "@LisaSu live-confirmed on fxtwitter (code 200: 'Lisa Su', bio 'Chair and CEO of @AMD', id 836224570013138944, 320,593 followers); register's declared grade stands",
  "sources": ["web_search_prime: 'Lisa Su AMD Instinct MI450 Helios OpenAI deal September 2026' (2026-09-29)", "web_search_prime: 'AMD Instinct MI450 MI400' (2026-09-29, one intermediate 429 rate-limit noted)", "api.fxtwitter.com/LisaSu (fetched this session)"]
 },
 {
  "ts": ts, "writer": W, "watch_id": "lunch-hock-tan", "name": "Hock Tan",
  "org": "Broadcom CEO", "lane": "compute", "window": WIN,
  "in_window": [
   {"signal": "Despite calls to slow frontier AI development, Hock Tan doubled down on Broadcom's AI semiconductor revenue targets of roughly $115B in fiscal 2027 and $230B in fiscal 2028", "date": "2026-09-15 (reported Sept 14-15; registered at window edge, see honesty note)",
    "source": "briefs.co 'Broadcom's Big AI Chip Bet and Key Customers' coverage via web_search_prime", "grade": "search"}
  ],
  "out_of_window_nearest": [
   {"signal": "Q3 results (Sep 2-3): FY2026 AI semiconductor revenue projected ~$58B, up 186% from FY2025; Tan first stated the $115B FY27 / $230B FY28 targets; Broadcom accelerating Google Ironwood TPU shipments to Anthropic plus TPU 8i units", "date": "2026-09-02", "source": "briefs.co via web_search_prime"},
   {"signal": "Goldman Sachs conference (Sep 8): demand for custom AI chips rising fast but growth constrained by datacenter power availability and site readiness, not demand", "date": "2026-09-08", "source": "web_search_prime search summary"},
   {"signal": "Extended Meta partnership (Apr 2026) to roll out industry's first 2nm AI compute accelerator", "date": "2026-04", "source": "web_search_prime search summary"}
  ],
  "date_honesty_note": "The doubling-down item is dated Sept 14-15 by the search bundle; Sept 14 sits 15 days back, so the row is registered at 2026-09-15 (window edge) with the range stated. The underlying targets and Ironwood-Anthropic acceleration are from Sept 2-3 earnings coverage, outside the window, folded as the substance Tan was defending. Domain-level URLs only.",
  "estate_angle": "VRAM ladder + local-inference economics: TPU-class ASICs diversify frontier compute supply, which leans on input/cache-side token prices for Claude-class rental - on the estate side that confirms the standing law that only OUTPUT-token cuts are real cheapeners (AGENTS.md clippy block). With power, not demand, named as the binding constraint, rental supply stays tight through 2027, so the local cheap tier - QLoRA 13B on one 24GB RTX 3090 (HARDWARE_RADAR_20260901.md:57-62) - remains the load-bearing rung for janitor and tuning work.",
  "handle_check": "org @Broadcom live-confirmed on fxtwitter (code 200: 'Broadcom', id 338504881, 66,720 followers, Palo Alto CA); register's org grade stands; Tan has no personal handle in the register (org-grade, correct)",
  "sources": ["web_search_prime: 'Hock Tan Broadcom custom AI accelerator news September 2026' (2026-09-29)", "api.fxtwitter.com/Broadcom (fetched this session)"]
 },
 {
  "ts": ts, "writer": W, "watch_id": "lunch-sanjay-mehrotra", "name": "Sanjay Mehrotra",
  "org": "Micron CEO", "lane": "compute", "window": WIN,
  "in_window": [
   {"signal": "Into the Sept 30 fiscal-Q4 print, Stifel reiterated Buy with a $1,500 price target, expecting Q4 results and guidance to top consensus while seeing upside as priced in", "date": "2026-09-27 (recency marker '2 days ago')",
    "source": "binance.com 'Micron Heads Into Fiscal Q4 Earnings With the Bar...' via web_search_prime", "grade": "search"}
  ],
  "out_of_window_nearest": [
   {"signal": "Coverage bundle: Mehrotra says Micron meets only 50-65% of key customers' HBM demand and CY2026 HBM4 capacity is sold out (article date unpinned in this search; standing facts corroborated by Dec 2025 / Mar 12 2026 / Jun 2026 sold-out statements)", "date": "unpinned in this search bundle; standing since at least 2025-12-18",
    "source": "insiderfinance.io 'Micron Stock Surges on HBM Shortage and Analyst Upgrades' + 247wallst, biggofinance, HTX via web_search_prime"},
   {"signal": "FQ4 guidance (issued with FQ3 results Jun 24, 2026): ~$50.0B revenue +/- $1.0B at ~86% gross margin", "date": "2026-06-24", "source": "web_search_prime search summary"}
  ],
  "date_honesty_note": "The only cleanly dated in-window leg is the Sept 27 Stifel repricing. The 50-65%/HBM4-sold-out facts carry no article date in this search bundle (window-plausible at best; the underlying statements trace to FY26 earnings calls from Dec 2025 onward) - registered as standing context, not as a fresh in-window statement. Domain-level URLs only; the Sept 30 earnings date is search-surfaced, not verified against Micron IR.",
  "estate_angle": "VRAM ladder + local-inference economics: HBM is the binding input on every accelerator rung above us (Rubin's HBM4e, MI455X's HBM4, Ironwood's stack), so sold-out-through-2026 HBM4 caps how fast rental supply can grow and keeps frontier price cuts shallow. The same memory supercycle lifts DRAM/GDDR costs, which inflates rather than deflates the used-24GB rungs of our VRAM ladder (RTX 3090 ~$1,100-1,300, HARDWARE_RADAR_20260901.md:27) - the attic buy-window logic needs a re-quote before any hardware purchase, not a green light from old prices.",
  "handle_check": "org @MicronTech live-confirmed on fxtwitter (code 200: 'Micron Technology', id 19037711, 64,051 followers, Boise ID); register's org grade stands",
  "sources": ["web_search_prime: 'Micron HBM supply sold out Mehrotra September 2026' (2026-09-29)", "web_search_prime: 'Micron earnings fiscal Q4 September 2026 HBM4 guidance' (2026-09-29)", "api.fxtwitter.com/MicronTech (fetched this session)"]
 },
 {
  "ts": ts, "writer": W, "watch_id": "lunch-elon-musk", "name": "Elon Musk",
  "org": "X, Tesla, SpaceX; xAI compute buildout", "lane": "compute+models", "window": WIN,
  "in_window": [
   {"signal": "x.ai/colossus Latest-News post 'Introducing Grok 4.7'", "date": "2026-09-21", "source": "https://x.ai/colossus (WebFetch this session)", "grade": "fetch"},
   {"signal": "x.ai/colossus Latest-News post 'Team Bots: AI coworkers that learn from your team'", "date": "2026-09-28", "source": "https://x.ai/colossus (WebFetch this session)", "grade": "fetch"},
   {"signal": "x.ai/colossus Latest-News post 'Introducing Grok Voice Transcribe 2.0'", "date": "2026-09-18", "source": "https://x.ai/colossus (WebFetch this session)", "grade": "fetch"},
   {"signal": "Page banner on x.ai/colossus reads 'Anthropic partners with Colossus'; page states 200,000 H100 GPUs in one interconnected cluster, 170 PB/s aggregate memory bandwidth, roadmap to 1M GPUs. Reading: a rival lab training on xAI compute. Interpretation flagged, not independently verified", "date": "page state as fetched 2026-09-29",
    "source": "https://x.ai/colossus (WebFetch this session)", "grade": "fetch (banner read; deal shape unverified)"}
  ],
  "out_of_window_nearest": [
   {"signal": "SpaceX-xAI merger (~$1.25T combined entity); SpaceX sought permission for up to 1M solar-powered satellites engineered as orbital data centers", "date": "2026-02-04", "source": "reuters.com via web_search_prime"},
   {"signal": "$20B 'Terafab' semiconductor plant announced for space-based-datacenter and vehicle chips (matches Musk's live X bio link 'http://Terafab.AI')", "date": "2026-03", "source": "Data Center Dynamics via web_search_prime"},
   {"signal": "SpaceX targeting 1 GW of orbital AI compute by end of 2026, scaling toward 100 GW in ~3.5 years", "date": "2026-06", "source": "KBTX via web_search_prime"},
   {"signal": "Colossus 2 online as first gigawatt-scale training cluster; third Memphis building purchased toward ~2 GW and ~555,000 GPUs (~$18B)", "date": "2026-01", "source": "teslarati.com + introl.com via web_search_prime"}
  ],
  "date_honesty_note": "The in-window legs are fetch-grade off x.ai/colossus with the page's own date stamps (Sep 18/21/28, 2026). Four searches found no fresh September xAI milestone beyond these; Grok 5 remains H2-2026-expected per coverage. 'Anthropic partners with Colossus' is the banner text as-read - what the partnership contractually is was NOT verifiable with the tools used. The Jan-Jun 2026 buildout items are context, outside the window.",
  "estate_angle": "VRAM ladder + local-inference economics: if the banner means Anthropic training on Colossus, rival labs are pooling compute, which loosens frontier supply at the margin while Grok 4.7 landing mid-cycle shows release cadence accelerating - the driving-ladder's model roster churns faster than the ribs refresh, so model pinning needs shorter refresh loops. The orbital/Terafab ambitions (1 GW by end-2026) are non-binding for local economics this window: our 24GB gemma-janitor ladder is untouched by them this quarter.",
  "handle_check": "@elonmusk live-confirmed on fxtwitter (code 200: 'Elon Musk', id 44196397, 241,720,780 followers, bio description resolving to 'http://Terafab.AI'); register's declared grade stands",
  "sources": ["https://x.ai/colossus (WebFetch this session 2026-09-29)", "web_search_prime: 'Elon Musk xAI Colossus 2 gigawatt Grok training September 2026' (2026-09-29)", "web_search_prime: 'xAI Grok 5 Colossus Memphis news September 28 2026' (2026-09-29)", "web_search_prime: 'xAI gigawatt Terafab SpaceX orbital data centers Musk' (2026-09-29)", "api.fxtwitter.com/elonmusk (fetched this session)"]
 }
]

existing = REG.read_text(encoding="utf-8") if REG.exists() else ""
mine_before = sum(1 for ln in existing.splitlines() if ln.strip() and json.loads(ln).get("writer") == W)
with REG.open("a", encoding="utf-8", newline="\n") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"appended {len(rows)} rows (writer={W} had {mine_before} rows before)")
