# ROW · atlas-g1

## ROW A — runs-family exact counts/mtimes
- **pointer**: /mag/memory/runs/{family}
- **claim**: /mag/memory/runs holds 449 entries total; per-family file counts + newest mtimes:
  - riddler: 113 · 2026-08-31 04:54:23
  - seat_corpus: 1 · 2026-08-29 17:46:05
  - openclaw_catalog: 5 · 2026-08-29 21:40:58
  - campaign: 163 · 2026-08-30 21:59:30
  - game_grok_night: 11 · 2026-08-27 07:16:14
  - swarm_worker: 7 · 2026-08-27 13:31:21
  - ask_router: 5 · 2026-08-31 04:54:29
- **type**: gopher · **confidence**: H · **status**: VERIFIED
- **evidence**: `ls /mag/memory/runs | wc -l` = 449; per-family `ls | wc -l` + `stat -c '%y'` outputs above (read-only).

## ROW B — elder_brief.md
- **pointer**: /mag/memory/runs/openclaw_catalog/elder_brief.md
- **claim**: mtime 2026-08-29 21:40:35. Top 3 sections by header lines: `# Elder review pack — 2026-08-29` (H1), `## Law`, `## Built this window (receipts)`. Head begins: "Elder review pack — 2026-08-29 ... You are DeepSeek, Mag's elder..." — covers Law (OpenClaw Control UI :18789 hypervisor, ONE mutator, supervisor/falsifier, Grey Swan Arena, conservation to 2026-09-02) and built-window receipts (TEN STEPS hypervisor).
- **type**: gopher · **confidence**: H · **status**: VERIFIED
- **evidence**: `stat -c '%y'` + `head -c 800` + `grep '^#'` (read-only).
