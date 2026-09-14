# SCOUT — grok CLI headless primer test (2026-09-04 ~02:30Z, via ~/.grok/bin/grok v1.0.13)

VERDICT: the CLI door WORKS headless. The exact command that worked (Git Bash on Windows):

```
~/.grok/bin/grok --always-approve -p "<prompt>" 
```

The TUI launch (`grok --always-approve "prompt"` with no `-p`) also runs the query fine —
auth OK, Grok 4.6 (high), always-approve active, "Worked for 1m35s" — but it opens the
interactive fullscreen TUI and never exits, so it is NOT headless. `-p / --single` is the
door: single-turn, prints response to stdout, exit 0. Help text: "Single-turn prompt.
Prints the response to stdout and exits." One adaptation used (two-strike law honored:
first run was not an error, it was a door-shape mismatch).

## CLI OUTPUT (verbatim, stdout, EXIT_CODE=0)

I'll pull the last week of X posts on local GLM-5.3 on Mac and 50+ concurrent agent swarms, then keep only the densest ones. The first pass already has a few dense hits; I'll tighten the search to tensor-parallel GLM-5.3 on Mac and to actual 50+ concurrent swarm runs.

**GLM-5.3 local on Mac**

- https://x.com/OrcaRouter/status/2093412262400905287 — **@OrcaRouter** — Full 743B GLM-5.3 (not Flash) as native MLX 2-bit (~322GB, ~80% retained): one high-RAM Mac can host a frontier local worker, but the box is the quota.
- https://x.com/pipenetwork/status/2093691186561143118 — **@pipenetwork** — Nine measured MLX builds (215–800GB) plus an mlx-lm bug that corrupted GLM past 2K tokens: long-context local agents are unsafe until that class of decoder bug is gone.
- https://x.com/pa1ar/status/2093470458993668103 — **@pa1ar** — 512GB Mac Studio fits 4-bit flagship at 15–20 tok/s and occupies the machine: local GLM-5.3 is a single-agent seat, not a 50-wide swarm host.

**Agent swarm harnesses, 50+ concurrent**

- https://x.com/0xMentor_/status/2094245294108020995 — **@0xMentor_** — Kimi K3 Agent Swarm claims up to 300 parallel agents collapsing web finds into a 1M-token context graph: the product shape is graph merge, not 300 chat tabs.
- https://x.com/0xfini/status/2095533036469211372 — **@0xfini** — 300 sub-agents, one `AGENTS.md`, three injection traps, zero bait taken: at 50+ concurrent the shared constraint file is the harness, not the model.
- https://x.com/AnnatarXBT/status/2094819006494478475 — **@AnnatarXBT** — 300 agents / 4,000 steps leave a map (nodes + edges) not 300 docs: fleet value is harness + loop + surviving graph, or you just paid for a pile.

## COMPARISON vs web run (watch/scout/GROK_RESEARCH_20260904.md)

- Coverage: MATCHES-OR-BEATS. The web run's topics 3 (swarms 50+) and 4 (GLM-5.3/z.ai news)
  are covered here; the CLI scoped topic 1 tighter (local-on-MAC specifically: quant, MLX,
  tok/s measurements) which is more Rocinante-relevant than the web run's general z.ai news
  angle. Web topics 1 (speculative decoding) and 2 (image-to-3D) were not in the CLI brief.
- URL freshness: 6/6 URLs NEW — zero overlap with the web run's 12 (different posts entirely,
  including in the shared topics). The two runs are complementary, not redundant.
- Quality: CLI returns measured numbers (743B MLX 2-bit ~322GB @ ~80% retention; 4-bit
  15–20 tok/s on 512GB Studio; mlx-lm >2K-token corruption bug) — directly actionable for
  Rocinante sizing. The @0xfini injection-trap post is fleet-relevant (AGENTS.md-as-harness
  is literally our repo-files-are-data law tested at 300 agents).
- Caveat (tri-state): URLs not yet fetch-verified — same trust level as the web run's raw
  output (one web-run ID was previously found truncated by the scout; intake still verifies).

## RUNTIME FACTS

- Binary: ~/.grok/bin/grok, Grok Build 1.0.13 (5e9a58528b76) [stable], model Grok 4.6 (high)
- Auth: pass-through (existing ~/.grok credentials), no login prompt headless
- Latency: first (TUI) run "Worked for 1m35s"; -p run comparable, well under the 300s window
- Status line during TUI run: 1.5K / 500K context — huge headroom for longer briefs
- Related surfaces: `grok export` (transcript as markdown), `grok sessions` (list/restore),
  `--output-format json` for machine-readable stdout, `--prompt-file` for batch briefs —
  all headless-compatible next steps for the primer lane.
