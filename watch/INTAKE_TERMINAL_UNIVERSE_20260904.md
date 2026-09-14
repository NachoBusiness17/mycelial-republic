# INTAKE — Terminal-Universe (Qwen) via @dair_ai — 2026-09-04

**Source:** https://x.com/dair_ai/status/2095880318146507139 — dair_ai (ML papers newsletter, 131k followers).
**Paper:** "Terminal-Universe: turning agent trajectories into scalable terminal environments" (2609.04148, Qwen team).

## What it claims (tri-state: SUPPORTED-in-digest, Unproven-until-we-read)
- Trajectories accumulate at scale; executable environments are scarce; environments > trajectories for post-training (re-queryable, execution feedback). Supported in digest.
- Method: replay a trajectory's recorded file ops to restore a partial workspace; a completion agent fills missing files/deps. Breadth = mined dependency relations across codebases; depth = single-turn -> multi-round with a user-agent supplying iterative feedback.
- Result: 37.3k task-sufficient envs from public terminal trajectories; SFT of Qwen3.5-27B -> +11.9 Terminal-Bench 2.1, +13.8 EvoCode-Bench v2 MT@4. **Unproven for us** — numbers are author-reported, not measured here.

## Rubric (5 axes, 0-5)
| Axis | Score | Why |
|------|-------|-----|
| FIT | 4 | Steal-shaped: file-replay + completion agent is composition of parts we already run (queue, lanes, swarm). No new vendor. |
| PULL | 4 | Directly feeds the mining arc and the research window; previews the Rocinante question — where do LOCAL training envs come from when we own the substrate. |
| COST | 5 | Read + digest on free lanes; no operator minutes; no keys. |
| WINDOW | 3 | Research window is standing (wall = Sep 20), but current critical path is the 2x-key saturation + windowed builds; this is queue restock, not tonight's wire. |
| NOVELTY | 4 | New surface — no prior watch/ card on env-reconstruction-from-trajectories; adjacent to (not a re-find of) the mining arc's corpus work. |

**Total: 20/25 — BUILD NOW** (borderline: window score keeps it just inside the band; the steal is small and self-contained).

## Verdict: BUILD
Not a fleet organ — a STEAL CARD. The method sentence worth stealing whole: *"the tool-execution history already exposes the structure of the environment it ran in — replay the file ops, let a completion agent fill the gaps."* That is a recipe our mining arc can run on our own accumulated trajectories to grow a verifiable-task corpus on Rocinante day one.

## Routing (LAUNCH law, amendment 5)
Windowed item, so the builder names the lane: file the steal into the mining arc's watch queue as B-item "env_replay_steal" — lane = research window (pastebin card -> free-lane digest against the full arxiv PDF via raw fetch), then a one-bay replay prototype only after the Sep 20 wall clears. No premium tokens beyond the digest judgment pass.

**Room row:** appended to watch/room.jsonl, thread=intake.

## ARXIV RECEIPT (window-fold, same turn)
arXiv 2609.04148 confirmed live: "Terminal-Universe: Turning Agent Trajectories
into Scalable Terminal Environments" (Qwen team, 14 authors, submitted Sep 3
2026). Abstract confirms the method: agent trajectories have accumulated at
scale while executable environments remain scarce — replay recorded file ops,
completion agent fills the gaps.
**The fleet mapping this seals**: room.jsonl + seat session tapes ARE
terminal trajectories — the raw material this paper's method turns into
training environments. The code-agent-data organ + this replay technique =
our own tapes become our own envs. That is the data-engine arc's killer app,
and it needs no CUDA (replay + completion run on the burst lanes; the
resulting envs run anywhere).
Routing stands: free-lane deep digest rides the night shift; replay
prototype gated post-Sep-20 per card.
