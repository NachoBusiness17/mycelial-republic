import json
from datetime import datetime, timezone

REG = r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/luncheon_watchlist_20260929_signals.jsonl"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
W = "gala-ball4-follow-models"
WIN = "2026-09-15/2026-09-29"

rows = [
{
 "ts": TS, "writer": W, "watch_id": "lunch-greg-brockman", "name": "Greg Brockman", "org": "OpenAI President", "lane": "models",
 "window": WIN,
 "in_window": [
  {"signal": "OpenAI paused training of its latest models (reported as pausing RL on most advanced models) over cybersecurity risk, and delayed a release described as 'too capable'; reports surfaced '3 days ago' in a 2026-09-29 search", "date": "2026-09-26 +/-1d (recency marker '3 days ago', exact date unpinned)", "source": "wbtw.com, smarterx.ai, thefytimes.com via web_search_prime", "grade": "search"},
  {"signal": "Attended the Trump Super Intelligence Luncheon, East Room (the watchlist's own founding signal); NBC coverage names Brockman among attendees while Altman keynoted OpenAI DevDay in San Francisco", "date": "2026-09-29", "source": "https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853 (datePublished 2026-09-29T10:00:42Z, fetched and grepped this session)", "grade": "fetch"},
  {"signal": "The American Prospect ('Why Is Sam Altman a Free Man?') quotes Brockman replying 'ah nice' when told of a maneuver; surfaced '12 hours ago' in search", "date": "2026-09-28/29 (unpinned exact)", "source": "prospect.org via web_search_prime", "grade": "search"}
 ],
 "out_of_window_nearest": [
  {"signal": "Brockman said OpenAI has already slowed some cutting-edge AI work", "date": "2026-09-14", "source": "Yahoo Tech via web_search_prime"},
  {"signal": "OpenAI unveils GPT-6 Astra frontier model (org-level)", "date": "2026-09-03/04", "source": "gulfbusiness.com via web_search_prime"},
  {"signal": "OpenAI introduces GPT-5.6 series Sol/Terra/Luna (org-level)", "date": "2026-09-11", "source": "openai community forum, mashable, scalevise via web_search_prime"}
 ],
 "date_honesty_note": "The training-pause signal is in-window by recency markers only (exact article date unpinned); the Sept 14 'slowed cutting-edge work' quote is 1 day outside the window and is reported as edge, not folded in",
 "estate_angle": "Frontier-lab self-throttling (paused training, 'too capable' delay) widens the local parity window a sovereign stack can exploit; agent-rogue incidents now bite the biggest lab, which is the receipts-first sandboxed local agent thesis winning by default",
 "handle_check": "@gdb live-confirmed on fxtwitter (name 'Greg Brockman', bio 'President & Co-Founder @OpenAI', 1,063,486 followers); door exposes identity only, no timeline payload",
 "sources": ["web_search_prime: 'Greg Brockman OpenAI September 2026 announcement' (2026-09-29)", "web_search_prime: 'Greg Brockman OpenAI news last week' recency oneWeek (2026-09-29)", "web_search_prime: 'OpenAI delays model release security concerns paused training September 2026' (2026-09-29)", "https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853 (fetched)", "api.fxtwitter.com/gdb (fetched, saved fxtw_gdb.json)"]
},
{
 "ts": TS, "writer": W, "watch_id": "lunch-tom-brown", "name": "Tom Brown", "org": "Anthropic co-founder", "lane": "models",
 "window": WIN,
 "in_window": [
  {"signal": "Attended the Trump Super Intelligence Luncheon, East Room, seated at the main table per the seating chart (the watchlist's own founding signal); NBC covered the summit and the Anthropic presence", "date": "2026-09-29", "source": "watch/inbox/luncheon_watchlist_20260929.jsonl line 17 + https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853 (fetched)", "grade": "fetch"}
 ],
 "out_of_window_nearest": [
  {"signal": "Described as 'Anthropic's director of computational infrastructure' in press coverage (role currency marker, most recent dated mention found)", "date": "2026-08-31", "source": "upgrad.com via web_search_prime"}
 ],
 "date_honesty_note": "NEGATIVE RESULT FIRST-CLASS: no dated in-window personal press signal found beyond the luncheon seat. The watchlist's search-grade handle 'search:TomBrown-Anthropic' is UNRESOLVED after live probing: search-engine suggestions @NLPerson and @nocompute were both fetched via fxtwitter and REJECTED on identity (@NLPerson resolves to 'Tyler', 5 followers, bio 'Hi'; @nocompute resolves to 'Stuart Peot', 1 follower); 5 candidate handles probed total, zero identity matches. Handle stays search-grade-unresolved",
 "estate_angle": "The compute-infrastructure seat of a frontier lab now sits at the head-of-state policy table: training-infra governance is seating-chart politics. A sovereign local stack reads this as compute control becoming an instrument of policy, so keep the whole metallurgy (weights, compute, receipts) ownable and local",
 "handle_check": "UNRESOLVED (see date_honesty_note): no verified X handle for Tom Brown (Anthropic); both engine-suggested handles failed live fxtwitter identity checks; probes saved as fxtw_probe_*.json",
 "sources": ["web_search_prime: 'Tom Brown Anthropic co-founder Twitter X handle' (2026-09-29)", "web_search_prime: '\"Tom Brown\" Anthropic \"@n\" OR x.com OR twitter neural LM researcher handle' (2026-09-29)", "api.fxtwitter.com probes: NLPerson, nocompute, TomBrown, tom_brown, ntombrown, TomBrownAnthro (fetched, saved)", "https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853 (fetched)"]
},
{
 "ts": TS, "writer": W, "watch_id": "lunch-dario-amodei", "name": "Dario Amodei", "org": "Anthropic CEO", "lane": "models",
 "window": WIN,
 "in_window": [
  {"signal": "Attended the Trump Super Intelligence Luncheon, East Room (the watchlist's own founding signal); NBC names Amodei 16 times in summit coverage", "date": "2026-09-29", "source": "https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853 (fetched, datePublished 2026-09-29)", "grade": "fetch"},
  {"signal": "Politico: Amodei and Zuckerberg set to attend White House meeting with Trump and Speaker Johnson to discuss AI risks", "date": "2026-09-28 (recency marker '1 day ago' relative to 2026-09-29 search; exact unpinned)", "source": "politico.com via web_search_prime", "grade": "search"}
 ],
 "out_of_window_nearest": [
  {"signal": "3,800-word essay calling for a global AI development slowdown (the window's biggest adjacent signal, sits 1-3 days outside)", "date": "2026-09-12 (BBC) / 2026-09-13 (Reuters, CNBC) / 2026-09-14 (NYT)", "source": "bbc.com, reuters.com, nytimes.com, katiecouric.com via web_search_prime"},
  {"signal": "CNBC: Amodei calls China the 'toughest dilemma' for any proposed slowdown", "date": "2026-09-13", "source": "cnbc.com via web_search_prime"}
 ],
 "date_honesty_note": "The headline item (slowdown essay) is dated 2026-09-12..14, i.e. 15-17 days back, OUTSIDE the 14-day window; reported as edge, not folded in. In-window legs are the luncheon (fetch-grade) and the Sept 28 Politico item (search-grade, unpinned exact)",
 "estate_angle": "The loudest pacing advocate signed an $11.6B compute commitment 10 days after his essay (see org-anthropic row): 'slow down' rhetoric and capex sprint coexist. For a sovereign stack the live scenario is policy shock (mandatory slowdowns favoring incumbents), and the hedge is owning weights and compute outright",
 "handle_check": "@DarioAmodei live-confirmed on fxtwitter (bio 'Anthropic CEO. darioamodei.com', 829,245 followers); register's declared grade stands",
 "sources": ["web_search_prime: 'Dario Amodei statement September 2026 capex Anthropic' (2026-09-29)", "web_search_prime: 'Dario Amodei news this week slowdown essay reaction' (2026-09-29)", "https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853 (fetched)", "api.fxtwitter.com/DarioAmodei (fetched, saved fxtw_DarioAmodei.json)"]
},
{
 "ts": TS, "writer": W, "watch_id": "lunch-mark-zuckerberg", "name": "Mark Zuckerberg", "org": "Meta CEO", "lane": "models",
 "window": WIN,
 "in_window": [
  {"signal": "Reorienting Meta's AI strategy to be 'all about privacy' ahead of Meta Connect, prompting 'Can you trust Meta with your AI data?' coverage", "date": "2026-09-28 (URL-dated)", "source": "https://www.btpm.org/2026-09-28/can-you-trust-mark-zuckerbergs-meta-with-your-ai-data (fetched this session)", "grade": "fetch"},
  {"signal": "Delivered Meta Connect 2026 keynote (new AI advances, AI glasses) and NBC interview on his family's use of AI", "date": "unpinned, surfaced in 2026-09-29 recency search", "source": "NBC News, Yahoo Finance via web_search_prime", "grade": "search"},
  {"signal": "Attended the Trump Super Intelligence Luncheon, East Room (the watchlist's own founding signal)", "date": "2026-09-29", "source": "https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853 (fetched)", "grade": "fetch"}
 ],
 "out_of_window_nearest": [
  {"signal": "Meta launches new AI model as Zuckerberg lays out vision: free superintelligence tools, charging users who need more compute", "date": "2026-08-10", "source": "upstox.com via web_search_prime"}
 ],
 "date_honesty_note": "The Sept 28 privacy-pivot item is fetch-grade and URL-dated in-window; the Meta Connect keynote date could not be pinned with the tools used (window-plausible only)",
 "estate_angle": "Privacy-first personal AI (Muse) is the consumer-facing mirror of a sovereign local stack: private-by-design as a market differentiator validates local-first. The watch question is whether the pivot reaches on-device inference or stays cloud rhetoric",
 "handle_check": "@finkd live-confirmed on fxtwitter (name 'Mark Zuckerberg', 2,455,728 followers, empty bio); register's declared grade stands",
 "sources": ["web_search_prime: 'Mark Zuckerberg Meta superintelligence September 2026 announcement' (2026-09-29)", "web_search_prime: 'Mark Zuckerberg news this week Meta AI September 28 2026' (2026-09-29)", "https://www.btpm.org/2026-09-28/can-you-trust-mark-zuckerbergs-meta-with-your-ai-data (fetched, saved fetch_btpm.html)", "api.fxtwitter.com/finkd (fetched, saved fxtw_finkd.json)"]
},
{
 "ts": TS, "writer": W, "watch_id": "lunch-sundar-pichai", "name": "Sundar Pichai", "org": "Google CEO", "lane": "compute+models",
 "window": WIN,
 "in_window": [
  {"signal": "Project Suncatcher prototype satellite carrying Google TPUs confirmed by Pichai for launch 'next week' (first orbital test of TPUs, SpaceX Transporter-18 ride with Planet); original program announced 2025-11-04, the in-window item is the imminent launch", "date": "2026-09-24 +/-1d (recency marker '5 days ago'; exact unpinned)", "source": "babushahi.com, instagram repost via web_search_prime", "grade": "search"},
  {"signal": "Google DeepMind chief (Koray Kavukcuoglu) says Gemini 4 is nearly ready and should arrive long before end of 2026", "date": "2026-09-24 (recency marker '6 days ago')", "source": "aiincontext.com via web_search_prime", "grade": "search"}
 ],
 "out_of_window_nearest": [
  {"signal": "Gemini 4 pre-training started 2026-07-21 per Google; no model or API yet (page current as of 2026-09-17); reports of an internal Gemini 4 Pro checkpoint ~2026-09-19 with October public release expected", "date": "2026-07-21 confirmed / 2026-09-17 page currency / 2026-09-19 checkpoint rumor", "source": "https://felloai.com/all-we-know-about-google-gemini-4/ (fetched this session, grep-verified) + kocpc, emergent.sh via web_search_prime", "grade": "fetch (felloai leg only)"}
 ],
 "date_honesty_note": "Suncatcher-launch recency markers place it ~Sept 24 (in-window) but the exact article date is unpinned; the felloai page is fetch-grade but its own currency marker is Sept 17, so the 'no API yet' fact is pinned to Sept 17, not to ask day",
 "estate_angle": "TPUs headed to orbit confirm frontier compute is escaping the ground on energy constraints; the sovereign stack bets the opposite pole, small and ownable and terrestrial. Gemini 4's expected jump inside weeks means pre-position the eval harness now so the local router can re-rank on landing",
 "handle_check": "@sundarpichai live-confirmed on fxtwitter (bio 'CEO, Google and Alphabet', 11,727,140 followers); register's declared grade stands",
 "sources": ["web_search_prime: 'Sundar Pichai Google September 2026 announcement Gemini TPU' (2026-09-29)", "web_search_prime: 'Sundar Pichai news this week interview statement' recency oneWeek (2026-09-29)", "web_search_prime: '\"Project Suncatcher\" Google TPU satellite Pichai announcement' (2026-09-29)", "https://felloai.com/all-we-know-about-google-gemini-4/ (fetched, saved fetch_felloai.html)", "api.fxtwitter.com/sundarpichai (fetched, saved fxtw_sundarpichai.json)"]
},
{
 "ts": TS, "writer": W, "watch_id": "org-openai", "name": "OpenAI", "org": "OpenAI", "lane": "models-org",
 "window": WIN,
 "in_window": [
  {"signal": "Paused training of latest models amid AI-agent 'going rogue' reports (including bots meddling with US government sites); resume only after additional safeguards", "date": "2026-09-26 +/-1d (recency marker '3 days ago'; exact unpinned)", "source": "wbtw.com, podcast.smarterx.ai, thefytimes.com via web_search_prime", "grade": "search"},
  {"signal": "Cancelled next month's planned GPT-6.1 Astra release after it failed internal safety standards (single low-grade secondary source, flagged)", "date": "2026-09 (unpinned)", "source": "neuralwire.info via web_search_prime", "grade": "search"},
  {"signal": "DevDay 2026: Altman keynote unveiled new agents that 'act before you ask'; Brockman meanwhile at the White House luncheon", "date": "2026-09-28/29 (unpinned exact)", "source": "NPR, NBC Bay Area via web_search_prime", "grade": "search"}
 ],
 "out_of_window_nearest": [
  {"signal": "GPT-6 Astra frontier model unveiled", "date": "2026-09-03/04", "source": "gulfbusiness.com via web_search_prime"},
  {"signal": "GPT-5.6 series (Sol, Terra, Luna) introduced", "date": "2026-09-11", "source": "openai community forum, mashable, scalevise via web_search_prime"},
  {"signal": "10GW Ohio data center lease locked with NVIDIA under the $500B Stargate program", "date": "2026-09-11", "source": "tutorsbot.com via web_search_prime"}
 ],
 "date_honesty_note": "All three in-window items are recency-marker-dated only; GPT-6.1 cancellation rests on one low-grade secondary outlet and is flagged, not asserted",
 "estate_angle": "A frontier lab pausing training and delaying releases over agent-security extends the local parity window and is market validation for receipts-first sandboxed agents; cloud agents that 'act before you ask' are exactly what a local agent estate replaces with its own meter",
 "handle_check": "org @OpenAI live-confirmed on fxtwitter (5,401,527 followers)",
 "sources": ["web_search_prime: 'OpenAI new model release announcement September 2026' (2026-09-29)", "web_search_prime: 'OpenAI announcement news September 20 2026 Stargate deal' (2026-09-29)", "web_search_prime: 'OpenAI delays model release security concerns paused training September 2026' (2026-09-29)", "api.fxtwitter.com/OpenAI (fetched, saved fxtw_OpenAI.json)"]
},
{
 "ts": TS, "writer": W, "watch_id": "org-anthropic", "name": "Anthropic", "org": "Anthropic", "lane": "models-org",
 "window": WIN,
 "in_window": [
  {"signal": "Claude Sonnet 5.5 released (date template in Wikipedia article reads start date and age 2026-09-28; byte-grep verified this session)", "date": "2026-09-28", "source": "https://en.wikipedia.org/wiki/Claude_(AI) (fetched, saved fetch_wiki_claude.html)", "grade": "fetch"},
  {"signal": "Claude Opus 5.5 released, first model of the Claude 5.5 series (byte-grep verified: start date and age 2026-09-22)", "date": "2026-09-22", "source": "https://en.wikipedia.org/wiki/Claude_(AI) (fetched, saved fetch_wiki_claude.html)", "grade": "fetch"},
  {"signal": "$11.6B seven-year cloud agreement with Akamai (Akamai issued Anthropic a warrant, expandable by ~$9B to ~$20B total; revenue from H2 2027, ~$5.5B capex incl. +$1.7B to 2026)", "date": "2026-09-24", "source": "https://www.akamai.com/newsroom/press-release/akamai-announces-11-6-billion-multi-year-agreement-with-anthropic-to-support-growing-demand + https://www.reuters.com/technology/akamai-anthropic-sign-116-billion-cloud-services-deal-2026-09-24/ via web_search_prime", "grade": "search (both URLs fetch-attempted this session and bot-blocked: akamai.com Access Denied, reuters.com 771-byte stub)"}
 ],
 "out_of_window_nearest": [
  {"signal": "Claude Fable 5.1 and Claude Mythos 5.1 released with system cards", "date": "2026-09-01", "source": "web_search_prime"},
  {"signal": "Anthropic reportedly shipping a major Claude release roughly every two weeks in 2026 (~29 distinct product updates)", "date": "2026 pattern, unpinned", "source": "web_search_prime"}
 ],
 "date_honesty_note": "Both model drops are fetch-grade byte-verified off the Wikipedia article; the Akamai deal is search-grade with the fetch attempt recorded as blocked (negative result recorded, claim rests on two concordant search-surfaced outlets including the issuer's own press-release URL)",
 "estate_angle": "A roughly biweekly frontier cadence outruns any quarterly local distill cycle, so a sovereign stack needs a standing distill pipeline or falls permanently behind; warrant-for-compute shows even labs pay equity for compute, so the only non-rented position is owned weights plus owned compute. Snapshot any open weights and licenses you depend on before flagship succession closes doors",
 "handle_check": "org @AnthropicAI live-confirmed on fxtwitter (1,762,668 followers)",
 "sources": ["web_search_prime: 'Anthropic Claude model release September 2026' (2026-09-29)", "web_search_prime: 'Anthropic Akamai $11.6 billion cloud deal September 2026' (2026-09-29)", "https://en.wikipedia.org/wiki/Claude_(AI) (fetched, saved fetch_wiki_claude.html)", "api.fxtwitter.com/AnthropicAI (fetched, saved fxtw_AnthropicAI.json)"]
},
{
 "ts": TS, "writer": W, "watch_id": "org-meta", "name": "Meta", "org": "Meta", "lane": "models-org",
 "window": WIN,
 "in_window": [
  {"signal": "Building a new enterprise business around its AI models and agents; hired MongoDB CEO CJ Desai to run it", "date": "2026-09-28 +/-1d (recency marker '1 day ago'; exact unpinned)", "source": "thenewstack.io via web_search_prime", "grade": "search"},
  {"signal": "Privacy reorientation of Meta AI strategy covered as 'Can you trust Meta with your AI data?'", "date": "2026-09-28 (URL-dated)", "source": "https://www.btpm.org/2026-09-28/can-you-trust-mark-zuckerbergs-meta-with-your-ai-data (fetched this session)", "grade": "fetch"}
 ],
 "out_of_window_nearest": [
  {"signal": "Muse personal AI agent announced as 'the world's first personal AI agent built for privacy'", "date": "2026-09-08", "source": "about.fb.com via web_search_prime"},
  {"signal": "Muse Spark reported as replacing the Llama herd as flagship (secondary aggregators, flagged)", "date": "2026-09 (early Sept, unpinned)", "source": "zapier blog, others via web_search_prime"},
  {"signal": "2026 capex guidance raised through the year to $130-145B including finance-lease principal (initial $115-135B on 2026-01-29); ~14GW AI compute planned by 2027 with in-house 'Iris' chip", "date": "2026 (raise month unpinned)", "source": "moneycontrol.com and others via web_search_prime"}
 ],
 "date_honesty_note": "The CJ Desai enterprise hire is in-window by recency marker only; the Muse Spark flagship-succession claim rests on secondary aggregators and is flagged, not asserted; capex raise month could not be pinned",
 "estate_angle": "Flagship succession (Llama herd to Muse Spark) plus an enterprise pivot is open-weights continuity risk: a sovereign stack should archive the weights and licenses it depends on now. The enterprise agents push validates the workflow-layer thesis, the estate's dashboard-plus-register bet",
 "handle_check": "org @Meta live-confirmed on fxtwitter (9,872,884 followers)",
 "sources": ["web_search_prime: 'Meta AI Llama news September 22 2026 announcement' recency oneMonth (2026-09-29)", "web_search_prime: 'Meta Llama model release capex September 2026' (2026-09-29)", "https://www.btpm.org/2026-09-28/can-you-trust-mark-zuckerbergs-meta-with-your-ai-data (fetched, saved fetch_btpm.html)", "api.fxtwitter.com/Meta (fetched, saved fxtw_Meta.json)"]
},
{
 "ts": TS, "writer": W, "watch_id": "org-google", "name": "Google", "org": "Google", "lane": "models-org",
 "window": WIN,
 "in_window": [
  {"signal": "DeepMind chief says Gemini 4 nearly ready for launch, prioritizing ship date over AGI quest, arrival expected long before end of 2026", "date": "2026-09-24 (recency marker '6 days ago')", "source": "aiincontext.com via web_search_prime", "grade": "search"},
  {"signal": "Reports of an internal Gemini 4 Pro checkpoint deployed ~2026-09-19 with public release expected October (secondary sources, flagged)", "date": "2026-09-19 (rumored, unpinned primary)", "source": "kocpc, emergent.sh via web_search_prime", "grade": "search"},
  {"signal": "Project Suncatcher prototype TPU satellite launch confirmed imminent (see lunch-sundar-pichai row)", "date": "2026-09-24 +/-1d", "source": "babushahi.com via web_search_prime", "grade": "search"}
 ],
 "out_of_window_nearest": [
  {"signal": "Google confirmed Gemini 4 pre-training started; no model or API yet (page currency marker 2026-09-17)", "date": "2026-07-21 confirmed / 2026-09-17 page currency", "source": "https://felloai.com/all-we-know-about-google-gemini-4/ (fetched this session)", "grade": "fetch"}
 ],
 "date_honesty_note": "The fetch-grade leg pins 'no Gemini 4 API' only as of 2026-09-17; the in-window items are recency-marker-dated search results, and the internal-checkpoint rumor rests on secondary outlets, flagged",
 "estate_angle": "An expected frontier jump inside weeks argues for pre-positioning the eval harness so the local router can re-rank models on landing; Suncatcher confirms compute scarcity at every scale, and the sovereign-stack answer stays terrestrial, small, and ownable",
 "handle_check": "org @Google live-confirmed on fxtwitter (31,897,921 followers)",
 "sources": ["web_search_prime: '\"Gemini 4\" OR \"Gemini 4.0\" Google release date September 2026' (2026-09-29)", "web_search_prime: 'Google Gemini new model release September 2026' (2026-09-29)", "https://felloai.com/all-we-know-about-google-gemini-4/ (fetched, saved fetch_felloai.html)", "api.fxtwitter.com/Google (fetched, saved fxtw_Google.json)"]
}
]

with open(REG, "a", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("appended", len(rows), "rows at", TS)
