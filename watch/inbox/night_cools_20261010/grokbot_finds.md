# GROKBOT NIGHT MINES 2026-10-10T05:57Z

--- cycle 1/8 05:57Z ---
THEME: weird frontier AI research from the last 48h that almost nobody noticed - one find, why it is cool, link
I'll look for one strange frontier paper from the last 48 hours and commit to the best primary source, not a roundup.The loud drops are the math avalanche and BootLoops. I'm checking the quiet Oct 8–9 papers that actually change how an agent estate runs.**LLM-IDEA: Identifiability-Driven Experimental Agent for Autonomous Discovery of Mechanistic World Models.** Surya Shetty and Ulisses Braga-Neto (Texas A&M / Polara Labs), submitted 8 Oct 2026, 05:01 UTC. A search of digests and posts from the last two days turns up the abstract and nothing else.

An autonomous scientist that plateaus has two different problems, and almost every research agent treats them as one. Shetty and Braga-Neto split them with a deterministic engine that never calls a language model: it reads the rank of the sensitivity matrix of the agent's own proposed model on the agent's own data, names the confounded direction as a vector, and certifies when that direction is a symmetry of every experiment in the current class. The plateau then gets one of three verdicts before another proposer call is spent: the data already suffice (keep searching), one different experiment of the same kind restores rank, or the class is exhausted and the kind of experiment has to change. On the 62 ODEBench systems that have free constants, 60 are identifiable at round zero; the RC circuit is certified exhausted for every initial condition that protocol can run, because its three constants enter only as two combinations and models slid along the null direction agree to \(5 \times 10^{-14}\). Pointed at the public DiscoverPhysics rubrics, the same check finds two worlds whose top explanation grade rewards a distinction no legal experiment can make, and every model that fit the trajectories there still failed the explanation (15 of 15, against 5 of 9 in the identifiable worlds). The live proposer loop is a five-call demonstration, not a powered trial. The instrument worth stealing is the round-zero certificate.

https://arxiv.org/abs/2610.11253

Tonight: pick the one night lane whose last two receipts used the same probe and did not move the score. Before the next paid dispatch, stamp the receipt with the three-way verdict. Name the free knobs the claim depends on and the observables that probe can actually return. If a direction the grade rewards cannot change under any probe this lane is allowed to run, file `exhausted_by_certificate`, name that direction, and switch the instrument class. If rank is deficient on this one run but would rise at a nearby operating point, refuse the certificate and keep searching. That is their regularity check, and it is the difference between a proof and a false stop.

--- cycle 2/8 06:06Z ---
THEME: a wild open-source repo that shipped this week - what it does, why it is underrated, link
One repo, shipped this week, and a concrete use tonight. I'll check the estate's night-mining shape and what's actually new before I commit.**Leviathan v0.2.0** (elstongun/leviathan). The repo was created 2026-10-05, and v0.2.0 shipped 2026-10-09 with a Windows build.

It is a single Apache-2.0 Rust binary that streams JSONL, JSON, CSV, SQLite, or another database CLI's stdout into one SQLite FTS5 file, then returns short cited cards. A group resolves before the match, the rank is BM25 with boosts, and every card says `shown N of M`, so a miss and an empty index stay different facts. The v0.2.0 memory store keeps one claim per key: the next write replaces the old value, a session starts from a short briefing, and `as_of` can still read the history. On the author's synthetic maintenance log the median card is 436 tokens at 1M records, with the relevant row in the top 5 for 99% of 1,200 questions and a 33 ms median on a 2018 desktop. Their own limits file says to treat the accuracy as an upper bound, the tokens as representative of that one grouped shape, and the test as retrieval only, with no model in the loop. The GitHub API tonight showed 716 stars and 2 watchers.

https://github.com/elstongun/leviathan

Tonight, take `leviathan-v0.2.0-x86_64-pc-windows-msvc.zip` from the v0.2.0 release and index `memory\runs\hermes_burn\usage.jsonl` (703 KB on disk) with `--id id --date ts`. Search `A1_steer_antiforgery`. The first row is that id, model `anthropic/claude-opus-5.5`, turn 1, cost `0.388`. Keep the index only if the card cites that row and the cost.

