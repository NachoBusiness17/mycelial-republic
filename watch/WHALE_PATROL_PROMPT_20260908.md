# WHALE PATROL — automation arming prompt (paste into a FRESH chat to arm)

Why here: this session was itself a scheduled task, and ZCode refuses nested automations
(same lesson as the 23:00 night shift — sessions host automations, arm from a survivor/fresh chat).

Schedule: hourly (`0 * * * *`), recurring.
Title: "Whale patrol — hourly watched-channel harvest + ping"

---8<--- PROMPT (copy everything below) ---

WHALE PATROL round (hourly, operator order 2026-09-08: "harvest our watched channels automatically, feed and process, ping me when someone we watch posts so we can reply-guy them"). Repo: C:\Users\foste\Documents\projects\local_sovereign_agent.

STEPS:
1. Read configs/watched_channels.yaml for the watchlist (handles, lanes, notes).
2. Pull fresh posts (last ~6h) from watched channels: run WebSearch queries like: <handle> (GLM OR agents OR LLM OR "open weights" OR AI) site:x.com — batch 2-3 handles per query; prefer the freshest posts. If the in-app browser is available, prefer opening https://x.com/home (Following timeline) and reading the freshest posts from watched handles directly — that lane is real-time where WebSearch is lagged.
3. Dedupe: read watch/whale_tracker.jsonl — skip any post ID already tracked.
4. For each NEW in-lane post: track it: python -m mag.whale_patrol track --url <post_url> --handle <h> --counts "replies/rt/likes" --text "<first 200 chars>" --note "<which receipt-lane applies>". Then compose a draft reply in the @NachoQuixotic voice (lead with a take, deadpan, receipts-backed from the fleet's verified numbers: 15 workers/0 rejections, $0 flash-tier fleet, hash-chained ledger, 94.3% warm starts; under 280 chars; never harassing; tear down ONLY if falsifiable-and-false) and include it via --draft. Re-run feed: python -m mag.whale_patrol feed.
5. PING (only if any new post is fresher than 6h AND local EDT time is 08:00-23:00): python -m mag.whale_patrol ping "<handle> posted <age>h ago: <one-line what> — draft ready in the feed".
6. If nothing new: bank one quiet-round row in watch/room.jsonl and stop.
LAWS: never auto-post (the operator fires every reply himself); $0 spend, free lanes only; English only; secrets never echoed; bank every action to watch/room.jsonl.

---8<--- END PROMPT ---

Surfaces after arming:
- Feed: http://127.0.0.1:8088/whale_feed.html (auto-refresh 2 min; server re-arm:
  cd dashboard/static && python -m http.server 8088 --bind 127.0.0.1)
- Tracker: watch/whale_tracker.jsonl · census: python -m mag.whale_patrol census
- Algo-reverse-engineering loop: track at fire → observe +1h/+24h/+7d → census deltas
  → EDISON table says which reply shapes the algo carries.
