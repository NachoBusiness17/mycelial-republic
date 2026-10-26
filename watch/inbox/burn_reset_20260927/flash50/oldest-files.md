# s2-17: the 10 oldest files in the repo, by git log

Date: 2026-09-28. Repo: local_sovereign_agent (Mag Resource Harness), branch mag/run-beta1-factory-build-audi-20260806T231709Z, clean tree.

## The instrument and the tie

Command run (this ask): `git log --diff-filter=A --format="@%ct|%H|%ad" --date=iso --name-only --reverse` piped into `.venv/Scripts/python.exe` which keeps each path's first-add tuple and sorts by (epoch, path).

Result: the root commit `eb07ad62e75d8bbd990510005aa3c583977e5486` ("Mag sovereign agent - clean publish baseline.", 2026-08-04 11:47:25 -0400, verified root via `git rev-list --max-parents=0 HEAD`) added 370 files in one shot (`git show --stat` = "370 files changed, 66434 insertions(+)"; `git ls-tree -r --name-only eb07ad62e | wc -l` = 370). Every tracked file therefore ties at epoch 1785858445. There is no second-oldest timestamp in the history.

Tiebreak used: the root commit's tree order, which is exactly the order `git log --name-only` emits for it. The 10 oldest are the first 10 paths in that emission. This is the honest reading of "oldest by git log" for a single-commit-baseline repo; any other tiebreak (alphabetical, mtime) is documented here as a choice, not a truth. Caveat carried from the f-21 skill census: git first-add can lie after history rewrites (12 of 18 skills had false first-adds), but git log is the instrument this item names.

The 10, in tiebreak order: `.dockerignore`, `.env.example`, `.gitignore`, `AGENTS.md`, `CONSTITUTION.md`, `Dockerfile`, `README.md`, `agents/__init__.py`, `agents/critic.py`, `agents/escalate_grok.py`. All 10 exist on disk today (verified `ls -la`; sizes 347 B to 16,671 B).

Per-file last-touch (`git log -1 --format="%ad %h" -- <path>`): .dockerignore 2026-09-14 d575bc168; .env.example 2026-08-04 eb07ad62e (never touched since); .gitignore 2026-09-27 383fed94f; AGENTS.md 2026-09-27 709e2928a; CONSTITUTION.md 2026-08-04 eb07ad62e (never touched); Dockerfile 2026-08-14 052732ebf; README.md 2026-08-09 de7bb85fe; agents/__init__.py, agents/critic.py, agents/escalate_grok.py all 2026-08-04 eb07ad62e (never touched).

## The 10, one by one

### 1. .dockerignore (1,313 B, 55 lines)

What: Docker build-context exclusion list. Keeps `models/` in the image because it is a python package (models/saelis-31b/ weights excluded separately, .dockerignore:25-28); carries two recorded build-crash lessons as comments: locked pytest dirs break the context send (.dockerignore:32-34, 53-54) and excluding `handoff/` crashed every container subprocess with ModuleNotFoundError (.dockerignore:50-55).

Still referenced: yes, structurally. It is consumed by every `docker build .` of the root Dockerfile: docker-compose.yml:13 and :265 say `build: .`, deploy/k8s/README.md:52 says `docker build -t mag-sovereign:local .`, and mag/docker_ops.py:37,19-21 manages that compose stack (`python -m mag.docker_ops status|probe|up|down`). Doctrine echo at memory/game/SYSTEM_MAP.md:54. Archive: NO, live build plumbing.

### 2. .env.example (347 B)

What: seed template for `.env` provider keys: XAI (+XAI_MODEL=grok-4), OPENROUTER, OPENAI, ANTHROPIC, GROQ, DEEPSEEK, DEEPSEEK_OVERMIND, GEMINI, TOGETHER, VAST. Header: "Copy to .env and fill. Never commit .env."

Encoding: the file is not clean text. Bytes: 346 of 347 are plain ASCII with CRLF, but one byte 0x97 (a C1 control character, the residue of a mangled dash) sits in the VAST comment at offset 299 (`vast.ai (GPU rent \x97 not an LLM provider key)`). That byte is why the Read tool classifies the file as binary and refused it; I read it via `.venv/Scripts/python.exe` byte dump instead.

