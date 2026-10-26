# CACHE_FARM_GAME_PROMPTS — self-contained game prompt anatomy
Research lane · 2026-09-01Z · operator directive: learn prompt structure for cache farming off z.ai "Mini Game" tab.

## 1) Find table (URLs + verify status)
| Source | Prompt structure carried | Verify |
|---|---|---|
| github.com/chojondocho/single-html-game-bench | zero-shot single-HTML game prompt, cross-model | 200 raw README, exact text quoted |
| github.com/megadigo/OnePromptGame (GAML schema) | frozen YAML metadata: config/entities/states/win | 200 raw README + GAML file |
| github.com/dontriskit/awesome-ai-system-prompts/.../Z.ai/prompt.md | official z.ai frozen scaffold prompt | 200 raw |
| summerengine.com/blog/tell-ai-what-game-to-make | 4-part variable "brief" structure | 200, exact 4-points quoted |
| github.com/shumatsumonobu/one-prompt-games | strict one-prompt style | 200 repo, incl. docs/{space-shooter,breakout,asteroid-dodge} |
| z.ai coding UI "Mini Game" tab | operator-confirmed previews 11:24Z (board game, grid, Memory Match) | operator drop; no published z.ai template found → UNVERIFIED structure |

## 2) Common anatomy across working prompts (frozen elements by how rarely they change)
Ranked most→least stable across all five sources:
1. **Output contract** — always: complete, single `.html`, vanilla JS/canvas, no deps, playable immediately. Never varies.
2. **Engine scaffold** — `requestAnimationFrame` 60fps loop, `<canvas>` id, keyboard/touch input, game states (menu/play/gameover/pause). GAML freezes this as `implementation/window/entities/game_states/ui`.
3. **Asset pipeline** — inline sprites/colors/shapes, Web Audio oscillators (no external assets).
4. **Data/state conventions** — localStorage for high score.
5. **Rules engine / entities** — player/enemies/collectibles specs (varies per game type).
6. **Win/lose + theme** — the ~20% tail. Varies every instance.

Benchmark prompt isolates the tail maximally (one concept line); GAML is the opposite extreme (fully frozen scaffold, game-type deltas as tail).

## 3) Proposed template for OUR game prompts (cache-farm structured)
**~80% frozen scaffold (prefix, verbatim every run):**
```
You are an expert HTML5 game developer. Build ONE self-contained
.html file, vanilla HTML/CSS/JS + <canvas id="game-canvas">, no
external libs, no CDNs, no console errors.
Frozen engine: requestAnimationFrame 60fps loop; game states
menu/playing/paused/gameover + restart + score + high-score via
localStorage; keyboard (arrows/WASD/Space) + mouse/touch.
Frozen asset pipeline: shape/canvas art only, gradients ok, Web
Audio oscillators for SFX, responsive layout, mobile-safe.
QA checklist (must all pass): opens doubled-clicked cold; no
infinite loops; every control mapped; score persists; instant win
and loss path reachable.
Output ONLY the complete HTML. No markdown, no extra text.
```
**~20% variable tail:**
```
GAME_THEME: "<one line: title + genre>"
MECHANICS_DELTA: "<2-3 bullets differing from stock>"
WIN: "<goal>";  LOSE: "<fail condition>";  ART: "<2 words>"
```

**Cache-hit rationale:** the scaffold prefix is byte-identical across all crypto-games; LLM output cache keys on exact input prefix, so the LONG frozen prefix is 100% cache-miss-avoided after the first generation in the family — only the short tail + generation differ per instance. Z.ai "Mini Game" tab previews (Memory Match, grid, board game) confirm these are low-fanout single-file workloads: ideal for a prefilled theme menu → maximal prefix reuse. Short output (~1 html file) also means small cached-input delta per run.

## 4) Fetch log
1. web_search x3 — swept z.ai/artifacts/reddit, surfaced primary repos.
2. web_fetch chojondocho raw README → 200, quoted prompt VERIFIED.
3. web_fetch megadigo raw README + gaml file → 200, frozen schema VERIFIED.
4. web_fetch dontriskit Z.ai/prompt.md → 200, official z.ai frozen scaffold VERIFIED.
5. web_fetch shumatsumonobu api contents → 200, per-game docs VERIFIED.
6. web_fetch summerengine blog → 200, 4-point brief VERIFIED.
7. web_fetch docs.z.ai/devpack/tool/zcode → 200, ZCode ADE context only (no mini-game template published). z.ai "Mini Game" tab = operator-confirmed, structure UNVERIFIED.
Two-strike: none hit (all fetched 200 first shot except docs path 404 on one guess, bailed immediately).
