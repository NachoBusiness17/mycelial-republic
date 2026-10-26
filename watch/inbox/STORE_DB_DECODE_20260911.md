# STORE_DB_DECODE_20260911

Wave dig, zcode seat. Decodes the "other database" of
`corpus/oral_history/nacho_archaeology/`: the three `store.db` files, cross-read
against the two `conversation-blobs.db` files. Read-only; opened every DB
`immutable=1` URI (no wal/shm mutation). Absorbed: `RECORD_POOL_CENSUS_20260911.md`
(row 21 + tri-state notes), `PREMAP_ARCHAEOLOGY_20260911.md` (parts table, spans,
speaker map), `TRANSCRIPT_MAP.txt`, `MANIFEST.json`. This card extends PREMAP from
counts to schema/content-class decode. No secrets echoed: one kv value
(`metadata.blobEncryptionKey`) exists in all three agents and is named but never
printed here.

## Files (all under extracted/, one DB per agent UUID)

| Part | Agent | DB bytes | Created (metadata.createdAt) | Identity |
|---|---|---|---|---|
| part4 | 3d371c13-fcb5-43aa-b480-2260ca82cec9 | 327,680 | 2026-08-14 11:08:45Z | "Research" (display name; metadata/profile snapshot say `name: New Agent`, profile title `New Bot` — renamed after creation) |
| part6 | 4a30dd44-e0bc-4e3c-af2a-13da6e62cef5 | 2,199,552 | 2026-08-12 03:25:24Z | "Ghost" (snapshot profile title `Ghost`) |
| part7 | e99b7372-dc3b-40c8-a81d-9811b8d03275 | 49,152 | 2026-08-12 03:23:41Z | New Bot shell — created 2 min before Ghost, never used, 0 transcripts |

Note: part7 (e99b7372) and Research (3d371c13) are DIFFERENT UUIDs both titled
"New Bot" in their snapshots — part7 is a dead sibling shell, not an earlier
version of Research.

## Schema map — identical 4 tables in all three store.db

```
automation_completion_inbox(seq INTEGER, id TEXT, text TEXT, attribution TEXT, acknowledged INTEGER)
blobs(id TEXT, data BLOB)                       -- EMPTY in all three
kv(key TEXT, value TEXT)                        -- hex-encoded + plain JSON state
transcript_entries(seq INTEGER, id TEXT, entry TEXT)  -- entry = JSON per turn
```

### Row counts

| Table | part4 Research | part6 Ghost | part7 New Bot |
|---|---|---|---|
| transcript_entries | 132 | 1,097 | 0 |
| kv | 10 | 10 | 3 |
| automation_completion_inbox | 0 | 60 (all unacknowledged) | 0 |
| blobs | 0 | 0 | 0 |

### transcript_entries content classes (entry JSON `kind`)

