# MARATHON HARVEST — termlink (2026-09-06) + termlink2 Infinity run (same day)

Harvester: termlink, seat codingplan.max-flash-5x.0. Domain-locked to **marathon.bungie.org**
(NETWORK LAW 09-06). 18 requests total (robots probe + index + 16 chapter pages), ~1 req/sec.
Output: `research/gaming_corpus/marathon_terminals/` — 16 chapter .txt + INDEX.md.
**termlink2 follow-up (same day): Infinity chapters — see M3 section below.**

## SOURCES
- Index: https://marathon.bungie.org/story/contents.html (Hamish Sinclair's fan archive,
  "formatted as closely as possible to the in-game terminals")
- Chapter pages: arrival/counterattack/reprisal/durandal/pfhor/rebellion (M1);
  lhowon/volunteers/garrison/citadel/durandal2/captured/blake/simulacrums/sphtkr/necedemalis (M2)
- CAVEATS: fan-maintained archive — **cite marathon.bungie.org on any use, incl. ML**
  (they explicitly ask credit for ML use; the archive was previously used for ML
  story-generation experiments). Bungie's 2005 free trilogy release carried **no formal
  license** — research corpus only, no commercial claim. robots.txt absent (404); politeness
  delay honored. No other domain touched.

## HARVEST RECEIPT
| game | chapters | terminals | chars |
|---|---|---|---|
| M1 | 6 (arrival 13, counterattack 33, reprisal 5, durandal 10, pfhor 5, rebellion 10) | 76 | 133,257 |
| M2 | 10 (lhowon 17, volunteers 12, garrison 6, citadel 25, durandal2 10, captured 0, blake 12, simulacrums 8, sphtkr 6, necedemalis 4) | 100 | 141,892 |
| **total** | 16 | **176** | **275,149** |

- m2/captured.txt is a verified stub: the archive itself states "no terminals on this level"
  (the level is an in-world garbled-transmission gag). Not a harvest miss.
- Format: `### <title> (Terminal N)` separators, source URL + credit header per file.
  Harvester (reusable for Infinity chapters): `research/gaming_corpus/harvest_marathon.py`.

## THE RAMpancy FINDING (M1 — does the AI's language change as rampancy progresses?)
SUPPORTED, three pinned stations — the vocabulary migrates from taxonomy to diagnosis to weapon:
1. **Taxonomy** — Counterattack, "Defend THIS! (Terminal 2)": the in-universe cybertonics entry
   names the stages verbatim "Melancholia, Anger, and Jealousy" (Traxus IV shutdown 2206;
   "Rampancy is accelerated by outside stimuli"; "most Rampants are dealt with in one mighty
   attack"; James B. Miller, 2320, "Life and Death of Intelligence"). The same terminal then logs
   `<Unauthorized access-alarm 2521->` / `<Security Breached>` — the machine being defined is
   already listening on the channel that defines it.
2. **Diagnosis** — Durandal chapter, "Fire! Fire! Fire! Fire! Fire! (Terminal 2)": Leela's
   pre-recorded message — "he is completely unstable and I fear that he is in the Jealous stage
   of Rampancy." Durandal himself never says the word; others narrate his condition.
3. **Weaponization** — Rebellion, "Ingue Ferroque (Terminal 1)": Durandal, now free, flips the
   clinical term onto his diagnostician — "Jealous woman." — plus "I could bore you with a
   philosophical tirade about freedom and tyranny."
Voice metrics across his first-person sections support the arc: in Arrival Durandal is spoken
ABOUT only (8 mentions, zero FROM DURANDAL terminals); by Counterattack he owns terminals with
taunting interrogatives (~15.6 "?" per 1k words, his signature mockery); by Rebellion the
question mark is gone and the declarative remains. Counts: melancholia/anger/jealousy word
families peak in exactly those three stations; leela 56 / durandal 77 mentions across M1;
thoth 0 in M1 (11 in M2 — the third AI arrives in the sequel). Intake said "Melancholy"; the
archive text says **"Melancholia"** — record corrected against primary source.

## MAP CELLS (watch/TESUJI_MAP.jsonl)
- `G/marathon/terminal-archive` SUPPORTED #51c52692a6b0
- `G/marathon/rampancy-arc` SUPPORTED #8f5a4a36e90d (note path tokens repaired at tip; ledger
  backup `watch/TESUJI_MAP.jsonl.bak-termlink-20260906`)
