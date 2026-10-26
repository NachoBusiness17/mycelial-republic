# STEAL: One-Shot Frontier Game Prompts — verified corpus (2026-09-24)

All items below verified via live web search / GitHub API / page fetches on 2026-09-24. Nothing from memory.

## The common anatomy (steal this)

Every verified one-shot game prompt shares six load-bearing moves:

1. **One artifact, zero build step.** The artifact constraint IS the prompt's spine: "Create a single HTML file containing CSS and JavaScript…" (Alex Albert's canonical opener). "Single HTML out" is even the scoring rule of whole benchmarks (goldiebench.com). Canvas or Three.js inside one file.
2. **Explicit feature checklist as bullets** — enumerated mechanics/data, not prose vibes: "Show the wind speed, precipitation and humidity"; Ozgur Ozer's city prompt enumerates skyscrapers, roads, moving cars, traffic lights, pedestrians, lampposts, day/night cycles.
3. **Juice demanded as a quality bar, not a feature:** "Animations should be smooth and elegant", "Should be a delight to look at", and the purest form — "Make it hilarious to play" (zack/@wenquai). Affect words do real work.
4. **A built-in demo loop / interaction contract stated up front:** "Clicking should cycle through a set of cities and weather conditions." Controls, replayability, and state transitions are specified before aesthetics.
5. **Named aesthetic references:** "GTA 1-style", "8-bit", "glass-like", "Jony Ive style" — one borrowed visual vocabulary replaces paragraphs of styling spec.
6. **Multi-turn shape = iterate against a visible reference:** documented verbatim from a viral three.js build: "Recreate this in a single HTML file with three.js. Keep comparing it against the reference and fix any differences." Plus incremental asks ("now multiplayer", "now ads") — the fly.pieter.com trajectory.

Tone is consistently short, imperative, unhedged. No system-preamble, no role-play.

## Verified examples

**1. Alex Albert (Anthropic) — animated weather card, Feb 24 2025.** The canonical single-file prompt of the Claude 3.7 wave. Verified opener from the post itself: "Create a single HTML file containing CSS and JavaScript to generate an animated weather card. The card…" with the widely republished bullet checklist (wind/precipitation/humidity; smooth elegant animations; delight to look at; day/night styling; click cycles cities). Not a game — but the template every game prompt copies. https://x.com/alexalbert__/status/1894426652429738349

**2. zack (@wenquai) — "Anthropic Researcher Simulator", Feb 2025.** HTML/Three.js job-sim of an AI researcher's day (searching for reward hacks, waiting on jobs, coffee); prompt ends "Make it hilarious to play." Prompt paraphrase verified via FavTutor's collection. https://twitter.com/wenquai/status/1894109880253833241 · collection: https://favtutor.com/articles/claude-3-7-sonnet-examples

**3. Rowan Cheung — Minecraft clone in one prompt, Feb 2025.** Viral anchor of the wave. Trajectory only — prompt text not published. https://twitter.com/rowancheung/status/1894106441536946235

**4. Ammaar Reshi — heart-rate Snake on Apple Watch, Feb 2025.** ~5 prompts; snake speed keyed to live heart rate. Multi-turn refinement shape (game core → sensor wiring → juice). https://x.com/ammaar/status/1894131337583288636

**5. Ozgur Ozer — Three.js living 3D city, Feb 2025.** Checklist prompt (skyscrapers, moving cars, traffic lights, pedestrians, day/night, camera controls). Prompt described, verified via FavTutor. https://twitter.com/ozgrozer/status/1894125497379926101

**6. Pieter Levels — fly.pieter.com, Feb–Mar 2025.** The most commercially viral case: 3D flight sim built with Claude 3.7 Sonnet in Cursor in ~30 minutes, later multiplayer with in-game ad billboards (six-figure revenue claims). Prompted trajectory published on X; original ask widely reported as "make a 3D flying game in the sky with a plane" — trajectory only. Spawned his 2025 vibe-code game jam (1,000+ entries). https://fly.pieter.com · https://levels.io · coverage: https://snyk.io/blog (Highs and Lows of Vibe Coding), Creative Bloq, Mar 2025.

**7. Matt Godbolt — daredevil-demis, 2026.** "An attempt at one-shotting a BBC Micro game with Claude and jsbeeb-mcp": playable spoof of Daredevil Dennis in 6502 assembly, browser-playable via jsbeeb, with an MCP screenshot/memory/autopilot test harness published in `tools/`. Prompt text not in the README — trajectory only, but the eval rig is the steal here. https://github.com/mattgodbolt/daredevil-demis

**8. @amgauge — "Claude Code building 100 mini games with one prompt (5.3M tokens)", Mar 2026.** HN-carried. https://twitter.com/amgauge/status/2031809325375897931 · https://news.ycombinator.com/item?id=47340379

**9. Simon Willison — correction to the brief.** His collections are the **pelican SVG benchmark**, not playable games: prompt is one line — "Generate an SVG of a pelican riding a bicycle." — run across dozens of models. Repo: https://github.com/simonw/pelican-bicycle · keynote writeup (962-pt HN thread): https://simonwillison.net/2025/Jun/6/six-months-in-llms/ · https://news.ycombinator.com/item?id=44215352

**10. goldiebench (Julian Goldie) — standing one-shot game leaderboard.** Every model gets a fixed prompt, one try, single HTML file; tasks: raycaster maze, fluid sim, neon city flythrough, top-down RPG. Prompt strings not published on-page (methodology on agentos.guide). https://goldiebench.com

**11. Collections (GitHub API-verified):** https://github.com/AnthemK/Prompt-to-Play (AI mini-games + prompts) · https://github.com/xiiyioozzz/opus55-3d-games (three playable 3D web games, one-shot, zero manual code edits) · https://github.com/ofirsharony/vibe-apps (single-file HTML vibe apps) · https://github.com/luksamuk/arcade-games (Snake+Breakout, one conversational session, Kimi; ports JS→C→Rust/WASM) · https://github.com/Yuan-ManX/ai-game-devtools

## Verdict on the "GTA 1 one-shot" wave

The wave is real and datable: Claude 3.7 Sonnet launched 2025-02-24 (HN launch thread, 2,127 points: https://news.ycombinator.com/item?id=43163011) and single-HTML-file game demos (Minecraft, city sims, flight, GTA-style) went viral within hours. **But no canonical original "GTA 1-style" artifact with published prompt text is indexed anywhere I could verify** — the GTA prompt circulates as copy-paste reposts on X/Threads ("steal this prompt") without a stable source. Treat the GTA prompt as folklore in the single-file + checklist + juice anatomy above; cite examples 1–8 for load-bearing verbatim text instead.