Still referenced: weakly. `.dockerignore:10` re-includes `!.env.example` into the image context. NO tracked doc or script says "copy .env.example" (git grep "env\.example" hits only the two ignore files plus catalog rows). 

Defect found (proven this ask): .gitignore:22 is `!.env.example# live provider/mesh credentials ...` - the negation is glued to its own comment. Gitignore `#` starts a comment only at line start, so the whole line parses as a negation pattern matching nothing, and line 21 `.env.*` silently ignores `.env.example`. Proof: `touch .env.zzprobe && git check-ignore -v .env.zzprobe` -> matched by `.gitignore:21:.env.*`; `git check-ignore -v --no-index .env.example` -> `.gitignore:21:.env.*  .env.example`, rc 0, i.e. an untracked .env.example WOULD be ignored and the :22 negation never fires. The file survives only because it is already tracked (plain `git check-ignore -v .env.example` rc 1 because tracked files are exempt without --no-index). The same glued line is replicated at .zcodeignore:22, and the :22 comment itself carries mojibake (double-encoded dash bytes c3a2 e282 ac 22). Archive: NO, keep as template; the fix is one line in .gitignore and .zcodeignore (put the comment on its own line), not an archive.

### 3. .gitignore (222 lines, 5,439 B)

What: the repo's exclusion law: secrets never commit (.gitignore:18-24), models/ and weights out (:25-27), runtime state/memory local-only (:28-147), watch surface rules (:141-147, 183-184), android build artifacts (:161-166), the 2026-09-27 never-a-blob set incl. the 1.59GB ESSENTIALS_PACK and the 155MB catalog_fts.sqlite (:213-221, landed in 383fed94f).

Still referenced: yes, inherently, by every git operation on the machine; last modified 2 days ago in the gate-fix window commit 383fed94f which names it directly in its message. Archive: NO, the most live file of the ten (but see the line 22 defect above; line 22 is the one dead rule inside it).

### 4. AGENTS.md (118 lines, 16,671 B)

What: the workspace instruction card every seat loads (it is in my own system context this session): load order, shared artifact boundary, clippy standing reminders, driving ladder law (RIB_DRIVING_LADDER_20260928), fan-out width law, build discipline (ratchet, workflow gate, scenario suite, freshness), command card.

Still referenced: yes, maximally. docs/FRAMEWORK_LOAD.md:23, 73, 249, 267 place it in the load order and point agents at it; tools/census_drift_patrol.py parses its test-census claim line per the B2-215/244/249 carrier laws quoted inside it; last modified 2026-09-27 709e2928a ("CODE AS LAW - the driving ladder enforced"). Archive: NO.

### 5. CONSTITUTION.md (435 B, 15 lines)

What: a pure pointer file: "Binding constitution lives in the product repo: ../mycelial-republic/docs/CONSTITUTION.md" plus the five obligations it must obey (fork equality, T0-T3 tiers, handoff.v1, append-only router audit, no auto-merge mining).

Target verified this ask: `../mycelial-republic/docs/CONSTITUTION.md` EXISTS (8,598 B, mtime Jul 31 17:17), and config.py:309 resolves exactly that path (`home / "Documents" / "projects" / "mycelial-republic" / "docs" / "CONSTITUTION.md"`) with the no-Path.home-at-import guard documented at config.py:300-308. AGENTS.md's Constitution line and docs/FRAMEWORK_LOAD.md route readers through it. Archive: NO. Never modified since root, but it is the pointer the code's own constitution loader and the boot docs depend on; archiving it would strand the pointer.

### 6. Dockerfile (1,030 B, 32 lines)

What: python:3.12-slim-bookworm container cage: MAG_CONTAINER=1, MAG_BIND_HOST=0.0.0.0, ports 8765+8000, healthcheck on /api/v1/health, entrypoint scripts/container/entrypoint.sh (exists on disk, -rwxr-xr-x, 385 B).

Still referenced: yes. docker-compose.yml:13 and :265 `build: .` build from it (compose file mtime Sep 26); deploy/k8s/README.md:52 and docs/BOOT_DOC.md:48 document it; mag/docker_ops.py provides the launch path for that compose stack. Archive: NO. Whether the operator actually rebuilt the image recently is not verifiable from files alone; the wiring is present and the compose file is 2 days old.

### 7. README.md (213 lines, 9,288 B)

