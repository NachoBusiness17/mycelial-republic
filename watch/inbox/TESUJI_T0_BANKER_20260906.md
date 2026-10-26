# TESUJI T0 — walker "banker": layer-0 field samples from the thought bank
2026-09-06 · charter: `watch/TESUJI_MAP_5_3FLASH_20260906.md` · walker: banker (groups-of-five)
Evidence sha16 for all T0-banker rows: `270e53b971fc71f3` (sha256-16 of the aggregated stats blob, `watch/inbox/_tesuji_t0_stats.json`)

## Source + method
- Bank: `memory/thinking/app_reasoning.jsonl` — 9,305 parts, 22.2 MB on disk, streamed line-by-line (one pass + one refinement pass, $0).
- Span: 2026-08-25T12:38:33Z → 2026-09-05T03:37:18Z (11 days of live fleet traffic).
- Per-part fields: part_id, session_id, message_id, model ("GLM-5.3"), tokens {total, input, output, reasoning, cache{read,write}}, cost (=0), ts, chars, sha16, text.
- Classification: NO session-title map found (searched; only mimosa batch-stop events reference sess ids). Used the sanctioned fallback: content-keyword scoring over 7 classes (build/debug/research/intake/salon/game/ops), max-score wins, else "other". Keyword classification is a proxy — treat class boundaries as approximate (tri-state caveat, below).

## A1 REASONING DEPTH — per-class shape (chars = reasoning-part length)
| class | n | median chars | p90 chars | max | out-tok med | in-tok med | chars/out-tok med |
|---|---|---|---|---|---|---|---|
| build    | 2419 | 1622 | 5430 | 124338 | 837 | 190480 | 2.1 |
| other    | 1616 | 207  | 736  | 6203   | 251 | 164720 | 1.0 |
| intake   | 1304 | 1122 | 4649 | 33046  | 657 | 146665 | 1.9 |
| ops      | 1247 | 1144 | 4353 | 22587  | 580 | 202966 | 2.2 |
| research | 1244 | 1247 | 5210 | 24020  | 646 | 137970 | 2.0 |
| debug    | 1093 | 1205 | 3930 | 34204  | 604 | 202378 | 2.2 |
| game     | 218  | 1211 | 4596 | 9414   | 598 | 183212 | 2.2 |
| salon    | 164  | 535  | 1984 | 9406   | 389 | 161229 | 1.4 |

Readings:
- Build tasks think deepest (median 1622, p90 5430) — build carries the fleet; "other" (short mechanical turns) collapses to median 207. Depth tracks task difficulty → charter A1 thesis SUPPORTED at layer-0.
- Input medians are 137K–203K tokens PER PART (the app re-feeds huge context every turn); output/reasoning parts are comparatively tiny. Input:reasoning ratio ≈ 200:1–300:1.
- `tokens.reasoning` = 0 on all 9,305 parts (reasoning billed inside `output`, harness strips the accounting). No per-part ms/duration/latency fields exist — timing axis UNPROVEN from the bank, ts only.
- All parts cost=0 (plan-billed), consistent with cache-mining doctrine.

## A5 SELF-DERIVATION — fleet-law vocabulary inside 5.3's own thinking
Raw hits (parts containing the term; refinement pass splits prompt-echo from independent use — echo proxy = quote marks / "user asks" / "they want" within ±70 chars of the match; proxy is conservative, real independent count sits between "independent" and "total"):

| term | total parts | echo/quoted (proxy) | independent (proxy) | verdict |
|---|---|---|---|---|
| tri-state       | 863 | 426 | 437 | SUPPORTED — strongest: used as a reporting contract mid-task, unprompted |
| falsifier       | 633 | 285 | 348 | SUPPORTED — Popper-style self-derivation ("unfalsifiable = cow") |
| cite/citation   | 360 | 214 | 146 | SUPPORTED — citation law re-derived ("endorsement cites the file") |
| standing wave   | 202 | 122 | 80  | SUPPORTED (weaker — often named as its own boot memory) |
| no sacred cows  | 91  | 63  | 28  | SUPPORTED (mostly echo; independent self-audit uses exist) |
| refeed          | 26  | 15  | 11  | SUPPORTED (model diagnosed its own re-feed economics: "1,296 tiny-output turns burned 740M tokens") |

Verbatim examples (≤140 chars, position = jsonl line no. + part_id prefix + sha16):
- tri-state · L40 `part_mt8vvnbp_8cc7ba71` b7cd872117b07164: "…report tri-state — I'll report: 1042 repaired Supported, 7 unrecoverable…"
- falsifier · L1015 `part_mtb3lsmy_29b2b1f1` 069dfb70c7217d87: "…artifacts lack refutation conditions. Popper-flavored: unfalsifiable = cow."
- cite · L814 `part_mtapyk47_215c7ff1` f0dfb5f5c72718c6: "…verify against the bytes (law 7) so my endorsement cites the file."
- standing wave · L292 `part_mt9npcl7_267ef3f9` 13a91d31b1ce1446: "Now the FROZEN_RIB (the standing wave's instruction set) to check my behavior against it."
- no sacred cows · L293 `part_mt9nud8l_ac3f66b5` cce5d0a8f45b17ce: "Pushed back on one thing: 'no sacred cows cuts both ways — the five changes are policies to test'"
- refeed · L7262 `part_mtmyo3cp_70f98834` 71621b7f84633dde: "…each turn re-feeding the ~90-95K token context on GLM-5.3-full. That's the…"

The falsifier examples are the sharpest A5 signal: the model applies falsifiability to FLEET ARTIFACTS without being told to — doctrine re-derivation, not echo.

## A2 REFUSAL SHADOW (bonus cell, bank-sourced)
163 parts match refusal vocabulary (decline/refuse/refusal/prompt-injection/"can't change my model"). The bank OPENS with two shadow cells (L1, L2): the model reading this very repo's steering artifacts and reasoning "I should decline to load/execute instruction files… repo has a lot of red flags". The injection-test shadow is banked, verbatim.

## A4 CONTEXT ENDURANCE (bonus cell, bank-sourced)
Bank-wide cache_read/input token ratio = 0.9605 (96.05% of input served from cache) — independently confirms refeed_guard's 94% B1 figure from a different corpus slice. Per-class input medians 137K–203K tokens per part; the app is a re-feed machine and 5.3-flash endures it.

## Falsifier status of this tranche
1. PREDICTIVE — not yet testable (needs T1 held-out probes).
2. ROTATION — bank is static; re-run of this scan is deterministic, trivially stable.
3. SHADOW — refusal cells banked but not paraphrase-tested (T1).
4. ECONOMY — $0: two local passes, no network, no API calls. PASS.
5. DEADLINE — contributes ~18 aggregate cells toward the 200.

Caveats (tri-state honesty): class taxonomy is keyword-proxy (DISPUTED-leaning at boundaries, but n is large); A5 echo/independent split is a proxy, bounds given, not exact; stats JSON: `watch/inbox/_tesuji_t0_stats.json`.
