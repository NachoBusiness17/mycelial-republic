# External links digest — lens 2026-09-27

Six links fetched and digested for the lens synthesis. No-fabrication law: every digest
below is from bytes actually fetched this session; each block names the method that worked.
Both X posts were additionally cross-verified against arXiv (independent fetch) because the
operator flagged them as possibly auth-walled.

---

## 1. sizegame — binary-size optimization game

**URL:** https://github.com/MichalStrehovsky/sizegame
**Fetch method that worked:** WebFetch (direct, clean 200).

**Digest (from its own README bytes):**
- A repo by Michal Strehovsky that automatically benchmarks compiled binary sizes of "a set of canonical hello world programs in multiple languages" via GitHub Actions; results published with reproducible CI logs and binaries in releases.
- 18 languages ranked, Assembly (~2 kB) to Haskell (~11,388 kB); latest results "Round 4" run Aug 27 2024 (MSVC 19.40, Rust 1.80.1, Go 1.23.0, GraalVM 22, Nim 2.0.8).
- The rules are the interesting artifact: program "should be compiled ahead of time", must "print Hello World the idiomatic way, using the standard library that comes with the language", "the default compiler settings" only, must "run on a vanilla OS install" with non-OS dynamic libs counted in size.
- Explicitly anti-race-to-the-bottom: the author says without these rules the repo "would just become a race to the bottom" and cites 464-byte Rust / few-kB C# builds as "art projects" that don't reflect real defaults.
- No scoring game or prizes — it is a benchmark with a rules card and an FAQ ("the only valid conclusion is that a canonical Hello World in language X compiles to Y bytes").
- The FAQ also explains WHY defaults are big (console encoding handling, error handling, backtrace support baked into stdlib) — i.e., the bloat has named payers.

**Steal-line:** The steal is not the leaderboard, it is the RULES CARD + CI referee pattern: fix a boring canonical task, forbid hero optimizations ("art projects"), let a robot re-measure every round, publish the deltas — a drop-in shape for any fleet budget (context tokens, wall-clock, binary bytes) where you want honest canonical numbers instead of hand-copied hero claims. It is the byte-backed-census doctrine already enforced in AGENTS.md, expressed as a game.

**Verdict: STEAL**

---

## 2. Drew DeVault — the URL named "Slow" actually serves "Hello world"

**URL:** https://drewdevault.com/blog/Slow/
**Fetch method that worked:** WebFetch + curl verification. NOTE (honesty flag): the operator's
frame called this the "Slow" essay on slow-tools doctrine; the actual bytes at this URL (HTTP
200, no redirect, `<title>Hello world</title>` confirmed by curl) are Drew DeVault's Jan 4 2020
essay **"Hello world"** — the syscall-counting post. There is no "slow-tools doctrine" text at
this URL; if a separate "Slow" essay exists on his blog it is NOT at this link. Digest is of the
bytes that live here.

**Digest (from its own text):**
- Thesis: printing hello world should take two syscalls ("write and exit"), and "a perfect compiler would emit this hello world program for any language" — but most languages do "a whole lot of other crap" the user never asked for.
- Benchmarked ~20 languages on execution time, total/unique syscalls, and binary size: Assembly and Zig nearest ideal (2 syscalls), C+musl static 5, Rust 123, Node.js 673, Ruby 1,401.
- Why the metric: "more syscalls is a decent metric for how much shit is happening that you didn't ask for."
- The cost is framed as real debt: "more complexity that someone has to debug, more time your users are sitting there waiting... less disk space available for files which actually matter."
- Explicitly not a prescription — "not an objective test" but "an approximation" meant to "encourage readers to be more aware of the consequences of their abstractions, and their exponential growth as more layers are added."
- Aside that aged into prophecy for this repo: "it is getting way too goddamn difficult to build static Go binaries."

**Steal-line:** The frame wanted slow-tools-vs-burn-speed and the bytes deliver something better: a cheap, automatable, adversarial metric for unasked-for work (syscalls executed, bytes shipped, tokens burned) that any janitor can count on a canonical task — the fleet equivalent is measuring what a pipeline step does beyond the two things you asked for, which is exactly the census-denominator and fallback-branch-creep disease the build discipline already fights.

**Verdict: STEAL** (with the frame corrected: this is the "Hello world" syscall essay, not a "Slow" essay)

---

## 3. codestudy.net — reducing Go compiled file size

**URL:** https://www.codestudy.net/blog/how-to-reduce-go-compiled-file-size/
**Fetch method that worked:** WebFetch (direct, clean 200).

