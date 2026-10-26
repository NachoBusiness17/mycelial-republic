---
name: df-wiki-mine-20260925
description: DF wiki mined 9/25 (LINKS-341/342) per operator law "mine it all,
  why else would i put this here" — Dwarven_language raws parsed (2,122 words,
  41 banked in tools/df_words.json), DF naming laws kept verbatim,
  ArtifactLore.luau built and wired into LedgerExchange (dwarven names +
  strange-mood lines on every Marble Run artifact)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_d7f6f4b6-0b61-484e-8bea-0408db77ca4f
---

Operator dropped dwarffortresswiki.org with "useful", then "mine it all why
else would i put this here". Mined same session: the wiki needs a browser
User-Agent (bare curl times out/404s) and /index.php/Page paths. The
Dwarven_language page carries the dictionary in DF raws format
`[T_WORD:ENGLISH:dwarven]` — 2,122 words parsed, 41 evocative ones banked
(mosus room, nazush blood, shedim shadow, edëm key, zuntîr anvil...) in
tools/df_words.json.

Laws kept from the Name/Artifact/Strange_mood pages: first word stays
untranslated, names are two-word compounds (Noun-Noun/Adj-Noun/Verb-Noun);
artifacts are "the ultimate expression of desires, fears, memories and hopes
in art-form"; moods are Fey/Secretive/Possessed; ☼ = masterwork quality ring.

Built `roblox/src/shared/ArtifactLore.luau` (dwarvenCompound/name/moodLine,
generated programmatically from df_words.json — do not hand-edit the word
table) and wired into LedgerExchange: every Marble Run artifact carries a
dwarven compound name + mood line on its billboard, and buys write the full
lore string to the ShadowLedger. Upgrade path on record: generated chronicles
(legends mode) for the MUD rooms, wiki-with-numbers as THE MOUNTAIN doc
standard.

**WORLDGEN MINE (operator: "mine it for data and world gen ideas and novel
mechanics", LINKS-343, commit fa268fcbd):** ages law folded — worlds start in
the Age of Myth, megabeast deaths drive transitions, ages recur with ordinals
("The Second Age of Legends"); `Worldgen.luau` implements `ageText()` and
Ossuary King fells call `noteBossKill` so the world age is live server state.
Forgotten-beast law folded: Hall wisps announce mined dwarven names + sourced
spheres (caverns/water/theft/thralldom/darkness/suicide/muck from the
Forgotten_beast page; animals/nature/plants/rivers from Titan raws
[SPHERE:] tokens). Villain temptation-vs-values law registered as the Vellum
plot template (signing the grant = temptation roll against counted-chairs
history). Full laws + owed register in roblox/docs/WORLDGEN_MINE.md: full
sphere list renders as a graph IMAGE on the wiki (needs a public
list_sphere.txt mirror), the <=3-great-powers age branch and the villain
rumor/informer loop are unmined. Mountain's three great powers: THE ANSWER,
THE SKELETON KING, THE MAKER.

Related: [[the-mountain-roblox-20260924]], [[pratchett-mud-crosswalk-20260918]]
