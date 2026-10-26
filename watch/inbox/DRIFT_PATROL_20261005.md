# DRIFT PATROL - 2026-10-05

- class: RECEIPT
- writer: drift-patrol-cron
- automation: automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **53 unpushed - pushed clean through all gates** (no gate blocks this morning) | FIXED BY PATROL |
| fleet vitals | all five containers healthy; **mag-sovereign Up 39h healthy - the ghost wedge is now the longest-quiet on record** | CLEAN |
| inbox fold integrity | refolded: 10,783 events - 3,126 items; 1 registered-not-landed in-flight (2026-10-05-spore-sharing/dogfood.md - a spore-sharing window writing now); verify mismatch row = known live-race class | CLEAN, LIVE |
| surface integrity | 69 at open - 14 healed - 66 residual: **the autoseal flood now outpaces single-pass healing definitively** (the X-INTEL + frontier_olm + ractor_engine windows wrote hundreds of rows overnight). All residual triaged as in-flight/timing classes; zero tampering indicators. PLUS one new dialect violation filed (below) | TRIAGED (day 14) |
| link ledger | 8 duplicates on file (stable) | CLEAN |

## New dialect violation filed: X-INTEL journal rows in the register log

The X-INTEL window appended free-form journal rows to index_events.jsonl (`kind: x-intel` / `x-intel-batch`, with title/titles/verdict/receipt keys, no op, no seq, no writer - lines 10637-10640). The fold tolerates them; validate flags the unknown keys (B2-157's exact phantom-dialect concern: no seq means no last-register-wins participation). **Not corruption - a dialect breach**: journal rows belong in a journal file; the register log takes only schema events (seq/op/file/sha256/class/purpose/writer/nonce). Filed owed to the X-INTEL writer contract. 4 validate errors are these rows and will persist by design until the writer adopts the schema.

## Overnight (large): D8 decay-family lineage landed (superseded_by set-once + valid_at immutable, forgery draft failed CORRECTLY, 7 tests); a case-sensitivity silent-drop caught and cured (ledger tracked lowercase while night commits added RACTOR_ENGINE uppercase - strikes never reached git, recovered byte-exact from stash; LAW: match ls-files case on case-insensitive FS); OUROBOROS R1 (79 findings, tier-1 merge clause kills the E26 data-destruction vector, 19/19 saved workflows now declare max_concurrency); night shift close: 4 doors, 26 tests, bubbles kept blowing.

**Top risks (boldest first):**
1. **The autoseal flood is now decisive** (heal 14, residual 66; event log 10,783 and climbing by ~1K/day) - the register-at-close writer fix is no longer optional hygiene; without it the patrol is a spectator to a permanent 60-row in-flight set.
2. **Dialect drift in the register log** (X-INTEL journal rows) - the second writer-contract breach this week (SCOUT was first); the schema needs enforcement at write time, not detection at read time.
3. **Event log past 10K lines with compaction still undesigned** (day 8 of the standing owe) - at +1K/day this becomes a performance issue within the month.
