# L05: FLE U1 feasibility on this box (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L05) · **Class:** RECEIPT / feasibility
**Closes:** the "U1 pilot substrate" question from the v6 brief crosswalk.

**Verdict: FEASIBLE on this Windows 11 box with one non-negotiable dependency: Docker Desktop + WSL2. No Factorio game purchase needed in the current 0.4.x version (game only for optional rendering). Python 3.11 venv compatible. First smoke test: 4-8 hours, plan 8.**

## Install shape

- README prerequisites: Docker, Python 3.10+, Factorio 2.0.73+ ONLY for optional rendering. Core runs on a Docker-provisioned headless server via `fle cluster start`.
- Caveat worth an hour: the paper-era FLE required a purchased license (v1.110); the 0.4.x rewrite dropped that requirement but the mechanism by which the Docker image gets the headless binary is undocumented in fetched material. Worst case: free Factorio account, download the Linux64 headless tarball from factorio.com, mount it.
- Deps: gymnasium >=1.3.0, factorio-rcon-py, lupa (Lua bridge), fastapi, docker, psycopg2; extras [eval] [mcp] [agents] [cluster]. `pip install factorio-learning-environment[eval,mcp]`. 0.4.5 restored Python <3.12 compat, so 3.11 is safe. Active maintenance (v0.4.8, 2026-09-04; 1.2K stars).

## API shape (differs from our assumption)

- NOT classic Gym reset/step from the agent's view: CODE SYNTHESIS VIA REPL. The agent emits a Python program (reference agent caps 30 lines), the environment executes it against a 23-27-method Python API, observation = program STDOUT/STDERR with typed exceptions. Under the hood: Python client + Lua server over RCON; RCON is plumbing, not the agent interface.
- Throughput oracle exactly matches the v6 brief's V1 needs: 60-second in-game holdout using Factorio production statistics; targets 16 items/s solids, 250/s fluids; open-play scored via value-weighted Production Score + milestones.

## Session economics (paper Table 3 actuals)

- 128 API calls per lab-play trajectory; ~1.2-1.6M tokens per session. 24 careers x 20 sessions = 480 sessions = ~600-750M tokens: ~$95-120 on a GPT-4o-mini-class lane, or $0 on free lanes/local Ollama via the 0.4.6 `--model-base-url` passthrough (points FLE at Ollama's OpenAI-compatible API; exactly our gate).
- WARNING from the paper's own data: cheap lanes barely solve lab-play (GPT-4o-mini 5.2% success at 128 interactions, Claude 21.9%). If careers require verified throughput gains, weak free lanes produce mostly failed episodes. Budget reality: the experiment wants a mid lane.
- The brief's "45-minute wall-clock" cap is NOT an FLE config (no trace in paper/README/changelog); enforce it in our harness if wanted (trivial). The 128-interaction cap is real in the paper; whether it is a config key in 0.4.x unverified (config JSON 404'd on raw fetch; check after install).

## Windows blockers

Docker Desktop with WSL2 backend required (Linux64 headless in container). Python client fine in Git Bash + 3.11 on Windows. No Windows-hostile surfaces found; expect rough edges (0.4.7 added init-retries for transient env-init failures).

## Effort table to first verified episode

Docker Desktop + WSL2 0.5-1.5h; venv + pip 0.25h; `fle cluster start` (binary provisioning unknowns) 0.5-1.5h; wire basic_agent.py to Ollama via --model-base-url, one lab-play task 1-2h; Windows/RCON/flakiness debug 1-3h. Total 4-8h.

## Debt carried

Eval-config schema in 0.4.8 (locate real config post-install; is interaction cap a key); Docker image's Factorio-binary provenance and any account need; 24-career matrix has no token-budget precedent beyond ~1.3M/session; Ollama concurrency may serialize sessions (model inference is the bottleneck, not the harness; paper measured ~218 ops/sec headless).
