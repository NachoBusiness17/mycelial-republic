# STEAL — X PRO HARVEST: how the field mines the deck (2026-09-04)

Competitive steal. The fleet has a Pro deck (Premium+); this is what power users —
OSINT analysts, investigative journalists, traders — actually run on it, so we adopt
their practice instead of inventing our own. Tri-state throughout; every claim sourced.

Headline finding: **the deck is not a dashboard, it is a set of STANDING QUERIES.**
The field's core discipline is query hygiene (paired raw/filtered lanes, column triage,
column death), and their harvest discipline is human-paced capture with archive-on-discovery.
The scraping-everything instinct is the ban pattern, and X has been losing the court cases
while winning the account bans.

---

## 1. SEARCH-OPERATOR CHEAT SHEET — what power users run in columns

Canonical reference: Igor Brigadir's twitter-advanced-search repo
(github.com/igorbrigadir/twitter-advanced-search) — the field's standard. Operators work
in X Pro columns, x.com search, and the search-URL form; supported by Bellingcat's toolkit
entry (bellingcat.gitbook.io/toolkit/more/all-tools/twitter-advanced-search). Supported:
these are documented and cross-confirmed across GIJN, Bellingcat, OSINTCurious, cheat sheets.
Harvest FOR = what it does in a deck-column harvesting context.

### People & reach
| Operator | FOR (harvest context) | State |
|---|---|---|
| `from:user` | Person lane — one author, standing column. The Profile-column primitive. | Supported |
| `to:user` | Conversation capture — everything aimed AT a target (replies, callouts). | Supported |
| `@user` | Mention net — third parties touching the target, wider than `to:`. | Supported |
| `list:owner/name` | Curated-set sweep INSIDE a search column: list + operators combined (`list:x/y filter:links`) — the pro move; our Tier kit as a queryable. | Supported |
| `filter:follows` | Chronological follows-only timeline, NO algorithm injection — the clean radar query. | Supported (OSINTCurious) |

### Time
| Operator | FOR | State |
|---|---|---|
| `since:YYYY-MM-DD` | Window start — event reconstruction, "what happened during X". | Supported |
| `until:YYYY-MM-DD` | Window end. Pairs with since: for the operational window (SpecialEurasia: reconstruct movement/sentiment in a window). | Supported |

### Engagement — THE volume valves (and the quiet lane)
| Operator | FOR | State |
|---|---|---|
| `min_faves:N` / `min_retweets:N` / `min_replies:N` | Signal lane — valve on high-volume streams (OSINTCurious example: `osint min_faves:8`). Counts approximate above ~1000 (ExportData). Dropped from API v2, STILL WORK in UI/columns (X devcommunity thread). | Supported |
| `-min_faves:N` (negation) | **QUIET LANE — the field's best trick.** Negation = CEILING: `-min_faves:10` finds posts with FEWER than 10 likes. Catches first reports and low-visibility signal before engagement exists (Brigadir repo; GIJN law below). | Supported |
| `retweets_of:user` | Amplification tracing — who is spreading a target's posts. | Supported |

### Content type
| Operator | FOR | State |
|---|---|---|
| `filter:links` / `-filter:links` | Citation lane vs chatter lane. Links are the steal substrate — the intake lane wants `filter:links`; `-filter:links` leaves pure commentary. | Supported |
| `filter:images` / `filter:native_video` | Primary-source lane — receipts: screenshots, event video, leaked docs. Feeds the visual-intelligence workflow (SpecialEurasia media-gallery forensics). | Supported |
| `filter:replies` / `-filter:replies` | Conversation capture vs broadcast-only. Default broadcast lanes with `-filter:replies -filter:retweets`. | Supported |
| `filter:quote` | Quote-dunks and quote-corrections — where context wars happen. | Supported |
| `url:keyword` / `url:domain` | Link mining — everything pointing at github.com, arxiv.org, a vendor changelog. Our WATCH-URLS as a live query. | Supported |

