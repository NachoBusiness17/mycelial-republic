---
name: union-fullsend-day-20260917
description: 2026-09-17 operator orders — union-alpha + Lite 5.3-flash two-window
  drive, then escalated to 24/7 STANDING full-width mesh drive (research or
  builds); self-tending cron automation-b499da5b every 20 min, WANTS.md intake,
  lane fallback past the union window expiry (~09-23), run-lock; commits 2c12eccac
  + 792401158
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Operator orders 2026-09-17, escalating in one session: (1) "are we using union alpha? run it all day full blast on everything our whole mesh"; (2) "we have 10k credits and a parallel line to 5.3 flash, use it — drive 2 windows"; (3) "it needs to be run 24/7 from this point forward, full width on our problems, research or builds."

**The standing engine (commit 792401158):**
- Driver `scripts/union_fullsend_day.py`: routes by lane_hint (union→or-union-alpha, lite→zai-lite, any→parity), reuses mag/research_fanout LANES/_env; three system styles (digger = research, ractor = brutal witness w/ claim-status tables, parable = nameless no-em-dashes); failure-preserving raw.jsonl receipts; 2 attempts then DEAD-with-row; flight-recorder telemetry; DAY_PACK.md regenerated per run; **attempt-2 lane fallback** (_RETRY_ORDER over live free lanes — a dead union window is a lane-swap, not a queue death); **run-lock** (concurrent fires no-op, stale locks self-clear 15 min — added after a manual run overlapped a scheduled fire, verified no double-spend).
- Queue 42 items (UF-01..42) at `watch/inbox/union_fullsend_20260917/queue.jsonl`; `WANTS.md` = operator/any-window intake — the tender converts wants to queue items and marks them QUEUED.
- Cron **automation-b499da5b every 20 min is SELF-TENDING**: when remaining < 12 it appends up to 12 items (priority: fresh WANTS → un-receipted fifty-wide FW tasks as digs/build-drafts → standing veins: WoW/modding/hosting/law research, doctrine stress tests w/ falsifiers, X-radar plays, parable drafts, primary-doc hunts). Tender had to be folded into the drive cron — see [[cron-one-automation-per-session]].
- Law 15 structural on the lite window (1,400 credits/day ceiling, monitor-clamped, LITE_PACED is a row not a crash); builds stay DRAFTS until a coding window promotes by byte check — model text proposes, bytes dispose.
- Verified: batch 1 8/8 union (30-76s, 1.4-2k chars), run 3 → 20/42 done, 0 dead. Union-alpha had been idle since TT3 (09-16 23:57) — always probe before assuming a lane drives. Dead that day: mistral-small (429), or-glm52.
- **Build lane folded into the same cron (STEP 3)**: `scripts/build_lane_game.py --batch 1` — drafts RUINS GO levels and promotes ONLY through the node gate. Operator correction en route: NO max_tokens caps on reasoning models ([[no-token-caps-100k-windows]]). Cancelled foreground runs leave stale locks that self-clear in 15 min — LOCKED replies are normal, not failures. Loop proven end-to-end: one glm draft ("P01 Paid Passage") reached the gate and was honestly REJECTED (`exhausted @2`, sealed player) with the row preserved — first PROMOTION still owed.
- **Later operator corrections (same day, evening)**: "we have multiple keys on open router use them" → build lane rotates OPENROUTER_API_KEY_2 → OPENROUTER_API_KEY on 429/401/402; "i know what ox is thats an old config. we're using union" → model chain = sticky → stealth/union-alpha → glm-5.3-flash, env OPENROUTER_MODEL ignored ([[ox-alpha-was-glm53-flash]]). Sticky state model pinned to union-alpha.
- Tender behavior: it only appends when remaining < 12 (a fire with remaining 22 skips tendering); the `lcg-bones-mine` WANTS entry (Assembly-CSharp.dll + resources.assets extraction from the installed Lara Croft GO Steam dir) converts on the first below-threshold fire.
- **Wave mode + wide lanes (late evening, "underutilizing by orders of magnitude"):** `_wide_lanes(env)` builds lanes dynamically from key presence — groq ×2 keys × 3 models, mistral ×2, OpenRouter ×2 keys × union/ling3/nemotron, cohere free, gemini-flash, together llama-70b free, deepseek (next-to-free), xai grok seat, zai-lite = 18+ lanes; `--all` fires every remaining item across all live lanes, 12 workers; max_tokens removed from the research call() too. **Env gotchas:** the lite key is `ZAI_API_KEY_Lite` (not _L); `CEREBAS_API_KEY` name exists but is EMPTY; `GROK_API_KEY`/`_2` are empty — the grok seats ride `XAI_API_KEY`.
- **STANDBY (operator "stop new flash window", ~23:00Z 09-17):** cron automation-b4995b put report-only (no drivers, no queue appends, resume only on explicit operator word). Frozen state: research 20/42 done 0 dead (22 remaining), build 0 promoted / 8 rejected.
- **Cron context-bleed lesson (why he stopped it):** the automation's own session burned 5.7M tokens across 22 fires — each fire inherits the whole growing conversation (~330k-token tool reads by the end). The drivers and receipts are stateless on disk; when resumed, fires should run from FRESH sessions (read state → batch → one line → die), never an ever-growing cron session. (Operator clarification when resuming: "that wasn't the lesson — 5.3 is fine, we just want 5.3-flash because it's free right now"; the burn itself was never the problem.)
- **RESUMED same night ("gather the orphans, go wide, resume knocking them out" + "keep the burn of the openrouter stealth double max lanes churning 24/7"):** wave run 4 fired ALL 22 orphans across the 18 lanes → 21/22 answered (41/42 done, 0 dead; UF-37's lone HTTP 429 retried next fire). NIM lanes added to _wide_lanes (NVIDIABuild key is LIVE, 70 chars: nim-qwen72b, nim-dsr1, nim-llama33 on integrate.api.nvidia.com). groq key 2 back in rotation after being unused since the 7th (groq-qwen2/groq-oss2/groq-oss202). **Cron restored to LEAN full drive** (batch 16 + build 2, tender <12, "keep this fire LEAN — read only state files, reply one line, do NOT read the full session history") — the stateless-fire lesson is now written into the automation prompt itself.
- Lite window usage answered from bytes: zai-lite WAS in the wave rotation (4 rows ok, law-15 paced) but had no dedicated build window — a --lane lite mode for build_lane_game.py (separate state dir build_lane_lite, _LANES_LITE on ZAI_API_KEY_Lite with lite_guard pacing, ALLOWED_HOSTS + api.z.ai) was half-wired when the operator pivoted to the dogfood self-steal; finish it before relying on it ([[dogfood-canonical-machinery-20260917]] — the cleaner path is chat_provider("z_ai3")).

- **FINAL STATE 2026-09-17 night (commits 76745e0f5 + 7e57a57c8):** research battery 42/42
  COMPLETE, 0 dead. Build lane 4 promoted / 8 rejected — every promotion on GENERATION ONE
  (see [[ruins-go-shipped-20260917]]). Cron automation-b499da5b running LEAN full drive
  (batch 16 + build 2, tender <12, one-line replies, state files only). Two git-notes:
  configs/providers.yaml is gitignored (key references — on-disk fixes still count, the
  z_ai3 endpoint-law fix lives there); a git add glob that matches nothing silently
  no-ops and the commit dies "no changes added" — stage exact paths.
- **Queue re-tendered same night (first post-completion fire):** +12 items UF-43..54 (queue
  54): the lcg-bones-mine want converted first (Unity dll decompile toolchain, assets
  extraction, RE legality), plus librarian-citation falsifier test, imprint freshness law,
  GHOST_HANDLE 7-day watch protocol (3 hypotheses + signals), BenchLM/Kimi-optimizer
  verification digs, Eluna security surface, Looking-Glass chess PD texts, the-librarian
  parable draft, and 3 substantive tide-amendment candidates. Tender math confirmed: a
  drained queue triggers immediate wants-first refill; batch 16 + build 2 fired background.

- **LATE-NIGHT STATE (post-tender waves, queue 54):** research 53/54 done 0 dead (UF-54
  HTTP 400 lone orphan; tender tops up next fire). Build 6 promoted / 8 rejected — the last
  two the FIRST GEN-2 passes ("The Queen of Venom" 15 moves, "The Unstamped Seal" 9 moves:
  failed gen 1, read the verdict, fixed themselves — see [[ruins-go-shipped-20260917]]).

- **"You're not even trying" correction (latest):** operator dropped omp.sh + can1357/oh-my-pi +
  two OpenRouter screenshots — the STEALTH page shows Union+Ox windows did 6T tokens/day
  industry-wide Aug 20-25 and a NEW window opened Sep 14 (both stealth models live again);
  his own Activity page names the proven models my lane set lacked (Kimi K2.6 11.6M tok,
  Ox Alpha 8.03M, DeepSeek V4 Flash 3.19M, Gemini 3.7 Flash, Dots3-Note, North Mini Code).
  Wired all six × both keys → **35 lanes** (18 OpenRouter). My Union Alpha usage was 155K of
  a 6T/day window — the dribble metric to never repeat. Queue re-tendered to 66 (UF-66:
  graph build-candidate specs, UnityPy recipes, amendment candidates, parables). See
  [[operator-usage-as-probe]] and [[omp-oh-my-pi-steal]].

- **RUN 8 — RESEARCH BATTERY 66/66 COMPLETE, 0 dead** (35-lane set incl. the stealth/Kimi/
  DeepSeek rotation, zero failures on the new lanes). Build lane LOCKED that fire (in-flight
  holder). Cron tender math holding: drained queues trigger wants-first refill immediately.

- **MODEL LAW + SCHEDULE LAW (operator fury at a cron silent-downgrade, commits 41cf9ead8 +
  c2d00eb5c):** the cron probe once treated a transient union-alpha failure as permanent and
  stuck the lane to glm-5.3 — "why was the model switched to 5.3 again, its the fucking cron
  job... fix it and make sure this doesnt happen again." Fix in build_lane_game.py: probe
  retries the primary twice; fallback serves THIS RUN ONLY; the only value ever persisted to
  state["model"] is stealth/union-alpha. PLUS the schedule: after 11:00 local, union + glm
  rotate as SCHEDULED CO-PRIMALS (both free windows burn together); before 11:00, law-15
  pacing. Transport-victim revival: the dead-prune now RESETS the attempt counter for
  transport deaths (200-error-body had burned P-sentry-weave + P-scale-finale's real
  attempts). See [[lite-free-window-schedule]].
- **Agora filed (elvis/omarsar0 drop, arXiv 2609.18094):** NVIDIA's Git-as-shared-memory
  collective auto-research — 13 workers, no planner, 1,703 commits, 141-donor hybrid model
  with no gradients, 165/165 reproductions = the mycelial republic externally validated.
  Crosswalk battery UF-84..92 tendered (Agora deep-dive, fleet crosswalk, no-planner lit,
  stealth-window watch protocol, websocket relay patterns, twin-boss spec, amendment-one
  final draft, EM physics-canon gap).

- **FINAL STANDING STATE (night 09-17):** research **92/92 COMPLETE, zero dead** across the
  entire 3-battery arc (outward 66 + inward UF-67..80 + verify/frontier UF-81..92) — run 14
  swept the last two transport orphans on retry, proving the two-attempt law end-to-end.
  Build 6 promoted / 8 rejected (2 gen-2 self-corrections). Cron keeps spinning: next fires
  carry the revived briefs and the fresh tender.
- **STALE-LOCK STARVATION + X receipts (latest fire, run 14 → 92/92):** the build lane sat
  idle 27 min because a stale lock guarded it — drivers IGNORE locks past the 900s threshold
  but nothing RE-FIRED on expiry; fixed by hand (rm stale lock + relaunch), banked fix: the
  driver should self-clear expired locks. UF-84..92 answered: amendment-one draft (picked
  transport-deaths-never-count), twin-boss spec (lane did a ractor presupposition check —
  good instinct, unusable grid), stealth-watch REFUSED by a lane ("can't help with that" —
  reframe needed). Agora (arXiv 2609.18094) filed: NVIDIA's Git-as-shared-memory collective
  (13 workers, no planner, 1,703 commits, 141-donor hybrid, 165/165 reproductions) = the
  mycelial republic externally validated. Tender +6: UF-93..98 (Isfahan lock sourcing,
  glm context ceiling, solver-in-loop generation, AI Director lineage, Mono decompiler
  recipe, windows-into-memory law). Mimosa splits compound Bash that heredocs JSON AND runs
  .py drivers in one call — split tender from fire.
- **GAP ANALYSIS + inward battery (operator: "do a gap analysis... our game, our history,
  our training, our memories, our tech, our frontier. EVERYTHING. SELF STEAL")** — see
  [[gap-analysis-inward-battery-20260917]]. UF-67..80 appended (queue 80). One driver lesson
  banked: append JSONL via a python json.dumps writer, never shell heredocs (a mangled tail
  required truncation-to-valid + clean re-append; history preserved byte-for-byte).
  Run 9: 9/14 answered (75/80 done), 5 transport failures (429/404/400) retained as rows
  for the retry pass.

- **TRUE FINAL (run 16, night close):** research **98/98 COMPLETE, zero dead** — run 15
  answered 3/6 of the fresh tender (UF-93 Isfahan, UF-95 solver-gen, UF-96 AI-director hit
  429/empty transport, retried), run 16 swept all three orphans clean, proving amendment
  001's transport-retry law end-to-end on its first night. Queue drained again → next fire
  tenders fresh (standing veins + any new WANTS). "Nexty" conversion done between fires:
  amendment 001 filed, twin-boss hand design gate-rejected, pack restored (see
  [[ruins-go-shipped-20260917]]).

- **STALE-LOCK LAUNCH GAP ("come on why aren't you launching"):** the build lane sat idle
  because its stale lock expired the 900s guard but nothing RE-FIRED on expiry — drivers
  ignore expired locks, so the lane waited for a hand. Fix banked: clear + relaunch by
  hand, and the driver should self-clear expired locks. Also fixed the same window: the
  200-error-body pattern (OpenRouter 200 + error JSON, no `choices`) now ROTATES KEYS in
  build_lane_game.py like a 429 — previously only HTTPError codes rotated, so stealth-lane
  200-bodies burned attempts.
- **SELF-STEAL ADDENDUM (operator "self steal" on the enhancement order):** the gap scan
  itself needed one — "swarm ZERO" was true of the research tape and FALSE of the fleet:
  the ox desk's **U8_UNION_TECH_INTEL.md** had already measured union-alpha (256K context,
  128K max output, vision-capable, 24-concurrent with zero 429s — limit is LATENCY not
  rejection; key free_tier:false so :free gates don't bind; no implicit cache; extra keys
  don't help, capacity is global), and **SWARM_LENS_PROTOCOL.md** already laws the 6-gate
  verification cycle. Wired: driver concurrency 12 → 16 per U8; SWARM_LENS adopted as the
  annotation gate; new standing law — **grep the estate before any battery fires; our
  shelves are the first lane** (commit a260a5d78).
- **RACTOR SALON → 5-ENHANCEMENT PLAN (union on 256K, full gap analysis + graph in
  context):** (1) librarian --coldload = estate-index slices + imprint through the 256K
  window [SHIPPED, see [[the-librarian-fleet-imprint-20260917]]]; (2) latency-knee
  controller — sweep 8→24 workers, find where p95 bends, falsifier: 16→24 <10% gain = pin
  16; (3) SWARM_LENS attack-passes on OUTPUTS not just annotations (start: the 18 ruins_go
  levels), falsifier <1 catch/10 artifacts = ceremony; (4) ground mycelium edges to real
  estate paths (resolve_edges.py), falsifier >30% unresolvable = rebuild from
  flight-recorder co-access; (5) lineage manifest fields (PARENT + STOLEN_ORGAN) on every
  build, falsifier: no correlation with ramp movement after 10 builds = narrative. All
  wiring-not-invention — every mechanism cited from the estate.

- **NIGHT-CLOSE FIRES (runs 15-16, post-salon):** run 15 answered 3/6 fresh tender
  (UF-93/95/96 transport: 429×2 + empty_content), run 16 swept all three → **research 98/98
  COMPLETE, zero dead** across the whole day's arc. Build lane's revived briefs
  (P-sentry-weave, P-scale-finale) hit the 200-error-body pattern AGAIN — the key-rotation
  hole closed (200-bodies now rotate keys like a 429 in build_lane_game.py; previously only
  HTTPError codes rotated, commit in the 200-body-fix), both briefs refired under dual-
  primary. Salon specs UF-99..104 tendered (Sep-20 proof inventory, stranger's 30-min
  falsifier demo script, difficulty-curve formulas, latency-knee/estate-grounding/
  lens-gates plans). Note: SWARM_LENS's own law almost bit us — a research lane REFUSED the
  stealth-watch prompt ("can't help with that"); reframe before requeueing watch-style asks.

- **FINAL DROPS (operator, night close):** two X filings — (1) Giannou "Looped Transformers
  as Programmable Computers" (arXiv 2301.13196, via @hooshaaii): feed output back + programmable
  weights = Turing-complete; completes the night's looped-recurrent TRIANGLE (our evolution
  loop at inference, Helbling flow-recurrent at training, Giannou at architecture) — UF-105
  crosswalks all three into the ractor spec (Laplacian graph + iterative diffusion + threshold
  verdicts IS a looped shape; no-BPTT = the zero-training-budget property). (2) the OPERATOR'S
  OWN April 12 parable (status 2043392641505574915): hidden-garden MIRRORS — one event into
  the shared well, mirrors each reflecting a different truth (dragons vs windmills), fractured
  certainty as harvestable nectar = the Rashomon mechanism published as spec BEFORE the events;
  filed T1, UF-106 formalizes the register entry + demands its forward testable claim. Run 17:
  6/6 answered instantly → 104/106 done, last two in flight. Cron fires continue on the
  heartbeat; queue self-tenders when drained.

- **ABSOLUTE FINAL (run 18, night close):** research **106/106 COMPLETE, zero dead** across
  the full day arc. Build lane: the last two revived briefs BOTH PROMOTED ON GENERATION ONE
  under the post-11:00 dual-primary rotation — "ch2-the-mirror-sentries the mirror sentries ·
  9 moves" (P-sentry-weave) and "ch4-scale-weight-and-shadow the scale: weight and shadow ·
  8 moves" (P-scale-finale, named for the operator's parable, bred by glm-5.3-flash's
  first two promotions). Final scoreboard: **8 promoted / 12 rejected; the tomb is 20
  levels** (12 hand-designed + 8 model-bred, two of them gen-2 self-corrections). Every one
  of the original ten briefs now promoted or died on merit with receipts.

