# SPORE SEED — race/dice family germination seed (v1, 2026-09-01)

> The canonical spore: byte-identical across fan-out lanes except the APPENDIX line.
> Cache-farming shape: everything above the appendix is shared prefix material.

## MISSION
Germinate one cultural game into a corpus L3 pack. The pack is a delta over the race/dice engine — not a full rules rewrite. Output: (a) the pack file, (b) a one-paragraph PLAYABLE BUILD PROMPT (a single instruction that makes any LLM produce the playable game).

## ENGINE REFERENCE (read first)
- /board/corpus/L1_engines/race_dice.DRAFT.md (race engine: linear/ring track, seeded movement, bear-off/win, capture-on-landing flag)
- /board/corpus/L0_universal_contract.DRAFT.md (six-function contract, universal RNG protocol — LLM never improvises rolls)

## PACK TEMPLATE (your output file follows this exactly)
```
CULTURAL PACK: {game}
ENGINE: race_dice
RULE DELTA: only what differs from the engine (track shape, movement source, special squares, win condition)
HISTORICAL MODULE: era, culture, archaeology, sources, uncertainties — with research_status: attested|reconstructed|speculative
MATERIALS MODULE: original pieces (sticks/cowries/beans/tetrahedra) with modern-skin equivalents
REGIONAL VARIANTS: named deltas
ETHICS/ATTRIBUTION: origin culture, sources, sensitivity notes
BUILD PROMPT: one paragraph — the one-shot instruction
```

## OUTPUT CONTRACT
1. Write the pack to /board/corpus/L3_packs/{game}.DRAFT.md (DRAFT header, research_status field present).
2. Never invent archaeology: contested history ships as named competing schools.
3. Dice: seeded external resolution only; historical RNG modes per the L0 protocol.
4. Byte-stable formatting: static-first, your variant content last.

---APPENDIX--- (the ONLY variable line)
