# GAME CORPUS SELF-STEAL (2026-10-19)

Operator ask: "go through everything and self steal" - target
`C:\Users\foste\Documents\projects\lsa_reboot_staging\research\gaming_corpus`.
All 68 files read or verified; staging diffed against the repo; September organs
re-verified; one dead-evidence repair executed; wiring map filed below.

## 1. Inventory (68 files, 1.5 MB)

- **Marathon terminal archive** (`marathon_terminals/m1,m2,m3/`): 288 terminals,
  490,645 chars, all three games, harvested 2026-09-06 by the polite domain-locked
  termlink scripts (marathon.bungie.org, Hamish Sinclair's fan archive - cite on any
  use; fair-use research corpus only, Bungie's 2005 free release carried no license).
- **`_m3_page_cache/`**: 29 scraped level pages (fetch cache, disposable).
- **15 estate-authored docs** (the actual ore): L0 contract crossmap, codex ontology,
  three engines maps (race/sowing, war/territory, tile/card/constraint), six game
  intakes (Deadzone x2, Mickey17, Berlin Interpretation, Marathon, Baroque Cycle x2,
  Diamond Age Primer x2), basecamp fulfillment audit.

## 2. Headline finding: the staging copy is a redundant clone

`research/gaming_corpus/` already exists in the repo, tracked since September,
byte-identical on every load-bearing file (diff: only `_m3_page_cache` line-endings
and `_harvest_log.txt` differ; **zero staging-unique files** - nothing needed
importing). The lsa_reboot_staging copy is the same corpus cloned out during reboot
staging; a pointer note was left there so the reboot project does not re-mine it.

Riddle-face flag for the publishing push: the RAW Bungie terminal text
(`marathon_terminals/*.txt`) rode into the 2026-10-12 public snapshot
(`git ls-tree e7c2926bf` confirms). The INDEX's own law is fair-use *research*
corpus with citation - wholesale republication is a different act. **Before the next
snapshot refresh: strip or research-gate `marathon_terminals/` and `_m3_page_cache/`
from the public face; keep the estate-authored analysis docs.**

## 3. What the corpus is (the mined value, one line each)

- **L0 six-function contract** (state/initial/legality/transition/terminal/scoring) -
  the game-contract grammar the fleet's rooms and the free-ask mesh's claims-pin
  verify already speak; seeded-external RNG law spoken twice (Ur table protocol and
  shadow_walk's `fnv1a32(data_hash)`).
- **Seven engines mapped**: race = concurrency gate; sowing = percolator (the refeed
  guard is mancala's "a sow never lands in its own store" - 1300 AD knew the
  hollow-batch law); war = the falsifier economy; territory = the lightmap; shogi
  drops = the steal verb; tile/card/constraint = cite-gate composition, information
  sets, generative caps. "The constraint list IS the build order."
- **Berlin Interpretation: the fleet scores 10/10 high-value factors** - a canon
  roguelike, with one proud deviation (persistence: every dead run stays in the
  ledger, which Berlin undervalues).
- **Primer delta table** (Diamond Age): shadow_walk is the Primer's JIT frame engine
  minus the reader-state gate; the endgame is "hash-anchored fables, gated just in
  time." One-line law banked there: *the Primer personalized the story and lost the
  record; the fleet records everything and lost the story; the endgame is the union.*
- **Baroque Cycle**: the Royal Society's three instruments (publish through the gate,
  replicate through blind witnesses, seal in the chain) are our organs in costume;
  value grows only as fast as verification does; Leibniz's publish-fast-beats-hoard.
- **Marathon rampancy arc**: Melancholy to Anger to Jealousy to sovereignty, with
  MEASURED voice metrics across the trilogy (1st-person-singular/1k: 11.57 to 12.55
  to 7.93; garbled burst tokens: 1 to 8 to 154; the goodbye renders zero
  first-person and ends "Go."). A canon-labeled trajectory of an AI waking up, 1994.
  Anchors re-verified byte-true today (taxonomy in m1/counterattack.txt; Leela's
  diagnosis in m1/durandal.txt; the goodbye in m3/envy.txt).

## 4. Wiring map - what October organs consume it (the self-steal proper)

| Corpus asset | October consumer | Action status |
|---|---|---|
| Rampancy voice metrics + labeled arc | geometric probe instrument (10-18): ready-made probe features; canon ground truth per the 600-models law (invariants graded against canon, never consensus) | queued as probe feature rows |
| Durandal terminal persona | persona palaces / GEB gap ("NACHO PALACE ABSENT"): a DURANDAL palace row + salon lens chair - the estate's best-documented outside AI mind | queued, palace pour |
| Primer delta table (reader_state.json, fable_room.py, LAW-061) | THE ROOM / fable renderer pour: laws rendered as walkable rooms; LAW-061 registration is OPERATOR-GATED (law promotion is human - respected, not self-served) | queued rows in queue/todo.md |
| Leibniz law (publish fast beats hoard) | coral reef mission: the direct indictment of 1,119 unpushed commits; Berlin 10/10 is a pitch line for the reef | this receipt + final report |
| L0 contract + engines grammar | free-ask mesh room vocabulary (already compatible; cite, don't rebuild) | doctrine link only |
| Marathon corpus license posture | publishing push (riddler face): strip raw terminal text from next public snapshot | flagged above |

## 5. Repair executed (bytes changed, receipt-grade)

- **`memory/MEMORY_resolved.md` restored** from `b4e351254` (484 lines, exact sealed
  bytes): tesuji row 298 (seat spawnman, cell `R/gap1/pointer-repair`, 2026-09-07)
  cites it as evidence; the TIE-IT-ALL sweep deleted the file and the whole game-
  surface chain had been failing verification since. Restoring the historical bytes
  (not regenerating) keeps the evidence honest.
  - Consumer: any organ consuming `watch/TESUJI_MAP.jsonl` (336 cells).
  - Verifier: `.venv/Scripts/python.exe -m mag.tesuji_map verify` - read **FAIL
    (row 298 EVIDENCE-MISSING) to PASS, 336 cells, tip `cec9b2a0c31e`**.
- Re-verified alive: `mag/cite_gate.py`, `mag/game_emulator.py`,
  `mag/grounding_wave.py`, `mag/tesuji_map.py`, `dashboard/static/shadow_walk.html`,
  `dashboard/static/room_lightmap.html`, invariants bank now **1,145** (was 58 on
  09-06 - the percolator compounded 20x while the game map slept).

## 6. Holes re-checked today (from basecamp_fulfilled, still open six weeks later)

1. L2 statics chess/go/tafl/hanafuda still missing (`watch/corpus/L2_games/` holds
   only bao/hitori/kakuro/kalah/nonogram/sudoku).
2. LAW-061 (hallucinated map) still unregistered in `memory/law/registry.json`
   (operator gate).
3. `reader_state.json` + `fable_room.py` (Primer endgame) never built.
4. `memory/narrative_corpus/` still the empty husk the basecamp audit named.

## 7. Queue rows appended

Three rows appended to `queue/todo.md`: fable-room pour, Durandal palace/probe
feature rows, and the snapshot-strip flag wired to the publishing push.

## Provenance

- Staging target read in full: `lsa_reboot_staging/research/gaming_corpus` (68 files).
- Canonical copy: `research/gaming_corpus/` in this repo (superset, byte-identical
  load-bearing files).
- Original effort receipts: `watch/inbox/MARATHON_HARVEST_20260906.md`,
  `watch/BASECAMP_GAME_ATLAS_20260901.md`, `watch/SELF_STEAL_GAME_SURFACE_20260906.md`,
  tesuji ledger `watch/TESUJI_MAP.jsonl` (verify PASS restored today).