- **POST-MIDNIGHT CONTINUATION (runs 19-21 + tender waves, queue to 113):** the drive kept
  converting operator X-drops into ledger rows + falsifiable queue items same-hour: DATPO
  entropy-forked branching (rollout-stagnation crosswalk), Agora donor-assembly, ART
  rank-then-reward steal (UF-107), top-50 unsolved ciphers as a swarm target (UF-108),
  gate-hack degeneracy probe (UF-109, after Goodfire), autoencoder-imprint mapping (UF-110),
  Sep-20 proof inventory + stranger demo script (UF-111/112), twin-boss v2 with ractor
  constraints (UF-113). Research stands 111/113 done 0 dead (UF-111 429 + UF-113
  empty_content retained per amendment 001). Build lane: 14 promoted / 13 rejected,
  decoration 9-for-9 (D-L06 refire landed), briefs exhausted → boss tier seeds from
  UF-113. **Wheel-churn pattern proven sustainable:** drops → LINKS rows + queue items →
  answers → promotion/conversion, all on the 20-min heartbeat with lean fires.

- **NIGHT-CLOSE (runs 22-23):** research **113/113 COMPLETE, zero dead** — run 22 swept
  UF-111 (Sep-20 proof inventory: trajectory spine / referee chain / games / librarian /
  drive receipts, each EXISTS/MISSING/PARTIAL with paths) and UF-113 (twin-boss v2 spec
  honoring the ractor disputes: twin parks on the ONLY plate before the collapse-ring
  descent) on retry per amendment 001. Build briefs EXHAUSTED at 14 promoted / 13
  merit-rejected (decoration tier closed 9-for-9); boss tier seeds from UF-113's spec
  into briefs.json on the next main-window pass. Wing Chun/Monroe/Jobs operating lenses
  filed and active (see [[wing-chun-operating-lenses]]) — rolling contact, folding
  corrections same-session, falsifier: 3 un-folded corrections voids the lens set.
