# Daily compute plan — drain the free wall every day · 2026-09-24

*Operator: "we have so much free shit now, how do we use it — we have the stealth
models and all these free lanes, we need to use this compute everyday."*

## The standing daily burn (automatic, 09:00–09:50)

| time | task | what it burns | status |
|---|---|---|---|
| 09:00 | Estate Spine Index | local CPU (~7 min, 1.2M files) | live, Result 0 daily |
| 09:15 | Estate Librarian | local CPU + canon audit | live, Result 0 daily |
| 09:25 | Estate Gopher | z_ai Lite pool #2 (label farm; ~0.14 credits/day = ~0% of pool) | live, Result 0 daily |
| 09:35 | Estate FullScan | deepseek + **groq gpt-oss-120b ×2 keys** (fixed today from dead llamas) + more; 2,473 records re-queued; ~944/4,129 briefed | live, Result 0 daily |
| 09:45 | Estate KeyAudit | none (audit) | fixed today, Result 0 |
| **hourly :10** | **Estate Cooker** | fires any pool refill the moment it lands: openrouter free wall sweep + 15-min task-wall burst daily 00:00Z; z_ai Lite meter read Sat 02:19Z (never auto-rearm) | **registered Ready today, first fire proven** |
| **09:50** | **Estate StealthSweep** | **OpenRouter free wall: 1 stealth + 20 free lanes/run, scored chore, cursor rotates the whole wall across days** | **registered Ready today** |

## The idle capacity (what's wired and waiting for demand)

- **openrouter a1 + a2** — 114.9 tok/s light champion + 48.1 heavy-capable; task-wall lanes
- **deepseek-chat** — 70.4 tok/s workhorse, 5/5 correct in bake-off
- **nvidia glm-5.3-flash** — 12.8 tok/s heavy carrier; NVIDIA's 102-model catalog still only ~3 wired (untapped depth)
- **groq gpt-oss-120b + 20b** — verified today post-rotation; 229–407ms; 2–4× cheaper than the dead llamas; now also cache-read priced
- **together DeepSeek-V4-Flash-0731** — verified today (the V3 zombie-503 repoint)
- **zai Lite pool #2 (gopher)** — ~1% used; GOPHER_DAILY_CREDITS kill switch armed
- **MiMo free window** — opencode serve :4096, $0, ends ~09-28
- **local 7b (qwen2.5-coder)** — 21.8 tok/s, night-window only (family-box law)
- **run-1 stealth sweep discoveries**: nex-n2.5-mini 150.5 tok/s; **nemotron-3-super-120b 128.9 tok/s**; **nemotron-3-ultra-550b 100.8 tok/s** (550B-class, free); poolside laguna-s; nemotron-3.5-lightning. Sighting: thinkingmachines/inkling (gated 403).

## The demand side (real work that absorbs the capacity)

1. **Full scan** — 3,185 records remaining of 4,129; each record is model calls. The single biggest legitimate sink.
2. **Task wall** — ~50 real backlog chores/pass (label farm, pillar anchors, gap questions); passes can scale with lane count.
3. **Stealth/bake-off discovery** — now daily: every new free model that appears gets scored within a day of appearing.
4. **Old-books digs + research mine** — standing directive, workflow-driven, model-heavy.
5. **Training spine** — 536K events → Kev diet; BLOCKED on the AMD driver update (GPU falls back to CPU). **The driver update is the single biggest unlock for daily compute use.**

## CLARITAS faces (promoted same night)

The CL4R1T4S leaked system-prompt distillation slept in `watch/salon_runner.py.bak-20260904`;
now it is `mag/claritas.py` — the default system prompt for every burn lane, matched by
vendor family (openai/gemini/anthropic/grok/... neutral house contract otherwise). First
receipt: the gemma/lfm retry passes with faces turned hollow-receipt FAILs into CORRECT
(lfm-2.5-2.6b @ 120.7 tok/s).

## The meters that prove burn

- `logs/provider_usage.jsonl` — every call, every lane, ok/fail
- `state/fuel/stealth_ledger.jsonl` — sweep cursor + per-model scores
- `watch/inbox/STEALTH_SWEEP_LATEST.md` — today's free-wall scoreboard
- KeyAudit 09:45 — keys/lanes/mapping health (model-catalog audit proposed, awaiting GO)

## One law proposed (not yet built)

**Model law:** a lane's model name is a key — the 09:45 audit verifies every model
name referenced by estate files still exists in its provider's live catalog, failing
loud with the successor. Groq (clean 404) and Together (zombie 503) both proved this
week that provider churn is discovered at failure time when it should be caught at 09:45.
