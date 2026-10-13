# lexicon_FOLD.md — DF language raws fold (2026-09-25)

Source: Dwarf Fortress install (READ ONLY), `data/vanilla/vanilla_languages/objects/`.
Deliverable: `df_lexicon_full.json` — keys: dwarf, elf, human, goblin.

## Counts

Per-language dictionaries are structurally identical (same 2,124 English keys;
only the native words differ):

| lang | entries | nouns | adjectives | verbs | prefixes |
|------|---------|-------|------------|-------|----------|
| dwarf | 3,223 | 1,697 | 829 | 681 | 16 |
| elf | 3,223 | 1,697 | 829 | 681 | 16 |
| human | 3,223 | 1,697 | 829 | 681 | 16 |
| goblin | 3,223 | 1,697 | 829 | 681 | 16 |

Entries exceed keys because 907 of 2,124 keys are multi-POS (e.g. ACE is noun
+ adjective + verb); each (key, POS) pair is its own JSON entry with a
`roles` array of compound-slot tags.

## Fold notes for ArtifactLore

1. **POS tags are not in the dictionaries.** `language_DWARF.txt` etc. are pure
   `[T_WORD:ENGLISH:nativeword]` maps. POS lives only in
   `language_words.txt` (`[NOUN:sing:plur]`, `[ADJ:form]`+`[ADJ_DIST]`,
   `[VERB:5-forms]`, `[PREFIX]`). Any future mining must join on the English
   key; never expect per-line tags in the per-language files.

2. **DF name grammar is slot-tagged, not free.** Compound slots
   (FRONT/REAR_COMPOUND, THE_COMPOUND, OF_NOUN, ADJ_DIST, STANDARD_VERB) say
   exactly where a word may sit in a generated name. Proper DF names pair
   ADJ+NOUN or NOUN+NOUN; 554 dwarven adjectives are FRONT_COMPOUND_ADJ
   capable.

3. **Adjectives the module lacked** (dwarven FRONT_COMPOUND_ADJ, gloss ->
   native): ancient `zustash`, amber `thukkan`, ardent `kíddir`, acrid
   `tatek`, absolute `ilas`, ashamed `mangròd`, bold `murak`, bloody `nashon`,
   putrid `uvir`, small `est`. Rich vein vs. prior adjective stock.

4. **Encoding trap: raws are CP437, not UTF-8.** `etäg` stores as 0x84;
   UTF-8 decode yields U+FFFD mojibake silently. Parse with `cp437`, emit
   UTF-8 (`ensure_ascii=False`). The JSON on disk is verified clean.

5. **Symmetry is a feature:** all four languages share one keyset, so
   cross-language word-shape studies (elf vowel-heavy vs dwarven consonant
   clusters) need no alignment pass. Example mined compounds:
   `etägustos` (big+anger), `istbardan` (rose+couple), `estbanik` (small+hex).
