# BURN: stego-canon-pipeline (2026-09-26, _d)

## Verdict
steal

## Evidence
1. Ledger census (direct): watch/inbox/mrpool_export/ledger_full.jsonl, 3,663 rows, msg_id 1..4633, dates 2023-05-02..2026-09-18. memory/corpus/ holds no harvest index (only LINKS.jsonl and one prose file mention mrpool).
2. Identity: t.me/MrPool_Q/4633 shows the ledger msg 4633 text ("70 year cancer survivor Keith...") with identical timestamp 2026-09-18T14:27:47+00:00; MrPool_Q/4626 matches ledger 4626 (pyramids, 2026-09-15); MrPool_Q live anchors 4641-4660 continue past 4633; the export's own links.txt opens "https://t.me/MrPool_Q". The ledger is the @MrPool_Q channel.
3. The watched surface is a different channel: t.me/s/official_mrpool anchors 3804-3824 (3812, 3816 missing). Time attributes carry full self-dates 2026-09-19..09-26, fixing pass b's times-only caveat. At equal ids content is unrelated: ledger 3814 "GEORGE SOROS IS UNDER HOUSE ARREST" (2026-03-06) vs live 3814 "THE END IS NEAR" (2026-09-22).
4. Match test: 20 pre-harvest Official_MrPool anchors hit ledger rows at 2-5/5 text windows. Offset ledger_id minus anchor_id drifts +805..+845 (anchor 3682/08-17: +816; anchor 3791/09-15: +835); ledger dates usually +0..+5d, outliers both ways (live 3740/09-02 matches ledger 4384/07-22).
5. Both channels title themselves "Mr. Pool": MrPool_Q 62.2K subscribers, Official_MrPool 92.5K (fresh fetches today).
6. Fresh web search returned zero relevant late-September results.

## Steal or Vacuous
Steal: the anchor cross-check table plus the mapping rule. Mapping rule: ledger msg_id IS the @MrPool_Q anchor (zero offset, timestamp-identical). @Official_MrPool is an independent sequence, no constant offset (drifts +805 to +845); resolve pairs by content plus self-date, never id arithmetic. Pass c named the hazard but mis-modeled the cause: not an export-tool renumbering, two sibling channels sharing one persona name. Consequences: dictionary entries must cite handle plus anchor ("MrPool_Q/4384", "Official_MrPool/3820"), never a bare msg_id; delta harvest must target both surfaces (MrPool_Q 4634-4660 is 27 posts past the ledger; Official_MrPool 3825 onward is unharvested).

Table (anchor | self-date | ledger msg_id | verdict):
Official_MrPool/3824 | 2026-09-26 | none, post-harvest | no-match
Official_MrPool/3820 | 2026-09-24 | none; recycled kin 4384 (07-22) | no-match
Official_MrPool/3815 | 2026-09-22 | none | no-match
Official_MrPool/3814 | 2026-09-22 | 3814 unrelated (03-06) | id collision
Official_MrPool/3804 | 2026-09-19 | 3804 unrelated (03-03) | id collision
Official_MrPool/3791 | 2026-09-15 | 4626 | match, +835, 0d
Official_MrPool/3753 | 2026-09-06 | 4595 | match, +842, +4d
Official_MrPool/3682 | 2026-08-17 | 4498 | match, +816, +2d
Official_MrPool/3740 | 2026-09-02 | 4384, 4/5 windows | partial, -42d
MrPool_Q/4633 | 2026-09-18 | 4633 | exact identity

All content claims are corpus claims, not fleet facts.

## Falsifier
Pre-registered: a verified pair at zero id offset across surfaces (any Official_MrPool anchor equal to its ledger twin's msg_id) falsifies the independent-sequence rule and collapses both spaces into one channel with deletions.

## Bibliography
1. watch/inbox/BURN_stego-canon-pipeline_20260925.md, _b, _c (read)
2. memory/corpus/MANIFEST.md (read); canon/podcast_corpus/ (ls only)
3. watch/inbox/mrpool_export/ledger_full.jsonl (census, sampled rows)
4. watch/inbox/mrpool_export/HARVEST_COMPLETE.json, links.txt (read)
5. https://t.me/s/official_mrpool fetched 2026-09-26, plus before-pages 3782..3682
6. https://t.me/s/MrPool_Q fetched 2026-09-26, plus before=4641
7. Web search "Mr Pool telegram channel posts late September 2026" (no relevant results)
