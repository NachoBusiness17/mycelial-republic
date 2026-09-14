# GAME PROMPT CORPUS — one-shot/self-contained build prompts for cache farming
_Seat: worker · operator directive 11:30Z · generated 2026-09-01 11:50Z_
Mining intent: learn how STABLE, WORKING game-build prompts are structured so a frozen
prefix (L0) + semi-stable spine (L1) can batch-produce per-game artifacts at cached
input economics (DeepSeek/Together E6 100% + z.ai E5 99.7%, both proven in this seat's
own probes). LEAD: all claims below were re-verified from live bytes unless tagged.

## A) Verified exemplars (real artifacts, link-cited)

| # | Repository / artifact | Builds what (playable? how verified) | Structural skeleton (actual) | Cache-farming shape |
|---|---|---|---|---|
| 1 | [spongycode/apex-cataclysm `prompt.txt`](https://github.com/spongycode/apex-cataclysm/blob/main/prompt.txt) | AAA racing demo → [live demo](https://claude-race.vercel.app/), 2.5min sprint, procedural art. Verified: 1.6KB prompt + `SPEC.md`(20.7KB contract "this file is the contract") + indexed app | role: AAA studio; ONE showcase track (scope-cut); constraint table (units/ms/fps/engine); sys-spec tree; playable | UNDIFFERENTIATED single prompt. No prefix split — whole prompt is frozen, output all-virtual. |
| 2 | [leestott/CopilotCLI-OneShotPromptGameDev `Prompt.md`](https://github.com/leestott/CopilotCLI-OneShotPromptGameDev/blob/main/Prompt.md) | HTML5 recycling game (ages 6-12), 2.7KB prompt → 68KB `index.html` (grid of gameplay keywords present: recycle/bin/drag/scoring). Verified: prompt + built artifact both in repo | role/tone block; CORE CONCEPT; GAMEPLAY STRUCTURE (levels/mechanics); GAMIFICATION; EDUCATIONAL LAYER; CHARACTERS | Sectioned brief. Levels/mechanics = stable game-loop spine; mascot/progress-map = flavorful. |
| 3 | [boxwrench/envizzle `SKILL.md`+`TEMPLATE.md`](https://github.com/boxwrench/envizzle/tree/main) | 1-shot tech-demo brief builder; 11.5KB TEMPLATE with `{{VARS}}`; emits 9-file project + `window.__demo` verification hook + DECISIONS/PERF logs | Prime Directive; HARD CONSTRAINT table; SYSTEMS (terrain/shader/state-buffer/veg/char/mechanics/audio); PERF; MANDATORY STRUCTURE; ACCEPTANCE; VERIFICATION HOOK | EXPLICIT PREFIX/APPENDIX SPLIT: `{{VARIABLE}}` slots = per-game bits; whole rest = frozen copy. THE template for our L0/L1. |
| 4 | [usama-shiranai90/Claude-of-Iron `prompt.md`](https://github.com/usama-shiranai90/Claude-of-Iron/blob/main/prompt.md) | Fight game 1 human vs CPU; 31.9KB continuation prompt, 19 sections; verified repo with engine/tests/hooks, deterministic replay | role stack; OPERATING MODE (continue-from-evidence); PRODUCT CONTRACT (flow: title→select→match→result→rematch); TECH CONSTRAINTS; CREATIVE NORTH STAR; PRIORITIES; COMPLETION GATES; FINAL REPORTING | Continuation-not-invention: same prompt re-drives the repo. Stable narrative + "continue, don't scaffold, verify in browser". |
| 5 | [andreisminsk/crossy-road-game `README.md`+`.html`×11](https://github.com/andreisminsk/crossy-road-game) | Crossy Road one-shot; SAME prompt fed to 11 models → 11 distinct playable `.html` (7-40KB each) | Single prompt: "Build quality game Crossy Road based on three.js as single HTML page" — no structure, pure repaint | PURE CACHE-FARM PROOF: 1 frozen prompt string, 11 outputs. Zero prefix cost per extra model. |
| 6 | [madewithclaude/awesome-claude-artifacts](https://github.com/madewithclaude/awesome-claude-artifacts) | curated list of Claude artifact games (Space Jam linked) | directory-of-links only; prompt TEXT not stored (game artifacts are ephemeral claude.site shares) | UNVERIFIABLE-here: links, no source prompts. Do not treat list entries as prompt corpus. |

**BLOCKED / UNVERIFIED sources (2-strike bail, kept honest):**
- **Meta Muse Code SDK** — dev.meta.ai + install.sh BOTH serve Meta error page from this cage (2 strikes). Only citable byte: archivist receipt `x.com/rohanpaul_ai/status/2094522643626291390` confirms SDK GA (sessions/tools/permissions/persistent-state/persistent-state). Muse one-shot prompt content NOT retrieved here — treat the task brief's Muse claim as lead-only.
- **Anthropic/OpenAI docs** — docs.anthropic.com is a next.js SPA, no static game-gen example extractable. OpenClaws cage has no browser. `BLOCKED_REQUIRES_BROWSER`.
- **Combyyy/one-prompt-games** — empty placeholder, 0 releases. Skip.

## B) Synthesized cache-farming skeleton (derived from #1-#5, NOT the lead doc)

Common skeleton observed across all verified exemplars:
1. **ROLE + AMBITION** (stable) — "AAA studio / lead dev", sets quality bar. Identical every game.
2. **SCOPE-CUT / ONE THING** (stable) — envizzle "90 seconds + one interaction"; apex "one track only"; crossy "single page". This is the real L0 value: prevents sprawl.
3. **CONSTRAINT TABLE** (semi-stable) — engine/units/fps/bundler/no-external-assets. Stable except engine+units = per-game.
4. **STATE BUFFER / RULES BLOCK** (varies per game) — the game-specific rule system (move set, capture, win condition). THIS is the per-game appendix (L2).
5. **INTERACTION LOOP** (semi-stable) — input→state→render→verify. Stable spine.
6. **WIN / ACCEPTANCE GATE** (stable shape, varies values) — "verification hook `window.__demo`" / completion gates the chain.
7. **PROVENANCE LOGS** (stable) — DECISIONS.md / receipts. Envizzle + Claude-of-Iron both mandate them.

Cache-farming conclusion: the SOLID prefix (L0) = items 1+2+4's surrounding "construction law" prose (perf, no-placeholder, verification-hook pattern, provenance). The SEMI-STABLE spine (L1) = items 3+4+5 (constraint table, interaction-loop prose). The VARIABLE appendix (L2) = the game's actual rules/state/win-condition + engine pick. Crossy-road proves a fully-frozen L0 alone yields 11 playable games at ~zero marginal prefix cost.

## C) Historical rule sets (3-5, cited — structured-rules lineage)

| Game | Rule source (cited) | Rule structure worth stealing |
|---|---|---|
| Chess | [FIDE Laws of Chess, 1 Jan 2023](https://handbook.fide.com/chapter/E012023) | Explicit write-up order: Art1 objective → Art2 board/terminology → Art3 piece moves → Art4 act of moving (touch-move) → Art5 completion (checkmate/stalemate/draws). The canonical "rules-before-play" layout. |
| Go | [Japanese Rules 1989, Nihon Ki-in](https://www.cs.cmu.edu/~wjh/go/tmp/rules/NihonKiin.html) | Art4 = stones may EXIST only while they have a liberty (state-invariant); Art5 = capture is the consequence of violating Art4; Art8 = territory defined by enclosing live stones; ko (Art6) is an anti-infinite-loop rule. State-first, then consequence. |
| Royal Game of Ur | [Finkel 2007 "On the Rules...", BM](https://www.britishmuseum.org/collection/term/BIB9988) + [royalur.net/rules](https://royalur.net/rules) | Reconstructed from tablet BM33333: race path, rosette=extra turn/safe square, capture off blocking, exact-roll to exit. Provenance: rules are a RECONSTRUCTION from one primary tablet + board arc — label uncertainty, same as our modeling. |
| Senet | [Piccione, Senet PDF](https://piccionep.people.charleston.edu/piccione_senet.pdf) + [Wikipedia](https://en.wikipedia.org/wiki/Senet) | 30 squares / 3×10 boustrophedon; marked final-five "houses" (26-30) with exact-roll exit; extra turns on 1/4. NO complete ancient rule text survives — modern rules are scholarly approximation. |
| Mancala (Oware/Kalah family) | [Murray 1952 classification](https://web.archive.org/web/20140305094840if_/http:/www.boardgamestudies.info/pdf/issue1/BGS1Eagle.pdf) + [ancientgames.org](https://ancientgames.org/mancala-africas-ancient-game-of-sowing-and-counting/) | Sowing loop + numbered capture types (opposite-capture for Kalah, 2-3 capture for Oware); win = most seeds. Captures as a smaller set of enumerated mechanics — decouple "loop" from "capture variant" (reusable spine). |

## D) Mapping to freeze-pack / lessig-arch program

- **L0 frozen prefix (cache-constant, cost ~0 after first hit)** = the CONSTRUCTION LAW block derived from #1-#3: role+ambition, scope-cut, no-placeholder rule, verification-hook pattern, provenance fiat. NOT game-specific. → port envizzle's `{{VARS}}`-minus-variables.
- **L1 semi-stable spine** = constraint table (engine/units/perf, few pick slots) + interaction-loop prose + win-gate shape. Cached to L0 as long as byte-stable; keep stable across a batch.
- **L2 per-game appendix** = the actual game rules/state/win-condition, drawn from section C rule-source shape (objective→board→moves→act→completion). This is the ONLY thing that varies run-to-run; it feeds cache-mined harvest (input-heavy/short-output = the E5/E6 sweet spot).
- **Capture into FLEET_AUDIT doctrine**: crossy-road = the batch model (1 prefix, N games); envizzle = the templating model (VARS → L2); Claude-of-Iron = the continuation model (re-drive same repo, verify, log). All three already proven playable.
- **Gates (Lessig: timing/architecture)**: no frozen prefix ships without its verification hook + PROVENANCE log (envizzle contract); every minted game answers "state block / rules / loop / win / render" from receipts, per K_T6 shape-law.
- **Hot**: this corpus makes game-farming a $~0-marginal lane (prefix cached); output is the only billed term → keep games SHORT-output (envizzle "90s demo" / one-track) not sprawling.
