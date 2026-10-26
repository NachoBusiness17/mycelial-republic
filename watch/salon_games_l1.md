# SALON L1 — PROMPTS AS GAMES, STRUCTURED FOR CACHE FARMING
_Seat: worker · lens: CORPUS-STRUCTURE · 2026-09-01_
Sources: MOONSHOT_RIGHT_TIME_20260901.md (Q5) · SALON_RIGHT_TIME_SYNTHESIS_20260901.md
(E6/E5 PASS) · GAME_PROMPT_CORPUS_20260901.md (present) · GAME_PROMPT_GENOME_LEAD
(external LEAD) · PACK_DIAMOND_AGE_SYNTHESIS_20260830.md.
All prices/mechanics quoted from those bytes unless tagged UNVERIFIED.

## 1) STABLE-PREFIX SKELETON
Across verified exemplars (apex-cataclysm, CopilotCLI-OneShot, envizzle, Claude-of-Iron,
crossy-road — corpus §A) + rules lineage (chess/go/ur/senet/kalah — §C) the spine splits
into SHARED PREFIX vs PER-GAME APPENDIX.

**SHARED PREFIX (identical every game → L0/L1 cache material)**

| field | class | byte-stable? |
|---|---|---|
| ROLE+AMBITION | "AAA studio / lead dev", quality bar | STABLE (L0) |
| SCOPE-CUT / ONE THING | "90s+one interaction" (envizzle), "one track" (apex), "single page" (crossy) | STABLE (L0) |
| CONSTRUCTION LAW | no-placeholder, no-external-assets, verify-hook pattern, provenance fiat | STABLE (L0) |
| CONSTRAINT TABLE | engine/units/fps/bundler — shape stable, VALUES per-game | SEMI-STABLE (L1) |
| INTERACTION LOOP | input→state→render→verify prose | STABLE (L1) |
| WIN/ACCEPTANCE GATE | `window.__demo` / completion-gate shape | STABLE shape (L1) |
| PROVENANCE LOG fiat | DECISIONS.md / receipts / "continue, don't scaffold, verify" | STABLE (L0) |

**PER-GAME APPENDIX (the ONLY varying material → L2)**
- BOARD STATE / piece layout (go Art4 liberty-invariant; chess FIDE Art2)
- MOVE SET / capture rules (chess Art3; kalah — decouple "loop" from "capture")
- WIN-CONDITION GRAMMAR (chess completion Art5; go territory Art8; ur exact-roll exit)
- TURN/ACT MACHINE (chess Art4 touch-move; ur rosette extra-turn)
- RULES-ORDER TEMPLATE (steal every time): objective→board→moves→act→completion. This
  ordering is the field-level contract so any appendix parses into any prefix.

Cache corollary: crossy-road = 1 frozen prefix string → 11 playable games (§A row 5)
proves shared portion carries the batch; appendix is pure delta.

## 2) FREEZE-PACK MAPPING (L0/L1/L2 → skeleton → warm cache)
One game's prompt becomes the next's warm cache by freezing L0+L1 byte-stable, swapping
only L2. Meter-field `usage.prompt_tokens_details.cached_tokens` is the hit-witness.

| row | Freeze pack | Skeleton fields held | Cache effect | Byte rule |
|---|---|---|---|---|
| 1 | L0 CONSTRUCTION LAW | role/ambition, scope-cut, no-placeholder, verify-hook, provenance | cached 1st call → ~0 cost after | frozen, append-only, never edited in place |
| 2 | L1 SPINE | constraint-table SHAPE, interaction loop, win-gate shape | cached while byte-stable across batch | keep stable one batch, then bump version |
| 3 | L1 VARIABLES | engine pick, units/fps, few slot values | small billed delta within L1 | the envizzle `{{VARS}}` slot fill |
| 4 | L2 APPENDIX | the game's rules/state/win/move-set | ONLY billed input; short=cheap | objective→board→moves→act→completion |
| 5 | L2 source | chess/go/ur/senet/kalah rule shapes (§C) | parses into any L0/L1 | reuse ordering + state-invariant |
| 6 | VERIFY HOOK | `window.__demo` / acceptance gate | per-game value, not invoice | minted game must answer state/rules/loop/win/render |
| 7 | PROVENANCE | DECISIONS.md / receipts / continuation fiat | zero cache cost | K_T6: "what built/when/why" from receipts |
| 8 | Meter | `cached_tokens` field (E5/E6) | the rollover witness | log per call; M-L1 (never infer balance from a 200) |

