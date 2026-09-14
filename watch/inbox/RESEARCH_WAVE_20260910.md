# RESEARCH WAVE — 12 X POSTS + TAVERNBRAWL (2026-09-10)

Filed by: zcode seat. All 12 posts fetched directly (no login walls). Wave context: the
Sep-9 feed is dominated by a "fruit-fly connectome" meme wave (posts 2, 7, 10) and by
Astra (GPT-6) demos. Post 12 quotes the exact repo the operator tagged TAVERNBRAWL.
Tri-state convention: S = Supported (receipt attached), D = Disputed, U = Unproven.

---

## 1. @thermalpastor — Astra robot juggling
- WHAT: GPT-6 Astra orchestrating two robots juggling one ball, real MuJoCo physics sim at 1x speed; follow-up teases 4 robots / 7 balls / 35 catches with crossing paths.
- WHO: H (@thermalpastor), robotics-demo account; 41K views. Dmytro Hrybov reply: 1x-speed control is the impressive part.
- RELEVANCE: S for robot/swarm organs — multi-agent physical coordination under real-time physics is exactly the swarm-orchestration shape; watch the 4-robot follow-up.

## 2. @nrol_ling — fruit-fly brain damage speech model
- WHAT: OrukLabs copied 499 fruit-fly neuron connections into a speech model, froze the wiring, trained a small output head to label emotion; lesioning one neuron flips angry→neutral classification. "We didn't give a real fly brain damage" (it's the mapped connectome, simulated).
- WHO: Nathan Roll (@nrol_ling) + @OrukLabs (emotion/intent AI speech models). 14.2K views.
- RELEVANCE: S as an organ pattern — tiny fixed-architecture model + trained readout head = cheap, inspectable classifier; direct adjacency to memlance/percolator fixed-lens probes and the eye's emotion/sentiment organs.

## 3. @connorkapoor — Ace-Mini-1 casting surrogate
- WHAT: Digital Metal's Ace-Mini-1, tiny model fine-tuned on metal-casting simulations (filling, solidification, deformation); 65-minute solve → 0.26s (~8042x), avg error <5%. Open weights on HF (DigitalMetal/ace-mini-1); trained on ~50 geometries, 17-4PH steel only.
- WHO: Connor Kapoor / Digital Metal (@digitalmetalinc).
- RELEVANCE: S as the distill-surrogate thesis proven again in industry — same shape as MAX_DISTILL: expensive slow oracle → tiny surrogate, bounded domain, stated error. Steal the "50-geometry, one-material" scoping discipline.

## 4. @robotsdigest — Q-Chunking (RL acts in chunks)
- WHAT: RL agent picks action *chunks* [a_t..a_t+k] instead of one action per step; offline data → behavior-cloning flow policy → Q-function selects best chunks; n-step TD across the chunk. "Change the timescale RL reasons at." Paper arxiv 2507.07969, code github.com/ColinQiyangLi/qc.
- WHO: Robots Digest aggregating the paper (Li et al.); @thermalpastor in replies.
- RELEVANCE: S twice — (a) long-horizon swarm task planning, (b) tavern-brawl bot controllers: frame-chunk policies are exactly how Melee AI should think (60fps single-step RL never learns wavedashes).

## 5. @SocraticScribe — Neumann-boundary wave ring
- WHAT: Wave sim where a circular ring of obstacles acts as perfect non-inverting mirrors; pulses + reflections overlap into interference/echo patterns. Follow-up links YouTube "Waves escaping a ring of obstacles with Neumann boundary conditions."
- WHO: @SocraticScribe ("Bluntly Put Philosopher"). Tiny engagement (485 views).
- RELEVANCE: S for shadow fields — same lineage as the Shadertoy steal: a cheap 1D/2D wave solver with reflective boundaries is a ready salon shadow_fields candidate and arena visual for game organs.

## 6. @marco_fugaro — Astra protein viz app on Spline V2
- WHAT: "I asked Astra to build me a protein visualization app using Spline V2" — pulls live data from the Protein Data Bank, two visualization modes. Video demo.
- WHO: Marco Fugaro; ~6.2K views; replies asking for the code.
- RELEVANCE: U on quality (demo only, no code shared) — relevance is X-desk-shaped: this is the "asked Astra to build X" meme format the reply desk can ride; weak for swarm.

## 7. @alright_mark — the fly is learning to drive
- WHAT: "the fly is learning to drive" — connectome-based fruit fly learning to operate a car in sim; progress posts ("learned to steer", "using the pedals"); open code (github flyhard) + joke sponsorship site thedrivingfly.com ("ad space from $1").
- WHO: Breg Grockman (@alright_mark). ~1.4K views, part of the fly wave.
- RELEVANCE: S for game organs (RL agent in a game environment = our bot-organ shape) and X-desk bait (the sponsorship joke is a repeatable format for fleet demos).

## 8. @reprompting — squeezed attention
- WHAT: "reading about squeezed attention today" + arxiv 2411.09688 (Squeezed Attention: KV-cache compression for long-context LLMs).
- WHO: light (@reprompting); ~1K views, low engagement.
- RELEVANCE: S for local inference — KV compression directly helps the ollama eye and long-context fleet lanes on modest hardware; file under inference-efficiency notes.

## 9. @CosmosNetwork — spring-loaded wedge lock
- WHAT: Four-part spring-loaded wedge lock, no screws — push a pin into the pocket, brass wedges bite; pull side tabs to release. "The mechanism behind battery packs, SIM trays, quick-clamps."
- WHO: The Cosmos Network (mechanism-video account). 613 views.
- RELEVANCE: UNRELATED to current arcs — hardware joinery. Park it; only wakes if Rocinante ever gets a physical build phase. No action.

## 10. @sainimatic — fruit fly heaven (vs. the cruelty wave)
- WHAT: Quoted post from @evnsnclr (Sep 4) ran the FULL MaleCNS v1.0 connectome (166,700 neurons) inside Minecraft with GPT-6 Astra help, neural activity driving movement. Macroblock jokes everyone tortures the fly (black-mirror mazes, endless Beat Saber) and is building "fruit fly heaven" — free flight forever. ~1M views, 16K likes.
- WHO: Macroblock (@sainimatic) + evnsnclr. The fly wave's biggest post.
- RELEVANCE: S for game organs — connectome-as-NPC-controller inside a game world is a live, viral proof of the organ pattern; also the reply-desk's best hook this week (1M-view thread).

## 11. @lanyon_ai — formally verified PDE-algorithm discovery
- WHAT: Lanyon autonomously discovers discontinuous Galerkin discretization algorithms; verifies via formal Lean proofs (reconstruction, surface/volume terms, entropy stability); compiles winners to optimized C. Claims: p=1/p=2 results, ~30K lines C + 40K lines Lean "in minutes, <$1 inference." Repos: lanyonai/AdvectionDiffusion, BurgersEquation.
- WHO: Lanyon AI; research notes by @minmodammar. DISPUTED in the open: @jasisz1 argues Lean proofs re-typeset the same expressions rather than checking generated Racket, cites GitHub issue #7 (2D DG modal ordering mismatch / incorrect volume terms).
- RELEVANCE: S for the verification doctrine — this is our cite-gate/tri-state debate at research scale: generated artifact + claimed proof ≠ verified artifact; issue #7 is a free case study. Also a free-lane discovery-loop template (search → prove → compile → run).

## 12. @_KevinTang — Melee in mixed reality
- WHAT: "Super Smash Bros Melee in MR! Messing around with this using Astra. Fox and Marth going at it on my table." Quotes banteg (Sep 7): Melee fully decompiled after 6+ years, sped up by LLMs and "finished off with astra," 3.88MB of compiled code, links github.com/doldecomp/melee. Replies joke "It's Brawl, not Melee."
- WHO: Kevin Tang; banteg quoted. 4.8K views.
- RELEVANCE: S and load-bearing — this is the thread that surfaced TAVERNBRAWL: the decomp milestone went mainstream-viral the same week the operator tagged the repo. Direct feed to target 13 and future announcement bait.

---

## 13. doldecomp/melee — THE TAVERNBRAWL SECTION

**What it is.** A *matching decompilation* of Super Smash Bros. Melee: the community
(doldecomp org, "a bunch of clever folks") rewrote the game's entire PowerPC binary in C
so it recompiles to the original `main.dol` — GameCube version 1.02, Game ID GALE01.
~2,000 stars, 271 forks, 3,780 commits, commits landed the day of this research
(melee is the org's flagship; 19 repos total, incl. a Brawl decomp, Super Mario
Sunshine, Wii Sports, Mario Kart Wii).

**Completion state.** decomp.dev shows Melee at **100.00% decompiled / 100.00% fully
linked** — every function rewritten and byte-perfect on rebuild. Timeline per banteg:
6+ years of work, LLM-accelerated in the endgame, finished off with Astra; 3.88MB of
compiled code. The org's brawl repo is still WIP by contrast. This is done work, not a
moving target.

**How decomp→recomp works (technical).** "Matching" means: source written from scratch
must compile byte-identical to the shipped binary, using the *original* compiler
(CodeWarrior, run under Wine on non-x86 hosts), the decompiled Dolphin SDK
(dolsdk2001/2004), and diff tooling (objdiff, m2c, decomp.me). No assets are in the
repo — you must extract system data from your own retail ISO via Dolphin. The built DOL
is "shiftable" (code can be added/removed, which is the modding door). README is blunt:
the output "isn't portable to PCs" — it is a GameCube binary, full stop.

**Legal posture.** Gray-zone but long-tolerated: authored-from-scratch C that is still a
derivative of Nintendo's copyrighted code, framed "entirely for research and archival
purposes." Nintendo has left matching decomp projects alone while striking emulators
(yuzu, Ryujinx settlements) — tolerance so far is S, tolerance forever is U. The fleet
rule if we ever touch this: read/learn from it, never redistribute builds or ship its
code inside anything.

**Platforms.** The game runs on real GameCube hardware and on Dolphin — which is where
**Slippi** lives: Project Slippi (Fizzi) = Ishiiruka (an old performance-focused Dolphin
fork) + in-game gecko mods + rollback netplay + .SLP replays + stats; now migrating to a
mainline-Dolphin beta. Slippi/Ishiiruka are **reference-only** for us: they run Nintendo's
game; nothing in them is ours to copy into a new title.

**What an original brawl-style game takes.** The Melee approach inverts cleanly:
- MECHANICS ARE NOT COPYRIGHTABLE. Frame data, hitbox/hurtbox systems, knockback
  formulas, DI, L-cancel, shieldstun, wavedash physics (air-dodge slide), 60fps fixed
  tick, ECB terrain collision — all of it is documented publicly by the community and
  can go into a clean-room *mechanics spec*. What IS protected: characters, names, art,
  music, stages as creative expression. A tavern brawler with original characters and
  melee-feel movement is legally clean.
- Precedents exist: NyxTheShield/Godot-Smash-Engine, L4igi/PlatformFighterGodot,
  Physis21/fisticuffs (implements Melee-style ECB + shield), Castagne engine (MPL-2.0,
  traditional-fighter oriented). None shipped a finished Melee-feel game — the feel is
  the hard part, not the engine.
- The decomp's real gift to us is *readable ground truth*: the actual knockback and
  friction constants, in C. A mechanics spec written from it (reference-only, no code
  copied) beats guessing from frame-data wikis.

**Fleet fit.** Our game organs are browser/HTML arenas under the L0 six-function game
contract (maze_arena, water arena). TAVERNBRAWL v0 = 2 players, one tavern stage,
percent + knock-off-the-map, one attack per direction, DI, fixed 60fps tick — native to
the organ shape we already run.

### VERDICT
**Split-scale, and the split is the answer.** TAVERNBRAWL is a **weekend-scale
prototype** as a fleet game organ (v0 above is maze_arena-class; the L0 contract plus a
knockback-state machine is one wave of work) — but it is **season-scale if the bar is
"feels like Melee"** (frame-perfect movement, ECB, shield/L-cancel physics, roster
balance, rollback netplay — that's the part that took the Melee community six years,
and rollback is its own season). Recommended line: file the clean-room mechanics spec
card now, fire the weekend v0 on the L0 contract, defer netplay and Melee-feel tuning to
a season card. The decomp is our constant table, never our codebase.

---

## ROUTE TABLE

| # | Target | Arc it feeds | Next action |
|---|--------|--------------|-------------|
| 1 | thermalpastor (Astra juggling) | robot/swarm organs | Watch 4-robot/7-ball follow-up; note MuJoCo real-time control pattern |
| 2 | nrol_ling (fly lesion) | organs / memlance adjacency | Fixed-wiring + readout-head probe idea to percolator notes |
| 3 | connorkapoor (Ace-Mini-1) | MAX_DISTILL / free lanes | Check HF weights; steal the 50-geometry scoping discipline |
| 4 | robotsdigest (Q-Chunking) | swarm planning + tavern-brawl bots | Paper+code into research queue; frame-chunk policy for brawl AI |
| 5 | SocraticScribe (Neumann ring) | shadow fields | Steal wave-ring sim as salon shadow_fields candidate |
| 6 | marco_fugaro (protein app) | X reply desk | Meme-format note only; no build action |
| 7 | alright_mark (fly drives) | game organs + X desk | Sweep flyhard repo; sponsorship-joke format to reply desk |
| 8 | reprompting (squeezed attention) | local inference | File arxiv 2411.09688 under eye/lane KV-compression notes |
| 9 | CosmosNetwork (wedge lock) | none / hardware | Park; wakes only on a physical Rocinante build |
| 10 | sainimatic (fly heaven) | game organs + X desk | 1M-view thread: connectome-NPC proof + best reply hook this week |
| 11 | lanyon_ai (verified discovery) | verification doctrine | Study issue #7 proof-vs-code gap; cite-gate case study; free-lane loop template |
| 12 | _KevinTang (Melee MR) | TAVERNBRAWL + X desk | Viral hook; keep for tavern-brawl announcement quote-bait |
| 13 | doldecomp/melee | TAVERNBRAWL | File clean-room mechanics spec card; weekend v0 on L0 contract, GO-gated on operator; netplay deferred |

— wave closed; all 13 targets covered, none skipped.

## ADDENDUM — Desert Ant Labs (desertant.com, operator drop)
On-device little-brains model shop (17 models, source-available license, free <100k devices). Verified public on HF: Clear (denoise, Windows ok), Redact (PII strip, Windows ok, 899 dl), Gist/Tongue/Title. VERDICT: Voz (300x STT) is Apple/CoreML only — ear stays whisper tonight; adopt Clear as audio preproc + Redact as transcript hygiene in space_ear v0.1; watch Voz for Windows ship. Doctrine receipt: "little brains in every product" = our vessels thesis, productized by strangers.
