# CONTEXT HOG AUDIT — agent:main:main — 2026-09-01

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: tool-result payloads dominate the main-agent context window (~57% of session bytes, driven by untrimmed board-file reads and config echoes) — SUPPORTED (byte-level parse of the 285-event rollover transcript JSONL) · falsifier: re-parse of the same transcript showing tool-results well under half of session bytes

Method: parsed main-session transcript JSONL at the 100%-context rollover boundary.
Target file: `64543440-8a1e-4432-86e4-3e57a26d74d0.jsonl` (285 events; the file that
carries the `compaction` event firing at 2026-09-01T06:39:24Z). Session `sessions.json`
shows `compactionCount: 1` and a 4-member `usageFamilySessionIds` rollover chain
(1546d5f5→cb581a7c→a25cc707→64543440). Historic `.jsonl.reset.*` files confirm the
100%-full rollover recurs (08-30, 08-31, 09-01T04:03, 09-01T06:39).

Compaction marker text: "Context contained 213 messages (0 oversized). Summary
unavailable due to size limits." — = the 100% window hit.

## 1) Bytes per class (this session)
- assistant-text : 285,701 B  (100 msgs / 89 with embedded toolCall blocks)
- tool-result    : 450,409 B  (142 msgs)  ← DOMINANT
- user           :  27,486 B  (21 msgs)
- completion-event:  11,253 B (1 compaction)
- runtime-event  :   5,499 B  (21 custom/session/model events)

## 2) Top 15 messages by bytes (index, type, bytes, slug)
- #114 tool-result 18967 [gateway] {SLOT/config block echo
- #11  tool-result 18556 [read] MEMORY long-term doc
- #42  tool-result 17267 [exec] AUDIT_A_ATTEMPTS file body
- #15  tool-result 16233 [exec] SURFACES fleet doc
- #10  tool-result 15765 [exec] ls/stat listing
- #51  assistant-text 15445 Catalog confirms memory…
- #33  tool-result 14320 [cron] {config dump
- #34  tool-result 14304 [cron] {config dump
- #13  tool-result 14153 [read] {config doc
- #232 assistant-text 13761 Tonight's receipts-first answer…
- #53  tool-result 13271 [cron] {config dump
- #50  tool-result 12830 [exec] top keys: ok,schema,ts,law…
- #79  tool-result 11808 [workboard_complete] {ticket echo
- #235 assistant-text 11405 Both workflows already filed…
- #284 completion-event 11253 [compaction event]

## 3) Top recurring hog patterns
1. **exec stdout/stderr dumps** — 49 calls, 148,331 B. Full-file board docs
   (AUDIT_A 17KB, SURFACES 16KB, ls listings) re-cat'd into context each turn.
2. **ToolResult payload echoes** — 142 tool-result msgs = 450KB (57% of session
   bytes). Config blobs (gateway 18.9KB, cron x3 ~14KB each, workboard_complete
   11.8KB) re-injected unchanged + assistant re-echoes them.
3. **Assistant text blocks carrying toolCall JSON** — 89 msgs / 275,404 B. Large
   tool-argument JSON and verbose prose stay resident across every turn.
4. **Long config/state reads re-fetched repeatedly** — 11 read (70KB) + 11 cron
   (72KB) + 7 gateway (22KB): same SLOT/config boards re-loaded turn after turn.
5. **Recurring compaction rollover** — family chain rolls a new session each time
   the window fills (4 rollovers in <24h); current one fired @06:39:24Z with 213
   messages, summary dropped ("unavailable due to size limits").

## Verdict
Window maxes on **tool-result payloads (~57%)**, driven by re-injecting full board
files (exec/read of AUDIT/SURFACES/MEMORY) and config echoes (gateway/cron) that
never get trimmed, with verbose assistant re-echoes compounding it.