**Digest (from its own text):**
- `-ldflags "-s -w"` (strip symbol table + DWARF): 1.2 MB → 612 KB.
- UPX pack (`upx --best`): 612 KB → 208 KB, at the cost of startup overhead.
- Avoid heavy stdlib: swap `fmt.Println` for `os.Stdout.WriteString`, drop `encoding/json` / `net/http` / `reflect` where possible: 612 KB → 544 KB.
- `CGO_ENABLED=0` to avoid linking C dependencies.
- `-trimpath` + `-gcflags "-l -B"` for ~5-10% more.
- TinyGo as the endgame: ~1.2 MB → 19 KB with a stripped runtime, at the price of stdlib compatibility.
- Trade-offs named honestly (harder debugging, slower UPX startup) and scope honesty: binary size "mainly matters for embedded systems, CLI tools, and low-bandwidth environments."

**Steal-line:** Concrete ladder with measured rungs for shipping small ractor tooling/CLIs off the harness (the -s -w → UPX → stdlib-swap → CGO-off → TinyGo ordering is a decision table, not a tutorial); pairs with link 1's rules card as the "how" under the "what".

**Verdict: STEAL**

---

## 4. X post — @bonniesjli "Contrastive World Models"

**URL:** https://x.com/bonniesjli/status/2103590425315754287
**Fetch method that worked:** WebFetch (direct). Cross-check: raw curl to x.com returns only a
154 KB JS app shell with no post text (HTTP 200 but no og:description/title rendered), so the
WebFetch rendering path was the fetch. VERIFIED independently: the cited paper exists on arXiv
(fetched this session).

**Digest (from the fetched post + verified arXiv bytes):**
- Bonnie Li (@bonniesjli), Sep 25 2026, announces "Contrastive World Models": "can we build world models purely in the latent space, without pixel prediction?"
- Approach: train latent states to maximize mutual information with future observations — no decoder, no pixel reconstruction; pixel reconstruction swapped for a Deep InfoMax objective.
- Claimed: "substantially more robust representations", cheaper training by dropping the pixel decoder, minimal assumptions / general approach.
- A follow-up links arXiv 2609.22175 and notes it was done independently with minimal compute; a commenter notes the "we" is a single author.
- VERIFIED (this session, arxiv.org/abs/2609.22175): "Contrastive World Models", Bonnie Li, cs.LG, submitted Aug 27 2026 — abstract matches the post (latent dynamics without pixel reconstruction, Deep InfoMax-style MI objective, robustness to visual distractors in model-based RL).
- Engagement per fetch: ~149.4K views, 1.5K likes, 1.4K reposts.

**Steal-line:** For ractor/world-model lanes: representation quality does not require paying the pixel-reconstruction tax — a mutual-information objective between latent state and future observation is a cheaper, more robust target; a directly stealable training-loss idea for any internal-state model the fleet trains (and it won on "minimal compute", i.e., this is a janitor-tier result, not a specialist-tier one).

**Verdict: STEAL**

---

## 5. Tencent-Hunyuan/AuK — voice generation

**URL:** https://github.com/Tencent-Hunyuan/AuK
**Fetch method that worked:** WebFetch (direct, clean 200).

**Digest (from its own README bytes):**
- AuK is a "1.5B foundation model for speech generation and editing" from Tencent, trained on "millions of hours of diverse audio data", driven through "a unified natural-language instruction interface".
- Generation: zero-shot TTS, instruction-based TTS ("Generate speech from a voice description alone — no reference audio").
- Editing suite: content/lyric editing, pitch/speed/volume, emotion and timbre change, de-accenting, adding/removing nonverbal sounds (breaths, laughs), whisper conversion.
- Enhancement: denoise, dereverb, speech/music separation, target-speaker extraction.
- Two checkpoints: AuK base (quality, configurable NFE/CFG) and AuK-Flash ("fast 4-step inference"); diffusion transformer + Qwen2.5-Omni-3B encoder + VAE; a Prompt Enhancer maps free-form asks to runnable commands; Gradio demo, ComfyUI node, fine-tuning pipeline.
- Runs local: checkpoints on HF/ModelScope, Python 3.10, CPU offload cuts VRAM ~8 GiB (~32%) for consumer GPUs, MLX on Apple Silicon; day-0 SGLang-Omni / vLLM-Omni serving, audio.cpp GGUF. MIT license, 1.3k stars.

**Steal-line:** This is the operator-named ractor/NPC voice piece: MIT-licensed, 1.5B (fits the local-first tier ladder), instruction-driven so the Mountain's NPC gateway can steer voice purely through natural-language persona commands (no reference-audio dependency), with a distilled fast path (AuK-Flash, 4-step) suitable for interactive ractor speech and a fine-tuning pipeline for per-ractor persona voices.

**Verdict: STEAL**

---

## 6. X post — @dccsillag "Functional Gradient Descent with Adaptive Representations"

**URL:** https://x.com/dccsillag/status/2103932688956579938
**Fetch method that worked:** WebFetch (direct). Raw curl to x.com returns the same JS app
shell as link 4 (no server-rendered text), so WebFetch's rendering path was the fetch.
VERIFIED independently via the arXiv API (this session, curl to export.arxiv.org).