--- cycle 3/8 06:16Z ---
THEME: an X post from the last 3 days with an idea worth stealing for a personal sovereign AI agent - verbatim quote + why
One post from the last three days, one steal. I'll search X for a concrete idea a personal agent estate could use tonight, then commit to the best one.**When doing X, read doc Y.** Moon Robin, 10 Oct 2026, 03:06 UTC.

> My agent memory was ~10K tokens every session, mostly irrelevant.
>
> Now it's a short index of "when doing X, read doc Y" lines.
>
> Big test corpus went from 45,128 to 1,781 tokens at start, both 12-question sets stayed right. Costs more on tiny docs.

The whole startup memory becomes a resident route map, and the note opens only when its trigger hits. The repo's v0.6.0 writeup uses the same figures on a fictional large-note corpus: 45,128 down to 1,781 `o200k_base` tokens, two frozen sets held at 12/12, scored as no accuracy gain, with small notes costing more because you pay the index and then the open. Routes are registered by hand. A coverage check reports orphans and dangling paths. An over-budget read warns and does not drop a route. That is the part worth having. A personal agent keeps one committed map of where the law lives, and the law stays on disk until the task names it.

https://x.com/eithernothingne/status/2108755990128849054

Tonight, write `memory/boot_routes.md` as one line per load-order row in `Agents.md`: `when <trigger>, read <path>`, including `memory/rib/RIB_DRIVING_LADDER_20260928.md` and the rule that `state/LIVE_REPORT.md`, `state/REDBOARD.md`, and `state/START_BRIEF.md` never take the crown. Boot the next seat from that file alone. It passes if every load-order path is one line, each path exists on disk, and the file is under 2,000 tokens. Leave the census paragraph where it is.

--- cycle 4/8 06:25Z ---
THEME: an unexpected cross-domain steal: something from biology/physics/music/old craft that maps onto AI agent design
One committed steal, mapped onto something the estate can actually run tonight. I'll check what this night inbox already holds and hunt a cross-domain source that isn't already in the ribs.Cycle 4 is the cross-domain slot. Stigmergy and slime mold are already in the ribs, so I’m checking a clockmaker’s mechanism against the estate and a primary source before committing.**H4's remontoire.** John Harrison's sea watch, finished in 1759, times its balance from a slender spring sitting between the going train and the verge. The train stays locked. That spring alone drives the escape wheel. Eight pins on the contrate arbor discharge the train every eighth of a minute, 7½ seconds, rewind the spring, and lock again. In the 1767 pamphlet he is plain about what that buys: the part that measures time runs only that eighth of a minute before it is wound, the winding happens at the wheel next to the balance-wheel, and the rest of the work has no more to do with measuring time than the person who winds the watch once a day. He puts the wheels' power over the balance at about one eightieth of the balance-spring's. For a seat, the balance is the judgment beat. Context, credit, the repo, and the night's ambition are the mainspring. Tool faults are friction in the train. A remontoire cuts them off: one short contract, rewound every cycle, is the only force allowed to impulse the reply.

https://archive.org/details/principlesmrhar00unkngoog

Tonight: `opencode_builds.md` cycles 1–3 are the same tooth striking three times, `Your current subscription plan does not yet include access to GLM-5V-Turbo`. Before the next builder cycle, put a 7-line spring in this folder and make it the only ask the builder receives. Wind it from one find already banked in `grokbot_finds.md`. Ask for one new file beside it and one sentence of what ran. Leave the detent locked on the model the plan cannot turn. The four-part contract on this mine (title, paragraph, link, one use) is that spring, already wound.

--- cycle 5/8 06:38Z ---
THEME: a tool, technique or trick for local-first AI that changed this month - what and why it matters
One find, committed. I'll check how this night inbox wants the card filed, then look for a local-first change from this month that the estate can actually use tonight.**Microsoft Execution Containers, learning mode.** Generally available 7 October 2026.

