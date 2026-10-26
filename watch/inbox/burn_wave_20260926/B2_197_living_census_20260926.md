# B2-197 living-law rollout census (2026-09-26)

## Verdict

LANDED with one owed alarm. Census of all 978 baseline INDEX items: 15 jsonl/log-like, 2 living (LINKS.jsonl, phone_relay_log.jsonl), 13 static. Byte-tested all 13 against their seals: zero were growing at census time, so re-classification followed writer evidence, not extension guesses. Migrated 3 true append-only originals to sealed living (EVENTS.jsonl, verb_trace.jsonl, quote_hitrate.jsonl) and first-registered 2 hot unregistered originals as sealed living (endpoint_news/endpoint_news.jsonl, mrpool_export/vision_nightly_receipts.jsonl), both cron-armed. Both verify gates agree: living_files {ok: 6, open: 1, unverified: 0}. During the lane, LINKS.jsonl took an unowned in-place edit inside its sealed prefix: LIVING PREFIX MISMATCH, correctly hard-failing; filed owed, not re-sealed.

## Evidence with file:line quotes

- mag/verb.py:73-74: "every verb row commits to its predecessor, so the trace is an append-only execution record, not a log"; :81 opens verb_trace.jsonl "a". Byte proof: 09-21 register sha matches newline-aligned prefix at byte 51,293 of today's 51,997.
- mag/link_library.py:21-25: event rows "mirrored with provenance into watch/inbox/EVENTS.jsonl ... New event filings go to EVENTS.jsonl"; mtime 12:31:49Z today; writers scout/seat/endpoint-news/x-intel-dig (B2-146).
- tools/quote_hitrate.py: run() opens jsonl "a", one row per run; rows 04:48Z and 04:52Z today.
- scripts/endpoint_news.py:158 opens NEWS "a"; :13 "append diff rows to ... endpoint_news.jsonl"; cron MagEndpointNewsDaily Ready daily 06:30; 112,154 bytes, never registered.
- scripts/vision_nightly.py:71 opens RECEIPTS "a"; cron MagVisionNightly Ready 02:30 nightly; 3,424 bytes, never registered.
- Stragglers named, not migrated: mimo_watch.jsonl (tools/mimo_watch.py:124 open "a"; 09-22 10:29 register sha matches prefix at byte 125 of 492: byte-proven appender, writer not cron-armed, dormant 4 days); MEMORY_GAUGE.jsonl (memory_gauge.py:93 open "a", 2 identical registers, frozen since 09-22); union_fullsend_20260917/queue.jsonl (amend-row growth ended 09-19); pricing_ratios_20260922.csv (5 registers in 3h on 09-22, one non-append content change then 4 identical refreshes: pure patrol papering, point-in-time table, correctly static); hot unregistered build_lane/proposals.jsonl (build_lane_game.py:431 open "a") and grounding_chain.jsonl (grounding_chain.py:37).
- Mid-lane alarm: LINKS.jsonl sealed 13:30:57Z over 219,904 bytes (index_events.jsonl:3091) verified living-ok at 13:46Z; by 13:55Z sha256(first 219,904) = A4EBE75D03673849 vs sealed 9DC30BDD31..., file 220,613 bytes; appends by writer zcode-seat-20260926 (tail row ts 13:42:56Z), in-place edit 13:46-13:53Z unattributed (row 256 anomaly is the documented B2-172 image-drop exception, ruled out); no register event follows; B2-199 receipt clause 4: "report and file as owed, never auto-refresh".

## Work done

1. Read whole: index_fold_host.mjs, verb.py, link_library.py; write sites of quote_hitrate, mimo_watch, memory_gauge, endpoint_news, vision_nightly, build_lane_game, grounding_chain; B2-156 and B2-146 receipts; LIVING_HASH_LAW sections 1-6.
2. Byte-level prefix tests (newline-aligned) over all 13 static jsonl/log items and all multi-register items INDEX-wide (7, all .md semantic rewrites, no append proofs).
3. Migrations via fold add only, writer zcode-b2-197-living-census, seqs 1789823567015749413-417; verify: 966 hash-clean, 6 living-ok, 1 living-open, 0 missing, 0 living-unverified of 982; validate ok-living 6/open 1/unverified 0.
4. Did NOT re-seal LINKS.jsonl (another writer's semantic edit; sealing unknown bytes would paper it) and did NOT migrate dormant append-shaped logs (living is writer-asserted, law section 3).
5. Self-fed B2-221/222/223.

## Falsifier

Dies if: appending to any of the 5 newly living files yields LIVING PREFIX MISMATCH or HASH MISMATCH on verify; EVENTS.jsonl or endpoint_news.jsonl shows an edit-shaped rewrite without a law-section-5 re-seal; MagVisionNightly or MagEndpointNewsDaily fires and the file stales; any migrated row lands in living-unverified; the LINKS prefix proof above does not reproduce.

## Bibliography closed

scripts/index_fold_host.mjs; mag/verb.py; mag/link_library.py; tools/quote_hitrate.py, mimo_watch.py, memory_gauge.py; scripts/endpoint_news.py, vision_nightly.py, build_lane_game.py, grounding_chain.py (write sites); INDEX.json (all 982 items swept); index_events.jsonl tails 3091-3104; LIVING_HASH_LAW_20260926.md; B2_156, B2_146, B2_199 receipts; QUEUE.md; schtasks MagEndpointNewsDaily/MagVisionNightly query output.
