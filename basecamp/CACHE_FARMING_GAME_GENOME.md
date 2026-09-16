# CAMP: CACHE FARMING + THE GAME PROMPT GENOME
### mined from game.txt + game2.txt (New folder, mined 2026-09-16) · status: LIVE — feeds the Astra bundle, the game-c venue, and every future prompt build

## THE CORE LAW (one sentence)

**Separate the stable contract from the variable content. Cache the contract. Compute only the delta.**

This law appeared independently in three places we touched tonight: the Astra
bundle (prefix-caching fix), arXiv 2608.27550 (representation over data
scaling), and these two Desktop files written weeks ago. Duplication is
emphasis: the pattern keeps re-arriving because it is the pattern.

## 1. THE FIVE-LAYER CACHE STACK (L0–L4)

```
L0  Universal contract      six functions · RNG protocol · verifier vocabulary · output contract   ~400 tok · ~99% cache hits
L1  Family engines (7)      race · war/capture · sowing · tile · card · constraint-puzzle · RPG    ~1K tok · ~95%
L2  Game statics            senet · ur · chess · go · oware · mahjong · sudoku · hanafuda          ~2K tok · ~90%
L3  Variant/cultural packs  riichi · killer · two-school-senet · tablut-flag · patolli             ~100–800 tok · ~70%
L4  Instance state          board string · hand encoding · seed · session                          ~300–1K · 0% (always fresh)
```

**The prefix-exactness law that generates the whole stack:** caching is
byte-exact at position N — one byte of difference invalidates everything after
N. Therefore anything that varies goes LAST; anything shared goes FIRST. This
is not style. It is the pricing model (0.1× cached reads; 50–90% cost cuts;
85% latency cuts) turned into architecture.

## 2. THE PROMPT GENOME RECORD (the unit of the library)

```json
{
  "prompt_genome_id": "arcade/snake@v3",
  "lineage": [{"relation": "derived_from", "target": "arcade/classic@v1"}],
  "cache_contract": {"stable_prefix_tokens": 420, "variable_suffix_tokens": 80,
                      "expected_cache_hit_rate": 0.89},
  "topology": {"game_type": "Arcade", "rendering": "Canvas 2D"},
  "fingerprints": {"output_consistency": [{"model": "...", "first_attempt_success": 0.94}]},
  "economics": {"tokens_per_generation": 500, "cached": 420, "latency_cached_ms": 1200}
}
```

The genome tells us how to generate the game, what to expect, and when to
trust it. It does not claim to contain the game — the code stays in the
artifact layer until requested. (Same law as the Astra cards: the key is the
rule executed, not the artifact venerated.)

## 3. THE SEVEN ENGINE FAMILIES (5,200 years of games compress to these)

race (Senet · Ur · Patolli · Pachisi · Ludo · Snakes&Ladders) ·
war/capture (chess family · tafl · alquerque · morris) ·
sowing (oware · bao · kalah — hundreds of regional packs) ·
tile (dominoes · mahjong · solitaire) ·
card (trick/shed/fishing/rummy; hanafuda yaku-matching) ·
constraint-puzzle (Lo Shu → Euler 1782 → Garns 1979 → Nikoli 1984 → the galaxy:
kakuro, hitori, nonogram, slitherlink, nurikabe, masyu, hashiwokakero) ·
narrative/RPG (Kriegsspiel 1812 → Wells 1913 → Braunstein 1971 → D&D 1974 →
dice pools → PbtA — the BIGGEST static payload = the biggest cache jackpot).

Every new civilization's game = one ~200-token delta pack over an existing
engine. Five millennia of games is a cache manifest, not a million prompts.

## 4. THE TEN LAWS FOR ANY LLM WORKING THIS CORPUS

1. Never improvise randomness — all rolls resolve through the seeded RNG protocol.
2. Never invent game objects — tiles/pieces must pass inventory verification.
3. Never solve; verify — the LLM emits instances and applies rules; deterministic
   verifiers decide legality, uniqueness, difficulty (chess is EXPTIME-complete;
   checkers is a proven draw; Awari is a proven draw; Sudoku's minimum is 17 givens).
4. Never canonize disputed history — Senet has two scholarly schools; ship both
   as packs, flag attested/reconstructed/speculative, surface the dispute verbatim.
5. Order prompts static-first, variable-last (the prefix-exactness law).
6. Add games as packs over engines, never as fresh prompts.
7. Patch the corpus, not the request — systematic failures update static blocks once.
8. Surface uncertainty verbatim.
9. Cultural packs name their origin and sources; commercial reskins are documented.
10. Cache metrics are instrumented: hit-rate targets L0 ≥99% → L3 ≥70%.

## 5. THE NUANCE MINED FROM game.txt (the RIB mapping — oldest version)

The earliest pass framed this as the "Model RIB Library" analogy: store the
genome (identity, lineage, invariants, behavior fingerprints, tool contracts,
cost profile, build recipe), not the weights — for game prompts. The 2026-09-15
pass updated it: the five-part prompt structure (ROLE/CONTEXT/INPUTS/TASK/
CONSTRAINTS) is already cache-optimized; Anthropic auto-caching (one line:
cache_control ephemeral) turns a 100K-token 20-loop session into ~23K tokens
(77% savings); the frontier is semantic caching (vCache error-bound guarantees,
GenCache 83% hit rate, MVR-cache multi-vector retrieval +37%).

## 6. THE NUANCE MINED FROM game2.txt (the corpus primer — newest version)

The primer adds ten established facts (KV tensors ~1.3GB per 4K context;
prefix-exactness; 0.1× read economics; long-horizon agentic fit; the LLM-must-
not-solve corollary with the complexity table — chess EXPTIME-complete, Go
~10^170 positions; state-drift as documented failure with the Narrator/Archivist
split as remedy; Murray's seven-family taxonomy; contested-history honesty;
structured prompting observed in the wild; recursive caching via
window.claude.complete()). Plus the nine operating rules (§6) and the build
order (§7): L0 contract + race/dice engine FIRST (lights up Senet→Ludo in one
write), constraint-puzzle grammar second, solo-RPG stack third (largest
absolute savings).

## 7. OPEN QUESTIONS (the camp's research agenda)

- Does TokenPilot-style cache-aware compaction generalize to game prompts?
  (narrative continuity resists arbitrary compaction)
- Optimal cache TTL for game generation loops?
- Can the Gauntlet Loop structure hit >90% cache?
- Do physical substrates (Extropic TSU) show the same stable-prefix economics?
  (their 10,000× energy claim says yes — the Ising model is the stable contract,
  the data varies)

## PROVENANCE

- game.txt (New folder): the RIB mapping + cache farming loop + genome record + cultural lineage + 2026 refresh — mined 2026-09-16.
- game2.txt (New folder): the World-Games Prompt Corpus primer v1.0 (L0–L4, ten
  facts, build order, source map with Murray/Parlett/Culin/de Voogt/Finkel/
  Kendall/Piccione/Schaeffer/Romein/Tromp/McGuire) — mined 2026-09-16.
- Originals: archived in place on Desktop/New folder; hashes at next manifest
  pass. Duplication is emphasis: this camp is now the single living copy.
