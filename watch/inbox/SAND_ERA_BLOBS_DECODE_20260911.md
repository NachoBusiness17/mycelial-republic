# SAND_ERA_BLOBS_DECODE_20260911

Lost-record dig, wave rotation width 2, lane: `conversation-blobs.db` decode.
Read-only except this file. Cards absorbed before the lane: `watch/inbox/RECORD_POOL_CENSUS_20260911.md`
(corpus stratum ranked #5 recovery value; docker-cp mtime caveat) and `watch/inbox/PREMAP_ARCHAEOLOGY_20260911.md`
(parts table, Aug 11-14 "sand" dating, per-agent DB layout, 0-byte wal/shm caveat).
Both DBs opened `immutable=1` read-only. All sample text redacted (key/token/hash patterns) — no secrets echoed; none surfaced.

## Targets

- GHOST: `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part5-conversation-blobs.db/agents/4a30dd44-e0bc-4e3c-af2a-13da6e62cef5/conversation-blobs.db` — 83,324,928 B
- RESEARCH: `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part3-conversation-blobs.db/agents/3d371c13-fcb5-43aa-b480-2260ca82cec9/conversation-blobs.db` — 6,201,344 B

## Schema map (identical in both)

```
TABLE blobs ( id TEXT , data BLOB )   + sqlite_autoindex_blobs_1 (unique on id)
```

One table, two columns, no indexes beyond the autoindex, no kv, no FTS. It is a
**content-addressed append-only blob store**: every `id` is a 64-char lowercase hex
string (SHA-256), 13,522/13,522 distinct in Ghost, 1,232/1,232 in Research. There
is no conversation/message/link table here — the id->position mapping lives in the
companion `store.db` (PREMAP parts 4/6), which references these hashes.

## Counts

| DB | rows | payload bytes | avg blob | max blob | <1KB / 1-8KB / 8-64KB / >=64KB |
|---|---|---|---|---|---|
| Ghost | 13,522 | 75,587,329 | 5,589 B | 2,144,443 B | 6,172 / 5,613 / 1,639 / 98 |
| Research | 1,232 | 5,558,508 | 4,511 B | 304,510 B | 665 / 406 / 150 / 11 |

## Content classes (sniffed on first bytes, full-table scan)

| Class | Ghost n | Ghost B | Research n | Research B | What it is |
|---|---|---|---|---|---|
| JSON | 5,948 | 49.8 MB | 532 | 3.9 MB | AI-SDK chat messages: `{content, id?, providerOptions?, role}`. Roles (Ghost): **tool 3,438, assistant 2,081, user 394, system 25** (Research: 310/168/50/3). |
| Protobuf | 7,158 | 25.7 MB | 649 | 1.6 MB | NOT gzip/zlib — protobuf wire format (leading `0a` field-1 length-delimited). Text embedded verbatim: `[SAND_HIDDEN_PROMPT][first run] This…`, `[t0] lmao`, `<system_reminder> Reply t…`, `# Deep research — all-seat re…`, `map-gaps`. Some carry a field-2 binary payload (metadata/timestamps). |
| utf8-text | 410 | 79 KB | 50 | 45 KB | plain text fragments |
| markup | 6 | 372 B | 1 | 62 B | html/xml scraps |

The tool-role dominance (58% of JSON messages) is the box's MCP surface working:
`ListMachines`/`ExternalShell`/`ExternalRead` tool results stored as first-class
messages — the outside-in fleet view PREMAP flagged, confirmed at message granularity.

Cross-agent proof of shared store: the SAME `[SAND_HIDDEN_PROMPT]` blob bytes appear
as an early row in BOTH DBs — content addressing dedupes the sand automation prompt
across agents.

## Date coverage (ISO-date regex over every blob, full scan)

- **Ghost: dense 2026-08-05 → 2026-08-16.** Day hits: 08-05:118, 08-06:135, 08-07:101, 08-08:308, 08-09:450, 08-10:958, 08-11:1284, 08-12:943, 08-13:1135, **08-14:3584 (peak)**, 08-15:394, 08-16:36. Then nothing.
- **Research: 2026-08-03 → 2026-08-14**, peak 08-14:686 (its one-day live era, corroborating PREMAP's 11:08→16:55Z store.db window).
- Stray 2023/2024/2025 and 2026-02/03 dates (~340 hits) are citations inside quoted
  memory/steal text, not separate conversations — corroborates PREMAP's histogram verdict.
- **The blobs DBs END Aug 14/16.** The Aug 17→Sep 5 tail (store.db transcript_entries to
  Aug 26; AFK sand runs to Sep 5) lives OUTSIDE these files. PREMAP's "whole-corpus Aug
  11 → Sep 5" is true of the archive, not of the blobs DBs specifically.

## Era reconstruction (what the 92-agent sand era is, per these DBs)

NOT 92 sessions in one table. These DBs are **per-agent**: one DB per box agent
(Ghost `4a30dd44`, Research `3d371c13`; New Bot `e99b7372` has none — stub). The
"92 agents" = 90 scheduled sand-subagent runners + Ghost + Research (PREMAP's census;
corroborated here byte-level by the sand markers). What the blobs DBs show of that era:

1. **Aug 5-10 warm-up** (Ghost only): operator + assistant turns ramping — the interface-agent era before the chord.
2. **Aug 11-14 = the sand peak**: heaviest message volume (Ghost 6,904 ISO hits across 4 days; Research's whole life is Aug 14), `[SAND_HIDDEN_PROMPT]`/`[SAND_TRUSTED_AUTOMATION_PROMPT]` bytes literal in the store, deep-research seat-steer content (`# Deep research — all-seat…`).
3. **Aug 15-16 shutdown taper**: 394 then 36 hits — the DB goes quiet; the record moves to store.db + AFK receipts.

So: the blobs DBs are the **raw message-body store of the Cursor-box interface agents**
— operator voice turns, assistant replies, system prompts, and 3,700+ MCP tool results —
covering the chord-strike week (Aug 11-14) and stopping at Aug 16.

## Tri-state recoverability verdicts

- **SUPPORTED — JSON class fully recoverable.** 5,948+532 standard message dicts; parseable with zero schema archaeology; tool results include the shell-command history of the fleet-from-outside.
- **SUPPORTED (with one small parser) — protobuf class recoverable.** Embedded UTF-8 is readable inline today; a ~30-line varint/length-delimited parser yields clean text + metadata. No compression, no encryption.
- **SUPPORTED — sand-era dating.** Byte-level sand markers + day histogram agree with PREMAP's Aug 11-14 window; two independent methods, one verdict.
- **DISPUTED — "the 92-agent era is in these DBs."** The DBs hold 2 agents' message bodies, not 92 sessions; the sand runners' transcripts live in `chat-transcripts/`+`produced/` (part1), not here.
- **DISPUTED — blobs coverage to Sep 5.** Hard stop Aug 16 (Ghost) / Aug 14 (Research); later era is store.db + receipts territory.
- **DISPUTED (as content-era) — pre-2026-07 dates.** Citations in quoted text only; earliest genuine conversational bytes are Aug 5 (Ghost warm-up), hard operator era Aug 11.
- **UNPROVEN — whether the box held chats before Aug 5.** Blobs are content-addressed and garbage-collectable; absence is not evidence of absence. PREMAP's "ghost downgrade Aug 7" reference stays open.

## Method note (for repro)

Python sqlite3, `connect("file:...?immutable=1", uri=True)` (PREMAP's wal/shm caveat honored). Pass 1: tables/schemas/counts/2-row samples + widest-column full scan (class sniff, size buckets, ISO-date histogram). Pass 2: id shape census, magic-byte histogram of non-JSON/non-gzip class, zlib probe (0 hits — it's protobuf), JSON shape + role census. Two Bash calls total on the lane.
