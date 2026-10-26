---
name: x-tweet-extraction-endpoints
description: Verified chain for pulling full X/Twitter tweet text (incl. 280+
  note tweets) without JS — api.fxtwitter.com is the best endpoint; snowflake
  decode dates a status ID before fetching
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_fdec1d5f-1961-4cb6-b45f-9c612d3f6dff
---

x.com blocks plain fetches. Working chain (verified 2026-09-14 on an Obama note tweet, [shitpost desk run](shitpost-desk-workflow.md)):

1. **Best:** `https://api.fxtwitter.com/<user>/status/<id>` — full JSON: complete note-tweet text, created_at, views/likes/RT/quotes/replies/bookmarks.
2. `https://publish.twitter.com/oembed?url=...` — 301s to publish.x.com; returns author + date + truncated text (WebFetch must follow the redirect to publish.x.com).
3. `https://cdn.syndication.twimg.com/tweet-result?id=<id>&token=a` — JSON with engagement counts, verified badge, and a note_tweet ID, but text truncated at 275 chars.

Bonus: decode any status ID to its post time with snowflake math — `timestamp_ms = (id >> 22) + 1288834974657` — to check freshness before searching for context.