- **TRUE NIGHT CLOSE (post-lens fires):** both queues drained at handoff — research
  113/113 QUEUE_EMPTY (refills from standing veins next fire), build 14 promoted / 13
  rejected with the BOSS-twin-v2 brief seeded into briefs.json and fired in background
  (briefs.json array+object boundary bug repaired via split-parse-dedupe — appending a
  bare object after a JSON array silently breaks the driver's parse into QUEUE_EMPTY).
 UF-112's stranger demo script (5 falsifier checks) and UF-113's constrained twin-boss
 grid spec are the Sep-20 + boss-tier seeds on disk. Final-final: **the boss BRED** —
 "the mirror toll" promoted by glm via the rotation law after union hit transport walls
 twice; pack 21 levels ALL PASS, commit eab20cc48 (see
 [[ruins-go-shipped-20260917]]). Also same night: operator asked for reply drafts to
 Lilith Datura's one-geometric-primitive post — 3 candidates delivered in his voice
 (crown: claim + receipt + number, fiber-bundle handshake), drafts only, he posts.
 Research held 113/113 through the boss fires. Related:
 [[wing-chun-operating-lenses]], [[ruins-go-shipped-20260917]].

Related: [[union-alpha-free-window-20260916]], [[lite-key-seat-glm53flash]], [[fifty-wide-board-20260917]], [[no-token-caps-100k-windows]], [[the-librarian-fleet-imprint-20260917]], [[fleet-knowledge-graph-20260917]], [[operator-usage-as-probe]], [[omp-oh-my-pi-steal]], [[gap-analysis-inward-battery-20260917]].