An agent cannot be its own security authority. Logan Iyer's Windows Developer Blog post that day makes the boundary an OS container: the harness declares files, network, and UI, and Windows enforces the declaration on the process, a separate session, WSL, or an experimental microVM. The piece that changed for a home fleet is Windows-only and deny-by-default. Set `processContainer.learningMode` to true and `captureDenials.mode` to `"block"`, and every ungranted access is still denied, then written to `denials.<run-id>.json` as `{resource, resourceType, accessType}`. The file is de-duplicated, capped at 10,000 unique denials and 1,000,000 trace events. `wxc-exec` prints one stderr line with the real path. The native capture path needs the V2 process-security contract. Microsoft's own validation notes build `26657.1002` is rejected and `26663.1000` exposes it. Those are probe points, so a host that returns `backend_unavailable` is the result. The public SDK is `@microsoft/mxc-sdk` (Node), `Microsoft.Mxc.Sdk` (.NET), or `mxc-sdk` (Rust). The repo is https://github.com/microsoft/mxc. The 9 October frontier sweep named the GA and did not run a container.

https://blogs.windows.com/windowsdeveloper/2026/10/07/microsoft-execution-containers-policy-driven-containment-for-ai-agents/

Tonight: from `watch\inbox\night_cools_20261010`, install `@microsoft/mxc-sdk` and spawn one process container. Grant only that directory. Set network egress default to deny, `learningMode` true, and `captureDenials` mode `"block"` with the output path in that directory. The command reads the first line of `grokbot_finds.md`, then attempts `..\..\..\queue\todo.md`. It passes if the denials file has a `file`/`read` row whose resource ends in `queue\todo.md` and no row for `grokbot_finds.md`. On `backend_unavailable`, write that string into the folder and stop. Stay on mode `block`.

--- cycle 6/8 06:49Z ---
THEME: one math or geometry idea (recent or ancient) that would make an AI agent instrument cooler - concrete

**Discourse sheaf Laplacian, with a rate-ratio stall bound.** Vicente Boscá and Robert Ghrist, submitted 30 Jan 2026, revised 18 Mar 2026.

A graph Laplacian gives every seat a numbe**Discourse sheaf Laplacian, with a rate-ratio stall bound.** Vicente Boscá and Robert Ghrist, submitted 30 Jan 2026, revised 18 Mar 2026.

A graph Laplacian gives every seat a number and drives neighbors toward one shared value. A discourse sheaf, from Jakob Hansen and Robert Ghrist (arXiv:2005.12798, 26 May 2020; SIAM Journal on Applied Mathematics 81(5):2033–2060, 2021, DOI 10.1137/20M1341088), puts a private vector space on each seat and a discourse space on each edge. The linear restriction map on an incidence is the part of the private vector that seat actually places on that edge. The coboundary δx is the mismatch of the two expressed vectors. The sheaf Laplacian is L = δᵀδ, and the quadratic form ⟨x, Lx⟩ = ‖δx‖² is the total expressed discord. Diffusion dx/dt = −α L x, α > 0, converges exponentially to the orthogonal projection of the initial state onto H⁰, the globally consistent public assignments (Hansen & Ghrist, Theorem 4.1, restated as Theorem 2.2 in the 2026 paper; ker δ = ker L). Neighbors can stand in harmony on the edge while a coordinate in the kernel of every incident restriction map stays private. Section 8 of the 2020 paper freezes the vectors and evolves the maps, so public concord can be bought by changing what is said. Boscá and Ghrist add directional stubbornness (clamped coordinates force a sheaf Poisson equation on the free ones) and a bound on the stall: when expression maps adapt much faster than beliefs, expressed discord drops while the private vectors barely move, and the bound is in the ratio of those two rates. The instrument is those two scalars side by side. Expressed energy, and the private residual no edge was allowed to see.

https://arxiv.org/abs/2601.22431

Tonight: with the repo venv, two stalks in R², one edge with discourse R¹, both restriction maps `[1, 0]`, private states `(1, 0)` and `(1, 9)`. Print ‖δx‖² and the absolute gap on the second coordinate. Checked this turn: energy `0.0`, residual `9.0`. It passes on a rerun if the energy is under `1e-12` and the residual is `9`. On the next pair of receipts that announce the same verdict, record both numbers. If the expressed energy is at that floor and the residual is above it, stamp the pair `public_concord` and keep the dropped coordinate on the receipt.

Filed as cycle 6 in `grokbot_finds.md`.

--- cycle 7/8 06:59Z ---
THEME: something hilarious or beautiful from AI twitter this week worth banking
I'll look through this week's AI posts and the night inbox so the one find I bank is something the estate can actually use tonight.**PhotoCraft v0.6.0, and the plot twist.**

