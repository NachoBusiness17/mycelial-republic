# F4 — ESOTERIC / PARABLE CANON (wave 2026-09-16)

- **Lane:** F4 · free+legal only (pre-1929 PD + verified-legal translations) · no git
- **Mission:** the esoteric/parable public-domain canon → `memory/corpus/esoteric_canon/` for the riddler-seat voice and the parable register
- **Law:** receipt FIRST, append as you go (this file) · public-domain fetches only — Project Gutenberg / Standard Ebooks / archive.org legal copies
- **Patron text note:** Chesterton "The Man Who Was Thursday" is the riddler canon's patron text (Sunday is the patron puzzle; Chesterton the ex-atheist mirrors the operator's own journey)
- **Targets:** Chesterton "The Man Who Was Thursday" · Chesterton "Orthodoxy" (chapter-per-stone) · Carroll "Alice's Adventures in Wonderland" + "Through the Looking-Glass" (riddles, mirror logic, double-cover of looking-glass space) · Borges "The Garden of Forking Paths" (careful: 1941 Ellery Queen translation — VERIFY before fetching, else record blocked) · Borges "Ficciones" (NOT PD — skip) · Kafka "The Trial" (PD German original + verified-free translation) · Senet/Go historical sources if PD

## Plan

| # | Target | Source | Status |
|---|--------|--------|--------|
| 1 | Chesterton — "The Man Who Was Thursday" (1908) | Project Gutenberg #1695 | **FETCHED** |
| 2 | Chesterton — "Orthodoxy" (1908) | Project Gutenberg #130 | **FETCHED** |
| 3 | Carroll — "Alice's Adventures in Wonderland" (1865) | Project Gutenberg #11 | **FETCHED** |
| 4 | Carroll — "Through the Looking-Glass" (1871) | Project Gutenberg #12 | **FETCHED** |
| 5 | Kafka — "Der Process" (1925, German original, PD) | Project Gutenberg #69327 | **FETCHED** |
| 6 | Kafka — "The Trial" (English, Wyllie free translation) | Project Gutenberg #7849 | **FETCHED** (free w/ permission, not PD — see log) |
| 7 | Borges — "The Garden of Forking Paths" (1941 EQMM translation) | VERIFY ONLY | **BLOCKED** (see verdict) |
| 8 | Borges — "Ficciones" | n/a | SKIPPED (not PD, per mission) |
| 9 | Go historical source — Arthur Smith, "The Game of Go: The National Game of Japan" (1908) | archive.org `gameofgonational00smit` | **FETCHED** |
| 10 | Senet historical source — Falkener, "Games Ancient and Oriental" (1892) | archive.org `gamesancientand00falkgoog` | **FETCHED** (Egyptian game under period name "The Game of Tau"; the modern word "senet" postdates 1892) |

## Fetch log (append as you go)

*(start 2026-09-16, receipt filed before first byte fetched)*