### Precision
| Operator | FOR | State |
|---|---|---|
| `"exact phrase"` / `OR` (caps) / `-word` / `()` | Query precision. OR-variants and **misspelling coverage** are GIJN's completeness law: query for misspellings of target keywords or you miss the whole picture. | Supported |
| `#hashtag` | Event/communion lane. GIJN's `#breaking` column: garbage-heavy but catches events 10-20 min before the wire. Passive watch. | Supported |
| `lang:xx` | Region sweep — e.g. `lang:ru` for Russia coverage when locals report first (GIJN; regime-monitoring practice). | Supported |

### Geo (sparingly!)
| Operator | FOR | State |
|---|---|---|
| `geocode:lat,long,r` / `near:"place" within:Xmi` | Event pinning to a place. **CAVEAT: cuts volume drastically and only ~8% of tweets carry location anyway** (OSINTCurious) — field treats geo as scalpel, never default. | Supported |

### Algorithm purge (the mute-words trick)
Mute-words list that strips X's algorithmic injections out of a timeline/home column:
`suggest_recap`, `suggest_activity`, `suggest_pyle_tweet`, `ActivityTweet`,
`RankedOrganicTweet`, `suggest_interaction`, `suggest_ranked_organic_tweet`,
`suggest_grouped_tweet`, `suggest_scroller_organic_tweet`, ` TweetDeck`.
Supported (OSINTCurious, 2019; widely re-cited since — operator names may drift, re-verify in-app).

### Fuzzy / Unproven
- `context:` (topic annotations) — exists in the X era, poorly documented, no field methodology found. Unproven.
- Column-level UI filters (likes:, member-of-list filters in X Pro column settings) — exist per Bellingcat/X help, exact current syntax in the rebuilt X Pro UI Unproven until we poke our own deck.

---

## 2. COLUMN ARCHITECTURE PATTERNS

### The OSINT triad (Gralhix regime-monitoring) — Supported
Only THREE column types are needed for monitoring:
1. **Lists** — content from a chosen set of users (local news, officials, journalists, NGOs). MUST be **private lists**: adding to a public list notifies the target ("sneaky is good"). Gralhix's deck = decks/groups of these; "a few dozen columns" starts lagging — soft ceiling.
2. **Searches** — standing operator queries, topic-based, account-independent.
3. **Profiles** — one target, optionally combined with keywords/hashtags.
Verify impersonators before trusting any account column.

### The journalist pattern (GIJN) — Supported
- Keep the **homepage column** (follows feed) as early-warning radar — curated by who you follow.
- One **`#breaking` hashtag column** for passive event catch (10-20 min head start, high noise).
- **Boolean precision**: quoted phrases, OR variants, misspellings.
- Column filters: content (mute words), **engagement (min-engagement as valve on high-volume streams)**, location (sparingly), users.
- **THE LAW: do not filter too early.** Watch the raw stream first, learn its noise profile, THEN add filters. First reports of a breaking event carry zero engagement — an engagement filter applied blind deletes exactly the signal you wanted. Consequence: **run the same query twice, adjacent columns — one RAW, one min_faves: — raw lane catches the first report, filtered lane catches the signal.**
- Column hygiene: clear-stream button (water drop) marks read; DELETE non-performing columns; be specific; mute spam accounts inside the column, not globally.

### The trader pattern — Supported
- Few columns, all real-time: wire/news lists, breaking hashtags, `$ticker` searches, official accounts (central banks, ministers). Amplify Trading's setup (Anthony Cheung, YouTube) and the r/StockMarket forex-stream guides agree on shape.
- **Triage by alerts, not watching**: the deck makes checking cheap; anything they can't watch gets a push/WhatsApp alert (crypto lane migrated to alert-first tools like Xanguard after the Premium+ paywall). The column is the queue; the alert is the pager.

### The X-Pro era specifics — Supported
Decks = named groups of columns (per investigation/theme); full composer; advanced search in columns; saved searches/lists/columns carried over from legacy TweetDeck (help.x.com/en/using-x/x-pro). Paywalled: Premium+ tier (~£47/mo).

### Cadence summary
Columns push in real time; nobody sane watches 24/7. Field cadence = check on a rhythm, alerts for the unwatchable, clear-stream as the read-marker, dead columns get deleted. Nobody reports a magic refresh number — the discipline is hygiene, not cadence.