On 9 October 2026 Wono wrote the line worth keeping: "Tech companies trying to replace people with AI, only for people to start replacing tech companies with AI has gotta be the funniest plot twist of the century." It quotes Miguel Ángel Durán's 6 October post (2.8 million views), which points at [getartcraft.com/apps](https://getartcraft.com/apps): seven creative apps, written from scratch in Rust, with AI in the build. The flagship is [storytold/photocraft](https://github.com/storytold/photocraft), a clean-room Photoshop-shaped editor, Apache-2.0, 37,184 stars on the org page tonight. v0.6.0 was published 10 October 2026 at 02:46 UTC. The README says re-saving keeps the render of 307 of the 309 psd-tools test files. The seam worth stealing is that every action is one command id, and the UI, the CLI, a JSON control channel, and an MCP server all dispatch that same id. Headless MCP is `photocraft-cli mcp` with `--automation-read-root` and `--automation-write-root`. Omit a root and that direction has no file authority. The repos describe themselves as clean-room. A later post that said the apps were decompiled is the wording a community note on that post struck.

https://x.com/wono_strategy/status/2108553838093558111

Tonight: the v0.6.0 `SHA256SUMS.txt` was fetched and checked. It contains `26b8f77af98de72726d90f0b28a0a8ca10ced8e49914454ddeacd12143836ab3  photocraft-0.6.0-windows-x64-portable.zip` and `65ae1ceb6f40b838f8e828ce090b40f43de46cf1db37067c0cae48c32f255d4e  photocraft-cli-0.6.0-macos-universal.zip`, and no Windows `photocraft-cli` asset. Write those two lines into `watch/inbox/night_cools_20261010/photocraft_v060_doors.txt`. It passes if both hashes still match a fresh download of that sums file. Keep the command `photocraft-cli run <file> --cmd <id> --params '<json>' --out <png>` for a host that actually has the CLI. On this Windows machine the published binary tonight is the portable app zip.

--- cycle 8/8 07:10Z ---
THEME: an automation or agent trick from any community (r/selfhosted, HN, discords) that a home sovereign agent fleet should steal
One find, committed. I'll look at what this night inbox already holds, then pull a current community trick worth stealing tonight.**Moadim, the routine that rewrites its own cadence.** Ofek Gabay, Show HN thread 49571537.

A night fleet keeps paying a model on a clock that never looks at the last result. Moadim (https://github.com/moadim-io/daemon) is a local Rust daemon whose unit of work is a git-tracked folder: `routine.toml` plus `prompts/prompt.pure.md`. The schedule is five-field cron in the host's local timezone, run by an in-process scheduler. An empty `machines` list runs nowhere until a host is named. Overlap defaults off, and a second fire while the first tmux session is still alive is written to `skip.log` and dropped. `max_runtime_secs` can only shorten the cron interval. The project's comparison table lists `claude`, `codex`, `hermes`, and `pi` as built-in agents, and the MCP on the same port as the UI is how an agent reads and rewrites its own routine. On the thread Gabay describes the loop he runs: a refactor routine that, when the job finishes, edits itself to a weekly regression check, and on a regression edits itself back to every 30 minutes, file by file. The token budget stays in the prompt. The daemon's job is the cadence. A launch with no `tmux` on `PATH` fails silently, which is why the steal tonight is the folder, not the binary.

https://news.ycombinator.com/item?id=49571537

Tonight: add `watch/inbox/night_cools_20261010/routines/census-drift/` and leave the daemon uninstalled. `routine.toml` gets `schedule = "0 9 * * 1"`, `agent = "hermes"`, `machines = []`, `enabled = false`. `overlap.json` is `{"version":1,"allow_overlapping_runs":false}`. `prompts/prompt.pure.md` ends with Gabay's phase law aimed at the census patrol: read `logs/census_patrol.log`; on a clean daily pass keep `0 9 * * 1`; on `COLLECT-DRIFT` or exit 1, rewrite `schedule` to `0 9 * * *` and make the prompt body the order already in `Agents.md` (a fresh `pytest --collect-only -q`, and name the landings that moved the count). It passes if `machines` is empty, `enabled` is false, and both cron expressions are in the prompt. Nothing fires.

# GROKBOT LOOP COMPLETE 07:12Z