What: the human front door: framework load pointers, lane table (L0/L2/L3), FIND-FILE-LOAD doors, dashboard quickstart, run/escalation/product-home cards, multi-model M0, research-pack, sovereign dispatch, provider config. Carries fresh FW-11 fence-owner stamps dated 2026-09-28 inside (README.md:43, 69, 79, 101, 154, 167, 185, 201).

Still referenced: yes, 195 tracked docs/py files mention "README.md" (git grep count this ask, excluding catalog). Archive: NO.

Defect found this ask: the file ends mid-sentence at line 213 - the last line is the bare word "Also" (verified with `tail -5 README.md` and `wc -l` = 213). A truncated closing thought at EOF; likely a lost tail from the 2026-08-09 de7bb85fe edit. Cosmetic but it is the repo's front door.

### 8. agents/__init__.py (23 B)

What: two-line package marker ("# agent nodes package") for the five LangGraph node modules.

Still referenced: yes. graph.py:9-13 imports agents.critic, agents.escalate_grok, agents.executor, agents.planner, agents.wait_human; mag/act.py:186 imports agents.escalate_grok. The package cannot be archived without breaking the graph builder. Archive: NO.

### 9. agents/critic.py (163 lines, 5,827 B)

What: the critic / process-value node: LLM-judged IJL value (valence, intensity, stuck, short_circuit), decision mapping via ijl_core.map_value_to_decision, replan/escalate retry ladder, escalation suppressed without a [priority] tag via mag.lanes.text_has_priority (agents/critic.py:95-109), skill bead write on done (agents/critic.py:122-137).

Still referenced: yes. graph.py:9 import, graph.py:68 `g.add_node("critic", critic_node)`. Zero modifications since root, i.e. it survived 55 days of burn waves untouched. Archive: NO, live node.

### 10. agents/escalate_grok.py (125 lines, 4,697 B)

What: the L2 escalation node: writes a handoff.v1 packet to queue/handoff/ (via handoff.schema.new_handoff/write_handoff, agents/escalate_grok.py:46-69), prefers the local brief over raw chat (:31-44), enforces data-tier constraints in the packet (:60-63), optionally runs the Grok CLI harness headless when MAG_ESCALATE_HARNESS is not 0 (:77-112).

Still referenced: yes. graph.py:10 + graph.py:69, mag/act.py:186 + :197.

Defect found this ask: line 89 says `cwd=ROOT` but ROOT is never imported or defined in the file (grep "ROOT" over the file returns only line 89). The first harness escalation therefore raises NameError inside the try at :82, which the blanket except at :111 swallows into `harness = {"ok": False, "error": "name 'ROOT' is not defined"}` - the node silently degrades to park-only handoff forever, exactly the fallback-branch creep the build discipline forbids. Archive: NO (referenced node), but this defect plus the .gitignore:22 glue and the README:213 truncation are the three real findings of this census.

## Verdict

Archive: 0 of 10. Seven are load-bearing the moment the repo is touched (.gitignore, AGENTS.md, README.md, the agents package trio, .dockerignore, Dockerfile via compose), one is a live code pointer (CONSTITUTION.md to an existing sibling file, resolved by config.py:309), one is a seed template kept alive only by already being tracked (.env.example). Nothing here is dead weight; the age is a property of the 2026-08-04 single-commit baseline, not of neglect - 6 of 10 were never modified after the root commit yet 3 of those 6 are on the live import path of graph.py.

Defects found (all proven by commands in this ask, none fixed here - census only):
1. .gitignore:22 (and .zcodeignore:22): `!.env.example` glued to its comment; the negation never fires; proof: `git check-ignore -v --no-index .env.example` returns `.gitignore:21:.env.*`. Plus mojibake bytes in that comment.
2. agents/escalate_grok.py:89: `cwd=ROOT` with no ROOT import; NameError swallowed by except at :111; harness escalation path can never succeed as written.
3. README.md:213: file ends on the dangling word "Also" (truncated sentence).

Not run / limits: no pytest or gate was in scope for this item. Whether a docker image was recently BUILT from the Dockerfile is not evidenced by files (only the wiring is); I did not run a build. The tiebreak (tree order) is a choice, documented above, because 370 files genuinely tie.

Files: this report is banked byte-identical as watch/inbox/burn_reset_20260927/flash50/oldest-files.md and watch/inbox/burn_reset_20260927/flash50/s2-17.md.