---

## 3. HARVEST MECHANICS — getting data OUT, and the legal line

### What the field actually does — Supported
1. **Manual curation first**: bookmark + archive. SpecialEurasia: Wayback/archive.is capture **on discovery** is "required procedure for maintaining chain of custody" — posts delete fast; capture or lose it.
2. **Screenshot/DOM capture** for receipts (journalists archive before citing).
3. **Search-URL reuse**: a column query is a URL — the harvest artifact IS the query string, re-runnable, shareable. This is how OSINT shops hand investigations to each other.
4. **Bookmarks as training signal**: private, reversible, tunes the recommender — the quiet consensus move for researchers training their feed.

### Tooling that exists (GitHub) — Supported as existing; effectiveness varies
- **helmisatria/tweet-harvest** — Playwright CLI, scrapes search results to CSV by keyword/date range (MIT). The popular harvest CLI.
- **matteo-grella/tweetdeck-scraper** — Docker daemon continuously scraping deck columns into ElasticSearch + RabbitMQ queue. The continuous-harvest pattern — and the ban-magnet pattern (daemon-paced, not human-paced).
- **dimdenGD/OldTweetDeck** — resurrects the 2015-2018 client. Museum + fallback.
- **CIPHER387/OSINT_STUFF_TOOL_COLLECTION** — the field's tool index.
- Note: `min_faves`-family operators were **dropped from API v2** but live in the UI — meaning the UI/deck is now MORE capable than the cheap API. The deck is the good end of the pipe.

### The legal/TOS line — Supported
- X Developer Policy: scraping is "100% prohibited" under the Developer Agreement and ToS (docs.x.com/developer-terms/policy).
- **X Corp v. Bright Data (N.D.Cal., dismissed May 2024)**: X LOST the contract claim against scraping PUBLIC data — court held copyright law preempts ToS terms that restate copyright; no evidence Bright Data took nonpublic data. X's antitrust counterclaim exposure (Bright Data's Sherman Act claim) is still live. So: **public data via a real logged-in session is the defensible zone; bulk daemon scraping is ToS-prohibited regardless of court outcomes.**
- The practical line the field walks: ToS vs courts aside, **X enforces with account bans and rate limits** — and our lane is the operator's paid Premium+ account. Losing the deck to a ban costs £47/mo plus the trained graph. Human-paced browsing, bookmark capture, archive-on-discovery = field practice and our fair-use firewall agree.

---

## 4. FLEET MAPPING — which pattern becomes which organ

