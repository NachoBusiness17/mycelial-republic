# BUBBLE-NET — the capture organ (spec v0, 2026-09-01)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: a notepad paste-surface plus a 30-min DS-Flash processor auto-organizes operator pastes at ~$0.0001 per 50KB without touching 5.3/main lanes — UNPROVEN (spec only, no run receipts in card) · falsifier: paste-stream tokens reaching 5.3/main, dupes surviving sha dedupe, or digest/ledger rows absent after processing

**Operator ask:** a local agent surface he pastes DeepSeek output, links, and thoughts into all day — auto-organized, deduped, meat stripped, applicable pieces routed. The prompt box is just a notepad file; treat it as one.

## The three parts
1. **THE NET** — `/board/capture_inbox.md`: one append-only paste surface. Any format. No rules. From Windows: the shared board path (notepad-friendly). Cursor = last processed line (tracked in /board/.capture_cursor).
2. **THE PROCESSOR** — cron lane, 30-min cadence, DS-Flash worker (never 5.3, never main):
   - reads lines after cursor
   - **dedupe**: sha256 each non-empty block; if seen in index_events or capture ledger → drop, log dup
   - **classify + strip**:
     - LINK → web_fetch extract → archive to /board/research/ with sha + 2-line abstract → digest line
     - DEEPSEEK DUMP (long model output) → distill: claims/decisions/numbers → /board/research/<topic>.md → digest line
     - ASK (question/directive shaped) → route: append to /board/STATUS.md open-questions or the owning card → digest line
     - JUNK/noise → hashed, dropped, digest line says so
   - updates cursor + ledger (/board/capture_ledger.jsonl: {ts, sha, class, disposition})
3. **THE TALKER** (separate rung): the local 7B seat (Bionic server) for unlimited chatter — the capture lane handles artifacts, the talk seat handles conversation, main handles judgment.

## Token economics
50KB paste → main: 0 tokens · processor: ~5K DS-Flash (~$0.0001) · digest: +1 line. The paste-stream cannot reach 5.3 or main — structurally, by routing.

## Laws it inherits
One-way mirror: personal content in pastes gets iso-reencoded before anything leaves the estate boundary. Creed: bytes archived with sha before anything is claimed. Two-strike per lane run.

## Rungs
- R0 (tonight): surface + spec + processor script + first cron fire. LIVE.
- R1: link-fetcher wiring (web_fetch inside the lane).
- R2: deepseek-dump distiller tuned on real dumps (learn the shapes).
- R3: talker seat wired to Bionic server once it's serving.
- R4: memlance grounding — the processor consults the sea before filing (dedupe against 47 decisions, not just hashes).

## Provenance
Operator directive 17:31Z: "we gotta start having a local agent i just talk to that i just paste deepseek shit into all day to then have it auto organize... the prompt box is just a notepad++ file that you can do whatever you please with." This is the bubble-net for the soap kingdom — the organ that catches blown bubbles so none pop unused.
