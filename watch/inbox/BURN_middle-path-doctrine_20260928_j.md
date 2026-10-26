# BURN middle-path-doctrine 20260928 j

## Verdict

steal

## Evidence

- Kill event site (mud.html:2013, inside `killEnemy(e)` at :1924): `evlog.push(Object.assign(evt(), { e: 'kill', k: e.type }));` and kill value flows to the player only (:1928): `player.xp += e.xp;` plus soulOrbs (:1930-1938). No pool receives it.
- Season counters cannot ride evlog: `evlog.length = 0;` (mud.html:2504) wipes it each run in `startGame`.
- The only pools in the file are the bones pool (`const BONES_KEY = 'mud_bones', BONES_CAP = 10;` :507) and the boon draft (`const pool = BOONS.filter(...)` :1804). Neither is a VM pool.
- Greps over mud.html (2026-09-28): "faction" 0 hits, "sentiment" 0 hits, "donation"/"gift"/"shared pot" 0 hits, "vm" 0 economy hits, "season" 0 hits. "ledger" appears only in flavor text (:616) and the grudge-ledger comment (:571-577).
- Only network egress is the presence relay: `const RELAY = 'http://127.0.0.1:8766';` (:456), `fetch(RELAY + '/mud/seen', ...)` in `relayTick()` (:2608-2615).
- WebSearch 2026-09-28, "mud economy instrumentation seasonal metrics 2026": thin, marine benthos hits only, unread, owed.

## Steal or Vacuous

Steal: the instrumentation spec, grounded and honest. Build-first flag fired harder than expected: F8's precondition fails on BOTH channels, not just gifts. The stub has no factions, no sentiment meters, no VM pool, no gift action. F8 is not fireable against this code; a gated stub build must land first. When it does, the counters hook here, per the existing machine-state law (mud.html:2506 marks lore and the bones pool deliberately NOT reset across runs, the `mud_lore` pattern :476-477): (1) kill-fed counter incremented inside `killEnemy` at the :2013 receipt, extended to carry `{ pool: N }`; (2) gift-fed counter at the new donation action (closest seams: boon altar :1803-1814, courtyard :515); (3) both accumulated in a new SAFE_STORE key `mud_season`, excluded from the `startGame` reset like `mud_lore`; (4) sentiment meters are F5 canon, absent from this file, so the build adds them beside the season key; (5) season closure emits one JSONL line per season via the relay, the stub's only off-surface write path. Ledger row shape: `{"season":"...","kill_fed_total":N,"gift_fed_total":N,"sentiment_start":S0,"sentiment_end":S1}`. F8 fires on that line: gift_fed_total over 50 percent of inflow with sentiment_end above sentiment_start. Until the build, F8 stays armed-on-paper; the i-pass demotion rule holds (a falsifier that cannot fire is not armed).

## Pilot annotation

Annotation-only arm; nothing measured.

## Bibliography

- watch/inbox/BURN_middle-path-doctrine_20260928_i.md (full)
- dashboard/static/games/mud.html (greps for pool/vm/kill/faction/donation/gift/sentiment/season/ledger/fetch run 2026-09-28; lines 60-89, 440-484, 1798-1817, 1924-1993, 2496-2531, 2604-2620 read)
- WebSearch 2026-09-28, "mud economy instrumentation seasonal metrics 2026" (thin, unread, owed)