### ADOPT (Supported fits)
1. **The monitor (X_RESEARCH_KIT) <- Lists-as-columns.** Our Tier 0/1/2 handle kit becomes PRIVATE X lists, one per theme (steal-set, launch-watch, papers-first) — then `list:owner/name` queries let us sweep a tier WITH operators (`list:... filter:links`). Privacy law: never public lists (they notify targets — and our watch targets are exactly the people who'd notice).
2. **The scout (X_SCOUT_DOCTRINE) <- the operator cheat sheet becomes the scout's query genome.** Each standing research need = a standing query string (the harvest artifact IS the query), run raw + filtered. The mute-words purge goes into the scout's DOM-read path so the follows lane stays chronological. Numeric-user-ID pivot (SpecialEurasia) becomes scout identity policy: track IDs, handles are nicknames.
3. **The intake genome (research-socratic) <- engagement valve as PRE-intake cheap filter, with the GIJN guard.** `min_faves:` triage before spend — but never the only lane; the raw lane feeds intake un-valed, or we re-derive the field's own failure (deleting zero-engagement first reports) as fleet doctrine.
4. **Archive-on-discovery <- receipts law.** External receipts (posts) get archived (Wayback/archive.today) at intake time, before deletion. Chain of custody is their term for our receipts law.
5. **Column hygiene <- digest laws we already run.** Clear-stream = read-marker; delete non-performing columns = our handle-demotion/dedup gates; deck-per-theme = our environments. Convergent — steal the vocabulary, keep our gates.
6. **Watch-URLs upgrade**: our GH-Atom WATCH-URLS gains `url:github.com` / `url:arxiv.org` standing search columns — the field's link-mining query as a live pre-public radar.

### BAN PATTERNS (what we avoid — the field's own warnings)
1. **Daemon-paced harvest on the operator account** (the tweetdeck-scraper pattern). ToS-prohibited, ban-priced, and our scout doctrine already says human-paced. Third-party harvest daemons never touch the Premium+ account. Supported.
2. **Public lists.** They notify the target. Every source that mentions lists says PRIVATE. Supported.
3. **Blind engagement filters.** Kills first reports (GIJN). Never a single lane. Supported.
4. **Geo as default.** ~8% coverage, drastic volume cut; scalpel only. Supported.
5. **Automated actions** (posting/following/DMing under the handle). Scout doctrine already holds bookmark-only; field automation rules agree. Supported.
6. **Trusting the deck as archive.** X search is not a research database (coverage holes, algorithm drift, operator churn). The deck is a NET, not a STORE — everything worth keeping leaves the deck immediately (bookmark + archive + intake row). Supported by the whole field's capture discipline.
7. **Paying twice**: X Pro already gatekept behind Premium+; third-party "deck alternatives" that want our credentials (Xanguard-class) are credential-echo violations. Supported by law (never edit/echo own credentials).

### Open questions (Unproven, next poke)
- Current X Pro column-settings UI syntax (likes:, member filters) — verify in our own deck.
- `context:` operator behavior. — Whether the mute-words injection names still work post-rebuild.
- Whether decks export (column configs) — no tool surfaced; if the deck dies we lose the standing queries unless they live in a file. FLEET FIX: the query genome lives in OUR repo, deck is disposable.

---

## SOURCES
- GIJN, "How to Use TweetDeck for Open Source Investigations" — https://gijn.org/stories/how-to-use-tweetdeck-for-open-source-investigations/
- Bellingcat, "The Most Comprehensive TweetDeck Research Guide In Existence (Probably)" — https://www.bellingcat.com/resources/how-tos/2019/06/21/the-most-comprehensive-tweetdeck-research-guide-in-existence-probably/
- Gralhix, "How to monitor oppressive regimes on Twitter using TweetDeck" — https://gralhix.com/2022/12/17/how-to-monitor-oppressive-regimes-on-twitter-using-tweetdeck/
- OSINTCurious, "Muting the Twitter algorithm and using basic search operators for better OSINT research" — https://www.osintcurio.us/2019/08/01/muting-the-twitter-algorithm-and-using-basic-search-operators-for-better-osint-research/index.htm
- Igor Brigadir, twitter-advanced-search — https://github.com/igorbrigadir/twitter-advanced-search
- SpecialEurasia, "OSINT Tips: Investigating X" (2026-04) — https://www.specialeurasia.com/2026/04/22/osint-tips-investigating-x/
- X help, "About X Pro" — https://help.x.com/en/using-x/x-pro
- X Developer Policy (scraping prohibition) — https://docs.x.com/developer-terms/policy
- CNBC, "X loses lawsuit against Bright Data over data scraping" (2024-05) — https://www.cnbc.com/2024/05/10/elon-musks-x-loses-lawsuit-against-bright-data-over-data-scraping.html
- tweet-harvest — https://github.com/helmisatria/tweet-harvest · tweetdeck-scraper — https://github.com/matteo-grella/tweetdeck-scraper · OldTweetDeck — https://github.com/dimdenGD/OldTweetDeck
- Amplify Trading TweetDeck-for-trading (Anthony Cheung) — https://www.youtube.com/watch?v=venVF0UOoAQ · r/StockMarket forex stream setup — https://www.reddit.com/r/StockMarket/comments/dok0ml/
- Sorsa operator cheat sheet (2026) — https://api.sorsa.io/blog/twitter-search-operators · ExportData — https://www.exportdata.io/blog/advanced-twitter-search-operators/
- Bellingcat toolkit, Twitter Advanced Search — https://bellingcat.gitbook.io/toolkit/more/all-tools/twitter-advanced-search