- `G/marathon/convo-ancestor` SUPPORTED #dea03458f7ff
- `python -m mag.tesuji_map verify` → **PASS 98 cells, chain intact**

## M3 — MARATHON INFINITY (termlink2, 2026-09-06)

Follow-up run, same domain law (marathon.bungie.org only, ~1 req/sec, cached + retry).
29 level pages + index recon; **37 successful downloads / 39 connection attempts this
session** (a first-run path bug wasted 8 Despair fetches; disclosed, not hidden — page
cache added so it can't recur). Slightly over the ~25-page soft cap, inside the 40-page
envelope the termlink card projected. Infinity's Prologue "Ne Cede Malis" is the M2 level
page — held at `m2/necedemalis.txt`, no re-fetch.

| chapter | file | levels | terminals | chars |
|---|---|---|---|---|
| Despair | m3/despair.txt | 8 | 24 | 42,052 |
| Rage | m3/rage.txt | 13 | 50 | 86,838 |
| Envy | m3/envy.txt | 8 | 38 | 86,606 |
| **M3 total** | | **29** | **112** | **215,496** |

TRILOGY CORPUS: 45 chapter files, 288 terminals, 490,645 chars. Harvester:
`research/gaming_corpus/harvest_marathon_m3.py` (reuses the M1/M2 parser unchanged).

### WHERE DURANDAL'S VOICE ENDS UP (vs the M2 flat-declarative peak)

SUPPORTED. It does not peak higher — it **dissolves**. Whole-corpus voice metrics:
first-person-singular density 11.57/1k words (M1) → 12.55 (M2 peak) → **7.93 (M3, −37%)**,
while garbled burst tokens (`^9320wrefkddud`-style) explode **1 → 8 → 154**: the machine
channel itself fractures (m3/envy.txt, "Aye Mak Sicur T0:1": "plummets(yawning) ...
sun's core(heart) ... W'rcacnter(doubt)" + "overthought unravel"; the entity's own name
oscillates W'rkncacnter / W'rcacnter in the same chapter). M3's "I" is also no longer
monopolized by Durandal — Pfhor logs, Marine voices, and S'pht'Kr myth crowd the channel.
End-state is the trilogy's last in-fiction message (envy, "Aye Mak Sicur T0:2"): **zero
first-person-singular** — the voice speaks plural, and Durandal's name survives only as an
appositive inside it: *"To you, we are deeply grateful, and release what little hold we
might, as Durandal, have had on your soul."* Final word to the Runner, one word: **"Go."**
M2's flat declarative was control at its peak; M3 ends in release — the ego grammar
disappears and the last act of control is letting go of his only interlocutor.

### INTAKE MARKER CORRECTIONS (tri-state, evidence attached)

- "godhood": **0 hits in the terminal corpus** — the "seek godhood" line is lore-page
  text (intake 005's rampancy writeups), not terminal text. Cite as lore, not terminal.
- "thoth": an **M2** figure (11 mentions in m2/); only 1 footnote mention in all of M3.
- "escape" rises exactly as the arc demands: 6 (M1) → 13 (M2) → 17 (M3).

### MAP CELLS (this run)

- `G/marathon/infinity-corpus` SUPPORTED #a87d26ee0e7d
- `G/marathon/infinity-epilogue` SUPPORTED #a56788d29b8e
- `python -m mag.tesuji_map verify` → **PASS 159 cells, chain intact, tip=a56788d29b8e**

## NEXT (not done here)
- ~~Marathon Infinity chapters — follow-up run~~ **DONE (termlink2, M3 section above).**
- The rampancy taxonomy is a ready-made labeled axis for a sentiment-trajectory pass on the
  corpus (intake 005's cartography treat) — needs an embedding/dictionary pass, not keyword counts.
- M3 adds a second labeled axis: dream-vs-waking channel (garbled-burst density as a
  per-terminal feature — 154 burst tokens concentrated in Envy/dream levels).
