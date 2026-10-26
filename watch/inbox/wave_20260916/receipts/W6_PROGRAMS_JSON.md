# W6 — PROGRAMS.json (machine-readable program-state ledger)

- **Lane:** W6 · **Date:** 2026-09-16 · **Agent:** deck-lane (ZCode)
- **Mission:** N1 command-deck's wished-for source, made real. PROGRAMS.json the deck reads instead of scraping prose.
- **Law honored:** receipt FIRST, appended as work proceeds. No git commands. Write/Edit for source. `.venv\Scripts\python.exe` only.

## Location decision (bytes-cited)

- `.gitignore` lines 27–29: `state/` + `state/**/*` are ignored (`!state/.gitkeep` only) → **state/ is gitignored-policy**.
- Durable root per shared-surface contract and mission law: **`watch/inbox/wave_20260916/PROGRAMS.json`** (watch/*.json globs are top-level only; watch/inbox/ is the durable write root for all clients).

## Progress log

- [x] Receipt opened FIRST (this file).
- [x] Wave receipts mined for tonight's truth (7 programs).
- [x] PROGRAMS.json written + schema-validated.
- [x] scripts/build_deck.py extended: PROGRAMS.json when present, prose-scrape fallback.
- [x] Deck regenerated; PROGRAMS section verified against seeded values.

## Schema (programs.v1)

Top level: `{"schema": "programs.v1", "updated", "writer", "note", "programs": [...]}`.
Per program — exactly six fields, nothing more:

```json
{"program": "<id>", "status": "green|amber|red", "gate": "none|operator-click|funding|decision",
 "evidence": ["<repo-relative file paths>"], "updated": "<date>", "next_stone": "<the next actionable stone, bytes-cited>"}
```

## Seeded values (verbatim from `watch/inbox/wave_20260916/PROGRAMS.json`)

| program | status | gate | updated | next_stone (verbatim) |
|---|---|---|---|---|
| referee-chain | green | operator-click | 2026-09-16 | Clear the 2 operator clicks — rotate DISCORD_BOT_TOKEN + grant #game-c-overview (403) — then live /bones boot before Sep-20 (D20 OPERATOR GATES: 'The adapter does not go live until both gates clear') |
| cube-program | amber | funding | 2026-09-16 | Operator $31 GO on the stage-0 order (electronics only); assembly proposed 2026-09-22, fallback 09-29; CONCERT amendments (dead twin, SHT31, grown barrage zones) still unmerged into the plan (R3 byte-finding) |
| ractor-salon | amber | operator-click | 2026-09-16 | Human scrub review of the 19 files (automated sweep clean; 2 OWNER placeholders await the GitHub username), then the OPERATOR-executed publish checklist: venv tests, git init+tag, repo create/push/release, catalog PR vs NousResearch/hermes-agent |
| grounding-wave | red | decision | 2026-09-16 | Operator cross-signed void of row 122 (MALFORMED_ROW) and the orphaned repair fork at 123 — canonical tip is 1-121 to 123 to 124, 122 dangles; v4 is built and the void is staged as PROPOSAL (dry-run only, nothing appended); no migration — fail-to-pass happens only through the operator's cross-signed void |
| ractor-engine | amber | none | 2026-09-16 | Run the Q3 OCEAN falsifier: zero-coupling placebo (trait adjectives in prompt, ALL graph gains neutral — the neutral-gain twin), parameter-level with prompt frozen, verdict-flip significance vs placebo; spec amendments landed (decoder bridge is load-bearing, not optional) |
| blind-challenge-set | green | none | 2026-09-16 | Open the prediction window: one-line pointer in queue/todo.md ('BCS-20260916 open'), then first non-claimant predictor row for C-01; set is SEALED, window dark, keys hash-committed outside every contract surface |
| mud-replay-law | green | none | 2026-09-16 | Rebuild the stale dist copies (site/dist/games/mud.html is byte-stale vs canonical 105,849 B); law holds: 18-seed-site port, replay 11/11, fifty-lane 51/51 x10, harness extended to 58/58 green x4 (N10 vault lanes) |

Evidence bytes (all paths verified on disk by the schema check):

- **referee-chain:** `receipts/D20_BONES_ADAPTER.md` (OPERATOR GATES: "Token rotation pending" + "#game-c-overview 403 permission click pending" — the 2 clicks), `receipts/W1_WORLD_SKELETON.md` line 82 ("12 passed" bones suite), `watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md` (Sep-20).
- **cube-program:** `physical_computing/receipts/C17_CUBE_INSTRUMENT_PLAN.md` (FILED, two-eyes pending), `receipts/CONCERT001_20260916.md` (stage 0 ~$31), `receipts/R3_GAP_ANALYSIS_SOCRATIC.md` (amendments unmerged byte-finding), `physical_computing/CUBE1_SHOPPING_LIST.md` (assembly 2026-09-22, fallback 09-29). NOTE: the mission capsule said "stage-0 Mon" — the bytes say 2026-09-22; bytes win.
- **ractor-salon:** `receipts/P1_RACTOR_PACKAGE.md` line 68 ("Human scrub review of the 19 files … the human gate is yours"; two OWNER placeholders) + OPERATOR-executed publish checklist; `receipts/P2_DEMO_SALON.md`.
- **grounding-wave:** `receipts/VC2_CHAIN_STATE.md` line 19 ("The chain is forked: canonical tip = 1–121 → 123 → 124 (`8d2cc3dd…`); 122 dangles as a side-branch"), `receipts/V4_GROUNDING_ADMISSION.md` (v4 built, 26/26 v4 suite; "Row-122 void staged as PROPOSAL (dry-run only, nothing appended)").
- **ractor-engine:** `receipts/RS_RACTOR_ENGINE_SALON.md` (Q3 falsifier design, unanimous neutral-gain twin / zero-coupling placebo; "3 best design amendments for the ractor engine spec"), `receipts/N5_RACTOR_DOGFOOD.md`. Falsifier designed, not yet run → amber.
- **blind-challenge-set:** `receipts/A1_BLIND_CHALLENGE_SET.md` ("Status: SEALED — … Awaiting predictor rows"; §open: "Open the prediction window: post a one-line pointer … and let the first non-claimant seat append its C-01 predictor row") — sealed, window dark.
- **mud-replay-law:** `receipts/FX4_MUD_REPLAY_PORT.md` ("Status: DONE — replay test 11/11 green, fifty-lane gate 51/51 green × 10"; "18-seed-site port"), `receipts/N10_PUZZLE_VAULT_CONSUMER.md` (harness 51 → 58 lanes; "58/58 lanes green" × 4 consecutive).

## Builder change (`scripts/build_deck.py`)

- New: `PROGRAM_JSON_CANDIDATES` (wave PROGRAMS.json → `watch/inbox/PROGRAMS.json` → `state/programs.json`), `PROGRAM_TITLES`, `load_programs()`.
- `load_programs()` returns ledger cards when a readable PROGRAMS.json with a non-empty `programs` list exists; otherwise falls back to the old `mine_programs()` prose-scrape. Both paths unit-verified (temp script, deleted after): ledger path → 7 cards with health/gate/updated; fallback path → 6 prose cards, no health field.
- `main()` wires `data["programs"]` + `data["programs_source"]`; print line now reports `programs=N source=…`.
- Renderer `programs()` now shows: per-card status chip (GREEN/AMBER/RED colored) + gate chip, next-stone as the accent line, optional detail, `updated <date> ·` prefix on the sources line, and the section header carries the live count + source label (ledger path or "prose-scrape fallback").
- One builder bug fixed during wiring: an intermediate edit left orphaned dict lines in `main()` (syntax error); caught by reading the region before rebuild, repaired, rebuilt clean.

## Deck regen output (verbatim)

```
deck written: C:\Users\foste\Documents\projects\local_sovereign_agent\dashboard\static\deck.html (36692 bytes)
programs=7 source=watch/inbox/wave_20260916/PROGRAMS.json
lanes=11 receipts=8 links_rows=182 verify=FAIL row 122: MALFORMED_ROW (missing/short hash — v4 refuses
```

Verification of the rendered PROGRAMS section:

- Embedded `deck-data` block parses as JSON; `programs_source` = `watch/inbox/wave_20260916/PROGRAMS.json`; 7 rows, each carrying `health` (green/amber/red), `gate`, `ledger_updated: 2026-09-16`, verbatim next-stone strings (spot-greps: "NEXT STONE: Operator $31 GO", "58/58 green x4", all present).
- `node --check` on the extracted inline script: **OK**.
- Fresh live values picked up on regen (deck is a REFRESH, not a snapshot): LINKS 174 → **182 rows**, grounding verify line now the v4 wording ("FAIL row 122: MALFORMED_ROW …"), receipts latest-8 refreshed.
- Note: uppercase chips (AMBER/GREEN/RED), the `updated 2026-09-16` prefix, and the source label are built client-side by the renderer at page load (verified present in the data block + template logic), so they do not appear as HTML literals — data-block greps confirm the underlying fields.
- Temp verify files (`scripts/_verify_programs.py`, `scripts/_deck_verify.js`) deleted after the pass.

## Update protocol (who writes PROGRAMS.json)

- **The fold lane writes it, once per wave.** At wave close, the fold reads the wave's receipts and updates each program row it has byte-evidence for: flip `status`/`gate`, replace `next_stone`, refresh `updated` to the wave date, and point `evidence` at the receipts that justify the change. Rows are never deleted — a retired program keeps its row with `next_stone` describing the retirement (rows are history-bearing, like the chain).
- **Who does NOT write it:** arbitrary lanes mid-wave do not edit rows directly — a lane that moves a program files its receipt and leaves the row to the fold (the same way wave state is folded). The deck never writes it; `build_deck.py` is read-only over the ledger.
- **Validation before fold-commit:** statuses must be in {green, amber, red}, gates in {none, operator-click, funding, decision}, every evidence path must exist on disk, `updated` must be the wave date. The builder tolerates a broken/empty file by falling back to prose-scrape (and the deck header then says so loudly — degradation is visible, per the N1 lesson).
- **Location:** `watch/inbox/wave_20260916/PROGRAMS.json` (state/ is gitignored — `.gitignore` lines 27–29 — so watch/inbox is the durable root per the shared-surface contract). Future waves may move it to `watch/inbox/PROGRAMS.json`; the builder already looks there.
- **Receipt end.** W6 complete: ledger real, deck data-driven, fallback armed.
