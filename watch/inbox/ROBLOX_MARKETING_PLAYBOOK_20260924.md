# Roblox Marketing Playbook — research receipt (2026-09-24)

Scope: how Roblox devs actually launch and grow games, verified against Roblox's own creator docs plus 2025-26 case coverage. Sources checked 2026-09-24.

## 1. The algorithm (official, verifiable)

Roblox's [Discovery doc](https://create.roblox.com/docs/en-us/discovery) confirms Home "Recommended for You" is two-stage: **retrieval** (small games qualify; ads/search/social speed up consideration) then **ranking driven ONLY by organic Recommended-for-You engagement** — paid, search, friend, and social traffic does not count toward ranking. Top signals, in the doc's own priority order:

- **Play-through rate (CTR)** — viewers who see the tile and play
- **First-play bounce rate** (negative) — sessions under 60s and 61–180s
- **Play days per user** — D1, D2–7, D8–28 buckets
- **Playtime per user** (capped 60 min/day)

Secondary: intentional co-play days, qualified sessions, spend days. All signals are **per-user averages**, so tiny games with engaged players are not disadvantaged. Updates trigger an explore/expand cycle: a content update spikes impressions ("explore"); if the new cohort retains, distribution expands. Analytics > Acquisition > Home Recommendations shows your own numbers. Explicitly penalized: "Robux!/giveaway" hooks, copied icons/metadata, trend-clone games.

## 2. Launch playbooks from breakouts

- **Doors (LSPLASH/RediblesQW, 2022):** grew via Roblox YouTuber/streamer seeding (KreekCraft, Thinknoodles) plus jump-scare clips going viral on TikTok/Shorts; platform promotion followed ([creator documentary](https://www.youtube.com/watch?v=RQ6MVKFhGdk), [co-creator interview](https://www.youtube.com/watch?v=VyBSvWSIkao)).
- **Dress to Impress (Gigi, 2023):** TikTok-native format — outfit reveals and runway fails are self-clipping; update-hype cycles, lore events, celebrity plays, brand collabs ([Vogue](https://www.vogue.com/article/roblox-dress-to-impress-grown-ups), [wiki stats](https://dti-dress-to-impress.fandom.com/wiki/Gigi)).
- **Grow a Garden (2025):** 16-year-old's idle loop, scaled by Jandel's team; record CCU (16–22M) rode organic Shorts clips of rare mutations plus very high update velocity ([GamesBeat](https://gamesbeat.com/janzen-madsen-interview/), [NYT](https://www.nytimes.com/2025/06/17/arts/grow-garden-roblox-record.html)).
- **Steal a Brainrot (2025):** meme IP + steal-from-others social loop; 25.4M CCU, all-time record ([coverage](http://www.mi-3.com.au/site/news/roblox-garden-brainrot-games-set-new-records-in-2025)).

Common thread: **shareable moments designed into the game + fast updates** did the marketing; paid ads were secondary for every breakout.

## 3. Icon/thumbnail craft

Official [icon guide](https://create.roblox.com/docs/en-us/production/publishing/experience-icons): 512×512, legible at ~150px, theme-clear, unambiguous imagery, use color/contrast for tone. Official [thumbnails guide](https://create.roblox.com/docs/en-us/production/publishing/thumbnails): 16:9 at 1920×1080, up to 10, video thumbnails (3/month quota, real gameplay only, no fake mechanics/VO). **Roblox's own A/B data: activating 2–5 thumbnails enables Thumbnail Personalization, averaging +8.5% qualified play-through lift (some games +50%); keep multiple live and refresh with updates.** Practitioner consensus (e.g. [creatorxp](https://creatorxp.gg/guides/roblox-game-icon-mistakes), [vizzbees](https://vizzbees.com/blog/how-to-make-a-roblox-thumbnail)): one clear subject, expressive face, high contrast/saturation, no or minimal bold text, readable at small size.

## 4. Off-platform traffic

2024–26 breakouts were all carried by TikTok/YouTube Shorts, not by ads. Practical pipeline: design 3–5 clippable moments (chases, reveals, rare drops, fails), post daily short-form devlogs/clips, funnel bio links to the game and Discord. Discord converts viewers into returning players (update pings); it is retention infrastructure, not discovery. Social links on the game page (max 5; publicly visible only from **13+ ID-verified** accounts) per [official docs](https://create.roblox.com/docs/en-us/production/promotion/social-media-links). A Roblox Group (free member feed, group-game momentum) is standard distribution.

## 5. Paid ads

Legacy "sponsored experiences" are gone; [Ads Manager](https://create.roblox.com/docs/en-us/production/promotion/ads-manager) is the only channel: up to 10 16:9 creatives, automated bidding (you set budget/duration), 24h Learning phase, 48h attribution lag. Goals: Plays (cheapest), Earnings, Engagement (higher cost-per-play, smaller audience). Community-reported costs (July 2025 [DevForum thread](https://devforum.roblox.com/t/urgent-new-ads-manager-is-delivering-significantly-less-plays-than-before/3694225)): roughly **$0.10–0.30 per play**, sometimes $0.10–0.15; expect ~500–2,000 visits from a $100–300 test. Only pay after organic signals (CTR, bounce) look sane — ads amplify whatever retention you already have.

## 6. Community infrastructure at launch

Roblox Group (payouts, ads permission, member feed) · Discord with Bloxlink verification and update-ping roles · social links set · Experience Events + notifications for update announcements ([docs](https://create.roblox.com/docs/en-us/production/promotion/experience-events)) · in-game voting/roadmap teasers to manufacture update hype (the DTI/GaG engine).

## Checklist

**Day 1:** replace default icon (512×512, face + contrast); upload 3–5 16:9 thumbnails and enable personalization; create Group + Discord (Bloxlink) and link via social links; write honest title/description (no "free Robux" bait); seed 10–30 friends/playtesters for first-session data; set up Analytics baselines.

**Week 1:** post daily short-form clip (1 game moment each); ship first update and announce via Experience Event; open a $50–150 Plays campaign for 3–4 days, judge CTR/bounce not vanity visits; watch Home Recommendations tab — if bounce >~40% at 60s, fix onboarding before more spend.

**Week 4:** ship update #3–4 (velocity = explore cycles); enable invite prompts + notifications opt-in; run a community event/vote; double ad budget only if CPP < ~$0.25 and D1 holding; repurpose best clips into YouTube Shorts compilation; document what moved play-through rate and do more of it.

---
*Receipt: research via create.roblox.com official docs (fetched 2026-09-24) + web sources above. All URLs live at check time.*
