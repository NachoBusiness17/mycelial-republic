---
name: corpus-harvest
description: Harvest any public corpus at full fidelity (text, timestamps, media, reactions, reply chains) with a receipt register for every item including failures. Use when the operator wants a channel, subreddit, site, or archive pulled and registered rather than skimmed.
---

# corpus-harvest

Harvest any public corpus at full fidelity: text, timestamps, media, reactions, and
reply chains, with a receipt register for every item including failures.

## The four paths

1. TELEGRAM (channels): authorized Telethon session (QR login once, session file
   kept). `iter_messages` walks full history. Capture: text (untruncated), date,
   edit_date, views, forward provenance, reactions as emoji-count pairs, reply
   counts, media type + `msg.file.size` (byte size enables cache matching later).
   Download media with paced `asyncio.sleep` between items. NEVER pass a `sleep`
   kwarg to `download_media` (TypeError; it reads as a protocol block when it is
   your own bug). Set each recovered file's mtime to its post date (`os.utime`).
2. CHAN / BOARD MIRRORS: find the canonical JSON superset first (e.g. qanon.pub
   `data/json/posts.json`: id, source board, threadId, link, unix timestamp, trip,
   full text, media[], NESTED references = the reply chain). If original media
   hosts are dead, the living mirror is usually IN THE SITE'S OWN ASSET PATHS:
   render the search UI and read its img srcs (qagg.news bakes every drop at
   `siteimages/qaggdropimage<N>.png`, keyed by canonical drop number, zero gaps).
   The site that still displays the corpus is the site that still hosts it.
3. REDDIT: the reddit.com JSON API rejects scripted access (403). Use arctic-shift,
   the Pushshift successor: `https://arctic-shift.photon-reddit.com/api/posts/search?author=<name>&limit=100&before=<epoch>`
   (descending `before` cursor, reverse at the end; `comments/search` the same).
   Media on i.redd.it / preview.redd.it is alive; download and stamp mtimes.
4. X/TWITTER: `https://api.fxtwitter.com/<user>/status/<id>` returns clean JSON
   (text, author, stats, media refs) for public tweets. Does not surface reply
   chains. No auth needed.

## Register discipline (every path)

- One JSONL row per item: source URL, original filename, sha256 (16-hex is enough
  for corpus work), bytes, TRUE timestamp (post date, not harvest date).
- Failure rows are data too: record url + error class. Never silently skip.
- Host validation on every request: http/https only; reject localhost, private,
  reserved, and non-global IPs. Onion hosts are out of scope by law.
- Pace bulk downloads (0.2 to 0.4s sleep), run as background passes, log milestones.
- Forensics before retry: classify failures first. DNS nxdomain = host migrated or
  dead (find the successor or the site-internal mirror). TCP-dead = host gone.
  403 = hotlink block (try browser UA + referer once, then declare). Tor-only =
  declared out of reach. Do not retry dead DNS hoping.
- At the close: reconciliation table against the source's own counts (channel
  media totals, drop numbering), and a RECEIPT.json with stats + recovery queue.

## Fleet integration

- Durable landing: `watch/inbox/<corpus>_export/` (ledger, media_full,
  media_register.jsonl, RECEIPT.json) + a LINKS.jsonl row.
- Analysis pairs with the worldline-lens instruments (tools/drift.py): define each
  corpus's cliff scalar BEFORE analyzing (countdown density, cadence surges,
  reaction signatures of called shots vs fades).