1. **Chesterton — The Man Who Was Thursday** → `memory/corpus/esoteric_canon/chesterton_the_man_who_was_thursday.txt` (PG #1695, 1908, header-verified). DONE.
2. **Chesterton — Orthodoxy** → `memory/corpus/esoteric_canon/chesterton_orthodoxy.txt` (PG #130, 1908, header-verified). DONE.
3. **Carroll — Alice's Adventures in Wonderland** → `memory/corpus/esoteric_canon/carroll_alices_adventures_in_wonderland.txt` (PG #11, 1865, header-verified). DONE.
4. **Carroll — Through the Looking-Glass** → `memory/corpus/esoteric_canon/carroll_through_the_looking_glass.txt` (PG #12, 1871, header-verified). DONE.
5. **Kafka — The Trial, David Wyllie translation** → `memory/corpus/esoteric_canon/kafka_the_trial_wyllie.txt` (PG #7849, header-verified). **Status note:** translation © David Wyllie, hosted by Project Gutenberg by the translator's permission — a legal free copy, NOT public domain. Kept as the "free translation" leg; PD leg is the German original (item 6).
6. **Kafka — Der Prozess (German original, 1925, PD)** → `memory/corpus/esoteric_canon/kafka_der_process_de_1925.txt` (PG #69327, `copyright: false` per Gutendex metadata, header-verified). DONE.

## Borges verdict (diligence record)

**VERDICT: BLOCKED — not verifiably public domain; nothing fetched.**

Due diligence performed 2026-09-16 (web search + Wikipedia "The Garden of Forking Paths"):

- **Correction to the brief:** the Ellery Queen's Mystery Magazine appearance is **August 1948** (Anthony Boucher translation — the first Borges in English), not 1941. The story itself (Spanish, *El jardín de senderos que se bifurcan*, Editorial Sur) is 1941; a second translation (Donald A. Yates) appeared 1958 and in *Labyrinths* (1962).
- **Spanish original (1941):** Borges died 1986. Argentina term is life+70 → protected in the source country on 1 Jan 1996 → **URAA-restored in the US**. Not PD; term runs into the 2050s. No Gutenberg/Standard Ebooks/archive.org PD copy exists.
- **Boucher English translation (EQMM, Aug 1948):** US works from 1948 run 95 years if renewed (into 2044). If unrenewed it would have fallen into PD decades ago — but no renewal-record verification was performed in this lane, and every legal surface (Gutenberg, Standard Ebooks, archive.org) carries it only under copyright. Per lane law: **unverifiable → record blocked, do not fetch.**
- **Ficciones (1944):** NOT PD — skipped per mission.

If the seat ever needs a fork-paths flavor legally: Chesterton's Thursday and Carroll's looking-glass already cover branching-perception and mirror-space registers; revisit Borges only on a verified-renewal-clear finding for the 1948 Boucher text (would need the Stanford/LOC CCE renewal databases, scanned periodical renewals 1970-1976).

### Post-close note

Classification: **RECEIPT** (this file) + corpus artifacts. Sources are public-domain legal copies (PG / archive.org) except `kafka_the_trial_wyllie.txt`, which is a PG-permission copy of a © translation — flagged above and in the file's own header. Validator: `.venv\Scripts\python.exe -m mag.shared_surface validate`.

## Fetched table + totals

All files at `memory/corpus/esoteric_canon/` (repo root: `C:\Users\foste\Documents\projects\local_sovereign_agent`). All header-verified by content; sha256 + bytes recorded per contract (trust bytes, not reports).

| File | Work | Year / status | Source | Bytes | sha256 (first 12) |
|------|------|---------------|--------|-------|-------------------|
| `chesterton_the_man_who_was_thursday.txt` | Chesterton, *The Man Who Was Thursday: A Nightmare* | 1908, PD | PG #1695 | 355,410 | `16fde29acf76` |
| `chesterton_orthodoxy.txt` | Chesterton, *Orthodoxy* | 1908, PD | PG #130 | 382,206 | `ec525c93afdd` |
| `carroll_alices_adventures_in_wonderland.txt` | Carroll, *Alice's Adventures in Wonderland* | 1865, PD | PG #11 | 174,311 | `01b38ea4c710` |
| `carroll_through_the_looking_glass.txt` | Carroll, *Through the Looking-Glass* | 1871, PD | PG #12 | 196,534 | `e40a38f5da84` |
| `kafka_der_process_de_1925.txt` | Kafka, *Der Prozess* (German original) | 1925, PD (`copyright: false`) | PG #69327 | 506,239 | `0254e2e361fc` |
| `kafka_the_trial_wyllie.txt` | Kafka, *The Trial* (David Wyllie translation) | free copy w/ permission — **translation © David Wyllie, not PD**; hosted legally by PG | PG #7849 | 476,819 | `31351cb91dcb` |
| `smith_the_game_of_go_1908.txt` | Arthur Smith, *The Game of Go: The National Game of Japan* | 1908, PD | archive.org `gameofgonational00smit` (OCR `djvu.txt`) | 295,609 | `09142f8bf751` |
| `falkener_games_ancient_and_oriental_1892.txt` | Falkener, *Games Ancient and Oriental and How to Play Them* (incl. "The Games of the Ancient Egyptians" / Game of Tau ≈ senet) | 1892, PD | archive.org `gamesancientand00falkgoog` (OCR `djvu.txt`) | 463,493 | `81917378f7e4` |

**Totals: 8 files fetched, 2,850,621 bytes (~2.7 MB). 1 target BLOCKED (Borges — see verdict above). 1 skipped (Ficciones, not PD). No git operations performed.**

Full sha256 (for the registry):

```text
01b38ea4c710a84bc18d0bd41271a5a1a92b94e97b2812f4dece97d4a694725e  carroll_alices_adventures_in_wonderland.txt
e40a38f5da841f9fb6acc557355c447b7c2ccb56a208caf5fcf2b05081f14d42  carroll_through_the_looking_glass.txt
ec525c93afddb05465bf6fa0af8f873078b8e42a2a24f9b999582994f054fdf2  chesterton_orthodoxy.txt
16fde29acf764ba5742fd5db8833f424b6b89c0f6e282d518f6c626006faf6e1  chesterton_the_man_who_was_thursday.txt
81917378f7e481cd928e5a2b7571d152e88dc4ff38846175ae7b7fe3d2901643  falkener_games_ancient_and_oriental_1892.txt
0254e2e361fca684887374ed3e4e4c32f03ac5b7022f54e9a128d1bff6b35b80  kafka_der_process_de_1925.txt
31351cb91dc50deb9bc3fb527b24b1352d4f9743a95f8d1a38bdfe0a9ec6b42f  kafka_the_trial_wyllie.txt
09142f8bf7516e00a63f9ab9fe93af6d979d16202916595f3e49d9ed64e83b79  smith_the_game_of_go_1908.txt
```

### Why each feeds the riddler-seat / parable register

| Work | The one line |
|------|--------------|
| *The Man Who Was Thursday* | The patron text: Sunday is the riddler made cosmology — a chase where every answer unmasks another mask, which is exactly the riddler-seat's answer-with-a-question voice. |
| *Orthodoxy* | The ex-atheist's return, chapter-per-stone: parables that argue for joy from paradox (the madman who has lost everything but his reason) — the register's defense-of-faith spine. |
| *Alice in Wonderland* | The canonical riddle engine ("Why is a raven like a writing-desk?") and the satire of rules that mean nothing — pure riddler-seat cadence. |
| *Through the Looking-Glass* | Mirror logic and the double-cover of looking-glass space: backwards moves win, names run ahead of things — the register's inversion grammar. |
| *Der Prozess* (German, PD) | The unreadable charge, the court that exists only in attics: the parable register's deepest well of institutional absurdity, in the original PD language. |
| *The Trial* (Wyllie, free w/ permission) | English mirror of the above for seat prompts; legal free copy, license noted — redistribution constrained by the © David Wyllie notice, local use per PG terms. |
| Smith, *The Game of Go* (1908) | Go as moral allegory ("a battle of influence, not capture") — the riddler's board-geometry register and the harvest-territory-over-kills ethic. |
| Falkener, *Games Ancient and Oriental* (1892) | Senet/Tau and the sacred-way games: the parable register's oldest stones — play as passage through the Duat, dice as judgment. |