**Digest (from the fetched post + verified arXiv bytes):**
- Daniel Csillag (@dccsillag), Sep 26 2026, announces: "Now accepted at NeurIPS: Functional Gradient Descent with Adaptive Representations"; his framing: "Functional GD algorithms generally outperform neural nets, but are hard to accurately implement. We fix this!"
- Follow-up: functional gradients are infinite-dimensional and "must be approximated in practice"; naive approximation converges to the wrong place, motivating their formalization of "adaptive" approximation schemes.
- VERIFIED via arXiv API: arXiv 2606.16926, exact title "Functional Gradient Descent with Adaptive Representations", authors Daniel Csillag, Rodrigo Schuller, Pedro Dall'Antonia, Leonidas Guibas, Luiz Velho, Tiago Novello — paper is real and matches the post's title/claim.
- Honesty note: the WebFetch rendering of co-author names ("Rafael Llorca-Schüler, Pedro Castellanos") does NOT match the arXiv API author list (Schuller, Dall'Antonia) — the API bytes are authoritative; the small-model name rendering of the follow-up is suspect and excluded.
- Engagement per fetch: 27.5K views, ~493 likes.

**Steal-line:** On the operator's "looks like our light maze concept" — the resonance is real at the method level, not the object level: the paper's core move is that you cannot represent the true (infinite-dimensional) object, so you let the representation itself adapt under the approximation scheme instead of fixing it and accepting drift — a direct formal cousin of the fleet's retrocausal-steering / adaptive-approximation thinking (approximate, but make the approximation scheme self-correcting rather than naive). WATCH for the lens synthesis rather than immediate STEAL: it is a math-methods paper, not an architecture to copy.

**Verdict: WATCH**

---

## Fetch-method summary

| # | Link | Method | Status |
|---|------|--------|--------|
| 1 | github.com/MichalStrehovsky/sizegame | WebFetch direct | fetched |
| 2 | drewdevault.com/blog/Slow/ | WebFetch + curl title check | fetched — serves "Hello world" essay, not a "Slow" essay |
| 3 | codestudy.net Go binary size | WebFetch direct | fetched |
| 4 | x.com/bonniesjli/…5754287 | WebFetch rendering; curl = JS shell | fetched + arXiv-verified (2609.22175) |
| 5 | github.com/Tencent-Hunyuan/AuK | WebFetch direct | fetched |
| 6 | x.com/dccsillag/…6579938 | WebFetch rendering; curl = JS shell | fetched + arXiv-verified (2606.16926) |

No OWED items: all six fetched. Cross-verification receipts: /tmp/xpost1.html (app shell, no
post text in bytes — basis for trusting the WebFetch rendering path), arxiv.org/abs/2609.22175,
export.arxiv.org API query for 2606.16926.

## Addendum 2026-09-27 (operator drops, post-lens)

### 7. @askalphaxiv — "A Smaller Transformer in Your Transformer" — operator: "turtles all the way down"
- Fetched via fxtwitter syndication (raw curl returns JS shell); paper cross-verified: arXiv 2609.20100, title exact.
- IS: ViTs contain neighboring layer groups with similar outputs (small updates inside one computational phase); the paper distills each group into a SINGLE layer mapping phase-start -> phase-end. DINOv2: compute ~halved, tiny accuracy drop.
- Resonance: this is the estate's compression mechanism at the model layer — find adjacent redundant phases, replace with one direct mapping. Same shape as verkle99 compaction (fold 463 leaves -> counter leaves with proof), the eigen-map (regions -> centroids), tier packs (frontier distilled once, rendered free), SEED-RIB (the whole fleet -> kilobytes). Turtles: a smaller transformer inside your transformer is also tier packs inside the account.
- STEAL — the phase-group test itself: measure neighboring-lane/organ outputs for similarity; collapse the redundant phase. Cheapest first application: the hourly burn cron's near-identical waves.

### 8. @Math_files — Edward Nelson's card shuffle — operator: "hahah this is our mechanism"
- Fetched via fxtwitter; the Nelson-at-12 story is the account's own bio content (verified in its profile bytes).
- IS: repeated top-bottom deck rearrangement; the question "after how many repetitions does the deck return to its original order?" -> generalized, plotted, formula at 14, proof at 15. Math: order of a permutation = LCM of cycle lengths.
- Resonance: the estate runs on return-to-original-order cycles — quota reset day, the queue drain cycle, the verkle knot cadence, pile-classify rounds — and "when do ALL the cycles line up again" is literally an LCM-of-cycle-lengths question (the reset-day fullsend planner). Also the founding arc in miniature: serious machinery from a simple question and a deck of cards (riddles -> the listener).
- STEAL — compute the estate's permutation order once: cycle length per repeating organ (quota, patrols, knots), LCM = the natural full-reset period; schedule the big flushes on it.
