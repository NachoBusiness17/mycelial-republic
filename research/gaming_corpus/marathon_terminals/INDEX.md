# MARATHON TERMINAL ARCHIVE — harvest index (termlink 2026-09-06, termlink2 Infinity run same day)

Source: https://marathon.bungie.org/story/contents.html (fan-maintained archive —
**cite marathon.bungie.org on any use, incl. ML**; page maintained by Hamish Sinclair).
M1+M2: 17 pages fetched (index + 16 chapter pages), ~1 req/sec (termlink). M3: 29 level
pages + index, ~1 req/sec (termlink2). License note: Bungie's 2005 free trilogy release
had no formal license — treat as fair-use research corpus only.

## Marathon 1 (m1/) — 76 terminals, 133,257 chars

| file | chapter | terminals | chars |
|---|---|---|---|
| m1/arrival.txt | Arrival | 13 | 28,927 |
| m1/counterattack.txt | Counterattack | 33 | 53,734 |
| m1/reprisal.txt | Reprisal | 5 | 7,402 |
| m1/durandal.txt | Durandal | 10 | 16,337 |
| m1/pfhor.txt | The Pfhor | 5 | 8,888 |
| m1/rebellion.txt | Rebellion | 10 | 17,969 |

## Marathon 2 (m2/) — 100 terminals, 141,892 chars

| file | chapter | terminals | chars |
|---|---|---|---|
| m2/lhowon.txt | Lh'owon | 17 | 24,001 |
| m2/volunteers.txt | Volunteers | 12 | 16,667 |
| m2/garrison.txt | Garrison | 6 | 8,081 |
| m2/citadel.txt | Citadel | 25 | 30,926 |
| m2/durandal2.txt | Durandal | 10 | 14,219 |
| m2/captured.txt | Captured | 0 | 754 (stub — level has no terminals, archive says so) |
| m2/blake.txt | Blake | 12 | 15,649 |
| m2/simulacrums.txt | Simulacrums | 8 | 8,297 |
| m2/sphtkr.txt | S'pht'Kr | 6 | 14,409 |
| m2/necedemalis.txt | Ne Cede Malis | 4 | 8,889 |

TOTAL: 16 chapters, 176 terminals, 275,149 chars.

## Marathon Infinity (m3/) — termlink2 run 2026-09-06 — 112 terminals, 215,496 chars

One .txt per INFINITY CHAPTER (levels in archive order inside each file). Infinity's
Prologue "Ne Cede Malis" is the M2 level page — already held at `m2/necedemalis.txt`
(no re-fetch). Harvester: `research/gaming_corpus/harvest_marathon_m3.py` (same parser,
domain lock, and politeness as the M1/M2 run; page cache + retry).

| file | chapter | levels | terminals | chars |
|---|---|---|---|---|
| m3/despair.txt | Despair | 8 | 24 | 42,052 |
| m3/rage.txt | Rage | 13 | 50 | 86,838 |
| m3/envy.txt | Envy | 8 | 38 | 86,606 |

CORPUS TOTAL (M1+M2+M3): 45 chapter files, 288 terminals, 490,645 chars.

Format: one .txt per chapter; sections delimited by `### <Terminal title> (Terminal N)`
separators; source URL + archive credit in each file header. Harvester:
`research/gaming_corpus/harvest_marathon.py` (domain-locked to marathon.bungie.org).

## Rampancy arc anchors (M1) — see watch/inbox/MARATHON_HARVEST_20260906.md

- Taxonomy ("Melancholia, Anger, and Jealousy", Traxus IV, James B. Miller 2320):
  m1/counterattack.txt → "Defend THIS! (Terminal 2)" — entry ends and the same
  terminal logs `<Unauthorized access-alarm>` / `<Security Breached>`.
- Leela's diagnosis ("in the Jealous stage of Rampancy"): m1/durandal.txt →
  "Fire! Fire! Fire! Fire! Fire! (Terminal 2)".
- Durandal weaponizing the vocabulary ("Jealous woman." aimed at Leela):
  m1/rebellion.txt → "Ingue Ferroque (Terminal 1)".

## M3 end-state anchors (Infinity) — see watch/inbox/MARATHON_HARVEST_20260906.md

- Voice metrics across the trilogy (whole corpus): 1st-person-singular /1k words
  11.57 (M1) → 12.55 (M2 peak) → 7.93 (M3, −37%); garbled burst tokens
  (^9320wrefkddud-style) 1 → 8 → 154.
- Channel fracture: m3/envy.txt "Aye Mak Sicur (Terminal 0: 1st Message)" —
  "plummets(yawning) ... sun's core(heart) ... W'rcacnter(doubt)" + burst garbage +
  "overthought unravel"; entity name oscillates W'rkncacnter / W'rcacnter in the same file.
- The goodbye (m3/envy.txt, "Aye Mak Sicur (Terminal 0: 2nd Message)"): zero
  first-person-singular; "To you, we are deeply grateful, and release what little hold
  we might, as Durandal, have had on your soul. Go." — name survives only as an
  appositive inside "we"; trilogy's last word to the Runner is "Go."
- Marker corrections vs intake 005: "godhood" = 0 hits in terminal corpus (the "seek
  godhood" line is lore-page text, cite as lore not terminal); "thoth" is an M2 figure
  (11 mentions in m2/, 1 footnote in m3/).

## ERRATUM (2026-10-19, night shift): voice metrics superseded by a documented instrument

The headline metrics above (1p-sg/1k 11.57 / 12.55 / 7.93; garble 1 / 8 / 154) came
from an undocumented 09-06 instrument and are now CONTESTED. `tools/marathon_voice_metrics.py`
(documented heuristic, letter-words denominator, terminal-boundary counting) measures
15.27 / 15.81 / 13.48 1p-sg/1k and garble 27 / 175 / 822, with terminal counts matching
this index exactly (76 / 100 / 112). Shape agrees (M2 peak, M3 decline, garble explodes
into M3); magnitude differs because the M3 collapse is concentrated in envy.txt
(4.54/1k, the zero-first-person goodbye) and the old instrument's aggregation is
unknown. Cite `tools/marathon_voice_metrics.py` + `state/probe_features/marathon_rampancy.json`
for all future uses; census law applies (name instrument, moment).