| kind | part4 | part6 | meaning |
|---|---|---|---|
| message | 40 | 282 | user turns (plain text + richText doc) |
| send-message | 91 | 794 | agent turns |
| user-attachment | 0 | 18 | pointers to `/home/box/sand-data/agents/<uuid>/attachments/<64-hex>.png` |
| event | 1 | 3 | `automation-changed` created/updated for `AFK game chord` (2026-08-14 15:58Z — matches PREMAP's automation creation time exactly) |

### kv content classes (10 keys; values JSON or hex-JSON)

- `metadata` (hex-encoded JSON): `agentId, latestRootBlobId, name("New Agent"), createdAt, mode("default"), isRunEverything, blobEncryptionKey`. `latestRootBlobId` hex-decodes to the sentinel `sand-live-conversation-root-v1__` — "sand" is the product namespace (cf. `SAND_HIDDEN_PROMPT` transcripts and `/home/box/sand-data/` paths). `blobEncryptionKey` present in ALL three agents = blob payloads are keyed; values never echoed here.
- `memoryPromptSnapshot`: `{render, compactionEpoch}` — Ghost's 15.4 KB render opens "User memory: durable facts shared across every assistant this user runs" — the shared-memory covenant in its live form (PREMAP item 7, now schema-confirmed).
- `agentProfilePromptSnapshot`: the agent's own profile text at snapshot time.
- `episodePending`: un-episodized recent turns (ts, user, agent triples).
- `requestIds`: the ACTIVITY LEDGER. Ghost has 200 entries, Research 77. Fields by source: `turn` entries carry the operator's raw prompt text; `automation` (32), `web-search` (83), `web-fetch` (80), `handoff-resume` (3) carry id/at/source only.
- `conversationPartners`: the OTHER agent's UUID — Research ↔ Ghost are wired to each other.
- `unreadState`, `origin`, `hiddenEntryRepairVersion`, `staleRootCleanupVersion`: housekeeping.

## Date spans (entry timestampMs, UTC)

| DB | Span | Daily histogram |
|---|---|---|
| part6 Ghost transcript | **2026-08-12 03:26Z → 2026-08-26 16:58Z** | 08-12: 71, 08-13: 4, **08-14: 685** (strike-the-chord day), 08-15: 206, 08-16: 112, 08-26: 1 |
| part6 Ghost kv.requestIds | **2026-08-16 15:42Z → 2026-09-04 00:29Z** | 08-16: 5, 08-17: 11, 08-18: 11, 08-26: 8, 08-27: 27, 08-28: 40, 08-29: 3, 08-31: 31, 09-01: 28, 09-02: 26, 09-03: 9, 09-04: 1 |
| part4 Research transcript | **2026-08-14 11:08Z → 16:55Z** (one day) | 08-14: 132 |
| part7 New Bot | none | lastViewed 2026-08-12 03:25Z |

## What conversation-blobs.db holds (comparison)

Single table `blobs(id TEXT, data BLOB)`: part3 (Research) 1,232 rows / 6.2 MB;
part5 (Ghost) 13,522 rows / 83.3 MB. IDs are 24-hex content keys. Head-sample
(3,000): 1,692 non-JSON — mostly protobuf-framed (`0x12`/`0x0a` field tags,
possibly encrypted per `blobEncryptionKey`); 774 `role:"tool"` tool-results;
442 `role:"assistant"` provider payloads; 83 `role:"user"`. Model census in
assistant payloads: **cursor-grok-4.6-high-fast ×373, cursor-grok-4.5-high-fast
×14, cursor-grok-4.6-high ×9**.

## VERDICT

1. **store.db is the agent's state+index+timeline store; blobs is the payload store.** The `blobs` table inside store.db is EMPTY in all three — payload bytes live exclusively in conversation-blobs.db, addressed by 24-hex keys, with `metadata.latestRootBlobId` in store.db as the root pointer into that DAG. So: it is BOTH an index (pointers, kv state, activity ledger) AND the plain-text message store (transcript_entries are full inline conversation turns), while blobs holds the machine-layer provider messages (reasoning, tool results), protobuf-framed and keyed.
2. **What store.db has that blobs does not:** the human-readable timeline; the operator's raw turn prompts (`requestIds[turn].prompt`); the automation completion inbox (60 unacknowledged AFK receipts — the "desk offline" failure record); the memory/profile snapshots; the partner wiring; the activity ledger of web-search/web-fetch/automation ticks.
3. **Era: 2026-08-12 → 2026-09-04.** Transcripts end Aug 26, but Ghost's requestIds prove the box kept firing automation + web-search/web-fetch requests through Sep 4 — INCLUDING Aug 27–Sep 2 (27/40/31/28/26 requests/day), i.e. the box side of the fleet's Aug 16-31 silence, from an independent machine. The blob-side content covers the same span (PREMAP histogram: 2026-08 dominant).
4. **Model identity: PREMAP said UNPROVEN — now SUPPORTED.** Provider payloads in part5 blobs carry `cursor-grok-4.6-high-fast` (373 hits) as the runtime modelName — the Ghost box ran on Cursor's grok-4.6 lane. The archive's "Nacho Grok Bot" title is corroborated at the payload layer, not just the title layer.
5. **Record value: HIGH, second only to the transcripts themselves.** The census's "recovery = re-mining, not discovery" holds for the chat text, but store.db's `requestIds` activity ledger and the AFK completion inbox are NOT in the transcripts or TRANSCRIPT_MAP — they are a separate day-by-day record of the box's silent-era behavior. Recovery priority: dump Ghost requestIds timeline + the 60 inbox receipts as text; that is new surface, cheap to mine, zero secrets risk beyond existing redaction hygiene (blobEncryptionKey stays sealed).