Architecture: L0 = mega-prefix every request reuses verbatim; L1 = batch spine stable
while N games mint; L2 = the one thing that varies. Same model+routing id + same bytes
= cache hit.

## 3) BUILD-FARM DESIGN (cache-first production)
**Design:** one `game_prefix` file = L0+L1 byte-stable, append-only. Every per-game request
= `game_prefix` + `\n---APPENDIX---\n` + {L2 only}. Batch loop (crossy model, §A5/§D) mints
N games from the same frozen prefix → N-1 pay ~zero input on the shared bytes.

**Economics (E6, Together V4-Flash, quoted §E6):**
- uncached in $0.14/M · cached in $0.03/M (≈4.7× discount) — E6 B-call 9176/9177 prompt
  tokens cached = 100% hit.
- L2 appendix (~1-2k tok) is the only billed input/game; at 100% prefix hit ≈
  $0.03/M × 2k ≈ **$0.00006**/game.
- Volume (input only), 100 games × (5k prefix + 2k app): all-fresh = 100×7k×$0.14/M
  ≈ **$0.098**; frozen = 100×2k×$0.03/M ≈ **$0.006** → **~17× savings**.
- Zai-mirror (E5, quoted): $0.075/M vs $0.015/M cached (5×), 99.7% hit → same farm rides
  a 2nd provider; parallel arms keep independent prefixes (no thrash). Input-heavy/
  short-output is the sweet spot (output bills full ~$4.40/M — keep games SHORT, §D).

## 4) NAMED RISKS — WHAT BREAKS THE CACHE + THE METER THAT CATCHES IT
| risk | failure mode | catcher |
|---|---|---|
| R1 PREFIX BYTE DRIFT | any byte change in L0/L1 → whole prefix cold | sha256 of `game_prefix` beside receipt; rebuild only if hash differs |
| R2 TEMPLATE JITTER | `{{VARS}}` slot / delimiter drifts | fixed separator `\n---APPENDIX---\n`; §B "slot=per-game, rest frozen copy" |
| R3 APPENDIX POLLUTION | game rules leak into L0/L1 (breaks cross-game reuse) | L2-only rule; receipt gates state/rules/loop/win/render split (K_T6) |
| R4 MODEL/ROUTING | endpoint toggle resets cache namespace (E6/E5 meter same field) | meter per call; expected-hit with cached_tokens==0 → BLOCKED/diagnose, no silent re-bill |
| R5 CACHE EVICTION/TTL | provider drops prefix after idle/length window | expected-hit with cached_tokens==0 → WARN row; reprime outside batch |
| R6 VERIFY-HOOK SILENCE | minted game ships without `window.__demo` / acceptance pass | PROVENANCE gate: no receipt without verify-hook + provenance log (§D step 6) |
| R7 OUTPUT BLOAT | long outputs bill full weight (~$4.40/M) → farm inverts | scope-cut (90s/one-track) is a hard L0 field, not advisor |

**Primary meter:** `usage.prompt_tokens_details.cached_tokens` per call, logged; hit-ratio
per prefix + per batch is health. Batch ratio drops below expectation → R1/R4/R5, never
re-bill blind.

---
_4 sections met, field-level skeleton, E6 token math incl. 4.7×/17×. No other files
modified. GAME_PROMPT_GENOME_LEAD numbers (vCache/GenCache/MVR 77%/83%/+37%) NOT used as
evidence — external LEAD, UNVERIFIED._