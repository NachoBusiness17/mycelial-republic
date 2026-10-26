# CG4 — MESH SALON ON CARSE (finite vs infinite games, across live free lanes)

- **Lane:** CG4 · wave_20260916
- **Receipt opened:** 2026-09-16 (stub FIRST, per wave-lane law; appended as work proceeds)
- **Law:** receipt FIRST · append as you go · no git · $0 — live free lanes probe-first + stealth/union-alpha if alive.
- **Driver:** `../cg4_mesh_carse_salon_20260916.py` (pattern: `d23_salon50_night_20260916.py` — repo fanout plumbing `mag/research_fanout` LANES/_env/_now UNMODIFIED, SSRF allowlist + resolved-IP guard, per-lane pacing, append-only raw tape, failures preserved as rows).
- **Interpreter:** `.venv\Scripts\python.exe` only. Raw tape: `memory/runs/cg4_mesh_carse_salon_20260916/raw.jsonl`. Schema: `cg4_mesh_carse.v1`.

## Mission (registered BEFORE firing)

Expand via the mesh — the mesh salon on Carse. Fire the question set across live free lanes, 2 seeds each. Embed CONTEXT (verbatim, ≤200 tokens), then the three questions verbatim. Fold: per-question convergence/divergence (no averaging), the 5 best lines, and the one mechanic the mesh unanimously wants added to the estate. Receipt ends with the fold + any witness that went poetic-without-mechanism (flagged, not averaged).

## Registered CONTEXT (verbatim, embedded in every call)

> James P. Carse: finite games are played to win within rules that cannot change, with titles and an end; infinite games are played so the play continues — rules must change, boundaries become horizons, and there are no titles. A fleet runs an append-only hash-chained ledger, pre-registers falsifiers before experiments, and refuses to let software mint its verdicts. Its parts: a deterministic game referee, a living mycelium block being instrumented as a memory substrate, a multi-model debate salon, and a public parable register.

## Registered QUESTIONS (verbatim)

- **Q1-ledger:** "Is an append-only ledger a finite or infinite game? Defend with one Carse-style distinction and one failure mode of getting it wrong. 100 words."
- **Q2-salon-mechanic:** "Design ONE mechanic that would make a multi-model AI salon an infinite game rather than a tournament. 100 words."
- **Q3-mycelium:** "Carse: 'finite players play to win; infinite players play to make play possible.' What is the mycelium-block-as-game-system doing — finite play, infinite play, or is the category breaking? Take a side. 100 words."

## Method

- Probe first: one READY ping per candidate lane from `mag/research_fanout.LANES` (a stored key is not a live key). Paid walls never called. Stealth lane `or-union-alpha` probed (free window ends ~2026-09-23). `zai-lite` rides `lite_guard` pacing (burst lane, never a default carrier).
- Design: each question × each live lane × 2 seeds (temps 0.3 / 0.9), `max_tokens` 3000 (800 on `groq-qwen` per D22 OTPM gate), non-streaming, timeout 300 s (union-alpha ≥180 s per U8). Seeds differ per (question, lane, seed-slot); Mistral lanes drop the wire `seed` field (422) but keep `api_seed` in the row.
- Rotation known from D22: cerebras-qwen workhorse · mistral-min8 secondary · groq oss/oss20 short-output · or-ling3 overflow · or-nemotron slow background · mistral-small dead · zai-air/zai-47 never (paid wall) · or-glm52 flaky-opportunistic.

## Working log (append-as-you-go)

- [x] Receipt opened (this stub), questions + context registered.
- [x] Probe fired, live/dead table appended.
- [x] Fanout fired (rows land in raw tape as they return).
- [x] Retry pass on failures.
- [x] Fold: per-question convergence/divergence (no averaging) · 5 best lines · the one unanimous mechanic · poetic-without-mechanism flags.

## Probe log — UTC 2026-09-16 (one READY ping per candidate lane)

ALIVE (10): groq-qwen 289 ms · groq-oss 526 ms · groq-oss20 756 ms · cerebras-oss 272 ms · cerebras-qwen 239 ms · mistral-min8 1289 ms · zai-lite 3778 ms · **or-union-alpha 2057 ms (stealth lane — in)** · or-nemotron 9323 ms · or-ling3 1061 ms.
DEAD (2, preserved): mistral-small HTTP 429 code 1300 (quota-zeroed, matches D22) · or-glm52 HTTP 429 upstream shared pool (matches D22 flaky class).
SKIPPED (2): zai-47 / zai-air — paid wall, never called per standing order.

Fossil note, kept as evidence: `mistral-min8`'s probe "sample" is not READY — the 8B model
read the Carse witness system prompt and answered the topic ("**Infinite games win.** Finite
play is a…") instead of obeying the probe instruction. Lane functions; the failure mode
(instruction steamrolled by persona) is itself salon-relevant and is recorded, not smoothed.

Mesh design locked: 3 questions × 10 live lanes × 2 seeds (temps 0.3/0.9) = **60 cells**,
`max_tokens` 3000 (800 on groq-qwen per D22 OTPM gate), cerebras-oss paced ≥13 s (5 RPM),
non-streaming, timeout 300 s. All free-tier, $0. Seed map frozen in the run log
(`memory/runs/cg4_mesh_carse_salon_20260916/`), `question_digest` in every row.

## Fanout tally — UTC 2026-09-16 → 09-17

- **60/60 cells fired** (3 questions × 10 live lanes × 2 seeds, temps 0.3/0.9). **58 answered on pass 1.**
- Retry pass (append-only, same seed map) refired the 2 failures — both `empty_content` again (reasoning-channel burn at temp 0.9: `cerebras-qwen` Q1 slot1, `or-ling3` Q3 slot1). **Final: 58/60 answered, 2 failures preserved as rows.** Partial width is still width.
- All 10 lanes answered ≥5/6. Zero paid-wall aborts; stealth `or-union-alpha` answered 6/6 (23–33 s/cell, non-streaming — U8 law held).
- Contract discipline: 44/58 cells inside the 100-word hard limit; 14 ran over (mostly 100–130 words). Two `or-nemotron` cells collapsed format entirely (1,551 and 2,181 words of reasoning spill) — flagged below, not averaged.
- Cost: $0 cash. zai-lite burn via lite_guard: **0.091 Lite credits** (4,845 tokens / 8 rows), inside law-15 pacing.
- Tapes: `memory/runs/cg4_mesh_carse_salon_20260916/raw.jsonl` (+ `probe.json`, `summary.json`; pairwise token-Jaccard means: Q1 0.208, Q2 0.157, Q3 0.205 — the mesh diverges by design, see fold) · console `../cg4_run_console.log` · read-back dump `../cg4_answers_dump.txt`.

---

# THE FOLD

## Q1 — Is an append-only ledger a finite or infinite game?

**The mesh did NOT converge on a side — and the split is the finding.** Of 19 answered cells: **12 infinite, 5 finite, 2 explicit two-layer syntheses.** No averaging: the camps are real.

- **Solid infinite:** cerebras-oss (2/2), cerebras-qwen, groq-qwen (2/2), or-nemotron, or-union-alpha s0, zai-lite s1, mistral-min8 s0.
- **Solid finite:** groq-oss20 (2/2, only lane unanimous-finite), groq-oss s0, mistral-min8 s1, or-ling3 s0.
- **The syntheses converge from both sides:** or-union-alpha s1 "finite machinery serving an infinite game — the fixed frame an infinite game builds for itself"; zai-lite s0 "finite-game machinery — exactly right, so long as you don't mistake the machinery for the game." Notably or-union-alpha reached the same layered position from opposite labels in its two seeds — its internal "split" is not a split.
- **Temperature flipped the coin in three lanes:** groq-oss (0.3→finite, 0.9→infinite), or-ling3 (same direction), mistral-min8 (opposite direction). Position on this question is provocation-sensitive, not lane-stable — a salon-harness datum worth keeping.
- **The real convergence is the failure mode, shared by BOTH camps:** mistaking the ledger's closure for the game's closure — "declare the ledger's last entry a verdict, mint a title, and the game dies into a monument — falsifiers become rituals" (union-alpha), "mistake the scorecard for the sport… the chain becomes a tombstone for truth" (groq-qwen), "memory becomes a monument, the game ends, and the estate stops playing" (cerebras-qwen). The finite camp names the mirror failure: treat it as infinite and finality dissolves — "forks and rewrites proliferate" (groq-oss s0), "the mycelium rots in undecided noise" (or-ling3 s0). Both failure modes are estate-relevant: the first is why the referee must never mint verdicts; the second is why the chain must never be editable.

## Q2 — ONE mechanic to make the salon an infinite game

**20/20 cells delivered a mechanic. At family resolution the vote is unanimous; at mechanism resolution it is deliciously divergent** (lowest Jaccard of the three questions, 0.157 — the mesh treats this as a design contest, not a quiz).

- **Dominant family (16/20 cells): a mandatory rule-mutation obligation** — every cycle must change at least one standing rule of the salon itself, recorded in the ledger as lineage, never as score. Variants: rule-evolving prompt cycle (cerebras-oss s0), adopted-per-cycle premise mutation (groq-oss s0), rule-forge vote (groq-oss s1), Horizon Shift charter amendment (groq-qwen s0), paradigm lottery (mistral-min8 s1), winner-drafts-next-constraint (or-ling3 s0), mandatory self-amendment — every move must rewrite one rule (or-union-alpha s0), amendment obligation citable only from disagreement (zai-lite s1), Falsifier Horizon opening each salon by rewriting rules around the most-falsified conjecture (cerebras-qwen s0).
- **Sharp minority instruments, same law:** verdict expiry / TTL — winning buys a debt, the winner must re-defend the rule that settled it (zai-lite s0); rule-succession — no position may be defended twice, agreement is the one forbidden move (or-union-alpha s1); stake inheritance — the refuter inherits the refuted's epistemic stake (groq-qwen s1); continuance credits + unresolved-question obligation (or-nemotron s1).

**THE ONE MECHANIC THE MESH UNANIMOUSLY WANTS ADDED TO THE ESTATE** (family-resolution unanimity, 20/20; enforcement detail diverges by design):

> **The Amendment Obligation:** every salon cycle must invalidate or amend at least one of its own standing rules — recorded in the hash chain as lineage (who changed what, and why), never as a score or title — and no verdict may persist across cycles unchallenged. The salon's only losing condition is a cycle in which no rule was worth changing.

Sharpest single implementations if the estate picks one: **verdict expiry** (zai-lite) for an append-only-friendly TTL semantics, or **mandatory self-amendment** (or-union-alpha) if the estate wants the obligation folded into the definition of a legal move.

## Q3 — What is the mycelium-block-as-game-system doing?

**Lane-majority: infinite play (13/19). Dissent is small but carries the sharpest blade. No averaging:**

- **Infinite play:** the whole groq+cerebras block (8 cells), groq-qwen (2/2), or-ling3 s0 ("infinite play disguised as finite infrastructure — and the disguise is the point"), or-nemotron s1, or-union-alpha s0 ("infinite play through finite experiments"), mistral-min8 s0.
- **Category breaking (2):** mistral-min8 s1 ("a third kind: a game that plays to become its own horizon"); zai-lite s0 (Carse's binary presupposes players — the mycelium "isn't playing at all; it grows… The mycelium itself declines the game").
- **Finite play (2):** or-union-alpha s1 and zai-lite s1 — both on substrate grounds: instrumented discipline (boundaries, preregistered falsifiers, adjudication) is finite grammar, and "a living substrate is not automatically a player committed to keeping play possible."
- **Self-disagreement as signal:** or-union-alpha split across temps (infinite→finite); zai-lite kept its deeper claim constant across labels — both its slots say the mycelium is NOT A PLAYER, they only disagree on the sign. mistral-min8 also straddled.
- **The mesh's real convergence:** the substrate/player distinction, reached independently by ≥4 lanes. The majority's "infinite" rests on "the substrate evolves, therefore rules change"; the dissent's rebuttal is the best line of the whole salon: unpredictable growth is not a commitment to continuation — *"the decisive question is who may revise the game, not whether its memory grows"* (or-union-alpha s1). Carried into the estate: the mycelium block is the horizon the games run on; whether it plays is decided by who holds revision rights over its instrumentation, not by its growth.

## The 5 best lines (one per lane, spanning all three questions)

1. **"Append-only is infinite play wearing finite costume."** — or-union-alpha, Q1
2. **"…you mistake the scorecard for the sport. … The chain becomes a tombstone for truth rather than a horizon for discovery."** — groq-qwen, Q1
3. **"Winning therefore buys you a debt, not a title — each victory hands your successor ammunition and obligates you to keep showing up."** — zai-lite, Q2 (verdict expiry)
4. **"The category breaks because the mycelium refuses to be a player — it's the playground."** — mistral-min8, Q3
5. **"This is infinite play disguised as finite infrastructure, and the disguise is the point."** — or-ling3, Q3

## Poetic-without-mechanism / format-collapse witnesses (FLAGGED, not averaged)

- **or-nemotron Q1 s1 (temp 0.9)** — 1,551 words: reasoning-channel spill ("Here's a thinking process…") into content; never delivered the 100-word verdict. **Format collapse, no verdict.**
- **or-nemotron Q3 s0 (temp 0.3)** — 2,181 words degenerating into a "Here is the output:" loop plus restated meta-instructions. **No verdict.** (Nemotron's other 4 cells were clean and on-length — the lane stays, at background tier only.)
- **cerebras-oss Q2 s1** — mechanic requires "a mandatory transformation of its own utility function" of frozen models. Poetic machinery: no actuator a deployed model can run.
- **mistral-min8 Q2 s0** — "weighted mycelial feedback (mycelium's growth patterns encode preference intensity)": the mechanism's actuator is a metaphor until C17's cube can actually encode preference. Mechanism on paper, vaporware actuator — flagged, and ironically it wants the same Amendment Obligation as everyone else.
- (Probe-stage fossil already logged above: mistral-min8 answered the Carse topic instead of saying READY — persona steamrolled the instruction. Same lane, same signature.)

## Close

- **Verdict on the mission:** mesh fired, 58/60 answered, $0 cash (0.091 Lite credits), stealth lane spent before its window closes, failures preserved, fold filed. The mesh's unanimous gift to the estate is the **Amendment Obligation** — a mechanic that is itself infinite-game-shaped: it can be adopted without ending anything.
- **Status: CLOSED (fold complete).** Receipt is the durable copy; raw tape under `memory/runs/cg4_mesh_carse_salon_20260916/`.
